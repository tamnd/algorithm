# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/successive-cancellation-decoding/. The authors are listed in prov/CTNMA4.jsonl.
"""Successive cancellation (SC) decoding of polar codes, in the LLR domain and on the BEC.

The code is x = u F^(kron n) over GF(2) with F = [[1, 0], [1, 1]] and no bit reversal.
The input is the list of N channel LLRs lambda_j = ln W(y_j | 0) / W(y_j | 1) and the list
of N frozen flags (frozen bits are 0). The decoder returns (u_hat, x_hat) with
x_hat = u_hat F^(kron n). It runs in O(N log N) operations, and the recursion depth is
log2 N, so it is safe for each length that fits in memory.
"""

import math
from typing import Callable, List, Optional, Sequence, Tuple

Bits = List[int]


def f_exact(a: float, b: float) -> float:
    """f(a, b) = 2 atanh(tanh(a/2) tanh(b/2)), written so that it does not overflow."""
    s = math.copysign(1.0, a) * math.copysign(1.0, b)
    return (s * min(abs(a), abs(b)) + math.log1p(math.exp(-abs(a + b)))
            - math.log1p(math.exp(-abs(a - b))))


def f_min_sum(a: float, b: float) -> float:
    """The min-sum approximation sign(a) sign(b) min(|a|, |b|)."""
    s = math.copysign(1.0, a) * math.copysign(1.0, b)
    return s * min(abs(a), abs(b))


def g(a: float, b: float, u: int) -> float:
    """g(a, b, u) = b + (1 - 2u) a."""
    return b + a if u == 0 else b - a


def sc_decode(lam: Sequence[float], frozen: Sequence[bool],
              f: Callable[[float, float], float] = f_exact) -> Tuple[Bits, Bits]:
    """Return (u_hat, x_hat). len(lam) = len(frozen) = N, a power of two. Cost O(N log N)."""
    n = len(lam)  # @line L1
    if n == 1:  # @line L2
        b = 0 if frozen[0] or lam[0] >= 0 else 1  # @line L3
        return [b], [b]  # @line L4
    h = n // 2  # @line L5
    alpha = [f(lam[j], lam[j + h]) for j in range(h)]  # @line L6
    ua, xa = sc_decode(alpha, frozen[:h], f)  # @line L7
    beta = [g(lam[j], lam[j + h], xa[j]) for j in range(h)]  # @line L8
    ub, xb = sc_decode(beta, frozen[h:], f)  # @line L9
    return ua + ub, [p ^ q for p, q in zip(xa, xb)] + xb  # @line L10


def leaf_llrs(lam: Sequence[float], frozen: Sequence[bool],
              f: Callable[[float, float], float] = f_exact) -> List[float]:
    """The LLR that SC computes at each leaf, in decoding order (for traces and tests)."""
    out: List[float] = []

    def rec(v: List[float], fr: Sequence[bool]) -> Bits:
        if len(v) == 1:
            out.append(v[0])
            b = 0 if fr[0] or v[0] >= 0 else 1
            return [b]
        h = len(v) // 2
        xa = rec([f(v[j], v[j + h]) for j in range(h)], fr[:h])
        xb = rec([g(v[j], v[j + h], xa[j]) for j in range(h)], fr[h:])
        return [p ^ q for p, q in zip(xa, xb)] + xb

    rec(list(lam), frozen)
    return out


Erasable = Optional[int]


def sc_decode_bec(y: Sequence[Erasable], frozen: Sequence[bool],
                  genie: Optional[Sequence[int]] = None) -> Tuple[Bits, List[bool]]:
    """SC on BEC(eps). y_j is 0, 1 or None (erased).

    On the BEC an LLR is +inf, -inf or 0, so f and g become: f(a, b) = a xor b if both are
    known, else erased; g(a, b, u) = b if b is known, else a xor u if a is known, else erased.
    Returns (u_hat, erased) where erased[i] says that leaf i saw an erasure. An erased
    information bit is set to 0 (a guess). If `genie` is given, the decoder uses the true
    bits genie[i] as its past decisions, which is the setting of the synthetic channels.
    """
    u_out: Bits = []
    erased: List[bool] = []

    def rec(v: List[Erasable], fr: Sequence[bool]) -> Bits:
        if len(v) == 1:
            i = len(u_out)
            erased.append(v[0] is None)
            if genie is not None:
                b = genie[i]
            else:
                b = 0 if fr[0] or v[0] is None else v[0]
            u_out.append(b)
            return [b]
        h = len(v) // 2
        alpha = [None if v[j] is None or v[j + h] is None else v[j] ^ v[j + h] for j in range(h)]
        xa = rec(alpha, fr[:h])
        beta: List[Erasable] = []
        for j in range(h):
            if v[j + h] is not None:
                beta.append(v[j + h])
            elif v[j] is not None:
                beta.append(v[j] ^ xa[j])
            else:
                beta.append(None)
        xb = rec(beta, fr[h:])
        return [p ^ q for p, q in zip(xa, xb)] + xb

    rec(list(y), frozen)
    return u_out, erased


def polar_transform(u: Sequence[int]) -> Bits:
    """x = u F^(kron n) over GF(2). Cost (N/2) log2 N XORs."""
    x = list(u)
    n, h = len(x), 1
    while h < n:
        for s in range(0, n, 2 * h):
            for j in range(s, s + h):
                x[j] ^= x[j + h]
        h *= 2
    return x


def bec_bhattacharyya(n: int, eps):
    """Erasure probabilities of the synthetic channels on BEC(eps), by z -> 2z - z^2, z^2."""
    z = [eps]
    for _ in range(n):
        z = [w for v in z for w in (2 * v - v * v, v * v)]
    return z
