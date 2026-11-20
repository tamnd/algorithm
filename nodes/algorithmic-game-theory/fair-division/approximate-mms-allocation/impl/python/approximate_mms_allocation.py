# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-mms-allocation/. The authors are listed in prov/1VB5JR.jsonl.

from fractions import Fraction
from math import gcd as _gcd
from typing import Optional, Sequence

ALPHA = Fraction(3, 4)


def mms_partition(row: Sequence[Fraction], goods: Sequence[int], n: int) -> tuple[Fraction, list[list[int]]]:
    """Maximin share of an additive valuation over the given goods, for n bundles.

    Returns (MMS, partition), where the partition has n bundles and its
    worst bundle has value MMS. Branch and bound: the goods go out in
    decreasing order of value, bundles with equal loads count once, and a
    branch stops when the water level of the remaining value cannot beat
    the best partition found so far. Exponential time in the worst case
    (the problem is NP-hard); fine for m up to about 20 small values.
    """
    items = sorted(goods, key=lambda g: (-row[g], g))
    if n <= 0:
        raise ValueError("n must be positive")
    # Scale to integers, so that the search compares small ints.
    scale = 1
    for g in items:
        scale = scale * Fraction(row[g]).denominator // _gcd(scale, Fraction(row[g]).denominator)
    val = {g: int(Fraction(row[g]) * scale) for g in items}
    suffix = [0] * (len(items) + 1)
    for k in range(len(items) - 1, -1, -1):
        suffix[k] = suffix[k + 1] + val[items[k]]
    upper = suffix[0] // n
    loads = [0] * n
    parts: list[list[int]] = [[] for _ in range(n)]
    best: list = [-1, None]

    def water(rem: int) -> int:
        # The largest integer the smallest load can reach if the rest were divisible.
        low = sorted(loads)
        acc = 0
        for k in range(n):
            acc += low[k]
            level = (acc + rem) // (k + 1)
            if k + 1 == n or level <= low[k + 1]:
                return level
        return (acc + rem) // n

    def dfs(k: int) -> None:
        if best[0] == upper:
            return
        if k == len(items):
            low = min(loads)
            if low > best[0]:
                best[0] = low
                best[1] = [list(b) for b in parts]
            return
        if water(suffix[k]) <= best[0]:
            return
        g = items[k]
        tried = set()
        for b in sorted(range(n), key=lambda b: (loads[b], b)):
            if loads[b] in tried:
                continue
            tried.add(loads[b])
            loads[b] += val[g]
            parts[b].append(g)
            dfs(k + 1)
            parts[b].pop()
            loads[b] -= val[g]

    dfs(0)
    return Fraction(best[0], scale), best[1]


def pick_back(owner_of_position: Sequence[int], goods: Sequence[int], vals: dict) -> dict:
    """Undo an ordering: position q is the q-th largest value of every agent.

    Positions are handled in increasing order; the owner of position q
    picks its most valuable good among those not taken yet (ties to the
    smallest good). vals[i][g] is the value of agent i for good g. Returns
    a dict from agents to lists of goods.
    """
    free = sorted(goods)
    out: dict = {}
    for i in owner_of_position:
        g = max(free, key=lambda g: (vals[i][g], -g))
        free.remove(g)
        out.setdefault(i, []).append(g)
    return out


def approx_mms(values: Sequence[Sequence], stats: Optional[dict] = None) -> list[list[int]]:
    """A 3/4-MMS allocation: the Garg-Taki algorithm in the form of Akrami, Garg, Sharma and Taki.

    values[i][g] is the nonnegative additive value of agent i for good g.
    Returns bundles A with v_i(A_i) >= (3/4) MMS_i for every agent i. If
    stats is a dict, it gets the rules applied ("rules", a list of pairs
    (agent, rule number)) and the agents left for bag filling ("bagfill").

    Cost: the reductions and bag filling take O(n m log m + n^2 (n + m))
    steps, plus O(n^2) exact MMS computations, which take exponential time
    in the worst case. Garg and Taki also give a strongly polynomial
    version that does not need exact MMS values; this file does not.
    """
    v = [[Fraction(x) for x in row] for row in values]
    n = len(v)
    if n == 0:
        raise ValueError("at least one agent is needed")
    m = len(v[0])
    if any(len(row) != m for row in v) or any(x < 0 for row in v for x in row):
        raise ValueError("every agent needs a nonnegative value for every good")
    w = [sorted(row, reverse=True) for row in v]  # @line L1
    agents = list(range(n))
    ranks = list(range(m))
    owner_of_rank = [-1] * m
    rules: list[tuple[int, int]] = []
    while agents and ranks:  # @line L2
        k = len(agents)
        mms = {i: mms_partition(w[i], ranks, k)[0] for i in agents}  # @line L3
        size = len(ranks)
        sets = [
            [ranks[0]],
            ranks[k - 1:k + 1] if size >= k + 1 else [],
            ranks[2 * k - 2:2 * k + 1] if size >= 2 * k + 1 else [],
            [ranks[0], ranks[2 * k]] if size >= 2 * k + 1 else [],
        ]
        found = None
        for rule, s in enumerate(sets):  # @line L4
            if not s:
                continue
            for i in agents:
                if sum(w[i][r] for r in s) >= ALPHA * mms[i]:
                    found = (i, rule)
                    break
            if found:
                break
        if found is None:  # @line L6
            break
        i, rule = found
        for r in sets[rule]:  # @line L5
            owner_of_rank[r] = i
        agents.remove(i)
        ranks = [r for r in ranks if r not in sets[rule]]
        rules.append((i, rule + 1))
    if stats is not None:
        stats["rules"] = rules
        stats["bagfill"] = list(agents) if ranks else []
    if agents and ranks:
        k = len(agents)
        u = {}
        for i in agents:  # @line L7
            _, part = mms_partition(w[i], ranks, k)
            u[i] = {}
            for bundle in part:
                total = sum(w[i][r] for r in bundle)
                for r in bundle:
                    u[i][r] = w[i][r] / total
        order = {i: sorted((u[i][r] for r in ranks), reverse=True) for i in agents}  # @line L8
        size = len(ranks)
        if size < 2 * k:
            raise AssertionError("an R1-irreducible instance has at least 2n goods")
        bags = [[t, 2 * k - 1 - t] for t in range(k)]  # @line L9
        free_goods = list(range(2 * k, size))
        free_bags = list(range(k))
        waiting = list(agents)
        bag_of: dict = {}
        while waiting:  # @line L10
            hit = None
            for i in waiting:
                for b in free_bags:
                    if sum(order[i][q] for q in bags[b]) >= ALPHA:
                        hit = (i, b)
                        break
                if hit:
                    break
            if hit:  # @line L11
                bag_of[hit[0]] = hit[1]
                waiting.remove(hit[0])
                free_bags.remove(hit[1])
            elif free_goods:  # @line L12
                bags[free_bags[0]].append(free_goods.pop(0))
            else:
                raise AssertionError("bag filling ran out of goods")
        owner_of_position = [-1] * size
        for i, b in bag_of.items():  # @line L13
            for q in bags[b]:
                owner_of_position[q] = i
        for q in free_goods:
            owner_of_position[q] = agents[0]
        got = pick_back(owner_of_position, ranks, u)
        for i, rs in got.items():
            for r in rs:
                owner_of_rank[r] = i
    for r in range(m):
        if owner_of_rank[r] < 0:
            owner_of_rank[r] = 0
    final = pick_back(owner_of_rank, range(m), {i: v[i] for i in range(n)})
    return [sorted(final.get(i, [])) for i in range(n)]  # @line L14
