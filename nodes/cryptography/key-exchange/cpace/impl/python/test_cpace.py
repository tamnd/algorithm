# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cpace/. The authors are listed in prov/RGPFSD.jsonl.

import random

import pytest

from cpace import (
    CPaceError,
    calculate_generator,
    decode_u,
    derive_isk,
    generator_string,
    h_hash,
    lv_cat,
    message,
    prepend_len,
    run,
    scalar_mult_vfy,
    transcript_ir,
    transcript_oc,
    x25519,
)


def h(s: str) -> bytes:
    return bytes.fromhex("".join(s.split()))


# ---------------------------------------------------------------- RFC 7748, Section 5.2, copied by hand


def test_x25519_rfc7748_section_5_2():
    assert x25519(
        h("a546e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449ac4"),
        h("e6db6867583030db3594c1a424b15f7c726624ec26b3353b10a903a6d0ab1c4c"),
    ) == h("c3da55379de9c6908e94ea4df28d084f32eccf03491c71f754b4075577a28552")
    assert x25519(
        h("4b66e9d4d1b4673c5ad22691957d6af5c11b6421e0ea01d42ca4169e7918ba0d"),
        h("e5210f12786811d3f4b7959d0538ae2c31dbe7106fc03c3efc4cd549c715a493"),
    ) == h("95cbde9476e8907d7aade45cb4b873f88b595a68799fa152e6f8f7647aac7957")


# ---------------------------------------------------------------- draft-irtf-cfrg-cpace-21, Appendix A.1, copied by hand


def test_prepend_len_and_lv_cat():
    assert prepend_len(b"") == h("00")
    assert prepend_len(b"1234") == h("0431323334")
    assert prepend_len(bytes(range(127)))[:1] == h("7f") and len(prepend_len(bytes(range(127)))) == 128
    assert prepend_len(bytes(range(128)))[:2] == h("8001") and len(prepend_len(bytes(range(128)))) == 130
    assert lv_cat(b"1234", b"5", b"", b"678") == h("043132333401350003363738")


# ---------------------------------------------------------------- draft-irtf-cfrg-cpace-21, Appendix B.1, copied by hand

PRS = b"Password"
CI = h("0b415f696e69746961746f720b425f726573706f6e646572")
SID = h("7e4b4791d6a8ef019b936c79fb7f2c57")
GEN_STR = h("""
0843506163653235350850617373776f72646d000000000000000000
00000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000180b415f696e69746961746f
720b425f726573706f6e646572107e4b4791d6a8ef019b936c79fb7f
2c57""")
GEN_HASH = h("03998087bdb1a2617bbe25ef5a7c18cd4f84f902328701790958755ee4aed1d3")
GEN_FIELD = h("03998087bdb1a2617bbe25ef5a7c18cd4f84f902328701790958755ee4aed153")
GEN_G = h("d04bf6d41f6a289632a2e929fa29bebd51092512a7829fdde7d314b62f05a73f")
YA_SCALAR = h("21b4f4bd9e64ed355c3eb676a28ebedaf6d8f17bdc365995b319097153044080")
YA = h("1d13c89278cdadd826f6d8d7f887701430f8380ddc17611cdd6dc989ce0c9f32")
YB_SCALAR = h("848b0779ff415f0af4ea14df9dd1d3c29ac41d836c7808896c4eba19c51ac40a")
YB = h("248cccf6d5cdc3646f0ad593f9e6cef4e69d4945f8372e623512ecea32185623")
K = h("5b067effbdc0b2a0e1d907b21ebb25cfedb96a852179a847c37e43ee71322c6b")
TR_IR = h("""
201d13c89278cdadd826f6d8d7f887701430f8380ddc17611cdd6dc9
89ce0c9f320341446120248cccf6d5cdc3646f0ad593f9e6cef4e69d
4945f8372e623512ecea3218562303414462""")
ISK_IR = h("""
6e19b875f7a561d6b3ca3dbb9ef42ac55de3e717881018204b8922b4
d5e53bb2aa82c300bea7b65d2b671da71922ddf6472301b79bc270ad
fa8bf413285f2263""")
TR_OC = h("""
6f6320248cccf6d5cdc3646f0ad593f9e6cef4e69d4945f8372e6235
12ecea3218562303414462201d13c89278cdadd826f6d8d7f8877014
30f8380ddc17611cdd6dc989ce0c9f3203414461""")
ISK_OC = h("""
eef745e2f6e7ae2b1a1e53da340e777167a07fe150436648c51fb199
c11f3cbabfc683a2b48e1af5881940dc398d375c95e6b4ae9948a45b
8770de0656382be4""")
SID_OUT_IR = h("""
cbc73f62589bbc96ab6a95ec2363df621e93bc3b0cea83ba6b9571d0
05fa8f5d2d08f7165622777fa484c02a9e6b20a84ee2dbebae8c53be
757dcfc0eebdeb5f""")


def test_b11_calculate_generator():
    gs = generator_string(b"CPace255", PRS, CI, SID)
    assert gs == GEN_STR and len(gs) == 170
    assert h_hash(gs, 32) == GEN_HASH
    assert decode_u(GEN_HASH) == int.from_bytes(GEN_FIELD, "little")
    assert calculate_generator(PRS, CI, SID) == GEN_G


def test_b12_to_b14_messages_and_K():
    assert message(PRS, CI, SID, YA_SCALAR) == YA
    assert message(PRS, CI, SID, YB_SCALAR) == YB
    assert scalar_mult_vfy(YA_SCALAR, YB) == K
    assert scalar_mult_vfy(YB_SCALAR, YA) == K


def test_b15_b16_isk_and_b17_sid_output():
    assert transcript_ir(YA, b"ADa", YB, b"ADb") == TR_IR
    assert derive_isk(YA_SCALAR, YB, SID, TR_IR) == ISK_IR
    assert derive_isk(YB_SCALAR, YA, SID, TR_IR) == ISK_IR
    assert transcript_oc(YA, b"ADa", YB, b"ADb") == TR_OC
    assert derive_isk(YA_SCALAR, YB, SID, TR_OC) == ISK_OC
    assert h_hash(b"CPaceSidOutput" + TR_IR) == SID_OUT_IR


def test_run_reproduces_vector():
    isk_a, isk_b = run(PRS, PRS, CI, SID, ya=YA_SCALAR, yb=YB_SCALAR)
    assert isk_a == isk_b == ISK_IR


# Appendix B.1.10: low-order and non-canonical u-coordinates.
S_LOW = h("af46e36bf0527c9d3b16154b82465edd62144c0ac1fc5a18506a2244ba449aff")
LOW_ORDER_ABORT = [
    "0000000000000000000000000000000000000000000000000000000000000000",
    "0100000000000000000000000000000000000000000000000000000000000000",
    "ecffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f",
    "e0eb7a7c3b41b8ae1656e3faf19fc46ada098deb9c32b1fd866205165f49b800",
    "5f9c95bca3508c24b1d0b1559c83ef5b04445cc4581c8e86d8224eddd09f1157",
    "edffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f",
    "eeffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7f",
]
NON_CANONICAL = [
    ("daffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
     "d8e2c776bbacd510d09fd9278b7edcd25fc5ae9adfba3b6e040e8d3b71b21806"),
    ("dbffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
     "c85c655ebe8be44ba9c0ffde69f2fe10194458d137f09bbff725ce58803cdb38"),
    ("d9ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
     "db64dafa9b8fdd136914e61461935fe92aa372cb056314e1231bc4ec12417456"),
    ("cdeb7a7c3b41b8ae1656e3faf19fc46ada098deb9c32b1fd866205165f49b880",
     "e062dcd5376d58297be2618c7498f55baa07d7e03184e8aada20bca28888bf7a"),
    ("4c9c95bca3508c24b1d0b1559c83ef5b04445cc4581c8e86d8224eddd09f11d7",
     "993c6ad11c4c29da9a56f7691fd0ff8d732e49de6250b6c2e80003ff4629a175"),
]


@pytest.mark.parametrize("u", LOW_ORDER_ABORT)
def test_b110_low_order_points_abort(u):
    assert scalar_mult_vfy(S_LOW, h(u)) == bytes(32)
    with pytest.raises(CPaceError):
        derive_isk(S_LOW, h(u), SID, b"")


@pytest.mark.parametrize("u,q", NON_CANONICAL)
def test_b110_non_canonical_inputs(u, q):
    assert scalar_mult_vfy(S_LOW, h(u)) == h(q)


def test_wrong_password_gives_different_keys():
    rng = random.Random(5)
    ya = bytes(rng.randrange(256) for _ in range(32))
    yb = bytes(rng.randrange(256) for _ in range(32))
    isk_a, isk_b = run(b"Password", b"Passw0rd", CI, SID, ya=ya, yb=yb)
    assert isk_a != isk_b


def test_generator_depends_on_sid():
    assert calculate_generator(PRS, CI, SID) != calculate_generator(PRS, CI, bytes(16))
