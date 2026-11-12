# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lrfu/. The authors are listed in prov/ETPAQ6.jsonl.

import heapq
import math
from collections.abc import Hashable, Iterable


class LRFU:
    """LRFU (Lee et al. 2001) on a cache of k blocks with the parameter lam.

    Each resident block b has a combined recency and frequency value
    CRF(b) = sum of F(t - t_i) over its references t_i since it was loaded,
    with F(x) = (1/2)^(lam x). The block with the least CRF is evicted.
    C[b] holds the CRF at the time last[b] of the last reference, and the CRF
    at time t is C[b] * 2^(-lam (t - last[b])). All blocks decay by the same
    factor, so the order is that of log2 C[b] + lam * last[b], which does not
    change while b is not referenced. A min-heap on this key, with ties to the
    older last reference, finds the victim. Heap entries of old keys are
    skipped (lazy deletion), and the heap is rebuilt when it grows too large.
    """

    def __init__(self, k: int, lam: float) -> None:
        if k < 1 or not 0.0 <= lam <= 1.0:
            raise ValueError("need k >= 1 and 0 <= lam <= 1")
        self.k, self.lam = k, lam
        self.crf: dict[Hashable, float] = {}
        self.last: dict[Hashable, int] = {}
        self.heap: list[tuple[float, int, Hashable]] = []
        self.t = 0
        self.evicted: Hashable | None = None

    def __contains__(self, x: Hashable) -> bool:
        return x in self.crf

    def __len__(self) -> int:
        return len(self.crf)

    def value(self, x: Hashable) -> float:
        """The CRF of the resident block x at the current time."""
        return self.crf[x] * 2.0 ** (-self.lam * (self.t - self.last[x]))

    def _key(self, x: Hashable) -> tuple[float, int, Hashable]:
        return (math.log2(self.crf[x]) + self.lam * self.last[x], self.last[x], x)

    def _push(self, x: Hashable) -> None:
        heapq.heappush(self.heap, self._key(x))
        if len(self.heap) > 2 * self.k + 16:
            self.heap = [self._key(y) for y in self.crf]
            heapq.heapify(self.heap)

    def access(self, x: Hashable) -> bool:
        """Serve one request. Return True on a hit, False on a miss."""
        self.evicted = None
        self.t += 1  # @line L1
        if x in self.crf:  # @line L2
            d = self.t - self.last[x]
            self.crf[x] = 1.0 + 2.0 ** (-self.lam * d) * self.crf[x]  # @line L3
            self.last[x] = self.t
            self._push(x)  # @line L4
            return True
        if len(self.crf) == self.k:  # @line L5
            while True:  # @line L6
                _, s, v = heapq.heappop(self.heap)
                if v in self.last and self.last[v] == s:
                    break
            del self.crf[v], self.last[v]  # @line L7
            self.evicted = v
        self.crf[x] = 1.0  # @line L8
        self.last[x] = self.t
        self._push(x)  # @line L9
        return False


def lrfu_hits(trace: Iterable[Hashable], k: int, lam: float) -> list[bool]:
    """Run LRFU with k blocks and the parameter lam."""
    cache = LRFU(k, lam)
    return [cache.access(x) for x in trace]
