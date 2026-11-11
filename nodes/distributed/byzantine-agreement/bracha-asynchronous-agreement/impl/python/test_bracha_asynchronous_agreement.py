# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bracha-asynchronous-agreement/. The authors are listed in prov/R0F3DQ.jsonl.

import itertools
import random

from bracha_asynchronous_agreement import D1, STRATEGIES, Run, check, run

SCHEDULERS = ("random", "adversarial", "fifo")


def test_all_traitor_sets_n4() -> None:
    n, t = 4, 1
    for f in range(n):
        for inputs in itertools.product((0, 1), repeat=n):
            for name, strat in STRATEGIES.items():
                sch = SCHEDULERS[(f + sum(inputs)) % 3]
                res = run(n, t, list(inputs), {f}, strat, sch, seed=f)
                assert check(list(inputs), {f}, res) == [], (inputs, f, name, sch)


def test_seeded_runs_n7() -> None:
    rng = random.Random(1987)
    n, t = 7, 2
    for _ in range(40):
        faulty = set(rng.sample(range(n), rng.randint(0, t)))
        inputs = [rng.randint(0, 1) for _ in range(n)]
        strat = rng.choice(list(STRATEGIES.values()))
        res = run(n, t, inputs, faulty, strat, rng.choice(SCHEDULERS), rng.randrange(10**6))
        assert check(inputs, faulty, res) == []


def test_unanimous_inputs_decide_in_round_one() -> None:
    """Validation stops the faulty processes from pushing the other value."""
    for n, t in ((4, 1), (7, 2)):
        for v in (0, 1):
            for name, strat in STRATEGIES.items():
                inputs = [v] * n
                res = run(n, t, inputs, set(range(t)), strat, "adversarial", 3)
                assert res["decision"] == {p: v for p in range(t, n)} and res["rounds"] == 1, name


def test_validation_rejects_an_unjustified_vote() -> None:
    """With only 0s in step 2, a step-3 message ("d", 1) is never valid."""
    R = Run(4, 1, [0, 0, 0, 0], {3}, STRATEGIES["silent"])
    R.valid[0][(1, 2)] = {0: 0, 1: 0, 2: 0}
    assert not R.justified(0, 1, 3, D1)
    assert R.justified(0, 1, 3, ("d", 0))
    assert not R.justified(0, 1, 3, "?")


def test_mean_rounds_are_small_against_these_adversaries() -> None:
    """The measured mean number of rounds until the last honest decision."""
    for n, t in ((4, 1), (7, 2)):
        rounds = []
        for seed in range(20):
            inputs = [i % 2 for i in range(n)]
            res = run(n, t, inputs, set(range(n - t, n)), STRATEGIES["random"], "random", seed)
            assert check(inputs, set(range(n - t, n)), res) == []
            rounds.append(res["rounds"])
        assert sum(rounds) / len(rounds) <= 3
