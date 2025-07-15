"""
Shape matching utilities for creating visual indicators and highlighting.

This module provides mobjects that automatically match and highlight other
mobjects, including surrounding rectangles, background rectangles, crosses
for marking, and underlines for emphasis.
"""

from __future__ import annotations

from colour import Color

from manimlib.config import manim_config
from manimlib.constants import BLACK, RED, YELLOW, DEFAULT_MOBJECT_COLOR
from manimlib.constants import DL, DOWN, DR, LEFT, RIGHT, UL, UR
from manimlib.constants import SMALL_BUFF
from manimlib.mobject.geometry import Line
from manimlib.mobject.geometry import Rectangle
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Sequence
    from manimlib.mobject.mobject import Mobject
    from manimlib.typing import ManimColor, Self


class SurroundingRectangle(Rectangle):
    """
    A rectangle that automatically sizes itself to surround another mobject.
    
    This is useful for highlighting or drawing attention to specific mobjects
    in a scene. The rectangle maintains a specified buffer distance from the
    mobject's boundary.
    
    Parameters
    ----------
    mobject : Mobject
        The mobject to surround
    buff : float, optional
        Buffer distance from the mobject boundary (default: SMALL_BUFF)
    color : ManimColor, optional
        Color of the surrounding rectangle (default: YELLOW)
    **kwargs
        Additional arguments passed to parent Rectangle class
        
    Examples
    --------
    Highlight a text mobject:
    
    >>> text = Text("Important!")
    >>> highlight = SurroundingRectangle(text, color=RED)
    >>> self.add(text, highlight)
    """
    def __init__(
        self,
        mobject: Mobject,
        buff: float = SMALL_BUFF,
        color: ManimColor = YELLOW,
        **kwargs
    ):
        super().__init__(color=color, **kwargs)
        self.buff = buff
        self.surround(mobject)
        if mobject.is_fixed_in_frame():
            self.fix_in_frame()

    def surround(self, mobject, buff=None) -> Self:
        """
        Update the rectangle to surround a new mobject.
        
        Parameters
        ----------
        mobject : Mobject
            The mobject to surround
        buff : float, optional
            New buffer distance (uses current buff if None)
            
        Returns
        -------
        Self
            Returns self for method chaining
        """
        self.mobject = mobject
        self.buff = buff if buff is not None else self.buff
        super().surround(mobject, self.buff)
        return self

    def set_buff(self, buff) -> Self:
        """
        Set a new buffer distance and update the surrounding rectangle.
        
        Parameters
        ----------
        buff : float
            New buffer distance from the mobject
            
        Returns
        -------
        Self
            Returns self for method chaining
        """
        self.buff = buff
        self.surround(self.mobject)
        return self


class BackgroundRectangle(SurroundingRectangle):
    """
    A rectangle that provides a background behind a mobject.
    
    This is useful for ensuring text or objects are readable over complex
    backgrounds. The rectangle automatically matches the background color
    and provides opacity control.
    
    Parameters
    ----------
    mobject : Mobject
        The mobject to provide background for
    color : ManimColor, optional
        Background color (uses scene background if None)
    stroke_width : float, optional
        Width of the border stroke (default: 0)
    stroke_opacity : float, optional
        Opacity of the border stroke (default: 0)
    fill_opacity : float, optional
        Opacity of the background fill (default: 0.75)
    buff : float, optional
        Buffer distance from the mobject (default: 0)
    **kwargs
        Additional arguments passed to parent SurroundingRectangle class
        
    Examples
    --------
    Add background to text for readability:
    
    >>> text = Text("Clear Text")
    >>> background = BackgroundRectangle(text, fill_opacity=0.8)
    >>> self.add(background, text)
    """
    def __init__(
        self,
        mobject: Mobject,
        color: ManimColor = None,
        stroke_width: float = 0,
        stroke_opacity: float = 0,
        fill_opacity: float = 0.75,
        buff: float = 0,
        **kwargs
    ):
        if color is None:
            color = manim_config.camera.background_color
        super().__init__(
            mobject,
            color=color,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
            fill_opacity=fill_opacity,
            buff=buff,
            **kwargs
        )
        self.original_fill_opacity = fill_opacity

    def pointwise_become_partial(self, mobject: Mobject, a: float, b: float) -> Self:
        """Update fill opacity based on partial animation progress."""
        self.set_fill(opacity=b * self.original_fill_opacity)
        return self

    def set_style(
        self,
        stroke_color: ManimColor | None = None,
        stroke_width: float | None = None,
        fill_color: ManimColor | None = None,
        fill_opacity: float | None = None,
        family: bool = True,
        **kwargs
    ) -> Self:
        """
        Set style properties, with fixed stroke settings.
        
        Only fill_opacity can be changed, other properties are fixed
        to maintain the background appearance.
        """
        # Unchangeable style, except for fill_opacity
        VMobject.set_style(
            self,
            stroke_color=BLACK,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=fill_opacity
        )
        return self

    def get_fill_color(self) -> Color:
        """Get the fill color as a Color object."""
        return Color(self.color)


class Cross(VGroup):
    """
    Two intersecting lines that form an X shape over a mobject.
    
    This is useful for marking objects as crossed out, deleted, or incorrect.
    The cross automatically sizes itself to match the target mobject.
    
    Parameters
    ----------
    mobject : Mobject
        The mobject to place the cross over
    stroke_color : ManimColor, optional
        Color of the cross lines (default: RED)
    stroke_width : float | Sequence[float], optional
        Width of the cross lines (default: [0, 6, 0] for tapered effect)
    **kwargs
        Additional arguments passed to parent VGroup class
        
    Examples
    --------
    Mark an equation as incorrect:
    
    >>> equation = MathTex("2 + 2 = 5")
    >>> cross = Cross(equation, stroke_color=RED)
    >>> self.add(equation, cross)
    """
    def __init__(
        self,
        mobject: Mobject,
        stroke_color: ManimColor = RED,
        stroke_width: float | Sequence[float] = [0, 6, 0],
        **kwargs
    ):
        super().__init__(
            Line(UL, DR),
            Line(UR, DL),
        )
        self.insert_n_curves(20)
        self.replace(mobject, stretch=True)
        self.set_stroke(stroke_color, width=stroke_width)


class Underline(Line):
    """
    A line that appears underneath a mobject to provide emphasis.
    
    This is commonly used to emphasize text or mathematical expressions.
    The underline automatically positions itself below the target mobject
    with customizable styling.
    
    Parameters
    ----------
    mobject : Mobject
        The mobject to underline
    buff : float, optional
        Distance below the mobject (default: SMALL_BUFF)
    stroke_color : ManimColor, optional
        Color of the underline (default: DEFAULT_MOBJECT_COLOR)
    stroke_width : float | Sequence[float], optional
        Width of the underline (default: [0, 3, 3, 0] for tapered ends)
    stretch_factor : float, optional
        Factor to stretch the underline width relative to mobject (default: 1.2)
    **kwargs
        Additional arguments passed to parent Line class
        
    Examples
    --------
    Emphasize important text:
    
    >>> text = Text("Important Point")
    >>> underline = Underline(text, stroke_color=BLUE)
    >>> self.add(text, underline)
    """
    def __init__(
        self,
        mobject: Mobject,
        buff: float = SMALL_BUFF,
        stroke_color=DEFAULT_MOBJECT_COLOR,
        stroke_width: float | Sequence[float] = [0, 3, 3, 0],
        stretch_factor=1.2,
        **kwargs
    ):
        super().__init__(LEFT, RIGHT, **kwargs)
        if not isinstance(stroke_width, (float, int)):
            self.insert_n_curves(len(stroke_width) - 2)
        self.set_stroke(stroke_color, stroke_width)
        self.set_width(mobject.get_width() * stretch_factor)
        self.next_to(mobject, DOWN, buff=buff)
