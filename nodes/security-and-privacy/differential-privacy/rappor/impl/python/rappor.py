# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rappor/. The authors are listed in prov/WNQFZC.jsonl.
"""RAPPOR (Erlingsson, Pihur and Korolova, CCS 2014).

A client hashes its value into a Bloom filter of k bits with h hash functions,
applies a permanent randomized response to each bit (memoized per value), and
then sends a fresh instantaneous randomized response of the memoized bits in
each report. The collector counts the ones per bit and cohort, removes the
bias of the two randomizations, and fits the counts of a list of candidate
values by least squares.

The probabilities f, p and q are Fractions so that the coins are exact and the
report pmf can be checked with fractions. random.Random is used only so that
the tests are reproducible; a deployment needs a cryptographic source of
randomness. The hash is SHA-256 of the cohort, the hash index and the value.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import random
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Hashable, Sequence

Bits = tuple[int, ...]


@dataclass(frozen=True)
class RapporParams:
    """k bits, h hash functions, m cohorts, permanent f and instantaneous p < q."""

    k: int
    h: int
    f: Fraction
    p: Fraction
    q: Fraction
    m: int = 1

    def __post_init__(self) -> None:
        if self.k < 1 or self.h < 1 or self.m < 1:
            raise ValueError("need k, h and m at least 1")
        if not (0 <= self.f < 1 and 0 <= self.p < self.q <= 1):
            raise ValueError("need 0 <= f < 1 and 0 <= p < q <= 1")


def _coin(prob: Fraction, rng: random.Random) -> int:
    """1 with probability prob, exactly, from one uniform integer draw."""
    return 1 if rng.randrange(prob.denominator) < prob.numerator else 0


def bloom_positions(value: Hashable, cohort: int, params: RapporParams) -> list[int]:
    """The h positions H_1(value), ..., H_h(value) of the cohort's hash functions."""
    out = []
    for j in range(params.h):
        digest = hashlib.sha256(f"{cohort}|{j}|{value!r}".encode()).digest()
        out.append(int.from_bytes(digest[:8], "big") % params.k)
    return out


def bloom_filter(value: Hashable, cohort: int, params: RapporParams) -> Bits:
    """The k-bit Bloom filter B of the value: bit i is 1 when some H_j(value) = i."""
    b = [0] * params.k
    for i in bloom_positions(value, cohort, params):
        b[i] = 1
    return tuple(b)


def permanent_rr(b: Bits, f: Fraction, rng: random.Random) -> Bits:
    """Each bit becomes 1 with probability f/2, 0 with probability f/2, else stays."""
    out = []
    for bit in b:
        u = rng.randrange(2 * f.denominator)
        if u < f.numerator:
            out.append(1)
        elif u < 2 * f.numerator:
            out.append(0)
        else:
            out.append(bit)
    return tuple(out)


def instantaneous_rr(bp: Bits, p: Fraction, q: Fraction, rng: random.Random) -> Bits:
    """Each bit of the report is 1 with probability q if the memoized bit is 1, else p."""
    return tuple(_coin(q if bit else p, rng) for bit in bp)


@dataclass
class RapporClient:
    """One client: its cohort and the memo of permanent bits for each value it has seen."""

    cohort: int
    params: RapporParams
    memo: dict[Hashable, Bits] = field(default_factory=dict)

    def report(self, value: Hashable, rng: random.Random) -> Bits:
        """One RAPPOR report of value.

        Precondition: 0 <= cohort < m. All reports of the same value reuse the
        same permanent bits, so together they leak at most epsilon_infinity.
        Cost: O(h + k) word operations and at most 2k uniform draws per report.
        """
        if not 0 <= self.cohort < self.params.m:
            raise ValueError("cohort out of range")
        if value not in self.memo:  # @line L1
            b = bloom_filter(value, self.cohort, self.params)  # @line L2
            bp = permanent_rr(b, self.params.f, rng)  # @line L3
            self.memo[value] = bp  # @line L4
        bp = self.memo[value]  # @line L5
        s = instantaneous_rr(bp, self.params.p, self.params.q, rng)  # @line L6
        return s  # @line L7


def one_probabilities(params: RapporParams) -> tuple[Fraction, Fraction]:
    """(q*, p*): the chance that a reported bit is 1 when the true bit is 1, and when it is 0."""
    f, p, q = params.f, params.p, params.q
    q_star = f * (p + q) / 2 + (1 - f) * q
    p_star = f * (p + q) / 2 + (1 - f) * p
    return q_star, p_star


def epsilon_permanent(params: RapporParams) -> float:
    """epsilon_infinity = 2 h ln((1 - f/2) / (f/2)), the bound for all reports of one value."""
    if params.f == 0:
        return math.inf
    half = params.f / 2
    return 2 * params.h * math.log((1 - half) / half)


def epsilon_one_report(params: RapporParams) -> float:
    """epsilon_1 = h ln(q* (1 - p*) / (p* (1 - q*))), the bound for a single report."""
    q_star, p_star = one_probabilities(params)
    if p_star == 0 or q_star == 1:
        return math.inf
    return params.h * math.log(q_star * (1 - p_star) / (p_star * (1 - q_star)))


def bit_counts(reports: Sequence[tuple[int, Bits]], params: RapporParams) -> tuple[list[list[int]], list[int]]:
    """c[j][i], the number of reports of cohort j with bit i set, and N[j], the reports of cohort j."""
    c = [[0] * params.k for _ in range(params.m)]
    totals = [0] * params.m
    for cohort, s in reports:
        totals[cohort] += 1
        for i, bit in enumerate(s):
            c[cohort][i] += bit
    return c, totals


def debiased_counts(c: list[list[int]], totals: list[int], params: RapporParams) -> list[list[Fraction]]:
    """t[j][i] = (c[j][i] - p* N[j]) / ((1 - f)(q - p)), an unbiased estimate of the true bit counts."""
    _, p_star = one_probabilities(params)
    scale = (1 - params.f) * (params.q - params.p)
    return [[(c[j][i] - p_star * totals[j]) / scale for i in range(params.k)] for j in range(params.m)]


def design_matrix(candidates: Sequence[Hashable], params: RapporParams) -> list[list[int]]:
    """The km x M matrix X: column v has a 1 in row (j, i) when bit i of v's filter in cohort j is 1."""
    rows = [[0] * len(candidates) for _ in range(params.k * params.m)]
    for col, v in enumerate(candidates):
        for j in range(params.m):
            for i, bit in enumerate(bloom_filter(v, j, params)):
                if bit:
                    rows[j * params.k + i][col] = 1
    return rows


def _solve(a: list[list[Fraction]], b: list[Fraction]) -> list[Fraction]:
    """Solve a x = b by Gauss-Jordan elimination with exact fractions."""
    n = len(a)
    mat = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = next((r for r in range(col, n) if mat[r][col] != 0), None)
        if piv is None:
            raise ValueError("the candidates are not separable: X has dependent columns")
        mat[col], mat[piv] = mat[piv], mat[col]
        for r in range(n):
            if r != col and mat[r][col] != 0:
                ratio = mat[r][col] / mat[col][col]
                mat[r] = [x - ratio * y for x, y in zip(mat[r], mat[col])]
    return [mat[i][n] / mat[i][i] for i in range(n)]


def fit_candidates(t: list[list[Fraction]], candidates: Sequence[Hashable], params: RapporParams) -> list[Fraction]:
    """The least squares solution of X a = t, with t flattened cohort by cohort.

    Precondition: X has independent columns. Cost: O(k m M^2 + M^3) exact operations.
    """
    x = design_matrix(candidates, params)  # @line L10
    y = [t[j][i] for j in range(params.m) for i in range(params.k)]
    cols = len(candidates)
    xtx = [[Fraction(sum(row[a] * row[b] for row in x)) for b in range(cols)] for a in range(cols)]
    xty = [sum((row[a] * yv for row, yv in zip(x, y)), Fraction(0)) for a in range(cols)]
    return _solve(xtx, xty)  # @line L11


def rappor_estimate(reports: Sequence[tuple[int, Bits]], candidates: Sequence[Hashable], params: RapporParams) -> list[Fraction]:
    """Least squares estimates of how many clients hold each candidate value.

    reports is a list of (cohort, report) pairs, one report per client.
    Precondition: the clients are spread evenly over the m cohorts, and the
    design matrix has independent columns. The fit gives the count of each
    candidate in one cohort, so the result is m times the fit. This is the
    least squares stage of the paper; its Lasso stage that picks the
    candidates first is left out. Cost: O(N k) for the counts and
    O(k m M^2 + M^3) exact arithmetic operations for the fit.
    """
    c, totals = bit_counts(reports, params)  # @line L8
    t = debiased_counts(c, totals, params)  # @line L9
    per_cohort = fit_candidates(t, candidates, params)
    return [params.m * a for a in per_cohort]  # @line L12


def permanent_pmf(b: Bits, f: Fraction) -> dict[Bits, Fraction]:
    """The exact pmf of the permanent bits B' given the Bloom filter b."""
    keep_one = 1 - f / 2
    out = {}
    for bp in itertools.product((0, 1), repeat=len(b)):
        pr = Fraction(1)
        for bit, new in zip(b, bp):
            pr *= keep_one if bit == new else f / 2
        out[bp] = pr
    return out


def first_report_pmf(b: Bits, params: RapporParams) -> dict[Bits, Fraction]:
    """The exact pmf of one report of a value with Bloom filter b, before any memo exists."""
    q_star, p_star = one_probabilities(params)
    out = {}
    for s in itertools.product((0, 1), repeat=len(b)):
        pr = Fraction(1)
        for bit, rep in zip(b, s):
            one = q_star if bit else p_star
            pr *= one if rep else 1 - one
        out[s] = pr
    return out
