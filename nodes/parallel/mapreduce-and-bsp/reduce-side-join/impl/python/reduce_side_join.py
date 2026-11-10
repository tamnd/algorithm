# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduce-side-join/. The authors are listed in prov/2FMSJX.jsonl.

"""The reduce-side (repartition) join of R(A, B) and S(B, C) on B, on a small MapReduce simulator.

Map tags each tuple with its relation and emits it under its join key b.
The shuffle sends key b to reducer h(b) mod k. The reducer for b splits its
values by tag and outputs the cross product. With buffer_r_only, the tag is
part of the key (a secondary sort), so the R tuples of b arrive first and the
reducer buffers only them while the S tuples stream past.
"""

import itertools
import zlib
from dataclasses import dataclass, field
from typing import Any


def h(key: Any) -> int:
    """A hash that is the same in every process."""
    return zlib.crc32(repr(key).encode("utf-8"))


@dataclass
class JoinStats:
    pairs_sent: int = 0
    reducer_input: list[int] = field(default_factory=list)
    largest_buffer: int = 0  # most tuples one reduce call holds in memory at once

    @property
    def largest_reducer_input(self) -> int:
        return max(self.reducer_input, default=0)


def reduce_side_join(r_rel: list[tuple[Any, Any]], s_rel: list[tuple[Any, Any]], k: int,
                     buffer_r_only: bool = False) -> tuple[list[tuple[Any, Any, Any]], JoinStats]:
    """Join R(A, B) and S(B, C) on B with k reducers. Bag semantics: duplicates are kept."""
    stats = JoinStats(reducer_input=[0] * k)
    inbox: list[list[tuple[Any, tuple[int, Any]]]] = [[] for _ in range(k)]
    map_out = [(b, (0, a)) for a, b in r_rel]  # @line L1
    map_out += [(b, (1, c)) for b, c in s_rel]  # @line L2
    for b, tagged in map_out:  # @line L3
        inbox[h(b) % k].append((b, tagged))
        stats.pairs_sent += 1
    output = []
    for j, box in enumerate(inbox):  # the reducers are independent
        stats.reducer_input[j] = len(box)
        if buffer_r_only:
            box.sort(key=lambda kv: (repr(kv[0]), kv[1][0]))  # sort by (b, tag): R before S
        else:
            box.sort(key=lambda kv: repr(kv[0]))  # group by b; the tags arrive in any order
        for b, run in itertools.groupby(box, key=lambda kv: kv[0]):  # @line L4
            if buffer_r_only:
                xs: list[Any] = []
                for _, (tag, val) in run:
                    if tag == 0:
                        xs.append(val)  # R tuples come first: buffer them
                    else:
                        output.extend((a, b, val) for a in xs)  # stream each S tuple past them
                stats.largest_buffer = max(stats.largest_buffer, len(xs))
                continue
            values = [tagged for _, tagged in run]
            xs = [v for tag, v in values if tag == 0]  # @line L5
            ys = [v for tag, v in values if tag == 1]  # @line L6
            stats.largest_buffer = max(stats.largest_buffer, len(values))
            output.extend((a, b, c) for a in xs for c in ys)  # @line L7
    return output, stats


def nested_loop_join(r_rel: list[tuple[Any, Any]], s_rel: list[tuple[Any, Any]]) -> list[tuple[Any, Any, Any]]:
    """The one-machine reference."""
    return [(a, b, c) for a, b in r_rel for b2, c in s_rel if b == b2]


def join_size(r_rel: list[tuple[Any, Any]], s_rel: list[tuple[Any, Any]]) -> int:
    """sum over b of |R_b| * |S_b|."""
    count_r: dict[Any, int] = {}
    for _, b in r_rel:
        count_r[b] = count_r.get(b, 0) + 1
    return sum(count_r.get(b, 0) for b, _ in s_rel)
