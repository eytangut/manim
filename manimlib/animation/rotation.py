"""
Rotation-based animations for mobjects.

This module provides animations for rotating mobjects around various axes
and pivot points, including continuous rotation and discrete rotation animations.
"""
from __future__ import annotations

from manimlib.animation.animation import Animation
from manimlib.constants import ORIGIN, OUT
from manimlib.constants import PI, TAU
from manimlib.utils.rate_functions import linear
from manimlib.utils.rate_functions import smooth

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np
    from typing import Callable
    from manimlib.mobject.mobject import Mobject


class Rotating(Animation):
    """
    Animation that continuously rotates a mobject around an axis.
    
    This animation rotates a mobject by a specified angle around a given axis,
    optionally around a specific point or edge. Useful for creating spinning
    or orbiting effects.
    
    Args:
        mobject: The mobject to rotate.
        angle: Total angle to rotate in radians (default: TAU for full rotation).
        axis: Axis of rotation as a 3D vector (default: OUT for z-axis).
        about_point: Point to rotate around (default: mobject center).
        about_edge: Edge to rotate around (overrides about_point).
        run_time: Duration of the rotation (default: 5.0).
        rate_func: Rate function for rotation timing (default: linear).
        suspend_mobject_updating: Whether to suspend mobject updates.
        **kwargs: Additional animation parameters.
    
    Example:
        >>> square = Square()
        >>> # Rotate 360 degrees around z-axis
        >>> self.play(Rotating(square, angle=TAU))
        >>> # Rotate around specific point
        >>> self.play(Rotating(square, angle=PI, about_point=ORIGIN))
    """
    def __init__(
        self,
        mobject: Mobject,
        angle: float = TAU,
        axis: np.ndarray = OUT,
        about_point: np.ndarray | None = None,
        about_edge: np.ndarray | None = None,
        run_time: float = 5.0,
        rate_func: Callable[[float], float] = linear,
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        self.angle = angle
        self.axis = axis
        self.about_point = about_point
        self.about_edge = about_edge
        super().__init__(
            mobject,
            run_time=run_time,
            rate_func=rate_func,
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs
        )

    def interpolate_mobject(self, alpha: float) -> None:
        """
        Interpolate the mobject rotation at a given animation progress.
        
        Args:
            alpha: Animation progress from 0 to 1.
        """
        pairs = zip(
            self.mobject.family_members_with_points(),
            self.starting_mobject.family_members_with_points(),
        )
        for sm1, sm2 in pairs:
            for key in sm1.pointlike_data_keys:
                sm1.data[key][:] = sm2.data[key]
        self.mobject.rotate(
            self.rate_func(self.time_spanned_alpha(alpha)) * self.angle,
            axis=self.axis,
            about_point=self.about_point,
            about_edge=self.about_edge,
        )


class Rotate(Rotating):
    """
    Animation that rotates a mobject by a specific angle.
    
    Similar to Rotating but with different defaults optimized for discrete
    rotation animations rather than continuous spinning.
    
    Args:
        mobject: The mobject to rotate.
        angle: Angle to rotate in radians (default: PI for 180 degrees).
        axis: Axis of rotation as a 3D vector (default: OUT for z-axis).
        run_time: Duration of the rotation (default: 1.0).
        rate_func: Rate function for rotation timing (default: smooth).
        about_edge: Edge to rotate around (default: ORIGIN).
        **kwargs: Additional animation parameters.
    
    Example:
        >>> triangle = Triangle()
        >>> # Rotate 90 degrees with smooth easing
        >>> self.play(Rotate(triangle, angle=PI/2))
        >>> # Rotate around left edge
        >>> self.play(Rotate(triangle, angle=PI, about_edge=LEFT))
    """
    def __init__(
        self,
        mobject: Mobject,
        angle: float = PI,
        axis: np.ndarray = OUT,
        run_time: float = 1,
        rate_func: Callable[[float], float] = smooth,
        about_edge: np.ndarray = ORIGIN,
        **kwargs
    ):
        super().__init__(
            mobject, angle, axis,
            run_time=run_time,
            rate_func=rate_func,
            about_edge=about_edge,
            **kwargs
        )
