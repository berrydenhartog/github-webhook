import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "generic": {
            "()": "logging.Formatter",
            "style": "{",
            "fmt": "{asctime}({levelname},{name}): {message}",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
        }
    },
    "handlers": {
        "console": {"formatter": "generic", "class": "logging.StreamHandler", "stream": "ext://sys.stdout"},
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "httpx": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "uvicorn": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "httpcore": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}


def setup_logging(level: str) -> None:
    logging.config.dictConfig(LOGGING_CONFIG)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
