# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-algorithm-referring-expressions/. The authors are listed in prov/NEB4RM.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from incremental_algorithm_referring_expressions import (
    distinguishes,
    greedy_description,
    make_referring_expression,
    minimal_description,
    rules_out,
)

DOG1 = {"type": "dog", "size": "small", "colour": "black"}
DOG2 = {"type": "dog", "size": "large", "colour": "white"}
CAT3 = {"type": "cat", "size": "small", "colour": "black"}


def test_dale_reiter_example():
    # Section 2.2 and Section 4.4 of the paper (with cat for siamese-cat).
    got = make_referring_expression(DOG1, [DOG2, CAT3], ["type", "colour", "size"])
    assert got == [("type", "dog"), ("colour", "black")]
    got = make_referring_expression(DOG1, [DOG2, CAT3], ["type", "size", "colour"])
    assert got == [("type", "dog"), ("size", "small")]


def test_type_is_added_at_the_end():
    got = make_referring_expression(DOG1, [DOG2], ["colour", "size", "type"])
    assert got == [("colour", "black"), ("type", "dog")]
    # No distractors: the loop stops at the first attribute with only the type.
    assert make_referring_expression(DOG1, [], ["colour"]) == [("type", "dog")]


def test_not_minimal():
    r = {"type": "dog", "colour": "black", "size": "small"}
    x1 = {"type": "cat", "colour": "white", "size": "small"}
    x2 = {"type": "cat", "colour": "black", "size": "large"}
    got = make_referring_expression(r, [x1, x2], ["colour", "size", "type"])
    assert got == [("colour", "black"), ("size", "small"), ("type", "dog")]
    assert minimal_description(r, [x1, x2], ["colour", "size", "type"]) == [("type", "dog")]


def test_k_pairs_against_one():
    # The input of Theorem 4 in the proofs file.
    for k in range(2, 8):
        attrs = ["a%d" % i for i in range(1, k + 1)]
        r = {a: 1 for a in attrs}
        dist = []
        for i in range(1, k):
            x = {a: 1 for a in attrs}
            x["a%d" % i] = 0
            x["a%d" % k] = 0
            dist.append(x)
        y = {a: 1 for a in attrs}
        y["a%d" % k] = 0
        dist.append(y)
        got = make_referring_expression(r, dist, attrs)
        assert got == [(a, 1) for a in attrs]
        assert minimal_description(r, dist, attrs) == [("a%d" % k, 1)]


def set_cover_instance(sets, m):
    """The reduction of Theorem 5: one attribute per set, one distractor per element."""
    attrs = ["s%d" % j for j in range(len(sets))]
    r = {a: 1 for a in attrs}
    dist = [{a: (0 if u in sets[j] else 1) for j, a in enumerate(attrs)} for u in range(m)]
    return r, dist, attrs


def test_set_cover_reduction():
    rng = random.Random(72)
    for _ in range(200):
        m = rng.randint(1, 6)
        sets = [set(u for u in range(m) if rng.random() < 0.4) for _ in range(rng.randint(1, 5))]
        r, dist, attrs = set_cover_instance(sets, m)
        best = None
        for size in range(len(sets) + 1):
            for js in combinations(range(len(sets)), size):
                if set().union(*[sets[j] for j in js]) == set(range(m)):
                    best = size
                    break
            if best is not None:
                break
        desc = minimal_description(r, dist, attrs)
        assert (desc is None) == (best is None)
        if desc is not None:
            assert len(desc) == best


def test_failure():
    twin = dict(DOG1)
    assert make_referring_expression(DOG1, [twin, DOG2], ["type", "colour", "size"]) is None
    assert minimal_description(DOG1, [twin], ["type", "colour", "size"]) is None


def test_unknown_value_is_not_ruled_out():
    x = {"type": "dog"}
    assert rules_out("colour", "black", [x]) == []
    assert make_referring_expression(DOG1, [x], ["colour", "size"]) is None


def replay(r, distractors, preferred):
    """An independent run with sets of indices; returns the pairs or None."""
    left = set(range(len(distractors)))
    pairs = []
    for a in preferred:
        if a in r:
            gone = {i for i in left if a in distractors[i] and distractors[i][a] != r[a]}
            if gone:
                pairs.append((a, r[a]))
                left -= gone
        if not left:
            if "type" in r and not any(p[0] == "type" for p in pairs):
                pairs.append(("type", r["type"]))
            return pairs
    return None


def harmonic(n):
    return sum(Fraction(1, i) for i in range(1, n + 1))


def test_random_against_brute_force():
    rng = random.Random(1995)
    attrs = ["type", "colour", "size", "shape", "material"]
    worse = 0
    for _ in range(800):
        def obj(full):
            o = {}
            for a in attrs:
                if full or rng.random() < 0.85:
                    o[a] = rng.randint(0, 2)
            return o
        r = obj(True)
        dist = [obj(False) for _ in range(rng.randint(0, 6))]
        pref = rng.sample(attrs, rng.randint(1, len(attrs)))
        got = make_referring_expression(r, dist, pref)
        assert got == replay(r, dist, pref)
        best = minimal_description(r, dist, pref + [a for a in attrs if a not in pref])
        best_p = minimal_description(r, dist, pref)
        assert (got is None) == (best_p is None)
        if got is None:
            continue
        assert distinguishes(got, dist)
        assert all(r[a] == v for a, v in got)
        assert len(got) >= len(best)
        if len(got) > len(best):
            worse += 1
        g = greedy_description(r, dist, pref)
        assert g is not None and distinguishes(g, dist)
        # Johnson (1974): greedy set cover is within H(n) of the optimum.
        assert len(g) <= harmonic(len(dist)) * len(best_p) or len(dist) == 0
    # The incremental algorithm is often not minimal.
    assert worse > 50
