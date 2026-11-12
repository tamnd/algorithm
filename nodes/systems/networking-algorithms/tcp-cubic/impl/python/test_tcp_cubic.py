# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tcp-cubic/. The authors are listed in prov/NC11TV.jsonl.

import random

import pytest

from tcp_cubic import BETA, C, Cubic, k_of, run_rounds, w_cubic


def test_k_and_end_points():
    k = k_of(100, 70)
    assert k == pytest.approx(75 ** (1 / 3)) and k == pytest.approx(4.2172, abs=1e-4)
    assert w_cubic(0, 100, k) == pytest.approx(70)
    assert w_cubic(k, 100, k) == pytest.approx(100)


def test_random_k_returns_to_w_max():
    rng = random.Random(9438)
    for _ in range(600):
        w_max = rng.uniform(2, 10000)
        epoch = rng.uniform(1, w_max)
        k = k_of(w_max, epoch)
        assert k >= 0
        assert w_cubic(0, w_max, k) == pytest.approx(epoch, rel=1e-9, abs=1e-9)
        assert w_cubic(k, w_max, k) == pytest.approx(w_max)


def test_concave_then_convex():
    k = k_of(100, 70)
    h = 0.05
    for i in range(1, 160):
        t = i * h
        second = w_cubic(t + h, 100, k) - 2 * w_cubic(t, 100, k) + w_cubic(t - h, 100, k)
        if t + h < k:
            assert second < 0
        elif t - h > k:
            assert second > 0
        assert w_cubic(t, 100, k) > w_cubic(t - h, 100, k)  # always increasing


def test_page_trace():
    cc = Cubic(100, 0.1)
    cc.on_loss(0.0)
    assert cc.cwnd == pytest.approx(70) and cc.w_max == 100
    tr = run_rounds(cc, 51, 1e9)
    got = [round(tr[i][1], 2) for i in range(0, 51, 10)]
    assert got == [70.0, 86.64, 95.61, 99.26, 99.99, 100.2]


def test_reno_friendly_region_for_small_windows():
    cc = Cubic(10, 0.1)
    cc.on_loss(0.0)
    run_rounds(cc, 5, 1e9)
    assert cc.region == "reno-friendly"
    big = Cubic(1000, 0.1)
    big.on_loss(0.0)
    run_rounds(big, 10, 1e9)
    assert big.region == "concave"


def test_growth_depends_on_time_not_rtt():
    windows = []
    for rtt in (0.05, 0.2):
        cc = Cubic(1000, rtt)
        cc.on_loss(0.0)
        run_rounds(cc, int(round(3.0 / rtt)), 1e9)
        windows.append(cc.cwnd)
    k = k_of(1000, 700)
    for w in windows:
        assert w == pytest.approx(w_cubic(3.0, 1000, k), rel=0.02)


def test_loss_period_close_to_k():
    cc = Cubic(1000, 0.1)
    cc.on_loss(0.0)
    tr = run_rounds(cc, 700, 1000.5)
    losses = [t for t, w, lost in tr if lost]
    gaps = [b - a for a, b in zip(losses, losses[1:])]
    k = k_of(1000, 700)
    assert len(gaps) >= 5
    assert all(0.85 * k < g < 1.05 * k for g in gaps[1:])


def test_decrease_and_fast_convergence():
    cc = Cubic(100, 0.1, fast_convergence=True)
    cc.on_loss(0.0)
    assert (cc.w_max, cc.cwnd) == (100, pytest.approx(70))
    cc.cwnd = 80.0
    cc.on_loss(1.0)
    assert cc.w_max == pytest.approx(80 * (1 + BETA) / 2)
    assert cc.cwnd == pytest.approx(56)
    assert cc.k == pytest.approx(((cc.w_max - 56) / C) ** (1 / 3))
