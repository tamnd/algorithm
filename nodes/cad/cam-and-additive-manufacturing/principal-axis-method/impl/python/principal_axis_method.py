# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/principal-axis-method/. The authors are listed in prov/WFBXPX.jsonl.

"""Principal axis method (PAM) for five-axis milling with a toroidal end mill.

The tool is a toroidal end mill: a flat bottom disk of radius R and a corner
of radius r. The centers of the corner circles form the center circle C, of
radius R, in the plane at height r above the tool tip. With r = 0 the tool
is a flat end mill.

At a cutter contact point p the surface has the unit normal n (pointing out
of the material, toward the tool), the unit direction e_min of minimum
normal curvature and the maximum normal curvature kappa_max. A curvature is
positive where the surface bends toward the tool (a concave part, such as
the inside of a trough).

PAM tilts the tool axis away from n by the angle lam in the plane of n and
e_min. Seen along e_min, the tilted center circle is an ellipse with semi
axes R and R sin(lam). Its radius of curvature at the lowest point is
R / sin(lam), so the tool cuts a profile of radius R / sin(lam) + r in the
plane of maximum curvature. PAM picks the smallest tilt for which this
radius is not less than 1 / kappa_max:

    sin(lam) = R / (1/kappa_max - r).

Numbers may be float or Fraction. With Fractions, tool_pose_sc takes the sine
and cosine of the tilt and is exact.
"""

import math


def _add(u, v):
    return tuple(a + b for a, b in zip(u, v))


def _scale(k, u):
    return tuple(k * a for a in u)


def _cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def pam_tilt(R, r, kappa_max, lam_min=0.0):
    """The PAM tilt angle in radians, from the tool and the maximum curvature."""
    if R <= 0 or r < 0:
        raise ValueError("the tool needs R > 0 and r >= 0")
    if kappa_max <= 0:  # @line L1
        return lam_min  # @line L2
    rho = 1 / kappa_max  # @line L3
    if R > rho - r:  # @line L4
        raise ValueError("no tilt avoids a gouge: the tool is too wide for the curvature")
    return max(math.asin(R / (rho - r)), lam_min)  # @line L5


def tool_pose_sc(p, n, e_min, s, c, R, r):
    """Place the tool for a tilt with sine s and cosine c.

    Returns (axis, tip, e): the unit tool axis, the center of the tool tip
    (the bottom disk) and the unit direction e in the bottom plane from the
    axis to the lowest point of the center circle.
    """
    axis = _add(_scale(c, n), _scale(s, e_min))  # @line L6
    e = _add(_scale(c, e_min), _scale(-s, n))  # @line L7
    tip = _add(_add(p, _scale(r, n)), _add(_scale(-r, axis), _scale(-R, e)))  # @line L8
    return axis, tip, e


def tool_pose(p, n, e_min, lam, R, r):
    """Place the tool for the tilt angle lam (radians)."""
    return tool_pose_sc(p, n, e_min, math.sin(lam), math.cos(lam), R, r)


def principal_axis_method(p, n, e_min, kappa_max, R, r, lam_min=0.0):
    """Run PAM at one contact point. Returns (lam, axis, tip)."""
    lam = pam_tilt(R, r, kappa_max, lam_min)
    axis, tip, _ = tool_pose(p, n, e_min, lam, R, r)
    return lam, axis, tip  # @line L9


def center_circle_point(axis, tip, e, R, r, cos_t, sin_t):
    """The point of the center circle at the angle t from e, given cos t and sin t."""
    w = _cross(axis, e)
    return _add(_add(tip, _scale(r, axis)), _add(_scale(R * cos_t, e), _scale(R * sin_t, w)))
