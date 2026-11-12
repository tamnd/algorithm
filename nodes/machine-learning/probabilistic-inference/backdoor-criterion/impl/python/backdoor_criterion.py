# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backdoor-criterion/. The authors are listed in prov/7C4MVG.jsonl.

"""The back-door criterion and the adjustment formula, with the front-door
criterion for contrast.

A causal graph is a DAG on nodes 0 .. n-1 given as a list of edges (a, b)
for a -> b. Hidden variables are ordinary nodes that the caller does not
observe. A joint distribution is a dict from value tuples (one entry per
observed variable, indexed like the nodes) to Fractions.
"""

import itertools
from collections import deque
from fractions import Fraction


def _adj(n, edges):
    pa = [set() for _ in range(n)]
    ch = [set() for _ in range(n)]
    for a, b in edges:
        pa[b].add(a)
        ch[a].add(b)
    return pa, ch


def _closure(start, nxt):
    seen, stack = set(start), list(start)
    while stack:
        for w in nxt[stack.pop()]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def ancestors(n, edges, s):
    return _closure(s, _adj(n, edges)[0])


def descendants(n, edges, s):
    return _closure(s, _adj(n, edges)[1])


def d_separated(n, edges, xs, ys, zs) -> bool:
    """X and Y are d-separated by Z, by the reachability search of Koller and Friedman (Algorithm 3.1)."""
    pa, ch = _adj(n, edges)
    zs = set(zs)
    anc = ancestors(n, edges, zs)
    up, down = 0, 1                       # arrived from a child, arrived from a parent
    seen = set()
    queue = deque((x, up) for x in xs)
    while queue:
        v, d = queue.popleft()
        if (v, d) in seen:
            continue
        seen.add((v, d))
        if v not in zs and v in ys:
            return False
        if d == up and v not in zs:
            queue.extend((p, up) for p in pa[v])
            queue.extend((c, down) for c in ch[v])
        elif d == down:
            if v not in zs:
                queue.extend((c, down) for c in ch[v])
            if v in anc:                  # a collider that is in Z or has a descendant in Z
                queue.extend((p, up) for p in pa[v])
    return True


def is_backdoor_set(n, edges, xs, ys, zs) -> bool:
    """Z has no descendant of X, and Z d-separates X from Y once the edges out of X are removed."""
    xs, zs = set(xs), set(zs)
    if zs & descendants(n, edges, xs):
        return False
    cut = [(a, b) for a, b in edges if a not in xs]
    return d_separated(n, cut, xs, ys, zs)


def backdoor_paths_blocked(n, edges, x, y, zs) -> bool:
    """Pearl's path form for one cause x and one effect y: every path from x to y
    that starts with an edge into x has a non-collider in Z, or a collider
    that is not in Z and has no descendant in Z."""
    pa, ch = _adj(n, edges)
    zs = set(zs)
    anc = ancestors(n, edges, zs)
    nbr = [pa[v] | ch[v] for v in range(n)]
    stack = [[x, p] for p in pa[x]]
    while stack:
        path = stack.pop()
        v = path[-1]
        if v == y:
            open_ = True
            for i in range(1, len(path) - 1):
                a, b, c = path[i - 1], path[i], path[i + 1]
                collider = a in pa[b] and c in pa[b]
                if (collider and b not in anc) or (not collider and b in zs):
                    open_ = False
                    break
            if open_:
                return False
            continue
        for w in nbr[v]:
            if w not in path:
                stack.append(path + [w])
    return True


def prob(pj, event: dict[int, int], given: dict[int, int] | None = None) -> Fraction:
    given = given or {}
    both = {**given, **event}
    num = sum((p for v, p in pj.items() if all(v[i] == a for i, a in both.items())), Fraction(0))
    den = sum((p for v, p in pj.items() if all(v[i] == a for i, a in given.items())), Fraction(0))
    return num / den


def _values(pj, s):
    return sorted({tuple(v[i] for i in s) for v in pj})


def adjustment(pj, x: dict[int, int], y: dict[int, int], zs) -> Fraction:
    """The back-door adjustment formula: sum over z of P(y | x, z) P(z)."""
    zs = sorted(zs)
    total = Fraction(0)
    for zv in _values(pj, zs):
        z = dict(zip(zs, zv))
        pz = prob(pj, z)
        if pz:
            total += prob(pj, y, {**x, **z}) * pz
    return total


def is_frontdoor_set(n, edges, x: int, y: int, ms) -> bool:
    """M meets every directed path from x to y, x has no open back-door path
    to M, and x blocks every back-door path from M to y."""
    ms = set(ms)
    _, ch = _adj(n, edges)
    keep = [set(c) - ms for c in ch]
    if x in ms or y in _closure([x], keep):
        return False
    if not d_separated(n, [(a, b) for a, b in edges if a != x], {x}, ms, set()):
        return False
    return d_separated(n, [(a, b) for a, b in edges if a not in ms], ms, {y}, {x})


def front_door(pj, x: int, xv: int, ms, y: int, yv: int) -> Fraction:
    """The front-door formula: sum over m of P(m | x) sum over x' of P(y | x', m) P(x')."""
    ms = sorted(ms)
    total = Fraction(0)
    for mv in _values(pj, ms):
        m = dict(zip(ms, mv))
        inner = sum(prob(pj, {y: yv}, {x: x2, **m}) * prob(pj, {x: x2}) for (x2,) in _values(pj, [x]))
        total += prob(pj, m, {x: xv}) * inner
    return total


def all_backdoor_sets(n, edges, x, y, candidates):
    """Every subset of the candidates that satisfies the back-door criterion."""
    out = []
    for k in range(len(candidates) + 1):
        for zs in itertools.combinations(candidates, k):
            if is_backdoor_set(n, edges, {x}, {y}, set(zs)):
                out.append(set(zs))
    return out
