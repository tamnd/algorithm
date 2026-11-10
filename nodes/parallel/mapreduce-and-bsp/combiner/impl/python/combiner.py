# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combiner/. The authors are listed in prov/1WW8S5.jsonl.

"""Combiners on a small MapReduce simulator.

The framework may run a combiner zero, one or many times on any part of a map
task's output. The simulator models this: with an rng, each map task either
skips the combiner, or runs it on spills of a random size, and then maybe once
more on the merged spills. A job is correct only if its output is the same for
every such choice. The file has a correct job (sum), the mean as the classic
failure, and the (sum, count) fix.
"""

import itertools
import random
import zlib
from fractions import Fraction
from typing import Any, Callable, Iterable

Pair = tuple[Any, Any]


def stable_hash(key: Any) -> int:
    return zlib.crc32(repr(key).encode("utf-8"))


def group_sorted(pairs: list[Pair]) -> list[tuple[Any, list[Any]]]:
    ordered = sorted(pairs, key=lambda kv: kv[0])
    return [(k, [v for _, v in run]) for k, run in itertools.groupby(ordered, key=lambda kv: kv[0])]


def apply_combiner(pairs: list[Pair], combiner: Callable) -> list[Pair]:
    return [kv for key, vals in group_sorted(pairs) for kv in combiner(key, vals)]


def map_task(split: list[Pair], mapper: Callable, combiner: Callable | None,
             rng: random.Random | None) -> list[Pair]:
    """Map one split, then run the combiner zero, one or more times.

    Without rng the combiner (if any) runs once on the whole output. With rng
    the task skips it, or runs it per spill of a random size and maybe again
    on the merge.
    """
    out = [kv for k, v in split for kv in mapper(k, v)]
    if combiner is None or not out:
        return out
    if rng is None:
        return apply_combiner(out, combiner)
    if rng.random() < 0.25:
        return out  # the framework chose not to run the combiner
    size = rng.randrange(1, len(out) + 1)
    out = [kv for i in range(0, len(out), size) for kv in apply_combiner(out[i:i + size], combiner)]
    if rng.random() < 0.5:
        out = apply_combiner(out, combiner)
    return out


def run_round(splits: list[list[Pair]], mapper: Callable, reducer: Callable, r: int,
              combiner: Callable | None = None,
              rng: random.Random | None = None) -> tuple[dict[Any, Any], int]:
    """One round. Returns (the reduce output as a dict, the number of pairs shuffled)."""
    inbox: list[list[Pair]] = [[] for _ in range(r)]
    sent = 0
    for split in splits:  # independent map tasks
        for k, v in map_task(split, mapper, combiner, rng):
            inbox[stable_hash(k) % r].append((k, v))
            sent += 1
    if rng is not None:
        for box in inbox:
            rng.shuffle(box)
    out = {}
    for box in inbox:  # independent reducers
        for key, vals in group_sorted(box):
            for k, v in reducer(key, vals):
                out[k] = v
    return out, sent


def make_splits(records: list[Pair], m: int) -> list[list[Pair]]:
    n = len(records)
    bounds = [i * n // m for i in range(m + 1)]
    return [records[bounds[i]:bounds[i + 1]] for i in range(m)]


# A correct combiner: the sum. reduce = identity after +, and + is associative and commutative.

def identity_map(key: Any, value: Any) -> Iterable[Pair]:
    yield (key, value)


def sum_reduce(key: Any, values: list[int]) -> Iterable[Pair]:
    yield (key, sum(values))


# The failure: using the mean reducer as its own combiner.

def mean_reduce(key: Any, values: list[Fraction]) -> Iterable[Pair]:
    yield (key, Fraction(sum(values), len(values)))


# The fix: the mapper emits (x, 1), the combiner adds pairs, the reducer divides.

def mean_map_pairs(key: Any, value: int) -> Iterable[Pair]:
    yield (key, (value, 1))


def pair_sum_combiner(key: Any, values: list[tuple[int, int]]) -> Iterable[Pair]:
    yield (key, (sum(s for s, _ in values), sum(c for _, c in values)))


def mean_reduce_pairs(key: Any, values: list[tuple[int, int]]) -> Iterable[Pair]:
    s = sum(x for x, _ in values)
    c = sum(n for _, n in values)
    yield (key, Fraction(s, c))


# A second failure: the counting reducer as a combiner (count of counts).

def one_map(key: Any, value: Any) -> Iterable[Pair]:
    yield (key, 1)


def count_reduce(key: Any, values: list[Any]) -> Iterable[Pair]:
    yield (key, len(values))


def mean_of_means(groups: list[list[int]]) -> Fraction:
    """What a mean combiner computes when the values are cut into these groups."""
    return Fraction(sum(Fraction(sum(g), len(g)) for g in groups), len(groups))
