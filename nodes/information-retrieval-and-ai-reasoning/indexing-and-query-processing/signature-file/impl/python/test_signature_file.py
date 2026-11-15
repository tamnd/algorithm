# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signature-file/. The authors are listed in prov/WA5X66.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

import irtoy
from signature_file import SignatureFile, false_drop_probability


def toy(f: int = 32, m: int = 2) -> SignatureFile:
    s = SignatureFile(f, m)
    for d, text in irtoy.DOCS.items():
        s.insert(d, irtoy.tokenize(text))
        s.check_invariant()
    return s


def scan(docs: dict, query: list[str]) -> list:
    return [d for d, ts in docs.items() if set(query) <= set(ts)]


def test_worked_example_of_the_page():
    s = toy()
    sig = s.term_signature("sorted")
    assert [p for p in range(32) if sig >> p & 1] == [18, 27]
    assert s.candidates(["sorted"]) == [1, 2, 4, 6, 8]
    assert s.search(["sorted"]) == [1, 2, 4, 8]
    assert s.candidates(["quantum"]) == [5]
    assert s.search(["quantum"]) == []
    q = irtoy.tokenize(irtoy.QUERIES["q2"])
    assert s.candidates(q) == [3, 4]
    assert s.search(q) == []
    assert s.search(irtoy.tokenize(irtoy.QUERIES["q1"])) == [1]


def test_no_false_negatives_on_the_toy_collection():
    s = toy()
    docs = {d: irtoy.tokenize(t) for d, t in irtoy.DOCS.items()}
    vocab = sorted({t for ts in docs.values() for t in ts})
    for t in vocab + ["quantum", "lists", "document"]:
        want = scan(docs, [t])
        assert s.search([t]) == want
        assert set(want) <= set(s.candidates([t]))


def test_edge_cases():
    s = SignatureFile()
    assert s.search(["a"]) == [] and s.candidates([]) == []
    s.insert("e", [])
    s.insert("x", ["a"])
    s.check_invariant()
    # The empty query has the zero signature, which every document covers.
    assert s.search([]) == ["e", "x"]
    assert s.search(["a"]) == ["x"]
    assert s.search(["a", "a"]) == ["x"]
    full = SignatureFile(8, 8)
    full.insert(1, ["p"])
    full.insert(2, ["q"])
    # With m = F every term sets every bit, so every document is a candidate.
    assert full.candidates(["r"]) == [1, 2]
    assert full.search(["r"]) == []
    with pytest.raises(ValueError):
        SignatureFile(4, 5)


def test_term_signature_has_m_bits():
    for f, m in [(1, 1), (7, 3), (64, 4), (100, 7), (16, 16)]:
        s = SignatureFile(f, m, salt=b"k")
        for i in range(200):
            w = s.term_signature("t%d" % i)
            assert bin(w).count("1") == m and w < 1 << f


def test_random_collections_against_a_direct_scan():
    rng = random.Random(84)
    for _ in range(600):
        f = rng.choice([8, 16, 32, 64])
        m = rng.randint(1, 4)
        s = SignatureFile(f, m, salt=bytes([rng.randrange(256)]))
        alphabet = ["w%d" % i for i in range(rng.randint(1, 30))]
        docs = {}
        for d in range(rng.randint(0, 12)):
            docs[d] = rng.sample(alphabet, rng.randint(0, min(8, len(alphabet))))
            s.insert(d, docs[d])
        s.check_invariant()
        for _ in range(5):
            q = rng.sample(alphabet, rng.randint(1, min(3, len(alphabet))))
            want = scan(docs, q)
            assert s.search(q) == want
            assert set(want) <= set(s.candidates(q))


def test_formula_against_full_enumeration():
    # All (C(F, m))^(D+1) choices of the m-subsets, for small F, m and D.
    for f, m, d in [(4, 1, 2), (5, 2, 2), (6, 2, 3), (6, 3, 2)]:
        subsets = [frozenset(c) for c in itertools.combinations(range(f), m)]
        hits = 0
        for doc in itertools.product(subsets, repeat=d):
            union = frozenset().union(*doc)
            hits += sum(1 for q in subsets if q <= union)
        exact = Fraction(hits, len(subsets) ** (d + 1))
        assert math.isclose(false_drop_probability(f, m, d), float(exact), rel_tol=1e-12)


def test_false_drop_rate_matches_the_formula():
    f, m, d, n = 16, 2, 4, 150000
    s = SignatureFile(f, m, salt=b"rate")
    rng = random.Random(1984)
    drops = 0
    for _ in range(n):
        terms = ["d%d" % rng.getrandbits(60) for _ in range(d)]
        q = "q%d" % rng.getrandbits(60)
        doc = s.signature(terms)
        qs = s.term_signature(q)
        drops += doc & qs == qs
        s._cache.clear()
    p = false_drop_probability(f, m, d)
    # Hoeffding: P(|rate - p| >= t) <= 2 exp(-2 n t^2) = delta.
    delta = 1e-6
    t = math.sqrt(math.log(2 / delta) / (2 * n))
    assert abs(drops / n - p) < t
    # The approximation (1 - e^(-m d / F))^m is close to the exact value.
    assert abs((1 - math.exp(-m * d / f)) ** m - p) < 0.005
