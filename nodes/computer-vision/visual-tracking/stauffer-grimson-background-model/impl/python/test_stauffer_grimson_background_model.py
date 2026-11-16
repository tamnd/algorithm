# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stauffer-grimson-background-model/. The authors are listed in prov/193Y4C.jsonl.

import itertools
import math
import random

from stauffer_grimson_background_model import (
    BackgroundModel,
    PixelMixture,
    background_set,
)


def brute_background_set(comps, t):
    """The definition by search: the smallest prefix of the w / sigma order with weight above t."""
    keys = [c[0] / math.sqrt(c[2]) for c in comps]
    order = sorted(range(len(comps)), key=lambda k: (-keys[k], k))
    for b in range(1, len(comps) + 1):
        if sum(comps[k][0] for k in order[:b]) > t:
            return set(order[:b])
    return set(order)


def random_comps(rng, k):
    ws = [rng.random() for _ in range(k)]
    s = sum(ws)
    return [[w / s, rng.uniform(0, 255), rng.uniform(4, 900)] for w in ws]


def test_background_set_against_definition_and_heavy_component():
    rng = random.Random(1)
    for _ in range(500):
        comps = random_comps(rng, rng.randint(1, 5))
        t = rng.choice([0.5, 0.7, 0.9])
        got = background_set(comps, t)
        assert got == brute_background_set(comps, t)
        for k, c in enumerate(comps):
            if c[0] >= 1.0 - t:
                assert k in got  # a component of weight at least 1 - T is background


def test_page_example():
    base = [[0.6, 50.0, 16.0], [0.3, 120.0, 100.0], [0.1, 200.0, 900.0]]
    assert background_set(base, 0.7) == {0, 1}
    results = {}
    for x in (126.0, 200.0, 90.0):
        p = PixelMixture(0.0)
        p.comps = [c[:] for c in base]
        results[x] = (p.update(x), p.comps)
    bg, comps = results[126.0]
    assert bg and [round(c[0], 12) for c in comps] == [0.594, 0.307, 0.099]
    rho = 0.01 * math.exp(-0.18) / math.sqrt(2 * math.pi * 100.0)
    assert abs(rho - 0.000333) < 1e-6
    assert abs(comps[1][1] - (120.0 + 6.0 * rho)) < 1e-12
    bg, comps = results[200.0]
    assert not bg and [round(c[0], 12) for c in comps] == [0.594, 0.297, 0.109]
    bg, comps = results[90.0]
    assert not bg and comps[2] == [0.05, 90.0, 900.0]
    assert abs(comps[0][0] - 0.95 * 2 / 3) < 1e-12 and abs(comps[1][0] - 0.95 / 3) < 1e-12


def test_weights_stay_a_probability_vector():
    rng = random.Random(2)
    for mode in ("paper", "alpha_over_w"):
        p = PixelMixture(100.0, k=4)
        lo = hi = 100.0
        for _ in range(2000):
            x = rng.choice([rng.gauss(100, 3), rng.gauss(180, 5), rng.uniform(0, 255)])
            lo, hi = min(lo, x), max(hi, x)
            p.update(x, rho_mode=mode)
            assert all(c[0] >= 0 for c in p.comps)
            assert abs(sum(c[0] for c in p.comps) - 1.0) < 1e-9
            assert all(c[2] >= 4.0 for c in p.comps)
            assert all(lo - 1e-9 <= c[1] <= hi + 1e-9 for c in p.comps if c[0] > 0)


def test_weight_closed_form_under_repeated_matches():
    alpha, w0 = 0.01, 0.05
    p = PixelMixture(50.0)
    for _ in range(200):
        p.update(50.0, alpha=alpha)
    assert p.update(200.0, alpha=alpha, w0=w0) is False  # no match: a new component
    k = max(range(3), key=lambda i: p.comps[i][1])
    assert p.comps[k][0] == w0
    for t in range(1, 60):
        p.update(200.0, alpha=alpha)
        assert abs(p.comps[k][0] - (1.0 - (1.0 - w0) * (1.0 - alpha) ** t)) < 1e-12


def test_stationary_object_absorbed_after_the_bound():
    alpha, t_bg, w0 = 0.01, 0.7, 0.05
    bound = math.ceil(math.log(t_bg / (1.0 - w0)) / math.log(1.0 - alpha))
    assert bound == 31
    p = PixelMixture(50.0)
    for _ in range(200):
        assert p.update(50.0, alpha=alpha, t=t_bg)
    flags = [p.update(200.0, alpha=alpha, t=t_bg, w0=w0) for _ in range(60)]
    # frame 0 creates the component; frame 31 is the first background frame
    assert flags.index(True) == bound and all(flags[bound:])
    # the old background value is still background
    assert p.update(50.0, alpha=alpha, t=t_bg)


def test_bimodal_pixel_is_background():
    rng = random.Random(4)
    p3 = PixelMixture(60.0, k=3)
    p1 = PixelMixture(60.0, k=1)
    flags3, flags1 = [], []
    for f in range(600):
        x = (60.0 if f % 2 == 0 else 190.0) + rng.gauss(0, 2)
        flags3.append(p3.update(x))
        flags1.append(p1.update(x))
    assert all(flags3[100:])  # both modes are background
    assert not any(flags1[1:])  # one Gaussian never settles on two modes


def make_video(seed, size=16, frames=50, start=35):
    """A static textured background with noise 2, and a 6 by 6 square of value 230
    that enters at frame `start` and moves one pixel to the right per frame."""
    rng = random.Random(seed)
    base = [[rng.uniform(40, 120) for _ in range(size)] for _ in range(size)]
    video, truth = [], []
    for f in range(frames):
        img = [[base[y][x] + rng.gauss(0, 2) for x in range(size)] for y in range(size)]
        mask = [[0] * size for _ in range(size)]
        if f >= start:
            x0 = f - start
            for y in range(5, 11):
                for x in range(x0, min(size, x0 + 6)):
                    img[y][x] = 230.0 + rng.gauss(0, 2)
                    mask[y][x] = 1
        video.append(img)
        truth.append(mask)
    return video, truth


def test_moving_square_detected():
    for mode in ("paper", "alpha_over_w"):
        video, truth = make_video(5)
        model = BackgroundModel(video[0], rho_mode=mode)
        tp = fp = fn = 0
        for f in range(1, len(video)):
            mask = model.apply(video[f])
            if f < 35:
                continue
            for a, b in zip(itertools.chain(*mask), itertools.chain(*truth[f])):
                tp += a and b
                fp += a and not b
                fn += b and not a
        assert fn == 0
        assert fp <= 0.01 * (tp + fp)
