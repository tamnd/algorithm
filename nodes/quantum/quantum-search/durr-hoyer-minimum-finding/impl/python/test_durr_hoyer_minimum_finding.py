# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/durr-hoyer-minimum-finding/. The authors are listed in prov/5EDMDS.jsonl.

import math
import random
from fractions import Fraction

from durr_hoyer_minimum_finding import (
    default_budget,
    durr_hoyer_minimum,
    expected_bound,
    expected_queries,
    grover_state,
    num_choices,
    next_m,
    phase_cost,
    round_success,
)
from qsim import probabilities

TOL = 1e-9
EXAMPLE = [52, 17, 93, 41, 8, 66, 30, 75, 23, 88, 5, 61, 47, 12, 99, 36]


def random_table(rng: random.Random, n_items: int, distinct: bool) -> list[int]:
    if distinct:
        return rng.sample(range(10 * n_items), n_items)
    return [rng.randrange(max(2, n_items // 4)) for _ in range(n_items)]


def test_grover_state_is_uniform_on_the_marked_items() -> None:
    # The proof needs a measured improvement to be uniform among all
    # items below the threshold, with total probability sin^2((2j+1) theta).
    rng = random.Random(1)
    for n_items in (5, 8, 13, 16):
        table = random_table(rng, n_items, distinct=False)
        for y in range(n_items):
            marked = [x for x in range(n_items) if table[x] < table[y]]
            t = len(marked)
            theta = math.asin(math.sqrt(t / n_items))
            for j in range(5):
                probs = probabilities(grover_state(table, y, j))
                total = sum(probs[x] for x in marked)
                assert abs(total - math.sin((2 * j + 1) * theta) ** 2) < TOL
                for x in marked:
                    assert abs(probs[x] - total / t) < TOL


def test_round_success_closed_form() -> None:
    for n_items in (4, 9, 16, 30):
        table = list(range(n_items))
        for t in range(1, n_items):
            y = t  # exactly t values are below table[t]
            for c in range(1, 7):
                avg = sum(sum(probabilities(grover_state(table, y, j))[:t]) for j in range(c)) / c
                assert abs(avg - round_success(c, n_items, t)) < TOL


def test_rounds_succeed_with_one_quarter_above_three_quarters() -> None:
    # Claim 2 of the proof: t > 3N/4 gives P_c >= 1/4 for every c.
    for n_items in range(2, 65):
        for t in range(1, n_items):
            if 4 * t <= 3 * n_items:
                continue
            for c in range(1, math.isqrt(n_items - 1) + 2):
                assert round_success(c, n_items, t) >= 0.25 - TOL


def test_phase_cost_bounds() -> None:
    # Claim 3: one phase with t marked items costs at most
    # 9 sqrt(N/t) iterations and log_{6/5} sqrt(N) + 5 rounds.
    for n_items in range(2, 65):
        log_term = math.log(math.sqrt(n_items)) / math.log(1.2) + 5
        for t in range(1, n_items):
            iters, rounds = phase_cost(n_items, t)
            if 4 * t > 3 * n_items:
                assert iters < 5 and rounds <= 4
            assert iters < 9 * math.sqrt(n_items / t)
            assert rounds < log_term


def test_expected_queries_below_the_bound() -> None:
    rng = random.Random(2)
    for n_items in range(1, 65):
        assert expected_queries([1] * n_items) <= expected_bound(n_items)
        for _ in range(3):
            table = random_table(rng, n_items, distinct=False)
            values = sorted(set(table))
            counts = [table.count(v) for v in values]
            assert expected_queries(counts) <= expected_bound(n_items)


def test_expected_queries_values_of_the_page() -> None:
    rows = [(16, 9.1), (64, 20.6), (256, 44.6), (1024, 92.9)]
    for n_items, want in rows:
        assert abs(expected_queries([1] * n_items) - want) < 0.05
    assert default_budget(16) == 216
    assert default_budget(1024) == 1487


def test_example_run() -> None:
    y, used, thresholds = durr_hoyer_minimum(EXAMPLE, random.Random(6), target=5)
    assert (y, used) == (10, 13)
    assert [EXAMPLE[i] for i in thresholds] == [93, 47, 36, 8, 5]
    y, used, _ = durr_hoyer_minimum(EXAMPLE, random.Random(6))
    assert y == 10
    assert default_budget(16) <= used < default_budget(16) + 5 + 1


def test_rank_r_is_a_threshold_with_probability_1_over_r() -> None:
    # Lemma 1 of Duerr and Hoyer, by seeded sampling. Each indicator is
    # bounded, so by Hoeffding the error is below sqrt(ln(2/1e-4)/(2 n))
    # = 0.050 for n = 2000 runs, except with probability 1e-4 per rank.
    rng = random.Random(3)
    n_items = 16
    table = list(range(n_items))  # the value r - 1 has rank r
    runs = 2000
    hits = [0] * n_items
    for _ in range(runs):
        _, _, thresholds = durr_hoyer_minimum(table, rng, budget=10 ** 9, target=0)
        for i in thresholds:
            hits[table[i]] += 1
    tol = math.sqrt(math.log(2 / 1e-4) / (2 * runs))
    for value in range(n_items):
        assert abs(hits[value] / runs - 1 / (value + 1)) < tol


def test_mean_queries_match_the_exact_value() -> None:
    # The mean of C over 2000 seeded runs, against the exact E[C], with a
    # tolerance of 5 standard errors (sample standard deviation).
    rng = random.Random(4)
    n_items = 16
    table = list(range(n_items))
    samples = []
    for _ in range(2000):
        _, used, _ = durr_hoyer_minimum(table, rng, budget=10 ** 9, target=0)
        samples.append(used)
    mean = sum(samples) / len(samples)
    var = sum((s - mean) ** 2 for s in samples) / (len(samples) - 1)
    assert abs(mean - expected_queries([1] * n_items)) < 5 * math.sqrt(var / len(samples))


def test_success_with_the_default_budget() -> None:
    # Theorem: success probability >= 1/2 with the default budget. On
    # random tables with N = 16 to 64, distinct or with ties, the seeded
    # rate is far above 1/2. A run stopped at the true minimum has the same
    # outcome as the full run, because y never changes after that.
    rng = random.Random(5)
    runs = 0
    found = 0
    for n_items in (16, 23, 32, 47, 64):
        for distinct in (True, False):
            for _ in range(8):
                table = random_table(rng, n_items, distinct)
                low = min(table)
                budget = default_budget(n_items)
                for _ in range(5):
                    y, used, _ = durr_hoyer_minimum(table, rng, budget=budget, target=low)
                    runs += 1
                    found += table[y] == low
    assert found / runs >= 0.95


def test_full_runs_return_a_minimum_index() -> None:
    rng = random.Random(6)
    for n_items in (1, 2, 3, 16, 32):
        for distinct in (True, False):
            table = random_table(rng, n_items, distinct)
            y, used, thresholds = durr_hoyer_minimum(table, rng)
            assert 0 <= y < n_items
            assert table[y] == min(table)
            budget = default_budget(n_items)
            assert used < budget + math.isqrt(max(0, n_items - 1)) + 2
            assert all(table[a] > table[b] for a, b in zip(thresholds, thresholds[1:]))


def test_m_schedule() -> None:
    m = Fraction(1)
    seen = []
    for _ in range(12):
        seen.append(num_choices(m, 64))
        m = next_m(m, 64)
    assert seen == [1, 2, 2, 2, 3, 3, 3, 4, 5, 6, 7, 8]
