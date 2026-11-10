# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scatter-and-gather/. The authors are listed in prov/FB12GR.jsonl.

"""Gather, scatter and permute as single synchronous PRAM steps.

Every processor reads the old state first; all writes are then applied
together. A scatter with repeated indices needs a CRCW rule.
"""

import random
from typing import Callable, TypeVar

T = TypeVar("T")


class WriteConflict(Exception):
    pass


def gather(a: list[T], idx: list[int]) -> list[T]:
    """b[i] = a[idx[i]]. Repeated indices are concurrent reads (CREW)."""
    n = len(idx)  # @line L1: one processor for each i
    b = [a[idx[i]] for i in range(n)]  # @line L2
    return b  # @line L3


def scatter(
    a: list[T],
    idx: list[int],
    out: list[T],
    rule: str = "exclusive",
    combine: Callable[[T, T], T] | None = None,
    rng: random.Random | None = None,
) -> list[T]:
    """out[idx[i]] = a[i], in one step, with a rule for concurrent writes.

    exclusive: repeated indices are an error (EREW, CREW).
    common: writers to one cell must write the same value.
    arbitrary: one writer wins, chosen by rng.
    priority: the writer with the smallest index i wins.
    combining: the cell gets the old value combined with all written values,
    in increasing order of i.
    """
    writers: dict[int, list[int]] = {}
    for i in range(len(a)):  # @line L4: all processors i in parallel
        writers.setdefault(idx[i], []).append(i)
    b = list(out)
    for j, ws in writers.items():  # @line L5: the writes of one step
        vals = [a[i] for i in ws]
        if len(ws) == 1 or rule == "priority":
            b[j] = vals[0]
        elif rule == "exclusive":
            raise WriteConflict(f"processors {ws} write cell {j}")
        elif rule == "common":
            if any(v != vals[0] for v in vals):
                raise WriteConflict(f"different values written to cell {j}")
            b[j] = vals[0]
        elif rule == "arbitrary":
            b[j] = (rng or random.Random(0)).choice(vals)
        elif rule == "combining":
            assert combine is not None
            acc = b[j]
            for v in vals:
                acc = combine(acc, v)
            b[j] = acc
        else:
            raise ValueError(rule)
    return b  # @line L6


def permute(a: list[T], p: list[int]) -> list[T]:
    """Scatter with a permutation p: the result has a[i] at position p[i]."""
    assert sorted(p) == list(range(len(a)))
    return scatter(a, p, [None] * len(a))  # type: ignore[list-item]


def inverse(p: list[int]) -> list[int]:
    """The inverse permutation, itself one scatter of the indices."""
    return scatter(list(range(len(p))), p, [0] * len(p))


def is_exclusive(idx: list[int]) -> bool:
    """True when no two processors access the same cell (EREW is enough)."""
    return len(set(idx)) == len(idx)
