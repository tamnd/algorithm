# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discordant-read-pair-method/. The authors are listed in prov/47N3AD.jsonl.
"""Structural variant calls from discordant read pairs, on one chromosome.

A pair is (pos1, strand1, pos2, strand2): the 0-based leftmost reference
positions of the two mates with pos1 <= pos2, and their strands "+" or "-".
Both mates have the read length L. The library has the forward-reverse (FR)
layout: a normal pair is "+" then "-", and its insert size, the span
pos2 + L - pos1, is close to the mean mu with standard deviation sigma.

A pair is discordant when its layout or its span does not fit the library:

- "+-" with span > mu + z sigma: DEL (a deletion in the sample);
- "+-" with span < mu - z sigma: INS (an insertion in the sample);
- "++" or "--": INV (one mate is inside an inversion);
- "-+": DUP (a tandem duplication).

Two discordant pairs of the same type are linked when both their left
mates and their right mates start at most d apart. A cluster is a connected
component of this relation, and a cluster with at least min_support pairs
is a call. The default d is mu + z sigma, the largest distance two pairs
that cross the same breakpoint can have at one end.

What this code leaves out compared with tools such as BreakDancer or DELLY:
several chromosomes and translocations, mapping quality, pairs where one
mate does not map, the probability score of a call, the split-read
refinement of the breakpoints, and genotypes.
"""

from __future__ import annotations

from statistics import median
from typing import Dict, List, Sequence, Tuple

Pair = Tuple[int, str, int, str]


def library_stats(spans: Sequence[int]) -> Tuple[float, float]:
    """Robust mean and standard deviation of the insert size: the median and 1.4826 times the MAD."""
    mu = float(median(spans))
    mad = float(median(abs(s - mu) for s in spans))
    return mu, 1.4826 * mad


def span(pair: Pair, L: int) -> int:
    return pair[2] + L - pair[0]


def classify(pair: Pair, L: int, mu: float, sigma: float, z: float = 3.0) -> str:
    """"DEL", "INS", "INV", "DUP" or "" for a concordant pair."""
    s1, s2 = pair[1], pair[3]
    if s1 == s2:
        return "INV"
    if s1 == "-":
        return "DUP"
    x = span(pair, L)
    if x > mu + z * sigma:
        return "DEL"
    if x < mu - z * sigma:
        return "INS"
    return ""


class _DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, a: int) -> int:
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a: int, b: int) -> None:
        a, b = self.find(a), self.find(b)
        if a != b:
            self.parent[max(a, b)] = min(a, b)


def cluster(pairs: Sequence[Pair], d: float) -> List[List[int]]:
    """Connected components of the relation |pos1 - pos1'| <= d and |pos2 - pos2'| <= d.

    All pairs must have the same type and strand layout. Returns lists of indices into pairs,
    each sorted, in the order of their smallest index.
    """
    order = sorted(range(len(pairs)), key=lambda i: pairs[i][0])  # @line L4
    dsu = _DSU(len(pairs))
    for a, i in enumerate(order):  # @line L5
        for j in order[a + 1:]:
            if pairs[j][0] - pairs[i][0] > d:
                break
            if abs(pairs[j][2] - pairs[i][2]) <= d:  # @line L6
                dsu.union(i, j)  # @line L7
    groups: Dict[int, List[int]] = {}
    for i in range(len(pairs)):
        groups.setdefault(dsu.find(i), []).append(i)
    return [groups[r] for r in sorted(groups)]


def call_svs(pairs: Sequence[Pair], L: int, mu: float, sigma: float, z: float = 3.0,
             min_support: int = 3, d: float = None) -> List[dict]:
    """Return the calls, sorted by type, strands and position.

    Pairs are clustered separately for each type and strand layout, so the
    "++" and "--" pairs of one inversion give two calls, one for each of its
    breakpoints. Each call is a dict with the keys type, strands, support,
    left and right, and for DEL and INS also size. left and right bound the
    breakpoints, as the end (or start) of the mates nearest to them:

    - DEL, INS and INV "++": left is the largest end of a left mate, so the
      left breakpoint is at or after left;
    - DUP and INV "--": left is the smallest start of a left mate, so the
      left breakpoint is at or before left;
    - DEL, INS and INV "--": right is the smallest start of a right mate, so
      the right breakpoint is at or before right;
    - DUP and INV "++": right is the largest end of a right mate, so the
      right breakpoint is at or after right.

    The size of a DEL is the median span of its pairs minus mu, and the size
    of an INS is mu minus the median span.
    """
    if d is None:
        d = mu + z * sigma
    by_type: Dict[Tuple[str, str], List[Pair]] = {}
    for p in pairs:  # @line L1
        t = classify(p, L, mu, sigma, z)  # @line L2
        if t:
            by_type.setdefault((t, p[1] + p[3]), []).append(p)  # @line L3
    calls = []
    for t, strands in sorted(by_type):
        group = by_type[(t, strands)]
        for members in cluster(group, d):
            if len(members) < min_support:  # @line L8
                continue
            ps = [group[i] for i in members]
            starts_left = t == "DUP" or strands == "--"
            ends_right = t == "DUP" or strands == "++"
            call = {
                "type": t,
                "strands": strands,
                "support": len(ps),
                "left": min(p[0] for p in ps) if starts_left else max(p[0] + L for p in ps),
                "right": max(p[2] + L for p in ps) if ends_right else min(p[2] for p in ps),
            }  # @line L9
            spans = [span(p, L) for p in ps]
            if t == "DEL":
                call["size"] = float(median(spans)) - mu
            elif t == "INS":
                call["size"] = mu - float(median(spans))
            calls.append(call)
    calls.sort(key=lambda c: (c["type"], c["strands"], c["left"]))
    return calls  # @line L10
