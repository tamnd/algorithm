# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/statistical-query-model/. The authors are listed in prov/ASCCKX.jsonl.
"""The statistical query model of Kearns (1998): oracles, simulators, a learner and a lower bound.

A query is a function chi(x, y) -> [0, 1] on an input x in {0, 1}^d and a label y in {0, 1}. The oracle
STAT(chi, tau) returns some value within tau of E[chi(x, c(x))], where x is drawn from the input
distribution D and c is the target. Inputs are drawn from a product distribution: x_i = 1 with
probability p[i], independently.
"""

import math
import random
from itertools import product
from typing import Callable

Point = tuple[int, ...]
Query = Callable[[Point, int], float]
Target = Callable[[Point], int]


def points(p: list[float]) -> list[tuple[Point, float]]:
    """Every input with its probability under the product distribution."""
    out = []
    for x in product((0, 1), repeat=len(p)):
        w = 1.0
        for xi, pi in zip(x, p):
            w *= pi if xi else 1 - pi
        out.append((x, w))
    return out


def draw_point(p: list[float], rng: random.Random) -> Point:
    return tuple(int(rng.random() < pi) for pi in p)


def expectation(chi: Query, target: Target, p: list[float]) -> float:
    return sum(w * chi(x, target(x)) for x, w in points(p))


class ExactOracle:
    """Answers every query with the exact expectation. Counts the queries."""

    def __init__(self, target: Target, p: list[float]):
        self.target, self.p, self.calls = target, p, 0

    def stat(self, chi: Query, tau: float) -> float:
        self.calls += 1
        return expectation(chi, self.target, self.p)


class AdversarialOracle(ExactOracle):
    """Moves every answer by tau, in the direction given by sign (+1, -1) or chosen at random (0)."""

    def __init__(self, target: Target, p: list[float], sign: int, seed: int = 0):
        super().__init__(target, p)
        self.sign, self.rng = sign, random.Random(seed)

    def stat(self, chi: Query, tau: float) -> float:
        s = self.sign or self.rng.choice((-1, 1))
        return super().stat(chi, tau) + s * tau


class SampleOracle:
    """Simulates STAT from labeled examples: m = ceil(ln(2q/delta) / (2 tau^2)) fresh examples per query.
    By Hoeffding and the union bound, all q answers are within tau with probability at least 1 - delta."""

    def __init__(self, target: Target, p: list[float], q: int, delta: float, rng: random.Random):
        self.target, self.p, self.q, self.delta, self.rng = target, p, q, delta, rng
        self.calls = self.examples = 0

    def sample_size(self, tau: float) -> int:
        return math.ceil(math.log(2 * self.q / self.delta) / (2 * tau * tau))

    def stat(self, chi: Query, tau: float) -> float:
        self.calls += 1
        m = self.sample_size(tau)
        self.examples += m
        total = 0.0
        for _ in range(m):
            x = draw_point(self.p, self.rng)
            total += chi(x, self.target(x))
        return total / m


class NoisySampleOracle(SampleOracle):
    """Simulates STAT from examples whose labels are flipped independently with a known rate eta < 1/2.

    E[chi(x, y_noisy)] = (1 - 2 eta) E[chi(x, c(x))] + eta E[chi(x, 0) + chi(x, 1)], so the answer is
    (noisy mean - eta * s) / (1 - 2 eta). Both means are estimated to t = tau (1 - 2 eta) / 2 from the same
    m = ceil(2 ln(4q/delta) / t^2) examples; the total error is at most tau (1 + eta) / 2 < tau."""

    def __init__(self, target: Target, p: list[float], eta: float, q: int, delta: float, rng: random.Random):
        super().__init__(target, p, q, delta, rng)
        self.eta = eta

    def sample_size(self, tau: float) -> int:
        t = tau * (1 - 2 * self.eta) / 2
        return math.ceil(2 * math.log(4 * self.q / self.delta) / (t * t))

    def stat(self, chi: Query, tau: float) -> float:
        self.calls += 1
        m = self.sample_size(tau)
        self.examples += m
        noisy = s = 0.0
        for _ in range(m):
            x = draw_point(self.p, self.rng)
            y = self.target(x) ^ int(self.rng.random() < self.eta)
            noisy += chi(x, y)
            s += chi(x, 0) + chi(x, 1)
        return (noisy / m - self.eta * s / m) / (1 - 2 * self.eta)


# Conjunctions. A literal j in 0..2d-1 is variable j // 2, negated when j is odd.

def literal_value(j: int, x: Point) -> int:
    v = x[j // 2]
    return 1 - v if j % 2 else v


def conjunction(lits: tuple[int, ...]) -> Target:
    return lambda x: int(all(literal_value(j, x) for j in lits))


def learn_conjunction(oracle, d: int, eps: float) -> tuple[int, ...]:
    """2d queries P[literal false and label 1] with tolerance tau = eps / (4d). Keep a literal if the
    answer is at most tau. Every target literal is kept, so h(x) = 1 implies c(x) = 1, and each kept
    literal adds at most 2 tau = eps / (2d) to the error."""
    tau = eps / (4 * d)
    kept = []
    for j in range(2 * d):
        chi = lambda x, y, j=j: float(literal_value(j, x) == 0 and y == 1)
        if oracle.stat(chi, tau) <= tau:
            kept.append(j)
    return tuple(kept)


def error(h: Target, c: Target, p: list[float]) -> float:
    return sum(w for x, w in points(p) if h(x) != c(x))


# Parities under the uniform distribution: the lower bound.

def parity(s: tuple[int, ...]) -> Target:
    """c_S(x) = sum of x_i over i in S, mod 2. S is a 0/1 indicator tuple."""
    return lambda x: sum(a & b for a, b in zip(s, x)) & 1


def fourier_coefficient(f: Callable[[Point], float], s: tuple[int, ...], d: int) -> float:
    """f^(S) = E[f(x) (-1)^(S . x)] under the uniform distribution."""
    return sum(f(x) * (-1) ** sum(a & b for a, b in zip(s, x)) for x in product((0, 1), repeat=d)) / 2 ** d


def adversary_answer(chi: Query, d: int) -> float:
    """E[g] + E[h] / 2, where chi(x, y) = g(x) + y h(x). It does not depend on the parity S, and it is the
    true answer E[g] + E[h]/2 - h^(S)/2 for every S with h^(S) = 0."""
    xs = list(product((0, 1), repeat=d))
    return sum(chi(x, 0) + chi(x, 1) for x in xs) / (2 * len(xs))


def surviving_parities(queries: list[Query], tau: float, d: int) -> list[tuple[int, ...]]:
    """The parities for which the adversary's answer to every query is within tau of the truth."""
    answers = [adversary_answer(chi, d) for chi in queries]
    out = []
    for s in product((0, 1), repeat=d):
        c = parity(s)
        u = [(x, 1.0 / 2 ** d) for x in product((0, 1), repeat=d)]
        if all(abs(sum(w * chi(x, c(x)) for x, w in u) - a) <= tau for chi, a in zip(queries, answers)):
            out.append(s)
    return out


if __name__ == "__main__":
    d, eps = 8, 0.2
    c = conjunction((0, 5, 8))  # x0 and (not x2) and x4
    for p in ([0.5] * d, [0.8, 0.97, 0.4, 0.5, 0.7, 0.5, 0.5, 0.99]):
        for sign in (1, -1):
            o = AdversarialOracle(c, p, sign)
            h = learn_conjunction(o, d, eps)
            print(p[:2], sign, h, o.calls, round(error(conjunction(h), c, p), 4), round(expectation(
                lambda x, y: float(y), c, p), 4))
    d = 3
    for eta in (0.0, 0.2):
        rng = random.Random(1)
        c = conjunction((0, 3))
        o = NoisySampleOracle(c, [0.5] * d, eta, 2 * d, 0.1, rng) if eta else SampleOracle(c, [0.5] * d, 2 * d, 0.1, rng)
        h = learn_conjunction(o, d, 0.5)
        print("eta", eta, h, o.examples, round(error(conjunction(h), c, [0.5] * d), 4))
