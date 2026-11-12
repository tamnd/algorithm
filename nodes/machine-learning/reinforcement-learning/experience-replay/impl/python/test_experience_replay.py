# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/experience-replay/. The authors are listed in prov/05WE42.jsonl.

import random

import pytest

from experience_replay import ReplayBuffer, collect, replay_q_learning


def test_overwrite_order():
    buf = ReplayBuffer(4)
    for t in range(1, 8):
        buf.add(t)
    # Seven adds into four slots: slots hold 5 6 7 4, the oldest is 4.
    assert buf.data == [5, 6, 7, 4]
    assert buf.in_order() == [4, 5, 6, 7]
    assert len(buf) == 4
    assert buf.next == 3


def test_partial_fill_and_capacity_one():
    buf = ReplayBuffer(5)
    for t in range(3):
        buf.add(t)
    assert buf.in_order() == [0, 1, 2]
    one = ReplayBuffer(1)
    for t in range(10):
        one.add(t)
    assert one.data == [9]
    with pytest.raises(ValueError):
        ReplayBuffer(0)
    with pytest.raises(ValueError):
        ReplayBuffer(3).sample(1, random.Random(0))


def test_in_order_against_list_model():
    rng = random.Random(11)
    for _ in range(300):
        cap = rng.randint(1, 7)
        buf = ReplayBuffer(cap)
        model = []
        for t in range(rng.randint(0, 25)):
            buf.add(t)
            model.append(t)
            assert buf.in_order() == model[-cap:]


def test_sample_is_randrange_of_size():
    buf = ReplayBuffer(6)
    for t in range(9):
        buf.add(t)
    twin = random.Random(5)
    expected = [buf.data[twin.randrange(6)] for _ in range(20)]
    assert buf.sample(20, random.Random(5)) == expected


def test_uniform_frequencies():
    buf = ReplayBuffer(6)
    for t in range(6):
        buf.add(t)
    rng = random.Random(2024)
    counts = [0] * 6
    m = 60000
    for x in buf.sample(m, rng):
        counts[x] += 1
    # Each count is Binomial(60000, 1/6): mean 10000, standard deviation about 91.3.
    for c in counts:
        assert abs(c - 10000) < 5 * 91.3


def chain_step(s, a):
    """Chain 0..4: action 1 moves right, action 0 moves left; leaving 4 to the right ends with reward 1."""
    if a == 1:
        if s == 4:
            return 1.0, 4, True
        return 0.0, s + 1, False
    return 0.0, max(s - 1, 0), False


def test_replay_learns_q_star_from_random_behavior():
    rng = random.Random(7)
    buf = ReplayBuffer(500)
    collect(chain_step, 0, 2, buf, 3000, rng)
    q = replay_q_learning(buf, 5, 2, 0.9, 0.2, 3000, 32, rng)
    for s in range(5):
        q_right = 0.9 ** (4 - s)
        q_left = 0.9 * 0.9 ** (4 - max(s - 1, 0))
        assert abs(q[s][1] - q_right) < 1e-6
        assert abs(q[s][0] - q_left) < 1e-6
        assert q[s][1] > q[s][0]
