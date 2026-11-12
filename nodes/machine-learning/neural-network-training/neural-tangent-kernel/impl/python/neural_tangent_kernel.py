# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/neural-tangent-kernel/. The authors are listed in prov/G9XN5F.jsonl.

"""The neural tangent kernel of a two layer ReLU network.

The network in the NTK parameterization is

    f(x) = (1 / sqrt(m)) * sum_j a_j * relu(w_j . x),

with w_j ~ N(0, I_d) and a_j ~ N(0, 1) at initialization. Its empirical NTK is
Theta(x, x') = <grad_theta f(x), grad_theta f(x')> over theta = (a, W). As
m -> infinity it tends to the closed form built from the arc cosine kernels
of Cho and Saul (2009) of degree 0 and 1.
"""

import math
import random
from typing import List, Sequence, Tuple

Vec = Sequence[float]


def relu(t: float) -> float:
    return t if t > 0.0 else 0.0


def dot(u: Vec, v: Vec) -> float:
    return sum(a * b for a, b in zip(u, v))


class TwoLayerNet:
    """A width m two layer ReLU network in the NTK parameterization."""

    def __init__(self, d: int, m: int, rng: random.Random):
        self.d, self.m = d, m
        self.w = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(m)]
        self.a = [rng.gauss(0.0, 1.0) for _ in range(m)]

    def forward(self, x: Vec) -> float:
        s = sum(aj * relu(dot(wj, x)) for aj, wj in zip(self.a, self.w))
        return s / math.sqrt(self.m)

    def gradient(self, x: Vec) -> Tuple[List[float], List[List[float]]]:
        """(df/da, df/dW) at x."""
        c = 1.0 / math.sqrt(self.m)
        ga, gw = [], []
        for aj, wj in zip(self.a, self.w):
            z = dot(wj, x)
            ga.append(c * relu(z))
            ind = 1.0 if z > 0.0 else 0.0
            gw.append([c * aj * ind * xi for xi in x])
        return ga, gw

    def params(self) -> List[float]:
        return list(self.a) + [t for row in self.w for t in row]

    def set_params(self, theta: Sequence[float]) -> None:
        m, d = self.m, self.d
        self.a = list(theta[:m])
        self.w = [list(theta[m + j * d: m + (j + 1) * d]) for j in range(m)]


def flat_gradient(net: TwoLayerNet, x: Vec) -> List[float]:
    ga, gw = net.gradient(x)
    return ga + [t for row in gw for t in row]


def empirical_ntk(net: TwoLayerNet, x: Vec, y: Vec) -> float:
    """Theta_m(x, y), the inner product of the two parameter gradients."""
    return dot(flat_gradient(net, x), flat_gradient(net, y))


def empirical_ntk_fast(net: TwoLayerNet, x: Vec, y: Vec) -> float:
    """The same kernel from the closed sum over hidden units, O(m d) time."""
    xy = dot(x, y)
    s = 0.0
    for aj, wj in zip(net.a, net.w):
        zx, zy = dot(wj, x), dot(wj, y)
        s += relu(zx) * relu(zy)
        if zx > 0.0 and zy > 0.0:
            s += aj * aj * xy
    return s / net.m


def _angle(x: Vec, y: Vec) -> Tuple[float, float, float]:
    nx, ny = math.sqrt(dot(x, x)), math.sqrt(dot(y, y))
    # theta = 2 atan2(|u - v|, |u + v|) for unit u, v; stable near 0 and pi.
    u = [t / nx for t in x]
    v = [t / ny for t in y]
    dm = math.sqrt(sum((a - b) ** 2 for a, b in zip(u, v)))
    dp = math.sqrt(sum((a + b) ** 2 for a, b in zip(u, v)))
    return nx, ny, 2.0 * math.atan2(dm, dp)


def arc_cosine_kernel(x: Vec, y: Vec, degree: int) -> float:
    """The arc cosine kernel k_n of Cho and Saul for n = 0 or 1.

    k_0 = 1 - theta / pi and k_1 = |x| |y| (sin theta + (pi - theta) cos theta) / pi.
    These equal 2 E[step(w.x) step(w.y)] and 2 E[relu(w.x) relu(w.y)] for w ~ N(0, I).
    """
    nx, ny, th = _angle(x, y)
    if degree == 0:
        return 1.0 - th / math.pi
    if degree == 1:
        return nx * ny * (math.sin(th) + (math.pi - th) * math.cos(th)) / math.pi
    raise ValueError("only degrees 0 and 1 are implemented")


def infinite_width_ntk(x: Vec, y: Vec) -> float:
    """The limit of Theta_m as m -> infinity for the network above.

    The a part tends to E[relu(w.x) relu(w.y)] = k_1 / 2, and the W part tends
    to E[a^2] E[step(w.x) step(w.y)] x.y = (k_0 / 2) x.y.
    """
    return 0.5 * arc_cosine_kernel(x, y, 1) + 0.5 * arc_cosine_kernel(x, y, 0) * dot(x, y)


def train_squared_loss(net: TwoLayerNet, xs: Sequence[Vec], ys: Sequence[float], eta: float, steps: int) -> float:
    """Full batch gradient descent on L = (1/2n) sum (f(x_i) - y_i)^2. Returns the final loss."""
    n = len(xs)
    theta = net.params()
    for _ in range(steps):
        g = [0.0] * len(theta)
        for x, y in zip(xs, ys):
            r = (net.forward(x) - y) / n
            for k, gk in enumerate(flat_gradient(net, x)):
                g[k] += r * gk
        theta = [t - eta * gk for t, gk in zip(theta, g)]
        net.set_params(theta)
    return sum((net.forward(x) - y) ** 2 for x, y in zip(xs, ys)) / (2 * n)


def gram(kernel, xs: Sequence[Vec]) -> List[List[float]]:
    return [[kernel(u, v) for v in xs] for u in xs]


def relative_change(k0: Sequence[Sequence[float]], k1: Sequence[Sequence[float]]) -> float:
    """Frobenius norm of k1 - k0 divided by that of k0."""
    num = sum((b - a) ** 2 for r0, r1 in zip(k0, k1) for a, b in zip(r0, r1))
    den = sum(a * a for r0 in k0 for a in r0)
    return math.sqrt(num / den)
