# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-join/. The authors are listed in prov/1RHMXP.jsonl.

import random

import pytest

from sliding_window_join import CountWindowJoin, TimeWindowJoin


def brute_time(events, t_a, t_b):
    """All pairs (id of A, id of B): the later tuple sees the earlier one in the earlier one's window."""
    length = {"A": t_a, "B": t_b}
    out = []
    for j, (sj, tj, kj, ij) in enumerate(events):
        for si, ti, ki, ii in events[:j]:
            if si != sj and ki == kj and ti > tj - length[si]:
                out.append((ii, ij) if si == "A" else (ij, ii))
    return sorted(out)


def brute_count(events, n_a, n_b):
    size = {"A": n_a, "B": n_b}
    out = []
    for j, (sj, kj, ij) in enumerate(events):
        other = [e for e in events[:j] if e[0] != sj][-size["B" if sj == "A" else "A"]:]
        for _, ki, ii in other:
            if ki == kj:
                out.append((ij, ii) if sj == "A" else (ii, ij))
    return sorted(out)


def run_time(events, t_a, t_b):
    j = TimeWindowJoin(t_a, t_b)
    out = []
    for s, t, k, i in events:
        out += [(a[2], b[2]) for a, b in j.arrive(s, t, k, i)]
    return sorted(out), j


def test_page_example():
    events = [("A", 1, "x", "a1"), ("B", 2, "x", "b1"), ("B", 2, "y", "b2"),
              ("A", 4, "y", "a2"), ("B", 5, "x", "b3"), ("A", 6, "x", "a3")]
    out, j = run_time(events, 3, 3)
    assert out == [("a1", "b1"), ("a2", "b2"), ("a3", "b3")]
    assert out == brute_time(events, 3, 3)
    assert j.stored() == 3  # a2, a3 and b3 have times > 6 - 3


def time_streams(rng):
    yield [("A" if i % 2 else "B", i, 0, i) for i in range(60)]  # one key: every pair in range joins
    yield [("A" if i % 3 else "B", 5, i % 2, i) for i in range(40)]  # one timestamp for all
    yield [("A" if i < 20 else "B", i * 10, 0, i) for i in range(40)]  # large gaps
    for _ in range(60):
        t, ev = 0.0, []
        for i in range(rng.randint(0, 120)):
            t += rng.choice([0, 0, 0.5, 1, 3])
            ev.append((rng.choice("AB"), t, rng.randint(0, rng.choice([1, 3, 10])), i))
        yield ev


@pytest.mark.parametrize("t_a,t_b", [(0.25, 0.25), (1, 1), (3, 3), (2, 7), (10, 0.5), (1000, 1000)])
def test_time_join_against_brute_force(t_a, t_b):
    rng = random.Random(int(t_a * 100 + t_b))
    for events in time_streams(rng):
        out, j = run_time(events, t_a, t_b)
        assert out == brute_time(events, t_a, t_b)
        assert j.probed == len(out)  # the hash probe touches only matching tuples
        if events:
            t = events[-1][1]
            live = sum(1 for s, ti, _, _ in events if ti > t - (t_a if s == "A" else t_b))
            assert j.stored() == live


@pytest.mark.parametrize("n_a,n_b", [(1, 1), (2, 5), (4, 4), (10, 3), (100, 100)])
def test_count_join_against_brute_force(n_a, n_b):
    rng = random.Random(n_a * 31 + n_b)
    for trial in range(60):
        ev = [(rng.choice("AB"), rng.randint(0, [0, 2, 6][trial % 3]), i) for i in range(rng.randint(0, 100))]
        j = CountWindowJoin(n_a, n_b)
        out = []
        for s, k, i in ev:
            out += [(a[2], b[2]) for a, b in j.arrive(s, k, i)]
        assert sorted(out) == brute_count(ev, n_a, n_b)
        na = sum(1 for e in ev if e[0] == "A")
        assert j.stored() == min(na, n_a) + min(len(ev) - na, n_b)


def test_output_rate_matches_cost_model():
    rng = random.Random(7)
    lam_a, lam_b, t_a, t_b, keys, horizon = 1.0, 2.0, 5.0, 3.0, 4, 3000.0
    events, t, i = [], 0.0, 0
    while True:
        t += rng.expovariate(lam_a + lam_b)
        if t > horizon:
            break
        s = "A" if rng.random() < lam_a / (lam_a + lam_b) else "B"
        events.append((s, t, rng.randrange(keys), i))
        i += 1
    j = TimeWindowJoin(t_a, t_b)
    total = sum(len(j.arrive(s, ti, k, idx)) for s, ti, k, idx in events)
    expected = (1 / keys) * lam_a * lam_b * (t_a + t_b) * horizon
    assert abs(total - expected) < 0.05 * expected


def test_bad_arguments():
    with pytest.raises(ValueError):
        TimeWindowJoin(0, 1)
    with pytest.raises(ValueError):
        CountWindowJoin(1, 0)
