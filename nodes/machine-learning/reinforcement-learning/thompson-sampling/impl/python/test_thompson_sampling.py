# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/thompson-sampling/. The authors are listed in prov/JKGDPY.jsonl.

import math
import random
from fractions import Fraction
from math import comb

from thompson_sampling import bernoulli_arms, mean_regret_curve, posterior, regret, thompson_sampling


def beta_integral(p: int, q: int) -> Fraction:
    """The exact value of the integral of t^p (1 - t)^q over [0, 1], by expanding (1 - t)^q."""
    return sum((Fraction((-1) ** j * comb(q, j), p + j + 1) for j in range(q + 1)), Fraction(0))


def bayes_moment(prior: tuple[int, int], outcomes: list[int], m: int) -> Fraction:
    """E[theta^m] under prior density times likelihood, normalized, all exact.

    The prior density is proportional to t^(a-1) (1-t)^(b-1). Each outcome multiplies
    the density by t (a success) or by 1 - t (a failure). This is Bayes' rule with no
    use of the conjugate formula.
    """
    a, b = prior
    s = sum(outcomes)
    f = len(outcomes) - s
    p, q = a - 1 + s, b - 1 + f
    return beta_integral(p + m, q) / beta_integral(p, q)


def beta_moment(a: int, b: int, m: int) -> Fraction:
    out = Fraction(1)
    for j in range(m):
        out *= Fraction(a + j, a + b + j)
    return out


def ucb1_curve(means: list[float], checkpoints: list[int], seeds) -> list[float]:
    """UCB1 of Auer, Cesa-Bianchi and Fischer, for comparison, with arms Random(s)."""
    k, n, best = len(means), max(checkpoints), max(means)
    out = [0.0] * len(checkpoints)
    for s in seeds:
        pull = bernoulli_arms(means, random.Random(s))
        counts, sums = [1] * k, [float(pull(a)) for a in range(k)]
        acc, j = sum(best - m for m in means), 0
        for t in range(k + 1, n + 1):
            lg = math.log(t - 1)
            a = max(range(k), key=lambda i: sums[i] / counts[i] + math.sqrt(2 * lg / counts[i]))
            sums[a] += pull(a)
            counts[a] += 1
            acc += best - means[a]
            while j < len(checkpoints) and checkpoints[j] == t:
                out[j] += acc
                j += 1
    return [v / len(seeds) for v in out]


def test_posterior_update_is_bayes_rule_exactly() -> None:
    rng = random.Random(1)
    for prior in [(1, 1), (2, 5), (3, 1)]:
        for length in range(0, 9):
            outcomes = [rng.randrange(2) for _ in range(length)]
            a, b = posterior(prior, outcomes)
            for m in range(1, 5):
                assert bayes_moment(prior, outcomes, m) == beta_moment(a, b, m)


def test_posterior_mean_by_hand() -> None:
    # Uniform prior, then 1, 0, 1: the posterior is Beta(3, 2) with mean 3/5.
    a, b = posterior((1, 1), [1, 0, 1])
    assert (a, b) == (3, 2)
    assert bayes_moment((1, 1), [1, 0, 1], 1) == Fraction(3, 5)


def test_trace_of_the_page() -> None:
    trace: list = []
    actions, rewards, alpha, beta = thompson_sampling(
        bernoulli_arms([0.7, 0.5, 0.3], random.Random(103)), 3, 10, random.Random(3), trace=trace
    )
    assert actions == [2, 2, 2, 0, 1, 0, 1, 0, 1, 1]
    assert rewards == [0, 0, 0, 0, 1, 1, 0, 1, 1, 0]
    assert (alpha, beta) == ([3, 3, 1], [2, 3, 4])
    assert [round(x, 3) for x in trace[0]] == [0.257, 0.333, 0.935]


def test_counts_match_the_posterior() -> None:
    actions, rewards, alpha, beta = thompson_sampling(
        bernoulli_arms([0.6, 0.4], random.Random(8)), 2, 500, random.Random(9)
    )
    for i in range(2):
        mine = [r for a, r in zip(actions, rewards) if a == i]
        assert (alpha[i], beta[i]) == posterior((1, 1), mine)


def test_regret_logarithmic_and_below_ucb1() -> None:
    means = [0.9, 0.6, 0.3]
    cps = [1000, 2000, 4000, 8000, 16000]
    ts = mean_regret_curve(means, cps, range(20))
    steps = [b - a for a, b in zip(ts, ts[1:])]
    # Each doubling of n adds about the same regret: growth like log n.
    assert all(0.5 * steps[0] <= s <= 2 * steps[0] for s in steps)
    assert ts[-1] / ts[0] < 2.5
    # UCB1 on the same arm seeds: 38.7, 49.0, 59.1, 69.0, 79.4 (the UCB1 page).
    ucb = ucb1_curve(means, cps, range(20))
    assert [round(u, 1) for u in ucb] == [38.7, 49.0, 59.1, 69.0, 79.4]
    assert all(x < u / 3 for x, u in zip(ts, ucb))
    # The Lai-Robbins rate for these arms is about 1.545 ln n; one doubling adds about 1.07.
    lr_step = math.log(2) * (0.3 / 0.31119 + 0.6 / 1.03256)
    assert all(0.5 * lr_step <= s <= 2 * lr_step for s in steps)


def test_fractional_rewards_use_a_bernoulli_trial() -> None:
    actions, rewards, alpha, beta = thompson_sampling(lambda a: 0.5, 2, 200, random.Random(4))
    assert sum(alpha) + sum(beta) == 4 + 200
    assert regret([0.5, 0.5], actions) == 0
