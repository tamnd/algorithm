# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lagrangian-relaxation-gate-sizing/. The authors are listed in prov/AB69M9.jsonl.

import itertools
import math
import random

from lagrangian_relaxation_gate_sizing import (Circuit, area, delay, flow_through, gate_delay,
                                               local_resize, lr_sizing, project)

TOL = 1e-3


def grid_search(ckt, target, pts, rounds=6):
    """Least area over a grid of sizes in log scale that meet the target,
    refined around the best point a few times."""
    free = [i for i in range(ckt.n) if ckt.lo[i] < ckt.hi[i]]
    box = [(math.log(ckt.lo[i]), math.log(ckt.hi[i])) for i in free]
    best = None
    for _ in range(rounds):
        axes = [[l + (h - l) * t / (pts - 1) for t in range(pts)] for (l, h) in box]
        for ys in itertools.product(*axes):
            x = list(ckt.lo)
            for i, y in zip(free, ys):
                x[i] = math.exp(y)
            if delay(ckt, x) <= target:
                ar = area(ckt, x)
                if best is None or ar < best[0]:
                    best = (ar, x)
        if best is None:
            return None
        box = [(max(math.log(ckt.lo[i]), math.log(best[1][i]) - 2 * (h - l) / (pts - 1)),
                min(math.log(ckt.hi[i]), math.log(best[1][i]) + 2 * (h - l) / (pts - 1)))
               for i, (l, h) in zip(free, box)]
    return best[0]


def dual_value(ckt, mu, target):
    """Q(mu) = min over x of area + sum lam_i D_i(x) - T * (flow into the sink).
    By weak duality it is a lower bound on the least area."""
    lam = flow_through(ckt, mu)
    x = local_resize(ckt, lam, list(ckt.lo), sweeps=5000, tol=1e-14)
    total = sum(m for m, (u, v) in zip(mu, ckt.edges) if v == ckt.n)
    return area(ckt, x) + sum(lam[i] * gate_delay(ckt, x, i) for i in range(ckt.n)) - target * total


def random_case(rng, shape):
    if shape == "chain":
        m = rng.randint(2, 3)
        fanin = [[]] + [[i - 1] for i in range(1, m + 1)]
    else:  # a driver, two gates in parallel, and a gate that joins them
        fanin = [[], [0], [0], [1, 2]]
    n = len(fanin)
    r = [rng.uniform(1, 3) for _ in range(n)]
    a = [rng.uniform(1, 3) for _ in range(n)]
    f = [0.0] * (n - 1) + [rng.uniform(5, 20)]
    if shape == "dag":
        f[1] = rng.uniform(0, 4)  # gate 1 also drives some wire
    ckt = Circuit(fanin, [1.0] * n, r, [1.0] * n, a, f, [1.0] * n, [1.0] + [8.0] * (n - 1))
    target = delay(ckt, [1.0] * n) * rng.uniform(0.6, 0.95)
    return ckt, target


def test_against_grid_search(rng=random.Random(1999)):
    checked = 0
    for k in range(24):
        ckt, target = random_case(rng, "chain" if k % 3 else "dag")
        free = sum(1 for i in range(ckt.n) if ckt.lo[i] < ckt.hi[i])
        best = grid_search(ckt, target, pts=40 if free == 2 else 14)
        if best is None:
            continue  # no sizing in the box meets the target
        x, mu = lr_sizing(ckt, target)
        assert all(ckt.lo[i] - 1e-12 <= x[i] <= ckt.hi[i] + 1e-12 for i in range(ckt.n))
        assert delay(ckt, x) <= target * (1 + TOL)
        assert abs(area(ckt, x) - best) <= TOL * best
        # the multipliers certify the answer: the dual bound is close to it
        q = dual_value(ckt, mu, target)
        assert q <= best * (1 + TOL) and q >= best * (1 - TOL)
        checked += 1
    assert checked >= 15


def test_zero_multiplier_stays_zero_under_projection(rng=random.Random(3)):
    # proportional scaling keeps a zero edge at zero while another edge into
    # the same gate is positive; only a positive update can bring it back
    ckt, _ = random_case(rng, "dag")
    edges = ckt.edges
    join = edges.index((2, 3))
    for _ in range(20):
        mu = [rng.uniform(0.5, 2) for _ in edges]
        mu[join] = 0.0
        assert project(ckt, mu)[join] == 0.0


def test_projection_conserves_flow(rng=random.Random(4)):
    ckt, _ = random_case(rng, "dag")
    for _ in range(50):
        mu = project(ckt, [rng.uniform(0, 3) for _ in ckt.edges])
        for i in range(ckt.n):
            into = sum(m for m, (u, v) in zip(mu, ckt.edges) if v == i)
            out = sum(m for m, (u, v) in zip(mu, ckt.edges) if u == i)
            assert abs(into - out) <= 1e-9 * (1 + out)


def test_local_resize_is_optimal(rng=random.Random(6)):
    # the relaxed problem for fixed multipliers is convex in log sizes; the
    # gate by gate closed form must reach the grid minimum
    for _ in range(10):
        ckt, _ = random_case(rng, "chain")
        lam = [rng.uniform(0.1, 2) for _ in range(ckt.n)]
        x = local_resize(ckt, lam, list(ckt.lo), sweeps=5000, tol=1e-14)

        def value(z):
            return area(ckt, z) + sum(lam[i] * gate_delay(ckt, z, i) for i in range(ckt.n))

        free = [i for i in range(ckt.n) if ckt.lo[i] < ckt.hi[i]]
        best = math.inf
        for ys in itertools.product(*[[math.exp(math.log(8) * t / 30) for t in range(31)]] * len(free)):
            z = list(ckt.lo)
            for i, y in zip(free, ys):
                z[i] = y
            best = min(best, value(z))
        assert value(x) <= best + 1e-9


def test_example_of_the_page():
    ckt = Circuit([[], [0], [1]], [1.0] * 3, [1.0, 1.0, 1.0], [1.0] * 3, [1.0] * 3,
                  [0.0, 0.0, 16.0], [1.0, 1.0, 1.0], [1.0, 16.0, 16.0])
    assert delay(ckt, [1.0] * 3) == 21
    x, mu = lr_sizing(ckt, 12.0)
    assert abs(x[1] - 1.2340) < 1e-3 and abs(x[2] - 2.9984) < 1e-3
    assert abs(delay(ckt, x) - 12) < 1e-3 and abs(area(ckt, x) - 5.2324) < 1e-3
    # on a chain, flow conservation makes all multipliers equal
    assert max(mu) - min(mu) < 1e-9 and abs(mu[0] - 1.0318) < 1e-3
    # the closed forms of the local resizing hold at the answer
    m = mu[0]
    assert abs(x[1] - math.sqrt(m * x[2] / (1 + m))) < 1e-6
    assert abs(x[2] - math.sqrt(m * 16 / (1 + m / x[1]))) < 1e-6
    assert abs(grid_search(ckt, 12.0, pts=40) - area(ckt, x)) < TOL * area(ckt, x)
