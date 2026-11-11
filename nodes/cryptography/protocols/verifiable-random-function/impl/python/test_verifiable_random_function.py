# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verifiable-random-function/. The authors are listed in prov/NY3QP4.jsonl.
#
# Official vectors: RFC 9381, Appendix B.3 (ECVRF-EDWARDS25519-SHA512-TAI),
# Examples 16, 17 and 18, copied by hand. The secret keys are those of
# RFC 8032, Section 7.1, TESTS 1, 2 and 3.

import random

from verifiable_random_function import (
    BASE,
    IDENTITY,
    Q,
    decode_proof,
    encode_to_curve,
    nonce_generation,
    point_equal,
    point_to_string,
    proof_to_hash,
    prove,
    public_key,
    scalar_mult,
    secret_scalar,
    string_to_point,
    verify,
)


def h(s: str) -> bytes:
    return bytes.fromhex(s.replace(" ", ""))


VECTORS = [
    # RFC 9381, Appendix B.3, Example 16
    dict(
        sk="9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60",
        pk="d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a",
        alpha="",
        x="307c83864f2833cb427a2ef1c00a013cfdff2768d980c0a3a520f006904de94f",
        H="91bbed02a99461df1ad4c6564a5f5d829d0b90cfc7903e7a5797bd658abf3318",
        k="8a49edbd1492a8ee09766befe50a7d563051bf3406cbffc20a88def030730f0f",
        U="aef27c725be964c6a9bf4c45ca8e35df258c1878b838f37d9975523f09034071",
        V="5016572f71466c646c119443455d6cb9b952f07d060ec8286d678615d55f954f",
        pi="8657106690b5526245a92b003bb079ccd1a92130477671f6fc01ad16f26f7"
        "23f26f8a57ccaed74ee1b190bed1f479d9727d2d0f9b005a6e456a35d4fb0daab1"
        "268a1b0db10836d9826a528ca76567805",
        beta="90cf1df3b703cce59e2a35b925d411164068269d7b2d29f3301c03dd757"
        "876ff66b71dda49d2de59d03450451af026798e8f81cd2e333de5cdf4f3e140fdd"
        "8ae",
    ),
    # RFC 9381, Appendix B.3, Example 17
    dict(
        sk="4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb",
        pk="3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c",
        alpha="72",
        x="68bd9ed75882d52815a97585caf4790a7f6c6b3b7f821c5e259a24b02e502e51",
        H="5b659fc3d4e9263fd9a4ed1d022d75eaacc20df5e09f9ea937502396598dc551",
        k="d8c3a66921444cb3427d5d989f9b315aa8ca3375e9ec4d52207711a1fdb44107",
        U="1dcb0a4821a2c48bf53548228b7f170962988f6d12f5439f31987ef41f034ab3",
        V="fd03c0bf498c752161bae4719105a074630a2aa5f200ff7b3995f7bfb1513423",
        pi="f3141cd382dc42909d19ec5110469e4feae18300e94f304590abdced48aed"
        "5933bf0864a62558b3ed7f2fea45c92a465301b3bbf5e3e54ddf2d935be3b67926"
        "da3ef39226bbc355bdc9850112c8f4b02",
        beta="eb4440665d3891d668e7e0fcaf587f1b4bd7fbfe99d0eb2211ccec90496"
        "310eb5e33821bc613efb94db5e5b54c70a848a0bef4553a41befc57663b56373a5"
        "031",
    ),
    # RFC 9381, Appendix B.3, Example 18
    dict(
        sk="c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7",
        pk="fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025",
        alpha="af82",
        x="909a8b755ed902849023a55b15c23d11ba4d7f4ec5c2f51b1325a181991ea95c",
        H="bf4339376f5542811de615e3313d2b36f6f53c0acfebb482159711201192576a",
        k="5ffdbc72135d936014e8ab708585fda379405542b07e3bd2c0bd48437fbac60a",
        U="2bae73e15a64042fcebf062abe7e432b2eca6744f3e8265bc38e009cd577ecd5",
        V="88cba1cb0d4f9b649d9a86026b69de076724a93a65c349c988954f0961c5d506",
        pi="9bc0f79119cc5604bf02d23b4caede71393cedfbb191434dd016d30177ccb"
        "f8096bb474e53895c362d8628ee9f9ea3c0e52c7a5c691b6c18c9979866568add7"
        "a2d41b00b05081ed0f58ee5e31b3a970e",
        beta="645427e5d00c62a23fb703732fa5d892940935942101e456ecca7bb217c"
        "61c452118fec1219202a0edcf038bb6373241578be7217ba85a2687f7a0310b2df"
        "19f",
    ),
]


def test_public_keys_rfc8032():
    for v in VECTORS:
        assert public_key(h(v["sk"])) == h(v["pk"])


def test_intermediate_values():
    for v in VECTORS:
        sk, pk, alpha = h(v["sk"]), h(v["pk"]), h(v["alpha"])
        x = secret_scalar(sk)
        assert x.to_bytes(32, "little") == h(v["x"])
        hp = encode_to_curve(pk, alpha)
        assert point_to_string(hp) == h(v["H"])
        k = nonce_generation(sk, point_to_string(hp))
        assert k.to_bytes(32, "little") == h(v["k"])
        assert point_to_string(scalar_mult(k, BASE)) == h(v["U"])
        assert point_to_string(scalar_mult(k, hp)) == h(v["V"])


def test_prove_and_hash_match_rfc9381():
    for v in VECTORS:
        pi = prove(h(v["sk"]), h(v["alpha"]))
        assert pi == h(v["pi"])
        assert proof_to_hash(pi) == h(v["beta"])


def test_verify_accepts_official_proofs():
    for v in VECTORS:
        assert verify(h(v["pk"]), h(v["alpha"]), h(v["pi"])) == h(v["beta"])


def test_verify_rejects_changed_inputs():
    v = VECTORS[1]
    pk, alpha, pi = h(v["pk"]), h(v["alpha"]), h(v["pi"])
    assert verify(pk, b"\x73", pi) is None  # other input
    assert verify(h(VECTORS[0]["pk"]), alpha, pi) is None  # other key
    for i in (0, 33, 50, 79):  # a change in Gamma, c or s
        bad = bytearray(pi)
        bad[i] ^= 1
        assert verify(pk, alpha, bytes(bad)) is None


def test_s_not_reduced_is_rejected():
    v = VECTORS[0]
    pi = h(v["pi"])
    s = int.from_bytes(pi[48:], "little")
    bad = pi[:48] + (s + Q).to_bytes(32, "little")
    assert decode_proof(bad) is None


def test_small_order_key_is_rejected():
    # The point (0, -1) has order 2. A key of small order would let a
    # cheating prover make proofs for many outputs.
    small = string_to_point((2**255 - 20).to_bytes(32, "little"))
    assert small is not None
    assert point_equal(scalar_mult(8, small), IDENTITY)
    v = VECTORS[0]
    assert verify(point_to_string(small), h(v["alpha"]), h(v["pi"])) is None


def test_uniqueness_and_determinism():
    rng = random.Random(9381)
    sk = bytes(rng.randrange(256) for _ in range(32))
    pk = public_key(sk)
    outs = set()
    for i in range(6):
        alpha = bytes([i])
        pi1, pi2 = prove(sk, alpha), prove(sk, alpha)
        assert pi1 == pi2
        beta = verify(pk, alpha, pi1)
        assert beta is not None and len(beta) == 64
        outs.add(beta)
    assert len(outs) == 6


def test_group_order():
    assert point_equal(scalar_mult(Q, BASE), IDENTITY)
    assert not point_equal(scalar_mult(Q - 1, BASE), IDENTITY)
