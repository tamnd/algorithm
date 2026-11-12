# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-td/. The authors are listed in prov/6WB7ES.jsonl.

"""Least-squares temporal-difference learning, LSTD(lambda), batch and recursive.

A transition is (s, r, s_next). s_next is None when the episode ends there; its features are then 0
and the eligibility trace is reset before the next transition. phi(s) is a sequence of d numbers.
With Fractions as input every result is exact.
"""

from fractions import Fraction
from typing import Callable, Optional, Sequence

Number = float | Fraction
Transition = tuple[object, Number, Optional[object]]


def solve(a: list[list[Number]], b: Sequence[Number]) -> list[Number]:
    """Solve a x = b by Gaussian elimination with partial pivoting. O(d^3)."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(m[i][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for i in range(n):
            if i != c and m[i][c] != 0:
                f = m[i][c] / m[c][c]
                m[i] = [u - f * v for u, v in zip(m[i], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def _features(phi: Callable[[object], Sequence[Number]], s: Optional[object], d: int) -> list[Number]:
    return [0] * d if s is None else list(phi(s))


def lstd(
    transitions: Sequence[Transition],
    phi: Callable[[object], Sequence[Number]],
    d: int,
    gamma: Number,
    lam: Number = 0,
    epsilon: Number = 0,
) -> list[Number]:
    """Batch LSTD(lambda): solve (epsilon I + sum z (phi - gamma phi')^T) theta = sum r z.

    O(T d^2 + d^3) time and O(d^2) memory for T transitions and d features.
    """
    a = [[epsilon if i == j else 0 for j in range(d)] for i in range(d)]  # @line L1
    b = [0] * d
    z = [0] * d
    for s, r, s_next in transitions:  # @line L2
        f, f_next = _features(phi, s, d), _features(phi, s_next, d)  # @line L3
        z = [gamma * lam * zi + fi for zi, fi in zip(z, f)]  # @line L4
        v = [fi - gamma * gi for fi, gi in zip(f, f_next)]
        a = [[a[i][j] + z[i] * v[j] for j in range(d)] for i in range(d)]  # @line L5
        b = [bi + r * zi for bi, zi in zip(b, z)]  # @line L6
        if s_next is None:  # @line L7
            z = [0] * d
    return solve(a, b)  # @line L8


def recursive_lstd(
    transitions: Sequence[Transition],
    phi: Callable[[object], Sequence[Number]],
    d: int,
    gamma: Number,
    lam: Number = 0,
    epsilon: Number = 1,
) -> list[list[Number]]:
    """Recursive LSTD(lambda): keep B = A^(-1) by the Sherman-Morrison formula.

    Starts from A = epsilon I, so B = I / epsilon, and returns theta after every transition.
    O(d^2) time per transition. The last theta equals lstd(..., epsilon=epsilon).
    """
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    inv = 1.0 / epsilon if isinstance(epsilon, float) else Fraction(1) / epsilon
    bm = [[inv if i == j else 0 for j in range(d)] for i in range(d)]
    b = [0] * d
    z = [0] * d
    thetas = []
    for s, r, s_next in transitions:
        f, f_next = _features(phi, s, d), _features(phi, s_next, d)
        z = [gamma * lam * zi + fi for zi, fi in zip(z, f)]
        v = [fi - gamma * gi for fi, gi in zip(f, f_next)]
        bz = [sum(bm[i][k] * z[k] for k in range(d)) for i in range(d)]
        vb = [sum(v[k] * bm[k][j] for k in range(d)) for j in range(d)]
        den = 1 + sum(v[k] * bz[k] for k in range(d))
        if den == 0:
            raise ValueError("A became singular")
        bm = [[bm[i][j] - bz[i] * vb[j] / den for j in range(d)] for i in range(d)]
        b = [bi + r * zi for bi, zi in zip(b, z)]
        thetas.append([sum(bm[i][k] * b[k] for k in range(d)) for i in range(d)])
        if s_next is None:
            z = [0] * d
    return thetas
