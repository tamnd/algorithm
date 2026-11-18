# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/liang-hyphenation/. The authors are listed in prov/6YQPVW.jsonl.

"""Liang's hyphenation algorithm, as in TeX82.

A pattern is a string of letters with a digit (0 to 9) in each gap, for
example "hy3ph" or ".ach4". A missing digit is 0. The mark "." stands for
the edge of the word. To hyphenate a word, put "." at both ends, find every
pattern that occurs in it, and at each gap take the largest digit of all
patterns that cover the gap. An odd value allows a hyphen, an even value
forbids it. Then remove the breaks that are too near the ends of the word
(lefthyphenmin and righthyphenmin of TeX).

The patterns are kept in a trie of nested dicts. The page packed-trie gives
the compact table that TeX uses for the same lookup.
"""

from typing import Dict, Iterable, List, Optional, Tuple


def parse_pattern(p: str) -> Tuple[str, List[int]]:
    """Split a pattern into its letters and its gap values.

    parse_pattern("hy3ph") == ("hyph", [0, 0, 3, 0, 0]). The list has one
    value per gap: before the first letter, between letters, and after the
    last letter.
    """
    letters: List[str] = []
    values: List[int] = [0]
    for ch in p:
        if ch.isdigit():
            values[-1] = int(ch)
        else:
            letters.append(ch)
            values.append(0)
    return "".join(letters), values


class PatternTrie:
    """A trie of patterns. Each node is a dict; the key None holds the values."""

    def __init__(self, patterns: Iterable[str] = ()) -> None:
        self.root: Dict = {}
        self.count = 0
        for p in patterns:
            self.add(p)

    def add(self, p: str) -> None:
        letters, values = parse_pattern(p)
        node = self.root
        for ch in letters:
            node = node.setdefault(ch, {})
        if None in node:
            # the same letters twice: keep the larger digit in each gap
            node[None] = [max(a, b) for a, b in zip(node[None], values)]
        else:
            node[None] = values
            self.count += 1


def hyphenation_values(word: str, trie: PatternTrie, stats: Optional[dict] = None) -> List[int]:
    """The gap values of the word: v[k] is the value of the gap before word[k].

    The list has len(word) + 1 entries; v[0] and v[len(word)] are the gaps
    at the edges. If stats is a dict, stats["steps"] counts the trie steps.
    """
    w = "." + word.lower() + "."  # @line L1
    v = [0] * (len(w) + 1)  # @line L2
    steps = 0
    for i in range(len(w)):  # @line L3
        node = trie.root  # @line L4
        for j in range(i, len(w)):  # @line L5
            steps += 1
            node = node.get(w[j])  # @line L6
            if node is None:
                break  # @line L7
            values = node.get(None)
            if values is not None:  # @line L8
                for t, d in enumerate(values):
                    if d > v[i + t]:
                        v[i + t] = d  # @line L9
    if stats is not None:
        stats["steps"] = steps
    # gap k of the word (before word[k]) is gap k + 1 of w
    return v[1 : len(word) + 2]


def hyphen_positions(
    word: str,
    trie: PatternTrie,
    left: int = 2,
    right: int = 3,
    exceptions: Optional[Dict[str, List[int]]] = None,
) -> List[int]:
    """The positions k (a hyphen goes before word[k]) that the patterns allow.

    left and right are lefthyphenmin and righthyphenmin; plain TeX uses 2
    and 3. exceptions maps a lowercase word to its positions, as the
    \\hyphenation list of TeX does, and overrides the patterns.
    """
    if exceptions is not None and word.lower() in exceptions:
        return list(exceptions[word.lower()])
    v = hyphenation_values(word, trie)
    n = len(word)
    return [k for k in range(1, n) if v[k] % 2 == 1 and k >= left and n - k >= right]  # @line L10


def hyphenate(word: str, trie: PatternTrie, left: int = 2, right: int = 3, exceptions=None) -> str:
    """The word with "-" at each allowed position, for examples."""
    pos = set(hyphen_positions(word, trie, left, right, exceptions))
    return "".join(("-" if k in pos else "") + ch for k, ch in enumerate(word))
