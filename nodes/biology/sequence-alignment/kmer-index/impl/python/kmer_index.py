# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kmer-index/. The authors are listed in prov/3PGQMC.jsonl.

"""A direct-address k-mer index of a DNA text.

The index stores, for each of the 4^k codes, the sorted list of the positions
where that k-mer starts. The lists are laid out one after the other in one
array `pos`, and `off[c] .. off[c + 1] - 1` is the slot range of code c,
as in a counting sort. With `step > 1` only the positions that are multiples
of `step` are indexed (BLAT indexes the non-overlapping k-mers, step = k).
"""

VALUE = {"A": 0, "C": 1, "G": 2, "T": 3}


def kmer_codes(text: str, k: int, step: int = 1) -> list[tuple[int, int]]:
    """Return (position, code) for each k-mer of text made of A, C, G, T only.

    The code is the base-4 number of the k-mer, computed by a rolling update.
    K-mers that hold another letter (such as N) are skipped.
    """
    out = []
    mask = (1 << (2 * k)) - 1
    code = 0
    valid = 0  # number of valid letters at the end of the current window
    for i, ch in enumerate(text):
        v = VALUE.get(ch)
        if v is None:
            valid = 0
            code = 0
            continue
        code = ((code << 2) | v) & mask
        valid += 1
        p = i - k + 1
        if valid >= k and p % step == 0:
            out.append((p, code))
    return out


def encode(kmer: str) -> int:
    code = 0
    for ch in kmer:
        code = 4 * code + VALUE[ch]
    return code


class KmerIndex:
    def __init__(self, text: str, k: int, step: int = 1) -> None:
        if k < 1 or step < 1:
            raise ValueError("k and step must be positive")
        self.k = k
        self.step = step
        size = 4 ** k
        pairs = kmer_codes(text, k, step)
        cnt = [0] * size  # @line L1
        for _, c in pairs:  # @line L2: positions in increasing order
            cnt[c] += 1  # @line L3
        off = [0] * (size + 1)  # @line L4
        for c in range(size):
            off[c + 1] = off[c] + cnt[c]  # @line L5
        nxt = off[:size]  # @line L6
        pos = [0] * len(pairs)
        for p, c in pairs:  # @line L7
            pos[nxt[c]] = p  # @line L8
            nxt[c] += 1  # @line L9
        self.off = off  # @line L10
        self.pos = pos

    def lookup(self, kmer: str) -> list[int]:
        """Sorted start positions of kmer among the indexed positions."""
        if len(kmer) != self.k or any(ch not in VALUE for ch in kmer):  # @line L11
            return []
        c = encode(kmer)  # @line L12
        return self.pos[self.off[c]:self.off[c + 1]]  # @line L13

    def count(self, kmer: str) -> int:
        return len(self.lookup(kmer))

    def seed_hits(self, query: str) -> list[tuple[int, int]]:
        """All pairs (query position, text position) of equal k-mers.

        Every k-mer of the query is looked up, overlapping or not.
        """
        hits = []  # @line L14
        for q, c in kmer_codes(query, self.k):  # @line L15
            for p in self.pos[self.off[c]:self.off[c + 1]]:  # @line L16
                hits.append((q, p))
        return hits  # @line L17


def naive_lookup(text: str, kmer: str, step: int = 1) -> list[int]:
    k = len(kmer)
    return [p for p in range(0, len(text) - k + 1, step) if text[p:p + k] == kmer]
