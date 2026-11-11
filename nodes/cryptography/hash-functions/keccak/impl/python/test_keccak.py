# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/keccak/. The authors are listed in prov/MDJVBV.jsonl.

import hashlib

from keccak import RC, RHO, from_bytes, keccak256, keccak_f, sha3_256, to_bytes

# XKCP, tests/TestVectors/KeccakF-1600-IntermediateValues.txt, "Example with the all-zero
# input": the output lanes of Keccak-f[1600] on the zero state, copied by hand, row y = 0 first.
ZERO_OUT = [
    0xF1258F7940E1DDE7, 0x84D5CCF933C0478A, 0xD598261EA65AA9EE, 0xBD1547306F80494D, 0x8B284E056253D057,
    0xFF97A42D7F8E6FD4, 0x90FEE5A0A44647C4, 0x8C5BDA0CD6192E76, 0xAD30A6F71B19059C, 0x30935AB7D08FFC64,
    0xEB5AA93F2317D635, 0xA9A6E6260D712103, 0x81A57C16DBCF555F, 0x43B831CD0347C826, 0x01F22F1A11A5569F,
    0x05E5635A21D9AE61, 0x64BEFEF28CC970F2, 0x613670957BC46611, 0xB87C5A554FD00ECB, 0x8C3EE88A1CCF32C8,
    0x940C7922AE3A2614, 0x1841F924A2C509E4, 0x16F53526E70465C2, 0x75F644E97F30A13B, 0xEAF1FF7B5CECA249,
]

# NIST, Example Values, SHA3-256_Msg0.pdf: the state of SHA3-256("") in round 0, as 200 bytes.
ABSORBED = bytes([0x06]) + bytes(134) + bytes([0x80]) + bytes(64)
AFTER_THETA_0 = bytes.fromhex(
    "0700000000000000060000000000000000000000000000800000000000000000"
    "0c00000000000000010000000000000006000000000000000000000000000080"
    "00000000000000000c0000000000000001000000000000000600000000000000"
    "000000000000008000000000000000000c000000000000000100000000000000"
    "0600000000000080000000000000008000000000000000000c00000000000000"
    "0100000000000000060000000000000000000000000000800000000000000000"
    "0c00000000000000"
)
AFTER_IOTA_0 = bytes.fromhex(
    "0600000000040000000000000060000000000300000400000700000000000000"
    "000003000060000008000000000000000000c00000d000000800000000000010"
    "0000000000d000000000c000000000100c00000000000000200c000000000000"
    "00000400000000000c0c00000000000020000400000000000018006000000000"
    "0040000010000000001800000000000000400060000000000000000010000000"
    "0000000000060020000000000000000018000000000600000000000000020020"
    "1800000000000000"
)


def test_zero_state_kat() -> None:
    assert keccak_f([0] * 25) == ZERO_OUT


def test_round_constants_and_offsets() -> None:
    # The same XKCP file lists RC[0], RC[1], RC[2] and RC[23], and the offsets r[x][y].
    assert RC[0] == 0x0000000000000001 and RC[1] == 0x0000000000008082
    assert RC[2] == 0x800000000000808A and RC[23] == 0x8000000080008008
    rows = [[0, 1, 62, 28, 27], [36, 44, 6, 55, 20], [3, 10, 43, 25, 39],
            [41, 45, 15, 21, 8], [18, 2, 61, 56, 14]]
    assert RHO == [v for row in rows for v in row]


def test_sha3_256_empty_round_0() -> None:
    trace: list = []
    out = keccak_f(from_bytes(ABSORBED), trace)
    assert to_bytes(trace[0][2]) == AFTER_THETA_0
    assert to_bytes(trace[1][2]) == AFTER_IOTA_0
    # SHA3-256_Msg0.pdf, the final state as lanes: [0, 0] and [4, 4].
    assert out[0] == 0x66D71EBFF8C6FFA7 and out[24] == 0x92136E0EFB7B70E5


def test_keccak256_ethereum() -> None:
    # go-ethereum, core/types/hashes.go: EmptyCodeHash = Keccak-256 of the empty string, and
    # EmptyRootHash = Keccak-256 of the RLP encoding 0x80 of the empty list.
    assert keccak256(b"").hex() == "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
    assert keccak256(b"\x80").hex() == "56e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b421"


def test_padding_differs_from_sha3() -> None:
    # NIST, Example Values, SHA3-256_Msg0.pdf.
    assert sha3_256(b"").hex() == "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"
    assert keccak256(b"") != sha3_256(b"")
    assert sha3_256(b"abc") == hashlib.sha3_256(b"abc").digest()


def test_permutation_is_invertible_on_samples() -> None:
    # Distinct inputs give distinct outputs (a small sanity check of bijectivity).
    outs = {tuple(keccak_f([i] + [0] * 24)) for i in range(20)}
    assert len(outs) == 20
