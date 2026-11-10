# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reversible-jump-mcmc/. The authors are listed in prov/183JNF.jsonl.

import math
import random

import pytest

from reversible_jump_mcmc import DimensionJump, log_up_ratio, reversible_jump_mcmc


def ess(xs):
    """Effective sample size by Geyer's initial positive sequence."""
    n = len(xs)
    m = sum(xs) / n
    c = [x - m for x in xs]
    var = sum(v * v for v in c) / n
    if var == 0:
        return 1.0

    def rho(k):
        return sum(c[i] * c[i + k] for i in range(n - k)) / (n * var)

    tau, k = -1.0, 0
    while k + 1 < n:
        g = rho(k) + rho(k + 1)
        if g <= 0:
            break
        tau += 2 * g
        k += 2
    return n / max(tau, 1e-9)


def check_mean(xs, mu, sd):
    # the sample mean has standard error about sd / sqrt(ESS)
    assert abs(sum(xs) / len(xs) - mu) < 5 * sd / math.sqrt(ess(xs))


LOG_NORMAL = -0.5 * math.log(2 * math.pi)


def log_phi(x):
    return LOG_NORMAL - x * x / 2


WEIGHTS = (0.3, 0.7)


def log_target(k, theta):
    # model 0: theta in R with density N(0, 1); model 1: theta in R^2 with density N(0, I_2)
    return math.log(WEIGHTS[k]) + sum(log_phi(t) for t in theta)


def rwm(log_t, sigma=1.0):
    def step(k, theta, rng):
        new = tuple(t + sigma * rng.gauss(0.0, 1.0) for t in theta)
        d = log_t(k, new) - log_t(k, theta)
        return new if d >= 0 or rng.random() < math.exp(d) else theta

    return step


def split_merge(log_jacobian=math.log(2)):
    # (theta, u) -> (theta - u, theta + u), whose Jacobian determinant is 2 in absolute value
    return DimensionJump(
        draw_u=lambda rng: rng.gauss(0.0, 1.0),
        log_u_density=log_phi,
        up=lambda theta, u: (theta[0] - u, theta[0] + u),
        down=lambda t: (((t[0] + t[1]) / 2,), (t[1] - t[0]) / 2),
        log_jacobian=lambda theta, u: log_jacobian,
    )


def test_page_example_ratio() -> None:
    jump = split_merge()
    new = jump.up((0.2,), 0.5)
    assert new == pytest.approx((-0.3, 0.7))
    r = math.exp(log_up_ratio(log_target, jump, 0, (0.2,), 0.5, new))
    assert r == pytest.approx(14 / 3 * math.exp(-0.145))
    assert round(r, 3) == 4.037


def test_detailed_balance_with_the_jacobian() -> None:
    # pi(0, theta) g(u) a_up = pi(1, theta') a_down |J|, the density form of detailed balance
    rng = random.Random(1)
    jump = split_merge()
    for _ in range(200):
        theta, u = (rng.gauss(0, 2),), rng.gauss(0, 2)
        new = jump.up(theta, u)
        back, u_back = jump.down(new)
        assert back[0] == pytest.approx(theta[0]) and u_back == pytest.approx(u)
        a_up = min(1.0, math.exp(log_up_ratio(log_target, jump, 0, theta, u, new)))
        a_down = min(1.0, math.exp(-log_up_ratio(log_target, jump, 0, theta, u, new)))
        left = math.exp(log_target(0, theta) + log_phi(u)) * a_up
        right = math.exp(log_target(1, new)) * a_down * 2
        assert left == pytest.approx(right, rel=1e-9)


def model_fraction(jump, seed, n=40000):
    chain, prop, acc = reversible_jump_mcmc(log_target, rwm(log_target), [jump], 0, (0.0,), n, random.Random(seed))
    return chain, [float(k) for k, _ in chain], acc / prop


def test_model_probabilities_recovered() -> None:
    chain, ks, rate = model_fraction(split_merge(), 2)
    check_mean(ks, 0.7, math.sqrt(0.21))
    assert 0.3 < rate < 0.9
    second = [t[1] for k, t in chain if k == 1]
    first = [t[0] for k, t in chain if k == 0]
    check_mean(second, 0.0, 1.0)
    check_mean([t * t for t in first], 1.0, math.sqrt(2))


def test_dropping_the_jacobian_gives_seven_thirteenths() -> None:
    _, ks, _ = model_fraction(split_merge(log_jacobian=0.0), 3)
    check_mean(ks, 7 / 13, math.sqrt(7 / 13 * 6 / 13))
    assert abs(sum(ks) / len(ks) - 0.7) > 0.1


def test_nonconstant_jacobian() -> None:
    # model 1 is an ordered pair theta_1 < theta_2 of two N(0, 1) values, with mass 0.7
    def log_t(k, theta):
        if k == 0:
            return math.log(0.3) + log_phi(theta[0])
        if theta[0] >= theta[1]:
            return -math.inf
        return math.log(0.7 * 2) + log_phi(theta[0]) + log_phi(theta[1])

    jump = DimensionJump(
        draw_u=lambda rng: rng.gauss(0.0, 1.0),
        log_u_density=log_phi,
        up=lambda theta, u: (theta[0], theta[0] + math.exp(u)),
        down=lambda t: ((t[0],), math.log(t[1] - t[0])),
        log_jacobian=lambda theta, u: u,
    )
    chain, prop, acc = reversible_jump_mcmc(log_t, rwm(log_t), [jump], 0, (0.0,), 40000, random.Random(4))
    check_mean([float(k) for k, _ in chain], 0.7, math.sqrt(0.21))
    gaps = [t[1] - t[0] for k, t in chain if k == 1]
    mean_gap = 2 / math.sqrt(math.pi)  # E|X - Y| for independent N(0, 1)
    check_mean(gaps, mean_gap, math.sqrt(2 - mean_gap**2))


def test_three_nested_models() -> None:
    # model k has k + 1 coordinates, all N(0, 1); a birth move appends u ~ N(0, 1) with Jacobian 1
    weights = (0.5, 0.2, 0.3)

    def log_t(k, theta):
        return math.log(weights[k]) + sum(log_phi(t) for t in theta)

    birth = DimensionJump(
        draw_u=lambda rng: rng.gauss(0.0, 1.0),
        log_u_density=log_phi,
        up=lambda theta, u: tuple(theta) + (u,),
        down=lambda t: (t[:-1], t[-1]),
        log_jacobian=lambda theta, u: 0.0,
    )
    chain, _, _ = reversible_jump_mcmc(log_t, rwm(log_t), [birth, birth], 2, (5.0, 5.0, 5.0), 40000, random.Random(5))
    for j, w in enumerate(weights):
        check_mean([float(k == j) for k, _ in chain], w, math.sqrt(w * (1 - w)))


def test_bad_inputs() -> None:
    rng = random.Random(6)
    with pytest.raises(ValueError):
        reversible_jump_mcmc(log_target, rwm(log_target), [split_merge()], 2, (0.0,), 5, rng)

    def zero(k, theta):
        return -math.inf

    with pytest.raises(ValueError):
        reversible_jump_mcmc(zero, rwm(zero), [split_merge()], 0, (0.0,), 5, rng)
