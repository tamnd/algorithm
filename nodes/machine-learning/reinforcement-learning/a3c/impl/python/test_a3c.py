# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a3c/. The authors are listed in prov/VZH9DA.jsonl.

import math
import random

from a3c import a3c, random_schedule, rollout, softmax, worker_gradient

P = [[[0.5, 0.25], [0.0, 0.75]], [[0.5, 0.0], [0.0, 0.0]]]
R = [[1.0, 0.0], [0.0, 3.0]]
MU = [1.0, 0.0]
PHI = [[1.0, 0.0], [0.0, 1.0]]
GAMMA, ETA, BETA, CV = 0.5, 0.1, 0.01, 0.5


def a2c_step(theta, w, segments, eta):
    """Oracle: one synchronous A2C step with summed n-step advantage gradients, written from the formulas."""
    pi = [[math.exp(x) / sum(math.exp(y) for y in row) for x in row] for row in theta]
    th = [row[:] for row in theta]
    ww = list(w)
    for states, actions, rewards, last, ended in segments:
        n = len(states)
        for t in range(n):
            G = sum(GAMMA ** (j - t) * rewards[j] for j in range(t, n))
            if not ended:
                G += GAMMA ** (n - t) * w[last]
            s, a = states[t], actions[t]
            A = G - w[s]
            H = -sum(p * math.log(p) for p in pi[s])
            for b in range(2):
                dH = -pi[s][b] * (math.log(pi[s][b]) + H)
                th[s][b] += eta * (A * ((1 if a == b else 0) - pi[s][b]) + BETA * dH)
            ww[s] += eta * CV * A
    return th, ww


def close(x, y):
    return all(abs(a - b) < 1e-9 for a, b in zip(x, y))


def run(schedule, n_workers, seed=0):
    log = []
    th0 = [[0.2, -0.1], [0.0, 0.3]]
    w0 = [0.5, 1.0]
    th, w = a3c(P, R, MU, GAMMA, th0, w0, PHI, n_workers, 5, schedule, ETA, random.Random(seed), beta=BETA, c_v=CV, log=log)
    return th0, w0, th, w, log


def test_zero_delay_equals_sequential_a2c():
    n_workers = 3
    schedule = [i for _ in range(4) for i in range(n_workers) for _ in range(2)]  # read i, write i, read j, write j, ...
    th0, w0, th, w, log = run(schedule, n_workers)
    cur_th, cur_w = th0, w0
    for _, th_read, w_read, seg in log:
        assert all(close(a, b) for a, b in zip(th_read, cur_th)) and close(w_read, cur_w)  # every read sees the latest parameters
        cur_th, cur_w = a2c_step(cur_th, cur_w, [seg], ETA)
    assert all(close(a, b) for a, b in zip(th, cur_th)) and close(w, cur_w)


def test_fully_stale_round_equals_one_batched_a2c_step():
    n_workers = 4
    schedule = list(range(n_workers)) * 2  # all read, then all write
    th0, w0, th, w, log = run(schedule, n_workers)
    assert all(th_read == th0 and w_read == w0 for _, th_read, w_read, _ in log)
    th2, w2 = a2c_step(th0, w0, [seg for *_, seg in log], ETA)
    assert all(close(a, b) for a, b in zip(th, th2)) and close(w, w2)


def test_stale_gradient_is_applied_to_newer_parameters():
    # worker 0 reads, worker 1 reads and writes, then worker 0 writes its old gradient
    th0, w0, th, w, log = run([0, 1, 1, 0], 2)
    (_, _, _, seg0), (_, _, _, seg1) = log
    mid_th, mid_w = a2c_step(th0, w0, [seg1], ETA)
    g0_th, g0_w = a2c_step(th0, w0, [seg0], ETA)  # computed at theta_0
    expect_th = [[m + (g - t) for m, g, t in zip(r1, r2, r3)] for r1, r2, r3 in zip(mid_th, g0_th, th0)]
    expect_w = [m + (g - t) for m, g, t in zip(mid_w, g0_w, w0)]
    assert all(close(a, b) for a, b in zip(th, expect_th)) and close(w, expect_w)
    assert th != a2c_step(mid_th, mid_w, [seg0], ETA)[0]  # it differs from a fresh gradient at the newer point


def test_worker_gradient_terminal_and_bootstrap():
    seg = ([0, 1], [0, 1], [1.0, 3.0], None, True)
    d_th, d_w = worker_gradient([[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0], PHI, seg, 0.5, 0.0)
    assert d_th == [[1.25, -1.25], [-1.5, 1.5]]
    assert d_w == [2.5, 3.0]
    seg = ([0], [1], [0.0], 1, False)
    d_th, d_w = worker_gradient([[0.0, 0.0], [0.0, 0.0]], [0.0, 2.0], PHI, seg, 0.5, 0.0)
    assert d_w == [1.0, 0.0] and d_th[0] == [-0.5, 0.5]


def test_rollout_stops_at_the_end():
    rng = random.Random(4)
    for _ in range(200):
        states, actions, rewards, last, ended = rollout(P, R, MU, [[0.5, 0.5], [0.5, 0.5]], None, 5, rng)
        assert len(states) <= 5 and ended == (last is None)
        if ended:
            s, a = states[-1], actions[-1]
            assert sum(P[s][a]) < 1


def test_random_schedule_alternates():
    sched = random_schedule(4, 50, random.Random(1))
    seen = [0] * 4
    for i in sched:
        seen[i] += 1
    assert sum(seen) == 100 and all(x % 2 == 0 for x in seen)


def test_learning_with_random_interleaving():
    sched = random_schedule(4, 600, random.Random(7))
    th, w = a3c(P, R, MU, GAMMA, [[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0], PHI, 4, 5, sched, 0.1, random.Random(3), beta=0.01)
    pi = softmax(th)
    assert pi[0][0] > 0.9 and pi[1][1] > 0.9
    assert abs(w[1] - 3.0) < 0.5
