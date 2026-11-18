# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/packed-trie/. The authors are listed in prov/JVDGBF.jsonl.

"""Liang's packed trie: the families of an indexed trie overlapped in one table.

An indexed trie gives each node (a family, or state) an array with one slot
per letter of the alphabet. Most slots are empty. The packed trie puts all
families into one table. A family with base b puts its transition on the
letter c in the slot b + code(c). Each slot stores the letter, so that a
lookup can tell its own transitions from those of other families that use
the same slot. Two families never get the same base. The families are
placed one at a time by first fit: each one goes to the lowest base where
its slots are free and the base is not taken.

A slot holds (letter, link, out). link is the base of the child family, or
None when the child has no transitions. out is the value of the key that
ends with this transition, or None.
"""

from typing import Dict, Iterator, List, Optional, Sequence, Tuple


class _Node:
    __slots__ = ("children", "value", "has_value")

    def __init__(self) -> None:
        self.children: Dict[str, "_Node"] = {}
        self.value = None
        self.has_value = False


class PackedTrie:
    """A static map from nonempty strings to values, packed by first fit."""

    def __init__(self, items: Dict[str, object], alphabet: Optional[Sequence[str]] = None) -> None:
        if any(len(k) == 0 for k in items):
            raise ValueError("keys must be nonempty")
        if any(v is None for v in items.values()):
            raise ValueError("None marks a missing value, so it cannot be a value")
        letters = sorted(set("".join(items))) if alphabet is None else list(alphabet)
        self.code = {c: i + 1 for i, c in enumerate(letters)}  # codes 1 .. sigma
        root = _Node()
        for key, value in items.items():
            node = root
            for ch in key:
                node = node.children.setdefault(ch, _Node())
            node.value, node.has_value = value, True
        self.char: List[Optional[str]] = []
        self.link: List[Optional[int]] = []
        self.out: List[object] = []
        self.owner: List[Optional[int]] = []  # the family that claimed the slot, for tests
        self.taken: set = set()
        self.families = 0
        self.transitions = 0
        self.first_fit_tries = 0
        self.root_base = self._pack(root)

    def _grow(self, size: int) -> None:
        while len(self.char) < size:
            self.char.append(None)
            self.link.append(None)
            self.out.append(None)
            self.owner.append(None)

    def _first_fit(self, codes: List[int]) -> int:
        """The lowest base b, not taken, with every slot b + code free."""
        b = 0  # @line L9
        while True:  # @line L10
            self.first_fit_tries += 1
            if b not in self.taken and all(b + c >= len(self.char) or self.char[b + c] is None for c in codes):  # @line L11
                return b  # @line L12
            b += 1  # @line L13

    def _pack(self, root: _Node) -> Optional[int]:
        """Pack the families in breadth-first order; return the base of the root."""
        if not root.children:
            return None
        order: List[Tuple[_Node, Optional[Tuple[int]]]] = [(root, None)]
        base_of_root = None
        q = 0
        while q < len(order):  # @line L14
            node, parent_slot = order[q]
            q += 1
            codes = sorted(self.code[c] for c in node.children)
            b = self._first_fit(codes)  # @line L15
            fam = self.families
            self.families += 1
            self.taken.add(b)  # @line L16
            self._grow(b + codes[-1] + 1)
            for ch, child in sorted(node.children.items()):  # @line L17
                s = b + self.code[ch]
                self.char[s] = ch  # @line L18
                self.owner[s] = fam
                self.out[s] = child.value if child.has_value else None
                self.transitions += 1
                if child.children:
                    order.append((child, (s,)))  # @line L19
            if parent_slot is None:
                base_of_root = b
            else:
                self.link[parent_slot[0]] = b  # @line L20
        return base_of_root

    def _slot(self, base: Optional[int], ch: str) -> Optional[int]:
        if base is None or ch not in self.code:
            return None
        s = base + self.code[ch]  # @line L1
        if s < len(self.char) and self.char[s] == ch:  # @line L2
            return s
        return None  # @line L3

    def get(self, key: str, default=None):
        """The value of key, or default. One table index per letter."""
        base = self.root_base
        s = None
        for ch in key:  # @line L4
            s = self._slot(base, ch)  # @line L5
            if s is None:
                return default  # @line L6
            base = self.link[s]  # @line L7
        if s is None or self.out[s] is None:
            return default
        return self.out[s]  # @line L8

    def __contains__(self, key: str) -> bool:
        return self.get(key, None) is not None

    def prefix_values(self, text: str, start: int = 0) -> Iterator[Tuple[int, object]]:
        """Yield (end, value) for each key equal to text[start:end].

        This is the walk of Liang's method at one start position.
        """
        base = self.root_base
        for j in range(start, len(text)):
            s = self._slot(base, text[j])
            if s is None:
                return
            if self.out[s] is not None:
                yield j + 1, self.out[s]
            base = self.link[s]

    def check_invariant(self) -> None:
        """Distinct bases, one owner per used slot, and every used slot inside a family."""
        assert len(self.taken) == self.families
        used = [s for s in range(len(self.char)) if self.char[s] is not None]
        assert len(used) == self.transitions
        for s in used:
            assert self.owner[s] is not None

    def size(self) -> int:
        """The number of slots of the table (its length)."""
        return len(self.char)

    def density(self) -> float:
        """The fraction of slots that hold a transition."""
        return self.transitions / max(1, self.size())
