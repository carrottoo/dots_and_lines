import pytest
from src.vector import TwoDimensionalVector
#  Unit test two dimensional vector

def test_initialization():
    vector = TwoDimensionalVector(3.0, 4.0)
    assert vector.x == 3.0
    assert vector.y == 4.0

def test_addition():
    vector1 = TwoDimensionalVector(1.0, 2.0)
    vector2 = TwoDimensionalVector(3.0, 4.0)
    result = vector1 + vector2
    assert result.x == 4.0
    assert result.y == 6.0

def test_subtraction():
    vector1 = TwoDimensionalVector(5.0, 3.0)
    vector2 = TwoDimensionalVector(2.0, 1.0)
    result = vector1 - vector2
    assert result.x == 3.0
    assert result.y == 2.0

def test_scalar_multiplication():
    vector = TwoDimensionalVector(2.0, 3.0)
    result = vector * 2.0
    assert result.x == 4.0
    assert result.y == 6.0

def test_vector_multiplication():
    vector1 = TwoDimensionalVector(2.0, -1.0)
    vector2 = TwoDimensionalVector(0, 3.0)
    result = vector1 * vector2
    assert result.x == 0
    assert result.y == -3.0

def test_scalar_division():
    vector = TwoDimensionalVector(6.0, 9.0)
    result = vector / 3.0
    assert result.x == 2.0
    assert result.y == 3.0

def test_distance():
    vector1 = TwoDimensionalVector(3.0, 4.0)
    vector2 = TwoDimensionalVector(0.0, 0.0)
    distance = vector1.distance(vector2)
    assert distance == 5.0  



