"""
Directory management utilities for organizing Manim assets and outputs.

This module provides functions for getting and managing standard directories
used throughout Manim, including cache, temporary storage, output directories,
and asset storage locations. These functions respect user configuration
settings and provide sensible defaults.
"""

from __future__ import annotations

import os
import tempfile
import appdirs


from manimlib.config import manim_config
from manimlib.config import get_manim_dir
from manimlib.utils.file_ops import guarantee_existence


def get_directories() -> dict[str, str]:
    """
    Get all configured directory paths.
    
    Returns
    -------
    dict[str, str]
        Dictionary mapping directory names to their paths
    """
    return manim_config.directories


def get_cache_dir() -> str:
    """
    Get the cache directory for storing temporary files and computations.
    
    Returns
    -------
    str
        Path to the cache directory
    """
    return get_directories()["cache"] or appdirs.user_cache_dir("manim")


def get_temp_dir() -> str:
    """
    Get the temporary storage directory for intermediate files.
    
    Returns
    -------
    str
        Path to the temporary storage directory
    """
    return get_directories()["temporary_storage"] or tempfile.gettempdir()


def get_downloads_dir() -> str:
    """
    Get the downloads directory for external assets.
    
    Returns
    -------
    str
        Path to the downloads directory
    """
    return get_directories()["downloads"] or appdirs.user_cache_dir("manim_downloads")


def get_output_dir() -> str:
    """
    Get the output directory for rendered videos and images.
    
    Creates the directory if it doesn't exist.
    
    Returns
    -------
    str
        Path to the output directory
    """
    return guarantee_existence(get_directories()["output"])


def get_raster_image_dir() -> str:
    """
    Get the directory for raster image assets (PNG, JPEG, etc.).
    
    Returns
    -------
    str
        Path to the raster images directory
    """
    return get_directories()["raster_images"]


def get_vector_image_dir() -> str:
    """
    Get the directory for vector image assets (SVG, etc.).
    
    Returns
    -------
    str
        Path to the vector images directory
    """
    return get_directories()["vector_images"]


def get_sound_dir() -> str:
    """
    Get the directory for sound and audio assets.
    
    Returns
    -------
    str
        Path to the sounds directory
    """
    return get_directories()["sounds"]


def get_shader_dir() -> str:
    """
    Get the directory containing shader files for rendering.
    
    Returns
    -------
    str
        Path to the shaders directory
    """
    return os.path.join(get_manim_dir(), "manimlib", "shaders")
