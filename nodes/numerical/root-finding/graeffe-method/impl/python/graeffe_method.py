# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graeffe-method/. The authors are listed in prov/4YAGDA.jsonl.

"""Graeffe's root squaring method: the moduli of all roots of a real polynomial.

Coefficients are real and listed highest degree first: a[0] x^n + ... + a[n].
One squaring step maps p to the polynomial q with q(x^2) = (-1)^n p(x) p(-x),
whose roots are the squares of the roots of p. After k steps the roots are
raised to the power N = 2^k, the moduli separate, and the modulus of a root
can be read off two coefficients.

The coefficients grow like r^N, far beyond the range of a float, so they are
kept as Decimal numbers with a huge exponent range. A coefficient index j is
"regular" when the step squares it: (-1)^j c_j / b_j^2 is within tol of 1. Between
two consecutive regular indices i < l lie l - i roots of one common modulus
|b_l / b_i|^(1 / (N (l - i))).
"""

import math
from collections import namedtuple
from decimal import Context, Decimal, MAX_EMAX, MIN_EMIN

GraeffeResult = namedtuple("GraeffeResult", "groups roots steps status")
# groups: list of (modulus, count), largest modulus first, zeros last.
# roots:  the real roots found for groups of count 1 (a lone modulus must
#         belong to a real root when the coefficients are real).
# status: "separated" when every index became regular, else "max-iter"; then
#         the groups merge roots whose moduli were not yet separated.

CTX = Context(prec=40, Emax=MAX_EMAX, Emin=MIN_EMIN)


def square_step(b):
    """One Graeffe step: c_j = (-1)^j (b_j^2 + 2 sum_i (-1)^i b_(j-i) b_(j+i))."""
    n = len(b) - 1
    c = []
    for j in range(n + 1):
        s = CTX.multiply(b[j], b[j])
        for i in range(1, min(j, n - j) + 1):
            t = CTX.multiply(CTX.multiply(b[j - i], b[j + i]), Decimal(2))
            s = CTX.add(s, t) if i % 2 == 0 else CTX.subtract(s, t)
        c.append(s if j % 2 == 0 else CTX.minus(s))
    return c


def _regular(b, c):
    """The deviations |(-1)^j c_j / b_j^2 - 1|, infinite where b_j or c_j is 0."""
    dev = []
    for j in range(len(b)):
        if b[j] == 0 or c[j] == 0:
            dev.append(math.inf)  # cancelled coefficient: irregular
            continue
        r = float(CTX.divide(c[j], CTX.multiply(b[j], b[j])))
        dev.append(abs((r if j % 2 == 0 else -r) - 1.0))
    return dev


def _groups(b, reg, N):
    """Moduli of the groups between consecutive regular indices."""
    out = []
    for i, l in zip(reg, reg[1:]):
        lg = CTX.subtract(CTX.ln(CTX.abs(b[l])), CTX.ln(CTX.abs(b[i])))
        out.append((math.exp(float(lg) / (N * (l - i))), l - i))
    return out


def _horner(a, x):
    s = 0.0
    for c in a:
        s = s * x + c
    return s


def graeffe(a, tol=1e-12, max_iter=30):
    a = [float(c) for c in a]
    if any(math.isnan(c) or math.isinf(c) for c in a):
        raise ValueError("coefficients must be finite")
    while a and a[0] == 0.0:  # @line L1
        a.pop(0)
    if not a:
        raise ValueError("the zero polynomial has no well defined roots")
    zeros = 0
    while len(a) > 1 and a[-1] == 0.0:  # @line L1
        a.pop()
        zeros += 1
    n = len(a) - 1
    if n == 0:
        groups = [(0.0, zeros)] if zeros else []
        return GraeffeResult(groups, [0.0] * zeros, 0, "separated")
    b = [Decimal(c) for c in a]  # @line L2
    k, status, dev = 0, "max-iter", [0.0] * (n + 1)
    while k < max_iter:  # @line L3
        c = square_step(b)  # @line L4
        k += 1  # @line L5
        dev = _regular(b, c)  # @line L6
        b = c  # @line L7
        if max(dev) <= tol:  # @line L8
            status = "separated"
            break
    reg = [j for j in range(n + 1) if dev[j] <= tol or j in (0, n)]  # @line L9
    N = 2 ** k
    groups = _groups(b, reg, N)  # @line L10
    groups.sort(key=lambda g: -g[0])
    roots = []
    for rho, cnt in groups:  # @line L11
        if cnt == 1:
            roots.append(rho if abs(_horner(a, rho)) <= abs(_horner(a, -rho)) else -rho)
    if zeros:
        groups.append((0.0, zeros))
        roots.extend([0.0] * zeros)
    return GraeffeResult(groups, roots, k, status)  # @line L12
