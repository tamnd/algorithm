# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rsa-fault-attack/. The authors are listed in prov/YCAWG0.jsonl.

import random

from rsa_fault_attack import (
    CrtKey,
    bellcore_attack,
    garner,
    lenstra_difference_attack,
    sign_crt,
    sign_crt_shamir,
    sign_crt_verified,
    sign_plain,
)

# A toy key with two 128 binary digit primes. No real key is this small.
P = 273864138845241657029075268143536711069
Q = 173710947069375085680776429514357002701
KEY = CrtKey(p=P, q=Q, e=65537)
MESSAGE = 0x6661756c7420617474616320746f79206d657373616765  # "fault attac toy message"
SMALL_PRIME = 2147483647  # a Mersenne prime, the r of Shamir's trick


def test_the_crt_signature_is_the_plain_signature() -> None:
    assert KEY.n == P * Q
    assert sign_crt(KEY, MESSAGE) == sign_plain(KEY, MESSAGE)
    assert pow(sign_crt(KEY, MESSAGE), KEY.e, KEY.n) == MESSAGE
    assert garner(KEY, MESSAGE % P, MESSAGE % Q) == MESSAGE


def test_one_faulty_signature_gives_the_factors() -> None:
    """The Bellcore attack with the improvement of Lenstra."""
    faulty = sign_crt(KEY, MESSAGE, fault_in="p", fault_mask=1)
    found = bellcore_attack(KEY.n, KEY.e, MESSAGE, faulty)
    assert found is not None
    recovered, other, d = found
    # The fault was in the half modulo p, so the half modulo q was correct,
    # and the gcd gives q.
    assert recovered == Q and other == P
    assert pow(MESSAGE, d, KEY.n) == sign_plain(KEY, MESSAGE)


def test_the_attack_works_for_random_faults_in_either_half() -> None:
    rnd = random.Random(20251111)
    for _ in range(20):
        message = rnd.randrange(2, KEY.n)
        half = rnd.choice(["p", "q"])
        mask = 1 << rnd.randrange(0, 120)  # one flipped bit, anywhere in the half
        faulty = sign_crt(KEY, message, fault_in=half, fault_mask=mask)
        found = bellcore_attack(KEY.n, KEY.e, message, faulty)
        assert found is not None
        assert {found[0], found[1]} == {P, Q}
        assert found[0] == (Q if half == "p" else P)


def test_the_difference_form_needs_the_correct_signature_too() -> None:
    correct = sign_crt(KEY, MESSAGE)
    faulty = sign_crt(KEY, MESSAGE, fault_in="q", fault_mask=1 << 7)
    assert lenstra_difference_attack(KEY.n, correct, faulty) == (P, Q)
    assert lenstra_difference_attack(KEY.n, correct, correct) is None


def test_a_correct_signature_leaks_nothing() -> None:
    good = sign_crt(KEY, MESSAGE)
    assert bellcore_attack(KEY.n, KEY.e, MESSAGE, good) is None


def test_a_fault_in_both_halves_leaks_nothing() -> None:
    """The equation needs one half to be right. Two faults break it."""
    faulty = sign_crt(KEY, MESSAGE, fault_in="both", fault_mask=1)
    assert bellcore_attack(KEY.n, KEY.e, MESSAGE, faulty) is None


def test_verifying_before_output_blocks_the_attack() -> None:
    """The first countermeasure: the faulty value never leaves the device."""
    assert sign_crt_verified(KEY, MESSAGE) == sign_plain(KEY, MESSAGE)
    for half in ("p", "q", "both"):
        assert sign_crt_verified(KEY, MESSAGE, fault_in=half, fault_mask=1 << 3) is None


def test_shamirs_trick_catches_the_fault_without_the_public_exponent() -> None:
    """The second countermeasure: the two halves must agree modulo r."""
    assert sign_crt_shamir(KEY, MESSAGE, SMALL_PRIME) == sign_plain(KEY, MESSAGE)
    for half in ("p", "q"):
        assert sign_crt_shamir(KEY, MESSAGE, SMALL_PRIME, fault_in=half,
                               fault_mask=1 << 5) is None


def test_the_attacker_uses_public_data_only() -> None:
    import inspect

    import rsa_fault_attack
    source = inspect.getsource(rsa_fault_attack.bellcore_attack)
    for secret in ("key.d", "d_p", "d_q", "key.p", "key.q"):
        assert secret not in source
