# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tr-bdf2/. The authors are listed in prov/W1B2JC.jsonl.
"""TR-BDF2 for circuit equations f(x) + d/dt q(x) = u(t).

A circuit is any object with the methods
  f(x) -> list, G(x) -> matrix (df/dx), q(x) -> list, C(x) -> matrix (dq/dx),
  u(t) -> list,
in the notation of modified nodal analysis: x holds node voltages and branch
currents, f the resistive part, q the charges and fluxes, u the sources.

One step of size h from (t, x):
  stage 1, trapezoidal rule to t + gamma h,
  stage 2, BDF2 on the points t, t + gamma h, t + h.
With gamma = 2 - sqrt(2) both stages solve a system with the same matrix
C + (gamma h / 2) G, so for a linear circuit one LU serves both stages.
The local error estimate is 2 k h F[t, t + gamma h, t + h] h^2, the second
divided difference of F = u - f = dq/dt, with the error constant k.
"""

import math

from sim3dense import solve

GAMMA = 2 - math.sqrt(2)


def error_constant(g=GAMMA):
    """k with (exact - numerical) = k h^3 q''' + O(h^4) for one TR-BDF2 step."""
    return (-3 * g * g + 4 * g - 2) / (12 * (2 - g))


def stability_function(z, g=GAMMA):
    """R(z) of TR-BDF2 for y' = lambda y, z = h lambda, any gamma in (0, 1)."""
    r1 = (1 + g * z / 2) / (1 - g * z / 2)  # trapezoidal stage
    a = 1 / (g * (2 - g))
    b = (1 - g) ** 2 / (g * (2 - g))
    d = (1 - g) / (2 - g)
    return (a * r1 - b) / (1 - d * z)


class NewtonFailure(RuntimeError):
    """Newton's method did not converge for a stage."""


def _sub(a, b):
    return [x - y for x, y in zip(a, b)]


def _norm(v):
    return max((abs(x) for x in v), default=0.0)


def newton_stage(ckt, t, guess, qconst, beta, tol=1e-12, maxit=50):
    """Solve q(x) + beta (f(x) - u(t)) = qconst for x by Newton's method."""
    x = list(guess)
    ut = ckt.u(t)
    for it in range(maxit):
        r = [qi + beta * (fi - ui) - ci for qi, fi, ui, ci in zip(ckt.q(x), ckt.f(x), ut, qconst)]
        cm, gm = ckt.C(x), ckt.G(x)
        jac = [[c + beta * g for c, g in zip(crow, grow)] for crow, grow in zip(cm, gm)]
        dx = solve(jac, [-v for v in r])
        x = [a + b for a, b in zip(x, dx)]
        if _norm(dx) <= tol * (1 + _norm(x)):
            return x, it + 1
    raise NewtonFailure(f"no convergence at t = {t}")


def rate(ckt, t, x):
    """F = u - f, which equals dq/dt on a solution."""
    return [ui - fi for ui, fi in zip(ckt.u(t), ckt.f(x))]


def trapezoidal_step(ckt, t, x, h):
    """One step of the trapezoidal rule (used as stage 1 and for comparison)."""
    qn, fn = ckt.q(x), rate(ckt, t, x)
    qconst = [a + h / 2 * b for a, b in zip(qn, fn)]
    xn, _ = newton_stage(ckt, t + h, x, qconst, h / 2)
    return xn


def backward_euler_step(ckt, t, x, h):
    """One step of backward Euler (used for comparison)."""
    xn, _ = newton_stage(ckt, t + h, x, ckt.q(x), h)
    return xn


def tr_bdf2_step(ckt, t, x, h, g=GAMMA):
    """One TR-BDF2 step; returns (x_new, x_stage, error estimate in q)."""
    qn, fn = ckt.q(x), rate(ckt, t, x)
    qconst = [a + g * h / 2 * b for a, b in zip(qn, fn)]
    xg, _ = newton_stage(ckt, t + g * h, x, qconst, g * h / 2)  # @line L3
    qg = ckt.q(xg)
    a = 1 / (g * (2 - g))
    b = (1 - g) ** 2 / (g * (2 - g))
    d = (1 - g) / (2 - g)
    qconst2 = [a * p - b * r for p, r in zip(qg, qn)]
    xn, _ = newton_stage(ckt, t + h, xg, qconst2, d * h)  # @line L4
    k = error_constant(g)
    f0, f1, f2 = fn, rate(ckt, t + g * h, xg), rate(ckt, t + h, xn)
    est = [2 * k * h * (p / g - r / (g * (1 - g)) + s / (1 - g)) for p, r, s in zip(f0, f1, f2)]  # @line L5
    return xn, xg, est


def tr_bdf2_fixed(ckt, x0, t0, t1, steps):
    """Fixed step size; returns the list of (t, x)."""
    h = (t1 - t0) / steps
    out, x = [(t0, list(x0))], list(x0)
    for i in range(steps):
        x, _, _ = tr_bdf2_step(ckt, t0 + i * h, x, h)
        out.append((t0 + (i + 1) * h, x))
    return out


def tr_bdf2_adaptive(ckt, x0, t0, t1, h, rtol=1e-4, atol=1e-9, hmin=1e-15):
    """Adaptive step size from the local error estimate.

    Returns (points, rejected) where points is the list of accepted (t, x).
    """
    t, x = t0, list(x0)  # @line L1
    out, rejected = [(t, list(x))], 0
    while t < t1 and t1 - t > 1e-12 * max(1.0, abs(t1)):  # @line L2
        h = min(h, t1 - t)
        try:
            xn, _, est = tr_bdf2_step(ckt, t, x, h)
        except NewtonFailure:
            h /= 4
            rejected += 1
            if h < hmin:
                raise
            continue
        qn = ckt.q(xn)
        r = max(abs(e) / (rtol * abs(qv) + atol) for e, qv in zip(est, qn))  # @line L6
        if r <= 1:  # @line L7
            t, x = t + h, xn
            out.append((t, x))
        else:
            rejected += 1
        h *= min(2.0, max(0.2, 0.9 * (r if r > 0 else 1e-12) ** (-1 / 3)))  # @line L8
        if h < hmin:
            raise NewtonFailure("step size underflow")
    return out, rejected  # @line L9
