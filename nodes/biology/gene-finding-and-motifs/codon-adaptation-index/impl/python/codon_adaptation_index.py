# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/codon-adaptation-index/. The authors are listed in prov/QCTP6D.jsonl.
"""The codon adaptation index (CAI) of Sharp and Li (1987).

The index has two steps:
- relative_adaptiveness(reference) counts the codons of a reference set of
  highly expressed genes and gives each sense codon its weight
  w = X / X_max, where X is the count of the codon and X_max the count of the
  most used codon of the same amino acid. A codon that the reference set
  never uses gets the count 1/2, as in the paper. The weights are Fractions.
- cai(gene, w) is the geometric mean of the weights of the codons of the gene.
  Codons of amino acids with a single codon (ATG for Met and TGG for Trp in the
  standard code), stop codons and codons with a letter other than A, C, G or T
  are skipped, because their weight carries no information.

Genes are read in frame 0, three bases at a time; a last part shorter than
three bases is dropped. The caller removes an initiation codon other than ATG
(for example GTG) if it must not count.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, Iterable, Mapping

from bioseq import CODON_TABLE

ZERO_COUNT = Fraction(1, 2)


def _codons(seq: str):
    """The codons of seq in frame 0, in upper case."""
    s = seq.upper()
    return (s[i:i + 3] for i in range(0, len(s) - 2, 3))


def synonym_families(code: Mapping[str, str] = CODON_TABLE) -> Dict[str, list]:
    """For each amino acid, the list of its codons (stops are left out)."""
    fam: Dict[str, list] = {}
    for c in sorted(code):
        if code[c] != "*":
            fam.setdefault(code[c], []).append(c)
    return fam


def codon_counts(genes: Iterable[str], code: Mapping[str, str] = CODON_TABLE) -> Dict[str, int]:
    """The number of times each sense codon occurs in the genes, in frame 0."""
    X = {c: 0 for c in code if code[c] != "*"}
    for g in genes:
        for c in _codons(g):
            if c in X:
                X[c] += 1
    return X


def relative_adaptiveness(genes: Iterable[str], code: Mapping[str, str] = CODON_TABLE,
                          zero_count: Fraction = ZERO_COUNT) -> Dict[str, Fraction]:
    """The weight w of each sense codon, from a reference set of genes."""
    X = codon_counts(genes, code)  # @line L1
    Xf = {c: (Fraction(x) if x > 0 else zero_count) for c, x in X.items()}  # @line L2
    w: Dict[str, Fraction] = {}
    for aa, cods in synonym_families(code).items():
        x_max = max(Xf[c] for c in cods)  # @line L3
        for c in cods:
            w[c] = Xf[c] / x_max  # @line L4
    return w


def counted_codons(gene: str, w: Mapping[str, Fraction], code: Mapping[str, str] = CODON_TABLE):
    """The codons of the gene that enter the index, in order."""
    fam = synonym_families(code)
    single = {cods[0] for cods in fam.values() if len(cods) == 1}
    return [c for c in _codons(gene) if c in w and c not in single]


def cai(gene: str, w: Mapping[str, Fraction], code: Mapping[str, str] = CODON_TABLE) -> float:
    """The codon adaptation index of the gene under the weights w.

    Raises ValueError if the gene has no codon that counts.
    """
    fam = synonym_families(code)
    single = {cods[0] for cods in fam.values() if len(cods) == 1}
    S, L = 0.0, 0  # @line L5
    for c in _codons(gene):  # @line L6
        if c in w and c not in single:  # @line L7
            S += math.log(w[c])  # @line L8
            L += 1
    if L == 0:
        raise ValueError("the gene has no codon that counts")
    return math.exp(S / L)  # @line L9
