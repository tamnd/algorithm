# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clock-pro/. The authors are listed in prov/P3XQXT.jsonl.

from collections.abc import Hashable, Iterable


class _Entry:
    __slots__ = ("key", "hot", "resident", "ref", "test", "prev", "next")

    def __init__(self, key: Hashable) -> None:
        self.key = key
        self.hot = False
        self.resident = True
        self.ref = False
        self.test = True
        self.prev: _Entry = self
        self.next: _Entry = self


class ClockPro:
    """CLOCK-Pro of Jiang, Chen and Zhang (USENIX ATC 2005) for m pages.

    One circular list holds hot pages, resident cold pages and non-resident
    cold pages. The head of the list is the place just behind HAND_hot, which
    is the place that HAND_hot reaches last. Removing an entry under a hand
    moves that hand to the next entry.

    Two choices are ours, because the paper leaves them open: a resident
    cold page that HAND_cold finds with its bit set but out of its test
    period starts a new test period, and the hot pages are kept at or below
    m - mc by running HAND_hot after each page turns hot.
    """

    def __init__(self, m: int, mc: int | None = None, adaptive: bool = True) -> None:
        if m < 2:
            raise ValueError("CLOCK-Pro needs at least two pages")
        self.m = m
        self.mc = max(1, m // 100) if mc is None else mc
        if not 1 <= self.mc <= m - 1:
            raise ValueError("mc must be between 1 and m - 1")
        self.adaptive = adaptive
        self.table: dict[Hashable, _Entry] = {}
        self.hand_hot: _Entry | None = None
        self.hand_cold: _Entry | None = None
        self.hand_test: _Entry | None = None
        self.n_hot = 0
        self.n_cold = 0  # resident cold pages
        self.n_nonres = 0  # non-resident cold pages
        self.evicted: Hashable | None = None

    def __contains__(self, x: Hashable) -> bool:
        e = self.table.get(x)
        return e is not None and e.resident

    def __len__(self) -> int:
        return self.n_hot + self.n_cold

    def access(self, x: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        e = self.table.get(x)
        if e is not None and e.resident:  # @line L1
            e.ref = True  # @line L2
            return True
        if len(self) == self.m:  # @line L3
            self._run_hand_cold()  # @line L4
        e = self.table.get(x)
        if e is not None:  # @line L5
            self._grow_cold()  # @line L6
            e.hot, e.resident, e.ref, e.test = True, True, False, False  # @line L7
            self.n_nonres -= 1
            self.n_hot += 1
            self._to_head(e)
            self._balance()  # @line L8
        else:  # @line L9
            e = _Entry(x)  # @line L10
            self.table[x] = e
            self._insert_head(e)
            self.n_cold += 1
        return False  # @line L11

    # The list.

    def _insert_head(self, e: _Entry) -> None:
        if self.hand_hot is None:
            e.prev = e.next = e
            self.hand_hot = self.hand_cold = self.hand_test = e
            return
        h = self.hand_hot
        e.prev, e.next = h.prev, h
        h.prev.next = e
        h.prev = e

    def _unlink(self, e: _Entry) -> None:
        nxt = None if e.next is e else e.next
        if self.hand_hot is e:
            self.hand_hot = nxt
        if self.hand_cold is e:
            self.hand_cold = nxt
        if self.hand_test is e:
            self.hand_test = nxt
        e.prev.next = e.next
        e.next.prev = e.prev
        e.prev = e.next = e

    def _to_head(self, e: _Entry) -> None:
        self._unlink(e)
        self._insert_head(e)

    def _remove(self, e: _Entry) -> None:
        self._unlink(e)
        del self.table[e.key]

    # The adaptive target.

    def _grow_cold(self) -> None:
        if self.adaptive:
            self.mc = min(self.mc + 1, self.m - 1)

    def _shrink_cold(self) -> None:
        if self.adaptive:
            self.mc = max(self.mc - 1, 1)

    # The hands.

    def _run_hand_cold(self) -> None:
        while True:  # @line L12
            e = self.hand_cold  # @line L13
            if e.hot or not e.resident:  # @line L14
                self.hand_cold = e.next
            elif not e.ref:  # @line L15
                e.resident = False  # @line L16
                self.n_cold -= 1
                self.evicted = e.key
                if e.test:
                    self.n_nonres += 1
                    self.hand_cold = e.next  # @line L17
                else:
                    self._remove(e)
                while self.n_nonres > self.m:  # @line L18
                    self._run_hand_test()
                return  # @line L19
            elif e.test:  # @line L20
                e.ref, e.hot, e.test = False, True, False  # @line L21
                self.n_cold -= 1
                self.n_hot += 1
                self._grow_cold()
                self._to_head(e)
                self._balance()  # @line L22
            else:  # @line L23
                e.ref, e.test = False, True  # @line L24
                self._to_head(e)

    def _balance(self) -> None:
        while self.n_hot > self.m - self.mc:  # @line L25
            self._run_hand_hot()

    def _end_test(self, e: _Entry, hand: str) -> None:
        """Lines L29 and L30 (or L34 and L35) for a cold entry under a hand."""
        if e.test:  # @line L29
            e.test = False
            self._shrink_cold()
        if not e.resident:  # @line L30
            self.n_nonres -= 1
            self._remove(e)
        else:
            setattr(self, hand, e.next)

    def _run_hand_hot(self) -> None:
        while True:  # @line L26
            e = self.hand_hot  # @line L27
            if not e.hot:  # @line L28
                self._end_test(e, "hand_hot")
            elif e.ref:  # @line L31
                e.ref = False
                self.hand_hot = e.next
            else:  # @line L32
                e.hot = False
                self.n_hot -= 1
                self.n_cold += 1
                self.hand_hot = e.next
                return

    def _run_hand_test(self) -> None:
        e = self.hand_test  # @line L33
        if not e.hot:  # @line L34
            self._end_test(e, "hand_test")  # @line L35
        else:
            self.hand_test = e.next


def clock_pro_hits(trace: Iterable[Hashable], m: int, mc: int | None = None, adaptive: bool = True) -> list[bool]:
    """Run CLOCK-Pro with m pages on the trace. Return one hit flag per request."""
    cache = ClockPro(m, mc, adaptive)
    return [cache.access(x) for x in trace]
