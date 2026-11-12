# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-minimal-optimization/. The authors are listed in prov/9XT69N.jsonl.

"""Platt's sequential minimal optimization (SMO) for the soft margin SVM dual.

The dual problem is

    maximize   W(a) = sum_i a_i - 1/2 sum_ij a_i a_j y_i y_j K_ij
    subject to 0 <= a_i <= C and sum_i a_i y_i = 0.

The decision function is f(x) = sum_j a_j y_j k(x_j, x) + b. Platt writes
u = w . x - b, so his threshold is the negative of b here. E_i = f(x_i) - y_i.

This follows Platt (1998): the outer loop alternates one pass over all
examples with passes over the non-bound examples; the second multiplier is
chosen by the largest |E1 - E2|, then from the non-bound examples from a
random start, then from all examples from a random start; the two-variable
step is analytic, with clipping to [L, H]; eta <= 0 is handled by comparing
the objective at the two ends. The errors are cached for all examples and
updated after each step.

The step threshold eps (line L21) defaults to 1e-8. With eps = 1e-3, steps
smaller than about 0.1 % of the multipliers are refused, and the run can end
with KKT violations well above tol.
"""

import random
from fractions import Fraction
from itertools import product
from typing import Optional, Sequence


class SMO:
    def __init__(
        self,
        k: Sequence[Sequence[float]],
        y: Sequence[int],
        c: float,
        tol: float = 1e-3,
        eps: float = 1e-8,
        rng: Optional[random.Random] = None,
    ) -> None:
        self.k, self.y, self.c, self.tol, self.eps = k, list(y), c, tol, eps
        self.n = len(y)
        self.rng = rng or random.Random(0)
        self.alpha = [0.0] * self.n  # @line L1
        self.b = 0.0
        self.err = [-float(v) for v in y]  # f = 0 at the start, so E_i = -y_i
        self.steps = 0

    def _bound(self, i: int) -> bool:
        return self.alpha[i] <= 0.0 or self.alpha[i] >= self.c

    def run(self, max_passes: int = 10000) -> tuple[list[float], float]:
        changed, examine_all, passes = 0, True, 0  # @line L2
        while (changed > 0 or examine_all) and passes < max_passes:  # @line L3
            passes += 1
            changed = 0  # @line L4
            idx = range(self.n) if examine_all else [i for i in range(self.n) if not self._bound(i)]  # @line L5
            for i in idx:
                changed += self.examine(i)  # @line L6
            if examine_all:  # @line L7
                examine_all = False
            elif changed == 0:
                examine_all = True
        return self.alpha, self.b  # @line L8

    def examine(self, i2: int) -> int:
        y2, a2, e2 = self.y[i2], self.alpha[i2], self.err[i2]
        r2 = e2 * y2  # @line L9  (r2 = y2 f(x2) - 1)
        if (r2 < -self.tol and a2 < self.c) or (r2 > self.tol and a2 > 0):  # @line L10
            free = [i for i in range(self.n) if not self._bound(i)]
            if len(free) > 1:  # @line L11 (second choice heuristic)
                i1 = max(free, key=lambda i: abs(self.err[i] - e2))
                if self.take_step(i1, i2):
                    return 1
            if free:  # @line L12
                start = self.rng.randrange(len(free))
                for t in range(len(free)):
                    if self.take_step(free[(start + t) % len(free)], i2):
                        return 1
            start = self.rng.randrange(self.n)  # @line L13
            for t in range(self.n):
                if self.take_step((start + t) % self.n, i2):
                    return 1
        return 0  # @line L14

    def _pair_objective(self, i1: int, i2: int, a1: float, a2: float) -> float:
        """W restricted to (a1, a2), up to a constant, with the other alphas fixed."""
        k, y = self.k, self.y
        # v_i = sum over j not in {i1, i2} of a_j y_j K_ij
        v1 = self.err[i1] + y[i1] - self.b - y[i1] * self.alpha[i1] * k[i1][i1] - y[i2] * self.alpha[i2] * k[i1][i2]
        v2 = self.err[i2] + y[i2] - self.b - y[i1] * self.alpha[i1] * k[i1][i2] - y[i2] * self.alpha[i2] * k[i2][i2]
        s = y[i1] * y[i2]
        return (
            a1
            + a2
            - 0.5 * k[i1][i1] * a1 * a1
            - 0.5 * k[i2][i2] * a2 * a2
            - s * k[i1][i2] * a1 * a2
            - y[i1] * a1 * v1
            - y[i2] * a2 * v2
        )

    def take_step(self, i1: int, i2: int) -> bool:
        if i1 == i2:  # @line L15
            return False
        k, c = self.k, self.c
        y1, y2 = self.y[i1], self.y[i2]
        alph1, alph2 = self.alpha[i1], self.alpha[i2]
        e1, e2 = self.err[i1], self.err[i2]
        s = y1 * y2
        if y1 != y2:  # @line L16
            lo, hi = max(0.0, alph2 - alph1), min(c, c + alph2 - alph1)
        else:
            lo, hi = max(0.0, alph1 + alph2 - c), min(c, alph1 + alph2)
        if lo >= hi:  # @line L17
            return False
        k11, k12, k22 = k[i1][i1], k[i1][i2], k[i2][i2]
        eta = k11 + k22 - 2 * k12  # @line L18
        if eta > 0:  # @line L19
            a2 = alph2 + y2 * (e1 - e2) / eta
            a2 = lo if a2 < lo else hi if a2 > hi else a2
        else:  # @line L20
            obj_lo = self._pair_objective(i1, i2, alph1 + s * (alph2 - lo), lo)
            obj_hi = self._pair_objective(i1, i2, alph1 + s * (alph2 - hi), hi)
            if obj_lo > obj_hi + self.eps:
                a2 = lo
            elif obj_lo < obj_hi - self.eps:
                a2 = hi
            else:
                a2 = alph2
        if abs(a2 - alph2) < self.eps * (a2 + alph2 + self.eps):  # @line L21
            return False
        a1 = alph1 + s * (alph2 - a2)  # @line L22
        # Guard against rounding: snap values within 1e-12 C of a bound onto it.
        a1 = 0.0 if a1 < 1e-12 * c else c if a1 > c * (1 - 1e-12) else a1
        d1, d2 = y1 * (a1 - alph1), y2 * (a2 - alph2)
        b1 = self.b - e1 - d1 * k11 - d2 * k12  # @line L23
        b2 = self.b - e2 - d1 * k12 - d2 * k22
        if 0 < a1 < c:
            b_new = b1
        elif 0 < a2 < c:
            b_new = b2
        else:
            b_new = (b1 + b2) / 2
        db = b_new - self.b
        for i in range(self.n):  # @line L24
            self.err[i] += d1 * k[i1][i] + d2 * k[i2][i] + db
        self.alpha[i1], self.alpha[i2], self.b = a1, a2, b_new
        self.steps += 1
        return True  # @line L25


def smo(k, y, c, tol=1e-3, eps=1e-8, rng=None):
    """Run SMO and return (alpha, b)."""
    s = SMO(k, y, c, tol, eps, rng)
    return s.run()


# ----- checks ----------------------------------------------------------------


def decision_values(k, y, alpha, b) -> list[float]:
    n = len(y)
    return [sum(alpha[j] * y[j] * k[j][i] for j in range(n)) + b for i in range(n)]


def kkt_violation(k, y, alpha, b, c) -> float:
    """The largest violation of the KKT conditions of the soft margin dual."""
    worst = abs(sum(a * t for a, t in zip(alpha, y)))
    for a, t, f in zip(alpha, y, decision_values(k, y, alpha, b)):
        m = t * f
        worst = max(worst, -a, a - c)
        if a <= 1e-12:
            worst = max(worst, 1 - m)
        elif a >= c - 1e-12:
            worst = max(worst, m - 1)
        else:
            worst = max(worst, abs(m - 1))
    return worst


def dual_objective(k, y, alpha) -> float:
    n = len(y)
    return sum(alpha) - 0.5 * sum(alpha[i] * alpha[j] * y[i] * y[j] * k[i][j] for i in range(n) for j in range(n))


def _solve_exact(a: list[list[Fraction]], rhs: list[Fraction]) -> Optional[list[Fraction]]:
    n = len(a)
    m = [row[:] + [r] for row, r in zip(a, rhs)]
    for col in range(n):
        p = next((r for r in range(col, n) if m[r][col] != 0), None)
        if p is None:
            return None
        m[col], m[p] = m[p], m[col]
        m[col] = [v / m[col][col] for v in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [u - f * v for u, v in zip(m[r], m[col])]
    return [m[i][n] for i in range(n)]


def exact_svm_dual(k, y, c) -> Optional[tuple[list[Fraction], Fraction]]:
    """Solve the dual exactly by enumerating which multipliers are 0, free or C.

    For each split (Z, F, U) with F nonempty, solve the linear KKT system
    y_i f(x_i) = 1 for i in F and sum_i a_i y_i = 0 in the unknowns a_F and b,
    then check 0 < a_F < C and the sign conditions on Z and U. A point that
    satisfies the KKT conditions is optimal because the problem is convex.
    For tiny n only: there are 3^n splits.
    """
    n = len(y)
    kk = [[Fraction(v) for v in row] for row in k]
    cc = Fraction(c)
    for split in product((0, 1, 2), repeat=n):  # 0: a = 0, 1: free, 2: a = C
        free = [i for i in range(n) if split[i] == 1]
        if not free:
            continue
        upper = [i for i in range(n) if split[i] == 2]
        m = len(free)
        rows, rhs = [], []
        for i in free:  # y_i (sum_j a_j y_j K_ij + b) = 1
            rows.append([y[i] * y[j] * kk[i][j] for j in free] + [Fraction(y[i])])
            rhs.append(1 - y[i] * sum(cc * y[j] * kk[i][j] for j in upper))
        rows.append([Fraction(y[j]) for j in free] + [Fraction(0)])
        rhs.append(-sum(cc * y[j] for j in upper))
        sol = _solve_exact(rows, rhs)
        if sol is None:
            continue
        alpha = [Fraction(0)] * n
        for t, i in enumerate(free):
            alpha[i] = sol[t]
        for i in upper:
            alpha[i] = cc
        b = sol[m]
        if any(not (0 < alpha[i] < cc) for i in free):
            continue
        ok = True
        for i in range(n):
            mi = y[i] * (sum(alpha[j] * y[j] * kk[i][j] for j in range(n)) + b)
            if split[i] == 0 and mi < 1 or split[i] == 2 and mi > 1:
                ok = False
                break
        if ok:
            return alpha, b
    return None
