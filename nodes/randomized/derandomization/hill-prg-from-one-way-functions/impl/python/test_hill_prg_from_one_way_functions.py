# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hill-prg-from-one-way-functions/. The authors are listed in prov/4E8GV3.jsonl.

import random
from fractions import Fraction

from hill_prg_from_one_way_functions import (
    advantage_on_bmy,
    bmy,
    from_bits,
    inner,
    is_permutation,
    linear_attack_test,
    linear_permutation,
    one_step,
    rank_gf2,
    stretch_extension,
    to_bits,
)


def random_perm(rng, n):
    f = list(range(2**n))
    rng.shuffle(f)
    return f


def random_invertible_rows(rng, n):
    while True:
        rows = [rng.randrange(2**n) for _ in range(n)]
        if rank_gf2(rows) == n:
            return rows


def test_trace_on_page() -> None:
    f = [(5 * x + 3) % 16 for x in range(16)]
    assert is_permutation(f)
    out = bmy(f, 4, 6, 11, 6)
    assert len(out) == 4 + 4 + 6
    assert out[8:] == (1, 1, 1, 1, 0, 1)
    assert from_bits(out[:4]) == 12


def test_output_length_and_structure() -> None:
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randrange(1, 6)
        ell = rng.randrange(0, 12)
        f = random_perm(rng, n)
        x, r = rng.randrange(2**n), rng.randrange(2**n)
        out = bmy(f, n, x, r, ell)
        assert len(out) == 2 * n + ell
        assert out[n : 2 * n] == to_bits(r, n)
        y = x
        for i in range(ell):
            assert out[2 * n + i] == inner(y, r)
            y = f[y]
        assert from_bits(out[:n]) == y


def test_bmy_is_stretch_extension_of_one_step() -> None:
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randrange(1, 6)
        ell = rng.randrange(0, 10)
        f = random_perm(rng, n)

        def g(state, f=f, n=n):
            return one_step(f, n, from_bits(state[:n]), from_bits(state[n:]))

        x, r = rng.randrange(2**n), rng.randrange(2**n)
        assert stretch_extension(g, to_bits(x, n) + to_bits(r, n), ell) == bmy(f, n, x, r, ell)


def test_first_2n_bits_exactly_uniform() -> None:
    rng = random.Random(3)
    for n in range(1, 5):
        f = random_perm(rng, n)
        seen = [one_step(f, n, x, r)[: 2 * n] for x in range(2**n) for r in range(2**n)]
        assert len(set(seen)) == 4**n


def test_distinguisher_equals_predictor() -> None:
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randrange(1, 4)
        f = random_perm(rng, n)
        accept = {z for z in range(2 ** (2 * n + 1)) if rng.randrange(2)}

        def d(bits):
            return 1 if from_bits(bits) in accept else 0

        gen = Fraction(sum(d(one_step(f, n, x, r)) for x in range(2**n) for r in range(2**n)), 4**n)
        uni = Fraction(len(accept), 2 ** (2 * n + 1))
        right = 0
        for x in range(2**n):
            for r in range(2**n):
                head = to_bits(f[x], n) + to_bits(r, n)
                for c in (0, 1):
                    guess = c if d(head + (c,)) else 1 - c
                    right += guess == inner(x, r)
        assert Fraction(right, 2 * 4**n) == Fraction(1, 2) + gen - uni


def test_linear_f_is_broken() -> None:
    rng = random.Random(5)
    for _ in range(20):
        n = rng.randrange(1, 4)
        rows = random_invertible_rows(rng, n)
        f = linear_permutation(rows, n)
        assert is_permutation(f)
        ell = n + 1
        test = linear_attack_test(rows, n, ell)
        assert advantage_on_bmy(f, n, ell, test) == Fraction(1, 2)
