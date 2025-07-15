"""
Disk-based caching utilities for performance optimization.

This module provides caching functionality to store computation results
on disk, reducing the need to recalculate expensive operations. This is
particularly useful for operations like TeX compilation, image processing,
and other time-consuming computations in animation generation.
"""

from __future__ import annotations

import os
from diskcache import Cache
from contextlib import contextmanager
from functools import wraps

from manimlib.utils.directories import get_cache_dir
from manimlib.utils.simple_functions import hash_string

from typing import TYPE_CHECKING, TypeVar, Callable

if TYPE_CHECKING:
    T = TypeVar('T')


CACHE_SIZE = 1e9  # 1 Gig
_cache = Cache(get_cache_dir(), size_limit=CACHE_SIZE)


def cache_on_disk(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to cache function results on disk.
    
    This decorator caches the return value of a function based on its
    arguments, storing the results on disk for future use. Subsequent
    calls with the same arguments will return the cached result instead
    of recomputing.
    
    Parameters
    ----------
    func : Callable[..., T]
        The function to cache
        
    Returns
    -------
    Callable[..., T]
        The wrapped function with caching behavior
        
    Examples
    --------
    Cache an expensive computation:
    
    >>> @cache_on_disk
    ... def expensive_function(n):
    ...     # Some time-consuming calculation
    ...     return sum(i**2 for i in range(n))
    
    >>> result = expensive_function(1000000)  # Computed and cached
    >>> result = expensive_function(1000000)  # Retrieved from cache
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = hash_string(f"{func.__name__}{args}{kwargs}")
        value = _cache.get(key)
        if value is None:
            value = func(*args, **kwargs)
            _cache.set(key, value)
        return value
    return wrapper


def clear_cache():
    """
    Clear all cached data from disk.
    
    This removes all stored cache entries, freeing up disk space but
    requiring future computations to be recalculated.
    
    Examples
    --------
    Clear the cache when memory is needed:
    
    >>> clear_cache()  # All cached results are removed
    """
    _cache.clear()
