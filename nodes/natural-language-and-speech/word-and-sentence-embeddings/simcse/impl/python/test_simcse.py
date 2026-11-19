# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simcse/. The authors are listed in prov/355PND.jsonl.

import math
import random

import pytest

from simcse import (
    alignment,
    cosine,
    cosine_grad,
    simcse_loss,
    simcse_loss_and_grad,
    simcse_loss_direct,
    uniformity,
)


def rand_matrix(rng, n, d):
    return [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(n)]


def noisy_copy(rng, H, sigma):
    return [[x + rng.gauss(0.0, sigma) for x in row] for row in H]


def numeric_grad(f, M, h=1e-6):
    g = []
    for i in range(len(M)):
        row = []
        for k in range(len(M[i])):
            old = M[i][k]
            M[i][k] = old + h
            up = f()
            M[i][k] = old - h
            down = f()
            M[i][k] = old
            row.append((up - down) / (2 * h))
        g.append(row)
    return g


def assert_close_matrix(A, B, tol):
    for ra, rb in zip(A, B):
        for x, y in zip(ra, rb):
            assert abs(x - y) <= tol, (x, y)


def test_page_example():
    H = [[1.0, 0.0], [0.0, 1.0]]
    Hp = [[1.0, 1.0], [-1.0, 1.0]]
    tau = 0.5
    c = 1 / math.sqrt(2)
    # z_11 = c / tau, z_12 = -c / tau, z_21 = z_22 = c / tau.
    l1 = math.log(math.exp(c / tau) + math.exp(-c / tau)) - c / tau
    l2 = math.log(2 * math.exp(c / tau)) - c / tau
    assert l2 == pytest.approx(math.log(2), abs=1e-12)
    assert simcse_loss(H, Hp, tau) == pytest.approx((l1 + l2) / 2, abs=1e-12)
    assert simcse_loss(H, Hp, tau) == pytest.approx(0.3753, abs=1e-4)


def test_matches_direct_formula():
    rng = random.Random(1)
    for tau in (1.0, 0.5, 0.05):
        H = rand_matrix(rng, 5, 4)
        Hp = noisy_copy(rng, H, 0.3)
        Hn = rand_matrix(rng, 5, 4)
        assert simcse_loss(H, Hp, tau) == pytest.approx(simcse_loss_direct(H, Hp, tau), rel=1e-12)
        assert simcse_loss(H, Hp, tau, Hn) == pytest.approx(simcse_loss_direct(H, Hp, tau, Hn), rel=1e-12)


def test_small_temperature_overflows_without_log_space():
    rng = random.Random(2)
    H = rand_matrix(rng, 4, 3)
    Hp = noisy_copy(rng, H, 0.1)
    with pytest.raises(OverflowError):
        simcse_loss_direct(H, Hp, 1e-3)
    loss = simcse_loss(H, Hp, 1e-3)
    assert math.isfinite(loss) and loss >= 0


@pytest.mark.parametrize("tau", [0.5, 0.05])
@pytest.mark.parametrize("hard", [False, True])
def test_gradient_against_central_differences(tau, hard):
    rng = random.Random(3)
    H = rand_matrix(rng, 4, 3)
    Hp = noisy_copy(rng, H, 0.5)
    Hn = rand_matrix(rng, 4, 3) if hard else None
    _, gH, gP, gN = simcse_loss_and_grad(H, Hp, tau, Hn)

    def f():
        return simcse_loss(H, Hp, tau, Hn)

    assert_close_matrix(gH, numeric_grad(f, H), 1e-5)
    assert_close_matrix(gP, numeric_grad(f, Hp), 1e-5)
    if hard:
        assert_close_matrix(gN, numeric_grad(f, Hn), 1e-5)
    else:
        assert gN is None


def test_cosine_gradient():
    rng = random.Random(4)
    a = [rng.gauss(0, 1) for _ in range(5)]
    b = [rng.gauss(0, 1) for _ in range(5)]
    ga, gb = cosine_grad(a, b)
    h = 1e-6
    for k in range(5):
        ap = list(a)
        am = list(a)
        ap[k] += h
        am[k] -= h
        assert ga[k] == pytest.approx((cosine(ap, b) - cosine(am, b)) / (2 * h), abs=1e-7)
        bp = list(b)
        bm = list(b)
        bp[k] += h
        bm[k] -= h
        assert gb[k] == pytest.approx((cosine(a, bp) - cosine(a, bm)) / (2 * h), abs=1e-7)
    # The cosine does not change along a, so its gradient is orthogonal to a.
    assert math.fsum(x * y for x, y in zip(ga, a)) == pytest.approx(0.0, abs=1e-12)


def test_gradient_is_orthogonal_to_each_vector():
    rng = random.Random(5)
    H = rand_matrix(rng, 6, 4)
    Hp = noisy_copy(rng, H, 0.2)
    _, gH, gP, _ = simcse_loss_and_grad(H, Hp, 0.05)
    for row, g in zip(H + Hp, gH + gP):
        assert math.fsum(x * y for x, y in zip(row, g)) == pytest.approx(0.0, abs=1e-9)


def test_scale_invariance():
    rng = random.Random(6)
    H = rand_matrix(rng, 5, 3)
    Hp = noisy_copy(rng, H, 0.3)
    scaled = [[3.0 * x for x in row] for row in H]
    assert simcse_loss(scaled, Hp) == pytest.approx(simcse_loss(H, Hp), rel=1e-12)


def test_single_sentence_has_zero_loss():
    loss, gH, gP, _ = simcse_loss_and_grad([[1.0, 2.0]], [[0.5, -1.0]], 0.05)
    assert loss == pytest.approx(0.0, abs=1e-15)
    assert all(abs(x) < 1e-15 for x in gH[0] + gP[0])


@pytest.mark.parametrize("n", [2, 3, 4])
def test_orthonormal_batch_closed_form(n):
    tau = 0.05
    E = [[1.0 if i == k else 0.0 for k in range(4)] for i in range(n)]
    expected = math.log(1 + (n - 1) * math.exp(-1 / tau))
    assert simcse_loss(E, E, tau) == pytest.approx(expected, rel=1e-9)


def test_loss_is_at_least_the_identical_pair_bound():
    rng = random.Random(7)
    for _ in range(50):
        n = rng.randint(2, 6)
        H = rand_matrix(rng, n, 3)
        Hp = noisy_copy(rng, H, 0.4)
        tau = rng.choice([0.05, 0.1, 1.0])
        # Each row has z_ii <= 1/tau and z_ij >= -1/tau, so l_i >= log(1 + (n - 1) exp(-2/tau)).
        bound = math.log(1 + (n - 1) * math.exp(-2 / tau))
        assert simcse_loss(H, Hp, tau) >= bound - 1e-12


def test_hard_negatives_raise_the_loss():
    rng = random.Random(8)
    H = rand_matrix(rng, 5, 4)
    Hp = noisy_copy(rng, H, 0.3)
    Hn = rand_matrix(rng, 5, 4)
    assert simcse_loss(H, Hp, 0.05, Hn) > simcse_loss(H, Hp, 0.05)


def test_gradient_steps_lower_the_loss():
    rng = random.Random(9)
    H = rand_matrix(rng, 6, 4)
    Hp = noisy_copy(rng, H, 1.0)
    tau = 0.1
    before = simcse_loss(H, Hp, tau)
    for _ in range(20):
        _, gH, gP, _ = simcse_loss_and_grad(H, Hp, tau)
        H = [[x - 0.05 * g for x, g in zip(r, gr)] for r, gr in zip(H, gH)]
        Hp = [[x - 0.05 * g for x, g in zip(r, gr)] for r, gr in zip(Hp, gP)]
    assert simcse_loss(H, Hp, tau) < before


def test_alignment_and_uniformity_hand_values():
    assert alignment([[1.0, 0.0]], [[2.0, 0.0]]) == pytest.approx(0.0)
    assert alignment([[1.0, 0.0]], [[0.0, 3.0]]) == pytest.approx(2.0)
    assert uniformity([[1.0, 0.0], [-1.0, 0.0]]) == pytest.approx(-8.0)
    square = [[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]]
    # Four pairs at squared distance 2 and two at 4.
    expected = math.log((4 * math.exp(-4) + 2 * math.exp(-8)) / 6)
    assert uniformity(square) == pytest.approx(expected)


def test_bad_input():
    with pytest.raises(ValueError):
        simcse_loss([], [])
    with pytest.raises(ValueError):
        simcse_loss([[1.0]], [[1.0], [2.0]])
    with pytest.raises(ValueError):
        simcse_loss([[1.0]], [[1.0]], tau=0.0)
    with pytest.raises(ValueError):
        cosine([0.0, 0.0], [1.0, 0.0])
