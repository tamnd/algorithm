# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coherence-factor/. The authors are listed in prov/BGW13T.jsonl.
"""The coherence factor of delayed array samples, and CF weighting.

For the delayed (focused) channel samples s_1, ..., s_M of one pixel,

    CF = |sum_i s_i|^2 / (M sum_i |s_i|^2),

the energy of the coherent sum over M times the total energy. It lies in
[0, 1] by the Cauchy-Schwarz inequality, and it is 1 exactly when all samples
are equal and not all zero. CF weighting multiplies the delay-and-sum output
by CF^p; the exponent p is a design choice (p = 1 is the common one).
"""


def coherence_factor(samples):
    """CF of one delayed channel vector; 0 when every sample is 0."""
    m = len(samples)
    coherent = abs(sum(samples)) ** 2  # @line L1
    incoherent = m * sum(abs(s) ** 2 for s in samples)  # @line L2
    if incoherent == 0:  # @line L3
        return 0.0
    return coherent / incoherent  # @line L4


def cf_weighted(samples, p=1.0):
    """The delay-and-sum value times CF^p."""
    return sum(samples) * coherence_factor(samples) ** p  # @line L5


def triangle_coherence_cf(m):
    """E|sum s|^2 / (M E sum |s|^2) when the channel correlation is 1 - |i - j| / M.

    This is the pulse-echo van Cittert-Zernike coherence of fully developed
    speckle for a uniform transmit aperture as wide as the receive aperture.
    The value is (2 M^2 + 1) / (3 M^2), which tends to 2/3.
    """
    return (2 * m * m + 1) / (3 * m * m)
