# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bellman-equation/. The authors are listed in prov/Y80W1T.jsonl.

import random
from fractions import Fraction as F

from bellman_equation import (
    backup,
    backward_induction,
    bellman_operator,
    best_proper_policy,
    greedy_policy,
    is_fixed_point,
    policy_cost,
    q_value,
    reaches_goal,
)

GOALS = {"G"}


def example():
    return {
        "A": {"safe": (F(4), [(F(1), "G")]), "risky": (F(1), [(F(1, 2), "G"), (F(1, 2), "B")])},
        "B": {"back": (F(1), [(F(1), "A")]), "jump": (F(2), [(F(1, 3), "G"), (F(2, 3), "B")])},
    }


def random_model(rng: random.Random, n: int, k: int):
    """Every action reaches the goal with positive probability, so every policy is proper."""
    states = list(range(n))
    model = {}
    for s in states:
        acts = {}
        for a in range(k):
            weights = [rng.randint(0, 3) for _ in states] + [rng.randint(1, 3)]
            total = sum(weights)
            outs = [(F(w, total), t) for w, t in zip(weights, states + ["G"]) if w]
            acts[a] = (F(rng.randint(1, 9)), outs)
        model[s] = acts
    return model


def test_example_fixed_point():
    m = example()
    v, pi = best_proper_policy(m, GOALS)
    assert v == {"A": F(3), "B": F(4)}
    assert pi == {"A": "risky", "B": "back"}
    assert is_fixed_point(m, GOALS, v)
    assert q_value(m, GOALS, v, "B", "jump") == F(14, 3)
    assert backup(m, GOALS, v, "A") == (F(3), "risky")


def test_policy_costs():
    m = example()
    assert policy_cost(m, GOALS, {"A": "safe", "B": "back"}) == {"A": F(4), "B": F(5)}
    assert policy_cost(m, GOALS, {"A": "risky", "B": "jump"}) == {"A": F(4), "B": F(6)}


def test_backward_induction():
    m = example()
    vals, pols = backward_induction(m, GOALS, 6, {"A": F(10), "B": F(10)})
    assert vals[1] == {"A": F(4), "B": F(26, 3)}
    assert vals[2] == {"A": F(4), "B": F(5)}
    assert vals[6] == {"A": F(13, 4), "B": F(17, 4)}
    assert pols[0] == {"A": "safe", "B": "jump"}
    assert pols[1] == {"A": "safe", "B": "back"}
    assert pols[2] == {"A": "risky", "B": "back"}
    low, _ = backward_induction(m, GOALS, 8)
    assert low[8] == {"A": F(45, 16), "B": F(15, 4)}


def test_improper_zero_cost_loop_has_many_fixed_points():
    m = example()
    m["B"]["wait"] = (F(0), [(F(1), "B")])
    assert not reaches_goal(m, GOALS, {"A": "risky", "B": "wait"})
    for x in [F(4), F(1), F(0), F(-10)]:
        assert is_fixed_point(m, GOALS, {"A": min(F(4), 1 + x / 2), "B": x})
    assert not is_fixed_point(m, GOALS, {"A": F(4), "B": F(5)})


def test_random_models():
    rng = random.Random(7)
    for _ in range(40):
        m = random_model(rng, rng.randint(1, 3), rng.randint(1, 3))
        v, pi = best_proper_policy(m, GOALS)
        assert is_fixed_point(m, GOALS, v)
        assert bellman_operator(m, GOALS, v) == v
        assert policy_cost(m, GOALS, greedy_policy(m, GOALS, v)) == v
        # value iteration from zero rises to v and stays below it
        w = {s: F(0) for s in m}
        for _ in range(12):
            w = bellman_operator(m, GOALS, w)
            assert all(w[s] <= v[s] for s in m)
        fm = {s: {a: (float(c), [(float(p), t) for p, t in o]) for a, (c, o) in d.items()} for s, d in m.items()}
        x = {s: 0.0 for s in m}
        for _ in range(3000):
            x = {s: min(c + sum(p * (0.0 if t == "G" else x[t]) for p, t in o) for c, o in fm[s].values()) for s in m}
        assert all(abs(float(v[s]) - x[s]) < 1e-6 * (1 + float(v[s])) for s in m)
