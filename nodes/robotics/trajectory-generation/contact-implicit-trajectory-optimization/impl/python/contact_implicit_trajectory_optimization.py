# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contact-implicit-trajectory-optimization/. The authors are listed in prov/YCM0CN.jsonl.
"""Contact-implicit trajectory optimization for a point mass above the ground.

A point of unit mass moves on a vertical line, with height q >= 0 above the
ground. It has a thrust u and feels gravity g and a contact force lam from
the ground. The time-stepping model with step h is

    v_(k+1) = v_k + h (u_k - g + lam_k),    q_(k+1) = q_k + h v_(k+1),
    0 <= q_(k+1)  complementary to  lam_k >= 0,

so the ground can push only while the mass touches it. The task: start at
rest on the ground and be at rest at height H after N steps, with the least
thrust energy (h/2) sum u_k^2. The contact forces are decision variables,
so the optimizer decides when the mass leaves the ground.

The velocities are eliminated: v_(k+1) = (q_(k+1) - q_k)/h, and the thrust
is the linear function u_k = (q_(k+1) - 2 q_k + q_(k-1))/h^2 + g - lam_k with
q_(-1) = q_0 = 0 (rest on the ground). The end at rest at height H fixes
q_(N-1) = q_N = H. The variables are x = (q_1, ..., q_(N-2), lam_0, ...,
lam_(N-1)).

The complementarity is relaxed to q_(k+1) lam_k <= eps, and the relaxed
problem is solved by a log barrier with Newton steps. The relaxation eps and
the barrier weight mu go to zero together, and each stage starts from the
answer of the stage before.
"""

import math

G = 9.81


class Problem:
    def __init__(self, n_steps=10, h=0.1, height=0.5, g=G, contact=True):
        """contact=False drops the complementarity and keeps only q >= 0 and lam >= 0."""
        if n_steps < 3:
            raise ValueError("need at least three steps")
        self.N, self.h, self.H, self.g = n_steps, h, height, g
        self.nq = n_steps - 2  # free heights q_1 .. q_(N-2)
        self.nx = self.nq + n_steps
        self.contact = contact

    def pairs(self):
        """The steps k whose pair (q_(k+1), lam_k) carries a complementarity constraint."""
        return range(self.N) if self.contact else range(0)

    def heights(self, x):
        """q_(-1), q_0, ..., q_N as a list of length N + 2."""
        return [0.0, 0.0] + list(x[:self.nq]) + [self.H, self.H]

    def forces(self, x):
        return list(x[self.nq:])

    def thrust(self, x):
        q, lam, h = self.heights(x), self.forces(x), self.h
        return [(q[k + 2] - 2.0 * q[k + 1] + q[k]) / h ** 2 + self.g - lam[k] for k in range(self.N)]

    def thrust_jacobian(self):
        """u = M x + c, so du_k/dx_j = M[k][j]."""
        m = [[0.0] * self.nx for _ in range(self.N)]
        h2 = self.h ** 2
        for k in range(self.N):
            for idx, coef in ((k + 1, 1.0), (k, -2.0), (k - 1, 1.0)):  # q_(k+1), q_k, q_(k-1)
                if 1 <= idx <= self.nq:
                    m[k][idx - 1] += coef / h2
            m[k][self.nq + k] = -1.0
        return m

    def energy(self, x):
        return 0.5 * self.h * sum(u * u for u in self.thrust(x))

    def gap(self, x, k):
        """The height q_(k+1) at the end of step k, which pairs with lam_k."""
        return self.heights(x)[k + 2]

    def gap_index(self, k):
        """Index of q_(k+1) in x, or None if it is fixed."""
        return k if k + 1 <= self.nq else None

    def complementarity(self, x):
        """The largest product q_(k+1) lam_k; zero exactly when the contact is physical."""
        lam = self.forces(x)
        return max(self.gap(x, k) * lam[k] for k in range(self.N))


def cholesky(a):
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    return None
                low[i][i] = math.sqrt(s)
            else:
                low[i][j] = s / low[j][j]
    return low


def chol_solve(low, b):
    n = len(low)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(low[i][k] * y[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(low[k][i] * x[k] for k in range(i + 1, n))) / low[i][i]
    return x


def feasible(prob, x, eps):
    """Strict feasibility for the barrier: q > 0, lam > 0, q lam < eps."""
    if any(v <= 0.0 for v in x):
        return False
    lam = prob.forces(x)
    return all(prob.gap(x, k) * lam[k] < eps for k in prob.pairs())


def barrier(prob, x, eps, mu):
    lam = prob.forces(x)
    s = sum(math.log(v) for v in x)
    s += sum(math.log(eps - prob.gap(x, k) * lam[k]) for k in prob.pairs())
    return prob.energy(x) - mu * s


def barrier_derivatives(prob, x, eps, mu, m):
    n, h = prob.nx, prob.h
    u = prob.thrust(x)
    grad = [h * sum(m[k][j] * u[k] for k in range(prob.N)) for j in range(n)]
    hess = [[h * sum(m[k][i] * m[k][j] for k in range(prob.N)) for j in range(n)] for i in range(n)]
    for j in range(n):
        grad[j] -= mu / x[j]
        hess[j][j] += mu / x[j] ** 2
    lam = prob.forces(x)
    for k in prob.pairs():
        q, l_ = prob.gap(x, k), lam[k]
        s = eps - q * l_
        il, iq = prob.nq + k, prob.gap_index(k)
        # -mu log(eps - q lam): gradient mu (lam, q)/s, Hessian mu/s^2 [[lam^2, eps], [eps, q^2]].
        grad[il] += mu * q / s
        hess[il][il] += mu * q * q / s ** 2
        if iq is not None:
            grad[iq] += mu * l_ / s
            hess[iq][iq] += mu * l_ * l_ / s ** 2
            hess[iq][il] += mu * eps / s ** 2
            hess[il][iq] += mu * eps / s ** 2
    return grad, hess


def newton(prob, x, eps, mu, m, iters=100, tol=1e-10):
    for _ in range(iters):  # @line L4
        grad, hess = barrier_derivatives(prob, x, eps, mu, m)
        tau, low = 0.0, cholesky(hess)  # @line L5
        while low is None:
            tau = max(10.0 * tau, 1e-8)
            low = cholesky([[hess[i][j] + (tau if i == j else 0.0) for j in range(len(x))] for i in range(len(x))])
        d = chol_solve(low, [-v for v in grad])  # @line L6
        dec = -sum(a * b for a, b in zip(grad, d))
        if dec / 2.0 < tol:  # @line L8
            break
        phi, s = barrier(prob, x, eps, mu), 1.0
        while True:  # @line L7
            xn = [a + s * b for a, b in zip(x, d)]
            if feasible(prob, xn, eps) and barrier(prob, xn, eps, mu) <= phi - 1e-4 * s * dec:
                x = xn
                break
            s *= 0.5
            if s < 1e-16:
                return x
    return x


def initial_point(prob, eps):
    q = [prob.H * (k / (prob.N - 1)) for k in range(1, prob.nq + 1)]
    x = q + [0.0] * prob.N
    for k in range(prob.N):
        x[prob.nq + k] = min(1.0, 0.5 * eps / prob.gap(x, k))
    return x


def contact_implicit(prob, eps0=0.1, mu0=0.1, kappa=4.0, eps_min=1e-7, x0=None, log=None):
    """Returns x. log, if given, receives (eps, mu, energy, complementarity) after each stage."""
    m = prob.thrust_jacobian()
    eps, mu = eps0, mu0  # @line L1
    x = initial_point(prob, eps) if x0 is None else list(x0)  # @line L2
    if not feasible(prob, x, eps):
        raise ValueError("start is not strictly feasible")
    while True:  # @line L3
        x = newton(prob, x, eps, mu, m)
        if log is not None:
            log.append((eps, mu, prob.energy(x), prob.complementarity(x)))
        if eps < eps_min:  # @line L9
            return x
        eps, mu = eps / kappa, mu / kappa  # @line L10
        x = restore(prob, x, eps)  # @line L11


def restore(prob, x, eps):
    """Make x strictly feasible for a smaller eps: in each pair with q lam >= eps,
    shrink the smaller of the two (the gap in contact, the force in flight)."""
    x = list(x)
    lam = prob.forces(x)
    for k in prob.pairs():
        q, iq = prob.gap(x, k), prob.gap_index(k)
        if q * lam[k] < eps:
            continue
        if iq is not None and q < lam[k]:
            x[iq] = 0.5 * eps / lam[k]
        else:
            x[prob.nq + k] = 0.5 * eps / q
    return x


def simulate(prob, thrust):
    """Forward simulation with exact contact: the ground force is the smallest that keeps q >= 0."""
    q, v, qs, lams = 0.0, 0.0, [0.0], []
    for u in thrust:
        v_free = v + prob.h * (u - prob.g)
        q_free = q + prob.h * v_free
        lam = 0.0 if q_free >= 0.0 else -q_free / prob.h ** 2
        v = v_free + prob.h * lam
        q = q + prob.h * v
        qs.append(q)
        lams.append(lam)
    return qs, lams
