# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perfectref-rewriting/. The authors are listed in prov/4TB81W.jsonl.
"""PerfectRef: rewrite a conjunctive query over a DL-Lite_R TBox into a union of conjunctive queries.

Notation.
  A basic concept is ("A", name) for a concept name, or ("E", P, inverse) for some P or some P^-.
  A role is (P, inverse).
  The TBox holds positive inclusions: concept inclusions (B1, B2), read B1 is subsumed by B2,
  and role inclusions (R1, R2). Negative inclusions do not change the rewriting, only consistency.
  A query is (head, body): head is a tuple of variables, body a frozenset of atoms
  ("C", A, t) and ("R", P, t1, t2). Terms are variable names. The term "_" stands for a variable
  that occurs once in the body and not in the head (an unbound variable); each "_" is a new one.
  An ABox is a pair (concept facts {(A, a)}, role facts {(P, a, b)}).
"""

from typing import Iterable, Sequence

UNBOUND = "_"


def basic_atom(b: tuple, t: str) -> tuple:
    """The atom that says term t is in the basic concept b."""
    if b[0] == "A":
        return ("C", b[1], t)
    p, inv = b[1], b[2]
    return ("R", p, UNBOUND, t) if inv else ("R", p, t, UNBOUND)


def role_atom(r: tuple, t1: str, t2: str) -> tuple:
    """The atom that says (t1, t2) is in the role r."""
    p, inv = r
    return ("R", p, t2, t1) if inv else ("R", p, t1, t2)


def tau(head: tuple, body: Iterable[tuple]) -> tuple:
    """Replace every variable that occurs once in the body and not in the head by "_"."""
    body = list(body)
    count: dict[str, int] = {}
    for g in body:
        for t in g[2:]:
            if t != UNBOUND:
                count[t] = count.get(t, 0) + 1
    hs = set(head)

    def f(t: str) -> str:
        return UNBOUND if t != UNBOUND and t not in hs and count[t] == 1 else t

    return (tuple(head), frozenset(g[:2] + tuple(f(t) for t in g[2:]) for g in body))


def rewrite_atom(g: tuple, tbox_ci: Sequence[tuple], tbox_ri: Sequence[tuple]) -> list[tuple]:
    """gr(g, I) for every inclusion I that is applicable to the atom g."""
    out = []
    if g[0] == "C":
        for lhs, rhs in tbox_ci:
            if rhs == ("A", g[1]):
                out.append(basic_atom(lhs, g[2]))
        return out
    _, p, t1, t2 = g
    for lhs, rhs in tbox_ci:
        if rhs == ("E", p, False) and t2 == UNBOUND:
            out.append(basic_atom(lhs, t1))
        if rhs == ("E", p, True) and t1 == UNBOUND:
            out.append(basic_atom(lhs, t2))
    for r1, r2 in tbox_ri:
        if r2 == (p, False):
            out.append(role_atom(r1, t1, t2))
        elif r2 == (p, True):
            out.append(role_atom(r1, t2, t1))
    return out


def reduce_pair(q: tuple, g1: tuple, g2: tuple):
    """reduce(q, g1, g2): apply the most general unifier of g1 and g2 to q. None if they do not unify."""
    if g1[:2] != g2[:2]:
        return None
    head, body = q
    parent: dict[str, str] = {}

    def find(t: str) -> str:
        while t in parent:
            t = parent[t]
        return t

    hs = set(head)
    for a, b in zip(g1[2:], g2[2:]):
        if a == UNBOUND or b == UNBOUND:
            continue  # a new variable that occurs once unifies with anything and binds nothing
        a, b = find(a), find(b)
        if a != b:
            if a in hs:  # keep a head variable as the representative
                a, b = b, a
            parent[a] = b

    def sub(t: str) -> str:
        return t if t == UNBOUND else find(t)

    # The unified atom: at a position where one side is "_", the other side decides.
    unified = g1[:2] + tuple(sub(b) if a == UNBOUND else sub(a) for a, b in zip(g1[2:], g2[2:]))
    new_head = tuple(sub(t) for t in head)
    new_body = [g[:2] + tuple(sub(t) for t in g[2:]) for g in body if g != g1 and g != g2]
    return tau(new_head, new_body + [unified])


def perfect_ref(query: tuple, tbox_ci: Sequence[tuple], tbox_ri: Sequence[tuple] = ()) -> set[tuple]:
    """PerfectRef(q, T): the set of conjunctive queries of the rewriting."""
    start = tau(*query)
    pr = {start}  # @line L1
    todo = [start]
    while todo:  # @line L2
        q = todo.pop()
        head, body = q
        new = []
        for g in body:  # @line L3
            for g2 in rewrite_atom(g, tbox_ci, tbox_ri):  # @line L4
                new.append(tau(head, (body - {g}) | {g2}))  # @line L5
        atoms = sorted(body)
        for i in range(len(atoms)):  # @line L6
            for j in range(i + 1, len(atoms)):
                r = reduce_pair(q, atoms[i], atoms[j])  # @line L7
                if r is not None:
                    new.append(r)
        for q2 in new:
            if q2 not in pr:  # @line L8
                pr.add(q2)
                todo.append(q2)
    return pr  # @line L9


def evaluate_cq(q: tuple, abox: tuple) -> set[tuple]:
    """The answers of a conjunctive query over an ABox, as a database (closed world, no TBox)."""
    head, body = q
    concepts, roles = abox
    by_c: dict[str, list] = {}
    for a, x in concepts:
        by_c.setdefault(a, []).append(x)
    by_r: dict[str, list] = {}
    for p, x, y in roles:
        by_r.setdefault(p, []).append((x, y))
    atoms = sorted(body, key=lambda g: -sum(t != UNBOUND for t in g[2:]))
    out: set[tuple] = set()

    def match(t: str, v, env: dict) -> bool:
        if t == UNBOUND:
            return True
        if t in env:
            return env[t] == v
        env[t] = v
        return True

    def go(k: int, env: dict) -> None:
        if k == len(atoms):
            out.add(tuple(env[t] for t in head))
            return
        g = atoms[k]
        cands = [(x,) for x in by_c.get(g[1], ())] if g[0] == "C" else by_r.get(g[1], ())
        for vals in cands:
            e = dict(env)
            if all(match(t, v, e) for t, v in zip(g[2:], vals)):
                go(k + 1, e)

    go(0, {})
    return out


def evaluate_ucq(ucq: Iterable[tuple], abox: tuple) -> set[tuple]:
    out: set[tuple] = set()
    for q in ucq:
        out |= evaluate_cq(q, abox)
    return out


def certain_answers_by_rewriting(query: tuple, tbox_ci: Sequence[tuple], tbox_ri: Sequence[tuple], abox: tuple) -> set[tuple]:
    return evaluate_ucq(perfect_ref(query, tbox_ci, tbox_ri), abox)
