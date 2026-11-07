# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reproducible-summation/. The authors are listed in prov/R755YZ.jsonl.

"""Order-independent summation by pre-rounding to fixed boundaries.

reproducible_sum(xs, K) returns the same binary64 result for every
permutation of xs (and for every split of xs into parts that are summed
separately and merged with merge_partials). The method is the K-fold
extraction of Demmel and Nguyen, with the boundary chosen from max |x_i|
and n so that every extracted part sums exactly.
"""

import math

P = 53                       # binary64 precision
_MIN_EXP = -1021            # M >= 2^-1021 keeps the unit M * 2^-p >= 2^-1074


def _ceil_log2(v):
    """Smallest integer t with v <= 2^t, for v > 0 (a float or an int)."""
    m, e = math.frexp(v)
    return e - 1 if m == 0.5 else e


def boundaries(m, n, K):
    """The K boundaries M_1 > M_2 > ... used for max |x_i| = m and length n."""
    c = _ceil_log2(n) + 1                                  # 2^c >= 2n
    a = max(_ceil_log2(m) + c, _MIN_EXP)
    out = []
    for _ in range(K):
        if a > 1023:
            raise OverflowError("max |x_i| too large for this n")
        if a < _MIN_EXP:
            if out and out[-1] == math.ldexp(1.0, _MIN_EXP):
                out.append(0.0)        # residuals are now 0 or +-2^-1074: take them whole
                break
            a = _MIN_EXP               # one level with unit 2^-1074
        out.append(math.ldexp(1.0, a))
        a += c - P
    return out


def fold_partials(xs, Ms):
    """Exact per-level sums T_j of the extracted parts (order independent)."""
    T = [0.0] * len(Ms)                                    # @line L3
    for x in xs:                                           # @line L4
        v = x                                              # @line L5
        for j, M in enumerate(Ms):                         # @line L6
            q = (M + v) - M                                # @line L7
            v = v - q                                      # @line L8
            T[j] += q                                      # @line L9
    return T


def _combine(T):
    s = 0.0
    for t in reversed(T):                                  # @line L10
        s = t + s
    return s


def _special(xs):
    """Order-independent result for inputs with inf or nan, else None."""
    pos = neg = nan = False
    for x in xs:
        if math.isnan(x):
            nan = True
        elif x == math.inf:
            pos = True
        elif x == -math.inf:
            neg = True
    if nan or (pos and neg):
        return math.nan
    if pos:
        return math.inf
    if neg:
        return -math.inf
    return None


def reproducible_sum(xs, K=3):
    """Sum xs so that the result does not depend on the order of xs."""
    xs = list(xs)
    sp = _special(xs)
    if sp is not None:
        return sp
    m = max((abs(x) for x in xs), default=0.0)             # @line L1
    if m == 0.0:
        return 0.0
    Ms = boundaries(m, len(xs), K)                         # @line L2
    return _combine(fold_partials(xs, Ms))


def merge_partials(parts, K=3):
    """Sum a list of lists as if concatenated, summing each part separately.

    Each part only needs the global max and the global length, which is the
    pattern of a parallel reduction: one max-reduction, then one sum.
    """
    parts = [list(p) for p in parts]
    flat = [x for p in parts for x in p]
    sp = _special(flat)
    if sp is not None:
        return sp
    m = max((abs(x) for x in flat), default=0.0)
    if m == 0.0:
        return 0.0
    Ms = boundaries(m, len(flat), K)
    totals = [0.0] * len(Ms)
    for p in parts:
        for j, t in enumerate(fold_partials(p, Ms)):
            totals[j] += t                                 # exact, see the proof
    return _combine(totals)


if __name__ == "__main__":
    import random
    rng = random.Random(1)
    xs = [rng.uniform(-1, 1) * 10 ** rng.randint(-8, 8) for _ in range(1000)]
    ys = xs[:]
    rng.shuffle(ys)
    print(sum(xs), sum(ys), reproducible_sum(xs), reproducible_sum(ys), math.fsum(xs))
