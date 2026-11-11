# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ecdsa/. The authors are listed in prov/QNKB84.jsonl.

import random

from ecdsa import G, N, is_low_s, on_curve, point_mul, public_key, recover_public_key, sign, verify

# RFC 6979, Appendix A.2.5 (ECDSA, 256 bits, prime field), copied by hand.
X = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
UX = 0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6
UY = 0x7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299
VECTORS = [
    (  # With SHA-256, message = "sample"
        b"sample",
        0xA6E3C57DD01ABE90086538398355DD4C3B17AA873382B0F24D6129493D8AAD60,
        0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716,
        0xF7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8,
    ),
    (  # With SHA-256, message = "test"
        b"test",
        0xD16B6AE827F17175E040871A1C7EC3500192C4C92677336EC2537ACAEE0008E0,
        0xF1ABB023518351CD71D881567B1EA663ED3EFCF6C5132B354F28D3B0B7D38367,
        0x019F4113742A2B14BD25926B49C649155F267E60D3814B4C0CC84250E46F0083,
    ),
]


def test_rfc6979_a25_public_key() -> None:
    assert public_key(X) == (UX, UY)
    assert on_curve(G) and point_mul(G, N) is None


def test_rfc6979_a25_signatures() -> None:
    q = (UX, UY)
    for msg, k, r, s in VECTORS:
        r2, s2, _ = sign(X, msg, k=k)
        assert (r2, s2) == (r, s)
        assert verify(q, msg, r, s)
        assert not verify(q, msg + b"!", r, s)
        assert not verify(q, msg, r, (s + 1) % N)


def test_malleability_and_low_s() -> None:
    q = (UX, UY)
    msg, k, r, s = VECTORS[0]
    # (r, n - s) is a second valid signature on the same message.
    assert verify(q, msg, r, N - s)
    assert not is_low_s(s)  # the "sample" vector has a high s
    r2, s2, _ = sign(X, msg, k=k, low_s=True)
    assert r2 == r and s2 == N - s and is_low_s(s2)


def test_zero_signature_is_rejected() -> None:
    # CVE-2022-21449: a verifier that skips the range check accepts r = s = 0.
    q = (UX, UY)
    assert not verify(q, b"anything", 0, 0)
    assert not verify(q, b"anything", N, N)


def test_public_key_recovery() -> None:
    rng = random.Random(62)
    for i in range(4):
        d = rng.randrange(1, N)
        q = public_key(d)
        msg = b"recover %d" % i
        r, s, v = sign(d, msg, k=rng.randrange(1, N), low_s=(i % 2 == 0))
        assert verify(q, msg, r, s)
        assert recover_public_key(msg, r, s, v) == q
        # A wrong recovery id gives another key, which the signature does not match.
        other = recover_public_key(msg, r, s, v ^ 1)
        assert other != q


def test_random_round_trip() -> None:
    rng = random.Random(186)
    for i in range(3):
        d = rng.randrange(1, N)
        q = public_key(d)
        msg = b"round trip %d" % i
        r, s, _ = sign(d, msg, k=rng.randrange(1, N))
        assert verify(q, msg, r, s)
        assert not verify(public_key(d % (N - 1) + 1), msg, r, s)
