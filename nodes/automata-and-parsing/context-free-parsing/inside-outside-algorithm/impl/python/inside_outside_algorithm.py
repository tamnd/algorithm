# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inside-outside-algorithm/. The authors are listed in prov/9H2A1G.jsonl.

"""The inside-outside algorithm: one expectation-maximization step for a PCFG.

The grammar is in Chomsky normal form. A rule is a pair (A, rhs) where rhs is
(B, C) with two nonterminals, (a,) with one terminal, or () for S -> eps.
The nonterminals are the left sides; S -> eps is allowed only when S is on
no right side. theta maps each rule to its probability, and the rules of each
nonterminal should sum to 1. The numbers may be floats or Fractions; with
Fractions every result is exact.

inside[i][j][A] is the probability that A derives a_{i+1} ... a_j, and
outside[i][j][A] is the probability that S derives a_1 ... a_i A a_{j+1} ... a_n.
"""

from fractions import Fraction
from typing import Sequence, Union

Num = Union[float, Fraction]
Rule = tuple[str, tuple[str, ...]]
Chart = list[list[dict[str, Num]]]


def _check(theta: dict[Rule, Num], start: str) -> set[str]:
    nts = {a for a, _ in theta}
    for (a, rhs), _ in theta.items():
        if len(rhs) == 2 and not (rhs[0] in nts and rhs[1] in nts):
            raise ValueError(f"binary rule {a} -> {rhs} needs two nonterminals")
        if len(rhs) == 1 and rhs[0] in nts:
            raise ValueError(f"unit rule {a} -> {rhs} is not in Chomsky normal form")
        if len(rhs) == 0 and a != start:
            raise ValueError("only the start symbol may have an empty rule")
        if len(rhs) > 2:
            raise ValueError(f"rule {a} -> {rhs} is too long")
    if (start, ()) in theta and any(start in rhs for _, rhs in theta if len(rhs) == 2):
        raise ValueError("S -> eps needs S on no right side")
    return nts


def inside_chart(theta: dict[Rule, Num], start: str, w: Sequence[str]) -> Chart:
    """Inside probabilities for all spans of a nonempty w, shortest spans first."""
    n = len(w)
    binary = [(a, rhs[0], rhs[1], p) for (a, rhs), p in theta.items() if len(rhs) == 2]
    inside: Chart = [[{} for _ in range(n + 1)] for _ in range(n + 1)]
    for i in range(n):                                                # @line L4
        for (a, rhs), p in theta.items():
            if len(rhs) == 1 and rhs[0] == w[i]:
                inside[i][i + 1][a] = inside[i][i + 1].get(a, 0) + p
    for length in range(2, n + 1):                                    # @line L5
        for i in range(n - length + 1):
            j = i + length
            cell = inside[i][j]
            for k in range(i + 1, j):
                left, right = inside[i][k], inside[k][j]
                if not left or not right:
                    continue
                for a, b, c, p in binary:
                    if b in left and c in right:
                        cell[a] = cell.get(a, 0) + p * left[b] * right[c]
    return inside


def outside_chart(theta: dict[Rule, Num], start: str, inside: Chart, n: int) -> Chart:
    """Outside probabilities for all spans, longest spans first."""
    binary = [(a, rhs[0], rhs[1], p) for (a, rhs), p in theta.items() if len(rhs) == 2]
    outside: Chart = [[{} for _ in range(n + 1)] for _ in range(n + 1)]
    outside[0][n][start] = 1                                          # @line L7
    for length in range(n, 1, -1):                                    # @line L8
        for i in range(n - length + 1):
            j = i + length
            out = outside[i][j]
            if not out:
                continue
            for k in range(i + 1, j):
                left, right = inside[i][k], inside[k][j]
                for a, b, c, p in binary:
                    if a in out and b in left and c in right:         # @line L9
                        outside[i][k][b] = outside[i][k].get(b, 0) + out[a] * p * right[c]
                        outside[k][j][c] = outside[k][j].get(c, 0) + out[a] * p * left[b]
    return outside


def expected_counts(theta: dict[Rule, Num], start: str,
                    w: Sequence[str]) -> tuple[Num, dict[Rule, Num]]:
    """Return (Z, c): Z is the probability of w, and c[r] is the expected number
    of uses of rule r in a parse tree of w, given w. If Z = 0, c is empty."""
    _check(theta, start)
    n = len(w)
    counts: dict[Rule, Num] = {}
    if n == 0:                                                        # @line L3
        z = theta.get((start, ()), 0)
        if z:
            counts[(start, ())] = 1
        return z, counts
    inside = inside_chart(theta, start, w)
    z = inside[0][n].get(start, 0)                                    # @line L6
    if not z:
        return z, counts
    outside = outside_chart(theta, start, inside, n)
    for (a, rhs), p in theta.items():                                 # @line L10
        if len(rhs) != 2:
            continue
        b, c = rhs
        total: Num = 0
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length
                out = outside[i][j].get(a)
                if not out:
                    continue
                for k in range(i + 1, j):
                    lb, rc = inside[i][k].get(b), inside[k][j].get(c)
                    if lb and rc:
                        total += out * p * lb * rc
        if total:
            counts[(a, rhs)] = total / z
    for i in range(n):                                                # @line L11
        for (a, rhs), p in theta.items():
            if len(rhs) == 1 and rhs[0] == w[i]:
                out = outside[i][i + 1].get(a)
                if out:
                    counts[(a, rhs)] = counts.get((a, rhs), 0) + out * p / z
    return z, counts


def em_step(theta: dict[Rule, Num], start: str,
            corpus: Sequence[Sequence[str]]) -> tuple[dict[Rule, Num], list[Num]]:
    """One inside-outside step. Return the new probabilities and the
    probability of each sentence under the old ones. Sentences of probability 0
    are skipped; a nonterminal with no expected use keeps its old probabilities."""
    total: dict[Rule, Num] = {r: 0 for r in theta}                    # @line L1
    likelihoods: list[Num] = []
    for w in corpus:                                                  # @line L2
        z, counts = expected_counts(theta, start, w)
        likelihoods.append(z)
        for r, c in counts.items():
            total[r] += c
    by_lhs: dict[str, Num] = {}
    for (a, _), c in total.items():
        by_lhs[a] = by_lhs.get(a, 0) + c
    new: dict[Rule, Num] = {}
    for (a, rhs), c in total.items():                                 # @line L12
        new[(a, rhs)] = c / by_lhs[a] if by_lhs[a] else theta[(a, rhs)]
    return new, likelihoods                                           # @line L13
