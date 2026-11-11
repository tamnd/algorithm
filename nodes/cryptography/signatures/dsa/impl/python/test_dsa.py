# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dsa/. The authors are listed in prov/J4WE85.jsonl.
"""Tests for DSA with the vectors of RFC 6979, Appendix A.2.2 (DSA, 2048 bits,
N = 256). RFC 6979 derives k deterministically; here the printed k is passed
to the FIPS 186-4 signing routine, so the vectors test DSA itself, not the
derivation of k."""

import random

import pytest

from dsa import Params, generate_g, generate_pq, keygen, message_representative, sign, validate_pq, verify


def hx(s: str) -> int:
    return int("".join(s.split()), 16)


# RFC 6979, Appendix A.2.2, "Key pair".
P = hx("""9DB6FB5951B66BB6FE1E140F1D2CE5502374161FD6538DF1648218642F0B5C48
C8F7A41AADFA187324B87674FA1822B00F1ECF8136943D7C55757264E5A1A44F
FE012E9936E00C1D3E9310B01C7D179805D3058B2A9F4BB6F9716BFE6117C6B5
B3CC4D9BE341104AD4A80AD6C94E005F4B993E14F091EB51743BF33050C38DE2
35567E1B34C3D6A5C0CEAA1A0F368213C3D19843D0B4B09DCB9FC72D39C8DE41
F1BF14D4BB4563CA28371621CAD3324B6A2D392145BEBFAC748805236F5CA2FE
92B871CD8F9C36D3292B5509CA8CAA77A2ADFC7BFD77DDA6F71125A7456FEA15
3E433256A2261C6A06ED3693797E7995FAD5AABBCFBE3EDA2741E375404AE25B""")
Q = hx("F2C3119374CE76C9356990B465374A17F23F9ED35089BD969F61C6DDE9998C1F")
G = hx("""5C7FF6B06F8F143FE8288433493E4769C4D988ACE5BE25A0E24809670716C613
D7B0CEE6932F8FAA7C44D2CB24523DA53FBE4F6EC3595892D1AA58C4328A06C4
6A15662E7EAA703A1DECF8BBB2D05DBE2EB956C142A338661D10461C0D135472
085057F3494309FFA73C611F78B32ADBB5740C361C9F35BE90997DB2014E2EF5
AA61782F52ABEB8BD6432C4DD097BC5423B285DAFB60DC364E8161F4A2A35ACA
3A10B1C4D203CC76A470A33AFDCBDD92959859ABD8B56E1725252D78EAC66E71
BA9AE3F1DD2487199874393CD4D832186800654760E1E34C09E4D155179F9EC0
DC4473F996BDCE6EED1CABED8B6F116F7AD9CF505DF0F998E34AB27514B0FFE7""")
X = hx("69C7548C21D0DFEA6B9A51C9EAD4E27C33D3B3F180316E5BCAB92C933F0E4DBC")
Y = hx("""667098C654426C78D7F8201EAC6C203EF030D43605032C2F1FA937E5237DBD94
9F34A0A2564FE126DC8B715C5141802CE0979C8246463C40E6B6BDAA2513FA61
1728716C2E4FD53BC95B89E69949D96512E873B9C8F8DFD499CC312882561ADE
CB31F658E934C0C197F2C4D96B05CBAD67381E7B768891E4DA3843D24D94CDFB
5126E9B8BF21E8358EE0E0A30EF13FD6A664C0DCE3731F7FB49A4845A4FD8254
687972A2D382599C9BAC4E0ED7998193078913032558134976410B89D2C171D1
23AC35FD977219597AA7D15C1A9A428E59194F75C721EBCBCFAE44696A499AFA
74E04299F132026601638CB87AB79190D4A0986315DA8EEC6561C938996BEADF""")
PARAMS = Params(P, Q, G)

# RFC 6979, Appendix A.2.2, "Signatures": (hash, message, k, r, s).
VECTORS = [
    ("sha256", b"sample",
     "8926A27C40484216F052F4427CFD5647338B7B3939BC6573AF4333569D597C52",
     "EACE8BDBBE353C432A795D9EC556C6D021F7A03F42C36E9BC87E4AC7932CC809",
     "7081E175455F9247B812B74583E9E94F9EA79BD640DC962533B0680793A38D53"),
    ("sha256", b"test",
     "1D6CE6DDA1C5D37307839CD03AB0A5CBB18E60D800937D67DFB4479AAC8DEAD7",
     "8190012A1969F9957D56FCCAAD223186F423398D58EF5B3CEFD5A4146A4476F0",
     "7452A53F7075D417B4B013B278D1BB8BBD21863F5E7B1CEE679CF2188E1AB19E"),
    ("sha1", b"sample",  # a hash shorter than N = 256
     "888FA6F7738A41BDC9846466ABDB8174C0338250AE50CE955CA16230F9CBD53E",
     "3A1B2DBD7489D6ED7E608FD036C83AF396E290DBD602408E8677DAABD6E7445A",
     "D26FCBA19FA3E3058FFC02CA1596CDBB6E0D20CB37B06054F7E36DED0CDBBCCF"),
    ("sha512", b"test",  # a hash longer than N, truncated to its leftmost 256 binary digits
     "AFF1651E4CD6036D57AA8B2A05CCF1A9D5A40166340ECBBDC55BE10B568AA0AA",
     "89EC4BB1400ECCFF8E7D9AA515CD1DE7803F2DAFF09693EE7FD1353E90A68307",
     "C9F0BDABCC0D880BB137A994CC7F3980CE91CC10FAF529FC46565B15CEA854E1"),
]


def test_key_pair_consistency() -> None:
    assert P.bit_length() == 2048 and Q.bit_length() == 256
    assert (P - 1) % Q == 0
    assert pow(G, Q, P) == 1 and G != 1
    assert pow(G, X, P) == Y


@pytest.mark.parametrize("hash_name,msg,k,r,s", VECTORS)
def test_rfc6979_a22_vectors(hash_name: str, msg: bytes, k: str, r: str, s: str) -> None:
    sig = sign(PARAMS, X, msg, hash_name, k=hx(k))
    assert sig == (hx(r), hx(s))
    assert verify(PARAMS, Y, msg, sig, hash_name)


def test_rejections() -> None:
    r, s = hx(VECTORS[0][3]), hx(VECTORS[0][4])
    assert not verify(PARAMS, Y, b"samplf", (r, s))
    assert not verify(PARAMS, Y, b"sample", (r, s), "sha384")
    assert not verify(PARAMS, Y, b"sample", (r ^ 1, s))
    assert not verify(PARAMS, Y, b"sample", (r, s ^ 1))
    assert not verify(PARAMS, Y, b"sample", (0, s))
    assert not verify(PARAMS, Y, b"sample", (r, 0))
    assert not verify(PARAMS, Y, b"sample", (r + Q, s))
    assert not verify(PARAMS, Y, b"sample", (r, s + Q))
    assert not verify(PARAMS, Y * G % P, b"sample", (r, s))


def test_randomized_round_trips() -> None:
    rng = random.Random(7)
    x, y = keygen(PARAMS, rng)
    a, b = sign(PARAMS, x, b"m"), sign(PARAMS, x, b"m")
    assert a != b and verify(PARAMS, y, b"m", a) and verify(PARAMS, y, b"m", b)


def test_truncation_rule() -> None:
    import hashlib
    d = hashlib.sha512(b"test").digest()
    assert message_representative(b"test", Q, "sha512") == int.from_bytes(d[:32], "big")
    d1 = hashlib.sha1(b"sample").digest()
    assert message_representative(b"sample", Q, "sha1") == int.from_bytes(d1, "big")


def test_domain_parameter_generation_1024_160() -> None:
    rng = random.Random(17)  # this seed reaches a prime p at counter 13, which keeps the test fast
    p, q, seed, counter = generate_pq(1024, 160, seedlen=160, hash_name="sha256", rng=rng, rounds=20)
    assert p.bit_length() == 1024 and q.bit_length() == 160 and (p - 1) % q == 0
    assert validate_pq(p, q, seed, counter, 160, "sha256", rounds=20)
    assert not validate_pq(p, q, seed + 1, counter, 160, "sha256", rounds=20)
    assert not validate_pq(p, q, seed, counter + 1, 160, "sha256", rounds=20)
    g = generate_g(p, q)
    assert g > 1 and pow(g, q, p) == 1
    params = Params(p, q, g)
    x, y = keygen(params, rng)
    sig = sign(params, x, b"hello", "sha256")
    assert verify(params, y, b"hello", sig, "sha256")


def test_unapproved_pair_rejected() -> None:
    with pytest.raises(ValueError):
        generate_pq(1024, 256)
