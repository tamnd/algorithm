# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-sorting/. The authors are listed in prov/1SRXBE.jsonl.

"""Sorting with MapReduce: a sampling round, then a sort round with a range partitioner.

Round 1 draws s = a * R keys uniformly with replacement from the whole input
(each map task draws its share), sends them to one reducer, and picks the
splitters y_(a), y_(2a), ..., y_((R-1)a) of the sorted sample.
Round 2 sends key k to reducer |{splitters <= k}|; each reducer sorts its keys,
and the reducer outputs in order 0, 1, ..., R-1 form the sorted input.
Keys are made distinct by the tie-break (key, record id).
"""

import bisect
import math
import random
from typing import Any, Callable


def run_round(splits: list[list[Any]], mapper: Callable, reducer: Callable, r: int,
              partitioner: Callable[[Any, int], int]) -> tuple[list[list[Any]], list[int]]:
    """One round with explicit messages. Returns (output per reducer, input size per reducer)."""
    inbox: list[list[tuple[Any, Any]]] = [[] for _ in range(r)]
    for split in splits:  # independent map tasks
        for k, v in (kv for rec in split for kv in mapper(rec)):
            inbox[partitioner(k, r)].append((k, v))
    outputs = [reducer(sorted(box, key=lambda kv: kv[0])) for box in inbox]  # independent reducers
    return outputs, [len(box) for box in inbox]


def make_splits(records: list[Any], m: int) -> list[list[Any]]:
    n = len(records)
    bounds = [i * n // m for i in range(m + 1)]
    return [records[bounds[i]:bounds[i + 1]] for i in range(m)]


def sample_size_per_reducer(n: int, eps: float, delta: float) -> int:
    """The a of the page: a >= 2 (1 + eps) ln(n / delta) / eps^2 gives Pr[max bucket > ceil((1+eps) n/R)] <= delta."""
    return math.ceil(2 * (1 + eps) * math.log(n / delta) / eps ** 2)


def balance_bound(n: int, a: int, eps: float) -> float:
    """The proved failure probability n * exp(-eps^2 a / (2 (1 + eps)))."""
    return n * math.exp(-eps * eps * a / (2 * (1 + eps)))


def sampling_round(splits: list[list[Any]], a: int, r: int, rng: random.Random) -> tuple[list[Any], int]:
    """Round 1. Returns (the R - 1 splitters, the number of pairs shuffled = s = a R)."""
    n = sum(len(s) for s in splits)
    s = a * r
    owners = [i for i, sp in enumerate(splits) for _ in sp]
    counts = [0] * len(splits)
    for _ in range(s):  # the driver tells map task i how many draws s_i to make
        counts[owners[rng.randrange(n)]] += 1
    drawn = [[sp[rng.randrange(len(sp))] for _ in range(c)] for sp, c in zip(splits, counts)]
    outputs, sizes = run_round(drawn, lambda key: [(key, None)], lambda pairs: [k for k, _ in pairs], 1,
                               lambda k, n_red: 0)
    sample = outputs[0]
    return [sample[j * a - 1] for j in range(1, r)], sizes[0]


def range_partitioner(splitters: list[Any]) -> Callable[[Any, int], int]:
    return lambda key, r: bisect.bisect_right(splitters, key)


def sort_round(splits: list[list[Any]], splitters: list[Any], r: int) -> tuple[list[list[Any]], list[int]]:
    """Round 2: range partition, then each reducer outputs its keys in order."""
    return run_round(splits, lambda key: [(key, None)], lambda pairs: [k for k, _ in pairs], r,
                     range_partitioner(splitters))


def distributed_sort(keys: list[Any], m: int, r: int, a: int, rng: random.Random
                     ) -> tuple[list[Any], dict[str, Any]]:
    """Sort keys with M = m map tasks and R = r reducers. Returns (sorted keys, costs)."""
    records = [(k, i) for i, k in enumerate(keys)]  # the tie-break makes all keys distinct
    splits = make_splits(records, m)
    if not records:
        return [], {"rounds": 0, "sample_pairs": 0, "sort_pairs": 0, "bucket_sizes": [0] * r}
    splitters, sample_pairs = sampling_round(splits, a, r, rng)
    outputs, sizes = sort_round(splits, splitters, r)
    result = [k for out in outputs for k, _ in out]
    return result, {"rounds": 2, "sample_pairs": sample_pairs, "sort_pairs": sum(sizes), "bucket_sizes": sizes}


def max_bucket_with_fixed_splitters(keys: list[Any], splitters: list[Any]) -> int:
    """Largest bucket when the splitters are chosen without looking at the data."""
    sizes = [0] * (len(splitters) + 1)
    for k in keys:
        sizes[bisect.bisect_right(splitters, k)] += 1
    return max(sizes)
