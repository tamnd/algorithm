# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boids/. The authors are listed in prov/PDJW2G.jsonl.

"""Boids: Reynolds's three steering rules for a flock of agents in the plane.

Each boid i looks at the boids within the radius R and computes
  separation  sum over close neighbors of (p_i - p_j) / |p_i - p_j|^2,
  alignment   mean velocity of the neighbors minus v_i,
  cohesion    mean position of the neighbors minus p_i.
The weighted rules give a steering acceleration. The acceleration is limited
(optionally by prioritized allocation, separation first), the velocity is
kept between a minimum and a maximum speed, and all boids move at once.
The rules are heuristics; nothing here guarantees a flock.
"""

import math
import random
from dataclasses import dataclass
from typing import Sequence

Vec = tuple[float, float]


@dataclass
class Params:
    radius: float = 1.0        # neighbor radius R
    sep_radius: float = 0.4    # separation acts only within this distance
    w_sep: float = 1.5
    w_ali: float = 1.0
    w_coh: float = 1.0
    max_accel: float = math.inf
    min_speed: float = 0.0
    max_speed: float = math.inf
    dt: float = 0.1
    prioritized: bool = False  # allocate max_accel to separation, then alignment, then cohesion


def _norm(v: Vec) -> float:
    return math.hypot(v[0], v[1])


def _scale(v: Vec, s: float) -> Vec:
    return (v[0] * s, v[1] * s)


def _add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1])


def _clamp_norm(v: Vec, lo: float, hi: float) -> Vec:
    n = _norm(v)
    if n > hi:
        return _scale(v, hi / n)
    if 0 < n < lo:
        return _scale(v, lo / n)
    return v


def neighbors(i: int, pos: Sequence[Vec], radius: float) -> list[int]:
    return [j for j in range(len(pos)) if j != i and math.dist(pos[i], pos[j]) <= radius]


def rules(i: int, pos: Sequence[Vec], vel: Sequence[Vec], prm: Params) -> tuple[Vec, Vec, Vec]:
    """The three raw steering vectors (separation, alignment, cohesion) of boid i."""
    nb = neighbors(i, pos, prm.radius)  # @line L3
    if not nb:
        return (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)
    px, py = pos[i]
    sx = sy = 0.0
    for j in nb:  # @line L4
        dx, dy = px - pos[j][0], py - pos[j][1]
        d2 = dx * dx + dy * dy
        if 0 < d2 <= prm.sep_radius ** 2:
            sx, sy = sx + dx / d2, sy + dy / d2
    k = len(nb)
    mvx = sum(vel[j][0] for j in nb) / k
    mvy = sum(vel[j][1] for j in nb) / k
    ali = (mvx - vel[i][0], mvy - vel[i][1])  # @line L5
    cx = sum(pos[j][0] for j in nb) / k
    cy = sum(pos[j][1] for j in nb) / k
    coh = (cx - px, cy - py)  # @line L6
    return (sx, sy), ali, coh


def allocate(requests: Sequence[Vec], budget: float) -> Vec:
    """Prioritized acceleration allocation: take requests in order until the budget is used."""
    acc, left = (0.0, 0.0), budget
    for r in requests:
        n = _norm(r)
        if n <= left:
            acc, left = _add(acc, r), left - n
        else:
            if n > 0:
                acc = _add(acc, _scale(r, left / n))
            break
    return acc


def steer(i: int, pos: Sequence[Vec], vel: Sequence[Vec], prm: Params) -> Vec:
    sep, ali, coh = rules(i, pos, vel, prm)
    req = [_scale(sep, prm.w_sep), _scale(ali, prm.w_ali), _scale(coh, prm.w_coh)]  # @line L7
    if prm.prioritized:
        return allocate(req, prm.max_accel)
    acc = _add(_add(req[0], req[1]), req[2])
    return _clamp_norm(acc, 0.0, prm.max_accel)


def step(pos: Sequence[Vec], vel: Sequence[Vec], prm: Params) -> tuple[list[Vec], list[Vec]]:
    """One synchronous step of the whole flock (semi-implicit Euler)."""
    acc = [steer(i, pos, vel, prm) for i in range(len(pos))]  # @line L2
    new_v = [_clamp_norm(_add(v, _scale(a, prm.dt)), prm.min_speed, prm.max_speed)  # @line L8
             for v, a in zip(vel, acc)]
    new_p = [_add(p, _scale(v, prm.dt)) for p, v in zip(pos, new_v)]  # @line L9
    return new_p, new_v  # @line L10


def simulate(pos: Sequence[Vec], vel: Sequence[Vec], prm: Params, steps: int):
    p = [tuple(map(float, x)) for x in pos]
    v = [tuple(map(float, x)) for x in vel]
    for _ in range(steps):  # @line L1
        p, v = step(p, v, prm)
    return p, v


def order_parameter(vel: Sequence[Vec]) -> float:
    """|mean of the unit headings|: 1 when all boids head the same way, near 0 when random."""
    hx = hy = 0.0
    for v in vel:
        n = _norm(v)
        if n > 0:
            hx, hy = hx + v[0] / n, hy + v[1] / n
    return math.hypot(hx, hy) / len(vel)


def random_flock(n: int, rng: random.Random, box: float = 3.0, speed: float = 1.0):
    pos = [(rng.uniform(0, box), rng.uniform(0, box)) for _ in range(n)]
    vel = []
    for _ in range(n):
        a = rng.uniform(0, 2 * math.pi)
        vel.append((speed * math.cos(a), speed * math.sin(a)))
    return pos, vel
