# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcdonald-kreitman-test/. The authors are listed in prov/4QSXZX.jsonl.
"""The McDonald-Kreitman test (McDonald and Kreitman 1991).

Input: aligned coding sequences of two species, in frame, with no stop codon.

Counting rule. A codon is used only when every sequence has a codon over
ACGT there and at most one of its three positions varies over all the
sequences of both species. A codon with two or more varying positions is
skipped and counted in `skipped`, because the order of the changes is not
known. At the one varying position:
- the change is synonymous when all the codons seen at that place code the
  same amino acid, and nonsynonymous otherwise;
- it is a polymorphism when the site varies within species A or within
  species B, and a fixed difference when each species has one base and the
  two bases differ.

Test. Fisher's exact test of the 2 x 2 table [[Dn, Ds], [Pn, Ps]], two-sided
by the minimum-likelihood rule, in exact integer arithmetic. Summaries: the
neutrality index NI = (Pn / Ps) / (Dn / Ds) and alpha = 1 - NI, the
estimated fraction of adaptive amino acid substitutions.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb
from typing import NamedTuple, Optional, Sequence

from bioseq import CODON_TABLE, STOPS


class MKResult(NamedTuple):
    dn: int
    ds: int
    pn: int
    ps: int
    p_value: float
    neutrality_index: Optional[float]
    alpha: Optional[float]
    skipped: int


def fisher_exact(table, exact: bool = False):
    """Two-sided p-value of Fisher's exact test for [[a, b], [c, d]].

    The tables with the same margins are weighted by C(r1, k) C(r2, c1 - k);
    the p-value is the total weight of the tables with weight <= that of the
    observed one, over C(n, c1). All weights are integers, so ties are exact.
    """
    (a, b), (c, d) = table
    if min(a, b, c, d) < 0:
        raise ValueError("counts must be >= 0")
    r1, r2, c1 = a + b, c + d, a + c
    n = r1 + r2
    lo, hi = max(0, c1 - r2), min(r1, c1)
    w_obs = comb(r1, a) * comb(r2, c)
    total = 0
    for k in range(lo, hi + 1):
        w = comb(r1, k) * comb(r2, c1 - k)
        if w <= w_obs:
            total += w
    p = Fraction(total, comb(n, c1))
    return p if exact else float(p)


def classify_codons(species_a: Sequence[str], species_b: Sequence[str]):
    """The counts (dn, ds, pn, ps, skipped) of the counting rule."""
    seqs = [s.upper() for s in list(species_a) + list(species_b)]
    if not species_a or not species_b:
        raise ValueError("need at least one sequence of each species")
    length = len(seqs[0])
    if length % 3 or any(len(s) != length for s in seqs):
        raise ValueError("sequences must have the same length, a multiple of 3")
    na = len(species_a)
    dn = ds = pn = ps = skipped = 0  # @line L1
    for i in range(0, length, 3):  # @line L2
        codons = [s[i:i + 3] for s in seqs]
        if any(c not in CODON_TABLE for c in codons):
            skipped += 1
            continue
        if any(c in STOPS for c in codons):
            raise ValueError(f"stop codon at codon {i // 3}")
        varying = [j for j in range(3) if len({c[j] for c in codons}) > 1]
        if not varying:
            continue
        if len(varying) > 1:
            skipped += 1
            continue
        j = varying[0]
        syn = len({CODON_TABLE[c] for c in codons}) == 1  # @line L3
        in_a = {c[j] for c in codons[:na]}
        in_b = {c[j] for c in codons[na:]}
        if len(in_a) > 1 or len(in_b) > 1:  # @line L4
            if syn:
                ps += 1
            else:
                pn += 1
        else:  # @line L5
            if syn:
                ds += 1
            else:
                dn += 1
    return dn, ds, pn, ps, skipped


def mk_summary(dn: int, ds: int, pn: int, ps: int):
    """(NI, alpha), or (None, None) when Dn, Ps or Ds is 0."""
    if dn == 0 or ps == 0 or ds == 0:
        return None, None
    ni = (pn * ds) / (ps * dn)
    return ni, 1.0 - ni


def mk_test_from_counts(dn: int, ds: int, pn: int, ps: int, skipped: int = 0) -> MKResult:
    p = fisher_exact([[dn, ds], [pn, ps]])  # @line L6
    ni, alpha = mk_summary(dn, ds, pn, ps)  # @line L7
    return MKResult(dn, ds, pn, ps, p, ni, alpha, skipped)  # @line L8


def mk_test(species_a: Sequence[str], species_b: Sequence[str]) -> MKResult:
    """Count fixed and polymorphic changes of the two kinds, then test."""
    dn, ds, pn, ps, skipped = classify_codons(species_a, species_b)
    return mk_test_from_counts(dn, ds, pn, ps, skipped)
