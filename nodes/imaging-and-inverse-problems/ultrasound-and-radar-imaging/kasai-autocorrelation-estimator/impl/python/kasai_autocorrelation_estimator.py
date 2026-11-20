# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kasai-autocorrelation-estimator/. The authors are listed in prov/CC9PV7.jsonl.
"""The Kasai autocorrelation (pulse-pair) estimator of the mean Doppler velocity.

The input is the slow time ensemble of complex IQ samples x_g[0 .. N-1] of one
pixel, for G range gates g that are averaged together (G = 1 is the plain
estimator). The pulse repetition frequency is prf, the centre frequency f0 and
the speed of sound c. With the lag-one autocorrelation R1 and the power R0,

    v = c prf arg(R1) / (4 pi f0),
    sigma_v^2 = 2 (c prf / (4 pi f0))^2 (1 - |R1| / R0).

Sign convention: the IQ demodulation multiplies by exp(-i 2 pi f0 t), so an
echo from a scatterer that moves toward the probe has a phase that grows from
pulse to pulse, and v > 0 means motion toward the probe.
"""

import cmath
import math


def aliasing_velocity(c, prf, f0):
    """The largest velocity without aliasing, c prf / (4 f0)."""
    return c * prf / (4.0 * f0)


def doppler_iq(n, v, c, prf, f0, amp=1.0, phase0=0.0):
    """Slow time IQ samples of one scatterer with axial velocity v (toward the probe).

    The round trip delay of pulse k is tau_k = 2 (z0 - v k / prf) / c, so the IQ
    phase -2 pi f0 tau_k grows by 4 pi f0 v / (c prf) per pulse.
    """
    dphi = 4.0 * math.pi * f0 * v / (c * prf)
    return [amp * cmath.exp(1j * (phase0 + dphi * k)) for k in range(n)]


def lag_correlations(gates):
    """R0 = mean |x|^2 and R1 = mean conj(x[k]) x[k+1] over all gates and pulses."""
    g_count, n = len(gates), len(gates[0])
    r0 = sum(abs(v) ** 2 for x in gates for v in x) / (g_count * n)  # @line L1
    r1 = sum(x[k].conjugate() * x[k + 1] for x in gates for k in range(n - 1)) / (g_count * (n - 1))  # @line L2
    return r0, r1


def kasai(gates, c, prf, f0):
    """Return (v, power, sigma_v) for the IQ ensembles of the G gates of one pixel.

    v is the mean axial velocity, power is R0 (the power Doppler value) and
    sigma_v is the spectral width estimate of Kasai et al., in velocity units.
    """
    if len(gates[0]) < 2:
        raise ValueError("the ensemble needs at least two pulses")
    r0, r1 = lag_correlations(gates)
    if r0 == 0:
        return 0.0, 0.0, 0.0
    scale = c * prf / (4.0 * math.pi * f0)
    v = scale * cmath.phase(r1)  # @line L3
    ratio = min(1.0, abs(r1) / r0)
    sigma_v = scale * math.sqrt(2.0 * (1.0 - ratio))  # @line L4
    return v, r0, sigma_v  # @line L5


def kasai_image(ensembles, c, prf, f0, gate_avg=1):
    """Velocity image from ensembles[i][j] = the IQ list of pixel (i, j).

    Each pixel averages R0 and R1 over gate_avg depth samples centred on it
    (rows i - h .. i + h, clipped at the edges, with h = gate_avg // 2).
    """
    rows, cols = len(ensembles), len(ensembles[0])
    h = gate_avg // 2
    out = [[0.0] * cols for _ in range(rows)]
    for i in range(rows):
        lo, hi = max(0, i - h), min(rows, i + h + 1)
        for j in range(cols):
            out[i][j] = kasai([ensembles[r][j] for r in range(lo, hi)], c, prf, f0)[0]
    return out


def periodogram_peak_velocity(x, c, prf, f0, grid=4096):
    """Reference estimate: the velocity at the peak of |sum_k x[k] exp(-i w k)|^2 on a fine grid.

    For one tone in white noise this is the maximum likelihood estimate of the
    frequency. It costs O(N grid), far more than the Kasai estimator.
    """
    best, best_w = -1.0, 0.0
    for q in range(grid):
        w = -math.pi + 2.0 * math.pi * q / grid
        s = sum(v * cmath.exp(-1j * w * k) for k, v in enumerate(x))
        p = abs(s) ** 2
        if p > best:
            best, best_w = p, w
    return c * prf * best_w / (4.0 * math.pi * f0)
