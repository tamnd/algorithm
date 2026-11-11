# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/merkle-puzzles/. The authors are listed in prov/GMZJAJ.jsonl.
"""Merkle's puzzles: key agreement over a public channel with a quadratic gap.

Alice makes N puzzles. Puzzle i hides an identifier id_i and a session key
k_i under a weak puzzle key r_i drawn from a space of size S, so one puzzle
takes up to S trial decryptions to open. Bob opens one puzzle at random and
sends back its identifier in the clear. An eavesdropper who wants k must
open about half of the puzzles, about N S / 4 trials on average.

The puzzle cipher is a toy: a keystream of SHA-256(r | nonce | counter)
XORed with the plaintext, where r is a small integer. Each call to the
cipher counts as one unit of work.

For study only. The code is not constant time, and the gap between the
honest parties and the eavesdropper is only quadratic, so the scheme is not
secure for any practical N. Use X25519 from libsodium or the Python package
cryptography instead.

Cost: Alice does N encryptions, Bob at most S trial decryptions, and an
eavesdropper about N S / 4 trial decryptions on average (N S at worst).
"""

import hashlib
import random
from dataclasses import dataclass

MAGIC = b"PUZZLE!!"  # 8 known bytes that tell a right guess from a wrong one
ID_LEN = 16
KEY_LEN = 16


def _keystream(r: int, nonce: bytes, length: int) -> bytes:
    out = b""
    counter = 0
    while len(out) < length:
        out += hashlib.sha256(r.to_bytes(8, "big") + nonce + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def toy_encrypt(r: int, nonce: bytes, plaintext: bytes) -> bytes:
    """XOR the plaintext with the keystream of the puzzle key r. Also decrypts."""
    ks = _keystream(r, nonce, len(plaintext))
    return bytes(a ^ b for a, b in zip(plaintext, ks))


@dataclass
class Puzzle:
    nonce: bytes
    body: bytes


@dataclass
class Work:
    """Counts of cipher calls, the unit of work in Merkle's analysis."""

    calls: int = 0


def alice_make_puzzles(n: int, space: int, rng: random.Random, work: Work) -> tuple[list[Puzzle], dict[bytes, bytes]]:
    """Make n puzzles with puzzle keys in [0, space). Return the puzzles and Alice's table id -> key."""
    puzzles: list[Puzzle] = []
    table: dict[bytes, bytes] = {}
    for _ in range(n):  # @line L1
        ident, key, r = rng.randbytes(ID_LEN), rng.randbytes(KEY_LEN), rng.randrange(space)  # @line L2
        nonce = rng.randbytes(16)
        puzzles.append(Puzzle(nonce, toy_encrypt(r, nonce, MAGIC + ident + key)))  # @line L3
        work.calls += 1
        table[ident] = key
    rng.shuffle(puzzles)  # @line L4
    return puzzles, table


def solve_puzzle(puzzle: Puzzle, space: int, work: Work) -> tuple[bytes, bytes]:
    """Try each puzzle key until the plaintext starts with MAGIC. Return (id, key)."""
    for r in range(space):  # @line L6
        work.calls += 1
        plain = toy_encrypt(r, puzzle.nonce, puzzle.body)
        if plain.startswith(MAGIC):  # @line L7
            return plain[len(MAGIC) : len(MAGIC) + ID_LEN], plain[len(MAGIC) + ID_LEN :]
    raise ValueError("no puzzle key opens this puzzle")


def bob_respond(puzzles: list[Puzzle], space: int, rng: random.Random, work: Work) -> tuple[bytes, bytes]:
    """Bob picks one puzzle at random and opens it. He sends the id and keeps the key."""
    j = rng.randrange(len(puzzles))  # @line L5
    return solve_puzzle(puzzles[j], space, work)


def alice_finish(table: dict[bytes, bytes], ident: bytes) -> bytes:
    """Alice looks up the key of the puzzle that Bob opened."""
    return table[ident]  # @line L8


def eavesdrop(puzzles: list[Puzzle], space: int, ident: bytes, rng: random.Random, work: Work) -> bytes:
    """Eve sees all puzzles and the id. She opens puzzles in random order until the id matches."""
    order = list(range(len(puzzles)))
    rng.shuffle(order)
    for j in order:
        found_id, key = solve_puzzle(puzzles[j], space, work)
        if found_id == ident:
            return key
    raise ValueError("the id is not in any puzzle")


def run_protocol(n: int, space: int, seed: int) -> tuple[list[bytes], list[Work]]:
    """One run with an eavesdropper: the keys of Alice, Bob and Eve, and the work of each."""
    rng = random.Random(seed)
    wa, wb, we = Work(), Work(), Work()
    puzzles, table = alice_make_puzzles(n, space, rng, wa)
    ident, k_bob = bob_respond(puzzles, space, rng, wb)
    k_alice = alice_finish(table, ident)
    k_eve = eavesdrop(puzzles, space, ident, rng, we)
    return [k_alice, k_bob, k_eve], [wa, wb, we]
