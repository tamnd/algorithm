# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dagger/. The authors are listed in prov/C2SKZR.jsonl.

import random

from dagger import (ACTIONS, Lane, TableLearner, behavior_cloning, dagger, expected_cost,
                    expert, expert_action, expert_gap, loss, rollout, state_distributions)


def full_table(env, eps=0.1):
    return TableLearner([(x, expert_action(x)) for x in env.states()], eps)


def random_table(env, rng, eps):
    return TableLearner([(x, rng.choice(ACTIONS)) for x in env.states() if rng.random() < 0.7], eps)


def expert_q(env):
    """q[k][x][a]: cost of a in x, then the expert, with k steps in all."""
    v = {x: 0.0 for x in env.states()}
    q = [None]
    for _ in range(env.T):
        qk = {x: {a: env.cost(x) + v[env.next_state(x, a)] for a in ACTIONS} for x in env.states()}
        q.append(qk)
        v = {x: qk[x][expert_action(x)] for x in env.states()}
    return q


def test_expert_is_perfect_and_gap():
    env = Lane()
    assert expected_cost(env, expert) == 0.0
    assert expert_gap(env) == 2.0


def test_behavior_cloning_drifts():
    env = Lane()
    bc = behavior_cloning(env, 5, random.Random(0))
    assert bc.table == {0: -1}  # the expert never leaves x = 0
    assert abs(loss(env, bc, expert) - 0.1 * 2 / 3) < 1e-12
    assert expected_cost(env, bc) > 15.0
    assert expected_cost(env, bc) > 20 * expected_cost(env, full_table(env))


def test_dagger_recovers():
    env = Lane()
    best = expected_cost(env, full_table(env))
    learned = dagger(env, 5, 1, random.Random(0))
    assert len(learned) == 6
    assert learned[1].table == {0: -1}  # beta_1 = 1: the first round is behavior cloning
    for pol in learned[2:]:
        assert abs(expected_cost(env, pol) - best) < 1e-6
        assert all(a == expert_action(x) for x, a in pol.table.items())
        assert abs(loss(env, pol, pol) - 0.1 * 2 / 3) < 1e-9
    wins = 0
    for seed in range(20):
        last = dagger(env, 5, 1, random.Random(seed))[-1]
        bc = behavior_cloning(env, 5, random.Random(seed))
        assert expected_cost(env, last) < expected_cost(env, bc)
        wins += abs(expected_cost(env, last) - best) < 1e-6
    assert wins >= 15


def test_beta_one_everywhere_is_behavior_cloning():
    env = Lane()
    learned = dagger(env, 4, 2, random.Random(3), betas=[1.0] * 4)
    assert learned[-1].table == {0: -1}


def test_bounds_of_ross_and_bagnell():
    env = Lane(half_width=6, horizon=25)
    u = expert_gap(env)
    rng = random.Random(1)
    policies = [behavior_cloning(env, 2, rng)] + dagger(env, 4, 1, rng)
    policies += [random_table(env, rng, eps) for eps in (0.0, 0.05, 0.3, 1.0) for _ in range(10)]
    for pol in policies:
        j = expected_cost(env, pol)
        assert j <= 0.0 + env.T ** 2 * loss(env, pol, expert) + 1e-9  # Theorem 2.1
        assert j <= 0.0 + u * env.T * loss(env, pol, pol) + 1e-9  # Theorem 2.2 bound


def test_performance_difference_identity():
    env = Lane(half_width=5, horizon=15)
    q = expert_q(env)
    rng = random.Random(2)
    for _ in range(10):
        pol = random_table(env, rng, 0.2)
        dists = state_distributions(env, pol)
        total = 0.0
        for t, d in enumerate(dists):
            k = env.T - t
            for x, p in d.items():
                total += p * sum(pa * (q[k][x][a] - q[k][x][expert_action(x)])
                                 for a, pa in pol(x).items())
        assert abs(expected_cost(env, pol) - total) < 1e-9


def test_exact_distributions_match_simulation():
    env = Lane(half_width=6, horizon=12)
    pol = TableLearner([(0, -1)], 0.1)
    exact = state_distributions(env, pol)[-1]
    rng = random.Random(4)
    runs = 20000
    counts = {}
    for _ in range(runs):
        x = rollout(env, pol, rng)[-1]
        counts[x] = counts.get(x, 0) + 1
    for x in env.states():
        assert abs(counts.get(x, 0) / runs - exact.get(x, 0.0)) < 0.015
