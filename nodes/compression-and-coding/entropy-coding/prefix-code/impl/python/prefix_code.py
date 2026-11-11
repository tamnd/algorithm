# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prefix-code/. The authors are listed in prov/M6D811.jsonl.
"""A binary prefix code: encoding, decoding by walking the code tree, and decoding by table lookup."""

from fractions import Fraction
from typing import Hashable, Mapping, Sequence


class DecodeError(ValueError):
    pass


class PrefixCode:
    def __init__(self, codewords: Mapping[Hashable, str]) -> None:
        if not codewords:
            raise ValueError("the code is empty")
        for w in codewords.values():
            if not w or set(w) - {"0", "1"}:
                raise ValueError("a codeword must be a non-empty bit string")
        self.code = dict(codewords)
        # The code tree as a binary trie: node = [child0, child1, symbol].
        self.root: list = [None, None, None]
        for sym, w in self.code.items():
            node = self.root
            for i, b in enumerate(w):
                if node[2] is not None:
                    raise ValueError("a codeword is a prefix of another codeword")
                child = node[int(b)]
                if child is None:
                    child = [None, None, None]
                    node[int(b)] = child
                node = child
            if node[2] is not None or node[0] is not None or node[1] is not None:
                raise ValueError("a codeword is a prefix of another codeword")
            node[2] = sym
        self.max_len = max(len(w) for w in self.code.values())
        self.table = self._build_table()

    def kraft_sum(self) -> Fraction:
        return sum((Fraction(1, 2 ** len(w)) for w in self.code.values()), Fraction(0))

    def is_complete(self) -> bool:
        """True when the Kraft sum is 1: every internal node of the code tree has two children."""
        return self.kraft_sum() == 1

    def encode(self, symbols: Sequence[Hashable]) -> str:
        return "".join(self.code[s] for s in symbols)

    def decode_tree(self, bits: str) -> list:
        """Walk from the root, one bit at a time, and emit a symbol at each leaf."""
        out, node = [], self.root
        for b in bits:
            node = node[int(b)]
            if node is None:
                raise DecodeError("the bits do not start with a codeword")
            if node[2] is not None:
                out.append(node[2])
                node = self.root
        if node is not self.root:
            raise DecodeError("the bits end inside a codeword")
        return out

    def _build_table(self) -> list:
        """Entry v (a max_len-bit number) holds (symbol, length) of the codeword that starts v, or None."""
        L = self.max_len
        table: list = [None] * (1 << L)
        for sym, w in self.code.items():
            lo = int(w, 2) << (L - len(w))
            for v in range(lo, lo + (1 << (L - len(w)))):
                table[v] = (sym, len(w))
        return table

    def decode_table(self, bits: str) -> list:
        """Read max_len bits at a time (pad with 0 at the end), look up the codeword, and skip its length."""
        L, n, out, i = self.max_len, len(bits), [], 0
        while i < n:
            window = bits[i:i + L].ljust(L, "0")
            entry = self.table[int(window, 2)]
            if entry is None:
                raise DecodeError("the bits do not start with a codeword")
            sym, length = entry
            if i + length > n:
                raise DecodeError("the bits end inside a codeword")
            out.append(sym)
            i += length
        return out
