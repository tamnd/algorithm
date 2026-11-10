# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ntp/. The authors are listed in prov/PXEY9N.jsonl.

import random

from ntp import Peer, exchange, mitigate, ntp_select, on_wire, poll


def test_page_example() -> None:
    # Server 0.25 s ahead; 10 ms out, 30 ms back, 1 ms hold.
    t = exchange(0.25, 0.010, 0.030, 100.000, 0.001)
    assert [round(x, 9) for x in t] == [100.0, 100.26, 100.261, 100.041]
    theta, delta = on_wire(*t)
    assert abs(theta - 0.24) < 1e-9 and abs(delta - 0.040) < 1e-9
    assert abs(theta - 0.25) <= delta / 2


def test_symmetric_delays_are_exact() -> None:
    rng = random.Random(1)
    for _ in range(500):
        theta0 = rng.uniform(-10, 10)
        d = rng.uniform(0, 0.2)
        theta, delta = on_wire(*exchange(theta0, d, d, rng.uniform(0, 1e5), rng.uniform(0, 0.01)))
        assert abs(theta - theta0) < 1e-6 and abs(delta - 2 * d) < 1e-6


def test_asymmetric_error_is_half_the_difference() -> None:
    rng = random.Random(2)
    for _ in range(2000):
        theta0 = rng.uniform(-10, 10)
        a, b = rng.uniform(0, 0.3), rng.uniform(0, 0.3)
        theta, delta = on_wire(*exchange(theta0, a, b, rng.uniform(0, 1e5), rng.uniform(0, 0.01)))
        assert abs((theta - theta0) - (a - b) / 2) < 1e-6
        assert abs(delta - (a + b)) < 1e-6
        assert abs(theta - theta0) <= delta / 2 + 1e-6


def test_bound_is_reached() -> None:
    # All of the delay on the way out: the error is delta / 2.
    theta, delta = on_wire(*exchange(1.0, 0.08, 0.0, 50.0, 0.0))
    assert abs(abs(theta - 1.0) - delta / 2) < 1e-9


def test_clock_filter_takes_least_delay() -> None:
    rng = random.Random(3)
    p = Peer("s")
    for _ in range(20):
        poll(p, 0.5, rng, dmin=0.001, spread=0.02)
    theta, delta, _ = p.clock_filter()
    assert len(p.samples) == 8
    assert delta == min(s[1] for s in p.samples)
    assert abs(theta - 0.5) <= delta / 2 + 1e-9


def test_select_rejects_falseticker() -> None:
    assert ntp_select([(0.010, 0.004), (0.012, 0.003), (0.011, 0.005), (0.050, 0.002)]) is not None
    l, u, f = ntp_select([(0.010, 0.004), (0.012, 0.003), (0.011, 0.005), (0.050, 0.002)])
    assert f == 1 and l <= 0.012 <= u and not (l <= 0.050 <= u)


def test_full_chain_on_seeded_runs() -> None:
    for seed in range(60):
        rng = random.Random(100 + seed)
        truth = rng.uniform(-1, 1)  # the true offset of UTC from the client clock
        peers = [Peer(f"good{i}") for i in range(5)] + [Peer("liar")]
        for _ in range(8):
            for p in peers[:5]:
                poll(p, truth, rng, dmin=0.002, spread=0.005, asym=rng.choice([0.0, 0.004]))
            poll(peers[5], truth + 0.5, rng, dmin=0.002, spread=0.005)
        res = mitigate(peers)
        assert res is not None
        assert "liar" not in res["survivors"] and len(res["survivors"]) >= 3
        worst = max(p.root_distance() for p in peers[:5])
        assert abs(res["offset"] - truth) <= worst
