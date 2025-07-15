# API Reference

This section provides detailed documentation for Manim's core classes and functions.

## Overview

Manim is organized into several key modules:

- **Scene**: The main container for animations
- **Mobject**: Mathematical objects that can be animated  
- **Animation**: Classes that define how objects change over time
- **Camera**: Controls rendering and viewport
- **Utilities**: Helper functions for math, colors, and operations

## Core Classes

### Scene

```{eval-rst}
.. currentmodule:: manimlib

.. autoclass:: Scene
   :members:
   :undoc-members:
   :show-inheritance:
```

The `Scene` class is the fundamental building block for all Manim animations. It provides:

- **Animation Management**: Methods like `play()`, `add()`, `remove()`
- **Time Control**: `wait()`, animation timing
- **Object Management**: Tracking and organizing mobjects
- **Rendering**: Coordination with camera and output

**Key Methods:**
- `construct()`: Override this method to define your animation
- `play(*animations, **kwargs)`: Execute animations
- `add(*mobjects)`: Add objects to the scene
- `remove(*mobjects)`: Remove objects from the scene
- `wait(duration=1)`: Pause the animation

### Mobject

```{eval-rst}
.. autoclass:: Mobject
   :members:
   :undoc-members:
   :show-inheritance:
```

The `Mobject` (Mathematical Object) class is the base class for all visual elements in Manim.

**Core Properties:**
- Position, rotation, scale
- Color and stroke properties
- Points and anchors for curves
- Transformation history

**Common Subclasses:**
- `VMobject`: Vector-based mathematical objects
- `PMobject`: Point-based objects
- `ImageMobject`: Raster images
- `Group`: Collections of other mobjects

### Animation

```{eval-rst}
.. autoclass:: Animation
   :members:
   :undoc-members:
   :show-inheritance:
```

The `Animation` class defines how objects change over time.

**Key Parameters:**
- `mobject`: The object being animated
- `run_time`: Duration of the animation (default: 1 second)
- `rate_func`: Function controlling animation timing
- `lag_ratio`: For animating multiple objects

## Animation Types

### Creation Animations

```{eval-rst}
.. currentmodule:: manimlib.animation.creation

.. automodule:: manimlib.animation.creation
   :members:
   :undoc-members:
```

**Primary Classes:**
- `Create`: Draw objects as they appear
- `Write`: Write text character by character
- `ShowCreation`: Alternative creation animation
- `Uncreate`: Reverse creation animation

**Usage Examples:**

```python
# Basic creation
circle = Circle()
self.play(Create(circle))

# Text writing
text = Text("Hello World")
self.play(Write(text))

# Custom timing
square = Square()
self.play(Create(square), run_time=3)
```

### Transform Animations

```{eval-rst}
.. currentmodule:: manimlib.animation.transform

.. automodule:: manimlib.animation.transform
   :members:
   :undoc-members:
```

**Primary Classes:**
- `Transform`: Morph one object into another
- `ReplacementTransform`: Replace one object with another
- `TransformFromCopy`: Transform a copy, leaving original
- `ClockwiseTransform`: Specific rotation direction

**Transform Types:**

```python
# Basic transform
circle = Circle()
square = Square()
self.play(Transform(circle, square))

# Replacement transform (cleaner for subsequent animations)
text1 = Text("Before")
text2 = Text("After")
self.play(ReplacementTransform(text1, text2))

# Copy transform
original = Circle()
copy = Circle().shift(RIGHT * 2)
self.play(TransformFromCopy(original, copy))
```

### Movement Animations

```{eval-rst}
.. currentmodule:: manimlib.animation.movement

.. automodule:: manimlib.animation.movement
   :members:
   :undoc-members:
```

**Primary Classes:**
- `MoveToTarget`: Move object to predefined target
- `ApplyMethod`: Apply a method to an object
- `ApplyFunction`: Apply a function to an object

## Mobject Types

### Geometry

```{eval-rst}
.. currentmodule:: manimlib.mobject.geometry

.. automodule:: manimlib.mobject.geometry
   :members:
   :undoc-members:
```

**Shapes:**
- `Circle`: Circular shapes with customizable radius
- `Square`: Square shapes with side length control
- `Rectangle`: Rectangular shapes with width/height
- `Triangle`: Triangular shapes (equilateral by default)
- `Polygon`: Custom polygons from points
- `Line`: Straight lines between points

**Arcs and Curves:**
- `Arc`: Circular arcs with angle control
- `CubicBezier`: Bezier curves from control points
- `ParametricCurve`: Curves from parametric functions

**Examples:**

```python
# Basic shapes
circle = Circle(radius=2, color=BLUE)
square = Square(side_length=3, color=RED, fill_opacity=0.5)
triangle = Triangle(color=GREEN).rotate(PI/6)

# Custom polygon
pentagon = Polygon(
    [-1, 0, 0], [0, 1, 0], [1, 0, 0], [0.5, -1, 0], [-0.5, -1, 0],
    color=YELLOW
)

# Parametric curve
spiral = ParametricCurve(
    lambda t: [t * np.cos(t), t * np.sin(t), 0],
    t_range=[0, 4*PI]
)
```

### Text and LaTeX

```{eval-rst}
.. currentmodule:: manimlib.mobject.svg.tex_mobject

.. automodule:: manimlib.mobject.svg.tex_mobject
   :members:
   :undoc-members:
```

```{eval-rst}
.. currentmodule:: manimlib.mobject.svg.text_mobject

.. automodule:: manimlib.mobject.svg.text_mobject
   :members:
   :undoc-members:
```

**Text Classes:**
- `Text`: Regular text with font control
- `Tex`: LaTeX mathematical expressions
- `MathTex`: Specifically for math expressions
- `TexText`: Mixed text and math

**Text Examples:**

```python
# Regular text
title = Text("My Animation", font="Arial", font_size=48)

# LaTeX math
equation = Tex(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")

# Math-specific
formula = MathTex("E", "=", "mc^2")

# Mixed content
mixed = TexText("The formula ", r"$E = mc^2$", " is famous")
```

## Utilities

### Space Operations

```{eval-rst}
.. currentmodule:: manimlib.utils.space_ops

.. automodule:: manimlib.utils.space_ops
   :members:
   :undoc-members:
```

**Key Functions:**
- `normalize(vect)`: Normalize a vector
- `get_norm(vect)`: Get vector magnitude
- `rotate_vector(vector, angle, axis=OUT)`: Rotate a vector
- `angle_between_vectors(v1, v2)`: Angle between vectors
- `project_along_vector(point, vector)`: Vector projection

**Usage:**

```python
from manimlib.utils.space_ops import *

# Vector operations
v1 = np.array([3, 4, 0])
v1_normalized = normalize(v1)  # [0.6, 0.8, 0]
magnitude = get_norm(v1)       # 5.0

# Rotation
rotated = rotate_vector([1, 0, 0], PI/2)  # [0, 1, 0]
```

### Color Utilities

```{eval-rst}
.. currentmodule:: manimlib.utils.color

.. automodule:: manimlib.utils.color
   :members:
   :undoc-members:
```

**Color Functions:**
- `color_to_rgb(color)`: Convert color to RGB values
- `rgb_to_color(rgb)`: Convert RGB to color
- `invert_color(color)`: Get color inverse
- `interpolate_color(color1, color2, alpha)`: Blend colors

**Predefined Colors:**
- Basic: `RED`, `GREEN`, `BLUE`, `YELLOW`, `WHITE`, `BLACK`
- Extended: `ORANGE`, `PURPLE`, `PINK`, `BROWN`, `GRAY`
- Variations: `LIGHT_GRAY`, `DARK_BLUE`, `DARK_GREEN`

### Rate Functions

Rate functions control the timing and easing of animations:

```{eval-rst}
.. currentmodule:: manimlib.utils.rate_functions

.. automodule:: manimlib.utils.rate_functions
   :members:
   :undoc-members:
```

**Common Rate Functions:**
- `linear`: Constant speed
- `smooth`: Default smooth easing (sigmoid-based)
- `rush_into`: Fast start, slow end
- `rush_from`: Slow start, fast end
- `slow_into`: Very slow start
- `double_smooth`: Extra smooth transitions
- `wiggle`: Oscillating motion
- `there_and_back`: Go to target and return

**Custom Rate Functions:**

```python
def custom_ease(t):
    """Custom quadratic easing"""
    return t * t

def bounce(t):
    """Simple bounce effect"""
    return abs(np.sin(t * PI))

# Usage
self.play(
    Transform(obj1, obj2), 
    rate_func=custom_ease,
    run_time=2
)
```

## Constants

```{eval-rst}
.. currentmodule:: manimlib.constants

.. automodule:: manimlib.constants
   :members:
   :undoc-members:
```

### Mathematical Constants

- `PI`: π (3.14159...)
- `TAU`: 2π (6.28318...)
- `E`: Euler's number (2.71828...)
- `DEGREES`: π/180 (for degree conversion)

### Directional Constants

- `UP`: [0, 1, 0]
- `DOWN`: [0, -1, 0]
- `LEFT`: [-1, 0, 0]
- `RIGHT`: [1, 0, 0]
- `IN`: [0, 0, -1]
- `OUT`: [0, 0, 1]

**Corner Constants:**
- `UL`: UP + LEFT
- `UR`: UP + RIGHT
- `DL`: DOWN + LEFT
- `DR`: DOWN + RIGHT

### Animation Constants

- `DEFAULT_ANIMATION_RUN_TIME`: 1.0
- `DEFAULT_WAIT_TIME`: 1.0
- `FRAME_RATE`: 60

### Camera Constants

- `FRAME_WIDTH`: 14.222222222222221
- `FRAME_HEIGHT`: 8.0
- `PIXEL_WIDTH`: 1920
- `PIXEL_HEIGHT`: 1080

## Advanced Topics

### Custom Animations

Create your own animations by inheriting from `Animation`:

```python
class CustomGrow(Animation):
    def __init__(self, mobject, **kwargs):
        super().__init__(mobject, **kwargs)
        
    def interpolate_mobject(self, alpha):
        # alpha goes from 0 to 1 during animation
        scale_factor = alpha
        self.mobject.scale(scale_factor / getattr(self, 'last_alpha', 0.001))
        self.last_alpha = alpha
```

### Custom Mobjects

Create custom shapes by inheriting from `VMobject`:

```python
class Heart(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_points_as_corners([
            # Define heart shape points
            [0, 0, 0], [1, 1, 0], [2, 0, 0], 
            [1, -2, 0], [0, 0, 0]
        ])
```

### Scene Configuration

Configure scenes with class attributes:

```python
class MyScene(Scene):
    CONFIG = {
        "camera_config": {"background_color": BLACK},
        "frame_rate": 30,
        "run_time": 10,
    }
    
    def construct(self):
        # Your scene code
        pass
```

## Best Practices

### Performance Optimization

1. **Use appropriate quality settings** during development
2. **Limit object complexity** for real-time preview
3. **Remove unused objects** with `self.remove()`
4. **Group related objects** with `VGroup`

### Code Organization

1. **Use meaningful variable names**
2. **Break complex scenes into methods**
3. **Document your custom classes and functions**
4. **Use constants for repeated values**

### Animation Design

1. **Keep animations smooth** with appropriate timing
2. **Use rate functions** for natural motion
3. **Consider the viewer's attention** when timing multiple animations
4. **Test at different quality levels**

## Migration Notes

### From Previous Versions

- `ShowCreation` → `Create`
- `FadeIn`/`FadeOut` → Use with `opacity` parameter
- Configuration changes may require updating imports

### Common Gotchas

1. **Object references**: Transforming objects changes their identity
2. **Animation ordering**: Order matters in `self.play()`
3. **Coordinate system**: Y-axis points up (mathematical convention)
4. **Rate functions**: Apply to entire animation, not individual objects

For more examples and advanced usage, see the [tutorial](../getting_started/tutorial.md) and [troubleshooting guide](../getting_started/troubleshooting.md).