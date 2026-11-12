# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-filter/.

"""Bootstrap particle filter of Gordon, Salmond and Smith (1993).

Model: x_0 ~ p(x_0), x_t ~ p(x_t | x_(t-1)), y_t ~ p(y_t | x_t) for t = 1..T.
The caller gives three functions:
  sample_init(rng)             draws x_0 from the prior,
  sample_transition(x, t, rng) draws x_t given x_(t-1) = x,
  log_likelihood(y, x, t)      returns log p(y_t = y | x_t = x).
rng is a random.Random instance (or any object with a random() method that
the sampling functions use).
"""

import bisect
import math


def multinomial_resample(weights, n, rng):
    """Draw n ancestor indices independently with probabilities weights."""
    cumulative, total = [], 0.0
    for w in weights:
        total += w
        cumulative.append(total)
    return [min(bisect.bisect_right(cumulative, rng.random() * total), n - 1) for _ in range(n)]


def bootstrap_filter(sample_init, sample_transition, log_likelihood, ys, n, rng, test_fn=lambda x: x):
    """Return the filtered estimates of E[test_fn(x_t) | y_1..y_t] for
    t = 1..T and the estimate of log p(y_1..y_T)."""
    xs = [sample_init(rng) for _ in range(n)]  # @line L1
    weights = [1.0 / n] * n
    log_z, estimates = 0.0, []
    for t, y in enumerate(ys, 1):  # @line L2
        if t > 1:
            ancestors = multinomial_resample(weights, n, rng)  # @line L3
            xs = [xs[a] for a in ancestors]
        xs = [sample_transition(x, t, rng) for x in xs]  # @line L4
        logw = [log_likelihood(y, x, t) for x in xs]  # @line L5
        top = max(logw)
        if top == -math.inf:
            raise ValueError("all particles have zero likelihood")
        raw = [math.exp(v - top) for v in logw]
        s = sum(raw)
        log_z += top + math.log(s / n)  # @line L6
        weights = [v / s for v in raw]  # @line L7
        estimates.append(sum(w * test_fn(x) for w, x in zip(weights, xs)))
    return estimates, log_z  # @line L8
