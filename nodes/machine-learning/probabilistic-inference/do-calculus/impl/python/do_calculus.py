# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/do-calculus/. The authors are listed in prov/XER6WP.jsonl.

"""The three rules of Pearl's do-calculus as graph tests, and an exact
evaluator of interventional distributions to check them against.

A causal graph is a DAG on nodes 0 .. n-1 given as a list of edges (a, b)
for a -> b. Hidden common causes are explicit nodes that the caller does not
observe. All sets are Python sets of nodes.
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


def ancestors(n, edges, s):
    """s together with every node that has a directed path into s."""
    pa, _ = _adj(n, edges)
    seen, stack = set(s), list(s)
    while stack:
        for p in pa[stack.pop()]:
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return seen


def d_separated(n, edges, xs, ys, zs) -> bool:
    """Reachability search of Koller and Friedman (Algorithm 3.1)."""
    pa, ch = _adj(n, edges)
    zs = set(zs)
    anc = ancestors(n, edges, zs)
    seen = set()
    queue = deque((x, "up") for x in xs)
    while queue:
        v, d = queue.popleft()
        if (v, d) in seen:
            continue
        seen.add((v, d))
        if v not in zs and v in ys:
            return False
        if d == "up" and v not in zs:
            queue.extend((p, "up") for p in pa[v])
            queue.extend((c, "down") for c in ch[v])
        elif d == "down":
            if v not in zs:
                queue.extend((c, "down") for c in ch[v])
            if v in anc:
                queue.extend((p, "up") for p in pa[v])
    return True


def mutilate(edges, into=frozenset(), out_of=frozenset()):
    """Delete the edges into the nodes of `into` and the edges out of the nodes of `out_of`."""
    return [(a, b) for a, b in edges if b not in into and a not in out_of]


def rule1(n, edges, ys, xs, zs, ws) -> bool:
    """P(y | do(x), z, w) = P(y | do(x), w) if (Y _||_ Z | X, W) in G with the edges into X cut."""
    return d_separated(n, mutilate(edges, into=xs), ys, zs, xs | ws)


def rule2(n, edges, ys, xs, zs, ws) -> bool:
    """P(y | do(x), do(z), w) = P(y | do(x), z, w) if (Y _||_ Z | X, W) with the edges into X and out of Z cut."""
    return d_separated(n, mutilate(edges, into=xs, out_of=zs), ys, zs, xs | ws)


def rule3(n, edges, ys, xs, zs, ws) -> bool:
    """P(y | do(x), do(z), w) = P(y | do(x), w) if (Y _||_ Z | X, W) with the edges into X and into Z(W) cut,
    where Z(W) is the set of nodes of Z that are not ancestors of W in G with the edges into X cut."""
    gx = mutilate(edges, into=xs)
    zw = zs - ancestors(n, gx, ws)
    return d_separated(n, mutilate(edges, into=xs | zw), ys, zs, xs | ws)


class CausalBN:
    """A causal Bayesian network with binary nodes: cpt[v][parent values] = P(v = 1 | parents)."""

    def __init__(self, n, edges, cpt, hidden=frozenset()):
        self.n, self.cpt, self.hidden = n, cpt, set(hidden)
        self.pa = [sorted(a for a, b in edges if b == v) for v in range(n)]

    def joint(self, do=None):
        """P(v | do(...)) by the truncated factorization, with the hidden nodes summed out (shown as 0)."""
        do = do or {}
        out = {}
        for x in itertools.product((0, 1), repeat=self.n):
            if any(x[v] != val for v, val in do.items()):
                continue
            p = Fraction(1)
            for v in range(self.n):
                if v not in do:
                    q = self.cpt[v][tuple(x[u] for u in self.pa[v])]
                    p *= q if x[v] else 1 - q
            key = tuple(0 if v in self.hidden else x[v] for v in range(self.n))
            out[key] = out.get(key, Fraction(0)) + p
        return out


def prob(pj, event, given=None):
    """P(event | given), or None if the condition has probability zero."""
    given = given or {}
    both = {**given, **event}
    den = sum((p for v, p in pj.items() if all(v[i] == a for i, a in given.items())), Fraction(0))
    if den == 0:
        return None
    return sum((p for v, p in pj.items() if all(v[i] == a for i, a in both.items())), Fraction(0)) / den
