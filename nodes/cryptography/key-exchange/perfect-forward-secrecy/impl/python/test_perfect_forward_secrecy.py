# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perfect-forward-secrecy/. The authors are listed in prov/8KQ7AG.jsonl.

import random

from perfect_forward_secrecy import (
    G,
    P,
    Q,
    RSA_D,
    RSA_E,
    RSA_N,
    RSA_P,
    RSA_Q,
    attack_active_then_corrupt,
    attack_ephemeral_dh,
    attack_rsa_transport,
    attack_ticket_key,
    attack_with_unerased_ephemeral,
    ephemeral_dh_handshake,
    implicit_initiator,
    implicit_responder,
    issue_ticket,
    resumed_key_psk_only,
    rsa_transport_handshake,
    stream_xor,
)

SECRET = b"the wire transfer code is 0451; meet at noon"


def miller_rabin(n: int, rounds: int = 32) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    rng = random.Random(3)
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


def test_toy_parameters() -> None:
    assert miller_rabin(P) and miller_rabin(Q) and P == 2 * Q + 1 and pow(G, Q, P) == 1
    assert miller_rabin(RSA_P) and miller_rabin(RSA_Q) and RSA_N.bit_length() == 1023
    assert RSA_E * RSA_D % ((RSA_P - 1) * (RSA_Q - 1)) == 1


def test_rsa_key_transport_opens_after_the_long_term_key_leaks() -> None:
    rng = random.Random(1)
    nc, ns = rng.randbytes(16), rng.randbytes(16)
    transcript, key = rsa_transport_handshake(nc, ns, rng.randbytes(32))
    record = stream_xor(key, nc, SECRET)
    assert record != SECRET
    # Years later, the server's private key leaks.
    assert attack_rsa_transport(transcript, record, RSA_D) == SECRET


def test_ephemeral_dh_stays_closed_after_the_long_term_key_leaks() -> None:
    rng = random.Random(2)
    nc, ns = rng.randbytes(16), rng.randbytes(16)
    x, y = rng.randrange(1, Q), rng.randrange(1, Q)
    transcript, key = ephemeral_dh_handshake(nc, ns, x, y)
    record = stream_xor(key, nc, SECRET)
    assert attack_ephemeral_dh(transcript, record, RSA_D) != SECRET
    # The same session opens if the ephemeral secret was not erased and leaks.
    assert attack_with_unerased_ephemeral(transcript, record, x) == SECRET


def test_many_sessions() -> None:
    rng = random.Random(3)
    for _ in range(10):
        nc, ns = rng.randbytes(16), rng.randbytes(16)
        t1, k1 = rsa_transport_handshake(nc, ns, rng.randbytes(32))
        t2, k2 = ephemeral_dh_handshake(nc, ns, rng.randrange(1, Q), rng.randrange(1, Q))
        msg = rng.randbytes(40)
        assert attack_rsa_transport(t1, stream_xor(k1, nc, msg), RSA_D) == msg
        assert attack_ephemeral_dh(t2, stream_xor(k2, nc, msg), RSA_D) != msg


def test_two_message_implicit_protocol_has_weak_pfs_only() -> None:
    rng = random.Random(4)
    a, b = rng.randrange(1, Q), rng.randrange(1, Q)
    a_pub, b_pub = pow(G, a, P), pow(G, b, P)
    # Honest run: both sides agree.
    x, y = rng.randrange(1, Q), rng.randrange(1, Q)
    y_pub, kb = implicit_responder(b, a_pub, pow(G, x, P), y)
    assert implicit_initiator(a, b_pub, x, y_pub) == kb
    # Passive case (weak PFS): after a leaks, the recorder knows a, X and Y but not x.
    # The attack needs x; with any other value in its place it gets a wrong key.
    for wrong_x in (1, 2, x + 1):
        assert attack_active_then_corrupt(wrong_x, y_pub, b_pub, a) != kb
    assert attack_active_then_corrupt(x, y_pub, b_pub, a) == kb  # only the real x opens it
    # Active case: the attacker picks x itself and sends X to B as if it came from A.
    x_att = rng.randrange(1, Q)
    y_pub2, kb2 = implicit_responder(b, a_pub, pow(G, x_att, P), rng.randrange(1, Q))
    # B accepts a session "with A". Later A's long-term key leaks; the session opens.
    assert attack_active_then_corrupt(x_att, y_pub2, b_pub, a) == kb2


def test_ticket_key_leak_opens_psk_only_resumptions() -> None:
    rng = random.Random(5)
    stek = rng.randbytes(32)
    rs = rng.randbytes(32)
    tn = rng.randbytes(16)
    ticket = issue_ticket(stek, tn, rs)  # sent to the client in the clear part of the old session
    nc, ns = rng.randbytes(16), rng.randbytes(16)
    record = stream_xor(resumed_key_psk_only(rs, nc, ns), nc, SECRET)
    assert attack_ticket_key(ticket, tn, nc, ns, record, stek) == SECRET
    assert attack_ticket_key(ticket, tn, nc, ns, record, rng.randbytes(32)) != SECRET
