# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gittins-index/. The authors are listed in prov/7M9CFD.jsonl.

"""Gittins indices of a finite Markov arm, by the restart problem of Katehakis and Veinott (1987).

An arm has states 0 .. m-1, a reward r[x] for a pull in state x, and a transition
matrix P: a pull in state x moves the arm to y with probability P[x][y]. Arms that
are not pulled do not move. Rewards are discounted by gamma per pull.
"""

import itertools
from fractions import Fraction
from typing import Sequence


def restart_index(r: Sequence[float], P: Sequence[Sequence[float]], gamma: float, x: int, tol: float = 1e-12) -> float:
    """Gittins index of state x: (1 - gamma) V(x), where V solves the restart problem

    V(y) = max( r[y] + gamma sum_z P[y][z] V(z),  r[x] + gamma sum_z P[x][z] V(z) ).

    In each state the arm may continue from y or restart from x. Value iteration
    converges since the map is a gamma-contraction.
    """
    m = len(r)
    v = [0.0] * m  # @line L1
    while True:  # @line L2
        restart = r[x] + gamma * sum(P[x][z] * v[z] for z in range(m))  # @line L3
        new = [max(r[y] + gamma * sum(P[y][z] * v[z] for z in range(m)), restart) for y in range(m)]  # @line L4
        diff = max(abs(a - b) for a, b in zip(new, v))
        v = new
        if diff * gamma / (1 - gamma) < tol:  # @line L5
            return (1 - gamma) * v[x]  # @line L6


def gittins_indices(r: Sequence[float], P: Sequence[Sequence[float]], gamma: float) -> list[float]:
    return [restart_index(r, P, gamma, x) for x in range(len(r))]


def retirement_index(r, P, gamma: float, x: int, tol: float = 1e-10) -> float:
    """Whittle (1980): the index is (1 - gamma) M, where M is the smallest lump sum
    that makes retiring in state x as good as going on. Found by bisection."""
    m = len(r)
    lo, hi = min(r) / (1 - gamma), max(r) / (1 - gamma)

    def value_of_continuing(M: float) -> float:
        v = [M] * m
        while True:
            new = [max(M, r[y] + gamma * sum(P[y][z] * v[z] for z in range(m))) for y in range(m)]
            diff = max(abs(a - b) for a, b in zip(new, v))
            v = new
            if diff * gamma / (1 - gamma) < tol / 10:
                break
        return r[x] + gamma * sum(P[x][z] * v[z] for z in range(m))

    while hi - lo > tol:
        mid = (lo + hi) / 2
        if value_of_continuing(mid) > mid:
            lo = mid
        else:
            hi = mid
    return (1 - gamma) * (lo + hi) / 2


def chain_index(rewards: Sequence[Fraction], tail: Fraction, gamma: Fraction) -> Fraction:
    """Exact index of the first state of a deterministic chain.

    The arm pays rewards[0], rewards[1], ... in turn and then pays tail for ever.
    The index is the largest discounted average sum_{t<tau} gamma^t r_t / sum_{t<tau} gamma^t
    over stopping times tau >= 1; for a deterministic arm these are the prefixes and
    the whole infinite sequence.
    """
    best = None
    num, den, g = Fraction(0), Fraction(0), Fraction(1)
    for x in rewards:
        num += g * x
        den += g
        g *= gamma
        best = num / den if best is None else max(best, num / den)
    whole = (num + g * tail / (1 - gamma)) * (1 - gamma)
    return whole if best is None else max(best, whole)


def bernoulli_index(a: int, b: int, gamma: float, depth: int = 300, tol: float = 1e-9) -> float:
    """Index of a Bernoulli arm with a Beta(a, b) posterior on its mean.

    The state is the posterior (a + s, b + f). Calibration by a retirement reward,
    with backward induction over the tree of posteriors, cut at s + f = depth, where
    the mean is taken as known.
    """
    lo, hi = 0.0, 1.0 / (1 - gamma)
    while hi - lo > tol:
        M = (lo + hi) / 2
        nxt = None
        for k in range(depth, -1, -1):  # k = s + f
            cur = []
            for s in range(k + 1):
                p = (a + s) / (a + b + k)
                if nxt is None:
                    cont = p / (1 - gamma)
                else:
                    cont = p + gamma * (p * nxt[s + 1] + (1 - p) * nxt[s])
                cur.append(max(M, cont))
            nxt = cur
        # nxt[0] is the value of the root (a, b) with the option to retire for M.
        if nxt[0] > M + 1e-15:
            lo = M
        else:
            hi = M
    return (1 - gamma) * (lo + hi) / 2


def bernoulli_tree_arm(a: int, b: int, depth: int) -> tuple[list[float], list[list[float]], list[tuple[int, int]]]:
    """The tree of Beta posteriors up to s + f = depth as an explicit Markov arm.

    Leaves keep their posterior mean for ever (they move to themselves). The reward of
    a state is its posterior mean, which is the expected reward of a pull.
    """
    states = [(s, k - s) for k in range(depth + 1) for s in range(k + 1)]
    where = {st: i for i, st in enumerate(states)}
    m = len(states)
    r = [0.0] * m
    P = [[0.0] * m for _ in range(m)]
    for i, (s, f) in enumerate(states):
        p = (a + s) / (a + b + s + f)
        r[i] = p
        if s + f == depth:
            P[i][i] = 1.0
        else:
            P[i][where[(s + 1, f)]] += p
            P[i][where[(s, f + 1)]] += 1 - p
    return r, P, states


def optimal_values(arms, gamma: float, tol: float = 1e-12) -> dict:
    """Value iteration over the joint state space of several arms (only the pulled arm moves)."""
    joint = list(itertools.product(*[range(len(r)) for r, _ in arms]))
    v = {s: 0.0 for s in joint}
    while True:
        new = {}
        for s in joint:
            best = -float("inf")
            for a, (r, P) in enumerate(arms):
                q = r[s[a]]
                for y, pr in enumerate(P[s[a]]):
                    if pr:
                        q += gamma * pr * v[s[:a] + (y,) + s[a + 1 :]]
                best = max(best, q)
            new[s] = best
        diff = max(abs(new[s] - v[s]) for s in joint)
        v = new
        if diff * gamma / (1 - gamma) < tol:
            return v


def policy_values(arms, gamma: float, choose, tol: float = 1e-12) -> dict:
    """Value of the stationary policy choose(joint state) -> arm, by iteration."""
    joint = list(itertools.product(*[range(len(r)) for r, _ in arms]))
    v = {s: 0.0 for s in joint}
    while True:
        new = {}
        for s in joint:
            a = choose(s)
            r, P = arms[a]
            q = r[s[a]]
            for y, pr in enumerate(P[s[a]]):
                if pr:
                    q += gamma * pr * v[s[:a] + (y,) + s[a + 1 :]]
            new[s] = q
        diff = max(abs(new[s] - v[s]) for s in joint)
        v = new
        if diff * gamma / (1 - gamma) < tol:
            return v


def gittins_policy(arms, gamma: float):
    """The index policy: pull the arm whose current state has the largest index, ties to the first."""
    tables = [gittins_indices(r, P, gamma) for r, P in arms]
    return lambda s: max(range(len(arms)), key=lambda a: (tables[a][s[a]], -a))
