# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conjunctive-query-minimization/. The authors are listed in prov/PG64E9.jsonl.
"""Minimization of conjunctive queries under set semantics (Chandra and Merlin 1977).

A term is a variable (a str) or a constant (an int). An atom is (relation name, tuple of
terms). A conjunctive query is (head, body): head is a tuple of terms and body is a list of
atoms, and every variable of the head occurs in the body. The query Q(x) :- R(x, y), S(y, 3)
is (("x",), [("R", ("x", "y")), ("S", ("y", 3))]).
"""


def is_var(t) -> bool:
    return isinstance(t, str)


def variables(atoms) -> list:
    out = []
    for _, terms in atoms:
        for t in terms:
            if is_var(t) and t not in out:
                out.append(t)
    return out


def _extend(h: dict, terms, target_terms):
    """Extend the map h so that it sends terms to target_terms, or return None."""
    if len(terms) != len(target_terms):
        return None
    g = dict(h)
    for s, t in zip(terms, target_terms):
        if is_var(s):
            if s in g and g[s] != t:
                return None
            g[s] = t
        elif s != t:
            return None
    return g


def homomorphism(source, target):
    """Find a homomorphism from the query source to the query target.

    It is a map h from the variables of source to the terms of target, the identity on
    constants, with h(head of source) = head of target and h(atom) in the body of target for
    each atom of the body of source. Return the map as a dict, or None. Backtracking search,
    one source atom at a time."""
    head_s, body_s = source
    head_t, body_t = target
    start = _extend({}, head_s, head_t)                             # @line L6
    if start is None:
        return None
    by_name = {}
    for name, terms in body_t:
        by_name.setdefault(name, []).append(terms)
    order = sorted(range(len(body_s)), key=lambda i: len(by_name.get(body_s[i][0], ())))

    def search(k: int, h: dict):
        if k == len(order):                                          # @line L7
            return h
        name, terms = body_s[order[k]]
        for target_terms in by_name.get(name, ()):                   # @line L8
            g = _extend(h, terms, target_terms)                      # @line L9
            if g is not None:
                found = search(k + 1, g)                             # @line L10
                if found is not None:
                    return found
        return None                                                  # @line L11

    return search(0, start)


def is_contained(q1, q2) -> bool:
    """Q1 is contained in Q2 under set semantics iff there is a homomorphism from Q2 to Q1."""
    return homomorphism(q2, q1) is not None


def is_equivalent(q1, q2) -> bool:
    return is_contained(q1, q2) and is_contained(q2, q1)


def minimize(query, trace=None):
    """Return a minimal conjunctive query equivalent to query whose body is a subset of the
    body of query. The atoms are tried once each, in the order of the body. If trace is a list,
    append (atom, removed) for each atom tried."""
    head, body = query
    keep = list(body)                                                # @line L1
    for atom in body:                                                # @line L2
        rest = list(keep)
        rest.remove(atom)
        removed = homomorphism((head, keep), (head, rest)) is not None  # @line L3
        if removed:
            keep = rest                                              # @line L4
        if trace is not None:
            trace.append((atom, removed))
    return head, keep                                                # @line L5


def evaluate(query, db) -> set:
    """Evaluate a conjunctive query on a database under set semantics.

    db maps a relation name to a set of tuples of constants. Backtracking over the atoms."""
    head, body = query

    def search(k: int, h: dict, out: set) -> None:
        if k == len(body):
            out.add(tuple(h[t] if is_var(t) else t for t in head))
            return
        name, terms = body[k]
        for row in db.get(name, ()):
            g = _extend(h, terms, row)
            if g is not None:
                search(k + 1, g, out)

    out = set()
    search(0, {}, out)
    return out
