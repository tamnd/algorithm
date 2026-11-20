# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coarse-projective-integration/. The authors are listed in prov/6HJ81K.jsonl.
"""Coarse projective integration (Gear and Kevrekidis 2003).

A fine simulator advances a fine state u by micro steps of length dt. The
coarse variables are X = restrict(u), and lift(X) builds a fine state with
the given coarse variables. One outer step:

    lift X to u, run k + 1 micro steps, restrict after steps k and k + 1,
    estimate the coarse slope s = (X_{k+1} - X_k) / dt, and set
    X = X_{k+1} + M dt s.

An outer step advances the coarse time by (M + k + 1) dt and costs k + 1
micro steps. With lift and restrict the identity and a forward Euler micro
step, the method is projective forward Euler.
"""


def coarse_projective_integration(X0, lift, micro_step, restrict, dt, k, M, n):
    """n outer steps of coarse projective integration from the coarse state X0.

    micro_step(u, dt) returns the fine state after one micro step. Returns the
    coarse state after n outer steps, at time n (M + k + 1) dt.
    """
    X = list(X0)
    for _ in range(n):                                    # @line L1
        u = lift(X)                                       # @line L2
        Xk = None
        for j in range(k + 1):                            # @line L3
            if j == k:
                Xk = restrict(u)                          # @line L3
            u = micro_step(u, dt)                         # @line L3
        Xk1 = restrict(u)                                 # @line L3
        s = [(b - a) / dt for a, b in zip(Xk, Xk1)]       # @line L4
        X = [b + M * dt * c for b, c in zip(Xk1, s)]      # @line L5
    return X                                              # @line L6


def euler_step(f):
    """The forward Euler micro step for y' = f(y)."""
    def step(y, dt):
        return [a + dt * b for a, b in zip(y, f(y))]
    return step


def projective_forward_euler(f, y0, h, k, M, n):
    """Projective forward Euler: identity lift and restriction, Euler micro steps."""
    return coarse_projective_integration(y0, list, euler_step(f), list, h, k, M, n)


def euler(f, y0, h, steps):
    """Plain forward Euler, the full micro simulation for comparison."""
    step = euler_step(f)
    y = list(y0)
    for _ in range(steps):
        y = step(y, h)
    return y


def amplification(zeta, k, M):
    """The factor of one outer step on a mode with Euler factor zeta = 1 + h lambda."""
    return ((M + 1) * zeta - M) * zeta ** k
