# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ef1-and-pareto-optimal-algorithm/. The authors are listed in prov/HCYFF2.jsonl.

from fractions import Fraction
from typing import Optional, Sequence


def bundles_of(owner: Sequence[int], n: int) -> list[list[int]]:
    bundles: list[list[int]] = [[] for _ in range(n)]
    for j, k in enumerate(owner):
        bundles[k].append(j)
    return bundles


def is_price_ef1(bundles: Sequence[Sequence[int]], p: Sequence[Fraction]) -> bool:
    """pEF1: for all agents i and k, p(x_i) >= p(x_k) - p_j for some good j of x_k."""
    spend = [sum((p[j] for j in b), Fraction(0)) for b in bundles]
    n = len(bundles)
    for k in range(n):
        if not bundles[k]:
            continue
        reduced = spend[k] - max(p[j] for j in bundles[k])
        if any(i != k and spend[i] < reduced for i in range(n)):
            return False
    return True


def bkv_exact(values: Sequence[Sequence], max_steps: int = 100000, stats: Optional[dict] = None) -> list[list[int]]:
    """Barman, Krishnamurthy and Vaish's market algorithm, exact variant (epsilon = 0).

    values[i][j] is the additive value of agent i for good j, a positive
    integer or Fraction (every value must be > 0). Returns the bundles of an
    allocation that is EF1 and Pareto optimal. If stats is a dict, it gets
    the final prices ("prices"), the numbers of swaps ("swaps") and of
    price rises ("rises"), and a list "trace" of the events, each a tuple
    (kind, owner of each good, prices) with kind "start", "swap" or "rise".

    The original algorithm rounds the values to powers of (1 + epsilon) and
    has a pseudo-polynomial bound for that version. Here epsilon = 0, all
    least spenders are sources of the hierarchy, and every number is an
    exact Fraction. When the function returns, the allocation is EF1 and
    PO; no bound on the number of steps is proved for epsilon = 0, so the
    loop stops with RuntimeError after max_steps swaps and rises. One step
    costs O(n m) time.
    """
    v = [[Fraction(x) for x in row] for row in values]
    n = len(v)
    if n == 0:
        raise ValueError("at least one agent is needed")
    m = len(v[0])
    if any(len(row) != m for row in v) or any(x <= 0 for row in v for x in row):
        raise ValueError("every agent needs a positive value for every good")
    owner = [max(range(n), key=lambda k: (v[k][j], -k)) for j in range(m)]  # @line L1
    p = [v[owner[j]][j] for j in range(m)]
    swaps = rises = 0
    trace = stats.setdefault("trace", []) if stats is not None else None
    if trace is not None:
        trace.append(("start", list(owner), list(p)))
    while True:  # @line L2
        if swaps + rises > max_steps:
            raise RuntimeError("step limit reached")
        x = bundles_of(owner, n)
        if is_price_ef1(x, p):  # @line L3
            break
        spend = [sum((p[j] for j in x[i]), Fraction(0)) for i in range(n)]
        ratio = [max(v[i][j] / p[j] for j in range(m)) for i in range(n)]
        mbb = [[j for j in range(m) if v[i][j] / p[j] == ratio[i]] for i in range(n)]
        pmin = min(spend)
        level = {i: 0 for i in range(n) if spend[i] == pmin}  # @line L4
        layers = [sorted(level)]
        while layers[-1]:
            nxt = set()
            for g in layers[-1]:
                for j in mbb[g]:
                    h = owner[j]
                    if h not in level:
                        level[h] = len(layers)
                        nxt.add(h)
            layers.append(sorted(nxt))
        swap = None
        for depth in range(1, len(layers)):  # @line L5
            for h in layers[depth]:
                for j in x[h]:
                    parents = [g for g in layers[depth - 1] if j in mbb[g]]
                    if parents and spend[h] - p[j] > pmin:
                        swap = (j, parents[0])
                        break
                if swap:
                    break
            if swap:
                break
        if swap:
            owner[swap[0]] = swap[1]  # @line L6
            swaps += 1
            if trace is not None:
                trace.append(("swap", list(owner), list(p)))
            continue
        tree = set(level)
        owned = [j for j in range(m) if owner[j] in tree]
        outside = [j for j in range(m) if owner[j] not in tree]
        cands1 = [ratio[h] * p[j] / v[h][j] for h in tree for j in outside]
        alpha1 = min(cands1) if cands1 else None  # @line L7
        rest = [k for k in range(n) if k not in tree]
        if pmin > 0:
            alpha2 = max((spend[k] - max(p[j] for j in x[k]) if x[k] else Fraction(0)) for k in rest) / pmin  # @line L8
            alpha3 = min(spend[k] for k in rest) / pmin  # @line L9
        else:
            alpha2 = alpha3 = None
        alpha = min(a for a in (alpha1, alpha2, alpha3) if a is not None)  # @line L10
        for j in owned:
            p[j] *= alpha
        rises += 1
        if trace is not None:
            trace.append(("rise", list(owner), list(p)))
        if alpha == alpha2:  # @line L11
            break
    if stats is not None:
        stats["prices"] = list(p)
        stats["swaps"] = swaps
        stats["rises"] = rises
    return bundles_of(owner, n)  # @line L12
