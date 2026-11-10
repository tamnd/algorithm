# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-makespan-inapproximability/. The authors are listed in prov/KVD1F4.jsonl.
"""The gap lemma for integer makespans and the clique reduction for unit jobs with precedence.

A unit-job instance is (m, njobs, arcs): m machines, jobs 0 .. njobs-1, and arcs (a, b) meaning that a
ends before b starts. For small instances only: the feasibility test searches all slot assignments.
"""

from itertools import combinations


def gap_threshold(t: int) -> float:
    """If deciding OPT <= t is NP-hard and OPT is an integer, every ratio below (t + 1) / t is NP-hard."""
    return (t + 1) / t


def decides(t: int, rho: float, alg_value: int) -> bool:
    """With ratio rho < (t + 1) / t, an algorithm value of at most t means OPT <= t."""
    assert rho < gap_threshold(t)
    return alg_value <= t


def clique_to_prec(nv: int, edges: list[tuple[int, int]], k: int) -> tuple[int, int, list[tuple[int, int]]]:
    """The Lenstra and Rinnooy Kan instance: vertex jobs, edge jobs and three filler layers X, Y, Z."""
    ne = len(edges)
    l = k * (k - 1) // 2
    m = max(k, l + nv - k, ne - l) + 1
    arcs = []
    for i, (u, v) in enumerate(edges):
        arcs += [(u, nv + i), (v, nv + i)]
    base = nv + ne
    nx, ny, nz = m - k, m - l - nv + k, m - ne + l
    xs = list(range(base, base + nx))
    ys = list(range(base + nx, base + nx + ny))
    zs = list(range(base + nx + ny, base + nx + ny + nz))
    arcs += [(x, y) for x in xs for y in ys] + [(y, z) for y in ys for z in zs]
    return m, base + nx + ny + nz, arcs


def feasible(t: int, m: int, njobs: int, arcs: list[tuple[int, int]]) -> bool:
    """Is there a schedule of the unit jobs in t slots on m machines?"""
    preds = [[] for _ in range(njobs)]
    succs = [[] for _ in range(njobs)]
    for a, b in arcs:
        preds[b].append(a)
        succs[a].append(b)
    order, indeg = [], [len(p) for p in preds]
    ready = [j for j in range(njobs) if indeg[j] == 0]
    while ready:
        j = ready.pop()
        order.append(j)
        for s in succs[j]:
            indeg[s] -= 1
            if indeg[s] == 0:
                ready.append(s)
    tail = [0] * njobs
    for j in reversed(order):
        tail[j] = max((tail[s] + 1 for s in succs[j]), default=0)
    slot = [0] * njobs
    load = [0] * (t + 1)

    def place(i: int) -> bool:
        if i == len(order):
            return True
        j = order[i]
        lo = max((slot[p] + 1 for p in preds[j]), default=1)
        for s in range(lo, t - tail[j] + 1):
            if load[s] < m:
                slot[j], load[s] = s, load[s] + 1
                if place(i + 1):
                    return True
                load[s] -= 1
        return False

    return place(0)


def has_clique(nv: int, edges: list[tuple[int, int]], k: int) -> bool:
    es = set(edges) | {(v, u) for u, v in edges}
    return any(all((a, b) in es for a, b in combinations(c, 2)) for c in combinations(range(nv), k))
