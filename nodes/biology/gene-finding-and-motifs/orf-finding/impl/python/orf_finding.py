# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orf-finding/. The authors are listed in prov/1C4YKG.jsonl.
"""Six-frame open reading frame finding.

An ORF is reported as Orf(strand, frame, start, end, codons):
- strand is "+" or "-";
- frame is 0, 1 or 2, the offset of the first codon on that strand (on the
  minus strand the offset is counted on the reverse complement);
- start and end are 0-based, half-open coordinates on the forward strand, so
  seq[start:end] is the ORF for "+" and revcomp(seq[start:end]) for "-";
- codons is the number of sense codons, so the stop codon is not counted.

Two definitions are supported:
- mode="start-stop": from a start codon to the next in-frame stop codon, the
  stop included. For each stop only the longest ORF is kept, the one that
  begins at the first start codon after the previous in-frame stop.
- mode="stop-stop": the codons after an in-frame stop (or from the first full
  codon of the frame) up to and including the next in-frame stop.

A reading frame that reaches the end of the sequence without a stop is not
reported; it has no defined end.
"""

from __future__ import annotations

from collections import namedtuple
from typing import Iterable, List

from bioseq import STOPS, revcomp

Orf = namedtuple("Orf", ["strand", "frame", "start", "end", "codons"])


def _scan_frame(t: str, f: int, min_codons: int, starts: frozenset, mode: str):
    """ORFs of one frame of one strand, as (start, end, codons) on that strand."""
    out = []
    opened = None if mode == "start-stop" else f
    for i in range(f, len(t) - 2, 3):  # @line L3
        c = t[i:i + 3]
        if c in STOPS:  # @line L4
            if opened is not None and (i - opened) // 3 >= min_codons:  # @line L5
                out.append((opened, i + 3, (i - opened) // 3))  # @line L6
            opened = None if mode == "start-stop" else i + 3  # @line L7
        elif opened is None and c in starts:  # @line L8
            opened = i  # @line L9
    return out


def find_orfs(seq: str, min_codons: int = 100, mode: str = "start-stop",
              starts: Iterable[str] = ("ATG",)) -> List[Orf]:
    """All ORFs of seq in the six frames with at least min_codons sense codons.

    The result is sorted by (start, end, strand, frame).
    """
    if mode not in ("start-stop", "stop-stop"):
        raise ValueError("mode must be 'start-stop' or 'stop-stop'")
    s = seq.upper()
    G = len(s)
    start_set = frozenset(c.upper() for c in starts)
    found = []
    for strand, t in (("+", s), ("-", revcomp(s))):  # @line L1
        for f in range(3):  # @line L2
            for a, b, n in _scan_frame(t, f, min_codons, start_set, mode):
                if strand == "+":  # @line L10
                    found.append(Orf("+", f, a, b, n))
                else:
                    found.append(Orf("-", f, G - b, G - a, n))
    found.sort(key=lambda o: (o.start, o.end, o.strand, o.frame))
    return found  # @line L11


def orf_sequence(seq: str, orf: Orf) -> str:
    """The bases of an ORF, 5' to 3' on its own strand."""
    part = seq.upper()[orf.start:orf.end]
    return part if orf.strand == "+" else revcomp(part)


def longest_orf(seq: str, mode: str = "start-stop") -> Orf:
    """The ORF with the most codons (any length), or None if there is none."""
    orfs = find_orfs(seq, 0, mode)
    if not orfs:
        return None
    return max(orfs, key=lambda o: (o.codons, -o.start))
