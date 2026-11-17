# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variant-normalization/. The authors are listed in prov/YT7FC7.jsonl.
"""Normalization of a VCF-style variant (Tan, Abecasis and Kang 2015).

A variant is (pos, alleles): pos is the 1-based position of the first base
of the alleles on the reference, as in VCF, and alleles[0] is the reference
allele REF, equal to ref[pos - 1 : pos - 1 + len(REF)]. The other entries are
the ALT alleles. All alleles are non-empty strings over ACGT and pairwise
different.

normalize returns the unique left-aligned and parsimonious form. It needs
the reference base to the left of the variant whenever an allele becomes
empty; if the variant would have to move before position 1, it raises
ValueError (VCF then pads with the base after the event, which this code
leaves out).
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

Variant = Tuple[int, Tuple[str, ...]]


def check(ref: str, pos: int, alleles: Sequence[str]) -> None:
    """Raise ValueError unless (pos, alleles) is a valid variant on ref."""
    if len(alleles) < 2 or any(not a for a in alleles):
        raise ValueError("need REF and at least one ALT, all non-empty")
    if len(set(alleles)) != len(alleles):
        raise ValueError("alleles must be pairwise different")
    if pos < 1 or ref[pos - 1:pos - 1 + len(alleles[0])] != alleles[0]:
        raise ValueError("REF does not match the reference at pos")


def normalize(ref: str, pos: int, alleles: Sequence[str]) -> Variant:
    """The normalized form of the variant (pos, alleles) on the reference ref."""
    check(ref, pos, alleles)
    al: List[str] = list(alleles)
    changed = True
    while changed:  # @line L1
        changed = False  # @line L2
        if len({a[-1] for a in al}) == 1:  # @line L3
            al = [a[:-1] for a in al]
            changed = True
        if any(a == "" for a in al):  # @line L4
            if pos == 1:
                raise ValueError("the variant reaches position 1; pad on the right instead")
            pos -= 1  # @line L5
            al = [ref[pos - 1] + a for a in al]
            changed = True
    while len({a[0] for a in al}) == 1 and min(len(a) for a in al) >= 2:  # @line L6
        al = [a[1:] for a in al]  # @line L7
        pos += 1
    return pos, tuple(al)  # @line L8


def apply(ref: str, pos: int, ref_allele: str, alt: str) -> str:
    """The haplotype made by replacing ref_allele at pos (1-based) by alt."""
    i = pos - 1
    if ref[i:i + len(ref_allele)] != ref_allele:
        raise ValueError("REF does not match the reference at pos")
    return ref[:i] + alt + ref[i + len(ref_allele):]


def all_representations(ref: str, hap: str) -> List[Tuple[int, str, str]]:
    """Every (pos, REF, ALT) with non-empty alleles that turns ref into hap (brute force)."""
    out = []
    n = len(ref)
    for i in range(n):
        for j in range(i + 1, n + 1):
            head, tail = ref[:i], ref[j:]
            if len(head) + len(tail) >= len(hap) or not hap.startswith(head) or not hap.endswith(tail):
                continue
            alt = hap[len(head):len(hap) - len(tail)]
            if alt and alt != ref[i:j]:
                out.append((i + 1, ref[i:j], alt))
    return out
