# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/duplicate-read-marking/. The authors are listed in prov/398WVT.jsonl.
"""Duplicate marking of mapped reads by the rule of Picard MarkDuplicates.

A Read is one mapped read: library, chrom, pos (1-based leftmost mapped
reference base, as in SAM), cigar, reverse (True for the reverse strand) and
quals (the Phred base qualities). A template is a tuple of one Read (a
fragment: a single-end read, or a pair whose mate did not map) or two Reads
(a pair with both mates mapped).

Two pairs are duplicates when they have the same library and the same
unclipped 5' end, chromosome and strand for both mates. A fragment is a
duplicate of another fragment with the same end, and of every pair with an
end at that place. In each group the template with the highest score is
kept; the score of a read is the sum of its base qualities of at least 15,
capped at 16383, and the score of a pair is the sum over its two reads. Ties
go to the template that comes first in the input.

Left out: optical duplicates (Picard looks at tile and pixel coordinates of
the read names), the large score discount for reads that fail vendor
checks, and the secondary and supplementary records.
"""

from __future__ import annotations

import re
from collections import namedtuple
from typing import Dict, List, Sequence, Set, Tuple

Read = namedtuple("Read", ["library", "chrom", "pos", "cigar", "reverse", "quals"])

_CIGAR = re.compile(r"(\d+)([MIDNSHP=X])")
_REF_OPS = set("MDN=X")


def parse_cigar(cigar: str) -> List[Tuple[int, str]]:
    ops = [(int(n), op) for n, op in _CIGAR.findall(cigar)]
    if "".join(f"{n}{op}" for n, op in ops) != cigar or not ops:
        raise ValueError(f"bad CIGAR {cigar!r}")
    return ops


def unclipped_five_prime(r: Read) -> int:
    """The 1-based reference position of the 5' end of the read, with clipped bases put back."""
    ops = parse_cigar(r.cigar)
    if not r.reverse:
        lead = 0
        for n, op in ops:
            if op not in "SH":
                break
            lead += n
        return r.pos - lead
    span = sum(n for n, op in ops if op in _REF_OPS)
    trail = 0
    for n, op in reversed(ops):
        if op not in "SH":
            break
        trail += n
    return r.pos + span - 1 + trail


def end_key(r: Read) -> Tuple:
    return (r.library, r.chrom, unclipped_five_prime(r), r.reverse)


def read_score(r: Read) -> int:
    return min(sum(q for q in r.quals if q >= 15), 16383)


def score(t: Sequence[Read]) -> int:
    return sum(read_score(r) for r in t)


def _best(group: List[int], scores: List[int]) -> int:
    return max(group, key=lambda i: (scores[i], -i))


def mark_duplicates(templates: Sequence[Sequence[Read]]) -> Set[int]:
    """The set of indices of the templates that are marked as duplicates."""
    pairs: Dict[Tuple, List[int]] = {}  # @line L1
    frags: Dict[Tuple, List[int]] = {}
    pair_ends: Set[Tuple] = set()
    scores = [score(t) for t in templates]
    for i, t in enumerate(templates):  # @line L2
        if len(t) == 2:  # @line L3
            e1, e2 = end_key(t[0]), end_key(t[1])
            pairs.setdefault(tuple(sorted((e1, e2))), []).append(i)
            pair_ends.update((e1, e2))
        elif len(t) == 1:
            frags.setdefault(end_key(t[0]), []).append(i)  # @line L4
        else:
            raise ValueError("a template has one or two reads")
    dups: Set[int] = set()  # @line L5
    for group in pairs.values():  # @line L6
        keep = _best(group, scores)
        dups.update(i for i in group if i != keep)
    for key, group in frags.items():  # @line L7
        if key in pair_ends:  # @line L8
            dups.update(group)
        else:  # @line L9
            keep = _best(group, scores)
            dups.update(i for i in group if i != keep)
    return dups  # @line L10
