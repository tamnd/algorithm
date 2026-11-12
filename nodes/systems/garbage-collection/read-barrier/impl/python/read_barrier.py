# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/read-barrier/. The authors are listed in prov/CVZ3Q6.jsonl.

"""Two read barriers for a copying collector that runs in steps between
mutator operations.

BakerHeap: the to-space invariant. When the mutator loads a pointer into
from-space, the barrier copies the target (or follows its forwarding
address) and heals the slot, so that the mutator only ever holds to-space
pointers.

BrooksHeap: an indirection word. Every object has a field fwd that points to
the object itself or to its copy. Every load and store by the mutator goes
through fwd, so the mutator always uses the current copy, even when it holds
a pointer to the old one. The collector marks, copies a collection set in
steps, then updates the references and frees the old copies.
"""

import random
from typing import Optional


class Obj:
    __slots__ = ("oid", "fields", "space", "fwd")

    def __init__(self, oid: int, fields: list, space: str) -> None:
        self.oid = oid
        self.fields: list[Optional["Obj"]] = fields
        self.space = space  # "from", "to" or "freed" (Baker); "heap" or "freed" (Brooks)
        self.fwd: "Obj" = self


class BakerHeap:
    def __init__(self) -> None:
        self.roots: list[Optional[Obj]] = []
        self.objects: list[Obj] = []
        self.collecting = False
        self.queue: list[Obj] = []
        self.next_oid = 0

    def alloc(self, nfields: int) -> int:
        o = Obj(self.next_oid, [None] * nfields, "to")
        self.next_oid += 1
        self.objects.append(o)
        self.roots.append(o)
        return len(self.roots) - 1

    def evacuate(self, o: Obj) -> Obj:
        if o.space == "to":
            return o
        if o.fwd is not o:
            return o.fwd
        c = Obj(o.oid, list(o.fields), "to")
        o.fwd = c
        self.objects.append(c)
        self.queue.append(c)
        return c

    def read(self, o: Obj, i: int) -> Optional[Obj]:
        """The Baker read barrier."""
        v = o.fields[i]  # @line L1
        if self.collecting and v is not None and v.space == "from":  # @line L2
            v = self.evacuate(v)  # @line L3
            o.fields[i] = v  # @line L4
        return v  # @line L5

    def load(self, src: int, i: int, dst: int) -> None:
        o = self.roots[src]
        assert o is not None
        self.roots[dst] = self.read(o, i)

    def write(self, src: int, i: int, ref: Optional[int]) -> None:
        o = self.roots[src]
        assert o is not None
        o.fields[i] = None if ref is None else self.roots[ref]

    def flip(self) -> None:
        """Start a collection: all objects become from-space, the roots are evacuated."""
        for o in self.objects:
            o.space = "from"
        self.from_space, self.objects = self.objects, []
        self.collecting = True
        self.roots = [None if r is None else self.evacuate(r) for r in self.roots]

    def step(self) -> None:
        """Scan one gray object; when none is left, free from-space."""
        if not self.collecting:
            return
        if self.queue:
            c = self.queue.pop()
            c.fields = [None if t is None else self.evacuate(t) for t in c.fields]
        else:
            for o in self.from_space:
                o.space = "freed"
            self.from_space = []
            self.collecting = False


class BrooksHeap:
    def __init__(self) -> None:
        self.roots: list[Optional[Obj]] = []
        self.objects: list[Obj] = []
        self.next_oid = 0
        self.cset: list[Obj] = []
        self.evacuating = False

    def alloc(self, nfields: int) -> int:
        o = Obj(self.next_oid, [None] * nfields, "heap")
        self.next_oid += 1
        self.objects.append(o)
        self.roots.append(o)
        return len(self.roots) - 1

    @staticmethod
    def read(o: Obj, i: int) -> Optional[Obj]:
        return o.fwd.fields[i]  # @line L6

    @staticmethod
    def write_field(o: Obj, i: int, v: Optional[Obj]) -> None:
        o.fwd.fields[i] = v  # @line L7

    def load(self, src: int, i: int, dst: int) -> None:
        o = self.roots[src]
        assert o is not None
        self.roots[dst] = self.read(o, i)

    def write(self, src: int, i: int, ref: Optional[int]) -> None:
        o = self.roots[src]
        assert o is not None
        self.write_field(o, i, None if ref is None else self.roots[ref])

    def same(self, a: Optional[Obj], b: Optional[Obj]) -> bool:
        """Pointer equality must also go through the indirection."""
        return (a.fwd if a else None) is (b.fwd if b else None)

    def start(self, rng: random.Random, fraction: float = 0.6) -> None:
        """Mark the live objects and pick a collection set among them."""
        live: set[int] = set()
        stack = [r.fwd for r in self.roots if r is not None]
        while stack:
            o = stack.pop()
            if id(o) in live:
                continue
            live.add(id(o))
            stack.extend(t.fwd for t in o.fields if t is not None)
        dead = [o for o in self.objects if id(o) not in live]
        for o in dead:
            o.space = "freed"
        self.objects = [o for o in self.objects if id(o) in live]
        self.cset = [o for o in self.objects if rng.random() < fraction]
        self.evacuating = True

    def copy_step(self) -> None:
        """Copy one object of the collection set."""
        if not self.cset:
            return
        o = self.cset.pop()
        c = Obj(o.oid, list(o.fwd.fields), "heap")  # @line L8
        o.fwd = c
        self.objects.append(c)

    def update_refs(self) -> None:
        """Make every pointer point to the current copy, then free the old copies."""
        while self.cset:
            self.copy_step()
        for o in self.objects:
            if o.fwd is o:
                o.fields = [None if t is None else t.fwd for t in o.fields]
        self.roots = [None if r is None else r.fwd for r in self.roots]
        for o in self.objects:
            if o.fwd is not o:
                o.space = "freed"
        self.objects = [o for o in self.objects if o.fwd is o]
        self.evacuating = False
