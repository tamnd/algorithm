# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayes-filter/. The authors are listed in prov/V7B1QT.jsonl.
# The tests of the shared helper robest.py are in this file too.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

import robest
from bayes_filter import bayes_filter, run_bayes_filter

# ---------------------------------------------------------------------------
# The door example of Thrun, Burgard and Fox (2005), Section 2.4.2.
# State 0 is "open", state 1 is "closed".

SENSE = {("open", 0): F(3, 5), ("closed", 0): F(2, 5), ("open", 1): F(1, 5), ("closed", 1): F(4, 5)}


def door_motion(x, u, xp):
    if u == "nothing":
        return F(1) if x == xp else F(0)
    # u == "push": an open door stays open, a closed door opens with 0.8
    if xp == 0:
        return F(1) if x == 0 else F(0)
    return F(4, 5) if x == 0 else F(1, 5)


def door_sense(z, x):
    return SENSE[(z, x)]


def test_door_example_exact():
    bels = run_bayes_filter([F(1, 2), F(1, 2)], ["nothing", "push"], ["open", "open"], door_motion, door_sense)
    assert bels[0] == [F(3, 4), F(1, 4)]
    assert bels[1] == [F(57, 58), F(1, 58)]
    assert abs(float(bels[1][0]) - 0.98276) < 1e-5


# ---------------------------------------------------------------------------
# A cyclic corridor of 6 cells with doors at cells 0, 1 and 3.

N_CELLS = 6
DOORS = {0, 1, 3}
STEP = {0: F(1, 10), 1: F(4, 5), 2: F(1, 10)}  # move by 0, 1 or 2 cells


def corridor_motion(x, u, xp):
    """The command u = 1 asks for one cell forward; the robot moves 0, 1 or 2 cells."""
    return STEP.get((x - xp) % N_CELLS, F(0))


def corridor_sense(z, x):
    hit = F(3, 4) if x in DOORS else F(1, 5)
    return hit if z == "door" else 1 - hit


def brute_force_posterior(bel0, controls, measurements):
    """p(x_T | z_1:T, u_1:T) by summing the joint over all state paths."""
    T = len(controls)
    post = [F(0)] * N_CELLS
    for path in itertools.product(range(N_CELLS), repeat=T + 1):
        p = bel0[path[0]]
        for t in range(1, T + 1):
            u, z = controls[t - 1], measurements[t - 1]
            if u is not None:
                p *= corridor_motion(path[t], u, path[t - 1])
            elif path[t] != path[t - 1]:
                p = F(0)
            if z is not None:
                p *= corridor_sense(z, path[t])
            if p == 0:
                break
        post[path[T]] += p
    total = sum(post)
    return [v / total for v in post]


def test_corridor_motion_is_a_distribution():
    for xp in range(N_CELLS):
        assert sum(corridor_motion(x, 1, xp) for x in range(N_CELLS)) == 1


@pytest.mark.parametrize(
    "controls, measurements",
    [
        ([1, 1, 1, 1], ["door", "door", "wall", "door"]),
        ([None, 1, 1, 1], ["door", None, "wall", "door"]),
        ([1, 1, None, 1], ["wall", "wall", "door", None]),
    ],
)
def test_matches_brute_force_over_paths(controls, measurements):
    bel0 = [F(1, N_CELLS)] * N_CELLS
    bels = run_bayes_filter(bel0, controls, measurements, corridor_motion, corridor_sense)
    assert bels[-1] == brute_force_posterior(bel0, controls, measurements)
    for b in bels:
        assert sum(b) == 1 and all(v >= 0 for v in b)


def test_zero_probability_measurement_raises():
    def never(z, x):
        return F(0)

    with pytest.raises(ValueError):
        bayes_filter([F(1, 2), F(1, 2)], None, "z", door_motion, never)


def test_particle_filter_agrees_with_exact_filter():
    """A particle version with the low variance sampler of robest is close to the exact belief."""
    rng = random.Random(11)
    controls = [1, 1, 1, 1, 1]
    measurements = ["door", "door", "wall", "door", "wall"]
    exact = run_bayes_filter([F(1, N_CELLS)] * N_CELLS, controls, measurements, corridor_motion, corridor_sense)[-1]
    n = 1000
    particles = [rng.randrange(N_CELLS) for _ in range(n)]
    weights = None
    for u, z in zip(controls, measurements):
        if weights is not None:
            idx = robest.low_variance_resample(rng, weights)
            particles = [particles[i] for i in idx]
        moved = []
        for xp in particles:
            r = rng.random()
            moved.append((xp + (0 if r < 0.1 else 1 if r < 0.9 else 2)) % N_CELLS)
        particles = moved
        weights = [float(corridor_sense(z, x)) for x in particles]
    total = sum(weights)
    est = [0.0] * N_CELLS
    for x, w in zip(particles, weights):
        est[x] += w / total
    assert max(abs(a - float(b)) for a, b in zip(est, exact)) < 0.05


# ---------------------------------------------------------------------------
# The shared helper robest.py.


def test_logodds_check_values():
    assert abs(robest.logodds(0.7) - 0.84730) < 1e-5
    assert abs(robest.logodds(0.6) - 0.40547) < 1e-5
    assert robest.logodds(0.5) == 0.0
    for p in (1e-9, 0.1, 0.3, 0.5, 0.7, 0.999999):
        assert abs(robest.prob_from_logodds(robest.logodds(p)) - p) < 1e-12
    assert robest.prob_from_logodds(1000.0) == 1.0
    assert robest.prob_from_logodds(-1000.0) == 0.0
    with pytest.raises(ValueError):
        robest.logodds(1.0)


def test_wrap_angle():
    pi = math.pi
    assert robest.wrap_angle(pi) == -pi
    assert robest.wrap_angle(-pi) == -pi
    assert abs(robest.wrap_angle(3 * pi / 2) + pi / 2) < 1e-12
    assert abs(robest.wrap_angle(-7.0) - (-7.0 + 2 * pi)) < 1e-12
    assert robest.wrap_angle(-1e-17) == -1e-17
    rng = random.Random(3)
    for _ in range(1000):
        a = rng.uniform(-50.0, 50.0)
        w = robest.wrap_angle(a)
        assert -pi <= w < pi
        k = (a - w) / (2 * pi)
        assert abs(k - round(k)) < 1e-9


def test_gauss_sample_mean_and_covariance():
    rng = random.Random(5)
    mean = [1.0, -2.0]
    cov = [[2.0, 0.6], [0.6, 1.0]]
    n = 2000
    xs = [robest.gauss_sample(rng, mean, cov) for _ in range(n)]
    m = [sum(x[i] for x in xs) / n for i in range(2)]
    c = [[sum((x[i] - m[i]) * (x[j] - m[j]) for x in xs) / (n - 1) for j in range(2)] for i in range(2)]
    # standard errors are about 0.03 for the mean and 0.06 for the covariance
    assert all(abs(m[i] - mean[i]) < 0.1 for i in range(2))
    assert all(abs(c[i][j] - cov[i][j]) < 0.2 for i in range(2) for j in range(2))
    s = [robest.gauss_sample(rng, 3.0, 0.25) for _ in range(n)]
    assert abs(sum(s) / n - 3.0) < 0.05


def test_gauss_pdf_and_mahalanobis():
    cov = [[4.0, 0.0], [0.0, 1.0]]
    assert abs(robest.mahalanobis2([2.0, 1.0], [0.0, 0.0], cov) - 2.0) < 1e-12
    assert abs(robest.mahalanobis2(3.0, 1.0, 4.0) - 1.0) < 1e-12
    p = robest.gauss_pdf([2.0, 1.0], [0.0, 0.0], cov)
    assert abs(p - robest.gauss_pdf(2.0, 0.0, 4.0) * robest.gauss_pdf(1.0, 0.0, 1.0)) < 1e-15
    assert abs(robest.gauss_pdf(0.0, 0.0, 1.0) - 1 / math.sqrt(2 * math.pi)) < 1e-15
    h = 0.01
    area = sum(robest.gauss_pdf(-8.0 + h * (k + 0.5), 0.0, 2.0) * h for k in range(1600))
    assert abs(area - 1.0) < 1e-6
    full = [[2.0, 0.6], [0.6, 1.0]]
    assert abs(robest.mahalanobis2([1.0, 1.0], [0.0, 0.0], full) - (1.0 - 1.2 + 2.0) / 1.64) < 1e-12


def test_low_variance_resample():
    rng = random.Random(9)
    w = [0.1, 0.0, 0.25, 0.65]
    for _ in range(200):
        idx = robest.low_variance_resample(rng, w)
        assert len(idx) == 4 and idx == sorted(idx)
        counts = [idx.count(i) for i in range(4)]
        assert counts[1] == 0
        for i in range(4):
            assert math.floor(4 * w[i]) <= counts[i] <= math.ceil(4 * w[i])
    assert robest.low_variance_resample(rng, [5.0]) == [0]
    with pytest.raises(ValueError):
        robest.low_variance_resample(rng, [0.0, 0.0])


def _chi2_cdf(x, k):
    if k == 1:
        return math.erf(math.sqrt(x / 2))
    if k == 2:
        return 1 - math.exp(-x / 2)
    return math.erf(math.sqrt(x / 2)) - math.sqrt(2 * x / math.pi) * math.exp(-x / 2)


def test_chi2_table():
    assert len(robest.CHI2) == 6
    for (k, level), q in robest.CHI2.items():
        assert abs(_chi2_cdf(q, k) - level) < 2e-4
