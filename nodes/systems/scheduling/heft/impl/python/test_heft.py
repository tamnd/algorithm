# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heft/. The authors are listed in prov/PKPCT3.jsonl.

import itertools
import random
from fractions import Fraction

from heft import heft, makespan, upward_ranks

# The example of Topcuoglu, Hariri and Wu (2002): 10 tasks, 3 processors.
# Tasks n1 .. n10 are 0 .. 9 here.
W = [[14, 16, 9], [13, 19, 18], [11, 13, 19], [13, 8, 17], [12, 13, 10],
     [13, 16, 9], [7, 15, 11], [5, 11, 14], [18, 12, 20], [21, 7, 16]]
E = {(0, 1): 18, (0, 2): 12, (0, 3): 9, (0, 4): 11, (0, 5): 14, (1, 7): 19, (1, 8): 16,
     (2, 6): 23, (3, 7): 27, (3, 8): 23, (4, 8): 13, (5, 7): 15, (6, 9): 17, (7, 9): 11, (8, 9): 13}


def check_feasible(w, comm, slots):
    for (i, j), c in comm.items():
        delay = 0 if slots[i].proc == slots[j].proc else c
        assert slots[j].start >= slots[i].finish + delay
    for s in slots:
        assert s.finish - s.start == w[s.task][s.proc] and s.start >= 0
    for a, b in itertools.combinations(slots, 2):
        if a.proc == b.proc:
            assert a.finish <= b.start or b.finish <= a.start


def ranks_by_paths(w, comm):
    """rank_u(i) as the heaviest path from i to an exit task, by enumeration of all paths."""
    n = len(w)
    mean = [Fraction(sum(row), len(row)) for row in w]
    succ = [[] for _ in range(n)]
    for (i, j) in comm:
        succ[i].append(j)
    out = []
    for s in range(n):
        best = Fraction(0)
        stack = [(s, mean[s])]
        while stack:
            v, length = stack.pop()
            if not succ[v]:
                best = max(best, length)
            for x in succ[v]:
                stack.append((x, length + comm[(v, x)] + mean[x]))
        out.append(best)
    return out


def optimum(w, comm):
    """The least makespan over all processor choices and all task lists, each task
    started as early as possible after the tasks before it on its processor."""
    n, q = len(w), len(w[0])
    pred = [[] for _ in range(n)]
    for (i, j) in comm:
        pred[j].append(i)
    best = None
    for perm in itertools.permutations(range(n)):
        pos = {t: x for x, t in enumerate(perm)}
        if any(pos[i] > pos[j] for (i, j) in comm):
            continue
        for procs in itertools.product(range(q), repeat=n):
            free = [0] * q
            fin = [0] * n
            for t in perm:
                ready = max((fin[i] + (0 if procs[i] == procs[t] else comm[(i, t)]) for i in pred[t]), default=0)
                fin[t] = max(ready, free[procs[t]]) + w[t][procs[t]]
                free[procs[t]] = fin[t]
            m = max(fin)
            best = m if best is None else min(best, m)
    return best


def random_instance(rng, n, q):
    w = [[rng.randrange(1, 10) for _ in range(q)] for _ in range(n)]
    comm = {(i, j): rng.randrange(0, 8) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.4}
    return w, comm


def test_paper_example() -> None:
    rank, order, slots = heft(W, E)
    assert [round(float(x), 3) for x in rank] == [108.0, 77.0, 80.0, 80.0, 69.0, 63.333, 42.667, 35.667, 44.333, 14.667]
    assert [i + 1 for i in order] == [1, 3, 4, 2, 5, 6, 9, 7, 8, 10]
    assert makespan(slots) == 80
    got = [(s.task + 1, s.proc + 1, int(s.start), int(s.finish)) for s in slots]
    assert got == [(1, 3, 0, 9), (2, 1, 27, 40), (3, 3, 9, 28), (4, 2, 18, 26), (5, 3, 28, 38),
                   (6, 2, 26, 42), (7, 3, 38, 49), (8, 1, 57, 62), (9, 2, 56, 68), (10, 2, 73, 80)]
    check_feasible(W, E, slots)


def test_edges() -> None:
    assert heft([], {}) == ([], [], [])
    rank, order, slots = heft([[4, 2]], {})
    assert rank == [3] and order == [0] and (slots[0].proc, slots[0].finish) == (1, 2)
    # a large transfer keeps the chain on one processor
    _, _, slots = heft([[3, 3], [3, 3]], {(0, 1): 100})
    assert slots[0].proc == slots[1].proc and makespan(slots) == 6


def test_ranks_and_feasibility() -> None:
    rng = random.Random(2002)
    for _ in range(200):
        n, q = rng.randrange(1, 9), rng.randrange(1, 4)
        w, comm = random_instance(rng, n, q)
        rank, order, slots = heft(w, comm)
        assert rank == upward_ranks(w, comm) == ranks_by_paths(w, comm)
        pos = {t: x for x, t in enumerate(order)}
        assert all(pos[i] < pos[j] and rank[i] > rank[j] for (i, j) in comm)
        assert all(rank[order[x]] >= rank[order[x + 1]] for x in range(n - 1))
        check_feasible(w, comm, slots)


def test_small_instance_of_the_page() -> None:
    # the greedy first step puts t1 on P2 and then pays for both transfers
    w, comm = [[4, 3], [2, 6], [1, 7]], {(0, 1): 2, (0, 2): 6}
    rank, order, slots = heft(w, comm)
    assert rank == [Fraction(27, 2), 4, 4] and order == [0, 1, 2]
    assert [(s.proc, s.start, s.finish) for s in slots] == [(1, 0, 3), (0, 5, 7), (0, 9, 10)]
    assert makespan(slots) == 10 and optimum(w, comm) == 7
    check_feasible(w, comm, slots)


def test_heuristic_not_optimal() -> None:
    rng = random.Random(5)
    worse = 0
    for _ in range(60):
        w, comm = random_instance(rng, rng.randrange(2, 5), 2)
        h, best = makespan(heft(w, comm)[2]), optimum(w, comm)
        assert h >= best
        worse += h > best
    assert worse > 0
