# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bell-states/. The authors are listed in prov/7ZRWP7.jsonl.

"""The four Bell states, the circuit that makes them and the Bell measurement.

Qubit 1 is the left symbol of a ket and qubit 0 the right one, so the list
index of |q1 q0> is 2*q1 + q0. With exact=True the amplitudes are exact
numbers a + b*sqrt(2) (the class R2 of qsim).
"""

from fractions import Fraction

from qsim import H, H_EXACT, R2, apply_1q, apply_cnot, basis_state, inner

NAMES = {(0, 0): "Phi+", (0, 1): "Psi+", (1, 0): "Phi-", (1, 1): "Psi-"}


def bell_state(x, y, exact=False):
    """beta_xy = CNOT_(1->0) (H on qubit 1) |x y>  =  (|0 y> + (-1)^x |1 (1-y)>) / sqrt(2)."""
    s = basis_state(2, 2 * x + y)
    if exact:
        s = [R2(a) for a in s]
    s = apply_1q(s, H_EXACT if exact else H, 1)
    return apply_cnot(s, 1, 0)


def bell_formula(x, y):
    """beta_xy written from the closed form, with exact amplitudes."""
    h = R2(0, Fraction(1, 2))  # 1/sqrt(2) = sqrt(2)/2
    s = [R2(0)] * 4
    s[y] = s[y] + h
    s[2 + (1 - y)] = s[2 + (1 - y)] + (h if x == 0 else -h)
    return s


def bell_basis_coefficients(state):
    """The amplitudes <beta_xy|state> of a two-qubit state, for each label (x, y)."""
    return {xy: inner(bell_state(*xy), state) for xy in NAMES}


def bell_measure_circuit(state):
    """Undo the Bell circuit: CNOT_(1->0), then H on qubit 1. A computational
    measurement of the result gives x on qubit 1 and y on qubit 0."""
    return apply_1q(apply_cnot(state, 1, 0), H, 1)
