import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from logging_middleware.log import Log


def safe_log(message: str, level: str = "info", stack: str = "backend", package: str = "campus_notifications") -> None:
    try:
        Log(stack, level, package, message)
    except Exception:
        pass