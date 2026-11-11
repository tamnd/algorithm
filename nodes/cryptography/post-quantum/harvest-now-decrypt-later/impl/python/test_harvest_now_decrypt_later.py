# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harvest-now-decrypt-later/. The authors are listed in prov/5T7EBA.jsonl.

import random

from harvest_now_decrypt_later import (
    G_DH,
    P_DH,
    Q_DH,
    Recorder,
    Server,
    exposed_window,
    latest_start,
    mosca,
    quantum_dlog,
    quantum_factor,
    session_ephemeral_dh,
    session_rsa_transport,
)


def test_mosca_inequality():
    assert mosca(10, 5, 12)
    assert not mosca(5, 5, 15)
    assert not mosca(5, 5, 10)  # equality: the last data expires as the threat arrives


def test_exposed_window():
    assert exposed_window(10, 5, 12) == (2.0, 5.0)
    assert exposed_window(25, 8, 15) == (0.0, 8.0)  # data from today is already exposed
    assert exposed_window(5, 5, 15) is None
    assert latest_start(10, 5, 12) == -3
    assert latest_start(5, 5, 15) == 5


def test_window_matches_inequality():
    rng = random.Random(1)
    for _ in range(500):
        x, y, z = rng.randint(0, 30), rng.randint(1, 15), rng.randint(1, 30)
        assert (exposed_window(x, y, z) is not None) == mosca(x, y, z)


def test_quantum_stand_ins():
    server = Server()
    f = quantum_factor(server.n)
    assert 1 < f < server.n and server.n % f == 0
    rng = random.Random(2)
    for _ in range(3):
        x = rng.randrange(1, Q_DH)
        assert quantum_dlog(pow(G_DH, x, P_DH)) == x


def _record_sessions(server, kind, count, seed):
    rng = random.Random(seed)
    adversary = Recorder()
    messages = [f"secret {kind} {i}".encode() for i in range(count)]
    session = session_rsa_transport if kind == "rsa" else session_ephemeral_dh
    for i, m in enumerate(messages):
        t = session(server, m, rng, i.to_bytes(4, "big"))
        assert t.ciphertext != m
        adversary.record(t)
    return adversary, messages


def test_nothing_is_exposed_today():
    server = Server()
    for kind in ("rsa", "dh"):
        adversary, _ = _record_sessions(server, kind, 4, 3)
        assert adversary.exposed(server) == []


def test_key_leak_exposes_static_rsa_transport():
    server = Server()
    adversary, messages = _record_sessions(server, "rsa", 5, 4)
    adversary.leak_long_term_key(server)
    assert adversary.exposed(server) == messages


def test_key_leak_does_not_expose_ephemeral_dh():
    server = Server()
    adversary, _ = _record_sessions(server, "dh", 5, 5)
    adversary.leak_long_term_key(server)
    assert adversary.exposed(server) == []


def test_quantum_computer_exposes_both():
    server = Server()
    for kind, seed in (("rsa", 6), ("dh", 7)):
        adversary, messages = _record_sessions(server, kind, 3, seed)
        adversary.get_quantum_computer(server)
        assert adversary.exposed(server) == messages
