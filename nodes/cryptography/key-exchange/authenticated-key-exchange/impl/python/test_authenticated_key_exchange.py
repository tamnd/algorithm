# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/authenticated-key-exchange/. The authors are listed in prov/NYN6YJ.jsonl.

import os
import random

from authenticated_key_exchange import (
    G,
    P,
    Q,
    Session,
    is_group_element,
    keygen,
    plain_dh_key,
    run,
    sign,
    verify,
)


def miller_rabin(n: int, rounds: int = 32) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    rng = random.Random(7)
    for _ in range(rounds):
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


class Rng:
    """A seeded stand-in for secrets.SystemRandom, so that the runs repeat."""

    def __init__(self, seed: int):
        self.r = random.Random(seed)

    def randrange(self, a: int, b: int) -> int:
        return self.r.randrange(a, b)


def make_world(seed: int = 1):
    rng = Rng(seed)
    keys = {name: keygen(rng) for name in ("alice", "bob", "eve")}
    directory = {name: pk for name, (_, pk) in keys.items()}
    return rng, keys, directory


def test_group_is_a_safe_prime_group() -> None:
    assert miller_rabin(P) and miller_rabin(Q) and P == 2 * Q + 1
    assert pow(G, Q, P) == 1 and G != 1
    assert not is_group_element(P - 1)  # order 2, outside the subgroup
    assert not is_group_element(1)


def test_schnorr_signature_verifies_and_rejects_changes() -> None:
    rng, keys, _ = make_world(2)
    sk, pk = keys["alice"]
    sig = sign(sk, b"hello")
    assert verify(pk, b"hello", sig)
    assert not verify(pk, b"hellp", sig)
    assert not verify(keys["bob"][1], b"hello", sig)
    assert not verify(pk, b"hello", (sig[0], (sig[1] + 1) % Q))


def test_honest_run_gives_partnered_sessions_with_one_key() -> None:
    rng, keys, directory = make_world(3)
    a = Session("alice", keys["alice"][0], directory, "initiator", rng)
    b = Session("bob", keys["bob"][0], directory, "responder", rng)
    run(a, b, "bob")
    assert a.state == b.state == "accepted"
    assert a.peer == "bob" and b.peer == "alice"
    assert a.sid == b.sid and a.sid[0] == "alice" and a.sid[1] == "bob"
    assert a.key == b.key and len(a.key) == 32
    assert a._x == 0 and b._x == 0  # ephemeral exponents are erased


def test_two_runs_give_independent_keys() -> None:
    rng, keys, directory = make_world(4)
    seen = set()
    for _ in range(5):
        a = Session("alice", keys["alice"][0], directory, "initiator", rng)
        b = Session("bob", keys["bob"][0], directory, "responder", rng)
        run(a, b, "bob")
        assert a.key == b.key
        seen.add(a.key)
    assert len(seen) == 5


def test_man_in_the_middle_who_swaps_y_makes_alice_reject() -> None:
    rng, keys, directory = make_world(5)
    a = Session("alice", keys["alice"][0], directory, "initiator", rng)
    b = Session("bob", keys["bob"][0], directory, "responder", rng)
    m1 = a.start("bob")
    _, y_pub, sig = b.respond(m1)
    e = rng.randrange(1, Q)
    assert a.finish(("bob", pow(G, e, P), sig)) is None
    assert a.state == "rejected" and a.key is None


def test_replay_of_an_old_m2_is_rejected() -> None:
    rng, keys, directory = make_world(6)
    a1 = Session("alice", keys["alice"][0], directory, "initiator", rng)
    b1 = Session("bob", keys["bob"][0], directory, "responder", rng)
    old_m2 = b1.respond(a1.start("bob"))
    a2 = Session("alice", keys["alice"][0], directory, "initiator", rng)
    a2.start("bob")
    assert a2.finish(old_m2) is None and a2.state == "rejected"


def test_m3_from_a_wrong_signer_is_rejected() -> None:
    rng, keys, directory = make_world(7)
    a = Session("alice", keys["alice"][0], directory, "initiator", rng)
    b = Session("bob", keys["bob"][0], directory, "responder", rng)
    m2 = b.respond(a.start("bob"))
    a.finish(m2)
    # Eve signs the m3 text with her own key and sends it in place of Alice's m3.
    forged = (sign(keys["eve"][0], b"m3" + b.__dict__["_y_pub"].to_bytes(32, "big") + b.__dict__["_x_pub"].to_bytes(32, "big") + b"bob"),)
    assert b.complete(forged) is False and b.state == "rejected"


def test_invalid_group_element_is_rejected() -> None:
    rng, keys, directory = make_world(8)
    b = Session("bob", keys["bob"][0], directory, "responder", rng)
    assert b.respond(("alice", P - 1)) is None and b.state == "rejected"


def test_the_test_game_breaks_plain_dh_but_not_signed_dh() -> None:
    """The Test query of Bellare and Rogaway: return the real key or a random one; the adversary guesses which.

    Against plain DH, an adversary in the middle substitutes its own value, knows the
    key of Alice's session (which has no partner), and wins every time. Against the
    signed protocol, the same substitution makes Alice reject, so there is no fresh
    accepted session to test.
    """
    rng, keys, directory = make_world(9)
    coin = random.Random(10)
    wins = 0
    trials = 20
    for _ in range(trials):
        x = rng.randrange(1, Q)
        x_pub = pow(G, x, P)
        e = rng.randrange(1, Q)
        e_pub = pow(G, e, P)  # the adversary's value, sent to Alice as "Bob's Y"
        alice_key = plain_dh_key(x_pub, e_pub, pow(e_pub, x, P))
        b = coin.randrange(2)
        challenge = alice_key if b == 1 else os.urandom(32)
        guess = 1 if challenge == plain_dh_key(x_pub, e_pub, pow(x_pub, e, P)) else 0
        wins += guess == b
    assert wins == trials  # advantage 1

    a = Session("alice", keys["alice"][0], directory, "initiator", rng)
    b_sess = Session("bob", keys["bob"][0], directory, "responder", rng)
    m1 = a.start("bob")
    _, _, sig = b_sess.respond(m1)
    assert a.finish(("bob", pow(G, 12345, P), sig)) is None and a.key is None


def test_random_runs_agree() -> None:
    for seed in range(20, 40):
        rng, keys, directory = make_world(seed)
        a = Session("alice", keys["alice"][0], directory, "initiator", rng)
        b = Session("bob", keys["bob"][0], directory, "responder", rng)
        run(a, b, "bob")
        assert a.key == b.key and a.sid == b.sid
