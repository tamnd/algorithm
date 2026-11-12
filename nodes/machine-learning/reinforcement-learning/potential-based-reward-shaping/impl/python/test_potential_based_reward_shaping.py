# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/potential-based-reward-shaping/. The authors are listed in prov/C2XHTJ.jsonl.

import random
from fractions import Fraction as F

from potential_based_reward_shaping import (optimal_action_sets, optimal_q, recover_q,
                                            shape_mdp, shaped_q_learning)

GAMMA = F(9, 10)


def corridor():
    """States 0..3; action 0 moves left (stays at 0), action 1 moves right.
    Moving right from 3 ends the episode with reward 1; other rewards are 0."""
    mdp = {}
    for s in range(4):
        mdp[(s, 0)] = [(F(1), F(0), max(s - 1, 0), False)]
        mdp[(s, 1)] = [(F(1), F(1), s, True)] if s == 3 else [(F(1), F(0), s + 1, False)]
    return mdp


def random_mdp(rng, n_states, n_actions):
    mdp = {}
    for s in range(n_states):
        for a in range(n_actions):
            k = rng.randint(1, 3)
            w = [rng.randint(1, 4) for _ in range(k)]
            outs = []
            for wi in w:
                done = rng.random() < 0.2
                outs.append((F(wi, sum(w)), F(rng.randint(-4, 4)), rng.randrange(n_states), done))
            mdp[(s, a)] = outs
    return mdp


def test_shaped_optimal_q_is_q_minus_phi():
    rng = random.Random(3)
    for _ in range(60):
        n, m = rng.randint(2, 4), rng.randint(2, 3)
        mdp = random_mdp(rng, n, m)
        phi = {s: F(rng.randint(-6, 6), rng.randint(1, 3)) for s in range(n)}
        q, _ = optimal_q(mdp, GAMMA)
        qs, _ = optimal_q(shape_mdp(mdp, phi, GAMMA), GAMMA)
        for s in range(n):
            assert qs[s] == [x - phi[s] for x in q[s]]
        assert recover_q(qs, phi) == q
        assert optimal_action_sets(qs) == optimal_action_sets(q)


def test_corridor_values():
    q, pol = optimal_q(corridor(), GAMMA)
    assert all(pol[s] == 1 for s in range(4))
    assert [q[s][1] for s in range(4)] == [GAMMA ** (3 - s) for s in range(4)]
    phi = {s: F(s, 2) for s in range(4)}
    qs, pols = optimal_q(shape_mdp(corridor(), phi, GAMMA), GAMMA)
    assert pols == pol
    assert q[0] == [F(6561, 10000), F(729, 1000)]
    assert qs[0] == [F(6561, 10000), F(729, 1000)]
    assert q[3] == [F(81, 100), F(1)]
    assert qs[3] == [F(-69, 100), F(-1, 2)]


def test_a_bonus_that_is_not_potential_based_changes_the_optimal_policy():
    # A bonus of c for every move to the right, and nothing for moves to the left.
    c = F(1, 2)
    mdp = corridor()
    bonus = {k: [(p, r + (c if k[1] == 1 else 0), s2, d) for p, r, s2, d in v]
             for k, v in mdp.items()}
    q, pol = optimal_q(bonus, GAMMA)
    assert pol[3] == 0  # step back and forth for ever instead of finishing
    # cycling from state 3: gamma c / (1 - gamma^2); finishing: 1 + c
    assert q[3][0] == GAMMA * c / (1 - GAMMA ** 2)
    assert q[3][1] == 1 + c
    assert q[3][0] > q[3][1]
    # the true return of that policy is 0, against gamma^(3 - s) for the optimal one
    true_q, _ = optimal_q(corridor(), GAMMA)
    assert true_q[3][1] == 1


def test_q_learning_with_shaping_equals_q_learning_with_phi_as_initial_values():
    # Wiewiora (2003): on the same transitions, shaped Q-learning from Q0 and plain
    # Q-learning from Q0 + Phi stay exactly Phi(s) apart.
    rng = random.Random(9)
    mdp = random_mdp(rng, 4, 2)
    phi = {s: F(rng.randint(-5, 5)) for s in range(4)}
    trans = []
    s = 0
    for _ in range(300):
        a = rng.randrange(2)
        outs = mdp[(s, a)]
        p, r, s2, done = outs[rng.randrange(len(outs))]
        trans.append((s, a, r, s2, done))
        s = rng.randrange(4) if done else s2
    q0 = {s: [F(0), F(0)] for s in range(4)}
    zero = {s: F(0) for s in range(4)}
    for k in (1, 10, 50, 300):
        qs = shaped_q_learning(trans[:k], q0, phi, GAMMA, F(1, 2))
        qp = shaped_q_learning(trans[:k], recover_q(q0, phi), zero, GAMMA, F(1, 2))
        assert recover_q(qs, phi) == qp
