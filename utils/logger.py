from loguru import logger

logger.add(
    "logs/scraper.log",
    rotation="5 MB",
    level="INFO",
    format="{time} | {level} | {message}"
)

def get_logger():
    return logger
