import os
import sys
from pathlib import Path

from dynaconf import Dynaconf

_BASE_DIR = Path(__file__).parent
_CONFIG_DIR = _BASE_DIR / "conf"
settings_files = [
    _CONFIG_DIR / "settings.toml",
    _CONFIG_DIR / ".secrets.toml",
]


settings = Dynaconf(
    envvar_prefix="KOI",
    settings_files=["./conf/settings.toml"],
    includes=[os.path.join(sys.prefix, "settings.toml")],
)


log_format = (
    "{time:YYYY-MM-DD HH:mm:ss,SSS}:{level: <8}[{thread}:{process}]"
    "({module}:{function}:{line: >3}) - {message}"
)

log_configs = {
    "handlers": [
        {"sink": sys.stdout, "format": log_format, "level": settings.default.log_level},
        {
            "sink": settings.default.log_path,
            "format": log_format,
            "level": settings.default.log_level,
            "retention": "1 week",  # Cleanup after some time
            "colorize": True,  # 开启颜色显示
            "backtrace": True,  # 是否输出整个堆栈，异常向上扩展
            "diagnose": True,  # 堆栈是否打印出变量来更方便debug,可能会有敏感信息被输出
            "enqueue": True,  # 在进入日志文件之前先进行排队，在多进程时有用,
        },
    ]
}


