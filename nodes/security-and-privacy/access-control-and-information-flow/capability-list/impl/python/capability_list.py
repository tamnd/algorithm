# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/capability-list/. The authors are listed in prov/P22TZC.jsonl.

"""Capability lists: the access matrix stored by row (Dennis and Van Horn 1966).

Each subject has a c-list, a table of slots. A slot holds a capability: an
object name, a set of rights, and a link to the capability it was copied
from. The table is held by the system, and a subject names a capability
only by a slot number of its own c-list, so a subject cannot forge one.
A copy never has more rights than its parent (attenuation), and revoking
a capability also removes every copy made from it (a derivation tree).
"""

from collections.abc import Hashable, Iterable
from dataclasses import dataclass, field

Subject = Hashable
Obj = Hashable
Right = Hashable


@dataclass
class Capability:
    """One capability, as the system stores it."""

    holder: Subject
    slot: int
    obj: Obj
    rights: frozenset[Right]
    parent: int | None
    children: set[int] = field(default_factory=set)


class CapabilityList:
    """The c-lists of all subjects of one protection state.

    create, check and the slot lookup take O(1) expected time (hash tables
    for the c-lists). delegate takes O(r) time for the subset test, where r
    is the number of rights. revoke takes time linear in the number of
    capabilities it removes. Slot numbers of a subject are never reused.
    """

    def __init__(self) -> None:
        self._clist: dict[Subject, dict[int, int]] = {}
        self._caps: dict[int, Capability] = {}
        self._next_slot: dict[Subject, int] = {}
        self._next_id = 0

    def _store(self, holder: Subject, obj: Obj, rights: frozenset[Right], parent: int | None) -> int:
        slot = self._next_slot.get(holder, 0)
        self._next_slot[holder] = slot + 1
        cid = self._next_id
        self._next_id += 1
        self._caps[cid] = Capability(holder, slot, obj, rights, parent)
        self._clist.setdefault(holder, {})[slot] = cid
        if parent is not None:
            self._caps[parent].children.add(cid)
        return slot

    def _lookup(self, s: Subject, i: int) -> Capability | None:
        cid = self._clist.get(s, {}).get(i)
        return None if cid is None else self._caps[cid]

    # The operations of the main pseudocode block.

    def create(self, s: Subject, o: Obj, rights: Iterable[Right]) -> int:
        """The system gives s a root capability for o; return its slot."""
        frozen = frozenset(rights)  # @line L1
        return self._store(s, o, frozen, None)  # @line L2

    def check(self, s: Subject, i: int, o: Obj, r: Right) -> bool:
        """Return True when slot i of the c-list of s names o and holds right r."""
        cap = self._lookup(s, i)
        if cap is None:  # @line L3
            return False
        obj, rights = cap.obj, cap.rights  # @line L4
        return obj == o and r in rights  # @line L5

    def delegate(self, s: Subject, i: int, t: Subject, rights: Iterable[Right]) -> int | None:
        """Give t a copy of slot i of s with the given rights; return the new slot.

        Return None when the slot is empty or when the rights are not a
        subset of the rights of the capability.
        """
        cap = self._lookup(s, i)
        if cap is None:  # @line L6
            return None
        cid = self._clist[s][i]  # @line L7
        wanted = frozenset(rights)
        if not wanted <= cap.rights:  # @line L8
            return None
        return self._store(t, cap.obj, wanted, cid)  # @line L9

    def revoke(self, s: Subject, i: int) -> int:
        """Remove slot i of s and every capability copied from it; return how many."""
        if self._lookup(s, i) is None:  # @line L10
            return 0
        root = self._clist[s][i]
        parent = self._caps[root].parent
        if parent is not None:
            self._caps[parent].children.discard(root)
        stack = [root]  # @line L11
        removed = 0
        while stack:  # @line L12
            cid = stack.pop()  # @line L13
            cap = self._caps.pop(cid)
            stack.extend(cap.children)
            del self._clist[cap.holder][cap.slot]  # @line L14
            removed += 1
        return removed

    # Views of the state.

    def slots(self, s: Subject) -> list[tuple[int, Obj, frozenset[Right]]]:
        """Return the c-list of s as (slot, object, rights), by slot number."""
        out = []
        for slot, cid in sorted(self._clist.get(s, {}).items()):
            cap = self._caps[cid]
            out.append((slot, cap.obj, cap.rights))
        return out

    def rights(self, s: Subject, o: Obj) -> frozenset[Right]:
        """Return the cell A[s, o]: the union of the rights of the capabilities of s for o."""
        out: frozenset[Right] = frozenset()
        for _, obj, rights in self.slots(s):
            if obj == o:
                out |= rights
        return out

    def to_matrix(self) -> dict[tuple[Subject, Obj], frozenset[Right]]:
        """Return the nonempty cells of the access matrix that the c-lists give."""
        out: dict[tuple[Subject, Obj], frozenset[Right]] = {}
        for cap in self._caps.values():
            if cap.rights:
                key = (cap.holder, cap.obj)
                out[key] = out.get(key, frozenset()) | cap.rights
        return out

    def holders(self, o: Obj) -> list[Subject]:
        """Return the subjects that hold some capability for o. This scans every c-list."""
        return sorted({cap.holder for cap in self._caps.values() if cap.obj == o}, key=repr)

    def check_invariant(self) -> None:
        """Raise AssertionError unless the slots, parents and children agree."""
        seen = 0
        for s, table in self._clist.items():
            for slot, cid in table.items():
                cap = self._caps[cid]
                assert cap.holder == s and cap.slot == slot
                seen += 1
        assert seen == len(self._caps), "a capability without a slot"
        for cid, cap in self._caps.items():
            if cap.parent is not None:
                parent = self._caps.get(cap.parent)
                assert parent is not None, "a live copy of a removed capability"
                assert cid in parent.children
                assert cap.obj == parent.obj
                assert cap.rights <= parent.rights, "a copy with more rights than its parent"
            for child in cap.children:
                assert self._caps[child].parent == cid
