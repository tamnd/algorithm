# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proof-of-work/. The authors are listed in prov/GDRFMD.jsonl.

import random
from fractions import Fraction

from proof_of_work import retarget, simulate_chain, solve, success_probability, verify


def trials(bits: int, count: int, seed: int) -> list[int]:
    """Solve `count` puzzles with p = 2**-bits, each on fresh random data."""
    rng = random.Random(seed)
    target = 2 ** (256 - bits)
    out = []
    for _ in range(count):
        data = rng.getrandbits(128).to_bytes(16, "big")
        nonce, tries = solve(data, target)
        assert verify(data, nonce, target)
        out.append(tries)
    return out


def test_solution_verifies_and_is_first() -> None:
    target = 2 ** 248
    nonce, tries = solve(b"block 7", target)
    assert verify(b"block 7", nonce, target)
    assert all(not verify(b"block 7", k, target) for k in range(nonce))
    assert tries == nonce + 1


def test_mean_tries_is_one_over_p() -> None:
    bits, count = 6, 2000  # p = 1/64
    xs = trials(bits, count, seed=11)
    mean = sum(xs) / count
    # the standard deviation of the mean is sqrt(1 - p) / p / sqrt(count), about 1.4
    assert abs(mean - 64) < 6


def test_tries_are_geometric() -> None:
    bits, count = 5, 3000  # p = 1/32
    p = Fraction(1, 2 ** bits)
    xs = trials(bits, count, seed=12)
    # P(N > k) = (1 - p)^k, for several k
    for k in (8, 16, 32, 64, 128):
        expected = float((1 - p) ** k)
        observed = sum(x > k for x in xs) / count
        assert abs(observed - expected) < 0.035
    # memoryless: P(N > 64 | N > 32) = P(N > 32)
    over32 = [x for x in xs if x > 32]
    cond = sum(x > 64 for x in over32) / len(over32)
    assert abs(cond - float((1 - p) ** 32)) < 0.06


def test_probability() -> None:
    assert success_probability(2 ** 240) == Fraction(1, 2 ** 16)


def test_retarget_clamps() -> None:
    t = 2 ** 200
    assert retarget(t, 600, 600, 2 ** 224) == t
    assert retarget(t, 300, 600, 2 ** 224) == t // 2  # blocks came twice as fast: harder
    assert retarget(t, 10, 600, 2 ** 224) == t // 4  # clamped at a factor of 4
    assert retarget(t, 10 ** 6, 600, 2 ** 224) == 4 * t
    assert retarget(2 ** 223, 10 ** 6, 600, 2 ** 224) == 2 ** 224  # never easier than the maximum


def test_difficulty_follows_hash_rate() -> None:
    window, spacing = 50, 600.0
    p0 = 2 ** -20
    base = 1.0 / (spacing * p0)  # hash rate that gives one block per 600 s at the start
    rates = [base] * 500 + [8 * base] * 1000  # the hash rate grows eight times
    intervals, targets = simulate_chain(rates, 2 ** 236, window, spacing, seed=3)
    early = sum(intervals[:500]) / 500
    jump = sum(intervals[500:550]) / 50
    late = sum(intervals[1100:]) / 400
    assert 500 < early < 700
    assert jump < 150  # right after the jump blocks come about eight times faster
    assert 500 < late < 700  # after a few windows the spacing is back near 600 s
    assert targets[-1] < targets[0] / 4  # the target fell (the puzzle got harder)
