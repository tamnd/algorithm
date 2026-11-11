# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-king-algorithm/. The authors are listed in prov/VHXE8S.jsonl.

import itertools
import random

from phase_king_algorithm import STRATEGIES, check, make_split, run


def all_cases(n: int, t: int):
    """Every traitor set of size t, every input of the honest processes."""
    for faulty in itertools.combinations(range(n), t):
        honest = [p for p in range(n) if p not in faulty]
        for bits in itertools.product((0, 1), repeat=len(honest)):
            inputs = [0] * n
            for p, b in zip(honest, bits):
                inputs[p] = b
            yield inputs, set(faulty)


def test_exhaustive_at_the_threshold() -> None:
    """n = 3t + 1: agreement and validity for all traitor sets, inputs and strategies."""
    for n, t in ((4, 1), (7, 2)):
        runs = 0
        for inputs, faulty in all_cases(n, t):
            for name, strat in STRATEGIES.items():
                res = run(n, t, inputs, faulty, strat, seed=runs)
                assert check(inputs, faulty, res) == [], (n, t, inputs, faulty, name)
                runs += 1
        assert runs > 0


def test_split_attack_cannot_win_above_the_threshold() -> None:
    for n, t in ((4, 1), (7, 2), (10, 3)):
        faulty = set(range(n - t, n))
        honest = [p for p in range(n) if p not in faulty]
        for k in range(1, len(honest)):
            group_a = set(honest[:k])
            inputs = [0 if p in group_a else 1 for p in range(n)]
            res = run(n, t, inputs, faulty, make_split(group_a))
            assert check(inputs, faulty, res) == []


def test_costs() -> None:
    n, t = 7, 2
    res = run(n, t, [0, 1, 0, 1, 0, 1, 0], {5, 6}, STRATEGIES["random"], seed=3)
    assert res["rounds"] == 3 * (t + 1)
    # at most n^2 values, n^2 proposals and n - 1 king messages per phase
    assert res["messages"] <= (t + 1) * (2 * n * n + n)


def test_seeded_random_runs_with_fewer_traitors() -> None:
    rng = random.Random(1989)
    for _ in range(300):
        t = rng.randint(1, 3)
        n = 3 * t + 1 + rng.randint(0, 2)
        faulty = set(rng.sample(range(n), rng.randint(0, t)))
        inputs = [rng.randint(0, 1) for _ in range(n)]
        strat = rng.choice(list(STRATEGIES.values()))
        res = run(n, t, inputs, faulty, strat, seed=rng.randrange(10**6))
        assert check(inputs, faulty, res) == []


def test_below_the_threshold_the_split_attack_breaks_agreement() -> None:
    """n = 3t: the honest processes split into two groups and stay apart."""
    for t in (1, 2):
        n = 3 * t
        faulty = set(range(2 * t, 3 * t))
        group_a = set(range(t))
        inputs = [0 if p in group_a else 1 for p in range(n)]
        res = run(n, t, inputs, faulty, make_split(group_a))
        assert check(inputs, faulty, res) == ["agreement"]
        assert all(res["decision"][p] == 0 for p in group_a)
        assert all(res["decision"][p] == 1 for p in range(t, 2 * t))
