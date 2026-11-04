# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sos-dp/. The authors are listed in prov/2ABXMX.jsonl.

from collections.abc import Callable, Sequence
from typing import TypeVar

T = TypeVar("T")


def _check_length(f: Sequence[object], n: int) -> None:
    if n < 0 or len(f) != 1 << n:
        raise ValueError("f must have exactly 2**n entries")


def sos_dp(f: Sequence[T], n: int, add: Callable[[T, T], T] = lambda a, b: a + b) -> list[T]:
    """Return F with F[m] = sum of f[s] over all submasks s of m.

    The values may be in any commutative monoid; `add` is its operation
    (for example max or operator.or_). Precondition: len(f) == 2**n.
    Cost: n * 2**(n-1) calls of add, Theta(n 2^n) time, the output array.
    """
    _check_length(f, n)
    F = list(f)  # @line L1
    for i in range(n):  # @line L2
        bit = 1 << i
        for m in range(1 << n):  # @line L3
            if m & bit:  # @line L4
                F[m] = add(F[m], F[m ^ bit])  # @line L5
    return F  # @line L6


def sos_dp_supersets(f: Sequence[T], n: int, add: Callable[[T, T], T] = lambda a, b: a + b) -> list[T]:
    """Return G with G[m] = sum of f[s] over all supermasks s of m (within n bits)."""
    _check_length(f, n)
    G = list(f)
    for i in range(n):
        bit = 1 << i
        for m in range(1 << n):
            if not m & bit:
                G[m] = add(G[m], G[m | bit])
    return G


def mobius(F: Sequence[int], n: int) -> list[int]:
    """Inverse of sos_dp over the integers: return f with sos_dp(f, n) == F."""
    _check_length(F, n)
    f = list(F)
    for i in range(n):
        bit = 1 << i
        for m in range(1 << n):
            if m & bit:
                f[m] -= f[m ^ bit]
    return f
