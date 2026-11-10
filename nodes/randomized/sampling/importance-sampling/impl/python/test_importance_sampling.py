# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/importance-sampling/. The authors are listed in prov/ES82YY.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

from importance_sampling import (
    effective_sample_size,
    exact_mean_and_variance,
    is_estimate,
    optimal_proposal,
    rare_event_normal_tail,
    snis_estimate,
)

# The example of the page: p = (7/10, 2/10, 1/10), f = (0, 1, 10), mu = 6/5.
P = {1: F(7, 10), 2: F(2, 10), 3: F(1, 10)}
FV = {1: F(0), 2: F(1), 3: F(10)}
Q = {1: F(1, 3), 2: F(1, 3), 3: F(1, 3)}
MU = F(6, 5)


def law_of_estimator(estimator, q, n):
    """The exact law of an estimator over all n-tuples drawn from q."""
    law = {}
    for xs in itertools.product(list(q), repeat=n):
        pr = F(1)
        for x in xs:
            pr *= q[x]
        if pr == 0:
            continue
        v = estimator(xs)
        law[v] = law.get(v, F(0)) + pr
    return law


def mean(law):
    return sum(v * pr for v, pr in law.items())


def var(law):
    m = mean(law)
    return sum((v - m) ** 2 * pr for v, pr in law.items())


def is_exact(xs, p=P, q=Q, f=FV):
    return sum(p[x] / q[x] * f[x] for x in xs) / len(xs)


def snis_exact(xs, p_tilde, q=Q, f=FV):
    w = [p_tilde[x] / q[x] for x in xs]
    return sum(wi * f[x] for wi, x in zip(w, xs)) / sum(w)


def test_example_numbers() -> None:
    m1, v1 = exact_mean_and_variance(FV, P, Q)
    assert m1 == MU and v1 == F(42, 25)  # 3.12 - 1.44 = 1.68
    plain = sum(P[x] * FV[x] ** 2 for x in P) - MU ** 2
    assert plain == F(219, 25)  # 8.76
    qs = optimal_proposal(FV, P)
    assert qs == {1: F(0), 2: F(1, 6), 3: F(5, 6)}


def test_unbiased_and_variance_exact() -> None:
    for n in [1, 2, 3, 4]:
        law = law_of_estimator(is_exact, Q, n)
        assert mean(law) == MU
        assert var(law) == F(42, 25) / n
    # Another proposal.
    q2 = {1: F(1, 2), 2: F(1, 4), 3: F(1, 4)}
    law = law_of_estimator(lambda xs: is_exact(xs, q=q2), q2, 3)
    assert mean(law) == MU


def test_zero_variance_proposal() -> None:
    qs = optimal_proposal(FV, P)
    law = law_of_estimator(lambda xs: is_exact(xs, q=qs), qs, 3)
    assert law == {MU: F(1)}


def test_optimal_is_best_among_many() -> None:
    rng = random.Random(1)
    _, best = exact_mean_and_variance(FV, P, optimal_proposal(FV, P))
    assert best == 0
    for _ in range(200):
        a = [rng.randint(1, 20) for _ in range(3)]
        q = {x: F(a[x - 1], sum(a)) for x in (1, 2, 3)}
        m1, v1 = exact_mean_and_variance(FV, P, q)
        assert m1 == MU and v1 >= best


def test_missing_support_is_biased() -> None:
    # q = 0 where f p != 0: the third value is never drawn.
    q = {1: F(1, 2), 2: F(1, 2), 3: F(0)}
    law = law_of_estimator(lambda xs: is_exact(xs, q=q), q, 2)
    assert mean(law) == F(1, 5)
    assert mean(law) != MU


def test_wrong_variant_no_weights() -> None:
    # Averaging f under q, without the weights, estimates E_q[f], not E_p[f].
    law = law_of_estimator(lambda xs: sum(FV[x] for x in xs) / len(xs), Q, 2)
    assert mean(law) == F(11, 3) and mean(law) != MU


def test_self_normalized_bias() -> None:
    p_tilde = {x: 5 * P[x] for x in P}  # the constant does not matter
    biases = []
    for n in [1, 2, 3, 4, 5]:
        law = law_of_estimator(lambda xs: snis_exact(xs, p_tilde), Q, n)
        law_scaled = law_of_estimator(lambda xs: snis_exact(xs, P), Q, n)
        assert law == law_scaled
        biases.append(mean(law) - MU)
    assert biases[0] == F(11, 3) - MU  # n = 1 gives f(X_1), so E_q[f]
    assert all(b != 0 for b in biases)
    assert all(abs(biases[i + 1]) < abs(biases[i]) for i in range(4))
    # The first-order bias -E_q[w^2 (f - mu)] / n with w = p / q.
    lead = -sum(Q[x] * (P[x] / Q[x]) ** 2 * (FV[x] - MU) for x in Q)
    assert lead == F(381, 250)
    # n * bias is 2.4667, 2.4765, 2.3147, ... and moves toward the first-order value 1.524.
    law8 = law_of_estimator(lambda xs: snis_exact(xs, P), Q, 8)
    nb8 = 8 * (mean(law8) - MU)
    assert lead < nb8 < 5 * biases[4] and abs(float(nb8 - lead)) < 0.4


def test_effective_sample_size() -> None:
    assert effective_sample_size([1, 1, 1, 1]) == 4
    assert effective_sample_size([1, 0, 0, 0]) == 1
    assert abs(effective_sample_size([3, 1]) - 1.6) < 1e-12
    # N(0, 1) target, N(0, 4) proposal: ESS / n -> 1 / E_q[w^2] = sqrt(7) / 4.
    rng = random.Random(1992)
    n = 100000
    est, ess = snis_estimate(
        lambda x: x * x,
        lambda x: math.exp(-0.5 * x * x),
        lambda x: math.exp(-x * x / 8.0),
        lambda r: r.gauss(0.0, 2.0),
        n,
        rng,
    )
    assert abs(est - 1.0) < 0.03
    assert abs(ess / n - math.sqrt(7) / 4) < 0.02


def test_rare_event() -> None:
    rng = random.Random(4)
    c = 4.0
    truth = 0.5 * math.erfc(c / math.sqrt(2.0))
    n = 20000
    est = rare_event_normal_tail(c, n, rng)
    # Var of one term: E_q[w^2 1{X > c}] - truth^2 = e^{c^2} Pr[N(0, 1) > 2c] - truth^2.
    sd_one = math.sqrt(math.exp(c * c) * 0.5 * math.erfc(2 * c / math.sqrt(2.0)) - truth ** 2)
    assert abs(est - truth) < 6 * sd_one / math.sqrt(n)
    assert abs(est - truth) / truth < 0.05


def test_plain_is_continuous() -> None:
    # E_p[X^2] = 1 under N(0, 1), with a N(0, 4) proposal and normalized densities.
    rng = random.Random(8)
    est = is_estimate(
        lambda x: x * x,
        lambda x: math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi),
        lambda x: math.exp(-x * x / 8.0) / math.sqrt(8 * math.pi),
        lambda r: r.gauss(0.0, 2.0),
        100000,
        rng,
    )
    assert abs(est - 1.0) < 0.03
