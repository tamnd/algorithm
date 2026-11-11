# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/causal-tree/. The authors are listed in prov/B5EAJ4.jsonl.

"""The causal tree of Grishchenko (2010), an op-based sequence CRDT.

Every edit is an atom with a unique id (Lamport time, site) and a cause: the
atom it was typed after. The atoms form a tree under the cause relation, with
a root atom at the start. The text is the depth-first walk of the tree (the
weave), with the children of each atom visited in descending id order, so a
newer atom comes nearer its cause. A deletion is an atom too: a delete atom
whose cause is the deleted atom. An atom with a delete child is hidden.
Atoms must arrive in causal order, so that the cause of an atom is present.
"""

from typing import Any, NamedTuple

Id = tuple[int, int]  # (Lamport time, site)
ROOT: Id = (0, -1)


class Atom(NamedTuple):
    id: Id
    cause: Id
    kind: str  # "char" or "del"
    value: Any


class CausalTree:
    """One replica of a causal tree, with site id site."""

    def __init__(self, site: int) -> None:
        self.site = site
        self.clock = 0
        self.atoms: dict[Id, Atom] = {ROOT: Atom(ROOT, ROOT, "root", None)}  # @line L1
        self.children: dict[Id, list[Id]] = {ROOT: []}

    def add(self, atom: Atom) -> None:
        """Put an atom into the tree. Its cause must already be present."""
        if atom.id in self.atoms:
            return
        self.clock = max(self.clock, atom.id[0])
        self.atoms[atom.id] = atom  # @line L2
        self.children[atom.id] = []
        sib = self.children[atom.cause]  # @line L3
        sib.append(atom.id)
        sib.sort(reverse=True)  # @line L4

    def weave(self) -> list[Atom]:
        """Depth-first walk, children in descending id order."""
        out: list[Atom] = []
        stack = [ROOT]  # @line L5
        while stack:
            a = stack.pop()  # @line L6
            out.append(self.atoms[a])  # @line L7
            stack.extend(reversed(self.children[a]))  # @line L8
        return out[1:]

    def _visible(self) -> list[Atom]:
        dead = {a.cause for a in self.atoms.values() if a.kind == "del"}
        return [a for a in self.weave() if a.kind == "char" and a.id not in dead]  # @line L9

    def _new_id(self) -> Id:
        self.clock += 1
        return (self.clock, self.site)

    def local_insert(self, i: int, value: Any) -> Atom:
        vis = self._visible()
        cause = vis[i - 1].id if i > 0 else ROOT
        atom = Atom(self._new_id(), cause, "char", value)
        self.add(atom)
        return atom

    def local_delete(self, i: int) -> Atom:
        atom = Atom(self._new_id(), self._visible()[i].id, "del", None)
        self.add(atom)
        return atom

    def apply(self, atom: Atom) -> None:
        self.add(atom)

    def value(self) -> list[Any]:
        return [a.value for a in self._visible()]

    def order(self) -> list[Id]:
        """Ids of the character atoms in weave order, deleted ones included."""
        return [a.id for a in self.weave() if a.kind == "char"]

    def check_invariant(self) -> None:
        for a in self.atoms.values():
            if a.id != ROOT:
                assert a.cause in self.atoms and a.cause < a.id, "a cause is older than its effect"
        assert sum(len(c) for c in self.children.values()) == len(self.atoms) - 1
