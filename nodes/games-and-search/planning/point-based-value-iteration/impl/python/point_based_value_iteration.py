# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/point-based-value-iteration/. The authors are listed in prov/M7E96B.jsonl.

"""Point-based value iteration (PBVI) for POMDPs, after Pineau, Gordon and Thrun.

A model has: S, A, O (lists); T[s][a] a dict of next states to probabilities;
Z[a][s2][o] the probability of o after a led to s2; R[s][a] the reward; gamma.
A belief is a tuple of probabilities in the order of S. A value function is a
list of (action, alpha vector) pairs. Use Fraction values for exact answers.
"""

import random
from fractions import Fraction
from typing import List, Optional, Sequence, Tuple

Vector = Tuple
Belief = Tuple


class Pomdp:
    def __init__(self, S, A, O, T, Z, R, gamma=Fraction(1)):
        self.S, self.A, self.O = list(S), list(A), list(O)
        self.T, self.Z, self.R, self.gamma = T, Z, R, gamma
        self.idx = {s: i for i, s in enumerate(self.S)}

    def update(self, b: Belief, a, o) -> Tuple[object, Optional[Belief]]:
        """(Pr(o | b, a), the next belief) by Bayes rule."""
        joint = [0] * len(self.S)
        for i, s in enumerate(self.S):
            if b[i]:
                for t, q in self.T[s][a].items():
                    joint[self.idx[t]] += b[i] * q * self.Z[a][t][o]
        z = sum(joint)
        if z == 0:
            return 0, None
        return z, tuple(x / z for x in joint)

    def project(self, alpha: Vector, a, o) -> Vector:
        """g(s) = the sum over s2 of T(s2 | s, a) Z(o | a, s2) alpha(s2)."""
        return tuple(
            sum(q * self.Z[a][t][o] * alpha[self.idx[t]] for t, q in self.T[s][a].items())
            for s in self.S
        )


def dot(alpha: Sequence, b: Sequence):
    return sum(x * y for x, y in zip(alpha, b))


def value(gamma_set: List[Tuple[object, Vector]], b: Belief):
    return max(dot(v, b) for _, v in gamma_set)


def backup(m: Pomdp, gamma_set: List[Tuple[object, Vector]], b: Belief) -> Tuple[object, Vector]:
    """The point-based backup: the best vector at b of the form R(., a) + gamma * sum_o g_{a,o}."""
    best = None
    for a in m.A:
        vec = [m.R[s][a] for s in m.S]
        for o in m.O:
            g = max((m.project(v, a, o) for _, v in gamma_set), key=lambda g: dot(g, b))  # @line L6
            vec = [x + m.gamma * y for x, y in zip(vec, g)]  # @line L7
        vec = tuple(vec)
        if best is None or dot(vec, b) > dot(best[1], b):
            best = (a, vec)
    return best  # @line L8


def improve(m: Pomdp, gamma_set, beliefs: Sequence[Belief]):
    """One PBVI sweep: back up at each belief, and drop duplicate vectors."""
    out, seen = [], set()
    for b in beliefs:
        a, v = backup(m, gamma_set, b)
        if v not in seen:
            seen.add(v)
            out.append((a, v))
    return out


def l1(b: Belief, c: Belief):
    return sum(abs(x - y) for x, y in zip(b, c))


def sample(dist, rng: random.Random):
    """dist is a list of (probability, item) pairs."""
    x = rng.random()
    acc = 0.0
    for p, item in dist:
        acc += float(p)
        if x < acc:
            return item
    return dist[-1][1]


def expand(m: Pomdp, beliefs: List[Belief], rng: random.Random) -> List[Belief]:
    """Stochastic simulation with exploratory action: for each belief, try each action once by
    simulation, and keep the successor belief that is farthest from the set in L1 distance."""
    new = list(beliefs)
    for b in beliefs:
        best, best_d = None, None
        for a in m.A:  # @line L9
            s = sample([(p, s) for p, s in zip(b, m.S) if p], rng)
            t = sample([(q, t) for t, q in m.T[s][a].items()], rng)
            o = sample([(m.Z[a][t][o], o) for o in m.O], rng)
            _, nb = m.update(b, a, o)
            d = min(l1(nb, c) for c in new)
            if best_d is None or d > best_d:
                best, best_d = nb, d
        if best_d and best not in new:  # @line L10
            new.append(best)
    return new


def pbvi(m: Pomdp, b0: Belief, expansions: int, sweeps: int, rng: random.Random, start=None, beliefs=None):
    """Run PBVI. start is the first value function: [(None, 0 vector)] for a finite horizon,
    or the vector R_min / (1 - gamma) for a discounted problem. Returns (value function, beliefs)."""
    B = list(beliefs) if beliefs else [tuple(b0)]  # @line L1
    if start is None:
        start = [(None, tuple(0 for _ in m.S))]
    G = list(start)
    for e in range(expansions + 1):  # @line L2
        for _ in range(sweeps):  # @line L3
            G = improve(m, G, B)
        if e < expansions:
            B = expand(m, B, rng)  # @line L4
    return G, B  # @line L5


def lower_start(m: Pomdp):
    """The vector R_min / (1 - gamma) in every state: the value of a policy, so a lower bound."""
    rmin = min(m.R[s][a] for s in m.S for a in m.A)
    return [(None, tuple(rmin / (1 - m.gamma) for _ in m.S))]


def tiger(accuracy=Fraction(17, 20), gamma=Fraction(1)):
    S = ["left", "right"]
    A = ["listen", "open-left", "open-right"]
    O = ["hear-left", "hear-right"]
    half = Fraction(1, 2)
    T = {s: {"listen": {s: Fraction(1)}, "open-left": {"left": half, "right": half}, "open-right": {"left": half, "right": half}} for s in S}
    Z = {
        "listen": {"left": {"hear-left": accuracy, "hear-right": 1 - accuracy}, "right": {"hear-left": 1 - accuracy, "hear-right": accuracy}},
        "open-left": {s: {o: half for o in O} for s in S},
        "open-right": {s: {o: half for o in O} for s in S},
    }
    R = {
        "left": {"listen": Fraction(-1), "open-left": Fraction(-100), "open-right": Fraction(10)},
        "right": {"listen": Fraction(-1), "open-left": Fraction(10), "open-right": Fraction(-100)},
    }
    return Pomdp(S, A, O, T, Z, R, gamma)
