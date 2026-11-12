# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tricolor-marking/. The authors are listed in prov/SZ1DX2.jsonl.

"""Tricolor marking with an interleaved mutator, in the model of Dijkstra et al. 1978.

Heap model: objects 0 to n - 1, each with k pointer fields (an object or
None), and a fixed set of root objects. The marker and the mutator take
turns in an order that the caller chooses:

- a marker step takes one gray object, shades each of its children (a
  white child becomes gray), and makes the object black;
- a mutator step writes x.f <- y, where x and y (or None) are reachable
  from the roots at that moment.

The barrier runs inside the write: "none" does nothing, "dijkstra" shades
the new target y (incremental update), "yuasa" shades the old value of x.f
(snapshot at the beginning, a deletion barrier).

Each step costs O(k) plus the barrier, O(1). The invariant checks cost
O(n k) each.
"""

from __future__ import annotations

WHITE, GRAY, BLACK = "white", "gray", "black"


class TricolorHeap:
    """A heap that a tricolor marker traces while a mutator writes to it."""

    def __init__(self, fields: list[list[int | None]], roots: list[int], barrier: str = "none") -> None:
        if barrier not in ("none", "dijkstra", "yuasa"):
            raise ValueError("unknown barrier")
        self.fields = [list(f) for f in fields]
        self.roots = list(roots)
        self.barrier = barrier
        self.color = [WHITE] * len(fields)
        for r in self.roots:
            self.shade(r)

    def shade(self, x: int | None) -> None:
        """Make a white object gray. Gray and black objects do not change."""
        if x is not None and self.color[x] == WHITE:
            self.color[x] = GRAY

    def grays(self) -> list[int]:
        return [x for x, c in enumerate(self.color) if c == GRAY]

    def marker_step(self, x: int) -> None:
        """Scan the gray object x: shade its children, then make it black."""
        if self.color[x] != GRAY:
            raise ValueError("the marker scans only gray objects")
        for y in self.fields[x]:
            self.shade(y)
        self.color[x] = BLACK

    def write(self, x: int, f: int, y: int | None) -> None:
        """The mutator stores y in field f of x, through the barrier."""
        if self.barrier == "dijkstra":
            self.shade(y)
        elif self.barrier == "yuasa":
            self.shade(self.fields[x][f])
        self.fields[x][f] = y

    def reachable(self) -> set[int]:
        seen = set(self.roots)
        stack = list(seen)
        while stack:
            for y in self.fields[stack.pop()]:
                if y is not None and y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen

    def strong_invariant(self) -> bool:
        """No black object has a field that points to a white object."""
        return all(
            self.color[y] != WHITE
            for x, c in enumerate(self.color) if c == BLACK
            for y in self.fields[x] if y is not None
        )

    def weak_invariant(self) -> bool:
        """Every white object that a black object points to is reachable from a gray object through white objects."""
        protected = set()
        stack = []
        for g in self.grays():
            for y in self.fields[g]:
                if y is not None and self.color[y] == WHITE and y not in protected:
                    protected.add(y)
                    stack.append(y)
        while stack:
            for y in self.fields[stack.pop()]:
                if y is not None and self.color[y] == WHITE and y not in protected:
                    protected.add(y)
                    stack.append(y)
        return all(
            y in protected
            for x, c in enumerate(self.color) if c == BLACK
            for y in self.fields[x] if y is not None and self.color[y] == WHITE
        )

    def lost(self) -> set[int]:
        """After marking ends: the reachable objects that are still white, which a sweep would free."""
        return {x for x in self.reachable() if self.color[x] == WHITE}
