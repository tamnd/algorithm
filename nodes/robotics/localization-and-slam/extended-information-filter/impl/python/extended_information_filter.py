# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-information-filter/. The authors are listed in prov/DYEYTV.jsonl.

"""The extended information filter (EIF), after Thrun, Burgard and Fox (2005), Section 3.5.

The belief N(mu, Sigma) is stored as the information matrix Omega = Sigma^(-1)
and the information vector xi = Omega mu. The models are

  x_t = g(u_t, x_{t-1}) + noise N(0, R_t)
  z   = h(x_t) + noise N(0, Q)

The filter linearizes g at the mean of the last belief and h at the
predicted mean, as the EKF does. With the same linearization points the two
filters give the same belief, up to rounding.

Matrices are lists of rows. The functions return new lists and do not change
their arguments.
"""

import rbm


def to_information(mu, sigma):
    """Return (xi, Omega) of the belief N(mu, Sigma)."""
    omega = rbm.inv(sigma)
    return rbm.matvec(omega, mu), omega


def to_moments(xi, omega):
    """Return (mu, Sigma) of the belief with information (xi, Omega)."""
    sigma = rbm.inv(omega)
    return rbm.matvec(sigma, xi), sigma


def recover_mean(xi, omega):
    """Return mu = Omega^(-1) xi by one linear solve."""
    return rbm.solve(omega, xi)


def predict(xi, omega, u, g, gjac, r):
    """Return (xi_bar, Omega_bar, mu_bar) after the motion: lines L1 to L5.

    g(u, x) is the motion model, gjac(u, x) its Jacobian with respect to x,
    and r the covariance of the motion noise in state coordinates. The step
    needs the mean and the inverse of Omega, so it costs O(n^3).
    """
    mu = recover_mean(xi, omega)  # @line L1
    gm = gjac(u, mu)  # @line L2
    sigma = rbm.inv(omega)
    omega_bar = rbm.inv(rbm.add(rbm.mul(rbm.mul(gm, sigma), rbm.transpose(gm)), r))  # @line L3
    omega_bar = symmetrize(omega_bar)
    mu_bar = g(u, mu)  # @line L4
    xi_bar = rbm.matvec(omega_bar, mu_bar)  # @line L5
    return xi_bar, omega_bar, mu_bar


def update(xi, omega, mu_bar, z, h, hjac, q, residual=None):
    """Return (xi, Omega) after one reading z: lines L7 to L9.

    h(x) is the measurement model and hjac(x) its Jacobian, both evaluated
    at the predicted mean mu_bar. residual(z, zhat) gives z - zhat, for
    example with a wrapped angle; by default it is the plain difference.
    Only the columns where the Jacobian is not zero take part, so a reading
    that depends on k state entries changes only a k by k block of Omega
    and k entries of xi.
    """
    n = len(xi)
    d = len(z)
    hm = hjac(mu_bar)  # @line L7
    cols = [c for c in range(n) if any(hm[a][c] != 0.0 for a in range(d))]
    hs = [[hm[a][c] for c in cols] for a in range(d)]
    qinv = rbm.inv(q)
    zhat = h(mu_bar)
    nu = residual(z, zhat) if residual is not None else rbm.sub(z, zhat)
    hmu = [sum(hs[a][k] * mu_bar[c] for k, c in enumerate(cols)) for a in range(d)]
    target = rbm.add(nu, hmu)  # z - h(mu_bar) + H mu_bar
    hq = rbm.mul(rbm.transpose(hs), qinv)  # k by d
    info = rbm.mul(hq, hs)
    vec = rbm.matvec(hq, target)
    omega = [list(row) for row in omega]
    xi = list(xi)
    for a, ca in enumerate(cols):
        for b, cb in enumerate(cols):
            omega[ca][cb] += info[a][b]  # @line L8
        xi[ca] += vec[a]  # @line L9
    return xi, omega


def eif(xi, omega, u, zs, g, gjac, r, h, hjac, q, residual=None):
    """One step of the EIF: lines L1 to L10.

    zs is a list of readings. h(x, i) and hjac(x, i) are the model of
    reading i and its Jacobian. All readings are linearized at the
    predicted mean, so their order does not matter.
    """
    xi, omega, mu_bar = predict(xi, omega, u, g, gjac, r)
    for i, z in enumerate(zs):  # @line L6
        xi, omega = update(xi, omega, mu_bar, z, lambda x, i=i: h(x, i), lambda x, i=i: hjac(x, i), q, residual)
    return xi, omega  # @line L10


def symmetrize(a):
    """Return (A + A^T) / 2, to remove rounding asymmetry."""
    n = len(a)
    return [[(a[i][j] + a[j][i]) / 2.0 for j in range(n)] for i in range(n)]
