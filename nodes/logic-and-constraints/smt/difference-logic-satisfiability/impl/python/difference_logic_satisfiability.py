# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/difference-logic-satisfiability/. The authors are listed in prov/K5P9JR.jsonl.

"""Decide a conjunction of difference constraints with Bellman-Ford.

A constraint (x, y, c) means x - y <= c, where x and y are variable indices
0 .. n-1 and c is an integer or a fraction. It becomes the edge y -> x with
weight c, because a model must have x <= y + c, the triangle inequality of
shortest paths. A virtual source has an edge of weight 0 to each variable,
which is the same as starting all distances at 0.

The result is (True, model) with model[v] = the shortest distance to v, or
(False, cycle) where cycle is a list of constraint indices that form a cycle
of negative total weight. The sum of the constraints on such a cycle reads
0 <= (a negative number), so they cannot all hold.
"""

from fractions import Fraction

Number = int | Fraction


def solve(n: int, constraints: list[tuple[int, int, Number]]) -> tuple[bool, list]:
    if n == 0:
        return True, []
    dist: list[Number] = [0] * n  # the virtual source gives each variable 0
    pred: list[int | None] = [None] * n  # the constraint that last lowered v
    last = None
    for _ in range(n):  # n rounds: n - 1 for the n + 1 vertices, plus one to detect
        last = None
        for k, (x, y, c) in enumerate(constraints):
            if dist[y] + c < dist[x]:
                dist[x] = dist[y] + c
                pred[x] = k
                last = x
        if last is None:
            return True, dist
    # Round n still changed a distance, so a negative cycle exists. Walk back
    # n steps along pred to be sure that we stand on the cycle.
    v = last
    for _ in range(n):
        v = constraints[pred[v]][1]
    cycle = []
    u = v
    while True:
        k = pred[u]
        cycle.append(k)
        u = constraints[k][1]
        if u == v:
            break
    cycle.reverse()
    return False, cycle


def check_model(constraints: list[tuple[int, int, Number]], model: list[Number]) -> bool:
    return all(model[x] - model[y] <= c for x, y, c in constraints)


def check_cycle(constraints: list[tuple[int, int, Number]], cycle: list[int]) -> bool:
    """The edges y -> x of the cycle must join head to tail and weigh < 0."""
    if not cycle:
        return False
    for a, b in zip(cycle, cycle[1:] + cycle[:1]):
        if constraints[a][0] != constraints[b][1]:  # head of a is tail of b
            return False
    return sum(constraints[k][2] for k in cycle) < 0
