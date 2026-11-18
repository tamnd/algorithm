# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyphenation-pattern-generation/. The authors are listed in prov/980NJ6.jsonl.

"""Hyphenation pattern generation in the manner of Liang's patgen.

The input is a list of words with their correct hyphen positions. The
output is a set of patterns for Liang's rule (the largest digit at each gap
wins, odd allows a hyphen, even forbids it).

Patterns are chosen one level at a time. Odd levels add hyphenating
patterns, even levels add inhibiting patterns. Inside a level, the patterns
of each length are chosen in separate passes, one pass for each position of
the gap (the "dot") inside the pattern, so a pattern of length k takes k + 1
passes. Each pass hyphenates the whole word list with the patterns chosen so
far, and counts, for each candidate, the gaps where it would help (good) and
where it would hurt (bad):

- at an odd level, good is a correct hyphen that is not found yet, and bad
  is a gap with no hyphen that is not hyphenated now;
- at an even level, good is a wrong hyphen that the patterns now give, and
  bad is a correct hyphen that they find now.

A candidate is kept when good_wt * good - bad_wt * bad >= thresh, the rule
of patgen. Only the gaps at least left letters from the start and right
letters from the end are counted.

This version keeps the counting simple: it counts every candidate in a
dict. patgen counts in a packed trie and drops hopeless candidates early.
"""

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

Patterns = Dict[str, List[int]]  # letters -> gap values, as in parse_pattern


@dataclass(frozen=True)
class Level:
    """The parameters of one level: weights, threshold, pattern lengths."""

    good_wt: int
    bad_wt: int
    thresh: int
    min_len: int
    max_len: int


@dataclass
class LevelReport:
    level: int
    patterns: int  # patterns chosen at this level
    passes: int
    found: int  # correct hyphens found after the level
    errors: int  # wrong hyphens after the level
    missed: int  # correct hyphens not found after the level


def parse_hyphenated(entry: str) -> Tuple[str, frozenset]:
    """'hy-phen-ation' -> ('hyphenation', {2, 6}): k means a hyphen before word[k]."""
    word, pos, k = [], set(), 0
    for ch in entry:
        if ch == "-":
            pos.add(k)
        else:
            word.append(ch)
            k += 1
    return "".join(word), frozenset(pos)


def gap_values(word: str, patterns: Patterns) -> List[int]:
    """Liang's rule: v[k] is the value of the gap before word[k], k = 0 .. len(word)."""
    w = "." + word + "."
    v = [0] * (len(w) + 1)
    lengths = sorted({len(p) for p in patterns})
    for i in range(len(w)):
        for k in lengths:
            if i + k > len(w):
                break
            vals = patterns.get(w[i : i + k])
            if vals is not None:
                for t, d in enumerate(vals):
                    if d > v[i + t]:
                        v[i + t] = d
    return v[1 : len(word) + 2]


def counted_gaps(n: int, left: int, right: int) -> range:
    return range(max(1, left), n - max(1, right) + 1)


def hyphens(word: str, patterns: Patterns, left: int, right: int) -> set:
    v = gap_values(word, patterns)
    return {k for k in counted_gaps(len(word), left, right) if v[k] % 2 == 1}


def add_pattern(patterns: Patterns, letters: str, dot: int, value: int) -> None:
    vals = patterns.setdefault(letters, [0] * (len(letters) + 1))
    vals[dot] = max(vals[dot], value)


def generate(
    entries: Sequence[str],
    levels: Sequence[Level],
    left: int = 2,
    right: int = 2,
) -> Tuple[Patterns, List[LevelReport]]:
    """Generate patterns from hyphenated words, level by level."""
    words = [parse_hyphenated(e.lower()) for e in entries]
    patterns: Patterns = {}  # @line G1
    reports: List[LevelReport] = []
    for lev, par in enumerate(levels, start=1):  # @line G2
        odd = lev % 2 == 1
        chosen = 0
        passes = 0
        for k in range(par.min_len, par.max_len + 1):  # @line G3
            for dot in range(k + 1):  # @line G4
                passes += 1
                count: Dict[str, List[int]] = {}  # @line G5
                for word, true in words:  # @line G6
                    v = gap_values(word, patterns)  # @line G7
                    w = "." + word + "."
                    for g in counted_gaps(len(word), left, right):  # @line G8
                        is_hyphen, now = g in true, v[g] % 2 == 1
                        if odd:
                            good, bad = is_hyphen and not now, (not is_hyphen) and not now
                        else:
                            good, bad = (not is_hyphen) and now, is_hyphen and now
                        if not (good or bad):
                            continue
                        start = g + 1 - dot  # gap g of the word is gap g + 1 of w
                        if start < 0 or start + k > len(w):
                            continue
                        letters = w[start : start + k]  # @line G9
                        c = count.setdefault(letters, [0, 0])
                        c[0 if good else 1] += 1  # @line G10
                for letters, (good, bad) in sorted(count.items()):  # @line G11
                    if par.good_wt * good - par.bad_wt * bad >= par.thresh:  # @line G12
                        add_pattern(patterns, letters, dot, lev)  # @line G13
                        chosen += 1
        found = errors = missed = 0
        for word, true in words:
            h = hyphens(word, patterns, left, right)
            t = {g for g in true if g in counted_gaps(len(word), left, right)}
            found += len(h & t)
            errors += len(h - t)
            missed += len(t - h)
        reports.append(LevelReport(lev, chosen, passes, found, errors, missed))
    return patterns, reports  # @line G14


def pattern_strings(patterns: Patterns) -> List[str]:
    """The patterns in the usual notation, for example 'hy3ph'."""
    out = []
    for letters, vals in sorted(patterns.items()):
        s = []
        for t, ch in enumerate(letters):
            if vals[t]:
                s.append(str(vals[t]))
            s.append(ch)
        if vals[len(letters)]:
            s.append(str(vals[len(letters)]))
        out.append("".join(s))
    return out
