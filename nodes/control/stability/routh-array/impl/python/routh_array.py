# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/routh-array/. The authors are listed in prov/43YJD3.jsonl.

"""The Routh array of a real polynomial, in exact arithmetic.

A polynomial is a list of coefficients, highest power first:
[a0, a1, ..., an] is a0 s^n + a1 s^(n-1) + ... + an. The entries may be
int, Fraction or float; floats are converted exactly to Fraction.

Two special cases are handled as on the page:
- a zero first entry in a row that is not all zero is replaced by a
  positive infinitesimal eps (the epsilon method). The entries are then
  rational functions of eps, and a sign is the sign as eps -> 0+;
- a row of zeros is replaced by the coefficients of the derivative of the
  auxiliary polynomial, which is made from the row above.
"""

from fractions import Fraction


# ---------------------------------------------------------------- eps algebra
# A polynomial in eps is a list of Fractions, lowest power first, with no
# trailing zeros. The zero polynomial is [].


def _ptrim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def _padd(a, b):
    n = max(len(a), len(b))
    return _ptrim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def _pneg(a):
    return [-x for x in a]


def _pmul(a, b):
    if not a or not b:
        return []
    c = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                c[i + j] += x * y
    return _ptrim(c)


def _pdivmod(a, b):
    """Quotient and remainder of a by b (b nonzero), lowest power first."""
    a = list(a)
    q = [Fraction(0)] * max(len(a) - len(b) + 1, 0)
    lb = b[-1]
    while len(a) >= len(b) and a:
        k = len(a) - len(b)
        f = a[-1] / lb
        q[k] = f
        for i, y in enumerate(b):
            a[i + k] -= f * y
        a = _ptrim(a)
    return _ptrim(q), a


def _pgcd(a, b):
    while b:
        a, b = b, _pdivmod(a, b)[1]
    return [x / a[-1] for x in a]  # monic


def _lowest(a):
    for x in a:
        if x != 0:
            return x
    return Fraction(0)


class EpsFrac:
    """A rational function num(eps) / den(eps), eps a positive infinitesimal."""

    __slots__ = ("num", "den")

    def __init__(self, num, den=None):
        num = _ptrim(Fraction(x) for x in num)
        den = [Fraction(1)] if den is None else _ptrim(Fraction(x) for x in den)
        if not den:
            raise ZeroDivisionError("zero denominator")
        if not num:
            self.num, self.den = [], [Fraction(1)]
            return
        if len(den) > 1:
            g = _pgcd(num, den)
            if len(g) > 1:
                num = _pdivmod(num, g)[0]
                den = _pdivmod(den, g)[0]
        lead = den[-1]
        self.num = [x / lead for x in num]
        self.den = [x / lead for x in den]

    @staticmethod
    def const(x):
        return EpsFrac([x])

    @staticmethod
    def eps():
        return EpsFrac([0, 1])

    def is_zero(self):
        return not self.num

    def is_constant(self):
        return len(self.num) <= 1 and len(self.den) == 1

    def value(self):
        """The Fraction value; only for a constant."""
        if not self.is_constant():
            raise ValueError("entry depends on eps")
        return self.num[0] if self.num else Fraction(0)

    def sign(self):
        """The sign as eps -> 0+: -1, 0 or +1."""
        if not self.num:
            return 0
        s = _lowest(self.num) * _lowest(self.den)
        return 1 if s > 0 else -1

    def __sub__(self, o):
        return EpsFrac(_padd(_pmul(self.num, o.den), _pneg(_pmul(o.num, self.den))), _pmul(self.den, o.den))

    def __mul__(self, o):
        return EpsFrac(_pmul(self.num, o.num), _pmul(self.den, o.den))

    def __truediv__(self, o):
        if o.is_zero():
            raise ZeroDivisionError("division by a zero entry")
        return EpsFrac(_pmul(self.num, o.den), _pmul(self.den, o.num))

    def __repr__(self):
        if self.is_constant():
            return repr(self.value())
        return "EpsFrac(%r, %r)" % (self.num, self.den)


# ---------------------------------------------------------------- the array


class RouthResult:
    """rows: the array, row i belongs to s^(n-i); entries are EpsFrac.
    first_column: the first entries; a Fraction where it does not depend on eps.
    signs: the signs of the first column (as eps -> 0+).
    sign_changes: the number of sign changes in signs.
    events: a list of ("epsilon", i) and ("zero_row", i, aux) in the order met;
    aux is the auxiliary polynomial (highest power first) made from row i - 1.
    """

    def __init__(self, degree, rows, events):
        self.degree = degree
        self.rows = rows
        self.events = events
        self.signs = [r[0].sign() for r in rows]
        self.first_column = [_out(r[0]) for r in rows]
        self.sign_changes = sum(1 for a, b in zip(self.signs, self.signs[1:]) if a != b)  # @line L12

    @property
    def regular(self):
        return not self.events

    @property
    def used_epsilon(self):
        return any(e[0] == "epsilon" for e in self.events)

    def table(self):
        """The rows as lists of plain values (Fraction where possible)."""
        return [[_out(x) for x in r] for r in self.rows]


def _out(x):
    return x.value() if x.is_constant() else x


def normalize(coeffs):
    """Exact Fraction coefficients without leading zeros."""
    c = [Fraction(x) for x in coeffs]
    while c and c[0] == 0:
        c.pop(0)
    if not c:
        raise ValueError("the zero polynomial has no Routh array")
    return c


def routh_array(coeffs):
    """Build the Routh array of the polynomial coeffs (highest power first)."""
    a = normalize(coeffs)  # @line L1
    n = len(a) - 1
    width = n // 2 + 1

    def row_len(i):
        return (n - i) // 2 + 1

    rows = [[EpsFrac.const(x) for x in a[0::2]], [EpsFrac.const(x) for x in a[1::2]]]  # @line L2
    rows = [r + [EpsFrac.const(0)] * (row_len(i) - len(r)) for i, r in enumerate(rows[: n + 1])]
    events = []
    zero = EpsFrac.const(0)

    i = 1
    while i <= n:  # @line L3
        if i >= 2:  # @line L4
            up, cur = rows[i - 2], rows[i - 1]
            c = cur[0]  # @line L5
            new = []
            for j in range(row_len(i)):
                u1 = up[j + 1] if j + 1 < len(up) else zero
                c1 = cur[j + 1] if j + 1 < len(cur) else zero
                new.append((c * u1 - up[0] * c1) / c)  # @line L6
            rows.append(new)
        row = rows[i]
        if all(x.is_zero() for x in row):  # @line L7
            # Row of zeros: use the derivative of the auxiliary polynomial.
            prev = rows[i - 1]
            d = n - (i - 1)  # @line L8
            aux = []
            for j, x in enumerate(prev):
                aux.append(_out(x))
                if j < len(prev) - 1:
                    aux.append(Fraction(0))
            aux = (aux + [Fraction(0)] * (d + 1))[: d + 1]
            rows[i] = [EpsFrac.const(d - 2 * j) * prev[j] for j in range(row_len(i))]  # @line L9
            events.append(("zero_row", i, aux))
        elif rows[i][0].is_zero():  # @line L10
            rows[i][0] = EpsFrac.eps()  # @line L11
            events.append(("epsilon", i))
        i += 1
    assert len(rows) == n + 1 and all(len(r) <= width for r in rows)
    return RouthResult(n, rows, events)  # @line L13


def rhp_count(coeffs):
    """The number of sign changes in the first column. It equals the number
    of roots in the open right half plane in the cases proved on the page."""
    return routh_array(coeffs).sign_changes


def is_hurwitz(coeffs):
    """True if and only if every root has a negative real part."""
    r = routh_array(coeffs)
    return r.regular and r.sign_changes == 0


def hurwitz_determinants(coeffs):
    """The leading principal minors D_1, ..., D_n of the Hurwitz matrix,
    computed directly by fraction elimination (used to check the page)."""
    a = normalize(coeffs)
    n = len(a) - 1

    def coef(k):
        return a[k] if 0 <= k <= n else Fraction(0)

    H = [[coef(2 * (j + 1) - (i + 1)) for j in range(n)] for i in range(n)]
    out = []
    for k in range(1, n + 1):
        out.append(_det([row[:k] for row in H[:k]]))
    return out


def _det(M):
    M = [list(r) for r in M]
    n = len(M)
    det = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            det = -det
        det *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                for k in range(c, n):
                    M[r][k] -= f * M[c][k]
    return det
