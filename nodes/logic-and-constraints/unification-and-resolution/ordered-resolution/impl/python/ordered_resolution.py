# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ordered-resolution/. The authors are listed in prov/HD62FE.jsonl.

"""Ordered resolution with selection, in a given-clause loop with subsumption.

The atom order is the Knuth-Bendix order (KBO) in which every symbol and
every variable has weight 1, and symbols are compared by a precedence. A
predicate symbol is treated as a function symbol. A literal is compared by
the multiset of its atoms: A is the multiset {A} and the negative literal
not A is {A, A}. So not A is above A, and both are below every literal
whose atom is above A.

A selection function maps a clause to the index of one of its negative
literals, or to None. Ordered resolution resolves C or A with D or not B
under the mgu s of A and B when
  * nothing is selected in C or A, and A s is strictly maximal in (C or A) s;
  * not B is selected in D or not B, or nothing is selected there and
    not B s is maximal in (D or not B) s.
Ordered factoring merges two positive literals when nothing is selected and
the merged literal is maximal. With a total precedence the calculus is
refutation complete (Bachmair and Ganzinger), also when tautologies and
subsumed clauses are deleted. Subsumption here is multiset subsumption:
distinct literals of the subsuming clause go to distinct literals.

Terms are nested tuples, and a variable is a str. A literal is (sign, atom),
and a clause is a sorted tuple of distinct literals.
"""

import heapq
from typing import Any, Callable

Term = Any
Literal = tuple[bool, Term]
Clause = tuple[Literal, ...]
Subst = dict[str, Term]
Select = Callable[[Clause], int | None]

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


def weight(t: Term) -> int:
    n, stack = 0, [t]
    while stack:
        u = stack.pop()
        n += 1
        if not isinstance(u, str):
            stack.extend(u[1:])
    return n


def var_counts(t: Term) -> dict[str, int]:
    out: dict[str, int] = {}
    stack = [t]
    while stack:
        u = stack.pop()
        if isinstance(u, str):
            out[u] = out.get(u, 0) + 1
        else:
            stack.extend(u[1:])
    return out


def kbo_greater(s: Term, t: Term, prec: dict[str, int]) -> bool:
    """Knuth-Bendix order with all weights 1. Symbols missing from prec rank lowest, then by name."""
    if s == t or isinstance(s, str):
        return False
    vs, vt = var_counts(s), var_counts(t)
    if any(vs.get(x, 0) < k for x, k in vt.items()):
        return False
    ws, wt = weight(s), weight(t)
    if ws != wt:
        return ws > wt
    if isinstance(t, str):
        return False
    ks = (prec.get(s[0], -1), s[0], len(s))
    kt = (prec.get(t[0], -1), t[0], len(t))
    if ks != kt:
        return ks > kt
    for a, b in zip(s[1:], t[1:]):
        if a != b:
            return kbo_greater(a, b, prec)
    return False


def lit_greater(x: Literal, y: Literal, prec: dict[str, int]) -> bool:
    """Multiset extension: A is {A}, not A is {A, A}."""
    if x[1] == y[1]:
        return not x[0] and y[0]
    return kbo_greater(x[1], y[1], prec)


def strictly_maximal(c: list[Literal], i: int, prec) -> bool:
    return all(k == i or (c[k] != c[i] and not lit_greater(c[k], c[i], prec)) for k in range(len(c)))


def maximal(c: list[Literal], i: int, prec) -> bool:
    return all(k == i or not lit_greater(c[k], c[i], prec) for k in range(len(c)))


def no_selection(c: Clause) -> int | None:
    return None


def is_tautology(c: Clause) -> bool:
    pos = {a for sg, a in c if sg}
    return any(not sg and a in pos for sg, a in c)


def subsumes(c: Clause, d: Clause) -> bool:
    """Multiset subsumption: c s is part of d, and distinct literals of c go to distinct literals of d."""
    if len(c) > len(d):
        return False
    stack: list[tuple[int, Subst, frozenset[int]]] = [(0, {}, frozenset())]
    while stack:
        i, s, used = stack.pop()
        if i == len(c):
            return True
        sg, a = c[i]
        for k, (sg2, b) in enumerate(d):
            if sg2 == sg and k not in used:
                m = match(a, b, s)
                if m is not None:
                    stack.append((i + 1, m, used | {k}))
    return False


def ordered_factors(c: Clause, prec, select: Select):
    if select(c) is not None:
        return
    for i in range(len(c)):
        for j in range(i + 1, len(c)):
            if c[i][0] and c[j][0]:
                s = unify(c[i][1], c[j][1])
                if s is None:
                    continue
                cs = [(sg, substitute(a, s)) for sg, a in c]
                if maximal(cs, i, prec):
                    yield make_clause(cs), i, j, s


def eligible(c: Clause, cs: list[Literal], i: int, prec, select: Select) -> bool:
    """Can literal i of c take part in a resolution step, given the instance cs of c?"""
    k = select(c)
    if c[i][0]:
        return k is None and strictly_maximal(cs, i, prec)
    return k == i if k is not None else maximal(cs, i, prec)


def ordered_resolvents(c: Clause, d: Clause, prec, select: Select):
    d2 = rename_apart(d)
    for i, (sg, a) in enumerate(c):
        for j, (sg2, b) in enumerate(d2):
            if sg == sg2:
                continue
            s = unify(a, b)
            if s is None:
                continue
            cs = [(g, substitute(t, s)) for g, t in c]
            ds = [(g, substitute(t, s)) for g, t in d2]
            if eligible(c, cs, i, prec, select) and eligible(d, ds, j, prec, select):
                rest = [x for k, x in enumerate(cs) if k != i] + [x for k, x in enumerate(ds) if k != j]
                yield make_clause(rest), i, j, s


def ordered_resolution(clauses, prec: dict[str, int] | None = None, select: Select = no_selection, limit: int = 5000, age_every: int = 5):
    """Saturate under ordered resolution and ordered factoring.

    Return (UNSAT, proof), (SATURATED, active) or (UNKNOWN, None). A proof is a
    list of steps (id, clause, rule, parents, info) as in robinson-resolution.
    """
    prec = prec or {}
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
        heapq.heappush(by_weight, (sum(weight(a) for _, a in c), len(store) - 1))
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
        new = [(f, "factor", (g_id,), (i, j, s)) for f, i, j, s in ordered_factors(g, prec, select)]  # @line L8
        for a in active:  # @line L9
            for r, i, j, s in ordered_resolvents(g, store[a][0], prec, select):
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
