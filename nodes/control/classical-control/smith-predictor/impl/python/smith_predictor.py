# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smith-predictor/. The authors are listed in prov/R7T7GR.jsonl.

"""The Smith predictor (Smith, 1957) as a sampled controller.

The plant is P(s) = P0(s) e^(-theta s), with P0 = C (sI - A)^(-1) B. With the
sampling period h and a zero-order hold, P0 becomes x_(k+1) = Ad x_k + Bd u_k,
y_k = C x_k (exact for a held input), and the delay theta = d h becomes d
samples. The predictor runs a model (Am, Bm, Cm, dm) of the plant. At each
sample the controller sees

    y_f = y + (yhat0 - yhat_d),

where yhat0 is the output of the model without delay and yhat_d the output
of the model with its delay dm. With an exact model y = yhat_d, and the
controller sees the delay-free output yhat0.

The primary controller is a PI controller with the forward difference
integral: v = K e + I, then I = I + (K h / Ti) e.

All classes work in floating point. The order of the operations in
step() makes y_f equal yhat0 exactly when y equals yhat_d.
"""

import math
from collections import deque

from ctlmat import expm, matvec

__all__ = ["zoh", "PI", "SmithPredictor", "DelayedPlant", "run_loop"]


def zoh(A, B, h):
    """Return (Ad, Bd) of x' = A x + B u with u held over steps of length h.

    Uses the exponential of [[A, B], [0, 0]] h (one input)."""
    n = len(A)
    big = [[h * v for v in list(A[i]) + [B[i][0]]] for i in range(n)] + [[0.0] * (n + 1)]
    E = expm(big)
    return [row[:n] for row in E[:n]], [[E[i][n]] for i in range(n)]


class PI:
    """Sampled PI controller v = K e + I, I += K h/Ti e (Ti = None: P only)."""

    def __init__(self, K, Ti, h):
        self.K, self.bi, self.I = K, (0.0 if Ti is None else K * h / Ti), 0.0

    def step(self, e):
        v = self.K * e + self.I
        self.I += self.bi * e
        return v


class DelayedPlant:
    """x_(k+1) = Ad x_k + Bd (u_(k-d) + w_k), y_k = C x_k, from rest.

    w is a load disturbance at the plant input."""

    def __init__(self, Ad, Bd, C, d):
        self.Ad, self.Bd, self.C = Ad, Bd, C
        self.x = [0.0] * len(Ad)
        self.line = deque([0.0] * d)

    def output(self):
        return matvec([self.C], self.x)[0]

    def advance(self, u, w=0.0):
        self.line.append(u)
        ua = self.line.popleft() + w
        self.x = [sum(a * xi for a, xi in zip(row, self.x)) + b[0] * ua
                  for row, b in zip(self.Ad, self.Bd)]


class SmithPredictor:
    """The Smith predictor around a primary controller with a step(e) method."""

    def __init__(self, Am, Bm, Cm, dm, controller):
        self.Am, self.Bm, self.Cm = Am, Bm, Cm
        self.xm = [0.0] * len(Am)
        self.line = deque([0.0] * dm)     # past model outputs yhat0
        self.ctl = controller
        self.dm = dm

    def step(self, r, y):
        """Return u_k from the set point r_k and the measurement y_k."""
        yhat0 = matvec([self.Cm], self.xm)[0]
        yhat_d = self.line[0] if self.dm else yhat0
        yf = yhat0 + (y - yhat_d)  # @line L1
        e = r - yf  # @line L2
        u = self.ctl.step(e)  # @line L3
        self.xm = [sum(a * xi for a, xi in zip(row, self.xm)) + b[0] * u  # @line L4
                   for row, b in zip(self.Am, self.Bm)]
        if self.dm:
            self.line.append(yhat0)  # @line L5
            self.line.popleft()
        return u  # @line L6


def run_loop(plant, controller, n, r=1.0, w=None):
    """Run n samples. controller is a SmithPredictor or a plain controller
    with step(e). w(k) is the load at the plant input. Returns (ys, us)."""
    ys, us = [], []
    for k in range(n):
        y = plant.output()
        if isinstance(controller, SmithPredictor):
            u = controller.step(r, y)
        else:
            u = controller.step(r - y)
        plant.advance(u, 0.0 if w is None else w(k))
        ys.append(y)
        us.append(u)
    return ys, us


def _self_test():
    h = 0.1
    Ad, Bd = zoh([[-1.0]], [[1.0]], h)
    assert abs(Ad[0][0] - math.exp(-h)) < 1e-15
    plant = DelayedPlant(Ad, Bd, [1.0], 20)
    sp = SmithPredictor(Ad, Bd, [1.0], 20, PI(2.0, 1.0, h))
    ys, _ = run_loop(plant, sp, 400)
    assert abs(ys[-1] - 1) < 1e-6
    return True


if __name__ == "__main__":
    _self_test()
