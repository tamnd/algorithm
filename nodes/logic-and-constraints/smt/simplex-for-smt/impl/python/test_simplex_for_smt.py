# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplex-for-smt/. The authors are listed in prov/W3SMMR.jsonl.

import itertools
import random
from fractions import Fraction

from simplex_for_smt import GeneralSimplex, solve

OPS = ("<=", "<", ">=", ">", "=")


def holds(atom: tuple, x: list[Fraction]) -> bool:
    coeffs, op, rhs = atom
    v = sum(Fraction(a) * x[j] for j, a in coeffs.items())
    return {"<=": v <= rhs, "<": v < rhs, ">=": v >= rhs, ">": v > rhs, "=": v == rhs}[op]


def certificate_ok(n: int, atoms: list[tuple], conflict: list) -> bool:
    """Check a Farkas certificate exactly: the atoms in it cannot all hold."""
    total = [Fraction(0)] * n
    const = Fraction(0)
    strict_used = False
    for tag, mu in conflict:
        coeffs, op, rhs = atoms[tag]
        if op in ("<=", "<") and mu <= 0:
            return False
        if op in (">=", ">") and mu >= 0:
            return False
        for j, a in coeffs.items():
            total[j] += mu * a
        const -= mu * rhs  # sum of mu * e is the constant -sum(mu * rhs)
        strict_used |= op in ("<", ">")
    if any(total):
        return False
    return const > 0 or (const == 0 and strict_used)


def solve_square(rows: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction] | None:
    """Solve a square system by Gauss-Jordan elimination; None if singular."""
    k = len(rows)
    m = [list(r) + [b] for r, b in zip(rows, rhs)]
    for c in range(k):
        p = next((r for r in range(c, k) if m[r][c] != 0), None)
        if p is None:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[c])]
    return [m[r][k] / m[r][r] for r in range(k)]


def brute_feasible(n: int, atoms: list[tuple]) -> bool:
    """Feasibility by vertex enumeration of a bounded polytope in (x, t).

    Each atom becomes rows a.x <= b. A strict row becomes a.x + t <= b. With
    -1 <= t <= 1 and a box on x among the atoms, the set is a polytope. The
    atoms are feasible iff the largest t is positive, and the largest t is
    reached at a vertex: a point where n + 1 linearly independent rows are
    tight.
    """
    rows: list[tuple[list[Fraction], Fraction]] = []
    for coeffs, op, rhs in atoms:
        a = [Fraction(coeffs.get(j, 0)) for j in range(n)]
        b = Fraction(rhs)
        neg = [-v for v in a]
        if op in ("<=", "="):
            rows.append((a + [Fraction(0)], b))
        if op in (">=", "="):
            rows.append((neg + [Fraction(0)], -b))
        if op == "<":
            rows.append((a + [Fraction(1)], b))
        if op == ">":
            rows.append((neg + [Fraction(1)], -b))
    rows.append(([Fraction(0)] * n + [Fraction(1)], Fraction(1)))
    rows.append(([Fraction(0)] * n + [Fraction(-1)], Fraction(1)))
    best = None
    for sub in itertools.combinations(range(len(rows)), n + 1):
        p = solve_square([rows[r][0] for r in sub], [rows[r][1] for r in sub])
        if p is None:
            continue
        if all(sum(a * v for a, v in zip(r, p)) <= b for r, b in rows):
            best = p[n] if best is None else max(best, p[n])
    return best is not None and best > 0


def box(n: int, b: int) -> list[tuple]:
    out = []
    for j in range(n):
        out.append(({j: 1}, "<=", b))
        out.append(({j: 1}, ">=", -b))
    return out


def random_atom(rng: random.Random, n: int) -> tuple:
    while True:
        coeffs = {j: rng.randint(-3, 3) for j in range(n)}
        coeffs = {j: a for j, a in coeffs.items() if a}
        if coeffs:
            return coeffs, rng.choice(OPS), rng.randint(-6, 6)


def test_page_example() -> None:
    # x + y >= 4, x - y <= 1, x <= 1, y <= 2 is unsat; the page traces it.
    atoms = [({0: 1, 1: 1}, ">=", 4), ({0: 1, 1: -1}, "<=", 1), ({0: 1}, "<=", 1), ({1: 1}, "<=", 2)]
    ok, conflict = solve(2, atoms)
    assert not ok
    assert certificate_ok(2, atoms, conflict)
    assert sorted(t for t, _ in conflict) == [0, 2, 3]
    ok, x = solve(2, atoms[:3])
    assert ok and all(holds(a, x) for a in atoms[:3])


def test_strict_bounds() -> None:
    atoms = [({0: 1, 1: 1}, "<", 2), ({0: 1}, ">", 1), ({1: 1}, ">", 1)]
    ok, conflict = solve(2, atoms)
    assert not ok and certificate_ok(2, atoms, conflict)
    atoms = [({0: 1, 1: 1}, "<", 2), ({0: 1}, ">", 0), ({1: 1}, ">", 1)]
    ok, x = solve(2, atoms)
    assert ok and all(holds(a, x) for a in atoms)


def test_edges() -> None:
    assert solve(1, [])[0]
    ok, conflict = solve(1, [({}, ">=", 1)])
    assert not ok and certificate_ok(1, [({}, ">=", 1)], conflict)
    atoms = [({0: 2}, "=", 3), ({0: -4}, ">=", -6)]
    ok, x = solve(1, atoms)
    assert ok and x == [Fraction(3, 2)]
    atoms = [({0: 1}, "<=", 0), ({0: 1}, ">=", 1)]
    ok, conflict = solve(1, atoms)
    assert not ok and certificate_ok(1, atoms, conflict)


def test_random_against_vertices() -> None:
    rng = random.Random(2006)
    for trial in range(250):
        n = 1 if trial < 50 else (2 if trial < 200 else 3)
        m = rng.randint(1, 4 if n < 3 else 3)
        atoms = box(n, 5) + [random_atom(rng, n) for _ in range(m)]
        rng.shuffle(atoms)
        ok, out = solve(n, atoms)
        assert ok == brute_feasible(n, atoms)
        if ok:
            assert all(holds(a, out) for a in atoms)
        else:
            assert certificate_ok(n, atoms, out)


def test_incremental_push_pop() -> None:
    rng = random.Random(81)
    for _ in range(20):
        n = 2
        s = GeneralSimplex(n)
        base = box(n, 4)
        for t, (c, op, r) in enumerate(base):
            assert s.assert_atom(c, op, r, ("box", t)) is None
        made = {("box", t): a for t, a in enumerate(base)}
        stack: list[list[tuple]] = [[]]
        for step in range(12):
            if len(stack) > 1 and rng.random() < 0.3:
                s.pop()
                stack.pop()
                conflict = s.check()
            else:
                s.push()
                atom = random_atom(rng, n)
                made[("atom", step)] = atom
                stack.append(stack[-1] + [atom])
                conflict = s.assert_atom(*atom, ("atom", step))
                if conflict is None:
                    conflict = s.check()
            current = base + stack[-1]
            assert (conflict is None) == brute_feasible(n, current)
            if conflict is None:
                assert all(holds(a, s.model()) for a in current)
            else:
                assert certificate_ok(n, made, conflict)
                assert all(made[t] in current for t, _ in conflict)
                s.pop()  # as DPLL(T) does: undo the last atom after a conflict
                stack.pop()


def test_incremental_certificates() -> None:
    rng = random.Random(7)
    for _ in range(30):
        n = 2
        s = GeneralSimplex(n)
        atoms = box(n, 4)
        for t, a in enumerate(atoms):
            s.assert_atom(*a, t)
        for _ in range(6):
            s.push()
            a = random_atom(rng, n)
            atoms.append(a)
            conflict = s.assert_atom(*a, len(atoms) - 1)
            if conflict is None:
                conflict = s.check()
            if conflict is None:
                assert brute_feasible(n, atoms)
                assert all(holds(b, s.model()) for b in atoms)
            else:
                assert not brute_feasible(n, atoms)
                assert certificate_ok(n, atoms, conflict)
                s.pop()
                atoms.pop()
