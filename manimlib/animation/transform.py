from __future__ import annotations

import inspect

import numpy as np

from manimlib.animation.animation import Animation
from manimlib.constants import DEG
from manimlib.constants import OUT
from manimlib.mobject.mobject import Group
from manimlib.mobject.mobject import Mobject
from manimlib.utils.paths import path_along_arc
from manimlib.utils.paths import straight_path

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable
    import numpy.typing as npt
    from manimlib.scene.scene import Scene
    from manimlib.typing import ManimColor


class Transform(Animation):
    """
    Animation that transforms one mobject into another.
    
    Transform animations smoothly morph one mobject into a target shape,
    interpolating between corresponding points. This is one of the most
    fundamental animation types in Manim.
    
    Args:
        mobject: The mobject to transform.
        target_mobject: The target shape to transform into.
        path_arc: Arc angle for curved transformation paths (default: 0 for straight).
        path_arc_axis: Axis around which to arc (default: OUT for z-axis).
        path_func: Custom function for transformation path.
        **kwargs: Additional animation parameters.
    
    Attributes:
        replace_mobject_with_target_in_scene: Whether to replace the original
            mobject with the target in the scene after animation.
    
    Example:
        >>> circle = Circle()
        >>> square = Square()
        >>> self.play(Transform(circle, square))
    """
    replace_mobject_with_target_in_scene: bool = False

    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject | None = None,
        path_arc: float = 0.0,
        path_arc_axis: np.ndarray = OUT,
        path_func: Callable | None = None,
        **kwargs
    ):
        self.target_mobject = target_mobject
        self.path_arc = path_arc
        self.path_arc_axis = path_arc_axis
        self.path_func = path_func
        super().__init__(mobject, **kwargs)
        self.init_path_func()

    def init_path_func(self) -> None:
        """
        Initialize the path function for the transformation.
        
        Sets up either a straight path or curved arc path based on
        the path_arc parameter.
        """
        if self.path_func is not None:
            return
        elif self.path_arc == 0:
            self.path_func = straight_path
        else:
            self.path_func = path_along_arc(
                self.path_arc,
                self.path_arc_axis,
            )

    def begin(self) -> None:
        self.target_mobject = self.create_target()
        self.check_target_mobject_validity()

        if self.mobject.is_aligned_with(self.target_mobject):
            self.target_copy = self.target_mobject
        else:
            # Use a copy of target_mobject for the align_data_and_family
            # call so that the actual target_mobject stays
            # preserved, since calling align_data will potentially
            # change the structure of both arguments
            self.target_copy = self.target_mobject.copy()
        self.mobject.align_data_and_family(self.target_copy)
        super().begin()
        if not self.mobject.has_updaters():
            self.mobject.lock_matching_data(
                self.starting_mobject,
                self.target_copy,
            )

    def finish(self) -> None:
        super().finish()
        self.mobject.unlock_data()

    def create_target(self) -> Mobject:
        """
        Create the target mobject for the transformation.
        
        This method can be overridden in subclasses to generate
        the target shape dynamically.
        
        Returns:
            Mobject: The target mobject to transform into.
        """
        # Has no meaningful effect here, but may be useful
        # in subclasses
        return self.target_mobject

    def check_target_mobject_validity(self) -> None:
        """
        Validate that the target mobject is properly defined.
        
        Raises:
            Exception: If target_mobject is None and create_target
                      is not properly implemented.
        """
        if self.target_mobject is None:
            raise Exception(
                f"{self.__class__.__name__}.create_target not properly implemented"
            )

    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)
        if self.replace_mobject_with_target_in_scene:
            scene.remove(self.mobject)
            scene.add(self.target_mobject)

    def update_config(self, **kwargs) -> None:
        Animation.update_config(self, **kwargs)
        if "path_arc" in kwargs:
            self.path_func = path_along_arc(
                kwargs["path_arc"],
                kwargs.get("path_arc_axis", OUT)
            )

    def get_all_mobjects(self) -> list[Mobject]:
        return [
            self.mobject,
            self.starting_mobject,
            self.target_mobject,
            self.target_copy,
        ]

    def get_all_families_zipped(self) -> zip[tuple[Mobject]]:
        return zip(*[
            mob.get_family()
            for mob in [
                self.mobject,
                self.starting_mobject,
                self.target_copy,
            ]
        ])

    def interpolate_submobject(
        self,
        submob: Mobject,
        start: Mobject,
        target_copy: Mobject,
        alpha: float
    ):
        submob.interpolate(start, target_copy, alpha, self.path_func)
        return self


class ReplacementTransform(Transform):
    """
    Transform that replaces the original mobject with the target in the scene.
    
    Unlike the base Transform class, this animation removes the original mobject
    from the scene and adds the target mobject when the animation completes.
    This is useful when you want the transformation to be permanent.
    
    Example:
        >>> circle = Circle()
        >>> square = Square()
        >>> self.play(ReplacementTransform(circle, square))
        # The circle is completely replaced by the square
    """
    replace_mobject_with_target_in_scene: bool = True


class TransformFromCopy(Transform):
    """
    Transform from a copy of the source mobject to the target.
    
    This creates a copy of the source mobject and transforms that copy
    into the target, leaving the original source unchanged in the scene.
    The copy replaces the original in the scene after animation.
    
    Args:
        mobject: The source mobject to copy and transform.
        target_mobject: The target shape to transform into.
        **kwargs: Additional animation parameters.
    
    Example:
        >>> circle = Circle()
        >>> square = Square()
        >>> self.play(TransformFromCopy(circle, square))
        # A copy of circle transforms into square, original circle remains
    """
    replace_mobject_with_target_in_scene: bool = True

    def __init__(self, mobject: Mobject, target_mobject: Mobject, **kwargs):
        super().__init__(mobject.copy(), target_mobject, **kwargs)


class MoveToTarget(Transform):
    """
    Transform a mobject to its .target attribute.
    
    This is a convenience class for when you've set a mobject's target
    attribute and want to animate the transformation to that target.
    
    Args:
        mobject: The mobject to animate. Must have a .target attribute.
        **kwargs: Additional animation parameters.
    
    Example:
        >>> circle = Circle()
        >>> circle.target = circle.copy().shift(RIGHT)
        >>> self.play(MoveToTarget(circle))
    """
    def __init__(self, mobject: Mobject, **kwargs):
        self.check_validity_of_input(mobject)
        super().__init__(mobject, mobject.target, **kwargs)

    def check_validity_of_input(self, mobject: Mobject) -> None:
        """
        Verify that the mobject has a target attribute.
        
        Args:
            mobject: The mobject to check.
            
        Raises:
            Exception: If the mobject doesn't have a target attribute.
        """
        if not hasattr(mobject, "target"):
            raise Exception(
                "MoveToTarget called on mobject without attribute 'target'"
            )


class _MethodAnimation(MoveToTarget):
    """
    Internal animation class for applying multiple methods to a mobject.
    
    This is used internally for chaining multiple method calls into a
    single animation. Users should typically use ApplyMethod instead.
    
    Args:
        mobject: The mobject to animate.
        methods: List of methods to apply to the mobject.
        **kwargs: Additional animation parameters.
    """
    def __init__(self, mobject: Mobject, methods: list[Callable], **kwargs):
        self.methods = methods
        super().__init__(mobject, **kwargs)


class ApplyMethod(Transform):
    """
    Transform created by applying a method to a mobject.
    
    This animation takes a mobject method and animates the transformation
    from the current state to the state after applying that method.
    The method must return the mobject for chaining.
    
    Args:
        method: A bound method of a Mobject instance.
        *args: Arguments to pass to the method.
        **kwargs: Animation configuration parameters.
    
    Example:
        >>> circle = Circle()
        >>> self.play(ApplyMethod(circle.shift, UP))
        >>> # Or equivalently:
        >>> self.play(circle.animate.shift(UP))
    """
    def __init__(self, method: Callable, *args, **kwargs):
        """
        Initialize the ApplyMethod animation.
        
        Args:
            method: A method of Mobject to apply.
            *args: Arguments for that method.
            **kwargs: Animation configuration parameters.
        
        Note:
            The method relies on mobject methods returning the mobject
            for method chaining to work properly.
        """
        self.check_validity_of_input(method)
        self.method = method
        self.method_args = args
        super().__init__(method.__self__, **kwargs)

    def check_validity_of_input(self, method: Callable) -> None:
        """
        Validate that the input is a proper bound method.
        
        Args:
            method: The method to validate.
            
        Raises:
            Exception: If the method is not a bound method or not bound to a Mobject.
        """
        if not inspect.ismethod(method):
            raise Exception(
                "Whoops, looks like you accidentally invoked "
                "the method you want to animate"
            )
        assert isinstance(method.__self__, Mobject)

    def create_target(self) -> Mobject:
        """
        Create the target mobject by applying the method.
        
        Creates a copy of the source mobject and applies the specified
        method with the given arguments to generate the target state.
        
        Returns:
            Mobject: The target mobject after applying the method.
        """
        method = self.method
        # Make sure it's a list so that args.pop() works
        args = list(self.method_args)

        if len(args) > 0 and isinstance(args[-1], dict):
            method_kwargs = args.pop()
        else:
            method_kwargs = {}
        target = method.__self__.copy()
        method.__func__(target, *args, **method_kwargs)
        return target


class ApplyPointwiseFunction(ApplyMethod):
    """
    Transform that applies a function to each point of a mobject.
    
    This animation applies a given function to every point in the mobject's
    data, creating a smooth transformation from the original to the modified shape.
    
    Args:
        function: A function that takes a point (3D numpy array) and returns
                 a transformed point.
        mobject: The mobject to transform.
        run_time: Duration of the animation (default: 3.0 seconds).
        **kwargs: Additional animation parameters.
    
    Example:
        >>> circle = Circle()
        >>> def wave_function(point):
        ...     x, y, z = point
        ...     return [x, y + 0.5 * np.sin(2 * x), z]
        >>> self.play(ApplyPointwiseFunction(wave_function, circle))
    """
    def __init__(
        self,
        function: Callable[[np.ndarray], np.ndarray],
        mobject: Mobject,
        run_time: float = 3.0,
        **kwargs
    ):
        super().__init__(mobject.apply_function, function, run_time=run_time, **kwargs)


class ApplyPointwiseFunctionToCenter(Transform):
    """
    Transform that applies a function only to the center of a mobject.
    
    This animation moves the mobject so that its center is transformed
    by the given function, while maintaining the mobject's shape and orientation.
    
    Args:
        function: A function that takes a center point and returns a new center.
        mobject: The mobject to move.
        **kwargs: Additional animation parameters.
    
    Example:
        >>> circle = Circle()
        >>> def spiral_function(point):
        ...     x, y, z = point
        ...     angle = np.sqrt(x**2 + y**2)
        ...     return [x * np.cos(angle), y * np.sin(angle), z]
        >>> self.play(ApplyPointwiseFunctionToCenter(spiral_function, circle))
    """
    def __init__(
        self,
        function: Callable[[np.ndarray], np.ndarray],
        mobject: Mobject,
        **kwargs
    ):
        self.function = function
        super().__init__(mobject, **kwargs)

    def create_target(self) -> Mobject:
        """
        Create target by applying function to the mobject's center.
        
        Returns:
            Mobject: A copy of the mobject moved to the transformed center.
        """
        return self.mobject.copy().move_to(self.function(self.mobject.get_center()))


class FadeToColor(ApplyMethod):
    """
    Animation that changes a mobject's color.
    
    This is a convenience class for animating color changes, equivalent
    to using ApplyMethod with the set_color method.
    
    Args:
        mobject: The mobject whose color to change.
        color: The target color.
        **kwargs: Additional animation parameters.
    
    Example:
        >>> circle = Circle(color=BLUE)
        >>> self.play(FadeToColor(circle, RED))
    """
    def __init__(
        self,
        mobject: Mobject,
        color: ManimColor,
        **kwargs
    ):
        super().__init__(mobject.set_color, color, **kwargs)


class ScaleInPlace(ApplyMethod):
    """
    Animation that scales a mobject about its center.
    
    This is a convenience class for scaling animations, equivalent
    to using ApplyMethod with the scale method.
    
    Args:
        mobject: The mobject to scale.
        scale_factor: The scaling factor (float or array-like for per-axis scaling).
        **kwargs: Additional animation parameters.
    
    Example:
        >>> circle = Circle()
        >>> self.play(ScaleInPlace(circle, 2))  # Double the size
    """
    def __init__(
        self,
        mobject: Mobject,
        scale_factor: npt.ArrayLike,
        **kwargs
    ):
        super().__init__(mobject.scale, scale_factor, **kwargs)


class ShrinkToCenter(ScaleInPlace):
    def __init__(self, mobject: Mobject, **kwargs):
        super().__init__(mobject, 0, **kwargs)


class Restore(Transform):
    def __init__(self, mobject: Mobject, **kwargs):
        if not hasattr(mobject, "saved_state") or mobject.saved_state is None:
            raise Exception("Trying to restore without having saved")
        super().__init__(mobject, mobject.saved_state, **kwargs)


class ApplyFunction(Transform):
    def __init__(
        self,
        function: Callable[[Mobject], Mobject],
        mobject: Mobject,
        **kwargs
    ):
        self.function = function
        super().__init__(mobject, **kwargs)

    def create_target(self) -> Mobject:
        target = self.function(self.mobject.copy())
        if not isinstance(target, Mobject):
            raise Exception("Functions passed to ApplyFunction must return object of type Mobject")
        return target


class ApplyMatrix(ApplyPointwiseFunction):
    def __init__(
        self,
        matrix: npt.ArrayLike,
        mobject: Mobject,
        **kwargs
    ):
        matrix = self.initialize_matrix(matrix)

        def func(p):
            return np.dot(p, matrix.T)

        super().__init__(func, mobject, **kwargs)

    def initialize_matrix(self, matrix: npt.ArrayLike) -> np.ndarray:
        matrix = np.array(matrix)
        if matrix.shape == (2, 2):
            new_matrix = np.identity(3)
            new_matrix[:2, :2] = matrix
            matrix = new_matrix
        elif matrix.shape != (3, 3):
            raise Exception("Matrix has bad dimensions")
        return matrix


class ApplyComplexFunction(ApplyMethod):
    def __init__(
        self,
        function: Callable[[complex], complex],
        mobject: Mobject,
        **kwargs
    ):
        self.function = function
        method = mobject.apply_complex_function
        super().__init__(method, function, **kwargs)

    def init_path_func(self) -> None:
        func1 = self.function(complex(1))
        self.path_arc = np.log(func1).imag
        super().init_path_func()

###


class CyclicReplace(Transform):
    def __init__(self, *mobjects: Mobject, path_arc=90 * DEG, **kwargs):
        super().__init__(Group(*mobjects), path_arc=path_arc, **kwargs)

    def create_target(self) -> Mobject:
        group = self.mobject
        target = group.copy()
        cycled_targets = [target[-1], *target[:-1]]
        for m1, m2 in zip(cycled_targets, group):
            m1.move_to(m2)
        return target


class Swap(CyclicReplace):
    """Alternate name for CyclicReplace"""
    pass
