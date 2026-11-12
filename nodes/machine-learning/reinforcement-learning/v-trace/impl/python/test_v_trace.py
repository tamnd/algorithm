# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/v-trace/. The authors are listed in prov/V75JCF.jsonl.

import random
from fractions import Fraction as F

from v_trace import state_values, truncated_target_policy, v_trace, v_trace_operator

ACTIONS = [0, 1]


def table_policy(rows):
    return lambda a, x: rows[x][a]


def dist(v1, v2):
    return max(abs(v1[k] - v2[k]) for k in v1)


# Switch MDP: action 0 moves to the other state, action 1 stays; discounted, no end.
SWITCH = {
    (0, 0): [(F(1), F(1), 1)],
    (0, 1): [(F(1), F(0), 0)],
    (1, 0): [(F(1, 2), F(0), 0), (F(1, 2), F(3), 1)],
    (1, 1): [(F(1), F(2), 1)],
}
G = F(9, 10)
PI = table_policy({0: [F(9, 10), F(1, 10)], 1: [F(1, 5), F(4, 5)]})
MU = table_policy({0: [F(1, 4), F(3, 4)], 1: [F(1, 2), F(1, 2)]})


def test_fixed_point_is_the_value_of_pi_rho_bar_for_any_c_bar() -> None:
    for rho_bar in (F(1, 2), F(1), F(2), F(4), None):
        target = state_values(SWITCH, truncated_target_policy(PI, MU, ACTIONS, rho_bar), ACTIONS, G)
        for c_bar in (F(0), F(1, 2), F(1), F(2), F(4)):
            if rho_bar is not None and c_bar > rho_bar:
                continue
            assert v_trace_operator(target, SWITCH, PI, MU, ACTIONS, G, rho_bar, c_bar) == target


def test_limits_of_rho_bar() -> None:
    v_pi = state_values(SWITCH, PI, ACTIONS, G)
    v_mu = state_values(SWITCH, MU, ACTIONS, G)
    assert state_values(SWITCH, truncated_target_policy(PI, MU, ACTIONS, None), ACTIONS, G) == v_pi
    assert state_values(SWITCH, truncated_target_policy(PI, MU, ACTIONS, F(36, 10)), ACTIONS, G) == v_pi
    assert state_values(SWITCH, truncated_target_policy(PI, MU, ACTIONS, F(2, 15)), ACTIONS, G) == v_mu
    assert v_pi != v_mu


def test_one_step_example_table() -> None:
    model = {("x", 0): [(F(1), F(1), None)], ("x", 1): [(F(1), F(0), None)]}
    pi = table_policy({"x": [F(9, 10), F(1, 10)]})
    mu = table_policy({"x": [F(1, 5), F(4, 5)]})
    expected = {F(1, 10): F(1, 5), F(1, 2): F(1, 2), F(1): F(2, 3), F(2): F(4, 5), F(9, 2): F(9, 10)}
    for rho_bar, value in expected.items():
        assert v_trace_operator({"x": value}, model, pi, mu, ACTIONS, G, rho_bar, F(1, 10)) == {"x": value}
        assert state_values(model, truncated_target_policy(pi, mu, ACTIONS, rho_bar), ACTIONS, G) == {"x": value}


def test_contraction_rate_bound() -> None:
    rng = random.Random(0)
    for rho_bar, c_bar in ((F(1), F(1)), (F(2), F(1, 2)), (F(1, 2), F(1, 2))):
        target = state_values(SWITCH, truncated_target_policy(PI, MU, ACTIONS, rho_bar), ACTIONS, G)
        beta = min(sum(MU(a, x) * min(rho_bar, PI(a, x) / MU(a, x)) for a in ACTIONS) for x in (0, 1))
        eta = 1 - (1 - G) * beta
        v = {x: F(rng.randrange(-20, 21)) for x in (0, 1)}
        for _ in range(6):
            nv = v_trace_operator(v, SWITCH, PI, MU, ACTIONS, G, rho_bar, c_bar)
            assert dist(nv, target) <= eta * dist(v, target)
            v = nv


def test_on_policy_targets_are_n_step_returns() -> None:
    rng = random.Random(1)
    for _ in range(20):
        n = rng.randrange(1, 7)
        steps = [(rng.randrange(3), rng.randrange(2), F(rng.randrange(-4, 5))) for _ in range(n)]
        last = rng.choice([None, 0, 1, 2])
        v = {x: F(rng.randrange(-9, 10), 4) for x in range(3)}
        pol = table_policy({x: [F(1, 3), F(2, 3)] for x in range(3)})
        for c_bar in (F(1), F(3, 2), None):
            targets, _ = v_trace(steps, last, v, pol, pol, G, None if c_bar is None else c_bar + 1, c_bar)
            for s in range(n):
                ret = sum(G ** (t - s) * steps[t][2] for t in range(s, n)) + G ** (n - s) * (0 if last is None else v[last])
                assert targets[s] == ret


LAYERED = {
    ("s", 0): [(F(1, 2), F(1), "u"), (F(1, 2), F(0), "v")],
    ("s", 1): [(F(1, 3), F(2), "u"), (F(2, 3), F(-1), "v")],
    ("u", 0): [(F(1), F(3), None)],
    ("u", 1): [(F(1, 2), F(0), "w"), (F(1, 2), F(1), None)],
    ("v", 0): [(F(1), F(1), "w")],
    ("v", 1): [(F(1), F(-2), None)],
    ("w", 0): [(F(1), F(4), None)],
    ("w", 1): [(F(1, 4), F(0), None), (F(3, 4), F(2), None)],
}
L_PI = table_policy({"s": [F(1, 4), F(3, 4)], "u": [F(1, 2), F(1, 2)], "v": [F(9, 10), F(1, 10)], "w": [F(1, 3), F(2, 3)]})
L_MU = table_policy({"s": [F(1, 2), F(1, 2)], "u": [F(4, 5), F(1, 5)], "v": [F(1, 2), F(1, 2)], "w": [F(1, 2), F(1, 2)]})


def episodes(x):
    for a in ACTIONS:
        for p, r, y in LAYERED[x, a]:
            if y is None:
                yield L_MU(a, x) * p, [(x, a, r)]
            else:
                for p2, rest in episodes(y):
                    yield L_MU(a, x) * p * p2, [(x, a, r)] + rest


def test_mean_target_is_the_operator() -> None:
    rng = random.Random(2)
    v = {x: F(rng.randrange(-6, 7), 2) for x in "suvw"}
    for rho_bar, c_bar in ((F(1), F(1)), (F(3, 2), F(1, 2)), (None, None)):
        rv = v_trace_operator(v, LAYERED, L_PI, L_MU, ACTIONS, F(1), rho_bar, c_bar)
        for x in "suvw":
            mean = sum(p * v_trace(ep, None, dict(v), L_PI, L_MU, F(1), rho_bar, c_bar)[0][0] for p, ep in episodes(x))
            assert mean == rv[x]


def test_sampled_v_trace_learns_v_pi_rho_bar() -> None:
    target = state_values(SWITCH, truncated_target_policy(PI, MU, ACTIONS, F(1)), ACTIONS, G)
    pi = lambda a, x: float(PI(a, x))
    mu = lambda a, x: float(MU(a, x))
    rng = random.Random(0)
    v = {0: 0.0, 1: 0.0}
    for _ in range(6000):
        x, steps = rng.randrange(2), []
        for _ in range(10):
            a = 0 if rng.random() < mu(0, x) else 1
            outcomes = SWITCH[x, a]
            p, r, y = outcomes[0] if len(outcomes) == 1 or rng.random() < 0.5 else outcomes[1]
            steps.append((x, a, float(r)))
            x = y
        v_trace(steps, x, v, pi, mu, 0.9, 1.0, 1.0, alpha=0.01)
    assert max(abs(v[x] - float(target[x])) for x in v) < 0.15
