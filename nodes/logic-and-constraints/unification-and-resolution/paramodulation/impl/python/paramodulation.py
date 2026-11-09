# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paramodulation/. The authors are listed in prov/9GTMK7.jsonl.

"""Resolution with paramodulation, in a given-clause loop.

An equation s = t is the atom ("=", s, t). Paramodulation from a clause
C or l = r into a clause D[u], where u is a subterm of D at a position that
does not hold a variable, gives (C or D[r]) s when s is a most general
unifier of l and u. The equation is used in both directions.

The prover adds the reflexivity axiom x = x and, when asked, one
functional reflexivity axiom f(x1, ..., xn) = f(x1, ..., xn) for each
function symbol of the input. Robinson and Wos (1969) proved that
resolution, factoring and paramodulation are refutation complete for
equality on such sets. This loop also deletes tautologies and clauses that
are subsumed by an earlier clause, but it never deletes an input clause.

Terms are nested tuples, and a variable is a str. A literal is (sign, atom),
and a clause is a sorted tuple of distinct literals.
"""

import heapq
from typing import Any

Term = Any
Literal = tuple[bool, Term]
Clause = tuple[Literal, ...]
Subst = dict[str, Term]

UNSAT, SATURATED, UNKNOWN = "unsat", "saturated", "unknown"
EQ = "="


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


def subterms(atom: Term):
    """Yield (path, subterm) for each subterm of the arguments of atom that is not a variable."""
    stack = [((k,), a) for k, a in enumerate(atom[1:], 1)]
    while stack:
        path, t = stack.pop()
        if isinstance(t, str):
            continue
        yield path, t
        stack.extend((path + (k,), a) for k, a in enumerate(t[1:], 1))


def replace_at(t: Term, path: tuple[int, ...], new: Term) -> Term:
    if not path:
        return new
    k = path[0]
    return t[:k] + (replace_at(t[k], path[1:], new),) + t[k + 1:]


def at(t: Term, path: tuple[int, ...]) -> Term:
    for k in path:
        t = t[k]
    return t


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


def paramodulants(c: Clause, d: Clause):
    """Paramodulate from a positive equation of c into d (renamed apart).

    Yield (clause, i, side, j, path, mgu): literal i of c is l = r with l the
    argument at index side (1 or 2), and the subterm of literal j of d at path
    is unified with l and replaced by r.
    """
    d2 = rename_apart(d)
    for i, (sg, eq) in enumerate(c):
        if not sg or eq[0] != EQ or eq[1] == eq[2]:
            continue
        for side in (1, 2):
            lhs, rhs = eq[side], eq[3 - side]
            for j, (sg2, atom) in enumerate(d2):
                for path, u in subterms(atom):
                    s = unify(lhs, u)
                    if s is None:
                        continue
                    lits = [x for k, x in enumerate(c) if k != i]
                    lits += [x for k, x in enumerate(d2) if k != j]
                    lits.append((sg2, replace_at(atom, path, rhs)))
                    yield make_clause((g, substitute(t, s)) for g, t in lits), i, side, j, path, s


def function_symbols(clauses) -> set[tuple[str, int]]:
    out: set[tuple[str, int]] = set()
    stack = [a for c in clauses for _, a in c]
    while stack:
        t = stack.pop()
        for u in t[1:]:
            if not isinstance(u, str):
                if len(u) > 1:
                    out.add((u[0], len(u) - 1))
                stack.append(u)
    return out


def equality_axioms(clauses, functional_reflexivity: bool = True) -> list[Clause]:
    out = [((True, (EQ, "x", "x")),)]
    if functional_reflexivity:
        for f, n in sorted(function_symbols(clauses)):
            t = (f,) + tuple("x%d" % k for k in range(n))
            out.append(((True, (EQ, t, t)),))
    return out


def paramodulation(clauses, limit: int = 5000, functional_reflexivity: bool = True, age_every: int = 5):
    """Saturate under resolution, factoring and paramodulation.

    Return (UNSAT, proof), (SATURATED, active) or (UNKNOWN, None). A proof is a
    list of steps (id, clause, rule, parents, info). For "factor" and
    "resolve", info is (i, j, mgu) as in robinson-resolution. For
    "paramodulate", parents is (from, into), the into clause is renamed with
    rename_apart, and info is (i, side, j, path, mgu).
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

    inputs = [make_clause(c) for c in clauses]
    for c in inputs + equality_axioms(inputs, functional_reflexivity):  # @line L1
        add(make_clause(c), "input", (), None)
    n_inputs = len(store)
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
        if g_id >= n_inputs and (is_tautology(g) or any(subsumes(store[a][0], g) for a in active)):  # @line L5
            continue
        active = [a for a in active if a < n_inputs or not subsumes(g, store[a][0])]  # @line L6
        active.append(g_id)  # @line L7
        new = [(f, "factor", (g_id,), (i, j, s)) for f, i, j, s in factors(g)]  # @line L8
        for a in active:
            for r, i, j, s in resolvents(g, store[a][0]):  # @line L9
                new.append((r, "resolve", (g_id, a), (i, j, s)))
            for x, y in {(g_id, a), (a, g_id)}:  # @line L10
                for r, i, side, j, path, s in paramodulants(store[x][0], store[y][0]):
                    new.append((r, "paramodulate", (x, y), (i, side, j, path, s)))
        for c, rule, parents, info in new:  # @line L11
            add(c, rule, parents, info)
        if len(store) > limit:  # @line L12
            return UNKNOWN, None
    return SATURATED, [store[a][0] for a in active]  # @line L13


def _proof(store, k: int):
    need, stack = set(), [k]
    while stack:
        x = stack.pop()
        if x not in need:
            need.add(x)
            stack.extend(store[x][2])
    return [(x,) + store[x] for x in sorted(need)]
