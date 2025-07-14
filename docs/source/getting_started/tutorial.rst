Basic Tutorial
==============

This tutorial will guide you through creating your first Manim animation.

Your First Scene
-----------------

Let's start by creating a simple scene with a circle:

.. code-block:: python

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

Understanding the Code
^^^^^^^^^^^^^^^^^^^^^^

1. **Import Manim**: The ``from manimlib import *`` line imports all Manim classes and functions.

2. **Define a Scene**: Every animation is contained in a Scene class that inherits from ``Scene``.

3. **The construct method**: This is where you define what happens in your animation.

4. **Create objects**: ``Circle()`` creates a circle mobject with specified properties.

5. **Add to scene**: ``self.add()`` places the object in the scene.

6. **Animate**: ``self.play()`` runs an animation, in this case ``Create()`` which shows the circle appearing.

7. **Wait**: ``self.wait()`` pauses the animation.

Running Your Scene
^^^^^^^^^^^^^^^^^^^

Save the code above in a file called ``basic_scene.py`` and run:

.. code-block:: bash

    manimgl basic_scene.py BasicShapes

This will open a window showing your animation. Add the ``-w`` flag to save it as a video file:

.. code-block:: bash

    manimgl basic_scene.py BasicShapes -w

Adding More Objects
--------------------

Let's create a more complex scene with multiple objects:

.. code-block:: python

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

Key Concepts
^^^^^^^^^^^^

- **Positioning**: Use ``.shift()``, ``.move_to()``, etc. to position objects
- **Multiple animations**: Pass multiple animations to ``self.play()`` to run them simultaneously
- **Animate property**: Use ``.animate`` to smoothly transition object properties
- **Run time**: Control animation speed with the ``run_time`` parameter

Text and LaTeX
---------------

Manim excels at mathematical text and equations:

.. code-block:: python

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

What's Next?
------------

Now that you understand the basics, explore:

- The :doc:`example_scenes` for more complex examples
- The :doc:`../documentation/api_reference` for complete class documentation
- Different animation types in the manimlib.animation modules
- Various mobject types for geometric shapes, graphs, and more