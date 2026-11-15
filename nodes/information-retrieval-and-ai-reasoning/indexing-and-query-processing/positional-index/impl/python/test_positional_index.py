# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/positional-index/. The authors are listed in prov/F109TQ.jsonl.

import random

import irtoy
from positional_index import PositionalIndex, build_positional_index


def toy_index() -> PositionalIndex:
    return build_positional_index({d: irtoy.tokenize(t) for d, t in irtoy.DOCS.items()})


def scan_positions(tokens: list[str], term: str) -> list[int]:
    return [i for i, t in enumerate(tokens) if t == term]


def test_example() -> None:
    ix = toy_index()
    assert ix.entries("sorted") == [(1, [7]), (2, [4, 8]), (4, [5]), (8, [1])]
    assert ix.entries("list") == [(3, [9]), (4, [2, 6])]
    assert ix.entries("posting") == [(3, [8]), (4, [1]), (5, [8])]
    assert ix.positions("a", 4) == [0, 4]
    assert ix.positions("a", 2) == []
    assert ix.positions("quantum", 1) == []
    assert ix.postings("array") == [1, 2, 8]
    assert ix.tf("sorted", 2) == 2


def test_irtoy_statistics() -> None:
    ix = toy_index()
    ix.check_invariant()
    terms = ix.terms()
    assert len(terms) == 50
    assert sum(ix.df(t) for t in terms) == 74
    assert sum(ix.cf(t) for t in terms) == 79
    for t in terms:
        assert ix.df(t) == irtoy.df(t)
        assert ix.cf(t) == irtoy.cf(t)
        for d in irtoy.DOCS:
            tokens = irtoy.tokenize(irtoy.DOCS[d])
            assert ix.positions(t, d) == scan_positions(tokens, t)
            assert ix.tf(t, d) == irtoy.tf(t, d)


def test_order_check() -> None:
    ix = PositionalIndex()
    ix.add_document(3, ["a", "b"])
    for bad in (3, 1):
        try:
            ix.add_document(bad, ["a"])
        except ValueError:
            pass
        else:
            raise AssertionError("an id out of order was accepted")
    ix.add_document(7, [])
    ix.add_document(9, ["b", "b", "b"])
    assert ix.entries("b") == [(3, [1]), (9, [0, 1, 2])]
    assert ix.entries("zzz") == []


def test_random_collections() -> None:
    rng = random.Random(1709)
    for _ in range(200):
        vocab = [f"w{i}" for i in range(rng.randint(1, 12))]
        ids = sorted(rng.sample(range(1000), rng.randint(0, 30)))
        docs = {d: [rng.choice(vocab) for _ in range(rng.randint(0, 40))] for d in ids}
        ix = build_positional_index(docs)
        ix.check_invariant()
        total = 0
        for t in vocab:
            expect = [(d, scan_positions(docs[d], t)) for d in ids if t in docs[d]]
            assert ix.entries(t) == expect
            assert ix.postings(t) == [d for d, _ in expect]
            total += ix.cf(t)
            for d in ids:
                assert ix.positions(t, d) == scan_positions(docs[d], t)
        assert total == sum(len(v) for v in docs.values())
