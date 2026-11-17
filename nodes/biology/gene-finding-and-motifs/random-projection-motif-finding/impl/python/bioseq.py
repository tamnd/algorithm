# SPDX-License-Identifier: MIT
# Shared helper of the biology pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small DNA utilities shared by the biology pages.

Conventions:
- DNA is a str over "ACGT", written 5' to 3'. Positions are 0-based.
- Random draws use a random.Random object that the caller passes in, and the
  order of the draws is fixed and written in each docstring, so that a seed
  gives the same output on every run.
- Alignment scores are added: pass match as a positive number and mismatch and
  gap as negative numbers. A CIGAR string uses M (a column with a base of both
  strings, equal or not), I (a base of a, the query, against a gap) and D (a
  base of b, the reference, against a gap).

This module holds no algorithm of a page: no ORF finder, no motif finder and
no caller. The functions are building blocks for the page code and its tests.
"""

from __future__ import annotations

import math
import random
from collections import namedtuple
from typing import Dict, List, Sequence, Tuple, Union

DNA = "ACGT"

_COMPLEMENT = {"A": "T", "C": "G", "G": "C", "T": "A", "N": "N",
               "a": "t", "c": "g", "g": "c", "t": "a", "n": "n"}


def revcomp(seq: str) -> str:
    """The reverse complement of seq. N maps to N; other letters raise KeyError."""
    return "".join(_COMPLEMENT[c] for c in reversed(seq))


# NCBI genetic code table 1 (the standard code), in the TCAG order of the NCBI
# listing: the first base changes slowest and the third base fastest.
_AAS = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
_ORDER = "TCAG"
CODON_TABLE: Dict[str, str] = {
    a + b + c: _AAS[16 * i + 4 * j + k]
    for i, a in enumerate(_ORDER)
    for j, b in enumerate(_ORDER)
    for k, c in enumerate(_ORDER)
}
STOPS = frozenset(c for c, aa in CODON_TABLE.items() if aa == "*")


def translate(seq: str, frame: int = 0) -> str:
    """Translate seq[frame:] codon by codon with CODON_TABLE.

    frame is 0, 1 or 2. A stop codon gives "*", a codon with a letter other than
    A, C, G or T gives "X", and a last part shorter than three bases is dropped.
    The function does not look for start or stop codons.
    """
    if frame not in (0, 1, 2):
        raise ValueError("frame must be 0, 1 or 2")
    s = seq.upper()
    out = []
    for i in range(frame, len(s) - 2, 3):
        out.append(CODON_TABLE.get(s[i:i + 3], "X"))
    return "".join(out)


def random_dna(rng: random.Random, n: int, gc: float = 0.5) -> str:
    """n random bases, independent, with P(G) = P(C) = gc/2 and P(A) = P(T) = (1 - gc)/2.

    Draw order: one rng.random() per base, from left to right.
    """
    if not 0.0 <= gc <= 1.0:
        raise ValueError("gc must be in [0, 1]")
    half_gc, cut = gc / 2.0, gc + (1.0 - gc) / 2.0
    out = []
    for _ in range(n):
        u = rng.random()
        if u < half_gc:
            out.append("C")
        elif u < gc:
            out.append("G")
        elif u < cut:
            out.append("A")
        else:
            out.append("T")
    return "".join(out)


def _other_base(rng: random.Random, base: str) -> str:
    """A base other than base, uniform among the other three (one rng.choice)."""
    return rng.choice([b for b in DNA if b != base])


def mutate(rng: random.Random, seq: str, rate: float) -> str:
    """Substitute each base with probability rate, uniformly by one of the other three.

    Draw order: for each position from left to right, one rng.random(); if it is
    below rate, one rng.choice for the new base. Letters other than A, C, G and T
    are kept and use no draw. No insertions or deletions.
    """
    out = []
    for c in seq:
        if c in DNA and rng.random() < rate:
            out.append(_other_base(rng, c))
        else:
            out.append(c)
    return "".join(out)


SimRead = namedtuple("SimRead", ["read", "pos", "strand", "true_seq"])


def simulate_reads(rng: random.Random, genome: str, n: int, length: int,
                   error_rate: float) -> List[SimRead]:
    """n single-end reads of the given length from both strands of genome.

    Each item is SimRead(read, pos, strand, true_seq): pos is the 0-based start
    of the read on the forward strand of genome, strand is "+" or "-", true_seq
    is the error-free read (genome[pos:pos + length], or its reverse complement
    for "-"), and read is true_seq with substitution errors at rate error_rate.

    Draw order for each read: rng.randrange(len(genome) - length + 1) for pos,
    then rng.random() < 0.5 for the "+" strand, then the draws of mutate on
    true_seq.
    """
    if length > len(genome) or length <= 0:
        raise ValueError("need 0 < length <= len(genome)")
    reads = []
    for _ in range(n):
        pos = rng.randrange(len(genome) - length + 1)
        strand = "+" if rng.random() < 0.5 else "-"
        frag = genome[pos:pos + length]
        true_seq = frag if strand == "+" else revcomp(frag)
        reads.append(SimRead(mutate(rng, true_seq, error_rate), pos, strand, true_seq))
    return reads


def phred_to_prob(q: float) -> float:
    """Error probability of the Phred score q: p = 10^(-q/10)."""
    return 10.0 ** (-q / 10.0)


def prob_to_phred(p: float) -> float:
    """Phred score of the error probability p in (0, 1]: Q = -10 log10(p)."""
    if not 0.0 < p <= 1.0:
        raise ValueError("p must be in (0, 1]")
    return -10.0 * math.log10(p)


def hamming(a: Sequence, b: Sequence) -> int:
    """The number of positions where a and b differ; they must have the same length."""
    if len(a) != len(b):
        raise ValueError("hamming needs sequences of equal length")
    return sum(1 for x, y in zip(a, b) if x != y)


def kmers(seq: str, k: int) -> List[str]:
    """All len(seq) - k + 1 substrings of length k, from left to right (with repeats)."""
    if k <= 0:
        raise ValueError("k must be positive")
    return [seq[i:i + k] for i in range(len(seq) - k + 1)]


def gc_content(seq: str) -> float:
    """The fraction of G and C letters in seq (upper or lower case); 0.0 for an empty seq."""
    if not seq:
        return 0.0
    s = seq.upper()
    return (s.count("G") + s.count("C")) / len(s)


Number = Union[int, float]


def _cigar(ops: List[str]) -> str:
    """Run-length code a list of single-letter operations, for example MMMID to 3M1I1D."""
    out = []
    i = 0
    while i < len(ops):
        j = i
        while j < len(ops) and ops[j] == ops[i]:
            j += 1
        out.append(f"{j - i}{ops[i]}")
        i = j
    return "".join(out)


def _fill(a: str, b: str, match: Number, mismatch: Number, gap: Number, free_b_ends: bool):
    """The dynamic programming table of a linear gap alignment of a and b."""
    n, m = len(a), len(b)
    S = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        S[i][0] = i * gap
    for j in range(1, m + 1):
        S[0][j] = 0 if free_b_ends else j * gap
    for i in range(1, n + 1):
        ai = a[i - 1]
        row, up = S[i], S[i - 1]
        for j in range(1, m + 1):
            diag = up[j - 1] + (match if ai == b[j - 1] else mismatch)
            row[j] = max(diag, up[j] + gap, row[j - 1] + gap)
    return S


def _trace(S, a: str, b: str, i: int, j: int, match: Number, mismatch: Number,
           gap: Number, free_b_ends: bool) -> Tuple[List[str], int]:
    """Trace back from cell (i, j); prefer M, then I, then D. Returns the ops and the start in b."""
    ops: List[str] = []
    while i > 0 or (j > 0 and not free_b_ends):
        if i > 0 and j > 0 and S[i][j] == S[i - 1][j - 1] + (match if a[i - 1] == b[j - 1] else mismatch):
            ops.append("M")
            i, j = i - 1, j - 1
        elif i > 0 and S[i][j] == S[i - 1][j] + gap:
            ops.append("I")
            i -= 1
        else:
            ops.append("D")
            j -= 1
    ops.reverse()
    return ops, j


def global_align(a: str, b: str, match: Number = 1, mismatch: Number = -1,
                 gap: Number = -1) -> Tuple[Number, str]:
    """Needleman-Wunsch alignment of all of a with all of b, with linear gaps.

    Returns (score, cigar). The cigar uses M, I (a base of a only) and D (a base of
    b only); an empty alignment gives "".
    """
    S = _fill(a, b, match, mismatch, gap, False)
    ops, _ = _trace(S, a, b, len(a), len(b), match, mismatch, gap, False)
    return S[len(a)][len(b)], _cigar(ops)


def semiglobal_align(a: str, b: str, match: Number = 1, mismatch: Number = -1,
                     gap: Number = -1, with_start: bool = False):
    """Align all of a (the query) to a substring of b (the reference), with linear gaps.

    Bases of b before and after the aligned part cost nothing and are not in the
    cigar, as in SAM. Returns (score, cigar), or (score, cigar, start) with
    with_start=True, where start is the 0-based position in b of the first
    reference base of the alignment. Among best end columns the leftmost wins.
    """
    S = _fill(a, b, match, mismatch, gap, True)
    n = len(a)
    best_j = max(range(len(b) + 1), key=lambda j: (S[n][j], -j))
    ops, start = _trace(S, a, b, n, best_j, match, mismatch, gap, True)
    if with_start:
        return S[n][best_j], _cigar(ops), start
    return S[n][best_j], _cigar(ops)
