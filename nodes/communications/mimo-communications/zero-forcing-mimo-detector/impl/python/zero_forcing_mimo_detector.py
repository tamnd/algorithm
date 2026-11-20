# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-forcing-mimo-detector/. The authors are listed in prov/Q1ZTZN.jsonl.

"""The zero-forcing (ZF) MIMO detector.

The model is y = H x + w, with H an m by n complex matrix of full column rank
(so m >= n), x a vector of n constellation points and w ~ CN(0, N0 I).
The detector applies the pseudoinverse W = (H^H H)^(-1) H^H, so that
W y = x + W w, and then slices each entry to the nearest constellation point.
Stream k sees noise of variance N0 [(H^H H)^(-1)]_kk, so its post-detection
SNR is (Es / N0) / [(H^H H)^(-1)]_kk.
"""

import cbb


def nearest(z: complex, points: list[complex]) -> int:
    """The index of the point nearest to z (the lowest index on a tie)."""
    best, arg = float("inf"), -1
    for i, p in enumerate(points):
        d = abs(z - p) ** 2
        if d < best:
            best, arg = d, i
    return arg


def zf_matrix(h: list[list[complex]]) -> list[list[complex]]:
    """The n by m pseudoinverse (H^H H)^(-1) H^H. Raises ValueError if H has dependent columns."""
    if len(h) < len(h[0]):
        raise ValueError("ZF needs at least as many receive antennas as streams")
    hh = cbb.herm(h)
    g = cbb.matmul(hh, h)  # @line L1
    try:
        return cbb.solve(g, hh)  # @line L2
    except ValueError:
        raise ValueError("H^H H is singular: the columns of H are dependent") from None


def zf_outputs(y: list[complex], h: list[list[complex]]) -> list[complex]:
    """The unquantized ZF outputs z = W y = x + W w."""
    return cbb.matvec(zf_matrix(h), y)


def zf_detect(y: list[complex], h: list[list[complex]], points: list[complex]) -> list[int]:
    """The ZF decisions: the index of the nearest point to each entry of W y."""
    w = zf_matrix(h)
    z = cbb.matvec(w, y)  # @line L3
    out = []
    for k in range(len(z)):  # @line L4
        out.append(nearest(z[k], points))  # @line L5
    return out  # @line L6


def noise_gains(h: list[list[complex]]) -> list[float]:
    """The diagonal of (H^H H)^(-1): stream k has output noise variance N0 times this value."""
    hh = cbb.herm(h)
    p = cbb.inv(cbb.matmul(hh, h))
    return [p[k][k].real for k in range(len(p))]


def post_detection_snr(h: list[list[complex]], es: float, n0: float) -> list[float]:
    """The SNR of each stream after ZF: (Es / N0) / [(H^H H)^(-1)]_kk."""
    return [es / (n0 * g) for g in noise_gains(h)]
