"""转写引擎注册表"""

ENGINES = {
    "whisper-v3": {
        "name": "Whisper Large-v3",
        "description": "OpenAI Whisper large-v3 via faster-whisper (最高准确率，速度较慢)",
        "module": "engines.whisper_v3",
        "class": "WhisperV3Engine",
        "install": "pip install faster-whisper",
    },
    "whisper-turbo": {
        "name": "Whisper Large-v3-Turbo",
        "description": "OpenAI Whisper large-v3-turbo via mlx-whisper (快6倍，准确率接近v3)",
        "module": "engines.whisper_turbo",
        "class": "WhisperTurboEngine",
        "install": "pip install mlx-whisper",
    },
    "qwen3-asr": {
        "name": "Qwen3-ASR",
        "description": "通义千问语音模型 via mlx (极快，准确率超越Whisper，中英双优)",
        "module": "engines.qwen3_asr",
        "class": "Qwen3ASREngine",
        "install": "pip install mlx-qwen3-asr",
    },
}

DEFAULT_ENGINE = "whisper-turbo"


def get_engine(engine_name: str):
    """动态加载并返回引擎实例。"""
    import importlib

    if engine_name not in ENGINES:
        raise ValueError(f"未知引擎: {engine_name}，可选: {', '.join(ENGINES.keys())}")

    info = ENGINES[engine_name]
    try:
        module = importlib.import_module(info["module"])
    except ImportError:
        raise ImportError(
            f"引擎 {engine_name} 依赖未安装，请运行:\n  {info['install']}"
        )

    engine_class = getattr(module, info["class"])
    return engine_class()


def list_engines():
    """打印所有可用引擎。"""
    for key, info in ENGINES.items():
        default = " (默认)" if key == DEFAULT_ENGINE else ""
        print(f"  {key:<16} {info['name']}{default}")
        print(f"  {' ' * 16} {info['description']}")
        print(f"  {' ' * 16} 安装: {info['install']}")
        print()
