# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/photon-map/. The authors are listed in prov/JNG669.jsonl.

import math
import random

import pytest

from photon_map import Photon, PhotonMap, left_size


def random_photons(n: int, rng: random.Random, flat: bool = False) -> list[Photon]:
    out = []
    for _ in range(n):
        z = 0.0 if flat else rng.random()
        out.append(Photon((rng.random(), rng.random(), z), rng.random()))
    return out


def d2(a, b) -> float:
    return sum((a[i] - b[i]) ** 2 for i in range(3))


def brute_k_nearest(photons, x, k, max_radius=math.inf):
    cands = sorted(d2(p.position, x) for p in photons if d2(p.position, x) < max_radius * max_radius)
    return cands[:k]


def test_left_size_matches_a_complete_tree() -> None:
    for n in range(1, 200):
        # Count the nodes of the subtree at index 2 in a heap array of n nodes.
        count, level = 0, [2]
        while level:
            level = [i for i in level if i <= n]
            count += len(level)
            level = [c for i in level for c in (2 * i, 2 * i + 1)]
        assert left_size(n) == count


@pytest.mark.parametrize("n", [1, 2, 3, 7, 8, 100, 1000])
def test_tree_invariant(n: int) -> None:
    rng = random.Random(n)
    pm = PhotonMap(random_photons(n, rng))
    assert all(pm.heap[i] is not None for i in range(1, n + 1))  # no gaps in the array
    for i in range(1, n + 1):
        axis, split = pm.axis[i], pm.heap[i].position[pm.axis[i]]
        for child, sign in ((2 * i, -1), (2 * i + 1, 1)):
            stack = [child]
            while stack:
                j = stack.pop()
                if j > n:
                    continue
                v = pm.heap[j].position[axis]
                assert (v <= split) if sign < 0 else (v >= split)
                stack += [2 * j, 2 * j + 1]


@pytest.mark.parametrize("seed", range(5))
def test_k_nearest_against_brute_force(seed: int) -> None:
    rng = random.Random(seed)
    photons = random_photons(2000, rng)
    pm = PhotonMap(photons)
    for _ in range(50):
        x = (rng.uniform(-0.2, 1.2), rng.uniform(-0.2, 1.2), rng.uniform(-0.2, 1.2))
        k = rng.choice([1, 5, 20, 50])
        r = rng.choice([math.inf, 0.1, 0.25])
        got = [d for d, _ in pm.k_nearest(x, k, r)]
        assert got == brute_k_nearest(photons, x, k, r)


def test_in_radius_against_brute_force() -> None:
    rng = random.Random(9)
    photons = random_photons(1500, rng)
    pm = PhotonMap(photons)
    for _ in range(50):
        x = (rng.random(), rng.random(), rng.random())
        r = rng.uniform(0.01, 0.3)
        got = sorted(d2(p.position, x) for p in pm.in_radius(x, r))
        want = sorted(d2(p.position, x) for p in photons if d2(p.position, x) < r * r)
        assert got == want


def test_duplicates_and_flat_sets() -> None:
    rng = random.Random(4)
    photons = random_photons(300, rng, flat=True) + [Photon((0.5, 0.5, 0.0), 1.0)] * 40
    pm = PhotonMap(photons)
    x = (0.5, 0.5, 0.0)
    got = [d for d, _ in pm.k_nearest(x, 45)]
    assert got == brute_k_nearest(photons, x, 45)
    assert got[:40] == [0.0] * 40


def test_density_estimate_bias_of_the_k_nearest_radius() -> None:
    # Uniform points of density lam on a plane. The estimate k / (pi r_k^2) has the mean
    # lam k / (k - 1) for a Poisson process, and (k - 1) / (pi r_k^2) has the mean lam.
    rng = random.Random(2001)
    side, n, k = 10.0, 20000, 10
    lam = n / side**2
    photons = [Photon((rng.uniform(0, side), rng.uniform(0, side), 0.0), 1.0) for _ in range(n)]
    pm = PhotonMap(photons)
    ests = []
    for i in range(30):
        for j in range(30):
            x = (3 + 4 * (i + 0.5) / 30, 3 + 4 * (j + 0.5) / 30, 0.0)
            ests.append(pm.density_estimate(x, k)[0])
    m = len(ests)
    mean = sum(ests) / m
    se = math.sqrt(sum((e - mean) ** 2 for e in ests) / (m - 1) / m)
    assert abs(mean - lam * k / (k - 1)) < 4 * se
    unbiased = mean * (k - 1) / k
    assert abs(unbiased - lam) < 4 * se
    assert mean - lam > 4 * se  # the plain estimate is biased upward
