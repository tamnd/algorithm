# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/input-output-linearization/. The authors are listed in prov/VH21RF.jsonl.

"""Input-output linearization of a single-input single-output system

    x' = f(x) + g(x) u,    y = h(x),    x in R^n,

where f, g and h have polynomial entries with exact rational coefficients.

The algorithm differentiates the output along the system with exact Lie
derivatives L_f phi = (d phi / dx) f until the input appears. The first k
with L_g L_f^k h (x0) != 0 gives the relative degree r = k + 1 at x0. Then

    y^(i) = L_f^i h (x)                    for i < r,
    y^(r) = L_f^r h (x) + L_g L_f^(r-1) h (x) u,

and the feedback u = (v - L_f^r h) / (L_g L_f^(r-1) h) makes y^(r) = v.

A polynomial vanishes on a neighborhood of a point if and only if it is the
zero polynomial, so the test "L_g L_f^k h = 0 near x0" is exact here. No
finite differences are used. The internal dynamics are not examined: the
caller must check that they stay bounded (see the zero dynamics page).
"""

from fractions import Fraction

__all__ = [
    "Poly",
    "variables",
    "lie_derivative",
    "lie_bracket",
    "IOLinearization",
    "io_linearize",
    "tracking_control",
    "closed_loop",
]


class Poly:
    """A polynomial in n variables: a dict from exponent tuples to Fractions."""

    __slots__ = ("n", "terms")

    def __init__(self, n, terms=None):
        self.n = n
        self.terms = {}
        for e, c in (terms or {}).items():
            if len(e) != n:
                raise ValueError("exponent tuple of the wrong length")
            c = Fraction(c)
            if c != 0:
                self.terms[tuple(e)] = c

    @classmethod
    def const(cls, n, c):
        return cls(n, {(0,) * n: c})

    @classmethod
    def var(cls, n, i):
        e = [0] * n
        e[i] = 1
        return cls(n, {tuple(e): 1})

    def _lift(self, other):
        if isinstance(other, Poly):
            if other.n != self.n:
                raise ValueError("polynomials in different numbers of variables")
            return other
        if isinstance(other, (int, Fraction)):
            return Poly.const(self.n, other)
        return NotImplemented

    def __add__(self, other):
        other = self._lift(other)
        if other is NotImplemented:
            return other
        t = dict(self.terms)
        for e, c in other.terms.items():
            t[e] = t.get(e, 0) + c
        return Poly(self.n, t)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.n, {e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        other = self._lift(other)
        if other is NotImplemented:
            return other
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        other = self._lift(other)
        if other is NotImplemented:
            return other
        t = {}
        for e1, c1 in self.terms.items():
            for e2, c2 in other.terms.items():
                e = tuple(a + b for a, b in zip(e1, e2))
                t[e] = t.get(e, 0) + c1 * c2
        return Poly(self.n, t)

    __rmul__ = __mul__

    def __pow__(self, k):
        if not isinstance(k, int) or k < 0:
            raise ValueError("only powers by integers k >= 0")
        out = Poly.const(self.n, 1)
        for _ in range(k):
            out = out * self
        return out

    def __eq__(self, other):
        other = self._lift(other)
        if other is NotImplemented:
            return False
        return self.terms == other.terms

    def __hash__(self):
        return hash((self.n, frozenset(self.terms.items())))

    def is_zero(self):
        return not self.terms

    def diff(self, i):
        """The exact partial derivative with respect to x_i."""
        t = {}
        for e, c in self.terms.items():
            if e[i] > 0:
                d = list(e)
                d[i] -= 1
                d = tuple(d)
                t[d] = t.get(d, 0) + c * e[i]
        return Poly(self.n, t)

    def __call__(self, x):
        """Evaluate at x. The entries of x may be int, Fraction, float or Poly."""
        if len(x) != self.n:
            raise ValueError("point of the wrong dimension")
        total = 0
        for e, c in self.terms.items():
            term = c
            for xi, k in zip(x, e):
                if k:
                    term = term * xi ** k
            total = total + term
        return total

    def __repr__(self):
        if not self.terms:
            return "0"
        parts = []
        for e in sorted(self.terms, reverse=True):
            mono = "*".join(f"x{i + 1}" + (f"^{k}" if k > 1 else "") for i, k in enumerate(e) if k)
            parts.append(f"{self.terms[e]}" + ("*" + mono if mono else ""))
        return " + ".join(parts)


def variables(n):
    """The coordinate functions x1, ..., xn as polynomials."""
    return tuple(Poly.var(n, i) for i in range(n))


def lie_derivative(phi, f):
    """L_f phi = sum_i (d phi / d x_i) f_i, exactly."""
    if len(f) != phi.n:
        raise ValueError("the vector field and the function have different dimensions")
    out = Poly(phi.n)
    for i, fi in enumerate(f):
        out = out + phi.diff(i) * fi
    return out


def lie_bracket(f, g):
    """[f, g] = (dg/dx) f - (df/dx) g, the sign used by Isidori and Khalil."""
    return [lie_derivative(gi, f) - lie_derivative(fi, g) for fi, gi in zip(f, g)]


class IOLinearization:
    """The result of io_linearize.

    status is "ok", "undefined" (L_g L_f^k h vanishes at x0 but not near x0,
    so no relative degree exists at x0) or "no input effect" (L_g L_f^k h is
    zero for k = 0, ..., n - 1, so no relative degree exists near x0).
    For status "ok": r is the relative degree, xi = [h, L_f h, ...,
    L_f^(r-1) h], a = L_g L_f^(r-1) h with a(x0) != 0, and b = L_f^r h.
    For "undefined", k is the index with the bad L_g L_f^k h, kept in a.
    """

    def __init__(self, status, r=None, xi=None, a=None, b=None, k=None):
        self.status = status
        self.r = r
        self.xi = xi or []
        self.a = a
        self.b = b
        self.k = k

    def __repr__(self):
        return f"IOLinearization(status={self.status!r}, r={self.r}, a={self.a!r}, b={self.b!r})"


def io_linearize(f, g, h, x0):
    """Find the relative degree of y = h(x) at x0 and the linearizing terms."""
    n = h.n
    if len(f) != n or len(g) != n or len(x0) != n:
        raise ValueError("f, g, h and x0 must have the same dimension n")
    if any(p.n != n for p in list(f) + list(g)):
        raise ValueError("every entry of f and g must be a polynomial in n variables")
    phi = h  # @line L1
    xi = []  # @line L1
    for k in range(n):  # @line L2
        xi.append(phi)  # @line L3
        a = lie_derivative(phi, g)  # @line L4
        if a(x0) != 0:  # @line L5
            b = lie_derivative(phi, f)  # @line L6
            return IOLinearization("ok", r=k + 1, xi=xi, a=a, b=b)  # @line L7
        if not a.is_zero():  # @line L8
            return IOLinearization("undefined", xi=xi, a=a, k=k)  # @line L8
        phi = lie_derivative(phi, f)  # @line L9
    return IOLinearization("no input effect", xi=xi)  # @line L10


def tracking_control(lin, c, yd):
    """The feedback u(t, x) that makes y track y_d.

    c = [c_0, ..., c_(r-1)] are the coefficients of s^r + c_(r-1) s^(r-1)
    + ... + c_0, which should be Hurwitz. yd = [y_d, y_d', ..., y_d^(r)] is a
    list of r + 1 functions of t. The tracking error e = y - y_d then obeys
    e^(r) + c_(r-1) e^(r-1) + ... + c_0 e = 0 while a(x) != 0.
    """
    if lin.status != "ok":
        raise ValueError("the system has no relative degree at the point")
    r = lin.r
    if len(c) != r or len(yd) != r + 1:
        raise ValueError("need r coefficients and r + 1 reference derivatives")

    def u(t, x):
        v = yd[r](t) - sum(c[i] * (float(lin.xi[i](x)) - yd[i](t)) for i in range(r))  # @line L11
        return (v - float(lin.b(x))) / float(lin.a(x))  # @line L11

    return u


def closed_loop(f, g, control):
    """The closed-loop field F(t, x, _) = f(x) + g(x) control(t, x), in float.

    The control is evaluated inside the field, so an RK4 step integrates the
    closed loop itself and not a zero-order hold of the input.
    """
    def F(t, x, _u=None):
        u = control(t, x)
        return [float(fi(x)) + float(gi(x)) * u for fi, gi in zip(f, g)]

    return F
