# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/train-algorithm/. The authors are listed in prov/GG2PBV.jsonl.

"""The train algorithm (Hudson and Moss, 1992) for a mature object space.

The space is a sequence of trains, each a sequence of cars of at most
`car_size` objects. Cars are ordered by (train number, car number), and each
collection processes only the lowest car. Each car has a remembered set of
the slots, in cars that come later in the order, that point into it.

An object is named by an integer id that does not change when it moves; its
location is the car that holds it. So "moving" an object changes its car,
and the pointers to it stay valid, as if each slot were updated.

A collection either frees the whole lowest train, if nothing outside that
train refers into it, or collects its lowest car: objects referenced from
the roots go to a later train, objects referenced from another train go to
the end of that train, objects referenced from the same train go to the end
of the same train, and the objects they reach in the car follow them. What
is left in the car is garbage.

With `fix_futile=True`, a collection that frees nothing and moves nothing out
of the lowest train keeps one outside reference into that train as an extra
root, until a collection makes progress. This is the repair of Seligmann and
Grarup for a mutator that keeps moving its references so that the lowest
train never empties.
"""

from typing import Optional


class TrainHeap:
    def __init__(self, car_size: int = 3, fix_futile: bool = True) -> None:
        if car_size < 1:
            raise ValueError("a car holds at least one object")
        self.car_size = car_size
        self.fix_futile = fix_futile
        self.fields: dict[int, list[Optional[int]]] = {}
        self.car_of: dict[int, int] = {}  # object -> car
        self.objects: dict[int, list[int]] = {}  # car -> its objects
        self.train_of: dict[int, int] = {}  # car -> train
        self.trains: dict[int, list[int]] = {}  # train -> its cars, in order
        self.remset: dict[int, set[tuple[int, int]]] = {}  # car -> slots (src, field)
        self.roots: list[Optional[int]] = []
        self.extra_roots: dict[int, Optional[int]] = {}  # object -> train to move it to
        self.next_obj = self.next_car = self.next_train = 0
        self.collections = self.futile = 0
        self.freed: set[int] = set()

    # ---- the layout ----------------------------------------------------
    def key(self, car: int) -> tuple[int, int]:
        return (self.train_of[car], car)  # cars are numbered in creation order

    def lowest_train(self) -> Optional[int]:
        return min(self.trains) if self.trains else None

    def new_train(self) -> int:
        t = self.next_train
        self.next_train += 1
        self.trains[t] = []
        return t

    def new_car(self, t: int) -> int:
        c = self.next_car
        self.next_car += 1
        self.train_of[c] = t
        self.trains[t].append(c)
        self.objects[c] = []
        self.remset[c] = set()
        return c

    def place(self, x: int, t: int) -> None:
        """Append x to the last car of train t, or to a new car at its end."""
        cars = self.trains[t]
        c = cars[-1] if cars and len(self.objects[cars[-1]]) < self.car_size else self.new_car(t)
        old = self.car_of.get(x)
        if old is not None:
            self.objects[old].remove(x)
        self.objects[c].append(x)
        self.car_of[x] = c

    def later_train(self) -> int:
        """The last train, or a new one if the last train is the lowest."""
        last = max(self.trains) if self.trains else None
        if last is None or last == self.lowest_train():
            return self.new_train()
        return last

    # ---- the mutator ---------------------------------------------------
    def alloc(self, nfields: int) -> int:
        """Promote a new object into the mature space; return its root index."""
        x = self.next_obj
        self.next_obj += 1
        self.fields[x] = [None] * nfields
        self.place(x, self.later_train())  # never into the lowest train
        self.roots.append(x)
        return len(self.roots) - 1

    def record(self, s: int, i: int) -> None:
        """The write barrier: remember a slot that points to an earlier car."""
        v = self.fields[s][i]
        if v is not None and self.key(self.car_of[v]) < self.key(self.car_of[s]):  # @line L16
            self.remset[self.car_of[v]].add((s, i))

    def write(self, src_root: int, i: int, ref_root: Optional[int]) -> None:
        s = self.roots[src_root]
        assert s is not None
        self.fields[s][i] = None if ref_root is None else self.roots[ref_root]  # @line L15
        self.record(s, i)

    def load(self, src_root: int, i: int, dst_root: int) -> None:
        s = self.roots[src_root]
        assert s is not None
        self.roots[dst_root] = self.fields[s][i]

    # ---- the collector -------------------------------------------------
    def entries(self, car: int) -> list[tuple[int, int]]:
        """The remembered slots of a car that still point into it."""
        return [(s, i) for (s, i) in self.remset[car]
                if s in self.fields and self.fields[s][i] is not None and self.car_of[self.fields[s][i]] == car]

    def outside_refs(self, t: int) -> list[tuple[int, Optional[int]]]:
        """The references into train t from outside it, as pairs (target, u):
        u is the train of the referring slot, or None for a root."""
        out: list[tuple[int, Optional[int]]] = []
        out += [(r, None) for r in self.roots if r is not None and self.train_of[self.car_of[r]] == t]
        out += [(x, u) for x, u in sorted(self.extra_roots.items(), key=lambda p: p[0])
                if self.train_of[self.car_of[x]] == t]
        for c in self.trains[t]:
            for (s, i) in sorted(self.entries(c)):
                u = self.train_of[self.car_of[s]]
                if u != t:
                    out.append((self.fields[s][i], u))
        return out

    def free_car(self, c: int) -> int:
        t = self.train_of[c]
        for x in self.objects[c]:
            del self.fields[x]
            del self.car_of[x]
            self.freed.add(x)
        n = len(self.objects[c])
        self.trains[t].remove(c)
        del self.objects[c], self.remset[c], self.train_of[c]
        if not self.trains[t]:
            del self.trains[t]
        return n

    def collect(self) -> None:
        """One step of the train algorithm."""
        if not self.trains:
            return
        self.collections += 1
        t = self.lowest_train()  # @line L1
        c = self.trains[t][0]
        before = sum(len(self.objects[k]) for k in self.trains[t])
        if not self.outside_refs(t):  # @line L2
            for k in list(self.trains[t]):  # @line L3
                self.free_car(k)
            self.extra_roots.clear()
            return
        moved: list[int] = []

        def move(x: int, u: int) -> None:
            if self.car_of[x] == c:  # @line L13
                self.place(x, u)  # @line L14
                moved.append(x)

        later: Optional[int] = None
        pinned = sorted(self.extra_roots.items(), key=lambda p: p[0])
        for r, u in [(r, None) for r in self.roots if r is not None] + pinned:  # @line L4
            if self.car_of[r] == c:
                if u is None:
                    later = self.later_train() if later is None else later
                move(r, later if u is None else u)
        slots = self.entries(c)
        for (s, i) in sorted(slots):  # @line L5
            u = self.train_of[self.car_of[s]]
            if u != t:
                move(self.fields[s][i], u)
        for (s, i) in sorted(slots):  # @line L6
            if self.train_of[self.car_of[s]] == t and self.car_of[s] != c:
                move(self.fields[s][i], t)
        for (s, i) in slots:
            if s in self.fields and self.car_of[s] != c:
                self.record(s, i)
        k = 0
        while k < len(moved):  # @line L7
            o = moved[k]
            k += 1
            for i, v in enumerate(self.fields[o]):
                if v is not None and self.car_of[v] == c:  # @line L8
                    move(v, self.train_of[self.car_of[o]])
                if v is not None:
                    self.record(o, i)  # @line L9
        freed = self.free_car(c)  # @line L10
        after = sum(len(self.objects[q]) for q in self.trains.get(t, []))
        if freed == 0 and after == before:  # @line L11
            self.futile += 1
            if self.fix_futile and t in self.trains:
                refs = [p for p in self.outside_refs(t) if p[0] not in self.extra_roots]
                if refs:
                    x, u = refs[0]
                    self.extra_roots[x] = u  # moved later to train u, or to a later train
        else:
            self.extra_roots.clear()  # @line L12

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
                if v is not None and self.key(self.car_of[v]) < self.key(self.car_of[s]):
                    if (s, i) not in self.remset[self.car_of[v]]:
                        return False
        return True
