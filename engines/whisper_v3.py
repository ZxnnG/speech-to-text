"""Whisper Large-v3 引擎 (faster-whisper)"""

from engines.base import BaseEngine, TranscribeResult, Segment


class WhisperV3Engine(BaseEngine):
    name = "whisper-v3"

    def __init__(self):
        from faster_whisper import WhisperModel
        self.model = WhisperModel("large-v3", device="auto", compute_type="float32")

    def transcribe(self, audio_path: str, language: str | None = None) -> TranscribeResult:
        segments_iter, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=10,
            best_of=10,
            patience=2.0,
            temperature=0.0,
            condition_on_previous_text=False,
            hallucination_silence_threshold=0.5,
            no_speech_threshold=0.4,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=200, speech_pad_ms=100),
        )

        segments = []
        prev_text = ""
        repeat_count = 0
        for seg in segments_iter:
            text = seg.text.strip()
            if text == prev_text:
                repeat_count += 1
                if repeat_count >= 3:
                    continue
            else:
                repeat_count = 0
            prev_text = text
            segments.append(Segment(start=seg.start, end=seg.end, text=text))

        full_text = "\n".join(s.text for s in segments)
        return TranscribeResult(text=full_text, language=info.language, segments=segments)
