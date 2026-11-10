# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nisan-wigderson-generator/. The authors are listed in prov/TFPG45.jsonl.

"""The Nisan-Wigderson generator with a polynomial design.

The seed y is a tuple of d bits. A design is a list of sorted tuples of positions
in range(d). The hard function f maps a tuple of l bits to 0 or 1. This code shows
the structure and the reconstruction step of the proof. It makes no security claim:
the functions used in tests are small and easy.
"""

from itertools import product
from typing import Callable, List, Sequence, Tuple

Bits = Tuple[int, ...]


def poly_eval(coeffs: Sequence[int], alpha: int, q: int) -> int:
    """p(alpha) mod q for p = coeffs[0] + coeffs[1] t + ..."""
    v = 0
    for c in reversed(coeffs):
        v = (v * alpha + c) % q
    return v


def polynomial_design(q: int, r: int) -> List[Tuple[int, ...]]:
    """The sets S_p = {(alpha, p(alpha))} for all p over GF(q), q prime, deg p < r.

    The point (alpha, beta) has number alpha * q + beta, so d = q^2. There are q^r
    sets of size q, and two of them share at most r - 1 points. It needs r <= q:
    for r > q two different coefficient lists can give the same function."""
    design = []
    for coeffs in product(range(q), repeat=r):  # @line L5
        s = tuple(alpha * q + poly_eval(coeffs, alpha, q) for alpha in range(q))  # @line L6
        design.append(s)
    return design  # @line L7


def restrict(y: Sequence[int], s: Sequence[int]) -> Bits:
    """y restricted to the positions in s, in increasing order."""
    return tuple(y[p] for p in s)


def nw(y: Sequence[int], design: Sequence[Sequence[int]], f: Callable[[Bits], int]) -> Bits:
    """The Nisan-Wigderson generator: (f(y|S_1), ..., f(y|S_m))."""
    out = []
    for s in design:  # @line L1
        z = restrict(y, s)  # @line L2
        out.append(f(z))  # @line L3
    return tuple(out)  # @line L4


def max_intersection(design: Sequence[Sequence[int]]) -> int:
    best = 0
    sets = [set(s) for s in design]
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            best = max(best, len(sets[i] & sets[j]))
    return best


def predictor_from_fixing(
    design: Sequence[Sequence[int]],
    f: Callable[[Bits], int],
    test: Callable[[Bits], int],
    i: int,
    fixed: Sequence[int],
    r: Sequence[int],
) -> Callable[[Bits], int]:
    """The circuit C of the reconstruction proof, for position i (1-based).

    fixed holds the seed bits outside S_i (any values at positions in S_i are
    ignored), and r = (r_i, ..., r_m). On z in {0,1}^l, C puts z on S_i, computes
    y_j = f(y|S_j) for j < i, and outputs r_i if test(y_1 .. y_(i-1), r) = 1, else
    1 - r_i. Each y_j depends only on the bits of z on S_i and S_j together."""
    s_i = design[i - 1]

    def c(z: Bits) -> int:
        y = list(fixed)
        for pos, bit in zip(s_i, z):
            y[pos] = bit
        prefix = tuple(f(restrict(y, design[j])) for j in range(i - 1))
        return r[0] if test(prefix + tuple(r)) else 1 - r[0]

    return c
