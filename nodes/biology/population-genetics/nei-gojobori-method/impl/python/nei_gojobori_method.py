# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nei-gojobori-method/. The authors are listed in prov/10S5MW.jsonl.
"""The Nei-Gojobori (1986) method for dN and dS of two coding sequences.

Sites. For a sense codon c, s(c) is the sum over its three positions of the
fraction of the three other bases at that position that give a codon for the
same amino acid; n(c) = 3 - s(c). A change to a stop codon counts as
nonsynonymous. The site counts are exact Fractions.

Differences. For two sense codons x and y that differ at k positions, each of
the k! orders of the k changes is a pathway. A step is synonymous when the two
codons of the step code the same amino acid. The synonymous and nonsynonymous
differences of the pair are the averages over the pathways, all with the same
weight. Pathways through a stop codon are left out by default (the 1986 paper
does not discuss them; programs commonly leave them out). If every pathway
goes through a stop codon, all pathways are used, and a step into or out of a
stop counts as nonsynonymous.

Distances. p = differences / sites, and d = -(3/4) ln(1 - 4p/3), the
Jukes-Cantor correction; d is None when p >= 3/4.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction
from typing import NamedTuple, Optional, Tuple

from bioseq import CODON_TABLE, DNA, STOPS


class Result(NamedTuple):
    syn_sites: Fraction
    nonsyn_sites: Fraction
    syn_diffs: Fraction
    nonsyn_diffs: Fraction
    p_s: float
    p_n: float
    d_s: Optional[float]
    d_n: Optional[float]
    omega: Optional[float]
    codons: int


def _check_codon(c: str) -> None:
    if c not in CODON_TABLE:
        raise ValueError(f"not a codon over ACGT: {c!r}")
    if c in STOPS:
        raise ValueError(f"stop codon {c} in a coding sequence")


def codon_sites(c: str) -> Tuple[Fraction, Fraction]:
    """(s(c), n(c)), the synonymous and nonsynonymous sites of a sense codon."""
    _check_codon(c)
    aa = CODON_TABLE[c]
    s = Fraction(0)
    for i in range(3):
        for b in DNA:
            if b != c[i] and CODON_TABLE[c[:i] + b + c[i + 1:]] == aa:
                s += Fraction(1, 3)
    return s, 3 - s


def codon_differences(x: str, y: str, skip_stop_paths: bool = True) -> Tuple[Fraction, Fraction]:
    """(s_d, n_d): synonymous and nonsynonymous differences of two sense codons,
    averaged over the pathways between them."""
    _check_codon(x)
    _check_codon(y)
    pos = [i for i in range(3) if x[i] != y[i]]
    if not pos:
        return Fraction(0), Fraction(0)
    paths = []
    for order in itertools.permutations(pos):
        cur = x
        syn = non = 0
        through_stop = False
        for i in order:
            nxt = cur[:i] + y[i] + cur[i + 1:]
            if nxt in STOPS:
                through_stop = True
            if CODON_TABLE[nxt] == CODON_TABLE[cur]:
                syn += 1
            else:
                non += 1
            cur = nxt
        paths.append((syn, non, through_stop))
    kept = [p for p in paths if not p[2]] if skip_stop_paths else paths
    if not kept:
        kept = paths
    m = len(kept)
    return Fraction(sum(p[0] for p in kept), m), Fraction(sum(p[1] for p in kept), m)


def jukes_cantor(p: float) -> Optional[float]:
    """d = -(3/4) ln(1 - 4p/3), or None when p >= 3/4."""
    if p < 0:
        raise ValueError("p must be >= 0")
    if p >= 0.75:
        return None
    return -0.75 * math.log1p(-4.0 * p / 3.0)


def nei_gojobori(seq1: str, seq2: str, skip_stop_paths: bool = True) -> Result:
    """dN, dS and dN/dS of two aligned coding sequences in the same frame.

    Codons with a letter other than A, C, G or T in either sequence (gaps,
    N) are left out. A stop codon raises ValueError. omega is None when dS is
    0 or undefined, or dN is undefined.
    """
    a = seq1.upper()
    b = seq2.upper()
    if len(a) != len(b) or len(a) % 3:
        raise ValueError("need two sequences of the same length, a multiple of 3")
    s_sites = Fraction(0)  # @line L1
    s_d = Fraction(0)
    n_d = Fraction(0)
    r = 0
    for i in range(0, len(a), 3):  # @line L2
        x, y = a[i:i + 3], b[i:i + 3]
        if x not in CODON_TABLE or y not in CODON_TABLE:
            continue
        s_sites += (codon_sites(x)[0] + codon_sites(y)[0]) / 2  # @line L3
        sd, nd = codon_differences(x, y, skip_stop_paths)  # @line L4
        s_d += sd  # @line L5
        n_d += nd
        r += 1
    n_sites = 3 * r - s_sites  # @line L6
    if s_sites == 0 or n_sites == 0:
        raise ValueError("no synonymous or no nonsynonymous sites")
    p_s = float(s_d / s_sites)
    p_n = float(n_d / n_sites)
    d_s = jukes_cantor(p_s)  # @line L7
    d_n = jukes_cantor(p_n)
    omega = d_n / d_s if d_s and d_n is not None else None
    return Result(s_sites, n_sites, s_d, n_d, p_s, p_n, d_s, d_n, omega, r)  # @line L8
