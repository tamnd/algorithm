# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robinson-resolution/. The authors are listed in prov/ZY28KR.jsonl.

"""Resolution with factoring and subsumption in a given-clause loop.

Terms are nested tuples. A variable is a str. A constant c is the tuple
("c",), and f(t1, ..., tk) is ("f", t1, ..., tk). An atom has the same form,
with a predicate symbol in front. A literal is (sign, atom), where sign is
True for a positive literal. A clause is a sorted tuple of distinct literals,
and the empty tuple is the empty clause.

The prover is a semi-decision procedure. On an unsatisfiable input it finds
the empty clause if the clause limit is large enough. On a satisfiable input
it can stop with SATURATED, or it can reach the limit and answer UNKNOWN.
For ground input with n distinct atoms there are at most 3^n clauses, so the
loop stops after O(9^n) resolution attempts.
"""

import heapq
from typing import Any

Term = Any
Literal = tuple[bool, Term]
Clause = tuple[Literal, ...]
Subst = dict[str, Term]

UNSAT, SATURATED, UNKNOWN = "unsat", "saturated", "unknown"


def is_var(t: Term) -> bool:
    return isinstance(t, str)


def walk(t: Term, s: Subst) -> Term:
    while isinstance(t, str) and t in s:
        t = s[t]
    return t


def substitute(t: Term, s: Subst) -> Term:
    """Apply s to t, following chains of bindings to the end."""
    t = walk(t, s)
    if isinstance(t, str):
        return t
    return (t[0],) + tuple(substitute(a, s) for a in t[1:])


def rename(t: Term, ren: dict[str, str]) -> Term:
    """Replace each variable v by ren[v] in one step, with no chains of bindings."""
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
    """Extend s to a substitution m with p m == t. The variables of t stay fixed."""
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


def term_vars(t: Term, out: list[str]) -> list[str]:
    stack = [t]
    while stack:
        u = stack.pop()
        if isinstance(u, str):
            if u not in out:
                out.append(u)
        else:
            stack.extend(reversed(u[1:]))
    return out


def clause_vars(c: Clause) -> list[str]:
    out: list[str] = []
    for _, atom in c:
        term_vars(atom, out)
    return out


def make_clause(lits) -> Clause:
    """Sort the literals, drop duplicates, and rename the variables to X0, X1, ..."""
    c = tuple(sorted(set(lits), key=repr))
    ren = {v: "X%d" % i for i, v in enumerate(clause_vars(c))}
    return tuple(sorted({(sg, rename(a, ren)) for sg, a in c}, key=repr))


def rename_apart(c: Clause) -> Clause:
    """A variant of c whose variables end with a quote, so they differ from X0, X1, ..."""
    ren = {v: v + "'" for v in clause_vars(c)}
    return tuple((sg, rename(a, ren)) for sg, a in c)


def weight(c: Clause) -> int:
    n = 0
    for _, atom in c:
        stack = [atom]
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
    """True if c has at most as many literals as d and c m is a subset of d for some m."""
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
    """Yield (factor, i, j, mgu) for each pair of literals of c with the same sign that unify."""
    for i in range(len(c)):
        for j in range(i + 1, len(c)):
            if c[i][0] == c[j][0]:
                s = unify(c[i][1], c[j][1])
                if s is not None:
                    yield make_clause((sg, substitute(a, s)) for sg, a in c), i, j, s


def resolvents(c: Clause, d: Clause):
    """Yield (resolvent, i, j, mgu): c[i] and the renamed d[j] have opposite signs and their atoms unify."""
    d2 = rename_apart(d)
    for i, (sg, a) in enumerate(c):
        for j, (sg2, b) in enumerate(d2):
            if sg != sg2:
                s = unify(a, b)
                if s is not None:
                    rest = [x for k, x in enumerate(c) if k != i] + [x for k, x in enumerate(d2) if k != j]
                    yield make_clause((g, substitute(t, s)) for g, t in rest), i, j, s


def prove(clauses, limit: int = 5000, use_factoring: bool = True, use_subsumption: bool = True, age_every: int = 5, trace: list | None = None):
    """Run the given-clause loop.

    Return (UNSAT, proof), (SATURATED, active) or (UNKNOWN, None). A proof is a
    list of steps (id, clause, rule, parents, info) in the order of derivation;
    rule is "input", "factor" or "resolve", and info is (i, j, mgu) for a
    factor or a resolvent. The parent of a resolvent at position 1 is renamed
    with rename_apart before the step.
    """
    store: list[tuple[Clause, str, tuple[int, ...], Any]] = []
    by_weight: list[tuple[int, int]] = []
    by_age: list[int] = []
    taken: set[int] = set()
    seen: set[Clause] = set()

    def add(c: Clause, rule: str, parents: tuple[int, ...], info: Any) -> None:
        # A clause that was stored before is not stored again.
        if c in seen:
            return
        seen.add(c)
        store.append((c, rule, parents, info))
        k = len(store) - 1
        heapq.heappush(by_weight, (weight(c), k))
        heapq.heappush(by_age, k)

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
        if is_tautology(g):  # @line L5
            continue
        if any(store[a][0] == g for a in active):
            continue
        if use_subsumption and any(subsumes(store[a][0], g) for a in active):
            continue
        if use_subsumption:  # @line L6
            active = [a for a in active if not subsumes(g, store[a][0])]
        active.append(g_id)  # @line L7
        if trace is not None:
            trace.append((g_id, g, len(store)))
        new = []  # @line L8
        if use_factoring:
            for f, i, j, s in factors(g):
                new.append((f, "factor", (g_id,), (i, j, s)))
        for a in active:
            for r, i, j, s in resolvents(g, store[a][0]):
                new.append((r, "resolve", (g_id, a), (i, j, s)))
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


# ---------------------------------------------------------------- clausal form
#
# A formula is ("atom", A), ("not", F), ("and", F, G), ("or", F, G),
# ("imp", F, G), ("iff", F, G), ("all", x, F) or ("ex", x, F).


def _nnf(f, positive: bool, env: dict[str, str], fresh: list[int]):
    tag = f[0]
    if tag == "atom":
        return ("lit", positive, rename(f[1], env))
    if tag == "not":
        return _nnf(f[1], not positive, env, fresh)
    if tag == "imp":
        return _nnf(("or", ("not", f[1]), f[2]), positive, env, fresh)
    if tag == "iff":
        a, b = f[1], f[2]
        both = ("and", ("or", ("not", a), b), ("or", a, ("not", b)))
        return _nnf(both, positive, env, fresh)
    if tag in ("and", "or"):
        op = tag if positive else ("or" if tag == "and" else "and")
        return (op, _nnf(f[1], positive, env, fresh), _nnf(f[2], positive, env, fresh))
    q = tag if positive else ("ex" if tag == "all" else "all")
    fresh[0] += 1
    v = "V%d" % fresh[0]
    return (q, v, _nnf(f[2], positive, {**env, f[1]: v}, fresh))


def _skolem(f, scope: list[str], s: Subst, counter: list[int]):
    tag = f[0]
    if tag == "lit":
        return ("lit", f[1], substitute(f[2], s))
    if tag in ("and", "or"):
        return (tag, _skolem(f[1], scope, s, counter), _skolem(f[2], scope, s, counter))
    if tag == "all":
        return _skolem(f[2], scope + [f[1]], s, counter)
    counter[0] += 1
    used = _free_vars(f[2], s)
    args = tuple(v for v in scope if v in used)
    return _skolem(f[2], scope, {**s, f[1]: ("sk%d" % counter[0],) + args}, counter)


def _free_vars(f, s: Subst) -> set[str]:
    out: list[str] = []
    stack = [f]
    while stack:
        g = stack.pop()
        if g[0] == "lit":
            term_vars(substitute(g[2], s), out)
        elif g[0] in ("and", "or"):
            stack.extend(g[1:])
        else:
            stack.append(g[2])
    return set(out)


def _distribute(f) -> list[list[Literal]]:
    if f[0] == "lit":
        return [[(f[1], f[2])]]
    a, b = _distribute(f[1]), _distribute(f[2])
    if f[0] == "and":
        return a + b
    return [x + y for x in a for y in b]


def _define(f, out: list[list[Literal]], counter: list[int]) -> Literal:
    """Return a literal that stands for f, and add the clauses that define it."""
    if f[0] == "lit":
        return (f[1], f[2])
    a = _define(f[1], out, counter)
    b = _define(f[2], out, counter)
    counter[0] += 1
    vs: list[str] = []
    for _, atom in (a, b):
        term_vars(atom, vs)
    d = ("def%d" % counter[0],) + tuple(sorted(vs))
    if f[0] == "and":
        out.append([(False, d), a])
        out.append([(False, d), b])
    else:
        out.append([(False, d), a, b])
    return (True, d)


def clausal_form(formula, structural: bool = False) -> list[Clause]:
    """Clauses that are satisfiable if and only if the closed formula is.

    The steps are: negation normal form with bound variables renamed apart,
    Skolemization, and then distribution (structural=False) or one new
    predicate for each binary connective (structural=True, the
    Plaisted-Greenbaum form of the Tseitin idea). Distribution can give
    exponentially many clauses; the structural form has O(size) clauses.
    """
    g = _skolem(_nnf(formula, True, {}, [0]), [], {}, [0])
    if not structural or g[0] == "lit":
        raw = _distribute(g)
    else:
        raw: list[list[Literal]] = []
        top = _define(g, raw, [0])
        raw.append([top])
    return [make_clause(c) for c in raw]
