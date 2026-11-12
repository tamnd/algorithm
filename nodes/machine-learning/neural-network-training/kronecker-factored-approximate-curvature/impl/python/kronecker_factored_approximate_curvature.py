# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kronecker-factored-approximate-curvature/. The authors are listed in prov/CAQ103.jsonl.

"""K-FAC (Martens and Grosse 2015) for a tanh multilayer perceptron with a
softmax output and cross entropy loss, block diagonal version.

Layer l computes s_l = W_l abar_{l-1}, where abar is the input with a 1
appended (homogeneous coordinate). The Fisher block of W_l is approximated
by A_{l-1} kron G_l with A = E[abar abar^T] and G = E[g g^T], g the gradient
of log p(y|x) with respect to s_l for targets y sampled from the model.
vec stacks columns, so vec(g abar^T) = abar kron g and
(A kron G)^(-1) vec(V) = vec(G^(-1) V A^(-1)).

The step uses factored Tikhonov damping (Section 6.3), the rescaling by the
exact Fisher quadratic model (Section 6.4) and the Levenberg-Marquardt rule
for lambda (Section 6.5). Matrices are lists of rows; the helpers work for
floats and Fractions.
"""

import math


# ---------- matrix helpers ----------

def identity(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(r) for r in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(r, c)) for c in bt] for r in a]


def outer(u, v):
    return [[a * b for b in v] for a in u]


def kron(a, b):
    """Kronecker product: block (i, j) is a[i][j] * b."""
    p, q = len(b), len(b[0])
    return [[a[i // p][j // q] * b[i % p][j % q] for j in range(len(a[0]) * q)] for i in range(len(a) * p)]


def vec(x):
    """Stack the columns of x."""
    return [x[i][j] for j in range(len(x[0])) for i in range(len(x))]


def unvec(v, n, m):
    return [[v[j * n + i] for j in range(m)] for i in range(n)]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def solve(a, b):
    """Solve a x = b for a matrix b by Gaussian elimination with partial pivoting."""
    n = len(a)
    m = [list(a[i]) + list(b[i]) for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ZeroDivisionError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [[x / m[i][i] for x in m[i][n:]] for i in range(n)]


def inverse(a):
    return solve(a, identity(len(a)))


# ---------- the network ----------

def softmax(z):
    top = max(z)
    e = [math.exp(v - top) for v in z]
    s = sum(e)
    return [v / s for v in e]


def init_mlp(sizes, rng):
    """W_l has shape sizes[l+1] x (sizes[l] + 1); the last column is the bias."""
    return [[[rng.gauss(0, 1 / math.sqrt(sizes[l] + 1)) for _ in range(sizes[l])] + [0.0]
             for _ in range(sizes[l + 1])] for l in range(len(sizes) - 1)]


def forward(ws, x):
    """Returns the layer inputs abar_0..abar_{L-1} and the output probabilities."""
    abar, a = [], list(x)
    for l, w in enumerate(ws):
        ab = a + [1.0]
        abar.append(ab)
        s = [sum(wij * aj for wij, aj in zip(row, ab)) for row in w]
        a = [math.tanh(v) for v in s] if l < len(ws) - 1 else s
    return abar, softmax(a)


def backward(ws, abar, dlogits):
    """Backpropagate dL/ds_L. Returns the weight gradients g_l abar_{l-1}^T and the g_l."""
    gs = [None] * len(ws)
    g = list(dlogits)
    for l in range(len(ws) - 1, -1, -1):
        gs[l] = g
        if l > 0:
            a = abar[l][:-1]
            da = [sum(ws[l][i][j] * g[i] for i in range(len(g))) for j in range(len(a))]
            g = [d * (1 - v * v) for d, v in zip(da, a)]
    return [outer(gs[l], abar[l]) for l in range(len(ws))], gs


def loss(ws, batch, eta=0.0):
    """Mean cross entropy plus (eta / 2) ||theta||^2."""
    total = sum(-math.log(forward(ws, x)[1][y]) for x, y in batch) / len(batch)
    return total + 0.5 * eta * sum(v * v for w in ws for row in w for v in row)


def loss_grad(ws, batch, eta=0.0):
    grads = [[[eta * v for v in row] for row in w] for w in ws]
    for x, y in batch:
        abar, p = forward(ws, x)
        d = [pk - (1.0 if k == y else 0.0) for k, pk in enumerate(p)]
        gw, _ = backward(ws, abar, d)
        for l in range(len(ws)):
            for i, row in enumerate(gw[l]):
                for j, v in enumerate(row):
                    grads[l][i][j] += v / len(batch)
    return grads


def factor_stats(ws, batch, rng):
    """A_l = mean abar abar^T and G_l = mean g g^T with y sampled from the model."""
    A = [[[0.0] * len(w[0]) for _ in w[0]] for w in ws]
    G = [[[0.0] * len(w) for _ in w] for w in ws]
    for x, _ in batch:
        abar, p = forward(ws, x)
        u, y, acc = rng.random(), len(p) - 1, 0.0
        for k, pk in enumerate(p):
            acc += pk
            if u < acc:
                y = k
                break
        _, gs = backward(ws, abar, [pk - (1.0 if k == y else 0.0) for k, pk in enumerate(p)])
        for l in range(len(ws)):
            for M, v in ((A[l], abar[l]), (G[l], gs[l])):
                for i in range(len(v)):
                    for j in range(len(v)):
                        M[i][j] += v[i] * v[j] / len(batch)
    return A, G


def damping_pi(a, g):
    """pi = sqrt((tr A / dim A) / (tr G / dim G)), which minimizes the trace
    norm of the cross terms of the factored damping."""
    ta, tg = trace(a) / len(a), trace(g) / len(g)
    return math.sqrt(ta / tg) if ta > 0 and tg > 0 else 1.0


def kfac_direction(grads, A, G, gamma2):
    """Delta_l = -(G_l + (gamma/pi) I)^(-1) grad_l (A_l + pi gamma I)^(-1), gamma = sqrt(gamma2)."""
    out = []
    c = math.sqrt(gamma2)
    for gw, a, g in zip(grads, A, G):
        pi = damping_pi(a, g)
        ad = [[a[i][j] + (pi * c if i == j else 0.0) for j in range(len(a))] for i in range(len(a))]
        gd = [[g[i][j] + (c / pi if i == j else 0.0) for j in range(len(g))] for i in range(len(g))]
        x = solve(gd, gw)
        u = transpose(solve(ad, transpose(x)))
        out.append([[-v for v in row] for row in u])
    return out


def fisher_quadratic(ws, batch, dws):
    """d^T F d for the exact Fisher of the softmax output, via a forward tangent:
    mean over x of sdot^T (diag p - p p^T) sdot, sdot = J d."""
    total = 0.0
    for x, _ in batch:
        a, da = list(x), [0.0] * len(x)
        for l, (w, dw) in enumerate(zip(ws, dws)):
            ab, dab = a + [1.0], da + [0.0]
            s = [sum(p * q for p, q in zip(row, ab)) for row in w]
            ds = [sum(p * q for p, q in zip(drow, ab)) + sum(p * q for p, q in zip(row, dab))
                  for row, drow in zip(w, dw)]
            if l < len(ws) - 1:
                a = [math.tanh(v) for v in s]
                da = [(1 - v * v) * d for v, d in zip(a, ds)]
        p = softmax(s)
        mean = sum(pk * dk for pk, dk in zip(p, ds))
        total += sum(pk * dk * dk for pk, dk in zip(p, ds)) - mean * mean
    return total / len(batch)


def _dot(a, b):
    return sum(x * y for wa, wb in zip(a, b) for ra, rb in zip(wa, wb) for x, y in zip(ra, rb))


def kfac(ws, data, steps, rng, batch_size=32, lam=1.0, eta=1e-5, t1=5):
    """Run K-FAC. Returns the final weights and the list of minibatch losses."""
    A = G = None  # @line L1
    omega = (19 / 20) ** t1
    history = []
    for k in range(1, steps + 1):  # @line L2
        batch = rng.sample(data, min(batch_size, len(data)))  # @line L3
        h0 = loss(ws, batch, eta)
        grads = loss_grad(ws, batch, eta)  # @line L4
        a_new, g_new = factor_stats(ws, batch, rng)  # @line L5
        e = min(1 - 1 / k, 0.95)
        if A is None:
            A, G = a_new, g_new
        else:
            A = [[[e * x + (1 - e) * y for x, y in zip(r1, r2)] for r1, r2 in zip(m1, m2)] for m1, m2 in zip(A, a_new)]
            G = [[[e * x + (1 - e) * y for x, y in zip(r1, r2)] for r1, r2 in zip(m1, m2)] for m1, m2 in zip(G, g_new)]  # @line L6
        delta = kfac_direction(grads, A, G, lam + eta)  # @line L7
        gd, dd = _dot(grads, delta), _dot(delta, delta)
        dfd = fisher_quadratic(ws, batch, delta)
        alpha = -gd / (dfd + (lam + eta) * dd)  # @line L8
        new = [[[v + alpha * d for v, d in zip(r, dr)] for r, dr in zip(w, dw)] for w, dw in zip(ws, delta)]  # @line L9
        if k % t1 == 0:
            model = alpha * gd + 0.5 * alpha * alpha * (dfd + eta * dd)
            rho = (loss(new, batch, eta) - h0) / model if model < 0 else 0.0
            if rho > 0.75:
                lam *= omega
            elif rho < 0.25:
                lam /= omega  # @line L10
        ws = new
        history.append(h0)
    return ws, history  # @line L11
