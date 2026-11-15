# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rocchio-algorithm/. The authors are listed in prov/SMAEPR.jsonl.

import math
import random
from fractions import Fraction

import irtoy
from rocchio_algorithm import centroid, rocchio, top_terms

STOP = {"a", "an", "the", "in", "of", "is", "by", "for", "with", "to", "into", "up", "each"}


def tf_vector(d, stop=frozenset()):
    v = {}
    for t in irtoy.tokenize(irtoy.DOCS[d]):
        if t not in stop:
            v[t] = v.get(t, 0) + 1
    return v


def query_vector(q):
    return {t: 1 for t in irtoy.tokenize(irtoy.QUERIES[q])}


def dot(a, b):
    return sum(w * b.get(t, 0) for t, w in a.items())


def cosine(a, b):
    na, nb = math.sqrt(dot(a, a)), math.sqrt(dot(b, b))
    return dot(a, b) / (na * nb) if na and nb else 0.0


def rank(q, stop=frozenset()):
    s = {d: cosine(q, tf_vector(d, stop)) for d in irtoy.DOCS}
    return sorted(s, key=lambda d: (-s[d], d)), s


def random_vector(rng, terms):
    return {t: Fraction(rng.randint(0, 4)) for t in rng.sample(terms, rng.randint(1, len(terms)))}


def test_matches_the_formula_exactly():
    rng = random.Random(1)
    terms = list("abcdefgh")
    for _ in range(300):
        q = random_vector(rng, terms)
        rel = [random_vector(rng, terms) for _ in range(rng.randint(0, 4))]
        non = [random_vector(rng, terms) for _ in range(rng.randint(0, 4))]
        al, be, ga = Fraction(1), Fraction(3, 4), Fraction(3, 20)
        for clamp in (False, True):
            got = rocchio(q, rel, non, al, be, ga, clamp)
            for t in terms:
                want = al * q.get(t, 0)
                if rel:
                    want += be * sum(d.get(t, 0) for d in rel) / len(rel)
                if non:
                    want -= ga * sum(d.get(t, 0) for d in non) / len(non)
                if clamp:
                    assert got.get(t, 0) == max(want, 0)
                    assert all(w > 0 for w in got.values())
                elif t in got:
                    assert got[t] == want
                else:
                    assert want == 0


def test_centroid_difference_is_the_optimal_unit_query():
    rng = random.Random(2)
    dim = 5
    for _ in range(100):

        def unit():
            v = [rng.gauss(0, 1) for _ in range(dim)]
            n = math.sqrt(sum(x * x for x in v))
            return {i: x / n for i, x in enumerate(v)}

        rel = [unit() for _ in range(rng.randint(1, 4))]
        non = [unit() for _ in range(rng.randint(1, 4))]

        def objective(q):
            return sum(dot(q, d) for d in rel) / len(rel) - sum(dot(q, d) for d in non) / len(non)

        diff = rocchio({}, rel, non, alpha=0.0, beta=1.0, gamma=1.0, clamp=False)
        norm = math.sqrt(dot(diff, diff))
        q_opt = {t: w / norm for t, w in diff.items()}
        best = objective(q_opt)
        assert abs(best - norm) < 1e-9
        for _ in range(50):
            assert objective(unit()) <= best + 1e-12


def test_empty_feedback_keeps_the_scaled_query():
    q = {"x": 2.0, "y": 1.0}
    assert rocchio(q, [], []) == q
    assert rocchio(q, [], [], alpha=0.5) == {"x": 1.0, "y": 0.5}
    assert centroid([{"x": 1.0}, {"y": 3.0}]) == {"x": 0.5, "y": 1.5}


def test_toy_feedback_on_q1():
    q = query_vector("q1")
    d1, d6 = tf_vector(1), tf_vector(6)
    new = rocchio(q, [d1], [d6])
    want = {"sorted": 1.75, "array": 1.75, "search": 1.75, "a": 1.2, "binary": 0.75, "finds": 0.6, "in": 0.6, "key": 0.6}
    assert new.keys() == want.keys()
    for t in want:
        assert abs(new[t] - want[t]) < 1e-12
    before, _ = rank(q)
    after, s = rank(new)
    assert before == [1, 2, 8, 7, 4, 3, 5, 6]
    # The nonrelevant d6 shares "a", "finds", "key" and "in" with d1 and climbs to rank 3.
    assert after == [1, 2, 6, 4, 8, 7, 3, 5]
    assert abs(s[1] - 0.8780) < 1e-4 and abs(s[6] - 0.3461) < 1e-4


def test_toy_feedback_on_q1_without_stop_words():
    q = query_vector("q1")
    new = rocchio(q, [tf_vector(1, STOP)], [tf_vector(6, STOP)])
    want = {"sorted": 1.75, "array": 1.75, "search": 1.75, "binary": 0.75, "finds": 0.6, "key": 0.6}
    assert new.keys() == want.keys()
    after, s = rank(new, STOP)
    assert after == [1, 2, 8, 7, 4, 6, 3, 5]
    assert top_terms(new, 3) == {"array": 1.75, "search": 1.75, "sorted": 1.75}
