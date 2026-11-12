# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-buddy-system/. The authors are listed in prov/QQ2EAC.jsonl.

"""The lazy buddy system of Barkley and Lee (1989), over a binary buddy heap.

Each class k (blocks of 2^k words) has three kinds of blocks: active
(allocated), locally free (free, but still marked as in use for the buddy
logic, so it never merges) and globally free (free and merged with its buddy
when possible). The slack of class k is D = active - locally free. A free
picks one of three modes from D: lazy (D >= 2), reclaiming (D = 1) or
accelerated (D = 0). So D never drops below 0, and each class keeps at most
as many locally free blocks as it has active blocks.

The flag flush_on_failure is an addition of this implementation, not a rule
of the paper: when a request fails, it frees all locally free blocks globally
and tries once more.
"""


class LazyBuddySystem:
    """Binary buddy allocator over 2^m words with lazy coalescing.

    With lazy=False every free is global, which is the eager buddy system.
    """

    def __init__(self, m: int, lazy: bool = True, flush_on_failure: bool = False) -> None:
        if m < 0:
            raise ValueError("m must be at least 0")
        self.m = m
        self.lazy = lazy
        self.flush_on_failure = flush_on_failure
        self.local: list[dict[int, None]] = [{} for _ in range(m + 1)]
        self.glob: list[dict[int, None]] = [{} for _ in range(m + 1)]
        self.glob[m][0] = None
        self.active = [0] * (m + 1)
        self.allocated: dict[int, int] = {}  # address -> order
        self.splits = 0
        self.merges = 0

    def slack(self, k: int) -> int:
        """D = active - locally free for class k."""
        return self.active[k] - len(self.local[k])

    def _take(self, k: int) -> int | None:
        if self.local[k]:  # @line L2
            p, _ = self.local[k].popitem()
            return p
        if self.glob[k]:  # @line L3
            p, _ = self.glob[k].popitem()
            return p
        j = k + 1  # @line L4
        while j <= self.m and not self.local[j] and not self.glob[j]:
            j += 1
        if j > self.m:
            return None
        src = self.local[j] if self.local[j] else self.glob[j]
        p, _ = src.popitem()
        while j > k:  # split down; each upper half is globally free
            j -= 1
            self.glob[j][p + (1 << j)] = None
            self.splits += 1
        return p

    def malloc(self, n: int) -> int | None:
        """Allocate 2^k >= n words. Return the address, or None."""
        if n < 1:
            raise ValueError("n must be at least 1")
        k = (n - 1).bit_length()  # @line L1
        if k > self.m:
            return None
        p = self._take(k)
        if p is None and self.flush_on_failure:
            self.flush()
            p = self._take(k)
        if p is None:
            return None
        self.active[k] += 1  # @line L5
        self.allocated[p] = k
        return p

    def free(self, p: int) -> None:
        """Free the block at address p, which malloc returned."""
        if p not in self.allocated:
            raise ValueError("p is not an allocated block")
        k = self.allocated.pop(p)  # @line L6
        d = self.slack(k)
        self.active[k] -= 1
        if not self.lazy:
            self._global_free(p, k)
        elif d >= 2:  # @line L7
            self.local[k][p] = None
        elif d == 1:  # @line L8
            self._global_free(p, k)
        else:  # @line L9
            q, _ = self.local[k].popitem()
            self._global_free(p, k)
            self._global_free(q, k)

    def _global_free(self, p: int, k: int) -> None:
        while k < self.m and (p ^ (1 << k)) in self.glob[k]:  # @line L10
            del self.glob[k][p ^ (1 << k)]  # @line L11
            p = min(p, p ^ (1 << k))
            k += 1
            self.merges += 1
        self.glob[k][p] = None  # @line L12

    def flush(self) -> None:
        """Free every locally free block globally."""
        for k in range(self.m + 1):
            while self.local[k]:
                q, _ = self.local[k].popitem()
                self._global_free(q, k)

    def free_blocks(self) -> tuple[list[set[int]], list[set[int]]]:
        """(locally free, globally free) as sets of addresses per class."""
        return [set(x) for x in self.local], [set(x) for x in self.glob]

    def check_invariant(self) -> None:
        """Raise AssertionError unless the state is legal."""
        blocks = [(p, k) for p, k in self.allocated.items()]
        for k in range(self.m + 1):
            blocks += [(p, k) for p in self.local[k]]
            blocks += [(p, k) for p in self.glob[k]]
            assert len(self.local[k]) <= self.active[k], "D must stay at least 0"
            assert self.active[k] == sum(1 for o in self.allocated.values() if o == k)
            for p in self.glob[k]:
                assert p % (1 << k) == 0, "blocks are aligned"
                if k < self.m:
                    assert (p ^ (1 << k)) not in self.glob[k], "no globally free buddies"
        pos = 0
        for p, k in sorted(blocks):
            assert p == pos, "blocks must tile the heap"
            pos = p + (1 << k)
        assert pos == 1 << self.m
