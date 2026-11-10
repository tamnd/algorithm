# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-conjunctive-predicate-detection/. The authors are listed in prov/A6CJ2B.jsonl.

"""Detection of a weak conjunctive predicate l_0 and l_1 and ... and l_(n-1),
after Garg and Waldecker (IEEE TPDS 1994).

Process i has local states s_i^0, s_i^1, ..., where s_i^a is the state after
its first a events. The vector clock of s_i^a is the vector clock of event a
(all zeros when a = 0), so V(s_i^a)[i] = a. A global state that takes s_i^(a_i)
from each process is consistent iff V(s_j^(a_j))[i] <= a_i for all i and j.

Each process sends to a checker the vector clock of every local state in which
its local predicate is true, in order. The checker keeps one FIFO queue per
process and removes a head that cannot be in any consistent global state with
the heads of the other queues.
"""

import itertools
import random
from collections import deque

Vec = tuple[int, ...]


def random_computation(n: int, steps: int, rng: random.Random) -> list[list[tuple]]:
    comp: list[list[tuple]] = [[] for _ in range(n)]
    transit: list[tuple[int, int, int]] = []
    mid = 0
    for _ in range(steps):
        i = rng.randrange(n)
        mine = [x for x in transit if x[2] == i]
        r = rng.random()
        if mine and r < 0.4:
            x = rng.choice(mine)
            transit.remove(x)
            comp[i].append(("recv", x[0], x[1]))
        elif r < 0.8:
            dest = rng.choice([j for j in range(n) if j != i])
            comp[i].append(("send", mid, dest))
            transit.append((mid, i, dest))
            mid += 1
        else:
            comp[i].append(("int",))
    return comp


def state_clocks(comp: list[list[tuple]]) -> list[list[Vec]]:
    """V(s_i^a) for a = 0 .. len(comp[i])."""
    n = len(comp)
    out: list[list[Vec]] = [[tuple([0] * n)] for _ in range(n)]
    sent: dict[int, Vec] = {}
    pos = [0] * n
    cur = [[0] * n for _ in range(n)]
    left = sum(len(p) for p in comp)
    while left:
        moved = False
        for i in range(n):
            while pos[i] < len(comp[i]):
                e = comp[i][pos[i]]
                if e[0] == "recv":
                    if e[1] not in sent:
                        break
                    cur[i] = [max(a, b) for a, b in zip(cur[i], sent[e[1]])]
                cur[i][i] += 1
                if e[0] == "send":
                    sent[e[1]] = tuple(cur[i])
                out[i].append(tuple(cur[i]))
                pos[i] += 1
                left -= 1
                moved = True
        if not moved:
            raise ValueError("a receive has no send")
    return out


def candidates(clocks: list[list[Vec]], pred: list[list[bool]]) -> list[list[Vec]]:
    """The vectors each process sends to the checker."""
    return [[v for v, ok in zip(clocks[i], pred[i]) if ok] for i in range(len(clocks))]


def detect(queues: list[list[Vec]]) -> tuple[tuple[int, ...] | None, int]:
    """Return (the cut a with a_i = V(head_i)[i], or None) and the number of
    scalar comparisons the checker made."""
    n = len(queues)
    ptr = [0] * n
    if any(not q for q in queues):
        return None, 0
    head = lambda k: queues[k][ptr[k]]
    todo = deque(range(n))  # @line L1
    queued = [True] * n
    cmp = 0
    while todo:
        i = todo.popleft()
        queued[i] = False
        for j in range(n):
            if j == i:
                continue
            cmp += 1
            if head(j)[i] > head(i)[i]:  # @line L2
                ptr[i] += 1  # @line L3
                if ptr[i] == len(queues[i]):
                    return None, cmp  # @line L4
                todo.append(i)
                queued[i] = True
                break
            cmp += 1
            if head(i)[j] > head(j)[j]:  # @line L5
                ptr[j] += 1
                if ptr[j] == len(queues[j]):
                    return None, cmp
                if not queued[j]:
                    todo.append(j)
                    queued[j] = True
    return tuple(head(k)[k] for k in range(n)), cmp  # @line L6


def consistent(vs: tuple[Vec, ...]) -> bool:
    n = len(vs)
    return all(vs[j][i] <= vs[i][i] for i in range(n) for j in range(n))


def brute_force(queues: list[list[Vec]]) -> list[tuple[int, ...]]:
    """Every consistent choice of one candidate per process, as a cut."""
    out = []
    for vs in itertools.product(*queues):
        if consistent(vs):
            out.append(tuple(v[k] for k, v in enumerate(vs)))
    return out
