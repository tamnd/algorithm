# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/musig/. The authors are listed in prov/AZY9JE.jsonl.

import random

from musig import (
    G,
    N,
    bip340_sign_with_scalar,
    cbytes,
    cpoint,
    key_agg,
    naive_key_sum,
    nonce_agg,
    nonce_gen,
    partial_sig_agg,
    partial_sig_verify,
    point_add,
    point_mul,
    point_neg,
    schnorr_verify,
    sign,
    xbytes,
)

# BIP 327, file bip-0327/vectors/key_agg_vectors.json, "pubkeys" and "valid_test_cases",
# copied by hand.
KEY_AGG_PUBKEYS = [
    bytes.fromhex("02F9308A019258C31049344F85F89D5229B531C845836F99B08601F113BCE036F9"),
    bytes.fromhex("03DFF1D77F2A671C5F36183726DB2341BE58FEAE1DA2DECED843240F7B502BA659"),
    bytes.fromhex("023590A94E768F8E1815C2F24B4D80A8E3149316C3518CE7B7AD338368D038CA66"),
]
KEY_AGG_VALID = [
    ([0, 1, 2], "90539EEDE565F5D054F32CC0C220126889ED1E5D193BAF15AEF344FE59D4610C"),
    ([2, 1, 0], "6204DE8B083426DC6EAF9502D27024D53FC826BF7D2012148A0575435DF54B2B"),
    ([0, 0, 0], "B436E3BAD62B8CD409969A224731C193D051162D8C5AE8B109306127DA3AA935"),
    ([0, 0, 1, 1], "69BC22BFA5D106306E48A20679DE1D7389386124D07571D0D872686028C26A3E"),
]


def test_bip327_key_agg_vectors() -> None:
    for idx, expected in KEY_AGG_VALID:
        q = key_agg([KEY_AGG_PUBKEYS[i] for i in idx])
        assert xbytes(q).hex().upper() == expected


def run_session(sks: list[int], msg: bytes, rng: random.Random) -> tuple[list[bytes], bytes]:
    pubkeys = [cbytes(point_mul(G, sk)) for sk in sks]
    nonces = [nonce_gen(rng) for _ in sks]
    aggnonce = nonce_agg([pn for _, pn in nonces])
    psigs = []
    for sk, pk, (secn, pubn) in zip(sks, pubkeys, nonces):
        s_i = sign(secn, sk, aggnonce, pubkeys, msg)
        assert partial_sig_verify(s_i, pubn, pk, aggnonce, pubkeys, msg)
        psigs.append(s_i)
    return pubkeys, partial_sig_agg(psigs, aggnonce, pubkeys, msg)


def test_two_and_three_signers_verify_under_bip340() -> None:
    rng = random.Random(327)
    for count in (2, 3):
        sks = [rng.randrange(1, N) for _ in range(count)]
        msg = b"MuSig2 with %d signers" % count
        pubkeys, sig = run_session(sks, msg, rng)
        agg = xbytes(key_agg(pubkeys))
        assert schnorr_verify(msg, agg, sig)
        assert not schnorr_verify(msg + b"!", agg, sig)


def test_bad_partial_signature_is_caught() -> None:
    rng = random.Random(9)
    sks = [rng.randrange(1, N) for _ in range(2)]
    pubkeys = [cbytes(point_mul(G, sk)) for sk in sks]
    nonces = [nonce_gen(rng) for _ in sks]
    aggnonce = nonce_agg([pn for _, pn in nonces])
    s0 = sign(nonces[0][0], sks[0], aggnonce, pubkeys, b"m")
    assert not partial_sig_verify((s0 + 1) % N, nonces[0][1], pubkeys[0], aggnonce, pubkeys, b"m")
    # A partial signature checked against the other signer's nonce fails too.
    assert not partial_sig_verify(s0, nonces[1][1], pubkeys[0], aggnonce, pubkeys, b"m")


def test_rogue_key_breaks_naive_sum_but_not_key_agg() -> None:
    rng = random.Random(2019)
    victim = cbytes(point_mul(G, rng.randrange(1, N)))
    beta = rng.randrange(1, N)
    # The attacker announces rogue = beta G - P_victim and knows no secret for it.
    rogue = cbytes(point_add(point_mul(G, beta), point_neg(cpoint(victim))))
    msg = b"pay everything to the attacker"
    naive = naive_key_sum([victim, rogue])
    assert naive == point_mul(G, beta)
    forged = bip340_sign_with_scalar(beta, msg, rng.randrange(1, N))
    assert schnorr_verify(msg, xbytes(naive), forged)
    # With BIP 327 key aggregation the aggregate key is not beta G, so the same forgery fails.
    q = key_agg([victim, rogue])
    assert q != point_mul(G, beta)
    assert not schnorr_verify(msg, xbytes(q), forged)
