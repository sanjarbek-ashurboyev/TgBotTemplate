"""Logging configuration."""

import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level,
        stream=sys.stdout,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # aiogram logs the full body of every polling request; far too noisy at DEBUG.
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
