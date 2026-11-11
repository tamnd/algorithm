# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/x448/. The authors are listed in prov/J4FG25.jsonl.

import random

import pytest

from x448 import P, decode_scalar, decode_u_coordinate, public_key, x448, x448_shared


def H(s: str) -> bytes:
    return bytes.fromhex(s.replace(" ", ""))


# RFC 7748 Section 5.2, the two X448 test vectors, copied by hand
# (each value is split over two lines in the RFC).
VECTORS = [
    (
        "3d262fddf9ec8e88495266fea19a34d28882acef045104d0d1aae121 700a779c984c24f8cdd78fbff44943eba368f54b29259a4f1c600ad3",
        "06fce640fa3487bfda5f6cf2d5263f8aad88334cbd07437f020f08f9 814dc031ddbdc38c19c6da2583fa5429db94ada18aa7a7fb4ef8a086",
        "ce3e4ff95a60dc6697da1db1d85e6afbdf79b50a2412d7546d5f239f e14fbaadeb445fc66a01b0779d98223961111e21766282f73dd96b6f",
    ),
    (
        "203d494428b8399352665ddca42f9de8fef600908e0d461cb021f8c5 38345dd77c3e4806e25f46d3315c44e0a5b4371282dd2c8d5be3095f",
        "0fbcc2f993cd56d3305b0b7d9e55d4c1a8fb5dbb52f8e9a1e9b6201b 165d015894e56c4d3570bee52fe205e28a78b91cdfbde71ce8d157db",
        "884a02576239ff7a2f2f63b2db6a9ff37047ac13568e1e30fe63c4a7 ad1b3ee3a5700df34321d62077e63633c575c1c954514e99da7c179d",
    ),
]

# RFC 7748 Section 5.2, the inputs in base 10 (copied by hand).
SCALAR_1_DEC = int(
    "599189175373896402783756016145213256157230856"
    "085026129926891459468622403380588640249457727"
    "683869421921443004045221642549886377526240828"
)
U_1_DEC = int(
    "382239910814107330116229961234899377031416365"
    "240571325148346555922438025162094455820962429"
    "142971339584360034337310079791515452463053830"
)
SCALAR_2_DEC = int(
    "633254335906970592779259481534862372382525155"
    "252028961056404001332122152890562527156973881"
    "968934311400345568203929409663925541994577184"
)
U_2_DEC = int(
    "622761797758325444462922068431234180649590390"
    "024811299761625153767228042600197997696167956"
    "134770744996690267634159427999832340166786063"
)

# RFC 7748 Section 5.2, the iterated test (k = u = 5 at the start).
ITER_1 = "3f482c8a9f19b01e6c46ee9711d9dc14fd4bf67af30765c2ae2b846a 4d23a8cd0db897086239492caf350b51f833868b9bc2b3bca9cf4113"
ITER_1000 = "aa3b4749d55b9daf1e5b00288826c467274ce3ebbdd5c17b975e09d4 af6c67cf10d087202db88286e2b79fceea3ec353ef54faa26e219f38"
# The 1,000,000 iteration value is not run: it takes hours in pure Python.

# RFC 7748 Section 6.2, the Alice and Bob example.
ALICE_PRIV = "9a8f4925d1519f5775cf46b04b5800d4ee9ee8bae8bc5565d498c28d d9c9baf574a9419744897391006382a6f127ab1d9ac2d8c0a598726b"
ALICE_PUB = "9b08f7cc31b7e3e67d22d5aea121074a273bd2b83de09c63faa73d2c 22c5d9bbc836647241d953d40c5b12da88120d53177f80e532c41fa0"
BOB_PRIV = "1c306a7ac2a0e2e0990b294470cba339e6453772b075811d8fad0d1d 6927c120bb5ee8972b0d3e21374c9c921b09d1b0366f10b65173992d"
BOB_PUB = "3eb7a829b0cd20f5bcfc0b599b6feccf6da4627107bdb0d4f345b430 27d8b972fc3e34fb4232a13ca706dcb57aec3dae07bdc1c67bf33609"
SHARED = "07fff4181ac6cc95ec1c16a94a0f74d12da232ce40a77552281d282b b60c0b56fd2464c335543936521c24403085d59a449a5037514a879d"


@pytest.mark.parametrize("k,u,out", VECTORS)
def test_rfc7748_section_5_2_vectors(k: str, u: str, out: str) -> None:
    assert x448(H(k), H(u)) == H(out)


def test_rfc7748_decimal_forms() -> None:
    assert decode_scalar(H(VECTORS[0][0])) == SCALAR_1_DEC
    assert decode_u_coordinate(H(VECTORS[0][1])) == U_1_DEC
    assert decode_scalar(H(VECTORS[1][0])) == SCALAR_2_DEC
    assert decode_u_coordinate(H(VECTORS[1][1])) == U_2_DEC


def test_rfc7748_iterated_1_and_1000() -> None:
    k = u = (5).to_bytes(56, "little")
    for i in range(1, 1001):
        k, u = x448(k, u), k
        if i == 1:
            assert k == H(ITER_1)
    assert k == H(ITER_1000)


def test_rfc7748_section_6_2_alice_and_bob() -> None:
    a, b = H(ALICE_PRIV), H(BOB_PRIV)
    assert public_key(a) == H(ALICE_PUB)
    assert public_key(b) == H(BOB_PUB)
    assert x448_shared(a, H(BOB_PUB)) == H(SHARED)
    assert x448_shared(b, H(ALICE_PUB)) == H(SHARED)


def test_random_agreement() -> None:
    rng = random.Random(448)
    for _ in range(10):
        a, b = rng.randbytes(56), rng.randbytes(56)
        assert x448(a, public_key(b)) == x448(b, public_key(a))


def test_clamping() -> None:
    rng = random.Random(4480)
    for _ in range(200):
        k = decode_scalar(rng.randbytes(56))
        assert k % 4 == 0 and 2**447 <= k < 2**448


def test_parameters() -> None:
    assert P == 2**448 - 2**224 - 1
    # p is prime (Fermat test to a few bases is enough as a sanity check here).
    for base in (2, 3, 5, 7):
        assert pow(base, P - 1, P) == 1
    assert (156326 - 2) // 4 == 39081 and (156326 - 2) % 4 == 0


def test_small_order_points_give_all_zero() -> None:
    # u = 0 is the point (0, 0) of order 2; u = 1 has order 4 (on the curve or
    # its twist). A clamped scalar is a multiple of 4, so the output is zero.
    rng = random.Random(44)
    for u in (0, 1, P, P + 1):
        enc = u.to_bytes(56, "little")
        k = rng.randbytes(56)
        assert x448(k, enc) == bytes(56)
        with pytest.raises(ValueError):
            x448_shared(k, enc)


def test_bad_lengths() -> None:
    with pytest.raises(ValueError):
        x448(bytes(55), bytes(56))
    with pytest.raises(ValueError):
        x448(bytes(56), bytes(32))
