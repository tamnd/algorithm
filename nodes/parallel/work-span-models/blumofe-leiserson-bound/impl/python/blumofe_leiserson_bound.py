# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blumofe-leiserson-bound/. The authors are listed in prov/4P69AP.jsonl.

"""Checks of the potential-function proof of the work-stealing bound.

The module runs randomized work stealing on a fork-join DAG of unit nodes
(the same scheduler as on the work-stealing page: work first, owner at the
bottom of its deque, thieves at the top, one action per processor per step)
and computes, after each step, the quantities of the proof by Arora,
Blumofe and Plaxton:

- the designated parent of each enabled node (the predecessor whose
  execution enabled it), its depth d in the enabling tree, and its weight
  w = T_inf - d;
- the potential 3^(2w - 1) of an assigned node and 3^(2w) of a node in a
  deque, and the total potential Phi.

It also gives the exact probability of the balls-and-weighted-bins event by
enumeration, for small numbers of bins. Standard library only. The cost is
O(T_p * (p + total deque size)) per run.
"""

import itertools
import random
from collections import deque
from fractions import Fraction
from typing import Callable, Hashable, Mapping, Sequence


def build_dag(program: Mapping[Hashable, Sequence[tuple]], root: Hashable):
    """Unfold a fork-join program into (succ, child): unit nodes, node 0 the root.

    Statements: ("work", k), ("spawn", g), ("call", g), ("sync",). Each
    procedure has an entry node, an exit node and an implicit final sync.
    child[s] is the first node of the child spawned by spawn node s.
    """
    succ: list[list[int]] = []
    child: dict[int, int] = {}

    def new(preds: Sequence[int]) -> int:
        succ.append([])
        for u in preds:
            succ[u].append(len(succ) - 1)
        return len(succ) - 1

    def instance(name: Hashable, pred: int | None) -> tuple[int, int]:
        entry = new([] if pred is None else [pred])
        cur, pending = entry, []
        for st in program[name]:
            if st[0] == "work":
                for _ in range(st[1]):
                    cur = new([cur])
            elif st[0] == "spawn":
                s = new([cur])
                c_entry, c_exit = instance(st[1], s)
                child[s] = c_entry
                pending.append(c_exit)
                cur = s
            elif st[0] == "call":
                _, cur = instance(st[1], cur)
            elif st[0] == "sync" and pending:
                cur, pending = new([cur, *pending]), []
        if pending:
            cur = new([cur, *pending])
        return entry, new([cur])

    instance(root, None)
    return succ, child


def span(succ: list[list[int]]) -> int:
    """Nodes on a longest path; node ids are a topological order."""
    longest = [1] * len(succ)
    for u in range(len(succ)):
        for v in succ[u]:
            longest[v] = max(longest[v], longest[u] + 1)
    return max(longest, default=0)


def run(succ: list[list[int]], child: dict[int, int], p: int, rng: random.Random,
        on_step: Callable[[list, list, dict], None] | None = None) -> dict:
    """Randomized work stealing. on_step(assigned, deques, depth) runs after each step.

    depth[v] is the depth of v in the enabling tree (the root has depth 0).
    Returns the time, the steal attempts and the steps of each node.
    """
    n = len(succ)
    missing = [0] * n
    for vs in succ:
        for v in vs:
            missing[v] += 1
    assigned: list[int | None] = [None] * p
    deques = [deque() for _ in range(p)]  # left = top, right = bottom
    depth = {0: 0} if n else {}
    if n:
        assigned[0] = 0
    done = attempts = t = 0
    while done < n:
        t += 1
        thieves = []
        for q in range(p):
            u = assigned[q]
            if u is None:
                thieves.append(q)
                continue
            done += 1
            enabled = []
            for v in succ[u]:
                missing[v] -= 1
                if missing[v] == 0:
                    depth[v] = depth[u] + 1  # u is the designated parent of v
                    enabled.append(v)
            if len(enabled) == 2:
                c = child[u]
                deques[q].append(enabled[0] if enabled[1] == c else enabled[1])
                assigned[q] = c
            elif len(enabled) == 1:
                assigned[q] = enabled[0]
            else:
                assigned[q] = deques[q].pop() if deques[q] else None
        for q in thieves:
            attempts += 1
            if p > 1:
                r = rng.randrange(p - 1)
                r += r >= q
                if deques[r]:
                    assigned[q] = deques[r].popleft()
        if on_step is not None:
            on_step(assigned, deques, depth)
    return {"time": t, "attempts": attempts}


def potential(assigned: list, deques: list, depth: dict, tinf: int) -> tuple[int, list[int]]:
    """The total potential and the potential of each processor."""
    per = []
    for q in range(len(assigned)):
        phi = 0
        if assigned[q] is not None:
            phi += 3 ** (2 * (tinf - depth[assigned[q]]) - 1)
        for v in deques[q]:
            phi += 3 ** (2 * (tinf - depth[v]))
        per.append(phi)
    return sum(per), per


def balls_in_weighted_bins(weights: Sequence[Fraction], beta: Fraction) -> Fraction:
    """Exact Pr[X >= beta * W] when len(weights) balls fall into the bins uniformly.

    X is the total weight of the bins that get at least one ball, and W is
    the sum of the weights. Enumerates all P^P outcomes, so use P <= 6.
    """
    p = len(weights)
    total = sum(weights)
    good = 0
    for throw in itertools.product(range(p), repeat=p):
        if sum(weights[i] for i in set(throw)) >= beta * total:
            good += 1
    return Fraction(good, p ** p)
