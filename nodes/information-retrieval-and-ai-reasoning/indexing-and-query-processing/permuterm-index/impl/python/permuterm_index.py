# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/permuterm-index/. The authors are listed in prov/J3EW3B.jsonl.
"""A permuterm index of a vocabulary, for wildcard queries.

Each term t gets the end mark $, and every rotation of t$ is a key that
points back to t. The keys are kept in one sorted array. A query X*Y is
rotated to Y$X, and the answer is the set of terms whose keys start with
Y$X: one binary search for each end of the range. With more than one *,
the outer pieces give the range and a postfilter checks the middle pieces.
"""

import bisect

MARK = "$"
STAR = "*"
TOP = "\U0010ffff"  # sorts after every letter of a term and after $


def rotations(t: str) -> list[str]:
    """Return the |t| + 1 rotations of t$, starting with t$ itself. Cost O(|t|^2)."""
    s = t + MARK
    return [s[i:] + s[:i] for i in range(len(s))]


def matches(t: str, q: str) -> bool:
    """Tell if t matches q, where * stands for any string. Cost O(|t| |q|) at most."""
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


class PermutermIndex:
    """A sorted array of (key, term) pairs, one pair for each rotation of t$ of each term t.

    Terms are strings without $, * and the character TOP; the empty term is
    allowed. Invariant: keys is sorted, has no repeats, and holds exactly the
    rotations of t$ for the terms t of the vocabulary; owner[i] is the term of
    keys[i].
    """

    def __init__(self) -> None:
        self.keys: list[str] = []
        self.owner: list[str] = []
        self.count = 0

    def __len__(self) -> int:
        return self.count

    def __contains__(self, t: str) -> bool:
        key = t + MARK
        i = bisect.bisect_left(self.keys, key)
        return i < len(self.keys) and self.keys[i] == key

    def insert(self, t: str) -> None:
        """Add the term t. Cost O(|t|) binary searches, plus O(|t| K) to shift the arrays of K keys."""
        if MARK in t or STAR in t or TOP in t:
            raise ValueError("a term has no $, * or TOP")
        if t in self:  # @line L9
            return
        for r in rotations(t):  # @line L10
            i = bisect.bisect_left(self.keys, r)
            self.keys.insert(i, r)
            self.owner.insert(i, t)
        self.count += 1

    def delete(self, t: str) -> None:
        """Remove the term t if it is present. Same cost as insert."""
        if t not in self:
            return
        for r in rotations(t):
            i = bisect.bisect_left(self.keys, r)
            del self.keys[i]
            del self.owner[i]
        self.count -= 1

    def prefix_range(self, p: str) -> tuple[int, int]:
        """Return the range [lo, hi) of the keys that start with p. Cost O(|p| log K)."""
        return bisect.bisect_left(self.keys, p), bisect.bisect_left(self.keys, p + TOP)

    def wildcard(self, q: str) -> list[str]:
        """Return the sorted list of the terms that match q, where * stands for any string.

        Precondition: q has no $ and no TOP. Cost: O(|q| log K) for the range, plus
        O(r log r) to sort the r terms found; with two or more *, also
        O(|t| |q|) to check each term t of the range.
        """
        if STAR not in q:  # @line L1
            return [q] if q in self else []
        x, z = q[: q.index(STAR)], q[q.rindex(STAR) + 1 :]  # @line L2
        p = z + MARK + x  # @line L3
        lo, hi = self.prefix_range(p)  # @line L4
        c = self.owner[lo:hi]
        if q.count(STAR) == 1:  # @line L5
            return sorted(c)
        return sorted(t for t in c if matches(t, q))  # @line L6

    def range_terms(self, q: str) -> list[str]:
        """Return the terms of the key range of q before any postfilter, sorted. Precondition: q has a *."""
        x, z = q[: q.index(STAR)], q[q.rindex(STAR) + 1 :]
        lo, hi = self.prefix_range(z + MARK + x)
        return sorted(self.owner[lo:hi])

    def check_invariant(self) -> None:
        """Raise AssertionError unless keys and owner hold exactly the rotations of the terms, sorted."""
        assert len(self.keys) == len(self.owner)
        assert all(self.keys[i] < self.keys[i + 1] for i in range(len(self.keys) - 1))
        terms = {t for t in self.owner}
        assert len(terms) == self.count
        want = sorted((r, t) for t in terms for r in rotations(t))
        assert want == list(zip(self.keys, self.owner))
