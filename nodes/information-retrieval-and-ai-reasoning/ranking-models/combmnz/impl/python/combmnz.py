# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combmnz/. The authors are listed in prov/HTFVCS.jsonl.

import statistics
from typing import Any, Hashable, Mapping, Sequence

Run = Mapping[Hashable, float]


def normalize(run: Run, method: str = "minmax") -> dict[Any, float]:
    """Rescale the scores of one run.

    minmax maps the lowest score to 0 and the highest to 1 (all scores 1 when they are
    equal); sum divides by the sum of the scores after a shift that makes the lowest 0;
    zmuv subtracts the mean and divides by the standard deviation; none keeps the scores.
    """
    if not run or method == "none":
        return dict(run)
    lo, hi = min(run.values()), max(run.values())
    if method == "minmax":
        return {d: (s - lo) / (hi - lo) if hi > lo else 1.0 for d, s in run.items()}
    if method == "sum":
        tot = sum(s - lo for s in run.values())
        return {d: (s - lo) / tot if tot > 0 else 1.0 / len(run) for d, s in run.items()}
    if method == "zmuv":
        mu = statistics.fmean(run.values())
        sd = statistics.pstdev(run.values())
        return {d: (s - mu) / sd if sd > 0 else 0.0 for d, s in run.items()}
    raise ValueError("method must be minmax, sum, zmuv or none")


def comb_scores(runs: Sequence[Run], rule: str = "MNZ", norm: str = "minmax") -> dict[Any, float]:
    """Return the fused score of each document of the union of the runs.

    SUM is the sum of the normalized scores of a document over the runs that retrieved
    it, and MNZ is that sum times h(d), the number of runs that retrieved it. MAX, MIN
    and MED take the largest, smallest and median normalized score, and ANZ is SUM / h(d).
    """
    normed = [normalize(r, norm) for r in runs]  # @line L1
    seen: dict[Any, list[float]] = {}
    for r in normed:  # @line L2
        for d, s in r.items():
            seen.setdefault(d, []).append(s)
    out = {}
    for d, ss in seen.items():  # @line L3
        total, h = sum(ss), len(ss)
        if rule == "SUM":
            out[d] = total
        elif rule == "MNZ":
            out[d] = h * total  # @line L4
        elif rule == "ANZ":
            out[d] = total / h
        elif rule == "MAX":
            out[d] = max(ss)
        elif rule == "MIN":
            out[d] = min(ss)
        elif rule == "MED":
            out[d] = statistics.median(ss)
        else:
            raise ValueError("rule must be SUM, MNZ, ANZ, MAX, MIN or MED")
    return out


def comb(runs: Sequence[Run], rule: str = "MNZ", norm: str = "minmax") -> list[Any]:
    """Fuse the runs and return the documents by fused score, high first, ties by id."""
    s = comb_scores(runs, rule, norm)
    return sorted(s, key=lambda d: (-s[d], d))  # @line L5
