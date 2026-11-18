# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bucket-algorithm/. The authors are listed in prov/GBX8BH.jsonl.

"""The bucket algorithm for conjunctive queries and conjunctive views.

An atom is a pair (predicate, tuple of variables). A conjunctive query is a
pair (head, body): head is a tuple of variables and body is a list of atoms.
All terms are variables: there are no constants and no comparisons. A view is
a conjunctive query whose head has distinct variables, and views is a dict
from view name to view. A rewriting is a conjunctive query whose predicates
are view names. Set semantics holds throughout.
"""

import itertools


def variables(atoms):
    """The variables of a list of atoms, in order of first occurrence."""
    seen = {}
    for _, args in atoms:
        for a in args:
            seen.setdefault(a, None)
    return list(seen)


def _matches(atoms, index, binding):
    """Yield each extension of binding that maps every atom to a tuple of index."""
    if not atoms:
        yield binding
        return
    pred, args = atoms[0]
    for tup in index.get(pred, ()):
        if len(tup) != len(args):
            continue
        new = dict(binding)
        ok = True
        for a, v in zip(args, tup):
            if new.setdefault(a, v) != v:
                ok = False
                break
        if ok:
            yield from _matches(atoms[1:], index, new)


def evaluate(query, instance):
    """The answers of a conjunctive query on an instance {predicate: set of tuples}."""
    head, body = query
    return {tuple(m[x] for x in head) for m in _matches(list(body), instance, {})}


def contained(q1, q2):
    """True if q1 is contained in q2: a containment mapping sends q2 onto the frozen q1."""
    (head1, body1), (head2, body2) = q1, q2
    if len(head1) != len(head2):
        return False
    start = {}
    for a, b in zip(head2, head1):
        if start.setdefault(a, b) != b:
            return False
    index = {}
    for pred, args in body1:
        index.setdefault(pred, set()).add(tuple(args))
    return next(_matches(list(body2), index, start), None) is not None


def expand(rewriting, views):
    """Replace each view atom by the body of its view, with fresh existential variables.

    The fresh variable for the existential u of the k-th atom is "u#k". Query
    and rewriting variables must not contain "#".
    """
    head, body = rewriting
    out = []
    for k, (name, args) in enumerate(body):
        vhead, vbody = views[name]
        ren = dict(zip(vhead, args))
        for pred, us in vbody:
            out.append((pred, tuple(ren.setdefault(u, "%s#%d" % (u, k)) for u in us)))
    return (tuple(head), out)


class _Classes:
    """A small union-find over hashable items."""

    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

    def groups(self):
        out = {}
        for x in list(self.parent):
            out.setdefault(self.find(x), []).append(x)
        return out


def build_buckets(query, views):
    """Step 1: for each subgoal of the query, the view atoms that can cover it."""
    qhead, qbody = query
    dist = set(qhead)
    order = {x: k for k, x in enumerate(list(qhead) + variables(qbody))}
    fresh = itertools.count(1)
    buckets = []
    for pred, args in qbody:  # @line L1
        bucket = []  # @line L2
        for name in sorted(views):  # @line L3
            vhead, vbody = views[name]
            for vpred, vargs in vbody:
                if vpred != pred or len(vargs) != len(args):
                    continue
                uf = _Classes()
                for x, a in zip(args, vargs):
                    uf.union(("q", x), ("v", a))
                cls = uf.groups()
                heads = {("v", y) for y in vhead}
                if any(not any(m in heads for m in cls[uf.find(("q", x))]) for x in args if x in dist):  # @line L4
                    continue
                entry = []
                for y in vhead:
                    qs = [m[1] for m in cls.get(uf.find(("v", y)), []) if m[0] == "q"]
                    if qs:
                        entry.append(min(qs, key=lambda x: (x not in dist, order[x])))
                    else:
                        entry.append("_%d" % next(fresh))
                bucket.append((name, tuple(entry)))  # @line L5
        buckets.append(bucket)
    return buckets


def equatings(query, rewriting, views):
    """Each most general way to equate variables of rewriting so that its expansion
    is contained in query. Yields a dict from rewriting variables to variables.

    The search picks, for each subgoal of the query, an atom of the expansion
    with the same predicate, and unifies the two. An existential variable of the
    expansion may be unified only with query variables.
    """
    qhead, qbody = query
    rhead, rbody = rewriting
    ehead, ebody = expand(rewriting, views)
    rvars = list(rhead) + [v for v in variables(rbody) if v not in rhead]
    rset = set(rvars)
    pos = {v: k for k, v in enumerate(rvars)}

    def valid(uf):
        for members in uf.groups().values():
            es = [m[1] for m in members if m[0] == "e"]
            if len(es) > 1 and any(t not in rset for t in es):
                return False
        return True

    def rec(i, uf):
        if i == len(qbody):
            theta = {}
            for members in uf.groups().values():
                es = sorted((m[1] for m in members if m[0] == "e" and m[1] in rset), key=pos.get)
                for t in es:
                    theta[t] = es[0]
            yield theta
            return
        pred, args = qbody[i]
        for epred, eargs in ebody:
            if epred != pred or len(eargs) != len(args):
                continue
            new = _Classes()
            new.parent = dict(uf.parent)
            for x, t in zip(args, eargs):
                new.union(("q", x), ("e", t))
            if valid(new):
                yield from rec(i + 1, new)

    start = _Classes()
    for x, y in zip(qhead, rhead):
        start.union(("q", x), ("e", y))
    if valid(start):
        yield from rec(0, start)


def _apply(theta, rewriting):
    head, body = rewriting
    new_body = []
    for name, args in body:
        atom = (name, tuple(theta.get(a, a) for a in args))
        if atom not in new_body:
            new_body.append(atom)
    return (tuple(theta.get(x, x) for x in head), new_body)


def minimize(query):
    """Drop atoms of a conjunctive query while the result stays equivalent to it."""
    head, body = query
    body = list(body)
    i = 0
    while i < len(body):
        rest = body[:i] + body[i + 1:]
        if set(head) <= set(variables(rest)) and contained((head, rest), (head, body)):
            body = rest
        else:
            i += 1
    return (head, body)


def bucket_algorithm(query, views):
    """A union of conjunctive rewritings that is the maximally contained rewriting of query."""
    qhead, qbody = query
    buckets = build_buckets(query, views)
    found = []  # @line L6
    for combo in itertools.product(*buckets):  # @line L7
        candidate = (tuple(qhead), list(combo))  # @line L8
        for theta in equatings(query, candidate, views):  # @line L9
            r = minimize(_apply(theta, candidate))
            if r not in found:
                found.append(r)  # @line L10
    kept = []
    for r in found:  # @line L11
        if any(contained(r, k) for k in kept):
            continue
        kept = [k for k in kept if not contained(k, r)] + [r]
    return kept


def answer(rewritings, view_instance):
    """The answers of a union of rewritings on an instance of the views."""
    out = set()
    for r in rewritings:
        out |= evaluate(r, view_instance)
    return out
