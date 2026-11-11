# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-modeling/. The authors are listed in prov/XX6766.jsonl.

"""Adaptive probability models and their ideal code lengths.

An adaptive model predicts each symbol from the counts of the symbols before
it, and then adds the symbol to the counts. The decoder can do the same, so
no model is sent. The ideal code length of a sequence is -lg of the product
of the predicted probabilities; an arithmetic coder comes within a few bits.

- The additive estimator P(s) = (c_s + delta) / (n + k delta): Laplace for
  delta = 1, Krichevsky-Trofimov (KT) for delta = 1/2.
- Escape methods A, B, C and D for symbols not seen yet.
- A frequency model that halves its counts when the total reaches a limit.
"""

import math
from fractions import Fraction


def sequential_probability(seq: list[int], k: int, delta: Fraction) -> Fraction:
    """The product of the predictions (c_s + delta) / (n + k delta), in exact arithmetic."""
    counts = [0] * k
    p = Fraction(1)
    for n, s in enumerate(seq):
        p *= (counts[s] + delta) / (n + k * delta)
        counts[s] += 1
    return p


def code_length(seq: list[int], k: int, delta: float) -> float:
    """The ideal code length in bits of the additive estimator, in floating point."""
    counts = [0] * k
    total = 0.0
    for n, s in enumerate(seq):
        total -= math.log2((counts[s] + delta) / (n + k * delta))
        counts[s] += 1
    return total


def kt_length(seq: list[int], k: int = 2) -> float:
    return code_length(seq, k, 0.5)


def laplace_length(seq: list[int], k: int = 2) -> float:
    return code_length(seq, k, 1.0)


def ml_length(seq: list[int], k: int = 2) -> float:
    """-lg of the largest probability that an iid model gives the sequence: n H_0."""
    n = len(seq)
    counts = [seq.count(s) for s in range(k)]
    return -sum(c * math.log2(c / n) for c in counts if c)


def laplace_closed_form_length(counts: list[int]) -> float:
    """lg of the multinomial coefficient plus lg C(n + k - 1, k - 1): the Laplace length
    of any sequence with these counts, the same for every order of the symbols."""
    n, k = sum(counts), len(counts)
    multinomial = math.factorial(n)
    for c in counts:
        multinomial //= math.factorial(c)
    return math.log2(multinomial) + math.log2(math.comb(n + k - 1, k - 1))


def escape_probabilities(method: str, counts: dict) -> tuple[dict, Fraction]:
    """Return ({symbol: probability}, escape probability) for the seen symbols.

    n is the number of symbols seen and q the number of distinct ones.
    A: c / (n + 1) and 1 / (n + 1).  B: (c - 1) / n and q / n.
    C: c / (n + q) and q / (n + q).  D: (2c - 1) / (2n) and q / (2n).
    """
    n = sum(counts.values())
    q = sum(1 for c in counts.values() if c > 0)
    if n == 0:
        return {}, Fraction(1)
    if method == "A":
        return {s: Fraction(c, n + 1) for s, c in counts.items()}, Fraction(1, n + 1)
    if method == "B":
        return {s: Fraction(c - 1, n) for s, c in counts.items()}, Fraction(q, n)
    if method == "C":
        return {s: Fraction(c, n + q) for s, c in counts.items()}, Fraction(q, n + q)
    if method == "D":
        return {s: Fraction(2 * c - 1, 2 * n) for s, c in counts.items()}, Fraction(q, 2 * n)
    raise ValueError("unknown escape method")


class HalvingModel:
    """Counts that start at 1 and are halved (rounding up) when the total reaches limit."""

    def __init__(self, k: int, increment: int = 1, limit: int | None = None) -> None:
        self.counts = [1] * k
        self.total = k
        self.increment = increment
        self.limit = limit

    def probability(self, s: int) -> float:
        return self.counts[s] / self.total

    def update(self, s: int) -> None:
        self.counts[s] += self.increment
        self.total += self.increment
        if self.limit is not None and self.total >= self.limit:
            self.counts = [(c + 1) // 2 for c in self.counts]
            self.total = sum(self.counts)


def model_length(seq: list[int], model: HalvingModel) -> float:
    total = 0.0
    for s in seq:
        total -= math.log2(model.probability(s))
        model.update(s)
    return total
