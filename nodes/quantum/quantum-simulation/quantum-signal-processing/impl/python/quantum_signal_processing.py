# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-signal-processing/. The authors are listed in prov/9B38VZ.jsonl.
"""Quantum signal processing on one qubit.

Signal: W(x) = [[x, i sqrt(1 - x^2)], [i sqrt(1 - x^2), x]] = e^(i arccos(x) X).
Sequence: U_Phi(x) = e^(i phi_0 Z) W(x) e^(i phi_1 Z) ... W(x) e^(i phi_d Z), and P(x) = <0|U_Phi(x)|0>.
"""

import cmath
import math

from qsim import qsp_full_phases, qsp_matrix, solve_linear


def signal(x):
    """W(x), the signal rotation."""
    s = math.sqrt(max(0.0, 1.0 - x * x))
    return [[complex(x), 1j * s], [1j * s, complex(x)]]


def reflection(x):
    """R(x) = [[x, sqrt(1 - x^2)], [sqrt(1 - x^2), -x]], the signal in the reflection convention."""
    s = math.sqrt(max(0.0, 1.0 - x * x))
    return [[complex(x), complex(s)], [complex(s), complex(-x)]]


def _mul(a, b):
    return [[a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
            [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]]]


def _rz(ph):
    return [[cmath.exp(1j * ph), 0j], [0j, cmath.exp(-1j * ph)]]


def qsp_unitary(phases, x):
    """U_Phi(x) for d + 1 phases."""
    return qsp_matrix(phases, x)


def qsp_polynomial(phases, x):
    """P(x) = <0|U_Phi(x)|0>."""
    return qsp_matrix(phases, x)[0][0]


def reflection_sequence(phases, x):
    """prod_(j=1..d) e^(i phi_j Z) R(x), the form of Corollary 8 of Gilyen, Su, Low and Wiebe."""
    u = [[1 + 0j, 0j], [0j, 1 + 0j]]
    for ph in phases:
        u = _mul(u, _mul(_rz(ph), reflection(x)))
    return u


def to_reflection_phases(phases):
    """Phases psi with e^(i psi_0 Z) prod_j R(x) e^(i psi_j Z) = (-i)^d U_Phi(x).

    R(x) = -i e^(i pi/4 Z) W(x) e^(i pi/4 Z), so psi_0 = phi_0 - pi/4, psi_d = phi_d - pi/4
    and psi_j = phi_j - pi/2 in between.
    """
    d = len(phases) - 1
    out = [phases[0] - math.pi / 4] + [p - math.pi / 2 for p in phases[1:d]] + [phases[d] - math.pi / 4]
    if d == 0:
        out = [phases[0]]
    return out


def reflection_form(psi, x):
    """e^(i psi_0 Z) prod_(j=1..d) R(x) e^(i psi_j Z)."""
    u = _rz(psi[0])
    for ph in psi[1:]:
        u = _mul(_mul(u, reflection(x)), _rz(ph))
    return u


def _value_and_jacobian_row(full, x, m):
    """Re P(x) and its derivatives with respect to the m reduced (symmetric) phases."""
    d = len(full) - 1
    w = signal(x)
    left = [None] * (d + 1)
    left[0] = _rz(full[0])
    for j in range(1, d + 1):
        left[j] = _mul(_mul(left[j - 1], w), _rz(full[j]))
    right = [None] * (d + 1)
    right[d] = [[1 + 0j, 0j], [0j, 1 + 0j]]
    for j in range(d - 1, -1, -1):
        right[j] = _mul(_mul(w, _rz(full[j + 1])), right[j + 1])
    row = [0.0] * m
    for j in range(d + 1):
        # d/dphi_j of <0| left[j] right[j] |0> with left[j] ending in e^(i phi_j Z): insert iZ.
        g = 1j * (left[j][0][0] * right[j][0][0] - left[j][0][1] * right[j][1][0])
        row[min(j, d - j)] += g.real
    return left[d][0][0].real, row


def find_phases(f, d, tol=1e-13, max_iter=100):
    """Phases Phi (d + 1 of them) with Re P(x) = f(x) on [-1, 1].

    f is a real polynomial of degree at most d and parity d mod 2 with |f| < 1 on [-1, 1].
    """
    m = d // 2 + 1  # @line L1
    nodes = [math.cos((2 * k - 1) * math.pi / (4 * m)) for k in range(1, m + 1)]
    target = [f(x) for x in nodes]
    red = [0.0] * m  # @line L2

    def residual_and_jacobian(r):
        full = qsp_full_phases(r, d)  # @line L3
        res, jac = [], []
        for x, y in zip(nodes, target):
            v, row = _value_and_jacobian_row(full, x, m)
            res.append(v - y)  # @line L4
            jac.append(row)
        return res, jac

    res, jac = residual_and_jacobian(red)
    for _ in range(max_iter):
        err = max(abs(v) for v in res)
        if err <= tol:  # @line L5
            return qsp_full_phases(red, d)  # @line L7
        step = solve_linear(jac, res)  # @line L6
        t = 1.0
        while True:
            trial = [a - t * b for a, b in zip(red, step)]
            tres, tjac = residual_and_jacobian(trial)
            if max(abs(v) for v in tres) < err or t < 1e-4:
                red, res, jac = trial, tres, tjac
                break
            t /= 2
    raise RuntimeError("QSP phase solver did not converge")
