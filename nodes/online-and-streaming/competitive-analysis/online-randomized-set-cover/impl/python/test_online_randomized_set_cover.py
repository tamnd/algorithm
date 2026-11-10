# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-randomized-set-cover/. The authors are listed in prov/68PE88.jsonl.

import itertools
import math
import random

from online_randomized_set_cover import (
    OnlineRandomizedSetCover,
    expected_threshold_cost,
    fractional_step,
    uncovered_probability,
)


def opt_cover(sets, costs, elems) -> float:
    """Cheapest integral cover of elems, by trying every family of sets."""
    names = list(sets)
    best = math.inf
    for r in range(len(names) + 1):
        for fam in itertools.combinations(names, r):
            if set(elems) <= set().union(*(sets[s] for s in fam)):
                best = min(best, sum(costs[s] for s in fam))
    return best


def random_system(rng: random.Random):
    n = rng.randint(2, 9)
    m = rng.randint(2, 7)
    sets = {f"S{i}": frozenset(e for e in range(n) if rng.random() < 0.4) for i in range(m)}
    for e in range(n):
        if not any(e in v for v in sets.values()):
            s = f"S{rng.randrange(m)}"
            sets[s] = sets[s] | {e}
    costs = {s: float(rng.randint(1, 5)) for s in sets}
    arrivals = [e for e in range(n) if rng.random() < 0.8] or [0]
    rng.shuffle(arrivals)
    return sets, costs, arrivals, n


def test_example_from_page() -> None:
    sets = {"A": frozenset({1, 2}), "B": frozenset({2, 3}), "C": frozenset({1, 2, 3})}
    costs = {"A": 1.0, "B": 1.0, "C": 3.0}
    alg = OnlineRandomizedSetCover(sets, costs, random.Random(0))
    assert alg.d == 3 and alg.k == 3
    alg.arrive(1)
    assert abs(alg.x["A"] + alg.x["C"] - 1) < 1e-9
    assert abs(alg.x["A"] - 0.8280) < 1e-4 and abs(alg.x["C"] - 0.1720) < 1e-4
    assert abs(alg.y[1] - 1.2482) < 1e-4
    alg.arrive(3)
    assert abs(alg.x["B"] - 0.6168) < 1e-4 and abs(alg.x["C"] - 0.3832) < 1e-4
    assert abs(alg.y[3] - 1.0475) < 1e-4
    assert alg.chosen == {"A", "B", "C"} and alg.cost() == 5.0 and alg.fallbacks == 0
    assert abs(expected_threshold_cost(alg.x, costs, alg.k) - 4.2346) < 1e-4


def test_certificates_on_random_systems() -> None:
    rng = random.Random(21)
    for trial in range(250):
        sets, costs, arrivals, n = random_system(rng)
        alg = OnlineRandomizedSetCover(sets, costs, random.Random(trial))
        for e in arrivals:
            alg.arrive(e)
            assert sum(alg.x[s] for s in alg.containing[e]) >= 1 - 1e-9
        covered = set().union(*(sets[s] for s in alg.chosen))
        assert set(arrivals) <= covered
        opt = opt_cover(sets, costs, arrivals)
        L = math.log(1 + alg.d)
        P, D = alg.fractional_cost(), alg.dual_value()
        assert P <= 2 * D + 1e-7
        for s in sets:
            load = sum(alg.y[e] for e in alg.y if e in sets[s])
            assert load <= costs[s] * L + 1e-7
        assert D / L <= opt + 1e-7
        assert P <= 2 * L * opt + 1e-7
        # expected cost of the rounding, exactly, given the fractional run
        thr = expected_threshold_cost(alg.x, costs, alg.k)
        assert thr <= alg.k * P + 1e-9
        fb = 0.0
        for e, snap in alg.history:
            p = uncovered_probability(snap, alg.k)
            assert p <= math.exp(-alg.k) + 1e-12
            fb += p * min(costs[s] for s in snap)
        assert fb <= len(arrivals) * math.exp(-alg.k) * opt + 1e-9
        assert fb <= opt / n + 1e-9
        assert thr + fb <= 2 * alg.k * L * opt + opt / n + 1e-9


def test_average_over_seeds_within_bound() -> None:
    rng = random.Random(4)
    sets, costs, arrivals, n = random_system(rng)
    opt = opt_cover(sets, costs, arrivals)
    total = 0.0
    for seed in range(300):
        alg = OnlineRandomizedSetCover(sets, costs, random.Random(seed))
        for e in arrivals:
            alg.arrive(e)
        assert alg.cost() >= opt
        total += alg.cost()
    k = max(1, math.ceil(2 * math.log(n)))
    d = max(sum(1 for v in sets.values() if e in v) for e in range(n))
    assert total / 300 <= 2 * k * math.log(1 + d) * opt + opt


def test_halving_lower_bound() -> None:
    for k in range(1, 8):
        m = 2**k
        costs = {i: 1.0 for i in range(m)}
        x = {i: 0.0 for i in range(m)}
        fam = list(range(m))
        fractional_step(x, fam, costs, m)
        while len(fam) > 1:
            half = len(fam) // 2
            a, b = fam[:half], fam[half:]
            fam = a if sum(x[i] for i in a) <= sum(x[i] for i in b) else b
            fractional_step(x, fam, costs, m)
        assert x[fam[0]] >= 1 - 1e-9
        assert sum(x.values()) >= 1 + k / 2 - 1e-9


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
    print("ok")
