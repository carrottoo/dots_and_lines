# TODO: this should not be needed in Python >= 3.10
from __future__ import annotations
from typing import Any, Union
import math


class TwoDimensionalVector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # Implement arithmetic operations for two dimensional vector
    def __add__(self, other: TwoDimensionalVector) -> TwoDimensionalVector:
        return TwoDimensionalVector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: TwoDimensionalVector) -> TwoDimensionalVector:
        return TwoDimensionalVector(self.x - other.x, self.y - other.y)

    def __truediv__(self, other: float) -> TwoDimensionalVector:
        return self * (1 / other)

    # This is needed for TwoDimensionalVector * float
    def __mul__(self, other: Union[TwoDimensionalVector, float]) -> TwoDimensionalVector:
        if isinstance(other, TwoDimensionalVector):
            return TwoDimensionalVector(self.x * other.x, self.y * other.y)
        else:
            return self * TwoDimensionalVector(other, other)

    # This is needed for float * TwoDimensionalVector
    def __rmul__(self, other: float) -> TwoDimensionalVector:
        return self * other

    def distance(self, other: TwoDimensionalVector) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self):
        return f'TwoDimensionalVector({self.x}, {self.y})'

    def __str__(self):
        return repr(self)
