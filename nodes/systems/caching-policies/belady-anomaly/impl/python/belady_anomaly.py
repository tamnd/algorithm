# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belady-anomaly/. The authors are listed in prov/8EZ63W.jsonl.

"""Belady's anomaly: FIFO can have more faults with more frames. Simulators and a search for anomalies."""

import itertools
from collections import OrderedDict
from typing import Callable, Hashable, List, Optional, Sequence, Tuple


def fifo_trace(seq: Sequence[Hashable], frames: int) -> List[Tuple[bool, Tuple[Hashable, ...]]]:
    """For each request: (fault, the queue after the request, oldest first)."""
    queue: List[Hashable] = []
    out = []
    for x in seq:
        fault = x not in queue
        if fault:
            if len(queue) == frames:
                queue.pop(0)
            queue.append(x)
        out.append((fault, tuple(queue)))
    return out


def fifo_faults(seq: Sequence[Hashable], frames: int) -> int:
    return sum(1 for fault, _ in fifo_trace(seq, frames) if fault)


def lru_faults(seq: Sequence[Hashable], frames: int) -> int:
    cache: "OrderedDict[Hashable, bool]" = OrderedDict()
    faults = 0
    for x in seq:
        if x in cache:
            cache.move_to_end(x)
        else:
            faults += 1
            if len(cache) == frames:
                cache.popitem(last=False)
            cache[x] = True
    return faults


def second_chance_faults(seq: Sequence[Hashable], frames: int) -> int:
    """CLOCK in the form that sets the reference bit on a hit only, not on a load."""
    slot: List[Optional[Hashable]] = [None] * frames
    ref = [False] * frames
    hand = 0
    faults = 0
    for x in seq:
        if x in slot:
            ref[slot.index(x)] = True
            continue
        faults += 1
        while slot[hand] is not None and ref[hand]:
            ref[hand] = False
            hand = (hand + 1) % frames
        slot[hand] = x
        ref[hand] = False
        hand = (hand + 1) % frames
    return faults


def find_anomaly(policy: Callable[[Sequence[Hashable], int], int], pages: int, max_len: int,
                 max_frames: int) -> Optional[Tuple[Tuple[int, ...], int]]:
    """The first sequence, by length, over pages 1 .. pages, with policy(seq, f + 1) > policy(seq, f)."""
    for n in range(1, max_len + 1):
        for seq in itertools.product(range(1, pages + 1), repeat=n):
            faults = [policy(seq, f) for f in range(1, max_frames + 1)]
            for f in range(1, max_frames):
                if faults[f] > faults[f - 1]:
                    return seq, f
    return None
