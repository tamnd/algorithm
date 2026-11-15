# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neural-collaborative-filtering/. The authors are listed in prov/9XDZVT.jsonl.

"""NeuMF, the neural collaborative filtering model of He et al. (WWW 2017), by hand.

The score of (u, i) is

    g   = pG_u * qG_i                          (GMF part, elementwise product)
    z_0 = [pM_u ; qM_i]                        (MLP part, concatenation)
    z_l = ReLU(W_l z_(l-1) + b_l)              for l = 1, ..., L
    s   = h . [g ; z_L],     y_hat = sigma(s)

and the loss of one example (u, i, y), with y in {0, 1}, is the log loss
-y ln y_hat - (1 - y) ln(1 - y_hat). The backward pass is written out by hand
and checked against finite differences in the tests. Training is plain SGD
with q negatives per positive, drawn uniformly from the unused items of the
user in each epoch. The paper trains with Adam and pre-trains the two parts;
this module does neither, to stay short.

Parameters are a dict of 2-D lists (vectors are 1 x d rows).
"""

import math
import random

Matrix = list[list[float]]
Params = dict[str, Matrix]


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def softplus(z: float) -> float:
    """ln(1 + e^z) without overflow."""
    return z + math.log1p(math.exp(-z)) if z > 0 else math.log1p(math.exp(z))


def init(m: int, n: int, k: int, hidden: list[int], seed: int = 1, scale: float = 0.1) -> Params:
    """Gaussian start. hidden lists the widths of the ReLU layers. Cost O((m + n) k + sum of layer sizes)."""
    rng = random.Random(seed)

    def mat(r: int, c: int) -> Matrix:
        return [[rng.gauss(0.0, scale) for _ in range(c)] for _ in range(r)]

    p = {"PG": mat(m, k), "QG": mat(n, k), "PM": mat(m, k), "QM": mat(n, k)}  # @line L1
    width = 2 * k
    for l, w in enumerate(hidden):
        p[f"W{l}"] = mat(w, width)
        p[f"b{l}"] = mat(1, w)
        width = w
    p["h"] = mat(1, k + width)
    return p


def layers(p: Params) -> int:
    return sum(1 for name in p if name.startswith("W"))


def forward(p: Params, u: int, i: int) -> tuple[float, dict]:
    """The logit s and a cache for the backward pass. Cost O(k + sum of W_l sizes)."""
    g = [a * b for a, b in zip(p["PG"][u], p["QG"][i])]  # @line L8
    z = p["PM"][u] + p["QM"][i]  # @line L9
    zs, pre = [z], []
    for l in range(layers(p)):  # @line L10
        w, b = p[f"W{l}"], p[f"b{l}"][0]
        a = [sum(wr[c] * z[c] for c in range(len(z))) + b[r] for r, wr in enumerate(w)]
        z = [max(0.0, v) for v in a]
        pre.append(a)
        zs.append(z)
    phi = g + z
    s = sum(a * b for a, b in zip(p["h"][0], phi))  # @line L11
    return s, {"u": u, "i": i, "g": g, "zs": zs, "pre": pre, "phi": phi}


def score(p: Params, u: int, i: int) -> float:
    """y_hat = sigma(s)."""
    return sigmoid(forward(p, u, i)[0])


def loss(p: Params, examples: list[tuple[int, int, int]]) -> float:
    """The sum of the log losses of the examples. Cost O(len(examples)) forward passes."""
    total = 0.0
    for u, i, y in examples:
        s = forward(p, u, i)[0]
        total += softplus(-s) if y == 1 else softplus(s)
    return total


def backward(p: Params, cache: dict, ds: float, grads: dict) -> None:
    """Add the gradient of the loss to grads, given ds = dloss/ds. Cost of one forward pass."""
    k = len(p["PG"][0])
    u, i, phi = cache["u"], cache["i"], cache["phi"]
    h = p["h"][0]
    for c in range(len(h)):
        grads["h"][0][c] += ds * phi[c]
    dphi = [ds * v for v in h]
    dg, dz = dphi[:k], dphi[k:]
    for c in range(k):
        grads["PG"][u][c] += dg[c] * p["QG"][i][c]
        grads["QG"][i][c] += dg[c] * p["PG"][u][c]
    for l in range(layers(p) - 1, -1, -1):
        a, zin, w = cache["pre"][l], cache["zs"][l], p[f"W{l}"]
        da = [d if v > 0 else 0.0 for d, v in zip(dz, a)]
        gw, gb = grads[f"W{l}"], grads[f"b{l}"][0]
        for r in range(len(w)):
            gb[r] += da[r]
            for c in range(len(zin)):
                gw[r][c] += da[r] * zin[c]
        dz = [sum(w[r][c] * da[r] for r in range(len(w))) for c in range(len(zin))]
    for c in range(k):
        grads["PM"][u][c] += dz[c]
        grads["QM"][i][c] += dz[k + c]


def zeros_like(p: Params) -> Params:
    return {name: [[0.0] * len(row) for row in mat] for name, mat in p.items()}


def gradient(p: Params, examples: list[tuple[int, int, int]]) -> Params:
    """The gradient of loss(p, examples). d(log loss)/ds = sigma(s) - y."""
    grads = zeros_like(p)
    for u, i, y in examples:
        s, cache = forward(p, u, i)
        backward(p, cache, sigmoid(s) - y, grads)
    return grads


def train(
    pairs: set[tuple[int, int]],
    m: int,
    n: int,
    k: int,
    hidden: list[int],
    epochs: int,
    rate: float,
    negatives: int = 4,
    seed: int = 1,
) -> Params:
    """SGD on the log loss with negative sampling.

    Precondition: every user with a positive pair has an unused item.
    Cost O(epochs |S| (1 + negatives) c), with c the cost of one forward pass.
    """
    rng = random.Random(seed)
    p = init(m, n, k, hidden, seed)
    used: dict[int, set[int]] = {}
    for u, i in pairs:
        used.setdefault(u, set()).add(i)
    free = {u: [j for j in range(n) if j not in s] for u, s in used.items()}
    if any(not f for f in free.values()):
        raise ValueError("a user has used every item")
    for _ in range(epochs):  # @line L2
        data = [(u, i, 1) for u, i in sorted(pairs)]  # @line L3
        for u, _i in sorted(pairs):
            data.extend((u, rng.choice(free[u]), 0) for _ in range(negatives))
        rng.shuffle(data)
        for u, i, y in data:  # @line L4
            s, cache = forward(p, u, i)  # @line L5
            g = zeros_like_used(p, u, i)
            backward(p, cache, sigmoid(s) - y, g)
            step(p, g, u, i, rate)  # @line L6
    return p  # @line L7


def zeros_like_used(p: Params, u: int, i: int) -> dict:
    """A gradient buffer for one example.

    The dense weights get full zero matrices. The embedding tables get only
    the row of u or of i, as a dict {row: zeros}, so the cost does not grow
    with m and n.
    """
    out: dict = {name: [[0.0] * len(row) for row in mat] for name, mat in p.items() if name not in EMB}
    for name, row in (("PG", u), ("PM", u), ("QG", i), ("QM", i)):
        out[name] = {row: [0.0] * len(p[name][0])}
    return out


EMB = ("PG", "QG", "PM", "QM")


def step(p: Params, g: dict, u: int, i: int, rate: float) -> None:
    """p -= rate * g on the dense weights and on the rows of u and i."""
    for name, mat in p.items():
        if name in ("PG", "PM"):
            rows = [u]
        elif name in ("QG", "QM"):
            rows = [i]
        else:
            rows = list(range(len(mat)))
        for r in rows:
            gr = g[name][r]
            pr = mat[r]
            for c in range(len(pr)):
                pr[c] -= rate * gr[c]


def recommend(p: Params, u: int, used: set[int], n: int, top: int) -> list[int]:
    """The top items by score among the unused ones. Cost O(n) forward passes."""
    scored = sorted((-forward(p, u, i)[0], i) for i in range(n) if i not in used)
    return [i for _, i in scored[:top]]
