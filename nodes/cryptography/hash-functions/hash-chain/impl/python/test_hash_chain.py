# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-chain/. The authors are listed in prov/WAQZTJ.jsonl.

import hashlib

import pytest

from hash_chain import HashChain, Verifier, fold, md4, otp, otp_hash, sha256

# RFC 1320, Appendix A.5 (Test suite).
MD4_VECTORS = [
    (b"", "31d6cfe0d16ae931b73c59d7e0c089c0"),
    (b"a", "bde52cb31de33e46245e05fbdbd6fb24"),
    (b"abc", "a448017aaf21d8525fc10ae87aa6729d"),
    (b"message digest", "d9130a8164549fe818874806e1c7014b"),
    (b"abcdefghijklmnopqrstuvwxyz", "d79e1c308aa5bbcdeea8ed63df412da9"),
    (b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "043f8582f241db351ce627e153e7f0e4"),
    (b"1234567890" * 8, "e33b4ddc9c38f2199c3e7b164fcc0536"),
]

# RFC 2289, Appendix C (MD4, MD5 and SHA1 ENCODINGS): pass phrase, seed, count, hex.
P1, P2, P3 = "This is a test.", "AbCdEfGhIjK", "OTP's are good"
OTP_VECTORS = {
    "md4": [
        (P1, "TeSt", 0, "D185 4218 EBBB 0B51"),
        (P1, "TeSt", 1, "6347 3EF0 1CD0 B444"),
        (P1, "TeSt", 99, "C5E6 1277 6E6C 237A"),
        (P2, "alpha1", 0, "5007 6F47 EB1A DE4E"),
        (P2, "alpha1", 1, "65D2 0D19 49B5 F7AB"),
        (P2, "alpha1", 99, "D150 C82C CE6F 62D1"),
        (P3, "correct", 0, "849C 79D4 F6F5 5388"),
        (P3, "correct", 1, "8C09 92FB 2508 47B1"),
        (P3, "correct", 99, "3F3B F4B4 145F D74B"),
    ],
    "md5": [
        (P1, "TeSt", 0, "9E87 6134 D904 99DD"),
        (P1, "TeSt", 1, "7965 E054 36F5 029F"),
        (P1, "TeSt", 99, "50FE 1962 C496 5880"),
        (P2, "alpha1", 0, "8706 6DD9 644B F206"),
        (P2, "alpha1", 1, "7CD3 4C10 40AD D14B"),
        (P2, "alpha1", 99, "5AA3 7A81 F212 146C"),
        (P3, "correct", 0, "F205 7539 43DE 4CF9"),
        (P3, "correct", 1, "DDCD AC95 6F23 4937"),
        (P3, "correct", 99, "B203 E28F A525 BE47"),
    ],
    "sha1": [
        (P1, "TeSt", 0, "BB9E 6AE1 979D 8FF4"),
        (P1, "TeSt", 1, "63D9 3663 9734 385B"),
        (P1, "TeSt", 99, "87FE C776 8B73 CCF9"),
        (P2, "alpha1", 0, "AD85 F658 EBE3 83C9"),
        (P2, "alpha1", 1, "D07C E229 B5CF 119B"),
        (P2, "alpha1", 99, "27BC 7103 5AAF 3DC6"),
        (P3, "correct", 0, "D51F 3E99 BF8E 6F0B"),
        (P3, "correct", 1, "82AE B52D 9437 74E4"),
        (P3, "correct", 99, "4F29 6A74 FE15 67EC"),
    ],
}
CASES = [(alg, *v) for alg, vs in OTP_VECTORS.items() for v in vs]


@pytest.mark.parametrize("data,want", MD4_VECTORS)
def test_md4_rfc1320(data: bytes, want: str) -> None:
    assert md4(data).hex() == want


@pytest.mark.parametrize("alg,phrase,seed,count,want", CASES)
def test_rfc2289_appendix_c(alg: str, phrase: str, seed: str, count: int, want: str) -> None:
    assert otp(phrase, seed, count, alg) == bytes.fromhex(want.replace(" ", ""))


def test_rfc2289_parity_example_md5() -> None:
    # RFC 2289, Appendix C, "Parity Calculations".
    assert otp("A_Valid_Pass_Phrase", "AValidSeed", 99, "md5").hex() == "85c43ee03857765b"


def test_rfc2289_input_checks() -> None:
    # RFC 2289, Appendix C, "GENERAL CHECKS".
    for phrase, seed in [("Too_short", "iamvalid"), ("A_Valid_Pass_Phrase", "Length_Okay"),
                         ("A_Valid_Pass_Phrase", "LengthOfSeventeen"), ("A_Valid_Pass_Phrase", "A Seed")]:
        with pytest.raises(ValueError):
            otp(phrase, seed, 99, "md5")


def test_seed_is_case_insensitive() -> None:
    assert otp(P1, "TeSt", 5, "sha1") == otp(P1, "test", 5, "sha1") == otp(P1, "TEST", 5, "sha1")


def test_fold_against_hashlib_md5() -> None:
    # Second check: the MD5 step equals the fold of hashlib's MD5, recomputed by hand.
    x = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    d = hashlib.md5(x).digest()
    assert otp_hash("md5")(x) == bytes(a ^ b for a, b in zip(d[:8], d[8:]))
    assert fold(d, "md5") == otp_hash("md5")(x)


@pytest.mark.parametrize("alg", ["md4", "md5", "sha1"])
def test_server_accepts_count_minus_one(alg: str) -> None:
    # Section 7: the server hashes the received OTP once and compares with the stored one.
    stored = otp(P2, "alpha1", 99, alg)
    v = Verifier(stored, otp_hash(alg))
    assert v.verify(otp(P2, "alpha1", 98, alg))
    assert v.v == otp(P2, "alpha1", 98, alg)
    assert not v.verify(otp(P2, "alpha1", 98, alg))  # replay of the same value fails
    assert v.verify(otp(P2, "alpha1", 97, alg))


@pytest.mark.parametrize("t", [1, 3, 10, 64])
def test_chain_checkpoints_give_the_same_values(t: int) -> None:
    s = b"secret seed"
    full = [s]
    for _ in range(40):
        full.append(sha256(full[-1]))
    c = HashChain(s, 40, t)
    assert c.anchor == full[40]
    v = Verifier(c.anchor)
    for j in range(1, 41):
        y = c.next()
        assert y == full[40 - j]
        assert v.verify(y)
    with pytest.raises(ValueError):
        c.next()


def test_wrong_value_replay_and_skip() -> None:
    c = HashChain(b"k", 10)
    v = Verifier(c.anchor)
    y1 = c.next()
    assert not v.verify(b"\x00" * 32)  # a wrong value fails
    assert not v.verify(c.anchor)  # the anchor itself is not a password
    assert v.verify(y1)
    assert not v.verify(y1)  # replay fails
    c.next()  # this value is lost
    y3 = c.next()
    assert not v.verify(y3)  # plain verification needs one step
    assert v.verify_skip(y3, 4)  # TESLA style: hash forward a few steps


def test_checkpoint_cost() -> None:
    n, t = 100, 10
    c = HashChain(b"s", n, t)
    for _ in range(n):
        c.next()
    # Value x_i costs i mod t calls from its checkpoint: n (t - 1) / 2 calls in all.
    assert c.hash_calls == n * (t - 1) // 2
    assert len(c.checkpoints) == n // t + 1


def test_avalanche_of_one_step() -> None:
    a = sha256(b"chain value 0")
    b = sha256(b"chain value 1")
    diff = sum(bin(x ^ y).count("1") for x, y in zip(a, b))
    assert 90 <= diff <= 166  # about half of 256 bits
