# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epidemic-data-augmentation-mcmc/. The authors are listed in prov/YHHCY9.jsonl.

import math
import random

from epidemic_data_augmentation_mcmc import (
    Prior,
    initial_infection_times,
    log_infection_term,
    log_likelihood,
    pair_terms,
    pressure_integral,
    run,
    simulate_labeled,
)


def event_log_likelihood(inf, rem, n_pop, beta, gamma):
    """The same density by a sweep over the events: the log rate of each
    labelled event, minus the integral of the total rate between events."""
    events = sorted([(t, "inf", j) for j, t in enumerate(inf)] + [(t, "rem", j) for j, t in enumerate(rem)])
    s, i, last, total, started = n_pop, 0, None, 0.0, False
    for t, kind, _ in events:
        if started:
            total -= (beta * s * i / n_pop + gamma * i) * (t - last)
        if kind == "inf":
            if started:
                total += math.log(beta * i / n_pop)  # rate beta S I / N, then 1/S for the label
            started = True
            s, i = s - 1, i + 1
        else:
            total += math.log(gamma)  # rate gamma I, then 1/I for the label
            i -= 1
        last = t
    return total


def test_likelihood_matches_event_sweep():
    for seed in (3, 7, 9):
        inf, rem = simulate_labeled(random.Random(seed), 30, 2.0, 1.0)
        for beta, gamma in ((2.0, 1.0), (0.7, 1.9)):
            got = log_likelihood(inf, rem, 30, beta, gamma)
            want = event_log_likelihood(inf, rem, 30, beta, gamma)
            assert abs(got - want) < 1e-8 * max(1.0, abs(want))


def test_pair_terms_give_the_change_of_the_integral():
    inf, rem = simulate_labeled(random.Random(3), 30, 2.0, 1.0)
    a = pressure_integral(inf, rem, 30)
    for j in (0, 5, len(inf) - 1):
        new = list(inf)
        new[j] = rem[j] - 0.37
        delta = pair_terms(j, new, rem, 30) - pair_terms(j, inf, rem, 30)
        assert abs(a + delta - pressure_integral(new, rem, 30)) < 1e-9


def test_impossible_epidemics_have_zero_likelihood():
    # Case 1 is infected at time 2, after case 0 was removed at time 1.
    assert log_infection_term([0.0, 2.0], [1.0, 3.0]) == -math.inf
    assert log_likelihood([0.0, 2.0], [1.0, 3.0], 5, 1.0, 1.0) == -math.inf
    assert log_infection_term([0.0, 0.5], [1.0, 3.0]) == 0.0
    start = initial_infection_times([4.0, 1.0, 2.5])
    assert log_infection_term(start, [4.0, 1.0, 2.5]) > -math.inf


def exact_moments(rem, n_pop, prior, m=300):
    """E[r_1 - i_1], E[r_2 - i_2] and P(i_2 < i_1) for two cases, with beta
    and gamma integrated out, by the midpoint rule on d = t / (1 - t)."""
    n = len(rem)

    def log_marg(inf):
        li = log_infection_term(inf, rem)
        if li == -math.inf:
            return -math.inf
        a = pressure_integral(inf, rem, n_pop)
        d = sum(r - i for i, r in zip(inf, rem))
        return (li - (prior.a_beta + n - 1) * math.log(prior.b_beta + a / n_pop)
                - (prior.a_gamma + n) * math.log(prior.b_gamma + d))

    tot = e1 = e2 = p = 0.0
    for x in range(m):
        t1 = (x + 0.5) / m
        d1 = t1 / (1 - t1)
        for y in range(m):
            t2 = (y + 0.5) / m
            d2 = t2 / (1 - t2)
            lp = log_marg([rem[0] - d1, rem[1] - d2])
            if lp == -math.inf:
                continue
            w = math.exp(lp) / ((1 - t1) * (1 - t2)) ** 2
            tot += w
            e1 += w * d1
            e2 += w * d2
            p += w * (rem[1] - d2 < rem[0] - d1)
    return e1 / tot, e2 / tot, p / tot


def batch_means(xs, batches=40):
    size = len(xs) // batches
    means = [sum(xs[k * size:(k + 1) * size]) / size for k in range(batches)]
    mu = sum(means) / batches
    var = sum((v - mu) ** 2 for v in means) / (batches - 1)
    return mu, math.sqrt(var / batches)


def test_chain_matches_exact_posterior_of_infection_times():
    rem, n_pop = [1.0, 2.5], 3
    prior = Prior(3.0, 2.0, 3.0, 2.0)
    exact = exact_moments(rem, n_pop, prior)
    _, _, infs = run(random.Random(20261118), rem, n_pop, prior, 30000)
    stats = (
        [rem[0] - x[0] for x in infs],
        [rem[1] - x[1] for x in infs],
        [1.0 if x[1] < x[0] else 0.0 for x in infs],
    )
    for xs, want in zip(stats, exact):
        mu, se = batch_means(xs)
        assert abs(mu - want) <= 4 * se + 3e-3


def test_parameters_are_recovered_from_a_simulated_epidemic():
    inf, rem = simulate_labeled(random.Random(3), 30, 2.0, 1.0)
    assert len(rem) == 24
    betas, gammas, _ = run(random.Random(1), rem, 30, Prior(1.0, 1.0, 1.0, 1.0), 800)
    betas, gammas = sorted(betas[200:]), sorted(gammas[200:])
    k = len(betas)
    assert betas[int(0.025 * k)] < 2.0 < betas[int(0.975 * k)]
    assert gammas[int(0.025 * k)] < 1.0 < gammas[int(0.975 * k)]
