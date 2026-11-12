# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proportional-fair-scheduling/. The authors are listed in prov/PSY7PJ.jsonl.

import itertools
import math
import random

from proportional_fair_scheduling import ProportionalFair, rayleigh_rates, run, sum_log

SNR = [1, 3, 10, 30]


def test_hand_trace_alternates_on_a_fixed_channel() -> None:
    # t_c = 2, so each update moves R halfway. User 0 always gets rate 1 and
    # user 1 always gets rate 2. PF gives each user half of the slots.
    pf = ProportionalFair(2, 2)
    order, avgs = [], []
    for _ in range(4):
        avgs.append(tuple(pf.avg))
        order.append(pf.step([1, 2]))
    assert order == [1, 0, 1, 0]
    assert avgs == [(1.0, 1.0), (0.5, 1.5), (0.75, 0.75), (0.375, 1.375)]
    # A fading peak of user 0 wins the next slot.
    assert pf.step([3, 1]) == 0


def test_pf_beats_max_rate_and_round_robin_on_sum_of_logs() -> None:
    for seed in range(3):
        pf, _ = run("pf", SNR, 6000, seed)
        mr, _ = run("max-rate", SNR, 6000, seed)
        rr, _ = run("round-robin", SNR, 6000, seed)
        assert sum_log(pf) > sum_log(rr) + 1.0
        assert sum_log(pf) > sum_log(mr) + 3.0
        # Max-rate has the most total throughput, and PF beats round robin
        # on total throughput too (multiuser diversity).
        assert sum(mr) > sum(pf) > sum(rr)
        # Every user does better under PF than under round robin.
        assert all(p > r for p, r in zip(pf, rr))


def test_one_step_greedy_maximizes_next_sum_of_logs() -> None:
    # Serving argmax r_i / R_i maximizes sum log R_i(t + 1) over all choices.
    rng = random.Random(5)
    for _ in range(500):
        n = rng.randint(2, 6)
        tc = rng.choice([2, 10, 100])
        pf = ProportionalFair(n, tc)
        pf.avg = [rng.uniform(0.1, 3.0) for _ in range(n)]
        rates = [rng.uniform(0.0, 5.0) for _ in range(n)]
        b = 1 / tc

        def value(k: int) -> float:
            return sum(
                math.log((1 - b) * pf.avg[i] + (b * rates[i] if i == k else 0.0))
                for i in range(n)
            )

        best = max(value(k) for k in range(n))
        assert value(pf.choose(rates)) >= best - 1e-12


def test_equal_time_shares_when_rates_scale() -> None:
    # If r_i = c_i * h_i with h_i i.i.d., the ratio r_i / R_i does not depend
    # on c_i, so PF gives each user about 1 / N of the slots.
    rng = random.Random(2)
    c = [1, 4, 16]
    pf = ProportionalFair(3, 200)
    count = [0, 0, 0]
    for _ in range(15000):
        count[pf.step([ci * rng.expovariate(1.0) for ci in c])] += 1
    for k in count:
        assert abs(k / 15000 - 1 / 3) < 0.02


def test_no_fixed_weight_policy_does_better() -> None:
    # PF with a long time constant approaches the maximum of sum log T_i over
    # the rates that any scheduler can give. Policies that serve
    # argmax w_i r_i for fixed weights w are in that set; none beats PF by
    # more than the noise of the run.
    pf, _ = run("pf", SNR, 6000, 0, tc=500)
    target = sum_log(pf)
    rng = random.Random(9)
    weights = itertools.chain(
        [[1, 1, 1, 1], [1 / s for s in SNR], [1 / t for t in pf]],
        ([rng.uniform(0.1, 3) for _ in SNR] for _ in range(6)),
    )
    for w in weights:
        ch = random.Random(0)
        got = [0.0] * len(SNR)
        for _ in range(6000):
            r = rayleigh_rates(ch, SNR)
            i = max(range(len(SNR)), key=lambda k: w[k] * r[k])
            got[i] += r[i]
        assert sum_log([g / 6000 for g in got]) <= target + 0.05


def test_rejects_a_time_constant_that_zeroes_the_averages() -> None:
    for bad in (0.5, 1):
        try:
            ProportionalFair(2, bad)
        except ValueError:
            continue
        raise AssertionError("t_c <= 1 must be rejected")
