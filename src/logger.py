"""Logger configuration."""

import structlog
from litestar.logging.config import StructLoggingConfig
from litestar.plugins.structlog import StructlogConfig, StructlogPlugin

config = StructlogConfig(
    StructLoggingConfig(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.format_exc_info,
            structlog.processors.MaybeTimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.dev.ConsoleRenderer(),
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    ),
)

structlog_plugin = StructlogPlugin(config=config)
