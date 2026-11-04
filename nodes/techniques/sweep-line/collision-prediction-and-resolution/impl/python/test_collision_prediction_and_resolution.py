# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/collision-prediction-and-resolution/. The authors are listed in prov/F02YVH.jsonl.

import math
import random

from collision_prediction_and_resolution import (
    INF,
    Particle,
    bounce_off,
    bounce_off_horizontal_wall,
    bounce_off_vertical_wall,
    simulate,
    time_to_hit,
    time_to_hit_horizontal_wall,
    time_to_hit_vertical_wall,
)

TOL = 1e-9


def close(x: float, y: float, tol: float = TOL) -> bool:
    return abs(x - y) <= tol * max(1.0, abs(x), abs(y))


def momentum(ps: list[Particle]) -> tuple[float, float]:
    return sum(p.m * p.vx for p in ps), sum(p.m * p.vy for p in ps)


def energy(ps: list[Particle]) -> float:
    return sum(p.kinetic_energy() for p in ps)


def example() -> tuple[Particle, Particle]:
    return Particle(0.2, 0.4, 0.3, 0.0, 0.05, 1.0), Particle(0.78, 0.46, -0.2, 0.0, 0.05, 3.0)


def test_worked_example() -> None:
    p, q = example()
    assert close(time_to_hit(p, q), 1.0)
    assert close(time_to_hit(q, p), 1.0)
    assert close(time_to_hit_vertical_wall(p), 2.5)
    assert close(time_to_hit_vertical_wall(q), 3.65)
    assert time_to_hit_horizontal_wall(p) == INF
    p.move(1.0)
    q.move(1.0)
    assert close(q.rx - p.rx, 0.08) and close(q.ry - p.ry, 0.06)
    bounce_off(p, q)
    assert close(p.vx, -0.18) and close(p.vy, -0.36)
    assert close(q.vx, -0.04) and close(q.vy, 0.12)
    assert p.count == 1 and q.count == 1
    assert close(energy([p, q]), 0.105)


def test_worked_trace() -> None:
    p, q = example()
    done = simulate([p, q], 3.0)
    assert [(a, b) for _, a, b in done] == [(0, 1), (-1, 0)]
    assert close(done[0][0], 1.0) and close(done[1][0], 1.0 + 0.35 / 0.36)
    assert close(p.rx, 0.14) and close(p.ry, 0.42)
    assert close(q.rx, 0.50) and close(q.ry, 0.70)
    assert p.count == 2 and q.count == 1


def test_head_on_equal_masses_swap() -> None:
    p = Particle(0.3, 0.5, 0.7, 0.0, 0.05, 2.0)
    q = Particle(0.7, 0.5, -0.1, 0.0, 0.05, 2.0)
    dt = time_to_hit(p, q)
    assert close(dt, 0.3 / 0.8)
    p.move(dt)
    q.move(dt)
    bounce_off(p, q)
    assert close(p.vx, -0.1) and close(q.vx, 0.7)
    assert close(p.vy, 0.0) and close(q.vy, 0.0)


def test_no_collision_cases() -> None:
    p = Particle(0.3, 0.5, 0.0, 0.0)
    assert time_to_hit(p, p) == INF
    # moving apart
    assert time_to_hit(Particle(0.3, 0.5, -0.1, 0.0), Particle(0.6, 0.5, 0.1, 0.0)) == INF
    # same velocity: dv = 0
    assert time_to_hit(Particle(0.3, 0.5, 0.2, 0.1), Particle(0.6, 0.5, 0.2, 0.1)) == INF
    # passing by: approach but miss (d < 0)
    assert time_to_hit(Particle(0.2, 0.2, 0.1, 0.0, 0.01), Particle(0.8, 0.5, -0.1, 0.0, 0.01)) == INF
    # tangent: graze exactly once
    t = time_to_hit(Particle(0.2, 0.5, 0.1, 0.0, 0.01), Particle(0.8, 0.52, -0.1, 0.0, 0.01))
    assert close(t, 3.0)
    # at rest: no wall hit
    assert time_to_hit_vertical_wall(p) == INF
    assert time_to_hit_horizontal_wall(p) == INF


def test_walls() -> None:
    p = Particle(0.5, 0.5, -0.25, 0.5, 0.1)
    assert close(time_to_hit_vertical_wall(p), 1.6)
    assert close(time_to_hit_horizontal_wall(p), 0.8)
    bounce_off_vertical_wall(p)
    bounce_off_horizontal_wall(p)
    assert p.vx == 0.25 and p.vy == -0.5 and p.count == 2


def oracle_time(p: Particle, q: Particle) -> float:
    """First root of f(t) = |dr + t dv|^2 - sigma^2 by bisection, without the formula."""
    dx, dy = q.rx - p.rx, q.ry - p.ry
    dvx, dvy = q.vx - p.vx, q.vy - p.vy
    sigma = p.s + q.s

    def f(t: float) -> float:
        return (dx + t * dvx) ** 2 + (dy + t * dvy) ** 2 - sigma * sigma

    a = dvx * dvx + dvy * dvy
    if a == 0:
        return INF
    tmin = -(dvx * dx + dvy * dy) / a  # the time of the closest approach
    if tmin <= 0 or f(tmin) > 0:
        return INF
    lo, hi = 0.0, tmin  # f(lo) > 0 >= f(hi) and f decreases on [lo, hi]
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return hi


def random_pair(rng: random.Random) -> tuple[Particle, Particle]:
    while True:
        p = Particle(rng.random(), rng.random(), rng.uniform(-1, 1), rng.uniform(-1, 1),
                     rng.uniform(0.01, 0.2), rng.uniform(0.5, 5))
        q = Particle(rng.random(), rng.random(), rng.uniform(-1, 1), rng.uniform(-1, 1),
                     rng.uniform(0.01, 0.2), rng.uniform(0.5, 5))
        if math.hypot(q.rx - p.rx, q.ry - p.ry) > p.s + q.s:
            return p, q


def test_time_to_hit_against_bisection() -> None:
    rng = random.Random(61)
    hits = 0
    for _ in range(4000):
        p, q = random_pair(rng)
        got, want = time_to_hit(p, q), oracle_time(p, q)
        if want == INF:
            assert got == INF
        else:
            hits += 1
            assert close(got, want, 1e-7)
            assert got >= 0
    assert hits >= 500


def test_resolution_conserves_momentum_and_energy() -> None:
    rng = random.Random(62)
    for _ in range(1000):
        p, q = random_pair(rng)
        dt = time_to_hit(p, q)
        if dt == INF:
            continue
        p.move(dt)
        q.move(dt)
        mx, my = momentum([p, q])
        e = energy([p, q])
        dx, dy = q.rx - p.rx, q.ry - p.ry
        dvn = (q.vx - p.vx) * dx + (q.vy - p.vy) * dy
        dvt = (q.vx - p.vx) * -dy + (q.vy - p.vy) * dx
        bounce_off(p, q)
        mx2, my2 = momentum([p, q])
        assert close(mx, mx2) and close(my, my2)
        assert close(e, energy([p, q]))
        assert close((q.vx - p.vx) * dx + (q.vy - p.vy) * dy, -dvn)
        assert close((q.vx - p.vx) * -dy + (q.vy - p.vy) * dx, dvt)
        assert time_to_hit(p, q) == INF


def test_simulation_keeps_disks_apart() -> None:
    rng = random.Random(63)
    for _ in range(20):
        ps: list[Particle] = []
        while len(ps) < 6:
            s = rng.uniform(0.02, 0.06)
            c = Particle(rng.uniform(s, 1 - s), rng.uniform(s, 1 - s),
                         rng.uniform(-1, 1), rng.uniform(-1, 1), s, rng.uniform(0.5, 2))
            if all(math.hypot(c.rx - p.rx, c.ry - p.ry) > c.s + p.s for p in ps):
                ps.append(c)
        e = energy(ps)
        done = simulate(ps, 5.0)
        assert all(done[k][0] <= done[k + 1][0] for k in range(len(done) - 1))
        assert close(e, energy(ps), 1e-7)
        for i, p in enumerate(ps):
            assert -1e-9 <= p.rx - p.s and p.rx + p.s <= 1 + 1e-9
            assert -1e-9 <= p.ry - p.s and p.ry + p.s <= 1 + 1e-9
            for q in ps[i + 1:]:
                assert math.hypot(q.rx - p.rx, q.ry - p.ry) >= p.s + q.s - 1e-7


def test_empty_and_single() -> None:
    assert simulate([], 1.0) == []
    p = Particle(0.5, 0.5, 0.5, 0.0, 0.1)
    done = simulate([p], 1.0)
    assert [(a, b) for _, a, b in done] == [(0, -1)]
    assert close(done[0][0], 0.8)
    assert close(p.rx, 0.8) and p.vx == -0.5
