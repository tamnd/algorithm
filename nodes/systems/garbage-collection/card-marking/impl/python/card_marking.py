# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/card-marking/. The authors are listed in prov/45B69W.jsonl.

"""Card marking for a two-generation heap.

The old generation is an array of words M. An old object at address a has a
header M[a] = k (its number of fields) and its fields in M[a+1 .. a+k]. The
old generation is split into cards of 2**shift words, with one byte per card
in the card table C. The write barrier stores DIRTY into the card byte on
every pointer store into an old object, whatever the value: it does no test.
A crossing map F gives, for each card, the start of the object that covers
the first word of the card, so that a scan can start in the middle of an
object.

Pointers: None is nil, an int a >= 0 is the old object at address a, and an
int below 0 is a young object. A minor collection is a Cheney copy of the
young generation whose roots are the root slots and the young pointers found
on dirty cards. Survivors of age `tenure_age` are promoted into M.

mode "slot" marks the card of the stored slot and scans the slots on a dirty
card. mode "object" marks the card of the object header (as in Hoelzle's
variant with object boundaries) and scans all fields of each object whose
header lies on a dirty card.
"""

from typing import Callable, Optional

CLEAN, DIRTY = 1, 0  # marking a card is a store of zero
Ptr = Optional[int]


class Young:
    __slots__ = ("oid", "fields", "age")

    def __init__(self, oid: int, nfields: int) -> None:
        self.oid = oid
        self.fields: list[Ptr] = [None] * nfields
        self.age = 0


class CardHeap:
    def __init__(self, card_shift: int = 2, nursery_size: int = 8, tenure_age: int = 1, mode: str = "slot") -> None:
        if mode not in ("slot", "object"):
            raise ValueError("mode is 'slot' or 'object'")
        self.shift = card_shift
        self.nursery_size = nursery_size
        self.tenure_age = tenure_age
        self.mode = mode
        self.mem: list = []  # the old generation, word by word
        self.oid_at: dict[int, int] = {}  # old address -> object id
        self.cards = bytearray()  # the card table C
        self.first: list[int] = []  # the crossing map F
        self.young: dict[int, Young] = {}
        self.next_young = -1
        self.next_oid = 0
        self.roots: list[Ptr] = []
        self.minor_count = 0
        self.cards_scanned = 0

    # ---- helpers -------------------------------------------------------
    @staticmethod
    def is_young(v: Ptr) -> bool:
        return v is not None and v < 0

    def card_of(self, word: int) -> int:
        return word >> self.shift

    def fields_of(self, p: int) -> list:
        if p < 0:
            return self.young[p].fields
        n = self.mem[p]
        return self.mem[p + 1 : p + 1 + n]

    def oid(self, p: int) -> int:
        return self.young[p].oid if p < 0 else self.oid_at[p]

    def _new_young(self, oid: int, nfields: int) -> int:
        y = self.next_young
        self.next_young -= 1
        self.young[y] = Young(oid, nfields)
        return y

    def _alloc_old(self, oid: int, nfields: int) -> int:
        a = len(self.mem)
        self.mem.append(nfields)
        self.mem.extend([None] * nfields)
        self.oid_at[a] = oid
        top = len(self.mem)
        need = (top + (1 << self.shift) - 1) >> self.shift
        while len(self.cards) < need:
            self.cards.append(CLEAN)
            self.first.append(-1)
        lo = (a + (1 << self.shift) - 1) >> self.shift  # cards whose first word lies in [a, top)
        for c in range(lo, ((top - 1) >> self.shift) + 1):
            self.first[c] = a
        return a

    # ---- the mutator ---------------------------------------------------
    def alloc(self, nfields: int) -> int:
        """Allocate a young object; return the index of its root slot."""
        if len(self.young) >= self.nursery_size:
            self.minor_collect()
        y = self._new_young(self.next_oid, nfields)
        self.next_oid += 1
        self.roots.append(y)
        return len(self.roots) - 1

    def write(self, src_root: int, i: int, ref_root: Optional[int]) -> None:
        src = self.roots[src_root]
        assert src is not None
        v = None if ref_root is None else self.roots[ref_root]
        self.store(src, i, v)

    def store(self, src: int, i: int, v: Ptr) -> None:
        """The pointer store with the card-marking write barrier."""
        if src < 0:
            self.young[src].fields[i] = v  # the nursery has no cards
            return
        s = src + 1 + i
        self.mem[s] = v  # @line L1
        self.cards[self.card_of(s if self.mode == "slot" else src)] = DIRTY  # @line L2

    def load(self, src_root: int, i: int, dst_root: int) -> None:
        src = self.roots[src_root]
        assert src is not None
        self.roots[dst_root] = self.fields_of(src)[i]

    def drop(self, root: int) -> None:
        self.roots[root] = None

    # ---- the collector -------------------------------------------------
    def scan_dirty_cards(self, visit: Callable[[int], int], top: int) -> None:
        """Visit the young pointers on dirty cards below address `top`."""
        size = 1 << self.shift
        for c in range((top + size - 1) >> self.shift):  # @line L3
            if self.cards[c] != DIRTY:  # @line L4
                continue
            self.cards_scanned += 1
            self.cards[c] = CLEAN  # @line L5
            lo, hi = c << self.shift, (c + 1) << self.shift
            a = self.first[c]  # @line L6
            while a < hi and a < top:  # @line L7
                n = self.mem[a]
                if self.mode == "slot":
                    slots = range(max(a + 1, lo), min(a + 1 + n, hi))  # @line L8
                else:
                    slots = range(a + 1, a + 1 + n) if a >= lo else range(0)
                for s in slots:
                    if self.is_young(self.mem[s]):  # @line L9
                        self.mem[s] = visit(self.mem[s])  # @line L10
                        if self.is_young(self.mem[s]):  # @line L11
                            self.cards[c] = DIRTY
                a = a + 1 + n  # @line L12

    def minor_collect(self) -> None:
        self.minor_count += 1
        from_space = self.young
        self.young = {}
        forward: dict[int, int] = {}
        queue: list[int] = []
        top = len(self.mem)

        def evacuate(y: int) -> int:
            if y in forward:
                return forward[y]
            o = from_space[y]
            age = o.age + 1
            if age >= self.tenure_age:
                p = self._alloc_old(o.oid, len(o.fields))
                self.mem[p + 1 : p + 1 + len(o.fields)] = o.fields
            else:
                p = self._new_young(o.oid, len(o.fields))
                self.young[p].fields = list(o.fields)
                self.young[p].age = age
            forward[y] = p
            queue.append(p)
            return p

        def visit(v: int) -> int:
            return evacuate(v) if v in from_space else v

        for k, r in enumerate(self.roots):
            if r is not None and r in from_space:
                self.roots[k] = evacuate(r)
        self.scan_dirty_cards(visit, top)
        head = 0
        while head < len(queue):  # the Cheney scan of the copies
            p = queue[head]
            head += 1
            for i, t in enumerate(self.fields_of(p)):
                if t is not None and t in from_space:
                    nt = evacuate(t)
                    if p < 0:
                        self.young[p].fields[i] = nt
                    else:
                        s = p + 1 + i
                        self.mem[s] = nt
                        if self.is_young(nt):  # a promoted object points to a survivor  # @line L13
                            self.cards[self.card_of(s if self.mode == "slot" else p)] = DIRTY

    # ---- views used by the tests ---------------------------------------
    def old_objects(self) -> list[int]:
        out, a = [], 0
        while a < len(self.mem):
            out.append(a)
            a += 1 + self.mem[a]
        return out

    def old_to_young(self) -> list[tuple[int, int]]:
        return [(a, i) for a in self.old_objects() for i, t in enumerate(self.fields_of(a)) if self.is_young(t)]

    def covered(self, a: int, i: int) -> bool:
        word = a + 1 + i if self.mode == "slot" else a
        return self.cards[self.card_of(word)] == DIRTY
