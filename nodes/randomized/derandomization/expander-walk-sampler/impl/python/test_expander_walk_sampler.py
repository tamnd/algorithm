# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expander-walk-sampler/. The authors are listed in prov/RB6W2D.jsonl.

import itertools
import random
from fractions import Fraction

from expander_walk_sampler import (
    amplify_one_sided,
    check_regular_undirected,
    expander_walk_sample,
    margulis_gabber_galil,
    petersen,
    random_bits_used,
    spectral_expansion,
    stay_probability,
    walk_from_choices,
)


def hitting_bound(mu: Fraction, lam: float, t: int) -> float:
    return float(mu) * (float(mu) + lam * (1 - float(mu))) ** (t - 1)


def test_graphs_are_regular_and_undirected() -> None:
    assert check_regular_undirected(petersen()) == 3
    for m in (2, 3, 4, 5):
        assert check_regular_undirected(margulis_gabber_galil(m)) == 8


def test_spectral_expansion_known_values() -> None:
    assert abs(spectral_expansion(petersen()) - 2 / 3) < 1e-9
    # K4 with walk matrix J - I over 3: eigenvalues 1 and -1/3.
    k4 = [[v for v in range(4) if v != u] for u in range(4)]
    assert abs(spectral_expansion(k4) - 1 / 3) < 1e-9
    # A 6-cycle is bipartite, so lambda = 1.
    c6 = [[(u - 1) % 6, (u + 1) % 6] for u in range(6)]
    assert abs(spectral_expansion(c6) - 1) < 1e-9


def test_petersen_outer_cycle_exact() -> None:
    g = petersen()
    for t in range(1, 8):
        assert stay_probability(g, {0, 1, 2, 3, 4}, t) == Fraction(1, 2) * Fraction(2, 3) ** (t - 1)


def test_hitting_bound_all_sets_petersen() -> None:
    g = petersen()
    lam = 2 / 3
    for k in range(1, 10):
        mu = Fraction(k, 10)
        for b in itertools.combinations(range(10), k):
            for t in (1, 2, 3, 5):
                assert float(stay_probability(g, set(b), t)) <= hitting_bound(mu, lam, t) + 1e-12


def test_petersen_worst_sets() -> None:
    # The largest stay probability over all sets of a given size, for t = 4.
    g = petersen()
    worst4 = max(stay_probability(g, set(b), 4) for b in itertools.combinations(range(10), 4))
    worst5 = max(stay_probability(g, set(b), 4) for b in itertools.combinations(range(10), 5))
    assert worst4 == Fraction(1, 15)
    assert worst5 == Fraction(4, 27)


def test_hitting_bound_margulis_gabber_galil() -> None:
    rng = random.Random(11)
    for m in (3, 4):
        g = margulis_gabber_galil(m)
        n = len(g)
        lam = spectral_expansion(g)
        assert lam < 1
        subsets = [set(b) for b in itertools.combinations(range(n), 2)] if n <= 9 else []
        subsets += [set(rng.sample(range(n), rng.randint(1, n - 1))) for _ in range(150)]
        for b in subsets:
            mu = Fraction(len(b), n)
            for t in (2, 4, 6):
                assert float(stay_probability(g, b, t)) <= hitting_bound(mu, lam, t) * (1 + 1e-9)


def test_stay_probability_matches_enumeration() -> None:
    # Drive the walk with every start and every choice sequence.
    g = margulis_gabber_galil(3)
    bad = {0, 1, 4, 5, 7}
    t = 3
    hits = 0
    total = 0
    for start in range(len(g)):
        for choices in itertools.product(range(8), repeat=t - 1):
            path = walk_from_choices(g, start, list(choices))
            total += 1
            hits += all(v in bad for v in path)
    assert Fraction(hits, total) == stay_probability(g, bad, t)


def test_walk_is_uniform_at_each_step() -> None:
    # The uniform start is stationary, so each position of the walk is uniform.
    g = petersen()
    t = 3
    counts = [[0] * 10 for _ in range(t)]
    for start in range(10):
        for choices in itertools.product(range(3), repeat=t - 1):
            for i, v in enumerate(walk_from_choices(g, start, list(choices))):
                counts[i][v] += 1
    for row in counts:
        assert len(set(row)) == 1


def test_sampler_and_amplifier() -> None:
    rng = random.Random(5)
    g = margulis_gabber_galil(4)
    path = expander_walk_sample(g, 6, rng)
    assert len(path) == 6
    assert all(path[i + 1] in g[path[i]] for i in range(5))
    assert random_bits_used(16, 8, 6) == 4 + 5 * 3
    accept = set(range(8))  # density 1/2
    # The amplifier draws the same walk as the sampler for the same seed.
    for seed in range(30):
        walk = expander_walk_sample(g, 10, random.Random(seed))
        expected = any(v in accept for v in walk)
        assert amplify_one_sided(lambda v: v in accept, g, 10, random.Random(seed)) == expected
    assert not amplify_one_sided(lambda v: False, g, 10, rng)
    assert amplify_one_sided(lambda v: True, g, 1, rng)


def test_rejection_rate_statistical() -> None:
    # Fixed seed. The accepting set has density 1/2 in the MGG graph with m = 4.
    # The exact probability p of a wrong reject with t = 8 is computed, and
    # 20000 runs must give a rate within 0.02 of it: the Hoeffding bound
    # makes a failure of a correct sampler less likely than 2 exp(-16) < 1e-6.
    g = margulis_gabber_galil(4)
    accept = set(range(0, 16, 2))
    bad = set(range(16)) - accept
    p = float(stay_probability(g, bad, 8))
    rng = random.Random(77)
    runs = 20000
    rejects = sum(not amplify_one_sided(lambda v: v in accept, g, 8, rng) for _ in range(runs))
    assert abs(rejects / runs - p) < 0.02


def test_bad_input() -> None:
    try:
        check_regular_undirected([[1], [2], [0]])
    except ValueError:
        pass
    else:
        raise AssertionError("a directed 3-cycle must be rejected")
    try:
        amplify_one_sided(lambda v: True, petersen(), 0, random.Random(0))
    except ValueError:
        pass
    else:
        raise AssertionError("t = 0 must be rejected")
