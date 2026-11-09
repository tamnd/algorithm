# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperresolution/. The authors are listed in prov/BHQ7B0.jsonl.

"""Positive hyperresolution with factoring and subsumption in a given-clause loop.

A nucleus is a clause with at least one negative literal. Electrons are
positive clauses. One hyperresolution step resolves every negative literal of
a nucleus at once, each with a positive literal of an electron, under one
simultaneous most general unifier. The result is a positive clause.

Terms are nested tuples, and a variable is a str. A literal is (sign, atom),
and a clause is a sorted tuple of distinct literals. The electron in slot k
of a step is renamed by adding "'k" to each of its variables.

Positive hyperresolution with factoring is sound and refutation complete
(Robinson 1965). On ground input with n atoms there are at most 2^n positive
clauses, so the loop stops.
"""

import heapq
import itertools
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


def weight(c: Clause) -> int:
    n, stack = 0, [a for _, a in c]
    while stack:
        u = stack.pop()
        n += 1
        if not isinstance(u, str):
            stack.extend(u[1:])
    return n


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


def is_positive(c: Clause) -> bool:
    return all(sg for sg, _ in c)


def electron_copy(e: Clause, k: int) -> Clause:
    ren = {v: v + "'%d" % k for v in clause_vars(e)}
    return tuple((sg, rename(a, ren)) for sg, a in e)


def hyperresolvents(nucleus: Clause, electrons: list[tuple[int, Clause]], must_use: int | None):
    """Yield (clause, electron ids, positions, mgu) for each clash of the nucleus.

    The k-th negative literal of the nucleus is resolved with the literal at
    position positions[k] of the k-th electron. If must_use is not None, one
    of the electrons must have that id.
    """
    negs = [a for sg, a in nucleus if not sg]
    rest = [(sg, a) for sg, a in nucleus if sg]
    for chosen in itertools.product(electrons, repeat=len(negs)):
        if must_use is not None and all(eid != must_use for eid, _ in chosen):
            continue
        copies = [electron_copy(e, k) for k, (_, e) in enumerate(chosen)]
        for positions in itertools.product(*[range(len(c)) for c in copies]):
            left = ("tuple",) + tuple(negs)
            right = ("tuple",) + tuple(c[p][1] for c, p in zip(copies, positions))
            s = unify(left, right)
            if s is None:
                continue
            lits = list(rest)
            for c, p in zip(copies, positions):
                lits += [x for q, x in enumerate(c) if q != p]
            yield make_clause((sg, substitute(a, s)) for sg, a in lits), tuple(eid for eid, _ in chosen), positions, s


def hyperresolution(clauses, limit: int = 5000, age_every: int = 5):
    """Saturate under positive hyperresolution and factoring of electrons.

    Return (UNSAT, proof), (SATURATED, active) or (UNKNOWN, None). Each step of
    a proof is (id, clause, rule, parents, info). For rule "hyper", parents
    is (nucleus, electron 0, electron 1, ...) and info is (positions, mgu).
    For rule "factor", info is (i, j, mgu).
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
        if is_positive(c):
            heapq.heappush(by_weight, (weight(c), len(store) - 1))
            heapq.heappush(by_age, len(store) - 1)
        else:
            taken.add(len(store) - 1)

    for c in clauses:  # @line L1
        add(make_clause(c), "input", (), None)
    nuclei = [k for k in range(len(store)) if not is_positive(store[k][0])]
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
        if any(subsumes(store[a][0], g) for a in active):  # @line L5
            continue
        active = [a for a in active if not subsumes(g, store[a][0])]  # @line L6
        active.append(g_id)  # @line L7
        new = [(f, "factor", (g_id,), (i, j, s)) for f, i, j, s in factors(g)]  # @line L8
        electrons = [(a, store[a][0]) for a in active]
        for n in nuclei:
            for h, eids, positions, s in hyperresolvents(store[n][0], electrons, g_id):
                new.append((h, "hyper", (n,) + eids, (positions, s)))
        for c, rule, parents, info in new:  # @line L9
            add(c, rule, parents, info)
        if len(store) > limit:  # @line L10
            return UNKNOWN, None
    return SATURATED, [store[a][0] for a in active]  # @line L11


def _proof(store, k: int):
    need, stack = set(), [k]
    while stack:
        x = stack.pop()
        if x not in need:
            need.add(x)
            stack.extend(store[x][2])
    return [(x,) + store[x] for x in sorted(need)]
