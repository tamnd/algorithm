# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boris-pusher/. The authors are listed in prov/F8XC41.jsonl.
"""The Boris pusher for a charged particle in electric and magnetic fields.

The equations of motion are dx/dt = v and dv/dt = (q/m)(E(x) + v x B(x)),
nonrelativistic. The positions live at whole steps and the velocities at half
steps (leapfrog). One step is half an electric kick, an exact-length rotation
of the velocity about B, and another half electric kick, then a drift.

The step is the same as the implicit midpoint rule for the velocity,
(v_new - v_old) / h = (q/m) (E + (v_new + v_old)/2 x B), solved in closed form.

Cost: O(1) time and space per particle per step, plus one field evaluation.
"""

import math
from typing import Callable

Vec3 = tuple[float, float, float]
Field = Callable[[Vec3], tuple[Vec3, Vec3]]


def cross(a: Vec3, b: Vec3) -> Vec3:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def boris_velocity(v: Vec3, e: Vec3, b: Vec3, qm: float, h: float) -> Vec3:
    """New half-step velocity from the old one, for the fields e and b at the particle."""
    a = 0.5 * qm * h
    vm = tuple(v[k] + a * e[k] for k in range(3))  # @line L3
    t = tuple(a * b[k] for k in range(3))  # @line L4
    t2 = t[0] ** 2 + t[1] ** 2 + t[2] ** 2  # @line L4
    s = tuple(2 * t[k] / (1 + t2) for k in range(3))  # @line L4
    c = cross(vm, t)  # @line L5
    vp1 = tuple(vm[k] + c[k] for k in range(3))  # @line L5
    c = cross(vp1, s)  # @line L6
    vp = tuple(vm[k] + c[k] for k in range(3))  # @line L6
    return tuple(vp[k] + a * e[k] for k in range(3))  # @line L7


def boris_run(x: Vec3, v_half: Vec3, field: Field, qm: float, h: float, steps: int) -> tuple[Vec3, Vec3]:
    """Advance (x_0, v_{-1/2}) by `steps` Boris steps; return (x_steps, v_{steps-1/2})."""
    x, v = tuple(x), tuple(v_half)
    for _ in range(steps):  # @line L1
        e, b = field(x)  # @line L2
        v = boris_velocity(v, e, b, qm, h)
        x = tuple(x[k] + h * v[k] for k in range(3))  # @line L8
    return x, v  # @line L9


def start_velocity(x: Vec3, v0: Vec3, field: Field, qm: float, h: float) -> Vec3:
    """v_{-1/2} from v(0) by one explicit half step backward (error O(h^2))."""
    e, b = field(x)
    c = cross(v0, b)
    return tuple(v0[k] - 0.5 * h * qm * (e[k] + c[k]) for k in range(3))


def rotation_angle(omega_h: float) -> float:
    """The angle the velocity turns in one step in a pure field B, with omega_h = q |B| h / m."""
    return 2 * math.atan(omega_h / 2)
