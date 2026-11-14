# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asap-alap-scheduling/. The authors are listed in prov/5S0Z4R.jsonl.

import itertools
import random

import pytest

from asap_alap_scheduling import alap, asap, latency_of, mobility, topological_order

# The differential equation example (Paulin and Knight): v1 .. v11 are 0 .. 10.
DIFFEQ_N = 11
DIFFEQ_EDGES = [(0, 2), (1, 2), (2, 3), (3, 4), (5, 6), (6, 4), (7, 8), (9, 10)]


def random_dag(rng, n, p=0.35, most=3):
    delay = [rng.randint(1, most) for _ in range(n)]
    edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
    perm = list(range(n))
    rng.shuffle(perm)  # hide the numbering order from the code under test
    return delay_perm(delay, perm), [(perm[u], perm[v]) for (u, v) in edges]


def delay_perm(delay, perm):
    out = [0] * len(delay)
    for i, x in enumerate(delay):
        out[perm[i]] = x
    return out


def longest_from_sources(n, delay, edges, v):
    """The largest delay sum of a path that ends just before v, by walking all paths."""
    pred = [[] for _ in range(n)]
    for (a, b) in edges:
        pred[b].append(a)
    return max([0] + [delay[u] + longest_from_sources(n, delay, edges, u) for u in pred[v]])


def longest_to_sinks(n, delay, edges, v):
    """The largest delay sum of a path that starts at v, with v."""
    succ = [[] for _ in range(n)]
    for (a, b) in edges:
        succ[a].append(b)
    return delay[v] + max([0] + [longest_to_sinks(n, delay, edges, w) for w in succ[v]])


def feasible_schedules(n, delay, edges, latency):
    for t in itertools.product(range(1, latency + 1), repeat=n):
        if all(t[v] >= t[u] + delay[u] for (u, v) in edges) and latency_of(list(t), delay) <= latency:
            yield t


def test_diffeq():
    d = [1] * DIFFEQ_N
    assert asap(DIFFEQ_N, d, DIFFEQ_EDGES) == [1, 1, 2, 3, 4, 1, 2, 1, 2, 1, 2]
    assert alap(DIFFEQ_N, d, DIFFEQ_EDGES, 4) == [1, 1, 2, 3, 4, 2, 3, 3, 4, 3, 4]
    assert mobility(DIFFEQ_N, d, DIFFEQ_EDGES, 4) == [0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2]
    assert alap(DIFFEQ_N, d, DIFFEQ_EDGES, 3) is None
    assert mobility(DIFFEQ_N, d, DIFFEQ_EDGES, 6) == [2] * 5 + [3, 3, 4, 4, 4, 4]


def test_multicycle():
    # a two-step multiply feeds an add; a lone add can go anywhere
    delay = [2, 1, 1]
    edges = [(0, 1)]
    assert asap(3, delay, edges) == [1, 3, 1]
    assert alap(3, delay, edges, 3) == [1, 3, 3]
    assert alap(3, delay, edges, 5) == [3, 5, 5]
    assert alap(3, delay, edges, 2) is None
    assert latency_of(asap(3, delay, edges), delay) == 3


def test_cycle_rejected():
    with pytest.raises(ValueError):
        topological_order(3, [(0, 1), (1, 2), (2, 0)])
    with pytest.raises(ValueError):
        asap(2, [1, 1], [(0, 1), (1, 0)])


def test_against_longest_paths():
    rng = random.Random(5301)
    for _ in range(300):
        n = rng.randint(1, 9)
        delay, edges = random_dag(rng, n)
        early = asap(n, delay, edges)
        cp = latency_of(early, delay)
        assert cp == max(longest_to_sinks(n, delay, edges, v) for v in range(n))
        for v in range(n):
            assert early[v] == 1 + longest_from_sources(n, delay, edges, v)
        assert alap(n, delay, edges, cp - 1) is None
        for latency in (cp, cp + 2):
            late = alap(n, delay, edges, latency)
            for v in range(n):
                assert late[v] == latency + 1 - longest_to_sinks(n, delay, edges, v)
            assert latency_of(late, delay) == latency


def test_extremes_of_all_schedules():
    rng = random.Random(5302)
    for _ in range(120):
        n = rng.randint(1, 5)
        delay, edges = random_dag(rng, n, most=2)
        early = asap(n, delay, edges)
        cp = latency_of(early, delay)
        for latency in (cp, cp + 1):
            late = alap(n, delay, edges, latency)
            sched = list(feasible_schedules(n, delay, edges, latency))
            assert tuple(early) in sched and tuple(late) in sched
            for v in range(n):
                starts = {t[v] for t in sched}
                # the frame [ASAP, ALAP] is exactly the set of starts that some schedule uses
                assert starts == set(range(early[v], late[v] + 1))
        assert not list(feasible_schedules(n, delay, edges, cp - 1))
