# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/picnic-signature/. The authors are listed in prov/CCDYS8.jsonl.

import math
import random

from picnic_signature import (
    ROUNDS,
    T_ROUNDS,
    _commit,
    _expand,
    challenge,
    keygen,
    mpc_run,
    reconstruct,
    sign,
    signature_size,
    toy_cipher,
    verify,
)


def _signed(seed=2024, msg=b"hello"):
    rng = random.Random(seed)
    k, pk = keygen(rng)
    return k, pk, sign(k, pk, msg, rng)


def test_worked_example_key():
    rng = random.Random(2024)
    k, pk = keygen(rng)
    assert (k, pk) == (0x7857DD86, (0x2E84496E, 0xEB8ADDD7))
    assert toy_cipher(k, pk[0]) == pk[1]


def test_mpc_shares_add_up():
    rng = random.Random(5)
    for _ in range(200):
        key, p = rng.getrandbits(32), rng.getrandbits(32)
        k0, k1 = rng.getrandbits(32), rng.getrandbits(32)
        tapes = [[rng.getrandbits(32) for _ in range(ROUNDS)] for _ in range(3)]
        out, z = mpc_run(p, (k0, k1, key ^ k0 ^ k1), tapes)
        assert out[0] ^ out[1] ^ out[2] == toy_cipher(key, p)
        assert all(len(v) == ROUNDS for v in z)


def test_honest_signature_verifies():
    for seed in range(5):
        _, pk, sig = _signed(seed, b"msg %d" % seed)
        assert verify(pk, b"msg %d" % seed, sig)


def test_soundness_bound():
    assert T_ROUNDS * math.log2(3 / 2) > 128
    assert (T_ROUNDS - 1) * math.log2(3 / 2) < 128


def test_other_message_or_key_fails():
    k, pk, sig = _signed()
    assert not verify(pk, b"hellp", sig)
    assert not verify((pk[0], pk[1] ^ 1), b"hello", sig)
    assert not verify((pk[0] ^ 1, pk[1]), b"hello", sig)


def test_changed_views_fail():
    _, pk, (es, resp) = _signed()
    for j in (0, 7, 100, T_ROUNDS - 1):
        seed_e, seed_f, k2b, z_f, c_g = resp[j]
        bad = []
        z_bad = list(z_f)
        z_bad[1] ^= 1 << 9
        bad.append((seed_e, seed_f, k2b, z_bad, c_g))                       # an AND output of the second view
        bad.append((bytes([seed_e[0] ^ 1]) + seed_e[1:], seed_f, k2b, z_f, c_g))  # the seed of the first view
        bad.append((seed_e, bytes([seed_f[0] ^ 1]) + seed_f[1:], k2b, z_f, c_g))  # the seed of the second view
        bad.append((seed_e, seed_f, k2b, z_f, bytes([c_g[0] ^ 1]) + c_g[1:]))     # the closed commitment
        if k2b is not None:
            bad.append((seed_e, seed_f, bytes([k2b[0] ^ 1]) + k2b[1:], z_f, c_g))  # the input share of player 2
        for r in bad:
            changed = list(resp)
            changed[j] = r
            assert not verify(pk, b"hello", (es, changed))


def test_changed_challenge_fails():
    _, pk, (es, resp) = _signed()
    es2 = list(es)
    es2[3] = (es2[3] + 1) % 3
    assert not verify(pk, b"hello", (es2, resp))


def test_wrong_key_fails():
    rng = random.Random(9)
    k, pk = keygen(rng)
    assert not verify(pk, b"m", sign(k ^ 0x10, pk, b"m", rng))


def test_simple_cheat_passes_one_challenge_in_three():
    # A prover with a wrong key runs the MPC honestly and then fixes y_2 so that the
    # three output shares add up to y. The fix is caught unless player 2 stays closed.
    rng = random.Random(11)
    k, pk = keygen(rng)
    p, y = pk
    wrong = k ^ 0xDEAD
    sd = [rng.randbytes(16) for _ in range(3)]
    (k0, t0), (k1, t1), (_, t2) = (_expand(sd[i], i) for i in range(3))
    k2 = wrong ^ k0 ^ k1
    out, z = mpc_run(p, (k0, k1, k2), (t0, t1, t2))
    claimed = [out[0], out[1], out[2] ^ out[0] ^ out[1] ^ out[2] ^ y]
    k2b = k2.to_bytes(4, "little")
    cs = [_commit(sd[i], k2b if i == 2 else None, z[i]) for i in range(3)]
    passes = []
    for e in range(3):
        f, g = (e + 1) % 3, (e + 2) % 3
        r = (sd[e], sd[f], k2b if 2 in (e, f) else None, z[f], cs[g])
        ys, cs2 = reconstruct(pk, e, r)
        passes.append(ys == claimed and cs2 == cs)
    assert passes == [True, False, False]


def test_challenge_is_uniform_enough():
    es = challenge((1, 2), b"x", [[0, 0, 0]], [[b"a", b"b", b"c"]], 3000)
    counts = [es.count(i) for i in range(3)]
    assert all(900 < c < 1100 for c in counts)


def test_size():
    _, _, sig = _signed()
    # 219 rounds of two 16-byte seeds, a 32-byte commitment and four 4-byte AND outputs,
    # plus the input share of player 2 in about two rounds out of three.
    assert 219 * 80 < signature_size(sig) < 219 * 84 + 55
