# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rasta-filtering/. The authors are listed in prov/C4662N.jsonl.

"""RASTA filtering of the log band energies of speech, after Hermansky and Morgan (1994).

Each band trajectory (the log energy of one band, one value per frame) goes
through the band-pass filter

    H(z) = 0.1 (2 + z^-1 - z^-3 - 2 z^-4) / (1 - rho z^-1),

which is the filter of the paper without its factor z^4. That factor only moves
the output 4 frames earlier, so this causal form gives the same output 4 frames
later. The paper uses rho = 0.98. Ellis's rastamat code uses rho = 0.94.

Before the first frame the input is taken equal to x[0] and the output to 0, so a
constant trajectory gives 0 from the first frame on. The numerator taps sum to 0,
so adding a constant to a trajectory does not change the output.
"""

from typing import List, Sequence


def rasta_filter(x: Sequence[float], rho: float = 0.98) -> List[float]:
    """Filter one trajectory: y[t] = sum_k b_k x[t - k] + rho y[t - 1], with b = 0.1 (2, 1, 0, -1, -2)."""
    if not 0.0 <= rho < 1.0:
        raise ValueError("rho must be in [0, 1) for a stable filter")
    if not x:
        return []
    y: List[float] = []
    prev = 0.0

    def past(t: int) -> float:
        return x[t] if t >= 0 else x[0]

    for t in range(len(x)):
        # the taps in pairs, so that a constant gives exactly 0
        u = 0.1 * (2.0 * (x[t] - past(t - 4)) + (past(t - 1) - past(t - 3)))  # @line L3
        prev = u + rho * prev  # @line L4
        y.append(prev)
    return y  # @line L5


def rasta_bands(log_bands: Sequence[Sequence[float]], rho: float = 0.98) -> List[List[float]]:
    """Filter every band of a log band spectrogram given as rows of frames (T rows of B values).

    Returns T rows of B values. Each column (one band over time) is filtered on its own."""
    if not log_bands:
        return []
    width = len(log_bands[0])
    if any(len(row) != width for row in log_bands):
        raise ValueError("all frames must have the same number of bands")
    columns = []
    for j in range(width):  # @line L1
        traj = [row[j] for row in log_bands]  # @line L2
        columns.append(rasta_filter(traj, rho))
    return [[columns[j][t] for j in range(width)] for t in range(len(log_bands))]
