# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rope/. The authors are listed in prov/K8GJQ9.jsonl.

import random

import pytest

from rope import Rope


def test_example() -> None:
    r = Rope("the_quick_fox_jumps", leaf_max=4)
    r.check_invariant()
    assert r.leaf_count() == 5 and r.height() == 3
    assert r.char_at(10) == "f"
    a, b = r.split(10)
    assert (a.to_string(), b.to_string()) == ("the_quick_", "fox_jumps")
    r2 = r.insert(10, "brown_")
    r2.check_invariant()
    assert r2.to_string() == "the_quick_brown_fox_jumps"
    assert r.to_string() == "the_quick_fox_jumps"  # the old version is unchanged
    r3 = r2.delete(4, 10)
    assert r3.to_string() == "the_brown_fox_jumps"
    r3.check_invariant()


def test_edges() -> None:
    e = Rope()
    assert len(e) == 0 and e.to_string() == "" and e.height() == -1
    assert e.concat(e).to_string() == ""
    assert e.insert(0, "abc").to_string() == "abc"
    r = Rope("abc", leaf_max=1)
    assert r.delete(0, 3).to_string() == ""
    x, y = r.split(0)
    assert x.to_string() == "" and y.to_string() == "abc"
    with pytest.raises(IndexError):
        r.char_at(3)
    with pytest.raises(IndexError):
        r.split(4)


def test_long_concat_chain_stays_balanced() -> None:
    r = Rope(leaf_max=2)
    for k in range(2000):
        r = r.concat(Rope("ab"[k % 2] * 3, leaf_max=2))
    r.check_invariant()
    assert len(r) == 6000 and r.height() <= 1.45 * 12 + 2


def test_random_against_string() -> None:
    rng = random.Random(9090)
    for _ in range(500):
        leaf = rng.randint(1, 5)
        model = "".join(rng.choice("abc") for _ in range(rng.randint(0, 20)))
        r = Rope(model, leaf_max=leaf)
        for _ in range(rng.randint(0, 25)):
            op = rng.random()
            if op < 0.4:
                i = rng.randint(0, len(model))
                s = "".join(rng.choice("xyz") for _ in range(rng.randint(0, 6)))
                r, model = r.insert(i, s), model[:i] + s + model[i:]
            elif op < 0.7:
                i = rng.randint(0, len(model))
                j = rng.randint(i, len(model))
                r, model = r.delete(i, j), model[:i] + model[j:]
            else:
                other = "".join(rng.choice("pq") for _ in range(rng.randint(0, 8)))
                r, model = r.concat(Rope(other, leaf_max=leaf)), model + other
            r.check_invariant()
        assert r.to_string() == model and len(r) == len(model)
        if model:
            i = rng.randrange(len(model))
            assert r.char_at(i) == model[i]
            j = rng.randint(i, len(model))
            assert r.substring(i, j) == model[i:j]
