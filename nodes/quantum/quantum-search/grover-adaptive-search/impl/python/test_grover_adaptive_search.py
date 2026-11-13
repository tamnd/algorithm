# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grover-adaptive-search/. The authors are listed in prov/Z3TQD9.jsonl.

import math
import random
from fractions import Fraction

from grover_adaptive_search import (
    default_budget,
    grover_adaptive_search,
    grover_state,
    maxcut_qubo,
    next_k,
    num_choices,
    patience_expected_queries,
    patience_success,
    qubo_table,
    qubo_value,
    value_counts,
)
from qsim import H, apply_1q, apply_diagonal, probabilities

TOL = 1e-9
# Equation (14) of Gilliam, Woerner and Gonciulea:
# f = -2 x1 x3 - x2 x3 - x1 + 2 x2 - 3 x3, with x1, x2, x3 the bits 0, 1, 2.
EQ14 = ([[0, 0, -2], [0, 0, -1], [0, 0, 0]], [-1, 2, -3], 0)


def random_qubo(rng: random.Random, n: int):
    q = [[rng.randint(-4, 4) if j >= i else 0 for j in range(n)] for i in range(n)]
    b = [rng.randint(-4, 4) for _ in range(n)]
    return q, b, rng.randint(-3, 3)


def random_graph(rng: random.Random, n: int):
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.5]
    return edges or [(0, 1)]


def cut_size(edges, x: int) -> int:
    return sum(((x >> u) & 1) != ((x >> v) & 1) for u, v in edges)


def test_qubo_and_maxcut_values() -> None:
    rng = random.Random(1)
    for n in range(1, 9):
        q, b, c = random_qubo(rng, n)
        for x in range(1 << n):
            bits = [(x >> i) & 1 for i in range(n)]
            direct = c + sum(b[i] * bits[i] for i in range(n)) + sum(
                q[i][j] * bits[i] * bits[j] for i in range(n) for j in range(n))
            assert qubo_value(q, b, c, x) == direct
        edges = random_graph(rng, max(2, n))
        values = qubo_table(*maxcut_qubo(max(2, n), edges))
        assert values == [-cut_size(edges, x) for x in range(len(values))]
    assert qubo_table(*EQ14) == [0, -1, 2, 1, -3, -6, -2, -5]


def test_diffusion_is_the_gate_circuit() -> None:
    # A (2|0><0| - I) A^dagger with A = H^n, built from gates, equals the
    # reflection about the mean that grover_state uses.
    rng = random.Random(2)
    n = 3
    values = [rng.randint(-3, 3) for _ in range(1 << n)]
    for y in range(-3, 5):
        state = [0j] * (1 << n)
        state[0] = 1 + 0j
        for q in range(n):
            apply_1q(state, q, H)
        for r in range(4):
            got = grover_state(values, y, r)
            assert max(abs(a - b) for a, b in zip(got, state)) < TOL
            apply_diagonal(state, lambda x: -1.0 if values[x] < y else 1.0)
            for q in range(n):
                apply_1q(state, q, H)
            apply_diagonal(state, lambda x: 1.0 if x == 0 else -1.0)
            for q in range(n):
                apply_1q(state, q, H)


def test_success_probability_is_sin_squared() -> None:
    # For every threshold of random QUBOs with N = 2 to 64 points, r
    # iterations find a point below the threshold with probability
    # sin^2((2r+1) theta), sin^2 theta = t/N, uniform over those points.
    rng = random.Random(3)
    for n in range(1, 7):
        values = qubo_table(*random_qubo(rng, n))
        size = len(values)
        for y in sorted(set(values)) + [max(values) + 1]:
            marked = [x for x in range(size) if values[x] < y]
            t = len(marked)
            theta = math.asin(math.sqrt(t / size))
            for r in range(6):
                probs = probabilities(grover_state(values, y, r))
                total = sum(probs[x] for x in marked)
                assert abs(total - math.sin((2 * r + 1) * theta) ** 2) < TOL
                for x in marked:
                    assert abs(probs[x] - total / t) < TOL


def test_figure_8_probabilities() -> None:
    # With two of the eight points below the threshold, one iteration finds
    # one of them with certainty; with one point, with probability 25/32.
    values = qubo_table(*EQ14)
    probs = probabilities(grover_state(values, -3, 1))
    assert abs(probs[5] - 0.5) < TOL and abs(probs[7] - 0.5) < TOL
    probs = probabilities(grover_state(values, -5, 1))
    assert abs(probs[5] - 25 / 32) < TOL


def test_example_run() -> None:
    values = qubo_table(*EQ14)
    x, y, used, rounds = grover_adaptive_search(values, random.Random(6), patience=3)
    assert (x, y, used) == (5, -6, 12)
    assert [(r[0], r[2], r[3]) for r in rounds] == [
        (-1, 0, 6), (-2, 0, 0), (-2, 1, 7), (-5, 0, 2), (-5, 0, 2),
        (-5, 0, 5), (-6, 0, 7), (-6, 0, 1), (-6, 1, 5)]
    assert [r[1] for r in rounds] == [1, 1, Fraction(6, 5), 1, Fraction(6, 5),
                                      Fraction(36, 25), 1, Fraction(6, 5), Fraction(36, 25)]


def test_budget_rule_against_brute_force() -> None:
    # Random QUBOs and MaxCut instances with 2 to 8 variables. The proof
    # gives success >= 1/2 with the default budget; the seeded rate is far
    # higher. A run stopped at the true minimum has the outcome of the full
    # run, because the threshold never changes after it.
    rng = random.Random(4)
    runs = 0
    found = 0
    for n in range(2, 9):
        for kind in range(6):
            if kind % 2:
                values = qubo_table(*maxcut_qubo(n, random_graph(rng, n)))
            else:
                values = qubo_table(*random_qubo(rng, n))
            best = min(values)
            for _ in range(3):
                x, y, used, _ = grover_adaptive_search(values, rng, target=best)
                assert y == values[x]
                runs += 1
                found += y == best
    assert found / runs >= 0.95


def test_full_runs_keep_the_best_point() -> None:
    rng = random.Random(5)
    for n in (2, 3, 5, 6):
        values = qubo_table(*maxcut_qubo(n, random_graph(rng, n)))
        for patience in (None, 2, 8):
            x, y, used, rounds = grover_adaptive_search(values, rng, patience=patience)
            assert y == values[x]
            if rounds:
                assert y == min([rounds[0][0]] + [values[r[3]] for r in rounds])
            thresholds = [r[0] for r in rounds]
            assert all(a >= b for a, b in zip(thresholds, thresholds[1:]))
            if patience is None:
                assert used < default_budget(len(values)) + math.isqrt(len(values)) + 2
                assert y == min(values)
            else:
                assert not rounds or all(not r[5] for r in rounds[-patience:])


def test_patience_rule_exact_against_sampling() -> None:
    # Exact success probability and mean queries for equation (14) with
    # three rounds of patience, against 3000 seeded runs. Hoeffding: the
    # rate is within sqrt(ln(2/1e-4)/(2 n)) = 0.058 except with
    # probability 1e-4; the mean is within 5 standard errors.
    values = qubo_table(*EQ14)
    counts = value_counts(values)
    assert abs(patience_success(counts, 3) - 0.7663) < 1e-4
    assert abs(patience_expected_queries(counts, 3) - 7.824) < 1e-3
    rng = random.Random(7)
    runs = 3000
    hits = 0
    samples = []
    for _ in range(runs):
        _, y, used, _ = grover_adaptive_search(values, rng, patience=3)
        hits += y == min(values)
        samples.append(used)
    tol = math.sqrt(math.log(2 / 1e-4) / (2 * runs))
    assert abs(hits / runs - patience_success(counts, 3)) < tol
    mean = sum(samples) / runs
    var = sum((s - mean) ** 2 for s in samples) / (runs - 1)
    assert abs(mean - patience_expected_queries(counts, 3)) < 5 * math.sqrt(var / runs)


def test_patience_rule_on_maxcut_with_ties() -> None:
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    values = qubo_table(*maxcut_qubo(4, edges))
    counts = value_counts(values)
    assert counts == [2, 8, 4, 2]
    rng = random.Random(8)
    runs = 3000
    hits = sum(grover_adaptive_search(values, rng, patience=3)[1] == -4 for _ in range(runs))
    tol = math.sqrt(math.log(2 / 1e-4) / (2 * runs))
    assert abs(hits / runs - patience_success(counts, 3)) < tol


def test_patience_needed_grows_with_n() -> None:
    # Distinct values, N = 2^n: the success of a fixed patience falls with
    # n, and the least patience for success 1/2 is the table of the page.
    want = {3: 2, 4: 3, 5: 4, 6: 6, 7: 8, 8: 10, 9: 12, 10: 14}
    for n, p_half in want.items():
        counts = [1] * (1 << n)
        rates = [patience_success(counts, p) for p in range(1, p_half + 1)]
        assert all(a < b for a, b in zip(rates, rates[1:]))
        assert rates[-1] >= 0.5 > (rates[-2] if len(rates) > 1 else 0)
    assert abs(patience_success([1] * 256, 3) - 0.064) < 5e-4
    assert abs(patience_success([1] * 1024, 3) - 0.017) < 5e-4
    # The rows of the complexity table: (n, P, success, expected queries).
    rows = [(4, 3, 0.578, 8.6), (4, 6, 0.927, 17.4), (8, 10, 0.587, 47.9),
            (8, 14, 0.929, 80.6), (10, 14, 0.568, 97.8), (10, 18, 0.929, 162.6)]
    for n, patience, rate, cost in rows:
        counts = [1] * (1 << n)
        assert abs(patience_success(counts, patience) - rate) < 5e-4
        assert abs(patience_expected_queries(counts, patience) - cost) < 0.05
        assert patience_success(counts, patience - 1) < (0.5 if rate < 0.9 else 0.9)


def test_patience_upper_bound() -> None:
    # Part 3 of the theorem: success <= (n_1/N)(1 + P (2 c_P - 1)^2 ln N).
    rng = random.Random(9)
    for n in range(2, 11):
        size = 1 << n
        tables = [[1] * size]
        for _ in range(2):
            values = [rng.randrange(size // 2 + 1) for _ in range(size)]
            tables.append(value_counts(values))
        for counts in tables:
            for patience in (1, 2, 3, 5, 8):
                k = Fraction(1)
                for _ in range(patience - 1):
                    k = next_k(k, size)
                c_p = num_choices(k, size)
                bound = counts[0] / size * (1 + patience * (2 * c_p - 1) ** 2 * math.log(size))
                assert patience_success(counts, patience) <= bound + TOL


def test_rotation_count_schedule() -> None:
    k = Fraction(1)
    seen = []
    for _ in range(12):
        seen.append(num_choices(k, 64))
        k = next_k(k, 64)
    assert seen == [1, 2, 2, 2, 3, 3, 3, 4, 5, 6, 7, 8]
