# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phylogenetic-diversity-maximization/. The authors are listed in prov/BFRDCF.jsonl.
"""Maximizing phylogenetic diversity: the greedy algorithm for k taxa on
rooted and unrooted trees, and a tree knapsack DP for taxa with costs.

A rooted tree is a parent list: parent[v] is the parent of node v, with
parent[root] = -1, and length[v] >= 0 is the length of the edge above v.
The taxa are the nodes with no children (the root is never a taxon).
"""

import math


def children_of(parent: list) -> list:
    kids = [[] for _ in parent]
    for v, p in enumerate(parent):
        if p >= 0:
            kids[p].append(v)
    return kids


def taxa(parent: list) -> list:
    kids = children_of(parent)
    return [v for v in range(len(parent)) if parent[v] >= 0 and not kids[v]]


def postorder(parent: list) -> list:
    """The nodes in an order with each child before its parent, without recursion."""
    kids = children_of(parent)
    root = parent.index(-1)
    order, stack = [], [root]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(kids[v])
    order.reverse()
    return order


def pd_rooted(parent: list, length: list, chosen) -> float:
    """Total length of the edges with at least one chosen taxon below them."""
    below = [0] * len(parent)
    for v in chosen:
        below[v] += 1
    total = 0
    for v in postorder(parent):
        if parent[v] >= 0:
            below[parent[v]] += below[v]
            if below[v] > 0:
                total += length[v]
    return total


def pd_unrooted(parent: list, length: list, chosen) -> float:
    """Total length of the edges with chosen taxa on both sides."""
    chosen = list(chosen)
    below = [0] * len(parent)
    for v in chosen:
        below[v] += 1
    total = 0
    for v in postorder(parent):
        if parent[v] >= 0:
            below[parent[v]] += below[v]
            if 0 < below[v] < len(chosen):
                total += length[v]
    return total


def greedy_rooted(parent: list, length: list, k: int) -> list:
    """Greedy PD: k times, add the taxon whose path to the root has the
    longest uncovered part. Returns the taxa in the order chosen; each prefix
    of the list is an optimal set of its size (rooted PD)."""
    return greedy_rooted_from(parent, length, children_of(parent), parent.index(-1), [], k, taxa(parent))


def reroot(parent: list, length: list, new_root: int) -> tuple:
    """The same unrooted tree as a parent list rooted at new_root."""
    adj = [[] for _ in parent]
    for v, p in enumerate(parent):
        if p >= 0:
            adj[v].append((p, length[v]))
            adj[p].append((v, length[v]))
    new_parent, new_length = [-2] * len(parent), [0] * len(parent)
    new_parent[new_root] = -1
    stack = [new_root]
    while stack:
        v = stack.pop()
        for u, w in adj[v]:
            if new_parent[u] == -2:
                new_parent[u], new_length[u] = v, w
                stack.append(u)
    return new_parent, new_length


def _farthest(parent: list, length: list, start: int, among: list) -> int:
    p, l = reroot(parent, length, start)
    dist = [0] * len(p)
    for v in reversed(postorder(p)):
        if p[v] >= 0:
            dist[v] = dist[p[v]] + l[v]
    return max(among, key=lambda x: dist[x])


def greedy_unrooted(parent: list, length: list, k: int) -> list:
    """Steel's greedy algorithm for unrooted PD: start with two taxa at maximum
    distance, then add the taxon farthest from the current subtree."""
    leaves = taxa(parent)
    if k <= 1 or len(leaves) <= 1:
        return leaves[:k]
    a = _farthest(parent, length, leaves[0], leaves)
    b = _farthest(parent, length, a, leaves)
    # With a in the set, unrooted PD is rooted PD for the tree rooted at a.
    p, l = reroot(parent, length, a)
    kids = children_of(p)
    p[a] = -1
    rest = greedy_rooted_from(p, l, kids, a, [b], k - 1, [x for x in leaves if x != a])
    return [a] + rest


def greedy_rooted_from(parent, length, kids, root, start, k, leaves) -> list:
    """Greedy on a rooted tree, with the taxa in start already chosen."""
    covered = [False] * len(parent)  # @line L1: covered[v] means the edge above v is used
    covered[root] = True
    chosen = []
    for best in start:
        chosen.append(best)
        v = best
        while not covered[v]:
            covered[v] = True
            v = parent[v]
    while len(chosen) < min(k, len(leaves)):  # @line L2
        gain = [0] * len(parent)  # @line L3: uncovered length from the root down to v
        stack = [root]
        while stack:
            v = stack.pop()
            for c in kids[v]:
                gain[c] = gain[v] + (0 if covered[c] else length[c])
                stack.append(c)
        best = max((x for x in leaves if x not in chosen), key=lambda x: gain[x])  # @line L4
        chosen.append(best)  # @line L5
        v = best
        while not covered[v]:  # @line L6: mark the new part of the path
            covered[v] = True
            v = parent[v]
    return chosen  # @line L7


def budgeted_pd(parent: list, length: list, cost: dict, budget: int) -> float:
    """The largest rooted PD of a set of taxa with total integer cost at most
    budget, by a knapsack DP over the tree in O(n B^2) time."""
    kids = children_of(parent)
    neg = -math.inf
    any_val, nonempty = {}, {}  # arrays over budgets 0..budget
    for v in postorder(parent):
        if not kids[v]:
            if parent[v] < 0:
                return 0
            ne = [length[v] if b >= cost[v] else neg for b in range(budget + 1)]
        else:
            acc_any = [0] * (budget + 1)  # no child processed yet: the empty set
            acc_ne = [neg] * (budget + 1)
            for c in kids[v]:
                c_any, c_ne = any_val[c], nonempty[c]
                new_any = [neg] * (budget + 1)
                new_ne = [neg] * (budget + 1)
                for b1 in range(budget + 1):
                    for b2 in range(budget + 1 - b1):
                        b = b1 + b2
                        new_any[b] = max(new_any[b], acc_any[b1] + c_any[b2])
                        new_ne[b] = max(new_ne[b], acc_ne[b1] + c_any[b2], acc_any[b1] + c_ne[b2])
                acc_any, acc_ne = new_any, new_ne
            if parent[v] < 0:
                return max(acc_any)
            ne = [x + length[v] if x > neg else neg for x in acc_ne]
        nonempty[v] = ne
        any_val[v] = [max(0, x) for x in ne]
    raise ValueError("no root")
