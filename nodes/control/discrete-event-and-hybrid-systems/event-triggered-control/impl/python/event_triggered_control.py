# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/event-triggered-control/. The authors are listed in prov/66J2N7.jsonl.

"""Event-triggered state feedback for x' = A x + B u with a relative threshold.

The controller holds u = -K x(t_k) until the next event. With the error
e(t) = x(t_k) - x(t), the next event is the first time t > t_k with
||e(t)|| >= sigma ||x(t)|| (Euclidean norm), as in Tabuada (2007).

lyapunov(A_cl, Q) solves A_cl' P + P A_cl = -Q. For a Hurwitz A_cl = A - B K,
and with V = x' P x, the trigger gives
dV/dt <= -(lambda_min(Q) - 2 sigma ||P B K||) ||x||^2, so every
sigma < lambda_min(Q) / (2 ||P B K||) gives exponential stability
(sigma_max below). min_inter_event_time gives a lower bound tau* > 0 on the
time between two events (the derivation is on the page).

The simulation uses RK4 from ctlsim with a fixed step dt and tests the
trigger at the end of each step, so an event can be up to dt late.
"""

import math

from ctlmat import charpoly, kron, eye, mul, norm2, polyroots, solve, sub, transpose, unvec, vec
from ctlsim import lti, rk4_step

__all__ = ["lyapunov", "sigma_max", "min_inter_event_time", "simulate_etc"]


def lyapunov(acl, q):
    """Solve A' P + P A = -Q by the Kronecker form (I kron A' + A' kron I) vec(P) = -vec(Q)."""
    n = len(acl)
    at = transpose(acl)
    big = [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(kron(eye(n), at), kron(at, eye(n)))]
    return unvec(solve(big, [-v for v in vec(q)]), n)


def sigma_max(a, b, k, q):
    """Return (sigma_bar, P): sigma_bar = lambda_min(Q) / (2 ||P B K||_2)."""
    bk = mul(b, k)
    acl = sub(a, bk)
    p = lyapunov(acl, q)
    lam_min = min(z.real for z in polyroots(charpoly(q)))
    return lam_min / (2 * norm2([[float(v) for v in row] for row in mul(p, bk)])), p


def min_inter_event_time(a, b, k, sigma):
    """Lower bound tau* on the inter-event times for the trigger ||e|| >= sigma ||x||.

    With alpha = ||A - B K||_2 and beta = ||B K||_2, y = ||e|| / ||x|| obeys
    y' <= (alpha + beta y)(1 + y) and y(t_k) = 0, so y needs at least
    tau* = ln(alpha (1 + sigma) / (alpha + beta sigma)) / (alpha - beta) to reach sigma
    (sigma / (alpha (1 + sigma)) when alpha = beta).
    """
    bk = mul(b, k)
    al = norm2([[float(v) for v in row] for row in sub(a, bk)])
    be = norm2([[float(v) for v in row] for row in bk])
    if abs(al - be) <= 1e-12 * max(al, be):
        return sigma / (al * (1 + sigma))
    return math.log(al * (1 + sigma) / (al + be * sigma)) / (al - be)


def simulate_etc(a, b, k, x0, sigma, t_end, dt):
    """Simulate the event-triggered loop. Returns (event_times, ts, xs).

    The first event is at t = 0. After each RK4 step the trigger is tested;
    on an event the held state x_hat becomes x(t).
    """
    f = lti(a, b)
    x = [float(v) for v in x0]
    xhat = list(x)  # @line L1
    u = [-sum(kij * xj for kij, xj in zip(row, xhat)) for row in k]  # @line L2
    events, ts, xs = [0.0], [0.0], [list(x)]
    steps = round(t_end / dt)
    for i in range(steps):
        x = rk4_step(f, i * dt, x, u, dt)  # @line L3
        t = (i + 1) * dt
        e = math.sqrt(sum((p - q) ** 2 for p, q in zip(xhat, x)))  # @line L4
        if e >= sigma * math.sqrt(sum(v * v for v in x)):  # @line L5
            xhat = list(x)  # @line L6
            u = [-sum(kij * xj for kij, xj in zip(row, xhat)) for row in k]  # @line L7
            events.append(t)
        ts.append(t)
        xs.append(x)
    return events, ts, xs
