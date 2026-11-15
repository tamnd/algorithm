# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jury-stability-test/. The authors are listed in prov/7A0696.jsonl.

"""The Jury stability test for a real polynomial, in exact arithmetic.

A polynomial is a list of coefficients, highest power first:
[a0, a1, ..., an] is a0 z^n + a1 z^(n-1) + ... + an. The entries may be int,
Fraction or float; floats are converted exactly to Fraction, so the verdict
is exact for the polynomial whose coefficients are the given numbers.

jury_table follows the pseudocode of the page (lines L1 to L9). Each pass
removes the constant term of p_k with a multiple of the reversed polynomial
and divides by z. The first column F holds the leading coefficients of p_n,
p_(n-1), ..., p_0. If no entry of F is zero, the number of negative entries
is the number of roots outside the closed unit disc, and p is Schur (all
roots inside the open unit disc) exactly when that number is 0. A zero entry
is a singular step; p is then not Schur.

jury_classic checks the n + 1 conditions of the table of Jury and Blanchard:
p(1) > 0, (-1)^n p(-1) > 0, |an| < a0, and |lead| > |const| for the reduced
polynomials of degree n - 1 down to 2. It uses the division-free rows.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Optional


@dataclass
class JuryResult:
    """The outcome of jury_table.

    first: the first column a_0^n, a_0^(n-1), ..., a_0^j (as far as computed).
    rows: the coefficient lists of p_n, p_(n-1), ... (highest power first).
    alphas: alpha_n, alpha_(n-1), ... .
    outside: the number of roots outside the closed unit disc, or None if
        the table is singular.
    regular: False if some entry of the first column is zero.
    schur: True if every root lies in the open unit disc.
    """

    first: List[Fraction]
    rows: List[List[Fraction]]
    alphas: List[Fraction] = field(default_factory=list)
    outside: Optional[int] = None
    regular: bool = True
    schur: bool = False


def _exact(v):
    if isinstance(v, (int, Fraction)):
        return Fraction(v)
    if isinstance(v, float):
        return Fraction(v)
    raise TypeError("coefficients must be int, Fraction or float")


def _normalize(p):
    c = [_exact(v) for v in p]
    while c and c[0] == 0:
        c.pop(0)
    if not c:
        raise ValueError("the zero polynomial has no Jury table")
    return c


def jury_table(p):
    """Build the Jury table of p and return a JuryResult."""
    c = _normalize(p)  # @line L1
    if c[0] < 0:  # @line L1
        c = [-v for v in c]  # @line L1
    n = len(c) - 1
    first = [c[0]]  # @line L2
    rows = [list(c)]  # @line L2
    alphas = []
    for k in range(n, 0, -1):  # @line L3
        alpha = c[k] / c[0]  # @line L4
        alphas.append(alpha)
        c = [c[i] - alpha * c[k - i] for i in range(k)]  # @line L5
        first.append(c[0])  # @line L6
        rows.append(list(c))
        if c[0] == 0:  # @line L7
            return JuryResult(first, rows, alphas, None, False, False)  # @line L7
    neg = sum(1 for v in first if v < 0)  # @line L8
    return JuryResult(first, rows, alphas, neg, True, neg == 0)  # @line L9


def is_schur(p):
    """Return True if every root of p lies in the open unit disc."""
    return jury_table(p).schur


def outside_count(p):
    """Return the number of roots outside the closed unit disc, or None."""
    return jury_table(p).outside


def _polyval(c, x):
    s = Fraction(0)
    for v in c:
        s = s * x + v
    return s


def jury_classic(p):
    """Return True if the n + 1 conditions of the classic Jury table hold.

    The rows are formed without division: from the coefficients c of degree
    k, the next row has the entries c_0 c_i - c_k c_(k-i), i = 0..k-1, which
    are c_0 times the entries of jury_table. The conditions are
    p(1) > 0, (-1)^n p(-1) > 0, |c_k| < c_0 for the first row, and
    |lead| > |const| for the rows of degree n - 1 down to 2.
    """
    c = _normalize(p)
    if c[0] < 0:
        c = [-v for v in c]
    n = len(c) - 1
    if n == 0:
        return True
    if not _polyval(c, 1) > 0:
        return False
    if not (-1) ** n * _polyval(c, -1) > 0:
        return False
    if not abs(c[n]) < c[0]:
        return False
    for k in range(n, 2, -1):
        c = [c[0] * c[i] - c[k] * c[k - i] for i in range(k)]
        if not abs(c[0]) > abs(c[k - 1]):
            return False
    return True
