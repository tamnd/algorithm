# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oblivious-transfer-extension/. The authors are listed in prov/6D0YW3.jsonl.
# There are no official test vectors for IKNP. The tests run 10000 transfers
# with kappa = 128 base OTs from a local ideal OT and check each output
# directly against the sender's pairs, check the row correlation
# q_j = t_j xor r_j s, count the messages, and run the cheating receiver
# attack against local simulated parties.

import hashlib
import random

from oblivious_transfer_extension import (
    KAPPA,
    cheating_receiver_attack,
    hash_row,
    iknp,
    prg,
    transpose,
)

M = 10_000
NBYTES = 16


def random_pairs(m: int, rng: random.Random) -> list[tuple[bytes, bytes]]:
    return [(rng.randbytes(NBYTES), rng.randbytes(NBYTES)) for _ in range(m)]


def test_ten_thousand_transfers() -> None:
    rng = random.Random(2003)
    pairs = random_pairs(M, rng)
    r = [rng.getrandbits(1) for _ in range(M)]
    run = iknp(pairs, r, rng)
    assert all(run.outputs[j] == pairs[j][r[j]] for j in range(M))
    # The receiver's pad for the other message is not its own pad.
    assert all(hash_row(j, run.t_rows[j] ^ run.s, NBYTES) != hash_row(j, run.t_rows[j], NBYTES)
               for j in range(100))
    # The correlation behind it: q_j = t_j xor r_j s.
    assert all(run.q_rows[j] == run.t_rows[j] ^ (run.s if r[j] else 0) for j in range(M))
    # kappa base OTs, kappa * m bits from the receiver, 2 m messages from the sender.
    c = run.counters
    assert c.base_ots == KAPPA
    assert c.receiver_bits == KAPPA * M
    assert c.sender_bytes == 2 * NBYTES * M
    assert c.hash_calls == 3 * M


def test_transpose() -> None:
    rng = random.Random(1)
    m, k = 37, 11
    cols = [rng.getrandbits(m) for _ in range(k)]
    rows = transpose(cols, m)
    assert all(((rows[j] >> i) & 1) == ((cols[i] >> j) & 1) for i in range(k) for j in range(m))


def test_prg_and_hash_are_sha256() -> None:
    seed = bytes(16)
    first = hashlib.sha256(seed + bytes(8)).digest()
    assert prg(seed, 256) == int.from_bytes(first, "little")
    assert prg(seed, 10) == int.from_bytes(first, "little") & 1023
    assert hash_row(5, 0, 16) == hashlib.sha256((5).to_bytes(8, "big") + bytes(16)).digest()[:16]


def test_small_kappa_still_correct() -> None:
    # Correctness does not depend on kappa (security does).
    rng = random.Random(7)
    pairs = random_pairs(50, rng)
    r = [rng.getrandbits(1) for _ in range(50)]
    run = iknp(pairs, r, rng, kappa=8)
    assert all(run.outputs[j] == pairs[j][r[j]] for j in range(50))
    assert run.counters.base_ots == 8


def test_cheating_receiver_learns_s_and_both_messages() -> None:
    # Motivation for KOS: a receiver that puts a different choice vector in
    # each column (non-constant rows) learns the sender's secret s from
    # kappa probe transfers, and then both messages of all other transfers.
    rng = random.Random(2015)
    m = KAPPA + 500
    pairs = random_pairs(m, rng)
    known = {j: pairs[j][0] for j in range(KAPPA)}
    s_guess, learned = cheating_receiver_attack(pairs, known, random.Random(99))
    # Recompute the sender's s from the same randomness to compare.
    honest = iknp(pairs, [0] * m, random.Random(99))
    assert s_guess == honest.s
    assert learned == list(pairs[KAPPA:])


def test_honest_rows_do_not_reveal_the_other_message() -> None:
    # With constant rows, the receiver's only pad for message 1 - r_j is
    # H(j, t_j xor s), and it does not know s: guessing s = 0 gives the
    # wrong pad.
    rng = random.Random(3)
    pairs = random_pairs(200, rng)
    r = [0] * 200
    run = iknp(pairs, r, rng)
    wrong = [bytes(a ^ b for a, b in zip(run.y[j][1], hash_row(j, run.t_rows[j], NBYTES)))
             for j in range(200)]
    assert all(wrong[j] != pairs[j][1] for j in range(200))
