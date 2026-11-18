# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-system/. The authors are listed in prov/8JJ5P6.jsonl.

"""Tests of the Reeves particle system: emission, update and death with fixed seeds."""

import random

from particle_system import Params, ParticleSystem, free_fall


def run(seed, frames, params, dt=1.0 / 30.0):
    rng = random.Random(seed)
    ps = ParticleSystem(params)
    for _ in range(frames):
        ps.step(dt, rng)
    return ps


def busy_params():
    return Params(mean_parts=12.0, var_parts=5.0, radius=0.2, ejection=0.4,
                  mean_speed=5.0, var_speed=1.0, mean_life=20, var_life=6, floor=-1.0)


def test_same_seed_same_state():
    a = run(7, 60, busy_params()).state()
    b = run(7, 60, busy_params()).state()
    c = run(8, 60, busy_params()).state()
    assert a == b
    assert a != c


def test_emission_count_in_range_and_mean():
    p = Params(mean_parts=10.0, delta_mean_parts=0.5, var_parts=4.0, mean_life=1)
    rng = random.Random(3)
    ps = ParticleSystem(p, f0=0)
    total = 0
    frames = 400
    for f in range(frames):
        n = ps.step(0.01, rng)
        mean = 10.0 + 0.5 * f
        assert mean - 4.0 - 0.5 <= n <= mean + 4.0 + 0.5
        total += n - mean
    # Rand() has mean 0, so the average excess is near 0 (a measurement with a fixed seed).
    assert abs(total / frames) < 0.3


def test_lifetime_in_frames():
    # With no variance, m particles are born per frame and each lives L frames.
    m, life = 3, 5
    p = Params(mean_parts=float(m), mean_life=life, accel=(0.0, 0.0))
    rng = random.Random(1)
    ps = ParticleSystem(p)
    seen = {}
    for f in range(12):
        ps.step(0.1, rng)
        assert ps.alive() == m * min(f + 1, life)
        for ident, _, _, _ in ps.state():
            seen[ident] = seen.get(ident, 0) + 1
    born_early = [i for i in seen if i < m * (12 - life)]
    assert born_early and all(seen[i] == life for i in born_early)


def test_random_lifetimes_bounded():
    p = busy_params()
    p.floor = None
    rng = random.Random(11)
    ps = ParticleSystem(p)
    frames_alive = {}
    for _ in range(80):
        ps.step(1.0 / 30.0, rng)
        for ident, _, _, _ in ps.state():
            frames_alive[ident] = frames_alive.get(ident, 0) + 1
    finished = [k for k in frames_alive if k < 300]
    assert all(14 <= frames_alive[k] <= 26 for k in finished)


def test_floor_kills():
    # A particle that falls below the floor in one frame is removed in the next one.
    p = Params(mean_parts=5.0, var_parts=2.0, mean_speed=1.0, mean_life=1000, floor=-1.0)
    rng = random.Random(2)
    ps = ParticleSystem(p)
    below = set()
    killed = 0
    for _ in range(60):
        ps.step(0.05, rng)
        ids = {q.ident for q in ps.particles}
        assert not (below & ids)
        killed += len(below)
        below = {q.ident for q in ps.particles if q.x[1] < -1.0}
    assert killed > 0


def test_free_fall_check_value():
    p = Params(mean_parts=1.0, mean_speed=0.0, mean_life=100)
    rng = random.Random(0)
    ps = ParticleSystem(p)
    ps.step(0.1, rng)
    p.mean_parts = 0.0
    for _ in range(9):
        ps.step(0.1, rng)
    (q,) = ps.particles
    assert abs(q.x[1] - (-5.3955)) < 1e-12
    assert abs(free_fall(0.0, 10, 0.1) - (-5.3955)) < 1e-12
    assert abs(free_fall(0.0, 10, 0.1, order="explicit") - (-4.4145)) < 1e-12
    assert abs(-0.5 * 9.81 * 1.0 ** 2 - (-4.905)) < 1e-12


def test_straight_lines_without_forces():
    p = Params(mean_parts=4.0, var_parts=2.0, ejection=1.0, mean_speed=2.0, var_speed=1.0,
               mean_life=30, accel=(0.0, 0.0))
    rng = random.Random(5)
    ps = ParticleSystem(p)
    ps.step(0.1, rng)
    start = {q.ident: (q.x, q.v) for q in ps.particles}
    p.mean_parts = 0.0
    p.var_parts = 0.0
    for _ in range(10):
        ps.step(0.1, rng)
    for q in ps.particles:
        x0, v0 = start[q.ident]
        assert q.v == v0
        assert abs(q.x[0] - (x0[0] + 1.0 * v0[0])) < 1e-12
        assert abs(q.x[1] - (x0[1] + 1.0 * v0[1])) < 1e-12
