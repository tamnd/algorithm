# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-dimensional-wiener-pilot-interpolation/. The authors are listed in prov/G9C3T4.jsonl.

"""Two-dimensional Wiener interpolation of OFDM pilot estimates.

The channel H(n, k) is a function of the OFDM symbol n and the subcarrier k.
Pilots at the positions p_1, ..., p_K give noisy values y_i = H(p_i) + e_i,
where e_i has variance sigma^2 (N0 / |X_p|^2 for a least squares pilot
estimate). The channel has the correlation r(dn, dk) = E[H(n + dn, k + dk) conj(H(n, k))].
The linear estimate of H at a target t with the least mean squared error is

    w = (R + sigma^2 I)^(-1) c,   R[i][j] = r(p_i - p_j),   c[i] = r(p_i - t)
    H_hat(t) = sum over i of conj(w_i) y_i
    MSE = r(0, 0) - c^H (R + sigma^2 I)^(-1) c

Each target uses only its nearest pilots, so every solve is small. The
weights depend on the pilot pattern, the correlation and sigma^2, not on the
received data, so a receiver computes them once.
"""

import cbb

Position = tuple[int, int]


def nearest(target: Position, pilots: list[Position], count: int) -> list[int]:
    """Indices of the count pilots nearest to target (Euclidean distance in symbols and subcarriers)."""
    n, k = target
    order = sorted(range(len(pilots)), key=lambda i: ((pilots[i][0] - n) ** 2 + (pilots[i][1] - k) ** 2, i))
    return order[:count]


def wiener_weights(target: Position, pilots: list[Position], corr, noise_var: float) -> tuple[list[complex], float]:
    """The Wiener weights w for target from the given pilots, and the resulting MSE.

    corr(dn, dk) returns r(dn, dk); it must satisfy r(-dn, -dk) = conj(r(dn, dk)).
    """
    m = len(pilots)
    a = [[complex(corr(pilots[i][0] - pilots[j][0], pilots[i][1] - pilots[j][1])) for j in range(m)] for i in range(m)]  # @line L2
    for i in range(m):
        a[i][i] += noise_var  # @line L3
    c = [complex(corr(p[0] - target[0], p[1] - target[1])) for p in pilots]  # @line L4
    w = cbb.solve(a, c)  # @line L5
    mse = complex(corr(0, 0)).real - cbb.dot(c, w).real
    return w, mse


def estimate(targets: list[Position], pilots: list[Position], values: list[complex], corr, noise_var: float, count: int) -> list[complex]:
    """H_hat at each target from the pilot values, with count nearest pilots per target."""
    if len(values) != len(pilots) or not 1 <= count <= len(pilots):
        raise ValueError("one value per pilot and 1 <= count <= number of pilots")
    out = []
    for t in targets:
        idx = nearest(t, pilots, count)  # @line L1
        w, _ = wiener_weights(t, [pilots[i] for i in idx], corr, noise_var)
        out.append(sum(wi.conjugate() * values[i] for wi, i in zip(w, idx)))  # @line L6
    return out
