# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a5-1/. The authors are listed in prov/6XMTK8.jsonl.

import random

from a5_1 import REGISTERS, _step, a5_1_frame_keystreams, a5_1_keystream_bits, a5_1_setup

# The test vector of the 1999 pedagogical implementation by Briceno, Goldberg and
# Wagner. It is not an official ETSI vector: the GSM algorithm specifications are
# not public.
KEY = bytes.fromhex("12234567 89abcdef")
FRAME = 0x134
A_TO_B = "534eaa582fe8151ab6e1855a728c00"
B_TO_A = "24fd35a35d5fb6526d32f906df1ac0"


def test_pedagogical_vector() -> None:
    a, b = a5_1_frame_keystreams(KEY, FRAME)
    assert a.hex() == A_TO_B and b.hex() == B_TO_A


def test_registers_have_full_period_on_a_small_sample() -> None:
    # Each feedback polynomial is primitive, so plain stepping from a nonzero
    # state does not return to it before 2^L - 1 steps. Check R1 (2^19 - 1 steps).
    length = REGISTERS[0][0]
    r = start = 1
    for i in range(1, (1 << length)):
        r = _step(r, 0)
        if r == start:
            assert i == (1 << length) - 1
            break
    else:
        assert False


def test_keystream_depends_on_key_and_frame() -> None:
    rng = random.Random(51)
    key = bytes(rng.randrange(256) for _ in range(8))
    z = a5_1_keystream_bits(key, 7, 64)
    assert z != a5_1_keystream_bits(key, 8, 64)
    other = bytes([key[0] ^ 1]) + key[1:]
    assert z != a5_1_keystream_bits(other, 7, 64)


def test_round_trip() -> None:
    rng = random.Random(1)
    key = bytes(rng.randrange(256) for _ in range(8))
    frame = rng.randrange(1 << 22)
    msg = [rng.randrange(2) for _ in range(114)]
    z = a5_1_keystream_bits(key, frame, 114)
    c = [m ^ k for m, k in zip(msg, z)]
    assert [x ^ k for x, k in zip(c, a5_1_keystream_bits(key, frame, 114))] == msg


def test_setup_registers_fit_their_lengths() -> None:
    regs = a5_1_setup(KEY, FRAME)
    assert all(0 <= regs[j] < (1 << REGISTERS[j][0]) for j in range(3))
