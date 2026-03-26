#!/usr/bin/env python3
"""语音转文字 CLI 工具 - 支持多引擎本地转写"""

import argparse
import sys
import time
from pathlib import Path

from engines import DEFAULT_ENGINE, ENGINES, get_engine, list_engines


def fmt_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def transcribe_file(engine, audio_path: str, language: str | None, output_dir: str | None):
    """转写单个音频文件。"""
    path = Path(audio_path)
    if not path.exists():
        print(f"  跳过: 文件不存在 - {audio_path}")
        return

    print(f"\n转写中: {path.name}")
    start = time.time()

    result = engine.transcribe(str(path), language=language)

    elapsed = time.time() - start
    print(f"  语言: {result.language}  耗时: {elapsed:.1f}s")

    # 打印带时间戳的转写结果
    if result.segments:
        for seg in result.segments:
            print(f"  [{fmt_time(seg.start)} -> {fmt_time(seg.end)}] {seg.text}")

    # 保存到文件
    if output_dir:
        out_path = Path(output_dir) / path.with_suffix(".txt").name
        out_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        out_path = path.with_suffix(".txt")

    out_path.write_text(result.text, encoding="utf-8")
    print(f"  已保存: {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="语音转文字工具 - 支持 Whisper / Qwen3-ASR 多引擎本地转写",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s audio.wav                          # 默认引擎转写单个文件
  %(prog)s *.wav --engine qwen3-asr           # 用 Qwen3-ASR 批量转写
  %(prog)s audio.wav -e whisper-v3 -l zh      # 用 Whisper v3 指定中文
  %(prog)s *.mp3 -o output/                   # 结果保存到 output 目录
  %(prog)s --list-engines                     # 列出所有可用引擎
        """,
    )
    parser.add_argument("audio", nargs="*", help="音频文件路径（支持多个文件和通配符）")
    parser.add_argument("-e", "--engine", default=DEFAULT_ENGINE,
                        choices=list(ENGINES.keys()),
                        help=f"转写引擎 (默认: {DEFAULT_ENGINE})")
    parser.add_argument("-l", "--language", default=None,
                        help="语言代码，如 zh, en (默认: 自动检测)")
    parser.add_argument("-o", "--output", default=None,
                        help="输出目录 (默认: 与音频文件同目录)")
    parser.add_argument("--list-engines", action="store_true",
                        help="列出所有可用引擎")

    args = parser.parse_args()

    if args.list_engines:
        print("可用引擎:\n")
        list_engines()
        return

    if not args.audio:
        parser.print_help()
        sys.exit(1)

    # 加载引擎
    print(f"加载引擎: {ENGINES[args.engine]['name']} ...")
    try:
        engine = get_engine(args.engine)
    except ImportError as e:
        print(f"\n错误: {e}")
        sys.exit(1)

    # 逐个转写
    total_start = time.time()
    for audio_path in args.audio:
        transcribe_file(engine, audio_path, args.language, args.output)

    total_elapsed = time.time() - total_start
    print(f"\n全部完成! 共 {len(args.audio)} 个文件, 总耗时: {total_elapsed:.1f}s")


if __name__ == "__main__":
    main()
