# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contextual-bandit/. The authors are listed in prov/FHH31V.jsonl.

"""LinUCB with disjoint linear models (Li, Chu, Langford and Schapire 2010, Algorithm 1).

Each arm a has its own ridge regression: A_a = I + sum x x^T over the rounds it was
pulled, b_a = sum r x. The inverse of A_a is kept up to date with the
Sherman-Morrison formula, so a round costs O(K d^2) and no matrix is inverted.
"""

import math
import random
from typing import Callable, Sequence

Vector = list
Matrix = list


def identity(d: int, one=1.0) -> Matrix:
    return [[one if i == j else 0 * one for j in range(d)] for i in range(d)]


def mat_vec(M: Matrix, x: Sequence) -> Vector:
    return [sum(m * v for m, v in zip(row, x)) for row in M]


def dot(x: Sequence, y: Sequence):
    return sum(a * b for a, b in zip(x, y))


def sherman_morrison(A_inv: Matrix, x: Sequence) -> Matrix:
    """(A + x x^T)^{-1} from a symmetric A^{-1}: A^{-1} - (A^{-1} x)(A^{-1} x)^T / (1 + x^T A^{-1} x)."""
    u = mat_vec(A_inv, x)
    denom = 1 + dot(x, u)
    d = len(x)
    return [[A_inv[i][j] - u[i] * u[j] / denom for j in range(d)] for i in range(d)]


class LinUCB:
    """Disjoint LinUCB. Works with floats, or with Fractions when alpha is 0."""

    def __init__(self, k: int, d: int, alpha: float, one=1.0) -> None:
        self.alpha = alpha
        self.A_inv = [identity(d, one) for _ in range(k)]  # @line L1
        self.b = [[0 * one] * d for _ in range(k)]

    def scores(self, contexts: Sequence[Sequence]) -> list:
        out = []
        for a, x in enumerate(contexts):  # @line L3
            theta = mat_vec(self.A_inv[a], self.b[a])  # @line L4
            width = dot(x, mat_vec(self.A_inv[a], x))
            bonus = self.alpha * math.sqrt(width) if self.alpha else 0
            out.append(dot(theta, x) + bonus)  # @line L5
        return out

    def choose(self, contexts: Sequence[Sequence]) -> int:
        p = self.scores(contexts)
        return max(range(len(p)), key=lambda a: p[a])  # @line L6

    def update(self, a: int, x: Sequence, r) -> None:
        self.A_inv[a] = sherman_morrison(self.A_inv[a], x)  # @line L8
        self.b[a] = [bi + r * xi for bi, xi in zip(self.b[a], x)]  # @line L9


def run_linucb(
    contexts: Callable[[int], list],
    reward: Callable[[int, int, Sequence], float],
    k: int,
    d: int,
    n: int,
    alpha: float,
) -> list[int]:
    """Run LinUCB for n rounds. contexts(t) gives one feature vector per arm."""
    policy = LinUCB(k, d, alpha)
    actions = []
    for t in range(n):  # @line L2
        xs = contexts(t)
        a = policy.choose(xs)
        r = reward(t, a, xs[a])  # @line L7
        policy.update(a, xs[a], r)
        actions.append(a)
    return actions


class LinearInstance:
    """A seeded disjoint linear bandit: arm a has a hidden theta_a, and the reward of
    arm a in context x is theta_a . x plus Gaussian noise. All arms see the same context."""

    def __init__(self, k: int, d: int, n: int, rng: random.Random, noise: float = 0.1) -> None:
        self.thetas = [unit([rng.gauss(0, 1) for _ in range(d)]) for _ in range(k)]
        self.xs = [unit([rng.gauss(0, 1) for _ in range(d)]) for _ in range(n)]
        self.noise = [rng.gauss(0, noise) for _ in range(n)]
        self.k = k

    def contexts(self, t: int) -> list:
        return [self.xs[t]] * self.k

    def reward(self, t: int, a: int, x: Sequence) -> float:
        return dot(self.thetas[a], x) + self.noise[t]

    def regret(self, actions: Sequence[int]) -> list[float]:
        """Cumulative pseudo-regret after each round."""
        out, acc = [], 0.0
        for t, a in enumerate(actions):
            means = [dot(th, self.xs[t]) for th in self.thetas]
            acc += max(means) - means[a]
            out.append(acc)
        return out


def unit(v: Sequence[float]) -> list[float]:
    s = math.sqrt(sum(x * x for x in v))
    return [x / s for x in v]
