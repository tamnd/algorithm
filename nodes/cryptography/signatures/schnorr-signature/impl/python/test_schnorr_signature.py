# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schnorr-signature/. The authors are listed in prov/PS9P4P.jsonl.

import random

from schnorr_signature import (
    G,
    N,
    TOY_P,
    TOY_Q,
    point_add,
    point_mul,
    pubkey_gen,
    schnorr_sign,
    schnorr_verify,
    toy_keygen,
    toy_sign,
    toy_to_es,
    toy_verify,
    toy_verify_es,
)

# Official vectors: BIP 340, file bip-0340/test-vectors.csv, copied by hand.
# Columns: index, secret key, public key, aux_rand, message, signature, result.
SIGN_VECTORS = [
    (
        0,
        "0000000000000000000000000000000000000000000000000000000000000003",
        "F9308A019258C31049344F85F89D5229B531C845836F99B08601F113BCE036F9",
        "0000000000000000000000000000000000000000000000000000000000000000",
        "0000000000000000000000000000000000000000000000000000000000000000",
        "E907831F80848D1069A5371B402410364BDF1C5F8307B0084C55F1CE2DCA8215"
        "25F66A4A85EA8B71E482A74F382D2CE5EBEEE8FDB2172F477DF4900D310536C0",
    ),
    (
        1,
        "B7E151628AED2A6ABF7158809CF4F3C762E7160F38B4DA56A784D9045190CFEF",
        "DFF1D77F2A671C5F36183726DB2341BE58FEAE1DA2DECED843240F7B502BA659",
        "0000000000000000000000000000000000000000000000000000000000000001",
        "243F6A8885A308D313198A2E03707344A4093822299F31D0082EFA98EC4E6C89",
        "6896BD60EEAE296DB48A229FF71DFE071BDE413E6D43F917DC8DCF8C78DE3341"
        "8906D11AC976ABCCB20B091292BFF4EA897EFCB639EA871CFA95F6DE339E4B0A",
    ),
    (
        2,
        "C90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B14E5C9",
        "DD308AFEC5777E13121FA72B9CC1B7CC0139715309B086C960E18FD969774EB8",
        "C87AA53824B4D7AE2EB035A2B5BBBCCC080E76CDC6D1692C4B0B62D798E6D906",
        "7E2D58D8B3BCDF1ABADEC7829054F90DDA9805AAB56C77333024B9D0A508B75C",
        "5831AAEED7B44BB74E5EAB94BA9D4294C49BCF2A60728D8B4C200F50DD313C1B"
        "AB745879A5AD954A72C45A91C3A51D3C7ADEA98D82F8481E0E1E03674A6F3FB7",
    ),
]

# BIP 340 test-vectors.csv rows 4, 5 and 6: verification only.
VERIFY_VECTORS = [
    (
        4,
        "D69C3509BB99E412E68B0FE8544E72837DFA30746D8BE2AA65975F29D22DC7B9",
        "4DF3C3F68FCC83B27E9D42C90431A72499F17875C81A599B566C9889B9696703",
        "00000000000000000000003B78CE563F89A0ED9414F5AA28AD0D96D6795F9C63"
        "76AFB1548AF603B3EB45C9F8207DEE1060CB71C04E80F593060B07D28308D7F4",
        True,
    ),
    (
        5,  # public key not on the curve
        "EEFDEA4CDB677750A420FEE807EACF21EB9898AE79B9768766E4FAA04A2D4A34",
        "243F6A8885A308D313198A2E03707344A4093822299F31D0082EFA98EC4E6C89",
        "6CFF5C3BA86C69EA4B7376F31A9BCB4F74C1976089B2D9963DA2E5543E177769"
        "69E89B4C5564D00349106B8497785DD7D1D713A8AE82B32FA79D5F7FC407D39B",
        False,
    ),
    (
        6,  # has_even_y(R) is false
        "DFF1D77F2A671C5F36183726DB2341BE58FEAE1DA2DECED843240F7B502BA659",
        "243F6A8885A308D313198A2E03707344A4093822299F31D0082EFA98EC4E6C89",
        "FFF97BD5755EEEA420453A14355235D382F6472F8568A18B2F057A14602975563"
        "CC27944640AC607CD107AE10923D9EF7A73C643E166BE5EBEAFA34B1AC553E2",
        False,
    ),
]


def test_bip340_sign_vectors() -> None:
    for index, sk, pk, aux, msg, sig in SIGN_VECTORS:
        sk_b, pk_b = bytes.fromhex(sk), bytes.fromhex(pk)
        msg_b, sig_b = bytes.fromhex(msg), bytes.fromhex(sig)
        assert pubkey_gen(sk_b) == pk_b, index
        assert schnorr_sign(msg_b, sk_b, bytes.fromhex(aux)) == sig_b, index
        assert schnorr_verify(msg_b, pk_b, sig_b), index


def test_bip340_verify_vectors() -> None:
    for index, pk, msg, sig, expected in VERIFY_VECTORS:
        got = schnorr_verify(bytes.fromhex(msg), bytes.fromhex(pk), bytes.fromhex(sig))
        assert got is expected, index


def test_bip340_rejects_changes() -> None:
    _, sk, pk, aux, msg, sig = SIGN_VECTORS[1]
    pk_b, msg_b, sig_b = bytes.fromhex(pk), bytes.fromhex(msg), bytes.fromhex(sig)
    bad_msg = bytes([msg_b[0] ^ 1]) + msg_b[1:]
    assert not schnorr_verify(bad_msg, pk_b, sig_b)
    bad_sig = sig_b[:63] + bytes([sig_b[63] ^ 1])
    assert not schnorr_verify(msg_b, pk_b, bad_sig)
    # s = n is out of range and must be rejected, even though s = 0 mod n.
    high_s = sig_b[:32] + N.to_bytes(32, "big")
    assert not schnorr_verify(msg_b, pk_b, high_s)


def test_bip340_round_trip_and_odd_key() -> None:
    rng = random.Random(340)
    for _ in range(2):
        sk = rng.randrange(1, N).to_bytes(32, "big")
        msg = rng.randbytes(rng.randrange(0, 50))
        sig = schnorr_sign(msg, sk, rng.randbytes(32))
        assert schnorr_verify(msg, pubkey_gen(sk), sig)
    # A secret key d and its negation n - d have the same x-only public key.
    sk = (N - 3).to_bytes(32, "big")
    assert pubkey_gen(sk) == pubkey_gen((3).to_bytes(32, "big"))


def test_group_law() -> None:
    two_g = point_add(G, G)
    assert point_mul(G, 2) == two_g
    assert point_add(point_mul(G, 5), point_mul(G, 7)) == point_mul(G, 12)
    assert point_mul(G, N) is None


def test_toy_scheme_both_forms() -> None:
    rng = random.Random(1991)
    wrong_accepted = 0
    for _ in range(200):
        x = rng.randrange(1, TOY_Q)
        y = toy_keygen(x)
        msg = rng.randbytes(8)
        sig = toy_sign(x, msg, rng.randrange(1, TOY_Q))
        assert toy_verify(y, msg, sig)
        es = toy_to_es(y, msg, sig)
        assert toy_verify_es(y, msg, es)
        # A changed message passes only if the toy hash collides mod q (about 1 in 1019).
        wrong_accepted += toy_verify(y, msg + b"!", sig)
    assert wrong_accepted <= 3


def test_toy_worked_example() -> None:
    # The worked example of the page: x = 123, k = 456, message "hi".
    x, k, msg = 123, 456, b"hi"
    y = toy_keygen(x)
    r_elem, s = toy_sign(x, msg, k)
    assert y == pow(4, 123, TOY_P)
    assert r_elem == pow(4, 456, TOY_P)
    assert toy_verify(y, msg, (r_elem, s))
    e, s2 = toy_to_es(y, msg, (r_elem, s))
    assert s2 == s and toy_verify_es(y, msg, (e, s))


def test_toy_forgeries_fail() -> None:
    rng = random.Random(7)
    x = 321
    y = toy_keygen(x)
    sig = toy_sign(x, b"m", 99)
    rejected = 0
    for _ in range(200):
        r_elem, s = sig
        forged = (r_elem, (s + rng.randrange(1, TOY_Q)) % TOY_Q)
        rejected += not toy_verify(y, b"m", forged)
    assert rejected == 200
    # A value R outside the subgroup of order q is rejected.
    assert not toy_verify(y, b"m", (TOY_P - 1, sig[1]))
