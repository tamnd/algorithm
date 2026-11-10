# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/work-function-algorithm/. The authors are listed in prov/CQEK7R.jsonl.

import itertools
from typing import Dict, FrozenSet, List, Sequence, Tuple

Config = FrozenSet[int]


def config_distance(d: Sequence[Sequence[int]], a: Config, b: Config) -> int:
    """Cost of a minimum perfect matching between two configurations of equal size (brute force)."""
    xs, ys = sorted(a), sorted(b)
    return min(sum(d[x][y] for x, y in zip(xs, p)) for p in itertools.permutations(ys))


def initial_work_function(d: Sequence[Sequence[int]], k: int, start: Config) -> Dict[Config, int]:
    """w_0(X) = D(C_0, X) for every set X of k distinct points."""
    n = len(d)
    return {frozenset(x): config_distance(d, start, frozenset(x)) for x in itertools.combinations(range(n), k)}


def update_work_function(d: Sequence[Sequence[int]], w: Dict[Config, int], r: int) -> Dict[Config, int]:
    """w_t from w_{t-1}: w_t(X) = min over x in X of w_{t-1}(X - x + r) + d(x, r)."""
    out = {}
    for x_set, val in w.items():
        if r in x_set:
            out[x_set] = val
        else:
            out[x_set] = min(w[(x_set - {x}) | {r}] + d[x][r] for x in x_set)
    return out


def work_function_algorithm(
    d: Sequence[Sequence[int]], start: Sequence[int], requests: Sequence[int]
) -> Tuple[int, List[Config], List[Dict[Config, int]]]:
    """Serve requests on a finite metric with the work function algorithm (WFA).

    d: a symmetric distance matrix of a metric on the points 0 .. n-1.
    start: k distinct start points, with 1 <= k < n.
    Returns (cost, configurations C_0 .. C_m, work functions w_0 .. w_m).
    Each request costs O(C(n, k) * k) time to update the work function, and the
    tables take O(C(n, k)) space, so this is for small metrics only.
    """
    k = len(start)
    c: Config = frozenset(start)  # @line L1
    if len(c) != k:
        raise ValueError("the start points must be distinct")
    w = initial_work_function(d, k, c)  # @line L2
    cost = 0
    configs, works = [c], [w]
    for r in requests:  # @line L3
        w = update_work_function(d, w, r)  # @line L4
        if r not in c:  # @line L5
            s = min(sorted(c), key=lambda x: w[(c - {x}) | {r}] + d[x][r])  # @line L6
            cost += d[s][r]  # @line L7
            c = (c - {s}) | {r}  # @line L8
        configs.append(c)
        works.append(w)
    return cost, configs, works  # @line L9
