# Basic Tutorial

This tutorial will guide you through creating your first Manim animation step by step.

## Prerequisites

Before starting, make sure you have:
- Python 3.7+ installed
- Manim installed (`pip install manimgl`)
- A text editor or IDE
- FFmpeg installed (for video rendering)

## Your First Scene

Let's start by creating a simple scene with a circle:

```python
from manimlib import *

class BasicShapes(Scene):
    def construct(self):
        # Create a circle
        circle = Circle(radius=1, color=BLUE)
        
        # Add it to the scene
        self.add(circle)
        
        # Animate the circle appearing
        self.play(Create(circle))
        
        # Wait for a moment
        self.wait(1)
```

### Understanding the Code

Let's break down what each part does:

1. **Import Manim**: The `from manimlib import *` line imports all Manim classes and functions.

2. **Define a Scene**: Every animation is contained in a Scene class that inherits from `Scene`.

3. **The construct method**: This is where you define what happens in your animation.

4. **Create objects**: `Circle()` creates a circle mobject with specified properties.

5. **Add to scene**: `self.add()` places the object in the scene.

6. **Animate**: `self.play()` runs an animation, in this case `Create()` which shows the circle appearing.

7. **Wait**: `self.wait()` pauses the animation.

### Running Your Scene

Save the code above in a file called `basic_scene.py` and run:

```bash
manimgl basic_scene.py BasicShapes
```

This will open a window showing your animation. Add the `-w` flag to save it as a video file:

```bash
manimgl basic_scene.py BasicShapes -w
```

## Working with Multiple Objects

Let's create a more complex scene with multiple objects:

```python
class MultipleObjects(Scene):
    def construct(self):
        # Create multiple shapes
        circle = Circle(radius=1, color=BLUE)
        square = Square(side_length=2, color=RED)
        triangle = Triangle(color=GREEN)
        
        # Position them
        circle.shift(LEFT * 2)
        square.shift(RIGHT * 2)
        triangle.shift(UP * 2)
        
        # Add them all at once
        self.add(circle, square, triangle)
        
        # Animate them appearing
        self.play(
            Create(circle),
            Create(square),
            Create(triangle),
            run_time=2
        )
        
        # Animate them moving
        self.play(
            circle.animate.shift(UP),
            square.animate.rotate(PI/4),
            triangle.animate.scale(0.5),
            run_time=1.5
        )
        
        self.wait()
```

### Key Concepts

- **Positioning**: Use `.shift()`, `.move_to()`, etc. to position objects
- **Multiple animations**: Pass multiple animations to `self.play()` to run them simultaneously
- **Animate property**: Use `.animate` to smoothly transition object properties
- **Run time**: Control animation speed with the `run_time` parameter

## Text and Mathematical Expressions

Manim excels at mathematical text and equations:

```python
class TextExample(Scene):
    def construct(self):
        # Regular text
        title = Text("Manim Tutorial", font_size=48)
        title.to_edge(UP)
        
        # LaTeX equation
        equation = Tex(r"E = mc^2")
        equation.scale(2)
        
        # Add and animate
        self.play(Write(title))
        self.wait(0.5)
        self.play(Write(equation))
        self.wait()
```

### Text Types

- **Text**: For regular text with font control
- **Tex**: For mathematical expressions using LaTeX
- **TexText**: For mixed text and math

## Animation Types

### Creation Animations
- `Create()`: Draw objects as they appear
- `Write()`: Write text character by character
- `ShowCreation()`: Similar to Create but with different timing

### Transform Animations
- `Transform()`: Morph one object into another
- `ReplacementTransform()`: Replace one object with another
- `TransformFromCopy()`: Transform a copy, leaving original

### Movement Animations
- `Move()`: Move objects to new positions
- `Rotate()`: Rotate objects
- `Scale()`: Change object size

## Common Patterns

### Grouping Objects

```python
class GroupExample(Scene):
    def construct(self):
        # Create objects
        circle = Circle(color=BLUE)
        square = Square(color=RED).shift(RIGHT * 2)
        
        # Group them
        group = VGroup(circle, square)
        
        # Animate the entire group
        self.play(Create(group))
        self.play(group.animate.rotate(PI/4))
        self.wait()
```

### Using Coordinate Systems

```python
class CoordinateExample(Scene):
    def construct(self):
        # Coordinate constants
        # UP, DOWN, LEFT, RIGHT
        # UL (up-left), UR (up-right), DL (down-left), DR (down-right)
        
        dot = Dot(color=YELLOW)
        
        # Move to specific coordinates
        self.play(dot.animate.move_to(UP * 2 + RIGHT * 3))
        
        # Move relative to current position
        self.play(dot.animate.shift(DOWN + LEFT))
        
        self.wait()
```

## Best Practices

1. **Start Simple**: Begin with basic shapes and gradually add complexity
2. **Use Comments**: Document your code for clarity
3. **Test Frequently**: Run your scenes often to catch issues early
4. **Organize Code**: Keep related objects and animations together
5. **Use Constants**: Leverage built-in constants like `PI`, `TAU`, `UP`, `DOWN`

## Next Steps

Now that you understand the basics, explore:

- The [example scenes](example_scenes.rst) for more complex examples
- The [API reference](../documentation/api_reference.md) for complete class documentation
- Different animation types in the manimlib.animation modules
- Various mobject types for geometric shapes, graphs, and more
- Advanced topics like custom animations and 3D scenes

## Quick Reference

### Essential Imports
```python
from manimlib import *
```

### Basic Scene Structure
```python
class MyScene(Scene):
    def construct(self):
        # Your animation code here
        pass
```

### Common Methods
- `self.add(obj)`: Add object to scene
- `self.play(animation)`: Run animation
- `self.wait(duration)`: Pause scene
- `self.remove(obj)`: Remove object from scene

### Useful Constants
- Colors: `RED`, `BLUE`, `GREEN`, `YELLOW`, `WHITE`, `BLACK`
- Directions: `UP`, `DOWN`, `LEFT`, `RIGHT`
- Math: `PI`, `TAU`, `DEGREES`