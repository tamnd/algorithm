# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonlinear-complementary-filter/. The authors are listed in prov/R8HFJF.jsonl.

"""The explicit complementary filter of Mahony, Hamel and Pflimlin (2008).

Vectors are lists of 3 floats and matrices are lists of rows, as in rbm.py.
R is the attitude R_sb of the body in the space frame {s}, so the kinematics
are dR/dt = R [Omega] with Omega the body angular velocity. A gyro reads
Omega_y = Omega + b with a slowly varying bias b. A vector sensor reads the
body form v_i = R^T v0_i of a known direction v0_i (gravity, the magnetic
field). The filter keeps an estimate (R_hat, b_hat) and runs, in continuous
time,

    v_hat_i  = R_hat^T v0_i
    w_mes    = sum_i k_i v_i x v_hat_i
    db_hat   = -k_I w_mes dt
    dR_hat   = R_hat [Omega_y - b_hat + k_P w_mes] dt.

This module integrates those equations with one step of the exponential map
per sample, which keeps R_hat exactly on SO(3) up to rounding.
"""

import rbm


def _unit(v):
    n = rbm.norm(v)
    if n == 0.0:
        raise ValueError("zero vector")
    return [x / n for x in v]


def ecf_step(r_hat, b_hat, omega_y, vs, v0s, ks, k_p, k_i, dt):
    """Return (R_hat, b_hat, w_mes) after one step of length dt.

    omega_y is the gyro reading, vs the measured body vectors, v0s the known
    space vectors, ks their weights, k_p and k_i the gains.
    """
    rt = rbm.transpose(r_hat)
    v_hats = [rbm.matvec(rt, _unit(v0)) for v0 in v0s]  # @line L1
    w_mes = [0.0, 0.0, 0.0]
    for k, v, vh in zip(ks, vs, v_hats):
        c = rbm.cross(_unit(v), vh)
        w_mes = [w_mes[j] + k * c[j] for j in range(3)]  # @line L2
    b_new = [b_hat[j] - k_i * w_mes[j] * dt for j in range(3)]  # @line L3
    w = [(omega_y[j] - b_new[j] + k_p * w_mes[j]) * dt for j in range(3)]
    r_new = rbm.mul(r_hat, rbm.so3_exp(w))  # @line L4
    return r_new, b_new, w_mes


def measurement_error(r_hat, vs, v0s, ks):
    """Return E_mes = sum_i k_i (1 - v_i . v_hat_i)."""
    rt = rbm.transpose(r_hat)
    return sum(k * (1.0 - rbm.dot(_unit(v), rbm.matvec(rt, _unit(v0)))) for k, v, v0 in zip(ks, vs, v0s))
