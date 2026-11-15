# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/positional-index/. The authors are listed in prov/F109TQ.jsonl.

from bisect import bisect_left
from typing import Sequence


class PositionalIndex:
    """For each term, the strictly increasing ids of the documents that hold it, and for
    each such document the strictly increasing positions of the term in it.

    Positions count tokens from 0. Space is one entry per token plus one per posting.
    """

    def __init__(self) -> None:
        self._ids: dict[str, list[int]] = {}
        self._pos: dict[str, list[list[int]]] = {}
        self._last: int | None = None

    def add_document(self, doc_id: int, tokens: Sequence[str]) -> None:
        """Add a document. Precondition: doc_id is greater than every id added before.

        Cost O(len(tokens)) expected, with a hash table from terms to lists.
        """
        if self._last is not None and not (self._last < doc_id):  # @line L1
            raise ValueError("documents must be added in increasing id order")
        self._last = doc_id
        for i, term in enumerate(tokens):  # @line L2
            ids = self._ids.setdefault(term, [])  # @line L3
            pos = self._pos.setdefault(term, [])
            if not ids or ids[-1] != doc_id:  # @line L4
                ids.append(doc_id)
                pos.append([])
            pos[-1].append(i)  # @line L5

    def postings(self, term: str) -> list[int]:
        """Return the ids of the documents that hold term, in increasing order."""
        return list(self._ids.get(term, []))

    def entries(self, term: str) -> list[tuple[int, list[int]]]:
        """Return the positional posting list of term as (doc_id, positions) pairs."""
        return [(d, list(p)) for d, p in zip(self._ids.get(term, []), self._pos.get(term, []))]

    def positions(self, term: str, doc_id: int) -> list[int]:
        """Return the positions of term in document doc_id, or [] if it does not occur.

        Cost O(log df(term)) by binary search on the ids, plus the length of the answer.
        """
        ids = self._ids.get(term)  # @line L6
        if ids is None:
            return []
        p = bisect_left(ids, doc_id)  # @line L7
        if p < len(ids) and ids[p] == doc_id:  # @line L8
            return list(self._pos[term][p])
        return []  # @line L9

    def df(self, term: str) -> int:
        """Return the number of documents that hold term."""
        return len(self._ids.get(term, []))

    def tf(self, term: str, doc_id: int) -> int:
        """Return the number of times term occurs in document doc_id."""
        return len(self.positions(term, doc_id))

    def cf(self, term: str) -> int:
        """Return the number of times term occurs in the whole collection."""
        return sum(len(p) for p in self._pos.get(term, []))

    def terms(self) -> list[str]:
        """Return the terms of the index in sorted order."""
        return sorted(self._ids)

    def check_invariant(self) -> None:
        """Raise AssertionError unless all ids and all position lists are strictly increasing."""
        for term, ids in self._ids.items():
            pos = self._pos[term]
            assert len(ids) == len(pos)
            for i in range(1, len(ids)):
                assert ids[i - 1] < ids[i]
            for p in pos:
                assert p
                for i in range(1, len(p)):
                    assert p[i - 1] < p[i]


def build_positional_index(docs: dict[int, Sequence[str]]) -> PositionalIndex:
    """Build the positional index of a tokenized collection, reading the ids in increasing order."""
    index = PositionalIndex()
    for d in sorted(docs):
        index.add_document(d, docs[d])
    return index
