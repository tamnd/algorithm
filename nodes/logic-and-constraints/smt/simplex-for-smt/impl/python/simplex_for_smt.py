# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simplex-for-smt/. The authors are listed in prov/W3SMMR.jsonl.

"""The general simplex of Dutertre and de Moura (2006) for linear real arithmetic.

The solver keeps a tableau: each basic variable is a linear combination of the
nonbasic variables. Each variable can have a lower and an upper bound. Atoms
such as 2x + 3y <= 7 are turned into bounds on slack variables, so the tableau
is built once and only the bounds change. Strict bounds use delta-rationals:
a pair (c, k) stands for c + k*delta, where delta is a positive infinitesimal,
and pairs compare lexicographically.

An atom is (coeffs, op, rhs): coeffs maps a variable index 0 .. n-1 to a
nonzero number, op is one of "<=", "<", ">=", ">", "=", and rhs is a number.
All arithmetic is exact, with fractions.Fraction.
"""

from fractions import Fraction
from typing import Hashable

DR = tuple[Fraction, Fraction]  # (c, k) is c + k * delta
ZERO: DR = (Fraction(0), Fraction(0))


def dr_add(a: DR, b: DR) -> DR:
    return (a[0] + b[0], a[1] + b[1])


def dr_sub(a: DR, b: DR) -> DR:
    return (a[0] - b[0], a[1] - b[1])


def dr_scale(q: Fraction, a: DR) -> DR:
    return (q * a[0], q * a[1])


class Bound:
    """A bound x <= value or x >= value, the atom that caused it, and the scale.

    The atom said scale * x op rhs, so value = rhs / scale (with the delta part
    for a strict atom). A slack variable has scale 1.
    """

    __slots__ = ("value", "tag", "scale")

    def __init__(self, value: DR, tag: Hashable, scale: Fraction) -> None:
        self.value, self.tag, self.scale = value, tag, scale


class GeneralSimplex:
    """Incremental feasibility check of linear atoms over the reals.

    Use assert_atom to add atoms, check to decide them, and push and pop to
    backtrack. A conflict is a Farkas certificate: a list of (tag, mu) pairs.
    Each atom gives the term e = coeffs . x - rhs with e <= 0, e < 0, e >= 0,
    e > 0 or e = 0. The sum of mu * e has all variable coefficients 0, and
    mu > 0 for <= and <, mu < 0 for >= and >, so the atoms cannot all hold.
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.nvars = n
        self.rows: dict[int, dict[int, Fraction]] = {}  # basic var -> row
        self.lower: list[Bound | None] = [None] * n
        self.upper: list[Bound | None] = [None] * n
        self.beta: list[DR] = [ZERO] * n
        self.slack_of: dict[tuple, int] = {}
        self.trail: list[tuple[int, bool, Bound | None]] = []
        self.marks: list[int] = []
        self.pivots = 0

    # ------------------------------------------------------------ tableau

    def _slack(self, coeffs: dict[int, Fraction]) -> int:
        """Return the slack variable s = coeffs . x, and make it if it is new."""
        key = tuple(sorted(coeffs.items()))
        if key in self.slack_of:
            return self.slack_of[key]
        s = self.nvars
        self.nvars += 1
        row: dict[int, Fraction] = {}
        for j, a in coeffs.items():  # write the row over nonbasic variables
            if j in self.rows:
                for k, b in self.rows[j].items():
                    row[k] = row.get(k, Fraction(0)) + a * b
            else:
                row[j] = row.get(j, Fraction(0)) + a
        self.rows[s] = {k: v for k, v in row.items() if v != 0}
        self.lower.append(None)
        self.upper.append(None)
        val = ZERO
        for k, a in self.rows[s].items():
            val = dr_add(val, dr_scale(a, self.beta[k]))
        self.beta.append(val)
        self.slack_of[key] = s
        return s

    def _update(self, j: int, v: DR) -> None:
        """Set the nonbasic variable j to v and fix the basic variables."""
        diff = dr_sub(v, self.beta[j])
        for k, row in self.rows.items():  # @line L17
            a = row.get(j)
            if a:
                self.beta[k] = dr_add(self.beta[k], dr_scale(a, diff))
        self.beta[j] = v  # @line L18

    def _pivot_and_update(self, i: int, j: int, v: DR) -> None:
        """Make the basic i nonbasic with value v, and the nonbasic j basic."""
        a_ij = self.rows[i][j]
        theta = dr_scale(1 / a_ij, dr_sub(v, self.beta[i]))  # @line L19
        self.beta[i] = v  # @line L20
        self.beta[j] = dr_add(self.beta[j], theta)
        for k, row in self.rows.items():  # @line L21
            if k != i and j in row:
                self.beta[k] = dr_add(self.beta[k], dr_scale(row[j], theta))
        self._pivot(i, j)  # @line L22

    def _pivot(self, i: int, j: int) -> None:
        self.pivots += 1
        row_i = self.rows.pop(i)
        a_ij = row_i.pop(j)
        new_row = {k: -a / a_ij for k, a in row_i.items()}  # x_j = ...
        new_row[i] = 1 / a_ij
        for k, row in self.rows.items():
            c = row.pop(j, None)
            if c is None:
                continue
            for m, b in new_row.items():
                val = row.get(m, Fraction(0)) + c * b
                if val:
                    row[m] = val
                else:
                    row.pop(m, None)
        self.rows[j] = new_row

    # ------------------------------------------------------------ bounds

    def _set(self, x: int, is_upper: bool, b: Bound) -> None:
        old = self.upper[x] if is_upper else self.lower[x]
        self.trail.append((x, is_upper, old))
        if is_upper:
            self.upper[x] = b
        else:
            self.lower[x] = b

    def _assert_upper(self, x: int, b: Bound) -> list | None:
        u, lo = self.upper[x], self.lower[x]
        if u is not None and b.value >= u.value:  # @line L12
            return None
        if lo is not None and b.value < lo.value:  # @line L13
            return self._explain([(x, True, Fraction(1), b), (x, False, Fraction(1), lo)])
        self._set(x, True, b)  # @line L14
        if x not in self.rows and self.beta[x] > b.value:  # @line L15
            self._update(x, b.value)
        return None  # @line L16

    def _assert_lower(self, x: int, b: Bound) -> list | None:
        u, lo = self.upper[x], self.lower[x]
        if lo is not None and b.value <= lo.value:
            return None
        if u is not None and b.value > u.value:
            return self._explain([(x, False, Fraction(1), b), (x, True, Fraction(1), u)])
        self._set(x, False, b)
        if x not in self.rows and self.beta[x] < b.value:
            self._update(x, b.value)
        return None

    def assert_atom(self, coeffs: dict[int, int | Fraction], op: str, rhs: int | Fraction, tag: Hashable) -> list | None:
        """Add the atom coeffs . x op rhs. Return a conflict, or None."""
        cs = {j: Fraction(a) for j, a in coeffs.items() if a != 0}
        rhs = Fraction(rhs)
        if not cs:
            holds = {"<=": 0 <= rhs, "<": 0 < rhs, ">=": 0 >= rhs, ">": 0 > rhs, "=": rhs == 0}[op]
            if holds:
                return None
            sign = {"<=": 1, "<": 1, ">=": -1, ">": -1, "=": -1 if rhs > 0 else 1}[op]
            return [(tag, Fraction(sign))]
        if len(cs) == 1:
            (x, scale), = cs.items()
        else:
            x, scale = self._slack(cs), Fraction(1)
        c = rhs / scale
        if scale < 0:  # dividing by a negative number flips the relation
            op = {"<=": ">=", "<": ">", ">=": "<=", ">": "<", "=": "="}[op]
        strict = {"<": Fraction(-1), ">": Fraction(1)}.get(op, Fraction(0))
        b = Bound((c, strict), tag, scale)
        if op in ("<=", "<", "="):
            conflict = self._assert_upper(x, b)
            if conflict is not None or op != "=":
                return conflict
        return self._assert_lower(x, b)

    def push(self) -> None:
        self.marks.append(len(self.trail))

    def pop(self) -> None:
        """Undo the bounds since the last push. The assignment stays valid."""
        mark = self.marks.pop()
        while len(self.trail) > mark:
            x, is_upper, old = self.trail.pop()
            if is_upper:
                self.upper[x] = old
            else:
                self.lower[x] = old

    # ------------------------------------------------------------ check

    def _violated(self, i: int) -> bool:
        lo, u = self.lower[i], self.upper[i]
        return (lo is not None and self.beta[i] < lo.value) or (u is not None and self.beta[i] > u.value)

    def _can_increase(self, j: int) -> bool:
        return self.upper[j] is None or self.beta[j] < self.upper[j].value

    def _can_decrease(self, j: int) -> bool:
        return self.lower[j] is None or self.beta[j] > self.lower[j].value

    def check(self) -> list | None:
        """Decide the asserted atoms. Return None (sat) or a Farkas conflict."""
        while True:  # @line L1
            basics = [i for i in sorted(self.rows) if self._violated(i)]  # @line L2
            if not basics:  # @line L3
                return None
            i = basics[0]
            row = self.rows[i]
            lo = self.lower[i]
            if lo is not None and self.beta[i] < lo.value:  # @line L4
                cand = [j for j in sorted(row) if (row[j] > 0 and self._can_increase(j)) or (row[j] < 0 and self._can_decrease(j))]  # @line L5
                if not cand:  # @line L6
                    parts = [(i, False, Fraction(1), lo)]
                    for j, a in row.items():
                        parts.append((j, True, a, self.upper[j]) if a > 0 else (j, False, -a, self.lower[j]))
                    return self._explain(parts)
                self._pivot_and_update(i, cand[0], lo.value)  # @line L7
            else:  # @line L8
                u = self.upper[i]
                cand = [j for j in sorted(row) if (row[j] < 0 and self._can_increase(j)) or (row[j] > 0 and self._can_decrease(j))]  # @line L9
                if not cand:  # @line L10
                    parts = [(i, True, Fraction(1), u)]
                    for j, a in row.items():
                        parts.append((j, False, a, self.lower[j]) if a > 0 else (j, True, -a, self.upper[j]))
                    return self._explain(parts)
                self._pivot_and_update(i, cand[0], u.value)  # @line L11

    def _explain(self, parts: list) -> list:
        """Turn bounds with multipliers lambda into (tag, mu) on the atoms.

        An upper bound x <= c with multiplier lambda adds lambda (x - c) <= 0.
        The atom was scale * x op rhs, so this is (lambda / scale) * e.
        A lower bound adds lambda (c - x) <= 0, which is (-lambda / scale) * e.
        """
        mu: dict = {}
        for _x, is_upper, lam, b in parts:
            m = lam / b.scale if is_upper else -lam / b.scale
            mu[b.tag] = mu.get(b.tag, Fraction(0)) + m
        return [(t, m) for t, m in mu.items() if m != 0]

    # ------------------------------------------------------------ model

    def model(self) -> list[Fraction]:
        """A rational model of the original variables, after check gave None.

        Pick a rational delta0 > 0 small enough that each bound still holds
        when delta is replaced by delta0 (Dutertre and de Moura, Section 3.3).
        """
        delta = Fraction(1)
        for x in range(self.nvars):
            v = self.beta[x]
            for b, below in ((self.lower[x], True), (self.upper[x], False)):
                if b is None:
                    continue
                lo, hi = (b.value, v) if below else (v, b.value)
                if lo[0] < hi[0] and lo[1] > hi[1]:
                    delta = min(delta, (hi[0] - lo[0]) / (lo[1] - hi[1]))
        return [self.beta[x][0] + self.beta[x][1] * delta for x in range(self.n)]


def solve(n: int, atoms: list[tuple[dict, str, int | Fraction]]) -> tuple[bool, object]:
    """Decide a conjunction of atoms. Return (True, model) or (False, conflict).

    The tags of the conflict are the positions of the atoms in the list.
    """
    s = GeneralSimplex(n)
    for t, (coeffs, op, rhs) in enumerate(atoms):
        conflict = s.assert_atom(coeffs, op, rhs, t)
        if conflict is not None:
            return False, conflict
    conflict = s.check()
    if conflict is not None:
        return False, conflict
    return True, s.model()
