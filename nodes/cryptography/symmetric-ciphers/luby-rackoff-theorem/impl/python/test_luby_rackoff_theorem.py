# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luby-rackoff-theorem/. The authors are listed in prov/M3FGR1.jsonl.

import random

from luby_rackoff_theorem import FeistelOracle, RandomPermutationOracle

H = 8  # half length; the block has 2H = 16 bits
MASK = (1 << H) - 1


def split(x: int) -> tuple[int, int]:
    return x >> H, x & MASK


def two_round_distinguisher(oracle) -> bool:
    """Two queries with the same right half: for 2 rounds, L2 XOR L2' = L XOR L'."""
    l1, l2, r = 0x00, 0x5A, 0x33
    a, _ = split(oracle.enc((l1 << H) | r))
    b, _ = split(oracle.enc((l2 << H) | r))
    return a ^ b == l1 ^ l2


def three_round_inverse_distinguisher(oracle) -> bool:
    """Two encryption queries and one decryption query (Luby and Rackoff, the 3-round network is not a strong PRP)."""
    l1, l2, r = 0x00, 0xC3, 0x77
    s1, _ = split(oracle.enc((l1 << H) | r))
    s2, t2 = split(oracle.enc((l2 << H) | r))
    _, r3 = split(oracle.dec((s2 << H) | (t2 ^ l1 ^ l2)))
    return r3 == s2 ^ s1 ^ r


def three_round_birthday_distinguisher(oracle, q: int) -> bool:
    """Encryption queries only, with a fixed right half: a collision of the left output halves
    gives T XOR T' = L XOR L' for the 3-round network. About 2^(h/2) queries are needed."""
    r = 0x2B
    seen: dict[int, tuple[int, int]] = {}
    for left in range(q):
        s, t = split(oracle.enc((left << H) | r))
        if s in seen:
            l0, t0 = seen[s]
            if t ^ t0 == left ^ l0:
                return True
        seen[s] = (left, t)
    return False


def advantage(test, rounds: int, trials: int, seed: int) -> tuple[float, float]:
    rng = random.Random(seed)
    real = sum(test(FeistelOracle(rounds, H, rng)) for _ in range(trials)) / trials
    ideal = sum(test(RandomPermutationOracle(H, rng)) for _ in range(trials)) / trials
    return real, ideal


def test_feistel_round_trip() -> None:
    rng = random.Random(1)
    for rounds in (1, 2, 3, 4):
        f = FeistelOracle(rounds, H, rng)
        for x in range(0, 1 << (2 * H), 97):
            assert f.dec(f.enc(x)) == x


def test_two_rounds_are_not_a_prp() -> None:
    real, ideal = advantage(two_round_distinguisher, 2, 300, 2)
    assert real == 1.0
    assert ideal < 0.05


def test_three_rounds_are_not_a_strong_prp() -> None:
    real, ideal = advantage(three_round_inverse_distinguisher, 3, 300, 3)
    assert real == 1.0
    assert ideal < 0.05


def test_three_rounds_resist_the_two_round_attack() -> None:
    real, ideal = advantage(two_round_distinguisher, 3, 300, 4)
    assert abs(real - ideal) < 0.05


def test_four_rounds_resist_the_inverse_attack() -> None:
    real, ideal = advantage(three_round_inverse_distinguisher, 4, 300, 5)
    assert abs(real - ideal) < 0.05


def test_three_round_birthday_attack() -> None:
    # q = 64 queries with h = 8: about C(64, 2) / 2^8 = 7.9 collisions of S are expected.
    real, ideal = advantage(lambda o: three_round_birthday_distinguisher(o, 64), 3, 200, 6)
    assert real > 0.9
    assert ideal < 0.2
