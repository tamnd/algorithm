# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lfsr-reseeding/. The authors are listed in prov/NQ6987.jsonl.

import random

import pytest

from lfsr_reseeding import expand, output_forms, rank_of_cube, reseed

# Primitive feedback polynomials as tap sets: x^n + sum c_i x^i gives tap n - i for every c_i = 1.
PRIMITIVE = {3: [2, 3], 4: [3, 4], 5: [3, 5], 6: [5, 6], 7: [6, 7], 8: [4, 5, 6, 8], 10: [7, 10]}


def matches(stream: str, cube: str) -> bool:
    return all(c == "X" or c == s for c, s in zip(cube, stream))


def all_seeds(n, taps, cube):
    return [s for s in range(1 << n) if matches(expand(n, taps, s, len(cube)), cube)]


def test_page_example():
    # n = 4, x^4 + x + 1 (taps 3 and 4), a cube of length 10 with 4 care bits.
    cube = "XX1X0XX1X0"
    assert reseed(4, [3, 4], cube) == 0b1111
    assert expand(4, [3, 4], 0b1111, 10) == "1111000100"
    assert all_seeds(4, [3, 4], cube) == [0b1111]
    # One more care bit that disagrees with the only solution makes the system inconsistent.
    assert reseed(4, [3, 4], "0X1X0XX1X0") is None


def test_inconsistent_example():
    # x^3 + x + 1: a_(t+3) = a_(t+1) + a_t, so care bits 1, 0, 0 at t, t + 1, t + 3 conflict.
    for t in range(5):
        cube = ["X"] * 10
        cube[t], cube[t + 1], cube[t + 3] = "1", "0", "0"
        assert reseed(3, [2, 3], "".join(cube)) is None
        assert all_seeds(3, [2, 3], "".join(cube)) == []


def test_forms_match_expansion():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(1, 12)
        taps = rng.sample(range(1, n + 1), rng.randint(1, n))
        seed = rng.randrange(1 << n)
        length = rng.randint(0, 40)
        out = expand(n, taps, seed, length)
        forms = output_forms(n, taps, length)
        for t in range(length):
            assert int(out[t]) == bin(forms[t] & seed).count("1") % 2


def test_edge_cases():
    assert reseed(3, [2, 3], "") == 0
    assert reseed(3, [2, 3], "XXXXXXX") == 0
    assert reseed(1, [1], "1111") == 1
    assert reseed(1, [1], "10") is None
    with pytest.raises(ValueError):
        reseed(3, [4], "1")
    with pytest.raises(ValueError):
        reseed(3, [2, 3], "1Z")


def test_any_n_consecutive_bits_are_encodable():
    # With tap n present the state map is invertible, so any n consecutive care bits have a seed.
    rng = random.Random(8)
    for n, taps in PRIMITIVE.items():
        for _ in range(60):
            start = rng.randint(0, 30)
            bits = "".join(rng.choice("01") for _ in range(n))
            cube = "X" * start + bits + "X" * rng.randint(0, 5)
            seed = reseed(n, taps, cube)
            assert seed is not None and matches(expand(n, taps, seed, len(cube)), cube)


@pytest.mark.parametrize("n", [3, 4, 5, 6, 8])
def test_against_exhaustive_seed_search(n):
    rng = random.Random(1000 + n)
    for _ in range(150):
        taps = PRIMITIVE[n] if rng.random() < 0.5 else rng.sample(range(1, n + 1), rng.randint(1, n))
        length = rng.randint(1, 3 * n)
        p_care = rng.choice([0.1, 0.3, 0.6])
        cube = "".join(rng.choice("01") if rng.random() < p_care else "X" for _ in range(length))
        seeds = all_seeds(n, taps, cube)
        got = reseed(n, taps, cube)
        if not seeds:
            assert got is None
        else:
            assert got in seeds
            # The solutions form a coset of the null space: 2^(n - rank) seeds.
            assert len(seeds) == 2 ** (n - rank_of_cube(n, taps, cube))


def test_long_chain_against_exhaustive_n10():
    rng = random.Random(77)
    n, taps = 10, PRIMITIVE[10]
    for _ in range(30):
        length = 60
        cube = "".join(rng.choice("01") if rng.random() < 0.15 else "X" for _ in range(length))
        seeds = all_seeds(n, taps, cube)
        got = reseed(n, taps, cube)
        assert (got is None) == (not seeds)
        if got is not None:
            assert got in seeds


def test_cubes_from_real_streams_always_encode():
    # A cube cut from a real LFSR stream is consistent by construction.
    rng = random.Random(9)
    for _ in range(300):
        n = rng.choice(list(PRIMITIVE))
        taps = PRIMITIVE[n]
        s0 = rng.randrange(1 << n)
        length = rng.randint(1, 80)
        stream = expand(n, taps, s0, length)
        cube = "".join(c if rng.random() < 0.4 else "X" for c in stream)
        seed = reseed(n, taps, cube)
        assert seed is not None and matches(expand(n, taps, seed, length), cube)
