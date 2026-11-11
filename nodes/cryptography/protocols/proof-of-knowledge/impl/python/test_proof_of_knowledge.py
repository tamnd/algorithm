# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proof-of-knowledge/. The authors are listed in prov/2JJVZ2.jsonl.
# There are no official test vectors for proofs of knowledge. The tests run a
# rewinding extractor against local simulated provers in a toy group.

import random

from proof_of_knowledge import (
    G,
    P,
    Q,
    GuessingProver,
    PartialProver,
    accepting_challenges,
    extract,
    run,
    success_probability,
    verify,
)

X = 777
Y = pow(G, X, P)
FULL = list(range(Q))


def test_group():
    assert (P - 1) // 2 == Q and pow(G, Q, P) == 1 and G != 1


def test_honest_prover_is_accepted():
    prover = PartialProver(X, 100)
    for tape in range(50):
        assert run(prover, Y, tape, tape * 37 % Q) is not None


def test_extractor_recovers_x_from_a_weak_prover():
    rng = random.Random(1)
    for percent in (100, 30, 5):
        prover = PartialProver(X, percent, seed=percent)
        x, runs = extract(prover, Y, FULL, rng)
        assert x == X
        assert runs == prover.calls


def test_extractor_cost_grows_like_one_over_epsilon():
    # Expected runs are about 2 / epsilon. Average over many extractions.
    rng = random.Random(2)
    for percent in (50, 10):
        eps = percent / 100
        total = 0
        trials = 60
        for s in range(trials):
            x, runs = extract(PartialProver(X, percent, seed=1000 + s), Y, FULL, rng)
            assert x == X
            total += runs
        mean = total / trials
        assert 0.5 * (2 / eps) < mean < 2.0 * (2 / eps)


def test_two_transcripts_give_the_witness():
    prover = PartialProver(X, 100)
    tape, c1, c2 = 5, 3, 10
    z1, z2 = run(prover, Y, tape, c1), run(prover, Y, tape, c2)
    a = prover.commit(tape)
    assert verify(Y, a, c1, z1) and verify(Y, a, c2, z2)
    assert (z1 - z2) * pow(c1 - c2, -1, Q) % Q == X


def test_guessing_prover_has_success_exactly_one_over_c():
    small = list(range(8))
    cheater = GuessingProver(Y, small)
    tapes = range(300)
    # For each tape exactly one challenge is accepted ...
    for tape in tapes:
        assert len(accepting_challenges(cheater, Y, tape, small)) == 1
    # ... so the success probability is exactly 1/|C|.
    assert success_probability(cheater, Y, small, tapes) == 1 / 8


def test_extractor_fails_against_the_guessing_prover():
    rng = random.Random(3)
    cheater = GuessingProver(Y, list(range(8)))
    x, runs = extract(cheater, Y, list(range(8)), rng, budget=3000)
    assert x is None and runs == 3000


def test_extractor_succeeds_just_above_the_knowledge_error():
    # A prover that knows x but answers only 2 of the 8 challenges on each
    # tape has success 1/4 > 1/8, and two accepting challenges per tape are
    # enough to extract.
    class TwoOfEight(PartialProver):
        def respond(self, tape, c):
            self.calls += 1
            if c not in (tape % 8, (tape + 3) % 8):
                return None
            return (self.k(tape) + c * self.x) % Q

    small = list(range(8))
    prover = TwoOfEight(X, 0)
    assert success_probability(prover, Y, small, range(200)) == 0.25
    x, _ = extract(prover, Y, small, random.Random(4))
    assert x == X
