# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trial-deletion/. The authors are listed in prov/40TJAC.jsonl.

"""The synchronous cycle collector of Bacon and Rajan (2001), by trial deletion.

Plain reference counting on a heap of objects with fixed fields. Object 0 is
the root record; its fields are the roots, and it is never freed. A decrement
that leaves a count above zero makes the object a purple candidate. COLLECT
subtracts the counts due to references inside the subgraph below the
candidates (MarkGray), restores the counts of the part that something outside
still references (Scan, ScanBlack), and frees the rest (CollectWhite).
The recursive procedures of the paper are written here with explicit stacks.
"""

ROOT = 0
BLACK, GRAY, WHITE, PURPLE = "black", "gray", "white", "purple"


class CycleRCHeap:
    def __init__(self, roots: int) -> None:
        self.fields: dict[int, list[int | None]] = {ROOT: [None] * roots}
        self.rc: dict[int, int] = {ROOT: 1}
        self.color: dict[int, str] = {ROOT: BLACK}
        self.buffered: dict[int, bool] = {ROOT: False}
        self.candidates: list[int] = []
        self.freed: set[int] = set()
        self.next_id = 1

    def new(self, n: int) -> int:
        x = self.next_id
        self.next_id += 1
        self.fields[x] = [None] * n
        self.rc[x] = 0
        self.color[x] = BLACK
        self.buffered[x] = False
        return x

    def write(self, p: int, i: int, y: int | None) -> None:
        if y is not None:
            self.increment(y)
        z = self.fields[p][i]
        self.fields[p][i] = y
        if z is not None:
            self.decrement(z)

    def children(self, s: int) -> list[int]:
        return [t for t in self.fields[s] if t is not None]

    def increment(self, s: int) -> None:
        self.rc[s] += 1  # @line L1
        self.color[s] = BLACK

    def decrement(self, s: int) -> None:
        stack = [s]
        while stack:
            s = stack.pop()
            self.rc[s] -= 1  # @line L2
            if self.rc[s] == 0:  # @line L3
                stack.extend(self.children(s))  # Release, @line L4
                self.color[s] = BLACK  # @line L5
                if not self.buffered[s]:  # @line L6
                    self._free(s)
            else:
                self.possible_root(s)  # @line L7

    def possible_root(self, s: int) -> None:
        if self.color[s] != PURPLE:  # @line L8
            self.color[s] = PURPLE  # @line L9
            if not self.buffered[s]:  # @line L10
                self.buffered[s] = True
                self.candidates.append(s)

    def collect_cycles(self) -> set[int]:
        before = set(self.freed)
        self.mark_roots()
        for s in self.candidates:  # ScanRoots, @line L18
            self.scan(s)
        roots, self.candidates = self.candidates, []  # CollectRoots, @line L19
        for s in roots:
            self.buffered[s] = False  # @line L20
            self.collect_white(s)  # @line L21
        return self.freed - before

    def mark_roots(self) -> None:
        kept = []
        for s in self.candidates:  # @line L11
            if self.color[s] == PURPLE and self.rc[s] > 0:  # @line L12
                self.mark_gray(s)  # @line L13
                kept.append(s)
            else:
                self.buffered[s] = False  # @line L14
                if self.color[s] == BLACK and self.rc[s] == 0:  # @line L15
                    self._free(s)  # @line L16
        self.candidates = kept  # @line L17

    def mark_gray(self, s: int) -> None:
        if self.color[s] == GRAY:  # @line L22
            return
        self.color[s] = GRAY  # @line L23
        stack = [s]
        while stack:
            u = stack.pop()
            for t in self.children(u):  # @line L24
                self.rc[t] -= 1  # @line L25
                if self.color[t] != GRAY:  # MarkGray(T), @line L26
                    self.color[t] = GRAY
                    stack.append(t)

    def scan(self, s: int) -> None:
        stack = [s]
        while stack:
            u = stack.pop()
            if self.color[u] == GRAY:  # @line L27
                if self.rc[u] > 0:  # @line L28
                    self.scan_black(u)  # @line L29
                else:
                    self.color[u] = WHITE  # @line L30
                    stack.extend(self.children(u))  # @line L31

    def scan_black(self, s: int) -> None:
        self.color[s] = BLACK  # @line L32
        stack = [s]
        while stack:
            u = stack.pop()
            for t in self.children(u):  # @line L33
                self.rc[t] += 1  # @line L34
                if self.color[t] != BLACK:  # ScanBlack(T), @line L35
                    self.color[t] = BLACK
                    stack.append(t)

    def collect_white(self, s: int) -> None:
        stack = [s]
        while stack:
            u = stack.pop()
            if u in self.freed:
                continue
            if self.color[u] == WHITE and not self.buffered[u]:  # @line L36
                self.color[u] = BLACK  # @line L37
                stack.extend(self.children(u))  # @line L38
                self._free(u)  # @line L39

    def _free(self, x: int) -> None:
        self.freed.add(x)
        del self.fields[x], self.rc[x], self.color[x], self.buffered[x]
