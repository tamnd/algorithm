# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conservative-q-learning/. The authors are listed in prov/QCDBQ4.jsonl.

import random
from fractions import Fraction as F

from conservative_q_learning import cql_evaluate, cql_h, fqi, greedy, policy_q

GAMMA = 0.9


def corridor(s, a):
    """States 0..3; action 0 moves right (done after state 3), 1 stays, 2 moves left.
    Every step costs 1."""
    if a == 0:
        return -1, s + 1, s == 3
    if a == 1:
        return -1, s, False
    return -1, max(s - 1, 0), False


def corridor_data():
    """The behavior policy moves right 4 times out of 5 and stays once; it never moves left."""
    data = []
    for s in range(4):
        for a in (0, 0, 0, 0, 1):
            r, s2, done = corridor(s, a)
            data.append((s, a, r, s2, done))
    return data


def as_policy(actions, n_actions):
    return [[F(1) if a == b else F(0) for a in range(n_actions)] for b in actions]


def test_cql_is_below_true_values_on_missing_actions_and_fqi_is_above():
    data = corridor_data()
    qstar = policy_q(corridor, as_policy([0] * 4, 3), 4, 3, F(9, 10))
    for alpha in (0.5, 1.0, 2.0):
        q = cql_h(data, 4, 3, GAMMA, alpha, 100, 50, 2.0)
        pol = greedy(q)
        assert pol == [0, 0, 0, 0]  # the optimal policy: always move right
        qpi = policy_q(corridor, as_policy(pol, 3), 4, 3, F(9, 10))
        for s in range(4):
            assert q[s][2] < float(qpi[s][2]) - 1.0  # left is never in the data
    qf = fqi(data, 4, 3, GAMMA, 200)
    for s in range(4):
        assert qf[s][2] == 0.0
        assert qf[s][2] > float(qstar[s][2])
    # FQI then prefers the unseen action, and that policy is far from optimal
    pf = greedy(qf)
    assert pf == [2, 2, 2, 2]
    vf = policy_q(corridor, as_policy(pf, 3), 4, 3, F(9, 10))
    assert vf[0][2] == -10 and qstar[0][0] == F(-3439, 1000)


def test_cql_penalty_lowers_missing_actions_more_with_larger_alpha():
    data = corridor_data()
    q1 = cql_h(data, 4, 3, GAMMA, 0.5, 100, 50, 2.0)
    q2 = cql_h(data, 4, 3, GAMMA, 2.0, 100, 50, 2.0)
    for s in range(4):
        assert q2[s][2] < q1[s][2]
        assert q2[s][1] < q1[s][1]


def random_instance(rng):
    S, A = 4, 3
    table = {(s, a): (rng.randint(-3, 3), rng.randrange(S), rng.random() < 0.15)
             for s in range(S) for a in range(A)}

    def step(s, a):
        return table[(s, a)]

    data = []
    for s in range(S):
        for a in range(A):
            r, s2, done = step(s, a)
            data += [(s, a, r, s2, done)] * rng.randint(1, 4)
    pi = []
    for s in range(S):
        w = [F(rng.randint(1, 5)) for _ in range(A)]
        pi.append([x / sum(w) for x in w])
    return step, data, pi


def test_theorem_3_2_value_lower_bound_with_exact_backups():
    # With a deterministic MDP and data that holds every pair, B-hat = B, so any alpha > 0
    # gives E_pi Qhat(s, .) <= V^pi(s) in every state (Theorem 3.2).
    rng = random.Random(7)
    pointwise_above = 0
    for _ in range(40):
        step, data, pi = random_instance(rng)
        qpi = policy_q(step, pi, 4, 3, F(9, 10))
        pif = [[float(p) for p in row] for row in pi]
        for alpha in (0.1, 1.0):
            qhat = cql_evaluate(data, pif, 4, 3, GAMMA, alpha, 400)
            for s in range(4):
                vhat = sum(p * x for p, x in zip(pif[s], qhat[s]))
                vpi = float(sum(p * x for p, x in zip(pi[s], qpi[s])))
                assert vhat <= vpi + 1e-9
                pointwise_above += sum(qhat[s][a] > float(qpi[s][a]) + 1e-9 for a in range(3))
    # Theorem 3.2 bounds the value, not each Q(s, a): some pairs do lie above Q^pi.
    assert pointwise_above > 0


def test_cql_evaluate_with_zero_alpha_is_exact_evaluation():
    rng = random.Random(8)
    step, data, pi = random_instance(rng)
    qpi = policy_q(step, pi, 4, 3, F(9, 10))
    qhat = cql_evaluate(data, [[float(p) for p in r] for r in pi], 4, 3, GAMMA, 0.0, 400)
    for s in range(4):
        for a in range(3):
            assert abs(qhat[s][a] - float(qpi[s][a])) < 1e-9
