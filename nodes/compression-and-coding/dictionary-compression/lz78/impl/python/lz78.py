# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz78/. The authors are listed in prov/ZJ9XSK.jsonl.

"""LZ78 (Ziv and Lempel, 1978): an explicit dictionary of phrases in a trie.

The output is a list of pairs (j, c): phrase j of the dictionary (0 is the
empty phrase) followed by the byte c. The new phrase gets the next number.
If the input ends inside a known phrase, the last pair is (j, None).
"""

Pair = tuple[int, int | None]


def lz78_encode(data: bytes) -> list[Pair]:
    # The trie is a map from (node, byte) to the child node; node 0 is the root.
    child: dict[tuple[int, int], int] = {}  # @line L1
    nxt = 1
    out: list[Pair] = []  # @line L2
    v = 0
    for c in data:  # @line L3
        w = child.get((v, c))
        if w is not None:  # @line L4
            v = w  # @line L5
        else:  # @line L6
            out.append((v, c))  # @line L7
            child[(v, c)] = nxt  # @line L8
            nxt += 1
            v = 0  # @line L9
    if v != 0:  # @line L10
        out.append((v, None))
    return out  # @line L11


def lz78_decode(pairs: list[Pair]) -> bytes:
    phrases: list[bytes] = [b""]  # @line L12
    s = bytearray()
    for j, c in pairs:  # @line L13
        if not 0 <= j < len(phrases):
            raise ValueError("phrase index is not in the dictionary yet")
        w = phrases[j] if c is None else phrases[j] + bytes([c])  # @line L14
        s += w  # @line L15
        phrases.append(w)
    return bytes(s)  # @line L16
