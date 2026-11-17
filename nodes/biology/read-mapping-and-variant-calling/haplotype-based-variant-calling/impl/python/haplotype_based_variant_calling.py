# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/haplotype-based-variant-calling/. The authors are listed in prov/REPJDG.jsonl.
"""A small haplotype-based variant caller for one diploid sample and one region.

The steps follow the local reassembly of callers such as GATK HaplotypeCaller:

1. build a de Bruijn graph of k-mers from the reads of the region and from
   the reference of the region;
2. drop the edges that fewer than min_count reads support, except the edges
   of the reference;
3. take every path from the first to the last k-mer of the reference as a
   candidate haplotype;
4. score every read against every haplotype with a pair HMM (the forward
   algorithm);
5. align each haplotype to the reference to find its variants, and give each
   variant the genotype likelihoods of 0, 1 or 2 copies, then a genotype.

Reads are given on the forward strand of the reference, as a mapper reports
them, with one Phred quality for each base.

What this code leaves out: the choice of active regions, the mapping of
reads, downsampling, the increase of k when the graph has a cycle, the
recovery of dangling ends, the gap penalties that depend on the context (the
PCR indel model), the reference confidence model, multi-allelic sites that
overlap, and the speedups of the pair HMM. A region whose reference has a
repeated k-mer raises ValueError.
"""

from __future__ import annotations

import itertools
import math
from typing import Dict, List, Sequence, Tuple

Variant = Tuple[int, str, str]  # (0-based position on the reference, reference allele, alternative allele)


def build_graph(ref: str, reads: Sequence[str], k: int) -> Tuple[Dict[Tuple[str, str], int], set]:
    """The edge counts of the de Bruijn graph of the reads, and the set of reference edges.

    A node is a k-mer and an edge joins two k-mers that overlap in k - 1 bases
    in a read (a (k + 1)-mer). The count of an edge is its number of occurrences in the reads.
    """
    ref_kmers = [ref[i:i + k] for i in range(len(ref) - k + 1)]
    if len(set(ref_kmers)) != len(ref_kmers):
        raise ValueError("the reference of the region has a repeated k-mer; use a larger k")
    ref_edges = {(ref[i:i + k], ref[i + 1:i + k + 1]) for i in range(len(ref) - k)}
    counts: Dict[Tuple[str, str], int] = {}
    for r in reads:
        for i in range(len(r) - k):
            e = (r[i:i + k], r[i + 1:i + k + 1])
            counts[e] = counts.get(e, 0) + 1
    return counts, ref_edges


def haplotypes(ref: str, reads: Sequence[str], k: int, min_count: int = 2,
               max_haplotypes: int = 64) -> List[str]:
    """The candidate haplotypes: the reference first, then the other paths in sorted order.

    A path may not visit a k-mer twice, so a cycle in the graph is not followed.
    """
    counts, ref_edges = build_graph(ref, reads, k)  # @line L1
    adj: Dict[str, List[str]] = {}
    for (u, v), c in counts.items():
        if c >= min_count and (u, v) not in ref_edges:  # @line L2
            adj.setdefault(u, []).append(v)
    for u, v in ref_edges:
        adj.setdefault(u, []).append(v)
    for u in adj:
        adj[u].sort()
    source, sink = ref[:k], ref[-k:]
    out: List[str] = []
    path = [source]
    on_path = {source}

    def dfs(u: str) -> None:  # @line L3
        if len(out) >= max_haplotypes:
            return
        if u == sink:
            out.append(path[0] + "".join(x[-1] for x in path[1:]))
            return
        for v in adj.get(u, []):
            if v not in on_path:
                path.append(v)
                on_path.add(v)
                dfs(v)
                on_path.discard(v)
                path.pop()

    dfs(source)
    rest = sorted(h for h in out if h != ref)
    return [ref] + rest


def pair_hmm(read: str, quals: Sequence[int], hap: str, gap_open: float = 1e-3,
             gap_ext: float = 0.1) -> float:
    """ln P(read | hap) by the forward algorithm of a pair HMM.

    The read starts in the match state at a position of hap chosen uniformly
    and must end in the match or the insertion state; the parts of hap before
    and after the read are free. A match emits 1 - e for the same base and
    e / 3 for another, with e = 10^(-q / 10). An inserted read base has
    probability 1/4. From the match state the chain opens an insertion or a
    deletion with probability gap_open each; a gap goes on with probability gap_ext.
    """
    n, L = len(hap), len(read)
    mm, gap_close = 1.0 - 2.0 * gap_open, 1.0 - gap_ext
    prev_m = [0.0] * (n + 1)
    prev_i = [0.0] * (n + 1)
    prev_d = [0.0] * (n + 1)
    for i in range(1, L + 1):  # @line P1
        b = read[i - 1]
        e = 10.0 ** (-quals[i - 1] / 10.0)
        same, other = 1.0 - e, e / 3.0
        cur_m = [0.0] * (n + 1)
        cur_i = [0.0] * (n + 1)
        cur_d = [0.0] * (n + 1)
        for j in range(1, n + 1):  # @line P2
            emit = same if hap[j - 1] == b else other
            if i == 1:
                cur_m[j] = emit / n
            else:
                cur_m[j] = emit * (mm * prev_m[j - 1] + gap_close * (prev_i[j - 1] + prev_d[j - 1]))  # @line P3
            cur_i[j] = 0.25 * (gap_open * prev_m[j] + gap_ext * prev_i[j])  # @line P4
            cur_d[j] = gap_open * cur_m[j - 1] + gap_ext * cur_d[j - 1]  # @line P5
        prev_m, prev_i, prev_d = cur_m, cur_i, cur_d
    total = sum(prev_m) + sum(prev_i)  # @line P6
    return math.log(total) if total > 0 else -math.inf


def affine_align(a: str, b: str, match: int = 2, mismatch: int = -3, gap_open: int = -6,
                 gap_ext: int = -1) -> List[str]:
    """The operations of a best global alignment of a with b under affine gaps (Gotoh).

    A gap of length g scores gap_open + (g - 1) gap_ext. "M" uses a base of
    both, "I" a base of a only and "D" a base of b only. Affine gaps keep a
    deletion of two bases in one piece, where linear gaps may cut it in two.
    """
    n, m = len(a), len(b)
    NEG = -10 ** 9
    M = [[NEG] * (m + 1) for _ in range(n + 1)]
    X = [[NEG] * (m + 1) for _ in range(n + 1)]
    Y = [[NEG] * (m + 1) for _ in range(n + 1)]
    M[0][0] = 0
    for i in range(1, n + 1):
        X[i][0] = gap_open + (i - 1) * gap_ext
    for j in range(1, m + 1):
        Y[0][j] = gap_open + (j - 1) * gap_ext
    for i in range(n + 1):
        for j in range(m + 1):
            if i and j:
                s = match if a[i - 1] == b[j - 1] else mismatch
                M[i][j] = s + max(M[i - 1][j - 1], X[i - 1][j - 1], Y[i - 1][j - 1])
            if i and j:
                X[i][j] = max(M[i - 1][j] + gap_open, X[i - 1][j] + gap_ext)
                Y[i][j] = max(M[i][j - 1] + gap_open, Y[i][j - 1] + gap_ext)
    tables = {"M": M, "I": X, "D": Y}
    state = max("MID", key=lambda t: tables[t][n][m])
    i, j, ops = n, m, []
    while i or j:
        ops.append(state)
        if state == "M":
            s = match if a[i - 1] == b[j - 1] else mismatch
            prev = M[i][j] - s
            i, j = i - 1, j - 1
            state = next(t for t in "MID" if tables[t][i][j] == prev)
        elif state == "I":
            state = "M" if X[i][j] == M[i - 1][j] + gap_open else "I"
            i -= 1
        else:
            state = "M" if Y[i][j] == M[i][j - 1] + gap_open else "D"
            j -= 1
    ops.reverse()
    return ops


def _left_shift(ref: str, v: Variant) -> Variant:
    """Move an indel to the left as far as the reference allows, as in VCF normalization."""
    pos, a, b = v
    while len(a) != len(b) and pos > 0 and a[-1] == b[-1]:
        pos -= 1
        a, b = ref[pos] + a[:-1], ref[pos] + b[:-1]
    return pos, a, b


def variants_of(hap: str, ref: str) -> List[Variant]:
    """The variants of hap against ref from an affine gap alignment, in VCF style.

    A substitution is (pos, ref base, alt base). An insertion or a deletion is
    written with the base before it, as in VCF, and shifted to the left. A gap
    at the very start of the region is not allowed, because it has no base before it.
    """
    ops = affine_align(hap, ref)
    out: List[Variant] = []
    i = j = 0  # i in hap, j in ref
    t = 0
    while t < len(ops):
        op = ops[t]
        if op == "M":
            if hap[i] != ref[j]:
                out.append((j, ref[j], hap[i]))
            i, j, t = i + 1, j + 1, t + 1
            continue
        run = 1
        while t + run < len(ops) and ops[t + run] == op:
            run += 1
        if j == 0 or i == 0:
            raise ValueError("a gap at the start of the region")
        if op == "I":
            out.append(_left_shift(ref, (j - 1, ref[j - 1], ref[j - 1] + hap[i:i + run])))
            i += run
        else:
            out.append(_left_shift(ref, (j - 1, ref[j - 1:j + run], ref[j - 1])))
            j += run
        t += run
    return out


def _mix(w: float, la: float, lb: float) -> float:
    """ln(w e^la + (1 - w) e^lb) without underflow."""
    terms = [math.log(w) + la if w > 0 else -math.inf, math.log(1.0 - w) + lb if w < 1 else -math.inf]
    top = max(terms)
    if top == -math.inf:
        return -math.inf
    return top + math.log(sum(math.exp(x - top) for x in terms))


def call(ref: str, reads: Sequence[str], quals: Sequence[Sequence[int]], k: int = 15,
         min_count: int = 2, theta: float = 1e-3) -> dict:
    """Run the caller. Returns a dict with the haplotypes, the best haplotype pair
    (as indices into the haplotypes), and the calls: for each variant, the genotype
    (0, 1 or 2 copies), the three log10 likelihoods and the three posteriors.
    """
    H = haplotypes(ref, reads, k, min_count)
    lik = [[pair_hmm(r, q, h) for h in H] for r, q in zip(reads, quals)]  # @line L4
    best_pair, best_ll = (0, 0), -math.inf
    for a, b in itertools.combinations_with_replacement(range(len(H)), 2):  # @line L5
        ll = sum(_mix(0.5, row[a], row[b]) for row in lik)
        if ll > best_ll + 1e-9:
            best_pair, best_ll = (a, b), ll
    carriers: Dict[Variant, set] = {}
    for h_index, h in enumerate(H[1:], start=1):  # @line L6
        for v in variants_of(h, ref):
            carriers.setdefault(v, set()).add(h_index)
    prior = [1.0 - 1.5 * theta, theta, theta / 2.0]
    calls = []
    for v in sorted(carriers):  # @line L7
        alt_set = carriers[v]
        gl = [0.0, 0.0, 0.0]
        for row in lik:
            l_alt = max(row[h] for h in alt_set)
            l_ref = max(row[h] for h in range(len(H)) if h not in alt_set)
            for g in range(3):  # @line L8
                gl[g] += _mix(g / 2.0, l_alt, l_ref)
        lp = [gl[g] + math.log(prior[g]) for g in range(3)]  # @line L9
        top = max(lp)
        z = top + math.log(sum(math.exp(x - top) for x in lp))
        post = [math.exp(x - z) for x in lp]
        g = max(range(3), key=lambda x: (lp[x], -x))
        calls.append({"variant": v, "genotype": g, "log10_gl": [x / math.log(10) for x in gl],
                      "posterior": post})
    return {"haplotypes": H, "best_pair": best_pair,
            "calls": [c for c in calls if c["genotype"] > 0]}  # @line L10
