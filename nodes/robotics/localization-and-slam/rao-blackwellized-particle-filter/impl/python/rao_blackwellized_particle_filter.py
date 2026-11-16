# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rao-blackwellized-particle-filter/. The authors are listed in prov/E6NP93.jsonl.

"""A Rao-Blackwellized particle filter for a switching linear model.

The model is a jump Markov linear system with a scalar state:

  s_t        a mode in {0, ..., K-1}, a Markov chain with P(s_t = j | s_(t-1) = i) = trans[i][j]
  x_t        = a[s_t] x_(t-1) + b[s_t] + w_t,   w_t ~ N(0, q[s_t])
  z_t        = c x_t + v_t,                     v_t ~ N(0, r)

Given the mode history, the model is linear and Gaussian, so a Kalman
filter gives p(x_t | s_(1:t), z_(1:t)) exactly. The filter samples only
the modes, and each particle carries the mean and the variance of its
Kalman filter. This is the setting of Doucet, de Freitas, Murphy and
Russell (2000).

  rbpf_step(model, particles, z, rng, proposal)   one step, lines L1 to L8
  estimate(particles)                              the mixture mean of x_t and P(s_t = k)
  exact_posterior(model, zs)                       enumeration of all K^t mode histories
  bootstrap_pf_step(model, particles, z, rng)      a plain particle filter over (s, x), to compare

A particle is a list [s, mean, var, weight].
"""

import math

import robest


class Model:
    """The parameters of the switching linear model, with the prior of x_0 and s_0."""

    def __init__(self, trans, a, b, q, c, r, x0_mean, x0_var, s0_prob):
        self.trans = trans
        self.a = a
        self.b = b
        self.q = q
        self.c = c
        self.r = r
        self.x0_mean = x0_mean
        self.x0_var = x0_var
        self.s0_prob = s0_prob
        self.k = len(a)


def kalman_predict(model, s, mean, var):
    """Return the Kalman prediction of x_t given the mode s."""
    return model.a[s] * mean + model.b[s], model.a[s] ** 2 * var + model.q[s]


def predictive(model, s, mean, var):
    """Return the predicted moments and the likelihood mean and variance of z_t, given s."""
    pm, pv = kalman_predict(model, s, mean, var)
    return pm, pv, model.c * pm, model.c ** 2 * pv + model.r


def kalman_update(model, pm, pv, z):
    """Return the Kalman update of N(pm, pv) with the reading z."""
    sv = model.c ** 2 * pv + model.r
    gain = pv * model.c / sv
    return pm + gain * (z - model.c * pm), (1.0 - gain * model.c) * pv


def initial_particles(model, n, rng):
    """N particles with the modes drawn from s0_prob and the prior of x_0 in each."""
    out = []
    for _ in range(n):
        s = draw(rng, model.s0_prob)
        out.append([s, model.x0_mean, model.x0_var, 1.0 / n])
    return out


def draw(rng, probs):
    """Draw an index with the given probabilities."""
    u = rng.random() * sum(probs)
    acc = 0.0
    for i, p in enumerate(probs):
        acc += p
        if u < acc:
            return i
    return len(probs) - 1


def effective_size(particles):
    total = sum(p[3] for p in particles)
    return total * total / sum(p[3] * p[3] for p in particles)


def rbpf_step(model, particles, z, rng, proposal="optimal", resample_ratio=0.5):
    """One step of the RBPF, in place. Return the log of the step's likelihood estimate.

    proposal="prior" draws s_t from the Markov chain and weights by the
    predictive likelihood of z_t. proposal="optimal" draws s_t from
    p(s_t | s_(t-1), x-belief, z_t), whose weight does not depend on the
    draw. Resampling happens when the effective sample size falls below
    resample_ratio times N.
    """
    n = len(particles)
    total_before = sum(p[3] for p in particles)
    for p in particles:  # @line L1
        s_prev, mean, var, w = p
        probs, moments = [], []
        for s in range(model.k):
            pm, pv, zm, zv = predictive(model, s, mean, var)
            moments.append((pm, pv))
            probs.append(model.trans[s_prev][s] * robest.gauss_pdf(z, zm, zv))
        if proposal == "optimal":
            s = draw(rng, probs)  # @line L2
            factor = sum(probs)
        else:
            s = draw(rng, model.trans[s_prev])
            factor = probs[s] / model.trans[s_prev][s]
        pm, pv = moments[s]  # @line L3
        p[3] = w * factor  # @line L4
        p[0] = s
        p[1], p[2] = kalman_update(model, pm, pv, z)  # @line L5
    total = sum(p[3] for p in particles)
    if total <= 0.0:
        raise ValueError("all weights are zero")
    for p in particles:
        p[3] /= total  # @line L6
    if effective_size(particles) < resample_ratio * n:  # @line L7
        idx = robest.low_variance_resample(rng, [p[3] for p in particles])
        new = [[particles[i][0], particles[i][1], particles[i][2], 1.0 / n] for i in idx]
        particles[:] = new
    return math.log(total / total_before)


def estimate(particles):
    """Return E[x_t | z_(1:t)] and the list P(s_t = k | z_(1:t)) from the particles: line L8."""
    total = sum(p[3] for p in particles)
    mean = sum(p[3] * p[1] for p in particles) / total  # @line L8
    k = 1 + max(p[0] for p in particles)
    probs = [0.0] * k
    for p in particles:
        probs[p[0]] += p[3] / total
    return mean, probs


def rbpf(model, zs, n, rng, proposal="optimal"):
    """Run the RBPF over the readings zs. Return the list of (mean, mode probabilities) per step."""
    particles = initial_particles(model, n, rng)
    out = []
    for z in zs:
        rbpf_step(model, particles, z, rng, proposal)
        mean, probs = estimate(particles)
        probs = probs + [0.0] * (model.k - len(probs))
        out.append((mean, probs))
    return out


def exact_posterior(model, zs):
    """Enumerate all mode histories with a Kalman filter each. Cost O(K^(t+1)).

    Return the exact E[x_t | z_(1:t)], P(s_t = k | z_(1:t)) and p(z_(1:t)).
    """
    hyps = [(s, model.s0_prob[s], model.x0_mean, model.x0_var) for s in range(model.k) if model.s0_prob[s] > 0.0]
    lik = 1.0
    for z in zs:
        new = []
        for s_prev, w, mean, var in hyps:
            for s in range(model.k):
                if model.trans[s_prev][s] == 0.0:
                    continue
                pm, pv, zm, zv = predictive(model, s, mean, var)
                m, v = kalman_update(model, pm, pv, z)
                new.append((s, w * model.trans[s_prev][s] * robest.gauss_pdf(z, zm, zv), m, v))
        total = sum(h[1] for h in new)
        lik *= total
        hyps = [(s, w / total, m, v) for s, w, m, v in new]
    mean = sum(w * m for _, w, m, _ in hyps)
    probs = [0.0] * model.k
    for s, w, _, _ in hyps:
        probs[s] += w
    return mean, probs, lik


def bootstrap_pf_step(model, particles, z, rng):
    """One step of a plain particle filter that samples both s_t and x_t.

    A particle is [s, x, weight]. It resamples at every step.
    """
    n = len(particles)
    for p in particles:
        s = draw(rng, model.trans[p[0]])
        x = model.a[s] * p[1] + model.b[s] + math.sqrt(model.q[s]) * rng.gauss(0.0, 1.0)
        p[0], p[1] = s, x
        p[2] *= robest.gauss_pdf(z, model.c * x, model.r)
    total = sum(p[2] for p in particles)
    mean = sum(p[2] * p[1] for p in particles) / total
    idx = robest.low_variance_resample(rng, [p[2] for p in particles])
    particles[:] = [[particles[i][0], particles[i][1], 1.0 / n] for i in idx]
    return mean


def bootstrap_pf(model, zs, n, rng):
    """Run the plain particle filter; return the list of the estimates of E[x_t | z_(1:t)]."""
    particles = []
    for _ in range(n):
        s = draw(rng, model.s0_prob)
        particles.append([s, model.x0_mean + math.sqrt(model.x0_var) * rng.gauss(0.0, 1.0), 1.0 / n])
    return [bootstrap_pf_step(model, particles, z, rng) for z in zs]


def simulate(model, steps, rng):
    """Draw a mode path, a state path and readings from the model."""
    s = draw(rng, model.s0_prob)
    x = model.x0_mean + math.sqrt(model.x0_var) * rng.gauss(0.0, 1.0)
    modes, xs, zs = [], [], []
    for _ in range(steps):
        s = draw(rng, model.trans[s])
        x = model.a[s] * x + model.b[s] + math.sqrt(model.q[s]) * rng.gauss(0.0, 1.0)
        modes.append(s)
        xs.append(x)
        zs.append(model.c * x + math.sqrt(model.r) * rng.gauss(0.0, 1.0))
    return modes, xs, zs
