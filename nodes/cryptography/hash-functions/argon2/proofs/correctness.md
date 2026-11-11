---
title: Argon2 is a well-defined function of all its inputs, and its memory hardness reduces to graph pebbling
proves: [correctness]
status: full
---

We use the notation of the page: $m' = 4p \lfloor m / 4p \rfloor$ blocks, $q = m' / p$ columns, segments of $q / 4$ columns, and $W$ the reference set of line L4.

**Lemma 1 (every reference is defined).** When line L5 computes $B[i][j]$ in pass $r$ and slice $s$, the reference $B[l][z]$ is a block that is already computed in this run, and is not $B[i][j]$ itself.

*Proof.* In pass 0, slice 0, the lane is forced to $l = i$ and $W$ is the blocks $B[i][0], \ldots, B[i][j-2]$ of the current segment; these are computed because the segment is filled in order. Since $j \ge 2$ there, $W$ is not empty. In pass 0, slice $s \ge 1$, $W$ is the columns $0, \ldots, s \cdot q/4 - 1$ of lane $l$, which were finished in the earlier slices, plus, when $l = i$, the computed blocks of the current segment except $B[i][j-1]$; the last element is dropped for $l \ne i$ at the first block of a segment. Every block of an earlier slice is finished before the current slice starts, because slices are processed in order for all lanes. In later passes, $W$ is the three segments of lane $l$ outside the current slice, plus the computed part of the current segment when $l = i$; every block of the matrix holds a value from the earlier pass or this one. Blocks of other lanes in the current slice are never in $W$, so the order in which the lanes of one slice are computed does not matter. $\square$

**Lemma 2 (the index map stays in range).** Let $w = |W| \ge 1$ and $J_1 < 2^{32}$. Then $x = \lfloor J_1^2 / 2^{32} \rfloor < 2^{32}$, $y = \lfloor w x / 2^{32} \rfloor \le w - 1$, and $z' = w - 1 - y$ lies in $[0, w - 1]$.

*Proof.* $J_1^2 < 2^{64}$ gives $x < 2^{32}$, so $w x < w \cdot 2^{32}$ and $y < w$, so $y \le w - 1$ and $z' \ge 0$; clearly $z' \le w - 1$. The index $z'$ counts from the start of $W$, which is position 0 in pass 0 and the column after the current slice in later passes, modulo $q$. $\square$

**Theorem 1 (well defined).** By Lemmas 1 and 2, every line of the algorithm reads only defined values, and the result is a deterministic function of $(P, S, K, X, T, m, t, p, y)$. The code follows the same order (pass, then slice, then lane, then column), so it computes the same function as RFC 9106; the tests confirm the pre-hash, intermediate blocks and tags of Section 5 for all three types. $\blacksquare$

**Theorem 2 (all inputs are bound).** If two input tuples differ, their tags are equal only if one of the following happens: a collision of $H^{64}$ in line L1, or a collision in the rest of the computation from different $H_0$.

*Proof.* The input of line L1 is an injective encoding: each variable-length field is preceded by its length, and the fixed fields have fixed widths. So different tuples give different inputs to $H^{64}$, and equal $H_0$ means a BLAKE2b collision. $\square$

**Memory hardness as pebbling.** Fix the reference indices of one run. They define a directed acyclic graph $D$ with a node per block computation and edges from the previous block and the reference block. Model $G$ as a random oracle. Then any algorithm that computes the tag must query $G$ on the inputs of every node, in an order consistent with $D$, because an output it has not queried is uniform and unknown. The blocks it keeps in memory at each step form a pebbling of $D$, and its cumulative memory complexity is at least the block size times the cumulative pebbling cost of $D$, up to the small probability of guessing an oracle output. This is the ex-post-facto argument of Alwen and Serbinenko (STOC 2015).

- For Argon2i, $D$ does not depend on the password, so lower bounds on the pebbling cost of the graph family give lower bounds on CMC. Blocki and Zhou (2017) bound this cost for one pass; Alwen and Blocki (2016) show that any such graph has cost $O(n^2 \log \log n / \log n)$, so the bound cannot reach $n^2$.
- For Argon2d, the graph depends on oracle outputs, so the analysis is the one for data-dependent functions such as scrypt. RFC 9106 reports the best known trade-off, which lowers the time-area product by 1.33; no proof matching that number is given.

These statements are about the idealized function in the parallel random oracle model. The concrete factors quoted on the page come from attacks, and the gap between attacks and proofs is not closed for Argon2i.
