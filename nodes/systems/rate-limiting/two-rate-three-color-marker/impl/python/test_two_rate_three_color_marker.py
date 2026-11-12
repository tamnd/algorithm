# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-rate-three-color-marker/. The authors are listed in prov/2FQ2DX.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from two_rate_three_color_marker import (
    COLORS,
    GREEN,
    RED,
    YELLOW,
    TwoRateThreeColorMarker,
    mark,
)

RANK = {GREEN: 0, YELLOW: 1, RED: 2}


def rfc_reference(packets, pir, pbs, cir, cbs, color_aware):
    """RFC 2698, Section 3, followed step by step.

    Times and rates are integers. Tp gets PIR * (t - last) increments of one,
    each only while Tp < PBS, and Tc gets CIR * (t - last) increments of one,
    each only while Tc < CBS. Then the packet is colored with the text of
    the color-blind or the color-aware rules.
    """
    tp, tc = pbs, cbs
    last = packets[0][0] if packets else 0
    out, states = [], []
    for p in packets:
        t, b = p[0], p[1]
        for _ in range(pir * (t - last)):
            if tp < pbs:
                tp += 1
        for _ in range(cir * (t - last)):
            if tc < cbs:
                tc += 1
        last = t
        if not color_aware:
            if tp - b < 0:
                color = RED
            elif tc - b < 0:
                color, tp = YELLOW, tp - b
            else:
                color, tp, tc = GREEN, tp - b, tc - b
        else:
            pre = p[2]
            if pre == RED or tp - b < 0:
                color = RED
            elif pre == YELLOW or tc - b < 0:
                color, tp = YELLOW, tp - b
            else:
                color, tp, tc = GREEN, tp - b, tc - b
        out.append(color)
        states.append((tp, tc))
    return out, states


def run_with_states(packets, pir, pbs, cir, cbs, color_aware):
    m = TwoRateThreeColorMarker(pir, pbs, cir, cbs, color_aware, packets[0][0])
    out, states = [], []
    for p in packets:
        out.append(m.meter(p[0], p[1], p[2] if len(p) > 2 else None))
        states.append((m.tp, m.tc))
    return out, states


def token_bucket(packets, rate, depth):
    """A plain token bucket policer, full at the first packet."""
    x, last, out = depth, packets[0][0], []
    for t, b in packets:
        x = min(depth, x + rate * (t - last))
        last = t
        if x >= b:
            x -= b
            out.append(True)
        else:
            out.append(False)
    return out


def test_page_example():
    # PIR = 2000 bytes/s, PBS = 3000, CIR = 1000 bytes/s, CBS = 2000.
    trace = [
        (0, 1000), (0, 1000), (0, 1000), (0, 1000), (Fraction(1, 2), 1000),
        (1, 1000), (Fraction(5, 4), 500), (3, 1500), (3, 1500),
    ]
    m = TwoRateThreeColorMarker(2000, 3000, 1000, 2000)
    got = [(m.meter(t, b), m.tp, m.tc) for t, b in trace]
    assert got == [
        (GREEN, 2000, 1000), (GREEN, 1000, 0), (YELLOW, 0, 0), (RED, 0, 0),
        (YELLOW, 0, 500), (GREEN, 0, 0), (YELLOW, 0, 250),
        (GREEN, 1500, 500), (YELLOW, 0, 500),
    ]
    pre = [GREEN, YELLOW, GREEN, GREEN, GREEN, GREEN, GREEN, YELLOW, GREEN]
    a = TwoRateThreeColorMarker(2000, 3000, 1000, 2000, color_aware=True)
    got = [(a.meter(t, b, c), a.tp, a.tc) for (t, b), c in zip(trace, pre)]
    assert got == [
        (GREEN, 2000, 1000), (YELLOW, 1000, 1000), (GREEN, 0, 0), (RED, 0, 0),
        (YELLOW, 0, 500), (GREEN, 0, 0), (YELLOW, 0, 250),
        (YELLOW, 1500, 2000), (GREEN, 0, 500),
    ]


def test_rfc_rules_by_hand():
    m = TwoRateThreeColorMarker(2, 4, 1, 2)
    assert m.meter(0, 2) == GREEN and (m.tp, m.tc) == (2, 0)  # both buckets pay
    assert m.meter(0, 1) == YELLOW and (m.tp, m.tc) == (1, 0)  # only P pays
    assert m.meter(0, 2) == RED and (m.tp, m.tc) == (1, 0)  # red pays nothing
    # At t = 1, P gets 2 tokens and C gets 1, each bucket on its own.
    assert m.meter(1, 2) == YELLOW and (m.tp, m.tc) == (1, 1)
    # Both buckets cap at their own depth.
    assert m.meter(10, 5) == RED and (m.tp, m.tc) == (4, 2)
    # Color-aware: red stays red, yellow is never tested against C.
    a = TwoRateThreeColorMarker(2, 4, 1, 2, color_aware=True)
    assert a.meter(0, 1, RED) == RED and (a.tp, a.tc) == (4, 2)
    assert a.meter(0, 1, YELLOW) == YELLOW and (a.tp, a.tc) == (3, 2)
    assert a.meter(0, 2, GREEN) == GREEN and (a.tp, a.tc) == (1, 0)
    assert a.meter(0, 2, GREEN) == RED and (a.tp, a.tc) == (1, 0)


def test_bad_input():
    with pytest.raises(ValueError):
        TwoRateThreeColorMarker(1, 4, 2, 2)  # PIR < CIR
    with pytest.raises(ValueError):
        TwoRateThreeColorMarker(2, 0, 1, 2)
    with pytest.raises(ValueError):
        TwoRateThreeColorMarker(2, 4, 1, 0)
    m = TwoRateThreeColorMarker(2, 4, 1, 2)
    m.meter(3, 1)
    with pytest.raises(ValueError):
        m.meter(2, 1)
    with pytest.raises(ValueError):
        TwoRateThreeColorMarker(2, 4, 1, 2, color_aware=True).meter(0, 1)


def small_traces(length):
    """All traces of `length` packets: time steps 0 or 1, sizes 1 to 3, all precolors."""
    one = list(itertools.product((0, 1), (1, 2, 3), COLORS))
    for combo in itertools.product(one, repeat=length):
        t, trace = 0, []
        for step, b, c in combo:
            t += step
            trace.append((t, b, c))
        yield trace


@pytest.mark.parametrize(
    "pir,pbs,cir,cbs", [(2, 3, 1, 2), (1, 2, 1, 3), (3, 4, 1, 1), (2, 1, 2, 3), (3, 3, 2, 2)]
)
def test_exhaustive_against_rfc_reference(pir, pbs, cir, cbs):
    for length in (1, 2, 3):
        for trace in small_traces(length):
            for aware in (False, True):
                assert run_with_states(trace, pir, pbs, cir, cbs, aware) == rfc_reference(
                    trace, pir, pbs, cir, cbs, aware
                ), (trace, aware)


def test_random_against_rfc_reference():
    rng = random.Random(2698)
    for _ in range(300):
        cir = rng.randint(1, 3)
        pir = cir + rng.randint(0, 3)
        pbs, cbs = rng.randint(1, 12), rng.randint(1, 12)
        t, trace = 0, []
        for _ in range(rng.randint(1, 60)):
            t += rng.choice((0, 0, 1, 2, 5))
            trace.append((t, rng.randint(1, 8), rng.choice(COLORS)))
        for aware in (False, True):
            assert run_with_states(trace, pir, pbs, cir, cbs, aware) == rfc_reference(
                trace, pir, pbs, cir, cbs, aware
            )


def random_fraction_trace(rng, n):
    t, trace = Fraction(0), []
    for _ in range(n):
        t += Fraction(rng.randint(0, 6), rng.randint(1, 4))
        trace.append((t, rng.randint(1, 5), rng.choice(COLORS)))
    return trace


def random_params(rng):
    cir = Fraction(rng.randint(1, 4), rng.randint(1, 3))
    pir = cir + Fraction(rng.randint(0, 4), rng.randint(1, 3))
    return pir, rng.randint(1, 10), cir, rng.randint(1, 10)


def test_non_red_is_a_peak_token_bucket():
    rng = random.Random(11)
    for _ in range(300):
        pir, pbs, cir, cbs = random_params(rng)
        trace = random_fraction_trace(rng, rng.randint(1, 50))
        blind = mark([(t, b) for t, b, _ in trace], pir, pbs, cir, cbs)
        assert [c != RED for c in blind] == token_bucket([(t, b) for t, b, _ in trace], pir, pbs)
        aware = mark(trace, pir, pbs, cir, cbs, color_aware=True)
        sub = [(t, b) for t, b, c in trace if c != RED]
        got = [col != RED for col, p in zip(aware, trace) if p[2] != RED]
        assert got == (token_bucket(sub, pir, pbs) if sub else [])


def test_interval_bounds_and_no_upgrade():
    rng = random.Random(1999)
    for _ in range(200):
        pir, pbs, cir, cbs = random_params(rng)
        trace = random_fraction_trace(rng, rng.randint(1, 40))
        for aware in (False, True):
            colors = mark(trace, pir, pbs, cir, cbs, aware)
            if aware:
                assert all(RANK[c] >= RANK[p[2]] for c, p in zip(colors, trace))
            n = len(trace)
            for i in range(n):
                g = y = 0
                for j in range(i, n):
                    tau = trace[j][0] - trace[i][0]
                    if colors[j] == GREEN:
                        g += trace[j][1]
                    elif colors[j] == YELLOW:
                        y += trace[j][1]
                    assert g <= cbs + cir * tau
                    assert g + y <= pbs + pir * tau


def test_peak_bucket_can_starve_green():
    # With PBS < CBS, a burst that C could cover is cut by P.
    assert mark([(0, 1)] * 4, 2, 2, 1, 4) == [GREEN, GREEN, RED, RED]
