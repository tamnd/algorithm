# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mummer/. The authors are listed in prov/VB8A1D.jsonl.

"""A small model of MUMmer (Delcher et al., 1999).

1. Find the maximal unique matches (MUMs) of A and B with a suffix array of
   A # B $ and its LCP array (MUMmer 1 used a suffix tree).
2. Chain the MUMs: the heaviest set whose starts increase in both A and B,
   weighted by length (a weighted longest increasing subsequence).
3. Close the gaps between consecutive MUMs of the chain and classify them;
   gaps are aligned with unit-cost global alignment here.
"""

from bisect import bisect_left

Mum = tuple[int, int, int]  # (start in A, start in B, length)


def suffix_array(s: str) -> list[int]:
    return sorted(range(len(s)), key=lambda i: s[i:])


def lcp_array(s: str, sa: list[int]) -> list[int]:
    """lcp[r] = longest common prefix of the suffixes of rank r - 1 and r
    (Kasai et al., 2001); lcp[0] = 0."""
    n = len(s)
    rank = [0] * n
    for r, p in enumerate(sa):
        rank[p] = r
    lcp = [0] * n
    h = 0
    for p in range(n):
        if rank[p] > 0:
            q = sa[rank[p] - 1]
            while p + h < n and q + h < n and s[p + h] == s[q + h]:
                h += 1
            lcp[rank[p]] = h
            if h:
                h -= 1
        else:
            h = 0
    return lcp


def find_mums(a: str, b: str, min_len: int = 1) -> list[Mum]:
    s = a + "#" + b + "$"
    sa = suffix_array(s)  # @line L1
    lcp = lcp_array(s, sa)  # @line L2
    na = len(a)
    out = []
    for r in range(1, len(s)):  # @line L3: adjacent suffixes of rank r - 1 and r
        length = lcp[r]
        if length < min_len:
            continue
        p, q = sa[r - 1], sa[r]
        if (p < na) == (q < na):  # @line L4: one suffix from A and one from B
            continue
        left = lcp[r - 1] if r - 1 >= 0 else 0
        right = lcp[r + 1] if r + 1 < len(s) else 0
        if left >= length or right >= length:  # @line L5: a third suffix shares the prefix
            continue
        i, j = (p, q - na - 1) if p < na else (q, p - na - 1)
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:  # @line L6: not left-maximal
            continue
        out.append((i, j, length))  # @line L7
    return sorted(out)


def chain_mums(mums: list[Mum]) -> list[Mum]:
    """Heaviest chain with increasing starts in A and in B, weight = length.
    MUM starts are distinct in A and in B, so the order is strict."""
    order = sorted(mums)  # @line L8: by start in A
    bs = sorted(m[1] for m in mums)
    size = len(bs)
    tree = [(0, -1)] * (size + 1)  # Fenwick tree of prefix maxima over B ranks

    def query(i: int) -> tuple[int, int]:
        best = (0, -1)
        while i > 0:
            best = max(best, tree[i])
            i -= i & -i
        return best

    def update(i: int, val: tuple[int, int]) -> None:
        i += 1
        while i <= size:
            tree[i] = max(tree[i], val)
            i += i & -i

    f = [0] * len(order)
    prev = [-1] * len(order)
    for x, (i, j, length) in enumerate(order):  # @line L9
        rank = bisect_left(bs, j)
        best, arg = query(rank)  # @line L10: best chain ending at a smaller start in B
        f[x] = best + length  # @line L11
        prev[x] = arg
        update(rank, (f[x], x))  # @line L12
    if not order:
        return []
    x = max(range(len(order)), key=lambda y: f[y])  # @line L13
    chain = []
    while x != -1:
        chain.append(order[x])
        x = prev[x]
    return chain[::-1]


def edit_distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return prev[-1]


def classify(ga: int, gb: int) -> str:
    """MUMmer's classes of the gap between two consecutive MUMs."""
    if ga < 0 or gb < 0:
        return "repeat"  # the MUMs overlap in A or in B
    if ga == gb == 1:
        return "SNP"
    if ga == 0 or gb == 0:
        return "insertion"
    return "polymorphic"


def mummer(a: str, b: str, min_len: int = 3) -> tuple[list[Mum], list[tuple[str, int]], int]:
    """Return the chain, the gaps (class, cost) and the cost of the whole
    alignment that the chain induces (unit costs)."""
    chain = chain_mums(find_mums(a, b, min_len))
    gaps = []
    cost = 0
    ea = eb = 0  # end of the aligned part in A and in B
    for i, j, length in chain + [(len(a), len(b), 0)]:  # @line L14
        ga, gb = i - ea, j - eb
        if ga < 0 or gb < 0:  # @line L15: overlap; trim the start of this MUM
            cut = -min(ga, gb)
            if cut >= length and length > 0:
                gaps.append(("repeat", 0))  # nothing left of this MUM
                continue
            i, j, length = i + cut, j + cut, length - cut
        c = edit_distance(a[ea:i], b[eb:j])  # @line L16: align the gap
        if ga or gb:
            gaps.append((classify(ga, gb), c))
        cost += c
        ea, eb = i + length, j + length  # @line L17
    return chain, gaps, cost


# ---- naive versions for the tests ----

def naive_mems(a: str, b: str, min_len: int = 1) -> list[Mum]:
    out = []
    for i in range(len(a)):
        for j in range(len(b)):
            if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
                continue
            length = 0
            while i + length < len(a) and j + length < len(b) and a[i + length] == b[j + length]:
                length += 1
            if length >= min_len:
                out.append((i, j, length))
    return out


def count(text: str, w: str) -> int:
    return sum(text.startswith(w, p) for p in range(len(text) - len(w) + 1))


def naive_mums(a: str, b: str, min_len: int = 1) -> list[Mum]:
    return sorted((i, j, length) for i, j, length in naive_mems(a, b, min_len)
                  if count(a, a[i:i + length]) == 1 and count(b, a[i:i + length]) == 1)


def brute_force_chain(mums: list[Mum]) -> int:
    best = 0
    k = len(mums)
    order = sorted(mums)
    for mask in range(1 << k):
        pick = [order[x] for x in range(k) if mask >> x & 1]
        if all(pick[y][0] < pick[y + 1][0] and pick[y][1] < pick[y + 1][1] for y in range(len(pick) - 1)):
            best = max(best, sum(m[2] for m in pick))
    return best
