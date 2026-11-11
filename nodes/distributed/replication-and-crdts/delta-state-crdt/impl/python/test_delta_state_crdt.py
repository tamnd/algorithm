# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-state-crdt/. The authors are listed in prov/QRFZEK.jsonl.

import random

from delta_state_crdt import G_COUNTER, G_SET, full_mutator, join_all, optimal_delta, run


def _random_state(lat, rng: random.Random):
    x = lat.bottom()
    for _ in range(rng.randint(0, 6)):
        x = lat.join(x, lat.delta_mutator(x, rng.randrange(3), rng))
    return x


def test_delta_mutator_is_a_decomposition_of_the_mutator() -> None:
    # m(X) = X join m^delta(X), and the delta is much smaller than the state.
    for lat in (G_COUNTER, G_SET):
        for seed in range(250):
            x = _random_state(lat, random.Random(seed))
            i = seed % 3
            d = lat.delta_mutator(x, i, random.Random(seed + 7))
            m = full_mutator(lat, x, i, random.Random(seed + 7))
            assert lat.join(x, d) == m
            assert len(lat.encode(d)) <= max(len(lat.encode(m)), 1)


def test_optimal_delta_is_correct_and_minimal() -> None:
    rng = random.Random(77)
    for lat in (G_COUNTER, G_SET):
        for _ in range(250):
            a, b = _random_state(lat, rng), _random_state(lat, rng)
            d = optimal_delta(lat, a, b)
            assert lat.join(b, d) == lat.join(a, b)
            assert lat.leq(d, a)
            parts = lat.decompose(d)
            for k in range(len(parts)):  # dropping any part breaks the equation
                rest = join_all(lat, parts[:k] + parts[k + 1:])
                assert lat.join(b, rest) != lat.join(a, b)


def test_algorithm_2_reaches_the_states_of_the_full_state_crdt() -> None:
    # Loss, duplication, reordering and crashes. Every state, at every step,
    # is the join of the full states right after the updates it reflects, and
    # every delta-interval is joined only into a state above its start.
    rng = random.Random(2016)
    for case in range(500):
        lat = G_COUNTER if case % 2 else G_SET
        opts = case % 4 >= 2
        s = run(lat, rng, rng.randint(1, 4), rng.randint(0, 50), p_crash=0.05,
                avoid_back_propagation=opts, remove_redundant=opts)
        assert s.invariant_ok and s.merging_ok
        assert all(x == s.model for x in s.states)


def test_values_match_a_model() -> None:
    rng = random.Random(9)
    for _ in range(100):
        s = run(G_COUNTER, rng, 3, 60)
        updates = sum(s.model.values())
        assert all(sum(x.values()) == updates for x in s.states)


def test_crash_falls_back_to_the_full_state() -> None:
    rng = random.Random(4)
    full_msgs = 0
    for _ in range(30):
        s = run(G_SET, rng, 3, 60, p_crash=0.2)
        assert s.invariant_ok and s.merging_ok and all(x == s.model for x in s.states)
        full_msgs += s.full_messages
    assert full_msgs > 0


def test_ignoring_acks_breaks_causal_merging() -> None:
    rng = random.Random(5)
    broken = 0
    for _ in range(100):
        s = run(G_SET, rng, 3, 40, latest_only=True)
        broken += not (s.invariant_ok and s.merging_ok)
    assert broken > 0


def test_deltas_send_fewer_bytes_than_full_states_for_a_set() -> None:
    # Bytes are measured on the encoded messages, acks included, and compared
    # with full-state messages over the same sends.
    rng = random.Random(1)
    sent = full = 0
    for _ in range(5):
        s = run(G_SET, rng, 4, 150, avoid_back_propagation=True, remove_redundant=True)
        sent += s.bytes_sent
        full += s.full_state_bytes
    assert sent < full / 2
    # Without loss, plain Algorithm 2 also sends fewer bytes.
    rng = random.Random(1)
    sent = full = 0
    for _ in range(5):
        s = run(G_SET, rng, 3, 150, p_loss=0, p_dup=0, p_crash=0)
        sent += s.bytes_sent
        full += s.full_state_bytes
    assert sent < full
