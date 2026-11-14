# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/obrien-fleming-boundary/. The authors are listed in prov/C11SHN.jsonl.
"""O'Brien-Fleming and Pocock group sequential boundaries.

The statistics Z_1, ..., Z_K follow the canonical joint distribution: the score
S_k = Z_k sqrt(I_k) is a Brownian motion with drift theta observed at the
information levels I_1 < ... < I_K. A two-sided boundary c_1, ..., c_K rejects
H_0 at the first k with |Z_k| >= c_k.

The crossing probabilities are computed by recursive numerical integration
(Armitage, McPherson and Rowe 1969): the sub-density of S_k on the event that
no earlier boundary was crossed is carried from stage to stage on a Simpson
grid. The grid spacing is at most sqrt(I_k - I_(k-1)) / r, so the work of one
evaluation is O(K m^2) for m grid points per stage.
"""

import math
from collections.abc import Callable, Sequence

_SQRT2 = math.sqrt(2.0)
_INV_SQRT_2PI = 1.0 / math.sqrt(2.0 * math.pi)


def _norm_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / _SQRT2)


def _norm_sf(x: float) -> float:
    return 0.5 * math.erfc(x / _SQRT2)


def _norm_pdf(x: float) -> float:
    return _INV_SQRT_2PI * math.exp(-0.5 * x * x)


def norm_quantile(p: float) -> float:
    """The lower p-quantile of the standard normal, by bisection on erfc to 1e-15."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    lo, hi = -40.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _norm_cdf(mid) < p:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-15:
            break
    return 0.5 * (lo + hi)


def _simpson_grid(b: float, step: float) -> tuple[list[float], list[float]]:
    """Points and Simpson weights on [-b, b] with an even number of intervals of length <= step."""
    n = max(2, 2 * math.ceil(b / step))
    h = 2.0 * b / n
    xs = [-b + i * h for i in range(n + 1)]
    ws = [(1.0 if i in (0, n) else (4.0 if i % 2 else 2.0)) * h / 3.0 for i in range(n + 1)]
    return xs, ws


def crossing_probabilities(c: Sequence[float], info: Sequence[float], theta: float = 0.0,
                           r: int = 16) -> list[tuple[float, float]]:
    """Per-stage crossing probabilities of the two-sided boundary c on the z scale.

    Returns a list of pairs (upper_k, lower_k): the probabilities of stopping at
    analysis k with Z_k >= c_k or with Z_k <= -c_k, with no earlier crossing,
    when the score has drift theta per unit of information. Precondition:
    0 < info[0] < info[1] < ..., c_k > 0. Cost O(K m^2) with m about
    2 b_k r / sqrt(I_k - I_(k-1)) grid points at stage k.
    """
    if len(c) != len(info) or not c:
        raise ValueError("c and info must have the same positive length")
    out = []
    b = c[0] * math.sqrt(info[0])
    sd = math.sqrt(info[0])
    mu = theta * info[0]
    out.append((_norm_sf((b - mu) / sd), _norm_cdf((-b - mu) / sd)))
    xs, ws = _simpson_grid(b, sd / r)
    g = [_norm_pdf((x - mu) / sd) / sd for x in xs]
    for k in range(1, len(c)):
        delta = info[k] - info[k - 1]
        if delta <= 0:
            raise ValueError("information levels must increase")
        sd = math.sqrt(delta)
        mu = theta * delta
        b = c[k] * math.sqrt(info[k])
        up = sum(w * gu * _norm_sf((b - u - mu) / sd) for u, w, gu in zip(xs, ws, g))
        lo = sum(w * gu * _norm_cdf((-b - u - mu) / sd) for u, w, gu in zip(xs, ws, g))
        out.append((up, lo))
        if k + 1 < len(c):
            nxs, nws = _simpson_grid(b, min(sd, math.sqrt(info[k + 1] - info[k])) / r)
            wg = [w * gu for w, gu in zip(ws, g)]
            g = [sum(a * _norm_pdf((s - u - mu) / sd) for u, a in zip(xs, wg)) / sd for s in nxs]
            xs, ws = nxs, nws
    return out


def total_crossing(c: Sequence[float], info: Sequence[float], theta: float = 0.0, r: int = 16) -> float:
    """P(|Z_k| >= c_k for some k) under drift theta (two-sided rejection probability)."""
    return sum(u + l for u, l in crossing_probabilities(c, info, theta, r))


def _shape(kind: str, info: Sequence[float]) -> list[float]:
    if kind == "obrien-fleming":
        return [math.sqrt(info[-1] / i) for i in info]
    if kind == "pocock":
        return [1.0 for _ in info]
    raise ValueError("kind must be 'obrien-fleming' or 'pocock'")


def boundary_constant(kind: str, k_looks: int, alpha: float = 0.05, info: Sequence[float] | None = None,
                      tol: float = 1e-9, r: int = 16,
                      cross: Callable[..., float] | None = None) -> tuple[float, list[float]]:
    """The constant C and the z-scale boundary c_k = C shape_k at two-sided level alpha.

    kind is "obrien-fleming" (c_k = C sqrt(I_K / I_k)) or "pocock" (c_k = C).
    info defaults to equal spacing 1, 2, ..., K. Bisection on C to width tol;
    each step costs one evaluation of total_crossing.
    """
    if info is None:
        info = [float(i) for i in range(1, k_looks + 1)]
    if len(info) != k_looks or k_looks < 1:
        raise ValueError("info must have k_looks entries")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0, 1)")
    cross = cross or total_crossing
    shape = _shape(kind, info)
    lo = norm_quantile(1.0 - alpha / 2.0)  # @line L1
    hi = norm_quantile(1.0 - alpha / (2.0 * k_looks))  # @line L1
    while hi - lo > tol:  # @line L2
        mid = 0.5 * (lo + hi)  # @line L3
        if cross([mid * s for s in shape], info, 0.0, r) > alpha:  # @line L4
            lo = mid
        else:
            hi = mid
    big_c = 0.5 * (lo + hi)
    return big_c, [big_c * s for s in shape]  # @line L5


def obrien_fleming_boundary(k_looks: int, alpha: float = 0.05, info: Sequence[float] | None = None,
                            tol: float = 1e-9, r: int = 16) -> tuple[float, list[float]]:
    """O'Brien-Fleming: c_k = C sqrt(I_K / I_k), two-sided level alpha.

    Returns (C, [c_1, ..., c_K]). For K = 5 equally spaced looks and
    alpha = 0.05, C is about 2.0401.
    """
    return boundary_constant("obrien-fleming", k_looks, alpha, info, tol, r)


def pocock_boundary(k_looks: int, alpha: float = 0.05, info: Sequence[float] | None = None,
                    tol: float = 1e-9, r: int = 16) -> tuple[float, list[float]]:
    """Pocock: c_k = C at every look, two-sided level alpha."""
    return boundary_constant("pocock", k_looks, alpha, info, tol, r)


def cross_on_score_scale(big_c: float, info: Sequence[float], r: int = 16) -> float:
    """CROSS(C, I) of the pseudocode: the O'Brien-Fleming boundary is |S_k| >= C sqrt(I_K)."""
    b = big_c * math.sqrt(info[-1])  # @line L6
    sd = math.sqrt(info[0])
    p = 2.0 * _norm_sf(b / sd)  # @line L7
    xs, ws = _simpson_grid(b, sd / r)
    g = [_norm_pdf(x / sd) / sd for x in xs]  # @line L7
    for k in range(1, len(info)):  # @line L8
        sd = math.sqrt(info[k] - info[k - 1])  # @line L9
        p += sum(w * gu * (_norm_cdf((-b - u) / sd) + _norm_sf((b - u) / sd))  # @line L10
                 for u, w, gu in zip(xs, ws, g))
        if k + 1 < len(info):
            nxs, nws = _simpson_grid(b, min(sd, math.sqrt(info[k + 1] - info[k])) / r)
            wg = [w * gu for w, gu in zip(ws, g)]
            g = [sum(a * _norm_pdf((s - u) / sd) for u, a in zip(xs, wg)) / sd for s in nxs]  # @line L11
            xs, ws = nxs, nws
    return p  # @line L12


def expected_information(c: Sequence[float], info: Sequence[float], theta: float = 0.0, r: int = 16) -> float:
    """E[I_T], the expected information at stopping, where T is the stage of stopping (K if no crossing)."""
    probs = crossing_probabilities(c, info, theta, r)
    stop = [u + l for u, l in probs]
    return sum(p * i for p, i in zip(stop[:-1], info[:-1])) + (1.0 - sum(stop[:-1])) * info[-1]
