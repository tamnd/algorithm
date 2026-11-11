# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-puzzles/. The authors are listed in prov/GMZJAJ.jsonl.

import random

from merkle_puzzles import MAGIC, Puzzle, Work, run_protocol, solve_puzzle, toy_encrypt


def test_toy_cipher_round_trip() -> None:
    rng = random.Random(1)
    nonce, msg = rng.randbytes(16), rng.randbytes(70)
    assert toy_encrypt(5, nonce, toy_encrypt(5, nonce, msg)) == msg
    assert toy_encrypt(6, nonce, toy_encrypt(5, nonce, msg)) != msg


def test_solve_counts_trials() -> None:
    rng = random.Random(2)
    nonce = rng.randbytes(16)
    body = toy_encrypt(37, nonce, MAGIC + bytes(16) + b"k" * 16)
    w = Work()
    ident, key = solve_puzzle(Puzzle(nonce, body), 100, w)
    assert ident == bytes(16) and key == b"k" * 16
    assert w.calls == 38  # keys 0 to 37


def test_alice_and_bob_agree_and_eve_also_wins_with_more_work() -> None:
    n = space = 64
    for seed in range(5):
        keys, works = run_protocol(n, space, seed)
        assert keys[0] == keys[1] == keys[2]
        wa, wb, we = works
        assert wa.calls == n
        assert 1 <= wb.calls <= space
        assert we.calls <= n * space


def test_work_counts_follow_the_quadratic_gap() -> None:
    # Average over runs: Bob about S / 2, Eve about N S / 4.
    n = space = 64
    runs = 12
    bob = eve = 0
    for seed in range(100, 100 + runs):
        _, works = run_protocol(n, space, seed)
        bob += works[1].calls
        eve += works[2].calls
    bob_mean, eve_mean = bob / runs, eve / runs
    assert 10 <= bob_mean <= 54  # expected (S + 1) / 2 = 32.5
    assert 400 <= eve_mean <= 1800  # expected about N S / 4 = 1024
    assert eve_mean > 10 * bob_mean
