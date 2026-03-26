"""Qwen3-ASR 引擎 (mlx-qwen3-asr, Apple Silicon 原生加速)"""

from engines.base import BaseEngine, TranscribeResult, Segment


class Qwen3ASREngine(BaseEngine):
    name = "qwen3-asr"

    def __init__(self):
        from mlx_qwen3_asr import Session
        self.session = Session(model="Qwen/Qwen3-ASR-0.6B")

    def transcribe(self, audio_path: str, language: str | None = None) -> TranscribeResult:
        result = self.session.transcribe(audio_path)

        segments = []
        if hasattr(result, "segments") and result.segments:
            for seg in result.segments:
                segments.append(Segment(
                    start=getattr(seg, "start", 0.0),
                    end=getattr(seg, "end", 0.0),
                    text=getattr(seg, "text", "").strip(),
                ))

        full_text = result.text if hasattr(result, "text") else "\n".join(s.text for s in segments)
        detected_lang = language or "auto"
        return TranscribeResult(text=full_text, language=detected_lang, segments=segments)
