# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deferred-reference-counting/. The authors are listed in prov/0A4SH2.jsonl.

"""Deferred reference counting (Deutsch and Bobrow 1976) on a small heap model.

Objects have fixed lists of fields that hold object ids or None. The roots are
a separate list of variables. Only references from heap fields are counted.
An object whose count drops to zero goes into the zero count table (ZCT), and
COLLECT frees it only if no root points to it.
"""


class DRCHeap:
    def __init__(self, roots: int) -> None:
        self.roots: list[int | None] = [None] * roots
        self.fields: dict[int, list[int | None]] = {}
        self.rc: dict[int, int] = {}
        self.zct: set[int] = set()
        self.freed: set[int] = set()
        self.next_id = 1

    def new(self, n: int) -> int:
        x = self.next_id
        self.next_id += 1
        self.fields[x] = [None] * n  # @line L1
        self.rc[x] = 0
        self.zct.add(x)  # @line L2
        return x  # @line L3

    def write_root(self, i: int, y: int | None) -> None:
        self.roots[i] = y  # @line L4

    def write(self, p: int, i: int, y: int | None) -> None:
        if y is not None:  # @line L5
            self.rc[y] += 1
        z = self.fields[p][i]  # @line L6
        self.fields[p][i] = y
        if z is not None:  # @line L7
            self.dec(z)

    def dec(self, z: int) -> None:
        self.rc[z] -= 1  # @line L8
        if self.rc[z] == 0:  # @line L9
            self.zct.add(z)

    def collect(self) -> list[int]:
        """Free every object in the ZCT that no root and no field points to."""
        out: list[int] = []
        for r in self.roots:  # @line L10
            if r is not None:
                self.rc[r] += 1
        while self.zct:  # @line L11
            x = self.zct.pop()  # @line L12
            if self.rc[x] == 0:  # @line L13
                for c in self.fields[x]:  # @line L14
                    if c is not None:
                        self.dec(c)
                del self.fields[x]  # @line L15
                del self.rc[x]
                self.freed.add(x)
                out.append(x)
        for r in self.roots:  # @line L16
            if r is not None:
                self.dec(r)
        return out
