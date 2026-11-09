# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nelson-oppen/. The authors are listed in prov/P1JJQX.jsonl.
"""The Nelson-Oppen combination method, with two theory solvers.

Terms are variable names (str), integer constants (int), or applications
("f", t1, ..., tk) of uninterpreted function symbols. Literals are tuples
(op, s, t) with op one of "=", "!=", "<=", "<".

The solvers:
- euf_sat: equality with uninterpreted functions, by congruence closure.
- order_sat: the order of the integers (integer=True) or of the rationals
  (integer=False), with <=, <, =, != and integer constants. Over the integers
  it is not convex: 1 <= x <= 2 entails x = 1 or x = 2.
- at_most_two_sat: pure equality in a domain of at most two elements. It is
  not stably infinite.
"""

from itertools import product


# ---------- theory solvers ----------

def _subterms(t, out):
    if isinstance(t, tuple):
        for a in t[1:]:
            _subterms(a, out)
    out.add(t)


def euf_sat(lits):
    """Satisfiability of a conjunction of EUF literals ("=" and "!=")."""
    terms = set()
    for _, s, t in lits:
        _subterms(s, terms)
        _subterms(t, terms)
    parent = {t: t for t in terms}

    def find(t):
        while parent[t] != t:
            t = parent[t]
        return t

    for op, s, t in lits:
        if op == "=":
            parent[find(s)] = find(t)
    apps = [t for t in terms if isinstance(t, tuple)]
    changed = True
    while changed:  # congruence: equal arguments give equal values
        changed = False
        for p in apps:
            for q in apps:
                if p[0] == q[0] and len(p) == len(q) and find(p) != find(q):
                    if all(find(a) == find(b) for a, b in zip(p[1:], q[1:])):
                        parent[find(p)] = find(q)
                        changed = True
    return all(find(s) != find(t) for op, s, t in lits if op == "!=")


def order_sat(lits, integer=True):
    """Satisfiability of order literals over the integers or the rationals.

    Each literal becomes difference constraints u - v <= c, or u - v < c,
    where the node "0" stands for the number zero. A bound is a pair (c, e)
    meaning c + e * epsilon, with e = 0 for <= and e = -1 for <. The
    constraints are satisfiable iff the graph has no negative cycle. Over the
    integers u - v < c is u - v <= c - 1. A disequality is split into < and >.
    """
    def node(t):
        return ("0", t) if isinstance(t, int) else (t, 0)

    base, diseq = [], []
    for op, s, t in lits:
        (u, a), (v, b) = node(s), node(t)  # s = u + a, t = v + b
        if op == "<=":
            base.append((u, v, b - a, False))
        elif op == "<":
            base.append((u, v, b - a, True))
        elif op == "=":
            base.append((u, v, b - a, False))
            base.append((v, u, a - b, False))
        else:
            diseq.append(((u, a), (v, b)))

    def split(cons, k):  # depth-first over the two sides of each disequality
        if not _no_negative_cycle(cons, integer):
            return False
        if k == len(diseq):
            return True
        (u, a), (v, b) = diseq[k]
        return (split(cons + [(u, v, b - a, True)], k + 1)
                or split(cons + [(v, u, a - b, True)], k + 1))

    return split(base, 0)


def _no_negative_cycle(cons, integer):
    nodes = sorted({"0"} | {x for c in cons for x in c[:2]}, key=str)
    inf = None
    dist = {(i, j): ((0, 0) if i == j else inf) for i in nodes for j in nodes}
    for u, v, c, strict in cons:
        w = (c - 1, 0) if (strict and integer) else (c, -1 if strict else 0)
        if dist[(u, v)] is None or w < dist[(u, v)]:
            dist[(u, v)] = w
    for k in nodes:  # Floyd-Warshall on pairs (c, e), ordered lexicographically
        for i in nodes:
            if dist[(i, k)] is None:
                continue
            for j in nodes:
                if dist[(k, j)] is None:
                    continue
                w = (dist[(i, k)][0] + dist[(k, j)][0],
                     dist[(i, k)][1] + dist[(k, j)][1])
                if dist[(i, j)] is None or w < dist[(i, j)]:
                    dist[(i, j)] = w
    return all(dist[(i, i)] >= (0, 0) for i in nodes)


def int_order_sat(lits):
    return order_sat(lits, integer=True)


def rat_order_sat(lits):
    return order_sat(lits, integer=False)


def at_most_two_sat(lits):
    """Pure equality literals in a domain of at most two elements."""
    names = sorted({x for _, s, t in lits for x in (s, t)}, key=str)
    for vals in product((0, 1), repeat=len(names)):
        val = dict(zip(names, vals))
        if all((val[s] == val[t]) == (op == "=") for op, s, t in lits):
            return True
    return False


# ---------- purification ----------

def purify(lits):
    """Split mixed literals into EUF literals and order literals.

    An alien subterm gets a fresh variable and a defining equality on the side
    that owns it. Equalities between two variables go to both sides.
    """
    euf, arith, names = [], [], {}

    def fresh(t):
        if t not in names:
            names[t] = "v%d" % len(names)
        return names[t]

    def for_euf(t):
        if isinstance(t, str):
            return t
        if isinstance(t, int):  # an arithmetic term inside EUF
            if t not in names:
                arith.append(("=", fresh(t), t))
            return names[t]
        return (t[0],) + tuple(for_euf(a) for a in t[1:])

    def for_arith(t):
        if isinstance(t, (str, int)):
            return t
        if t not in names:  # an application inside arithmetic
            euf.append(("=", fresh(t), for_euf(t)))
        return names[t]

    for op, s, t in lits:
        if op in ("<=", "<") or isinstance(s, int) or isinstance(t, int):
            arith.append((op, for_arith(s), for_arith(t)))
        elif isinstance(s, str) and isinstance(t, str):
            euf.append((op, s, t))
            arith.append((op, s, t))
        else:
            euf.append((op, for_euf(s), for_euf(t)))
    return euf, arith


def _vars(lits):
    out = set()

    def walk(t):
        if isinstance(t, str):
            out.add(t)
        elif isinstance(t, tuple):
            for a in t[1:]:
                walk(a)

    for _, s, t in lits:
        walk(s)
        walk(t)
    return out


# ---------- the combination ----------

def nelson_oppen(phi1, phi2, sat1, sat2, split=True, stats=None):
    """Decide phi1 and phi2 in the combination of two theories.

    phi1 and phi2 are lists of pure literals of the two theories. With
    split=False the procedure only exchanges single equalities, which is the
    deterministic method for convex theories.
    """
    if stats is None:
        stats = {"calls": 0, "equalities": 0, "splits": 0}
    shared = sorted(_vars(phi1) & _vars(phi2))  # @line L1
    phis, sats = [list(phi1), list(phi2)], [sat1, sat2]

    def sat(i, extra=()):
        stats["calls"] += 1
        return sats[i](phis[i] + list(extra))

    def entails(i, c, d):
        return not sat(i, [("!=", c, d)])

    while True:  # @line L2
        if not sat(0) or not sat(1):  # @line L3
            return False
        new = None
        for i in (0, 1):  # @line L4
            for x in range(len(shared)):
                for y in range(x + 1, len(shared)):
                    c, d = shared[x], shared[y]
                    if new is None and entails(i, c, d) and not entails(1 - i, c, d):
                        new = (1 - i, c, d)
        if new is not None:
            j, c, d = new
            phis[j].append(("=", c, d))  # @line L5
            stats["equalities"] += 1
            continue
        reps = []  # @line L6
        for c in shared:
            if all(not entails(0, c, r) for r in reps):
                reps.append(c)
        cls = {c: next(r for r in reps if c == r or entails(0, c, r)) for c in shared}
        D = [(reps[x], reps[y]) for x in range(len(reps))  # @line L7
             for y in range(x + 1, len(reps))]
        ar = [("=", c, cls[c]) for c in shared if c != cls[c]]
        ar += [("!=", c, d) for c, d in D]
        if split and D and (not sat(0, ar) or not sat(1, ar)):  # @line L8
            stats["splits"] += 1
            for c, d in D:  # @line L9
                e = ("=", c, d)
                if nelson_oppen(phis[0] + [e], phis[1] + [e], sat1, sat2, split, stats):
                    return True
            return False  # @line L10
        return True  # @line L11


def set_partitions(items):
    """All partitions of a list into blocks."""
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in set_partitions(rest):
        yield [[first]] + p
        for k in range(len(p)):
            yield p[:k] + [[first] + p[k]] + p[k + 1:]


def arrangement(blocks):
    lits = []
    for b in blocks:
        lits += [("=", b[0], c) for c in b[1:]]
    for x in range(len(blocks)):
        for y in range(x + 1, len(blocks)):
            lits.append(("!=", blocks[x][0], blocks[y][0]))
    return lits


def nelson_oppen_guess(phi1, phi2, sat1, sat2):
    """The nondeterministic version: try every arrangement of the shared variables."""
    shared = sorted(_vars(phi1) & _vars(phi2))
    for blocks in set_partitions(shared):
        ar = arrangement(blocks)
        if sat1(phi1 + ar) and sat2(phi2 + ar):
            return True
    return False


def euf_order_sat(lits, integer=True, method="split"):
    """End to end: purify, then combine EUF with the order of Z or Q."""
    euf, arith = purify(lits)
    osat = int_order_sat if integer else rat_order_sat
    if method == "guess":
        return nelson_oppen_guess(euf, arith, euf_sat, osat)
    return nelson_oppen(euf, arith, euf_sat, osat, split=(method == "split"))
