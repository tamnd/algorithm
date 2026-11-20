# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geiger-method/. The authors are listed in prov/9PWX4B.jsonl.
"""Geiger's method: earthquake location by Gauss-Newton on arrival times.

Stations s_i = (x, y, z) in m (z positive down) record P arrival times T_i
in s. In a medium with the constant velocity v, the predicted time from a
source at h = (x, y, z) with origin time t0 is t0 + |h - s_i| / v. Each step
linearizes the times around the current guess and solves the normal
equations G^T G dm = G^T r for the update dm = (dx, dy, dz, dt0).
"""

import math

import imgla as la


def distance(h, s):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(h, s)))


def predicted_times(m, stations, v):
    """t0 + |h - s_i| / v for the model m = (x, y, z, t0)."""
    h, t0 = m[:3], m[3]
    return [t0 + distance(h, s) / v for s in stations]


def jacobian(m, stations, v):
    """Rows ((x - s_x) / (v D), (y - s_y) / (v D), (z - s_z) / (v D), 1), D = |h - s_i|."""
    h = m[:3]
    rows = []
    for s in stations:
        d = distance(h, s)
        rows.append([(h[0] - s[0]) / (v * d), (h[1] - s[1]) / (v * d), (h[2] - s[2]) / (v * d), 1.0])
    return rows


def misfit(m, stations, times, v):
    """The sum of squared residuals sum_i (T_i - predicted_i)^2."""
    return sum((t - p) ** 2 for t, p in zip(times, predicted_times(m, stations, v)))


def geiger(stations, times, v, m0, iters=20, damping=0.0, tol=1e-10,
           max_step=None, keep_below_surface=False):
    """Locate a source. Returns (m, history of misfits).

    With the defaults this is plain Gauss-Newton, as Geiger proposed. Three
    safeguards are heuristics and are off by default: damping > 0 adds
    damping * I to G^T G (a Levenberg step); max_step (in m) scales the
    update down so that the hypocenter moves at most that far; and
    keep_below_surface replaces a negative depth z by -z, which gives the
    same times when every station is at z = 0. The loop stops when the
    update is shorter than tol (in m and s) or after iters steps.
    """
    m = list(m0)  # @line L1
    history = [misfit(m, stations, times, v)]
    for _ in range(iters):  # @line L2
        pred = predicted_times(m, stations, v)
        r = [t - p for t, p in zip(times, pred)]  # @line L3
        g = jacobian(m, stations, v)  # @line L4
        gt = la.transpose(g)
        normal = la.matmul(gt, g)
        for i in range(4):
            normal[i][i] += damping
        dm = la.solve(normal, la.matvec(gt, r))  # @line L5
        if max_step is not None:
            size = math.sqrt(dm[0] ** 2 + dm[1] ** 2 + dm[2] ** 2)
            if size > max_step:
                dm = [c * max_step / size for c in dm]
        m = [a + b for a, b in zip(m, dm)]  # @line L6
        if keep_below_surface and m[2] < 0.0:
            m[2] = -m[2]
        history.append(misfit(m, stations, times, v))
        if max(abs(dm[0]), abs(dm[1]), abs(dm[2])) < tol and abs(dm[3]) < tol:
            break
    return m, history  # @line L7


def best_origin_time(h, stations, times, v):
    """For a fixed hypocenter h the least-squares origin time is the mean of T_i - D_i / v."""
    return sum(t - distance(h, s) / v for t, s in zip(times, stations)) / len(times)
