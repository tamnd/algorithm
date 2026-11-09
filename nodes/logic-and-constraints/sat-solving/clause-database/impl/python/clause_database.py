# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clause-database/. The authors are listed in prov/K9N1A5.jsonl.

"""A clause database for a CDCL solver, stored in one flat array.

Each clause is a header of three ints (size, flags, LBD) followed by its
literals. The reference of a clause is the index of its header. Flag bit 0
marks a learned clause and bit 1 marks a deleted one. The first two
literals of each live clause are its watched literals, and the watch list of
a literal holds the references of the clauses that watch it. Deletion is
lazy: a deleted clause stays in the array and in the watch lists until the
next garbage collection, which compacts the array and relocates the
references. Literals are nonzero ints in DIMACS style.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence

HEADER = 3
LEARNED = 1
DELETED = 2


def _idx(lit: int) -> int:
    return 2 * lit if lit > 0 else -2 * lit + 1


class ClauseDatabase:
    """Clauses over the variables 1..n with watch lists.

    Costs: add O(k) for k literals, delete O(1), swap_watch O(k + w) where w
    is the length of the old watch list, watchers O(w), collect_garbage
    O(|arena| + total length of the watch lists). Space O(|arena| + 2n).
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.arena: list[int] = []
        self.watches: list[list[int]] = [[] for _ in range(2 * n + 2)]
        self.wasted = 0  # ints held by deleted clauses

    # ------------------------------------------------------------ reading

    def size(self, r: int) -> int:
        return self.arena[r]

    def literals(self, r: int) -> list[int]:
        return self.arena[r + HEADER : r + HEADER + self.arena[r]]

    def is_learned(self, r: int) -> bool:
        return bool(self.arena[r + 1] & LEARNED)

    def is_deleted(self, r: int) -> bool:
        return bool(self.arena[r + 1] & DELETED)

    def lbd(self, r: int) -> int:
        return self.arena[r + 2]

    def set_lbd(self, r: int, g: int) -> None:
        self.arena[r + 2] = g

    def refs(self) -> Iterator[int]:
        """The references of the live clauses, in the order of the array."""
        r = 0
        while r < len(self.arena):
            if not self.arena[r + 1] & DELETED:
                yield r
            r += HEADER + self.arena[r]

    def watchers(self, lit: int) -> list[int]:
        """The live clauses that watch lit."""
        return [r for r in self.watches[_idx(lit)] if not self.arena[r + 1] & DELETED]

    # ----------------------------------------------------------- updating

    def add(self, lits: Sequence[int], learned: bool = False, lbd: int = 0) -> int:
        """Store a clause and watch its first two literals. Precondition: at
        least two literals over distinct variables in 1..n."""
        if len(lits) < 2 or len({abs(q) for q in lits}) != len(lits):
            raise ValueError("a stored clause needs two or more distinct variables")
        if any(q == 0 or abs(q) > self.n for q in lits):
            raise ValueError("literal out of range")
        r = len(self.arena)  # @line L1
        self.arena += [len(lits), LEARNED if learned else 0, lbd, *lits]  # @line L2
        self.watches[_idx(lits[0])].append(r)  # @line L3
        self.watches[_idx(lits[1])].append(r)
        return r  # @line L4

    def delete(self, r: int) -> None:
        """Mark the clause r as deleted. Its space is reclaimed by the next
        garbage collection."""
        if self.arena[r + 1] & DELETED:
            raise ValueError("clause already deleted")
        self.arena[r + 1] |= DELETED  # @line L5
        self.wasted += HEADER + self.arena[r]  # @line L6

    def swap_watch(self, r: int, i: int, k: int) -> None:
        """Make the literal at position k of clause r a watched literal in
        place of the one at position i. Precondition: i in {0, 1}, k >= 2."""
        if i not in (0, 1) or not 2 <= k < self.arena[r] or self.arena[r + 1] & DELETED:
            raise ValueError("bad watch swap")
        a, b = r + HEADER + i, r + HEADER + k
        old, new = self.arena[a], self.arena[b]
        self.arena[a], self.arena[b] = new, old  # @line L7
        self.watches[_idx(old)].remove(r)  # @line L8
        self.watches[_idx(new)].append(r)

    def collect_garbage(self) -> dict[int, int]:
        """Compact the array and drop deleted clauses from the watch lists.
        Return the map from old to new references of the live clauses; the
        caller must apply it to every reference it keeps, such as reasons."""
        new: list[int] = []  # @line L9
        moved: dict[int, int] = {}
        r = 0
        while r < len(self.arena):  # @line L10
            end = r + HEADER + self.arena[r]
            if not self.arena[r + 1] & DELETED:  # @line L11
                moved[r] = len(new)
                new += self.arena[r:end]
            r = end
        for j, ws in enumerate(self.watches):  # @line L12
            self.watches[j] = [moved[x] for x in ws if x in moved]
        self.arena = new  # @line L13
        self.wasted = 0
        return moved  # @line L14

    # ---------------------------------------------------------- invariant

    def check_invariant(self) -> bool:
        """The array parses into clauses, wasted counts the deleted space,
        and each live clause is in the watch lists of exactly its first two
        literals, once each."""
        live: set[int] = set()
        wasted = 0
        r = 0
        while r < len(self.arena):
            if r + HEADER > len(self.arena):
                return False
            k, flags = self.arena[r], self.arena[r + 1]
            if k < 2 or r + HEADER + k > len(self.arena) or flags & ~(LEARNED | DELETED):
                return False
            lits = self.arena[r + HEADER : r + HEADER + k]
            if any(q == 0 or abs(q) > self.n for q in lits) or len({abs(q) for q in lits}) != k:
                return False
            if flags & DELETED:
                wasted += HEADER + k
            else:
                live.add(r)
            r += HEADER + k
        if wasted != self.wasted:
            return False
        for j, ws in enumerate(self.watches):
            alive = [x for x in ws if x in live]
            if len(alive) != len(set(alive)):
                return False
            for x in ws:
                if x not in live and not (0 <= x < len(self.arena) and self.arena[x + 1] & DELETED):
                    return False
            expected = {x for x in live if j in (_idx(self.arena[x + HEADER]), _idx(self.arena[x + HEADER + 1]))}
            if set(alive) != expected:
                return False
        return True
