# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/channel-capacity/. The authors are listed in prov/MBQ0RF.jsonl.

import math
import random

from channel_capacity import bec, blahut_arimoto, bsc, mutual_information, z_channel, z_channel_capacity


def h(p: float) -> float:
    return 0.0 if p in (0.0, 1.0) else -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def grid_capacity_two_inputs(w, steps=20000) -> float:
    return max(mutual_information([a / steps, 1 - a / steps], w) for a in range(steps + 1))


def test_bsc() -> None:
    for p in (0.0, 0.01, 0.11, 0.3, 0.5):
        c, r, _ = blahut_arimoto(bsc(p))
        assert abs(c - (1 - h(p))) < 1e-9
        assert abs(r[0] - 0.5) < 1e-6


def test_bec() -> None:
    for eps in (0.0, 0.2, 0.5, 0.9):
        c, _, _ = blahut_arimoto(bec(eps))
        assert abs(c - (1 - eps)) < 1e-9


def test_z_channel_closed_form() -> None:
    assert math.isclose(z_channel_capacity(0.5), math.log2(1.25))
    for p in (0.0, 0.1, 0.5, 0.9):
        c, r, _ = blahut_arimoto(z_channel(p))
        assert abs(c - z_channel_capacity(p)) < 1e-9
        # derivation: the best input puts weight q* on 1 with q*(1 - p) = a / (1 + a)
        if p > 0:
            a = (1 - p) * p ** (p / (1 - p))
            assert abs(r[1] * (1 - p) - a / (1 + a)) < 1e-5
            # and I(q) = h(q (1 - p)) - q h(p)
            assert abs(h(r[1] * (1 - p)) - r[1] * h(p) - c) < 1e-9
        assert abs(grid_capacity_two_inputs(z_channel(p)) - z_channel_capacity(p)) < 1e-7
    # the best input is not uniform: at p = 1/2 it sends 1 with probability 2/5
    _, r, _ = blahut_arimoto(z_channel(0.5))
    assert abs(r[1] - 0.4) < 1e-5


def test_noiseless_and_typewriter() -> None:
    eye = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    assert abs(blahut_arimoto(eye)[0] - 2.0) < 1e-9
    # noisy typewriter: 26 letters, each goes to itself or the next one with probability 1/2
    tw = [[0.5 if j in (i, (i + 1) % 26) else 0.0 for j in range(26)] for i in range(26)]
    assert abs(blahut_arimoto(tw)[0] - math.log2(13)) < 1e-9


def test_symmetric_channel_formula() -> None:
    # rows are permutations of each other and so are columns: C = log2 |Y| - H(row)
    row = [0.5, 0.3, 0.2]
    w = [row[i:] + row[:i] for i in range(3)]
    hrow = -sum(p * math.log2(p) for p in row)
    assert abs(blahut_arimoto(w)[0] - (math.log2(3) - hrow)) < 1e-9


def test_random_channels_against_grid_and_bounds() -> None:
    rng = random.Random(12)
    for _ in range(15):
        w = []
        for _ in range(2):
            v = [rng.random() for _ in range(3)]
            s = sum(v)
            w.append([x / s for x in v])
        c, r, _ = blahut_arimoto(w)
        assert abs(c - grid_capacity_two_inputs(w)) < 1e-6
        assert abs(mutual_information(r, w) - c) < 1e-9
    for _ in range(10):  # three inputs: compare with a grid on the simplex
        w = []
        for _ in range(3):
            v = [rng.random() ** 3 for _ in range(4)]
            s = sum(v)
            w.append([x / s for x in v])
        c, r, _ = blahut_arimoto(w)
        steps = 120
        best = max(
            mutual_information([a / steps, b / steps, (steps - a - b) / steps], w)
            for a in range(steps + 1) for b in range(steps + 1 - a)
        )
        assert best <= c + 1e-9 and c - best < 1e-3
        # optimality conditions: D(W(.|x) || q) = C where r(x) > 0, and <= C everywhere
        q = [sum(r[x] * w[x][y] for x in range(3)) for y in range(4)]
        for x in range(3):
            dx = sum(w[x][y] * math.log2(w[x][y] / q[y]) for y in range(4) if w[x][y] > 0)
            assert dx <= c + 1e-6
            if r[x] > 1e-4:
                assert abs(dx - c) < 1e-5
