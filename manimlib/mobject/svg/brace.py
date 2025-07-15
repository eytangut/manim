"""
Brace mobjects for creating mathematical notation brackets and labels.

This module provides various types of braces used in mathematical notation,
including underbrace, overbrace, and specialized labeling systems for
highlighting and annotating mathematical expressions.
"""

from __future__ import annotations

import math
import copy

import numpy as np

from manimlib.constants import DEFAULT_MOBJECT_TO_MOBJECT_BUFF, SMALL_BUFF
from manimlib.constants import DOWN, LEFT, ORIGIN, RIGHT, DL, DR, UL, UP
from manimlib.constants import PI
from manimlib.animation.composition import AnimationGroup
from manimlib.animation.fading import FadeIn
from manimlib.animation.growing import GrowFromCenter
from manimlib.mobject.svg.tex_mobject import Tex
from manimlib.mobject.svg.tex_mobject import TexText
from manimlib.mobject.svg.text_mobject import Text
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.types.vectorized_mobject import VMobject
from manimlib.utils.iterables import listify
from manimlib.utils.space_ops import get_norm

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable

    from manimlib.animation.animation import Animation
    from manimlib.mobject.mobject import Mobject
    from manimlib.typing import Vect3


class Brace(Tex):
    """
    A mathematical brace that automatically sizes to fit around a mobject.
    
    This creates a curly brace (like { or }) that adapts its size to surround
    the given mobject. Commonly used for grouping mathematical expressions
    or indicating scope in equations.
    
    Parameters
    ----------
    mobject : Mobject
        The mobject to surround with the brace
    direction : Vect3, optional
        Direction the brace should face (default: DOWN)
    buff : float, optional
        Buffer space between brace and mobject (default: 0.2)
    tex_string : str, optional
        LaTeX string for the brace (default: R"\\underbrace{\\qquad}")
    **kwargs
        Additional arguments passed to parent Tex class
        
    Examples
    --------
    Create a brace under an equation:
    
    >>> equation = MathTex("x^2 + y^2 = z^2")
    >>> brace = Brace(equation, DOWN)
    >>> label = brace.get_tex("Pythagorean theorem")
    >>> self.add(equation, brace, label)
    """
    def __init__(
        self,
        mobject: Mobject,
        direction: Vect3 = DOWN,
        buff: float = 0.2,
        tex_string: str = R"\underbrace{\qquad}",
        **kwargs
    ):
        super().__init__(tex_string, **kwargs)

        angle = -math.atan2(*direction[:2]) + PI
        mobject.rotate(-angle, about_point=ORIGIN)
        left = mobject.get_corner(DL)
        right = mobject.get_corner(DR)
        target_width = right[0] - left[0]

        self.tip_point_index = np.argmin(self.get_all_points()[:, 1])
        self.set_initial_width(target_width)
        self.shift(left - self.get_corner(UL) + buff * DOWN)
        for mob in mobject, self:
            mob.rotate(angle, about_point=ORIGIN)

    def set_initial_width(self, width: float):
        """
        Adjust the brace width to match the target width.
        
        Parameters
        ----------
        width : float
            Target width for the brace
        """
        width_diff = width - self.get_width()
        if width_diff > 0:
            for tip, rect, vect in [(self[0], self[1], RIGHT), (self[5], self[4], LEFT)]:
                rect.set_width(
                    width_diff / 2 + rect.get_width(),
                    about_edge=vect, stretch=True
                )
                tip.shift(-width_diff / 2 * vect)
        else:
            self.set_width(width, stretch=True)
        return self

    def put_at_tip(
        self,
        mob: Mobject,
        use_next_to: bool = True,
        **kwargs
    ):
        """
        Position a mobject at the tip of the brace.
        
        Parameters
        ----------
        mob : Mobject
            The mobject to position
        use_next_to : bool, optional
            Whether to use next_to positioning (default: True)
        **kwargs
            Additional positioning arguments
        """
        if use_next_to:
            mob.next_to(
                self.get_tip(),
                np.round(self.get_direction()),
                **kwargs
            )
        else:
            mob.move_to(self.get_tip())
            buff = kwargs.get("buff", DEFAULT_MOBJECT_TO_MOBJECT_BUFF)
            shift_distance = mob.get_width() / 2.0 + buff
            mob.shift(self.get_direction() * shift_distance)
        return self

    def get_text(self, text: str, **kwargs) -> Text:
        """
        Create text positioned at the brace tip.
        
        Parameters
        ----------
        text : str
            Text content
        **kwargs
            Additional text formatting arguments
            
        Returns
        -------
        Text
            The positioned text mobject
        """
        buff = kwargs.pop("buff", SMALL_BUFF)
        text_mob = Text(text, **kwargs)
        self.put_at_tip(text_mob, buff=buff)
        return text_mob

    def get_tex(self, *tex: str, **kwargs) -> Tex:
        """
        Create LaTeX text positioned at the brace tip.
        
        Parameters
        ----------
        *tex : str
            LaTeX content strings
        **kwargs
            Additional LaTeX formatting arguments
            
        Returns
        -------
        Tex
            The positioned LaTeX mobject
        """
        buff = kwargs.pop("buff", SMALL_BUFF)
        tex_mob = Tex(*tex, **kwargs)
        self.put_at_tip(tex_mob, buff=buff)
        return tex_mob

    def get_tip(self) -> np.ndarray:
        """
        Get the 3D coordinates of the brace tip.
        
        Returns
        -------
        np.ndarray
            3D coordinates of the tip point
        """
        # Very specific to the LaTeX representation
        # of a brace, but it's the only way I can think
        # of to get the tip regardless of orientation.
        return self.get_all_points()[self.tip_point_index]

    def get_direction(self) -> np.ndarray:
        """
        Get the unit vector pointing from brace center to tip.
        
        Returns
        -------
        np.ndarray
            Normalized direction vector
        """
        vect = self.get_tip() - self.get_center()
        return vect / get_norm(vect)


class BraceLabel(VMobject):
    """
    A combined brace and label system for mathematical annotations.
    
    This convenience class creates a brace around an object and automatically
    positions a label at the brace tip. Useful for labeling parts of equations
    or diagrams with both visual grouping and text description.
    
    Parameters
    ----------
    obj : VMobject | list[VMobject]
        The object(s) to surround with the brace
    text : str | Iterable[str]
        Label text content
    brace_direction : np.ndarray, optional
        Direction for the brace (default: DOWN)
    label_scale : float, optional
        Scale factor for the label (default: 1.0)
    label_buff : float, optional
        Buffer between brace and label (default: DEFAULT_MOBJECT_TO_MOBJECT_BUFF)
    **kwargs
        Additional arguments passed to components
        
    Examples
    --------
    Label a group of terms:
    
    >>> terms = VGroup(x_term, y_term, z_term)
    >>> brace_label = BraceLabel(terms, "Variables", DOWN)
    >>> self.add(terms, brace_label)
    """
    label_constructor: type = Tex

    def __init__(
        self,
        obj: VMobject | list[VMobject],
        text: str | Iterable[str],
        brace_direction: np.ndarray = DOWN,
        label_scale: float = 1.0,
        label_buff: float = DEFAULT_MOBJECT_TO_MOBJECT_BUFF,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.brace_direction = brace_direction
        self.label_scale = label_scale
        self.label_buff = label_buff

        if isinstance(obj, list):
            obj = VGroup(*obj)
        self.brace = Brace(obj, brace_direction, **kwargs)

        self.label = self.label_constructor(*listify(text), **kwargs)
        self.label.scale(self.label_scale)

        self.brace.put_at_tip(self.label, buff=self.label_buff)
        self.set_submobjects([self.brace, self.label])

    def creation_anim(
        self,
        label_anim: Animation = FadeIn,
        brace_anim: Animation = GrowFromCenter
    ) -> AnimationGroup:
        """
        Create an animation group for the brace and label creation.
        
        Parameters
        ----------
        label_anim : Animation, optional
            Animation for the label (default: FadeIn)
        brace_anim : Animation, optional
            Animation for the brace (default: GrowFromCenter)
            
        Returns
        -------
        AnimationGroup
            Combined animation for both components
        """
        return AnimationGroup(brace_anim(self.brace), label_anim(self.label))

    def shift_brace(self, obj: VMobject | list[VMobject], **kwargs):
        """
        Move the brace to surround a new object.
        
        Parameters
        ----------
        obj : VMobject | list[VMobject]
            New object(s) to surround
        **kwargs
            Additional brace creation arguments
        """
        if isinstance(obj, list):
            obj = VMobject(*obj)
        self.brace = Brace(obj, self.brace_direction, **kwargs)
        self.brace.put_at_tip(self.label)
        self.submobjects[0] = self.brace
        return self

    def change_label(self, *text: str, **kwargs):
        """
        Update the label text.
        
        Parameters
        ----------
        *text : str
            New label text
        **kwargs
            Additional label formatting arguments
        """
        self.label = self.label_constructor(*text, **kwargs)
        if self.label_scale != 1:
            self.label.scale(self.label_scale)

        self.brace.put_at_tip(self.label)
        self.submobjects[1] = self.label
        return self

    def change_brace_label(self, obj: VMobject | list[VMobject], *text: str):
        """
        Update both the brace position and label text.
        
        Parameters
        ----------
        obj : VMobject | list[VMobject]
            New object(s) to surround
        *text : str
            New label text
        """
        self.shift_brace(obj)
        self.change_label(*text)
        return self

    def copy(self):
        """Create a deep copy of the BraceLabel."""
        copy_mobject = copy.copy(self)
        copy_mobject.brace = self.brace.copy()
        copy_mobject.label = self.label.copy()
        copy_mobject.set_submobjects([copy_mobject.brace, copy_mobject.label])

        return copy_mobject


class BraceText(BraceLabel):
    """
    A BraceLabel that uses TexText for the label instead of Tex.
    
    This is useful when you want to use text formatting rather than
    mathematical LaTeX formatting for the brace label.
    
    Examples
    --------
    Create a brace with formatted text label:
    
    >>> equation = MathTex("E = mc^2")
    >>> brace_text = BraceText(equation, "Einstein's equation", DOWN)
    >>> self.add(equation, brace_text)
    """
    label_constructor: type = TexText


class LineBrace(Brace):
    """
    A brace specifically designed to fit along a line.
    
    This creates a brace that aligns with the angle and position of a given
    line, useful for labeling line segments or indicating measurements.
    
    Parameters
    ----------
    line : Line
        The line to create a brace for
    direction : Vect3, optional
        Direction relative to the line (default: UP)
    **kwargs
        Additional arguments passed to parent Brace class
        
    Examples
    --------
    Create a brace along a diagonal line:
    
    >>> line = Line(LEFT, UP + RIGHT)
    >>> line_brace = LineBrace(line, UP)
    >>> label = line_brace.get_tex("\\sqrt{2}")
    >>> self.add(line, line_brace, label)
    """
    def __init__(self, line: Line, direction=UP, **kwargs):
        angle = line.get_angle()
        line.rotate(-angle)
        super().__init__(line, direction, **kwargs)
        line.rotate(angle)
        self.rotate(angle, about_point=line.get_center())
