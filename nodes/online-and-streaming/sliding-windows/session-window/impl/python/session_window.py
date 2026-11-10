# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/session-window/. The authors are listed in prov/9SPQ0S.jsonl.
"""Session windows with a gap g: the batch rule and the online merge of proto-windows."""

from bisect import bisect_left, insort
from typing import Dict, Hashable, Iterable, List, Tuple

Session = Tuple[int, int, int]  # (start, end, number of items)


def sessions_batch(times: Iterable[int], gap: int) -> List[Session]:
    """Cut the sorted timestamps of one key where two neighbours are at least `gap` apart."""
    if gap <= 0:
        raise ValueError("gap must be positive")
    ts = sorted(times)
    out: List[Session] = []
    if not ts:
        return out
    start, end, count = ts[0], ts[0] + gap, 1
    for t in ts[1:]:
        if t < end:
            end = t + gap
            count += 1
        else:
            out.append((start, end, count))
            start, end, count = t, t + gap, 1
    out.append((start, end, count))
    return out


class SessionWindows:
    """The sessions of one key, kept as disjoint sorted intervals [a, b), with items in any order."""

    def __init__(self, gap: int) -> None:
        if gap <= 0:
            raise ValueError("gap must be positive")
        self.gap = gap
        self.starts: List[int] = []
        self.info: Dict[int, Tuple[int, int]] = {}  # start -> (end, count)

    def insert(self, ts: int) -> Session:
        """Add one item (lines L1 to L4) and return its session after the merge."""
        lo, hi, count = ts, ts + self.gap, 1  # @line L1
        # Sessions overlap [ts, ts + gap) when a < ts + gap and ts < b; at most two do.
        i = bisect_left(self.starts, ts + self.gap)
        j = i - 1
        merged = 0
        while j >= 0:  # @line L2
            a = self.starts[j]
            b, c = self.info[a]
            if b <= ts:
                break
            del self.starts[j]  # @line L3
            del self.info[a]
            lo, hi, count = min(lo, a), max(hi, b), count + c
            merged += 1
            j -= 1
        assert merged <= 2
        insort(self.starts, lo)  # @line L4
        self.info[lo] = (hi, count)
        return lo, hi, count

    def sessions(self) -> List[Session]:
        return [(a, self.info[a][0], self.info[a][1]) for a in self.starts]


def sessions_by_key(events: Iterable[Tuple[Hashable, int]], gap: int) -> Dict[Hashable, List[Session]]:
    """Online sessions for (key, timestamp) pairs, one SessionWindows per key."""
    per_key: Dict[Hashable, SessionWindows] = {}
    for key, ts in events:
        per_key.setdefault(key, SessionWindows(gap)).insert(ts)
    return {k: s.sessions() for k, s in per_key.items()}
