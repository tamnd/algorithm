# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rao-blackwellized-particle-filter/. The authors are listed in prov/E6NP93.jsonl.

import math
import random

from rao_blackwellized_particle_filter import (
    Model,
    bootstrap_pf,
    effective_size,
    estimate,
    exact_posterior,
    initial_particles,
    kalman_predict,
    kalman_update,
    rbpf,
    rbpf_step,
    simulate,
)


def cart():
    """The example of the page: a cart that is stopped (mode 0) or moves 1 per step (mode 1)."""
    return Model([[0.9, 0.1], [0.1, 0.9]], [1.0, 1.0], [0.0, 1.0], [0.01, 0.01], 1.0, 0.25, 0.0, 0.01, [1.0, 0.0])


def test_example_of_the_page():
    m = cart()
    mean, probs, lik = exact_posterior(m, [0.9])
    assert abs(probs[0] - 0.6717) < 1e-4
    assert abs(mean - 0.3707) < 1e-4
    mean, probs, _ = exact_posterior(m, [0.9, 2.1, 2.0])
    assert abs(probs[1] - 0.6402) < 1e-4
    assert abs(mean - 2.4763) < 1e-4
    # one particle step by hand: both modes give the variance 0.02 (1 - 0.02 / 0.27)
    p = [[0, 0.0, 0.01, 1.0]]
    rbpf_step(m, p, 0.9, random.Random(0))
    assert abs(p[0][2] - 0.02 * (1.0 - 0.02 / 0.27)) < 1e-12
    want = 0.9 * 0.02 / 0.27 if p[0][0] == 0 else 1.0 - 0.1 * 0.02 / 0.27
    assert abs(p[0][1] - want) < 1e-12


def test_one_mode_is_the_kalman_filter():
    m = Model([[1.0]], [0.95], [0.3], [0.04], 2.0, 0.5, 1.0, 1.0, [1.0])
    rng = random.Random(4)
    _, xs, zs = simulate(m, 10, rng)
    particles = initial_particles(m, 5, rng)
    mean, var, loglik = 1.0, 1.0, 0.0
    for z in zs:
        pm, pv = kalman_predict(m, 0, mean, var)
        sv = m.c ** 2 * pv + m.r
        step_ll = -0.5 * math.log(2.0 * math.pi * sv) - 0.5 * (z - m.c * pm) ** 2 / sv
        loglik += step_ll
        mean, var = kalman_update(m, pm, pv, z)
        assert abs(rbpf_step(m, particles, z, rng) - step_ll) < 1e-12
        est, probs = estimate(particles)
        assert abs(est - mean) < 1e-12
        assert probs == [1.0]
        for p in particles:
            assert abs(p[2] - var) < 1e-15
    _, _, lik = exact_posterior(m, zs)
    assert abs(math.log(lik) - loglik) < 1e-9


def test_converges_to_the_exact_posterior():
    m = cart()
    _, _, zs = simulate(m, 8, random.Random(1))
    mean, probs, _ = exact_posterior(m, zs)
    for proposal in ("optimal", "prior"):
        est, est_probs = rbpf(m, zs, 2000, random.Random(2), proposal)[-1]
        assert abs(est - mean) < 0.03
        assert abs(est_probs[1] - probs[1]) < 0.03


def test_the_optimal_proposal_weight_does_not_depend_on_the_draw():
    m = cart()
    a = [[0, 0.0, 0.01, 0.5], [1, 1.0, 0.02, 0.5]]
    b = [list(p) for p in a]
    rbpf_step(m, a, 0.9, random.Random(1), resample_ratio=0.0)
    rbpf_step(m, b, 0.9, random.Random(7), resample_ratio=0.0)
    assert [p[3] for p in a] == [p[3] for p in b]
    assert abs(sum(p[3] for p in a) - 1.0) < 1e-12


def test_the_likelihood_estimate_is_unbiased():
    """The product of the step likelihoods averages to p(z_(1:t)) over many runs."""
    m = cart()
    _, _, zs = simulate(m, 5, random.Random(3))
    _, _, lik = exact_posterior(m, zs)
    total, runs = 0.0, 300
    for seed in range(runs):
        rng = random.Random(100 + seed)
        particles = initial_particles(m, 8, rng)
        total += math.exp(sum(rbpf_step(m, particles, z, rng, "prior") for z in zs))
    assert abs(total / runs / lik - 1.0) < 0.1


def test_resampling_keeps_the_size_and_resets_the_weights():
    m = cart()
    particles = initial_particles(m, 50, random.Random(5))
    rbpf_step(m, particles, 5.0, random.Random(6), "prior", resample_ratio=1.01)
    assert len(particles) == 50
    assert all(p[3] == 1.0 / 50 for p in particles)
    assert abs(effective_size(particles) - 50.0) < 1e-9


def test_fewer_particles_than_a_plain_particle_filter():
    """A measurement: at the same N, the RBPF error is smaller than the error of a filter that samples x too."""
    m = cart()
    _, _, zs = simulate(m, 8, random.Random(1))
    mean, _, _ = exact_posterior(m, zs)
    err_rb, err_pf = 0.0, 0.0
    for seed in range(20):
        err_rb += (rbpf(m, zs, 100, random.Random(seed))[-1][0] - mean) ** 2
        err_pf += (bootstrap_pf(m, zs, 100, random.Random(seed))[-1] - mean) ** 2
    assert err_rb < err_pf
