# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tumbling-window/. The authors are listed in prov/4SW0BT.jsonl.
"""Tumbling (fixed) windows: assignment of timestamps and running sums per window."""

from typing import Dict, Iterable, Iterator, List, Tuple


def tumbling_assign(ts: int, size: int, offset: int = 0) -> Tuple[int, int]:
    """Return the window [start, end) of size `size` and offset `offset` that holds `ts`."""
    if size <= 0:
        raise ValueError("size must be positive")
    j = (ts - offset) // size  # @line L1
    return offset + j * size, offset + (j + 1) * size  # @line L2


def tumbling_sums(
    stream: Iterable[Tuple[int, int]], size: int, offset: int = 0
) -> Iterator[Tuple[int, int, int]]:
    """Yield (start, end, sum) for each nonempty window, for a stream with nondecreasing timestamps.

    The state is one open window and one partial sum, as in lines L3 to L8.
    """
    cur = None  # @line L3
    acc = 0
    last = None
    for ts, v in stream:  # @line L4
        if last is not None and ts < last:
            raise ValueError("timestamps must not decrease")
        last = ts
        start = tumbling_assign(ts, size, offset)[0]  # @line L5
        if cur is not None and start != cur:  # @line L6
            yield cur, cur + size, acc
            acc = 0
        cur = start  # @line L7
        acc += v
    if cur is not None:  # @line L8
        yield cur, cur + size, acc


def group_tumbling(
    events: Iterable[Tuple[int, int]], size: int, offset: int = 0
) -> Dict[Tuple[int, int], List[int]]:
    """Group the values of (ts, value) pairs by their tumbling window, in any order of arrival."""
    out: Dict[Tuple[int, int], List[int]] = {}
    for ts, v in events:
        out.setdefault(tumbling_assign(ts, size, offset), []).append(v)
    return out
