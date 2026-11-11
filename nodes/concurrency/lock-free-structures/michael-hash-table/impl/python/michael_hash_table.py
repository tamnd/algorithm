# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/michael-hash-table/. The authors are listed in prov/Z81DZW.jsonl.

"""Michael's lock-free hash table (SPAA 2002) with hazard pointers.

The table has a fixed number m of buckets. Bucket i is the shared word
("bucket", i), which holds the marked pointer (first node, False) of a sorted
lock-free list: Michael's list. A node has the fields key and next; next is a
marked pointer (successor, mark). The hash of key k is k mod m.

FIND walks the list as in the paper. Each process p has three hazard pointers,
the words ("hp", p, 0), ("hp", p, 1) and ("hp", p, 2): hp0 protects next, hp1
protects cur and hp2 protects the node whose next field is prev. After it
writes a hazard pointer, FIND reads the word it came from again, to make sure
the node was still in the list when it was protected. A deleted node is
retired; when a process has R retired nodes, it scans all the hazard pointers
and frees the retired nodes that no hazard pointer holds.

With hazard=False the table writes no hazard pointers and frees a node as
soon as it unlinks it. That is the unsafe version: a slow process can then
read a freed node, and the memory can be reused under it.

Keys are read as steps, because a freed node can be reused with another key.
Each method is a generator that yields one shared memory step at a time (see
explorer.py). Use Handle(table, p) to get the operations of process p.
"""

from __future__ import annotations

from typing import Iterable

from explorer import NULL, Memory, Proc


class MichaelHashTable:
    def __init__(self, mem: Memory, m: int = 2, keys: Iterable[int] = (), nprocs: int = 2,
                 hazard: bool = True, R: int = 1) -> None:
        self.mem, self.m, self.nprocs, self.hazard, self.R = mem, m, nprocs, hazard, R
        self.retired: list[list[int]] = [[] for _ in range(nprocs)]
        for i in range(m):
            nxt = NULL
            for k in sorted((k for k in set(keys) if k % m == i), reverse=True):
                nxt = mem.new(key=k, next=(nxt, False))
            mem.init(("bucket", i), (nxt, False))
        for p in range(nprocs):
            for j in range(3):
                mem.init(("hp", p, j), NULL)

    def _protect(self, p: int, j: int, node: int) -> Proc:
        if self.hazard:
            yield ("write", ("hp", p, j), node)

    def find(self, p: int, k: int) -> Proc:
        """Return (found, prev, cur, next). prev is the word that points to cur."""
        while True:  # try_again
            prev = ("bucket", k % self.m)  # @line L1
            cur = (yield ("read", prev))[0]
            yield from self._protect(p, 1, cur)  # @line L2
            if (yield ("read", prev)) != (cur, False):  # @line L3
                continue
            while True:
                if cur == NULL:  # @line L4
                    return False, prev, cur, NULL
                nxt, cmark = yield ("read", (cur, "next"))  # @line L5
                yield from self._protect(p, 0, nxt)  # @line L6
                if (yield ("read", (cur, "next"))) != (nxt, cmark):  # @line L7
                    break
                ckey = yield ("read", (cur, "key"))  # @line L8
                if (yield ("read", prev)) != (cur, False):  # @line L9
                    break
                if not cmark:  # @line L10
                    if ckey >= k:  # @line L11
                        return ckey == k, prev, cur, nxt
                    prev = (cur, "next")  # @line L12
                    yield from self._protect(p, 2, cur)
                else:
                    if (yield ("cas", prev, (cur, False), (nxt, False))):  # @line L13
                        yield from self.retire(p, cur)
                    else:
                        break
                cur = nxt  # @line L14
                yield from self._protect(p, 1, nxt)

    def insert(self, p: int, k: int) -> Proc:
        node = None
        while True:
            found, prev, cur, _ = yield from self.find(p, k)  # @line L15
            if found:  # @line L16
                if node is not None:
                    yield ("free", node)  # never linked, so nobody else can see it
                return False
            if node is None:  # @line L17
                node = yield ("alloc", (("key", k), ("next", (cur, False))))
            else:
                yield ("write", (node, "next"), (cur, False))
            if (yield ("cas", prev, (cur, False), (node, False))):  # @line L18
                return True

    def delete(self, p: int, k: int) -> Proc:
        while True:
            found, prev, cur, nxt = yield from self.find(p, k)  # @line L19
            if not found:  # @line L20
                return False
            if not (yield ("cas", (cur, "next"), (nxt, False), (nxt, True))):  # @line L21
                continue
            if (yield ("cas", prev, (cur, False), (nxt, False))):  # @line L22
                yield from self.retire(p, cur)
            else:
                yield from self.find(p, k)
            return True  # @line L23

    def contains(self, p: int, k: int) -> Proc:
        found, _, _, _ = yield from self.find(p, k)  # @line L24
        return found

    def retire(self, p: int, node: int) -> Proc:
        if not self.hazard:
            yield ("free", node)  # unsafe: another process may still use it
            return
        self.retired[p].append(node)  # @line R1
        if len(self.retired[p]) >= self.R:  # @line R2
            yield from self.scan(p)

    def scan(self, p: int) -> Proc:
        hazards = set()
        for q in range(self.nprocs):  # @line R3
            for j in range(3):
                hazards.add((yield ("read", ("hp", q, j))))
        keep = []
        for node in self.retired[p]:  # @line R4
            if node in hazards:
                keep.append(node)
            else:
                yield ("free", node)  # @line R5
        self.retired[p] = keep

    # Not steps: for the tests, read the table when no process runs.
    def bucket_keys(self, i: int) -> list[int]:
        out, n = [], self.mem.peek(("bucket", i))[0]
        while n != NULL:
            if not self.mem.peek((n, "next"))[1]:
                out.append(self.mem.peek((n, "key")))
            n = self.mem.peek((n, "next"))[0]
        return out

    def keys(self) -> list[int]:
        return sorted(k for i in range(self.m) for k in self.bucket_keys(i))


class Handle:
    """The operations of process p on a shared table, for explorer.program."""

    def __init__(self, table: MichaelHashTable, p: int) -> None:
        self.t, self.p = table, p

    def insert(self, k: int) -> Proc:
        return self.t.insert(self.p, k)

    def delete(self, k: int) -> Proc:
        return self.t.delete(self.p, k)

    def contains(self, k: int) -> Proc:
        return self.t.contains(self.p, k)
