# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sasrec/. The authors are listed in prov/QW5Y7Z.jsonl.

"""SASRec (Kang and McAuley, ICDM 2018) with one block, by hand.

For a sequence s_0, ..., s_(T-1) of items (row vectors of length d):

    E_t = M[s_t] + P[t]                                   (Equation 1)
    X   = LN1(E),  Q = X WQ,  K = X WK,  V = X WV
    A_t = softmax over u <= t of Q_t . K_u / sqrt(d)      (causal, Equations 2 and 3)
    S_t = E_t + sum_(u <= t) A_(t,u) V_u                  (residual)
    F_t = S_t + ReLU(LN2(S_t) W1 + c1) W2 + c2            (Equation 4, residual)
    r_(i,t) = F_t . M[i]                                  (Equation 6, shared M)

LN is layer normalization with gain and bias. The loss of Section III-E is the
binary cross entropy with the next item as positive and one negative item per
step. The backward pass, including layer normalization and the softmax, is
written by hand and checked against finite differences in the tests.

Differences from the paper, kept to stay short: one block and one head, no
dropout, plain SGD in place of Adam, and no left padding (a sequence of
length T uses positions 0 to T - 1).
"""

import math
import random

Matrix = list[list[float]]
Params = dict[str, Matrix]
EPS = 1e-8


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def softplus(z: float) -> float:
    """ln(1 + e^z) without overflow."""
    return z + math.log1p(math.exp(-z)) if z > 0 else math.log1p(math.exp(z))


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def vecmat(v: list[float], w: Matrix) -> list[float]:
    """v W for a row vector v."""
    out = [0.0] * len(w[0])
    for a, row in zip(v, w):
        if a != 0.0:
            for c, x in enumerate(row):
                out[c] += a * x
    return out


def matvec(w: Matrix, v: list[float]) -> list[float]:
    """W v, which is v W^T as a row."""
    return [dot(row, v) for row in w]


def outer_add(g: Matrix, a: list[float], b: list[float]) -> None:
    """g += a^T b."""
    for r, x in enumerate(a):
        if x != 0.0:
            row = g[r]
            for c, y in enumerate(b):
                row[c] += x * y


def init(n_items: int, d: int, n_pos: int, seed: int = 1, scale: float = 0.3) -> Params:
    """Gaussian start, unit gains, zero biases. Cost O(n_items d + n_pos d + d^2)."""
    rng = random.Random(seed)

    def mat(r: int, c: int) -> Matrix:
        return [[rng.gauss(0.0, scale) for _ in range(c)] for _ in range(r)]

    return {
        "M": mat(n_items, d), "P": mat(n_pos, d),
        "g1": [[1.0] * d], "b1": [[0.0] * d],
        "WQ": mat(d, d), "WK": mat(d, d), "WV": mat(d, d),
        "g2": [[1.0] * d], "b2": [[0.0] * d],
        "W1": mat(d, d), "c1": [[0.0] * d], "W2": mat(d, d), "c2": [[0.0] * d],
    }


def layer_norm(x: list[float], g: list[float], b: list[float]) -> tuple[list[float], list[float], float]:
    """g * (x - mean) / sqrt(var + EPS) + b, with the normalized x and 1/sqrt(var + EPS)."""
    d = len(x)
    mu = sum(x) / d
    var = sum((v - mu) ** 2 for v in x) / d
    rstd = 1.0 / math.sqrt(var + EPS)
    xhat = [(v - mu) * rstd for v in x]
    return [a * h + c for a, h, c in zip(g, xhat, b)], xhat, rstd


def layer_norm_back(dy: list[float], xhat: list[float], rstd: float, g: list[float], dg: list[float], db: list[float]) -> list[float]:
    """Adds the gain and bias gradients; returns the gradient in x."""
    d = len(dy)
    dxhat = [a * b for a, b in zip(dy, g)]
    for c in range(d):
        dg[c] += dy[c] * xhat[c]
        db[c] += dy[c]
    m1 = sum(dxhat) / d
    m2 = sum(a * b for a, b in zip(dxhat, xhat)) / d
    return [rstd * (a - m1 - h * m2) for a, h in zip(dxhat, xhat)]


def forward(p: Params, seq: list[int]) -> tuple[Matrix, dict]:
    """The outputs F_t for every position, and a cache. Cost O(T^2 d + T d^2)."""
    d = len(p["M"][0])
    scale = 1.0 / math.sqrt(d)
    e = [[a + b for a, b in zip(p["M"][s], p["P"][t])] for t, s in enumerate(seq)]  # @line L9
    ln1 = [layer_norm(row, p["g1"][0], p["b1"][0]) for row in e]  # @line L10
    x = [r[0] for r in ln1]
    q = [vecmat(row, p["WQ"]) for row in x]
    k = [vecmat(row, p["WK"]) for row in x]
    v = [vecmat(row, p["WV"]) for row in x]
    att, s = [], []
    for t in range(len(seq)):
        z = [dot(q[t], k[u]) * scale for u in range(t + 1)]  # @line L11
        top = max(z)
        w = [math.exp(a - top) for a in z]
        tot = sum(w)
        a = [x_ / tot for x_ in w]
        att.append(a)
        o = [sum(a[u] * v[u][c] for u in range(t + 1)) for c in range(d)]
        s.append([x_ + y for x_, y in zip(e[t], o)])  # @line L12
    ln2 = [layer_norm(row, p["g2"][0], p["b2"][0]) for row in s]
    y = [r[0] for r in ln2]
    pre = [[a + b for a, b in zip(vecmat(row, p["W1"]), p["c1"][0])] for row in y]
    hid = [[max(0.0, a) for a in row] for row in pre]
    f = [[a + b + c for a, b, c in zip(srow, vecmat(hrow, p["W2"]), p["c2"][0])] for srow, hrow in zip(s, hid)]  # @line L13
    cache = {"seq": seq, "e": e, "ln1": ln1, "x": x, "q": q, "k": k, "v": v, "att": att,
             "s": s, "ln2": ln2, "y": y, "pre": pre, "hid": hid}
    return f, cache  # @line L14


def loss(p: Params, seq: list[int], pos: list[int], neg: list[int]) -> float:
    """Sum over t of -ln sigma(F_t . M[pos_t]) - ln(1 - sigma(F_t . M[neg_t]))."""
    f, _ = forward(p, seq)
    return sum(softplus(-dot(ft, p["M"][i])) + softplus(dot(ft, p["M"][j])) for ft, i, j in zip(f, pos, neg))


def zeros_like(p: Params) -> Params:
    return {name: [[0.0] * len(row) for row in mat] for name, mat in p.items()}


def loss_and_grad(p: Params, seq: list[int], pos: list[int], neg: list[int]) -> tuple[float, Params]:
    """The loss and its exact gradient in every parameter. Cost O(T^2 d + T d^2)."""
    d = len(p["M"][0])
    scale = 1.0 / math.sqrt(d)
    T = len(seq)
    f, c = forward(p, seq)
    g = zeros_like(p)
    total = 0.0
    df = []
    for t in range(T):
        mi, mj = p["M"][pos[t]], p["M"][neg[t]]
        lp, ln_ = dot(f[t], mi), dot(f[t], mj)
        total += softplus(-lp) + softplus(ln_)
        dp, dn = sigmoid(lp) - 1.0, sigmoid(ln_)
        df.append([dp * a + dn * b for a, b in zip(mi, mj)])
        for col in range(d):
            g["M"][pos[t]][col] += dp * f[t][col]
            g["M"][neg[t]][col] += dn * f[t][col]
    ds = []
    for t in range(T):
        dft = df[t]
        g["c2"][0] = [a + b for a, b in zip(g["c2"][0], dft)]
        outer_add(g["W2"], c["hid"][t], dft)
        dhid = matvec(p["W2"], dft)
        dpre = [a if b > 0 else 0.0 for a, b in zip(dhid, c["pre"][t])]
        g["c1"][0] = [a + b for a, b in zip(g["c1"][0], dpre)]
        outer_add(g["W1"], c["y"][t], dpre)
        dy = matvec(p["W1"], dpre)
        _, xhat, rstd = c["ln2"][t]
        dst = layer_norm_back(dy, xhat, rstd, p["g2"][0], g["g2"][0], g["b2"][0])
        ds.append([a + b for a, b in zip(dft, dst)])
    de = [row[:] for row in ds]
    dq = [[0.0] * d for _ in range(T)]
    dk = [[0.0] * d for _ in range(T)]
    dv = [[0.0] * d for _ in range(T)]
    for t in range(T):
        a, do = c["att"][t], ds[t]
        da = [dot(do, c["v"][u]) for u in range(t + 1)]
        for u in range(t + 1):
            for col in range(d):
                dv[u][col] += a[u] * do[col]
        mean = sum(x * y for x, y in zip(a, da))
        dz = [a[u] * (da[u] - mean) * scale for u in range(t + 1)]
        for u in range(t + 1):
            for col in range(d):
                dq[t][col] += dz[u] * c["k"][u][col]
                dk[u][col] += dz[u] * c["q"][t][col]
    for t in range(T):
        xt = c["x"][t]
        outer_add(g["WQ"], xt, dq[t])
        outer_add(g["WK"], xt, dk[t])
        outer_add(g["WV"], xt, dv[t])
        dx = [a + b + e for a, b, e in zip(matvec(p["WQ"], dq[t]), matvec(p["WK"], dk[t]), matvec(p["WV"], dv[t]))]
        _, xhat, rstd = c["ln1"][t]
        det = layer_norm_back(dx, xhat, rstd, p["g1"][0], g["g1"][0], g["b1"][0])
        de[t] = [a + b for a, b in zip(de[t], det)]
        for col in range(d):
            g["M"][seq[t]][col] += de[t][col]
            g["P"][t][col] += de[t][col]
    return total, g


def train(
    sequences: list[list[int]], n_items: int, d: int, epochs: int, rate: float, seed: int = 1
) -> Params:
    """SGD on the loss of Section III-E, one sequence at a time.

    Precondition: every sequence has at least 2 items and does not use every
    item. The model gets one position per input step of the longest sequence.
    Cost O(epochs sum_u (T_u^2 d + T_u d^2)), plus O(n_items d) per update.
    """
    rng = random.Random(seed)
    n_pos = max(len(s) for s in sequences) - 1
    if any(len(s) < 2 for s in sequences):
        raise ValueError("a sequence needs at least 2 items")
    free = [[j for j in range(n_items) if j not in set(s)] for s in sequences]
    if any(not f for f in free):
        raise ValueError("a sequence uses every item")
    p = init(n_items, d, n_pos, seed)  # @line L1
    for _ in range(epochs):  # @line L2
        order = list(range(len(sequences)))
        rng.shuffle(order)
        for u in order:  # @line L3
            s = sequences[u]
            inp, pos = s[:-1], s[1:]
            neg = [rng.choice(free[u]) for _ in inp]  # @line L4
            _, g = loss_and_grad(p, inp, pos, neg)  # @line L5
            for name, mat in p.items():  # @line L6
                for r, row in enumerate(mat):
                    gr = g[name][r]
                    for col in range(len(row)):
                        row[col] -= rate * gr[col]  # @line L7
    return p  # @line L8


def next_items(p: Params, seq: list[int], k: int, exclude_seen: bool = True) -> list[int]:
    """The k items with the highest r_(i,T) after the sequence.

    With exclude_seen, items of the sequence are left out, as the negatives of
    training never include them. Cost O(T^2 d + T d^2 + n d).
    """
    f, _ = forward(p, seq)
    last = f[-1]
    seen = set(seq) if exclude_seen else set()
    scores = [dot(last, m) for m in p["M"]]
    items = [i for i in range(len(scores)) if i not in seen]
    return sorted(items, key=lambda i: (-scores[i], i))[:k]
