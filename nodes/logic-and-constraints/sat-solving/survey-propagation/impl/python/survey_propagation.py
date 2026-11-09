# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/survey-propagation/. The authors are listed in prov/VFSYED.jsonl.

"""Survey propagation with decimation (Mezard, Parisi and Zecchina 2002;
Braunstein, Mezard and Zecchina 2005), followed by WalkSAT.

Clauses are DIMACS-style lists of nonzero ints over the variables 1 .. n.
This is a heuristic: it returns a model or None, and None proves nothing.
Every returned assignment is checked against all clauses.
"""

import random


class Contradiction(Exception):
    """A variable receives warnings from clauses of both signs."""


def simplify(clauses: list[list[int]], fixed: dict[int, bool]) -> list[list[int]] | None:
    """Apply the fixed values and unit propagation. None on an empty clause.

    fixed is extended in place with the values forced by unit clauses.
    """
    cls = [sorted(set(c)) for c in clauses]
    cls = [c for c in cls if not any(-l in c for l in c)]
    while True:
        out = []
        unit = None
        for c in cls:
            if any(fixed.get(abs(l)) == (l > 0) for l in c):
                continue  # satisfied
            c = [l for l in c if abs(l) not in fixed]
            if not c:
                return None
            if len(c) == 1 and unit is None:
                unit = c[0]
            out.append(c)
        if unit is None:
            return out
        fixed[abs(unit)] = unit > 0
        cls = out


def sp_update(clauses: list[list[int]], occ: dict[int, list[tuple[int, int, int]]], eta: list[list[float]], a: int) -> float:
    """Recompute the surveys of clause a in place. Return the largest change."""
    lits = clauses[a]
    ratio = []
    for lit in lits:
        j = abs(lit)
        ps = pu = 1.0  # products of (1 - eta) over the other clauses of j, same sign and opposite sign
        for b, r, l2 in occ[j]:
            if b == a:
                continue
            if (l2 > 0) == (lit > 0):
                ps *= 1.0 - eta[b][r]
            else:
                pu *= 1.0 - eta[b][r]
        pi_u = (1.0 - pu) * ps  # j is forced to violate a
        pi_s = (1.0 - ps) * pu  # j is forced to satisfy a
        pi_0 = ps * pu  # j is free
        den = pi_u + pi_s + pi_0
        if den <= 0.0:
            raise Contradiction
        ratio.append(pi_u / den)
    change = 0.0
    for q in range(len(lits)):
        new = 1.0
        for q2, x in enumerate(ratio):
            if q2 != q:
                new *= x
        change = max(change, abs(new - eta[a][q]))
        eta[a][q] = new
    return change


def survey_propagation(clauses: list[list[int]], rng: random.Random, eps: float = 1e-3, max_sweeps: int = 1000) -> list[list[float]] | None:
    """Iterate the SP equations to a fixed point. None if they do not converge."""
    occ: dict[int, list[tuple[int, int, int]]] = {}
    for a, c in enumerate(clauses):
        for q, lit in enumerate(c):
            occ.setdefault(abs(lit), []).append((a, q, lit))
    eta = [[rng.random() for _ in c] for c in clauses]
    order = list(range(len(clauses)))
    for _ in range(max_sweeps):
        rng.shuffle(order)
        change = 0.0
        for a in order:
            change = max(change, sp_update(clauses, occ, eta, a))
        if change < eps:
            return eta
    return None


def biases(clauses: list[list[int]], eta: list[list[float]]) -> dict[int, tuple[float, float, float]]:
    """W+(i), W-(i) and W0(i) for each variable i of the formula."""
    pp: dict[int, float] = {}
    pm: dict[int, float] = {}
    for a, c in enumerate(clauses):
        for q, lit in enumerate(c):
            d = pp if lit > 0 else pm
            d[abs(lit)] = d.get(abs(lit), 1.0) * (1.0 - eta[a][q])
    out = {}
    for i in set(pp) | set(pm):
        p, m = pp.get(i, 1.0), pm.get(i, 1.0)
        plus, minus, zero = (1.0 - p) * m, (1.0 - m) * p, p * m
        den = plus + minus + zero
        if den <= 0.0:
            raise Contradiction
        out[i] = (plus / den, minus / den, zero / den)
    return out


def walksat(n: int, clauses: list[list[int]], x: list[bool], rng: random.Random, p: float = 0.5, max_flips: int = 100000) -> list[bool] | None:
    """A plain WalkSAT (SKC rule) from the start x, used for the last phase."""
    x = [False] + x
    occ: list[list[int]] = [[] for _ in range(n + 1)]
    for j, c in enumerate(clauses):
        for lit in c:
            occ[abs(lit)].append(j)
    tc = [sum(x[abs(l)] == (l > 0) for l in c) for c in clauses]
    for _ in range(max_flips):
        false = [j for j, t in enumerate(tc) if t == 0]
        if not false:
            return x[1:]
        c = clauses[rng.choice(false)]

        def brk(v: int) -> int:
            return sum(1 for j in occ[v] if tc[j] == 1 and any(abs(l) == v and x[v] == (l > 0) for l in clauses[j]))

        bs = [(brk(abs(l)), abs(l)) for l in c]
        free = [v for b, v in bs if b == 0]
        if free:
            v = rng.choice(free)
        elif rng.random() < p:
            v = abs(rng.choice(c))
        else:
            least = min(b for b, _ in bs)
            v = rng.choice([v for b, v in bs if b == least])
        x[v] = not x[v]
        for j in occ[v]:
            tc[j] = sum(x[abs(l)] == (l > 0) for l in clauses[j])
    return None


def sp_decimation(n: int, clauses: list[list[int]], rng: random.Random | None = None, fraction: float = 0.05, delta: float = 1e-2, max_flips: int = 100000) -> list[bool] | None:
    """Return a model as a list of n booleans (x[v - 1] is the value of v), or None.

    Each round fixes a fraction of the free variables, those with the largest |W+ - W-|.
    """
    rng = rng or random.Random()
    fixed: dict[int, bool] = {}
    cur = simplify(clauses, fixed)
    if cur is None:
        return None
    while cur:  # @line L1
        try:
            eta = survey_propagation(cur, rng)  # @line L2
            if eta is None:
                return None  # @line L3
            if max(max(e) for e in eta) < delta:  # @line L4
                break
            w = biases(cur, eta)  # @line L5
        except Contradiction:
            return None
        ranked = sorted(w, key=lambda i: -abs(w[i][0] - w[i][1]))
        for i in ranked[: max(1, int(fraction * len(ranked)))]:  # @line L6
            fixed[i] = w[i][0] > w[i][1]
        cur = simplify(cur, fixed)  # @line L7
        if cur is None:
            return None  # @line L8
    start = [fixed.get(v, rng.random() < 0.5) for v in range(1, n + 1)]
    free = {abs(l) for c in cur for l in c}
    rest = walksat(n, cur, start, rng, max_flips=max_flips) if cur else start  # @line L9
    if rest is None:
        return None
    x = [rest[v - 1] if v in free else start[v - 1] for v in range(1, n + 1)]
    ok = all(any(x[abs(l) - 1] == (l > 0) for l in c) for c in clauses)
    return x if ok else None  # @line L10
