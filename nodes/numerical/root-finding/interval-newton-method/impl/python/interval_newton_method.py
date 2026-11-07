# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-newton-method/. The authors are listed in prov/MES2VT.jsonl.

"""The interval Newton method: verified enclosures of all zeros of f in [a, b].

f and its derivative df are written with ordinary operators, so that called
on an Interval they return an enclosure of the range (their natural interval
extension). Interval arithmetic here rounds outward by one ulp after every
operation with math.nextafter: round to nearest is off by at most half an ulp,
so the result encloses the exact one. iexp assumes math.exp is accurate to
within one ulp, which holds for common C libraries but is not guaranteed by
IEEE 754.

The Newton operator is N(X) = m - f([m]) / f'(X) with m the midpoint. Every
zero of f in X lies in N(X); if 0 is not in f'(X) and N(X) is inside X, then
X holds exactly one zero.
"""

import math
from collections import namedtuple

INF = math.inf
Box = namedtuple("Box", "lo hi status")  # status: "unique" or "possible"
NewtonResult = namedtuple("NewtonResult", "boxes evals iterations status")


def _dn(x):
    return math.nextafter(x, -INF)


def _up(x):
    return math.nextafter(x, INF)


class Interval:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        hi = lo if hi is None else hi
        if math.isnan(lo) or math.isnan(hi) or lo > hi:
            raise ValueError("invalid interval")
        self.lo, self.hi = float(lo), float(hi)

    @staticmethod
    def _c(x):
        return x if isinstance(x, Interval) else Interval(x)

    def __add__(self, o):
        o = Interval._c(o)
        return Interval(_dn(self.lo + o.lo), _up(self.hi + o.hi))

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, o):
        return self + (-Interval._c(o))

    def __rsub__(self, o):
        return Interval._c(o) + (-self)

    def __mul__(self, o):
        o = Interval._c(o)
        p = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return Interval(_dn(min(p)), _up(max(p)))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = Interval._c(o)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError("divisor interval contains 0")
        q = [self.lo / o.lo, self.lo / o.hi, self.hi / o.lo, self.hi / o.hi]
        return Interval(_dn(min(q)), _up(max(q)))

    def __rtruediv__(self, o):
        return Interval._c(o) / self

    def __pow__(self, k):
        if not isinstance(k, int) or k < 0:
            raise ValueError("only nonnegative integer powers")
        if k == 0:
            return Interval(1.0)
        r = self
        for _ in range(k - 1):
            r = r * self
        if k % 2 == 0 and self.lo < 0 < self.hi:
            r = Interval(0.0, r.hi)  # an even power is nonnegative
        elif k % 2 == 0:
            r = Interval(max(r.lo, 0.0), r.hi)
        return r

    def contains(self, x):
        return self.lo <= x <= self.hi

    def width(self):
        return self.hi - self.lo

    def __repr__(self):
        return f"Interval({self.lo!r}, {self.hi!r})"


def iexp(x):
    if isinstance(x, Interval):
        return Interval(max(0.0, _dn(_dn(math.exp(x.lo)))), _up(_up(math.exp(x.hi))))
    return math.exp(x)


def newton_operator(f, df, X):
    """N(X) intersected with X: a list of 0, 1 or 2 intervals, and a flag that
    says whether X was proved to hold exactly one zero."""
    m = 0.5 * X.lo + 0.5 * X.hi
    fm = f(Interval(m))
    D = df(X)
    if not (D.lo <= 0 <= D.hi):
        q = fm / D
        N = Interval(_dn(m - q.hi), _up(m - q.lo))
        lo, hi = max(N.lo, X.lo), min(N.hi, X.hi)
        unique = X.lo <= N.lo and N.hi <= X.hi
        return ([Interval(lo, hi)] if lo <= hi else []), unique
    if fm.lo <= 0 <= fm.hi:
        return [X], False  # no information: N(X) is the whole line
    # extended division: fm / D with 0 in D gives at most two half-lines
    pieces = []
    if fm.lo > 0:
        u = fm.lo
        if D.hi > 0:  # q >= u / D.hi, so m - q <= m - u / D.hi
            pieces.append((-INF, _up(m - _dn(u / D.hi))))
        if D.lo < 0:  # q <= u / D.lo, so m - q >= m - u / D.lo
            pieces.append((_dn(m - _up(u / D.lo)), INF))
    else:
        v = fm.hi
        if D.hi > 0:  # q <= v / D.hi
            pieces.append((_dn(m - _up(v / D.hi)), INF))
        if D.lo < 0:  # q >= v / D.lo
            pieces.append((-INF, _up(m - _dn(v / D.lo))))
    out = []
    for a, b in pieces:
        lo, hi = max(a, X.lo), min(b, X.hi)
        if lo <= hi:
            out.append(Interval(lo, hi))
    out.sort(key=lambda I: I.lo)
    return out, False


def interval_newton(f, df, a, b, tol=1e-12, max_iter=10000):
    if not (math.isfinite(a) and math.isfinite(b)) or a > b:
        raise ValueError("need a finite interval a <= b")
    stack, found = [Interval(a, b)], []  # @line L1
    evals = it = 0
    while stack:  # @line L2
        if it >= max_iter:  # @line L11
            rest = [Box(X.lo, X.hi, "possible") for X in stack]
            return NewtonResult(_merge(f, df, found + rest), evals, it, "max-iter")
        it += 1
        X = stack.pop()  # @line L3
        evals += 1
        if not f(X).contains(0.0):  # @line L4
            continue
        pieces, unique = newton_operator(f, df, X)  # @line L5
        evals += 2
        mid = 0.5 * X.lo + 0.5 * X.hi
        small = (X.width() <= tol * max(1.0, abs(X.lo), abs(X.hi))
                 or not X.lo < mid < X.hi)  # cannot be split any more
        if unique:  # @line L6
            Y = pieces[0]
            if small or Y.width() >= X.width():  # @line L7
                found.append(Box(Y.lo, Y.hi, "unique"))
            else:
                stack.append(Y)
        elif small:  # @line L8
            found.append(Box(X.lo, X.hi, "possible"))
        elif len(pieces) == 1 and pieces[0].width() <= 0.5 * X.width():  # @line L9
            stack.append(pieces[0])
        else:
            for Y in pieces:  # @line L10
                c = 0.5 * Y.lo + 0.5 * Y.hi
                if Y.width() > 0.5 * X.width() and Y.lo < c < Y.hi:
                    stack.extend([Interval(c, Y.hi), Interval(Y.lo, c)])
                else:
                    stack.append(Y)
    return NewtonResult(_merge(f, df, found), evals, it, "done")  # @line L12


def _verify(f, df, lo, hi):
    """Try to prove that [lo, hi], or a slightly inflated box around it, holds
    exactly one zero (a zero on the edge of a box cannot be verified without
    inflation). Returns (lo, hi, status)."""
    w = hi - lo
    inflated = Interval(_dn(_dn(lo - w)), _up(_up(hi + w)))
    for Z in (Interval(lo, hi), inflated):
        for _ in range(4):
            pieces, unique = newton_operator(f, df, Z)
            if unique:
                return pieces[0].lo, pieces[0].hi, "unique"
            if len(pieces) != 1 or pieces[0].width() >= Z.width():
                break
            Z = pieces[0]
    return lo, hi, "possible"


def _merge(f, df, boxes):
    """Join overlapping boxes (a zero on a split point lands in two boxes) and
    check each union for a unique zero with a few Newton tests."""
    boxes = sorted(boxes, key=lambda B: B.lo)
    joined = []
    for B in boxes:
        if joined and B.lo <= joined[-1][1]:
            lo, hi, k = joined.pop()
            joined.append((lo, max(hi, B.hi), k + 1))
        else:
            joined.append((B.lo, B.hi, 1))
    return [Box(*_verify(f, df, lo, hi)) for lo, hi, _ in joined]
