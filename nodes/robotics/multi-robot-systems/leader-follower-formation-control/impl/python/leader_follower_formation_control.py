# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leader-follower-formation-control/. The authors are listed in prov/P77YSV.jsonl.

"""Separation-bearing (l-psi) leader-follower control of unicycle robots.

A robot has the state (x, y, theta) and the inputs (v, omega), with
x' = v cos(theta), y' = v sin(theta), theta' = omega.

The follower controls its point P_F = (x_F + d cos theta_F, y_F + d sin theta_F),
at the distance d > 0 ahead of its wheel axle. The separation l and the bearing
psi are defined by P_F - p_L = l (cos(theta_L + psi), sin(theta_L + psi)), so psi
is measured from the heading of the leader. With gamma = theta_L + psi - theta_F,

    l'   = v_F cos(gamma) + d omega_F sin(gamma) - v_L cos(psi)
    psi' = (v_L sin(psi) - v_F sin(gamma) + d omega_F cos(gamma)) / l - omega_L.

The control below makes l' = a1 (l_d - l) and psi' = a2 (psi_d - psi).
"""

import math
from typing import Callable, Sequence

State = tuple  # (x, y, theta)


def wrap(a: float) -> float:
    """Wrap an angle to [-pi, pi)."""
    return (a + math.pi) % (2 * math.pi) - math.pi


def separation_bearing(leader: State, follower: State, d: float) -> tuple[float, float, float]:
    """Return (l, psi, gamma) of the follower with respect to its leader."""
    xl, yl, tl = leader
    xf, yf, tf = follower
    px, py = xf + d * math.cos(tf) - xl, yf + d * math.sin(tf) - yl
    l = math.hypot(px, py)
    psi = wrap(math.atan2(py, px) - tl)
    return l, psi, wrap(tl + psi - tf)


def follower_input(leader: State, vl: float, wl: float, follower: State, ld: float, psid: float,
                   d: float, a1: float, a2: float) -> tuple[float, float]:
    """The l-psi control law of one follower. Needs d > 0 and l > 0."""
    if d <= 0:
        raise ValueError("the offset d must be positive")
    l, psi, g = separation_bearing(leader, follower, d)  # @line L3
    a = a1 * (ld - l) + vl * math.cos(psi)  # @line L4
    b = l * (a2 * wrap(psid - psi) + wl) - vl * math.sin(psi)  # @line L5
    v = a * math.cos(g) - b * math.sin(g)  # @line L6
    w = (a * math.sin(g) + b * math.cos(g)) / d  # @line L7
    return v, w


def unicycle_rate(s: State, v: float, w: float) -> tuple[float, float, float]:
    return v * math.cos(s[2]), v * math.sin(s[2]), w


def all_inputs(states: Sequence[State], parent: Sequence[int], targets: Sequence[tuple],
               root_input: Callable[[float], tuple[float, float]], t: float, d: float,
               a1: float, a2: float) -> list[tuple[float, float]]:
    """Inputs of all robots. Robot 0 is the root; parent[i] < i for every follower i >= 1."""
    u = [root_input(t)]
    for i in range(1, len(states)):  # @line L2
        p = parent[i]
        ld, psid = targets[i]
        u.append(follower_input(states[p], u[p][0], u[p][1], states[i], ld, psid, d, a1, a2))
    return u


def simulate(states0: Sequence[State], parent: Sequence[int], targets: Sequence[tuple],
             root_input: Callable[[float], tuple[float, float]], t_end: float, h: float,
             d: float = 0.1, a1: float = 1.0, a2: float = 1.0) -> list[list[float]]:
    """Integrate the closed loop of a leader-follower tree with RK4 and fixed step h."""
    s = [list(map(float, q)) for q in states0]
    steps = max(1, round(t_end / h))
    h = t_end / steps
    t = 0.0

    def f(st, tt):
        u = all_inputs(st, parent, targets, root_input, tt, d, a1, a2)
        return [unicycle_rate(q, *ui) for q, ui in zip(st, u)]

    def add(st, k, c):
        return [[q[j] + c * kq[j] for j in range(3)] for q, kq in zip(st, k)]

    for _ in range(steps):  # @line L1
        k1 = f(s, t)
        k2 = f(add(s, k1, h / 2), t + h / 2)
        k3 = f(add(s, k2, h / 2), t + h / 2)
        k4 = f(add(s, k3, h), t + h)
        s = [[q[j] + h / 6 * (a[j] + 2 * b[j] + 2 * c[j] + e[j]) for j in range(3)]  # @line L8
             for q, a, b, c, e in zip(s, k1, k2, k3, k4)]
        t += h
    return s  # @line L9
