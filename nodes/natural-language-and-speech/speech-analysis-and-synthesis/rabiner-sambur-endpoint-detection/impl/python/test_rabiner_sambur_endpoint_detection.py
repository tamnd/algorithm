# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabiner-sambur-endpoint-detection/. The authors are listed in prov/B6AHEG.jsonl.

import random

from nlsdsp import all_pole, sine, white_noise
from rabiner_sambur_endpoint_detection import (
    detect_endpoints,
    endpoints_from_features,
    features,
    first_crossing,
    frame_energy,
    refine,
    thresholds,
    zero_crossings,
)

FS = 16000.0


def _background(rng, n):
    # low-pass noise: a lag-one correlation near 0.98 gives few zero crossings
    return all_pole(white_noise(rng, n, 0.0006), [0.98])


def _word(rng, lead_fricative=0, tail_fricative=0):
    """300 ms of background, an optional weak fricative, 500 ms of tone, an optional fricative, 300 ms of background."""
    sig = _background(rng, 4800)
    sig += white_noise(rng, 160 * lead_fricative, 0.006)
    sig += [s + b for s, b in zip(sine(300.0, FS, 8000, 0.3), _background(rng, 8000))]
    sig += white_noise(rng, 160 * tail_fricative, 0.006)
    sig += _background(rng, 4800)
    return sig


def test_frame_measures():
    assert frame_energy([0.5, -0.25, 0.0, 1.0]) == 1.75
    # zero counts as positive: + - + + - gives 3 sign changes
    assert zero_crossings([1.0, -1.0, 1.0, 0.0, -1.0]) == 3
    assert zero_crossings([0.0, 0.0, 0.0]) == 0
    e, z = features(sine(300.0, FS, 1600), FS)
    assert len(e) == 10 and len(z) == 10
    assert all(5 <= v <= 7 for v in z)  # about 2 f / fs * 160 = 6 per frame
    e, _ = features([0.0] * 1599, FS)
    assert len(e) == 9


def test_thresholds_by_hand():
    energy = [1.0] * 10 + [100.0]
    zcr = [10] * 10 + [3]
    itl, itu, izct = thresholds(energy, zcr)
    assert abs(itl - 3.97) < 1e-12 and abs(itu - 19.85) < 1e-12
    assert izct == 10.0
    # a noisy silence: IZC + 2 sigma is above 25, so the fixed value IF = 25 wins
    _, _, izct = thresholds(energy, [20, 30] * 5 + [3])
    assert izct == 25.0
    # a loud word: 0.03 (IMX - IMN) + IMN is above 4 IMN, so ITL = 4 IMN
    itl, itu, _ = thresholds([1.0] * 10 + [1000.0], zcr)
    assert itl == 4.0 and itu == 20.0


def _first_crossing_spec(energy, order, itl, itu):
    order = list(order)
    for pos, i in enumerate(order):
        if energy[i] > itl and (pos == 0 or energy[order[pos - 1]] <= itl):
            run = []
            for j in order[pos:]:
                if energy[j] <= itl:
                    break
                run.append(j)
            if any(energy[j] > itu for j in run):
                return i
    return None


def test_first_crossing_against_the_spec():
    rng = random.Random(9)
    for _ in range(400):
        n = rng.randint(1, 30)
        energy = [rng.choice([0.0, 1.0, 2.0, 3.0, 6.0]) * rng.uniform(0.5, 1.5) for _ in range(n)]
        for order in (range(n), range(n - 1, -1, -1)):
            assert first_crossing(energy, order, 1.5, 5.0) == _first_crossing_spec(energy, order, 1.5, 5.0)


def test_refine_rules():
    z = [0] * 40
    for j in (12, 20, 30):
        z[j] = 50
    assert refine(z, 35, -1, 25.0) == 12  # three hits in the 25 frames before 35: go to the earliest
    assert refine(z, 37, -1, 25.0) == 12  # frames 12 to 36 are the 25 frames before 37
    assert refine(z, 38, -1, 25.0) == 38  # frame 12 is now outside, and two hits are not enough
    z[12] = 0
    assert refine(z, 35, -1, 25.0) == 35  # two hits are not enough
    z = [0] * 40
    for j in (5, 6, 9):
        z[j] = 26
    assert refine(z, 2, +1, 25.0) == 9
    z[9] = 25  # Z must be strictly above IZCT
    assert refine(z, 2, +1, 25.0) == 2


def test_tone_word():
    # the tone fills the frames 30 to 79
    assert detect_endpoints(_word(random.Random(1)), FS) == (30, 79)


def test_weak_fricatives_are_found_by_the_zero_crossings():
    rng = random.Random(1)
    sig = _word(rng, lead_fricative=10, tail_fricative=8)
    energy, zcr = features(sig, FS)
    itl, _, izct = thresholds(energy, zcr)
    # the fricative frames stay under ITL, so the energy alone misses them
    assert all(e < itl for e in energy[30:40]) and all(z > izct for z in zcr[30:40])
    assert first_crossing(energy, range(len(energy)), *thresholds(energy, zcr)[:2]) == 40
    assert endpoints_from_features(energy, zcr) == (30, 97)


def test_background_alone_gives_no_word():
    for seed in range(5):
        assert detect_endpoints(_background(random.Random(seed), 16000), FS) is None


def test_bad_arguments():
    try:
        detect_endpoints([0.0] * 1000, FS)
    except ValueError:
        pass
    else:
        raise AssertionError("a signal shorter than 100 ms must fail")
    try:
        endpoints_from_features([1.0] * 12, [0] * 11)
    except ValueError:
        pass
    else:
        raise AssertionError("lengths must match")
