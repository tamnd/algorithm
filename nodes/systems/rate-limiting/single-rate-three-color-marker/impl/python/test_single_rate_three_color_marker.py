# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-rate-three-color-marker/. The authors are listed in prov/M9FPKM.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from single_rate_three_color_marker import (
    COLORS,
    GREEN,
    RED,
    YELLOW,
    SingleRateThreeColorMarker,
    mark,
)

RANK = {GREEN: 0, YELLOW: 1, RED: 2}


def rfc_reference(packets, cir, cbs, ebs, color_aware):
    """RFC 2697, Section 3, followed step by step.

    Times and CIR are integers. The CIR * (t - last) tokens of the time since
    the last packet are added one at a time with the rule of the RFC: to C if
    Tc < CBS, else to E if Te < EBS, else nowhere. Then the packet is colored
    with the text of the color-blind or the color-aware rules.
    """
    tc, te = cbs, ebs
    last = packets[0][0] if packets else 0
    out = []
    states = []
    for p in packets:
        t, b = p[0], p[1]
        for _ in range(cir * (t - last)):
            if tc < cbs:
                tc += 1
            elif te < ebs:
                te += 1
        last = t
        if not color_aware:
            if tc - b >= 0:
                color, tc = GREEN, max(0, tc - b)
            elif te - b >= 0:
                color, te = YELLOW, max(0, te - b)
            else:
                color = RED
        else:
            pre = p[2]
            if pre == GREEN and tc - b >= 0:
                color, tc = GREEN, max(0, tc - b)
            elif pre in (GREEN, YELLOW) and te - b >= 0:
                color, te = YELLOW, max(0, te - b)
            else:
                color = RED
        out.append(color)
        states.append((tc, te))
    return out, states


def run_with_states(packets, cir, cbs, ebs, color_aware):
    m = SingleRateThreeColorMarker(cir, cbs, ebs, color_aware, packets[0][0])
    out, states = [], []
    for p in packets:
        out.append(m.meter(p[0], p[1], p[2] if len(p) > 2 else None))
        states.append((m.tc, m.te))
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
    # CIR = 1000 bytes/s, CBS = 2000, EBS = 2000, times in seconds.
    trace = [
        (0, 1500), (0, 1500), (0, 1500), (1, 1500),
        (Fraction(3, 2), 1000), (5, 1500), (5, 1500), (5, 1000),
    ]
    m = SingleRateThreeColorMarker(1000, 2000, 2000)
    got = [(m.meter(t, b), m.tc, m.te) for t, b in trace]
    assert got == [
        (GREEN, 500, 2000), (YELLOW, 500, 500), (RED, 500, 500), (GREEN, 0, 500),
        (RED, 500, 500), (GREEN, 500, 2000), (YELLOW, 500, 500), (RED, 500, 500),
    ]
    pre = [GREEN, GREEN, YELLOW, GREEN, GREEN, YELLOW, GREEN, GREEN]
    a = SingleRateThreeColorMarker(1000, 2000, 2000, color_aware=True)
    got = [(a.meter(t, b, c), a.tc, a.te) for (t, b), c in zip(trace, pre)]
    assert got == [
        (GREEN, 500, 2000), (YELLOW, 500, 500), (RED, 500, 500), (GREEN, 0, 500),
        (RED, 500, 500), (YELLOW, 2000, 500), (GREEN, 500, 500), (RED, 500, 500),
    ]


def test_rfc_rules_by_hand():
    # Color-blind: green needs B tokens in C, yellow needs B tokens in E.
    m = SingleRateThreeColorMarker(1, 3, 2)
    assert m.meter(0, 3) == GREEN and (m.tc, m.te) == (0, 2)
    assert m.meter(0, 2) == YELLOW and (m.tc, m.te) == (0, 0)
    assert m.meter(0, 1) == RED and (m.tc, m.te) == (0, 0)
    # One token goes to C, which is not full.
    assert m.meter(1, 2) == RED and (m.tc, m.te) == (1, 0)
    # C fills to 3 at t = 3, then the overflow goes to E.
    assert m.meter(6, 4) == RED and (m.tc, m.te) == (3, 2)
    # A packet of size 4 is too big for both buckets.
    assert m.meter(100, 4) == RED and (m.tc, m.te) == (3, 2)
    # Color-aware: a yellow packet never uses C, a red one uses nothing.
    a = SingleRateThreeColorMarker(1, 3, 2, color_aware=True)
    assert a.meter(0, 1, RED) == RED and (a.tc, a.te) == (3, 2)
    assert a.meter(0, 1, YELLOW) == YELLOW and (a.tc, a.te) == (3, 1)
    assert a.meter(0, 2, YELLOW) == RED and (a.tc, a.te) == (3, 1)
    assert a.meter(0, 3, GREEN) == GREEN and (a.tc, a.te) == (0, 1)
    assert a.meter(0, 1, GREEN) == YELLOW and (a.tc, a.te) == (0, 0)


def test_bad_input():
    with pytest.raises(ValueError):
        SingleRateThreeColorMarker(0, 1, 1)
    with pytest.raises(ValueError):
        SingleRateThreeColorMarker(1, 0, 0)
    m = SingleRateThreeColorMarker(1, 1, 1)
    m.meter(5, 1)
    with pytest.raises(ValueError):
        m.meter(4, 1)
    with pytest.raises(ValueError):
        SingleRateThreeColorMarker(1, 1, 1, color_aware=True).meter(0, 1)


def small_traces(length):
    """All traces of `length` packets: time steps 0 or 1, sizes 1 to 3, all precolors."""
    one = list(itertools.product((0, 1), (1, 2, 3), COLORS))
    for combo in itertools.product(one, repeat=length):
        t, trace = 0, []
        for step, b, c in combo:
            t += step
            trace.append((t, b, c))
        yield trace


@pytest.mark.parametrize("cir,cbs,ebs", [(1, 2, 2), (2, 3, 1), (1, 0, 3), (3, 1, 0), (1, 3, 3)])
def test_exhaustive_against_rfc_reference(cir, cbs, ebs):
    for length in (1, 2, 3):
        for trace in small_traces(length):
            for aware in (False, True):
                assert run_with_states(trace, cir, cbs, ebs, aware) == rfc_reference(
                    trace, cir, cbs, ebs, aware
                ), (trace, aware)


def test_random_against_rfc_reference():
    rng = random.Random(2697)
    for _ in range(300):
        cir = rng.randint(1, 4)
        cbs, ebs = rng.randint(0, 12), rng.randint(0, 12)
        if cbs + ebs == 0:
            continue
        t, trace = 0, []
        for _ in range(rng.randint(1, 60)):
            t += rng.choice((0, 0, 1, 2, 5))
            trace.append((t, rng.randint(1, 8), rng.choice(COLORS)))
        for aware in (False, True):
            assert run_with_states(trace, cir, cbs, ebs, aware) == rfc_reference(
                trace, cir, cbs, ebs, aware
            )


def random_fraction_trace(rng, n):
    t, trace = Fraction(0), []
    for _ in range(n):
        t += Fraction(rng.randint(0, 6), rng.randint(1, 4))
        trace.append((t, rng.randint(1, 5), rng.choice(COLORS)))
    return trace


def test_green_is_a_token_bucket():
    rng = random.Random(7)
    for _ in range(300):
        cir = Fraction(rng.randint(1, 6), rng.randint(1, 3))
        cbs, ebs = rng.randint(1, 10), rng.randint(0, 10)
        trace = random_fraction_trace(rng, rng.randint(1, 50))
        blind = mark([(t, b) for t, b, _ in trace], cir, cbs, ebs)
        tb = token_bucket([(t, b) for t, b, _ in trace], cir, cbs)
        assert [c == GREEN for c in blind] == tb
        # Color-aware: green is the token bucket run on the precolored green packets.
        aware = mark(trace, cir, cbs, ebs, color_aware=True)
        sub = [(t, b) for t, b, c in trace if c == GREEN]
        got = [col == GREEN for col, p in zip(aware, trace) if p[2] == GREEN]
        assert got == (token_bucket(sub, cir, cbs) if sub else [])


def test_interval_bounds_and_no_upgrade():
    rng = random.Random(1999)
    for _ in range(200):
        cir = Fraction(rng.randint(1, 6), rng.randint(1, 3))
        cbs, ebs = rng.randint(0, 10), rng.randint(0, 10)
        if cbs + ebs == 0:
            continue
        trace = random_fraction_trace(rng, rng.randint(1, 40))
        for aware in (False, True):
            colors = mark(trace, cir, cbs, ebs, aware)
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
                    assert y <= ebs + cir * tau
                    assert g + y <= cbs + ebs + cir * tau


def test_burst_bound_is_reached():
    # From full buckets, CBS + EBS bytes pass at once, then CIR per second.
    trace = [(0, 1)] * 7 + [(1, 1)] * 3
    assert mark(trace, 2, 3, 2) == [GREEN] * 3 + [YELLOW] * 2 + [RED] * 2 + [GREEN] * 2 + [RED]
