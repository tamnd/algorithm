# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lista/. The authors are listed in prov/KG5S6M.jsonl.
"""Learned ISTA (LISTA) of Gregor and LeCun.

The network is given: a list of layers, each a triple (W_e, S, theta) with
W_e an n x m matrix, S an n x n matrix and theta a list of n thresholds.
Layer k maps x to soft(W_e y + S x, theta). With W_e = A^T / L,
S = I - A^T A / L and theta = lambda / L in every layer, K layers are
K steps of ISTA for the lasso (1/2)||A x - y||^2 + lambda ||x||_1.

Matrices are lists of rows. Vectors are lists of floats.
"""


def matvec(a, x):
    """The product A x."""
    return [sum(v * w for v, w in zip(row, x)) for row in a]


def soft(v, theta):
    """Soft thresholding: sign(v_i) max(|v_i| - theta_i, 0), entry by entry."""
    out = []
    for vi, ti in zip(v, theta):
        if vi > ti:
            out.append(vi - ti)
        elif vi < -ti:
            out.append(vi + ti)
        else:
            out.append(0.0)
    return out


def lista(y, layers):
    """Run the given layers on the data y and return the code x.

    layers is a list of K triples (W_e, S, theta). A network with tied
    weights repeats the same triple K times.
    Cost: K products with W_e (n m each) and with S (n^2 each).
    """
    n = len(layers[0][1])
    x = [0.0] * n  # @line L1
    for w_e, s, theta in layers:  # @line L2
        c = [a + b for a, b in zip(matvec(w_e, y), matvec(s, x))]  # @line L3
        x = soft(c, theta)  # @line L4
    return x  # @line L5


def ista_weights(a, lam, lip):
    """The triple (W_e, S, theta) for which one LISTA layer is one ISTA step.

    lip must be at least ||A||^2, the Lipschitz constant of the gradient of
    (1/2)||A x - y||^2.
    """
    m, n = len(a), len(a[0])
    w_e = [[a[i][j] / lip for i in range(m)] for j in range(n)]
    s = [[(1.0 if j == k else 0.0) - sum(a[i][j] * a[i][k] for i in range(m)) / lip
          for k in range(n)] for j in range(n)]
    return w_e, s, [lam / lip] * n


def ista(a, y, lam, lip, iters, x0=None):
    """Plain ISTA: x <- soft(x - A^T (A x - y) / lip, lam / lip), written from the gradient."""
    m, n = len(a), len(a[0])
    x = list(x0) if x0 is not None else [0.0] * n
    for _ in range(iters):
        r = [ax - yi for ax, yi in zip(matvec(a, x), y)]
        g = [sum(a[i][j] * r[i] for i in range(m)) for j in range(n)]
        x = soft([xj - gj / lip for xj, gj in zip(x, g)], [lam / lip] * n)
    return x


def lasso_objective(a, y, lam, x):
    """(1/2)||A x - y||^2 + lam ||x||_1."""
    r = [ax - yi for ax, yi in zip(matvec(a, x), y)]
    return 0.5 * sum(v * v for v in r) + lam * sum(abs(v) for v in x)


def lista_loss_and_grad(y, layers, target):
    """Loss (1/2)||x^K - target||^2 and its gradient in every weight, by backpropagation.

    Returns (loss, grads) with grads[k] = (dW_e, dS, dtheta) for layer k.
    Soft thresholding is not differentiable where |c_i| = theta_i; the
    formula uses the derivative of the active branch, which is right
    everywhere else.
    """
    n = len(layers[0][1])
    xs = [[0.0] * n]
    cs = []
    for w_e, s, theta in layers:
        c = [a + b for a, b in zip(matvec(w_e, y), matvec(s, xs[-1]))]
        cs.append(c)
        xs.append(soft(c, theta))
    g = [a - b for a, b in zip(xs[-1], target)]
    loss = 0.5 * sum(v * v for v in g)
    grads = [None] * len(layers)
    for k in range(len(layers) - 1, -1, -1):
        w_e, s, theta = layers[k]
        c, x_prev = cs[k], xs[k]
        dc = [gi if abs(ci) > ti else 0.0 for gi, ci, ti in zip(g, c, theta)]
        dtheta = [-gi * (1.0 if ci > 0 else -1.0) if abs(ci) > ti else 0.0
                  for gi, ci, ti in zip(g, c, theta)]
        d_we = [[dci * yj for yj in y] for dci in dc]
        d_s = [[dci * xj for xj in x_prev] for dci in dc]
        grads[k] = (d_we, d_s, dtheta)
        g = [sum(s[i][j] * dc[i] for i in range(n)) for j in range(n)]
    return loss, grads


def train_tied(data, layers_count, start, step, epochs):
    """Fit tied weights (W_e, S, theta) by full-batch gradient descent.

    data is a list of pairs (y, target). start is the initial triple, for
    example the ISTA weights. The gradient of tied weights is the sum of the
    gradients of the K copies. Returns the trained triple.
    """
    w_e = [row[:] for row in start[0]]
    s = [row[:] for row in start[1]]
    theta = list(start[2])
    for _ in range(epochs):
        gw = [[0.0] * len(w_e[0]) for _ in w_e]
        gs = [[0.0] * len(s[0]) for _ in s]
        gt = [0.0] * len(theta)
        for y, target in data:
            _, grads = lista_loss_and_grad(y, [(w_e, s, theta)] * layers_count, target)
            for d_we, d_s, dth in grads:
                for i, row in enumerate(d_we):
                    for j, v in enumerate(row):
                        gw[i][j] += v
                for i, row in enumerate(d_s):
                    for j, v in enumerate(row):
                        gs[i][j] += v
                for i, v in enumerate(dth):
                    gt[i] += v
        scale = step / len(data)
        w_e = [[v - scale * d for v, d in zip(row, drow)] for row, drow in zip(w_e, gw)]
        s = [[v - scale * d for v, d in zip(row, drow)] for row, drow in zip(s, gs)]
        theta = [max(0.0, v - scale * d) for v, d in zip(theta, gt)]
    return w_e, s, theta
