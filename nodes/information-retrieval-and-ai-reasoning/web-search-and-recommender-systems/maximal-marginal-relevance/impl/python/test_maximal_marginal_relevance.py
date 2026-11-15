# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-marginal-relevance/. The authors are listed in prov/2ZKYCZ.jsonl.

import math
import random
from collections import Counter

import pytest

import irtoy
from maximal_marginal_relevance import mmr, mmr_steps

TOL = 1e-12
VEC = {d: Counter(irtoy.tokenize(irtoy.DOCS[d])) for d in irtoy.DOCS}


def cosine(a, b):
    dot = sum(a[t] * b[t] for t in a)
    if dot == 0:
        return 0.0
    return dot / math.sqrt(sum(x * x for x in a.values()) * sum(x * x for x in b.values()))


def toy(qid):
    q = Counter(irtoy.tokenize(irtoy.QUERIES[qid]))
    rel = {d: cosine(q, VEC[d]) for d in VEC}
    cands = [d for d in VEC if rel[d] > 0]
    return cands, rel, lambda i, j: cosine(VEC[i], VEC[j])


def direct(candidates, rel, sim, lam, k):
    """The formula of Carbonell and Goldstein, with the maximum over S recomputed at every step."""
    s, out = [], []
    rest = sorted(set(candidates))
    while rest and len(s) < k:
        scores = {}
        for d in rest:
            penalty = max((sim(d, j) for j in s), default=0.0)
            scores[d] = lam * rel[d] - (1 - lam) * penalty
        top = max(scores.values())
        pick = min(d for d in rest if scores[d] == top)
        out.append((pick, top, scores))
        s.append(pick)
        rest.remove(pick)
    return out


def assert_same(got, want):
    assert [d for d, _ in got] == [d for d, _, _ in want]
    for (d, score), (_, top, _) in zip(got, want):
        assert math.isclose(score, top, rel_tol=TOL, abs_tol=TOL)


def test_example_of_the_page():
    cands, rel, sim = toy("q2")
    assert cands == [2, 3, 4, 5]
    assert mmr(cands, rel, sim, 1.0, 3) == [4, 3, 5]
    assert mmr(cands, rel, sim, 0.7, 3) == [4, 5, 3]
    assert mmr(cands, rel, sim, 0.5, 3) == [4, 5, 2]
    steps = mmr_steps(cands, rel, sim, 0.7, 3)
    assert math.isclose(steps[0][1], 0.7 * rel[4], rel_tol=TOL)
    assert math.isclose(steps[1][1], 0.7 * rel[5] - 0.3 * sim(5, 4), rel_tol=TOL)


@pytest.mark.parametrize("qid", ["q1", "q2", "q3"])
@pytest.mark.parametrize("lam", [0.0, 0.3, 0.5, 0.7, 1.0])
def test_toy_matches_the_formula(qid, lam):
    cands, rel, sim = toy(qid)
    for k in range(len(cands) + 2):
        assert_same(mmr_steps(cands, rel, sim, lam, k), direct(cands, rel, sim, lam, k))


@pytest.mark.parametrize("seed", range(200))
def test_random_instances_match_the_formula(seed):
    rng = random.Random(seed)
    n = rng.randint(1, 12)
    coarse = seed % 2 == 0  # values on a grid of 0.25 force many ties
    val = (lambda: rng.randint(0, 4) / 4) if coarse else rng.random
    ids = rng.sample(range(100), n)
    rel = {d: val() for d in ids}
    m = {}
    for a in ids:
        for b in ids:
            if a < b:
                m[a, b] = m[b, a] = val()
    sim = lambda i, j: m[i, j]
    lam = rng.choice([0.0, 0.25, 0.5, 0.75, 1.0, rng.random()])
    k = rng.randint(0, n + 1)
    assert_same(mmr_steps(ids, rel, sim, lam, k), direct(ids, rel, sim, lam, k))


def test_lambda_one_is_ranking_by_relevance():
    rng = random.Random(7)
    ids = list(range(10))
    rel = {d: rng.random() for d in ids}
    order = sorted(ids, key=lambda d: (-rel[d], d))
    assert mmr(ids, rel, lambda i, j: rng.random(), 1.0, 10) == order


def test_rejects_bad_lambda():
    with pytest.raises(ValueError):
        mmr([1], {1: 1.0}, lambda i, j: 0.0, 1.5, 1)
