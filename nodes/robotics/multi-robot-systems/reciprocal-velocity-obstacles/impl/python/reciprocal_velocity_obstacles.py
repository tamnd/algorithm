# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reciprocal-velocity-obstacles/. The authors are listed in prov/VJAYA8.jsonl.

"""Reciprocal velocity obstacles (RVO) for disc robots in the plane.

This follows van den Berg, Lin and Manocha (2008). The velocity obstacle of
robot A for a robot B is the set of velocities of A that lead to a collision
with B at some time if B keeps its velocity. The reciprocal velocity obstacle
moves the apex of that cone halfway: a new velocity v' of A is inside
RVO_A|B when 2 v' - v_A - v_B is a relative velocity that leads to a collision.

Each robot scores a fixed set of candidate velocities in its speed disc with
the penalty of the paper, weight / (time to collision) + |v' - v_pref|, and
takes the candidate with the smallest penalty. The paper draws random samples;
this file uses a fixed polar grid that is symmetric under v -> -v, so that two
robots in mirror image situations pick mirror image velocities. Vectors are
tuples (x, y). Robots are holonomic discs.
"""

import math
from typing import NamedTuple, Optional, Sequence


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


class Agent(NamedTuple):
    position: tuple
    velocity: tuple
    radius: float
    vmax: float
    pref: tuple  # preferred velocity


def time_to_collision(rel_pos, rel_vel, rad) -> float:
    """First t >= 0 with |t * rel_vel - rel_pos| < rad, or inf if the discs never overlap.

    rel_pos is p_B - p_A and rel_vel is the velocity of A relative to B. A
    grazing contact, where the discs only touch, does not count.
    """
    c = dot(rel_pos, rel_pos) - rad * rad
    if c <= 0.0:
        return 0.0
    a = dot(rel_vel, rel_vel)
    b = dot(rel_pos, rel_vel)
    disc = b * b - a * c
    if a == 0.0 or b <= 0.0 or disc <= 0.0:
        return math.inf
    return (b - math.sqrt(disc)) / a


def rvo_relative_velocity(a: Agent, b: Agent, v) -> tuple:
    """The relative velocity 2 v - v_A - v_B that RVO_A|B tests."""
    return sub(sub(mul(v, 2.0), a.velocity), b.velocity)


def in_rvo(a: Agent, b: Agent, v) -> bool:
    """True if the candidate velocity v of A lies in RVO_A|B."""
    rel = sub(b.position, a.position)
    return time_to_collision(rel, rvo_relative_velocity(a, b, v), a.radius + b.radius) < math.inf


def candidates(agent: Agent, rings: int = 6, spokes: int = 32) -> list:
    """The preferred velocity (clipped to the speed disc) and a polar grid in the disc.

    The spokes are measured from the direction of the preferred velocity, so a
    robot whose preferred velocity is the negative of another's gets the
    negated list in the same order. Ties then break the same way for both.
    """
    pref = agent.pref
    n = norm(pref)
    if n > agent.vmax:
        pref = mul(pref, agent.vmax / n)
    u = (pref[0] / n, pref[1] / n) if n > 0.0 else (1.0, 0.0)
    out = [pref, (0.0, 0.0)]
    for i in range(1, rings + 1):
        s = agent.vmax * i / rings
        for k in range(spokes):
            th = 2.0 * math.pi * k / spokes
            c, d = math.cos(th), math.sin(th)
            out.append((s * (c * u[0] - d * u[1]), s * (d * u[0] + c * u[1])))
    return out


def penalty(agent: Agent, others: Sequence[Agent], v, weight: float) -> float:
    tc = math.inf  # @line L3
    for b in others:  # @line L4
        w = rvo_relative_velocity(agent, b, v)  # @line L5
        tc = min(tc, time_to_collision(sub(b.position, agent.position), w, agent.radius + b.radius))  # @line L6
    if tc == 0.0:
        return math.inf
    return weight / tc + norm(sub(v, agent.pref))  # @line L7


def new_velocity(agent: Agent, others: Sequence[Agent], weight: float = 1.0, rings: int = 6, spokes: int = 32) -> tuple:
    """The RVO velocity of one robot: the candidate with the smallest penalty.

    Ties go to the earlier candidate in the list.
    """
    best, best_v = math.inf, None
    for v in candidates(agent, rings, spokes):  # @line L2
        pen = penalty(agent, others, v, weight)
        if pen < best:
            best, best_v = pen, v
    if best_v is None:
        best_v = (0.0, 0.0)  # every candidate overlaps already: stop
    return best_v  # @line L8


def step(agents: Sequence[Agent], dt: float, weight: float = 1.0, sensing: Optional[float] = None,
         rings: int = 6, spokes: int = 32) -> list:
    """One synchronous step: every robot picks its velocity from the same snapshot, then all move."""
    new = []
    for i, a in enumerate(agents):  # @line L1
        others = [
            b for k, b in enumerate(agents)
            if k != i and (sensing is None or norm(sub(b.position, a.position)) <= sensing)
        ]
        new.append(a._replace(velocity=new_velocity(a, others, weight, rings, spokes)))
    return [a._replace(position=add(a.position, mul(a.velocity, dt))) for a in new]  # @line L9
