from loguru import logger
import sys
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logger.remove()
logger.add(sys.stdout, level="INFO", format="<green>{timestamp}</green> <level>{message}</level>")
logger.add("logs/multi_agent_system.log", level="DEBUG", rotation="1 MB", retention="10 days", compression="zip", serialize=True, format= "{time} {level} {message}")

