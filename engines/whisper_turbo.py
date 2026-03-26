"""Whisper Large-v3-Turbo 引擎 (mlx-whisper, Apple Silicon 加速)"""

from engines.base import BaseEngine, TranscribeResult, Segment


class WhisperTurboEngine(BaseEngine):
    name = "whisper-turbo"

    def transcribe(self, audio_path: str, language: str | None = None) -> TranscribeResult:
        import mlx_whisper

        kwargs = {
            "path_or_hf_repo": "mlx-community/whisper-large-v3-turbo",
            "word_timestamps": False,
            "temperature": 0.0,
            "condition_on_previous_text": False,
            "no_speech_threshold": 0.4,
            "compression_ratio_threshold": 2.4,
        }
        if language:
            kwargs["language"] = language

        output = mlx_whisper.transcribe(audio_path, **kwargs)

        segments = []
        prev_text = ""
        repeat_count = 0
        for seg in output.get("segments", []):
            text = seg["text"].strip()
            if text == prev_text:
                repeat_count += 1
                if repeat_count >= 3:
                    continue
            else:
                repeat_count = 0
            prev_text = text
            segments.append(Segment(start=seg["start"], end=seg["end"], text=text))

        detected_lang = output.get("language", language or "unknown")
        full_text = "\n".join(s.text for s in segments)
        return TranscribeResult(text=full_text, language=detected_lang, segments=segments)
