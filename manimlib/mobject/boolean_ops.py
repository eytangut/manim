"""
Boolean operations for combining and manipulating 2D vector objects.

This module provides boolean operations (union, intersection, difference, exclusion)
for VMobjects using the Skia PathOps library. These operations allow for complex
shape creation by combining simpler shapes mathematically.

The implementation is adapted from ManimCommunity/manim and uses the pathops
library for robust geometric computation.
"""

from __future__ import annotations

import numpy as np
import pathops

from manimlib.mobject.types.vectorized_mobject import VMobject


# Boolean operations between 2D mobjects
# Borrowed from https://github.com/ManimCommunity/manim/

def _convert_vmobject_to_skia_path(vmobject: VMobject) -> pathops.Path:
    """
    Convert a VMobject to a Skia path for boolean operations.
    
    Parameters
    ----------
    vmobject : VMobject
        The vector mobject to convert
        
    Returns
    -------
    pathops.Path
        The converted Skia path
    """
    path = pathops.Path()
    for submob in vmobject.family_members_with_points():
        for subpath in submob.get_subpaths():
            quads = vmobject.get_bezier_tuples_from_points(subpath)
            start = subpath[0]
            path.moveTo(*start[:2])
            for p0, p1, p2 in quads:
                path.quadTo(*p1[:2], *p2[:2])
            if vmobject.consider_points_equal(subpath[0], subpath[-1]):
                path.close()
    return path


def _convert_skia_path_to_vmobject(
    path: pathops.Path,
    vmobject: VMobject
) -> VMobject:
    """
    Convert a Skia path back to a VMobject.
    
    Parameters
    ----------
    path : pathops.Path
        The Skia path to convert
    vmobject : VMobject
        The target VMobject to populate
        
    Returns
    -------
    VMobject
        The converted VMobject
    """
    PathVerb = pathops.PathVerb
    current_path_start = np.array([0.0, 0.0, 0.0])
    for path_verb, points in path:
        if path_verb == PathVerb.CLOSE:
            vmobject.add_line_to(current_path_start)
        else:
            points = np.hstack((np.array(points), np.zeros((len(points), 1))))
            if path_verb == PathVerb.MOVE:
                for point in points:
                    current_path_start = point
                    vmobject.start_new_path(point)
            elif path_verb == PathVerb.CUBIC:
                vmobject.add_cubic_bezier_curve_to(*points)
            elif path_verb == PathVerb.LINE:
                vmobject.add_line_to(points[0])
            elif path_verb == PathVerb.QUAD:
                vmobject.add_quadratic_bezier_curve_to(*points)
            else:
                raise Exception(f"Unsupported: {path_verb}")
    return vmobject.reverse_points()


class Union(VMobject):
    """
    Boolean union of multiple vector objects.
    
    Creates a new shape that represents the combined area of all input shapes.
    The result includes all regions that are inside any of the input shapes.
    
    Parameters
    ----------
    *vmobjects : VMobject
        Two or more vector objects to unite
    **kwargs
        Additional arguments passed to parent VMobject class
        
    Examples
    --------
    Create union of two overlapping circles:
    
    >>> circle1 = Circle().shift(LEFT * 0.5)
    >>> circle2 = Circle().shift(RIGHT * 0.5)
    >>> union = Union(circle1, circle2)
    >>> self.add(union)
    """
    def __init__(self, *vmobjects: VMobject, **kwargs):
        if len(vmobjects) < 2:
            raise ValueError("At least 2 mobjects needed for Union.")
        super().__init__(**kwargs)
        outpen = pathops.Path()
        paths = [
            _convert_vmobject_to_skia_path(vmobject)
            for vmobject in vmobjects
        ]
        pathops.union(paths, outpen.getPen())
        _convert_skia_path_to_vmobject(outpen, self)


class Difference(VMobject):
    """
    Boolean difference between two vector objects.
    
    Creates a new shape by subtracting the clip object from the subject object.
    The result includes regions that are inside the subject but outside the clip.
    
    Parameters
    ----------
    subject : VMobject
        The base object to subtract from
    clip : VMobject
        The object to subtract
    **kwargs
        Additional arguments passed to parent VMobject class
        
    Examples
    --------
    Create a circle with a square hole:
    
    >>> circle = Circle(radius=2)
    >>> square = Square(side_length=1)
    >>> difference = Difference(circle, square)
    >>> self.add(difference)
    """
    def __init__(self, subject: VMobject, clip: VMobject, **kwargs):
        super().__init__(**kwargs)
        outpen = pathops.Path()
        pathops.difference(
            [_convert_vmobject_to_skia_path(subject)],
            [_convert_vmobject_to_skia_path(clip)],
            outpen.getPen(),
        )
        _convert_skia_path_to_vmobject(outpen, self)


class Intersection(VMobject):
    """
    Boolean intersection of multiple vector objects.
    
    Creates a new shape that represents only the area common to all input shapes.
    The result includes only regions that are inside every input shape.
    
    Parameters
    ----------
    *vmobjects : VMobject
        Two or more vector objects to intersect
    **kwargs
        Additional arguments passed to parent VMobject class
        
    Examples
    --------
    Create intersection of two overlapping circles:
    
    >>> circle1 = Circle().shift(LEFT * 0.5)
    >>> circle2 = Circle().shift(RIGHT * 0.5)
    >>> intersection = Intersection(circle1, circle2)
    >>> self.add(intersection)
    """
    def __init__(self, *vmobjects: VMobject, **kwargs):
        if len(vmobjects) < 2:
            raise ValueError("At least 2 mobjects needed for Intersection.")
        super().__init__(**kwargs)
        outpen = pathops.Path()
        pathops.intersection(
            [_convert_vmobject_to_skia_path(vmobjects[0])],
            [_convert_vmobject_to_skia_path(vmobjects[1])],
            outpen.getPen(),
        )
        new_outpen = outpen
        for _i in range(2, len(vmobjects)):
            new_outpen = pathops.Path()
            pathops.intersection(
                [outpen],
                [_convert_vmobject_to_skia_path(vmobjects[_i])],
                new_outpen.getPen(),
            )
            outpen = new_outpen
        _convert_skia_path_to_vmobject(outpen, self)


class Exclusion(VMobject):
    """
    Boolean exclusive OR (XOR) of multiple vector objects.
    
    Creates a new shape that represents areas that are inside an odd number
    of the input shapes. This excludes regions of overlap between shapes.
    
    Parameters
    ----------
    *vmobjects : VMobject
        Two or more vector objects for exclusive OR operation
    **kwargs
        Additional arguments passed to parent VMobject class
        
    Examples
    --------
    Create XOR of two overlapping circles (donut-like shape):
    
    >>> circle1 = Circle().shift(LEFT * 0.5)
    >>> circle2 = Circle().shift(RIGHT * 0.5)
    >>> exclusion = Exclusion(circle1, circle2)
    >>> self.add(exclusion)
    """
    def __init__(self, *vmobjects: VMobject, **kwargs):
        if len(vmobjects) < 2:
            raise ValueError("At least 2 mobjects needed for Exclusion.")
        super().__init__(**kwargs)
        outpen = pathops.Path()
        pathops.xor(
            [_convert_vmobject_to_skia_path(vmobjects[0])],
            [_convert_vmobject_to_skia_path(vmobjects[1])],
            outpen.getPen(),
        )
        new_outpen = outpen
        for _i in range(2, len(vmobjects)):
            new_outpen = pathops.Path()
            pathops.xor(
                [outpen],
                [_convert_vmobject_to_skia_path(vmobjects[_i])],
                new_outpen.getPen(),
            )
            outpen = new_outpen
        _convert_skia_path_to_vmobject(outpen, self)
