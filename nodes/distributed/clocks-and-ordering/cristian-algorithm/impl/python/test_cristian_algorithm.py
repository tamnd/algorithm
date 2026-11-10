# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cristian-algorithm/. The authors are listed in prov/F0PB77.jsonl.

import random

from cristian_algorithm import Client, cristian, error_of, estimate, one_reading


def test_page_example() -> None:
    # The client is 2.5 s behind; request delay 3 ms, reply delay 9 ms.
    c = Client(offset=-2.5)
    r = one_reading(c, start=100.0, d1=0.003, d2=0.009, hold=0.0, read_frac=0.0)
    assert abs(r.rtt - 0.012) < 1e-12
    value, half = estimate(r)
    assert abs(value - 100.009) < 1e-12  # T = 100.003, plus 0.006
    assert abs(error_of(r) - (-0.003)) < 1e-12
    dmin = 0.002
    assert abs(error_of(r)) <= half - dmin + 1e-12


def test_bound_on_seeded_delays() -> None:
    dmin = 1.0
    for seed in range(300):
        rng = random.Random(seed)
        c = Client(offset=rng.uniform(-50, 50))
        d1 = dmin + rng.expovariate(0.5)
        d2 = dmin + rng.expovariate(0.5)
        hold = rng.choice([0.0, rng.uniform(0, 3)])
        r = one_reading(c, rng.uniform(0, 1000), d1, d2, hold, rng.random())
        _, half = estimate(r)
        assert abs(error_of(r)) <= half - dmin + 1e-9
        if hold == 0.0:
            # With no hold the error is exactly (d1 - d2) / 2.
            assert abs(error_of(r) - (d1 - d2) / 2) < 1e-9


def test_bound_is_tight() -> None:
    # All of the slack on one side: d1 = dmin, d2 = RTT - dmin.
    dmin = 1.0
    c = Client(offset=0.0)
    r = one_reading(c, 0.0, dmin, 7.0, 0.0, 0.0)
    _, half = estimate(r)
    assert abs(abs(error_of(r)) - (half - dmin)) < 1e-12


def test_bound_with_drift() -> None:
    dmin, rho = 0.5, 1e-3
    for seed in range(300):
        rng = random.Random(1000 + seed)
        rate = 1 + rng.uniform(-rho, rho)
        c = Client(offset=rng.uniform(-5, 5), rate=rate)
        r = one_reading(c, rng.uniform(0, 100), dmin + rng.expovariate(1), dmin + rng.expovariate(1), rng.uniform(0, 1), rng.random())
        _, half = estimate(r, rho)
        assert abs(error_of(r, rho)) <= half - dmin + 1e-9


def test_retry_until_small_round_trip() -> None:
    dmin = 1.0

    def delay(rng: random.Random) -> float:
        return dmin + rng.expovariate(1.0)

    total = 0
    for seed in range(200):
        rng = random.Random(seed)
        r, tries, _ = cristian(Client(3.0), dmin, delay, target=1.5, rng=rng)
        assert r is not None and r.rtt <= 3.0
        assert abs(error_of(r)) <= 1.5 - dmin + 1e-9
        total += tries
    # P(RTT <= 3) = P(X1 + X2 <= 1) for two Exp(1) = 1 - 2/e, about 0.264,
    # so the mean number of tries is about 3.8.
    assert 3.0 < total / 200 < 4.8


def test_gives_up() -> None:
    def delay(rng: random.Random) -> float:
        return 5.0

    r, tries, _ = cristian(Client(0.0), 5.0, delay, target=1.0, rng=random.Random(0), max_tries=7)
    assert r is None and tries == 7
