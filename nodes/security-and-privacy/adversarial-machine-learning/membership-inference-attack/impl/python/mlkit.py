# SPDX-License-Identifier: MIT
# Shared helper of the security and privacy pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small vector tools, synthetic data and two tiny models for the adversarial machine learning pages.

Vectors are lists of floats. Every model here is synthetic: it is built from a seeded
random.Random and never from real data. The helper holds no attack loop, no
certification and no defense; those live in the slug files of the pages.
"""

import math
import random
from typing import Callable, Sequence

Vector = list[float]
Matrix = list[list[float]]
Net = dict[str, list]
Data = list[tuple[Vector, int]]


def dot(u: Sequence[float], v: Sequence[float]) -> float:
    """Inner product of two vectors of the same length. Cost O(d)."""
    return math.fsum(a * b for a, b in zip(u, v, strict=True))


def add(u: Sequence[float], v: Sequence[float]) -> Vector:
    """Coordinatewise sum u + v. Cost O(d)."""
    return [a + b for a, b in zip(u, v, strict=True)]


def sub(u: Sequence[float], v: Sequence[float]) -> Vector:
    """Coordinatewise difference u - v. Cost O(d)."""
    return [a - b for a, b in zip(u, v, strict=True)]


def scale(c: float, v: Sequence[float]) -> Vector:
    """The vector c v. Cost O(d)."""
    return [c * a for a in v]


def norm1(v: Sequence[float]) -> float:
    """The l1 norm, the sum of |v_i|. Cost O(d)."""
    return math.fsum(abs(a) for a in v)


def norm2(v: Sequence[float]) -> float:
    """The Euclidean norm. Cost O(d)."""
    return math.sqrt(math.fsum(a * a for a in v))


def norminf(v: Sequence[float]) -> float:
    """The l_infinity norm, max |v_i|, and 0 for the empty vector. Cost O(d)."""
    return max((abs(a) for a in v), default=0.0)


def project_l2(v: Sequence[float], center: Sequence[float], radius: float) -> Vector:
    """Euclidean projection of v onto the l2 ball of the given center and radius >= 0.

    A point inside the ball is returned unchanged; a point outside is moved along the
    segment to the center until it is on the sphere. Cost O(d).
    """
    diff = sub(v, center)
    r = norm2(diff)
    if r <= radius:
        return list(v)
    return add(center, scale(radius / r, diff))


def project_linf(v: Sequence[float], center: Sequence[float], radius: float) -> Vector:
    """Euclidean projection of v onto the l_infinity ball: clip each coordinate to [c_i - r, c_i + r]. Cost O(d)."""
    return [min(max(a, c - radius), c + radius) for a, c in zip(v, center, strict=True)]


def clip01(v: Sequence[float]) -> Vector:
    """Euclidean projection onto the box [0, 1]^d. Cost O(d)."""
    return [min(max(a, 0.0), 1.0) for a in v]


def make_blobs(rng: random.Random, n: int, d: int, centers: Sequence[Sequence[float]], sigma: float) -> Data:
    """n synthetic points in R^d from Gaussian blobs N(center, sigma^2 I).

    Point i gets the label i mod len(centers) and is drawn around that center, so the
    classes are balanced. The points are not clipped. Cost O(n d) and n d draws of rng.
    """
    for c in centers:
        if len(c) != d:
            raise ValueError("each center must have d coordinates")
    data: Data = []
    for i in range(n):
        label = i % len(centers)
        x = [c + rng.gauss(0.0, sigma) for c in centers[label]]
        data.append((x, label))
    return data


def sigmoid(t: float) -> float:
    """The logistic function 1 / (1 + e^(-t)), computed without overflow. Cost O(1)."""
    if t >= 0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


def _softplus(t: float) -> float:
    """ln(1 + e^t) without overflow."""
    return max(t, 0.0) + math.log1p(math.exp(-abs(t)))


def logistic_loss(w: Sequence[float], b: float, x: Sequence[float], y: int) -> float:
    """Logistic loss of the linear model z = w.x + b on a label y in {0, 1}.

    The loss is ln(1 + e^(-s z)) with s = 2 y - 1. Cost O(d).
    """
    s = 2 * y - 1
    return _softplus(-s * (dot(w, x) + b))


def grad_x_logistic(w: Sequence[float], b: float, x: Sequence[float], y: int) -> Vector:
    """Gradient of logistic_loss in the input x: (sigmoid(z) - y) w. Cost O(d)."""
    g = sigmoid(dot(w, x) + b) - y
    return scale(g, w)


def grad_w_logistic(w: Sequence[float], b: float, x: Sequence[float], y: int) -> tuple[Vector, float]:
    """Gradient of logistic_loss in the parameters: ((sigmoid(z) - y) x, sigmoid(z) - y). Cost O(d)."""
    g = sigmoid(dot(w, x) + b) - y
    return scale(g, x), g


def train_logistic(data: Data, steps: int, lr: float, l2: float) -> tuple[Vector, float]:
    """Full-batch gradient descent on the mean logistic loss plus (l2 / 2) ||w||^2.

    Labels are in {0, 1}. The weights start at zero, so the result is deterministic.
    The bias has no penalty. Returns (w, b). Cost O(steps n d).
    """
    d = len(data[0][0])
    n = len(data)
    w = [0.0] * d
    b = 0.0
    for _ in range(steps):
        gw = [0.0] * d
        gb = 0.0
        for x, y in data:
            g = sigmoid(dot(w, x) + b) - y
            for j in range(d):
                gw[j] += g * x[j]
            gb += g
        w = [w[j] - lr * (gw[j] / n + l2 * w[j]) for j in range(d)]
        b -= lr * gb / n
    return w, b


def tiny_relu_net(rng: random.Random, d: int, h: int, k: int) -> Net:
    """A fixed-seed two-layer ReLU network with d inputs, h hidden units and k logits.

    The weights are drawn from N(0, 1/d) in the first layer and N(0, 1/h) in the second,
    and the biases from N(0, 0.01). The dict has the keys W1 (h rows of d), b1 (h),
    W2 (k rows of h) and b2 (k). Cost O(h d + k h).
    """
    s1, s2 = 1.0 / math.sqrt(d), 1.0 / math.sqrt(h)
    return {
        "W1": [[rng.gauss(0.0, s1) for _ in range(d)] for _ in range(h)],
        "b1": [rng.gauss(0.0, 0.1) for _ in range(h)],
        "W2": [[rng.gauss(0.0, s2) for _ in range(h)] for _ in range(k)],
        "b2": [rng.gauss(0.0, 0.1) for _ in range(k)],
    }


def _hidden(net: Net, x: Sequence[float]) -> tuple[Vector, Vector]:
    """Pre-activations and activations of the hidden layer."""
    pre = [dot(row, x) + bi for row, bi in zip(net["W1"], net["b1"], strict=True)]
    return pre, [max(a, 0.0) for a in pre]


def forward(net: Net, x: Sequence[float]) -> Vector:
    """Logits z(x) = W2 relu(W1 x + b1) + b2 of a tiny_relu_net. Cost O(h d + k h)."""
    _, act = _hidden(net, x)
    return [dot(row, act) + bi for row, bi in zip(net["W2"], net["b2"], strict=True)]


def argmax(z: Sequence[float]) -> int:
    """The first index of a largest entry. Cost O(k)."""
    best = 0
    for i in range(1, len(z)):
        if z[i] > z[best]:
            best = i
    return best


def softmax(z: Sequence[float]) -> Vector:
    """The softmax of a logit vector, shifted by the maximum to avoid overflow. Cost O(k)."""
    m = max(z)
    e = [math.exp(a - m) for a in z]
    s = math.fsum(e)
    return [a / s for a in e]


def cross_entropy(z: Sequence[float], label: int) -> float:
    """Cross-entropy loss -ln softmax(z)[label], computed as logsumexp(z) - z[label]. Cost O(k)."""
    m = max(z)
    return m + math.log(math.fsum(math.exp(a - m) for a in z)) - z[label]


def logits_jacobian(net: Net, x: Sequence[float]) -> Matrix:
    """The k by d Jacobian of the logits in the input, W2 diag(relu'(pre)) W1.

    The derivative of the ReLU is taken as 0 at a pre-activation of exactly 0.
    Cost O(k h d).
    """
    pre, _ = _hidden(net, x)
    d = len(x)
    rows = []
    for w2 in net["W2"]:
        row = [0.0] * d
        for i, a in enumerate(pre):
            if a > 0 and w2[i] != 0.0:
                c = w2[i]
                w1 = net["W1"][i]
                for j in range(d):
                    row[j] += c * w1[j]
        rows.append(row)
    return rows


def input_gradient(net: Net, x: Sequence[float], label: int) -> Vector:
    """Gradient in x of cross_entropy(forward(net, x), label), by backpropagation.

    The derivative of the ReLU is taken as 0 at a pre-activation of exactly 0.
    Cost O(h d + k h).
    """
    pre, act = _hidden(net, x)
    z = [dot(row, act) + bi for row, bi in zip(net["W2"], net["b2"], strict=True)]
    p = softmax(z)
    p[label] -= 1.0
    back = [0.0] * len(pre)
    for c, row in zip(p, net["W2"], strict=True):
        for i in range(len(pre)):
            back[i] += c * row[i]
    g = [0.0] * len(x)
    for i, a in enumerate(pre):
        if a > 0:
            w1 = net["W1"][i]
            for j in range(len(x)):
                g[j] += back[i] * w1[j]
    return g


def accuracy(predict: Callable[[Vector], int], data: Data) -> float:
    """Fraction of the pairs (x, y) of data with predict(x) == y. Cost: n calls of predict."""
    if not data:
        return 0.0
    return sum(1 for x, y in data if predict(x) == y) / len(data)
