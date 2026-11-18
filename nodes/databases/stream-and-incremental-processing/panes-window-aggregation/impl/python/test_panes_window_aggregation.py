# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/panes-window-aggregation/. The authors are listed in prov/0B550K.jsonl.

import random

import pytest

from panes_window_aggregation import AVG, COUNT, MAX, SUM, PanedAggregator, run

EXAMPLE = [(0, 3), (1, 5), (3, 2), (4, 7), (5, 1), (7, 4), (8, 6), (9, 2), (11, 8), (12, 3), (13, 5)]


def scratch(tuples, R, S, name):
    """Recompute every window [j*S, j*S + R) from scratch, by definition."""
    if not tuples:
        return []
    top = max(t for t, _ in tuples)
    out = []
    for j in range(top // S + 1):
        vals = [v for t, v in tuples if j * S <= t < j * S + R]
        if name == "sum":
            r = sum(vals)
        elif name == "count":
            r = len(vals)
        elif name == "max":
            r = max(vals) if vals else None
        else:
            r = (sum(vals), len(vals)) if vals else None
        out.append((j * S, j * S + R, r))
    return out


def accepted_by_definition(arrivals, R, S, delay):
    """The tuples whose pane is still open when they arrive."""
    from math import gcd

    g = gcd(R, S)
    keep, top, closed_before = [], None, 0
    for t, v in arrivals:
        # panes [i*g, (i+1)*g) with (i+1)*g <= top - delay are closed
        if top is not None:
            closed_before = max(closed_before, (top - delay) // g)
        if t // g >= closed_before:
            keep.append((t, v))
        top = t if top is None else max(top, t)
    return keep


def random_stream(rng, n, span):
    ts = sorted(rng.randrange(span) for _ in range(n))
    return [(t, rng.randint(-5, 9)) for t in ts]


def shuffle_bounded(rng, tuples, D):
    keyed = [(t + rng.randint(0, D), i, (t, v)) for i, (t, v) in enumerate(tuples)]
    keyed.sort()
    return [x for _, _, x in keyed]


def test_hand_example():
    out, _ = run(EXAMPLE, 6, 4, SUM)
    assert out == [(0, 6, 18), (4, 10, 20), (8, 14, 24), (12, 18, 8)]
    out, _ = run(EXAMPLE, 6, 4, MAX)
    assert [r for _, _, r in out] == [7, 7, 8, 5]


def test_hand_example_costs():
    out, pa = run(EXAMPLE, 6, 4, SUM)
    assert pa.g == 2 and pa.k == 3
    # one combine per tuple (pane level) and k per window (window level)
    assert pa.combines == len(EXAMPLE) + len(out) * pa.k


@pytest.mark.parametrize("R,S", [(6, 4), (10, 4), (5, 5), (12, 8), (7, 3), (4, 6), (9, 1)])
def test_in_order_matches_scratch(R, S):
    rng = random.Random(1000 + 31 * R + S)
    for _ in range(25):
        tuples = random_stream(rng, rng.randint(0, 40), 50)
        for agg in (SUM, COUNT, MAX, AVG):
            out, pa = run(tuples, R, S, agg)
            assert out == scratch(tuples, R, S, agg.name)
            assert pa.late == 0
            assert pa.combines == len(tuples) + len(out) * pa.k


def test_state_bound_in_order():
    rng = random.Random(7)
    R, S = 12, 8
    tuples = random_stream(rng, 120, 200)
    pa = PanedAggregator(R, S, SUM)
    for t, v in tuples:
        pa.insert(t, v)
        pa.advance(t)
        # the last k closed panes and the one open pane
        assert pa.state_size() <= pa.k + 1


def test_bounded_disorder_has_no_late_tuples():
    rng = random.Random(11)
    for _ in range(40):
        R, S = rng.choice([(6, 4), (10, 4), (8, 8), (9, 6)])
        D = rng.randint(0, 6)
        tuples = random_stream(rng, rng.randint(1, 40), 60)
        arrivals = shuffle_bounded(rng, tuples, D)
        out, pa = run(arrivals, R, S, SUM, delay=D)
        assert pa.late == 0
        assert out == scratch(tuples, R, S, "sum")


def test_too_fast_watermark_drops_exactly_the_late_tuples():
    rng = random.Random(12)
    seen_late = 0
    for _ in range(60):
        R, S = rng.choice([(6, 4), (10, 4), (8, 8), (9, 6)])
        D = rng.randint(3, 8)
        tuples = random_stream(rng, rng.randint(1, 40), 60)
        arrivals = shuffle_bounded(rng, tuples, D)
        delay = rng.randint(0, D - 1)
        keep = accepted_by_definition(arrivals, R, S, delay)
        for agg in (SUM, MAX):
            out, pa = run(arrivals, R, S, agg, delay=delay)
            assert pa.late == len(arrivals) - len(keep)
            assert out == scratch(keep, R, S, agg.name)
        seen_late += len(arrivals) - len(keep)
    assert seen_late > 0


def test_each_window_is_k_consecutive_panes():
    for R in range(1, 13):
        for S in range(1, 13):
            pa = PanedAggregator(R, S, SUM)
            g = pa.g
            for j in range(5):
                assert (j * S) % g == 0 and (j * S + R) % g == 0
                assert (j * S + R - j * S) // g == pa.k
            # no larger pane length divides all window boundaries
            for h in range(g + 1, R + S + 1):
                assert not (R % h == 0 and S % h == 0)


def test_empty_and_errors():
    assert run([], 6, 4, SUM)[0] == []
    with pytest.raises(ValueError):
        PanedAggregator(0, 4, SUM)
