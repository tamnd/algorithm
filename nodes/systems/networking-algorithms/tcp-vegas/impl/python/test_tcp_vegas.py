# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tcp-vegas/. The authors are listed in prov/NPTDBB.jsonl.

import random

import pytest

from tcp_vegas import VegasFlow, queueing_delay, simulate


def test_page_example():
    flows, tr = simulate([20.0, 20.0], 1.0, 40)
    assert tr.windows[0] == [2, 2] and tr.windows[8] == [10, 10] and tr.delay[8] == 0
    assert tr.windows[9] == [11, 11] and tr.delay[9] == pytest.approx(2.0)
    assert tr.windows[-1] == [11, 11]
    assert [f.diff for f in flows] == pytest.approx([1.0, 1.0])
    assert sum(tr.rates[-1]) == pytest.approx(1.0)


def test_diff_counts_the_flow_backlog():
    f = VegasFlow(12)
    f.on_round(20.0)
    f.cwnd = 12
    f.on_round(24.0)  # 12 packets, 4 ms of queueing in a 24 ms RTT
    assert f.diff == pytest.approx(2.0)
    assert f.cwnd == 12  # inside [alpha, beta]: no change


def test_rules():
    f = VegasFlow(10, alpha=1, beta=3)
    f.on_round(10.0)
    assert f.cwnd == 11  # no queue: Diff = 0 < alpha
    f.on_round(20.0)  # Diff = 11 * (1 - 10/20) = 5.5 > beta
    assert f.cwnd == 10
    with pytest.raises(ValueError):
        VegasFlow(2, alpha=3, beta=1)


def test_queueing_delay():
    assert queueing_delay([5, 5], [20, 20], 1.0) == 0.0
    assert queueing_delay([15, 15], [20, 20], 1.0) == pytest.approx(10.0)
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randrange(1, 6)
        w = [rng.randrange(0, 50) for _ in range(n)]
        d = [rng.uniform(1, 50) for _ in range(n)]
        c = rng.uniform(0.1, 3)
        q = queueing_delay(w, d, c)
        total = sum(wi / (di + q) for wi, di in zip(w, d))
        if q > 0:
            assert total == pytest.approx(c, rel=1e-9)
        else:
            assert total <= c + 1e-12


def test_equilibrium_keeps_alpha_to_beta_packets_queued():
    rng = random.Random(1994)
    for _ in range(60):
        n = rng.randrange(1, 5)
        d = [float(rng.randrange(5, 60)) for _ in range(n)]
        c = rng.choice([0.5, 1.0, 2.0])
        flows, tr = simulate(d, c, 400)
        assert tr.windows[-1] == tr.windows[-20]
        for f in flows:
            assert 1.0 - 1e-9 <= f.diff <= 3.0 + 1e-9
        assert sum(tr.rates[-1]) == pytest.approx(c)


def test_late_flow_gets_more():
    flows, tr = simulate([20.0] * 5, 1.0, 400, start=[0, 0, 0, 0, 200])
    assert flows[4].base_rtt == pytest.approx(30.0)
    r = tr.rates[-1]
    assert r[4] > 1.5 * r[0]
