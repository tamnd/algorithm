# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minicon-algorithm/. The authors are listed in prov/Y3KK7E.jsonl.

"""The MiniCon algorithm for conjunctive queries and conjunctive views.

An atom is a pair (predicate, tuple of variables). A conjunctive query is a
pair (head, body): head is a tuple of variables and body is a list of atoms.
All terms are variables: there are no constants and no comparisons. A view is
a conjunctive query whose head has distinct variables, and views is a dict
from view name to view. A rewriting is a conjunctive query whose predicates
are view names. Set semantics holds throughout.
"""


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
    """Replace each view atom by the body of its view, with fresh existential variables."""
    head, body = rewriting
    out = []
    for k, (name, args) in enumerate(body):
        vhead, vbody = views[name]
        ren = dict(zip(vhead, args))
        for pred, us in vbody:
            out.append((pred, tuple(ren.setdefault(u, "%s#%d" % (u, k)) for u in us)))
    return (tuple(head), out)


def _unify(phi, hmap, g_args, v_args, vhead):
    """Extend (phi, hmap) so that phi(g) = hmap(v), in the least restrictive way, or None.

    phi maps query variables to view variables. hmap maps each head variable of
    the view to its representative: it is the head homomorphism. vhead maps each
    head variable to its position, and the representative of a class is the
    head variable with the lowest position. An existential view variable may
    not be equated with any other view variable.
    """
    phi, hmap = dict(phi), dict(hmap)
    for x, a in zip(g_args, v_args):
        a = hmap.get(a, a)
        b = phi.get(x)
        if b is None:
            phi[x] = a
        elif b != a:
            if b not in vhead or a not in vhead:
                return None
            if vhead[a] < vhead[b]:
                a, b = b, a
            for y in hmap:
                if hmap[y] == a:
                    hmap[y] = b
            for y in phi:
                if phi[y] == a:
                    phi[y] = b
    return phi, hmap


def _close(query, view, phi, hmap, cover):
    """Yield each (phi, hmap, cover) that extends the input and satisfies Property 1."""
    qhead, qbody = query
    vhead, vbody = view
    vheadset = {y: k for k, y in enumerate(vhead)}
    if any(x in phi and phi[x] not in vheadset for x in qhead):  # @line L12
        return
    for j, (pred, args) in enumerate(qbody):  # @line L13
        if j not in cover and any(x in phi and phi[x] not in vheadset for x in args):
            break
    else:
        yield phi, hmap, cover
        return
    for vpred, vargs in vbody:  # @line L14
        if vpred == pred and len(vargs) == len(args):
            ext = _unify(phi, hmap, args, vargs, vheadset)  # @line L15
            if ext is not None:
                yield from _close(query, view, ext[0], ext[1], cover | {j})  # @line L16


def form_mcds(query, views):
    """The MiniCon descriptions: tuples (view name, hmap, phi, frozenset of subgoal indexes)."""
    qhead, qbody = query
    mcds = {}  # @line L1
    for i, (pred, args) in enumerate(qbody):  # @line L2
        for name in sorted(views):
            vhead, vbody = views[name]
            for vpred, vargs in vbody:
                if vpred != pred or len(vargs) != len(args):
                    continue
                start = _unify({}, {y: y for y in vhead}, args, vargs, {y: k for k, y in enumerate(vhead)})  # @line L3
                if start is None:
                    continue
                for phi, hmap, cover in _close(query, views[name], start[0], start[1], frozenset([i])):  # @line L4
                    key = (name, tuple(sorted(hmap.items())), tuple(sorted(phi.items())), cover)
                    mcds[key] = (name, hmap, phi, cover)  # @line L5
    return [mcds[k] for k in sorted(mcds, key=repr)]


def _partitions(n, mcds):
    """Each list of MCDs whose subgoal sets are disjoint and cover 0..n-1 (Property 2)."""

    def rec(covered, chosen):
        if len(covered) == n:
            yield list(chosen)
            return
        first = min(set(range(n)) - covered)
        for m in mcds:
            if first in m[3] and not (m[3] & covered):
                chosen.append(m)
                yield from rec(covered | m[3], chosen)
                chosen.pop()

    yield from rec(frozenset(), [])


def combine_mcds(query, views, mcds):
    """The conjunctive rewritings, one for each set of MCDs that partitions the subgoals."""
    qhead, qbody = query
    order = {x: k for k, x in enumerate(list(qhead) + variables(qbody))}
    result = []  # @line L6
    for combo in _partitions(len(qbody), mcds):  # @line L7
        parent = {x: x for x in order}

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x

        for _, _, phi, _ in combo:  # @line L8
            first = {}
            for x in sorted(phi, key=order.get):
                y = phi[x]
                if y in first:
                    rx, ry = find(x), find(first[y])
                    if rx != ry:
                        lo, hi = sorted((rx, ry), key=order.get)
                        parent[hi] = lo
                else:
                    first[y] = x
        fresh = 0
        body = []
        for name, hmap, phi, _ in combo:
            inv = {}
            for x in sorted(phi, key=order.get):
                inv.setdefault(phi[x], x)
            args = []
            for y in views[name][0]:
                y = hmap[y]
                if y not in inv:  # @line L9
                    fresh += 1
                    inv[y] = "_%d" % fresh
                    args.append(inv[y])
                else:
                    args.append(find(inv[y]) if inv[y] in parent else inv[y])
            body.append((name, tuple(args)))
        rewriting = (tuple(find(x) for x in qhead), body)
        if rewriting not in result:
            result.append(rewriting)  # @line L10
    return result


def minicon(query, views):
    """A union of conjunctive rewritings that is the maximally contained rewriting of query."""
    mcds = form_mcds(query, views)
    return combine_mcds(query, views, mcds)  # @line L11


def answer(rewritings, view_instance):
    """The answers of a union of rewritings on an instance of the views."""
    out = set()
    for r in rewritings:
        out |= evaluate(r, view_instance)
    return out
