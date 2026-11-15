# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/posting-list/. The authors are listed in prov/CHQP94.jsonl.

from typing import Any


class PostingList:
    """The posting list of one term: strictly increasing document ids, each with its term frequency.

    The ids may be any values with a total order that support < and ==.
    Space is two arrays of len(self) entries.
    """

    def __init__(self) -> None:
        self.ids: list[Any] = []
        self.tf: list[int] = []

    def __len__(self) -> int:
        return len(self.ids)

    def append(self, doc_id: Any, tf: int = 1) -> None:
        """Add a posting at the end. Precondition: doc_id is greater than the last id. Cost O(1) amortized."""
        if self.ids and not (self.ids[-1] < doc_id):  # @line L1
            raise ValueError("document ids must be appended in increasing order")
        self.ids.append(doc_id)  # @line L2
        self.tf.append(tf)

    def access(self, i: int) -> tuple[Any, int]:
        """Return the posting at index i as (doc_id, tf). Precondition: 0 <= i < len(self). Cost O(1)."""
        return self.ids[i], self.tf[i]

    def next_geq(self, x: Any, lo: int = 0) -> int:
        """Return the least index p >= lo with ids[p] >= x, or len(self) if there is none.

        Galloping search from lo. Precondition: 0 <= lo. If g = p - lo, the call makes
        one comparison when g = 0, and at most 2 floor(log2 g) + 2 comparisons when g >= 1.
        """
        ids = self.ids
        n = len(ids)  # @line L3
        if lo >= n or not (ids[lo] < x):  # @line L4
            return lo
        b = 1  # @line L5: ids[lo + b - 1] < x
        while lo + 2 * b - 1 < n and ids[lo + 2 * b - 1] < x:  # @line L6
            b *= 2
        a, c = lo + b, min(lo + 2 * b - 1, n)  # @line L7
        while a < c:  # @line L8
            q = (a + c) // 2  # @line L9
            if ids[q] < x:  # @line L10
                a = q + 1
            else:
                c = q
        return a  # @line L11

    def check_invariant(self) -> None:
        """Raise AssertionError unless the ids are strictly increasing and each tf is positive."""
        assert len(self.ids) == len(self.tf)
        for i in range(1, len(self.ids)):
            assert self.ids[i - 1] < self.ids[i]
        assert all(f >= 1 for f in self.tf)


def build_postings(docs: dict[int, list[str]]) -> dict[str, PostingList]:
    """Build the posting list of each term of a tokenized collection.

    The documents are read in increasing id order, so each append keeps the order.
    Cost O(T) expected time for T tokens, with a hash table from terms to lists.
    """
    index: dict[str, PostingList] = {}
    for d in sorted(docs):
        counts: dict[str, int] = {}
        for term in docs[d]:
            counts[term] = counts.get(term, 0) + 1
        for term, f in counts.items():
            index.setdefault(term, PostingList()).append(d, f)
    return index
