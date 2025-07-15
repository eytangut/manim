"""
Movement and flow-based animations.

This module contains animations that move and deform mobjects through
continuous transformations, including homotopies, vector field flows,
and complex plane animations.
"""
from __future__ import annotations

from manimlib.animation.animation import Animation
from manimlib.utils.rate_functions import linear

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Sequence

    import numpy as np

    from manimlib.mobject.mobject import Mobject
    from manimlib.mobject.types.vectorized_mobject import VMobject


class Homotopy(Animation):
    """
    Animation that applies a continuous deformation (homotopy) to a mobject.
    
    A homotopy is a continuous transformation that gradually morphs one shape
    into another. This animation takes a function that maps (x, y, z, t) to
    new coordinates (x', y', z') where t represents time.
    
    Args:
        homotopy: Function taking (x, y, z, t) and returning (x', y', z').
        mobject: The mobject to transform.
        run_time: Duration of the animation (default: 3.0).
        **kwargs: Additional animation parameters.
    
    Example:
        >>> def wave_homotopy(x, y, z, t):
        ...     return (x, y + 0.5 * np.sin(x + t), z)
        >>> square = Square()
        >>> self.play(Homotopy(wave_homotopy, square))
    """
    apply_function_config: dict = dict()

    def __init__(
        self,
        homotopy: Callable[[float, float, float, float], Sequence[float]],
        mobject: Mobject,
        run_time: float = 3.0,
        **kwargs
    ):
        self.homotopy = homotopy
        super().__init__(mobject, run_time=run_time, **kwargs)

    def function_at_time_t(self, t: float) -> Callable[[np.ndarray], Sequence[float]]:
        """
        Create a function that applies the homotopy at a specific time.
        
        Args:
            t: Time parameter for the homotopy.
            
        Returns:
            Function that transforms points at time t.
        """
        def result(p):
            return self.homotopy(*p, t)
        return result

    def interpolate_submobject(
        self,
        submob: Mobject,
        start: Mobject,
        alpha: float
    ) -> None:
        """
        Interpolate submobject by applying homotopy transformation.
        
        Args:
            submob: The submobject being animated.
            start: The starting state.
            alpha: Animation progress from 0 to 1.
        """
        submob.match_points(start)
        submob.apply_function(
            self.function_at_time_t(alpha),
            **self.apply_function_config
        )


class SmoothedVectorizedHomotopy(Homotopy):
    """
    Homotopy animation with smooth vectorized transformations.
    
    Similar to Homotopy but applies smoothing to the resulting curves
    for better visual quality with vectorized mobjects.
    """
    apply_function_config: dict = dict(make_smooth=True)


class ComplexHomotopy(Homotopy):
    """
    Homotopy animation using complex number transformations.
    
    Takes a function that operates on complex numbers and time,
    providing an intuitive way to animate in the complex plane.
    
    Args:
        complex_homotopy: Function taking (complex, time) and returning complex.
        mobject: The mobject to transform.
        **kwargs: Additional animation parameters.
    
    Example:
        >>> def spiral(z, t):
        ...     return z * np.exp(1j * t * TAU)
        >>> circle = Circle()
        >>> self.play(ComplexHomotopy(spiral, circle))
    """
    def __init__(
        self,
        complex_homotopy: Callable[[complex, float], complex],
        mobject: Mobject,
        **kwargs
    ):
        def homotopy(x, y, z, t):
            c = complex_homotopy(complex(x, y), t)
            return (c.real, c.imag, z)

        super().__init__(homotopy, mobject, **kwargs)


class PhaseFlow(Animation):
    """
    Animation that follows a vector field (phase flow).
    
    This animation moves points along trajectories defined by a vector field,
    simulating the flow of a dynamical system.
    
    Args:
        function: Vector field function taking position and returning velocity.
        mobject: The mobject to animate.
        virtual_time: Time scale for the flow (default: same as run_time).
        suspend_mobject_updating: Whether to suspend mobject updates.
        rate_func: Rate function for animation timing (default: linear).
        run_time: Duration of the animation (default: 3.0).
        **kwargs: Additional animation parameters.
    
    Example:
        >>> def flow_field(point):
        ...     x, y, z = point
        ...     return np.array([-y, x, 0])  # Circular flow
        >>> dots = VGroup(*[Dot() for _ in range(10)])
        >>> self.play(PhaseFlow(flow_field, dots))
    """
    def __init__(
        self,
        function: Callable[[np.ndarray], np.ndarray],
        mobject: Mobject,
        virtual_time: float | None = None,
        suspend_mobject_updating: bool = False,
        rate_func: Callable[[float], float] = linear,
        run_time: float =3.0,
        **kwargs
    ):
        self.function = function
        self.virtual_time = virtual_time or run_time
        super().__init__(
            mobject,
            rate_func=rate_func,
            run_time=run_time,
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs
        )

    def interpolate_mobject(self, alpha: float) -> None:
        if hasattr(self, "last_alpha"):
            dt = self.virtual_time * (alpha - self.last_alpha)
            self.mobject.apply_function(
                lambda p: p + dt * self.function(p)
            )
        self.last_alpha = alpha


class MoveAlongPath(Animation):
    def __init__(
        self,
        mobject: Mobject,
        path: VMobject,
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        self.path = path
        super().__init__(mobject, suspend_mobject_updating=suspend_mobject_updating, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        point = self.path.quick_point_from_proportion(self.rate_func(alpha))
        self.mobject.move_to(point)
