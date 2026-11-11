# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ecdh/. The authors are listed in prov/79PZ04.jsonl.

import hashlib
import random

import pytest

from ecdh import (
    P256,
    P384,
    Curve,
    ValidationError,
    ecc_cdh,
    ecdh_shared,
    generate_key_pair,
    is_on_curve,
    scalar_mult,
    validate_public_key,
)


def X(s: str) -> int:
    return int(s.replace(" ", ""), 16)


# RFC 5903 Section 8.1, the 256-bit random ECP group (P-256), copied by hand.
P256_I = X("C88F01F5 10D9AC3F 70A292DA A2316DE5 44E9AAB8 AFE84049 C62A9C57 862D1433")
P256_GI = (
    X("DAD0B653 94221CF9 B051E1FE CA5787D0 98DFE637 FC90B9EF 945D0C37 72581180"),
    X("5271A046 1CDB8252 D61F1C45 6FA3E59A B1F45B33 ACCF5F58 389E0577 B8990BB3"),
)
P256_R = X("C6EF9C5D 78AE012A 011164AC B397CE20 88685D8F 06BF9BE0 B283AB46 476BEE53")
P256_GR = (
    X("D12DFB52 89C8D4F8 1208B702 70398C34 2296970A 0BCCB74C 736FC755 4494BF63"),
    X("56FBF3CA 366CC23E 8157854C 13C58D6A AC23F046 ADA30F83 53E74F33 039872AB"),
)
P256_GIR = (
    X("D6840F6B 42F6EDAF D13116E0 E1256520 2FEF8E9E CE7DCE03 812464D0 4B9442DE"),
    X("522BDE0A F0D8585B 8DEF9C18 3B5AE38F 50235206 A8674ECB 5D98EDB2 0EB153A2"),
)

# RFC 5903 Section 8.2, the 384-bit random ECP group (P-384), copied by hand.
P384_I = X(
    "099F3C70 34D4A2C6 99884D73 A375A67F 7624EF7C 6B3C0F16 0647B674 14DCE655"
    "E35B5380 41E649EE 3FAEF896 783AB194"
)
P384_GI = (
    X(
        "667842D7 D180AC2C DE6F74F3 7551F557 55C7645C 20EF73E3 1634FE72 B4C55EE6"
        "DE3AC808 ACB4BDB4 C88732AE E95F41AA"
    ),
    X(
        "9482ED1F C0EEB9CA FC498462 5CCFC23F 65032149 E0E144AD A0241815 35A0F38E"
        "EB9FCFF3 C2C947DA E69B4C63 4573A81C"
    ),
)
P384_R = X(
    "41CB0779 B4BDB85D 47846725 FBEC3C94 30FAB46C C8DC5060 855CC9BD A0AA2942"
    "E0308312 916B8ED2 960E4BD5 5A7448FC"
)
P384_GR = (
    X(
        "E558DBEF 53EECDE3 D3FCCFC1 AEA08A89 A987475D 12FD950D 83CFA417 32BC509D"
        "0D1AC43A 0336DEF9 6FDA41D0 774A3571"
    ),
    X(
        "DCFBEC7A ACF31964 72169E83 8430367F 66EEBE3C 6E70C416 DD5F0C68 759DD1FF"
        "F83FA401 42209DFF 5EAAD96D B9E6386C"
    ),
)
P384_GIR = (
    X(
        "11187331 C279962D 93D60424 3FD592CB 9D0A926F 422E4718 7521287E 7156C5C4"
        "D6031355 69B9E9D0 9CF5D4A2 70F59746"
    ),
    X(
        "A2A9F38E F5CAFBE2 347CF7EC 24BDD5E6 24BC93BF A82771F4 0D1B65D0 6256A852"
        "C983135D 4669F879 2F2C1D55 718AFBB4"
    ),
)

RFC5903 = [
    (P256, P256_I, P256_GI, P256_R, P256_GR, P256_GIR),
    (P384, P384_I, P384_GI, P384_R, P384_GR, P384_GIR),
]


@pytest.mark.parametrize("curve,i,gi,r,gr,gir", RFC5903, ids=["P-256", "P-384"])
def test_rfc5903_section_8(curve: Curve, i: int, gi: tuple, r: int, gr: tuple, gir: tuple) -> None:
    assert scalar_mult(curve, i, curve.g) == gi
    assert scalar_mult(curve, r, curve.g) == gr
    validate_public_key(curve, gi)
    validate_public_key(curve, gr)
    z = gir[0].to_bytes(curve.size, "big")
    assert ecdh_shared(curve, i, gr) == z
    assert ecdh_shared(curve, r, gi) == z
    assert scalar_mult(curve, i, gr) == gir


@pytest.mark.parametrize("curve", [P256, P384], ids=["P-256", "P-384"])
def test_base_point_has_order_n(curve: Curve) -> None:
    assert is_on_curve(curve, curve.g)
    assert scalar_mult(curve, curve.n, curve.g) is None
    assert scalar_mult(curve, curve.n - 1, curve.g) == (curve.gx, (-curve.gy) % curve.p)


def test_random_agreement_p256() -> None:
    rng = random.Random(56)
    for _ in range(3):
        da, qa = generate_key_pair(P256, rng)
        db, qb = generate_key_pair(P256, rng)
        assert ecdh_shared(P256, da, qb) == ecdh_shared(P256, db, qa)


def test_validation_rejects_bad_points() -> None:
    gx, gy = P256.g
    bad = [
        None,  # the point at infinity
        (gx, gy + P256.p),  # a coordinate out of range
        (gx, (gy + 1) % P256.p),  # not on the curve
        (0, 0),  # not on the curve
    ]
    for q in bad:
        with pytest.raises(ValidationError):
            validate_public_key(P256, q, full=True)
        with pytest.raises(ValidationError):
            validate_public_key(P256, q, full=False)
        with pytest.raises(ValidationError):
            ecdh_shared(P256, 12345, q)


# ---------------------------------------------------------------- invalid curve attack
# A toy curve y^2 = x^3 - 3x + 76 over GF(65519) of prime order 65447, found
# by search for this test. It is far too small for real use; the attack runs
# only against a local simulated victim.
TOY_P = 65519
TOY = Curve(name="toy", p=TOY_P, a=TOY_P - 3, b=76, gx=2, gy=40463, n=65447, h=1)


def _qr_table(p: int) -> list[int]:
    chi = [-1] * p
    chi[0] = 0
    for y in range(1, p):
        chi[y * y % p] = 1
    return chi


def _count_points(p: int, a: int, b: int, chi: list[int]) -> int:
    return p + 1 + sum(chi[(x * x * x + a * x + b) % p] for x in range(p))


def _small_prime_factors(m: int, bound: int) -> list[int]:
    out = []
    for q in range(2, bound):
        if m % q == 0 and all(q % s for s in range(2, q)):
            out.append(q)
    return out


def _random_point(p: int, a: int, b: int, chi: list[int], rng: random.Random) -> tuple[int, int]:
    while True:
        x = rng.randrange(p)
        rhs = (x * x * x + a * x + b) % p
        if chi[rhs] == 1:
            return (x, pow(rhs, (p + 1) // 4, p))  # p = 3 mod 4


class Victim:
    """A server with a static key d. It answers each key share with a tag of Z.

    The tag stands for any message that depends on the shared secret, such
    as a key confirmation MAC or a record encrypted under a key from Z.
    """

    def __init__(self, d: int, validate: bool) -> None:
        self.d = d
        self.validate = validate

    def respond(self, q: tuple[int, int]) -> bytes:
        if self.validate:
            validate_public_key(TOY, q, full=True)
        try:
            z = ecc_cdh(TOY, self.d, q)
        except ValidationError:
            return b"error"
        return hashlib.sha256(z).digest()


def _tag(c: Curve, t: int, q: tuple[int, int]) -> bytes:
    pt = scalar_mult(c, t, q)
    if pt is None:
        return b"error"
    return hashlib.sha256(pt[0].to_bytes(c.size, "big")).digest()


def _crt(residues: list[tuple[int, int]]) -> tuple[int, int]:
    x, m = 0, 1
    for r, q in residues:
        t = ((r - x) * pow(m, -1, q)) % q
        x, m = x + m * t, m * q
    return x % m, m


def invalid_curve_attack(victim: Victim, public: tuple[int, int], rng: random.Random) -> int:
    """Recover the victim key with points of small order on curves y^2 = x^3 + a x + b'."""
    p, a = TOY.p, TOY.a
    chi = _qr_table(p)
    residues: list[tuple[int, int]] = []  # (r, l) with d = +r or -r mod l
    used: set[int] = set()
    modulus = 1
    b2 = 0
    while modulus <= TOY.n:
        b2 += 1
        if b2 == TOY.b:
            continue
        order = _count_points(p, a, b2, chi)
        fake = Curve(name="fake", p=p, a=a, b=b2, gx=0, gy=0, n=order, h=1)
        for ell in _small_prime_factors(order, 60):
            if ell in used:
                continue
            q = scalar_mult(fake, order // ell, _random_point(p, a, b2, chi, rng))
            if q is None:
                continue
            # q has order ell and lies on the fake curve, not on TOY.
            assert not is_on_curve(TOY, q)
            answer = victim.respond(q)
            r = next(t for t in range(ell) if _tag(fake, t, q) == answer)
            residues.append((r, ell))
            used.add(ell)
            modulus *= ell
    # Each residue is known up to sign. Try all sign choices and test against Q.
    for signs in range(1 << len(residues)):
        choice = [((-r) % ell if signs >> j & 1 else r, ell) for j, (r, ell) in enumerate(residues)]
        d, _ = _crt(choice)
        d %= TOY.n
        if scalar_mult(TOY, d, TOY.g) == public:
            return d
    raise AssertionError("attack failed")


def test_toy_curve_parameters() -> None:
    chi = _qr_table(TOY.p)
    assert TOY.p % 4 == 3
    assert _count_points(TOY.p, TOY.a, TOY.b, chi) == TOY.n
    assert all(TOY.n % s for s in range(2, 256))  # n is prime: 256^2 > n
    assert is_on_curve(TOY, TOY.g)
    assert scalar_mult(TOY, TOY.n, TOY.g) is None


def test_invalid_curve_attack_recovers_the_key_without_validation() -> None:
    rng = random.Random(2000)
    d, public = generate_key_pair(TOY, rng)
    victim = Victim(d, validate=False)
    assert invalid_curve_attack(victim, public, rng) == d


def test_validation_stops_the_invalid_curve_attack() -> None:
    rng = random.Random(2015)
    d, public = generate_key_pair(TOY, rng)
    victim = Victim(d, validate=True)
    with pytest.raises(ValidationError):
        invalid_curve_attack(victim, public, rng)
