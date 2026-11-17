# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandra-merlin-theorem/. The authors are listed in prov/ZF3N9M.jsonl.
"""Containment of conjunctive queries by the Chandra-Merlin homomorphism test.

A conjunctive query (CQ) is a pair (head, body). The head is a tuple of terms and the
body is a list of atoms (relation, terms). A term is a variable (a str) or a constant
(an int). Every variable of the head must occur in the body.

A database is a dict from relation names to sets of tuples.
"""


def _is_var(term) -> bool:
    return isinstance(term, str)


def _extend(mapping: dict, src: tuple, dst: tuple):
    """Extend mapping so that it maps the terms src to the terms dst, or return None."""
    if len(src) != len(dst):
        return None
    new = dict(mapping)
    for a, b in zip(src, dst):
        if _is_var(a):
            if new.setdefault(a, b) != b:
                return None
        elif a != b:
            return None
    return new


def find_homomorphism(q_from, q_to):
    """A map h from the variables of q_from to the terms of q_to with h(head) = head and
    h(atom) an atom of q_to for every atom of q_from, or None. Backtracking search."""
    head_from, body_from = q_from
    head_to, body_to = q_to
    start = _extend({}, head_from, head_to)
    if start is None:
        return None
    by_rel = {}
    for rel, terms in body_to:
        by_rel.setdefault(rel, []).append(terms)
    # Atoms with more variables already fixed are tried first.
    atoms = sorted(body_from, key=lambda a: -sum(1 for t in a[1] if not _is_var(t) or t in start))

    def search(i: int, h: dict):
        if i == len(atoms):
            return h
        rel, terms = atoms[i]
        for target in by_rel.get(rel, []):
            h2 = _extend(h, terms, target)
            if h2 is not None:
                found = search(i + 1, h2)
                if found is not None:
                    return found
        return None

    return search(0, start)


def contained(q1, q2) -> bool:
    """Q1 is contained in Q2 iff there is a homomorphism from Q2 to Q1 (Chandra and Merlin)."""
    return find_homomorphism(q2, q1) is not None


def equivalent(q1, q2) -> bool:
    return contained(q1, q2) and contained(q2, q1)


def canonical_db(q) -> dict:
    """The canonical database of q: each body atom becomes a fact, variables become values."""
    db = {}
    for rel, terms in q[1]:
        db.setdefault(rel, set()).add(tuple(terms))
    return db


def evaluate(q, db: dict) -> set:
    """The answer of q on db: all images of the head under valuations that map the body into db."""
    head, body = q
    out = set()

    def search(i: int, h: dict):
        if i == len(body):
            out.add(tuple(h[t] if _is_var(t) else t for t in head))
            return
        rel, terms = body[i]
        for fact in db.get(rel, ()):
            h2 = _extend(h, terms, fact)
            if h2 is not None:
                search(i + 1, h2)

    search(0, {})
    return out


def contained_by_canonical_db(q1, q2) -> bool:
    """The second form of the theorem: the head of Q1 is an answer of Q2 on the canonical database of Q1."""
    return tuple(q1[0]) in evaluate(q2, canonical_db(q1))


def minimize(q):
    """Remove body atoms while the query stays equivalent. The result is the core of q,
    the unique minimal equivalent CQ up to renaming of variables."""
    head, body = q
    body = list(dict.fromkeys(body))
    i = 0
    while i < len(body):
        smaller = body[:i] + body[i + 1:]
        head_vars = {t for t in head if _is_var(t)}
        body_vars = {t for _, terms in smaller for t in terms if _is_var(t)}
        # Q is contained in the smaller query by the identity map; test the other way.
        if head_vars <= body_vars and contained((head, smaller), (head, body)):
            body = smaller
        else:
            i += 1
    return head, body
