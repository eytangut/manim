"""
Logging utilities for Manim.

This module provides a configured logger instance for Manim that uses rich formatting
to provide colored and nicely formatted output messages.
"""
import logging

from rich.logging import RichHandler

__all__ = ["log"]


FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.WARNING, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("manimgl")
