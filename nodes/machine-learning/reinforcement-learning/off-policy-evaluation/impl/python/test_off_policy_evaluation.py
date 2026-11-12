# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/off-policy-evaluation/. The authors are listed in prov/982C79.jsonl.

from fractions import Fraction as F

from off_policy_evaluation import (
    direct_method,
    doubly_robust,
    inverse_propensity,
    self_normalized_ips,
    sequential_doubly_robust,
)

# Bandit: 2 equally likely contexts, 3 actions, Bernoulli rewards with mean Q[x][a].
ACTIONS = [0, 1, 2]
Q = {0: [F(1, 5), F(1, 2), F(9, 10)], 1: [F(3, 5), F(3, 10), F(1, 10)]}
PI = {0: [F(0), F(1, 5), F(4, 5)], 1: [F(1), F(0), F(0)]}
MU = {0: [F(1, 3)] * 3, 1: [F(1, 3)] * 3}
MU_WRONG = {0: [F(1, 2), F(1, 4), F(1, 4)], 1: [F(1, 4), F(1, 4), F(1, 2)]}
V_PI = F(71, 100)


def pol(table):
    return lambda a, x: table[x][a]


def q_right(x, a):
    return Q[x][a]


def q_wrong(x, a):
    return Q[x][a] + F(1, 10) * (a - 1) + F(1, 20)


def outcomes():
    """All (probability, single-sample dataset) under the true behavior policy MU."""
    for x in (0, 1):
        for a in ACTIONS:
            for r, pr in ((1, Q[x][a]), (0, 1 - Q[x][a])):
                yield F(1, 2) * MU[x][a] * pr, [(x, a, r)]


def mean(estimator):
    return sum(p * estimator(d) for p, d in outcomes())


def variance(estimator):
    m = mean(estimator)
    return sum(p * (estimator(d) - m) ** 2 for p, d in outcomes())


def test_true_value() -> None:
    assert sum(F(1, 2) * sum(PI[x][a] * Q[x][a] for a in ACTIONS) for x in (0, 1)) == V_PI


def test_doubly_robust_unbiased_if_either_part_is_right() -> None:
    assert mean(lambda d: doubly_robust(d, pol(PI), pol(MU), q_wrong, ACTIONS)) == V_PI
    assert mean(lambda d: doubly_robust(d, pol(PI), pol(MU_WRONG), q_right, ACTIONS)) == V_PI
    assert mean(lambda d: doubly_robust(d, pol(PI), pol(MU_WRONG), q_wrong, ACTIONS)) != V_PI


def test_dm_and_ips_need_their_own_part() -> None:
    assert mean(lambda d: direct_method(d, pol(PI), q_right, ACTIONS)) == V_PI
    assert mean(lambda d: direct_method(d, pol(PI), q_wrong, ACTIONS)) != V_PI
    assert mean(lambda d: inverse_propensity(d, pol(PI), pol(MU))) == V_PI
    assert mean(lambda d: inverse_propensity(d, pol(PI), pol(MU_WRONG))) != V_PI


def test_doubly_robust_reduces_variance_with_a_good_model() -> None:
    ips = variance(lambda d: inverse_propensity(d, pol(PI), pol(MU)))
    dr_good = variance(lambda d: doubly_robust(d, pol(PI), pol(MU), q_right, ACTIONS))
    dr_bad = variance(lambda d: doubly_robust(d, pol(PI), pol(MU), q_wrong, ACTIONS))
    assert dr_good < dr_bad < ips


def test_self_normalized_on_two_samples_is_biased() -> None:
    m = 0
    for p1, d1 in outcomes():
        for p2, d2 in outcomes():
            m += p1 * p2 * self_normalized_ips(d1 + d2, pol(PI), pol(MU))
    assert m == F(2741, 5400) != V_PI


# Sequential: a two-stage MDP. Stage 0 has state "s"; stage 1 has states "u" and "v"; then the end.
SEQ_ACTIONS = [0, 1]
TRANS = {
    ("s", 0): [(F(1, 2), F(1), "u"), (F(1, 2), F(0), "v")],
    ("s", 1): [(F(1, 4), F(2), "u"), (F(3, 4), F(-1), "v")],
    ("u", 0): [(F(1), F(3), None)],
    ("u", 1): [(F(1, 3), F(6), None), (F(2, 3), F(0), None)],
    ("v", 0): [(F(1, 2), F(4), None), (F(1, 2), F(-4), None)],
    ("v", 1): [(F(1), F(1), None)],
}
SEQ_PI = {"s": [F(1, 4), F(3, 4)], "u": [F(1, 2), F(1, 2)], "v": [F(1, 5), F(4, 5)]}
SEQ_MU = {"s": [F(1, 2), F(1, 2)], "u": [F(2, 3), F(1, 3)], "v": [F(1, 2), F(1, 2)]}
SEQ_MU_WRONG = {"s": [F(1, 3), F(2, 3)], "u": [F(1, 2), F(1, 2)], "v": [F(3, 4), F(1, 4)]}
G = F(9, 10)


def q_pi():
    q = {}
    for s in ("u", "v"):
        for a in SEQ_ACTIONS:
            q[s, a] = sum(p * r for p, r, _ in TRANS[s, a])
    v = {s: sum(SEQ_PI[s][a] * q[s, a] for a in SEQ_ACTIONS) for s in ("u", "v")}
    for a in SEQ_ACTIONS:
        q["s", a] = sum(p * (r + G * v[s2]) for p, r, s2 in TRANS["s", a])
    return q


def episodes(mu):
    for a0 in SEQ_ACTIONS:
        for p0, r0, s1 in TRANS["s", a0]:
            for a1 in SEQ_ACTIONS:
                for p1, r1, _ in TRANS[s1, a1]:
                    yield mu["s"][a0] * p0 * mu[s1][a1] * p1, [("s", a0, r0), (s1, a1, r1)]


def test_sequential_doubly_robust_unbiased_if_either_part_is_right() -> None:
    q = q_pi()
    v_pi = sum(SEQ_PI["s"][a] * q["s", a] for a in SEQ_ACTIONS)
    q_bad = {k: val + 1 for k, val in q.items()}
    assert sum(p for p, _ in episodes(SEQ_MU)) == 1

    def mean_dr(mu_hat, qh):
        return sum(p * sequential_doubly_robust([ep], pol(SEQ_PI), pol(mu_hat), lambda s, a: qh[s, a], SEQ_ACTIONS, G) for p, ep in episodes(SEQ_MU))

    assert mean_dr(SEQ_MU, q_bad) == v_pi
    assert mean_dr(SEQ_MU_WRONG, q) == v_pi
    assert mean_dr(SEQ_MU_WRONG, q_bad) != v_pi


def test_sequential_dr_with_zero_model_is_per_decision_is() -> None:
    for p, ep in episodes(SEQ_MU):
        rho, pdis = 1, 0
        for t, (s, a, r) in enumerate(ep):
            rho *= SEQ_PI[s][a] / SEQ_MU[s][a]
            pdis += G**t * rho * r
        assert sequential_doubly_robust([ep], pol(SEQ_PI), pol(SEQ_MU), lambda s, a: 0, SEQ_ACTIONS, G) == pdis
