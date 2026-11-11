# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/station-to-station-protocol/. The authors are listed in prov/NT8D3J.jsonl.

import random

from station_to_station_protocol import G, P, Q, Initiator, Responder, e_k, keygen, run, sign, verify


def miller_rabin(n: int) -> bool:
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    rng = random.Random(0)
    for _ in range(24):
        x = pow(rng.randrange(2, n - 1), d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def parties(seed: int):
    rng = random.Random(seed)
    (a, a_pub), (b, b_pub) = keygen(rng), keygen(rng)
    directory = {"A": a_pub, "B": b_pub}
    return rng, a, b, directory, Initiator("A", a, directory, rng), Responder("B", b, directory, rng)


def test_group_and_signature() -> None:
    assert miller_rabin(P) and miller_rabin(Q) and pow(G, Q, P) == 1
    sk, pk = keygen(random.Random(1))
    sig = sign(sk, b"msg")
    assert verify(pk, b"msg", sig) and not verify(pk, b"msh", sig)
    assert not verify(pk, b"msg", sig[:32] + bytes(32))


def test_small_example_numbers() -> None:
    p, g, x, y = 2039, 4, 57, 311
    assert (pow(g, x, p), pow(g, y, p)) == (1556, 1502)
    assert pow(1502, x, p) == pow(1556, y, p) == 661


def test_honest_runs_agree() -> None:
    for seed in range(10):
        _, _, _, _, a, b = parties(seed)
        res_a, res_b = run(a, b)
        assert res_a == (res_b[0], "B") and res_b[1] == "A"
        assert a.x == 0  # the initiator erased x


def test_man_in_the_middle_is_caught() -> None:
    rng, _, _, _, a, b = parties(20)
    name, x_pub = a.start()
    e = rng.randrange(1, Q)
    m2 = b.reply((name, pow(G, e, P)))  # Eve replaces X by her own value
    assert a.finish(m2) is None  # B signed (Y, E), not (Y, X)
    # Eve replaces Y in m2: A's key changes, decryption gives garbage, the signature fails.
    _, _, _, _, a, b = parties(21)
    m2 = b.reply(a.start())
    assert a.finish((m2[0], pow(G, e, P), m2[2])) is None


def test_replayed_m2_is_rejected() -> None:
    _, _, _, _, a, b = parties(30)
    old_m2 = b.reply(a.start())
    _, _, _, d2, a2, _ = parties(30)
    a2.rng = random.Random(999)  # a new run with a new x
    a2.start()
    assert a2.finish(old_m2) is None


def test_m3_by_the_wrong_key_is_rejected() -> None:
    rng, _, _, directory, a, b = parties(40)
    m2 = b.reply(a.start())
    m3, (key, _) = a.finish(m2)
    forged = e_k(key, b"m3", sign(rng.randrange(1, Q), bytes(64)))
    assert b.finish(forged) is None
    assert b.finish(m3) == (key, "A")


def test_unknown_key_share_by_public_key_substitution() -> None:
    """Blake-Wilson and Menezes (1999): Eve registers A's public key as 'E' and swaps the certificate in m3."""
    _, _, _, directory, a, b = parties(50)
    directory["E"] = directory["A"]  # a CA with no proof of possession
    m2 = b.reply(a.start())
    m3, res_a = a.finish(m2)
    res_b = b.finish(m3, claimed_peer="E")
    assert res_a == (res_b[0], "B") and res_b[1] == "E"  # same key; B thinks the peer is E
