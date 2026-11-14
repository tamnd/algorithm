# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/statistical-static-timing-analysis/. The authors are listed in prov/XMR9Q0.jsonl.

import math
from collections import deque
from typing import Mapping, NamedTuple, Sequence


class Canonical(NamedTuple):
    """A delay or arrival time in first-order canonical form.

    The value is mean + sum(coeffs[i] * Z_i) + rand * R, where the Z_i are the
    shared (global) sources of variation and R is a private source. All of
    them are independent standard normal variables, and R is independent of
    the private source of every other canonical form.
    """

    mean: float
    coeffs: tuple
    rand: float

    def variance(self) -> float:
        return sum(c * c for c in self.coeffs) + self.rand * self.rand

    def std(self) -> float:
        return math.sqrt(self.variance())


def constant(value: float, m: int) -> Canonical:
    return Canonical(float(value), (0.0,) * m, 0.0)


def pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def add(a: Canonical, b: Canonical) -> Canonical:
    """Sum of two canonical forms. Exact: means and coefficients add, and the
    private parts are independent, so their variances add."""
    coeffs = tuple(x + y for x, y in zip(a.coeffs, b.coeffs))  # @line L7
    return Canonical(a.mean + b.mean, coeffs, math.hypot(a.rand, b.rand))  # @line L8


def clark_max(a: Canonical, b: Canonical):
    """Statistical max of two canonical forms by Clark's formulas.

    Returns (c, t) where c is the canonical form and t the tightness
    probability P(A > B). The mean, the variance and the covariance with
    every global source are those of the true max(A, B) of the two Gaussian
    inputs; only the shape (Gaussian) is an approximation.
    """
    cov = sum(x * y for x, y in zip(a.coeffs, b.coeffs))
    va, vb = a.variance(), b.variance()
    theta2 = va + vb - 2.0 * cov
    if theta2 <= 1e-300:  # @line L9
        # A - B is a constant, so the max is exactly the one with the larger mean.
        return (a, 1.0) if a.mean >= b.mean else (b, 0.0)  # @line L10
    theta = math.sqrt(theta2)  # @line L11
    alpha = (a.mean - b.mean) / theta
    t = cdf(alpha)  # @line L12
    p = pdf(alpha)
    mean = a.mean * t + b.mean * (1.0 - t) + theta * p  # @line L13
    second = (a.mean ** 2 + va) * t + (b.mean ** 2 + vb) * (1.0 - t) + (a.mean + b.mean) * theta * p  # @line L14
    coeffs = tuple(t * x + (1.0 - t) * y for x, y in zip(a.coeffs, b.coeffs))  # @line L15
    rest = second - mean * mean - sum(c * c for c in coeffs)
    rand = math.sqrt(max(0.0, rest))  # @line L16
    return Canonical(mean, coeffs, rand), t  # @line L17


def topological_order(n: int, edges: Sequence[tuple]) -> list:
    """Kahn's algorithm. Raises ValueError if the graph has a cycle."""
    indeg = [0] * n
    out = [[] for _ in range(n)]
    for u, v, _ in edges:
        out[u].append(v)
        indeg[v] += 1
    queue = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if len(order) != n:
        raise ValueError("the timing graph has a cycle")
    return order


def statistical_static_timing_analysis(
    n: int,
    edges: Sequence[tuple],
    at_start: Mapping[int, Canonical],
) -> list:
    """Block-based SSTA: the canonical arrival time of every vertex.

    The vertices are 0 .. n-1, each edge is (u, v, d) with d a Canonical, and
    at_start gives the canonical arrival time of every vertex with no in-edge.
    In-edges are combined in the order in which they appear in edges.
    """
    order = topological_order(n, edges)  # @line L1
    into = [[] for _ in range(n)]
    for u, v, d in edges:
        into[v].append((u, d))
    at = [None] * n
    for v in order:  # @line L2
        if not into[v]:
            if v not in at_start:
                raise ValueError("no arrival time for start point %d" % v)
            at[v] = at_start[v]  # @line L3
            continue
        x = None
        for u, d in into[v]:
            s = add(at[u], d)  # @line L4
            x = s if x is None else clark_max(x, s)[0]  # @line L5
        at[v] = x
    return at  # @line L6


def timing_yield(x: Canonical, deadline: float) -> float:
    """P(X <= deadline) under the Gaussian form of X."""
    sd = x.std()
    if sd == 0.0:
        return 1.0 if x.mean <= deadline else 0.0
    return cdf((deadline - x.mean) / sd)
