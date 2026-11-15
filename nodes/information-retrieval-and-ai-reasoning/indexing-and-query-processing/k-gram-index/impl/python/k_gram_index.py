# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-gram-index/. The authors are listed in prov/HHWFE5.jsonl.
"""A k-gram index of a vocabulary, for wildcard queries.

Each term t is padded as $t$, and every substring of k letters of the padded
term is a k-gram. The index maps each k-gram to the sorted list of the terms
that contain it. A query with the wildcard * is answered by intersecting the
lists of the k-grams of the query, then by a postfilter that keeps only the
terms that match the query.
"""

import bisect

MARK = "$"
STAR = "*"


def grams(s: str, k: int) -> list[str]:
    """Return the k-grams of s, in order, with repeats. Cost O(|s| k)."""
    return [s[i : i + k] for i in range(len(s) - k + 1)]


def matches(t: str, q: str) -> bool:
    """Tell if the term t matches the query q, in which * stands for any string, also the empty one.

    The first piece of q must be a prefix of t, the last piece a suffix, and the
    middle pieces must occur in order in between, each at its leftmost place.
    Cost O(|t| |q|) at most.
    """
    pieces = q.split(STAR)
    if len(pieces) == 1:
        return t == q
    first, last = pieces[0], pieces[-1]
    if len(first) + len(last) > len(t) or not t.startswith(first) or not t.endswith(last):
        return False
    pos, end = len(first), len(t) - len(last)
    for p in pieces[1:-1]:
        i = t.find(p, pos, end)
        if i < 0:
            return False
        pos = i + len(p)
    return True


def intersect(a: list[str], b: list[str]) -> list[str]:
    """Merge-based intersection of two sorted lists. Cost O(|a| + |b|)."""
    i = j = 0
    out: list[str] = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            out.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return out


class KGramIndex:
    """A vocabulary of terms with, for each k-gram, the sorted list of the terms that contain it.

    Terms are nonempty strings without $ and *. Invariant: postings[g] is the
    sorted list, without repeats, of the terms t of the vocabulary such that g
    is a k-gram of $t$, and no list is empty.
    """

    def __init__(self, k: int = 3) -> None:
        if k < 1:
            raise ValueError("k must be at least 1")
        self.k = k
        self.terms: list[str] = []
        self.postings: dict[str, list[str]] = {}

    def __len__(self) -> int:
        return len(self.terms)

    def __contains__(self, t: str) -> bool:
        i = bisect.bisect_left(self.terms, t)
        return i < len(self.terms) and self.terms[i] == t

    def insert(self, t: str) -> None:
        """Add the term t. Cost O(|t| k) for the grams, plus O(L) to insert into each of their lists of length L."""
        if not t or MARK in t or STAR in t:
            raise ValueError("a term is a nonempty string without $ and *")
        if t in self:  # @line L8
            return
        bisect.insort(self.terms, t)  # @line L9
        for g in set(grams(MARK + t + MARK, self.k)):  # @line L10
            bisect.insort(self.postings.setdefault(g, []), t)

    def delete(self, t: str) -> None:
        """Remove the term t if it is present. Same cost as insert."""
        if t not in self:
            return
        self.terms.remove(t)
        for g in set(grams(MARK + t + MARK, self.k)):
            lst = self.postings[g]
            lst.pop(bisect.bisect_left(lst, t))
            if not lst:
                del self.postings[g]

    def query_grams(self, q: str) -> list[str]:
        """Return the distinct k-grams of $q$ that contain no *, sorted. Cost O(|q| k)."""
        return sorted({g for piece in (MARK + q + MARK).split(STAR) for g in grams(piece, self.k)})

    def candidates(self, q: str) -> list[str]:
        """Return the sorted terms that contain every k-gram of the query: a superset of the answer.

        Cost: the sum of the lengths of the lists of the query grams, or the
        whole vocabulary when the query has no k-gram.
        """
        g = self.query_grams(q)
        if not g:
            return list(self.terms)
        lists = sorted((self.postings.get(x, []) for x in g), key=len)
        c = lists[0]
        for lst in lists[1:]:
            c = intersect(c, lst)
        return c

    def wildcard(self, q: str) -> list[str]:
        """Return the sorted list of the terms that match q, where * stands for any string.

        Precondition: q has no $. Cost: that of candidates, plus O(|t| |q|) for each candidate t.
        """
        g = self.query_grams(q)  # @line L1
        if not g:  # @line L2
            c = list(self.terms)
        else:
            lists = sorted((self.postings.get(x, []) for x in g), key=len)  # @line L3
            c = lists[0]
            for lst in lists[1:]:
                c = intersect(c, lst)
        r: list[str] = []  # @line L4
        for t in c:  # @line L5
            if matches(t, q):  # @line L6
                r.append(t)
        return r  # @line L7

    def check_invariant(self) -> None:
        """Raise AssertionError unless the postings are exactly the k-grams of the terms, as sorted lists."""
        assert self.terms == sorted(set(self.terms))
        want: dict[str, set[str]] = {}
        for t in self.terms:
            for g in grams(MARK + t + MARK, self.k):
                want.setdefault(g, set()).add(t)
        assert set(want) == set(self.postings)
        for g, ts in want.items():
            assert self.postings[g] == sorted(ts)
