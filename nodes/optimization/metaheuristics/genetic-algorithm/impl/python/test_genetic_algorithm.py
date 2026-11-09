# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genetic-algorithm/. The authors are listed in prov/F1GKBX.jsonl.

import itertools
import math
import random
from fractions import Fraction

from genetic_algorithm import (
    bit_flip_mutation,
    genetic_algorithm,
    next_generation,
    one_plus_one_ea,
    one_point_crossover,
    onemax,
    roulette_wheel_select,
    tournament_select,
    tournament_winner,
    uniform_crossover,
)


def test_roulette_intervals_are_exact() -> None:
    rng = random.Random(11)
    for _ in range(300):
        fit = [Fraction(rng.randint(0, 9)) for _ in range(rng.randint(1, 7))]
        if sum(fit) == 0:
            fit[0] = Fraction(1)
        total = sum(fit)
        acc = Fraction(0)
        for i, fi in enumerate(fit):
            lo, hi = acc / total, (acc + fi) / total
            assert hi - lo == fi / total  # the interval of i has the length of its share
            if fi > 0:
                assert roulette_wheel_select(fit, lo) == i
                assert roulette_wheel_select(fit, hi - Fraction(1, 10**9)) == i
            acc += fi


def test_roulette_frequencies() -> None:
    rng = random.Random(12)
    fit = [1.0, 2.0, 3.0, 4.0]
    trials = 40000
    counts = [0] * 4
    for _ in range(trials):
        counts[roulette_wheel_select(fit, rng.random())] += 1
    for i in range(4):
        p = fit[i] / 10
        assert abs(counts[i] / trials - p) < 5 * math.sqrt(p * (1 - p) / trials)


def test_tournament_closed_form_by_enumeration() -> None:
    # With ties broken by the smaller index, the order is strict. The entrant of
    # rank r (1 = worst) wins with probability (r^k - (r - 1)^k) / N^k.
    for fit in ([5, 1, 4, 2, 3], [2, 2, 1, 2, 0], [7, 7, 7]):
        n = len(fit)
        order = sorted(range(n), key=lambda i: (fit[i], -i))
        rank = {idx: r + 1 for r, idx in enumerate(order)}
        for k in (1, 2, 3):
            wins = [0] * n
            for entrants in itertools.product(range(n), repeat=k):
                wins[tournament_winner(fit, entrants)] += 1
            for i in range(n):
                r = rank[i]
                assert Fraction(wins[i], n**k) == Fraction(r**k - (r - 1) ** k, n**k)


def test_tournament_frequencies() -> None:
    rng = random.Random(13)
    fit = [3.0, 9.0, 1.0, 5.0]
    trials, k = 40000, 2
    counts = [0] * 4
    for _ in range(trials):
        counts[tournament_select(fit, k, rng)] += 1
    rank = {2: 1, 0: 2, 3: 3, 1: 4}
    for i in range(4):
        p = (rank[i] ** k - (rank[i] - 1) ** k) / 16
        assert abs(counts[i] / trials - p) < 5 * math.sqrt(p * (1 - p) / trials)


def test_crossover_keeps_the_genes_of_each_position() -> None:
    rng = random.Random(14)
    for _ in range(500):
        n = rng.randint(2, 12)
        a = tuple(rng.randint(0, 1) for _ in range(n))
        b = tuple(rng.randint(0, 1) for _ in range(n))
        for cut in range(1, n):
            c, d = one_point_crossover(a, b, cut)
            assert c == a[:cut] + b[cut:] and d == b[:cut] + a[cut:]
            for i in range(n):
                assert sorted((c[i], d[i])) == sorted((a[i], b[i]))
        mask = [rng.randint(0, 1) for _ in range(n)]
        c, d = uniform_crossover(a, b, mask)
        for i in range(n):
            assert c[i] == (a[i] if mask[i] else b[i])
            assert sorted((c[i], d[i])) == sorted((a[i], b[i]))


def test_mutation_distribution() -> None:
    rng = random.Random(15)
    x = (0, 1, 0)
    p = 0.2
    trials = 50000
    counts: dict[tuple[int, ...], int] = {}
    for _ in range(trials):
        y = bit_flip_mutation(x, p, rng)
        assert len(y) == 3 and set(y) <= {0, 1}
        counts[y] = counts.get(y, 0) + 1
    for y in itertools.product((0, 1), repeat=3):
        h = sum(a != b for a, b in zip(x, y))
        q = p**h * (1 - p) ** (3 - h)
        assert abs(counts.get(y, 0) / trials - q) < 5 * math.sqrt(q * (1 - q) / trials)


def test_elitism_never_loses_the_best() -> None:
    rng = random.Random(16)
    for _ in range(300):
        n, length = rng.randint(2, 8), rng.randint(2, 8)
        pop = [tuple(rng.randint(0, 1) for _ in range(length)) for _ in range(n)]
        w = [rng.randint(0, 5) for _ in range(length)]

        def f(x: tuple[int, ...]) -> int:
            return sum(wi * xi for wi, xi in zip(w, x))

        elite = rng.randint(1, n)
        sel = rng.choice(["tournament", "roulette"]) if sum(map(f, pop)) > 0 else "tournament"
        q = next_generation(pop, f, 0.9, 0.3, elite, rng, sel)
        assert len(q) == n
        best = max(pop, key=lambda x: (f(x), -pop.index(x)))
        assert best in q
        assert max(map(f, q)) >= max(map(f, pop))


def test_ga_reaches_onemax_optimum() -> None:
    rng = random.Random(2024)
    n = 30
    best, fbest, hist = genetic_algorithm(onemax, n, 40, 0.9, 1 / n, 1, 300, rng, target=n)
    assert fbest == n and best == (1,) * n
    assert all(hist[t] <= hist[t + 1] for t in range(len(hist) - 1))  # elitism


def test_ga_roulette_runs_and_keeps_valid_strings() -> None:
    rng = random.Random(7)
    best, fbest, hist = genetic_algorithm(lambda x: 1 + onemax(x), 12, 20, 0.8, 1 / 12, 1, 200, rng, "roulette", target=13)
    assert fbest == 13 and len(best) == 12


def test_one_plus_one_ea_on_onemax() -> None:
    rng = random.Random(99)
    n, runs = 20, 200
    times = [one_plus_one_ea(onemax, n, n, rng, 100000) for _ in range(runs)]
    assert min(times) >= 0
    harmonic = sum(1 / i for i in range(1, n + 1))
    assert sum(times) / runs <= math.e * n * harmonic  # the fitness-level bound


def _schema_terms(pop, fit, h, p_c, p_m):
    """Exact E[m(H, t+1)] for one generation (roulette, one-point crossover, bit flips) and the bound."""
    n, length = len(pop), len(pop[0])
    total = sum(fit)
    fixed = [i for i, c in enumerate(h) if c != "*"]

    def q(x):  # probability that the mutated x is in H
        r = Fraction(1)
        for i in fixed:
            r *= p_m if x[i] != int(h[i]) else 1 - p_m
        return r

    pair = Fraction(0)
    for i in range(n):
        for j in range(n):
            w = fit[i] * fit[j] / (total * total)
            a, b = pop[i], pop[j]
            e = (1 - p_c) * (q(a) + q(b))
            for cut in range(1, length):
                c, d = one_point_crossover(a, b, cut)
                e += p_c / (length - 1) * (q(c) + q(d))
            pair += w * e
    expected = Fraction(n, 2) * pair
    inst = [i for i in range(n) if all(pop[i][k] == int(h[k]) for k in fixed)]
    delta = (fixed[-1] - fixed[0]) if fixed else 0
    bound = n * sum(fit[i] for i in inst) / total * (1 - p_c * Fraction(delta, length - 1)) * (1 - p_m) ** len(fixed)
    return expected, bound


def test_schema_theorem_inequality_exactly() -> None:
    rng = random.Random(17)
    length = 4
    schemata = ["".join(s) for s in itertools.product("01*", repeat=length)]
    for _ in range(12):
        n = 4
        pop = [tuple(rng.randint(0, 1) for _ in range(length)) for _ in range(n)]
        fit = [Fraction(rng.randint(1, 9)) for _ in range(n)]
        p_c = Fraction(rng.randint(0, 10), 10)
        p_m = Fraction(rng.randint(0, 5), 20)
        for h in schemata:
            expected, bound = _schema_terms(pop, fit, h, p_c, p_m)
            assert expected >= bound


def test_simulation_matches_the_exact_expectation() -> None:
    rng = random.Random(18)
    pop = [(1, 1, 0, 0), (0, 1, 1, 0), (1, 0, 1, 1), (0, 0, 0, 1)]
    fit = [Fraction(4), Fraction(1), Fraction(3), Fraction(2)]
    table = dict(zip(pop, fit))
    h = "1**1"
    p_c, p_m = Fraction(7, 10), Fraction(1, 10)
    expected, bound = _schema_terms(pop, fit, h, p_c, p_m)
    assert expected >= bound
    trials, s, s2 = 20000, 0, 0
    for _ in range(trials):
        q = next_generation(pop, lambda x: float(table[x]) if x in table else 0.0, 0.7, 0.1, 0, rng, "roulette")
        m = sum(1 for x in q if x[0] == 1 and x[3] == 1)
        s += m
        s2 += m * m
    mean = s / trials
    sd = math.sqrt(s2 / trials - mean * mean)
    assert abs(mean - float(expected)) < 5 * sd / math.sqrt(trials)
