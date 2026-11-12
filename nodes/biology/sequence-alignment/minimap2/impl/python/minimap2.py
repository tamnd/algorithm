# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimap2/. The authors are listed in prov/5DG5E4.jsonl.

"""A small model of the minimap2 seeding and chaining steps.

1. Sketch: the (w,k)-minimizers of a sequence, with an invertible integer
   hash of the 2-bit code of the canonical k-mer (the smaller of the k-mer
   and its reverse complement), so that both strands pick the same positions.
2. Index: a dict from minimizer hash to the reference positions.
3. Anchors: for each query minimizer, each reference hit with the same hash.
4. Chaining: the minimap2 recurrence with at most h predecessors, with an
   integer gap cost, and backtracking to the best chain.

The base-level alignment of the gaps between anchors is not done here.
"""

from collections import defaultdict

VALUE = {"A": 0, "C": 1, "G": 2, "T": 3}
MASK64 = (1 << 64) - 1


def hash64(key: int, mask: int) -> int:
    """Thomas Wang's invertible integer hash, restricted to `mask`."""
    key = (~key + (key << 21)) & mask
    key ^= key >> 24
    key = (key + (key << 3) + (key << 8)) & mask
    key ^= key >> 14
    key = (key + (key << 2) + (key << 4)) & mask
    key ^= key >> 28
    key = (key + (key << 31)) & mask
    return key


def kmer_hashes(seq: str, k: int) -> list[tuple[int, int, int]]:
    """(hash, end position, strand) of each canonical k-mer of seq.

    strand is 0 if the forward k-mer is the smaller code, 1 if its reverse
    complement is. K-mers that equal their reverse complement are skipped,
    as in minimap, and so are k-mers with a letter outside ACGT.
    """
    mask = (1 << (2 * k)) - 1
    fwd = rev = 0
    valid = 0
    out = []
    shift = 2 * (k - 1)
    for i, ch in enumerate(seq):
        v = VALUE.get(ch)
        if v is None:
            valid = fwd = rev = 0
            continue
        fwd = ((fwd << 2) | v) & mask
        rev = (rev >> 2) | ((3 - v) << shift)
        valid += 1
        if valid >= k and fwd != rev:
            strand = 0 if fwd < rev else 1
            out.append((hash64(min(fwd, rev), mask), i, strand))
    return out


def sketch(seq: str, w: int, k: int) -> list[tuple[int, int, int]]:
    """The minimizers (hash, end position, strand), leftmost on ties.

    A window is w consecutive entries of kmer_hashes (skipped k-mers do not
    count). Each distinct selected entry is reported once, by position.
    """
    hs = kmer_hashes(seq, k)
    chosen = []
    last = -1
    window = []  # monotone deque of indices into hs, as a list with a head
    head = 0
    for i in range(len(hs)):
        while len(window) > head and hs[window[-1]][0] > hs[i][0]:
            window.pop()
        window.append(i)
        if window[head] <= i - w:
            head += 1
        if i >= w - 1:
            j = window[head]
            if j != last:
                chosen.append(hs[j])
                last = j
    return chosen


def naive_sketch(seq: str, w: int, k: int) -> list[tuple[int, int, int]]:
    hs = kmer_hashes(seq, k)
    picked = set()
    for i in range(len(hs) - w + 1):
        picked.add(min(range(i, i + w), key=lambda p: (hs[p][0], p)))
    return [hs[p] for p in sorted(picked)]


class Index:
    def __init__(self, ref: str, w: int, k: int) -> None:
        self.ref, self.w, self.k = ref, w, k
        self.table: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for h, pos, strand in sketch(ref, w, k):
            self.table[h].append((pos, strand))


def anchors(index: Index, query: str) -> dict[int, list[tuple[int, int, int]]]:
    """Anchors (x, y, w) per relative strand (0 same, 1 opposite), sorted by x.

    x is the reference end position. For strand 1, y is the end position on
    the reverse complement of the query.
    """
    k, n = index.k, len(query)
    out: dict[int, list[tuple[int, int, int]]] = {0: [], 1: []}
    for h, qpos, qs in sketch(query, index.w, k):  # @line L1
        for rpos, rs in index.table.get(h, ()):  # @line L2
            if qs == rs:
                out[0].append((rpos, qpos, k))
            else:
                out[1].append((rpos, n - 1 - (qpos - k + 1), k))
    for s in out:
        out[s].sort()  # @line L3
    return out


def gap_cost(l: int, k: int) -> int:
    """Integer form of 0.01 * k * |l| + 0.5 * log2 |l|."""
    if l == 0:
        return 0
    a = abs(l)
    return (k * a) // 100 + (a.bit_length() - 1) // 2


def pair_score(aj: tuple[int, int, int], ai: tuple[int, int, int], max_gap: int) -> int | None:
    """alpha(j, i) - beta(j, i), or None when beta is infinite."""
    xj, yj, _ = aj
    xi, yi, wi = ai
    if yj >= yi or max(yi - yj, xi - xj) > max_gap:
        return None
    alpha = min(yi - yj, xi - xj, wi)
    return alpha - gap_cost((yi - yj) - (xi - xj), wi)


def chain_scores(a: list[tuple[int, int, int]], h: int, max_gap: int) -> tuple[list[int], list[int]]:
    """f(i) and the predecessor P(i) of the minimap2 recurrence.

    Predecessors are tried from i - 1 backwards; the search stops after h
    tries in a row that do not improve f(i). h = len(a) gives the exact DP.
    """
    n = len(a)
    f = [0] * n
    pred = [-1] * n
    for i in range(n):  # @line L4
        best, bp = a[i][2], -1  # @line L5
        misses = 0
        for j in range(i - 1, -1, -1):  # @line L6
            if a[i][0] - a[j][0] > max_gap:  # sorted by x, so all earlier ones are too far
                break
            s = pair_score(a[j], a[i], max_gap)
            if s is not None and f[j] + s > best:  # @line L7
                best, bp = f[j] + s, j
                misses = 0
            else:
                misses += 1
                if misses >= h:  # @line L8
                    break
        f[i], pred[i] = best, bp  # @line L9
    return f, pred


def best_chain(a: list[tuple[int, int, int]], h: int = 50, max_gap: int = 5000) -> tuple[int, list[int]]:
    if not a:
        return 0, []
    f, pred = chain_scores(a, h, max_gap)
    i = max(range(len(a)), key=lambda t: (f[t], -t))  # @line L10
    out = []
    while i != -1:  # @line L11
        out.append(i)
        i = pred[i]
    out.reverse()
    return f[out[-1]], out


def brute_force_best(a: list[tuple[int, int, int]], max_gap: int) -> int:
    """Best chain score over all subsequences of a (in order), small inputs."""
    n = len(a)
    best = 0
    for mask in range(1, 1 << n):
        idx = [i for i in range(n) if mask >> i & 1]
        score = a[idx[0]][2]
        ok = True
        for j, i in zip(idx, idx[1:]):
            s = pair_score(a[j], a[i], max_gap)
            if s is None:
                ok = False
                break
            score += s
        if ok:
            best = max(best, score)
    return best


def map_read(index: Index, query: str, h: int = 50, max_gap: int = 5000) -> tuple[int, int, int] | None:
    """Return (strand, reference start, chain score) of the best chain.

    The start is the reference position where the query (or its reverse
    complement) would begin, from the first anchor of the chain.
    """
    best = None
    for strand, a in anchors(index, query).items():
        if not a:
            continue
        score, ch = best_chain(a, h, max_gap)  # @line L12
        x, y, _ = a[ch[0]]
        start = x - y
        if best is None or score > best[2]:
            best = (strand, start, score)
    return best  # @line L13


COMP = {"A": "T", "C": "G", "G": "C", "T": "A"}


def revcomp(s: str) -> str:
    return "".join(COMP.get(c, "N") for c in reversed(s))
