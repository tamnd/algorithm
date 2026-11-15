# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signature-file/. The authors are listed in prov/WA5X66.jsonl.
"""A sequential signature file with superimposed coding.

Each term sets m distinct bits out of F. The signature of a document is the
OR of the signatures of its distinct terms. A query is the OR of the
signatures of its terms, and a document is a candidate when its signature
has a 1 in every place where the query has one. Candidates are then checked
against the terms of the document, which removes the false drops.
"""

import hashlib
from typing import Hashable, Iterable


class SignatureFile:
    """Signatures of F bits, m bits per term, one signature per document, in insertion order.

    The term sets of the documents are kept as well, in the role of the text
    file that the verification step reads.
    """

    def __init__(self, f: int = 64, m: int = 4, salt: bytes = b"") -> None:
        if not (1 <= m <= f <= 65536):
            raise ValueError("need 1 <= m <= f <= 65536")
        self.f, self.m, self.salt = f, m, salt[:16]
        self.ids: list[Hashable] = []
        self.sigs: list[int] = []
        self.terms: list[frozenset[str]] = []
        self._cache: dict[str, int] = {}

    def __len__(self) -> int:
        return len(self.ids)

    def term_signature(self, t: str) -> int:
        """Return the F-bit word of t: m distinct places, chosen by a keyed hash of t.

        The places come from 16-bit values of BLAKE2b, with rejection of values
        that would bias the place and of places already taken, so under the
        usual model of an ideal hash every m-subset is equally likely.
        Cost O(m) hash calls in expectation.
        """
        if t in self._cache:
            return self._cache[t]
        f, places, counter = self.f, set(), 0
        limit = 65536 - 65536 % f
        while len(places) < self.m:
            h = hashlib.blake2b(t.encode() + counter.to_bytes(4, "big"), key=self.salt, digest_size=32).digest()
            counter += 1
            for i in range(0, 32, 2):
                x = int.from_bytes(h[i : i + 2], "big")
                if x < limit:
                    places.add(x % f)
                    if len(places) == self.m:
                        break
        w = 0
        for p in places:
            w |= 1 << p
        if len(self._cache) < 1 << 16:
            self._cache[t] = w
        return w

    def signature(self, terms: Iterable[str]) -> int:
        """Return the OR of the term signatures of the distinct terms. Cost O(m) per term."""
        s = 0
        for t in set(terms):
            s |= self.term_signature(t)
        return s

    def insert(self, doc_id: Hashable, terms: Iterable[str]) -> None:
        """Append the signature of a document. Cost O(m) per distinct term of the document."""
        ts = frozenset(terms)
        self.ids.append(doc_id)
        self.sigs.append(self.signature(ts))
        self.terms.append(ts)

    def candidates(self, query: Iterable[str]) -> list[Hashable]:
        """Return the ids whose signature covers the query signature: the answers and the false drops.

        Cost: one scan of the N signatures, O(N F / w) word operations for words of w bits.
        """
        q = self.signature(query)
        return [d for d, s in zip(self.ids, self.sigs) if s & q == q]

    def search(self, query: Iterable[str]) -> list[Hashable]:
        """Return the ids of the documents that contain every query term, in insertion order.

        Cost: the scan of candidates, plus one check of the terms of each candidate.
        """
        qs = frozenset(query)
        q = 0  # @line L1
        for t in qs:  # @line L2
            q |= self.term_signature(t)
        r: list[Hashable] = []  # @line L3
        for d, s, ts in zip(self.ids, self.sigs, self.terms):  # @line L4
            if s & q == q:  # @line L5
                if qs <= ts:  # @line L6
                    r.append(d)
        return r  # @line L7

    def check_invariant(self) -> None:
        """Raise AssertionError unless each stored signature is the OR of the signatures of its terms."""
        assert len(self.ids) == len(self.sigs) == len(self.terms)
        for s, ts in zip(self.sigs, self.terms):
            assert s == self.signature(ts)
            assert 0 <= s < 1 << self.f


def false_drop_probability(f: int, m: int, d: int) -> float:
    """The exact probability that a one-term query that is not in a document of d distinct terms is a false drop.

    Model: each term sets a uniform random m-subset of the f places,
    independently. By inclusion and exclusion over the m places of the query,
    the result is sum over j of (-1)^j C(m, j) (C(f - j, m) / C(f, m))^d.
    Cost O(m) big-integer operations.
    """
    from fractions import Fraction
    from math import comb

    total = Fraction(0)
    for j in range(m + 1):
        total += (-1) ** j * comb(m, j) * Fraction(comb(f - j, m), comb(f, m)) ** d
    return float(total)
