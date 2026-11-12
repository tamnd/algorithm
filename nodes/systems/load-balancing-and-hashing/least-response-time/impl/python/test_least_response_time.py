# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-response-time/. The authors are listed in prov/4ZQE1H.jsonl.

import random
from fractions import Fraction as F

import pytest

from least_response_time import (LeastResponseTime, burst, ewma_closed_form, nginx_avg,
                                 nginx_eta)


def test_burst_of_the_page() -> None:
    assert burst([10, 12, 15], 6) == [0, 1, 2, 0, 1, 0]
    assert burst([10, 12, 15], 6, mode="latency") == [0] * 6


def test_step_response_of_the_page() -> None:
    lb = LeastResponseTime(1, alpha=F(1, 20))
    lb.L = [F(10)]
    for k in range(1, 46):
        lb.pick()
        lb.done(0, 50)
        assert lb.L[0] == 50 - 40 * F(19, 20) ** k
    assert lb.L[0] > 46
    assert abs(float(50 - 40 * F(19, 20) ** 14) - 30.493) < 1e-3


def test_nginx_examples_of_the_page() -> None:
    avg, trace = 0, []
    for v in [100, 100, 300, 300, 300]:
        avg = nginx_avg(avg, v)
        trace.append(avg)
    assert trace == [100, 100, 110, 120, 129]
    assert [nginx_eta(10, 0), nginx_eta(20, 0), nginx_eta(39, 2), nginx_eta(6000, 1)] == \
        [20, 40, 120, 10000]


def test_first_sample_and_errors() -> None:
    lb = LeastResponseTime(2)
    assert lb.pick() == 0          # no samples: both score 0, lowest index
    lb.done(0, 30)
    assert lb.L == [30, None]
    assert lb.pick() == 1          # an unmeasured backend is probed first
    with pytest.raises(ValueError):
        LeastResponseTime(1).done(0, 5)
    with pytest.raises(ValueError):
        LeastResponseTime(1, alpha=0)
    lb = LeastResponseTime(2)
    lb.up = [False, False]
    assert lb.pick() is None


def oracle(lb):
    cand = [j for j in range(len(lb.a)) if lb.up[j] and lb.w[j] > 0]
    if not cand:
        return None
    return min(cand, key=lambda j: (F(lb.score(j)) / lb.w[j], j))


def test_random_against_oracle_and_closed_form() -> None:
    rng = random.Random(9)
    for _ in range(300):
        n = rng.randint(1, 5)
        w = [rng.randint(0, 4) for _ in range(n)]
        alpha = F(rng.randint(1, 9), 10)
        l0 = [F(rng.randint(1, 50)) for _ in range(n)]
        lb = LeastResponseTime(n, alpha=alpha, weights=w, mode=rng.choice(["product", "latency"]))
        lb.L = list(l0)
        samples = [[] for _ in range(n)]
        for _ in range(40):
            if rng.random() < 0.1:
                lb.up[rng.randrange(n)] = rng.random() < 0.7
            busy = [j for j in range(n) if lb.a[j] > 0]
            if busy and rng.random() < 0.4:
                j = rng.choice(busy)
                x = F(rng.randint(1, 100))
                lb.done(j, x)
                samples[j].append(x)
                continue
            want = oracle(lb)
            assert lb.pick() == want
        for j in range(n):
            assert lb.L[j] == ewma_closed_form(l0[j], samples[j], alpha)
            lo = min([l0[j]] + samples[j])
            hi = max([l0[j]] + samples[j])
            assert lo <= lb.L[j] <= hi


def test_burst_share_bounds() -> None:
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(1, 6)
        lat = [F(rng.randint(1, 40)) for _ in range(n)]
        w = [rng.randint(1, 5) for _ in range(n)]
        u = [w[j] / lat[j] for j in range(n)]
        total = sum(u)
        for k in range(1, 30):
            picks = burst(lat, k, weights=w)
            for j in range(n):
                c = picks.count(j)
                assert c >= k * u[j] / total - 1
                assert c <= k * u[j] / total + (n - 1)
