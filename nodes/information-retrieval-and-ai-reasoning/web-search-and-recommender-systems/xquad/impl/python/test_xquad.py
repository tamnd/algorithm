# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xquad/. The authors are listed in prov/ZHZBK5.jsonl.

import math
import random

import pytest

from xquad import xquad, xquad_steps

TOL = 1e-12

# The example of the page: "jaguar" with a car aspect and an animal aspect.
REL = {1: 0.9, 2: 0.8, 3: 0.6, 4: 0.5}
ASPECTS = {"car": 0.6, "animal": 0.4}
COVER = {1: {"car": 0.9}, 2: {"car": 0.8}, 3: {"animal": 0.7}, 4: {"car": 0.3, "animal": 0.3}}


def direct_steps(docs, rel, p_aspect, cover, lam, k):
    """Equation 5 of Santos et al., with the product over S recomputed from scratch."""
    chosen = []
    rest = sorted(docs)
    while rest and len(chosen) < k:
        scores = {}
        for d in rest:
            div = 0.0
            for a, p in p_aspect.items():
                miss = 1.0
                for s, _ in chosen:
                    miss *= 1.0 - cover.get(s, {}).get(a, 0.0)
                div += p * cover.get(d, {}).get(a, 0.0) * miss
            scores[d] = (1.0 - lam) * rel[d] + lam * div
        top = max(scores.values())
        best = min(d for d in rest if scores[d] == top)
        chosen.append((best, scores[best]))
        rest.remove(best)
    return chosen


def coverage(selected, p_aspect, cover):
    total = 0.0
    for a, p in p_aspect.items():
        miss = 1.0
        for d in selected:
            miss *= 1.0 - cover.get(d, {}).get(a, 0.0)
        total += p * (1.0 - miss)
    return total


def random_instance(rng, grid):
    n = rng.randint(1, 10)
    m = rng.randint(1, 4)
    pick = (lambda: rng.choice([0.0, 0.25, 0.5, 0.75, 1.0])) if grid else rng.random
    weights = [rng.random() + 0.01 for _ in range(m)]
    p_aspect = {f"a{i}": w / sum(weights) for i, w in enumerate(weights)}
    rel = {d: pick() for d in range(1, n + 1)}
    cover = {}
    for d in rel:
        cover[d] = {a: pick() for a in p_aspect if rng.random() < 0.6}
    lam = rng.choice([0.0, 0.25, 0.5, 0.75, 1.0]) if grid else rng.random()
    return list(rel), rel, p_aspect, cover, lam


def same_steps(a, b):
    assert [d for d, _ in a] == [d for d, _ in b]
    for (_, x), (_, y) in zip(a, b):
        assert math.isclose(x, y, rel_tol=1e-9, abs_tol=TOL)


def test_example_lambda_zero_is_relevance_order():
    assert xquad(list(REL), REL, ASPECTS, COVER, 0.0, 4) == [1, 2, 3, 4]


def test_example_lambda_half():
    steps = xquad_steps(list(REL), REL, ASPECTS, COVER, 0.5, 4)
    assert [d for d, _ in steps] == [1, 3, 2, 4]
    for (_, got), want in zip(steps, [0.72, 0.44, 0.424, 0.2698]):
        assert math.isclose(got, want, rel_tol=1e-9)


def test_example_lambda_one():
    steps = xquad_steps(list(REL), REL, ASPECTS, COVER, 1.0, 4)
    assert [d for d, _ in steps] == [1, 3, 4, 2]
    for (_, got), want in zip(steps, [0.54, 0.28, 0.054, 0.0336]):
        assert math.isclose(got, want, rel_tol=1e-9)


@pytest.mark.parametrize("seed", range(200))
def test_matches_direct_formula_step_by_step(seed):
    rng = random.Random(seed)
    docs, rel, p_aspect, cover, lam = random_instance(rng, grid=seed % 2 == 0)
    k = rng.randint(0, len(docs) + 1)
    same_steps(xquad_steps(docs, rel, p_aspect, cover, lam, k), direct_steps(docs, rel, p_aspect, cover, lam, k))


@pytest.mark.parametrize("seed", range(50))
def test_lambda_one_is_greedy_on_coverage(seed):
    rng = random.Random(500 + seed)
    docs, rel, p_aspect, cover, _ = random_instance(rng, grid=False)
    prefix = []
    for d, score in xquad_steps(docs, rel, p_aspect, cover, 1.0, len(docs)):
        before = coverage(prefix, p_aspect, cover)
        gains = {x: coverage(prefix + [x], p_aspect, cover) - before for x in docs if x not in prefix}
        assert math.isclose(score, gains[d], rel_tol=1e-9, abs_tol=TOL)
        assert all(g <= score + TOL for g in gains.values())
        prefix.append(d)


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        xquad([1], {1: 0.5}, {"a": 1.0}, {1: {"a": 0.5}}, 1.5, 1)
    with pytest.raises(ValueError):
        xquad([1], {1: 0.5}, {"a": 1.0}, {1: {"b": 0.5}}, 0.5, 1)
    with pytest.raises(ValueError):
        xquad([1], {}, {"a": 1.0}, {}, 0.5, 1)
