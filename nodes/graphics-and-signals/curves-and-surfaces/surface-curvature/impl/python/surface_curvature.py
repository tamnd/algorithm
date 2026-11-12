# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-curvature/. The authors are listed in prov/N0S7K8.jsonl.

"""Gaussian, mean and principal curvatures of a parametric surface at a point.

The input is the five partials S_u, S_v, S_uu, S_uv, S_vv at the point. The
unit normal is n = S_u x S_v / |S_u x S_v|, so the sign of H and of the
principal curvatures follows the orientation of the parametrization. K does
not depend on the orientation.
"""

import math
from typing import Callable, List, Tuple

Vec = Tuple[float, float, float]
Forms = Tuple[float, float, float, float, float, float]


def _dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def forms_from_partials(su: Vec, sv: Vec, suu: Vec, suv: Vec, svv: Vec) -> Forms:
    """(E, F, G, L, M, N). Raises ValueError where S_u and S_v are parallel."""
    nn = _cross(su, sv)
    w = math.sqrt(_dot(nn, nn))
    if w == 0:
        raise ValueError("the parametrization is not regular at this point")
    n = (nn[0] / w, nn[1] / w, nn[2] / w)
    return (_dot(su, su), _dot(su, sv), _dot(sv, sv), _dot(suu, n), _dot(suv, n), _dot(svv, n))


def gaussian_curvature(forms: Forms) -> float:
    e, f, g, ell, m, n = forms
    return (ell * n - m * m) / (e * g - f * f)  # @line L1 L2


def mean_curvature(forms: Forms) -> float:
    e, f, g, ell, m, n = forms
    return (e * n - 2 * f * m + g * ell) / (2 * (e * g - f * f))  # @line L3


def shape_operator(forms: Forms) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """The matrix W = I^(-1) II of the Weingarten map in the basis S_u, S_v."""
    e, f, g, ell, m, n = forms
    d = e * g - f * f
    return ((g * ell - f * m) / d, (g * m - f * n) / d), ((e * m - f * ell) / d, (e * n - f * m) / d)


def principal_curvatures(forms: Forms) -> Tuple[float, float]:
    """(k1, k2) with k1 >= k2, from k = H +- sqrt(H^2 - K)."""
    h, k = mean_curvature(forms), gaussian_curvature(forms)
    # H^2 - K >= 0 in exact arithmetic; the max guards against rounding.
    r = math.sqrt(max(0.0, h * h - k))  # @line L4
    return h + r, h - r  # @line L5


def principal_directions(forms: Forms, rel: float = 1e-12) -> List[Tuple[Tuple[float, float], float]]:
    """[(d1, k1), (d2, k2)]: the eigenvectors of W in (u, v) coordinates, not normalized.

    At an umbilic (k1 = k2) every direction is principal; the function then
    returns S_u and the direction that is orthogonal to it in the first form.
    """
    e, f, g = forms[:3]
    k1, k2 = principal_curvatures(forms)
    h, k = mean_curvature(forms), gaussian_curvature(forms)
    if h * h - k <= rel * max(h * h, abs(k)):
        # the discriminant is at the rounding level, so k1 - k2 is about sqrt(rel) or less
        return [((1.0, 0.0), k1), ((-f, e), k2)]
    (a, b), (c, d) = shape_operator(forms)
    out = []
    for k in (k1, k2):
        x = (b, k - a)                     # the first row of (W - kI) x = 0
        y = (k - d, c)                     # the second row
        out.append((x if math.hypot(*x) >= math.hypot(*y) else y, k))
    return out


def normal_curvature(forms: Forms, d: Tuple[float, float]) -> float:
    e, f, g, ell, m, n = forms
    x, y = d
    return (ell * x * x + 2 * m * x * y + n * y * y) / (e * x * x + 2 * f * x * y + g * y * y)


def total_curvature(partials: Callable, u0: float, u1: float, v0: float, v1: float, n: int = 80) -> float:
    """The integral of K dA = K sqrt(EG - F^2) du dv over a rectangle, by product Simpson."""
    if n % 2:
        n += 1
    hu, hv = (u1 - u0) / n, (v1 - v0) / n
    w = [1 if k in (0, n) else (4 if k % 2 else 2) for k in range(n + 1)]
    acc = 0.0
    for i in range(n + 1):
        for j in range(n + 1):
            su, sv, suu, suv, svv = partials(u0 + i * hu, v0 + j * hv)
            nn = _cross(su, sv)
            w2 = _dot(nn, nn)
            if w2 == 0:
                continue                   # a pole; it has measure zero
            # K dA = (LN - M^2) / sqrt(EG - F^2) with L, M, N taken against the unnormalized normal
            ell, m, nv = _dot(suu, nn), _dot(suv, nn), _dot(svv, nn)
            acc += w[i] * w[j] * (ell * nv - m * m) / (w2 * math.sqrt(w2))
    return acc * hu * hv / 9
