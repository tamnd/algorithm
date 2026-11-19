# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phrase-pair-extraction/. The authors are listed in prov/ZVR7MS.jsonl.

"""Phrase pair extraction from a word-aligned sentence pair (Koehn, Och and Marcu 2003).

The source sentence f has m words and the target sentence e has l words. A link
is a pair (j, i) with source position j in 1 .. m and target position i in
1 .. l. A span (s, t) is fencepost: it covers the words s + 1 .. t. A phrase
pair is ((s, t), (u, v)), a source span and a target span.

A pair is consistent with the alignment A when it holds at least one link and
no link joins a word inside the pair to a word outside it. extract_phrase_pairs
returns every consistent pair with both sides of at most max_len words (7 is
the Moses default).
"""

from typing import Iterable

Link = tuple[int, int]
Span = tuple[int, int]
Pair = tuple[Span, Span]


def extract_phrase_pairs(m: int, l: int, links: Iterable[Link], max_len: int = 7) -> set[Pair]:
    """All phrase pairs consistent with the links, each side at most max_len words."""
    a = sorted(set(links))
    for j, i in a:
        if not (1 <= j <= m and 1 <= i <= l):
            raise ValueError(f"link {(j, i)} is outside the sentences")
    tgt_aligned = [False] * (l + 2)
    for _, i in a:
        tgt_aligned[i] = True
    pairs: set[Pair] = set()  # @line L1
    for s in range(m):  # @line L2
        for t in range(s + 1, min(m, s + max_len) + 1):  # @line L3
            targets = [i for j, i in a if s < j <= t]  # @line L4
            if not targets:  # @line L5
                continue
            u, v = min(targets) - 1, max(targets)  # @line L6
            if any(u < i <= v and not (s < j <= t) for j, i in a):  # @line L7
                continue
            u2 = u  # @line L8
            while True:  # @line L9
                v2 = v  # @line L10
                while True:  # @line L11
                    if v2 - u2 <= max_len:  # @line L12
                        pairs.add(((s, t), (u2, v2)))
                    v2 += 1  # @line L13
                    if v2 > l or tgt_aligned[v2]:  # @line L14
                        break
                u2 -= 1  # @line L15
                if u2 < 0 or tgt_aligned[u2 + 1]:  # @line L16
                    break
    return pairs  # @line L17


def is_consistent(pair: Pair, links: Iterable[Link]) -> bool:
    """The definition: at least one link inside, and no link that leaves the pair."""
    (s, t), (u, v) = pair
    inside = False
    for j, i in links:
        js, it = s < j <= t, u < i <= v
        if js and it:
            inside = True
        elif js or it:
            return False
    return inside


def brute_force_pairs(m: int, l: int, links: Iterable[Link], max_len: int = 7) -> set[Pair]:
    """Test every pair of a source span and a target span against the definition."""
    a = list(links)
    out = set()
    for s in range(m):
        for t in range(s + 1, min(m, s + max_len) + 1):
            for u in range(l):
                for v in range(u + 1, min(l, u + max_len) + 1):
                    if is_consistent(((s, t), (u, v)), a):
                        out.add(((s, t), (u, v)))
    return out


def phrase_strings(f: list[str], e: list[str], pairs: Iterable[Pair]) -> list[tuple[str, str]]:
    """The pairs as strings, sorted by source span and then by target span."""
    return [(" ".join(f[s:t]), " ".join(e[u:v])) for (s, t), (u, v) in sorted(pairs)]
