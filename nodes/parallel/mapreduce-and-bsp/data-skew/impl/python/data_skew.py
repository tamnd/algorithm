# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/data-skew/. The authors are listed in prov/95KA9B.jsonl.

"""Data skew in MapReduce: the loads it causes and three fixes, on a small simulator.

- hash_loads: the reducer inputs under a hash partitioner, one pair per occurrence.
- salted_sum: a sum by key in two rounds, where heavy keys get a random salt in round 1.
- lpt_partition: a skew-aware partitioner that puts the keys on reducers by the
  longest-processing-time-first greedy rule, from known key counts.
- skew_join: the join of R(A, B) and S(B, C) on B with the heavy hitter method of
  Beame, Koutris and Suciu (PODS 2014, Section 4.1): light values by hash, values
  heavy in one relation by spreading that side and broadcasting the other, and
  values heavy in both relations on a grid of servers of their own.
"""

import heapq
import math
import random
import zlib
from collections import Counter
from dataclasses import dataclass, field
from typing import Any


def h(key: Any, salt: str = "") -> int:
    """A hash that is the same in every process."""
    return zlib.crc32(f"{salt}\x00{key!r}".encode("utf-8"))


def hash_loads(keys: list[Any], r: int) -> list[int]:
    """The input of each of r reducers when each occurrence of a key sends one pair to h(key) mod r."""
    loads = [0] * r
    for key in keys:
        loads[h(key) % r] += 1
    return loads


@dataclass
class SaltStats:
    round1_input: list[int] = field(default_factory=list)
    round2_input: list[int] = field(default_factory=list)
    pairs_sent: int = 0


def salted_sum(pairs: list[tuple[Any, int]], r: int, heavy: set[Any], salts: int,
               rng: random.Random) -> tuple[dict[Any, int], SaltStats]:
    """Sum the values of each key. A heavy key is sent as (key, salt) with a random salt in
    0 .. salts - 1, so its pairs spread over up to `salts` reducers in round 1. Round 2 adds
    the partial sums of each heavy key. Light keys finish in round 1."""
    stats = SaltStats(round1_input=[0] * r, round2_input=[0] * r)
    round1: list[Counter] = [Counter() for _ in range(r)]
    for key, v in pairs:
        skey = (key, rng.randrange(salts)) if key in heavy else (key, None)
        j = h(skey) % r
        round1[j][skey] += v
        stats.round1_input[j] += 1
        stats.pairs_sent += 1
    result: dict[Any, int] = {}
    round2: list[Counter] = [Counter() for _ in range(r)]
    for part in round1:
        for (key, salt), total in part.items():
            if salt is None:
                result[key] = total
            else:
                j = h(key) % r
                round2[j][key] += total
                stats.round2_input[j] += 1
                stats.pairs_sent += 1
    for part in round2:
        result.update(part)
    return result, stats


def lpt_partition(counts: dict[Any, int], r: int) -> tuple[dict[Any, int], list[int]]:
    """Assign whole keys to r reducers: largest count first, each to the reducer with the least load."""
    heap = [(0, j) for j in range(r)]
    assign: dict[Any, int] = {}
    loads = [0] * r
    for key, c in sorted(counts.items(), key=lambda kc: (-kc[1], repr(kc[0]))):
        load, j = heapq.heappop(heap)
        assign[key] = j
        loads[j] = load + c
        heapq.heappush(heap, (loads[j], j))
    return assign, loads


@dataclass
class SkewJoinStats:
    server_load: list[int] = field(default_factory=list)  # tuples received by each server
    pairs_sent: int = 0

    @property
    def largest_load(self) -> int:
        return max(self.server_load, default=0)


def skew_join(r_rel: list[tuple[Any, Any]], s_rel: list[tuple[Any, Any]],
              p: int) -> tuple[list[tuple[Any, Any, Any]], SkewJoinStats]:
    """Join R(A, B) and S(B, C) on B. The light part uses p servers; each heavy value gets its own servers."""
    m1, m2 = len(r_rel), len(s_rel)
    c1 = Counter(b for _, b in r_rel)
    c2 = Counter(b for b, _ in s_rel)
    heavy1 = {b for b, c in c1.items() if c * p >= m1 and m1 > 0}  # m1(b) >= m1 / p
    heavy2 = {b for b, c in c2.items() if c * p >= m2 and m2 > 0}
    h12 = heavy1 & heavy2
    sigma = sum(c1[b] * c2[b] for b in h12)

    servers: list[tuple[list, list]] = [([], []) for _ in range(p)]  # the light part
    layout: dict[Any, tuple[str, int, int, int]] = {}  # value -> (kind, first server, rows, columns)
    for b in sorted(heavy1 | heavy2, key=repr):
        first = len(servers)
        if b in h12:
            p_b = math.ceil(p * c1[b] * c2[b] / sigma)
            rows = math.ceil(math.sqrt(p_b * c1[b] / c2[b]))
            cols = math.ceil(math.sqrt(p_b * c2[b] / c1[b]))
            layout[b] = ("grid", first, rows, cols)
            servers.extend(([], []) for _ in range(rows * cols))
        elif b in heavy1:  # heavy in R only: spread R(., b), broadcast S(b, .)
            p_b = math.ceil(p * c1[b] / m1)
            layout[b] = ("spread R", first, p_b, 1)
            servers.extend(([], []) for _ in range(p_b))
        else:  # heavy in S only
            p_b = math.ceil(p * c2[b] / m2)
            layout[b] = ("spread S", first, 1, p_b)
            servers.extend(([], []) for _ in range(p_b))

    stats = SkewJoinStats()
    seen1: Counter = Counter()
    for a, b in r_rel:
        if b not in layout:
            targets = [h(b) % p]
        else:
            kind, first, rows, cols = layout[b]
            row = seen1[b] % rows  # round robin over the rows of this value
            targets = [first + row * cols + col for col in range(cols)]
        seen1[b] += 1
        for t in targets:
            servers[t][0].append((a, b))
    seen2: Counter = Counter()
    for b, c in s_rel:
        if b not in layout:
            targets = [h(b) % p]
        else:
            kind, first, rows, cols = layout[b]
            col = seen2[b] % cols
            targets = [first + row * cols + col for row in range(rows)]
        seen2[b] += 1
        for t in targets:
            servers[t][1].append((b, c))

    output = []
    for xs, ys in servers:
        stats.server_load.append(len(xs) + len(ys))
        stats.pairs_sent += len(xs) + len(ys)
        by_b: dict[Any, list[Any]] = {}
        for b, c in ys:
            by_b.setdefault(b, []).append(c)
        output.extend((a, b, c) for a, b in xs for c in by_b.get(b, ()))
    return output, stats


def skew_join_bound(r_rel: list[tuple[Any, Any]], s_rel: list[tuple[Any, Any]], p: int) -> float:
    """max(m1/p, m2/p, sqrt(sum over b heavy in both of m1(b) m2(b) / p)): the main terms of the BKS load."""
    m1, m2 = len(r_rel), len(s_rel)
    c1 = Counter(b for _, b in r_rel)
    c2 = Counter(b for b, _ in s_rel)
    sigma = sum(c1[b] * c2[b] for b in c1 if c2[b] and c1[b] * p >= m1 and c2[b] * p >= m2)
    return max(m1 / p, m2 / p, math.sqrt(sigma / p))


def zipf_keys(rng: random.Random, n: int, keys: int) -> list[int]:
    """n draws from 1 .. keys with Pr[i] proportional to 1 / i."""
    return rng.choices(range(1, keys + 1), weights=[1 / i for i in range(1, keys + 1)], k=n)
