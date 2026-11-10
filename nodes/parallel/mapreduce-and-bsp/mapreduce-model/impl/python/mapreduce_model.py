# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mapreduce-model/. The authors are listed in prov/5E46VV.jsonl.

"""A small MapReduce simulator that counts what the cost model counts.

One call of run_round is one MapReduce round. The M map tasks are independent
(one list comprehension over the splits). Each map task cuts its output into R
regions with the partitioner. The shuffle is an explicit list of messages
(source map task, destination reducer, key, value). Each reducer sorts its
input by key, groups equal keys, and calls the reduce function once per group.

The simulator counts the pairs and bytes sent in the shuffle, the input of each
reducer, and the rounds. Python cannot show the speedup of a cluster, so the
code shows the dataflow exactly and counts its costs instead.
"""

import itertools
import random
import zlib
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

Pair = tuple[Any, Any]
Mapper = Callable[[Any, Any], Iterable[Pair]]
Reducer = Callable[[Any, list[Any]], Iterable[Pair]]
Partitioner = Callable[[Any, int], int]


def pair_size(key: Any, value: Any) -> int:
    """Bytes of a pair in a plain text encoding: the UTF-8 length of key and value."""
    return len(str(key).encode("utf-8")) + len(str(value).encode("utf-8"))


def stable_hash(key: Any) -> int:
    """A hash that is the same in every process (Python's hash of str is not)."""
    return zlib.crc32(repr(key).encode("utf-8"))


def hash_partitioner(key: Any, r: int) -> int:
    """The default partitioner: hash(key) mod R."""
    return stable_hash(key) % r


@dataclass
class RoundStats:
    """The costs of one round."""

    map_tasks: int = 0
    reducers: int = 0
    map_output_pairs: int = 0  # pairs that the map function emitted, before any combiner
    messages: list[tuple[int, int, Any, Any]] = field(default_factory=list)
    reducer_pairs: list[int] = field(default_factory=list)
    reducer_bytes: list[int] = field(default_factory=list)

    @property
    def pairs_sent(self) -> int:
        return len(self.messages)

    @property
    def bytes_sent(self) -> int:
        return sum(pair_size(k, v) for _, _, k, v in self.messages)

    @property
    def max_reducer_pairs(self) -> int:
        return max(self.reducer_pairs, default=0)

    @property
    def max_reducer_bytes(self) -> int:
        return max(self.reducer_bytes, default=0)


def group_sorted(pairs: list[Pair], sort_key: Callable[[Any], Any],
                 group_key: Callable[[Any], Any]) -> list[tuple[Any, list[Any]]]:
    """Sort pairs by sort_key(key) (a stable sort) and group runs with equal group_key(key).

    Each group is (the first key of the run, the values in sorted order).
    """
    ordered = sorted(pairs, key=lambda kv: sort_key(kv[0]))
    groups = []
    for _, run in itertools.groupby(ordered, key=lambda kv: group_key(kv[0])):
        run = list(run)
        groups.append((run[0][0], [v for _, v in run]))
    return groups


def combine(pairs: list[Pair], combiner: Reducer, sort_key: Callable[[Any], Any],
            group_key: Callable[[Any], Any]) -> list[Pair]:
    """Run the combiner once on each key group of one map task's buffer."""
    out: list[Pair] = []
    for key, values in group_sorted(pairs, sort_key, group_key):
        out.extend(combiner(key, values))
    return out


def run_map_task(split: list[Pair], mapper: Mapper, combiner: Reducer | None,
                 spill: int | None, merge_combine: bool, sort_key: Callable[[Any], Any],
                 group_key: Callable[[Any], Any]) -> tuple[list[Pair], int]:
    """Map one split. Return (the pairs to send, the number of pairs map emitted).

    With a combiner, the buffer is cut into spills of at most `spill` pairs, the
    combiner runs on each spill, and with merge_combine it runs once more on the
    merged spills. So the combiner can run once or twice on a value; with no
    combiner it runs zero times. A correct job gives the same output in each case.
    """
    emitted = [kv for k, v in split for kv in mapper(k, v)]
    if combiner is None:
        return emitted, len(emitted)
    size = spill if spill else max(1, len(emitted))
    spills = [emitted[i:i + size] for i in range(0, len(emitted), size)]
    out = [kv for s in spills for kv in combine(s, combiner, sort_key, group_key)]
    if merge_combine:
        out = combine(out, combiner, sort_key, group_key)
    return out, len(emitted)


def run_round(splits: list[list[Pair]], mapper: Mapper, reducer: Reducer | None, r: int,
              combiner: Reducer | None = None, partitioner: Partitioner = hash_partitioner,
              sort_key: Callable[[Any], Any] | None = None,
              group_key: Callable[[Any], Any] | None = None, spill: int | None = None,
              merge_combine: bool = False,
              rng: random.Random | None = None) -> tuple[list[list[Pair]], RoundStats]:
    """Run one MapReduce round on M = len(splits) map tasks and r reducers.

    With r = 0 the job is map only: each map task writes its own output and
    nothing is shuffled. With rng, each reducer receives its messages in a
    random order before the sort, as on a real cluster, so the order of values
    within a key is not fixed. Returns (one output list per reducer, or per map
    task when r = 0; the stats of the round).
    Cost of the simulation: O(P log P) time for P intermediate pairs.
    """
    sort_key = sort_key or (lambda k: k)
    group_key = group_key or (lambda k: k)
    stats = RoundStats(map_tasks=len(splits), reducers=r)
    # Map phase: the map tasks are independent of each other.
    results = [run_map_task(s, mapper, combiner, spill, merge_combine, sort_key, group_key)
               for s in splits]
    stats.map_output_pairs = sum(n for _, n in results)
    if r == 0:
        return [out for out, _ in results], stats
    # Partition: each pair becomes one message to the reducer that owns its key.
    for src, (out, _) in enumerate(results):
        for k, v in out:
            dst = partitioner(k, r)
            if not 0 <= dst < r:
                raise ValueError(f"partitioner sent key {k!r} to reducer {dst}, not in [0, {r})")
            stats.messages.append((src, dst, k, v))
    # Shuffle: deliver every message to its reducer.
    inbox: list[list[Pair]] = [[] for _ in range(r)]
    for _, dst, k, v in stats.messages:
        inbox[dst].append((k, v))
    if rng is not None:
        for box in inbox:
            rng.shuffle(box)
    stats.reducer_pairs = [len(box) for box in inbox]
    stats.reducer_bytes = [sum(pair_size(k, v) for k, v in box) for box in inbox]
    # Sort, group and reduce: the reducers are independent of each other.
    outputs = [[kv for key, values in group_sorted(box, sort_key, group_key)
                for kv in reducer(key, values)] for box in inbox]
    return outputs, stats


def run_job(splits: list[list[Pair]], stages: list[dict[str, Any]]) -> tuple[list[list[Pair]], list[RoundStats]]:
    """Run rounds one after another. Each reducer's output is one split of the next round."""
    all_stats = []
    for stage in stages:
        splits, stats = run_round(splits, **stage)
        all_stats.append(stats)
    return splits, all_stats


def make_splits(records: list[Pair], m: int) -> list[list[Pair]]:
    """Cut the input into m splits of consecutive records (sizes differ by at most one)."""
    n = len(records)
    bounds = [i * n // m for i in range(m + 1)]
    return [records[bounds[i]:bounds[i + 1]] for i in range(m)]


# The word count job, the example of the page.

def word_count_map(doc_id: Any, text: str) -> Iterable[Pair]:
    for w in text.split():
        yield (w, 1)


def sum_reduce(key: Any, values: list[int]) -> Iterable[Pair]:
    yield (key, sum(values))
