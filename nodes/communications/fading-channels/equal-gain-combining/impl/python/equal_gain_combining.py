# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equal-gain-combining/. The authors are listed in prov/FAG3FG.jsonl.

"""Equal gain combining (EGC) of L diversity branches.

Branch l receives y_l = h_l x + w_l with w_l ~ CN(0, N0), the same N0 on every
branch. EGC removes the phase of each branch, multiplying by
e^(-j arg h_l), and adds the branches with equal weights. The sum is
(sum |h_l|) x plus noise of variance L N0, so the output SNR is
E_s (sum |h_l|)^2 / (L N0). It needs the phases, not the amplitudes.

The error rate functions are for coherent BPSK and i.i.d. Rayleigh branches
with mean SNR gamma_bar per branch.
"""

import math

import cbb


def egc(h: list[complex], y: list[complex]) -> tuple[complex, float]:
    """The EGC estimate of x and the amplitude sum a = sum |h_l|."""
    if len(h) != len(y) or not h:
        raise ValueError("need L >= 1 branches with h and y each")
    c = [v / abs(v) if v != 0 else 0j for v in h]  # @line L1
    z = sum(c[l].conjugate() * y[l] for l in range(len(h)))  # @line L2
    a = sum(abs(v) for v in h)  # @line L3
    if a == 0.0:
        raise ValueError("all branch gains are zero")
    return z / a, a  # @line L4


def egc_snr(h: list[complex], n0: float, es: float = 1.0) -> float:
    """The output SNR of EGC: E_s (sum |h_l|)^2 / (L N0)."""
    return es * sum(abs(v) for v in h) ** 2 / (len(h) * n0)


def mean_snr_gain(branches: int) -> float:
    """E[output SNR] / gamma_bar for L i.i.d. Rayleigh branches: 1 + (L - 1) pi / 4."""
    return 1.0 + (branches - 1) * math.pi / 4.0


def ber_bpsk_rayleigh_dual(gbar: float) -> float:
    """Exact BPSK bit error rate of EGC with two i.i.d. Rayleigh branches: (1 - sqrt(g (g + 2)) / (g + 1)) / 2."""
    return 0.5 * (1.0 - math.sqrt(gbar * (gbar + 2.0)) / (gbar + 1.0))


def ber_bpsk_rayleigh_dual_integral(gbar: float, nr: int = 600, nphi: int = 120) -> float:
    """The same error rate by direct integration over the two amplitudes, in polar form.

    With E|h_l|^2 = 1 the amplitudes r_1, r_2 have the density 4 r_1 r_2 e^(-r_1^2 - r_2^2),
    and the error rate given them is Q((r_1 + r_2) sqrt(gamma_bar)). Simpson's
    rule is used in r on [0, 8] and in the angle on [0, pi / 2].
    """
    rmax = 8.0
    hr = rmax / nr
    hp = (math.pi / 2.0) / nphi
    sg = math.sqrt(gbar)

    def inner(phi):
        cs = math.cos(phi) + math.sin(phi)
        s = 0.0
        for k in range(1, nr + 1):
            r = k * hr
            w = 1 if k == nr else (4 if k % 2 else 2)
            s += w * r ** 3 * math.exp(-r * r) * cbb.qfunc(r * cs * sg)
        return s * hr / 3.0

    tot = 0.0
    for k in range(1, nphi):
        phi = k * hp
        w = 4 if k % 2 else 2
        tot += w * 4.0 * math.cos(phi) * math.sin(phi) * inner(phi)
    return tot * hp / 3.0
