# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skipjack/. The authors are listed in prov/F2V5M9.jsonl.

import random

from skipjack import F, decrypt_block, encrypt_block, encrypt_steps

KEY = bytes.fromhex("00998877665544332211")
PT = bytes.fromhex("33221100ddccbbaa")
CT = bytes.fromhex("2587cae27a12d300")

# "SKIPJACK and KEA Algorithm Specifications", Version 2.0 (29 May 1998),
# Annex III.A, "SKIPJACK - Codebook Mode", intermediate steps 0 to 32 as
# w1 w2 w3 w4 in hexadecimal.
TABLE = [
    "33221100ddccbbaa", "b0040baf1100ddcc", "e6883b460baf1100", "3c762d753b460baf",
    "4c4547ee2d753b46", "b949820a47ee2d75", "f0e3dd90820a47ee", "f9b9be50dd90820a",
    "d79b5599be50dd90", "dd901e0b820bbe50", "be504c52c391820b", "820b7f51f209c391",
    "c391f9c2fd56f209", "f20925ff3a5efd56", "fd5665dad7f83a5e", "3a5e69d99883d7f8",
    "d7f8899053979883", "9c00049289905397", "9fdccc5904928990", "3731beb2cc590492",
    "7afb7e7dbeb2cc59", "7759bb157e7dbeb2", "fb6445c0bb157e7d", "6f7f111545c0bb15",
    "65a7deaa111545c0", "45c0e0f9bb141115", "11153913a523bb14", "bb148ee6281da523",
    "a523bfe235ee281d", "281d0d841adc35ee", "35eee6f125871adc", "1adc60eed3002587",
    "2587cae27a12d300",
]


def test_annex_a_codebook() -> None:
    assert encrypt_block(KEY, PT) == CT
    assert decrypt_block(KEY, CT) == PT


def test_annex_a_intermediate_steps() -> None:
    states = encrypt_steps(KEY, PT)
    got = ["".join(f"{x:04x}" for x in s) for s in states]
    assert got == TABLE


def test_f_table() -> None:
    assert F[0x7A] == 0xD6  # the example in Section II.B.7
    assert sorted(F) == list(range(256))  # F is a permutation


def test_round_trip_random() -> None:
    rng = random.Random(12)
    for _ in range(20):
        key, m = rng.randbytes(10), rng.randbytes(8)
        assert decrypt_block(key, encrypt_block(key, m)) == m
