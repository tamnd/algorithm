# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bpe-dropout/. The authors are listed in prov/ZZH1HW.jsonl.

"""BPE-dropout of Provilkov, Emelianenko and Voita (2020).

The merge table is the one of ordinary byte-pair encoding. To segment a word,
start from its characters and repeat: list every position where a pair of the
table occurs, drop each position on its own with probability p, and apply the
surviving merge of highest priority (lowest rank) at its surviving positions.
Stop when no position survives. With p = 0 this is plain BPE, and with p = 1
it returns the characters.

segment draws one segmentation with a random.Random. distribution gives the
exact probability of every segmentation, as Fractions, by enumeration.
"""

import random
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

Pair = Tuple[str, str]
Seg = Tuple[str, ...]


def _merge_at(units: Sequence[str], positions: Sequence[int]) -> List[str]:
    """Join units[i] and units[i + 1] for each i in positions, from the left,
    skipping a position that overlaps the previous join."""
    take, last = set(), -2
    for i in sorted(positions):
        if i > last + 1:
            take.add(i)
            last = i
    out, i = [], 0
    while i < len(units):
        if i in take:
            out.append(units[i] + units[i + 1])
            i += 2
        else:
            out.append(units[i])
            i += 1
    return out


def _positions(units: Sequence[str], a: str, b: str) -> List[int]:
    return [i for i in range(len(units) - 1) if units[i] == a and units[i + 1] == b]


def train_bpe(freq: Dict[str, int], merges: int) -> List[Pair]:
    """Plain BPE: merge the most frequent pair, ties to the smallest pair."""
    seg = {w: list(w) for w in freq}
    out: List[Pair] = []
    for _ in range(merges):
        counts: Dict[Pair, int] = {}
        for w, u in seg.items():
            for pair in set(zip(u, u[1:])):
                k = len(u) - len(_merge_at(u, _positions(u, *pair)))  # non-overlapping count
                counts[pair] = counts.get(pair, 0) + freq[w] * k
        if not counts:
            break
        a, b = min(counts, key=lambda pr: (-counts[pr], pr))
        seg = {w: _merge_at(u, _positions(u, a, b)) for w, u in seg.items()}
        out.append((a, b))
    return out


def _occurrences(units: Sequence[str], rank: Dict[Pair, int]) -> List[int]:
    return [i for i in range(len(units) - 1) if (units[i], units[i + 1]) in rank]


def _step(units: Sequence[str], kept: Sequence[int], rank: Dict[Pair, int]) -> List[str]:
    best = min(((units[i], units[i + 1]) for i in kept), key=rank.__getitem__)
    return _merge_at(units, [i for i in kept if (units[i], units[i + 1]) == best])


def segment(word: str, merges: Sequence[Pair], p: float, rng: random.Random) -> Seg:
    """Draw one BPE-dropout segmentation of word (Algorithm 1 of the paper)."""
    rank = {pair: r for r, pair in enumerate(merges)}
    u = list(word)  # @line L1
    while True:  # @line L2
        occ = _occurrences(u, rank)  # @line L3
        kept = [i for i in occ if rng.random() >= p]  # @line L4
        if not kept:  # @line L5
            return tuple(u)
        a, b = min(((u[i], u[i + 1]) for i in kept), key=rank.__getitem__)  # @line L6
        u = _merge_at(u, [i for i in kept if (u[i], u[i + 1]) == (a, b)])  # @line L7


def bpe(word: str, merges: Sequence[Pair]) -> Seg:
    """Plain BPE segmentation: merge the pair of highest priority until none is left."""
    rank = {pair: r for r, pair in enumerate(merges)}
    u = list(word)
    while True:
        occ = _occurrences(u, rank)
        if not occ:
            return tuple(u)
        u = _step(u, occ, rank)


def distribution(word: str, merges: Sequence[Pair], p: Fraction) -> Dict[Seg, Fraction]:
    """The exact law of segment(word, merges, p), by enumerating the drops."""
    rank = {pair: r for r, pair in enumerate(merges)}
    memo: Dict[Seg, Dict[Seg, Fraction]] = {}

    def law(u: Seg) -> Dict[Seg, Fraction]:
        if u in memo:
            return memo[u]
        occ = _occurrences(u, rank)
        out: Dict[Seg, Fraction] = {}
        for mask in range(1 << len(occ)):
            kept = [occ[j] for j in range(len(occ)) if mask >> j & 1]
            weight = (1 - p) ** len(kept) * p ** (len(occ) - len(kept))
            if weight == 0:
                continue
            if not kept:
                out[u] = out.get(u, Fraction(0)) + weight
                continue
            for seg, q in law(tuple(_step(u, kept, rank))).items():
                out[seg] = out.get(seg, Fraction(0)) + weight * q
        memo[u] = out
        return out

    return law(tuple(word))
