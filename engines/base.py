"""引擎基类"""

from dataclasses import dataclass, field


@dataclass
class Segment:
    start: float
    end: float
    text: str


@dataclass
class TranscribeResult:
    text: str
    language: str
    segments: list[Segment] = field(default_factory=list)


class BaseEngine:
    """所有转写引擎的基类。"""

    name: str = "base"

    def transcribe(self, audio_path: str, language: str | None = None) -> TranscribeResult:
        raise NotImplementedError
