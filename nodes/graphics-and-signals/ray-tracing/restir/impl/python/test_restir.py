# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/restir/. The authors are listed in prov/T9MCYJ.jsonl.

"""ReSTIR against exact answers.

The exact tests use a table scene with three lights and Fraction values.
They list every outcome of the random choices: each tuple of candidates with
its probability, and each branch of each reservoir update with the
probability w / w_sum. The expected value of f(y) W is then a finite sum,
and the unbiased versions must give the pixel value exactly. The last test
renders frames of a geometric scene and asks each pixel to be within 4
standard errors of the exact sum over the lights.
"""

import itertools
import math
import random
from fractions import Fraction as Fr

from restir import Reservoir, clamp, combine, make_scene, render, ris

Z = 4.0


class Table:
    """A scene given by tables: target[q][y], visible[q][y] and the source density of each light."""

    def __init__(self, target, visible, source):
        self.t, self.v, self.p = target, visible, source

    def target(self, q, y):
        return self.t[q][y]

    def visible(self, q, y):
        return bool(self.v[q][y])

    def source_pdf(self, y):
        return self.p[y]

    def contribution(self, q, y):
        return self.t[q][y] if self.v[q][y] else Fr(0)

    def exact(self, q):
        return sum(self.contribution(q, y) for y in range(len(self.p)))


SCENE = Table(
    [[Fr(1), Fr(2), Fr(3)], [Fr(2), Fr(1), Fr(1)]],
    [[1, 1, 0], [0, 1, 1]],
    [Fr(1, 2), Fr(1, 4), Fr(1, 4)],
)


def branches(ws):
    """Every way the updates with the weights ws can go: (probability, uniform numbers)."""
    options, total = [], 0
    for w in ws:
        total += w
        t = w / total if total > 0 else Fr(0)
        step = []
        if t > 0:
            step.append((t, Fr(0)))
        if t < 1:
            step.append((1 - t, Fr(1)))
        options.append(step)
    for pick in itertools.product(*options):
        prob = Fr(1)
        for p, _ in pick:
            prob *= p
        yield prob, [u for _, u in pick]


def ris_outcomes(scene, q, m):
    n = len(scene.p)
    for xs in itertools.product(range(n), repeat=m):
        p = Fr(1)
        for x in xs:
            p *= scene.source_pdf(x)
        ws = [scene.target(q, x) / scene.source_pdf(x) for x in xs]
        for pu, us in branches(ws):
            yield p * pu, ris(scene, q, list(xs), us)


def combine_outcomes(scene, q, groups, owners, weighting):
    """Outcomes of COMBINE at q over independent inputs; groups[i] lists (prob, reservoir)."""
    for choice in itertools.product(*groups):
        p = Fr(1)
        for prob, _ in choice:
            p *= prob
        rs = [r for _, r in choice]
        ws = [scene.target(q, r.y) * r.W * r.m if r.y is not None else Fr(0) for r in rs]
        for pu, us in branches(ws):
            yield p * pu, combine(scene, q, rs, owners, us, weighting)


def mean_value(scene, q, outcomes):
    total = sum(p * scene.contribution(q, r.y) * r.W for p, r in outcomes if r.y is not None)
    assert isinstance(total, Fr)
    return total


def test_reservoir_keeps_each_item_in_proportion_to_its_weight() -> None:
    ws = [Fr(1), Fr(0), Fr(2), Fr(3)]
    got = [Fr(0)] * 4
    for prob, us in branches(ws):
        r = Reservoir()
        for x, (w, u) in enumerate(zip(ws, us)):
            r.update(x, w, u)
        got[r.y] += prob
        assert r.w_sum == 6 and r.m == 4
    assert got == [Fr(1, 6), Fr(0), Fr(1, 3), Fr(1, 2)]


def test_ris_is_exactly_unbiased() -> None:
    for q in range(2):
        for m in (1, 2, 3):
            outcomes = list(ris_outcomes(SCENE, q, m))
            assert sum(p for p, _ in outcomes) == 1
            assert mean_value(SCENE, q, outcomes) == SCENE.exact(q)
    assert SCENE.exact(0) == 3 and SCENE.exact(1) == 2


def test_ris_picks_lights_by_the_target_as_m_grows() -> None:
    # P(y = light 2) for pixel 0 goes from the source density 1/4 toward the target share 1/2.
    share = []
    for m in (1, 2, 3):
        share.append(sum(p for p, r in ris_outcomes(SCENE, 0, m) if r.y == 2))
    assert share[0] == Fr(1, 4) and share[0] < share[1] < share[2] < Fr(1, 2)


def test_a_target_with_holes_is_biased() -> None:
    holes = Table([[Fr(1), Fr(0), Fr(3)], SCENE.t[1]], SCENE.v, SCENE.p)
    outcomes = list(ris_outcomes(holes, 0, 2))
    assert mean_value(SCENE, 0, outcomes) == SCENE.exact(0) - SCENE.contribution(0, 1)


def test_spatial_reuse_unbiased_and_biased() -> None:
    groups = [list(ris_outcomes(SCENE, 0, 2)), list(ris_outcomes(SCENE, 1, 1))]
    for owners, extra in (([0, 1], []), ([0, 1, 1], [list(ris_outcomes(SCENE, 1, 1))])):
        for weighting in ("z", "mis"):
            fair = list(combine_outcomes(SCENE, 0, groups + extra, owners, weighting))
            assert sum(p for p, _ in fair) == 1
            assert mean_value(SCENE, 0, fair) == SCENE.exact(0)
            # W is an unbiased contribution weight for every light: E[1(y = l) W] = 1 on the support of p_0 V_0.
            for light in range(3):
                weight = sum(p * r.W for p, r in fair if r.y == light)
                assert weight == (1 if SCENE.visible(0, light) else 0)
    biased = list(combine_outcomes(SCENE, 0, groups, [0, 1], "biased"))
    value = mean_value(SCENE, 0, biased)
    assert value < SCENE.exact(0)
    # Light 0 is in the support of pixel 0 only, so its weight M_0 / (M_0 + M_1) = 2/3 is all it gets.
    assert sum(p * r.W for p, r in biased if r.y == 0) == Fr(2, 3)


def test_temporal_reuse_with_the_m_cap_is_unbiased() -> None:
    prev = list(ris_outcomes(SCENE, 0, 3))
    for limit in (1, 2, 3):
        groups = [list(ris_outcomes(SCENE, 0, 1)), [(p, clamp(r, limit)) for p, r in prev]]
        out = list(combine_outcomes(SCENE, 0, groups, [0, 0], "z"))
        assert mean_value(SCENE, 0, out) == SCENE.exact(0)
        assert all(r.m == 1 + limit for _, r in out)


def test_frames_agree_with_the_exact_sum() -> None:
    scene = make_scene(3)
    exact = [scene.exact(q) for q in range(len(scene.points))]
    assert min(exact) > 0
    assert any(not scene.visible(q, y) for q in range(8) for y in range(16))
    runs, frames = 300, 3
    for weighting, k in (("z", 2), ("mis", 2), ("z", 0)):
        sums = [[[0.0, 0.0] for _ in exact] for _ in range(frames)]
        rng = random.Random(11)
        for _ in range(runs):
            images = render(scene, frames, random.Random(rng.getrandbits(64)), weighting=weighting, k=k)
            for t, image in enumerate(images):
                for q, v in enumerate(image):
                    sums[t][q][0] += v
                    sums[t][q][1] += v * v
        for t in range(frames):
            for q, ref in enumerate(exact):
                s, s2 = sums[t][q]
                mean = s / runs
                se = math.sqrt(max(0.0, s2 / runs - mean * mean) / (runs - 1))
                assert abs(mean - ref) <= Z * se + 1e-12, (weighting, k, t, q, mean, se, ref)


def test_biased_reuse_is_darker_than_the_exact_sum() -> None:
    scene = make_scene(3)
    rng = random.Random(12)
    runs = 300
    total = [0.0] * 8
    for _ in range(runs):
        image = render(scene, 4, random.Random(rng.getrandbits(64)), weighting="biased")[-1]
        total = [a + b for a, b in zip(total, image)]
    assert sum(total) / runs < 0.8 * sum(scene.exact(q) for q in range(8))
