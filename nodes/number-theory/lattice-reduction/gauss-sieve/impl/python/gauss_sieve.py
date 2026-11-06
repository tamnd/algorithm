# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-sieve/. The authors are listed in prov/6BDMG5.jsonl.

import random
from fractions import Fraction
from math import floor
from typing import Sequence, Union

Number = Union[int, Fraction]
Vector = list[Fraction]


def _dot(u: Sequence[Fraction], v: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def _reduce_once(v: Vector, w: Vector, nw: Fraction) -> Vector:
    """v - q w with q the nearest integer to <v, w> / ||w||^2 (ties rounded up)."""
    q = floor(_dot(v, w) / nw + Fraction(1, 2))
    return [a - q * c for a, c in zip(v, w)]


def _independent(b: list[Vector]) -> bool:
    stars: list[Vector] = []
    for row in b:
        w = row[:]
        for s in stars:
            f = _dot(row, s) / _dot(s, s)
            w = [a - f * c for a, c in zip(w, s)]
        if not any(w):
            return False
        stars.append(w)
    return True


def gauss_sieve(
    basis: Sequence[Sequence[Number]],
    max_collisions: int = 50,
    max_samples: int = 2000,
    seed: int = 0,
    spread: int = 2,
) -> tuple[Vector, list[Vector]]:
    """Gauss sieve of Micciancio and Voulgaris, in exact rational arithmetic.

    The stack starts with the basis rows; further vectors are sampled as sum x_i b_i with
    x_i uniform in [-spread, spread], from random.Random(seed). The loop stops when the
    stack is empty and either max_collisions reductions to zero happened or max_samples
    samples were drawn. Returns (v, L): v is a shortest vector of the final list L, a nonzero
    lattice vector with ||v|| <= min ||b_i||, and L is pairwise Gauss-reduced
    (2 |<u, w>| <= min(||u||^2, ||w||^2)), so |L| is at most the kissing number tau_n in dimension n.
    v = lambda_1 is not guaranteed; it is the heuristic, observed outcome for enough
    collisions. Raises ValueError on invalid input.
    """
    if max_collisions < 1 or max_samples < 0 or spread < 1:
        raise ValueError("need max_collisions >= 1, max_samples >= 0 and spread >= 1")
    b = [[Fraction(c) for c in row] for row in basis]
    n = len(b)
    if n == 0 or any(len(row) != len(b[0]) for row in b):
        raise ValueError("need at least one basis row, all of the same length")
    if not _independent(b):
        raise ValueError("the basis vectors are linearly dependent")
    rng = random.Random(seed)
    lst: list[Vector] = []
    norms: list[Fraction] = []
    stack: list[Vector] = [row[:] for row in reversed(b)]  # @line L1
    collisions, samples = 0, 0
    while stack or (collisions < max_collisions and samples < max_samples):  # @line L2
        if stack:
            v = stack.pop()  # @line L3
        else:
            x = [rng.randint(-spread, spread) for _ in range(n)]
            samples += 1
            v = [sum((xi * row[j] for xi, row in zip(x, b)), Fraction(0)) for j in range(len(b[0]))]
        nv = _dot(v, v)
        changed = nv != 0
        while changed:  # @line L4
            changed = False
            for w, nw in zip(lst, norms):
                if nw <= nv and 2 * abs(_dot(v, w)) > nw:
                    v = _reduce_once(v, w, nw)
                    nv = _dot(v, v)
                    changed = nv != 0
                    if not changed:
                        break
        if nv == 0:
            collisions += 1  # @line L5
            continue
        keep_l: list[Vector] = []
        keep_n: list[Fraction] = []
        for w, nw in zip(lst, norms):  # @line L6
            if nw > nv and 2 * abs(_dot(v, w)) > nv:
                stack.append(_reduce_once(w, v, nv))  # @line L7
            else:
                keep_l.append(w)
                keep_n.append(nw)
        lst, norms = keep_l + [v], keep_n + [nv]  # @line L8
    i = min(range(len(lst)), key=lambda j: norms[j])
    return lst[i], lst  # @line L9
