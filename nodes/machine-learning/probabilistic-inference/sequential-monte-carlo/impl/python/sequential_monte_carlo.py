# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-monte-carlo/.

"""Sequential importance sampling with resampling when the effective sample
size falls under a threshold (adaptive SMC).

The targets are distributions gamma_t(x_0..x_t) / Z_t for t = 1..T. The
caller gives:
  sample_init(rng)                   draws x_0 (all weights start equal),
  sample_proposal(x_prev, t, rng)    draws x_t from q_t(. | x_prev),
  log_incremental(x_prev, x, t)      returns log of the incremental weight
      gamma_t(x_0..x_t) / (gamma_(t-1)(x_0..x_(t-1)) q_t(x_t | x_(t-1))).
For a state space model with prior p(x_0), this weight is
p(y_t | x_t) p(x_t | x_(t-1)) / q_t(x_t | x_(t-1)), and Z_T = p(y_1..y_T).
"""

import math


def ess(weights):
    """Effective sample size 1 / sum w_i^2 of normalized weights."""
    return 1.0 / sum(w * w for w in weights)


def systematic_resample(weights, rng):
    """One uniform U; the points (j + U) / n select the ancestors."""
    n = len(weights)
    u = rng.random()
    ancestors, i, cumulative = [], 0, weights[0]
    for j in range(n):
        point = (j + u) / n
        while point >= cumulative and i < n - 1:
            i += 1
            cumulative += weights[i]
        ancestors.append(i)
    return ancestors


def sequential_monte_carlo(
    sample_init, sample_proposal, log_incremental, T, n, rng, threshold=0.5, test_fn=lambda x: x
):
    """Return the estimates of E[test_fn(x_t)] under each target, the
    estimate of log Z_T, the times at which it resampled, and the ESS seen
    at the start of each step."""
    xs = [sample_init(rng) for _ in range(n)]  # @line L1
    W = [1.0 / n] * n
    log_z, estimates, resampled, ess_seen = 0.0, [], [], []
    for t in range(1, T + 1):  # @line L2
        e = ess(W)  # @line L3
        ess_seen.append(e)
        if e < threshold * n:  # @line L4
            xs = [xs[a] for a in systematic_resample(W, rng)]
            W = [1.0 / n] * n
            resampled.append(t)
        new = [sample_proposal(x, t, rng) for x in xs]  # @line L5
        inc = [log_incremental(x, x_new, t) for x, x_new in zip(xs, new)]  # @line L6
        top = max(inc)
        if top == -math.inf:
            raise ValueError("all incremental weights are zero")
        raw = [w * math.exp(v - top) for w, v in zip(W, inc)]
        s = sum(raw)
        log_z += top + math.log(s)  # @line L7
        W = [v / s for v in raw]  # @line L8
        xs = new
        estimates.append(sum(w * test_fn(x) for w, x in zip(W, xs)))
    return estimates, log_z, resampled, ess_seen  # @line L9
