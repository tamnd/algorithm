# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perfectly-matched-layer/. The authors are listed in prov/D5V4KY.jsonl.

import math

from perfectly_matched_layer import (pml_step, profiles, reflection, sigma_max_for,
                                     theoretical_reflection)


def test_sigma_max_and_theoretical_reflection_are_inverse():
    for R in (1e-2, 1e-6):
        for m in (0, 2, 3):
            s = sigma_max_for(R, 12.0, m)
            assert abs(theoretical_reflection(s, 12.0, m) - R) < 1e-12 * max(1, R)
    s = sigma_max_for(1e-4, 10.0, 2)
    assert theoretical_reflection(s, 10.0, 2, cos_theta=0.5) > 1e-4     # oblique waves see less


def test_profiles_are_zero_inside_and_graded_in_the_layer():
    sE, sH = profiles(30, 5, 1.0, 2.0, 2)
    assert all(v == 0.0 for v in sE[5:26]) and all(v == 0.0 for v in sH[5:25])
    assert sE[0] == sE[30] == 2.0
    assert all(sE[i] > sE[i + 1] for i in range(5))
    assert sH == sH[::-1] and sE == sE[::-1]


def test_conductor_without_layer_reflects_everything():
    assert reflection(0, 0.0, 0, interior=120) > 0.95


def test_layer_with_zero_conductivity_is_just_more_free_space():
    # the pulse goes on into the layer and comes back from the wall behind it
    assert reflection(10, 0.0, 0, interior=120) > 0.95


def test_graded_layer_is_far_better_than_a_step_in_conductivity():
    step = reflection(20, sigma_max_for(1e-6, 20.0, 0), 0, interior=120)
    graded = reflection(20, sigma_max_for(1e-6, 20.0, 2), 2, interior=120)
    assert step > 0.05 and graded < 1e-4


def test_discrete_reflection_falls_as_the_layer_gets_thicker():
    r = [reflection(N, sigma_max_for(1e-6, float(N), 2), 2, interior=120) for N in (5, 10, 20)]
    assert r[0] > r[1] > r[2]
    assert r[0] > 1e-6                          # the discrete layer is not perfect


def test_a_weak_smooth_layer_reaches_its_design_reflection():
    R = 1e-2
    got = reflection(20, sigma_max_for(R, 20.0, 3), 3, interior=120)
    assert 0.8 * R < got < 1.2 * R


def test_unmatched_layer_reflects():
    # loss only in E breaks the impedance match: E_t + sigma E = H_x, H_t = E_x
    n, npml, dx, dt = 200, 20, 1.0, 0.5
    smax = sigma_max_for(1e-6, 20.0, 2)
    x0, width = 100.0, 6.0
    out = []
    for matched in (True, False):
        sE, sH = profiles(n, npml, dx, smax, 2)
        if not matched:
            sH = [0.0] * n
        E = [math.exp(-((i - x0) / width) ** 2) for i in range(n + 1)]
        H = [-math.exp(-((i + 0.5 + dt / 2 - x0) / width) ** 2) for i in range(n)]
        E[0] = E[n] = 0.0
        for _ in range(int(2 * (80 + 40 + 30))):
            pml_step(E, H, sE, sH, dx, dt)
        out.append(max(abs(v) for v in E[npml:n - npml]))
    assert out[0] < 1e-3 and out[1] > 10 * out[0]
