# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multivariate-division-algorithm/. The authors are listed in prov/8BTTVF.jsonl.

"""Division of a polynomial by an ordered list of polynomials in K[x_1, ..., x_n].

A polynomial is a dict that maps an exponent tuple (a_1, ..., a_n) to a nonzero
coefficient. The coefficients belong to a field: Fraction, or any type with
+, -, *, / and == 0 (for example a class for Z/pZ). The zero polynomial is {}.
"""

from typing import Callable, Dict, List, Sequence, Tuple

Exp = Tuple[int, ...]
Poly = Dict[Exp, object]


def order_key(order: str) -> Callable[[Exp], tuple]:
    """Return a sort key such that a larger key means a larger monomial."""
    if order == "lex":
        return lambda a: tuple(a)
    if order == "grlex":
        return lambda a: (sum(a), tuple(a))
    if order == "grevlex":
        return lambda a: (sum(a), tuple(-e for e in reversed(a)))
    raise ValueError("order must be lex, grlex or grevlex")


def leading_monomial(f: Poly, order: str) -> Exp:
    """LM(f) for a nonzero polynomial f."""
    return max(f, key=order_key(order))


def _divides(a: Exp, b: Exp) -> bool:
    return all(x <= y for x, y in zip(a, b))


def _sub_term_times(p: Poly, c: object, m: Exp, g: Poly) -> None:
    """p <- p - c * x^m * g, in place, dropping zero coefficients."""
    for e, v in g.items():
        k = tuple(x + y for x, y in zip(m, e))
        w = p.get(k, 0) - c * v
        if w == 0:
            p.pop(k, None)
        else:
            p[k] = w


def divide(f: Poly, divisors: Sequence[Poly], order: str) -> Tuple[List[Poly], Poly]:
    """Divide f by the ordered list divisors = (f_1, ..., f_s) for a monomial order.

    Returns (q_1, ..., q_s) and r with f = q_1 f_1 + ... + q_s f_s + r, where no
    term of r is divisible by any LT(f_i), and LM(q_i f_i) <= LM(f) when q_i f_i
    is not zero. Precondition: each divisor is nonzero, and all exponent tuples
    have the same length. Cost: N passes of the outer loop, each with at most s
    divisibility tests and one subtraction of at most max |f_i| terms; for a
    graded order N is at most the number of monomials of degree <= deg f.
    """
    if any(not g for g in divisors):
        raise ValueError("each divisor must be a nonzero polynomial")
    key = order_key(order)
    heads = [max(g, key=key) for g in divisors]
    q: List[Poly] = [{} for _ in divisors]  # @line L1
    r: Poly = {}
    p: Poly = dict(f)
    while p:  # @line L2
        m = max(p, key=key)
        c = p[m]
        i = 0  # @line L3
        divided = False
        while i < len(divisors) and not divided:  # @line L4
            if _divides(heads[i], m):  # @line L5
                t = tuple(x - y for x, y in zip(m, heads[i]))
                ct = c / divisors[i][heads[i]]
                q[i][t] = q[i].get(t, 0) + ct  # @line L6
                if q[i][t] == 0:
                    del q[i][t]
                _sub_term_times(p, ct, t, divisors[i])  # @line L7
                divided = True  # @line L8
            else:
                i += 1  # @line L9
        if not divided:  # @line L10
            r[m] = c  # @line L11
            del p[m]  # @line L12
    return q, r  # @line L13
