# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vibe-background-subtraction/. The authors are listed in prov/2FRG4D.jsonl.

import itertools
import math
import random

from vibe_background_subtraction import ViBe


def brute_is_background(v, samples, radius, min_matches):
    return sum(1 for s in samples if abs(v - s) < radius) >= min_matches


def test_classification_against_full_count():
    rng = random.Random(1)
    model = ViBe([[0]])
    for _ in range(2000):
        samples = [rng.randint(0, 255) for _ in range(20)]
        v = rng.randint(0, 255)
        assert model.is_background(v, samples) == brute_is_background(v, samples, 20, 2)


def test_page_example_classification():
    model = ViBe([[0]], n=6)
    samples = [100, 104, 131, 96, 160, 119]
    assert model.is_background(110, samples)  # 100, 104, 96 and 119 are closer than 20
    assert not model.is_background(140, samples)  # only 131; 160 is at distance 20, not closer
    assert model.is_background(150, samples)  # 131 and 160


def survival_frequency(n, phi, frames, runs, seed):
    """A 1 by 1 image that is always background: how often does the first sample survive?"""
    rng = random.Random(seed)
    alive = 0
    for _ in range(runs):
        model = ViBe([[100]], n=n, phi=phi, seed=rng.randrange(10 ** 9))
        model.samples[0][0] = [101] + [100] * (n - 1)  # mark the first sample
        for _ in range(frames):
            model.apply([[100]])
        alive += 101 in model.samples[0][0]
    return alive / runs


def test_survival_is_memoryless():
    # With phi = 1 each frame replaces one of N = 5 samples: survival (4/5)^t.
    for t in (1, 3, 6):
        f = survival_frequency(5, 1, t, 1200, 10 + t)
        assert abs(f - 0.8 ** t) < 0.045


def test_expected_lifetime_is_phi_times_n():
    rng = random.Random(4)
    n, phi, runs = 5, 4, 1500
    total = 0
    for _ in range(runs):
        model = ViBe([[100]], n=n, phi=phi, seed=rng.randrange(10 ** 9))
        model.samples[0][0] = [101] + [100] * (n - 1)
        t = 0
        while 101 in model.samples[0][0]:
            model.apply([[100]])
            t += 1
        total += t
    mean = total / runs
    assert abs(mean - phi * n) < 0.1 * phi * n


def test_interior_lifetime_formula():
    # Own updates and the eight neighbors: the survival per frame and the mean lifetime.
    n, phi = 20, 16
    q = (1 - 1 / (phi * n)) * (1 - 1 / (8 * phi * n)) ** 8
    assert abs(1 / (1 - q) - 160.36) < 0.01
    assert abs(math.log(q) * 320 + 2.0) < 0.002


def test_foreground_pixels_never_update():
    model = ViBe([[50] * 6 for _ in range(6)], phi=1, seed=3)
    before = [[s[:] for s in row] for row in model.samples]
    for _ in range(20):
        mask = model.apply([[200] * 6 for _ in range(6)])
        assert all(all(row) for row in mask)
    assert model.samples == before


def ghost_counts(phi, frames, seed):
    """The first frame has a 6 by 6 object of value 200 on a background of 50, then
    the object is gone. Returns the number of foreground pixels per frame."""
    size = 12
    first = [[200 if 3 <= y < 9 and 3 <= x < 9 else 50 for x in range(size)] for y in range(size)]
    model = ViBe(first, phi=phi, seed=seed)
    bg = [[50] * size for _ in range(size)]
    return [sum(itertools.chain(*model.apply(bg))) for _ in range(frames)]


def test_ghost_erodes_from_its_border():
    counts = ghost_counts(1, 80, 7)
    assert 16 <= counts[0] <= 36  # at most the object; its border already mixes in background samples
    assert all(a >= b for a, b in zip(counts, counts[1:]))
    assert counts[-1] == 0
    # with the default phi = 16 the same ghost is still there after 80 frames
    assert ghost_counts(16, 80, 7)[-1] > 0


def test_moving_square_detected():
    rng = random.Random(5)
    size = 16
    base = [[60 + 3 * x + 2 * y for x in range(size)] for y in range(size)]
    model = ViBe(base, seed=9)
    tp = fp = fn = 0
    for f in range(1, 40):
        img = [[base[y][x] + rng.gauss(0, 2) for x in range(size)] for y in range(size)]
        truth = [[0] * size for _ in range(size)]
        if f >= 25:
            for y in range(5, 11):
                for x in range(f - 25, min(size, f - 19)):
                    img[y][x] = 230 + rng.gauss(0, 2)
                    truth[y][x] = 1
        mask = model.apply(img)
        if f < 25:
            continue
        for a, b in zip(itertools.chain(*mask), itertools.chain(*truth)):
            tp += a and b
            fp += a and not b
            fn += b and not a
    assert fn == 0
    assert fp <= 0.02 * (tp + fp)
