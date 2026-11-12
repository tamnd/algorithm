# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/garbage-first-collector/. The authors are listed in prov/CWW6G2.jsonl.

"""Garbage-First (G1), after Detlefs, Flood, Heller and Printezis (2004).

This is a small model of the heap in Python, not a memory manager. The heap is
a row of regions of region_size words. An object is a record at an address,
with a size and a list of pointer fields. The model keeps the parts of G1 that
make it work:

* a post-write barrier that records each pointer from one region into another
  in the remembered set of the target region;
* concurrent marking with a snapshot-at-the-beginning (SATB) pre-write barrier
  and a top-at-mark-start (TAMS) per region, which counts the live words of
  each region;
* evacuation pauses that collect all young regions and, after a marking, the
  old regions with the most garbage per unit of predicted cost, while the
  predicted pause fits a budget. Live objects of the collection set are found
  from the roots and the remembered sets and copied to free regions.

Simplifications, stated plainly: a pause does not overlap a marking (a pause
first finishes the marking); every survivor is copied to an old region at once
(no survivor regions and no ages); there are no humongous objects. When the
marking ends, the model drops the records of objects that it proved dead,
which stands for G1 scanning only marked objects below TAMS.
"""

from __future__ import annotations

from collections import deque


class OutOfMemory(Exception):
    pass


class Obj:
    __slots__ = ("oid", "size", "fields", "forward")

    def __init__(self, oid: int, size: int, fields: list[int | None]) -> None:
        self.oid, self.size, self.fields = oid, size, fields
        self.forward: int | None = None


def greedy_collection_set(old: list[tuple[int, int, int]], budget: int) -> tuple[list[int], int]:
    """old holds (region, garbage, cost). Take regions in decreasing order of garbage per cost
    while the total cost fits the budget; stop at the first region that does not fit.
    Return the chosen regions and the total cost."""
    order = sorted(old, key=lambda t: (-t[1] / t[2], t[0]))
    chosen, t = [], 0
    for r, _, c in order:  # @line L6
        if t + c > budget:  # @line L7
            break
        chosen.append(r)  # @line L8
        t += c
    return chosen, t


class G1:
    def __init__(self, regions: int, region_size: int, registers: int, young_regions: int = 2,
                 budget: int = 60, fixed_cost: int = 4, rs_cost: int = 1, copy_cost: int = 1,
                 satb: bool = True) -> None:
        self.n, self.R = regions, region_size
        self.young_regions, self.budget = young_regions, budget
        self.fixed_cost, self.rs_cost, self.copy_cost = fixed_cost, rs_cost, copy_cost
        self.satb_barrier = satb
        self.kind = ["free"] * regions  # free, young or old
        self.top = [0] * regions
        self.rs: list[set[tuple[int, int]]] = [set() for _ in range(regions)]
        self.live: list[int | None] = [None] * regions  # live words found by the last marking
        self.objects: dict[int, Obj] = {}
        self.roots: list[int | None] = [None] * registers
        self.eden: int | None = None
        self.to: int | None = None
        self.marking = False
        self.marked: set[int] = set()
        self.stack: list[int] = []
        self.satb: list[int] = []
        self.tams = [0] * regions
        self.next_oid = 0
        self.pauses = 0
        self.markings = 0
        self.collection_sets: list[tuple[list[int], list[int]]] = []  # (young, old) of each pause

    def region(self, a: int) -> int:
        return a // self.R

    def take_free(self, kind: str) -> int | None:
        for r in range(self.n):
            if self.kind[r] == "free":
                self.kind[r], self.top[r], self.live[r] = kind, 0, None
                return r
        return None

    # ---- the mutator ----

    def new(self, reg: int, size: int, nfields: int) -> int:
        if not 0 < size <= self.R:
            raise ValueError("object size out of range")
        if self.eden is None or self.top[self.eden] + size > self.R:
            if self.kind.count("young") >= self.young_regions:
                self.pause()
            self.eden = self.take_free("young")
            if self.eden is None:
                self.pause()
                self.eden = self.take_free("young")
                if self.eden is None:
                    raise OutOfMemory
        a = self.eden * self.R + self.top[self.eden]
        self.top[self.eden] += size
        self.objects[a] = Obj(self.next_oid, size, [None] * nfields)
        self.next_oid += 1
        self.roots[reg] = a
        return a

    def load(self, dst: int, src: int, f: int) -> None:
        x = self.roots[src]
        if x is not None and f < len(self.objects[x].fields):
            self.roots[dst] = self.objects[x].fields[f]

    def store(self, dst: int, f: int, src: int) -> None:
        x, y = self.roots[dst], self.roots[src]
        if x is None or f >= len(self.objects[x].fields):
            return
        o = self.objects[x]
        if self.marking and self.satb_barrier and o.fields[f] is not None:  # @line L1
            self.satb.append(o.fields[f])
        o.fields[f] = y  # @line L2
        if y is not None and self.region(y) != self.region(x):  # @line L3
            self.rs[self.region(y)].add((x, f))

    def move(self, dst: int, src: int) -> None:
        self.roots[dst] = self.roots[src]

    # ---- concurrent marking ----

    def start_marking(self) -> None:
        self.marking, self.markings = True, self.markings + 1
        self.tams = list(self.top)  # objects above TAMS are allocated during marking and count as live
        self.marked = set()
        self.satb = []
        self.stack = [a for a in self.roots if a is not None]

    def below_tams(self, a: int) -> bool:
        r = self.region(a)
        return a < r * self.R + self.tams[r]

    def mark_step(self) -> bool:
        """One step of the marking thread; False when there is nothing left to do."""
        if self.satb:  # @line L4
            a = self.satb.pop()
        elif self.stack:
            a = self.stack.pop()
        else:
            return False
        if a not in self.marked and self.below_tams(a):
            self.marked.add(a)
            self.stack.extend(y for y in self.objects[a].fields if y is not None)
        return True

    def finish_marking(self) -> None:
        """Remark (drain the SATB queue and the stack) and cleanup (count live words, free empty regions)."""
        while self.mark_step():
            pass
        self.marking = False
        dead = [a for a in self.objects if self.below_tams(a) and a not in self.marked]
        for a in dead:
            del self.objects[a]
        for r in range(self.n):
            self.rs[r] = {(x, f) for (x, f) in self.rs[r] if x in self.objects}
        live = [0] * self.n
        for a, o in self.objects.items():
            live[self.region(a)] += o.size
        for r in range(self.n):
            if self.kind[r] == "old":
                self.live[r] = live[r]
                if live[r] == 0:
                    self.free_region(r)

    # ---- evacuation pauses ----

    def cost(self, r: int, live: int) -> int:
        return self.fixed_cost + self.rs_cost * len(self.rs[r]) + self.copy_cost * live

    def choose(self) -> set[int]:
        young = [r for r in range(self.n) if self.kind[r] == "young"]
        t = sum(self.cost(r, self.top[r]) for r in young)  # @line L5
        old = [(r, self.top[r] - self.live[r], self.cost(r, self.live[r])) for r in range(self.n)
               if self.kind[r] == "old" and self.live[r] is not None and self.top[r] > self.live[r]]
        chosen, _ = greedy_collection_set(old, max(0, self.budget - t))
        self.collection_sets.append((young, sorted(chosen)))
        return set(young) | set(chosen)

    def evacuate(self, a: int, queue: deque[int]) -> int:
        o = self.objects[a]
        if o.forward is not None:  # @line L15
            return o.forward
        if self.to is None or self.top[self.to] + o.size > self.R:  # @line L16
            self.to = self.take_free("old")
            if self.to is None:
                raise OutOfMemory("evacuation failure")
        b = self.to * self.R + self.top[self.to]
        self.top[self.to] += o.size
        self.objects[b] = Obj(o.oid, o.size, list(o.fields))
        o.forward = b
        queue.append(b)
        return b

    def free_region(self, r: int) -> None:
        lo, hi = r * self.R, (r + 1) * self.R
        for a in [a for a in self.objects if lo <= a < hi]:
            del self.objects[a]
        self.kind[r], self.top[r], self.live[r] = "free", 0, None
        self.rs[r] = set()
        for s in self.rs:
            s -= {(x, f) for (x, f) in s if lo <= x < hi}

    def pause(self) -> None:
        if self.marking:
            self.finish_marking()
        self.pauses += 1
        cs = self.choose()
        self.eden, self.to = None, None
        queue: deque[int] = deque()
        for i, a in enumerate(self.roots):  # @line L9
            if a is not None and self.region(a) in cs:
                self.roots[i] = self.evacuate(a, queue)
        for c in sorted(cs):  # @line L10
            for x, f in sorted(self.rs[c]):
                if self.region(x) in cs or x not in self.objects or f >= len(self.objects[x].fields):
                    continue
                y = self.objects[x].fields[f]
                if y is not None and self.region(y) == c:  # @line L11
                    z = self.evacuate(y, queue)
                    self.objects[x].fields[f] = z
                    if self.region(z) != self.region(x):
                        self.rs[self.region(z)].add((x, f))
        while queue:  # @line L12
            x = queue.popleft()
            o = self.objects[x]
            for f, y in enumerate(o.fields):  # @line L13
                if y is None:
                    continue
                if self.region(y) in cs:
                    y = o.fields[f] = self.evacuate(y, queue)
                if self.region(y) != self.region(x):
                    self.rs[self.region(y)].add((x, f))
        for c in cs:  # @line L14
            self.free_region(c)

    # ---- views for the tests ----

    def logical_graph(self) -> tuple:
        def oid(a: int | None) -> int | None:
            return None if a is None else self.objects[a].oid
        seen: dict[int, tuple] = {}
        stack = [a for a in self.roots if a is not None]
        while stack:
            a = stack.pop()
            o = self.objects[a]
            if o.oid in seen:
                continue
            seen[o.oid] = (o.size, tuple(oid(y) for y in o.fields))
            stack.extend(y for y in o.fields if y is not None)
        return tuple(oid(a) for a in self.roots), tuple(sorted(seen.items()))
