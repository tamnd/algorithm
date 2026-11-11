# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-cryptosystem/. The authors are listed in prov/D5K7RQ.jsonl.

import math
import random

from rsa_cryptosystem import (
    PrivateKey,
    PublicKey,
    crt_combine,
    cube_root_attack,
    decrypt,
    decrypt_single_exponent,
    encrypt,
    generate_key,
    hastad_broadcast_attack,
    i2osp,
    integer_root,
    is_probable_prime,
    os2ip,
    random_prime,
)

# Key 1 of the official PKCS #1 v2.1 test vector file oaep-vect.txt, from
# pkcs-1v2-1-vec.zip (RSA Laboratories), Example 1: a 1024-bit RSA key pair.
N_HEX = (
    "a8b3b284af8eb50b387034a860f146c4919f318763cd6c5598c8ae4811a1e0ab"
    "c4c7e0b082d693a5e7fced675cf4668512772c0cbc64a742c6c630f533c8cc72"
    "f62ae833c40bf25842e984bb78bdbf97c0107d55bdb662f5c4e0fab9845cb514"
    "8ef7392dd3aaff93ae1e6b667bb3d4247616d4f5ba10d4cfd226de88d39f16fb"
)
D_HEX = (
    "53339cfdb79fc8466a655c7316aca85c55fd8f6dd898fdaf119517ef4f52e8fd"
    "8e258df93fee180fa0e4ab29693cd83b152a553d4ac4d1812b8b9fa5af0e7f55"
    "fe7304df41570926f3311f15c4d65a732c483116ee3d3d2d0af3549ad9bf7cbf"
    "b78ad884f84d5beb04724dc7369b31def37d0cf539e9cfcdd3de653729ead5d1"
)
P_HEX = (
    "d32737e7267ffe1341b2d5c0d150a81b586fb3132bed2f8d5262864a9cb9f30a"
    "f38be448598d413a172efb802c21acf1c11c520c2f26a471dcad212eac7ca39d"
)
Q_HEX = (
    "cc8853d1d54da630fac004f471f281c7b8982d8224a490edbeb33d3e3d5cc93c"
    "4765703d1dd791642f1f116a0dd852be2419b2af72bfe9a030e860b0288b5d77"
)
DP_HEX = (
    "0e12bf1718e9cef5599ba1c3882fe8046a90874eefce8f2ccc20e4f2741fb0a3"
    "3a3848aec9c9305fbecbd2d76819967d4671acc6431e4037968db37878e695c1"
)
DQ_HEX = (
    "95297b0f95a2fa67d00707d609dfd4fc05c89dafc2ef6d6ea55bec771ea33373"
    "4d9251e79082ecda866efef13c459e1a631386b7e354c899f5f112ca85d71583"
)
QINV_HEX = (
    "4f456c502493bdc0ed2ab756a3a6ed4d67352a697d4216e93212b127a63d5411"
    "ce6fa98d5dbefd73263e3728142743818166ed7dd63687dd2a8ca1d2f4fbd8e1"
)
VECTOR_KEY = PrivateKey(
    n=int(N_HEX, 16),
    e=0x010001,
    d=int(D_HEX, 16),
    p=int(P_HEX, 16),
    q=int(Q_HEX, 16),
    dp=int(DP_HEX, 16),
    dq=int(DQ_HEX, 16),
    qinv=int(QINV_HEX, 16),
)


def test_vector_key_is_consistent() -> None:
    """The official key material meets the conditions of RFC 8017 Section 3."""
    k = VECTOR_KEY
    assert k.n.bit_length() == 1024
    assert k.p * k.q == k.n
    assert is_probable_prime(k.p) and is_probable_prime(k.q)
    lam = (k.p - 1) * (k.q - 1) // math.gcd(k.p - 1, k.q - 1)
    assert k.e * k.d % lam == 1
    assert k.e * k.dp % (k.p - 1) == 1
    assert k.e * k.dq % (k.q - 1) == 1
    assert k.q * k.qinv % k.p == 1


def test_vector_key_round_trip() -> None:
    k = VECTOR_KEY
    m = os2ip(b"the message representative of a short string")
    c = encrypt(k.public(), m)
    assert decrypt(k, c) == m
    assert decrypt_single_exponent(k, c) == m


def test_handbook_example_8_4() -> None:
    """Menezes, van Oorschot and Vanstone, Handbook of Applied Cryptography,
    Chapter 8, Example 8.4 (RSA with artificially small parameters)."""
    p, q, e = 2357, 2551, 3674911
    n = p * q
    assert n == 6012707
    phi = (p - 1) * (q - 1)
    assert phi == 6007800
    d = pow(e, -1, phi)
    assert d == 422191
    m = 5234673
    c = pow(m, e, n)
    assert c == 3650502
    assert pow(c, d, n) == m


def _toy_key(bits: int = 256, e: int = 65537, seed: int = 11) -> PrivateKey:
    rnd = random.Random(seed)
    return generate_key(bits, e, rnd.getrandbits, lambda n: rnd.randrange(n))


def test_generate_key_shape() -> None:
    k = _toy_key()
    assert k.n.bit_length() == 256
    assert k.p != k.q and k.p * k.q == k.n
    assert is_probable_prime(k.p) and is_probable_prime(k.q)
    lam = (k.p - 1) * (k.q - 1) // math.gcd(k.p - 1, k.q - 1)
    assert k.e * k.d % lam == 1
    assert k.d < k.n
    assert k.e * k.dp % (k.p - 1) == 1 and k.e * k.dq % (k.q - 1) == 1
    assert k.q * k.qinv % k.p == 1


def test_round_trip_random_messages() -> None:
    """CRT decryption inverts encryption for 500 random message representatives,
    and agrees with the single exponentiation c^d mod n."""
    k = _toy_key()
    rnd = random.Random(7)
    for _ in range(500):
        m = rnd.randrange(k.n)
        c = encrypt(k.public(), m)
        assert decrypt(k, c) == m
        assert decrypt_single_exponent(k, c) == m


def test_round_trip_for_messages_not_coprime_to_n() -> None:
    """Correctness holds for every m in [0, n), also when gcd(m, n) > 1."""
    k = _toy_key()
    for m in (0, 1, k.n - 1, k.p, k.q, 2 * k.p % k.n, 3 * k.q % k.n, k.p * 5 % k.n):
        c = encrypt(k.public(), m)
        assert decrypt(k, c) == m
        assert math.gcd(m, k.n) in (1, k.p, k.q, k.n)


def test_out_of_range_is_rejected() -> None:
    k = _toy_key()
    for bad in (-1, k.n, k.n + 1):
        try:
            encrypt(k.public(), bad)
        except ValueError:
            pass
        else:
            raise AssertionError("out of range message was accepted")
        try:
            decrypt(k, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("out of range ciphertext was accepted")


def test_textbook_rsa_is_deterministic_and_malleable() -> None:
    """Two properties that make textbook RSA unfit for real use."""
    k = _toy_key()
    pub = k.public()
    m1, m2 = 4242, 1111
    assert encrypt(pub, m1) == encrypt(pub, m1)
    assert encrypt(pub, m1) * encrypt(pub, m2) % pub.n == encrypt(pub, m1 * m2 % pub.n)
    r = 12345
    forged = encrypt(pub, m1) * pow(r, pub.e, pub.n) % pub.n
    assert decrypt(k, forged) == m1 * r % pub.n


def test_integer_root_and_octet_strings() -> None:
    assert integer_root(0, 3) == 0 and integer_root(1, 3) == 1
    assert integer_root(8, 3) == 2 and integer_root(7, 3) == 1
    assert integer_root(10**30, 3) == 10**10
    rnd = random.Random(3)
    for _ in range(200):
        x = rnd.randrange(1, 10**12)
        k = rnd.choice([2, 3, 5])
        r = integer_root(x, k)
        assert r**k <= x < (r + 1) ** k
    assert i2osp(1, 4) == b"\x00\x00\x00\x01"
    assert os2ip(i2osp(0x1234, 3)) == 0x1234


def test_small_message_cube_root_attack() -> None:
    """Toy attack against local keys: e = 3 with no padding and a short message."""
    k = _toy_key(bits=256, e=3, seed=5)
    m = os2ip(b"hello")
    c = encrypt(k.public(), m)
    assert m**3 < k.n
    assert cube_root_attack(k.public(), c) == m
    big = k.n - 1
    assert cube_root_attack(k.public(), encrypt(k.public(), big)) is None


def test_hastad_broadcast_attack() -> None:
    """Three keys with e = 3 and the same unpadded message (Hastad 1988)."""
    keys = [_toy_key(bits=256, e=3, seed=s) for s in (21, 22, 23)]
    m = os2ip(b"broadcast message to three keys")
    pubs = [k.public() for k in keys]
    assert all(m < pub.n for pub in pubs)
    cts = [encrypt(pub, m) for pub in pubs]
    assert all(cube_root_attack(pub, c) is None for pub, c in zip(pubs, cts))
    assert hastad_broadcast_attack(pubs, cts) == m


def test_crt_combine() -> None:
    assert crt_combine([2, 3, 2], [3, 5, 7]) == 23
    rnd = random.Random(4)
    for _ in range(200):
        mods = [3, 5, 7, 11, 13]
        x = rnd.randrange(3 * 5 * 7 * 11 * 13)
        assert crt_combine([x % m for m in mods], mods) == x


def test_random_prime_and_primality() -> None:
    rnd = random.Random(9)
    p = random_prime(64, rnd.getrandbits, lambda n: rnd.randrange(n))
    assert p.bit_length() == 64 and is_probable_prime(p)
    assert not is_probable_prime(p * 3)
    for n in (1, 4, 9, 15, 21, 25, 561, 1105, 1729):  # 561 and 1105 are Carmichael
        assert not is_probable_prime(n)
    for n in (2, 3, 5, 7, 97, 65537):
        assert is_probable_prime(n)


def test_public_exponent_must_be_coprime_to_lambda() -> None:
    try:
        PublicKey(15, 2)
    except ValueError:  # pragma: no cover - PublicKey takes any pair
        pass
    rnd = random.Random(2)
    k = generate_key(128, 3, rnd.getrandbits, lambda n: rnd.randrange(n))
    assert math.gcd(3, (k.p - 1) * (k.q - 1)) == 1
