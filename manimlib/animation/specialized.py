"""
Specialized animation effects for unique visual presentations.

This module contains animations designed for specific visual effects and
presentations that don't fit into standard animation categories, such
as broadcast ripple effects and other custom visual patterns.
"""

from __future__ import annotations

from manimlib.animation.composition import LaggedStart
from manimlib.animation.transform import Restore
from manimlib.constants import BLACK, WHITE
from manimlib.mobject.geometry import Circle
from manimlib.mobject.types.vectorized_mobject import VGroup

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from manimlib.typing import ManimColor


class Broadcast(LaggedStart):
    """
    Animation that creates a ripple effect emanating from a focal point.
    
    This animation generates a series of expanding circles that create a
    broadcasting or ripple effect, useful for showing signal propagation,
    emphasis, or wave-like phenomena.
    
    Parameters
    ----------
    focal_point : np.ndarray
        The 3D point from which the ripples emanate
    small_radius : float, optional
        Starting radius of the circles (default: 0.0)
    big_radius : float, optional
        Final radius of the circles (default: 5.0)
    n_circles : int, optional
        Number of ripple circles to create (default: 5)
    start_stroke_width : float, optional
        Initial stroke width of the circles (default: 8.0)
    color : ManimColor, optional
        Color of the ripple circles (default: WHITE)
    run_time : float, optional
        Total duration of the animation (default: 3.0)
    lag_ratio : float, optional
        Delay ratio between successive ripples (default: 0.2)
    remover : bool, optional
        Whether to remove circles after animation (default: True)
    **kwargs
        Additional arguments passed to parent LaggedStart class
        
    Examples
    --------
    Create a broadcast effect at the origin:
    
    >>> broadcast = Broadcast(focal_point=ORIGIN)
    >>> self.play(broadcast)
    
    Create a colored broadcast with custom parameters:
    
    >>> broadcast = Broadcast(
    ...     focal_point=UP + RIGHT,
    ...     color=BLUE,
    ...     n_circles=8,
    ...     big_radius=3.0,
    ...     run_time=2.0
    ... )
    """
    def __init__(
        self,
        focal_point: np.ndarray,
        small_radius: float = 0.0,
        big_radius: float = 5.0,
        n_circles: int = 5,
        start_stroke_width: float = 8.0,
        color: ManimColor = WHITE,
        run_time: float = 3.0,
        lag_ratio: float = 0.2,
        remover: bool = True,
        **kwargs
    ):
        self.focal_point = focal_point
        self.small_radius = small_radius
        self.big_radius = big_radius
        self.n_circles = n_circles
        self.start_stroke_width = start_stroke_width
        self.color = color

        circles = VGroup()
        for x in range(n_circles):
            circle = Circle(
                radius=big_radius,
                stroke_color=BLACK,
                stroke_width=0,
            )
            circle.add_updater(lambda c: c.move_to(focal_point))
            circle.save_state()
            circle.set_width(small_radius * 2)
            circle.set_stroke(color, start_stroke_width)
            circles.add(circle)
        super().__init__(
            *map(Restore, circles),
            run_time=run_time,
            lag_ratio=lag_ratio,
            remover=remover,
            **kwargs
        )
