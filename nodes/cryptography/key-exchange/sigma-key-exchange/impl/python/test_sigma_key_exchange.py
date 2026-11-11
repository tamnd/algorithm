# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sigma-key-exchange/. The authors are listed in prov/7AWQRY.jsonl.

import random

from sigma_key_exchange import G, P, Q, Party, keygen, misbind_m3, run, unlp


def world(seed: int, **flags):
    rng = random.Random(seed)
    keys = {n: keygen(rng) for n in ("A", "B", "E")}
    directory = {n: pk for n, (_, pk) in keys.items()}  # Eve is a registered user with her own key
    a = Party("A", keys["A"][0], directory, rng, **flags)
    b = Party("B", keys["B"][0], directory, rng, **flags)
    return rng, keys, a, b


def test_sigma_i_honest_runs() -> None:
    for seed in range(8):
        _, _, a, b = world(seed)
        res_a, res_b = run(a, b)
        assert res_a[1] == "B" and res_b[1] == "A" and res_a[0] == res_b[0]
        ke, km, ks = a.keys
        assert len({ke, km, ks}) == 3 and res_a[0] == ks
        assert a.e == 0  # x erased


def test_basic_sigma_without_encryption_also_agrees() -> None:
    _, _, a, b = world(9, encrypt=False)
    res_a, res_b = run(a, b)
    assert res_a == (res_b[0], "B") and res_b[1] == "A"


def test_mitm_value_swap_is_rejected() -> None:
    rng, _, a, b = world(10)
    s, _ = a.start()
    m2 = b.reply((s, pow(G, rng.randrange(1, Q), P)))  # Eve swapped X
    assert a.finish(m2) is None


def test_sign_only_falls_to_identity_misbinding() -> None:
    _, keys, a, b = world(11, encrypt=False, use_mac=False)
    m2 = b.reply(a.start())
    m3, res_a = a.finish(m2)
    forged = misbind_m3(m3, "E", keys["E"][0], a.x_pub, a.y_pub)
    res_b = b.complete(forged)
    # A: key with B. B: same key, but with E. Eve does not know the key.
    assert res_a[1] == "B" and res_b[1] == "E" and res_a[0] == res_b[0]


def test_mac_over_own_identity_stops_the_misbinding() -> None:
    _, keys, a, b = world(12, encrypt=False, use_mac=True)
    m2 = b.reply(a.start())
    m3, _ = a.finish(m2)
    tag_a = unlp(m3[1])[2]
    for tag in (b"", tag_a, bytes(32)):
        assert b.complete(misbind_m3(m3, "E", keys["E"][0], a.x_pub, a.y_pub, tag)) is None
    assert b.complete(m3)[1] == "A"


def test_sigma_i_ciphertext_cannot_be_relabelled() -> None:
    _, keys, a, b = world(13)
    m2 = b.reply(a.start())
    m3, _ = a.finish(m2)
    assert b.complete(misbind_m3(m3, "E", keys["E"][0], a.x_pub, a.y_pub)) is None
    flipped = (m3[0], bytes([m3[1][0] ^ 1]) + m3[1][1:])
    assert b.complete(flipped) is None
