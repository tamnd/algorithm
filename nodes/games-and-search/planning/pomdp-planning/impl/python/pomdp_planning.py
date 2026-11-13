# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pomdp-planning/. The authors are listed in prov/J05MEA.jsonl.

"""Exact finite-horizon POMDP planning, offline and online.

A model has: states, actions, observations (lists); T[s][a] a dict of next
states to probabilities; Z[a][s2][o] the probability of o after a led to s2;
R[s][a] the expected reward. Use Fraction values for exact answers.

Offline: alpha vectors by enumeration (Monahan), with pruning.
Online: the value of one belief by search in the tree of beliefs (expectimax).
"""

from fractions import Fraction
from itertools import product
from typing import Dict, List, Tuple

Vector = Tuple[Fraction, ...]


class Pomdp:
    def __init__(self, states, actions, observations, T, Z, R, gamma=Fraction(1)):
        self.S, self.A, self.O = list(states), list(actions), list(observations)
        self.T, self.Z, self.R, self.gamma = T, Z, R, gamma

    # ---- beliefs ----
    def update(self, b: Dict, a, o):
        """Returns (Pr(o | b, a), the next belief)."""
        joint = {}
        for s, p in b.items():
            if p == 0:
                continue
            for t, q in self.T[s][a].items():
                joint[t] = joint.get(t, 0) + p * q * self.Z[a][t][o]
        z = sum(joint.values())
        if z == 0:
            return Fraction(0), None
        return z, {t: x / z for t, x in joint.items() if x != 0}

    def reward(self, b: Dict, a):
        return sum(p * self.R[s][a] for s, p in b.items())

    # ---- online: search in the tree of beliefs ----
    def value(self, b: Dict, horizon: int) -> Tuple[Fraction, object]:
        """V_H(b) and a best first action, by expectimax over actions and observations."""
        if horizon == 0:
            return Fraction(0), None
        best, best_a = None, None
        for a in self.A:
            q = self.reward(b, a)
            for o in self.O:
                z, nb = self.update(b, a, o)
                if z:
                    q += self.gamma * z * self.value(nb, horizon - 1)[0]
            if best is None or q > best:
                best, best_a = q, a
        return best, best_a

    # ---- offline: alpha vectors ----
    def backup_vector(self, a, choice: Dict) -> Vector:
        """The vector of the plan: do a, then follow choice[o] after the observation o."""
        out = []
        for s in self.S:
            x = self.R[s][a]
            for t, q in self.T[s][a].items():
                for o in self.O:
                    x += self.gamma * q * self.Z[a][t][o] * choice[o][self.S.index(t)]
            out.append(x)
        return tuple(out)

    def alpha_vectors(self, horizon: int, prune=None) -> List[Tuple[object, Vector]]:
        """Gamma_H as (first action, vector) pairs; prune is applied after each step."""
        gamma: List[Tuple[object, Vector]] = [(None, tuple(Fraction(0) for _ in self.S))]
        for _ in range(horizon):
            vecs = [v for _, v in gamma]
            new = []
            for a in self.A:
                for pick in product(range(len(vecs)), repeat=len(self.O)):
                    choice = {o: vecs[i] for o, i in zip(self.O, pick)}
                    new.append((a, self.backup_vector(a, choice)))
            gamma = prune(new) if prune else new
        return gamma


def dot(alpha: Vector, b: Dict, states) -> Fraction:
    return sum(alpha[i] * b.get(s, 0) for i, s in enumerate(states))


def value_from_alphas(gamma, b: Dict, states) -> Fraction:
    return max(dot(v, b, states) for _, v in gamma)


def prune_dominated(gamma):
    """Remove duplicates and vectors that another vector beats or ties in every state."""
    out = []
    for i, (a, v) in enumerate(gamma):
        dominated = False
        for j, (_, w) in enumerate(gamma):
            if i != j and all(x <= y for x, y in zip(v, w)) and (v != w or j < i):
                dominated = True
                break
        if not dominated:
            out.append((a, v))
    return out


def prune_two_states(gamma):
    """Exact pruning for |S| = 2: keep the vectors that are strictly best on some interval of [0, 1].

    A vector (x0, x1) is the line x1 + (x0 - x1) p at the belief p = b(first state).
    The kept vectors are the pieces of the upper envelope, from p = 0 to p = 1.
    """
    gamma = prune_dominated(gamma)
    if not gamma:
        return gamma
    line = lambda v, p: v[1] + (v[0] - v[1]) * p
    p = Fraction(0)
    # start with the best line at p = 0, ties broken by the larger slope
    cur = max(gamma, key=lambda av: (line(av[1], p), av[1][0] - av[1][1]))
    out = [cur]
    while True:
        slope = cur[1][0] - cur[1][1]
        nxt, nxt_p = None, None
        for av in gamma:
            s2 = av[1][0] - av[1][1]
            if s2 <= slope:
                continue
            q = (cur[1][1] - av[1][1]) / (s2 - slope)  # where the two lines cross
            if q < p or q >= 1:
                continue
            key = (q, -s2)
            if nxt is None or key < (nxt_p, -(nxt[1][0] - nxt[1][1])):
                nxt, nxt_p = av, q
        if nxt is None:
            return out
        cur, p = nxt, nxt_p
        out.append(cur)


def tiger(accuracy=Fraction(17, 20), listen=Fraction(-1), win=Fraction(10), lose=Fraction(-100), gamma=Fraction(1)):
    """The tiger problem of Kaelbling, Littman and Cassandra (1998). The state is the tiger's side."""
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
        "left": {"listen": listen, "open-left": lose, "open-right": win},
        "right": {"listen": listen, "open-left": win, "open-right": lose},
    }
    return Pomdp(S, A, O, T, Z, R, gamma)
