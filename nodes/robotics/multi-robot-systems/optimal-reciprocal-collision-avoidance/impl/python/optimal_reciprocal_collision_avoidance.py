# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-reciprocal-collision-avoidance/. The authors are listed in prov/D7S5SH.jsonl.

"""Optimal reciprocal collision avoidance (ORCA) for disc robots in the plane.

This follows van den Berg, Guy, Lin and Manocha (2011) and the structure of
their RVO2 library: each robot builds one half-plane of permitted velocities per
neighbor, then solves a 2D linear program for the velocity closest to its
preferred velocity inside all half-planes and inside the disc of maximum speed
(an incremental, Seidel style solver). If the program is infeasible, a second
program finds the velocity that violates the half-planes the least, measured by
the largest distance to a half-plane.

Vectors are tuples (x, y). A half-plane is a Line(point, direction) with a unit
direction; the permitted side is the left side, det(direction, v - point) >= 0.
Agents are holonomic discs: they can take any velocity of length at most vmax.
"""

import math
from typing import NamedTuple, Optional, Sequence

EPS = 1e-9


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, k):
    return (a[0] * k, a[1] * k)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def norm(a):
    return math.hypot(a[0], a[1])


def normalize(a):
    n = norm(a)
    return (a[0] / n, a[1] / n)


class Line(NamedTuple):
    point: tuple
    direction: tuple


class Agent(NamedTuple):
    position: tuple
    velocity: tuple
    radius: float
    vmax: float
    pref: tuple  # preferred velocity


def orca_line(a: Agent, b: Agent, tau: float, dt: float) -> Line:
    """The half-plane ORCA_A|B for agent a, with v_opt equal to the current velocity."""
    rel_pos = sub(b.position, a.position)
    rel_vel = sub(a.velocity, b.velocity)
    dist_sq = dot(rel_pos, rel_pos)
    rad = a.radius + b.radius
    rad_sq = rad * rad
    if dist_sq > rad_sq:
        # No overlap: the boundary of VO is a cut-off circle and two legs.
        w = sub(rel_vel, mul(rel_pos, 1.0 / tau))  # @line L4
        w_len_sq = dot(w, w)
        dot1 = dot(w, rel_pos)
        if dot1 < 0.0 and dot1 * dot1 > rad_sq * w_len_sq:
            w_len = math.sqrt(w_len_sq)  # nearest point is on the cut-off circle
            unit_w = mul(w, 1.0 / w_len)
            direction = (unit_w[1], -unit_w[0])
            u = mul(unit_w, rad / tau - w_len)
        else:
            leg = math.sqrt(dist_sq - rad_sq)  # nearest point is on a leg
            if det(rel_pos, w) > 0.0:
                direction = (
                    (rel_pos[0] * leg - rel_pos[1] * rad) / dist_sq,
                    (rel_pos[0] * rad + rel_pos[1] * leg) / dist_sq,
                )
            else:
                direction = (
                    -(rel_pos[0] * leg + rel_pos[1] * rad) / dist_sq,
                    -(-rel_pos[0] * rad + rel_pos[1] * leg) / dist_sq,
                )
            u = sub(mul(direction, dot(rel_vel, direction)), rel_vel)
    else:
        # Overlap already: push apart within one time step.
        w = sub(rel_vel, mul(rel_pos, 1.0 / dt))
        w_len = norm(w)
        unit_w = mul(w, 1.0 / w_len)
        direction = (unit_w[1], -unit_w[0])
        u = mul(unit_w, rad / dt - w_len)
    return Line(add(a.velocity, mul(u, 0.5)), direction)  # @line L5


def lp1(lines, k, radius, opt, direction_opt):
    """Optimize on line k, inside the disc and the lines 0..k-1. Returns a point or None."""
    ln = lines[k]
    d = dot(ln.point, ln.direction)
    disc = d * d + radius * radius - dot(ln.point, ln.point)
    if disc < 0.0:
        return None
    s = math.sqrt(disc)
    t_left, t_right = -d - s, -d + s
    for i in range(k):
        denom = det(ln.direction, lines[i].direction)
        numer = det(lines[i].direction, sub(ln.point, lines[i].point))
        if abs(denom) <= EPS:
            if numer < 0.0:
                return None
            continue
        t = numer / denom
        if denom >= 0.0:
            t_right = min(t_right, t)
        else:
            t_left = max(t_left, t)
        if t_left > t_right:
            return None
    if direction_opt:
        t = t_right if dot(opt, ln.direction) > 0.0 else t_left
    else:
        t = min(max(dot(ln.direction, sub(opt, ln.point)), t_left), t_right)
    return add(ln.point, mul(ln.direction, t))


def lp2(lines, radius, opt, direction_opt=False):
    """Closest point to opt in the half-planes and the disc (or extreme point in
    direction opt). Returns (number of lines satisfied before a failure, point)."""
    if direction_opt:
        result = mul(opt, radius)
    elif dot(opt, opt) > radius * radius:
        result = mul(normalize(opt), radius)
    else:
        result = opt
    for i in range(len(lines)):  # @line L7
        if det(lines[i].direction, sub(lines[i].point, result)) > 0.0:
            new = lp1(lines, i, radius, opt, direction_opt)  # @line L8
            if new is None:
                return i, result
            result = new
    return len(lines), result


def lp3(lines, begin, radius, result):
    """Minimize the largest violation of the lines, starting from line begin."""
    distance = 0.0
    for i in range(begin, len(lines)):
        if det(lines[i].direction, sub(lines[i].point, result)) > distance:
            proj = []
            for j in range(i):
                denom = det(lines[i].direction, lines[j].direction)
                if abs(denom) <= EPS:
                    if dot(lines[i].direction, lines[j].direction) > 0.0:
                        continue
                    point = mul(add(lines[i].point, lines[j].point), 0.5)
                else:
                    t = det(lines[j].direction, sub(lines[i].point, lines[j].point)) / denom
                    point = add(lines[i].point, mul(lines[i].direction, t))
                proj.append(Line(point, normalize(sub(lines[j].direction, lines[i].direction))))
            temp = result
            opt = (-lines[i].direction[1], lines[i].direction[0])
            count, new = lp2(proj, radius, opt, True)
            result = temp if count < len(proj) else new
            distance = det(lines[i].direction, sub(lines[i].point, result))
    return result


def new_velocity(agent: Agent, others: Sequence[Agent], tau: float, dt: float) -> tuple:
    """The ORCA velocity of one agent, given the agents it sees.

    Returns (velocity, feasible). feasible is False when the linear program has
    no solution and the velocity comes from the fallback program.
    """
    lines = [orca_line(agent, b, tau, dt) for b in others]  # @line L3
    count, v = lp2(lines, agent.vmax, agent.pref)  # @line L6
    if count < len(lines):  # @line L9
        return lp3(lines, count, agent.vmax, v), False  # @line L10
    return v, True  # @line L11


def step(agents: Sequence[Agent], tau: float, dt: float, sensing: Optional[float] = None) -> tuple:
    """One synchronous step: every agent computes its velocity, then all move.

    Returns (new agents, True if every linear program was feasible).
    """
    new = []
    all_feasible = True
    for i, a in enumerate(agents):  # @line L1
        others = [
            b for k, b in enumerate(agents)
            if k != i and (sensing is None or norm(sub(b.position, a.position)) <= sensing)
        ]  # @line L2
        v, ok = new_velocity(a, others, tau, dt)
        all_feasible = all_feasible and ok
        new.append(a._replace(velocity=v))
    moved = [a._replace(position=add(a.position, mul(a.velocity, dt))) for a in new]  # @line L12
    return moved, all_feasible


def time_to_collision(pa, va, pb, vb, rad) -> float:
    """First time t >= 0 at which the discs touch with constant velocities, or inf."""
    p = sub(pb, pa)
    v = sub(va, vb)
    a = dot(v, v)
    b = dot(p, v)
    c = dot(p, p) - rad * rad
    if c <= 0.0:
        return 0.0
    disc = b * b - a * c
    if a <= 0.0 or b <= 0.0 or disc < 0.0:
        return math.inf
    return (b - math.sqrt(disc)) / a
