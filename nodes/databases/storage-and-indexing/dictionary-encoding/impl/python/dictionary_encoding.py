# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dictionary-encoding/. The authors are listed in prov/4407VK.jsonl.

"""Dictionary encoding of one column, with and without order preservation.

The dictionary D lists the distinct non-null values of the column. Value D[x]
has the code x + 1, and NULL has the code 0. In an ordered dictionary D is
sorted, so that a < b if and only if code(a) < code(b); in an unordered one D
is in order of first appearance. The codes are packed, w bits each, into a
bytearray, least significant bit first, where w is the number of bits of |D|.

A selection with a comparison (=, <>, <, <=, >, >=) and a constant returns the
positions where it holds; a comparison with NULL never holds. An ordered
dictionary turns a range predicate into a range of codes with two binary
searches. An unordered one must compare the constant with every entry of D.
The counters self.compares and self.decodes count comparisons of values and
lookups of D, so that tests can check that a scan works on codes only.
"""

import bisect
import operator
from typing import Dict, List, Optional, Sequence, Set

OPS = {"=": operator.eq, "<>": operator.ne, "<": operator.lt,
       "<=": operator.le, ">": operator.gt, ">=": operator.ge}


class DictColumn:
    def __init__(self, values: Sequence[object], ordered: bool = True) -> None:
        self.ordered = ordered
        distinct = list(dict.fromkeys(v for v in values if v is not None))
        self.D: List[object] = sorted(distinct) if ordered else distinct   # @line L1
        self.code: Dict[object, int] = {v: x + 1 for x, v in enumerate(self.D)}  # @line L2
        self.w = max(1, len(self.D).bit_length())             # @line L3
        self.n = len(values)
        self.bits = bytearray((self.n * self.w + 7) // 8)
        for i, v in enumerate(values):                        # @line L4
            self._put(i, 0 if v is None else self.code[v])    # @line L2 L4
        self.compares = 0
        self.decodes = 0

    # ------------------------------------------------------------ bits

    def _put(self, i: int, x: int) -> None:
        pos = i * self.w
        for b in range(self.w):
            if x >> b & 1:
                self.bits[(pos + b) >> 3] |= 1 << ((pos + b) & 7)

    def code_at(self, i: int) -> int:
        pos, x = i * self.w, 0                                # @line L5
        for b in range(self.w):                               # @line L5
            x |= (self.bits[(pos + b) >> 3] >> ((pos + b) & 7) & 1) << b  # @line L5
        return x

    def size_bytes(self) -> int:
        return len(self.bits)

    # ------------------------------------------------------------ decode

    def decode(self, i: int) -> object:
        x = self.code_at(i)
        if x == 0:                                            # @line L6
            return None                                       # @line L6
        self.decodes += 1
        return self.D[x - 1]                                  # @line L6

    def decode_all(self) -> List[object]:
        return [self.decode(i) for i in range(self.n)]

    # ------------------------------------------------------------ select

    def code_range(self, op: str, v: object) -> Optional[range]:
        """For an ordered dictionary: the codes whose values satisfy op v, as a range."""
        lo = bisect.bisect_left(self.D, v)     # first entry >= v
        hi = bisect.bisect_right(self.D, v)    # first entry > v
        self.compares += 2 * max(1, len(self.D)).bit_length()
        first, last = {"=": (lo, hi), "<": (0, lo), "<=": (0, hi),
                       ">": (hi, len(self.D)), ">=": (lo, len(self.D))}[op]
        return range(first + 1, last + 1)

    def matching_codes(self, op: str, v: object) -> Set[int]:
        """For any dictionary: the codes whose values satisfy op v, by |D| comparisons."""
        self.compares += len(self.D)
        return {x + 1 for x, d in enumerate(self.D) if OPS[op](d, v)}

    def select(self, op: str, v: object) -> List[int]:
        if op not in OPS:
            raise ValueError(f"unknown comparison {op}")
        if v is None:
            return []
        if self.ordered and op != "<>":                       # @line L7
            r = self.code_range(op, v)                        # @line L8
            return [i for i in range(self.n) if r.start <= self.code_at(i) < r.stop]  # @line L9
        if op == "<>" and v in self.code:                     # the complement of one code
            c = self.code[v]
            return [i for i in range(self.n) if self.code_at(i) not in (0, c)]
        S = self.matching_codes(op, v)                        # @line L10 L11
        return [i for i in range(self.n) if self.code_at(i) in S]  # @line L12
