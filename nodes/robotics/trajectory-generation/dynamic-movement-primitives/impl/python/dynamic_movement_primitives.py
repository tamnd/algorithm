# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-movement-primitives/. The authors are listed in prov/DHD4FD.jsonl.
"""Discrete dynamic movement primitive for one coordinate.

The system, in the form of Ijspeert, Nakanishi, Hoffmann, Pastor and Schaal (2013):

    tau z' = alpha_z (beta_z (g - y) - z) + f(x)
    tau y' = z
    tau x' = -alpha_x x
    f(x)   = (sum_i psi_i(x) w_i / sum_i psi_i(x)) x (g - y0),  psi_i(x) = exp(-h_i (x - c_i)^2)

fit() learns the weights w_i from one demonstration by locally weighted
regression. rollout() integrates the system with the classical Runge-Kutta
method. The gains alpha_z = 25, beta_z = alpha_z / 4 (critical damping) and
alpha_x = 4 are tuning choices, not derived values.
"""

import math


class DMP:
    def __init__(self, n_basis=20, alpha_z=25.0, beta_z=None, alpha_x=4.0):
        self.alpha_z = alpha_z
        self.beta_z = alpha_z / 4 if beta_z is None else beta_z
        self.alpha_x = alpha_x
        # Centers spaced evenly in time, so geometrically in the phase x.
        self.c = [math.exp(-alpha_x * i / (n_basis - 1)) for i in range(n_basis)]
        self.h = [1.0 / (self.c[i + 1] - self.c[i]) ** 2 for i in range(n_basis - 1)]
        self.h.append(self.h[-1])
        self.w = [0.0] * n_basis
        self.y0 = 0.0
        self.g = 1.0

    def forcing(self, x, y0, g):
        psi = [math.exp(-h * (x - c) ** 2) for h, c in zip(self.h, self.c)]  # @line L2
        total = sum(psi)
        if total == 0:
            return 0.0
        return sum(p * w for p, w in zip(psi, self.w)) / total * x * (g - y0)  # @line L3

    def fit(self, ts, ys, yds, ydds, tau):
        """Learn w from samples of a demonstration (time, position, velocity, acceleration)."""
        self.y0, self.g = ys[0], ys[-1]
        az, bz, ax = self.alpha_z, self.beta_z, self.alpha_x
        xs = [math.exp(-ax * t / tau) for t in ts]
        ft = [tau * tau * a - az * (bz * (self.g - y) - tau * v) for y, v, a in zip(ys, yds, ydds)]  # @line L8
        s = [x * (self.g - self.y0) for x in xs]
        for i, (h, c) in enumerate(zip(self.h, self.c)):
            gam = [math.exp(-h * (x - c) ** 2) for x in xs]
            num = sum(si * gi * fi for si, gi, fi in zip(s, gam, ft))
            den = sum(si * si * gi for si, gi in zip(s, gam))
            self.w[i] = num / den if den > 0 else 0.0  # @line L9

    def derivs(self, state, g, tau):
        y, z, x = state
        f = self.forcing(x, self.y0, g)
        zd = (self.alpha_z * (self.beta_z * (g - y) - z) + f) / tau  # @line L4
        yd = z / tau  # @line L5
        xd = -self.alpha_x * x / tau  # @line L6
        return (yd, zd, xd)

    def rollout(self, tau, duration, dt=0.001, y0=None, g=None):
        """Integrate from rest; return lists of times and positions. y0 and g may differ from the demo."""
        if y0 is not None:
            self.y0 = y0
        g = self.g if g is None else g
        state = (self.y0, 0.0, 1.0)  # @line L1
        ts, ys = [0.0], [state[0]]
        n = int(round(duration / dt))
        for k in range(n):  # @line L7
            k1 = self.derivs(state, g, tau)
            k2 = self.derivs(tuple(s + dt / 2 * d for s, d in zip(state, k1)), g, tau)
            k3 = self.derivs(tuple(s + dt / 2 * d for s, d in zip(state, k2)), g, tau)
            k4 = self.derivs(tuple(s + dt * d for s, d in zip(state, k3)), g, tau)
            state = tuple(s + dt / 6 * (a + 2 * b + 2 * c + d) for s, a, b, c, d in zip(state, k1, k2, k3, k4))
            ts.append((k + 1) * dt)
            ys.append(state[0])
        self.last_state = state
        return ts, ys
