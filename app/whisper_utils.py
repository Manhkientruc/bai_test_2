from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(audio_path: str) -> str:
    segments, _ = model.transcribe(audio_path)

    full_text = ""
    for segment in segments:
        full_text += segment.text.strip() + " "

    return full_text.strip()
