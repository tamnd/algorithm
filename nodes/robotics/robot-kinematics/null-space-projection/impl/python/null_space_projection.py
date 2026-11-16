# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/null-space-projection/. The authors are listed in prov/SA0J6T.jsonl.
"""Null-space projection of a secondary joint velocity.

J is an m by n task Jacobian of full row rank (m < n for a redundant arm).

- projector(j) returns P = I - J^+ J with J^+ = J^T (J J^T)^-1.
- null_space_step(j, xdot, z) returns q' = J^+ x' + P z, the joint
  velocity closest to z among all joint velocities with J q' = x'.
- gradient_projection_run(...) integrates q' = J^+ (K e) + P (-k0 grad h)
  with explicit Euler steps: the task point is held (or pulled back) by the
  first term, and the secondary cost h(q) decreases through the second
  term (the gradient projection of Liegeois, 1977).

Matrices are lists of rows.
"""

import rbm


def projector(j):
    """Return the n by n matrix I - J^+ J."""
    jp = rbm.pinv_right(j)
    return rbm.sub(rbm.eye(len(j[0])), rbm.mul(jp, j))


def null_space_step(j, xdot, z):
    """Return J^+ x' + (I - J^+ J) z."""
    jp = rbm.pinv_right(j)  # @line L1
    p = rbm.sub(rbm.eye(len(j[0])), rbm.mul(jp, j))  # @line L2
    return rbm.add(rbm.matvec(jp, xdot), rbm.matvec(p, z))  # @line L3


def gradient_projection_run(fk, jac, grad_h, q0, x_d, gain, k0, dt, steps):
    """Return the joint path of q' = J^+ (gain (x_d - fk(q))) + P (-k0 grad h(q))."""
    q = [float(x) for x in q0]
    path = [q]
    for _ in range(steps):
        j = jac(q)
        e = rbm.sub(x_d, fk(q))
        z = [-k0 * g for g in grad_h(q)]
        qdot = null_space_step(j, [gain * x for x in e], z)
        q = [x + dt * d for x, d in zip(q, qdot)]
        path.append(q)
    return path
