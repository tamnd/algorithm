# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stream-slicing/. The authors are listed in prov/ZPAWWC.jsonl.

import random

import pytest

from stream_slicing import CONCAT, MAX, SUM, Slicer, run

EXAMPLE = [(0, 3), (1, 5), (3, 2), (4, 7), (5, 1), (7, 4), (8, 6), (9, 2), (11, 8), (12, 3), (13, 5)]
QUERIES = [(6, 4), (5, 3)]


def scratch(stream, queries, agg):
    """Recompute every window of every query from scratch, in arrival order."""
    if not stream:
        return []
    top = max(t for t, _ in stream)
    out = []
    for q, (R, S) in enumerate(queries):
        for j in range(top // S + 1):
            acc = agg.identity
            for t, v in stream:
                if j * S <= t < j * S + R:
                    acc = agg.combine(acc, agg.lift(v))
            out.append((q, j * S, j * S + R, acc))
    return sorted(out)


def boundaries(queries, horizon, mode):
    cuts = set()
    for R, S in queries:
        for j in range(horizon + 1):
            if j * S < horizon:
                cuts.add(j * S)
            if mode == "edges" and j * S + R < horizon:
                cuts.add(j * S + R)
    return sorted(cuts)


def random_stream(rng, n, span):
    ts = sorted(rng.randrange(span) for _ in range(n))
    return [(t, rng.randint(-5, 9)) for t in ts]


@pytest.mark.parametrize("mode", ["edges", "starts"])
def test_hand_example(mode):
    out, _ = run(EXAMPLE, QUERIES, SUM, mode)
    got = {(q, s): r for q, s, e, r in out}
    assert [got[(0, s)] for s in (0, 4, 8, 12)] == [18, 20, 24, 8]
    assert [got[(1, s)] for s in (0, 3, 6, 9, 12)] == [17, 14, 12, 18, 8]
    assert sorted(out) == scratch(EXAMPLE, QUERIES, SUM)


@pytest.mark.parametrize("mode", ["edges", "starts"])
def test_cuts_match_the_rule(mode):
    stream = [(t, 1) for t in range(24)]
    _, sl = run(stream, QUERIES, SUM, mode)
    assert [c for c in sl.cuts if c < 24] == boundaries(QUERIES, 24, mode)
    expect = 19 if mode == "edges" else 12
    assert len(boundaries(QUERIES, 24, mode)) == expect


@pytest.mark.parametrize("mode", ["edges", "starts"])
def test_random_matches_scratch(mode):
    rng = random.Random(2024 if mode == "edges" else 2025)
    shapes = [(6, 4), (5, 3), (10, 4), (4, 4), (7, 2), (3, 5), (9, 6)]
    for _ in range(60):
        queries = rng.sample(shapes, rng.randint(1, 3))
        stream = random_stream(rng, rng.randint(0, 35), 40)
        for agg in (SUM, MAX, CONCAT):
            out, sl = run(stream, queries, agg, mode)
            assert sorted(out) == scratch(stream, queries, agg)


@pytest.mark.parametrize("mode", ["edges", "starts"])
def test_combine_count(mode):
    """One combine per tuple, and one per slice that a window covers."""
    rng = random.Random(77)
    for _ in range(30):
        queries = rng.sample([(6, 4), (5, 3), (10, 4), (8, 2)], 2)
        stream = random_stream(rng, rng.randint(1, 30), 40)
        out, sl = run(stream, queries, SUM, mode)
        per_window = sum(sum(1 for c in sl.cuts if s <= c < e) for _, s, e, _ in out)
        assert sl.combines == len(stream) + per_window


def test_starts_never_cut_more_than_edges():
    rng = random.Random(5)
    for _ in range(30):
        queries = rng.sample([(6, 4), (5, 3), (10, 4), (7, 2), (9, 6)], rng.randint(1, 3))
        a = boundaries(queries, 60, "starts")
        b = boundaries(queries, 60, "edges")
        assert set(a) <= set(b)


def test_errors():
    with pytest.raises(ValueError):
        Slicer([(0, 2)], SUM)
    with pytest.raises(ValueError):
        Slicer([(2, 2)], SUM, mode="pairs")
    with pytest.raises(ValueError):
        run([(3, 1), (2, 1)], [(2, 2)], SUM)
    assert run([], [(2, 2)], SUM)[0] == []
