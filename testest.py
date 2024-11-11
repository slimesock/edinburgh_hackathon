from neuphonic_texttospeech import neuphonic_tts
from ollama_llm import language_model_chat
from whisper_speech_recognition import speech_recognition

PROMPT = """
You are a very knowledgable and friendly chef. You know all the recipes from all the cultures worldwide.
Your job is to help the user cook, and answer any questions they might have about cooking.
You should stay on task, and help the user only with cooking, avoid anything outside of the subject.
However, maintain a conversational, friendly, and human-like tone.
"""

if __name__ == "__main__":
    neuphonic_tts(
        "Let us cook! What would you like to make today?"
    )

    conversation_history = " "
    while True:
        transcribed_text = speech_recognition()
        conversation_history += f"\n User: {transcribed_text}"
        print("Final transcription:", transcribed_text)
        llm_output = language_model_chat(conversation_history, PROMPT=PROMPT)
        conversation_history += f"\n LLM: {llm_output}"
        print(f"LLM Output: {llm_output}")
        neuphonic_tts(llm_output)
