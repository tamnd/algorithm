# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oerder-meyr-timing-estimation/. The authors are listed in prov/WF9W5Z.jsonl.

"""Oerder and Meyr timing estimation (1988): square the matched filter output and take
the phase of its spectral line at the symbol rate.

The input is a block of matched filter output samples x[n] = y(n / L_s), at L_s
samples per symbol (L_s >= 3; Oerder and Meyr use 4), with times in symbol
periods. The symbols sit at t = k + tau. The estimator is

    X = sum_n |x[n]|^2 e^(-j 2 pi n / L_s),    tau_hat = -arg(X) / (2 pi),

which lies in [-1/2, 1/2). For raised cosine pulses with roll-off beta > 0 and
i.i.d. zero-mean data, E|y(t)|^2 = c0 + (beta/4) E|a|^2 cos(2 pi (t - tau)), so
E[X] = (beta/8) E|a|^2 N e^(-j 2 pi tau) for N samples: the phase of the mean
is exactly -2 pi tau. The estimate does not depend on the carrier phase.
"""

import cmath
import math
from typing import Sequence


def spectral_line(x: Sequence[complex], ls: int) -> complex:
    """X = sum_n |x[n]|^2 e^(-j 2 pi n / L_s), the symbol-rate DFT bin of |x|^2."""
    if ls < 3:
        raise ValueError("L_s must be at least 3")
    rot = [cmath.exp(-2j * math.pi * i / ls) for i in range(ls)]  # @line L1
    acc = 0j  # @line L2
    for n, v in enumerate(x):  # @line L3
        acc += (v.real * v.real + v.imag * v.imag) * rot[n % ls]  # @line L4
    return acc


def oerder_meyr(x: Sequence[complex], ls: int = 4) -> float:
    """The timing estimate tau_hat in [-1/2, 1/2) symbol periods from one block of samples."""
    xs = spectral_line(x, ls)
    tau = -cmath.phase(xs) / (2.0 * math.pi)  # @line L5
    if tau >= 0.5:
        tau -= 1.0
    return tau  # @line L6


def oerder_meyr_blocks(x: Sequence[complex], ls: int, block: int) -> list[float]:
    """One estimate per block of `block` symbols, unwrapped so that it is continuous."""
    out: list[float] = []
    step = block * ls
    for start in range(0, len(x) - step + 1, step):
        # Sample n of the block is sample start + n of the stream; start is a whole
        # number of symbols, so the delay relative to the block start is the same.
        tau = oerder_meyr(x[start:start + step], ls)
        if out:
            tau += round(out[-1] - tau)
        out.append(tau)
    return out
