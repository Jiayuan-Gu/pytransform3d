"""Testing utilities."""
import warnings
import numpy as np
from numpy.testing import assert_array_almost_equal
from ._utils import norm_axis_angle, norm_compact_axis_angle
from ._conversions import matrix_from_euler_zyx, matrix_from_euler_xyz


def assert_axis_angle_equal(a1, a2, *args, **kwargs):
    """Raise an assertion if two axis-angle are not approximately equal.

    Usually we assume that the rotation axis is normalized to length 1 and
    the angle is within [0, pi). However, this function ignores these
    constraints and will normalize the representations before comparison.
    See numpy.testing.assert_array_almost_equal for a more detailed
    documentation of the other parameters.

    Parameters
    ----------
    a1 : array-like, shape (4,)
        Axis of rotation and rotation angle: (x, y, z, angle)

    a2 : array-like, shape (4,)
        Axis of rotation and rotation angle: (x, y, z, angle)

    args : tuple
        Positional arguments that will be passed to
        `assert_array_almost_equal`

    kwargs : dict
        Positional arguments that will be passed to
        `assert_array_almost_equal`
    """
    # required despite normalization in case of 180 degree rotation
    if np.any(np.sign(a1) != np.sign(a2)):
        a1 = -a1
    a1 = norm_axis_angle(a1)
    a2 = norm_axis_angle(a2)
    assert_array_almost_equal(a1, a2, *args, **kwargs)


def assert_compact_axis_angle_equal(a1, a2, *args, **kwargs):
    """Raise an assertion if two axis-angle are not approximately equal.

    Usually we assume that the angle is within [0, pi). However, this function
    ignores this constraint and will normalize the representations before
    comparison. See numpy.testing.assert_array_almost_equal for a more detailed
    documentation of the other parameters.

    Parameters
    ----------
    a1 : array-like, shape (3,)
        Axis of rotation and rotation angle: angle * (x, y, z)

    a2 : array-like, shape (3,)
        Axis of rotation and rotation angle: angle * (x, y, z)

    args : tuple
        Positional arguments that will be passed to
        `assert_array_almost_equal`

    kwargs : dict
        Positional arguments that will be passed to
        `assert_array_almost_equal`
    """
    angle1 = np.linalg.norm(a1)
    angle2 = np.linalg.norm(a2)
    # required despite normalization in case of 180 degree rotation
    if (abs(angle1) == np.pi and abs(angle2) == np.pi and
            any(np.sign(a1) != np.sign(a2))):
        a1 = -a1
    a1 = norm_compact_axis_angle(a1)
    a2 = norm_compact_axis_angle(a2)
    assert_array_almost_equal(a1, a2, *args, **kwargs)


def assert_quaternion_equal(q1, q2, *args, **kwargs):
    """Raise an assertion if two quaternions are not approximately equal.

    Note that quaternions are equal either if q1 == q2 or if q1 == -q2. See
    numpy.testing.assert_array_almost_equal for a more detailed documentation
    of the other parameters.

    Parameters
    ----------
    q1 : array-like, shape (4,)
        Unit quaternion to represent rotation: (w, x, y, z)

    q2 : array-like, shape (4,)
        Unit quaternion to represent rotation: (w, x, y, z)

    args : tuple
        Positional arguments that will be passed to
        `assert_array_almost_equal`

    kwargs : dict
        Positional arguments that will be passed to
        `assert_array_almost_equal`
    """
    try:
        assert_array_almost_equal(q1, q2, *args, **kwargs)
    except AssertionError:
        assert_array_almost_equal(q1, -q2, *args, **kwargs)


def assert_euler_xyz_equal(e_xyz1, e_xyz2, *args, **kwargs):
    """Raise an assertion if two xyz Euler angles are not approximately equal.

    Note that Euler angles are only unique if we limit them to the intervals
    [-pi, pi], [-pi/2, pi/2], and [-pi, pi] respectively. See
    numpy.testing.assert_array_almost_equal for a more detailed documentation
    of the other parameters.

    Parameters
    ----------
    e_xyz1 : array-like, shape (3,)
        Angles for rotation around x-, y'-, and z''-axes (intrinsic rotations)

    e_xyz2 : array-like, shape (3,)
        Angles for rotation around x-, y'-, and z''-axes (intrinsic rotations)

    args : tuple
        Positional arguments that will be passed to
        `assert_array_almost_equal`

    kwargs : dict
        Positional arguments that will be passed to
        `assert_array_almost_equal`
    """
    warnings.warn("assert_euler_xyz_equal will be removed in version 2.0.0",
                  DeprecationWarning, stacklevel=2)
    R1 = matrix_from_euler_xyz(e_xyz1)
    R2 = matrix_from_euler_xyz(e_xyz2)
    assert_array_almost_equal(R1, R2, *args, **kwargs)


def assert_euler_zyx_equal(e_zyx1, e_zyx2, *args, **kwargs):
    """Raise an assertion if two zyx Euler angles are not approximately equal.

    Note that Euler angles are only unique if we limit them to the intervals
    [-pi, pi], [-pi/2, pi/2], and [-pi, pi] respectively. See
    numpy.testing.assert_array_almost_equal for a more detailed documentation
    of the other parameters.

    Parameters
    ----------
    e_zyx1 : array-like, shape (3,)
        Angles for rotation around z-, y'-, and x''-axes (intrinsic rotations)

    e_zyx2 : array-like, shape (3,)
        Angles for rotation around z-, y'-, and x''-axes (intrinsic rotations)

    args : tuple
        Positional arguments that will be passed to
        `assert_array_almost_equal`

    kwargs : dict
        Positional arguments that will be passed to
        `assert_array_almost_equal`
    """
    warnings.warn("assert_euler_zyx_equal will be removed in version 2.0.0",
                  DeprecationWarning, stacklevel=2)
    R1 = matrix_from_euler_zyx(e_zyx1)
    R2 = matrix_from_euler_zyx(e_zyx2)
    assert_array_almost_equal(R1, R2, *args, **kwargs)


def assert_rotation_matrix(R, *args, **kwargs):
    """Raise an assertion if a matrix is not a rotation matrix.

    The two properties :math:`\\boldsymbol{I} = \\boldsymbol{R R}^T` and
    :math:`det(R) = 1` will be checked. See
    numpy.testing.assert_array_almost_equal for a more detailed documentation
    of the other parameters.

    Parameters
    ----------
    R : array-like, shape (3, 3)
        Rotation matrix

    args : tuple
        Positional arguments that will be passed to
        `assert_array_almost_equal`

    kwargs : dict
        Positional arguments that will be passed to
        `assert_array_almost_equal`
    """
    assert_array_almost_equal(np.dot(R, R.T), np.eye(3), *args, **kwargs)
    assert_array_almost_equal(np.linalg.det(R), 1.0, *args, **kwargs)
