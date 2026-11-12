# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wake-sleep-algorithm/. The authors are listed in prov/08MB4F.jsonl.

"""The wake-sleep algorithm (Hinton, Dayan, Frey and Neal 1995) for a small Helmholtz machine.

Generative model (top down), H binary hidden units and V binary visible units:
    p(h_j = 1) = sigmoid(b_j)
    p(v_i = 1 | h) = sigmoid(c_i + sum_j W[i][j] h_j)
Recognition model (bottom up), factorial given v:
    q(h_j = 1 | v) = sigmoid(d_j + sum_i R[j][i] v_i)

A generative model is a tuple (b, c, W); a recognition model is a tuple (d, R).
"""

import itertools
import math


def sigmoid(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def _log_bern(bit, logit):
    """log P(bit) for a Bernoulli variable with P(1) = sigmoid(logit), computed stably."""
    s = logit if bit else -logit
    return -math.log1p(math.exp(-s)) if s >= 0 else s - math.log1p(math.exp(s))


def init_params(n_hidden, n_visible, rng, scale=0.1):
    gen = ([rng.gauss(0, scale) for _ in range(n_hidden)],
           [rng.gauss(0, scale) for _ in range(n_visible)],
           [[rng.gauss(0, scale) for _ in range(n_hidden)] for _ in range(n_visible)])
    rec = ([rng.gauss(0, scale) for _ in range(n_hidden)],
           [[rng.gauss(0, scale) for _ in range(n_visible)] for _ in range(n_hidden)])
    return gen, rec


def visible_logits(gen, h):
    _, c, W = gen
    return [c[i] + sum(W[i][j] * h[j] for j in range(len(h))) for i in range(len(c))]


def hidden_logits(rec, v):
    d, R = rec
    return [d[j] + sum(R[j][i] * v[i] for i in range(len(v))) for j in range(len(d))]


def log_p_joint(gen, v, h):
    b = gen[0]
    return (sum(_log_bern(h[j], b[j]) for j in range(len(b)))
            + sum(_log_bern(v[i], z) for i, z in enumerate(visible_logits(gen, h))))


def log_q(rec, h, v):
    return sum(_log_bern(h[j], z) for j, z in enumerate(hidden_logits(rec, v)))


def hidden_states(n_hidden):
    return list(itertools.product((0, 1), repeat=n_hidden))


def log_marginal(gen, v):
    """log p(v), by enumeration of the hidden states."""
    terms = [log_p_joint(gen, v, h) for h in hidden_states(len(gen[0]))]
    top = max(terms)
    return top + math.log(sum(math.exp(t - top) for t in terms))


def avg_log_likelihood(gen, data):
    return sum(log_marginal(gen, v) for v in data) / len(data)


def elbo(gen, rec, v):
    """E_q[log p(v, h) - log q(h | v)], by enumeration of the hidden states."""
    total = 0.0
    for h in hidden_states(len(gen[0])):
        lq = log_q(rec, h, v)
        total += math.exp(lq) * (log_p_joint(gen, v, h) - lq)
    return total


def sample_bits(logits, rng):
    return tuple(1 if rng.random() < sigmoid(z) else 0 for z in logits)


def wake_delta(gen, v, h):
    """The gradient of log p(v, h) in (b, c, W): local delta rules."""
    b = gen[0]
    db = [h[j] - sigmoid(b[j]) for j in range(len(b))]
    err = [v[i] - sigmoid(z) for i, z in enumerate(visible_logits(gen, h))]
    dW = [[err[i] * h[j] for j in range(len(h))] for i in range(len(v))]
    return db, err, dW


def sleep_delta(rec, h, v):
    """The gradient of log q(h | v) in (d, R): local delta rules."""
    err = [h[j] - sigmoid(z) for j, z in enumerate(hidden_logits(rec, v))]
    dR = [[err[j] * v[i] for i in range(len(v))] for j in range(len(h))]
    return err, dR


def _add(params, delta, eta):
    """params += eta * delta, for nested lists of the same shape."""
    for p, g in zip(params, delta):
        for k in range(len(p)):
            if isinstance(p[k], list):
                for m in range(len(p[k])):
                    p[k][m] += eta * g[k][m]
            else:
                p[k] += eta * g[k]


def wake_sleep(data, n_hidden, steps, rng, eta=0.05, init=None):
    """Run the wake-sleep algorithm. Each step is one wake update and one sleep update.
    Return the generative model and the recognition model."""
    n_visible = len(data[0])
    gen, rec = init if init is not None else init_params(n_hidden, n_visible, rng)  # @line L1
    for _ in range(steps):  # @line L2
        v = data[rng.randrange(len(data))]  # @line L3
        h = sample_bits(hidden_logits(rec, v), rng)
        _add(gen, wake_delta(gen, v, h), eta)  # @line L4
        h_dream = sample_bits(gen[0], rng)  # @line L5
        v_dream = sample_bits(visible_logits(gen, h_dream), rng)  # @line L6
        _add(rec, sleep_delta(rec, h_dream, v_dream), eta)  # @line L7
    return gen, rec  # @line L8
