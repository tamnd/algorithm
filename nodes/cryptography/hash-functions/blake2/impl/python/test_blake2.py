# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blake2/. The authors are listed in prov/9BR4W0.jsonl.

import hashlib

import pytest

from blake2 import BLAKE2B, BLAKE2S, blake2, blake2b, blake2s


def words(s: str) -> list[int]:
    return [int(x, 16) for x in s.split()]


def h(s: str) -> bytes:
    return bytes.fromhex("".join(s.split()))


# RFC 7693, Appendix A: BLAKE2b-512("abc"), the work vector v before round 0 (i= 0),
# after round 0 (i= 1) and after the last round (i=12), the final state h and the digest.
A_V0 = """6A09E667F2BDC948 BB67AE8584CAA73B 3C6EF372FE94F82B A54FF53A5F1D36F1 510E527FADE682D1
9B05688C2B3E6C1F 1F83D9ABFB41BD6B 5BE0CD19137E2179 6A09E667F3BCC908 BB67AE8584CAA73B
3C6EF372FE94F82B A54FF53A5F1D36F1 510E527FADE682D2 9B05688C2B3E6C1F E07C265404BE4294
5BE0CD19137E2179"""
A_V1 = """86B7C1568029BB79 C12CBCC809FF59F3 C6A5214CC0EACA8E 0C87CD524C14CC5D 44EE6039BD86A9F7
A447C850AA694A7E DE080F1BB1C0F84B 595CB8A9A1ACA66C BEC3AE837EAC4887 6267FC79DF9D6AD1
FA87B01273FA6DBE 521A715C63E08D8A E02D0975B8D37A83 1C7B754F08B7D193 8F885A76B6E578FE
2318A24E2140FC64"""
A_V12 = """12EF8A641EC4F6D6 BCED5DE977C9FAF5 733CA476C5148639 97DF596B0610F6FC F42C16519AD5AFA7
AA5AC1888E10467E 217D930AA51787F3 906A6FF19E573942 75AB709BD3DCBF24 EE7CE1F345947AA4
F8960D6C2FAF5F5E E332538A36B6D246 885BEF040EF6AA0B A4939A417BFB78A3 646CBB7AF6DCE980
E813A23C60AF3B82"""
A_H = """0D4D1C983FA580BA E9F6129FB697276A B7C45A68142F214C D1A2FFDB6FBB124B 2D79AB2A39C5877D
95CC3345DED552C2 5A92F1DBA88AD318 239900D4ED8623B9"""
A_OUT = """BA 80 A5 3F 98 1C 4D 0D 6A 27 97 B6 9F 12 F6 E9 4C 21 2F 14 68 5A C4 B7 4B 12 BB 6F DB FF A2 D1
7D 87 C5 39 2A AB 79 2D C2 52 D5 DE 45 33 CC 95 18 D3 8A A8 DB F1 92 5A B9 23 86 ED D4 00 99 23"""

# RFC 7693, Appendix B: BLAKE2s-256("abc"), v at (i=0), (i=1) and (i=10), h and the digest.
B_V0 = """6B08E647 BB67AE85 3C6EF372 A54FF53A 510E527F 9B05688C 1F83D9AB 5BE0CD19 6A09E667 BB67AE85
3C6EF372 A54FF53A 510E527C 9B05688C E07C2654 5BE0CD19"""
B_V1 = """16A3242E D7B5E238 CE8CE24B 927AEDE1 A7B430D9 93A4A14E A44E7C31 41D4759B 95BF33D3 9A99C181
608A3A6B B666383E 7A8DD50F BE378ED7 353D1EE6 3BB44C6B"""
B_V10 = """D9C994AA CFEC3AA6 700D0AB2 2C38670E AF6A1F66 1D023EF3 1D9EC27D 945357A5 3E9FFEBD 969FE811
EF485E21 A632797A DEEF082E AF3D80E1 4E86829B 4DEAFD3A"""
B_H = "8C5E8C50 E2147C32 A32BA7E1 2F45EB4E 208B4537 293AD69E 4C9B994D 82596786"
B_OUT = "50 8C 5E 8C 32 7C 14 E2 E1 A7 2B A3 4E EB 45 2F 37 45 8B 20 9E D6 3A 29 4D 99 9B 4C 86 67 59 82"

# RFC 7693, Appendix E: the "grand hash" constants blake2b_res and blake2s_res.
E_RES_B = "C2 3A 78 00 D9 81 23 BD 10 F5 06 C6 1E 29 DA 56 03 D7 63 B8 BB AD 2E 73 7F 5E 76 5A 7B CC D4 75"
E_RES_S = "6A 41 1F 08 CE 25 AD CD FB 02 AB A6 41 45 1C EC 53 C5 98 B2 4F 4F C7 87 FB DC 88 79 7F 4C 1D FE"


def test_rfc7693_appendix_a_trace() -> None:
    trace: list = []
    out = blake2(BLAKE2B, b"abc", 64, trace=trace)
    assert len(trace) == 13
    assert trace[0] == words(A_V0)
    assert trace[1] == words(A_V1)
    assert trace[12] == words(A_V12)
    assert out == h(A_OUT)
    state = [int.from_bytes(out[8 * i:8 * i + 8], "little") for i in range(8)]
    assert state == words(A_H)


def test_rfc7693_appendix_b_trace() -> None:
    trace: list = []
    out = blake2(BLAKE2S, b"abc", 32, trace=trace)
    assert len(trace) == 11
    assert trace[0] == words(B_V0)
    assert trace[1] == words(B_V1)
    assert trace[10] == words(B_V10)
    assert out == h(B_OUT)
    state = [int.from_bytes(out[4 * i:4 * i + 4], "little") for i in range(8)]
    assert state == words(B_H)


def selftest_seq(n: int, seed: int) -> bytes:
    """The Fibonacci byte generator of RFC 7693, Appendix E."""
    a, b, out = (0xDEAD4BAD * seed) & 0xFFFFFFFF, 1, bytearray()
    for _ in range(n):
        t = (a + b) & 0xFFFFFFFF
        a, b = b, t
        out.append(t >> 24)
    return bytes(out)


@pytest.mark.parametrize("which", ["b", "s"])
def test_rfc7693_appendix_e_self_test(which: str) -> None:
    if which == "b":
        f, md_len, in_len, want = blake2b, (20, 32, 48, 64), (0, 3, 128, 129, 255, 1024), E_RES_B
    else:
        f, md_len, in_len, want = blake2s, (16, 20, 28, 32), (0, 3, 64, 65, 255, 1024), E_RES_S
    acc = b""
    for outlen in md_len:
        for inlen in in_len:
            data = selftest_seq(inlen, inlen)
            acc += f(data, outlen)  # unkeyed hash
            acc += f(data, outlen, selftest_seq(outlen, outlen))  # keyed hash
    assert f(acc, 32) == h(want)


@pytest.mark.parametrize("n", [0, 1, 63, 64, 65, 127, 128, 129, 300])
@pytest.mark.parametrize("kk", [0, 1, 32])
def test_against_hashlib(n: int, kk: int) -> None:
    data = bytes(i % 251 for i in range(n))
    key = bytes(range(100, 100 + kk))
    assert blake2b(data, 64, key) == hashlib.blake2b(data, key=key).digest()
    assert blake2b(data, 17, key) == hashlib.blake2b(data, digest_size=17, key=key).digest()
    assert blake2s(data, 32, key) == hashlib.blake2s(data, key=key).digest()
    assert blake2s(data, 9, key) == hashlib.blake2s(data, digest_size=9, key=key).digest()


def test_salt_and_personalization_against_hashlib() -> None:
    data = b"message"
    assert blake2b(data, 32, b"k", b"salt", b"me") == hashlib.blake2b(
        data, digest_size=32, key=b"k", salt=b"salt", person=b"me").digest()
    assert blake2s(data, 32, b"", b"12345678", b"app") == hashlib.blake2s(
        data, salt=b"12345678", person=b"app").digest()


def test_digest_length_is_not_a_prefix() -> None:
    # nn is in the parameter block, so a shorter digest is not a prefix of a longer one.
    assert blake2b(b"abc", 32) != blake2b(b"abc", 64)[:32]


def test_wrong_key_fails() -> None:
    key = bytes(range(32))
    tag = blake2b(b"pay 10 euros", 32, key)
    bad = bytes([key[0] ^ 1]) + key[1:]
    assert blake2b(b"pay 10 euros", 32, bad) != tag
    assert blake2b(b"pay 11 euros", 32, key) != tag
    assert blake2b(b"pay 10 euros", 32) != tag


def test_key_is_not_the_first_block() -> None:
    # The keyed hash of m differs from the unkeyed hash of the padded key followed by m,
    # because kk is in the parameter block.
    key = b"secret"
    assert blake2b(b"m", 64, key) != blake2b(key.ljust(128, b"\0") + b"m", 64)


def test_avalanche() -> None:
    base = blake2b(b"The quick brown fox", 64)
    total = 0
    for i in range(19 * 8):
        msg = bytearray(b"The quick brown fox")
        msg[i // 8] ^= 1 << (i % 8)
        total += sum(bin(x ^ y).count("1") for x, y in zip(base, blake2b(bytes(msg), 64)))
    mean = total / (19 * 8)
    assert 246 <= mean <= 266  # about 256 of 512 bits


def test_bad_lengths() -> None:
    with pytest.raises(ValueError):
        blake2b(b"", 65)
    with pytest.raises(ValueError):
        blake2s(b"", 0)
    with pytest.raises(ValueError):
        blake2s(b"", 32, bytes(33))
