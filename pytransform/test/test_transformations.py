import numpy as np
from pytransform.transformations import (transform_from, invert_transform,
                                         vector_to_point, concat, transform)
from pytransform.rotations import matrix_from, random_axis_angle, random_vector
from nose.tools import assert_true
from numpy.testing import assert_array_almost_equal


def test_invert_transform():
    """Test inversion of transformations."""
    caught_error = False
    try:
        invert_transform(np.eye(3))
    except ValueError:
        caught_error = True
    finally:
        assert_true(caught_error)

    random_state = np.random.RandomState(0)
    for _ in range(5):
        R = matrix_from(a=random_axis_angle(random_state))
        p = random_vector(random_state)
        A2B = transform_from(R, p)
        B2A = invert_transform(A2B)
        A2B2 = np.linalg.inv(B2A)
        assert_array_almost_equal(A2B, A2B2)


def test_vector_to_point():
    """Test conversion from vector to homogenous coordinates."""
    v = np.array([1, 2, 3])
    pA = vector_to_point(v)
    assert_array_almost_equal(pA, [1, 2, 3, 1])

    random_state = np.random.RandomState(0)
    R = matrix_from(a=random_axis_angle(random_state))
    p = random_vector(random_state)
    A2B = transform_from(R, p)
    pB = transform(A2B, pA)


def test_concat():
    """Test concatenation of transforms."""
    random_state = np.random.RandomState(0)
    for _ in range(5):
        R = matrix_from(a=random_axis_angle(random_state))
        p = random_vector(random_state)
        A2B = transform_from(R, p)

        R = matrix_from(a=random_axis_angle(random_state))
        p = random_vector(random_state)
        B2C = transform_from(R, p)

        A2C = concat(A2B, B2C)

        p_A = np.array([0.3, -0.2, 0.9, 1.0])
        p_C = transform(A2C, p_A)

        C2A = invert_transform(A2C)
        p_A2 = transform(C2A, p_C)

        assert_array_almost_equal(p_A, p_A2)

        C2A2 = concat(invert_transform(B2C), invert_transform(A2B))
        p_A3 = transform(C2A2, p_C)
        assert_array_almost_equal(p_A, p_A3)


def test_transform():
    PA = np.array([[1, 2, 3, 1],
                   [2, 3, 4, 1]])

    random_state = np.random.RandomState(0)
    R = matrix_from(a=random_axis_angle(random_state))
    p = random_vector(random_state)
    A2B = transform_from(R, p)

    PB = transform(A2B, PA)
    p0B = transform(A2B, PA[0])
    p1B = transform(A2B, PA[1])
    assert_array_almost_equal(PB, np.array([p0B, p1B]))

    caught_error = False
    try:
        transform(A2B, np.zeros((2, 2, 4)))
    except ValueError:
        caught_error = True
    finally:
        assert_true(caught_error)
