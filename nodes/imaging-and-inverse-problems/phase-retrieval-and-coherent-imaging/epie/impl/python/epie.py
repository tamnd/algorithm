# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epie/. The authors are listed in prov/RV95GV.jsonl.

"""The extended ptychographical iterative engine (ePIE) of Maiden and Rodenburg.

Conventions:
- The object O is an n1 x n2 complex image and the probe P an m1 x m2
  complex image. Position j is the offset (r, c) of the probe window in the
  object, with r + m1 <= n1 and c + m2 <= n2. O_j is the m1 x m2 patch
  O[r + a][c + b].
- The exit wave at position j is psi_j = P * O_j (pixelwise). The far field
  is its unnormalized 2D DFT (imgkit), and the data are the amplitudes
  a_j = |DFT2(psi_j)|, the square roots of the measured intensities.
- One sweep visits every position once, in a random order drawn from
  random.Random(seed).

Cost per sweep: J positions, each with two m1 x m2 DFTs and O(m1 m2) other
work, so O(J m^2 log m) for m x m probes of power-of-two size.
"""

import random

from imgkit import dft2, idft2


def patch(obj, pos, m1, m2):
    """The m1 x m2 patch of obj at the offset pos = (r, c)."""
    r, c = pos
    return [row[c:c + m2] for row in obj[r:r + m1]]


def exit_wave(obj, probe, pos):
    """psi = P * O_j, pixelwise."""
    m1, m2 = len(probe), len(probe[0])
    o = patch(obj, pos, m1, m2)
    return [[p * v for p, v in zip(rp, ro)] for rp, ro in zip(probe, o)]


def forward_amplitudes(obj, probe, positions):
    """The noiseless data a_j = |DFT2(P * O_j)| for every position."""
    return [[[abs(v) for v in row] for row in dft2(exit_wave(obj, probe, pos))] for pos in positions]


def modulus_replace(spec, amp):
    """The nearest point to spec with modulus amp, entry by entry.

    An entry with spec = 0 has no phase; it gets the phase 0, which is one of
    the nearest points.
    """
    out = []
    for rs, ra in zip(spec, amp):
        row = []
        for s, a in zip(rs, ra):
            m = abs(s)
            row.append(a * s / m if m > 0.0 else complex(a))
        out.append(row)
    return out


def data_error(amps, positions, obj, probe):
    """sum_j || |DFT2(P * O_j)| - a_j ||^2 / sum_j ||a_j||^2."""
    num = den = 0.0
    for a, pos in zip(amps, positions):
        spec = dft2(exit_wave(obj, probe, pos))
        for rs, ra in zip(spec, a):
            for s, v in zip(rs, ra):
                num += (abs(s) - v) ** 2
                den += v * v
    return num / den


def epie(amps, positions, obj, probe, sweeps, alpha=1.0, beta=1.0, seed=0, update_probe=True):
    """Run ePIE and return the object and probe estimates.

    amps[j] holds the measured amplitudes for positions[j]. obj and probe are
    the start guesses; they are copied, not changed. With update_probe=False
    the probe stays fixed, which gives the PIE-like object-only update.
    """
    obj = [list(row) for row in obj]
    probe = [list(row) for row in probe]
    m1, m2 = len(probe), len(probe[0])
    rng = random.Random(seed)
    order = list(range(len(positions)))
    for _ in range(sweeps):  # @line L1
        rng.shuffle(order)  # @line L2
        for j in order:
            r, c = positions[j]
            o = patch(obj, (r, c), m1, m2)
            psi = [[p * v for p, v in zip(rp, ro)] for rp, ro in zip(probe, o)]  # @line L3
            spec = dft2(psi)  # @line L4
            psi2 = idft2(modulus_replace(spec, amps[j]))  # @line L5
            diff = [[x - y for x, y in zip(r2, r1)] for r2, r1 in zip(psi2, psi)]  # @line L6
            pmax = max(abs(p) ** 2 for row in probe for p in row)
            omax = max(abs(v) ** 2 for row in o for v in row)
            for a in range(m1):  # @line L7
                for b in range(m2):
                    obj[r + a][c + b] = o[a][b] + alpha * probe[a][b].conjugate() / pmax * diff[a][b]
            if update_probe and omax > 0.0:  # @line L8
                probe = [
                    [probe[a][b] + beta * o[a][b].conjugate() / omax * diff[a][b] for b in range(m2)]
                    for a in range(m1)
                ]
    return obj, probe  # @line L9
