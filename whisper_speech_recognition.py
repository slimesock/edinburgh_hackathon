import whisper
import queue
import threading
import torch
import sounddevice as sd
import numpy as np


def speech_recognition():
    model = whisper.load_model("small")  # Use the smallest model for speed
    audio_queue = queue.Queue()
    transcription = []
    end_of_speech = threading.Event()

    def audio_callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        audio_queue.put(indata.copy())

    def process_audio():
        audio_data = []
        while not end_of_speech.is_set():
            try:
                chunk = audio_queue.get(timeout=2.0)                                    # Gets 2 seconds of audio from the audio eueu at a time
                audio_data.extend(chunk[:, 0])                                          # Use only the first channel
                if len(audio_data) >= 16000 * 2:                                        # Process 2 seconds of audio at a time
                    audio_np = np.array(audio_data, dtype=np.float32)
                    if np.abs(audio_np).mean() > 0.0005:                                # Adjust this threshold as needed - signifies audio is coming in
                        audio_tensor = torch.from_numpy(audio_np).float()
                        with torch.no_grad():
                            result = model.transcribe(audio_tensor, verbose=False)      # Send audio data to be transcribed
                        if result['text'].strip() and len(result['text'].strip()) > 5:  
                            transcription.append(result['text'].strip())                
                            if result['text'].strip()[-1] in '.!?':                     # End sentence if the last character of the transcription is a fullstop, exclamation, or a question mark
                                end_of_speech.set()                                     
                    audio_data = audio_data[int(16000 * 1.5):]                          # Keep last 1.5 seconds for context
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in audio processing: {e}")
                end_of_speech.set()
    processing_thread = threading.Thread(target=process_audio, daemon=True)
    processing_thread.start()
    try:
        with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000, dtype='float32'):
            print("Start speaking (the function will end when a full sentence is detected)...")
            end_of_speech.wait()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        end_of_speech.set()  # Ensure the processing thread ends

    processing_thread.join()
    return ' '.join(transcription)


if __name__ == "__main__":
    while True:
        transcription = speech_recognition()
        print(f"Transcription: {transcription}")