# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayes-theorem/. The authors are listed in prov/ND3FAB.jsonl.

import itertools
import random
from fractions import Fraction as F

from bayes_theorem import odds_to_probability, posterior, posterior_odds, probability_to_odds


def test_base_rate_example_exact() -> None:
    # prevalence 1/1000, sensitivity 1, false positive rate 5/100
    post = posterior([F(1, 1000), F(999, 1000)], [F(1), F(5, 100)])
    assert post[0] == F(20, 1019)
    assert sum(post) == 1
    # a prevalence of 1/10 with the same test
    assert posterior([F(1, 10), F(9, 10)], [F(1), F(5, 100)])[0] == F(20, 29)
    # sensitivity 99/100
    assert posterior([F(1, 1000), F(999, 1000)], [F(99, 100), F(5, 100)])[0] == F(11, 566)


def test_odds_form_matches_probability_form() -> None:
    rng = random.Random(1763)
    for _ in range(200):
        p = F(rng.randint(1, 99), 100)
        la = F(rng.randint(1, 100), 100)
        lb = F(rng.randint(1, 100), 100)
        direct = posterior([p, 1 - p], [la, lb])[0]
        via_odds = odds_to_probability(posterior_odds(probability_to_odds(p), la / lb))
        assert direct == via_odds


def test_two_conditionally_independent_tests() -> None:
    # The joint over (disease, test1, test2) with tests independent given disease.
    prev, sens, fpr = F(1, 1000), F(1), F(5, 100)
    joint = {}
    for d, t1, t2 in itertools.product((0, 1), repeat=3):
        pd = prev if d else 1 - prev
        pt = sens if d else fpr
        joint[d, t1, t2] = pd * (pt if t1 else 1 - pt) * (pt if t2 else 1 - pt)
    by_enumeration = joint[1, 1, 1] / (joint[1, 1, 1] + joint[0, 1, 1])
    odds = probability_to_odds(prev)
    for _ in range(2):
        odds = posterior_odds(odds, sens / fpr)
    assert odds == F(400, 999)
    assert odds_to_probability(odds) == by_enumeration == F(400, 1399)
    # sequential update with the posterior as the new prior
    once = posterior([prev, 1 - prev], [sens, fpr])
    twice = posterior(once, [sens, fpr])
    assert twice[0] == by_enumeration


def test_partition_form_against_joint_table() -> None:
    rng = random.Random(7)
    for k in range(1, 6):
        w = [F(rng.randint(1, 20)) for _ in range(k)]
        prior = [x / sum(w) for x in w]
        lik = [F(rng.randint(0, 10), 10) for _ in range(k)]
        if sum(lik) == 0:
            lik[0] = F(1, 2)
        post = posterior(prior, lik)
        assert sum(post) == 1
        evidence = sum(p * l for p, l in zip(prior, lik))
        for j in range(k):
            # Pr(A_j | B) Pr(B) = Pr(B | A_j) Pr(A_j) = Pr(A_j and B)
            assert post[j] * evidence == lik[j] * prior[j]


def test_zero_evidence_is_rejected() -> None:
    try:
        posterior([F(1, 2), F(1, 2)], [F(0), F(0)])
    except ValueError:
        return
    raise AssertionError("expected ValueError")
