# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/position-based-visual-servoing/. The authors are listed in prov/CP9B6Z.jsonl.

"""Position-based visual servoing (PBVS).

The input is an estimate of the target pose T_ct in the current camera
frame (from a pose estimator such as PnP) and the target pose T_c*t in
the desired camera frame. The error is the pose of the current camera in
the desired camera frame, T_c*c = T_c*t T_ct^-1 = (R, t), written as
(t, theta u) with theta u = log(R). The law

    v = -lambda R^T t,    omega = -lambda theta u

makes t and theta u decay like exp(-lambda time), so the camera center
moves on a straight line to its goal. The twist V = (omega, v) is in the
camera frame, angular part first, and the camera pose moves by
T_wc exp([V] dt).

Matrices are lists of rows and vectors are lists. Only the standard library.
"""

from rbm import T_inv, matvec, mul, so3_log, se3_exp, transpose


def pbvs_step(t_ct, t_cstar_t, lam):
    """Return the camera twist (omega, v) of PBVS for the estimate t_ct."""
    t_err = mul(t_cstar_t, T_inv(t_ct))  # @line L1
    r = [row[:3] for row in t_err[:3]]  # @line L2
    p = [t_err[0][3], t_err[1][3], t_err[2][3]]
    theta_u = so3_log(r)  # @line L3
    v = [-lam * x for x in matvec(transpose(r), p)]  # @line L4
    w = [-lam * x for x in theta_u]  # @line L5
    return w + v  # @line L6


def simulate(t_wc, t_wt, t_cstar_t, lam, dt, steps, estimate=None):
    """Run PBVS; the twist is held for dt.

    estimate(t_ct) returns the pose estimate from the true pose; the default
    is exact. Return the list of camera poses t_wc for the steps 0 to steps.
    """
    out = [t_wc]
    for _ in range(steps):
        t_ct = mul(T_inv(t_wc), t_wt)
        est = estimate(t_ct) if estimate else t_ct
        v = pbvs_step(est, t_cstar_t, lam)
        t_wc = mul(t_wc, se3_exp([dt * c for c in v]))
        out.append(t_wc)
    return out
