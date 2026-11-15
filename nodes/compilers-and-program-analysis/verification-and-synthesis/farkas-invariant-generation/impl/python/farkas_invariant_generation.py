# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/farkas-invariant-generation/. The authors are listed in prov/K23N8A.jsonl.
"""Constraint-based generation of linear invariants with Farkas' lemma.

A loop has n rational variables x. Init is a list of rows (a, b), each the
inequality a . x <= b. A transition is a list of rows (a, b) with len(a) =
2n, each the inequality a[:n] . x + a[n:] . x' <= b over the old state x and
the new state x'. The template is c . x + d <= 0 with unknown c and d.

invariant_for(loop, bad, mus) looks for an inequality that holds initially,
is kept by every transition over the rationals, and is false at the point
bad. Each transition is handled by one of the cases ("cons", mu) with mu in
mus, where the transition keeps the inequality, or ("dis", 1), where the
transition cannot fire from a state of the inequality. Each choice of cases
gives one linear program, solved exactly with rational arithmetic. The
answer is (c, d) with coprime integers, or None. If Init is empty, the
answer is the inequality 1 <= 0, which is false and inductive.

Result: sound always; complete for the invariants whose consecution
multipliers lie in mus (see the proof file). Cost: (|mus| + 1)^k linear
programs for the k transitions with a nonempty relation, each with
O(n + m) unknowns for m rows in all.
"""

from itertools import product
from math import gcd

from fraclp import feasible_point


class Loop:
    """A loop with rational variables: n, the rows of Init, and the rows of
    each transition over (x, x')."""

    def __init__(self, n, init, trans):
        self.n = n
        self.init = [(list(a), b) for a, b in init]
        self.trans = [[(list(a), b) for a, b in t] for t in trans]


def affine(n, guard, update):
    """The rows of the transition 'if guard then x := U x + u'. guard is a
    list of rows (a, b) over x; update is a list of n pairs (U_k, u_k) and
    sets x'_k = U_k . x + u_k."""
    rows = [(list(a) + [0] * n, b) for a, b in guard]
    for k, (uk, ck) in enumerate(update):
        e = [0] * n
        e[k] = 1
        lhs = [-v for v in uk] + e
        rows.append((lhs, ck))
        rows.append(([-v for v in lhs], -ck))
    return rows


def equal(a, b):
    """The two rows of a . x = b."""
    return [(list(a), b), ([-v for v in a], -b)]


def cases(mus):
    """The order in which the cases of one transition are tried. The case
    ("dis", 0), an empty transition, is handled once in invariant_for."""
    return [("cons", mu) for mu in mus] + [("dis", 1)]


def empty(rows, n):
    """Whether the rows have no rational solution in n variables."""
    return feasible_point(a_ub=[a for a, _ in rows], b_ub=[b for _, b in rows], n=n, free=range(n)) is None


def _merge(rows):
    """Join each pair of rows a . v <= b, -a . v <= -b that follow each
    other into one equality. Its multiplier is then free in sign, which is
    the difference of the two nonnegative ones; the system is the same, only
    smaller. Returns a list of (a, b, is_equality)."""
    out = []
    i = 0
    while i < len(rows):
        a, b = rows[i]
        if i + 1 < len(rows) and rows[i + 1][1] == -b and all(u == -v for u, v in zip(rows[i + 1][0], a)):
            out.append((a, b, True))
            i += 2
        else:
            out.append((a, b, False))
            i += 1
    return out


def _system(loop, bad, choice):
    """The linear system of one choice of cases. Unknowns: c (n, free),
    d (free), then one multiplier per row of Init and of each transition."""
    n = loop.n
    blocks = [_merge(loop.init)] + [_merge(t) for t in loop.trans]
    nvar = n + 1 + sum(len(b) for b in blocks)
    free = list(range(n + 1))
    off = n + 1
    for block in blocks:
        free += [off + i for i, (_, _, eq) in enumerate(block) if eq]
        off += len(block)
    init, trans = blocks[0], blocks[1:]
    a_eq, b_eq, a_ub, b_ub = [], [], [], []

    def row():
        return [0] * nvar

    off = n + 1
    # @line L2 initiation: lambda0 P = c and lambda0 p <= -d
    for k in range(n):
        r = row()
        r[k] = -1
        for i, (a, _, _) in enumerate(init):
            r[off + i] = a[k]
        a_eq.append(r)
        b_eq.append(0)
    r = row()
    r[n] = 1
    for i, (_, b, _) in enumerate(init):
        r[off + i] = b
    a_ub.append(r)
    b_ub.append(0)
    off += len(init)
    # @line L3 one block of constraints per transition
    for t, (kind, mu) in zip(trans, choice):
        for k in range(n):
            # mu c + lambda A = 0, where A is the part over x
            r = row()
            r[k] = mu
            for i, (a, _, _) in enumerate(t):
                r[off + i] = a[k]
            a_eq.append(r)
            b_eq.append(0)
            # lambda A' = c (cons) or lambda A' = 0 (dis)
            r = row()
            if kind == "cons":
                r[k] = -1
            for i, (a, _, _) in enumerate(t):
                r[off + i] = a[n + k]
            a_eq.append(r)
            b_eq.append(0)
        r = row()
        for i, (_, b, _) in enumerate(t):
            r[off + i] = b
        if kind == "cons":
            # @line L4 lambda t <= (mu - 1) d
            r[n] = 1 - mu
            a_ub.append(r)
            b_ub.append(0)
        else:
            # @line L5 lambda t - mu d <= -1
            r[n] = -mu
            a_ub.append(r)
            b_ub.append(-1)
        off += len(t)
    # @line L6 c . bad + d >= 1
    r = row()
    for k in range(n):
        r[k] = -bad[k]
    r[n] = -1
    a_ub.append(r)
    b_ub.append(-1)
    return nvar, free, a_eq, b_eq, a_ub, b_ub


def normalize(c, d):
    """Scale c . x + d <= 0 to coprime integers."""
    vals = list(c) + [d]
    den = 1
    for v in vals:
        den = den * v.denominator // gcd(den, v.denominator)
    ints = [int(v * den) for v in vals]
    g = 0
    for v in ints:
        g = gcd(g, abs(v))
    g = g or 1
    return tuple(v // g for v in ints[:-1]), ints[-1] // g


def invariant_for(loop, bad, mus=(1, 0)):
    """An inductive inequality (c, d), meaning c . x + d <= 0, that is
    false at the point bad, or None. See the module docstring."""
    if empty(loop.init, loop.n):
        return (0,) * loop.n, 1  # Init is empty: false is inductive
    # A transition with an empty relation needs no condition: drop it.
    live = Loop(loop.n, loop.init, [t for t in loop.trans if not empty(t, 2 * loop.n)])
    # @line L1 try every choice of one case per transition
    for choice in product(cases(mus), repeat=len(live.trans)):
        nvar, free, a_eq, b_eq, a_ub, b_ub = _system(live, bad, choice)
        # @line L7 solve the linear program exactly
        sol = feasible_point(a_eq, b_eq, a_ub, b_ub, nvar, free=free)
        if sol is not None:
            return normalize(sol[: loop.n], sol[loop.n])
    # @line L8 no choice is feasible
    return None


def holds(c, d, x):
    """Whether c . x + d <= 0 at the point x."""
    return sum(ci * xi for ci, xi in zip(c, x)) + d <= 0
