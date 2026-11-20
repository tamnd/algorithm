# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/common-phase-error-correction/. The authors are listed in prov/3R84JE.jsonl.

"""Common phase error (CPE) correction in OFDM with pilot subcarriers.

Phase noise phi[n] multiplies time sample n by e^(j phi[n]). After the DFT,
with the unitary pair of the OFDM page,

    Y[k] = I_0 H[k] X[k] + (sum over m != k of I_(k - m) H[m] X[m]) + W[k]
    I_q  = (1/N) sum over n of e^(j phi[n]) e^(-j 2 pi q n / N)

I_0 is the same for every subcarrier: the common phase error. The other
terms are inter-carrier interference. The receiver knows H and the pilot
values X_p, and estimates the angle of I_0 from the pilots:

    C = sum over pilots p of Y[p] conj(H[p] X_p),  phi_hat = angle(C)

then rotates every subcarrier back by phi_hat before the one-tap equalizer.
"""

import cmath


def estimate_phase(y: list[complex], h: list[complex], pilots: list[int], pilot_values: list[complex]) -> float:
    """phi_hat = angle of sum over pilots of Y[p] conj(H[p] X_p)."""
    if len(pilots) != len(pilot_values) or not pilots:
        raise ValueError("need one value per pilot and at least one pilot")
    c = sum(y[p] * (h[p] * x).conjugate() for p, x in zip(pilots, pilot_values))  # @line L1
    return cmath.phase(c)  # @line L2


def correct(y: list[complex], h: list[complex], pilots: list[int], pilot_values: list[complex]) -> list[complex]:
    """The equalized subcarrier values Y[k] e^(-j phi_hat) / H[k] for all k."""
    phi = estimate_phase(y, h, pilots, pilot_values)
    rot = cmath.exp(-1j * phi)
    z = [v * rot / hk for v, hk in zip(y, h)]  # @line L3
    return z  # @line L4
