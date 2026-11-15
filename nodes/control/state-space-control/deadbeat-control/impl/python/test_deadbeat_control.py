# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadbeat-control/. The authors are listed in prov/HZQ8MT.jsonl.

import random
from fractions import Fraction

import pytest

import ctlmat as cm
from deadbeat_control import deadbeat_gain, nullspace, rref, steps_to_zero


def closed_loop(A, B, K):
    return cm.sub(A, cm.mul(B, K))


def nil_index(M):
    """Return the least N with M^N = 0 (exact), or None if M is not nilpotent."""
    n = len(M)
    P = cm.eye(n)
    for N in range(0, n + 1):
        if P == cm.zeros(n):
            return N
        P = cm.mul(M, P)
    return None


def ackermann_deadbeat(A, b):
    """Single-input deadbeat gain by Ackermann's formula with p(z) = z^n."""
    n = len(A)
    cols = [list(b)]
    for _ in range(n - 1):
        cols.append(cm.matvec(A, cols[-1]))
    q = cm.solve(cm.transpose(cm.transpose(cols)), [0] * (n - 1) + [1])
    return cm.mul([q], cm.mat_power(A, n))[0]


def run(A, B, K, x0, steps):
    x = list(x0)
    xs, us = [x], []
    for _ in range(steps):
        u = [-v for v in cm.matvec(K, x)]
        x = [a + b for a, b in zip(cm.matvec(A, x), cm.matvec(B, u))]
        xs.append(x)
        us.append(u)
    return xs, us


def test_zoh_double_integrator():
    for h in (Fraction(1, 10), Fraction(1, 4), Fraction(2)):
        A = [[1, h], [0, 1]]
        B = [[h * h / 2], [h]]
        K, N = deadbeat_gain(A, B)
        assert N == 2
        assert K == [[1 / h ** 2, Fraction(3, 2) / h]]
        xs, us = run(A, B, K, [1, 0], 2)
        assert xs[2] == [0, 0]
        assert us == [[-1 / h ** 2], [1 / h ** 2]]


def test_single_input_matches_ackermann():
    rng = random.Random(3)
    done = 0
    while done < 12:
        n = rng.randint(1, 5)
        A = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        b = [rng.randint(-2, 2) for _ in range(n)]
        W = cm.transpose([cm.matvec(cm.mat_power(A, k), b) for k in range(n)])
        if cm.det(W) == 0:
            continue
        K, N = deadbeat_gain(A, [[v] for v in b])
        assert N == n
        assert K[0] == ackermann_deadbeat(A, b)
        done += 1


def test_multi_input_minimum_time():
    rng = random.Random(4)
    for trial in range(25):
        n = rng.randint(2, 6)
        m = rng.randint(1, 3)
        A = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
        B = [[rng.randint(-1, 1) for _ in range(m)] for _ in range(n)]
        try:
            want = steps_to_zero(A, B)
        except ValueError:
            with pytest.raises(ValueError):
                deadbeat_gain(A, B)
            continue
        K, N = deadbeat_gain(A, B)
        assert N == want
        assert nil_index(closed_loop(A, B, K)) == N
        x0 = [rng.randint(-5, 5) for _ in range(n)]
        xs, _ = run(A, B, K, x0, N)
        assert xs[N] == [0] * n


def test_stated_three_state_example():
    A = [[1, 1, 0], [0, 1, 1], [0, 0, 1]]
    B = [[0, 0], [1, 0], [0, 1]]
    K, N = deadbeat_gain(A, B)
    assert N == 2
    Acl = closed_loop(A, B, K)
    assert cm.mat_power(Acl, 2) == cm.zeros(3)
    assert Acl != cm.zeros(3)


def test_singular_A_uncontrollable_zero_mode_is_fine():
    # The third state is not reachable but decays to 0 in one step by itself.
    A = [[0, 1, 0], [0, 0, 0], [0, 0, 0]]
    B = [[0], [1], [0]]
    K, N = deadbeat_gain(A, B)
    assert N == 2
    assert nil_index(closed_loop(A, B, K)) == 2


def test_unstable_uncontrollable_mode_rejected():
    A = [[1, 0], [0, 2]]
    B = [[1], [0]]
    with pytest.raises(ValueError):
        deadbeat_gain(A, B)
    with pytest.raises(ValueError):
        steps_to_zero(A, B)


def test_rref_and_nullspace():
    M = [[1, 2, 3], [2, 4, 6], [1, 0, 1]]
    R, piv = rref(M)
    assert piv == [0, 1]
    for v in nullspace(M):
        assert cm.matvec(M, v) == [0, 0, 0]
    assert len(nullspace(M)) == 1


def test_float_data():
    h = 0.1
    A = [[1.0, h], [0.0, 1.0]]
    B = [[h * h / 2], [h]]
    K, N = deadbeat_gain(A, B)
    assert N == 2
    assert abs(K[0][0] - 100.0) < 1e-9 and abs(K[0][1] - 15.0) < 1e-9
