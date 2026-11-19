# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alignment-error-rate/. The authors are listed in prov/T1YMPJ.jsonl.

"""Alignment error rate (Och and Ney 2000, 2003) and the measures around it.

A link is a pair (j, i): source position j, target position i. A is the
predicted set, S the sure gold links and P the possible gold links, with
S a subset of P. All results are exact fractions.

    precision(A, P) = |A & P| / |A|
    recall(A, S)    = |A & S| / |S|
    AER(A, S, P)    = 1 - (|A & S| + |A & P|) / (|A| + |S|)
"""

from fractions import Fraction
from typing import Iterable, Set, Tuple

Link = Tuple[int, int]


def _check(s: Set[Link], p: Set[Link]) -> None:
    if not s <= p:
        raise ValueError("the sure links S must be a subset of the possible links P")


def aer(a: Iterable[Link], s: Iterable[Link], p: Iterable[Link]) -> Fraction:
    """The alignment error rate. Raises ValueError if S is not inside P or if A and S are both empty."""
    a, s, p = set(a), set(s), set(p)
    _check(s, p)  # @line L1
    if not a and not s:
        raise ValueError("AER is undefined when A and S are both empty")
    hit_s = len(a & s)  # @line L2
    hit_p = len(a & p)  # @line L3
    return 1 - Fraction(hit_s + hit_p, len(a) + len(s))  # @line L4


def precision(a: Iterable[Link], p: Iterable[Link]) -> Fraction:
    a, p = set(a), set(p)
    if not a:
        raise ValueError("precision is undefined for an empty A")
    return Fraction(len(a & p), len(a))


def recall(a: Iterable[Link], s: Iterable[Link]) -> Fraction:
    a, s = set(a), set(s)
    if not s:
        raise ValueError("recall is undefined for an empty S")
    return Fraction(len(a & s), len(s))


def f_measure(a: Iterable[Link], s: Iterable[Link], p: Iterable[Link], alpha: Fraction = Fraction(1, 2)) -> Fraction:
    """The weighted F of Fraser and Marcu: 1 / (alpha / precision(A, P) + (1 - alpha) / recall(A, S)).

    Returns 0 if the precision or the recall is 0.
    """
    a, s, p = set(a), set(s), set(p)
    _check(s, p)
    pr, rc = precision(a, p), recall(a, s)
    if pr == 0 or rc == 0:
        return Fraction(0)
    return 1 / (alpha / pr + (1 - alpha) / rc)


def corpus_aer(items: Iterable[Tuple[Iterable[Link], Iterable[Link], Iterable[Link]]]) -> Fraction:
    """AER over a test set: the counts of all sentences are summed before the division."""
    hit_s = hit_p = size_a = size_s = 0
    for a, s, p in items:
        a, s, p = set(a), set(s), set(p)
        _check(s, p)
        hit_s += len(a & s)
        hit_p += len(a & p)
        size_a += len(a)
        size_s += len(s)
    if size_a + size_s == 0:
        raise ValueError("AER is undefined when A and S are both empty")
    return 1 - Fraction(hit_s + hit_p, size_a + size_s)
