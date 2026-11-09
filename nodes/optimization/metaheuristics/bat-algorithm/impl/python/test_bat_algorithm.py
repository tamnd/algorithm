# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bat-algorithm/. The authors are listed in prov/F7GN0A.jsonl.

import math
import random

from bat_algorithm import bat_algorithm, rastrigin, sphere, velocity_step


def test_velocity_step_example() -> None:
    # The example of the page: bat (3, 1), best (-1, 0), v = 0.
    y, v = velocity_step([3.0, 1.0], [0.0, 0.0], [-1.0, 0.0], 1.0)
    assert v == [4.0, 1.0] and y == [7.0, 2.0]  # pushed away from the best point
    y, v = velocity_step([3.0, 1.0], [0.0, 0.0], [-1.0, 0.0], -1.0)
    assert v == [-4.0, -1.0] and y == [-1.0, 0.0]  # a negative frequency pulls
    # Next iteration: the bat sits on the best point, but the old velocity still carries it away.
    y, v = velocity_step([-0.7, -0.2], [4.0, 1.0], [-0.7, -0.2], 1.5)
    assert v == [4.0, 1.0] and math.isclose(y[0], 3.3) and math.isclose(y[1], 0.8)
    assert math.isclose(sphere(y), 11.53)
    assert math.isclose(0.5 * (1.0 - math.exp(-0.9)), 0.29671517012970045, rel_tol=1e-12)


def test_velocity_grows_while_a_bat_is_not_moved() -> None:
    # If x and the best point stay fixed, v = v0 + (sum of q) (x - best): it grows without bound.
    rng = random.Random(3)
    x, best, v0 = [1.0, -2.0, 0.5], [0.0, 0.0, 0.0], [0.3, 0.1, -0.2]
    v, total = list(v0), 0.0
    for _ in range(200):
        q = rng.uniform(0.0, 2.0)
        total += q
        _, v = velocity_step(x, v, best, q)
    assert all(math.isclose(vk, v0k + total * (xk - bk), rel_tol=1e-9) for vk, v0k, xk, bk in zip(v, v0, x, best))
    assert total > 150  # so |v_1| > 150, far outside any box of width 10


def follow(q: float, e0: float, steps: int) -> list[float]:
    """Errors e_t = x_t - best when every velocity proposal is accepted (PSO with inertia 1)."""
    x, v, out = [e0], [0.0], [e0]
    for _ in range(steps):
        x, v = velocity_step(x, v, [0.0], q)
        out.append(x[0])
    return out


def test_fixed_frequency_recurrence() -> None:
    for q in (-0.5, -1.0, -3.0, 0.5, 1.0):
        e = follow(q, 1.0, 60)
        tau = 2.0 + q
        for t in range(1, 60):
            assert math.isclose(e[t + 1], tau * e[t] - e[t - 1], rel_tol=1e-9, abs_tol=1e-9)
    # Pull with 0 < |q| < 4: the quadratic form e_t^2 - tau e_t e_(t-1) + e_(t-1)^2 is conserved, so no convergence.
    e = follow(-1.0, 1.0, 200)
    forms = [e[t] ** 2 - 1.0 * e[t] * e[t - 1] + e[t - 1] ** 2 for t in range(1, 201)]
    assert all(math.isclose(c, forms[0], rel_tol=1e-9) for c in forms)
    assert max(abs(z) for z in e[100:]) > 0.5
    # Push (the sign of the paper) with q = 1: growth by the factor (3 + sqrt 5) / 2.
    e = follow(1.0, 1.0, 40)
    assert math.isclose(e[40] / e[39], (3 + math.sqrt(5)) / 2, rel_tol=1e-12)


def test_run_invariants() -> None:
    n, d, a0, r0, alpha, gamma = 6, 3, 1.0, 0.5, 0.9, 0.9
    rng = random.Random(11)
    start = [[rng.uniform(-5.12, 5.12) for _ in range(d)] for _ in range(n)]
    cur = [rastrigin(p) for p in start]
    count = [0] * n
    last = [0] * n
    evaluated = list(cur)

    def check(t, i, y, fy, local, accept, loud, rate):
        assert all(-5.12 <= v <= 5.12 for v in y)
        assert fy == rastrigin(y)
        evaluated.append(fy)
        if accept:
            assert fy < cur[i]
            cur[i] = fy
            count[i] += 1
            last[i] = t
        a = a0
        for _ in range(count[i]):
            a *= alpha
        assert loud == a
        assert rate == (r0 * (1.0 - math.exp(-gamma * last[i])) if count[i] else 0.0)

    g, fg, hist = bat_algorithm(rastrigin, [-5.12] * d, [5.12] * d, n, 0.0, 2.0, a0, r0, alpha, gamma, 60, random.Random(11), check)
    assert fg == min(evaluated) and fg == rastrigin(g)
    assert all(hist[t + 1] <= hist[t] for t in range(len(hist) - 1))
    assert sum(count) > 0


def test_fixed_seed_run_and_the_role_of_the_velocity() -> None:
    stats = {"vel": 0, "vel_border": 0, "vel_accepted": 0, "local_accepted": 0}

    def count(t, i, y, fy, local, accept, loud, rate):
        if local:
            stats["local_accepted"] += accept
        else:
            stats["vel"] += 1
            stats["vel_border"] += any(abs(v) == 5.12 for v in y)
            stats["vel_accepted"] += accept

    g, fg, _ = bat_algorithm(sphere, [-5.12] * 5, [5.12] * 5, 20, 0.0, 2.0, 1.0, 0.5, 0.9, 0.9, 500, random.Random(0), count)
    assert fg < 0.02 and fg == sphere(g)
    # Measured in this run: no velocity proposal was accepted, and 4911 of the 4956 lay on the border of the box.
    assert stats == {"vel": 4956, "vel_border": 4911, "vel_accepted": 0, "local_accepted": 153}
