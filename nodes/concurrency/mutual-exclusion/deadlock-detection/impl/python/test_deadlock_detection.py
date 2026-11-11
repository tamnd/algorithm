# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadlock-detection/. The authors are listed in prov/YGHDZH.jsonl.
import random

from deadlock_detection import deadlocked_in_wait_for_graph, detect, detect_fast, find_cycle, recover


def brute_force(avail, alloc, req):
    """Search the lattice of finished sets: a process is deadlocked iff no reachable set holds it."""
    n, m = len(alloc), len(avail)
    start = frozenset()
    seen, stack = {start}, [start]
    while stack:
        done = stack.pop()
        work = [avail[r] + sum(alloc[i][r] for i in done) for r in range(m)]
        for i in range(n):
            if i not in done and all(req[i][r] <= work[r] for r in range(m)):
                nxt = done | {i}
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    reach = set().union(*seen)
    return [i for i in range(n) if i not in reach]


def random_state(rng, n, m, cap=3):
    t = [rng.randint(1, cap) for _ in range(m)]
    alloc = [[0] * m for _ in range(n)]
    for r in range(m):
        for _ in range(rng.randint(0, t[r])):
            alloc[rng.randrange(n)][r] += 1
    avail = [t[r] - sum(alloc[i][r] for i in range(n)) for r in range(m)]
    req = [[rng.randint(0, t[r] - alloc[i][r]) if rng.random() < 0.4 else 0 for r in range(m)]
           for i in range(n)]
    return avail, alloc, req


EXAMPLE = (
    [0, 0, 0],
    [[1, 0, 1], [1, 1, 0], [0, 1, 0], [1, 0, 1]],
    [[0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 0, 0]],
)


def test_page_example():
    avail, alloc, req = EXAMPLE
    assert detect(avail, alloc, req) == []
    req2 = [row[:] for row in req]
    req2[3] = [0, 1, 0]
    assert detect(avail, alloc, req2) == [0, 1, 2, 3]
    req3 = [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 0, 0]]
    assert detect(avail, alloc, req3) == [0, 1, 2]  # p0 is on no cycle, yet deadlocked


def test_reduction_matches_brute_force():
    rng = random.Random(7)
    dead_seen = 0
    for _ in range(1500):
        n, m = rng.randint(1, 5), rng.randint(1, 3)
        s = random_state(rng, n, m)
        expect = brute_force(*s)
        assert detect(*s) == expect
        assert detect_fast(*s) == expect
        dead_seen += bool(expect)
    assert dead_seen > 20


def test_order_does_not_matter():
    rng = random.Random(8)
    for _ in range(300):
        avail, alloc, req = random_state(rng, 5, 2)
        perm = list(range(5))
        rng.shuffle(perm)
        d1 = detect(avail, alloc, req)
        d2 = detect(avail, [alloc[i] for i in perm], [req[i] for i in perm])
        assert sorted(perm[j] for j in d2) == d1


def test_single_unit_wait_for_graph():
    rng = random.Random(9)
    for _ in range(500):
        n = m = 4
        avail, alloc, req = [1] * m, [[0] * m for _ in range(n)], [[0] * m for _ in range(n)]
        for r in range(m):
            if rng.random() < 0.8:
                alloc[rng.randrange(n)][r], avail[r] = 1, 0
        for i in range(n):
            r = rng.randrange(m)
            if alloc[i][r] == 0 and avail[r] == 0 and rng.random() < 0.7:
                req[i][r] = 1
        succ = {i: {j for r in range(m) if req[i][r] for j in range(n) if alloc[j][r]} for i in range(n)}
        dead = deadlocked_in_wait_for_graph(succ)
        assert sorted(dead) == detect(avail, alloc, req)
        assert (find_cycle(succ) is not None) == bool(dead)


def test_find_cycle_returns_a_cycle():
    succ = {0: {1}, 1: {2}, 2: {3}, 3: {1}, 4: {0}}
    c = find_cycle(succ)
    assert c is not None and sorted(c) == [1, 2, 3]
    assert all(c[(k + 1) % len(c)] in succ[c[k]] for k in range(len(c)))
    assert deadlocked_in_wait_for_graph(succ) == {0, 1, 2, 3, 4}
    assert find_cycle({0: {1}, 1: set()}) is None


def test_recovery_by_victim_choice():
    rng = random.Random(10)
    for _ in range(300):
        avail, alloc, req = random_state(rng, 5, 3)
        held = [sum(row) for row in alloc]
        dead = detect(avail, alloc, req)
        victims = recover(avail, alloc, req, cost=lambda i: -held[i])
        assert set(victims) <= set(dead)
        assert bool(victims) == bool(dead)
        assert len(victims) <= len(dead)
