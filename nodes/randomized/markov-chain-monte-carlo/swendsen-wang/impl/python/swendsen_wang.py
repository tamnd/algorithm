# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swendsen-wang/. The authors are listed in prov/PXDRJN.jsonl.

import itertools
import random
from fractions import Fraction
from typing import Sequence


def _find(parent: list[int], v: int) -> int:
    while parent[v] != v:
        parent[v] = parent[parent[v]]
        v = parent[v]
    return v


def clusters(n: int, bonds: Sequence[tuple[int, int]]) -> list[int]:
    """Label the connected components of the graph ({0, ..., n - 1}, bonds) by 0, 1, 2, ..."""
    parent = list(range(n))
    for u, v in bonds:
        a, b = _find(parent, u), _find(parent, v)
        if a != b:
            parent[a] = b
    label: dict[int, int] = {}
    return [label.setdefault(_find(parent, v), len(label)) for v in range(n)]


def swendsen_wang_step(
    n: int,
    edges: Sequence[tuple[int, int]],
    q: int,
    p: float,
    sigma: Sequence[int],
    rng: random.Random,
) -> list[int]:
    """One Swendsen-Wang update of a q-state Potts configuration sigma on the graph (range(n), edges).

    The target is pi(sigma) proportional to exp(J * #{uv in edges : sigma_u = sigma_v}) with p = 1 - exp(-J).
    The Ising model with coupling beta is the case q = 2, J = 2 beta, so p = 1 - exp(-2 beta).
    """
    bonds = [(u, v) for u, v in edges if sigma[u] == sigma[v] and rng.random() < p]  # @line L3
    label = clusters(n, bonds)  # @line L4
    colour = [rng.randrange(q) for _ in range(max(label) + 1)]  # @line L5
    return [colour[label[v]] for v in range(n)]  # @line L6


def swendsen_wang(
    n: int,
    edges: Sequence[tuple[int, int]],
    q: int,
    p: float,
    sigma0: Sequence[int],
    n_steps: int,
    rng: random.Random,
) -> list[list[int]]:
    """Run n_steps Swendsen-Wang updates from sigma0 and return the configurations after each update."""
    if q < 2 or not 0 <= p < 1:
        raise ValueError("need q >= 2 and 0 <= p < 1")
    if len(sigma0) != n or any(not 0 <= s < q for s in sigma0):
        raise ValueError("sigma0 must have n entries in range(q)")
    if any(not (0 <= u < n and 0 <= v < n) or u == v for u, v in edges):
        raise ValueError("edges must join two different vertices in range(n)")
    sigma = list(sigma0)  # @line L1
    chain = []
    for _ in range(n_steps):  # @line L2
        sigma = swendsen_wang_step(n, edges, q, p, sigma, rng)
        chain.append(sigma)  # @line L7
    return chain  # @line L8


def transition_matrix(
    n: int, edges: Sequence[tuple[int, int]], q: int, p: Fraction
) -> tuple[list[tuple[int, ...]], list[list[Fraction]]]:
    """The exact Swendsen-Wang transition matrix on all q^n configurations, with a rational bond probability p."""
    states = list(itertools.product(range(q), repeat=n))
    index = {s: i for i, s in enumerate(states)}
    m = len(states)
    matrix = [[Fraction(0)] * m for _ in range(m)]
    for i, s in enumerate(states):
        agree = [(u, v) for u, v in edges if s[u] == s[v]]
        for keep in itertools.product((False, True), repeat=len(agree)):
            bonds = [e for e, k in zip(agree, keep) if k]
            weight = p ** len(bonds) * (1 - p) ** (len(agree) - len(bonds))
            label = clusters(n, bonds)
            c = max(label) + 1
            share = weight / q**c
            for colour in itertools.product(range(q), repeat=c):
                matrix[i][index[tuple(colour[label[v]] for v in range(n))]] += share
    return states, matrix
