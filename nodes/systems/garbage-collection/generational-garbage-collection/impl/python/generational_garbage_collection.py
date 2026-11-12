# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generational-garbage-collection/. The authors are listed in prov/JNBZA2.jsonl.

"""A two-generation collector on a small heap model.

The heap holds objects with a fixed number of pointer fields. The young
generation (the nursery plus the survivor objects) is collected by copying,
with the roots and the remembered set of old-to-young slots as the roots of
the collection. An object is promoted to the old generation when it has
survived `tenure_age` minor collections. The old generation is collected by a
full mark-sweep of both generations. Addresses change when an object is
copied; each object also keeps a fixed `oid`, which only the tests read.

The mutator works only through its root slots: alloc, write, load and drop.
"""

from collections import deque
from typing import Optional

Addr = int


class Obj:
    __slots__ = ("oid", "fields", "age")

    def __init__(self, oid: int, nfields: int) -> None:
        self.oid = oid
        self.fields: list[Optional[Addr]] = [None] * nfields
        self.age = 0


class GenHeap:
    """Nursery of `nursery_size` objects, old generation of `old_size` objects."""

    def __init__(self, nursery_size: int, old_size: int, tenure_age: int = 1) -> None:
        if nursery_size < 1 or tenure_age < 1:
            raise ValueError("nursery_size and tenure_age must be at least 1")
        self.nursery_size = nursery_size
        self.old_size = old_size
        self.tenure_age = tenure_age
        self.young: dict[Addr, Obj] = {}
        self.old: dict[Addr, Obj] = {}
        self.remset: set[tuple[Addr, int]] = set()
        self.roots: list[Optional[Addr]] = []
        self._next_addr = 1
        self._next_oid = 0
        self.minor_count = 0
        self.major_count = 0
        self.promoted = 0
        self.copied = 0

    # ------------------------------------------------------------ helpers
    def obj(self, a: Addr) -> Obj:
        return self.young[a] if a in self.young else self.old[a]

    def _new_addr(self) -> Addr:
        self._next_addr += 1
        return self._next_addr

    # ------------------------------------------------------------ mutator
    def alloc(self, nfields: int) -> int:
        """Allocate an object, put it in a new root slot and return the slot index."""
        if len(self.young) >= self.nursery_size:  # @line L1
            self.minor_collect()
        a = self._new_addr()  # @line L2
        self.young[a] = Obj(self._next_oid, nfields)
        self._next_oid += 1
        self.roots.append(a)
        return len(self.roots) - 1  # @line L3

    def write(self, src_root: int, i: int, ref_root: Optional[int]) -> None:
        """roots[src_root].fields[i] <- roots[ref_root] (or None), with the barrier."""
        src = self.roots[src_root]
        ref = None if ref_root is None else self.roots[ref_root]
        if src is None:
            raise ValueError("write through an empty root")
        self.obj(src).fields[i] = ref  # @line L4
        if src in self.old and ref is not None and ref in self.young:  # @line L5
            self.remset.add((src, i))

    def load(self, src_root: int, i: int, dst_root: int) -> None:
        """roots[dst_root] <- roots[src_root].fields[i]."""
        src = self.roots[src_root]
        if src is None:
            raise ValueError("load through an empty root")
        self.roots[dst_root] = self.obj(src).fields[i]

    def drop(self, root: int) -> None:
        self.roots[root] = None

    # ------------------------------------------------------------ minor
    def minor_collect(self) -> None:
        """Copy the live young objects; promote those that reach tenure_age."""
        self.minor_count += 1
        from_space = self.young
        self.young = {}
        forward: dict[Addr, Addr] = {}
        queue: deque[Addr] = deque()  # @line L6

        def evacuate(y: Addr) -> Addr:
            if y in forward:  # @line L16
                return forward[y]
            o = from_space[y]
            o.age += 1  # @line L17
            new = self._new_addr()
            if o.age >= self.tenure_age:  # @line L18
                self.old[new] = o
                self.promoted += 1
            else:  # @line L19
                self.young[new] = o
            self.copied += 1
            forward[y] = new  # @line L20
            queue.append(new)
            return new

        for k, r in enumerate(self.roots):  # @line L7
            if r is not None and r in from_space:  # @line L8
                self.roots[k] = evacuate(r)
        for (o, i) in list(self.remset):
            target = self.old[o].fields[i]
            if target is not None and target in from_space:
                self.old[o].fields[i] = evacuate(target)
        while queue:  # @line L9
            a = queue.popleft()  # @line L10
            o = self.obj(a)
            for i, t in enumerate(o.fields):  # @line L11
                if t is not None and t in from_space:
                    o.fields[i] = evacuate(t)  # @line L12
                t = o.fields[i]
                if a in self.old and t is not None and t in self.young:  # @line L13
                    self.remset.add((a, i))
        # The from-space is dropped as a whole; keep only the slots that still
        # point to a young object.
        self.remset = {(o, i) for (o, i) in self.remset  # @line L14
                       if self.old[o].fields[i] is not None and self.old[o].fields[i] in self.young}
        if len(self.young) >= self.nursery_size:
            self._promote_all_young()
        if len(self.old) > self.old_size:  # @line L15
            self.major_collect()

    def _promote_all_young(self) -> None:
        """Survivor-space overflow: move every young object to the old generation."""
        for a, o in self.young.items():
            self.old[a] = o
            self.promoted += 1
        self.young = {}
        self.remset = set()

    # ------------------------------------------------------------ major
    def major_collect(self) -> None:
        """Mark-sweep of both generations, then rebuild the remembered set."""
        self.major_count += 1
        marked: set[Addr] = set()
        stack = [r for r in self.roots if r is not None]
        while stack:
            a = stack.pop()
            if a in marked:
                continue
            marked.add(a)
            stack.extend(t for t in self.obj(a).fields if t is not None)
        self.young = {a: o for a, o in self.young.items() if a in marked}
        self.old = {a: o for a, o in self.old.items() if a in marked}
        self.remset = {(a, i) for a, o in self.old.items()
                       for i, t in enumerate(o.fields) if t is not None and t in self.young}

    # ------------------------------------------------------------ checks
    def all_objects(self) -> dict[Addr, Obj]:
        d = dict(self.old)
        d.update(self.young)
        return d

    def old_to_young_slots(self) -> set[tuple[Addr, int]]:
        return {(a, i) for a, o in self.old.items()
                for i, t in enumerate(o.fields) if t is not None and t in self.young}
