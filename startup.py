# imports
import sympy
import math
from typing import Optional
from enum import Enum

# useful type hint
NumericOrExpression = float|int|sympy.Expr


# modes
DEGREES = True

class Mode(Enum):
    MATH = (0, False)
    AUTO = (1, False)
    SYMPY = (2, False)
    NUMERIC_SYMPY = (3, True)
    NUMERIC_AUTO = (4, True)

    @property
    def enforce_numeric(self): return self.value[1]

CURRENT_MODE: Mode = Mode.AUTO


# helper functions
def _get_backend(n: NumericOrExpression, override_mode: Mode|None, b: NumericOrExpression = 0):
    mode = CURRENT_MODE if override_mode is None else override_mode
    if mode == Mode.MATH:
        return math
    elif mode == Mode.AUTO:
        return sympy if (isinstance(n, sympy.Expr) or isinstance(b, sympy.Expr)) else math
    elif mode == Mode.SYMPY:
        return sympy
    
    # numeric enforcement done in _enforce_numeric
    elif mode == Mode.NUMERIC_SYMPY:
        return sympy
    elif mode == Mode.NUMERIC_AUTO:
        return sympy if (isinstance(n, sympy.Expr) or isinstance(b, sympy.Expr)) else math
    
    else:
        raise ValueError(f"Invalid mode: {mode}. Expected one of {[m.name for m in Mode]}")

def _correct_angle_unit(n: NumericOrExpression, backend, override_degrees: bool|None) -> NumericOrExpression:
    d = DEGREES if override_degrees is None else override_degrees
    if d:
        return backend.radians(n)
    else:
        return n


def _enforce_numeric(n: NumericOrExpression, override_mode: Mode|None):
    mode = CURRENT_MODE if override_mode is None else override_mode
    if mode.enforce_numeric:
        if isinstance(n, sympy.Expr):
            return n.evalf()
        
    return n

def _trig(n: NumericOrExpression, degrees: bool|None, mode: Mode|None, func: str) -> NumericOrExpression:
    backend = _get_backend(n, mode)
    return _enforce_numeric(
        getattr(backend, func)(_correct_angle_unit(n, backend, degrees))
    )

def _inverse_trig(n: NumericOrExpression, degrees: bool|None, mode: Mode|None, func: str) -> NumericOrExpression:
    backend = _get_backend(n, mode)
    return _enforce_numeric(
        _correct_angle_unit(getattr(backend, func)(n), backend, degrees)
    )


# functions
def sin(n: NumericOrExpression, degrees: Optional[bool] = None, mode: Optional[Mode] = None) -> NumericOrExpression:
    return _trig(n, degrees, mode, "sin")
def cos(n: NumericOrExpression, degrees: Optional[bool] = None, mode: Optional[Mode] = None) -> NumericOrExpression:
    return _trig(n, degrees, mode, "cos")
def tan(n: NumericOrExpression, degrees: Optional[bool] = None, mode: Optional[Mode] = None) -> NumericOrExpression:
    return _trig(n, degrees, mode, "tan")

def arcsin(n: NumericOrExpression, degrees: Optional[bool] = None, mode: Optional[Mode] = None) -> NumericOrExpression:
    return _inverse_trig(n, degrees, mode, "asin")
def arccos(n: NumericOrExpression, degrees: Optional[bool] = None, mode: Optional[Mode] = None) -> NumericOrExpression:
    return _inverse_trig(n, degrees, mode, "acos")
def arctan(n: NumericOrExpression, degrees: Optional[bool] = None, mode: Optional[Mode] = None) -> NumericOrExpression:
    return _inverse_trig(n, degrees, mode, "atan")

def log(n: NumericOrExpression, base: NumericOrExpression = 10, mode: Optional[Mode] = None) -> NumericOrExpression:
    backend = _get_backend(n, mode, base) # dirty, but summing them together is an easy way to find out whether one of them was a sympy.Expr
    return _enforce_numeric(backend.log(n,base), mode)

def ln(n: NumericOrExpression, mode: Optional[Mode] = None) -> NumericOrExpression:
    return log(n, sympy.E, mode)



# The below is locatted down here to minimize conflict between the startup script and user activity in the terminal.

# These unused imports are for the user in the ipython terminal
from math import radians, degrees
from sympy import Eq, solve, symbols

# constants
# constants use sympy to be nicely compatable with symbolic equations.
# math makes use of the .__float__() method to handle them.
# DO NOT use these in this script, they could be changed by the user. Better safe than sorry.
π = sympy.pi
pi = sympy.pi
e = sympy.E
