# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/retrace/. The authors are listed in prov/Y7PV00.jsonl.

import random
from fractions import Fraction as F

from retrace import expected_operator, q_pi, retrace, trace_coefficient

KINDS = ("retrace", "tree-backup", "q-pi-lambda")
ACTIONS = [0, 1]


def table_policy(rows):
    return lambda a, x: rows[x][a]


def dist(q1, q2):
    return max(abs(q1[k] - q2[k]) for k in q1)


# Layered episodic MDP: s, then u or v, then possibly w, then the end.
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


def trajectories(x, a):
    """All (probability, steps) of episodes that start with action a in state x and then follow L_MU."""
    for p, r, y in LAYERED[x, a]:
        if y is None:
            yield p, [(x, a, r)]
            continue
        for b in ACTIONS:
            for p2, rest in trajectories(y, b):
                yield p * L_MU(b, y) * p2, [(x, a, r)] + rest


def test_mean_target_is_the_expected_operator() -> None:
    rng = random.Random(0)
    q = {k: F(rng.randrange(-5, 6), 3) for k in LAYERED}
    for gamma in (F(1), F(9, 10)):
        for kind in KINDS:
            for lam in (F(1), F(1, 2)):
                rq = expected_operator(q, LAYERED, L_PI, L_MU, ACTIONS, gamma, lam, kind)
                for x_a in LAYERED:
                    mean = sum(p * retrace(steps, None, dict(q), L_PI, L_MU, ACTIONS, gamma, lam, 0, kind)[0] for p, steps in trajectories(*x_a))
                    assert mean == rq[x_a]


def test_backward_recursion_is_the_sum_of_traced_td_errors() -> None:
    rng = random.Random(1)
    q = {k: F(rng.randrange(-5, 6), 2) for k in LAYERED}
    gamma, lam = F(9, 10), F(4, 5)
    for _, steps in trajectories("s", 1):
        targets = retrace(steps, None, dict(q), L_PI, L_MU, ACTIONS, gamma, lam, 0)
        nxt = [x for x, _, _ in steps[1:]] + [None]
        delta = [r + gamma * sum(L_PI(b, y) * q[y, b] for b in ACTIONS) - q[x, a] if y else r - q[x, a] for (x, a, r), y in zip(steps, nxt)]
        for t, (x, a, _) in enumerate(steps):
            total, trace = q[x, a], F(1)
            for s in range(t, len(steps)):
                if s > t:
                    xs, as_, _ = steps[s]
                    trace *= gamma * lam * min(1, L_PI(as_, xs) / L_MU(as_, xs))
                total += trace * delta[s]
            assert targets[t] == total


# Switch MDP: action 0 moves to the other state, action 1 stays. Discounted, no end.
SWITCH = {
    (0, 0): [(F(1), F(1), 1)],
    (0, 1): [(F(1), F(0), 0)],
    (1, 0): [(F(1), F(0), 0)],
    (1, 1): [(F(1), F(2), 1)],
}
G = F(9, 10)


def same_in_both(p0):
    return table_policy({0: [p0, 1 - p0], 1: [p0, 1 - p0]})


def iterate(kind, pi, mu, lam, k, q=None):
    q = q or {key: F(0) for key in SWITCH}
    out = [q]
    for _ in range(k):
        q = expected_operator(q, SWITCH, pi, mu, ACTIONS, G, lam, kind)
        out.append(q)
    return out


def test_q_pi_is_the_fixed_point_of_all_three() -> None:
    pi, mu = same_in_both(F(7, 10)), same_in_both(F(3, 10))
    target = q_pi(SWITCH, pi, ACTIONS, G)
    for kind in KINDS:
        assert expected_operator(target, SWITCH, pi, mu, ACTIONS, G, F(1), kind) == target


def test_retrace_and_tree_backup_contract_exactly() -> None:
    rng = random.Random(2)
    for _ in range(3):
        rows = {x: [F(rng.randrange(0, 11), 10)] for x in (0, 1)}
        mrows = {x: [F(rng.randrange(1, 10), 10)] for x in (0, 1)}
        pi = table_policy({x: [p[0], 1 - p[0]] for x, p in rows.items()})
        mu = table_policy({x: [p[0], 1 - p[0]] for x, p in mrows.items()})
        target = q_pi(SWITCH, pi, ACTIONS, G)
        for kind in ("retrace", "tree-backup"):
            qs = iterate(kind, pi, mu, F(1), 6, {k: F(rng.randrange(-9, 10)) for k in SWITCH})
            for a, b in zip(qs, qs[1:]):
                assert dist(b, target) <= G * dist(a, target)


def test_q_pi_lambda_diverges_far_off_policy() -> None:
    pi, mu = same_in_both(F(1)), same_in_both(F(1, 10))
    target = q_pi(SWITCH, pi, ACTIONS, G)
    qs = iterate("q-pi-lambda", pi, mu, F(1), 8)
    assert dist(qs[8], target) > 10**5 * dist(qs[0], target)
    qs = iterate("retrace", pi, mu, F(1), 8)
    assert dist(qs[8], target) <= G**8 * dist(qs[0], target)


def test_on_policy_retrace_with_lambda_one_is_exact_in_one_step() -> None:
    pi = same_in_both(F(1, 2))
    target = q_pi(SWITCH, pi, ACTIONS, G)
    assert iterate("retrace", pi, pi, F(1), 1)[1] == target
    assert iterate("tree-backup", pi, pi, F(1), 1)[1] != target


def test_sampled_retrace_learns_q_pi() -> None:
    pi, mu = same_in_both(0.7), same_in_both(0.3)
    target = {k: float(v) for k, v in q_pi(SWITCH, same_in_both(F(7, 10)), ACTIONS, G).items()}
    rng = random.Random(0)
    q = {k: 0.0 for k in SWITCH}
    for episode in range(4000):
        x, steps = rng.randrange(2), []
        for _ in range(8):
            a = 0 if rng.random() < mu(0, x) else 1
            _, r, y = SWITCH[x, a][0]
            steps.append((x, a, float(r)))
            x = y
        retrace(steps, x, q, pi, mu, ACTIONS, 0.9, 1.0, 0.02)
    assert max(abs(q[k] - target[k]) for k in q) < 0.01


def test_trace_coefficients() -> None:
    assert trace_coefficient("retrace", 1, F(1, 2), F(1, 4)) == 1
    assert trace_coefficient("retrace", 1, F(1, 4), F(1, 2)) == F(1, 2)
    assert trace_coefficient("tree-backup", F(1, 2), F(1, 4), F(1, 2)) == F(1, 8)
    assert trace_coefficient("importance-sampling", 1, F(1, 2), F(1, 4)) == 2
