# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/resolved-rate-motion-control/. The authors are listed in prov/XNS6ZX.jsonl.
"""Resolved-rate motion control of a position task, with a fixed time step.

The task is x = fk(q) in R^m with Jacobian jac(q), an m by n matrix of
full row rank (m <= n). Each step sets the joint rate

    q' = J^+ (x_d'(t) + K (x_d(t) - fk(q)))

with the right pseudoinverse J^+ = J^T (J J^T)^-1, and moves the joints by
one explicit Euler step q <- q + dt q'. With K = 0 this is the open-loop
scheme of Whitney (1969); with K > 0 the task error is fed back
(Siciliano et al., Robotics, Section 3.7.1).

rbm.pinv_right raises ValueError when J J^T is singular to working
precision, that is, at a kinematic singularity.
"""

import rbm


def joint_rate(j, v):
    """Return the minimum-norm q' with J q' = v."""
    return rbm.matvec(rbm.pinv_right(j), v)


def _gain_times(gain, e):
    if isinstance(gain, list):
        return rbm.matvec(gain, e)
    return [gain * x for x in e]


def resolved_rate(fk, jac, q0, xd, xd_dot, gain, dt, steps):
    """Return the list of joint vectors q_0, q_1, ..., q_steps.

    xd(t) and xd_dot(t) give the desired task position and velocity.
    gain is a number k (K = k I) or an m by m matrix K.
    """
    q = [float(x) for x in q0]  # @line L1
    path = [q]
    for k in range(steps):  # @line L2
        t = k * dt  # @line L3
        e = rbm.sub(xd(t), fk(q))  # @line L4
        j = jac(q)  # @line L5
        v = rbm.add(xd_dot(t), _gain_times(gain, e))  # @line L6
        qdot = joint_rate(j, v)  # @line L7
        q = [x + dt * d for x, d in zip(q, qdot)]  # @line L8
        path.append(q)
    return path  # @line L9
