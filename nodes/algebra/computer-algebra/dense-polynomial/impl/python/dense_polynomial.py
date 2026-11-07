# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dense-polynomial/. The authors are listed in prov/RVZNCP.jsonl.

"""Dense polynomials over a commutative ring R, and the recursive dense
representation of multivariate polynomials.

A DensePoly is a list of coefficients c[0], c[1], ..., c[m-1] in R, lowest
degree first, with c[m-1] != 0 (the empty list is the zero polynomial). The
coefficients may themselves be DensePoly objects: R[x_1, ..., x_n] is held as
R[x_1, ..., x_{n-1}][x_n], a dense polynomial in the main variable x_n whose
coefficients are dense polynomials in x_1, ..., x_{n-1}. Arithmetic on the
coefficients goes through Python's operators, so the depth of nested calls
equals the number of variables and no more.

Cost model: ring operations in R (for nested polynomials, operations in the
coefficient ring at the next level). For m and n coefficients, add costs
O(m + n), mul O(m n), evaluate O(m) and pseudo_divmod O(m (m - n + 1))
operations in R.
"""

from typing import Any, Dict, List, Tuple


class DensePoly:
    """A univariate dense polynomial over a commutative ring R.

    zero is the zero element of R; it is needed to build polynomials and to
    normalize, because R may itself be a polynomial ring.
    """

    __slots__ = ("c", "zero")

    def __init__(self, coeffs: List[Any], zero: Any) -> None:
        self.zero = zero
        self.c = _normalize(list(coeffs), zero)

    # basic access -----------------------------------------------------------

    def degree(self) -> int:
        """Degree in the main variable; -1 for the zero polynomial."""
        return len(self.c) - 1

    def lc(self) -> Any:
        """Leading coefficient. Precondition: self is not zero."""
        return self.c[-1]

    def is_zero(self) -> bool:
        return not self.c

    def __eq__(self, other: object) -> bool:
        if isinstance(other, DensePoly):
            return self.c == other.c
        if other == 0 or other == self.zero:
            return not self.c
        return False

    def __hash__(self) -> int:
        return hash(tuple(self.c))

    def __repr__(self) -> str:
        return "DensePoly(%r)" % (self.c,)

    # arithmetic ---------------------------------------------------------------

    def __add__(self, other: "DensePoly") -> "DensePoly":
        """Sum; O(m + n) additions in R."""
        a, b = self.c, other.c
        m, n = len(a), len(b)
        c = [self.zero] * max(m, n)  # @line L1
        for i in range(max(m, n)):
            c[i] = (a[i] if i < m else self.zero) + (b[i] if i < n else self.zero)
        return DensePoly(c, self.zero)  # @line L2

    def __neg__(self) -> "DensePoly":
        return DensePoly([-x for x in self.c], self.zero)

    def __sub__(self, other: "DensePoly") -> "DensePoly":
        return self + (-other)

    def __mul__(self, other: "DensePoly") -> "DensePoly":
        """Schoolbook product; m n multiplications in R."""
        a, b = self.c, other.c
        m, n = len(a), len(b)
        if m == 0 or n == 0:  # @line L3
            return DensePoly([], self.zero)
        c = [self.zero] * (m + n - 1)  # @line L4
        for i in range(m):  # @line L5
            for j in range(n):
                c[i + j] = c[i + j] + a[i] * b[j]
        return DensePoly(c, self.zero)  # @line L6

    def scale(self, s: Any) -> "DensePoly":
        """s times self, for s in R."""
        return DensePoly([s * x for x in self.c], self.zero)

    def shift(self, k: int) -> "DensePoly":
        """self times x^k."""
        if not self.c:
            return self
        return DensePoly([self.zero] * k + self.c, self.zero)

    def evaluate(self, u: Any) -> Any:
        """Value at x = u in R (for nested polynomials, u is in the coefficient
        ring, so this substitutes for the main variable). Horner, O(m)."""
        s = self.zero
        for x in reversed(self.c):
            s = s * u + x
        return s

    def derivative(self) -> "DensePoly":
        """Formal derivative in the main variable; i * c[i] as a sum of i copies
        is written i * c[i], which Python's ints and Fractions support, and for
        nested polynomials goes through scale_int."""
        out = []
        for i in range(1, len(self.c)):
            x = self.c[i]
            out.append(x.scale_int(i) if isinstance(x, DensePoly) else i * x)
        return DensePoly(out, self.zero)

    def scale_int(self, k: int) -> "DensePoly":
        """k times self, for an integer k, at every level, without recursion
        beyond the number of variables."""
        return DensePoly([x.scale_int(k) if isinstance(x, DensePoly) else k * x for x in self.c], self.zero)

    def pseudo_divmod(self, b: "DensePoly") -> Tuple["DensePoly", "DensePoly"]:
        """(q, r) with lc(b)^(m-n+1) self = q b + r and deg r < deg b, where
        m - 1 = deg self and n - 1 = deg b; needs no division in R.

        Precondition: b is not zero. Cost: O(m (m - n + 1)) operations in R.
        """
        if b.is_zero():
            raise ZeroDivisionError("pseudo-division by the zero polynomial")
        zero = self.zero
        r = self  # @line L9
        q = DensePoly([], zero)
        ell = b.lc()
        e = max(self.degree() - b.degree() + 1, 0)
        while r.degree() >= b.degree():  # @line L10
            t = DensePoly([r.lc()], zero).shift(r.degree() - b.degree())  # @line L11
            q = q.scale(ell) + t  # @line L12
            r = r.scale(ell) - t * b
            e -= 1  # @line L13
        f = _power(ell, e, zero)
        return q.scale(f), r.scale(f)  # @line L14

    # conversion -----------------------------------------------------------------

    def to_dict(self) -> Dict[Tuple[int, ...], Any]:
        """The distributed form: exponent tuple (e_1, ..., e_n) -> nonzero base
        coefficient. Uses an explicit stack."""
        out: Dict[Tuple[int, ...], Any] = {}
        stack: List[Tuple[Any, Tuple[int, ...]]] = [(self, ())]
        while stack:
            p, exps = stack.pop()
            if isinstance(p, DensePoly):
                for i, x in enumerate(p.c):
                    stack.append((x, (i,) + exps))
            elif p != 0:
                out[exps] = p
        return out

    def check_invariant(self) -> None:
        """At every level the last coefficient is nonzero, and all coefficients
        at one level have the same nesting depth."""
        stack: List[Any] = [self]
        while stack:
            p = stack.pop()
            if not isinstance(p, DensePoly):
                continue
            if p.c:
                assert not _is_zero(p.c[-1], p.zero), "trailing zero"
            kinds = {_depth(x) for x in p.c}
            assert len(kinds) <= 1, "mixed nesting depths"
            if p.c:
                assert _depth(p.zero) == kinds.pop()
            stack.extend(p.c)


def _is_zero(x: Any, zero: Any) -> bool:
    if isinstance(x, DensePoly):
        return not x.c
    return x == zero


def _normalize(c: List[Any], zero: Any) -> List[Any]:
    while c and _is_zero(c[-1], zero):  # @line L7
        c.pop()
    return c  # @line L8


def _depth(x: Any) -> int:
    d = 0
    while isinstance(x, DensePoly):
        d += 1
        x = x.zero
    return d


def _power(x: Any, e: int, zero: Any) -> Any:
    """x^e by repeated squaring; x^0 is the one of the ring, built as x^0 = 1."""
    result: Any = None
    base = x
    while e > 0:
        if e & 1:
            result = base if result is None else result * base
        base = base * base
        e >>= 1
    if result is None:
        return _one_like(x)
    return result


def _one_like(x: Any) -> Any:
    """The one of the ring that x belongs to."""
    if isinstance(x, DensePoly):
        return DensePoly([_one_like(x.zero)], x.zero)
    return type(x)(1)


def zero_of(nvars: int, base_zero: Any) -> Any:
    """The zero of R[x_1, ..., x_nvars] in the recursive dense representation."""
    z = base_zero
    for _ in range(nvars):
        z = DensePoly([], z)
    return z


def from_dict(d: Dict[Tuple[int, ...], Any], nvars: int, base_zero: Any) -> Any:
    """Build the recursive dense form of sum c * x_1^e_1 ... x_n^e_n.

    Works level by level, innermost variable x_1 first, without recursion.
    For nvars = 0 the result is the constant itself.
    """
    if nvars == 0:
        return d.get((), base_zero)
    level: Dict[Tuple[int, ...], Any] = {k: v for k, v in d.items() if v != 0}
    zero: Any = base_zero
    for _ in range(nvars):
        groups: Dict[Tuple[int, ...], Dict[int, Any]] = {}
        for exps, v in level.items():
            groups.setdefault(exps[1:], {})[exps[0]] = v
        level = {}
        for rest, g in groups.items():
            cs = [zero] * (max(g) + 1)
            for i, v in g.items():
                cs[i] = v
            level[rest] = DensePoly(cs, zero)
        zero = DensePoly([], zero)
    return level.get((), zero)
