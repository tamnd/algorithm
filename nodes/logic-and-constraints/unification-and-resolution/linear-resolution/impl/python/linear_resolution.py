# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-resolution/. The authors are listed in prov/4MCTF6.jsonl.

"""Linear resolution by iterative deepening.

A linear derivation starts with a top clause C0 of the input set S. Each next
center C(i+1) is a factor of C(i), or a resolvent of C(i) with a side clause
that is a clause of S, a factor of one, or an earlier center C(j), j < i.
Linear resolution is refutation complete (Loveland 1970, Luckham 1970): if S
is unsatisfiable and S minus C is satisfiable, there is a linear refutation
with top clause C.

Terms are nested tuples, and a variable is a str. A literal is (sign, atom),
and a clause is a sorted tuple of distinct literals. The search tries all
chains up to a depth bound, so its time is exponential in the bound: with b
choices at each step, depth d costs O(b^d) chains.
"""

from typing import Any

Term = Any
Literal = tuple[bool, Term]
Clause = tuple[Literal, ...]
Subst = dict[str, Term]

UNSAT, UNKNOWN = "unsat", "unknown"


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


def input_sides(s: list[Clause]) -> list[tuple[Clause, Any]]:
    """The input clauses, then all factors of them, factors of factors, and so on.

    Each entry is (clause, origin): origin is None for an input clause and
    (k, i, j, mgu) for a factor of entry k. Each factor is shorter than its
    parent, so the list is finite.
    """
    out: list[tuple[Clause, Any]] = [(c, None) for c in s]
    seen = set(s)
    k = 0
    while k < len(out):
        for f, i, j, sb in factors(out[k][0]):
            if f not in seen:
                seen.add(f)
                out.append((f, (k, i, j, sb)))
        k += 1
    return out


def linear_resolution(clauses, max_depth: int = 8, top: int | None = None):
    """Search for a linear refutation of at most max_depth steps.

    Return (UNSAT, (top, steps, sides)) or (UNKNOWN, None). sides is the
    list of input_sides. Each step is (center, rule, side, info): rule is
    "factor" (side is None) or "resolve", side is ("input", k) for entry k of
    sides or ("center", j) for the j-th center, and info is (i, j, mgu) as in
    resolvents. If top is given, only that input clause is tried as the top
    clause.
    """
    s = [make_clause(c) for c in clauses]
    sides = input_sides(s)  # @line L1
    ground = not any(clause_vars(c) for c in s)
    tops = range(len(s)) if top is None else [top]
    for depth in range(max_depth + 1):  # @line L2
        for t in tops:  # @line L3
            steps: list = []
            if _search([c for c, _ in sides], [s[t]], steps, depth, ground):  # @line L4
                return UNSAT, (t, steps, sides)
    return UNKNOWN, None  # @line L5


def _search(s: list[Clause], chain: list[Clause], steps: list, depth: int, ground: bool) -> bool:
    c = chain[-1]
    if not c:  # @line L6
        return True
    if depth == 0 or (ground and len(c) > depth):  # @line L7
        return False
    moves = [(f, "factor", None, (i, j, sb)) for f, i, j, sb in factors(c)]  # @line L8
    sides = [(("input", k), d) for k, d in enumerate(s)] + [(("center", k), d) for k, d in enumerate(chain[:-1])]
    for side, d in sides:
        for r, i, j, sb in resolvents(c, d):
            moves.append((r, "resolve", side, (i, j, sb)))
    for r, rule, side, info in moves:  # @line L9
        chain.append(r)
        steps.append((r, rule, side, info))
        if _search(s, chain, steps, depth - 1, ground):
            return True
        chain.pop()
        steps.pop()
    return False  # @line L10
