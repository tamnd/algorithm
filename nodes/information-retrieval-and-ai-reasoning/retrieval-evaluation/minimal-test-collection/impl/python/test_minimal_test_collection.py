# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimal-test-collection/. The authors are listed in prov/19JM8C.jsonl.

import itertools
import random
from fractions import Fraction

from irtoy import QRELS, RUN
from minimal_test_collection import bounds, coefficients, minimal_test_collection, weights


def average_precision(ranking, rel, r_total):
    if r_total == 0:
        return Fraction(0)
    hits = 0
    s = Fraction(0)
    for k, d in enumerate(ranking, 1):
        if rel.get(d, 0):
            hits += 1
            s += Fraction(hits, k)
    return s / r_total


def d_value(c, x):
    return sum(v * x[i] * x[j] for (i, j), v in c.items())


def completions(docs, judged):
    free = [d for d in docs if d not in judged]
    for bits in itertools.product((0, 1), repeat=len(free)):
        x = dict(judged)
        x.update(zip(free, bits))
        yield x


def sign(v):
    return (v > 0) - (v < 0)


def random_case(rng, n_max):
    n = rng.randint(1, n_max)
    universe = list(range(1, n + 3))
    a = rng.sample(universe, rng.randint(1, n))
    b = rng.sample(universe, rng.randint(1, n))
    rel = {d: rng.randint(0, 1) for d in universe}
    return a, b, rel


def test_toy_collection_two_tie_orders():
    rel = {d: 1 for d in QRELS["q1"]}
    scores = RUN["q1"]
    a = sorted(scores, key=lambda d: -scores[d])  # stable: 1, 6, 8, 2, 4
    b = sorted(scores, key=lambda d: (-scores[d], -d))  # ties by reverse id: 6, 1, 8, 4, 2
    assert a == [1, 6, 8, 2, 4] and b == [6, 1, 8, 4, 2]
    r_total = len(rel)
    assert average_precision(a, rel, r_total) == Fraction(29, 36)
    assert average_precision(b, rel, r_total) == Fraction(53, 90)
    s, order = minimal_test_collection(a, b, lambda d: rel.get(d, 0))
    assert s == 1 and order == [1, 6]
    docs, c = coefficients(a, b)
    assert bounds(c, {}) == (Fraction(-7, 10), Fraction(7, 10))
    assert weights(docs, c, {}, 1) == (Fraction(1, 2), Fraction(1, 20), 0, Fraction(11, 20))
    assert weights(docs, c, {}, 6) == (0, Fraction(11, 20), Fraction(1, 2), Fraction(1, 20))
    assert bounds(c, {1: 1}) == (Fraction(-1, 5), Fraction(7, 10))
    lo, hi = bounds(c, {1: 1, 6: 0})
    assert (lo, hi) == (Fraction(7, 20), Fraction(13, 20))
    vals = [d_value(c, x) for x in completions(docs, {1: 1, 6: 0})]
    assert min(vals) == lo and max(vals) == hi
    assert r_total * (average_precision(a, rel, r_total) - average_precision(b, rel, r_total)) == Fraction(13, 20)


def test_quadratic_form_is_r_times_delta_ap():
    rng = random.Random(1)
    for _ in range(500):
        a, b, rel = random_case(rng, 6)
        docs, c = coefficients(a, b)
        r_total = sum(rel.values())
        lhs = r_total * (average_precision(a, rel, r_total) - average_precision(b, rel, r_total))
        assert lhs == d_value(c, {d: rel[d] for d in docs})


def test_bounds_are_sound():
    rng = random.Random(2)
    for _ in range(400):
        a, b, rel = random_case(rng, 6)
        docs, c = coefficients(a, b)
        judged = {d: rel[d] for d in docs if rng.random() < 0.4}
        lo, hi = bounds(c, judged)
        vals = [d_value(c, x) for x in completions(docs, judged)]
        assert lo <= min(vals) and max(vals) <= hi


def test_weights_match_recomputed_bounds():
    rng = random.Random(3)
    for _ in range(300):
        a, b, rel = random_case(rng, 6)
        docs, c = coefficients(a, b)
        judged = {d: rel[d] for d in docs if rng.random() < 0.3}
        lo, hi = bounds(c, judged)
        for i in docs:
            if i in judged:
                continue
            w_r, w_n, v_r, v_n = weights(docs, c, judged, i)
            lo1, hi1 = bounds(c, {**judged, i: 1})
            lo0, hi0 = bounds(c, {**judged, i: 0})
            assert (w_r, w_n, v_r, v_n) == (lo1 - lo, lo0 - lo, hi - hi1, hi - hi0)
            assert min(w_r, w_n, v_r, v_n) >= 0


def test_judgments_decide_the_sign_against_brute_force():
    rng = random.Random(4)
    saved = 0
    for _ in range(600):
        a, b, rel = random_case(rng, 7)
        s, order = minimal_test_collection(a, b, lambda d: rel[d])
        docs, c = coefficients(a, b)
        assert len(order) == len(set(order)) <= len(docs)
        saved += len(docs) - len(order)
        judged = {d: rel[d] for d in order}
        for x in completions(docs, judged):
            assert sign(d_value(c, x)) == s
            full = rel.copy()
            full.update(x)
            r_total = sum(full.values())
            delta = average_precision(a, full, r_total) - average_precision(b, full, r_total)
            assert sign(delta) == s
    assert saved > 0


def test_stop_rule_is_sufficient_not_necessary():
    a, b = [3, 2, 4, 1], [3, 4, 1, 2]
    docs, c = coefficients(a, b)
    judged = {2: 1, 4: 1, 1: 0}
    vals = [d_value(c, x) for x in completions(docs, judged)]
    assert sorted(vals) == [Fraction(1, 6), Fraction(1, 4)]
    assert bounds(c, judged) == (0, Fraction(5, 12))


def test_edge_cases():
    same = [3, 1, 2]
    assert minimal_test_collection(same, same, lambda d: 1) == (0, [])
    s, order = minimal_test_collection([1], [2], lambda d: 1)
    assert s == 0 and sorted(order) == [1, 2]
    s, order = minimal_test_collection([1], [2], lambda d: int(d == 1))
    assert s == 1
    assert minimal_test_collection([1, 2], [2, 1], lambda d: 1, budget=0) == (None, [])
    s, order = minimal_test_collection([1, 2], [2, 1], lambda d: int(d == 2), budget=1)
    assert s is None and len(order) == 1
