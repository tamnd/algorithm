# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timed-event-graph/. The authors are listed in prov/KGRQ21.jsonl.

import random
from collections import deque
from fractions import Fraction

import pytest

from timed_event_graph import EPS, mp_matvec, mp_mul, mp_star, simulate, teg_matrix

# Two transitions; every place holds one token.
TWO = [(0, 0, 1, 3), (1, 1, 1, 4), (1, 0, 1, 7), (0, 1, 1, 2)]

# A production line: t0 = start on machine 1, t1 = start on machine 2,
# t2 = the part leaves. One pallet circulates.
LINE = [
    (0, 0, 1, 3),  # machine 1 is busy 3 per part
    (0, 1, 0, 3),  # the part reaches machine 2 after 3
    (1, 1, 1, 4),  # machine 2 is busy 4 per part
    (1, 2, 0, 4),  # the part leaves after 4 on machine 2
    (2, 0, 1, 0),  # the pallet goes back to machine 1 at once
]


def token_game(n, places, x0, k, rng):
    """Fire enabled transitions in a random order; tokens leave places in FIFO order."""
    queues = [deque() for _ in places]
    for idx, (j, _, m, tau) in enumerate(places):
        if m == 1:
            queues[idx].append(x0[j] + tau)
    ins = [[idx for idx, p in enumerate(places) if p[1] == i] for i in range(n)]
    outs = [[idx for idx, p in enumerate(places) if p[0] == i] for i in range(n)]
    times = [[] for _ in range(n)]
    while True:
        ready = [i for i in range(n) if len(times[i]) < k and all(queues[idx] for idx in ins[i])]
        if not ready:
            break
        i = rng.choice(ready)
        t = max(queues[idx].popleft() for idx in ins[i])
        times[i].append(t)
        for idx in outs[i]:
            queues[idx].append(t + places[idx][3])
    return times


def elementary_circuit_means(a):
    """All circuit means of the graph of a, by brute force over simple paths."""
    n = len(a)
    means = []

    def dfs(start, node, weight, length, seen):
        for nxt in range(n):
            w = a[nxt][node]  # arc node -> nxt
            if w == EPS or nxt < start:
                continue
            if nxt == start:
                means.append(Fraction(weight + w) / (length + 1))
            elif nxt not in seen:
                dfs(start, nxt, weight + w, length + 1, seen | {nxt})

    for s in range(n):
        dfs(s, s, 0, 0, {s})
    return means


def strongly_connected(a):
    n = len(a)
    for s in range(n):
        seen, stack = {s}, [s]
        while stack:
            u = stack.pop()
            for v in range(n):
                if a[v][u] != EPS and v not in seen:
                    seen.add(v)
                    stack.append(v)
        if len(seen) < n:
            return False
    return True


def random_teg(rng, n):
    order = list(range(n))
    rng.shuffle(order)
    rank = {t: r for r, t in enumerate(order)}
    places = [(i, i, 1, rng.randint(0, 5)) for i in range(n)]
    for _ in range(rng.randint(n, 3 * n)):
        j, i = rng.randrange(n), rng.randrange(n)
        tau = rng.randint(0, 9)
        if rank[j] < rank[i] and rng.random() < 0.5:
            places.append((j, i, 0, tau))  # zero-token places follow the order, so they form no circuit
        else:
            places.append((j, i, 1, tau))
    return places


def test_two_transition_example():
    a = teg_matrix(2, TWO)
    assert a == [[3, 7], [2, 4]]
    xs = simulate(a, [0, 0], 5)
    assert xs == [[0, 0], [7, 4], [11, 9], [16, 13], [20, 18], [25, 22]]
    # cycle time 4.5 and cyclicity 2: A^4 = 9 + A^2
    a2 = mp_mul(a, a)
    a4 = mp_mul(a2, a2)
    assert a2 == [[9, 11], [6, 9]]
    assert a4 == [[v + 9 for v in row] for row in a2]
    assert max(elementary_circuit_means(a)) == Fraction(9, 2)


def test_production_line_uses_the_star():
    a = teg_matrix(3, LINE)
    assert a == [[3, EPS, 0], [6, 4, 3], [10, 8, 7]]
    xs = simulate(a, [-3, -4, 0], 3)
    assert xs[1] == [0, 3, 7]
    assert xs[2] == [7, 10, 14]
    assert xs[3] == [14, 17, 21]
    assert max(elementary_circuit_means(a)) == 7


def test_star_rejects_a_token_free_circuit():
    with pytest.raises(ValueError):
        teg_matrix(2, [(0, 1, 0, 1), (1, 0, 0, 1)])
    with pytest.raises(ValueError):
        teg_matrix(1, [(0, 0, 0, 2)])


def test_star_matches_longest_paths():
    rng = random.Random(5)
    for _ in range(50):
        n = rng.randint(1, 5)
        a = [[EPS] * n for _ in range(n)]
        for i in range(n):
            for j in range(i):
                if rng.random() < 0.5:
                    a[i][j] = rng.randint(-3, 6)  # arcs j -> i with j < i: acyclic
        s = mp_star(a)
        # longest path by dynamic programming in topological order
        for src in range(n):
            best = [EPS] * n
            best[src] = 0
            for v in range(src + 1, n):
                best[v] = max([best[u] + a[v][u] for u in range(src, v)] + [EPS])
            assert [s[v][src] for v in range(n)] == best


def test_recurrence_matches_token_game():
    rng = random.Random(2024)
    for _ in range(150):
        n = rng.randint(1, 5)
        places = random_teg(rng, n)
        a = teg_matrix(n, places)
        x0 = [rng.randint(-5, 5) for _ in range(n)]
        k = 12
        xs = simulate(a, x0, k)
        times = token_game(n, places, x0, k, rng)
        for i in range(n):
            assert times[i] == [xs[r][i] for r in range(1, k + 1)]


def test_cycle_time_is_the_maximum_cycle_mean():
    rng = random.Random(77)
    tested = 0
    for _ in range(200):
        n = rng.randint(1, 4)
        places = random_teg(rng, n)
        a = teg_matrix(n, places)
        if not strongly_connected(a):
            continue
        tested += 1
        lam = max(elementary_circuit_means(a))
        x0 = [rng.randint(-5, 5) for _ in range(n)]
        x = x0
        for _ in range(400):
            x = mp_matvec(a, x)
        # eventually periodic: x(k + c) = x(k) + c lam for some c
        y, found = x, False
        for c in range(1, 25):
            y = mp_matvec(a, y)
            if all(yi - xi == c * lam for xi, yi in zip(x, y)):
                found = True
                break
        assert found
    assert tested > 40
