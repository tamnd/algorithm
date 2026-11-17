# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-haplotype-homozygosity/. The authors are listed in prov/DC6Q95.jsonl.
"""Extended haplotype homozygosity (Sabeti and coauthors 2002) and the
integrated EHH log ratio of Voight and coauthors (2006).

Input: phased haplotypes as equal-length sequences of 0 and 1 (0 is the
ancestral allele, 1 the derived allele), the map positions of the markers in
increasing order, and the index of the core marker.

EHH. For the carriers of allele a at the core, EHH at marker j is the
fraction of pairs of carriers that are identical at every marker from the
core to j (both ends included). It is 1 at the core and does not increase
when j moves away from the core.

Integrated EHH. On each side, the area under EHH by the trapezoid rule over
the map positions, from the core outward, over the segments whose outer end
has EHH >= cutoff; the sum stops at the first marker with EHH < cutoff. The
flags reached_left and reached_right say that the data ended before EHH fell
under the cutoff. Programs differ in this truncation rule.

Score. ln(iHH of the ancestral allele / iHH of the derived allele). It is
negative when the derived allele sits on long shared haplotypes. The
standardized score subtracts the mean and divides by the standard deviation
of the scores of markers with a similar derived allele frequency.
"""

from __future__ import annotations

import math
from fractions import Fraction
from math import comb
from typing import List, NamedTuple, Sequence


class IHH(NamedTuple):
    value: float
    reached_left: bool
    reached_right: bool


def carriers(haps: Sequence[Sequence[int]], core: int, allele: int) -> List[int]:
    """The indices of the haplotypes with the given allele at the core."""
    return [i for i, h in enumerate(haps) if h[core] == allele]


def ehh_curve(haps: Sequence[Sequence[int]], core: int, allele: int) -> List[Fraction]:
    """EHH of the carriers of allele at every marker, as exact fractions."""
    if not haps:
        raise ValueError("need haplotypes")
    m = len(haps[0])
    if any(len(h) != m for h in haps) or not 0 <= core < m:
        raise ValueError("haplotypes must have one length and core must be a marker")
    group = carriers(haps, core, allele)  # @line L1
    k = len(group)
    if k < 2:
        raise ValueError("need at least two carriers of the allele")
    pairs = comb(k, 2)
    e = [Fraction(0)] * m  # @line L2
    e[core] = Fraction(1)
    for step in (1, -1):  # @line L3
        classes = [group]  # @line L4
        j = core + step
        while 0 <= j < m and classes:  # @line L5
            split = []
            for cls in classes:  # @line L6
                parts = {}
                for i in cls:
                    parts.setdefault(haps[i][j], []).append(i)
                split.extend(p for p in parts.values() if len(p) >= 2)
            classes = split
            e[j] = Fraction(sum(comb(len(c), 2) for c in classes), pairs)  # @line L7
            j += step
    return e


def integrated_ehh(e: Sequence[Fraction], positions: Sequence[float], core: int,
                   cutoff: float = 0.05) -> IHH:
    """The trapezoid area under the EHH curve e, truncated at the cutoff."""
    if len(e) != len(positions):
        raise ValueError("one position per marker")
    if any(positions[i] >= positions[i + 1] for i in range(len(positions) - 1)):
        raise ValueError("positions must increase")
    area = 0.0
    reached = []
    for step in (-1, 1):
        j = core + step
        done = False
        while 0 <= j < len(e):  # @line L8
            if e[j] < cutoff:
                done = True
                break
            area += (float(e[j]) + float(e[j - step])) / 2.0 * abs(positions[j] - positions[j - step])
            j += step
        reached.append(not done)
    return IHH(area, reached[0], reached[1])  # @line L9


def ihh_log_ratio(haps: Sequence[Sequence[int]], positions: Sequence[float], core: int,
                  cutoff: float = 0.05) -> float:
    """ln(iHH of allele 0 / iHH of allele 1) at the core marker."""
    a = integrated_ehh(ehh_curve(haps, core, 0), positions, core, cutoff).value
    d = integrated_ehh(ehh_curve(haps, core, 1), positions, core, cutoff).value
    if a <= 0.0 or d <= 0.0:
        raise ValueError("an integrated EHH is 0; the log ratio is not defined")
    return math.log(a / d)


def standardize(scores: Sequence[float], freqs: Sequence[float], n_bins: int = 20) -> List[float]:
    """(score - bin mean) / bin standard deviation, with bins of equal width in
    the derived allele frequency. A bin with fewer than two scores, or with
    standard deviation 0, gives nan for its markers."""
    if len(scores) != len(freqs):
        raise ValueError("one frequency per score")
    bins = [min(int(f * n_bins), n_bins - 1) for f in freqs]
    out = [math.nan] * len(scores)
    for b in set(bins):
        idx = [i for i, x in enumerate(bins) if x == b]
        if len(idx) < 2:
            continue
        mean = sum(scores[i] for i in idx) / len(idx)
        sd = math.sqrt(sum((scores[i] - mean) ** 2 for i in idx) / (len(idx) - 1))
        if sd == 0.0:
            continue
        for i in idx:
            out[i] = (scores[i] - mean) / sd
    return out
