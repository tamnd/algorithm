# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timing-wheel/. The authors are listed in prov/GFWMKW.jsonl.

"""Timing wheels of Varghese and Lauck (SOSP 1987).

HashedWheel is Scheme 6: a circular array of N buckets, where a timer that
expires at tick e lives in bucket e mod N with a count of the full turns
that are left. With N larger than every interval it is the simple wheel of
Scheme 4. HierarchicalWheel is Scheme 7: several wheels, one per digit of
the expiry time in base N, with timers moved down a level when the digit
above them is reached. Each bucket is a dict, so START-TIMER and
STOP-TIMER take O(1) time, as with the doubly linked lists of the paper.
"""


class HashedWheel:
    def __init__(self, size: int) -> None:
        if size < 1:
            raise ValueError("size must be at least 1")
        self.size = size
        self.now = 0
        self.buckets: list[dict] = [{} for _ in range(size)]  # id -> rounds left
        self.where: dict = {}  # id -> bucket index

    def start_timer(self, tid, interval: int) -> None:
        """Make timer tid fire after interval >= 1 ticks."""
        if interval < 1:
            raise ValueError("interval must be at least 1 tick")
        if tid in self.where:
            raise ValueError("timer is already running")
        expiry = self.now + interval  # @line L1
        slot = expiry % self.size  # @line L2
        self.buckets[slot][tid] = (interval - 1) // self.size  # @line L3
        self.where[tid] = slot

    def stop_timer(self, tid) -> bool:
        """Cancel timer tid; return False if it is not running."""
        slot = self.where.pop(tid, None)  # @line L4
        if slot is None:
            return False
        del self.buckets[slot][tid]
        return True

    def tick(self) -> list:
        """Advance the clock by one tick; return the timers that expire, in start order."""
        self.now += 1  # @line L5
        bucket = self.buckets[self.now % self.size]
        fired = []
        for tid in list(bucket):  # @line L6
            if bucket[tid] == 0:  # @line L7
                del bucket[tid]
                del self.where[tid]
                fired.append(tid)
            else:
                bucket[tid] -= 1  # @line L8
        return fired

    def __len__(self) -> int:
        return len(self.where)


class HierarchicalWheel:
    """Scheme 7: `levels` wheels of `size` buckets each, plus an overflow list.

    A timer with expiry e > now sits on the highest level k at which the base
    `size` digits of e and now differ, in bucket digit_k(e). When the clock
    reaches a multiple of size**k, the bucket digit_k(now) of level k is
    emptied and its timers are placed again, on lower levels.
    """

    def __init__(self, size: int, levels: int) -> None:
        if size < 2 or levels < 1:
            raise ValueError("need size >= 2 and levels >= 1")
        self.size, self.levels = size, levels
        self.now = 0
        self.wheels = [[{} for _ in range(size)] for _ in range(levels)]
        self.overflow: dict = {}
        self.where: dict = {}  # id -> the dict that holds it
        self.expiry: dict = {}
        self.order: dict = {}  # id -> start number, to fire in start order
        self.count = 0
        self.moves = 0  # timers placed again by cascades, for the tests

    def _digit(self, x: int, k: int) -> int:
        return (x // self.size**k) % self.size

    def _place(self, tid) -> None:
        e = self.expiry[tid]
        if e // self.size**self.levels != self.now // self.size**self.levels:
            home = self.overflow
        else:
            k = 0
            for j in range(self.levels - 1, 0, -1):
                if self._digit(e, j) != self._digit(self.now, j):
                    k = j
                    break
            home = self.wheels[k][self._digit(e, k)]
        home[tid] = True
        self.where[tid] = home

    def start_timer(self, tid, interval: int) -> None:
        if interval < 1:
            raise ValueError("interval must be at least 1 tick")
        if tid in self.where:
            raise ValueError("timer is already running")
        self.expiry[tid] = self.now + interval
        self.order[tid] = self.count
        self.count += 1
        self._place(tid)

    def stop_timer(self, tid) -> bool:
        home = self.where.pop(tid, None)
        if home is None:
            return False
        del home[tid]
        del self.expiry[tid], self.order[tid]
        return True

    def _cascade(self, bucket: dict) -> None:
        items = list(bucket)
        bucket.clear()
        for tid in items:
            self.moves += 1
            self._place(tid)

    def tick(self) -> list:
        self.now += 1
        if self.now % self.size**self.levels == 0:
            self._cascade(self.overflow)
        for k in range(self.levels - 1, 0, -1):
            if self.now % self.size**k == 0:
                self._cascade(self.wheels[k][self._digit(self.now, k)])
        bucket = self.wheels[0][self._digit(self.now, 0)]
        fired = sorted(bucket, key=self.order.__getitem__)
        bucket.clear()
        for tid in fired:
            assert self.expiry[tid] == self.now
            del self.where[tid], self.expiry[tid], self.order[tid]
        return fired

    def __len__(self) -> int:
        return len(self.where)
