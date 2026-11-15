# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sontag-universal-formula/. The authors are listed in prov/B75HKW.jsonl.

"""Sontag's universal formula for a control-affine system

    x' = f(x) + g(x) u,    x in R^n,  u in R^m,

with a known control Lyapunov function V. At a state x let

    a = L_f V(x) = grad V(x) . f(x)            (a number)
    b = L_g V(x) = grad V(x) g(x)              (a row of m numbers)
    beta = |b|^2.

The feedback is u = 0 if beta = 0, and otherwise

    u = -phi b^T,    phi = (a + sqrt(a^2 + beta^2)) / beta.

Along the closed loop, V' = a - phi beta = -sqrt(a^2 + beta^2), which is
negative wherever a < 0 or b != 0, that is, at every x != 0 when V is a
control Lyapunov function.

When a <= 0 the numerator a + sqrt(a^2 + beta^2) cancels. The code then uses
the equal form phi = beta / (sqrt(a^2 + beta^2) - a), which has no
cancellation.

Precondition: f, g and grad V are given as functions that return lists. The
caller must make sure that V is a control Lyapunov function; the code does
not check it.

Cost: O(n m) arithmetic operations and one square root per state, plus one
evaluation each of f, g and grad V.
"""

import math

__all__ = ["sontag_gain", "sontag_feedback", "closed_loop"]


def sontag_gain(a, b):
    """Return the input u (a list of m numbers) from a = L_f V and b = L_g V.

    b is a list of m numbers. The result is u = -phi b with
    phi = (a + sqrt(a^2 + |b|^4)) / |b|^2, and u = 0 when b = 0.
    """
    beta = sum(bj * bj for bj in b)  # @line L3
    if beta == 0:  # @line L4
        return [0.0 for _ in b]  # @line L4
    s = math.sqrt(a * a + beta * beta)  # @line L5
    if a > 0:  # @line L5
        phi = (a + s) / beta  # @line L5
    else:
        phi = beta / (s - a)  # @line L5
    return [-phi * bj for bj in b]  # @line L6


def sontag_feedback(f, g, grad_V):
    """Return the feedback k(x) of Sontag's formula.

    f(x) returns the drift as a list of n numbers, g(x) returns the input
    matrix as n rows of m numbers, and grad_V(x) returns the gradient of V as
    a list of n numbers. k(x) returns a list of m numbers.
    """
    def k(x):
        p = grad_V(x)
        fx = f(x)
        gx = g(x)
        m = len(gx[0])
        a = sum(pi * fi for pi, fi in zip(p, fx))  # @line L1
        b = [sum(p[i] * gx[i][j] for i in range(len(p))) for j in range(m)]  # @line L2
        return sontag_gain(a, b)
    return k


def closed_loop(f, g, grad_V):
    """Return F(t, x, u) = f(x) + g(x) k(x) for the simulation helper.

    The feedback is evaluated inside the right side, so an RK4 step sees
    the continuous closed loop. The argument u is ignored.
    """
    k = sontag_feedback(f, g, grad_V)

    def F(t, x, u=None):
        uu = k(x)
        fx = f(x)
        gx = g(x)
        return [fx[i] + sum(gx[i][j] * uu[j] for j in range(len(uu))) for i in range(len(x))]
    return F
