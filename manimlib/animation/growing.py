"""
Growing animations that create the appearance of objects expanding from specific points.

This module provides various growing animations that make objects appear to grow
or expand from different locations like centers, edges, or arbitrary points.
All animations inherit from Transform for smooth scaling transitions.
"""

from __future__ import annotations

from manimlib.animation.transform import Transform

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np

    from manimlib.mobject.geometry import Arrow
    from manimlib.mobject.mobject import Mobject
    from manimlib.typing import ManimColor


class GrowFromPoint(Transform):
    """
    Animation that makes an object grow from a specific point.
    
    The object starts as a scaled-down version at the specified point and
    grows to its normal size and position. Useful for dramatic entrances
    or drawing attention to specific locations.
    
    Parameters
    ----------
    mobject : Mobject
        The object to animate
    point : np.ndarray
        The 3D point to grow from
    point_color : ManimColor, optional
        Color to use at the starting point
    **kwargs
        Additional arguments passed to parent Transform class
        
    Examples
    --------
    Grow a circle from a specific point:
    
    >>> circle = Circle()
    >>> point = np.array([1, 1, 0])
    >>> animation = GrowFromPoint(circle, point)
    """
    def __init__(
        self,
        mobject: Mobject,
        point: np.ndarray,
        point_color: ManimColor = None,
        **kwargs
    ):
        self.point = point
        self.point_color = point_color
        super().__init__(mobject, **kwargs)

    def create_target(self) -> Mobject:
        """Create the target mobject (unchanged copy)."""
        return self.mobject.copy()

    def create_starting_mobject(self) -> Mobject:
        """Create the starting mobject (scaled down at the point)."""
        start = super().create_starting_mobject()
        start.scale(0)
        start.move_to(self.point)
        if self.point_color is not None:
            start.set_color(self.point_color)
        return start


class GrowFromCenter(GrowFromPoint):
    """
    Animation that makes an object grow from its center.
    
    A convenience class that automatically uses the object's center point
    as the growing origin, perfect for symmetric expansion effects.
    
    Parameters
    ----------
    mobject : Mobject
        The object to animate
    **kwargs
        Additional arguments passed to parent GrowFromPoint class
        
    Examples
    --------
    Grow a square from its center:
    
    >>> square = Square()
    >>> animation = GrowFromCenter(square)
    """
    def __init__(self, mobject: Mobject, **kwargs):
        point = mobject.get_center()
        super().__init__(mobject, point, **kwargs)


class GrowFromEdge(GrowFromPoint):
    """
    Animation that makes an object grow from one of its edges.
    
    The object grows from a point on its bounding box determined by the
    specified edge direction vector.
    
    Parameters
    ----------
    mobject : Mobject
        The object to animate
    edge : np.ndarray
        Direction vector indicating which edge to grow from
    **kwargs
        Additional arguments passed to parent GrowFromPoint class
        
    Examples
    --------
    Grow a rectangle from its left edge:
    
    >>> rectangle = Rectangle()
    >>> animation = GrowFromEdge(rectangle, LEFT)
    """
    def __init__(self, mobject: Mobject, edge: np.ndarray, **kwargs):
        point = mobject.get_bounding_box_point(edge)
        super().__init__(mobject, point, **kwargs)


class GrowArrow(GrowFromPoint):
    """
    Animation that makes an arrow grow from its starting point.
    
    A specialized growing animation for arrows that uses the arrow's start
    point as the growing origin, creating a natural drawing effect.
    
    Parameters
    ----------
    arrow : Arrow
        The arrow object to animate
    **kwargs
        Additional arguments passed to parent GrowFromPoint class
        
    Examples
    --------
    Grow an arrow from its starting point:
    
    >>> arrow = Arrow(start=LEFT, end=RIGHT)
    >>> animation = GrowArrow(arrow)
    """
    def __init__(self, arrow: Arrow, **kwargs):
        point = arrow.get_start()
        super().__init__(arrow, point, **kwargs)
