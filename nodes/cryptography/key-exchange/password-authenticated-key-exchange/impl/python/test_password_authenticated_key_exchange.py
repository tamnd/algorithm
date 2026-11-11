# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/password-authenticated-key-exchange/. The authors are listed in prov/EJCGN9.jsonl.

import random

from password_authenticated_key_exchange import (
    ExponentClient,
    active_attack_on_exponent,
    honest_exponent_run,
    mac_protocol,
    passive_attack_on_mac,
)

DICTIONARY = [b"pass%04d" % i for i in range(2000)] + [b"letmein", b"sunshine", b"dragon"]


def seeded(seed: int):
    r = random.Random(seed)
    return lambda n: r.randrange(n)


def test_passive_attacker_recovers_password_from_one_mac_transcript():
    seen = mac_protocol(b"sunshine", seeded(1))
    assert passive_attack_on_mac(seen, DICTIONARY) == [b"sunshine"]


def test_exponent_protocol_works_for_honest_parties():
    assert honest_exponent_run(b"dragon", b"dragon", seeded(2))
    assert not honest_exponent_run(b"dragon", b"dragon!", seeded(3))


def test_one_active_run_recovers_password_from_exponent_protocol():
    client = ExponentClient(b"pass1234", seeded(4))
    assert active_attack_on_exponent(DICTIONARY, client, seeded(5)) == [b"pass1234"]


def test_password_outside_the_dictionary_is_not_found():
    seen = mac_protocol(b"a long passphrase nobody guesses", seeded(6))
    assert passive_attack_on_mac(seen, DICTIONARY) == []
