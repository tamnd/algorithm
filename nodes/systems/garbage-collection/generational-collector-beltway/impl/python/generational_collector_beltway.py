# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generational-collector-beltway/. The authors are listed in prov/WR1XXS.jsonl.

"""A model of the Beltway copying collector (Blackburn, Jones, McKinley and
Moss, 2002).

The heap is a list of belts. A belt is a FIFO queue of increments, and an
increment is a region that is collected on its own. `sizes[b]` is the most
objects an increment of belt b can hold. Objects have unit size and the heap
holds at most `usable` of them; the copy reserve is outside this limit.

Each increment has the key (belt, creation number). A collection always
takes the nonempty increment with the smallest key: the oldest increment of
the lowest belt that is not empty. Survivors go to the youngest increment of
the next belt, and survivors of the top belt go to the youngest increment of
the top belt itself (a new one if the youngest is the one being collected).
The write barrier remembers a pointer only if its target increment has a
smaller key than its source increment, so only pointers to increments that
will be collected first are remembered.

Configurations:
    sizes=[usable]                     BSS, a semi-space collector
    sizes=[usable, usable]             BA2, Appel's two generations
    sizes=[x, x]                       Beltway X.X (not complete if x < usable)
    sizes=[x, x, usable]               Beltway X.X.100 (complete)

An object is an integer id that does not change when it moves, as if every
slot were updated by the copy.
"""

from typing import Optional


class OutOfMemory(Exception):
    pass


class Beltway:
    def __init__(self, sizes: list[int], usable: int, nursery_trigger: bool = False) -> None:
        if not sizes or min(sizes) < 1 or max(sizes) > usable:
            raise ValueError("each increment holds between 1 and usable objects")
        self.sizes = sizes
        self.usable = usable
        self.nursery_trigger = nursery_trigger  # at most one nursery increment
        self.belts: list[list[int]] = [[] for _ in sizes]  # belt -> increments, oldest first
        self.belt_of: dict[int, int] = {}  # increment -> belt
        self.objects: dict[int, list[int]] = {}  # increment -> objects
        self.remset: dict[int, set[tuple[int, int]]] = {}  # increment -> slots (src, field)
        self.fields: dict[int, list[Optional[int]]] = {}
        self.inc_of: dict[int, int] = {}  # object -> increment
        self.roots: list[Optional[int]] = []
        self.next_obj = self.next_inc = 0
        self.collections = 0
        self.copied = 0

    # ---- the layout ----------------------------------------------------
    def key(self, inc: int) -> tuple[int, int]:
        return (self.belt_of[inc], inc)  # increments are numbered in creation order

    def used(self) -> int:
        return len(self.inc_of)

    def new_increment(self, b: int) -> int:
        k = self.next_inc
        self.next_inc += 1
        self.belt_of[k] = b
        self.objects[k] = []
        self.remset[k] = set()
        self.belts[b].append(k)
        return k

    def youngest(self, b: int, avoid: Optional[int] = None) -> int:
        """The youngest increment of belt b with room, other than `avoid`;
        a new increment at the end of the belt if there is none."""
        if self.belts[b]:
            k = self.belts[b][-1]
            if k != avoid and len(self.objects[k]) < self.sizes[b]:
                return k
        return self.new_increment(b)

    def place(self, x: int, k: int) -> None:
        old = self.inc_of.get(x)
        if old is not None:
            self.objects[old].remove(x)
        self.objects[k].append(x)
        self.inc_of[x] = k

    # ---- the mutator ---------------------------------------------------
    def alloc(self, nfields: int) -> int:
        """Allocate into the nursery; return the index of the new root."""
        steps = 0
        while self.used() >= self.usable or (
                self.nursery_trigger and self.belts[0]
                and len(self.objects[self.belts[0][-1]]) >= self.sizes[0]):  # @line L13
            if steps > 4 * self.usable + 10:
                raise OutOfMemory("no collection frees space")
            self.collect()
            steps += 1
        x = self.next_obj
        self.next_obj += 1
        self.fields[x] = [None] * nfields
        self.place(x, self.youngest(0))  # @line L14
        self.roots.append(x)
        return len(self.roots) - 1

    def record(self, s: int, i: int) -> None:
        """The write barrier: remember a slot whose target is collected first."""
        v = self.fields[s][i]
        if v is not None and self.inc_of[v] != self.inc_of[s] \
                and self.key(self.inc_of[v]) < self.key(self.inc_of[s]):  # @line L12
            self.remset[self.inc_of[v]].add((s, i))

    def write(self, src_root: int, i: int, ref_root: Optional[int]) -> None:
        s = self.roots[src_root]
        assert s is not None
        self.fields[s][i] = None if ref_root is None else self.roots[ref_root]  # @line L11
        self.record(s, i)

    def load(self, src_root: int, i: int, dst_root: int) -> None:
        s = self.roots[src_root]
        assert s is not None
        self.roots[dst_root] = self.fields[s][i]

    # ---- the collector -------------------------------------------------
    def collect(self) -> None:
        """Collect one increment: the oldest one of the lowest nonempty belt."""
        nonempty = [k for belt in self.belts for k in belt]
        if not nonempty:
            return
        self.collections += 1
        c = min(nonempty, key=self.key)  # @line L1
        b = self.belt_of[c]
        d = b + 1 if b + 1 < len(self.belts) else b  # @line L2
        copied: list[int] = []

        def evacuate(x: int) -> None:
            if self.inc_of[x] == c:  # @line L9
                self.place(x, self.youngest(d, avoid=c))  # @line L10
                copied.append(x)
                self.copied += 1

        slots = [(s, i) for (s, i) in sorted(self.remset[c])
                 if s in self.fields and self.fields[s][i] is not None
                 and self.inc_of[self.fields[s][i]] == c]
        for x in [r for r in self.roots if r is not None] + [self.fields[s][i] for s, i in slots]:  # @line L3
            if self.inc_of[x] == c:
                evacuate(x)
        k = 0
        while k < len(copied):  # @line L4
            o = copied[k]
            k += 1
            for i, v in enumerate(self.fields[o]):
                if v is not None and self.inc_of[v] == c:  # @line L5
                    evacuate(v)
                if v is not None:
                    self.record(o, i)  # @line L6
        for s, i in slots:  # @line L7
            if self.inc_of[s] != c:
                self.record(s, i)
        for x in self.objects[c]:  # @line L8
            del self.fields[x], self.inc_of[x]
        self.belts[b].remove(c)
        del self.objects[c], self.remset[c], self.belt_of[c]

    # ---- views used by the tests ---------------------------------------
    def reachable(self) -> set[int]:
        seen: set[int] = set()
        stack = [r for r in self.roots if r is not None]
        while stack:
            x = stack.pop()
            if x not in seen:
                seen.add(x)
                stack.extend(v for v in self.fields[x] if v is not None)
        return seen

    def remset_invariant(self) -> bool:
        for s, fs in self.fields.items():
            for i, v in enumerate(fs):
                if v is not None and self.inc_of[v] != self.inc_of[s] \
                        and self.key(self.inc_of[v]) < self.key(self.inc_of[s]):
                    if (s, i) not in self.remset[self.inc_of[v]]:
                        return False
        return True
