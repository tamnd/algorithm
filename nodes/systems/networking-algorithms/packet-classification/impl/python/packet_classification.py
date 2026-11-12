# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/packet-classification/. The authors are listed in prov/JDP7S8.jsonl.

"""Packet classification: the linear-search reference and range-to-prefix expansion.

A rule is a tuple of d closed ranges (lo, hi), one for each header field.
A prefix field (p, l) of a W-bit field is the range given by prefix_range.
The rules are in priority order: the first rule that matches wins.
"""

from itertools import product
from typing import Optional, Sequence

Range = tuple[int, int]
Rule = Sequence[Range]


def prefix_range(p: int, l: int, w: int) -> Range:
    """The addresses matched by the l-bit prefix p of a w-bit field."""
    lo = p << (w - l)
    return lo, lo + (1 << (w - l)) - 1


def matches(rule: Rule, packet: Sequence[int]) -> bool:
    return all(lo <= x <= hi for (lo, hi), x in zip(rule, packet))


def linear_classify(rules: Sequence[Rule], packet: Sequence[int]) -> Optional[int]:
    """The index of the first rule that matches the packet, or None."""
    for i in range(len(rules)):  # @line L1
        if matches(rules[i], packet):  # @line L2
            return i  # @line L3
    return None  # @line L4


def range_to_prefixes(lo: int, hi: int, w: int) -> list[tuple[int, int]]:
    """Split [lo, hi] into the fewest prefixes (p, l) of a w-bit field.

    Greedy: from the left end, take the largest aligned block that starts
    at lo and does not pass hi.
    """
    if not 0 <= lo <= hi < (1 << w):
        raise ValueError("need 0 <= lo <= hi < 2**w")
    out = []
    while lo <= hi:
        size = lo & -lo if lo else 1 << w  # the largest block aligned at lo
        while size > hi - lo + 1:
            size >>= 1
        k = size.bit_length() - 1  # the block has 2**k addresses
        out.append((lo >> k, w - k))
        lo += size
    return out


def expand_rule(rule: Rule, widths: Sequence[int]) -> list[tuple[tuple[int, int], ...]]:
    """All prefix rules (one prefix per field) whose union is the rule."""
    parts = [range_to_prefixes(lo, hi, w) for (lo, hi), w in zip(rule, widths)]
    return list(product(*parts))


def ternary_classify(entries, widths, packet) -> Optional[int]:
    """A TCAM model: entries are (prefix tuple, rule index) in order."""
    for prefixes, idx in entries:
        if all(x >> (w - l) == p for (p, l), w, x in zip(prefixes, widths, packet)):
            return idx
    return None


def to_tcam(rules: Sequence[Rule], widths: Sequence[int]):
    entries = []
    for i, rule in enumerate(rules):
        for prefixes in expand_rule(rule, widths):
            entries.append((prefixes, i))
    return entries
