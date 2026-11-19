# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hearst-patterns/. The authors are listed in prov/B0F1S5.jsonl.
"""Hearst patterns: find hyponym and hypernym noun phrases with six fixed
lexico-syntactic patterns.

A sentence is a list of items. An item is a noun phrase, given as a tuple of
tokens (the output of a chunker), or a single word given as a str, including
the comma ",". The six patterns, with the numbers of Hearst 1992:

  1  NP0 [,] such as LIST
  2  such NP0 as LIST
  3  LEFT [,] or other NP0
  4  LEFT [,] and other NP0
  5  NP0 [,] including LIST
  6  NP0 [,] especially LIST

LIST is NP ("," NP)* [[","] (and | or) NP], read to the right as far as it
goes, and LEFT is NP ("," NP)*, read to the left as far as it goes. Each NP of
the list is a hyponym of NP0.
"""

Item = tuple[str, ...] | str

CONJ = ("and", "or")


def is_np(items: list[Item], i: int) -> bool:
    return 0 <= i < len(items) and isinstance(items[i], tuple)


def word(items: list[Item], i: int) -> str | None:
    """The lowercased word at i, or None for a noun phrase or a position outside the list."""
    if 0 <= i < len(items) and isinstance(items[i], str):
        return items[i].lower()
    return None


def right_list(items: list[Item], q: int) -> list[int]:
    """The positions of the noun phrases of the longest LIST that starts at q."""
    if not is_np(items, q):
        return []
    out = [q]
    j = q + 1
    while True:
        if word(items, j) == "," and is_np(items, j + 1):
            out.append(j + 1)
            j += 2
        elif word(items, j) in CONJ and is_np(items, j + 1):
            out.append(j + 1)
            return out
        elif word(items, j) == "," and word(items, j + 1) in CONJ and is_np(items, j + 2):
            out.append(j + 2)
            return out
        else:
            return out


def left_list(items: list[Item], p: int) -> list[int]:
    """The positions of the noun phrases of the longest LEFT [,] that ends just before p."""
    j = p - 1
    if word(items, j) == ",":
        j -= 1
    if not is_np(items, j):
        return []
    out = [j]
    while word(items, j - 1) == "," and is_np(items, j - 2):
        j -= 2
        out.append(j)
    return out[::-1]


def np_before(items: list[Item], p: int) -> int | None:
    """The noun phrase just before p, with an optional comma between, or None."""
    if is_np(items, p - 1):
        return p - 1
    if word(items, p - 1) == "," and is_np(items, p - 2):
        return p - 2
    return None


def hearst_matches(items: list[Item]) -> list[tuple[int, int, int]]:
    """All (hyponym position, hypernym position, pattern) triples, in the order of the triggers.

    Cost: O(len(items)). A list holds only noun phrases, commas and one
    conjunction followed by a noun phrase, so it contains no trigger, the
    right lists do not overlap, the left lists do not overlap, and each item
    is read by at most two lists.
    """
    found: list[tuple[int, int, int]] = []  # @line L1
    for p in range(len(items)):  # @line L2
        w = word(items, p)
        if w == "such" and word(items, p + 1) == "as":  # @line L3
            h = np_before(items, p)
            if h is not None:
                found += [(x, h, 1) for x in right_list(items, p + 2)]
        elif w == "such" and is_np(items, p + 1) and word(items, p + 2) == "as":  # @line L4
            found += [(x, p + 1, 2) for x in right_list(items, p + 3)]
        elif w in ("including", "especially"):  # @line L5
            h = np_before(items, p)
            if h is not None:
                found += [(x, h, 5 if w == "including" else 6) for x in right_list(items, p + 1)]
        elif w in CONJ and word(items, p + 1) == "other" and is_np(items, p + 2):  # @line L6
            found += [(x, p + 2, 3 if w == "or" else 4) for x in left_list(items, p)]
    return found  # @line L7


def hearst_pairs(items: list[Item]) -> list[tuple[str, str, int]]:
    """The matches as (hyponym text, hypernym text, pattern)."""
    return [(" ".join(items[x]), " ".join(items[h]), k) for x, h, k in hearst_matches(items)]
