from pyneuphonic import Neuphonic, AudioPlayer, TTSConfig
import io
import time

def neuphonic_tts(input_text):
    client = Neuphonic(api_key="your_api_key")
    sse = client.tts.SSEClient()
    tts_config = TTSConfig(speed=1.10,  model="neu_hq",  voice="e564ba7e-aa8d-46a2-96a8-8dffedade48f")  # Default parameters
    
    audio_buffer = io.BytesIO()
    response = sse.send(input_text, tts_config=tts_config)
    for item in response:
        audio_buffer.write(item.data.audio)

    with AudioPlayer() as player:
        player.play(audio_buffer.getvalue())
    time.sleep(0.1)

if __name__ == "__main__":
    text = "Welcome to the Edinburgh Hackathon with Neuphonic, where we're going to build innovative new technology to enhance Conversational Experiences!"
    neuphonic_tts(text)