# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reference-counting/. The authors are listed in prov/3QGTQE.jsonl.

"""Reference counting on a small heap model.

The heap is a set of objects. Each object has a fixed list of fields, and each
field holds the id of an object or None. Object 0 is the root record: its
fields are the root variables of the mutator, and it is never freed. Every
reference, from a root or from a heap field, is counted.
"""

ROOT = 0


class RCHeap:
    def __init__(self, roots: int, lazy: bool = False) -> None:
        self.fields: dict[int, list[int | None]] = {ROOT: [None] * roots}
        self.rc: dict[int, int] = {ROOT: 0}
        self.freed: set[int] = set()
        self.lazy = lazy
        self.pending: list[int] = []  # dead objects whose fields are not yet released
        self.next_id = 1

    def new(self, n: int) -> int:
        """NEW: an object with n null fields and count 0. Store it at once."""
        if self.lazy and self.pending:
            self._free_one(self.pending.pop())  # bounded work per allocation
        x = self.next_id
        self.next_id += 1
        self.fields[x] = [None] * n  # @line L1
        self.rc[x] = 0  # @line L2
        return x  # @line L3

    def write(self, p: int, i: int, y: int | None) -> None:
        """WRITE: p[i] <- y, with the count updates."""
        if y is not None:  # @line L4
            self.rc[y] += 1
        z = self.fields[p][i]  # @line L5
        self.fields[p][i] = y  # @line L6
        if z is not None:  # @line L7
            self.release(z)

    def release(self, z: int) -> None:
        self.rc[z] -= 1  # @line L8
        if self.rc[z] != 0:  # @line L9
            return
        if self.lazy:
            self.pending.append(z)
            return
        stack = [z]  # @line L10
        while stack:  # @line L11
            x = stack.pop()  # @line L12
            for c in self.fields[x]:  # @line L13
                if c is not None:
                    self.rc[c] -= 1  # @line L14
                    if self.rc[c] == 0:  # @line L15
                        stack.append(c)
            self._free(x)  # @line L16

    def _free_one(self, x: int) -> None:
        for c in self.fields[x]:
            if c is not None:
                self.rc[c] -= 1
                if self.rc[c] == 0:
                    self.pending.append(c)
        self._free(x)

    def drain(self) -> None:
        """Lazy mode: finish all pending frees."""
        while self.pending:
            self._free_one(self.pending.pop())

    def _free(self, x: int) -> None:
        del self.fields[x]
        del self.rc[x]
        self.freed.add(x)

    def read(self, p: int, i: int) -> int | None:
        return self.fields[p][i]
