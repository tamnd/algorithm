# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-knowledge-proof/. The authors are listed in prov/EZD2B7.jsonl.
# There are no official test vectors for zero-knowledge proofs. The tests run
# local simulated parties on toy graphs and compare distributions exactly by
# enumeration where the instance is small enough.

import random
from collections import Counter
from fractions import Fraction
from itertools import permutations

from zero_knowledge_proof import (
    ColoringProver,
    GICheater,
    GIProver,
    apply_perm,
    best_cheating_acceptance,
    coloring_run,
    coloring_simulate,
    coloring_verify,
    commit,
    edge,
    gi_run,
    gi_simulate,
    gi_simulate_against,
    gi_verify,
)

N = 4
PERMS = list(permutations(range(N)))
# G0 is the path 0-1-2-3. G1 = pi(G0) for pi = (2, 0, 3, 1).
G0 = frozenset({(0, 1), (1, 2), (2, 3)})
PI = (2, 0, 3, 1)
G1 = apply_perm(PI, G0)
# The star K_{1,3} has 3 edges too but is not isomorphic to the path.
STAR = frozenset({(0, 1), (0, 2), (0, 3)})

# A 3-colorable toy graph: the 4-cycle with one chord.
C4_CHORD = frozenset({(0, 1), (1, 2), (2, 3), (0, 3), (0, 2)})
C4_COLORS = [0, 1, 2, 1]
K4 = frozenset(edge(u, v) for u in range(4) for v in range(u + 1, 4))


# ------------------------------------------------------- graph isomorphism
def test_gi_completeness():
    rng = random.Random(1)
    prover = GIProver(G0, G1, PI, N)
    assert all(gi_run(prover, G0, G1, 40, rng) for _ in range(50))


def test_gi_soundness_error_is_exactly_one_half():
    # For every first message H, at most one challenge bit can be answered
    # when G0 and STAR are not isomorphic: if both could, G0 ~ H ~ STAR.
    orbit0 = {apply_perm(t, G0) for t in PERMS}
    orbit1 = {apply_perm(t, STAR) for t in PERMS}
    assert not orbit0 & orbit1
    # The cheater who guesses the bit wins exactly half of all (guess, tau, b).
    cheater = GICheater(G0, STAR, N)
    wins = total = 0
    for guess in (0, 1):
        for tau in PERMS:
            cheater.guess, cheater.tau = guess, tau
            h = apply_perm(tau, STAR if guess else G0)
            for b in (0, 1):
                total += 1
                wins += gi_verify(G0, STAR, h, b, cheater.answer(b))
    assert Fraction(wins, total) == Fraction(1, 2)


def test_gi_cheater_over_many_rounds():
    rng = random.Random(2)
    cheater = GICheater(G0, STAR, N)
    passed = sum(gi_run(cheater, G0, STAR, 1, rng) for _ in range(4000))
    assert abs(passed / 4000 - 0.5) < 0.04
    passed10 = sum(gi_run(cheater, G0, STAR, 10, rng) for _ in range(4000))
    assert passed10 < 20            # expected 4000 / 1024, about 4


def test_gi_simulator_distribution_is_exact():
    # Real: sigma uniform over 24 permutations, b uniform.
    prover = GIProver(G0, G1, PI, N)
    real = Counter()
    for sigma in PERMS:
        for b in (0, 1):
            h = prover.first(None, sigma=sigma)
            real[(h, b, prover.answer(b))] += 1
    # Simulated: b uniform, tau uniform, H = tau(G_b). No use of PI.
    sim = Counter()
    for b in (0, 1):
        for tau in PERMS:
            sim[gi_simulate(G0, G1, N, None, b=b, tau=tau)] += 1
    assert real == sim
    assert sum(real.values()) == 48
    for h, b, tau in sim:
        assert gi_verify(G0, G1, h, b, tau)


def test_gi_simulator_with_rewinding_for_a_cheating_verifier():
    # This verifier picks b from H in a fixed but odd way.
    def verifier_bit(h):
        return hash(tuple(sorted(h))) & 1

    # Exact: accepted outputs of the rewinding simulator equal the real view.
    prover = GIProver(G0, G1, PI, N)
    real = Counter()
    for sigma in PERMS:
        h = prover.first(None, sigma=sigma)
        b = verifier_bit(h)
        real[(h, b, prover.answer(b))] += 1
    accepted = Counter()
    for guess in (0, 1):
        for tau in PERMS:
            h = apply_perm(tau, G1 if guess else G0)
            if verifier_bit(h) == guess:
                accepted[(h, guess, tau)] += 1
    assert real == accepted
    # Run the simulator itself: about 2 tries per transcript.
    rng = random.Random(3)
    tries = 0
    for _ in range(2000):
        (h, b, tau), t = gi_simulate_against(verifier_bit, G0, G1, N, rng)
        assert b == verifier_bit(h) and gi_verify(G0, G1, h, b, tau)
        tries += t
    assert 1.8 < tries / 2000 < 2.2


# ------------------------------------------------------- 3-coloring
def test_coloring_completeness():
    rng = random.Random(4)
    prover = ColoringProver(C4_CHORD, C4_COLORS)
    assert all(coloring_run(prover, C4_CHORD, 30, rng) for _ in range(30))


def test_k4_best_cheater_passes_exactly_five_sixths():
    good, total = best_cheating_acceptance(K4, 4)
    assert Fraction(good, total) == Fraction(5, 6)
    # Each graph that is not 3-colorable has error at most 1 - 1/|E|.
    assert good <= total - 1


def test_k4_cheater_frequency():
    # The cheater commits to the best improper coloring (one bad edge 0-1).
    rng = random.Random(5)
    colors = [0, 0, 1, 2]
    edges = sorted(K4)
    wins = 0
    for _ in range(3000):
        perm = [0, 1, 2]
        rng.shuffle(perm)
        cols = [perm[c] for c in colors]
        rs = [rng.getrandbits(256).to_bytes(32, "big") for _ in cols]
        coms = [commit(c, r) for c, r in zip(cols, rs)]
        e = rng.choice(edges)
        opening = ((cols[e[0]], rs[e[0]]), (cols[e[1]], rs[e[1]]))
        wins += coloring_verify(K4, coms, e, opening)
    assert abs(wins / 3000 - 5 / 6) < 0.03


def test_binding_stops_a_changed_opening():
    rng = random.Random(6)
    prover = ColoringProver(C4_CHORD, C4_COLORS)
    coms = prover.first(rng)
    (cu, ru), (cv, rv) = prover.answer((0, 1))
    assert coloring_verify(C4_CHORD, coms, (0, 1), ((cu, ru), (cv, rv)))
    other = 3 - cu - cv       # the third color
    assert not coloring_verify(C4_CHORD, coms, (0, 1), ((other, ru), (cv, rv)))
    # A non-edge is never a valid challenge.
    assert not coloring_verify(C4_CHORD, coms, (1, 3), prover.answer((1, 3)))


def test_coloring_simulator_opened_view_is_exact():
    # The opened view is (edge, color of u, color of v). Real: edge uniform
    # and color permutation uniform. Simulated: edge uniform and an ordered
    # pair of distinct colors uniform. Both are uniform over 5 x 6 values.
    prover = ColoringProver(C4_CHORD, C4_COLORS)
    edges = sorted(C4_CHORD)
    real = Counter()
    for perm in permutations(range(3)):
        prover.first(random.Random(0), perm=list(perm))
        for e in edges:
            (cu, _), (cv, _) = prover.answer(e)
            real[(e, cu, cv)] += 1
    sim = Counter()
    for e in edges:
        for pair in permutations(range(3), 2):
            coms, e2, ((cu, ru), (cv, rv)) = coloring_simulate(C4_CHORD, 4, random.Random(0), e=e, pair=pair)
            assert coloring_verify(C4_CHORD, coms, e2, ((cu, ru), (cv, rv)))
            sim[(e2, cu, cv)] += 1
    assert real == sim
    assert len(real) == 30 and set(real.values()) == {1}


def test_coloring_simulator_transcripts_verify():
    rng = random.Random(7)
    for _ in range(200):
        coms, e, opening = coloring_simulate(C4_CHORD, 4, rng)
        assert coloring_verify(C4_CHORD, coms, e, opening)
    # The simulator also produces accepting views for K4, which has no
    # 3-coloring: the view alone proves nothing, as zero knowledge requires.
    for _ in range(50):
        coms, e, opening = coloring_simulate(K4, 4, rng)
        assert coloring_verify(K4, coms, e, opening)
