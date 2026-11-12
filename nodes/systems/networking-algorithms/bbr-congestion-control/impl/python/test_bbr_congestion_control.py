# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bbr-congestion-control/. The authors are listed in prov/BBWT9S.jsonl.

import random

import pytest

from bbr_congestion_control import BBR, DRAIN_GAIN, GAINS, HIGH_GAIN, Link, simulate


def test_gains():
    assert HIGH_GAIN == pytest.approx(2.885, abs=1e-3)
    assert HIGH_GAIN * DRAIN_GAIN == pytest.approx(1.0)
    assert sum(GAINS) / len(GAINS) == pytest.approx(1.0)


def test_page_trace():
    link = Link(c=1000.0, d=0.04)
    bbr = BBR(init_rate=250.0, init_rtt=0.04)
    log = simulate(bbr, link, 40)
    states = [r.state for r in log[:8]]
    assert states == ["STARTUP"] * 5 + ["DRAIN"] + ["PROBE_BW"] * 2
    assert log[1].btl_bw == pytest.approx(721.3, abs=0.1)
    assert log[2].queue == pytest.approx(110.2, abs=0.1)
    assert log[6].queue == pytest.approx(0.0, abs=1e-9)
    probe = [i for i, r in enumerate(log) if r.queue > 1e-9 and i > 6]
    assert probe == [12, 20, 28, 36]  # one 1.25 round in every 8
    assert all(log[i].queue == pytest.approx(10.0) for i in probe)


def test_estimates_converge_and_queue_stays_small():
    rng = random.Random(2016)
    for _ in range(40):
        c = rng.uniform(100, 5000)
        d = rng.uniform(0.005, 0.2)
        link = Link(c=c, d=d)
        bbr = BBR(init_rate=10 / d, init_rtt=d)
        log = simulate(bbr, link, 200)
        assert bbr.state == "PROBE_BW"
        assert bbr.btl_bw == pytest.approx(c)
        assert bbr.rt_prop == pytest.approx(d)
        tail = log[-80:]
        rate = sum(r.rate * r.rtt for r in tail) / sum(r.rtt for r in tail)
        assert rate > 0.9 * c
        assert max(r.queue for r in tail) <= 0.25 * c * d + 1e-9


def test_probe_rtt_after_route_change():
    link = Link(c=1000.0, d=0.04)
    bbr = BBR(init_rate=250.0, init_rtt=0.04)
    simulate(bbr, link, 100)
    changed = link.log[-1].time
    link.d = 0.06
    log = simulate(bbr, link, 300)
    assert bbr.rt_prop == pytest.approx(0.06)
    entered = [r.time for r in log if r.state == "PROBE_RTT"]
    assert entered and entered[0] - changed == pytest.approx(10.0, abs=0.1)
    assert bbr.state == "PROBE_BW"


def test_small_buffer_still_finds_rate():
    link = Link(c=1000.0, d=0.04, buffer=20)
    bbr = BBR(init_rate=250.0, init_rtt=0.04)
    simulate(bbr, link, 200)
    assert bbr.btl_bw == pytest.approx(1000.0)
    assert bbr.rt_prop == pytest.approx(0.04)
