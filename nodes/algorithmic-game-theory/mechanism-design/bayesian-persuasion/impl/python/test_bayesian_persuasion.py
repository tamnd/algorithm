# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-persuasion/. The authors are listed in prov/7DNF62.jsonl.

import random
from fractions import Fraction

from bayesian_persuasion import optimal_scheme, posteriors, receiver_action, sender_value

F = Fraction
SEED = 20251120


def test_prosecutor_example():
    # States: 0 innocent, 1 guilty. Actions: 0 acquit, 1 convict.
    prior = [F(7, 10), F(3, 10)]
    judge = [[1, 0], [0, 1]]
    prosecutor = [[0, 1], [0, 1]]
    value, scheme = optimal_scheme(prior, judge, prosecutor)
    assert value == F(3, 5)
    assert scheme[1] == [0, 1] and scheme[0] == [F(4, 7), F(3, 7)]
    # The posterior after "convict" makes the judge exactly indifferent.
    post = {a: q for a, _, q in posteriors(prior, scheme)}
    assert post[1] == [F(1, 2), F(1, 2)] and post[0] == [1, 0]
    # Without information the judge acquits; with full information the conviction rate is 3/10.
    assert sender_value(prior, judge, prosecutor) == 0


def concave_closure_binary(mu0, receiver, sender):
    """Brute force: the concave closure of the sender's value at mu0 for two states."""
    A = len(receiver[0])
    points = {F(0), F(1)}
    for a in range(A):
        for b in range(A):
            d0 = F(receiver[0][a] - receiver[0][b])
            d1 = F(receiver[1][a] - receiver[1][b])
            if d0 != d1:
                mu = d0 / (d0 - d1)
                if 0 <= mu <= 1:
                    points.add(mu)

    def v(mu):
        return sender_value([1 - mu, mu], receiver, sender)

    best = v(mu0) if mu0 in points else None
    for lo in points:
        for hi in points:
            if lo <= mu0 <= hi and lo < hi:
                val = v(lo) + (v(hi) - v(lo)) * (mu0 - lo) / (hi - lo)
                best = val if best is None else max(best, val)
    return best


def test_matches_concavification_two_states():
    rng = random.Random(SEED)
    for _ in range(25):
        A = rng.randint(2, 4)
        receiver = [[rng.randint(-4, 4) for _ in range(A)] for _ in range(2)]
        sender = [[rng.randint(-4, 4) for _ in range(A)] for _ in range(2)]
        mu0 = F(rng.randint(1, 9), 10)
        value, _ = optimal_scheme([1 - mu0, mu0], receiver, sender)
        assert value == concave_closure_binary(mu0, receiver, sender)


def random_instance(rng, S, A):
    weights = [rng.randint(1, 5) for _ in range(S)]
    prior = [F(w, sum(weights)) for w in weights]
    receiver = [[rng.randint(-3, 3) for _ in range(A)] for _ in range(S)]
    sender = [[rng.randint(-3, 3) for _ in range(A)] for _ in range(S)]
    return prior, receiver, sender


def test_scheme_is_obedient_and_attains_value():
    rng = random.Random(SEED + 1)
    for _ in range(15):
        prior, receiver, sender = random_instance(rng, rng.randint(2, 4), rng.randint(2, 4))
        value, scheme = optimal_scheme(prior, receiver, sender)
        for row in scheme:
            assert all(p >= 0 for p in row) and sum(row) == 1
        total = F(0)
        for a, p, post in posteriors(prior, scheme):
            best = max(sum(post[w] * receiver[w][b] for w in range(len(prior))) for b in range(len(receiver[0])))
            assert sum(post[w] * receiver[w][a] for w in range(len(prior))) == best
            total += p * sender_value(post, receiver, sender)
        # Bayes plausibility: the posteriors average back to the prior.
        for w in range(len(prior)):
            assert sum(p * post[w] for _, p, post in posteriors(prior, scheme)) == prior[w]
        assert total == value


def test_at_least_no_information_and_full_information():
    rng = random.Random(SEED + 2)
    for _ in range(15):
        S = rng.randint(2, 4)
        prior, receiver, sender = random_instance(rng, S, rng.randint(2, 4))
        value, _ = optimal_scheme(prior, receiver, sender)
        no_info = sender_value(prior, receiver, sender)
        full = sum(prior[w] * sender_value([F(int(k == w)) for k in range(S)], receiver, sender) for w in range(S))
        assert value >= no_info and value >= full
        assert value <= sum(prior[w] * max(sender[w]) for w in range(S))


def test_aligned_interests_reveal_everything():
    rng = random.Random(SEED + 3)
    for _ in range(10):
        S = rng.randint(2, 4)
        prior, receiver, _ = random_instance(rng, S, rng.randint(2, 4))
        value, _ = optimal_scheme(prior, receiver, receiver)
        full = sum(prior[w] * max(receiver[w]) for w in range(S))
        assert value == full


def test_receiver_action_breaks_ties_for_sender():
    receiver = [[1, 0], [0, 1]]
    sender = [[0, 1], [0, 1]]
    assert receiver_action([F(1, 2), F(1, 2)], receiver, sender) == 1
    assert receiver_action([F(3, 5), F(2, 5)], receiver, sender) == 0


def test_bad_prior():
    try:
        optimal_scheme([F(1, 2), F(1, 3)], [[0], [0]], [[0], [0]])
    except ValueError:
        return
    raise AssertionError("expected ValueError")
