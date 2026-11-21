# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/access-control-list/. The authors are listed in prov/443DQ0.jsonl.

"""Access control lists: the access matrix stored by column (Lampson 1971).

Each object keeps a list of entries (subject, rights). The list holds at
most one entry for each subject, and no entry has an empty set of rights.
"""

from collections.abc import Hashable, Iterable, Mapping

Subject = Hashable
Obj = Hashable
Right = Hashable
Entry = tuple[Subject, frozenset[Right]]


class AccessControlList:
    """The access lists of all objects of one protection state.

    check, grant and revoke scan the list of one object, so each takes
    O(L) time, where L is the length of that list (L is at most the
    number of subjects). revoke_subject scans every list, so it takes time
    linear in the total number of entries. The space is linear in the
    number of nonempty cells of the access matrix, plus one list header
    for each object.
    """

    def __init__(self) -> None:
        self._acl: dict[Obj, list[Entry]] = {}

    # The operations of the main pseudocode block.

    def check(self, s: Subject, o: Obj, r: Right) -> bool:
        """Return True when the list of object o gives right r to subject s."""
        for subject, rights in self._acl.get(o, []):  # @line L1
            if subject == s:  # @line L2
                return r in rights
        return False  # @line L3

    def grant(self, s: Subject, o: Obj, r: Right) -> None:
        """Add right r for subject s to the list of object o.

        The object is created with an empty list when it is new.
        """
        entries = self._acl.setdefault(o, [])
        for k, (subject, rights) in enumerate(entries):  # @line L4
            if subject == s:
                entries[k] = (subject, rights | {r})  # @line L5
                return
        entries.append((s, frozenset([r])))  # @line L6

    def revoke(self, s: Subject, o: Obj, r: Right) -> None:
        """Remove right r of subject s from the list of object o, if it is there."""
        entries = self._acl.get(o, [])
        for k, (subject, rights) in enumerate(entries):  # @line L7
            if subject == s:  # @line L8
                rest = rights - {r}  # @line L9
                if rest:
                    entries[k] = (subject, rest)
                else:
                    del entries[k]  # @line L10
                return  # @line L11

    def revoke_subject(self, s: Subject) -> None:
        """Remove every entry of subject s from every list."""
        for o in self._acl:  # @line L12
            self._acl[o] = [(subject, rights) for subject, rights in self._acl[o] if subject != s]  # @line L13

    # Other operations.

    def create_object(self, o: Obj) -> None:
        """Make object o known with an empty list. Nothing happens if it exists."""
        self._acl.setdefault(o, [])

    def delete_object(self, o: Obj) -> None:
        """Remove object o and its list."""
        self._acl.pop(o, None)

    def rights(self, s: Subject, o: Obj) -> frozenset[Right]:
        """Return the cell A[s, o] of the access matrix."""
        for subject, rights in self._acl.get(o, []):
            if subject == s:
                return rights
        return frozenset()

    def entries(self, o: Obj) -> list[Entry]:
        """Return a copy of the list of object o (one column of the matrix)."""
        return list(self._acl.get(o, []))

    def objects(self) -> list[Obj]:
        """Return the objects in the order in which they were created."""
        return list(self._acl)

    def to_matrix(self) -> dict[tuple[Subject, Obj], frozenset[Right]]:
        """Return the nonempty cells of the access matrix as a dict."""
        return {(s, o): rights for o, entries in self._acl.items() for s, rights in entries}

    @classmethod
    def from_matrix(
        cls, matrix: Mapping[tuple[Subject, Obj], Iterable[Right]], objects: Iterable[Obj] = ()
    ) -> "AccessControlList":
        """Build the lists from the cells of a matrix. Empty cells give no entry."""
        acl = cls()
        for o in objects:
            acl.create_object(o)
        for (s, o), rights in matrix.items():
            acl.create_object(o)
            frozen = frozenset(rights)
            if frozen:
                acl._acl[o].append((s, frozen))
        return acl

    def check_invariant(self) -> None:
        """Raise AssertionError unless each list has distinct subjects and no empty entry."""
        for entries in self._acl.values():
            subjects = [subject for subject, _ in entries]
            assert len(subjects) == len(set(subjects)), "two entries for one subject"
            assert all(rights for _, rights in entries), "an entry with no rights"
