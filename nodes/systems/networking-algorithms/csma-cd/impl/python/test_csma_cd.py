# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/csma-cd/. The authors are listed in prov/296FV6.jsonl.

import random

from csma_cd import (
    SLOT_TIME,
    backoff_slots,
    csma_cd,
    delivered_frames,
    efficiency_approx,
    overlap_at,
)


def random_bus(seed, n=5, per_station=8):
    rng = random.Random(seed)
    pos = sorted(rng.sample(range(0, SLOT_TIME // 2 + 1), n))  # end-to-end delay at most 256
    frames = []
    for i in range(n):
        t = 0
        for _ in range(per_station):
            t += rng.randrange(0, 3000)
            dest = rng.choice([j for j in range(n) if j != i])
            frames.append((i, t, rng.randrange(SLOT_TIME, 3000), dest))
    return pos, frames


def test_every_frame_is_delivered_intact_with_long_frames():
    for seed in range(5):
        pos, frames = random_bus(seed)
        out, sig = csma_cd(pos, frames, random.Random(seed + 100))
        assert len(out) == len(frames)
        assert all(a != "dropped" for _, a in out.values())
        ok = delivered_frames(frames, pos, out, sig)
        assert all(ok.values())


def test_collisions_happen_and_every_sender_sees_its_collision():
    collided_somewhere = 0
    for seed in range(5):
        pos, frames = random_bus(seed)
        out, sig = csma_cd(pos, frames, random.Random(seed + 100))
        data = [s for s in sig if s.frame is not None]
        for a in data:
            for b in data:
                if a is b or a.src == b.src:
                    continue
                if any(overlap_at(a, b, y) for y in pos):
                    collided_somewhere += 1
                    # the frame was cut short: its sender detected the collision
                    assert a.end - a.start < frames[a.frame][2]
    assert collided_somewhere > 0


def test_short_frames_give_an_undetected_collision():
    # A at 0 and B at 300: the round trip is 600 bit times, more than the 100-bit frame.
    pos = [0, 300, 290]
    frames = [(0, 0, 100, 2), (1, 380, 100, 2)]
    out, sig = csma_cd(pos, frames, random.Random(1))
    assert out[0] == (196, 1)  # A finished at time 196 and saw no collision
    ok = delivered_frames(frames, pos, out, sig)
    assert ok[0] is False  # but its frame is garbled at the receiver C
    assert ok[1] is True  # B saw the collision and sent again


def test_same_scene_with_long_frames_is_detected():
    pos = [0, 300, 290]
    frames = [(0, 0, 600, 2), (1, 380, 600, 2)]
    out, sig = csma_cd(pos, frames, random.Random(1))
    first = [s for s in sig if s.frame == 0][0]
    assert (first.start, first.end) == (96, 680)  # B's signal reaches A at 380 + 300
    assert out[0][1] > 1 and out[1][1] > 1
    assert all(delivered_frames(frames, pos, out, sig).values())


def test_backoff_range():
    rng = random.Random(4)
    for c in range(1, 16):
        hi = 2 ** min(c, 10)
        draws = [backoff_slots(c, rng) for _ in range(200)]
        assert 0 <= min(draws) and max(draws) < hi


def test_lone_station_waits_only_the_gap():
    out, sig = csma_cd([0, 100], [(0, 10, 512, 1), (0, 10, 512, 1)], random.Random(2))
    assert [(s.start, s.end) for s in sig] == [(96, 608), (704, 1216)]


def test_efficiency_approximation_values():
    assert abs(efficiency_approx(1, 10) - 2 / 3) < 1e-12
    assert efficiency_approx(0, 5) == 1
