# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/malicious-adversary-model/. The authors are listed in prov/EASH3X.jsonl.
# There are no official test vectors for these protocols. The attack runs on
# toy fields against local simulated parties.

import random

from malicious_adversary_model import P61, Cheat, check_opening, commit, mac_sum, plain_sum, plain_sum_split_view


def test_honest_runs_are_correct() -> None:
    rng = random.Random(2012)
    for _ in range(500):
        n = rng.randrange(2, 7)
        xs = [rng.randrange(P61) for _ in range(n)]
        assert plain_sum(xs, P61, rng) == sum(xs) % P61
        assert mac_sum(xs, P61, rng) == sum(xs) % P61


def test_malicious_share_changes_plain_sum_undetected() -> None:
    rng = random.Random(5)
    xs = [52, 61, 47]
    out = plain_sum(xs, P61, rng, Cheat(party=2, error=1000))
    # The honest parties output 1160 instead of 160, and the protocol has no
    # step at which they could notice.
    assert out == 1160


def test_rushing_party_forces_any_output() -> None:
    # A fixed shift is no worse than a changed input for a sum. Forcing the
    # output to 0 whatever the honest inputs are is not possible in the ideal
    # world, where the cheater must fix its input before it sees anything.
    rng = random.Random(10)
    for _ in range(50):
        xs = [rng.randrange(P61) for _ in range(4)]
        assert plain_sum(xs, P61, rng, Cheat(party=3, target=0)) == 0


def test_without_broadcast_honest_parties_disagree() -> None:
    rng = random.Random(11)
    outs = plain_sum_split_view([52, 61, 47], P61, rng, party=2, errors=[0, 5, 0])
    assert outs == [160, 165, 160]


def test_mac_check_catches_the_same_attacks() -> None:
    rng = random.Random(6)
    xs = [52, 61, 47]
    for e in (1, 1000, P61 - 1):
        for party in range(3):
            assert mac_sum(xs, P61, rng, Cheat(party=party, error=e)) is None
    for party in range(3):
        assert mac_sum(xs, P61, rng, Cheat(party=party, target=0)) is None


def test_escape_probability_is_about_one_over_p() -> None:
    # Toy field p = 101: a cheater who guesses its MAC correction passes with
    # probability exactly 1/p, over the dealer's random alpha.
    p = 101
    rng = random.Random(7)
    trials = 30000
    passed = 0
    for _ in range(trials):
        shift = rng.randrange(p)
        if mac_sum([3, 4, 5], p, rng, Cheat(party=1, error=17, mac_shift=shift)) is not None:
            passed += 1
    expected = trials / p  # about 297
    assert abs(passed - expected) < 5 * (expected ** 0.5)


def test_without_commitments_a_rushing_party_always_passes() -> None:
    rng = random.Random(8)
    xs = [52, 61, 47]
    out = mac_sum(xs, P61, rng, Cheat(party=2, error=1000, rushing=True), use_commitments=False)
    assert out == 1160
    # With commitments the same party must fix sigma before it sees the others.
    assert mac_sum(xs, P61, rng, Cheat(party=2, error=1000, rushing=True)) is None


def test_commitment_opens_only_to_its_value() -> None:
    rng = random.Random(9)
    c, nonce = commit(42, rng)
    assert check_opening(c, 42, nonce)
    assert not check_opening(c, 43, nonce)
