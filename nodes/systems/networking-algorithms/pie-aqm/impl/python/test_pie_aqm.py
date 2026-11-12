# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pie-aqm/. The authors are listed in prov/97E1GT.jsonl.

import math
import random

from pie_aqm import PIE, auto_tune, simulate

RATE = 1.25e6  # 10 Mbit/s in bytes per second
TX = 1500 / RATE  # 1.2 ms per packet


def poisson(rng: random.Random, lam: float, horizon: float) -> list[float]:
    t, out = 0.0, []
    while True:
        t += rng.expovariate(lam)
        if t >= horizon:
            return out
        out.append(t)


def test_one_update_by_hand() -> None:
    # drop_prob = 0, qdelay_old = 0, qdelay = 30 ms:
    # p = 0.125 * 0.015 + 1.25 * 0.030 = 0.039375, divided by 2048.
    p = PIE(RATE, random.Random(1))
    p.bytes = int(0.030 * RATE)
    p.update()
    assert math.isclose(p.drop_prob, 0.039375 / 2048)
    assert p.qdelay_old == 0.030
    assert math.isclose(p.burst_allowance, 0.135)


def test_auto_tune_table() -> None:
    for prob, divisor in [(0.0, 2048), (5e-6, 512), (5e-5, 128), (5e-4, 32),
                          (5e-3, 8), (0.05, 2), (0.5, 1)]:
        assert math.isclose(auto_tune(1.0, prob), 1.0 / divisor)


def test_decay_and_clamp() -> None:
    p = PIE(RATE, random.Random(1))
    p.drop_prob = 0.5
    p.update()  # empty queue, qdelay_old = 0: p is negative, then x0.98
    assert math.isclose(p.drop_prob, (0.5 - 0.125 * 0.015) * 0.98)
    p.drop_prob = 0.0
    p.update()
    assert p.drop_prob == 0.0  # clamped at 0


def test_short_burst_is_not_dropped() -> None:
    # 50 packets at twice the link rate: arrivals last 60 ms < MAX_BURST.
    arrivals = [k * TX / 2 for k in range(50)]
    r = simulate(PIE(RATE, random.Random(1)), arrivals, until=1.0)
    assert r["drops"] == []
    assert max(d for _, d in r["delays"]) < 0.031


def test_long_burst_is_cut_after_the_allowance() -> None:
    arrivals = [k * TX / 2 for k in range(1666)]  # twice the link rate for 1 s
    r = simulate(PIE(RATE, random.Random(1)), arrivals, until=3.0)
    assert len(r["drops"]) > 500
    assert min(r["drops"]) > 0.150


def test_allowance_comes_back_after_idle() -> None:
    p = PIE(RATE, random.Random(1))
    arrivals = [k * TX / 2 for k in range(50)]
    simulate(p, arrivals, until=1.9)
    assert p.burst_allowance == 0.0  # used up by the updates
    p.enqueue(1500)
    assert p.burst_allowance == p.max_burst


def test_overload_holds_delay_near_target() -> None:
    # Poisson arrivals at 1.2 times the link rate, traffic that does not
    # respond: PIE drops about 1/6 and holds the mean delay near 15 ms.
    for seed in (1, 2):
        arrivals = poisson(random.Random(seed), 1.2 / TX, 60.0)
        r = simulate(PIE(RATE, random.Random(seed + 100)), arrivals)
        late = [d for a, d in r["delays"] if a > 30.0]
        assert 0.010 < sum(late) / len(late) < 0.020
        assert abs(len(r["drops"]) / len(arrivals) - 1 / 6) < 0.02


def test_integral_action() -> None:
    # Once drop_prob >= 0.1 there is no scaling, and if no clamp or decay acts,
    # the change of drop_prob telescopes:
    #   P_K - P_0 = alpha sum (q_k - REF) + beta (q_K - q_0).
    arrivals = poisson(random.Random(1), 1.2 / TX, 60.0)
    pie = PIE(RATE, random.Random(101))
    probs = simulate(pie, arrivals)["probs"]
    start = next(k for k, (_, prob, _) in enumerate(probs) if prob >= 0.1)
    window = probs[start:]
    assert all(0.1 <= prob < 1.0 for _, prob, _ in window)
    p0, q0 = window[0][1], window[0][2]
    pk, qk = window[-1][1], window[-1][2]
    s = sum(q - pie.ref for _, _, q in window[1:])
    assert math.isclose(pk - p0, pie.alpha * s + pie.beta * (qk - q0), abs_tol=1e-9)
    k = len(window) - 1
    qmax = max(q for _, _, q in window)
    mean = sum(q for _, _, q in window[1:]) / k
    assert abs(mean - pie.ref) <= (1 + pie.beta * qmax) / (pie.alpha * k)
