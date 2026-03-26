# Speech-to-Text

本地语音转文字工具，支持多引擎，完全离线运行，无需云端 API。

## 支持引擎

| 引擎 | 模型 | 速度 | 准确率 | 中文 | 适用场景 |
|------|------|------|--------|------|----------|
| `whisper-turbo` | Whisper large-v3-turbo | ★★★★ | ★★★★ | ★★★ | **默认推荐**，速度与准确率平衡 |
| `qwen3-asr` | Qwen3-ASR 0.6B | ★★★★★ | ★★★★★ | ★★★★★ | 中英双语最优，需 NVIDIA GPU |
| `whisper-v3` | Whisper large-v3 | ★★ | ★★★★★ | ★★★ | 最高准确率，速度较慢 |

> `whisper-turbo` 针对 Apple Silicon (M1/M2/M3/M4) 做了 MLX 原生加速。
>
> **注意：`qwen3-asr` 官方仅支持 NVIDIA GPU (CUDA)，macOS 上需依赖社区第三方适配 (mlx-qwen3-asr)，可能存在兼容性问题，不建议在 macOS 上使用。** 推荐 Linux + NVIDIA GPU 环境运行 Qwen3-ASR。

## 安装

```bash
git clone https://github.com/ZxnnG/speech-to-text.git
cd speech-to-text
python -m venv venv
source venv/bin/activate
```

按需安装引擎依赖：

```bash
# 推荐：Whisper Turbo（Apple Silicon 加速）
pip install mlx-whisper

# Qwen3-ASR（中英双语最优）
pip install mlx-qwen3-asr

# Whisper large-v3（最高准确率，较慢）
pip install faster-whisper

# 或全部安装
pip install mlx-whisper mlx-qwen3-asr faster-whisper
```

## 使用

```bash
# 转写单个文件（默认使用 whisper-turbo）
python transcribe.py audio.wav

# 选择引擎
python transcribe.py audio.wav --engine qwen3-asr
python transcribe.py audio.wav -e whisper-v3

# 批量转写
python transcribe.py *.wav
python transcribe.py file1.wav file2.mp3 file3.flac

# 指定语言（跳过自动检测）
python transcribe.py audio.wav -l zh
python transcribe.py audio.wav -l en

# 指定输出目录
python transcribe.py *.wav -o output/

# 查看所有可用引擎
python transcribe.py --list-engines
```

## 支持的音频格式

mp3, wav, flac, m4a, ogg, webm 等主流格式。

## 输出

转写结果保存为同名 `.txt` 文件（纯文本），控制台同时输出带时间戳的详细结果。

## 模型硬件需求

| 引擎 | 模型大小 | 运行内存 | 最低芯片 | macOS |
|------|----------|----------|----------|-------|
| `whisper-turbo` | 1.6 GB | ~4 GB | M1 | 13+ |
| `qwen3-asr` | 1.9 GB | ~3 GB | NVIDIA GPU (不建议 macOS) | Linux |
| `whisper-v3` | 3.0 GB | ~6 GB | 任意 (CPU) | 任意 |

> 首次运行会自动从 HuggingFace 下载模型，之后会缓存到本地。

## 系统要求

- Python >= 3.10
- macOS — 推荐使用 `whisper-turbo`（MLX 原生加速）或 `whisper-v3`
- `qwen3-asr` 官方仅支持 NVIDIA GPU，macOS 不建议使用
- `whisper-v3` 支持所有平台（macOS / Linux / Windows），无需 GPU

## License

MIT
