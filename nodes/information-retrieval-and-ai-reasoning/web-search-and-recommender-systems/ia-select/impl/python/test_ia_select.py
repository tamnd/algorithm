# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ia-select/. The authors are listed in prov/PXB2Y2.jsonl.

import math
import random

import pytest

from ia_select import best_subset, ia_select, ia_select_steps, objective

TOL = 1e-12
RATIO = 1.0 - 1.0 / math.e

# Table 1 of Agrawal et al. (2009): no single ordering is optimal for every k.
P_TABLE1 = {"c1": 0.5, "c2": 0.5}
V_TABLE1 = {1: {"c1": 0.8, "c2": 0.8}, 2: {"c1": 1.0}, 3: {"c2": 1.0}}


def random_instance(rng, n, m, single=False):
    weights = [rng.random() + 0.01 for _ in range(m)]
    total = sum(weights)
    p_cat = {f"c{i}": w / total for i, w in enumerate(weights)}
    value = {}
    for d in range(1, n + 1):
        cats = list(p_cat)
        if single:
            chosen = [rng.choice(cats)]
        else:
            chosen = [c for c in cats if rng.random() < 0.6] or [rng.choice(cats)]
        value[d] = {c: rng.choice([rng.random(), 1.0, 0.5]) for c in chosen}
    return p_cat, value


def test_greedy_is_not_optimal_on_table_1():
    docs = [1, 2, 3]
    assert ia_select(docs, P_TABLE1, V_TABLE1, 1) == [1]
    greedy = ia_select(docs, P_TABLE1, V_TABLE1, 2)
    assert greedy == [1, 2]
    g = objective(greedy, P_TABLE1, V_TABLE1)
    opt, best = best_subset(docs, P_TABLE1, V_TABLE1, 2)
    assert opt == [2, 3]
    assert math.isclose(g, 0.9, rel_tol=TOL) and math.isclose(best, 1.0, rel_tol=TOL)
    assert g >= RATIO * best


def test_gain_is_the_exact_marginal_gain():
    rng = random.Random(5)
    for _ in range(50):
        p_cat, value = random_instance(rng, rng.randint(1, 9), rng.randint(1, 5))
        docs = list(value)
        prefix = []
        for d, gain in ia_select_steps(docs, p_cat, value, len(docs)):
            before = objective(prefix, p_cat, value)
            prefix.append(d)
            assert math.isclose(gain, objective(prefix, p_cat, value) - before, rel_tol=1e-9, abs_tol=1e-12)
            # The pick maximizes the marginal gain over the remaining documents.
            others = [x for x in docs if x not in prefix]
            for x in others:
                alt = objective(prefix[:-1] + [x], p_cat, value) - before
                assert alt <= gain + 1e-12


@pytest.mark.parametrize("seed", range(150))
def test_at_least_one_minus_one_over_e_of_brute_force(seed):
    rng = random.Random(seed)
    n = rng.randint(1, 9)
    p_cat, value = random_instance(rng, n, rng.randint(1, 5))
    docs = list(value)
    for k in range(0, n + 1):
        greedy = ia_select(docs, p_cat, value, k)
        assert len(greedy) == min(k, n) and len(set(greedy)) == len(greedy)
        g = objective(greedy, p_cat, value)
        _, best = best_subset(docs, p_cat, value, k)
        assert g <= best + TOL
        assert g >= RATIO * best - TOL


@pytest.mark.parametrize("seed", range(60))
def test_optimal_when_each_document_has_one_category(seed):
    rng = random.Random(1000 + seed)
    n = rng.randint(1, 9)
    p_cat, value = random_instance(rng, n, rng.randint(1, 4), single=True)
    docs = list(value)
    for k in range(0, n + 1):
        g = objective(ia_select(docs, p_cat, value, k), p_cat, value)
        _, best = best_subset(docs, p_cat, value, k)
        assert math.isclose(g, best, rel_tol=1e-9, abs_tol=TOL)


def test_random_search_finds_non_optimal_instances():
    rng = random.Random(42)
    gaps = 0
    worst = 1.0
    for _ in range(300):
        p_cat, value = random_instance(rng, 6, 3)
        docs = list(value)
        g = objective(ia_select(docs, p_cat, value, 2), p_cat, value)
        _, best = best_subset(docs, p_cat, value, 2)
        if g < best - 1e-9:
            gaps += 1
            worst = min(worst, g / best)
    assert gaps > 0 and worst >= RATIO


def test_rejects_bad_values():
    with pytest.raises(ValueError):
        ia_select([1], {"c": 1.0}, {1: {"c": 1.5}}, 1)
    with pytest.raises(ValueError):
        ia_select([1], {"c": 1.0}, {1: {"x": 0.5}}, 1)
