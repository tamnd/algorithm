# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/van-ginneken-buffer-insertion/. The authors are listed in prov/98230Y.jsonl.

import random
from fractions import Fraction
from itertools import product

from van_ginneken_buffer_insertion import merge, prune, van_ginneken


def slack_of(parent, wire_r, wire_c, sinks, place, buffers, driver_r, driver_d):
    """Slack of one buffer placement, from the Elmore sum over R_ik C_k of
    every stage, with no use of the candidate lists."""
    n = len(parent)
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)
    arrival_in = {0: Fraction(0)}
    worst = None
    todo = [0]
    while todo:
        d = todo.pop()
        if d == 0:
            rd, dd = driver_r, driver_d
        else:
            _, rd, dd = buffers[place[d]]
        nodes, stack = [d], [d]
        while stack:
            u = stack.pop()
            if u != d and (u in place or u in sinks):
                continue
            for w in children[u]:
                nodes.append(w)
                stack.append(w)
        cap = {}
        for u in nodes:
            c = Fraction(0) if u == d else Fraction(wire_c[u], 2)
            if u != d and u in place:
                c += buffers[place[u]][0]
            elif u in sinks:
                c += sinks[u][0]
            else:
                c += sum(Fraction(wire_c[w], 2) for w in children[u])
            cap[u] = c

        def path(u):
            p = []
            while u != d:
                p.append(u)
                u = parent[u]
            return set(p)

        paths = {u: path(u) for u in nodes}
        for i in nodes:
            if i == d or not (i in place or i in sinks):
                continue
            t = Fraction(0)
            for k in nodes:
                common = paths[i] & paths[k]
                t += (rd + sum(wire_r[e] for e in common)) * cap[k]
            at = arrival_in[d] + dd + t
            if i in place:
                arrival_in[i] = at
                todo.append(i)
            else:
                s = sinks[i][1] - at
                worst = s if worst is None else min(worst, s)
    return worst


def random_net(rng, m):
    parent = [-1] + [rng.randrange(v) for v in range(1, m)]
    # split some edges with a node of degree two, as a buffer site on the wire
    for v in range(1, m):
        if rng.random() < 0.4:
            parent.append(parent[v])
            parent[v] = len(parent) - 1
    n = len(parent)
    has_child = [False] * n
    for v in range(1, n):
        has_child[parent[v]] = True
    wire_r = [0] + [rng.randint(0, 4) for _ in range(1, n)]
    wire_c = [0] + [rng.randint(0, 4) for _ in range(1, n)]
    sinks = {v: (Fraction(rng.randint(1, 3)), Fraction(rng.randint(10, 80))) for v in range(1, n) if not has_child[v]}
    positions = [v for v in range(1, n) if has_child[v] and rng.random() < 0.8]
    return parent, wire_r, wire_c, sinks, positions


def brute(parent, wire_r, wire_c, sinks, positions, buffers, driver_r, driver_d):
    best = None
    for pick in product(range(len(buffers) + 1), repeat=len(positions)):
        place = {v: b - 1 for v, b in zip(positions, pick) if b > 0}
        s = slack_of(parent, wire_r, wire_c, sinks, place, buffers, driver_r, driver_d)
        best = s if best is None else max(best, s)
    return best


def test_against_enumeration(rng=random.Random(98230)):
    done = 0
    while done < 300:
        m = rng.randint(2, 8)
        parent, wire_r, wire_c, sinks, positions = random_net(rng, m)
        if len(positions) > 6:
            continue
        nb = rng.choice([1, 1, 2])
        buffers = [(Fraction(rng.randint(1, 2)), Fraction(rng.randint(1, 3)), Fraction(rng.randint(0, 4))) for _ in range(nb)]
        driver_r, driver_d = Fraction(rng.randint(1, 5)), Fraction(rng.randint(0, 2))
        args = (parent, wire_r, wire_c, sinks, set(positions), buffers, driver_r, driver_d)
        slack, place, largest = van_ginneken(*args)
        assert slack == brute(parent, wire_r, wire_c, sinks, positions, buffers, driver_r, driver_d)
        assert set(place) <= set(positions)
        assert slack_of(parent, wire_r, wire_c, sinks, place, buffers, driver_r, driver_d) == slack
        if nb == 1:
            assert largest <= len(sinks) + len(positions)
        done += 1


def test_no_positions_gives_plain_elmore(rng=random.Random(7)):
    for _ in range(40):
        parent, wire_r, wire_c, sinks, _ = random_net(rng, rng.randint(2, 9))
        buffers = [(Fraction(1), Fraction(1), Fraction(1))]
        slack, place, _ = van_ginneken(parent, wire_r, wire_c, sinks, set(), buffers, Fraction(2), Fraction(0))
        assert place == {}
        assert slack == slack_of(parent, wire_r, wire_c, sinks, {}, buffers, Fraction(2), Fraction(0))


def test_prune_and_merge():
    assert prune([(1, 5, None), (2, 5, None), (2, 7, None), (3, 6, None), (4, 9, None)]) == [(1, 5, None), (2, 7, None), (4, 9, None)]
    a = [(1, 3, "a1"), (2, 6, "a2")]
    b = [(1, 4, "b1"), (3, 8, "b2")]
    got = [(c, q) for c, q, _ in merge(a, b)]
    assert got == [(2, 3), (3, 4), (5, 6)]


def test_example_of_the_page():
    # source 0 - 1 - 2, and 2 branches to sink 3 and, through node 4, to sink 5
    parent = [-1, 0, 1, 2, 2, 4]
    wire_r = [0, 2, 1, 1, 2, 2]
    wire_c = [0, 2, 2, 2, 2, 2]
    sinks = {3: (Fraction(1), Fraction(40)), 5: (Fraction(1), Fraction(60))}
    buffers = [(Fraction(1), Fraction(1), Fraction(2))]
    slack, place, _ = van_ginneken(parent, wire_r, wire_c, sinks, {1, 2, 4}, buffers, Fraction(3), Fraction(0))
    assert slack == 10 and place == {1: 0, 2: 0, 4: 0}
    assert slack == brute(parent, wire_r, wire_c, sinks, [1, 2, 4], buffers, Fraction(3), Fraction(0))
    assert slack_of(parent, wire_r, wire_c, sinks, {}, buffers, Fraction(3), Fraction(0)) == -29
    assert slack == slack_of(parent, wire_r, wire_c, sinks, place, buffers, Fraction(3), Fraction(0))
