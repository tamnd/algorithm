# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/computational-indistinguishability/. The authors are listed in prov/SBVWAV.jsonl.

"""Exact distinguishing advantages and the hybrid argument on small distributions.

A distribution is a dict from bit tuples to Fractions that sum to 1. A test is a
function from a bit tuple to 0 or 1. All values are exact, so the telescoping
identity of the hybrid argument can be checked with equality.
"""

from fractions import Fraction
from itertools import product
from typing import Callable, Dict, List, Sequence, Tuple

Bits = Tuple[int, ...]
Dist = Dict[Bits, Fraction]
Test = Callable[[Bits], int]
Gen = Callable[[Bits], Sequence[int]]


def uniform(m: int) -> Dist:
    """U_m: the uniform distribution on {0,1}^m. Cost: Theta(2^m)."""
    w = Fraction(1, 2**m)
    return {z: w for z in product((0, 1), repeat=m)}


def accept_prob(test: Test, p: Dist) -> Fraction:
    """Pr[test(Z) = 1] for Z drawn from p."""
    return sum((w for z, w in p.items() if test(z)), Fraction(0))


def advantage(test: Test, p: Dist, q: Dist) -> Fraction:
    """The signed advantage Pr[test(P) = 1] - Pr[test(Q) = 1]."""
    return accept_prob(test, p) - accept_prob(test, q)


def statistical_distance(p: Dist, q: Dist) -> Fraction:
    """Half the L1 distance between p and q."""
    keys = set(p) | set(q)
    return sum((abs(p.get(z, Fraction(0)) - q.get(z, Fraction(0))) for z in keys), Fraction(0)) / 2


def best_test(p: Dist, q: Dist) -> Test:
    """The test that accepts exactly where p gives more weight than q.

    Its advantage equals the statistical distance."""
    good = {z for z in set(p) | set(q) if p.get(z, Fraction(0)) > q.get(z, Fraction(0))}
    return lambda z: 1 if z in good else 0


def output_dist(gen: Gen, d: int) -> Dist:
    """The distribution of gen(U_d)."""
    out: Dist = {}
    w = Fraction(1, 2**d)
    for s in product((0, 1), repeat=d):
        z = tuple(gen(s))
        out[z] = out.get(z, Fraction(0)) + w
    return out


def prg_hybrids(gen: Gen, d: int, m: int) -> List[Dist]:
    """H_0, ..., H_m where H_i is the first i bits of gen(U_d) followed by m - i uniform bits.

    H_0 = U_m and H_m = gen(U_d). Cost: Theta(m 2^(d+m))."""
    hybrids = []
    for i in range(m + 1):
        h: Dist = {}
        w = Fraction(1, 2 ** (d + m - i))
        for s in product((0, 1), repeat=d):
            prefix = tuple(gen(s))[:i]
            for u in product((0, 1), repeat=m - i):
                z = prefix + u
                h[z] = h.get(z, Fraction(0)) + w
        hybrids.append(h)
    return hybrids


def product_hybrids(p: Dist, q: Dist, k: int) -> List[Dist]:
    """H_0, ..., H_k where H_i is i samples of p followed by k - i samples of q, all independent.

    H_0 = q^k and H_k = p^k."""
    hybrids = []
    for i in range(k + 1):
        h: Dist = {(): Fraction(1)}
        for j in range(k):
            src = p if j < i else q
            nxt: Dist = {}
            for z, w in h.items():
                for y, v in src.items():
                    nxt[z + y] = nxt.get(z + y, Fraction(0)) + w * v
            h = nxt
        hybrids.append(h)
    return hybrids


def hybrid_gaps(test: Test, hybrids: List[Dist]) -> List[Fraction]:
    """The gaps Pr[test(H_{i+1}) = 1] - Pr[test(H_i) = 1] for i = 0 .. len - 2.

    Their sum telescopes to Pr[test(H_last)] - Pr[test(H_0)]."""
    probs = [accept_prob(test, h) for h in hybrids]
    return [probs[i + 1] - probs[i] for i in range(len(probs) - 1)]


def yao_predictor_success(gen: Gen, d: int, m: int, test: Test, i: int) -> Fraction:
    """Exact success probability of Yao's predictor for bit i (1-based).

    The predictor sees y_1 .. y_(i-1) of y = gen(s), draws r_i .. r_m uniformly, and
    outputs r_i if test(y_1 .. y_(i-1), r_i .. r_m) = 1, else 1 - r_i. The proof of
    the hybrid argument shows that this equals 1/2 + p_i - p_(i-1)."""
    total = Fraction(0)
    w = Fraction(1, 2 ** (d + m - i + 1))
    for s in product((0, 1), repeat=d):
        y = tuple(gen(s))
        for r in product((0, 1), repeat=m - i + 1):
            guess = r[0] if test(y[: i - 1] + r) else 1 - r[0]
            if guess == y[i - 1]:
                total += w
    return total
