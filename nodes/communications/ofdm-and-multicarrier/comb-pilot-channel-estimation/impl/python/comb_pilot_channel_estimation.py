# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/comb-pilot-channel-estimation/. The authors are listed in prov/VPF3QG.jsonl.

"""Channel estimation in OFDM from comb-type pilots.

Every OFDM symbol carries known pilot values on the subcarriers
k0, k0 + D, k0 + 2D, ... (a comb with spacing D). The receiver sees
Y[k] = H[k] X[k] + W[k] on each subcarrier. It takes the least squares
estimate H_p = Y[p] / X[p] at each pilot and interpolates between pilots
along frequency. H[k] is periodic in k with period N (it is the DFT of the
taps), so the interpolation wraps around from the last pilot to the first.

order=1 is linear interpolation between the two nearest pilots.
order=2 is quadratic Lagrange interpolation through three pilots: the one
before k, the one after k and the one before that.
"""


def pilot_positions(n: int, spacing: int, k0: int = 0) -> list[int]:
    """The pilot subcarriers k0, k0 + D, ..., below N. N must be a multiple of D."""
    if spacing < 1 or n % spacing or not 0 <= k0 < spacing:
        raise ValueError("need N a multiple of D and 0 <= k0 < D")
    return list(range(k0, n, spacing))


def estimate(y: list[complex], pilot_values: list[complex], spacing: int, k0: int = 0, order: int = 1) -> list[complex]:
    """The channel estimate on all N subcarriers.

    y is the received symbol after the DFT. pilot_values[i] is the known value
    sent on subcarrier k0 + i D.
    """
    n = len(y)
    ps = pilot_positions(n, spacing, k0)
    if len(pilot_values) != len(ps):
        raise ValueError("one pilot value per pilot subcarrier")
    if order not in (1, 2):
        raise ValueError("order is 1 or 2")
    count = len(ps)
    hp = [y[p] / x for p, x in zip(ps, pilot_values)]  # @line L1
    out = []
    for k in range(n):
        i, rem = divmod((k - k0) % n, spacing)  # @line L2
        t = rem / spacing  # @line L3
        a, b = hp[i], hp[(i + 1) % count]  # @line L4
        if order == 1:
            out.append((1 - t) * a + t * b)  # @line L5
        else:
            c = hp[(i - 1) % count]
            out.append(t * (t - 1) / 2 * c + (1 - t) * (1 + t) * a + t * (t + 1) / 2 * b)
    return out  # @line L6
