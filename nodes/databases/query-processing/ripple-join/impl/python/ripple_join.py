# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ripple-join/. The authors are listed in prov/NQMZP0.jsonl.

"""Ripple join: an online estimate of SUM(value) over the equi-join of R and S.

The tuples of R and S are read in a random order (or in the given order when
rng is None, so that a caller can pass its own permutation). Each step reads
beta_R new tuples of R and beta_S new tuples of S, as far as they last, and
joins each new tuple with every tuple already read from the other input. After
step t the running sum covers exactly the pairs of the rectangle R_n x S_n of
the tuples read so far, and the estimate is

    |R| |S| / (n_R n_S) * (sum of value(r, s) over the joining pairs in R_n x S_n).

COUNT is SUM with value 1. The half width of the confidence interval uses the
first-order (delta method) variance

    |R|^2 |S|^2 ((1 - n_R/|R|) v_R / n_R + (1 - n_S/|S|) v_S / n_S),

where v_R is the sample variance over r in R_n of the mean value of r against
S_n, and v_S is the same for S. It is an approximation for large samples.

method "hash" keeps a hash table on the key of each input and probes it;
method "nested" compares the new tuple with every tuple read from the other
input. Both give the same running sums. A NULL key (None) never matches.
"""

import math
import random
from collections.abc import Callable, Sequence
from fractions import Fraction


def _sample_var(xs: list) -> float:
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def exact_variance(r_rows: Sequence[tuple], s_rows: Sequence[tuple], rkey: Callable, skey: Callable,
                   value: Callable, n_r: int, n_s: int) -> Fraction:
    """The exact variance of the estimate after reading n_r tuples of R and n_s of S.

    With v(r, s) the value of a joining pair (0 otherwise), a(r) and b(s) the
    row and column means, mu the overall mean and g = v - a - b + mu:

    Var = |R|^2 |S|^2 ((1 - f_R) S_a / n_r + (1 - f_S) S_b / n_s + (1 - f_R)(1 - f_S) S_g / (n_r n_s)),

    where f_R = n_r / |R|, S_a = sum (a - mu)^2 / (|R| - 1), and the same for
    b, and S_g = sum g^2 / ((|R| - 1)(|S| - 1)). A term with a zero factor
    (1 - f) is 0, also when |R| = 1 or |S| = 1.
    """
    big_r, big_s = len(r_rows), len(s_rows)

    def v(r, s):
        kr, ks = rkey(r), skey(s)
        return Fraction(value(r, s)) if kr is not None and ks is not None and kr == ks else Fraction(0)

    mat = [[v(r, s) for s in s_rows] for r in r_rows]
    mu = sum(map(sum, mat)) / (big_r * big_s)
    a = [sum(row) / big_s for row in mat]
    b = [sum(mat[i][j] for i in range(big_r)) / big_r for j in range(big_s)]
    fr, fs = Fraction(n_r, big_r), Fraction(n_s, big_s)
    var = Fraction(0)
    if fr != 1:
        var += (1 - fr) * sum((x - mu) ** 2 for x in a) / (big_r - 1) / n_r
    if fs != 1:
        var += (1 - fs) * sum((x - mu) ** 2 for x in b) / (big_s - 1) / n_s
    if fr != 1 and fs != 1:
        sg = sum((mat[i][j] - a[i] - b[j] + mu) ** 2 for i in range(big_r) for j in range(big_s))
        var += (1 - fr) * (1 - fs) * sg / ((big_r - 1) * (big_s - 1)) / (n_r * n_s)
    return (big_r * big_s) ** 2 * var


def ripple_join(r_rows: Sequence[tuple], s_rows: Sequence[tuple], rkey: Callable, skey: Callable,
                value: Callable, aspect: tuple = (1, 1), rng: random.Random | None = None,
                method: str = "hash", z: float = 1.96) -> list:
    """Run the ripple join to the end and return one snapshot per step.

    A snapshot is a dict with n_r, n_s, sum (exact, over the rectangle read),
    estimate (a Fraction), half_width (a float) and pairs (pairs that joined).
    """
    if method not in ("hash", "nested"):
        raise ValueError("method must be 'hash' or 'nested'")
    big_r, big_s = len(r_rows), len(s_rows)
    r_order, s_order = list(r_rows), list(s_rows)
    if rng is not None:
        rng.shuffle(r_order)  # @line L1
        rng.shuffle(s_order)
    seen = ([], [])
    tables = ({}, {})
    rowsum = ([], [])  # rowsum[0][i]: sum of value(r_i, s) over s read so far
    total = 0
    pairs = 0
    n = [0, 0]
    snaps = []
    keyf = (rkey, skey)
    orders = (r_order, s_order)
    if big_r == 0 or big_s == 0:
        return [{"n_r": 0, "n_s": 0, "sum": 0, "estimate": Fraction(0), "half_width": 0.0, "pairs": 0}]

    def add(side: int, t: tuple) -> None:
        nonlocal total, pairs
        other = 1 - side
        k = keyf[side](t)
        mine = 0
        if method == "hash":
            matches = tables[other].get(k, ()) if k is not None else ()
        else:
            matches = [j for j, u in enumerate(seen[other])
                       if k is not None and keyf[other](u) is not None and keyf[other](u) == k]
        for j in matches:
            u = seen[other][j]
            v = value(t, u) if side == 0 else value(u, t)
            mine += v
            rowsum[other][j] += v
            pairs += 1
        total += mine
        idx = len(seen[side])
        seen[side].append(t)
        rowsum[side].append(mine)
        if k is not None:
            tables[side].setdefault(k, []).append(idx)
        n[side] += 1

    while n[0] < big_r or n[1] < big_s:  # @line L2
        for _ in range(aspect[0]):
            if n[0] < big_r:
                add(0, orders[0][n[0]])  # @line L3
        for _ in range(aspect[1]):
            if n[1] < big_s:
                add(1, orders[1][n[1]])  # @line L4
        if n[0] == 0 or n[1] == 0:
            continue
        est = Fraction(big_r * big_s * total, n[0] * n[1])  # @line L5
        v_r = _sample_var([x / n[1] for x in rowsum[0]])
        v_s = _sample_var([x / n[0] for x in rowsum[1]])
        var = (big_r * big_s) ** 2 * ((1 - n[0] / big_r) * v_r / n[0] + (1 - n[1] / big_s) * v_s / n[1])
        half = z * math.sqrt(max(var, 0.0))  # @line L6
        snaps.append({"n_r": n[0], "n_s": n[1], "sum": total, "estimate": est,
                      "half_width": half, "pairs": pairs})  # @line L7
    return snaps
