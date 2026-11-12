# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dqn/. The authors are listed in prov/5J3KX3.jsonl.

import random

from dqn import QNet, dqn, dqn_target, huber_grad

L = 6
GAMMA = 0.9


def chain(s, a):
    """States 0..5, action 1 moves right, action 0 moves left; right from 5 ends with reward 1."""
    if a == 1:
        if s == L - 1:
            return 1.0, s, True
        return 0.0, s + 1, False
    return 0.0, max(s - 1, 0), False


def q_star(s, a):
    if a == 1:
        return GAMMA ** (L - 1 - s)
    return GAMMA * GAMMA ** (L - 1 - max(s - 1, 0))


def test_reaches_optimal_greedy_policy():
    for seed in (0, 1, 2):
        net = dqn(chain, L, 2, 0, GAMMA, 3000, 1000, 16, 50, 0.05, 16, random.Random(seed))
        for s in range(L):
            q = net.q(s)
            assert q[1] > q[0]
            assert abs(q[1] - q_star(s, 1)) < 0.02


def test_target_network_fixed_between_syncs():
    trace = []
    dqn(chain, L, 2, 0, GAMMA, 400, 1000, 8, 50, 0.05, 8, random.Random(5), trace=trace)
    prev = trace[0][1]
    changes = []
    for t, target, online in trace:
        if t % 50 == 0:
            assert target == online
        else:
            assert target == prev
        if target != prev:
            changes.append(t)
        prev = target
    # the online network trains from step 100 (the warm-up), so the syncs after it change the target
    assert changes == [100, 150, 200, 250, 300, 350, 400]


def test_huber_gradient_is_clipped_error():
    assert huber_grad(0.3) == 0.3
    assert huber_grad(-0.3) == -0.3
    assert huber_grad(2.5) == 1.0
    assert huber_grad(-7.0) == -1.0
    assert huber_grad(3.0, kappa=2.0) == 2.0


def test_target_terminal_and_bootstrap():
    net = QNet(3, 2, 4, random.Random(0))
    assert dqn_target(0.5, 1, True, net, GAMMA) == 0.5
    assert abs(dqn_target(0.5, 1, False, net, GAMMA) - (0.5 + GAMMA * max(net.q(1)))) < 1e-15


def loss(net, batch):
    total = 0.0
    for s, a, y in batch:
        d = y - net.q(s)[a]
        total += 0.5 * d * d if abs(d) <= 1 else abs(d) - 0.5
    return total / len(batch)


def test_sgd_step_matches_finite_differences():
    rng = random.Random(12)
    net = QNet(4, 3, 5, rng)
    batch = [(rng.randrange(4), rng.randrange(3), rng.uniform(-3, 3)) for _ in range(6)]
    h = 1e-6
    lr = 1e-3
    for name in ("w1", "w2"):
        mat = getattr(net, name)
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                old = mat[i][j]
                mat[i][j] = old + h
                up = loss(net, batch)
                mat[i][j] = old - h
                down = loss(net, batch)
                mat[i][j] = old
                fd = (up - down) / (2 * h)
                probe = QNet(4, 3, 5, random.Random(0))
                probe.copy_from(net)
                probe.sgd_step(batch, lr)
                step = (old - getattr(probe, name)[i][j]) / lr
                assert abs(step - fd) < 1e-5


def test_q_has_one_output_per_action():
    net = QNet(5, 4, 3, random.Random(1))
    assert len(net.q(2)) == 4
    assert len(net.params()) == 5 * 3 + 3 + 3 * 4 + 4
