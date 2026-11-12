# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/evidence-lower-bound/. The authors are listed in prov/9XGGSJ.jsonl.

import math
import random
from fractions import Fraction as F

from evidence_lower_bound import (
    add_logs,
    elbo,
    elbo_jensen_terms,
    evidence,
    exact_elbo,
    exact_kl,
    exact_log,
    exact_log_evidence,
    kl,
    posterior,
    to_float,
)

# p(z) = (1/2, 1/3, 1/6), p(x | z) = (1/4, 1/2, 3/4) for the observed x.
PRIOR = [F(1, 2), F(1, 3), F(1, 6)]
LIK = [F(1, 4), F(1, 2), F(3, 4)]
JOINT = [a * b for a, b in zip(PRIOR, LIK)]


def test_worked_example_values():
    assert JOINT == [F(1, 8), F(1, 6), F(1, 8)]
    assert evidence(JOINT) == F(5, 12)
    assert posterior(JOINT) == [F(3, 10), F(2, 5), F(3, 10)]
    q = [F(1, 3)] * 3
    # ELBO = (1/3) log(9/128) and KL = (1/3) log(250/243).
    third = F(1, 3)
    assert exact_elbo(JOINT, q) == {p: third * e for p, e in exact_log(F(9, 128)).items()}
    assert exact_kl(q, posterior(JOINT)) == {p: third * e for p, e in exact_log(F(250, 243)).items()}


def test_identity_exact_on_uniform_q():
    q = [F(1, 3)] * 3
    lhs = exact_log_evidence(JOINT)
    rhs = add_logs(exact_elbo(JOINT, q), exact_kl(q, posterior(JOINT)))
    assert lhs == rhs


def test_identity_exact_on_random_rational_q():
    rng = random.Random(1)
    post = posterior(JOINT)
    for _ in range(50):
        w = [rng.randint(1, 20) for _ in range(3)]
        q = [F(v, sum(w)) for v in w]
        assert exact_log_evidence(JOINT) == add_logs(exact_elbo(JOINT, q), exact_kl(q, post))


def test_identity_exact_on_random_models():
    rng = random.Random(2)
    for _ in range(30):
        k = rng.randint(2, 5)
        joint = [F(rng.randint(1, 30), rng.randint(31, 90)) for _ in range(k)]
        w = [rng.randint(0, 9) for _ in range(k)]
        if sum(w) == 0:
            w[0] = 1
        q = [F(v, sum(w)) for v in w]
        lhs = exact_log_evidence(joint)
        rhs = add_logs(exact_elbo(joint, q), exact_kl(q, posterior(joint)))
        assert lhs == rhs


def test_gap_zero_iff_q_is_posterior():
    post = posterior(JOINT)
    assert exact_kl(post, post) == {}
    assert exact_elbo(JOINT, post) == exact_log_evidence(JOINT)
    q = [F(1, 3)] * 3
    assert to_float(exact_kl(q, post)) > 0


def test_float_bound_and_jensen():
    rng = random.Random(3)
    joint = [float(v) for v in JOINT]
    logpx = math.log(sum(joint))
    for _ in range(200):
        w = [rng.random() for _ in range(3)]
        q = [v / sum(w) for v in w]
        val = elbo(joint, q)
        assert val <= logpx + 1e-12
        assert abs(val + kl(q, [v / sum(joint) for v in joint]) - logpx) < 1e-12
        jensen_left, jensen_right = elbo_jensen_terms(joint, q)
        assert jensen_right <= jensen_left + 1e-12


def test_q_with_smaller_support():
    # q puts no mass on z = 2: the bound still holds, and the gap is the KL.
    q = [F(1, 2), F(1, 2), F(0)]
    lhs = exact_log_evidence(JOINT)
    rhs = add_logs(exact_elbo(JOINT, q), exact_kl(q, posterior(JOINT)))
    assert lhs == rhs
    joint = [float(v) for v in JOINT]
    left, right = elbo_jensen_terms(joint, [0.5, 0.5, 0.0])
    assert abs(left - math.log(1 / 8 + 1 / 6)) < 1e-12
    assert right < left


def test_float_matches_exact():
    q = [F(1, 3)] * 3
    assert abs(to_float(exact_elbo(JOINT, q)) - elbo([float(v) for v in JOINT], [1 / 3] * 3)) < 1e-12
