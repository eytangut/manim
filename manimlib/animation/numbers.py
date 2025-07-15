"""
Animation classes for animating numerical values and decimal numbers.

This module provides animations specifically designed for changing numerical
values displayed as DecimalNumber mobjects, with smooth interpolation and
customizable update functions.
"""

from __future__ import annotations

from manimlib.animation.animation import Animation
from manimlib.mobject.numbers import DecimalNumber
from manimlib.utils.bezier import interpolate
from manimlib.utils.simple_functions import clip

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


class ChangingDecimal(Animation):
    """
    Animation that continuously updates a DecimalNumber based on a function.
    
    This animation allows for smooth transitions of numerical values by applying
    a custom update function that determines how the value changes over time.
    
    Parameters
    ----------
    decimal_mob : DecimalNumber
        The decimal number mobject to animate
    number_update_func : Callable[[float], float]
        Function that takes alpha (0-1) and returns the value at that point
    suspend_mobject_updating : bool, optional
        Whether to suspend automatic mobject updating during animation
    **kwargs
        Additional arguments passed to parent Animation class
        
    Examples
    --------
    Animate a number with a custom function:
    
    >>> decimal = DecimalNumber(0)
    >>> # Animate number following a sine wave
    >>> def sine_update(alpha):
    ...     return np.sin(alpha * np.pi)
    >>> animation = ChangingDecimal(decimal, sine_update)
    """
    def __init__(
        self,
        decimal_mob: DecimalNumber,
        number_update_func: Callable[[float], float],
        suspend_mobject_updating: bool = False,
        **kwargs
    ):
        assert isinstance(decimal_mob, DecimalNumber)
        self.number_update_func = number_update_func
        super().__init__(
            decimal_mob,
            suspend_mobject_updating=suspend_mobject_updating,
            **kwargs
        )
        self.mobject = decimal_mob

    def interpolate_mobject(self, alpha: float) -> None:
        """
        Update the decimal number value based on animation progress.
        
        Parameters
        ----------
        alpha : float
            Animation progress from 0 to 1
        """
        true_alpha = self.time_spanned_alpha(alpha)
        new_value = self.number_update_func(true_alpha)
        self.mobject.set_value(new_value)


class ChangeDecimalToValue(ChangingDecimal):
    """
    Animation that smoothly changes a decimal number to a target value.
    
    This is a specialized version of ChangingDecimal that interpolates between
    the current value and a specified target value using linear interpolation.
    
    Parameters
    ----------
    decimal_mob : DecimalNumber
        The decimal number mobject to animate
    target_number : float | complex
        The target value to animate towards
    **kwargs
        Additional arguments passed to parent ChangingDecimal class
        
    Examples
    --------
    Change a number from current value to 100:
    
    >>> decimal = DecimalNumber(0)
    >>> animation = ChangeDecimalToValue(decimal, 100)
    """
    def __init__(
        self,
        decimal_mob: DecimalNumber,
        target_number: float | complex,
        **kwargs
    ):
        start_number = decimal_mob.number
        super().__init__(
            decimal_mob,
            lambda a: interpolate(start_number, target_number, a),
            **kwargs
        )


class CountInFrom(ChangingDecimal):
    """
    Animation that counts/animates from a source number to the current value.
    
    This animation starts from a specified source number and animates to the
    decimal mobject's current value, useful for counting up or down effects.
    
    Parameters
    ----------
    decimal_mob : DecimalNumber
        The decimal number mobject to animate
    source_number : float | complex, optional
        The starting value to count from (default: 0)
    **kwargs
        Additional arguments passed to parent ChangingDecimal class
        
    Examples
    --------
    Count from 0 to the current number:
    
    >>> decimal = DecimalNumber(50)
    >>> animation = CountInFrom(decimal)  # Counts from 0 to 50
    
    Count from a specific starting value:
    
    >>> decimal = DecimalNumber(100)
    >>> animation = CountInFrom(decimal, source_number=25)  # Counts from 25 to 100
    """
    def __init__(
        self,
        decimal_mob: DecimalNumber,
        target_number: float | complex,
        **kwargs
    ):
        start_number = decimal_mob.number
        super().__init__(
            decimal_mob,
            lambda a: interpolate(start_number, target_number, a),
            **kwargs
        )


class CountInFrom(ChangingDecimal):
    """
    Animation that counts/animates from a source number to the current value.
    
    This animation starts from a specified source number and animates to the
    decimal mobject's current value, useful for counting up or down effects.
    
    Parameters
    ----------
    decimal_mob : DecimalNumber
        The decimal number mobject to animate
    source_number : float | complex, optional
        The starting value to count from (default: 0)
    **kwargs
        Additional arguments passed to parent ChangingDecimal class
        
    Examples
    --------
    Count from 0 to the current number:
    
    >>> decimal = DecimalNumber(50)
    >>> animation = CountInFrom(decimal)  # Counts from 0 to 50
    
    Count from a specific starting value:
    
    >>> decimal = DecimalNumber(100)
    >>> animation = CountInFrom(decimal, source_number=25)  # Counts from 25 to 100
    """
    def __init__(
        self,
        decimal_mob: DecimalNumber,
        source_number: float | complex = 0,
        **kwargs
    ):
        start_number = decimal_mob.get_value()
        super().__init__(
            decimal_mob,
            lambda a: interpolate(source_number, start_number, clip(a, 0, 1)),
            **kwargs
        )
