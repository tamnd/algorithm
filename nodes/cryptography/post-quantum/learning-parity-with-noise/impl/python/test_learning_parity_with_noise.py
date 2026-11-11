# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-parity-with-noise/. The authors are listed in prov/QEHHHQ.jsonl.
"""Tests for LPN sampling, the Gaussian elimination attack, HB, HB+ and the
GRS attack. LPN has no official test vectors; these tests check properties
against brute force and against the success probability formula, all on toy
sizes with fixed seeds.
"""

import random

from learning_parity_with_noise import (
    HBPlusTag,
    HBTag,
    dot,
    gauss_attack,
    grs_attack,
    hb_authenticate,
    hb_plus_authenticate,
    impersonate_hb_plus,
    lpn_sample,
    rank_probability,
    solve,
    uniform_sample,
)


def test_page_example():
    """n = 4, s = 1011 (bits s0..s3 = 1, 0, 1, 1), noise free equations."""
    s = 0b1101  # bit 0 = 1, bit 1 = 0, bit 2 = 1, bit 3 = 1
    eqs = [(0b0011, None), (0b0110, None), (0b1100, None), (0b1000, None)]
    eqs = [(a, dot(a, s)) for a, _ in eqs]
    assert [b for _, b in eqs] == [1, 1, 0, 1]
    assert solve(eqs, 4) == s


def test_solve_against_brute_force():
    rng = random.Random(1)
    n = 6
    done = 0
    while done < 500:
        s = rng.getrandbits(n)
        eqs = [(rng.getrandbits(n), 0) for _ in range(n)]
        eqs = [(a, dot(a, s)) for a, _ in eqs]
        brute = [c for c in range(1 << n) if all(dot(a, c) == b for a, b in eqs)]
        got = solve(eqs, n)
        if len(brute) == 1:
            assert got == brute[0] == s
            done += 1
        else:
            assert got is None


def test_noise_rate():
    rng = random.Random(2)
    n, tau, s = 16, 0.125, 0xBEEF
    flips = sum(b != dot(a, s) for a, b in (lpn_sample(s, n, tau, rng) for _ in range(20000)))
    assert abs(flips / 20000 - tau) < 0.01


def test_gaussian_attack_rounds_match_the_formula():
    """A round succeeds with probability rank_probability(n) (1 - tau)^n."""
    rng = random.Random(3)
    n, tau, trials = 20, 0.1, 60
    total = 0
    for _ in range(trials):
        s = rng.getrandbits(n)
        found, rounds = gauss_attack(lambda: lpn_sample(s, n, tau, rng), n, tau)
        assert found == s
        total += rounds
    expected = 1 / (rank_probability(n) * (1 - tau) ** n)
    assert abs(rank_probability(n) - 0.2888) < 0.001
    assert abs(total / trials - expected) < 0.25 * expected


def test_gaussian_attack_finds_nothing_in_uniform_samples():
    rng = random.Random(4)
    found, _ = gauss_attack(lambda: uniform_sample(16, rng), 16, 0.1, max_iter=200)
    assert found is None


def test_hb_completeness_and_soundness():
    rng = random.Random(5)
    k, eta, rounds, threshold = 32, 0.125, 100, 25
    x = rng.getrandbits(k)
    tag = HBTag(x, k, eta, rng)
    accepted = sum(hb_authenticate(x, k, tag.answer, rounds, threshold, rng) for _ in range(100))
    assert accepted >= 99
    guesser = sum(hb_authenticate(x, k, lambda a: rng.getrandbits(1), rounds, threshold, rng) for _ in range(100))
    assert guesser == 0


def test_passive_attack_on_hb_is_lpn():
    """Eavesdropped HB transcripts are LPN samples with secret x."""
    rng = random.Random(6)
    k, eta = 24, 0.05
    x = rng.getrandbits(k)
    tag = HBTag(x, k, eta, rng)
    transcript = []
    for _ in range(200):
        hb_authenticate(x, k, tag.answer, 40, 10, rng, transcript)
    stream = iter(transcript)
    found, _ = gauss_attack(lambda: next(stream), k, eta)
    assert found == x


def test_hb_plus_and_the_grs_attack():
    rng = random.Random(7)
    k, eta, rounds, threshold = 32, 0.125, 100, 25
    x, y = rng.getrandbits(k), rng.getrandbits(k)
    tag = HBPlusTag(x, y, k, eta, rng)
    honest = sum(hb_plus_authenticate(x, y, k, tag.commit, tag.answer, rounds, threshold, rng) for _ in range(50))
    assert honest >= 49

    def session(delta):
        return hb_plus_authenticate(x, y, k, tag.commit, lambda a: tag.answer(a ^ delta), rounds, threshold, rng)

    recovered = grs_attack(session, k)
    assert recovered == x
    commit, answer = impersonate_hb_plus(recovered)
    assert all(hb_plus_authenticate(x, y, k, commit, answer, rounds, threshold, rng) for _ in range(20))
