# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secondary-sort/. The authors are listed in prov/1NTC06.jsonl.

"""Secondary sort (value-to-key conversion) on a small MapReduce simulator.

A secondary sort needs three parts:
  1. a composite key (natural key, sort field),
  2. a partitioner that looks only at the natural key,
  3. a grouping function that looks only at the natural key,
while the sort uses the whole composite key. Then each reduce call gets one
natural key with its values in the order of the sort field.
"""

import itertools
import random
import zlib
from fractions import Fraction
from typing import Any, Callable, Iterable

Pair = tuple[Any, Any]


def stable_hash(key: Any) -> int:
    return zlib.crc32(repr(key).encode("utf-8"))


def run_round(splits: list[list[Pair]], mapper: Callable, reducer: Callable, r: int,
              partitioner: Callable[[Any, int], int] | None = None,
              sort_key: Callable[[Any], Any] | None = None,
              group_key: Callable[[Any], Any] | None = None,
              rng: random.Random | None = None) -> tuple[list[list[Pair]], list[int]]:
    """One round. Returns (output per reducer, number of reduce calls per reducer)."""
    partitioner = partitioner or (lambda k, n: stable_hash(k) % n)
    sort_key = sort_key or (lambda k: k)
    group_key = group_key or (lambda k: k)
    inbox: list[list[Pair]] = [[] for _ in range(r)]
    for split in splits:  # independent map tasks
        for k, v in (kv for rec in split for kv in mapper(*rec)):
            inbox[partitioner(k, r)].append((k, v))
    outputs, calls = [], []
    for box in inbox:  # independent reducers
        if rng is not None:
            rng.shuffle(box)
        box.sort(key=lambda kv: sort_key(kv[0]))  # Python's sort is stable, like a merge sort
        out, n_calls = [], 0
        for _, run in itertools.groupby(box, key=lambda kv: group_key(kv[0])):
            run = list(run)
            out.extend(reducer(run[0][0], [v for _, v in run]))
            n_calls += 1
        outputs.append(out)
        calls.append(n_calls)
    return outputs, calls


def make_splits(records: list[Any], m: int) -> list[list[Any]]:
    n = len(records)
    bounds = [i * n // m for i in range(m + 1)]
    return [records[bounds[i]:bounds[i + 1]] for i in range(m)]


def natural_partitioner(key: tuple, r: int) -> int:
    return stable_hash(key[0]) % r


# Sensor readings (sensor, time, reading): output each sensor's readings in time order.

def value_to_key_map(sensor: str, time: int, reading: int) -> Iterable[Pair]:
    yield ((sensor, time), reading)


def emit_series(key: tuple, readings: list[int]) -> Iterable[Pair]:
    yield (key[0], readings)


def sensor_series_secondary_sort(readings: list[tuple[str, int, int]], m: int, r: int,
                                 rng: random.Random | None = None) -> dict[str, list[int]]:
    """Value-to-key: the reducer receives the readings already in time order and keeps no buffer."""
    outputs, _ = run_round(make_splits(readings, m), value_to_key_map, emit_series, r,
                           partitioner=natural_partitioner, group_key=lambda k: k[0], rng=rng)
    return {s: series for out in outputs for s, series in out}


def sensor_series_reducer_sort(readings: list[tuple[str, int, int]], m: int, r: int,
                               rng: random.Random | None = None) -> dict[str, list[int]]:
    """The baseline: key = sensor, value = (time, reading), and the reducer sorts in memory."""
    outputs, _ = run_round(make_splits(readings, m), lambda s, t, x: [(s, (t, x))],
                           lambda s, vals: [(s, [x for _, x in sorted(vals)])], r, rng=rng)
    return {s: series for out in outputs for s, series in out}


# Order inversion (Lin and Dyer, Section 3.3): relative frequencies f(u | w) of neighbor words.
# The special value "*" makes the marginal count of w arrive before the counts of the pairs (w, u).

STAR = ""  # sorts before every word


def neighbor_map(doc_id: Any, text: str) -> Iterable[Pair]:
    words = text.split()
    for i, w in enumerate(words):
        for j in (i - 1, i + 1):
            if 0 <= j < len(words):
                yield ((w, words[j]), (words[j], 1))
                yield ((w, STAR), (STAR, 1))


def relative_frequency_reduce(key: tuple, values: list[tuple[str, int]]) -> Iterable[Pair]:
    w = key[0]
    marginal = 0
    current, count = None, 0
    for u, c in values:  # in increasing u, with STAR first
        if u == STAR:
            marginal += c
            continue
        if u != current and current is not None:
            yield ((w, current), Fraction(count, marginal))
            count = 0
        current = u
        count += c
    if current is not None:
        yield ((w, current), Fraction(count, marginal))


def relative_frequencies(docs: list[tuple[Any, str]], m: int, r: int,
                         rng: random.Random | None = None) -> dict[tuple[str, str], Fraction]:
    outputs, _ = run_round(make_splits(docs, m), neighbor_map, relative_frequency_reduce, r,
                           partitioner=natural_partitioner, group_key=lambda k: k[0], rng=rng)
    return {k: f for out in outputs for k, f in out}
