# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dipre/. The authors are listed in prov/RKXK3C.jsonl.

"""DIPRE, Dual Iterative Pattern Relation Expansion (Brin 1998), on a small set of pages.

A page is a pair (url, text). A relation pair is (author, title). The loop:

- find_occurrences: every place where both strings of a known pair appear close
  together on a page, with the order, the url, m characters before (prefix),
  the text between (middle) and m characters after (suffix);
- generate_patterns: group the occurrences by order and middle; a group gives the
  pattern (order, urlprefix, prefix, middle, suffix), where urlprefix is the
  longest common prefix of the urls, prefix the longest common suffix of the
  prefixes and suffix the longest common prefix of the suffixes; the pattern is
  kept if n > 1 and specificity * n > t, else the group is split by the next
  character of the urls and each part is tried again;
- match_pattern: all pairs that the pattern finds on pages whose url starts with
  urlprefix;
- dipre: repeat until no new pair is found or the round limit is reached.

As a simple guard on what a pattern may extract, a field (the author or the
title in a match) is any string of 1 to max_len characters with no '<', '>'
or newline.
"""

from bisect import bisect_left, bisect_right
from collections import defaultdict, namedtuple
from typing import Dict, Iterable, List, Sequence, Set, Tuple

Occurrence = namedtuple("Occurrence", "author title order url prefix middle suffix")
Pattern = namedtuple("Pattern", "order urlprefix prefix middle suffix")
Page = Tuple[str, str]
Pair = Tuple[str, str]

FORBIDDEN = set("<>\n")


def lcp(strings: Sequence[str]) -> str:
    """Longest common prefix of a non-empty list of strings."""
    first, last = min(strings), max(strings)
    k = 0
    while k < len(first) and first[k] == last[k]:
        k += 1
    return first[:k]


def lcs(strings: Sequence[str]) -> str:
    """Longest common suffix of a non-empty list of strings."""
    return lcp([s[::-1] for s in strings])[::-1]


def find_all(text: str, s: str) -> List[int]:
    out, i = [], text.find(s)
    while i >= 0:
        out.append(i)
        i = text.find(s, i + 1)
    return out


def window(positions: List[int], lo: int, hi: int) -> List[int]:
    """The sorted positions p with lo <= p <= hi."""
    return positions[bisect_left(positions, lo):bisect_right(positions, hi)]


def find_occurrences(pages: Iterable[Page], pairs: Iterable[Pair], m: int = 10,
                     max_middle: int = 40) -> List[Occurrence]:
    """All occurrences of the pairs: the first string, then 1 to max_middle characters, then the second.
    order is True when the author comes first."""
    out = []
    pairs = sorted(pairs)
    for url, text in pages:
        for author, title in pairs:
            for order, first, second in ((True, author, title), (False, title, author)):
                seconds = find_all(text, second)
                for i in find_all(text, first):  # @line L3
                    a = i + len(first)
                    for j in window(seconds, a + 1, a + max_middle):
                        out.append(Occurrence(author, title, order, url, text[max(0, i - m):i],
                                              text[a:j], text[j + len(second):j + len(second) + m]))
    return out


def specificity(p: Pattern) -> int:
    return len(p.middle) * len(p.urlprefix) * len(p.prefix) * len(p.suffix)


def _gen_one(group: List[Occurrence], t: int) -> List[Pattern]:
    if len(group) < 2:
        return []
    urls = [o.url for o in group]
    p = Pattern(group[0].order, lcp(urls), lcs([o.prefix for o in group]),  # @line L5
                group[0].middle, lcp([o.suffix for o in group]))
    if specificity(p) * len(group) > t:  # @line L6
        return [p]
    if len(set(urls)) == 1:
        return []
    k = len(p.urlprefix)
    parts: Dict[str, List[Occurrence]] = defaultdict(list)
    for o in group:  # @line L7
        parts[o.url[k:k + 1]].append(o)
    out = []
    for key in sorted(parts):
        out.extend(_gen_one(parts[key], t))
    return out


def generate_patterns(occs: Iterable[Occurrence], t: int) -> List[Pattern]:
    groups: Dict[Tuple[bool, str], List[Occurrence]] = defaultdict(list)
    for o in occs:  # @line L4
        groups[(o.order, o.middle)].append(o)
    out: Set[Pattern] = set()
    for key in sorted(groups):
        out.update(_gen_one(groups[key], t))
    return sorted(out)


def _field_ok(s: str, max_len: int) -> bool:
    return 1 <= len(s) <= max_len and not (set(s) & FORBIDDEN)


def match_pattern(p: Pattern, pages: Iterable[Page], max_len: int = 40) -> Set[Pair]:
    """All (author, title) pairs found by the pattern: prefix X middle Y suffix, url starting with urlprefix."""
    found = set()
    for url, text in pages:
        if not url.startswith(p.urlprefix):
            continue
        mids = find_all(text, p.middle)
        sufs = find_all(text, p.suffix)
        for i in find_all(text, p.prefix):
            x0 = i + len(p.prefix)
            for k in window(mids, x0 + 1, x0 + max_len):
                x = text[x0:k]
                if not _field_ok(x, max_len):
                    continue
                y0 = k + len(p.middle)
                for l in window(sufs, y0 + 1, y0 + max_len):
                    y = text[y0:l]
                    if _field_ok(y, max_len):
                        found.add((x, y) if p.order else (y, x))
    return found


def dipre(pages: Sequence[Page], seeds: Iterable[Pair], t: int, m: int = 10, rounds: int = 5,
          max_middle: int = 40, max_len: int = 40):
    """Run the loop. Return the final set of pairs and, per round, (occurrences, patterns, pairs)."""
    known: Set[Pair] = set(seeds)  # @line L1
    stats = []
    for _ in range(rounds):  # @line L2
        occs = find_occurrences(pages, known, m, max_middle)
        pats = generate_patterns(occs, t)
        new = set(known)
        for p in pats:  # @line L8
            new |= match_pattern(p, pages, max_len)
        stats.append((len(occs), len(pats), len(new)))
        if new == known:  # @line L9
            break
        known = new
    return known, stats  # @line L10
