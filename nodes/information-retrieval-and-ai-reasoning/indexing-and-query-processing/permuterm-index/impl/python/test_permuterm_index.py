# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/permuterm-index/. The authors are listed in prov/J3EW3B.jsonl.

import fnmatch
import random
import re

import pytest

import irtoy
from permuterm_index import PermutermIndex, matches, rotations


def scan(vocab, q):
    """The oracle: a direct scan of the vocabulary with fnmatch, checked against a regular expression."""
    by_fn = sorted(t for t in vocab if fnmatch.fnmatchcase(t, q))
    rx = re.compile(".*".join(re.escape(p) for p in q.split("*")))
    assert by_fn == sorted(t for t in vocab if rx.fullmatch(t))
    return by_fn


def build(terms):
    idx = PermutermIndex()
    for t in terms:
        idx.insert(t)
        idx.check_invariant()
    return idx


def test_rotations_of_hello():
    assert rotations("hello") == ["hello$", "ello$h", "llo$he", "lo$hel", "o$hell", "$hello"]


def test_examples_of_manning_raghavan_schuetze():
    idx = build(["man", "moron", "moon", "melon", "fishmonger", "filibuster", "hello"])
    assert idx.wildcard("m*n") == ["man", "melon", "moon", "moron"]
    assert idx.wildcard("hel*") == ["hello"] and idx.wildcard("*llo") == ["hello"]
    assert idx.wildcard("hello") == ["hello"]
    # *mo*er: the key range of er$ holds both terms; the postfilter keeps one.
    assert idx.range_terms("*mo*er") == ["filibuster", "fishmonger"]
    assert idx.wildcard("*mo*er") == ["fishmonger"]


def test_worked_example_on_the_toy_vocabulary():
    vocab = sorted({t for d in irtoy.DOCS for t in irtoy.tokenize(irtoy.DOCS[d])})
    idx = build(vocab)
    assert len(idx) == 50 and len(idx.keys) == 284
    assert idx.wildcard("s*ed") == ["sorted", "speed"]
    assert idx.wildcard("li*t") == ["list"]
    assert idx.wildcard("*ing") == ["encoding", "posting"]
    assert idx.wildcard("in*") == ["in", "index", "into", "inverted"]
    assert idx.range_terms("s*t*d") == ["sorted", "speed"]
    assert idx.wildcard("s*t*d") == ["sorted"]
    lo, hi = idx.prefix_range("ed$s")
    assert idx.keys[lo:hi] == ["ed$sort", "ed$spe"]


def test_one_star_needs_no_postfilter():
    rng = random.Random(11)
    for _ in range(300):
        vocab = {"".join(rng.choice("abc") for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 25))}
        idx = build(vocab)
        for _ in range(10):
            x = "".join(rng.choice("abc") for _ in range(rng.randint(0, 3)))
            y = "".join(rng.choice("abc") for _ in range(rng.randint(0, 3)))
            q = x + "*" + y
            assert idx.range_terms(q) == scan(vocab, q)


def test_edge_cases():
    idx = PermutermIndex()
    assert idx.wildcard("*") == [] and idx.wildcard("a") == [] and idx.wildcard("a*b*c") == []
    idx.insert("")
    idx.insert("a")
    idx.insert("a")
    idx.check_invariant()
    assert len(idx) == 2 and idx.keys == ["$", "$a", "a$"]
    assert idx.wildcard("*") == ["", "a"] and idx.wildcard("") == [""] and idx.wildcard("a*a") == []
    assert idx.wildcard("**") == ["", "a"] and idx.wildcard("*a*") == ["a"]
    idx.delete("b")
    idx.delete("")
    idx.check_invariant()
    assert idx.wildcard("*") == ["a"]
    with pytest.raises(ValueError):
        idx.insert("a$")
    assert matches("abcb", "a*b*b") and not matches("ab", "a*b*b")


def test_random_operations_against_a_scan():
    rng = random.Random(1976)
    needed = 0
    for _ in range(300):
        idx = PermutermIndex()
        model: set[str] = set()
        letters = "ab" if rng.random() < 0.5 else "abcd"
        for _ in range(40):
            r = rng.random()
            if r < 0.5:
                t = "".join(rng.choice(letters) for _ in range(rng.randint(0, 6)))
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
                if "*" in q:
                    cand = idx.range_terms(q)
                    assert set(want) <= set(cand)
                    needed += cand != want
            idx.check_invariant()
            assert sorted(set(idx.owner)) == sorted(model) and len(idx) == len(model)
    # With two or more *, the range alone is often too large.
    assert needed > 50
