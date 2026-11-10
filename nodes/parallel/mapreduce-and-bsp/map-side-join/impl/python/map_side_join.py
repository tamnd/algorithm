# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/map-side-join/. The authors are listed in prov/MES4WN.jsonl.

"""Map-side joins of R(A, B) and S(B, C) on B, with no shuffle.

broadcast_join copies the small relation S to every map task. Each task builds
a hash table of S on b and probes it with its own split of R.

merge_join joins part i of R with part i of S, when both inputs were cut into
the same parts by the same partitioner on b and each part is sorted by b, as
the outputs of two earlier MapReduce jobs with the same reducers are. Each map
task merges its two parts like a sort-merge join.
"""

import zlib
from dataclasses import dataclass, field
from typing import Any

Rel = list[tuple[Any, Any]]


def h(key: Any) -> int:
    """A hash that is the same in every process."""
    return zlib.crc32(repr(key).encode("utf-8"))


@dataclass
class MapJoinStats:
    tuples_copied: int = 0  # tuples sent over the network before or instead of a shuffle
    pairs_shuffled: int = 0  # always 0: these joins are map-only
    task_input: list[int] = field(default_factory=list)  # tuples read by each map task
    task_memory: list[int] = field(default_factory=list)  # most tuples one task holds at once


def split(rel: Rel, m: int) -> list[Rel]:
    """Cut a relation into m splits of nearly equal size, in input order."""
    n = len(rel)
    return [rel[i * n // m:(i + 1) * n // m] for i in range(m)]


def broadcast_join(r_splits: list[Rel], s_rel: Rel) -> tuple[list[tuple[Any, Any, Any]], MapJoinStats]:
    """Join each split of R with a full copy of the small relation S."""
    stats = MapJoinStats()
    output = []
    stats.tuples_copied = len(s_rel) * len(r_splits)  # @line L1
    for r_split in r_splits:  # @line L2
        table: dict[Any, list[Any]] = {}  # @line L3
        for b, c in s_rel:
            table.setdefault(b, []).append(c)
        for a, b in r_split:  # @line L4
            output.extend((a, b, c) for c in table.get(b, ()))  # @line L5
        stats.task_input.append(len(r_split) + len(s_rel))
        stats.task_memory.append(len(s_rel))
    return output, stats


def co_partition(rel: Rel, k: int, key_pos: int) -> list[Rel]:
    """What an earlier job with k reducers leaves behind: part j holds the keys with h(b) mod k = j, sorted by b."""
    parts: list[Rel] = [[] for _ in range(k)]
    for t in rel:
        parts[h(t[key_pos]) % k].append(t)
    for part in parts:
        part.sort(key=lambda t: t[key_pos])  # stable: equal keys keep their input order
    return parts


def merge_join(r_part: Rel, s_part: Rel) -> tuple[list[tuple[Any, Any, Any]], int]:
    """Merge one part of R (sorted by b) with the matching part of S (sorted by b).

    Returns the output and the largest run of one key in S, which is all the task holds in memory.
    """
    output = []
    largest_run = 0
    p, q = 0, 0  # @line L6
    while p < len(r_part) and q < len(s_part):  # @line L7
        rb, sb = r_part[p][1], s_part[q][0]
        if rb < sb:  # @line L8
            p += 1
        elif rb > sb:  # @line L9
            q += 1
        else:  # @line L10
            p_end, q_end = p, q  # @line L11
            while p_end < len(r_part) and r_part[p_end][1] == rb:
                p_end += 1
            while q_end < len(s_part) and s_part[q_end][0] == rb:
                q_end += 1
            largest_run = max(largest_run, q_end - q)
            output.extend((a, rb, c) for a, _ in r_part[p:p_end] for _, c in s_part[q:q_end])  # @line L12
            p, q = p_end, q_end  # @line L13
    return output, largest_run


def is_co_partitioned(r_parts: list[Rel], s_parts: list[Rel]) -> bool:
    """Same number of parts, each part sorted by b, and no key in two different parts."""
    if len(r_parts) != len(s_parts):
        return False
    owner: dict[Any, int] = {}
    for parts, pos in ((r_parts, 1), (s_parts, 0)):
        for j, part in enumerate(parts):
            keys = [t[pos] for t in part]
            if any(x > y for x, y in zip(keys, keys[1:])):
                return False
            for b in keys:
                if owner.setdefault(b, j) != j:
                    return False
    return True


def merge_join_all(r_parts: list[Rel], s_parts: list[Rel]) -> tuple[list[tuple[Any, Any, Any]], MapJoinStats]:
    """One map task per pair of matching parts. Raises if the inputs are not co-partitioned."""
    if not is_co_partitioned(r_parts, s_parts):
        raise ValueError("the inputs are not partitioned and sorted the same way on the join key")
    stats = MapJoinStats()
    output = []
    for r_part, s_part in zip(r_parts, s_parts):
        out, run = merge_join(r_part, s_part)
        output.extend(out)
        stats.task_input.append(len(r_part) + len(s_part))
        stats.task_memory.append(run)
    return output, stats


def nested_loop_join(r_rel: Rel, s_rel: Rel) -> list[tuple[Any, Any, Any]]:
    """The one-machine reference."""
    return [(a, b, c) for a, b in r_rel for b2, c in s_rel if b == b2]
