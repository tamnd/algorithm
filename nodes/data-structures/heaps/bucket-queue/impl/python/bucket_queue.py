# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bucket-queue/. The authors are listed in prov/DVKCF0.jsonl.

from collections.abc import Hashable
from typing import Generic, TypeVar

H = TypeVar("H", bound=Hashable)


class BucketQueue(Generic[H]):
    """A min-priority queue of items with integer keys in 0 .. c.

    B[k] holds the items with key k, in insertion order. key[x] is the key of
    item x. cur is a lower bound on the smallest key in the queue.
    insert, delete and decrease_key take O(1) time; extract_min takes
    O(1 + s) time, where s is the number of empty buckets it skips.
    """

    def __init__(self, c: int) -> None:
        if c < 0:
            raise ValueError("c must be at least 0")
        self.c = c
        self.buckets: list[dict[H, None]] = [{} for _ in range(c + 1)]
        self.key: dict[H, int] = {}
        self.cur = c + 1

    def __len__(self) -> int:
        return len(self.key)

    def __contains__(self, x: H) -> bool:
        return x in self.key

    def insert(self, x: H, k: int) -> None:
        if not 0 <= k <= self.c:  # @line L1
            raise ValueError("key out of range")
        if x in self.key:
            raise KeyError("item already in the queue")
        self.buckets[k][x] = None  # @line L2
        self.key[x] = k
        if k < self.cur:  # @line L3
            self.cur = k

    def delete(self, x: H) -> int:
        k = self.key.pop(x)  # @line L4
        del self.buckets[k][x]
        return k

    def decrease_key(self, x: H, k: int) -> None:
        if k > self.key[x]:  # @line L5
            raise ValueError("new key is larger than the current key")
        self.delete(x)  # @line L6
        self.insert(x, k)

    def find_min(self) -> tuple[H, int]:
        if not self.key:
            raise IndexError("find_min from an empty queue")
        while not self.buckets[self.cur]:
            self.cur += 1
        x = next(iter(self.buckets[self.cur]))
        return x, self.cur

    def extract_min(self) -> tuple[H, int]:
        if not self.key:  # @line L7
            raise IndexError("extract_min from an empty queue")
        while not self.buckets[self.cur]:  # @line L8
            self.cur += 1
        x = next(iter(self.buckets[self.cur]))  # @line L9
        self.delete(x)  # @line L10
        return x, self.cur  # @line L11

    def check_invariant(self) -> None:
        seen = 0
        for k, b in enumerate(self.buckets):
            for x in b:
                assert self.key[x] == k
                assert k >= self.cur
                seen += 1
        assert seen == len(self.key)
