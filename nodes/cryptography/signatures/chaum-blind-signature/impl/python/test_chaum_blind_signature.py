# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chaum-blind-signature/. The authors are listed in prov/BFYHY3.jsonl.
"""Tests for RSABSSA against the test vectors of RFC 9474, Appendix A.

The four vectors share the key, msg, salt and inv. Long outputs are checked
by their SHA-256 digests to keep the file small.
"""

import hashlib
import random

import pytest

from chaum_blind_signature import (
    PSS_DETERMINISTIC,
    PSS_RANDOMIZED,
    PSSZERO_DETERMINISTIC,
    PSSZERO_RANDOMIZED,
    blind,
    blind_sign,
    blinding_factor_for,
    emsa_pss_encode,
    finalize,
    key_from_primes,
    os2ip,
    prepare,
    verify,
)

P = int(
    "e1f4d7a34802e27c7392a3cea32a262a34dc3691bd87f3f310dc75673488930559c120fd0410194fb8a0da55bd0b81227e843fdca6692ae80e"
    "5a5d414116d4803fca7d8c30eaaae57e44a1816ebb5c5b0606c536246c7f11985d731684150b63c9a3ad9e41b04c0b5b27cb188a692c84696b"
    "742a80d3cd00ab891f2457443dadfeba6d6daf108602be26d7071803c67105a5426838e6889d77e8474b29244cefaf418e381b312048b457d7"
    "3419213063c60ee7b0d81820165864fef93523c9635c22210956e53a8d96322493ffc58d845368e2416e078e5bcb5d2fd68ae6acfa54f9627c"
    "42e84a9d3f2774017e32ebca06308a12ecc290c7cd1156dcccfb2311",
    16,
)
Q = int(
    "c601a9caea66dc3835827b539db9df6f6f5ae77244692780cd334a006ab353c806426b60718c05245650821d39445d3ab591ed10a7339f15d8"
    "3fe13f6a3dfb20b9452c6a9b42eaa62a68c970df3cadb2139f804ad8223d56108dfde30ba7d367e9b0a7a80c4fdba2fd9dde6661fc73fc2947"
    "569d2029f2870fc02d8325acf28c9afa19ecf962daa7916e21afad09eb62fe9f1cf91b77dc879b7974b490d3ebd2e95426057f35d0a3c9f45f"
    "79ac727ab81a519a8b9285932d9b2e5ccd347e59f3f32ad9ca359115e7da008ab7406707bd0e8e185a5ed8758b5ba266e8828f8d863ae13384"
    "6304a2936ad7bc7c9803879d2fc4a28e69291d73dbd799f8bc238385",
    16,
)
N_SHA256 = "1a6cf8eba29dfd29e72e94ea99e91a346a158494b73d3724fb4069a11a57503e"
MSG = bytes.fromhex(
    "8f3dc6fb8c4a02f4d6352edf0907822c1210a9b32f9bdda4c45a698c80023aa6b59f8cfec5fdbb36331372ebefedae7d"
)
SALT = bytes.fromhex(
    "051722b35f458781397c3a671a7d3bd3096503940e4c4f1aaa269d60300ce449555cd7340100df9d46944c5356825abf"
)
INV = int(
    "80682c48982407b489d53d1261b19ec8627d02b8cda5336750b8cee332ae260de57b02d72609c1e0e9f28e2040fc65b6f02d56dbd6aa9af8fd"
    "e656f70495dfb723ba01173d4707a12fddac628ca29f3e32340bd8f7ddb557cf819f6b01e445ad96f874ba235584ee71f6581f62d4f43bf03f"
    "910f6510deb85e8ef06c7f09d9794a008be7ff2529f0ebb69decef646387dc767b74939265fec0223aa6d84d2a8a1cc912d5ca25b4e144ab8f"
    "6ba054b54910176d5737a2cff011da431bd5f2a0d2d66b9e70b39f4b050e45c0d9c16f02deda9ddf2d00f3e4b01037d7029cd49c2d46a8e1fc"
    "2c0c17520af1f4b5e25ba396afc4cd60c494a4c426448b35b49635b337cfb08e7c22a39b256dd032c00adddafb51a627f99a0e1704170ac1f1"
    "912e49d9db10ec04c19c58f420212973e0cb329524223a6aa56c7937c5dffdb5d966b6cd4cbc26f3201dd25c80960a1a111b32947bb78973d2"
    "69fac7f5186530930ed19f68507540eed9e1bab8b00f00d8ca09b3f099aae46180e04e3584bd7ca054df18a1504b89d1d1675d0966c4ae1407"
    "be325cdf623cf13ff13e4a28b594d59e3eadbadf6136eee7a59d6a444c9eb4e2198e8a974f27a39eb63af2c9af3870488b8adaad444674f512"
    "133ad80b9220e09158521614f1faadfe8505ef57b7df6813048603f0dd04f4280177a11380fbfc861dbcbd7418d62155248dad5fdec0991f",
    16,
)

# (variant, msg_prefix, SHA-256 of encoded_msg, blinded_msg, blind_sig, sig)
VECTORS = [
    (
        PSS_RANDOMIZED,
        "8417e699b219d583fb6216ae0c53ca0e9723442d02f1d1a34295527e7d929e8b",
        "46ad345708f266d9dd091b49219bcf6a9c47b7d89421a8ad7ad77991d7d178cf",
        "c20660023bbbe565cd45163505209c98693ee6004f179ecff6446f07319d102c",
        "73b1978d4dbbb4ce892f04c9a022c3596ee8912a9be3c183a3912d42f915a7d1",
        "637dffe92ee76ccfd6fd3cb22190fa15164ed586baa5c2b9e872ddcd981c80ec",
    ),
    (
        PSSZERO_RANDOMIZED,
        "84ea86c8cf3beedfed73beceabd792027c609d1100bf041fdd60d826a718130d",
        "01a90fd1ca84ea6e9fa611bf30777d3839c847974081cea45a42cc058ae89941",
        "f755bbf19869b37e2177dbdee523f01df9b50c11b9a797d4dba130d549096f9c",
        "c3383ae4f2291cc5159313a023c633583df4523667f1fe8576fd78cf9f95ee13",
        "fa30839de7de289a7fc1e90560c06ff24457be997292d871ccb5990626814e9d",
    ),
    (
        PSS_DETERMINISTIC,
        None,
        "3226b666b9a92c20d2fc8ca1cac9eb68076dfa3c8549c1f9f6e3161feedd44b8",
        "60e1ee70f9e09de36e1cefe8a73a96ef3b9df13fbcb6f4fd849142bc41f4a559",
        "9317585a9f255b9e449d65ae681c9621d207430c03cf729ecfce968ea18d5fa9",
        "87fcc997e9d5ab1e2031a995641f2e40fd4c359cdd2adfcf4f642eb8ec9cf781",
    ),
    (
        PSSZERO_DETERMINISTIC,
        None,
        "a0ec24312b376180a15be54c1e17a391b485a6cd7e5919ddce0fdb838c3ed381",
        "2febd681d9bd5716c059dd2a9028e52fdc581203d35d7ef9428594fab25794d7",
        "a35fc81050ea8f65091d56693c3fc09c68ed75502d467e255f49aaf271c63f4a",
        "60b25927bf3ac543de3c8b6f6ca4f60241f4a099e7f3ab5e08a422cca8358e8f",
    ),
]

SK = key_from_primes(P, Q)
PK = SK.pk


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def test_key() -> None:
    assert sha(PK.n.to_bytes(512, "big")) == N_SHA256
    assert PK.n.bit_length() == 4096 and PK.k == 512


@pytest.mark.parametrize("vec", VECTORS, ids=[v[0].name for v in VECTORS])
def test_rfc9474_vector(vec) -> None:
    v, prefix, h_enc, h_blinded, h_bsig, h_sig = vec
    input_msg = prepare(MSG, v, bytes.fromhex(prefix) if prefix else None)
    salt = SALT[: v.salt_len]
    assert sha(emsa_pss_encode(input_msg, PK.n.bit_length() - 1, salt)) == h_enc
    blinded, inv = blind(PK, input_msg, v, salt=salt, r=pow(INV, -1, PK.n))
    assert inv == INV
    assert sha(blinded) == h_blinded
    bsig = blind_sign(SK, blinded)
    assert sha(bsig) == h_bsig
    sig = finalize(PK, input_msg, bsig, inv, v)
    assert sha(sig) == h_sig
    assert verify(PK, input_msg, sig, v)
    assert not verify(PK, input_msg + b"x", sig, v)


def test_signer_view_fits_every_signature() -> None:
    """Blindness: each session view (z, s') matches each final signature with
    some blinding factor r, so the views carry no link to the signatures."""
    v = PSS_RANDOMIZED
    sessions, outputs = [], []
    for i in range(2):
        m = prepare(b"coin %d" % i, v)
        z, inv = blind(PK, m, v)
        s1 = blind_sign(SK, z)
        sessions.append((z, s1))
        outputs.append((m, finalize(PK, m, s1, inv, v)))
    for z, s1 in sessions:
        for m, sig in outputs:
            assert verify(PK, m, sig, v)
            r = blinding_factor_for(PK, z, s1, sig)
            em = pow(os2ip(sig), PK.e, PK.n)  # the encoded message of the output
            assert em * pow(r, PK.e, PK.n) % PK.n == os2ip(z)


def test_finalize_rejects_a_bad_blind_signature() -> None:
    v = PSSZERO_DETERMINISTIC
    z, inv = blind(PK, MSG, v)
    bsig = bytearray(blind_sign(SK, z))
    bsig[-1] ^= 1
    with pytest.raises(ValueError):
        finalize(PK, MSG, bytes(bsig), inv, v)


def test_blinded_message_looks_uniform() -> None:
    """The same message blinded twice gives unrelated values."""
    v = PSS_DETERMINISTIC
    z1, _ = blind(PK, MSG, v, salt=SALT, r=random.Random(1).randrange(1, PK.n))
    z2, _ = blind(PK, MSG, v, salt=SALT, r=random.Random(2).randrange(1, PK.n))
    assert z1 != z2
    with pytest.raises(ValueError):
        blind_sign(SK, b"\xff" * PK.k)  # not below n
