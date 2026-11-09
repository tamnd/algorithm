# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/e-matching/. The authors are listed in prov/5EARHB.jsonl.
"""E-matching over a small e-graph, and a simple instantiation loop.

Terms:
    "a"                 a constant (an application with no arguments)
    ("f", t1, ..., tn)  an application
Patterns are terms that may also contain variables, strings that start
with "?", such as "?x".
"""


def is_var(p):
    return isinstance(p, str) and p.startswith("?")


def head_args(t):
    return (t, ()) if isinstance(t, str) else (t[0], t[1:])


class EGraph:
    """Hash-consed terms in classes, kept closed under congruence."""

    def __init__(self):
        self.parent = []
        self.nodes = []  # id -> (f, child ids as created)
        self.memo = {}  # (f, child roots) -> id
        self.term = []  # id -> a ground term of the class

    def find(self, a):
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def add(self, t):
        f, args = head_args(t)
        key = (f, tuple(self.find(self.add(a)) for a in args))
        if key in self.memo:
            return self.find(self.memo[key])
        i = len(self.nodes)
        self.parent.append(i)
        self.nodes.append(key)
        self.term.append(t)
        self.memo[key] = i
        return i

    def merge(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.parent[a] = b
            self.rebuild()

    def rebuild(self):
        """Restore congruence: equal canonical nodes must be in one class."""
        changed = True
        while changed:
            changed = False
            memo = {}
            for i, (f, args) in enumerate(self.nodes):
                key = (f, tuple(self.find(c) for c in args))
                j = memo.setdefault(key, i)
                if self.find(i) != self.find(j):
                    self.parent[self.find(i)] = self.find(j)
                    changed = True
            self.memo = memo

    def classes(self):
        return sorted({self.find(i) for i in range(len(self.nodes))})

    def index(self):
        """Map each class to its distinct canonical nodes."""
        idx = {}
        for f, args in self.nodes:
            node = (f, tuple(self.find(c) for c in args))
            root = self.find(self.memo[node])
            if node not in idx.setdefault(root, []):
                idx[root].append(node)
        return idx

    def equal(self, s, t):
        return self.find(self.add(s)) == self.find(self.add(t))


def ematch(g, idx, p, c, sigma):
    """All extensions of sigma (variable -> class) that put p in class c."""
    if is_var(p):  # @line L1
        if p not in sigma:  # @line L2
            return [dict(sigma, **{p: c})]
        return [sigma] if g.find(sigma[p]) == g.find(c) else []  # @line L3
    f, pargs = head_args(p)
    result = []  # @line L4
    for h, cargs in idx.get(g.find(c), []):  # @line L5
        if h != f or len(cargs) != len(pargs):
            continue
        subs = [sigma]  # @line L6
        for pi, ci in zip(pargs, cargs):  # @line L7
            subs = [s2 for s1 in subs for s2 in ematch(g, idx, pi, ci, s1)]
        result.extend(subs)  # @line L8
    return result  # @line L9


def match_all(g, p):
    """All matches of p in g, as dicts, without duplicates."""
    idx = g.index()
    out = []
    for c in g.classes():  # @line L10
        for s in ematch(g, idx, p, c, {}):
            s = {x: g.find(v) for x, v in s.items()}
            if (c, s) not in out:
                out.append((c, s))
    return out


def match_multi(g, patterns):
    """Matches of a multi-pattern: one substitution for all patterns."""
    idx = g.index()
    subs = [{}]
    for p in patterns:
        subs = [s2 for s1 in subs for c in g.classes() for s2 in ematch(g, idx, p, c, s1)]
    out = []
    for s in subs:
        s = {x: g.find(v) for x, v in s.items()}
        if s not in out:
            out.append(s)
    return out


def substitute(g, t, sigma):
    if is_var(t):
        return g.term[g.find(sigma[t])]
    f, args = head_args(t)
    return t if not args else (f,) + tuple(substitute(g, a, sigma) for a in args)


def instantiate(eqs, diseqs, axioms, rounds):
    """Saturate ground literals with instances of universal equations.

    axioms: list of (triggers, lhs, rhs) meaning forall vars. lhs = rhs,
    instantiated for each match of the multi-pattern triggers.
    Return ("unsat", n) when a disequation fails, or ("unknown", n) when a
    round adds no new instance or the rounds run out. n counts the instances.
    """
    g = EGraph()
    for s, t in eqs:
        g.merge(g.add(s), g.add(t))
    for s, t in diseqs:
        g.add(s)
        g.add(t)
    done, count = [], 0  # the instances made, as (axiom, substitution)

    def seen(k, s):  # an instance with the same classes was made before
        return any(j == k and all(g.find(old[x]) == g.find(v) for x, v in s.items())
                   for j, old in done)

    for _ in range(rounds):
        if any(g.equal(s, t) for s, t in diseqs):
            return "unsat", count
        new = []
        for k, (triggers, lhs, rhs) in enumerate(axioms):
            for s in match_multi(g, triggers):
                if not seen(k, s):
                    done.append((k, s))
                    new.append((substitute(g, lhs, s), substitute(g, rhs, s)))
        if not new:
            return "unknown", count
        for s, t in new:
            g.merge(g.add(s), g.add(t))
            count += 1
    if any(g.equal(s, t) for s, t in diseqs):
        return "unsat", count
    return "unknown", count
