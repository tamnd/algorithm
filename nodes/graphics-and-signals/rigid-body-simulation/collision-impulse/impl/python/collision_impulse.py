# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/collision-impulse/. The authors are listed in prov/RVWXT5.jsonl.

"""Frictionless collision impulse between two rigid bodies in 3D.

A body has its center of mass x, linear velocity v, angular velocity w (in
world coordinates), inverse mass inv_m and inverse inertia tensor inv_I (a
3 by 3 matrix in world coordinates, R I_body^(-1) R^T). A static body has
inv_m = 0 and inv_I = 0. All functions accept Fraction values, so the tests
can check the identities exactly.

Conventions (Baraff's course notes, Section 8): the contact normal n is a
unit vector that points from B to A, the relative normal velocity is
v_rel = n . (v_A(p) - v_B(p)), and v_rel < 0 means that the bodies approach.
The impulse j n acts on A and -j n acts on B.
"""

from anim import add, cross, dot, matvec, scale, sub


class Body:
    """A rigid body at one instant. m and I are needed only for the energy and momentum checks."""

    def __init__(self, x, v, w, inv_m, inv_I, m=None, I=None):
        self.x = tuple(x)
        self.v = tuple(v)
        self.w = tuple(w)
        self.inv_m = inv_m
        self.inv_I = [list(row) for row in inv_I]
        self.m = m
        self.I = None if I is None else [list(row) for row in I]

    def point_velocity(self, p):
        """Velocity of the material point of the body at the world point p."""
        return add(self.v, cross(self.w, sub(p, self.x)))


def static_body(x):
    """A body that no impulse can move (the ground)."""
    z = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    return Body(x, (0, 0, 0), (0, 0, 0), 0, z, m=None, I=None)


def relative_normal_velocity(a, b, p, n):
    """v_rel = n . (v_A(p) - v_B(p))."""
    return dot(n, sub(a.point_velocity(p), b.point_velocity(p)))


def effective_inverse_mass(a, b, p, n):
    """k = 1/m_A + 1/m_B + n.((I_A^-1 (r_A x n)) x r_A) + n.((I_B^-1 (r_B x n)) x r_B)."""
    r_a = sub(p, a.x)
    r_b = sub(p, b.x)
    k = a.inv_m + b.inv_m
    k += dot(n, cross(matvec(a.inv_I, cross(r_a, n)), r_a))
    k += dot(n, cross(matvec(b.inv_I, cross(r_b, n)), r_b))
    return k


def collision_impulse(a, b, p, n, e):
    """Apply the frictionless collision impulse at the contact point p and return j.

    After the call, n . (v_A(p) - v_B(p)) = -e times its value before the call,
    if the bodies were approaching. If they were not approaching, nothing changes
    and the result is 0.
    """
    r_a = sub(p, a.x)  # @line L1
    r_b = sub(p, b.x)  # @line L1
    v_rel = dot(n, sub(add(a.v, cross(a.w, r_a)), add(b.v, cross(b.w, r_b))))  # @line L2
    if v_rel >= 0:  # @line L3
        return 0  # @line L3
    k = a.inv_m + b.inv_m  # @line L4
    k += dot(n, cross(matvec(a.inv_I, cross(r_a, n)), r_a))  # @line L4
    k += dot(n, cross(matvec(b.inv_I, cross(r_b, n)), r_b))  # @line L4
    if k == 0:
        raise ValueError("both bodies are static")
    j = -(1 + e) * v_rel / k  # @line L5
    jn = scale(n, j)
    a.v = add(a.v, scale(jn, a.inv_m))  # @line L6
    a.w = add(a.w, matvec(a.inv_I, cross(r_a, jn)))  # @line L6
    b.v = sub(b.v, scale(jn, b.inv_m))  # @line L7
    b.w = sub(b.w, matvec(b.inv_I, cross(r_b, jn)))  # @line L7
    return j  # @line L8


def energy_loss(v_rel, k, e):
    """The kinetic energy that the collision removes: (1 - e^2) v_rel^2 / (2 k)."""
    return (1 - e * e) * v_rel * v_rel / (2 * k)


def kinetic_energy(bodies):
    """Sum of (m v.v + w.I w) / 2 over the bodies that have a mass."""
    total = 0
    for body in bodies:
        if body.m is None:
            continue
        total += body.m * dot(body.v, body.v) / 2 + dot(body.w, matvec(body.I, body.w)) / 2
    return total


def linear_momentum(bodies):
    total = (0, 0, 0)
    for body in bodies:
        if body.m is not None:
            total = add(total, scale(body.v, body.m))
    return total


def angular_momentum(bodies, origin=(0, 0, 0)):
    """Sum of (x - origin) x m v + I w over the bodies that have a mass."""
    total = (0, 0, 0)
    for body in bodies:
        if body.m is None:
            continue
        total = add(total, cross(sub(body.x, origin), scale(body.v, body.m)))
        total = add(total, matvec(body.I, body.w))
    return total
