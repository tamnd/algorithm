# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/model-inversion-attack/. The authors are listed in prov/PV1E6J.jsonl.

"""MI-FACE, the model inversion of Fredrikson, Jha and Ristenpart (2015), as an abstract model on synthetic data.

The attack looks for an input x in [0, 1]^d with a low cost c(x) = 1 - p_label(x), where
p_label is the confidence that a model gives to one class. The models here are a binary
logistic model, a softmax regression and a seeded tiny_relu_net from mlkit; the tests build
every model and every data point from a fixed seed. Nothing here reads a real data set or
queries a real model.
"""

import math
from typing import Callable, Sequence

from mlkit import Net, Vector, clip01, dot, forward, input_gradient, sigmoid, softmax

CostFn = Callable[[Sequence[float]], float]
GradFn = Callable[[Sequence[float]], Vector]


def logistic_cost(w: Sequence[float], b: float) -> tuple[CostFn, GradFn]:
    """The cost 1 - sigmoid(w.x + b) of the class 1 of a binary logistic model, and its gradient.

    The gradient is -sigmoid'(z) w with sigmoid'(z) = sigmoid(z) (1 - sigmoid(z)). Cost O(d) per call.
    """

    def cost(x: Sequence[float]) -> float:
        return 1.0 - sigmoid(dot(w, x) + b)

    def grad(x: Sequence[float]) -> Vector:
        s = sigmoid(dot(w, x) + b)
        return [-s * (1.0 - s) * wj for wj in w]

    return cost, grad


def softmax_cost(weights: Sequence[Sequence[float]], biases: Sequence[float], label: int) -> tuple[CostFn, GradFn]:
    """The cost 1 - p_label(x) of a softmax regression p(x) = softmax(W x + b), and its gradient.

    The gradient is -p_label (W_label - sum_k p_k W_k). Precondition: 0 <= label < k.
    Cost O(k d) per call.
    """

    def probs(x: Sequence[float]) -> Vector:
        return softmax([dot(row, x) + bk for row, bk in zip(weights, biases, strict=True)])

    def cost(x: Sequence[float]) -> float:
        return 1.0 - probs(x)[label]

    def grad(x: Sequence[float]) -> Vector:
        p = probs(x)
        d = len(x)
        mean = [math.fsum(p[k] * weights[k][j] for k in range(len(p))) for j in range(d)]
        return [-p[label] * (weights[label][j] - mean[j]) for j in range(d)]

    return cost, grad


def net_cost(net: Net, label: int) -> tuple[CostFn, GradFn]:
    """The cost 1 - p_label(x) of a tiny_relu_net, and its gradient p_label(x) times the input gradient of the cross-entropy.

    Since p_label = exp(-CE), the gradient of 1 - p_label is p_label times the gradient of CE.
    The derivative of the ReLU is taken as 0 at a pre-activation of exactly 0. Cost O(h d + k h) per call.
    """

    def cost(x: Sequence[float]) -> float:
        return 1.0 - softmax(forward(net, x))[label]

    def grad(x: Sequence[float]) -> Vector:
        p = softmax(forward(net, x))[label]
        return [p * g for g in input_gradient(net, x, label)]

    return cost, grad


def finite_difference_grad(cost: CostFn, h: float) -> GradFn:
    """A black box estimate of the gradient by central differences, 2 d queries of the cost per call.

    Precondition: h > 0. Cost: 2 d calls of cost.
    """

    def grad(x: Sequence[float]) -> Vector:
        g = []
        for j in range(len(x)):
            up, dn = list(x), list(x)
            up[j] += h
            dn[j] -= h
            g.append((cost(up) - cost(dn)) / (2.0 * h))
        return g

    return grad


def rounded_cost(cost: CostFn, r: float) -> CostFn:
    """The cost seen by a client when the service rounds each confidence to a multiple of r (a defense).

    Precondition: r > 0. Cost: one call of cost.
    """

    def out(x: Sequence[float]) -> float:
        return 1.0 - r * round((1.0 - cost(x)) / r)

    return out


def mi_face(cost: CostFn, grad: GradFn, d: int, alpha: int, beta: int, gamma: float, lam: float) -> tuple[Vector, float]:
    """MI-FACE (Algorithm 1 of Fredrikson et al. 2015) with PROCESS = the projection onto [0, 1]^d and no auxiliary term.

    Gradient descent on the cost from x_0 = 0, for at most alpha steps of size lam. It stops when
    the cost of x_i is at least the largest of the last beta costs (no progress), or when it is at
    most gamma. Returns the visited point of least cost (the first one on ties) and its cost.
    Precondition: d >= 1, alpha >= 0, beta >= 1, lam > 0.
    Cost O(alpha (g + c + beta)), where g and c are the costs of one call of grad and of cost.
    """
    x = [0.0] * d  # @line L1
    history = [cost(x)]
    best_x, best_c = x, history[0]
    for _ in range(alpha):  # @line L2
        g = grad(x)
        x = clip01([xj - lam * gj for xj, gj in zip(x, g, strict=True)])  # @line L3
        c = cost(x)
        if c < best_c:
            best_x, best_c = x, c
        if c >= max(history[-beta:]):  # @line L4
            break
        history.append(c)
        if c <= gamma:  # @line L5
            break
    return best_x, best_c  # @line L6
