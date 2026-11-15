# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-gram-index/. The authors are listed in prov/HHWFE5.jsonl.

import fnmatch
import random
import re

import pytest

import irtoy
from k_gram_index import KGramIndex, grams, matches


def scan(vocab, q):
    """The oracle: a direct scan of the vocabulary with fnmatch, checked against a regular expression."""
    by_fn = sorted(t for t in vocab if fnmatch.fnmatchcase(t, q))
    rx = re.compile(".*".join(re.escape(p) for p in q.split("*")))
    by_re = sorted(t for t in vocab if rx.fullmatch(t))
    assert by_fn == by_re
    return by_fn


def toy_index(k=3):
    vocab = sorted({t for d in irtoy.DOCS for t in irtoy.tokenize(irtoy.DOCS[d])})
    idx = KGramIndex(k)
    for t in vocab:
        idx.insert(t)
    idx.check_invariant()
    return idx, vocab


def test_grams_of_castle():
    assert grams("$castle$", 3) == ["$ca", "cas", "ast", "stl", "tle", "le$"]


def test_examples_of_manning_raghavan_schuetze():
    idx = KGramIndex(3)
    for t in ["beetroot", "metric", "petrify", "retrieval", "relive", "remove", "retrieve", "retired", "red", "reduce"]:
        idx.insert(t)
        idx.check_invariant()
    assert idx.postings["etr"] == ["beetroot", "metric", "petrify", "retrieval", "retrieve"]
    assert idx.wildcard("re*ve") == ["relive", "remove", "retrieve"]
    # red* has the grams $re and red, and so has retired: the postfilter removes it.
    assert idx.query_grams("red*") == ["$re", "red"]
    assert idx.candidates("red*") == ["red", "reduce", "retired"]
    assert idx.wildcard("red*") == ["red", "reduce"]


def test_worked_example_on_the_toy_vocabulary():
    idx, vocab = toy_index()
    assert len(vocab) == 50 and len(idx.postings) == 192
    assert sum(len(v) for v in idx.postings.values()) == 234
    assert idx.query_grams("s*ed") == ["ed$"]
    assert idx.candidates("s*ed") == ["compressed", "expected", "inverted", "sorted", "speed"]
    assert idx.wildcard("s*ed") == ["sorted", "speed"]
    assert idx.query_grams("li*t") == ["$li"]
    assert idx.candidates("li*t") == ["list", "lists"]
    assert idx.wildcard("li*t") == ["list"]
    assert idx.wildcard("*ing") == ["encoding", "posting"]
    assert idx.wildcard("se*ch") == ["search"]
    assert idx.wildcard("*or*") == ["for", "score", "sort", "sorted"]


def test_sequence_of_operations():
    idx = KGramIndex(3)
    for t in ["list", "lists", "sort", "sorted", "speed"]:
        idx.insert(t)
        idx.check_invariant()
    assert idx.postings["$li"] == ["list", "lists"]
    assert idx.wildcard("li*t") == ["list"]
    assert idx.wildcard("s*ed") == ["sorted", "speed"]
    idx.delete("lists")
    idx.check_invariant()
    assert "ts$" not in idx.postings
    assert idx.wildcard("li*") == ["list"]


def test_edge_cases():
    idx = KGramIndex(3)
    assert idx.wildcard("*") == [] and idx.wildcard("a") == []
    idx.insert("a")
    idx.insert("a")
    idx.check_invariant()
    assert len(idx) == 1 and idx.postings == {"$a$": ["a"]}
    assert idx.wildcard("*") == ["a"] and idx.wildcard("a") == ["a"] and idx.wildcard("a*a") == []
    assert idx.wildcard("**a**") == ["a"]
    idx.delete("b")
    idx.delete("a")
    idx.check_invariant()
    assert idx.postings == {} and idx.wildcard("*") == []
    for bad in ["", "a$", "a*"]:
        with pytest.raises(ValueError):
            idx.insert(bad)
    with pytest.raises(ValueError):
        KGramIndex(0)


def test_matches():
    assert matches("sorted", "s*ed") and not matches("sed", "se*ed") and matches("seed", "se*ed")
    assert matches("abab", "a*b*b") and not matches("aba", "ab*ba") and matches("abba", "ab*ba*")
    assert matches("abcb", "a*b*b") and not matches("ab", "a*b*b")
    assert matches("x", "*") and matches("", "*") and not matches("x", "")


def test_random_operations_against_a_scan():
    rng = random.Random(3)
    needed = 0
    for _ in range(300):
        k = rng.randint(1, 4)
        idx = KGramIndex(k)
        model: set[str] = set()
        letters = "ab" if rng.random() < 0.5 else "abcd"
        for _ in range(40):
            r = rng.random()
            if r < 0.5:
                t = "".join(rng.choice(letters) for _ in range(rng.randint(1, 6)))
                idx.insert(t)
                model.add(t)
            elif r < 0.65 and model:
                t = rng.choice(sorted(model))
                idx.delete(t)
                model.discard(t)
            else:
                pieces = ["".join(rng.choice(letters) for _ in range(rng.randint(0, 3))) for _ in range(rng.randint(1, 4))]
                q = "*".join(pieces)
                want = scan(model, q)
                assert idx.wildcard(q) == want
                cand = idx.candidates(q)
                assert set(want) <= set(cand)
                needed += cand != want
            idx.check_invariant()
            assert idx.terms == sorted(model)
    # The postfilter is needed: many queries have candidates that do not match.
    assert needed > 100
