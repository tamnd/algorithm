# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz78-parsing/. The authors are listed in prov/HYAQNT.jsonl.

"""The LZ78 parsing of a string, computed with a trie of the phrases.

Each phrase is the longest prefix of the rest of the string that is already
a phrase (or the empty string), plus the next symbol. The last phrase may
lack the extra symbol when the string ends inside a known phrase.
"""

from collections.abc import Sequence


def lz78_parse(t: Sequence) -> list[tuple[int, int]]:
    """Return (start, length) for each phrase, in order."""
    children: list[dict] = [{}]  # node 0 is the root, the empty phrase
    out: list[tuple[int, int]] = []
    start, v = 0, 0
    for i, c in enumerate(t):
        w = children[v].get(c)
        if w is not None:
            v = w
            continue
        children[v][c] = len(children)
        children.append({})
        out.append((start, i + 1 - start))
        start, v = i + 1, 0
    if start < len(t):
        out.append((start, len(t) - start))
    return out
