# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-queen-algorithm/. The authors are listed in prov/P9R1W2.jsonl.

import itertools
import random

from phase_queen_algorithm import STRATEGIES, check, last_queen_attack, run


def all_cases(n: int, t: int):
    for faulty in itertools.combinations(range(n), t):
        honest = [p for p in range(n) if p not in faulty]
        for bits in itertools.product((0, 1), repeat=len(honest)):
            inputs = [0] * n
            for p, b in zip(honest, bits):
                inputs[p] = b
            yield inputs, set(faulty)


def test_exhaustive_at_the_threshold() -> None:
    """n = 4t + 1: all traitor sets, all honest inputs, all strategies."""
    for n, t in ((5, 1), (9, 2)):
        runs = 0
        for inputs, faulty in all_cases(n, t):
            for name, strat in list(STRATEGIES.items()) + [("last-queen", last_queen_attack)]:
                res = run(n, t, inputs, faulty, strat, seed=runs)
                assert check(inputs, faulty, res) == [], (n, t, inputs, faulty, name)
                runs += 1
        assert runs > 0


def test_costs() -> None:
    n, t = 9, 2
    res = run(n, t, [i % 2 for i in range(n)], {7, 8}, STRATEGIES["random"], seed=5)
    assert res["rounds"] == 2 * (t + 1)
    assert res["messages"] <= (t + 1) * (n * n + n)


def test_seeded_random_runs() -> None:
    rng = random.Random(1989)
    for _ in range(300):
        t = rng.randint(1, 3)
        n = 4 * t + 1 + rng.randint(0, 2)
        faulty = set(rng.sample(range(n), rng.randint(0, t)))
        inputs = [rng.randint(0, 1) for _ in range(n)]
        strat = rng.choice(list(STRATEGIES.values()) + [last_queen_attack])
        res = run(n, t, inputs, faulty, strat, seed=rng.randrange(10**6))
        assert check(inputs, faulty, res) == []


def test_below_the_threshold_a_faulty_last_queen_breaks_both() -> None:
    """n = 4t: all honest start with 1, and still disagree at the end."""
    for t in (1, 2, 3):
        n = 4 * t
        faulty = set(range(1, t + 1))  # process t is the queen of the last phase
        inputs = [1] * n
        res = run(n, t, inputs, faulty, last_queen_attack)
        assert check(inputs, faulty, res) == ["agreement", "validity"]


def test_the_three_round_threshold_is_not_enough() -> None:
    """With 3t < n <= 4t the two-round algorithm fails; n = 7, t = 2 here."""
    n, t = 7, 2
    faulty = {1, 2}
    res = run(n, t, [1] * n, faulty, last_queen_attack)
    assert "agreement" in check([1] * n, faulty, res)
