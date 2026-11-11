# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/opaque/. The authors are listed in prov/4VXR26.jsonl.
#
# The code is a simplified OPAQUE, so the RFC 9807 test vectors are not used.
# These tests check registration, login, a wrong password, and what a server
# compromise gives the attacker.

import hashlib
import random

import pytest

from opaque import (
    P,
    OpaqueError,
    Server,
    expand,
    extract,
    hash_to_group,
    in_group,
    ksf,
    login,
    register,
)


def seeded(seed: int):
    r = random.Random(seed)
    return lambda n: r.randrange(n)


def test_hash_to_group_lands_in_the_subgroup():
    for w in (b"", b"a", b"password"):
        assert in_group(hash_to_group(w))


def test_registration_then_login():
    rng = seeded(1)
    server = Server(rng=rng)
    export_reg = register(server, b"cred-1", b"alice", b"tr0ub4dor", rng)
    k_client, k_server, export_login = login(server, b"cred-1", b"alice", b"tr0ub4dor", rng)
    assert k_client == k_server and len(k_client) == 32
    assert export_login == export_reg


def test_wrong_password_aborts_on_the_client():
    rng = seeded(2)
    server = Server(rng=rng)
    register(server, b"cred-1", b"alice", b"tr0ub4dor", rng)
    with pytest.raises(OpaqueError):
        login(server, b"cred-1", b"alice", b"tr0ub4dor&3", rng)


def test_wrong_client_identity_aborts():
    rng = seeded(3)
    server = Server(rng=rng)
    register(server, b"cred-1", b"alice", b"pw", rng)
    with pytest.raises(OpaqueError):
        login(server, b"cred-1", b"mallory", b"pw", rng)


def test_no_precomputation_before_compromise():
    # The same password at two servers gives unrelated records: the OPRF key is
    # a per-server secret, so a table built in advance from a dictionary matches nothing.
    rng = seeded(4)
    s1, s2 = Server(rng=rng), Server(rng=rng)
    register(s1, b"cred", b"alice", b"123456", rng)
    register(s2, b"cred", b"alice", b"123456", rng)
    r1, r2 = s1.records[b"cred"], s2.records[b"cred"]
    assert r1["masking_key"] != r2["masking_key"] and r1["pk_u"] != r2["pk_u"]
    table = {hashlib.sha256(w).digest() for w in (b"123456", b"password", b"qwerty")}
    assert r1["masking_key"] not in table


def test_after_compromise_each_guess_costs_an_exponentiation():
    # With the record and the OPRF key, the attacker can test guesses offline, one
    # exponentiation (and in practice one slow KSF call) per guess.
    rng = seeded(5)
    server = Server(rng=rng)
    register(server, b"cred", b"alice", b"dragon", rng)
    rec, k = server.records[b"cred"], server.oprf_key(b"cred")
    found = None
    for guess in (b"123456", b"password", b"qwerty", b"dragon", b"letmein"):
        n = pow(hash_to_group(guess), k, P)
        y = hashlib.sha256(len(guess).to_bytes(2, "big") + guess + n.to_bytes(128, "big") + b"Finalize").digest()
        if expand(extract(b"", y + ksf(y)), b"MaskingKey") == rec["masking_key"]:
            found = guess
    assert found == b"dragon"
