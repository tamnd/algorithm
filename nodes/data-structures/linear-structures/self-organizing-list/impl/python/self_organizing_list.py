# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/self-organizing-list/. The authors are listed in prov/2WXV0M.jsonl.

from collections.abc import Hashable, Iterator
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

RULES = ("mtf", "transpose", "count")


class _Node(Generic[K, V]):
    __slots__ = ("key", "value", "next", "count")

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.next: _Node[K, V] | None = None
        self.count = 1


class SelfOrganizingList(Generic[K, V]):
    """A dictionary stored as a singly linked list that reorders itself on each hit.

    The rule is "mtf" (move to front), "transpose" (one place forward) or
    "count" (keep the list sorted by access count, ties in order of arrival).
    get and put of a key at position i cost Theta(i); a miss and the put of
    a new key cost Theta(n); delete costs Theta(i). Space Theta(n).
    """

    def __init__(self, rule: str = "mtf") -> None:
        if rule not in RULES:
            raise ValueError(f"rule must be one of {RULES}")
        self.rule = rule
        self.head: _Node[K, V] | None = None
        self.n = 0

    def _access(self, k: K) -> "_Node[K, V] | None":
        pp: _Node[K, V] | None = None
        prev: _Node[K, V] | None = None
        cur = self.head  # @line L1
        while cur is not None and cur.key != k:  # @line L2
            pp, prev, cur = prev, cur, cur.next  # @line L3
        if cur is None:  # @line L4
            return None
        if prev is None:  # @line L5
            self.head = cur.next
        else:
            prev.next = cur.next
        p: _Node[K, V] | None
        if self.rule == "mtf":  # @line L6
            p = None
        elif self.rule == "transpose":  # @line L7
            p = pp
        else:  # @line L8
            cur.count += 1  # @line L9
            p, q = None, self.head
            while q is not None and q.count >= cur.count:  # @line L10
                p, q = q, q.next
        if p is None:  # @line L11
            cur.next = self.head
            self.head = cur
        else:
            cur.next = p.next
            p.next = cur
        return cur  # @line L12

    def get(self, k: K) -> V | None:
        """Return the value of k, or None if k is absent. Reorders on a hit."""
        x = self._access(k)
        return None if x is None else x.value

    def put(self, k: K, v: V) -> None:
        """Associate v with k. Theta(n) for a new key."""
        x = self._access(k)
        if x is not None:
            x.value = v
            return
        x = _Node(k, v)
        self.n += 1
        if self.rule == "mtf" or self.head is None:
            x.next = self.head
            self.head = x
            return
        last = self.head
        while last.next is not None:
            last = last.next
        last.next = x

    def delete(self, k: K) -> None:
        """Remove k and its value, if present. Does not reorder the other keys."""
        prev: _Node[K, V] | None = None
        cur = self.head
        while cur is not None and cur.key != k:
            prev, cur = cur, cur.next
        if cur is None:
            return
        if prev is None:
            self.head = cur.next
        else:
            prev.next = cur.next
        self.n -= 1

    def __len__(self) -> int:
        return self.n

    def keys(self) -> Iterator[K]:
        """The keys from front to back, without reordering."""
        cur = self.head
        while cur is not None:
            yield cur.key
            cur = cur.next

    def counts(self) -> list[int]:
        """The access counts from front to back."""
        out, cur = [], self.head
        while cur is not None:
            out.append(cur.count)
            cur = cur.next
        return out

    def check_invariant(self) -> None:
        """Assert (I1), the distinct keys of (I2), and (I3) under the rule count."""
        seen, cur, steps = set(), self.head, 0
        while cur is not None:
            assert steps < self.n, "cycle or wrong size"
            assert cur.key not in seen, "duplicate key"
            seen.add(cur.key)
            steps += 1
            cur = cur.next
        assert steps == self.n
        if self.rule == "count":
            c = self.counts()
            assert all(c[j] >= c[j + 1] for j in range(len(c) - 1))
