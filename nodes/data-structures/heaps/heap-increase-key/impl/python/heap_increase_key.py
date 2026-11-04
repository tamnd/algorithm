# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-increase-key/. The authors are listed in prov/ZN9K6H.jsonl.

from typing import Any, Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def heap_increase_key(a: list[T], i: int, key: T) -> None:
    """Raise a[i] to key in the max-heap a (0-based) and move it up. O(log n) time."""
    if not 0 <= i < len(a):
        raise IndexError("index out of range")
    if key < a[i]:  # @line L1
        raise ValueError("new key is smaller than the current key")
    a[i] = key  # @line L2
    while i > 0 and a[(i - 1) // 2] < a[i]:  # @line L3
        p = (i - 1) // 2
        a[i], a[p] = a[p], a[i]  # @line L4
        i = p  # @line L5


def max_heap_insert(a: list[T], key: T) -> None:
    """Insert key into the max-heap a by an increase from a key at most each other key."""
    a.append(key)
    heap_increase_key(a, len(a) - 1, key)
