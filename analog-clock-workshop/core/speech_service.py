import threading

import pyttsx3


_engine_lock = threading.Lock()


def speak_text(text: str) -> None:
    threading.Thread(target=_run_speech, args=(text,), daemon=True).start()


def _run_speech(text: str) -> None:
    with _engine_lock:
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)

        selected_voice_id = _find_spanish_voice(engine)
        if selected_voice_id is not None:
            engine.setProperty("voice", selected_voice_id)

        engine.say(text)
        engine.runAndWait()
        engine.stop()


def _find_spanish_voice(engine) -> str | None:
    voices = engine.getProperty("voices")

    for voice in voices:
        voice_name = getattr(voice, "name", "").lower()
        voice_id = getattr(voice, "id", "").lower()

        if (
            "spanish" in voice_name
            or "español" in voice_name
            or "spanish" in voice_id
            or "es-" in voice_id
            or "español" in voice_id
        ):
            return voice.id

    return None