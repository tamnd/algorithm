# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/test-vector-leakage-assessment/. The authors are listed in prov/89GDF4.jsonl.
"""The fixed versus random Welch t-test of TVLA (Goodwill, Jun, Jaffe, Rohatgi, 2011).

The traces come from a stated synthetic model of a device, drawn with a
seeded ``random.Random``: one sample leaks HW(S(p xor k)) + N(0, sigma^2)
with the 4-bit PRESENT S-box, or, for the masked model, two samples leak
HW(S(p xor k) xor m) and HW(m) for a fresh uniform mask m. No device, file
or clock is used.
"""

import math
import random

PRESENT_SBOX: tuple[int, ...] = (
    0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
    0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2,
)

Trace = list[float]


def hamming_weight(v: int) -> int:
    """Return the number of 1 bits of a non-negative integer."""
    return bin(v).count("1")


def device_trace(rng: random.Random, p: int, key: int, samples: int, sigma: float, masked: bool) -> Trace:
    """One synthetic trace of the given number of samples (at least 2).

    Unmasked: sample 0 is HW(S(p xor key)) + noise. Masked: sample 0 is
    HW(S(p xor key) xor m) + noise and sample 1 is HW(m) + noise for a
    fresh uniform m. Every other sample is noise with mean 2.
    """
    v = PRESENT_SBOX[p ^ key]
    tr = [2.0 + rng.gauss(0.0, sigma) for _ in range(samples)]
    if masked:
        m = rng.randrange(16)
        tr[0] = hamming_weight(v ^ m) + rng.gauss(0.0, sigma)
        tr[1] = hamming_weight(m) + rng.gauss(0.0, sigma)
    else:
        tr[0] = hamming_weight(v) + rng.gauss(0.0, sigma)
    return tr


def collect(
    rng: random.Random, n: int, fixed_input: int, key: int, samples: int, sigma: float, masked: bool
) -> tuple[list[Trace], list[Trace]]:
    """n traces with the fixed input and n with uniform inputs, in random order."""
    fixed: list[Trace] = []
    rand: list[Trace] = []
    while len(fixed) < n or len(rand) < n:
        if len(rand) >= n or (len(fixed) < n and rng.randrange(2) == 0):
            fixed.append(device_trace(rng, fixed_input, key, samples, sigma, masked))
        else:
            rand.append(device_trace(rng, rng.randrange(16), key, samples, sigma, masked))
    return fixed, rand


def welch_t(x: list[float], y: list[float]) -> float:
    """Welch's t statistic of two samples, each of size at least 2.

    t = (mean(x) - mean(y)) / sqrt(var(x)/|x| + var(y)/|y|) with unbiased
    variances. Returns 0.0 if both variances are 0 and the means are equal,
    and +-inf if only the variances are 0. Cost: Theta(|x| + |y|).
    """
    nx, ny = len(x), len(y)
    mx, my = sum(x) / nx, sum(y) / ny
    vx = sum((a - mx) ** 2 for a in x) / (nx - 1)
    vy = sum((b - my) ** 2 for b in y) / (ny - 1)
    se = math.sqrt(vx / nx + vy / ny)
    if se == 0.0:
        return 0.0 if mx == my else math.copysign(math.inf, mx - my)
    return (mx - my) / se


def centred_products(traces: list[Trace], i: int, j: int) -> list[float]:
    """Second-order preprocessing: (l[i] - mean_i) * (l[j] - mean_j) for each trace.

    The means are those of the given group. Cost: Theta(len(traces)).
    """
    mi = sum(t[i] for t in traces) / len(traces)
    mj = sum(t[j] for t in traces) / len(traces)
    return [(t[i] - mi) * (t[j] - mj) for t in traces]


def tvla(sets: list[tuple[list[Trace], list[Trace]]], threshold: float = 4.5) -> tuple[list[list[float]], list[int]]:
    """The fixed versus random test on independent sets of traces.

    Each set is (fixed traces, random traces), all with T samples and at
    least 2 traces in each group. Returns the t-values of each set at each
    sample and the samples where |t| > threshold in every set; the device
    fails the test if that list is not empty.
    Cost: Theta(s * n * T) for s sets of n traces in each group.
    """
    tvals: list[list[float]] = []
    for fixed, rand in sets:  # @line L1
        width = len(fixed[0])  # @line L2
        row = []
        for j in range(width):  # @line L3
            row.append(welch_t([t[j] for t in fixed], [t[j] for t in rand]))
        tvals.append(row)
    leaky = [j for j in range(len(tvals[0])) if all(abs(r[j]) > threshold for r in tvals)]  # @line L4
    return tvals, leaky  # @line L5
