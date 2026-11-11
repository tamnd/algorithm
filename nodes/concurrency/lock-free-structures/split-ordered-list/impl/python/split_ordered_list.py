# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-ordered-list/. The authors are listed in prov/XCTCZ1.jsonl.

"""The split-ordered list of Shalev and Shavit (PODC 2003, JACM 2006).

All keys live in one lock-free sorted list (Michael's list, with the mark bit
in the next word). The list is sorted by the split-order key: the bits of the
hash in reverse order. A regular key k (here the hash of k is k itself, with
0 <= k < 2**(W-1)) has the split-order key reverse(k | MSB), which is odd. The
dummy node of bucket b has the split-order key reverse(b), which is even.

The shared words are "size" (the number of buckets, a power of two),
"count" (the number of keys), and ("T", b) for b < MAXB: a pointer to the
dummy node of bucket b, or NULL while bucket b is not initialized. Bucket 0
is initialized at the start. A bucket is initialized on first use: its
parent bucket (b with its top bit cleared) is initialized first, then a dummy
node is inserted into the list from the parent's dummy, and ("T", b) is set.
When count > LOAD * size, a process doubles size with one CAS. No key ever
moves.

The bucket array is a flat array of MAXB words; the paper also gives a
two-level segment table so that the array can grow too.

With publish_early=True a bucket is published in T before its dummy is in
the list. That is a bug: a key inserted after the new dummy is lost when the
dummy's next field is set as it is linked.

Nodes are never freed (the model has a garbage collector), so the code reads
keys with Memory.peek. Each method is a generator that yields one shared
memory step at a time (see explorer.py).
"""

from __future__ import annotations

from typing import Iterable

from explorer import NULL, Memory, Proc

W = 8
MSB = 1 << (W - 1)


def reverse(x: int) -> int:
    return int(format(x, f"0{W}b")[::-1], 2)


def so_regular(k: int) -> int:
    return reverse(k | MSB)


def so_dummy(b: int) -> int:
    return reverse(b)


def parent(b: int) -> int:
    """b with its most significant set bit cleared."""
    return b & ~(1 << (b.bit_length() - 1))


class SplitOrderedList:
    def __init__(self, mem: Memory, keys: Iterable[int] = (), size: int = 2, load: int = 1,
                 maxb: int = 64, publish_early: bool = False) -> None:
        self.mem, self.load, self.maxb, self.early = mem, load, maxb, publish_early
        d0 = mem.new(key=so_dummy(0), next=(NULL, False))
        mem.init(("T", 0), d0)
        for b in range(1, maxb):
            mem.init(("T", b), NULL)
        mem.init("size", size)
        mem.init("count", 0)
        for k in keys:  # build the start state sequentially (not steps)
            self._now(self.insert(k))

    def _now(self, g: Proc) -> object:
        """Run a generator to its end with no other process (setup only)."""
        try:
            v = None
            while True:
                v = self.mem.apply(g.send(v))
        except StopIteration as e:
            return e.value

    def key(self, node: int) -> int:
        return self.mem.peek((node, "key"))

    # Michael's list, started at a dummy node (dummy nodes are never deleted).
    def list_find(self, start: int, so: int) -> Proc:
        while True:
            prev = (start, "next")
            cur = (yield ("read", prev))[0]
            while True:
                if cur == NULL:
                    return False, prev, cur, NULL
                nxt, m = yield ("read", (cur, "next"))
                if m:
                    if not (yield ("cas", prev, (cur, False), (nxt, False))):
                        break
                    cur = nxt
                    continue
                ck = self.key(cur)
                if ck >= so:
                    return ck == so, prev, cur, nxt
                prev, cur = (cur, "next"), nxt

    def list_insert(self, start: int, node: int) -> Proc:
        """Link node; if a node with its key is there, return (False, that node)."""
        so = self.key(node)
        while True:
            found, prev, cur, _ = yield from self.list_find(start, so)
            if found:
                return False, cur
            yield ("write", (node, "next"), (cur, False))
            if (yield ("cas", prev, (cur, False), (node, False))):
                return True, node

    def list_delete(self, start: int, so: int) -> Proc:
        while True:
            found, prev, cur, nxt = yield from self.list_find(start, so)
            if not found:
                return False
            if not (yield ("cas", (cur, "next"), (nxt, False), (nxt, True))):
                continue
            if not (yield ("cas", prev, (cur, False), (nxt, False))):
                yield from self.list_find(start, so)
            return True

    def bucket(self, b: int) -> Proc:
        """Return the dummy node of bucket b, and initialize the bucket first if needed."""
        d = yield ("read", ("T", b))
        if d == NULL:
            yield from self.initialize_bucket(b)
            d = yield ("read", ("T", b))
        return d

    def initialize_bucket(self, b: int) -> Proc:
        par = parent(b)  # @line L15
        pd = yield from self.bucket(par)  # @line L16
        dummy = yield ("alloc", (("key", so_dummy(b)), ("next", (NULL, False))))  # @line L17
        if self.early:
            if not (yield ("cas", ("T", b), NULL, dummy)):
                return
            yield from self.list_insert(pd, dummy)
            return
        _, dummy = yield from self.list_insert(pd, dummy)  # @line L18
        yield ("cas", ("T", b), NULL, dummy)  # @line L19

    def insert(self, k: int) -> Proc:
        node = yield ("alloc", (("key", so_regular(k)), ("next", (NULL, False))))  # @line L1
        size = yield ("read", "size")
        b = k % size  # @line L2
        d = yield from self.bucket(b)  # @line L3
        ok, _ = yield from self.list_insert(d, node)  # @line L4
        if not ok:
            return False
        csize = yield ("read", "size")  # @line L5
        if (yield ("faa", "count", 1)) + 1 > self.load * csize and 2 * csize <= self.maxb:  # @line L6
            yield ("cas", "size", csize, 2 * csize)
        return True  # @line L7

    def contains(self, k: int) -> Proc:
        size = yield ("read", "size")
        b = k % size  # @line L8
        d = yield from self.bucket(b)  # @line L9
        found, _, _, _ = yield from self.list_find(d, so_regular(k))  # @line L10
        return found

    def delete(self, k: int) -> Proc:
        size = yield ("read", "size")
        b = k % size  # @line L11
        d = yield from self.bucket(b)  # @line L12
        if not (yield from self.list_delete(d, so_regular(k))):  # @line L13
            return False
        yield ("faa", "count", -1)  # @line L14
        return True

    # Not steps: for the tests, read the structure when no process runs.
    def nodes(self) -> list[tuple[int, bool]]:
        """The reachable nodes as (split-order key, is_dummy), marked nodes left out."""
        out, n = [], self.mem.peek(("T", 0))
        while n != NULL:
            nxt, m = self.mem.peek((n, "next"))
            if not m:
                out.append((self.key(n), self.key(n) % 2 == 0))
            n = nxt
        return out

    def keys(self) -> list[int]:
        return sorted(reverse(s) & ~MSB for s, dummy in self.nodes() if not dummy)

    def dummies(self) -> dict[int, int]:
        """Bucket -> dummy node, for the initialized buckets."""
        return {b: self.mem.peek(("T", b)) for b in range(self.maxb) if self.mem.peek(("T", b)) != NULL}
