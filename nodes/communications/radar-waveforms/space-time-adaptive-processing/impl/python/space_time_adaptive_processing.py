# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/space-time-adaptive-processing/. The authors are listed in prov/STKZ5N.jsonl.

"""Sample matrix inversion (SMI) space-time adaptive processing.

An array of M elements receives P pulses. One range bin gives a space-time
snapshot x of length D = M P, ordered as x[p M + m] (pulse p, element m).
The target steering vector is v = b(f_t) kron a(f_s), with the spatial
vector a[m] = e^(j 2 pi f_s m) and the temporal vector b[p] = e^(j 2 pi f_t p);
f_s = (d / lambda) sin(theta) and f_t = f_d / PRF are normalized frequencies.

SMI estimates the clutter plus noise covariance from T training snapshots
of nearby range bins, R = (1/T) sum x_t x_t^H, adds diagonal loading delta I,
and uses the weight w = R^-1 v. The output is y = w^H x and the adaptive
matched filter (AMF) statistic is |w^H x|^2 / (v^H w).
"""

import cmath
import math
from typing import Sequence

from cbb import cholesky


def steering(m_count: int, p_count: int, fs: float, ft: float) -> list[complex]:
    """v[p M + m] = e^(j 2 pi (ft p + fs m)), that is b(ft) kron a(fs)."""
    return [cmath.exp(2j * math.pi * (ft * p + fs * m)) for p in range(p_count) for m in range(m_count)]


def sample_covariance(training: Sequence[Sequence[complex]]) -> list[list[complex]]:
    """R = (1/T) sum over t of x_t x_t^H. Cost Theta(T D^2)."""
    t_count = len(training)
    d = len(training[0])
    r = [[0j] * d for _ in range(d)]
    for x in training:
        for i in range(d):
            xi = x[i]
            ri = r[i]
            for k in range(d):
                ri[k] += xi * x[k].conjugate()
    return [[v / t_count for v in row] for row in r]


def cholesky_solve(g: list[list[complex]], v: Sequence[complex]) -> list[complex]:
    """Solve G G^H w = v for a lower triangular G, by a forward and a back substitution."""
    d = len(g)
    a = [0j] * d
    for i in range(d):
        a[i] = (v[i] - sum(g[i][k] * a[k] for k in range(i))) / g[i][i]
    w = [0j] * d
    for i in range(d - 1, -1, -1):
        w[i] = (a[i] - sum(g[k][i].conjugate() * w[k] for k in range(i + 1, d))) / g[i][i].conjugate()
    return w


def smi_stap(training: Sequence[Sequence[complex]], v: Sequence[complex], x: Sequence[complex],
             loading: float = 0.0) -> tuple[list[complex], complex, float]:
    """Return (w, y, amf) for the cell under test x.

    training holds T snapshots of length D; v is the steering vector of length D.
    T >= D is needed when loading is 0, or R is singular.
    Cost: Theta(T D^2 + D^3) time and Theta(D^2) space, with D = M P.
    """
    if not training or any(len(t) != len(v) for t in training) or len(x) != len(v):
        raise ValueError("need T >= 1 snapshots of the length of v")
    d = len(v)
    r = sample_covariance(training)  # @line L1
    for i in range(d):
        r[i][i] += loading  # @line L2
    g = cholesky(r)  # @line L3
    w = cholesky_solve(g, v)  # @line L4
    y = sum(wi.conjugate() * xi for wi, xi in zip(w, x))  # @line L5
    amf = abs(y) ** 2 / sum(vi.conjugate() * wi for vi, wi in zip(v, w)).real  # @line L6
    return w, y, amf  # @line L7


def clutter_covariance(m_count: int, p_count: int, beta: float, patches: int, cnr: float,
                       noise: float = 1.0) -> list[list[complex]]:
    """R = noise I + sum over patches of c v_c v_c^H for a side-looking array.

    Patch c has spatial frequency fs_c spread evenly over [-0.5, 0.5) and the
    Doppler ft_c = beta fs_c (the clutter ridge). The total clutter power over
    all patches, per element and pulse, is cnr * noise.
    """
    d = m_count * p_count
    r = [[complex(noise) if i == k else 0j for k in range(d)] for i in range(d)]
    c = cnr * noise / patches
    for q in range(patches):
        fs = -0.5 + q / patches
        vc = steering(m_count, p_count, fs, beta * fs)
        for i in range(d):
            for k in range(d):
                r[i][k] += c * vc[i] * vc[k].conjugate()
    return r


def sinr(w: Sequence[complex], v: Sequence[complex], r: Sequence[Sequence[complex]]) -> float:
    """|w^H v|^2 / (w^H R w): the output SINR for a unit-power target."""
    num = abs(sum(a.conjugate() * b for a, b in zip(w, v))) ** 2
    rw = [sum(r[i][k] * w[k] for k in range(len(w))) for i in range(len(w))]
    return num / sum(a.conjugate() * b for a, b in zip(w, rw)).real


def brennan_rank(m_count: int, p_count: int, beta: float) -> int:
    """Brennan's rule for the clutter rank: round(M + beta (P - 1))."""
    return round(m_count + beta * (p_count - 1))


def rmb_mean_loss(d: int, t_count: int) -> float:
    """The mean SINR loss of SMI without loading, E rho = (T + 2 - D) / (T + 1), for T >= D."""
    return (t_count + 2 - d) / (t_count + 1)
