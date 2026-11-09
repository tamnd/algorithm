# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unit-resolution/. The authors are listed in prov/HX313Y.jsonl.

"""Unit resolution: resolution in which one parent of each step is a unit clause.

Terms are nested tuples, and a variable is a str: ("f", "x", ("a",)) is
f(x, a). A literal is (sign, atom) and a clause is a sorted tuple of distinct
literals. The procedure is sound. It is refutation complete for Horn clauses,
and not complete in general. On ground input it always stops, because each
unit resolvent is a sub-clause of an input clause. For propositional input,
unit resolution is unit propagation, which runs in linear time with counters
(see horn-sat); this loop is a simple form without those counters.
"""

import heapq
from typing import Any

Term = Any
Literal = tuple[bool, Term]
Clause = tuple[Literal, ...]
Subst = dict[str, Term]

UNSAT, SATURATED, UNKNOWN = "unsat", "saturated", "unknown"


def walk(t: Term, s: Subst) -> Term:
    while isinstance(t, str) and t in s:
        t = s[t]
    return t


def substitute(t: Term, s: Subst) -> Term:
    t = walk(t, s)
    if isinstance(t, str):
        return t
    return (t[0],) + tuple(substitute(a, s) for a in t[1:])


def rename(t: Term, ren: dict[str, str]) -> Term:
    if isinstance(t, str):
        return ren.get(t, t)
    return (t[0],) + tuple(rename(a, ren) for a in t[1:])


def occurs(v: str, t: Term, s: Subst) -> bool:
    stack = [t]
    while stack:
        u = walk(stack.pop(), s)
        if isinstance(u, str):
            if u == v:
                return True
        else:
            stack.extend(u[1:])
    return False


def unify(a: Term, b: Term) -> Subst | None:
    """Return an idempotent most general unifier of a and b, or None."""
    s: Subst = {}
    stack = [(a, b)]
    while stack:
        x, y = stack.pop()
        x, y = walk(x, s), walk(y, s)
        if x == y:
            continue
        if isinstance(x, str):
            if occurs(x, y, s):
                return None
            s[x] = y
        elif isinstance(y, str):
            if occurs(y, x, s):
                return None
            s[y] = x
        elif x[0] != y[0] or len(x) != len(y):
            return None
        else:
            stack.extend(zip(x[1:], y[1:]))
    return {v: substitute(t, s) for v, t in s.items()}


def match(p: Term, t: Term, s: Subst) -> Subst | None:
    s = dict(s)
    stack = [(p, t)]
    while stack:
        p, t = stack.pop()
        if isinstance(p, str):
            if p in s:
                if s[p] != t:
                    return None
            else:
                s[p] = t
        elif isinstance(t, str) or p[0] != t[0] or len(p) != len(t):
            return None
        else:
            stack.extend(zip(p[1:], t[1:]))
    return s


def clause_vars(c: Clause) -> list[str]:
    out: list[str] = []
    stack = [a for _, a in reversed(c)]
    while stack:
        u = stack.pop()
        if isinstance(u, str):
            if u not in out:
                out.append(u)
        else:
            stack.extend(reversed(u[1:]))
    return out


def make_clause(lits) -> Clause:
    c = tuple(sorted(set(lits), key=repr))
    ren = {v: "X%d" % i for i, v in enumerate(clause_vars(c))}
    return tuple(sorted({(sg, rename(a, ren)) for sg, a in c}, key=repr))


def rename_apart(c: Clause) -> Clause:
    ren = {v: v + "'" for v in clause_vars(c)}
    return tuple((sg, rename(a, ren)) for sg, a in c)


def weight(c: Clause) -> int:
    n, stack = 0, [a for _, a in c]
    while stack:
        u = stack.pop()
        n += 1
        if not isinstance(u, str):
            stack.extend(u[1:])
    return n


def is_tautology(c: Clause) -> bool:
    pos = {a for sg, a in c if sg}
    return any(not sg and a in pos for sg, a in c)


def subsumes(c: Clause, d: Clause) -> bool:
    if len(c) > len(d):
        return False
    stack: list[tuple[int, Subst]] = [(0, {})]
    while stack:
        i, s = stack.pop()
        if i == len(c):
            return True
        sg, a = c[i]
        for sg2, b in d:
            if sg2 == sg:
                m = match(a, b, s)
                if m is not None:
                    stack.append((i + 1, m))
    return False


def factors(c: Clause):
    for i in range(len(c)):
        for j in range(i + 1, len(c)):
            if c[i][0] == c[j][0]:
                s = unify(c[i][1], c[j][1])
                if s is not None:
                    yield make_clause((sg, substitute(a, s)) for sg, a in c), i, j, s


def resolvents(c: Clause, d: Clause):
    d2 = rename_apart(d)
    for i, (sg, a) in enumerate(c):
        for j, (sg2, b) in enumerate(d2):
            if sg != sg2:
                s = unify(a, b)
                if s is not None:
                    rest = [x for k, x in enumerate(c) if k != i] + [x for k, x in enumerate(d2) if k != j]
                    yield make_clause((g, substitute(t, s)) for g, t in rest), i, j, s


def unit_resolution(clauses, limit: int = 5000, age_every: int = 5):
    """Saturate under unit resolution and factoring.

    Return (UNSAT, proof), (SATURATED, active) or (UNKNOWN, None). Each step of
    a proof is (id, clause, rule, parents, info) with rule "input", "factor"
    or "resolve"; for a resolvent, info is (i, j, mgu), parent 1 is renamed
    with rename_apart, and at least one parent is a unit clause.
    """
    store: list[tuple[Clause, str, tuple[int, ...], Any]] = []
    by_weight: list[tuple[int, int]] = []
    by_age: list[int] = []
    taken: set[int] = set()
    seen: set[Clause] = set()

    def add(c: Clause, rule: str, parents: tuple[int, ...], info: Any) -> None:
        if c in seen:
            return
        seen.add(c)
        store.append((c, rule, parents, info))
        heapq.heappush(by_weight, (weight(c), len(store) - 1))
        heapq.heappush(by_age, len(store) - 1)

    for c in clauses:  # @line L1
        add(make_clause(c), "input", (), None)
    active: list[int] = []
    picks = 0
    while len(taken) < len(store):  # @line L2
        picks += 1
        heap = by_age if picks % age_every == 0 else by_weight  # @line L3
        while True:
            top = heapq.heappop(heap)
            g_id = top if isinstance(top, int) else top[1]
            if g_id not in taken:
                break
        taken.add(g_id)
        g = store[g_id][0]
        if not g:  # @line L4
            return UNSAT, _proof(store, g_id)
        if is_tautology(g) or any(subsumes(store[a][0], g) for a in active):  # @line L5
            continue
        active = [a for a in active if not subsumes(g, store[a][0])]  # @line L6
        active.append(g_id)  # @line L7
        new = [(f, "factor", (g_id,), (i, j, s)) for f, i, j, s in factors(g)]  # @line L8
        for a in active:
            if len(g) == 1 or len(store[a][0]) == 1:  # @line L9
                for r, i, j, s in resolvents(g, store[a][0]):
                    new.append((r, "resolve", (g_id, a), (i, j, s)))
        for c, rule, parents, info in new:  # @line L10
            add(c, rule, parents, info)
        if len(store) > limit:  # @line L11
            return UNKNOWN, None
    return SATURATED, [store[a][0] for a in active]  # @line L12


def _proof(store, k: int):
    need, stack = set(), [k]
    while stack:
        x = stack.pop()
        if x not in need:
            need.add(x)
            stack.extend(store[x][2])
    return [(x,) + store[x] for x in sorted(need)]
