# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/data-exchange-core-computation/. The authors are listed in prov/6E0XMM.jsonl.

"""The core of the canonical universal solution, for source-to-target tgds.

A fact is a pair (relation, tuple of values). A value is a constant (a string)
or a labeled null (a Null). A tgd is a pair (body, head) of lists of atoms
(relation, tuple of variable names). The variables of the head that are not in
the body are existential. Set semantics: an instance is a set of facts.
"""


class Null:
    """A labeled null. Two nulls are equal when their numbers are equal."""

    __slots__ = ("id",)

    def __init__(self, i):
        self.id = i

    def __eq__(self, other):
        return isinstance(other, Null) and other.id == self.id

    def __hash__(self):
        return hash(("null", self.id))

    def __repr__(self):
        return "N%d" % self.id


def is_null(v):
    return isinstance(v, Null)


def value_key(v):
    """A total order on values: constants first, then nulls by number."""
    return (1, v.id, "") if is_null(v) else (0, 0, str(v))


def fact_key(f):
    return (f[0], tuple(value_key(v) for v in f[1]))


def _index(inst):
    by_rel = {}
    for rel, tup in sorted(inst, key=fact_key):
        by_rel.setdefault(rel, []).append(tup)
    return by_rel


def _matches(atoms, by_rel, binding, is_var):
    """Yield each extension of binding that maps every atom to a fact of the index.

    is_var(t) says which terms are variables. Any other term must map to itself.
    """
    if not atoms:
        yield binding
        return
    rel, terms = atoms[0]
    for tup in by_rel.get(rel, ()):
        if len(tup) != len(terms):
            continue
        new = dict(binding)
        ok = True
        for t, v in zip(terms, tup):
            if is_var(t):
                if new.setdefault(t, v) != v:
                    ok = False
                    break
            elif t != v:
                ok = False
                break
        if ok:
            yield from _matches(atoms[1:], by_rel, new, is_var)


def chase(source, tgds, first_null=1):
    """The canonical universal solution: each trigger fires once, with fresh nulls."""
    by_rel = _index(source)
    out = set()  # @line L8
    nxt = first_null
    for body, head in tgds:  # @line L9
        body_vars = {t for _, ts in body for t in ts}
        exist = sorted({t for _, ts in head for t in ts} - body_vars)
        seen = set()
        for m in _matches(list(body), by_rel, {}, lambda t: True):
            key = tuple(sorted(m.items()))
            if key in seen:
                continue
            seen.add(key)
            m = dict(m)
            for y in exist:
                m[y] = Null(nxt)
                nxt += 1
            for rel, ts in head:  # @line L10
                out.add((rel, tuple(m[t] for t in ts)))
    return out  # @line L11


def null_blocks(inst):
    """The blocks: the connected parts of the graph on the nulls in which two
    nulls are joined when they occur in the same fact. Sorted lists of nulls."""
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for _, tup in inst:
        ns = [v for v in tup if is_null(v)]
        for n in ns:
            parent.setdefault(n, n)
        for n in ns[1:]:
            ra, rb = find(ns[0]), find(n)
            if ra != rb:
                parent[rb] = ra
    groups = {}
    for n in parent:
        groups.setdefault(find(n), []).append(n)
    blocks = [sorted(g, key=value_key) for g in groups.values()]
    return sorted(blocks, key=lambda b: value_key(b[0]))


def apply(h, fact):
    rel, tup = fact
    return (rel, tuple(h.get(v, v) for v in tup))


def find_witness(part, inst):
    """A map h on the nulls of part with h(part) a subset of inst and h(part) != part, or None."""
    atoms = sorted(part, key=fact_key)
    for h in _matches(atoms, _index(inst), {}, is_null):
        if {apply(h, f) for f in part} != part:
            return h
    return None


def core(inst):
    """The core of an instance whose blocks are small, by retracting one block at a time."""
    inst = set(inst)
    for block in null_blocks(inst):  # @line L2
        nulls = set(block)
        part = {f for f in inst if any(v in nulls for v in f[1])}  # @line L3
        while True:
            h = find_witness(part, inst)  # @line L4
            if h is None:
                break
            image = {apply(h, f) for f in part}
            inst -= part - image  # @line L5
            part &= inst  # @line L6
    return inst  # @line L7


def core_solution(source, tgds):
    """The core of the universal solutions for source and the s-t tgds."""
    return core(chase(source, tgds))  # @line L1
