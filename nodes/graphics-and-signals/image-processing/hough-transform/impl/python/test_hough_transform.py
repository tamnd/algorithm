# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hough-transform/. The authors are listed in prov/ZV0TVQ.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

import pytest

from hough_transform import hough_lines, peaks

W = H = 40
T = 180


def brute_pairs(points, w, h, t):
    """Brute force voting: one vote for every (point, angle) pair, counted in a dictionary."""
    d = math.ceil(math.hypot(w - 1, h - 1))
    votes = Counter()
    for x, y in points:
        for k in range(t):
            rho = x * math.cos(k * math.pi / t) + y * math.sin(k * math.pi / t)
            votes[(k, math.floor(Fraction(rho) + Fraction(1, 2)))] += 1
    return [[votes[(k, j - d)] for j in range(2 * d + 1)] for k in range(t)]


def brute_cells(points, w, h, t):
    """Cell by cell: count the points whose rho falls in [rho_j - 1/2, rho_j + 1/2)."""
    d = math.ceil(math.hypot(w - 1, h - 1))
    acc = []
    for k in range(t):
        c, s = math.cos(k * math.pi / t), math.sin(k * math.pi / t)
        row = []
        for j in range(2 * d + 1):
            centre = j - d
            row.append(sum(1 for x, y in points if centre - 0.5 <= x * c + y * s < centre + 0.5))
        acc.append(row)
    return acc


def test_against_brute_force() -> None:
    rng = random.Random(79)
    for _ in range(30):
        w, h = rng.randint(1, 12), rng.randint(1, 12)
        t = rng.randint(1, 24)
        pts = [(rng.randrange(w), rng.randrange(h)) for _ in range(rng.randint(0, 15))]
        got = hough_lines(pts, w, h, t)
        assert got == brute_pairs(pts, w, h, t)
        assert got == brute_cells(pts, w, h, t)


def test_each_point_votes_once_per_angle() -> None:
    rng = random.Random(83)
    pts = [(rng.randrange(W), rng.randrange(H)) for _ in range(50)]
    acc = hough_lines(pts, W, H, T)
    assert all(sum(row) == 50 for row in acc)


PLANTED = [
    # (points, k, rho, votes)
    ([(12, y) for y in range(H)], 0, 12, H),
    ([(x, 7) for x in range(W)], 90, 7, W),
    ([(x, 30 - x) for x in range(31)], 45, round(30 / math.sqrt(2)), 31),
    ([(x, x + 5) for x in range(35)], 135, round(5 / math.sqrt(2)), 35),
]


@pytest.mark.parametrize("points,k,rho,votes", PLANTED)
def test_planted_line_is_the_top_peak(points, k, rho, votes) -> None:
    """Without noise the planted cell holds every vote. With noise the top peak is within one
    bin, because a segment of length L spreads over L sin(pi / T) < 1 in the next angle bin."""
    alone = hough_lines(points, W, H, T)
    assert alone[k][rho + math.ceil(math.hypot(W - 1, H - 1))] == votes
    rng = random.Random(89 + k)
    noise = [(rng.randrange(W), rng.randrange(H)) for _ in range(40)]
    v, theta, r = peaks(hough_lines(points + noise, W, H, T), T, 10)[0]
    assert abs(round(theta * T / math.pi) - k) <= 1 and abs(r - rho) <= 1 and v >= votes


def test_four_lines_at_once() -> None:
    pts = [p for points, _, _, _ in PLANTED for p in points]
    found = peaks(hough_lines(pts, W, H, T), T, 20)
    cells = {(round(theta * T / math.pi), rho) for _, theta, rho in found[:4]}
    assert cells == {(k, rho) for _, k, rho, _ in PLANTED}


def test_slope_two_line_within_one_bin() -> None:
    pts = [(x, 2 * x + 8) for x in range(16)]
    theta0 = math.atan2(1, -2)
    rho0 = 8 / math.sqrt(5)
    v, theta, rho = peaks(hough_lines(pts, W, H, T), T, 5)[0]
    assert v == 16
    assert abs(theta - theta0) <= math.pi / T + 1e-12
    assert abs(rho - rho0) <= 1.0


def test_rounded_points_of_an_oblique_line() -> None:
    theta0, rho0 = math.radians(60), 20.0
    pts = set()
    for s in range(-60, 61):
        x = rho0 * math.cos(theta0) - s * 0.5 * math.sin(theta0)
        y = rho0 * math.sin(theta0) + s * 0.5 * math.cos(theta0)
        if 0 <= round(x) < W and 0 <= round(y) < H:
            pts.add((round(x), round(y)))
    v, theta, rho = peaks(hough_lines(sorted(pts), W, H, T), T, 5)[0]
    assert abs(theta - theta0) <= 2 * math.pi / T + 1e-12
    assert abs(rho - rho0) <= 1.0


def test_edges() -> None:
    assert hough_lines([], 1, 1, 3) == [[0], [0], [0]]
    assert peaks([], 3, 1) == []
    with pytest.raises(ValueError):
        hough_lines([(0, 0)], 2, 2, 0)
