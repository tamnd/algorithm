# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/superposition/. The authors are listed in prov/8J4M9K.jsonl.

"""The superposition calculus for clauses of equations, with demodulation.

Every literal is an equation s = t or a disequation s != t; the atom is
("=", s, t) and is read without orientation. Terms are compared by the
Knuth-Bendix order (KBO) in which every symbol and variable has weight 1 and
symbols are ranked by a precedence. The literal s = t is the multiset {s, t},
the literal s != t is {s, s, t, t}, and literals are compared by the multiset
extension of KBO.

The inference rules, with s the mgu and every condition checked on the
instances under s:
  superposition   from C or l = r into D or L[u], u not a variable, s = mgu(l, u):
                  gives (C or D or L[r]) s, when r s is not >= l s, l = r is
                  strictly maximal in its clause, L is strictly maximal in its
                  clause when it is positive and maximal when it is negative,
                  and the other side of L is not >= the side that holds u;
  equality resolution   C or s != t gives C s when s = mgu(s, t) and
                  s != t is maximal;
  equality factoring    C or s = t or s' = t' gives (C or t != t' or s' = t') s
                  when s = mgu(s, s'), t s is not >= s s, and s = t is maximal.
The loop deletes tautologies and subsumed clauses, and rewrites each given
clause with the unit equations in the active set (demodulation). With a
total precedence this calculus is refutation complete (Bachmair and
Ganzinger 1990, 1994).
"""

import heapq
from typing import Any, Callable

Term = Any
Literal = tuple[bool, Term]
Clause = tuple[Literal, ...]
Subst = dict[str, Term]

UNSAT, SATURATED, UNKNOWN = "unsat", "saturated", "unknown"
EQ = "="


# ---------------------------------------------------------------- terms and substitutions


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


def subterms(t: Term, path: tuple[int, ...] = ()):
    """Yield (path, subterm) for each subterm of t that is not a variable, in preorder."""
    stack = [(path, t)]
    while stack:
        p, u = stack.pop()
        if isinstance(u, str):
            continue
        yield p, u
        stack.extend(reversed([(p + (k,), a) for k, a in enumerate(u[1:], 1)]))


def replace_at(t: Term, path: tuple[int, ...], new: Term) -> Term:
    if not path:
        return new
    k = path[0]
    return t[:k] + (replace_at(t[k], path[1:], new),) + t[k + 1:]


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
    lits = {(sg, (EQ,) + tuple(sorted(a[1:], key=repr))) for sg, a in lits}
    c = tuple(sorted(lits, key=repr))
    ren = {v: "X%d" % i for i, v in enumerate(clause_vars(c))}
    return tuple(sorted({(sg, rename(a, ren)) for sg, a in c}, key=repr))


def rename_apart(c: Clause, mark: str = "'") -> Clause:
    ren = {v: v + mark for v in clause_vars(c)}
    return tuple((sg, rename(a, ren)) for sg, a in c)


# ---------------------------------------------------------------- the order


def size(t: Term) -> int:
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
    ws, wt = size(s), size(t)
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


def kbo_geq(s: Term, t: Term, prec) -> bool:
    return s == t or kbo_greater(s, t, prec)


def lit_multiset(x: Literal) -> list[Term]:
    _, s, t = x[1]
    return [s, t] if x[0] else [s, s, t, t]


def multiset_greater(m: list[Term], n: list[Term], gt: Callable[[Term, Term], bool]) -> bool:
    m, n = list(m), list(n)
    for x in list(m):
        if x in n:
            n.remove(x)
            m.remove(x)
    return bool(m) and all(any(gt(a, b) for a in m) for b in n)


def lit_greater(x: Literal, y: Literal, prec) -> bool:
    return multiset_greater(lit_multiset(x), lit_multiset(y), lambda a, b: kbo_greater(a, b, prec))


def lit_same(x: Literal, y: Literal) -> bool:
    return sorted(lit_multiset(x), key=repr) == sorted(lit_multiset(y), key=repr)


def maximal(c: list[Literal], i: int, prec) -> bool:
    return all(k == i or not lit_greater(c[k], c[i], prec) for k in range(len(c)))


def strictly_maximal(c: list[Literal], i: int, prec) -> bool:
    return all(k == i or (not lit_same(c[k], c[i]) and not lit_greater(c[k], c[i], prec)) for k in range(len(c)))


# ---------------------------------------------------------------- inferences


def inst(c, s: Subst) -> list[Literal]:
    return [(sg, (EQ, substitute(a[1], s), substitute(a[2], s))) for sg, a in c]


def superpositions(c: Clause, d: Clause, prec):
    """From a positive literal of c into d (renamed apart).

    Yield (clause, i, lside, j, path, mgu): l is side lside of literal i of c,
    and u is the subterm of the atom of literal j of d at path (path[0] is
    the side of that literal that holds u).
    """
    d2 = rename_apart(d)
    for i, (sg1, e1) in enumerate(c):
        if not sg1:
            continue
        for lside in (1, 2):
            l, r = e1[lside], e1[3 - lside]
            for j, (sg2, e2) in enumerate(d2):
                for side in (1, 2):
                    for path, u in subterms(e2[side], (side,)):
                        s = unify(l, u)
                        if s is None:
                            continue
                        lt, rt = substitute(l, s), substitute(r, s)
                        st, tt = substitute(e2[side], s), substitute(e2[3 - side], s)
                        if kbo_geq(rt, lt, prec) or kbo_geq(tt, st, prec):
                            continue
                        cs, ds = inst(c, s), inst(d2, s)
                        if not strictly_maximal(cs, i, prec):
                            continue
                        if not (strictly_maximal(ds, j, prec) if sg2 else maximal(ds, j, prec)):
                            continue
                        new = (sg2, replace_at(e2, path, r))
                        lits = [x for k, x in enumerate(c) if k != i] + [x for k, x in enumerate(d2) if k != j] + [new]
                        yield make_clause(inst(lits, s)), i, lside, j, path, s


def equality_resolvents(c: Clause, prec):
    for j, (sg, e) in enumerate(c):
        if sg:
            continue
        s = unify(e[1], e[2])
        if s is not None and maximal(inst(c, s), j, prec):
            yield make_clause(inst([x for k, x in enumerate(c) if k != j], s)), j, s


def equality_factors(c: Clause, prec):
    for i, (sg1, e1) in enumerate(c):
        for j, (sg2, e2) in enumerate(c):
            if i == j or not sg1 or not sg2:
                continue
            for iside in (1, 2):
                for jside in (1, 2):
                    a, b = e1[iside], e1[3 - iside]
                    a2, b2 = e2[jside], e2[3 - jside]
                    s = unify(a, a2)
                    if s is None or kbo_geq(substitute(b, s), substitute(a, s), prec):
                        continue
                    if not maximal(inst(c, s), i, prec):
                        continue
                    lits = [x for k, x in enumerate(c) if k not in (i, j)] + [(False, (EQ, b, b2)), (True, (EQ, a2, b2))]
                    yield make_clause(inst(lits, s)), i, iside, j, jside, s


# ---------------------------------------------------------------- redundancy


def rewrite_once(t: Term, units: list[tuple[int, Clause]], prec, guard=None):
    """One leftmost-outermost rewrite step of t with a unit equation l = r, used in the direction l to r.

    The step needs l m > r m in KBO, and guard(l m, r m) when guard is given.
    Return (new term, (unit id, side of l, path, m)) or None.
    """
    for path, u in subterms(t):
        for uid, unit in units:
            e = rename_apart(unit, "'u")[0][1]
            for lside in (1, 2):
                m = match(e[lside], u, {})
                if m is None:
                    continue
                lt, rt = substitute(e[lside], m), substitute(e[3 - lside], m)
                if kbo_greater(lt, rt, prec) and (guard is None or guard(lt, rt)):
                    return replace_at(t, path, rt), (uid, lside, path, m)
    return None


def demodulate(t: Term, units: list[tuple[int, Clause]], prec) -> tuple[Term, list]:
    """Rewrite t to normal form with the oriented instances of the unit equations."""
    steps = []
    while True:
        step = rewrite_once(t, units, prec)
        if step is None:
            return t, steps
        t, info = step
        steps.append(info)


def demodulate_clause(c: Clause, units: list[tuple[int, Clause]], prec) -> tuple[Clause, list]:
    """Rewrite c while each step makes c redundant: the rewritten literal must be above l m = r m."""
    lits, steps = list(c), []
    k = 0
    while k < len(lits):
        sg, e = lits[k]
        done = False
        for side in (1, 2):
            step = rewrite_once(e[side], units, prec, lambda lt, rt: lit_greater((sg, e), (True, (EQ, lt, rt)), prec))
            if step is not None:
                new_side, (uid, lside, path, m) = step
                lits[k] = (sg, replace_at(e, (side,), new_side))
                steps.append((k, (side,) + path, uid, lside, m))
                done = True
                break
        if not done:
            k += 1
    return tuple(lits), steps


def is_tautology(c: Clause) -> bool:
    pos = {a for sg, a in c if sg}
    return any(sg and a[1] == a[2] for sg, a in c) or any(not sg and a in pos for sg, a in c)


def subsumes(c: Clause, d: Clause) -> bool:
    """Multiset subsumption: c m is part of d for some matcher m, and distinct
    literals of c go to distinct literals of d; equations match in both directions."""
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
                for b2 in (b, (EQ, b[2], b[1])):
                    m = match(a, b2, s)
                    if m is not None:
                        stack.append((i + 1, m, used | {k}))
    return False


# ---------------------------------------------------------------- the loop


def superposition(clauses, prec: dict[str, int] | None = None, limit: int = 5000, age_every: int = 5):
    """Saturate under superposition, equality resolution and equality factoring.

    Return (UNSAT, proof), (SATURATED, active) or (UNKNOWN, None). Each step of
    a proof is (id, clause, rule, parents, info). For "superpose" parents is
    (from, into), the into clause is renamed with rename_apart, and info is
    (i, lside, j, path, mgu). For "eqres" info is (j, mgu); for "eqfact" it
    is (i, iside, j, jside, mgu). For "demod" parents is (clause, units...)
    and info is the list of rewrite steps (literal, path, unit id, side, m).
    """
    prec = prec or {}
    store: list[tuple[Clause, str, tuple[int, ...], Any]] = []
    by_weight: list[tuple[int, int]] = []
    by_age: list[int] = []
    taken: set[int] = set()
    seen: set[Clause] = set()

    def add(c: Clause, rule: str, parents: tuple[int, ...], info: Any) -> int | None:
        if c in seen:
            return None
        seen.add(c)
        store.append((c, rule, parents, info))
        heapq.heappush(by_weight, (sum(size(a) for _, a in c), len(store) - 1))
        heapq.heappush(by_age, len(store) - 1)
        return len(store) - 1

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
        units = [(a, store[a][0]) for a in active if len(store[a][0]) == 1 and store[a][0][0][0]]
        g, steps = demodulate_clause(store[g_id][0], units, prec)  # @line L4
        if steps:
            g = make_clause(g)
            new_id = add(g, "demod", (g_id,) + tuple(sorted({st[2] for st in steps})), steps)
            if new_id is None:
                continue  # the rewritten clause is stored already
            g_id = new_id
            taken.add(g_id)
        if not g:  # @line L5
            return UNSAT, _proof(store, g_id)
        if is_tautology(g) or any(subsumes(store[a][0], g) for a in active):  # @line L6
            continue
        active = [a for a in active if not subsumes(g, store[a][0])]  # @line L7
        active.append(g_id)  # @line L8
        new = [(r, "eqres", (g_id,), (j, s)) for r, j, s in equality_resolvents(g, prec)]  # @line L9
        new += [(r, "eqfact", (g_id,), (i, a, j, b, s)) for r, i, a, j, b, s in equality_factors(g, prec)]
        for a in active:  # @line L10
            for x, y in {(g_id, a), (a, g_id)}:
                for r, i, lside, j, path, s in superpositions(store[x][0], store[y][0], prec):
                    new.append((r, "superpose", (x, y), (i, lside, j, path, s)))
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
