# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/consistent-cut/. The authors are listed in prov/5MWFYB.jsonl.

"""Cuts of a recorded distributed computation, their consistency, and the
lattice that the consistent cuts form.

A computation has n processes. Process i has a list of events; an event is
("int",), ("send", m, dest) or ("recv", m, src), where m is a message id.
A cut is a tuple k = (k_0, ..., k_(n-1)): it holds the first k_i events of
process i. The frontier event of process i is its event number k_i (1-based),
or none when k_i = 0.

The cut is consistent when no event in it is a receive whose send is outside
it. With vector clocks VC (VC(e)[j] = the number of events of j that happened
before or at e), the cut is consistent iff VC(e_j)[i] <= k_i for every frontier
event e_j and every i.
"""

import itertools
import random

Event = tuple
Computation = list[list[Event]]
Cut = tuple[int, ...]


def random_computation(n: int, steps: int, rng: random.Random, p_send: float = 0.4, p_recv: float = 0.4) -> Computation:
    """A seeded run: at each step one process does an internal event, sends to
    another process, or receives any message in transit to it (not FIFO)."""
    comp: Computation = [[] for _ in range(n)]
    transit: list[tuple[int, int, int]] = []  # (m, src, dest)
    mid = 0
    for _ in range(steps):
        i = rng.randrange(n)
        mine = [x for x in transit if x[2] == i]
        r = rng.random()
        if mine and r < p_recv:
            x = rng.choice(mine)
            transit.remove(x)
            comp[i].append(("recv", x[0], x[1]))
        elif n > 1 and r < p_recv + p_send:
            dest = rng.choice([j for j in range(n) if j != i])
            comp[i].append(("send", mid, dest))
            transit.append((mid, i, dest))
            mid += 1
        else:
            comp[i].append(("int",))
    return comp


def vector_clocks(comp: Computation) -> list[list[tuple[int, ...]]]:
    """VC of each event, by the rules of Fidge and Mattern. Runs the processes in
    any order that respects the messages."""
    n = len(comp)
    vc: list[list[tuple[int, ...]]] = [[] for _ in range(n)]
    sent: dict[int, tuple[int, ...]] = {}
    pos = [0] * n
    cur = [[0] * n for _ in range(n)]
    total = sum(len(p) for p in comp)
    done = 0
    while done < total:
        progress = False
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
                vc[i].append(tuple(cur[i]))
                pos[i] += 1
                done += 1
                progress = True
        if not progress:
            raise ValueError("a receive has no send")
    return vc


def frontier_vc(vc, cut: Cut) -> list[tuple[int, ...]]:
    n = len(cut)
    return [vc[j][cut[j] - 1] if cut[j] > 0 else tuple(0 for _ in range(n)) for j in range(n)]


def is_consistent(comp: Computation, cut: Cut) -> bool:
    """The definition: each receive in the cut has its send in the cut."""
    inside_sends = {e[1] for i in range(len(comp)) for e in comp[i][: cut[i]] if e[0] == "send"}
    return all(e[1] in inside_sends for i in range(len(comp)) for e in comp[i][: cut[i]] if e[0] == "recv")


def is_consistent_vc(vc, cut: Cut) -> bool:
    """The vector clock test: VC(e_j)[i] <= k_i for all i and j."""
    f = frontier_vc(vc, cut)
    return all(f[j][i] <= cut[i] for i in range(len(cut)) for j in range(len(cut)))


def happened_before(vc, a: tuple[int, int], b: tuple[int, int]) -> bool:
    """a = (process, 1-based index). a -> b iff VC(a) <= VC(b) and a != b."""
    va, vb = vc[a[0]][a[1] - 1], vc[b[0]][b[1] - 1]
    return a != b and all(x <= y for x, y in zip(va, vb))


def is_consistent_frontier(comp: Computation, vc, cut: Cut) -> bool:
    """The successor form: no successor of a frontier event happened before a
    frontier event. Here a missing frontier (k_i = 0) has the first event of
    process i as its successor."""
    n = len(cut)
    for i in range(n):
        succ = (i, cut[i] + 1)
        if cut[i] + 1 > len(comp[i]):
            continue
        for j in range(n):
            if cut[j] > 0 and happened_before(vc, succ, (j, cut[j])):
                return False
    return True


def all_cuts(comp: Computation) -> list[Cut]:
    return list(itertools.product(*[range(len(p) + 1) for p in comp]))


def consistent_cuts(comp: Computation) -> list[Cut]:
    vc = vector_clocks(comp)
    return [c for c in all_cuts(comp) if is_consistent_vc(vc, c)]


def join(a: Cut, b: Cut) -> Cut:
    return tuple(max(x, y) for x, y in zip(a, b))


def meet(a: Cut, b: Cut) -> Cut:
    return tuple(min(x, y) for x, y in zip(a, b))


def pairwise_concurrent_frontier(vc, cut: Cut) -> bool:
    """A sufficient test only: the frontier events are pairwise concurrent.
    When k_i = 0 the frontier of i is a virtual initial event that happened
    before every event e with VC(e)[i] >= 1."""
    n = len(cut)
    for i in range(n):
        for j in range(n):
            if i == j or cut[j] == 0:
                continue  # nothing happens before a virtual initial event
            if cut[i] == 0:
                if vc[j][cut[j] - 1][i] >= 1:
                    return False
            elif happened_before(vc, (i, cut[i]), (j, cut[j])):
                return False
    return True
