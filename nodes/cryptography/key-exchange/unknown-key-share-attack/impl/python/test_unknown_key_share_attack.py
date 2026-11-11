# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unknown-key-share-attack/. The authors are listed in prov/BECMKR.jsonl.

import random

from unknown_key_share_attack import CA, G, P, Q, is_uks, run, sign


def setup(check_pop: bool, rng: random.Random):
    a, b = rng.randrange(1, Q), rng.randrange(1, Q)
    ca = CA(check_pop)
    assert ca.register("A", pow(G, a, P), sign(a, b"popA"))
    assert ca.register("B", pow(G, b, P), sign(b, b"popB"))
    # Eve tries to register Alice's public key under her own name. She has no a, so no proof of possession.
    registered = ca.register("E", pow(G, a, P), None)
    return ca, {"A": a, "B": b}, registered


def test_honest_run_agrees() -> None:
    rng = random.Random(1)
    ca, keys, _ = setup(False, rng)
    alice, bob = run(ca, keys, rng.randrange(1, Q), rng.randrange(1, Q), attack=False)
    assert alice[0] == "B" and bob[0] == "A" and alice[1] == bob[1]


def test_uks_on_sign_only_protocol() -> None:
    rng = random.Random(2)
    for _ in range(5):
        ca, keys, registered = setup(False, rng)
        assert registered
        alice, bob = run(ca, keys, rng.randrange(1, Q), rng.randrange(1, Q), attack=True)
        assert is_uks(alice, bob) and bob[0] == "E"


def test_fix_proof_of_possession() -> None:
    rng = random.Random(3)
    ca, keys, registered = setup(True, rng)
    assert not registered
    alice, bob = run(ca, keys, rng.randrange(1, Q), rng.randrange(1, Q), attack=True)
    assert bob is None and not is_uks(alice, bob)


def test_fix_identities_in_kdf() -> None:
    rng = random.Random(4)
    ca, keys, _ = setup(False, rng)
    alice, bob = run(ca, keys, rng.randrange(1, Q), rng.randrange(1, Q), attack=True, ids_in_kdf=True)
    # Bob still accepts "with E", but the keys now differ: the session fails instead of a silent UKS.
    assert bob[0] == "E" and alice[1] != bob[1] and not is_uks(alice, bob)


def test_fix_sigma_mac_over_own_identity() -> None:
    rng = random.Random(5)
    for _ in range(5):
        ca, keys, _ = setup(False, rng)
        x, y = rng.randrange(1, Q), rng.randrange(1, Q)
        alice, bob = run(ca, keys, x, y, attack=False, mac_identity=True)
        assert bob == ("A", alice[1])
        alice, bob = run(ca, keys, x, y, attack=True, mac_identity=True)
        assert bob is None  # the MAC was over "A", Bob checks it over "E"
