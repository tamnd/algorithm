---
tag: WNYTAQ
kind: algorithm
slug: bender-farach-colton-rmq
name: Bender-Farach-Colton RMQ
aliases:
- O(1) RMQ via LCA
- Bender Farach-Colton algorithm
area: data-structures/range-query-structures
level: advanced
summary: Linear preprocessing and constant-time RMQ by reduction to LCA with block-based sparse tables.
solves: [range-minimum-query, lowest-common-ancestor]
model: word-ram
complexity:
  vars: {n: the length of the array; the time is per query, after O(n) preprocessing}
  time: {worst: O(1)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: true, recursive: false}
prereqs: [range-minimum-query, sparse-table, rmq-lca-equivalence, four-russians-method]
see_also: [cartesian-tree, euler-tour-technique, euler-tour-lca, fischer-heun-rmq, disjoint-sparse-table, sqrt-tree, monotonic-stack, word-ram]
sources:
  - paper: doi:10.1007/10719839_9
    title: "Michael A. Bender and Martin Farach-Colton, The LCA Problem Revisited, LATIN 2000: Theoretical Informatics, LNCS 1776, 88-94"
    locator: Section 2 (Lemma 3 and Observation 4, LCA to RMQ by an Euler tour), Section 3 (the sparse table, O(n log n) and O(1)), Section 4 (the ±1 RMQ with blocks of size (log n)/2, Observation 5 and Lemma 6 on normalized blocks) and Lemma 7 (RMQ to LCA by the Cartesian tree)
  - url: https://cp-algorithms.com/graph/lca_farachcoltonbender.html
    title: cp-algorithms, Lowest Common Ancestor - Farach-Colton and Bender Algorithm
    locator: the sections Algorithm (the Euler tour, blocks of size 0.5 log N, the sparse table over block minima and the bit masks of the blocks) and Implementation
  - paper: doi:10.1145/800057.808675
    title: "Harold N. Gabow, Jon Louis Bentley and Robert E. Tarjan, Scaling and related techniques for geometry problems, Proceedings of the 16th Annual ACM Symposium on Theory of Computing (STOC 1984), 135-143"
    locator: the Cartesian tree and the reduction of range minimum queries to lowest common ancestors
  - paper: doi:10.1137/0213024
    title: "Dov Harel and Robert E. Tarjan, Fast Algorithms for Finding Nearest Common Ancestors, SIAM Journal on Computing 13(2) (1984), 338-355"
    locator: the first algorithm with linear preprocessing and constant query time for lowest common ancestors
---

The Bender-Farach-Colton algorithm answers [range minimum queries](/range-minimum-query/) on a static array of $n$ items in $O(1)$ time after $O(n)$ preprocessing on the [word RAM](/word-ram/). It turns the array into its [Cartesian tree](/cartesian-tree/), so that the minimum of a range is a lowest common ancestor, and then turns the tree into the depth sequence of an [Euler tour](/euler-tour-technique/), so that the lowest common ancestor is again a range minimum, but on an array whose neighbours differ by exactly one. That *±1 array* is cut into blocks of size about $\frac12 \lg n$: a [sparse table](/sparse-table/) over the block minima has only $O(n)$ entries, and since a block is fixed by its pattern of $+1$ and $-1$ steps, there are only $O(\sqrt n)$ kinds of blocks, each with a small table of all its answers. The same structure gives [lowest common ancestors](/lowest-common-ancestor/) in $O(1)$ after $O(n)$ preprocessing, which was the aim of the 2000 paper.

## In plain words

A sparse table answers "where is the smallest item between positions $l$ and $r$?" in one step, but it stores about $n \lg n$ answers. The idea here is to store the table only for big pieces of the array, and to handle the small leftovers at the two ends with a trick.

The trick needs a special array, one in which each item is exactly one more or one less than the item before. Then a small piece is described completely by its first item and its list of ups and downs, and the place of the smallest item does not depend on the first item. Short pieces have only a few up-and-down patterns, so all answers for all patterns fit in a small table. Any array becomes such an array: build a tree from it and write down the depths of a walk around the tree.

## The problem

**Input.** A static array $A[0 \ldots n-1]$ over a totally ordered set.

**Queries.** $\textsc{rmq}(l, r)$ for $0 \le l \le r < n$: the position of the leftmost minimum of $A[l \ldots r]$.

**Goal.** $O(n)$ preprocessing time and space, and $O(1)$ time per query, on a word RAM with words of $\Theta(\log n)$ bits.

## The algorithm

**From the array to the ±1 array.** The Cartesian tree $C$ of $A$ has the position of the leftmost minimum as its root, the Cartesian tree of the part to its left as its left subtree, and that of the part to its right as its right subtree; a stack builds it in $O(n)$ time, as with a [monotonic stack](/monotonic-stack/). The minimum of $A[l \ldots r]$ is at the lowest common ancestor of the nodes $l$ and $r$ in $C$. A depth-first walk of $C$ that writes a node each time it is entered or returned to gives the tour $E[0 \ldots m-1]$ with $m = 2n - 1$, their depths $D[0 \ldots m-1]$, and the first index $F[v]$ of each node $v$ in $E$. The lowest common ancestor of $u$ and $v$ is the node of least depth in $E$ between $F[u]$ and $F[v]$, and adjacent depths differ by exactly one.

**The ±1 RMQ.** Cut $D$ into blocks of size $b = \max(1, \lfloor \frac12 \lg m \rfloor)$. Each block has a minimum position $M[j]$ and a *signature*, the $b - 1$ bits of its steps, 1 for $+1$ and 0 for $-1$. Two blocks with the same signature differ by a constant, so they have the same in-block answers.

```pseudo id=main
PREPROCESS(A)
L1  build the Cartesian tree C of A with a stack
L2  walk C depth first: tour E[0..m−1], depths D[0..m−1], first index F[v]
L3  b ← max(1, ⌊(lg m) / 2⌋), cut D into ⌈m / b⌉ blocks of size b
L4  for each block j: M[j] ← its leftmost minimum, sig[j] ← its steps as bits
L5  build a sparse table over the blocks, keyed by D[M[j]]
L6  for each signature that occurs: T[sig][i][k] ← the offset of the minimum of offsets i..k

QUERY(l, r)                                 ▷ 0 ≤ l ≤ r < n
L7  x ← F[l], y ← F[r]; if x > y then swap x and y
L8  bx ← ⌊x / b⌋, by ← ⌊y / b⌋
L9  if bx = by then k ← the in-block answer of block bx for x..y
L10 else k ← the least of: block bx from x to its end, the sparse table on blocks bx + 1..by − 1 (if any), block by from its start to y
L11 return E[k]
```

An in-block answer is one lookup $j b + T[\mathrm{sig}[j]][x - j b][y - j b]$. The sparse table query is the usual two overlapping powers of two, as the minimum is [idempotent](/idempotent-operation/).

## Example

Take $A = [4, 2, 5, 1, 6, 3]$. The Cartesian tree has the root 3 (value 1), whose left child is 1 (value 2) with the children 0 and 2, and whose right child is 5 (value 3) with the left child 4.

| index $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $E[k]$ | 3 | 1 | 0 | 1 | 2 | 1 | 3 | 5 | 4 | 5 | 3 |
| $D[k]$ | 0 | 1 | 2 | 1 | 2 | 1 | 0 | 1 | 2 | 1 | 0 |

So $F = [2, 1, 4, 0, 8, 7]$ for the positions $0, \ldots, 5$. To show the blocks on so small an input, take $b = 3$ instead of the formula. The blocks of $D$ are $[0, 1, 2]$, $[1, 2, 1]$, $[0, 1, 2]$ and $[1, 0]$, with the minimum positions $M = [0, 3, 6, 10]$ and the signatures $11$, $10$, $11$ and $0$. Blocks 0 and 2 share one table, so three tables are built for four blocks.

- $\textsc{rmq}(0, 2)$: $x = F[0] = 2$, $y = F[2] = 4$, in blocks 0 and 1. Block 0 from 2 to 2 gives index 2 (depth 2), block 1 from 3 to 4 gives index 3 (depth 1), and no block is in between. The least is index 3, and $E[3] = 1$: the minimum of $4, 2, 5$ is at position 1.
- $\textsc{rmq}(2, 5)$: $x = 4$, $y = 7$, in blocks 1 and 2. The candidates are index 5 (depth 1) and index 6 (depth 0), so $E[6] = 3$.
- $\textsc{rmq}(4, 5)$: $F[4] = 8 > F[5] = 7$, so $x = 7$, $y = 8$, both in block 2, and the table gives index 7, so $E[7] = 5$.
- $\textsc{rmq}(0, 5)$: $x = 2$, $y = 7$; block 1 lies in between and the sparse table gives $M[1] = 3$ (depth 1), so the candidates have depths 2, 1 and 0, and $E[6] = 3$.

## Correctness

There are three facts, proved in the [correctness proof](proofs/correctness.md). First, in the Cartesian tree with the leftmost minimum at each root, the lowest common ancestor of $l$ and $r$ is the leftmost minimum of $A[l \ldots r]$, because its subtree is a range of positions that contains $[l, r]$ and it is in $[l, r]$. Second, between the first visits of $u$ and $v$ the Euler tour stays in the subtree of their lowest common ancestor $w$ and visits $w$, so $w$ is the unique node of least depth there. Third, the query takes the minimum of $D$ over pieces that cover $[x, y]$: the in-block tables are right because $D$ restricted to a block is its first value plus a function of the signature, and the sparse table is right for the whole blocks in between.

## Complexity

**Preprocessing.** The Cartesian tree takes $O(n)$ time, since each position is pushed on and popped from the stack at most once; the tour takes $O(m) = O(n)$. The blocks and their signatures take $O(m)$. The sparse table has $\lceil m / b \rceil \lg \lceil m / b \rceil = O((m / \log m) \log m) = O(n)$ entries. There are at most $2^{b-1} \le 2^{\frac12 \lg m} = \sqrt m$ signatures, plus one for a short last block, and each table has $b^2$ entries filled in $O(b^2)$ time, so all tables take $O(\sqrt m \log^2 m) = o(n)$. In total, $O(n)$ time and words.

**Query.** Two table lookups for $F$, one division, at most two in-block lookups, one sparse table query with a bit length (one machine instruction or a table), and at most two comparisons: $O(1)$ time.

## Properties

- **Online after preprocessing.** Queries arrive one by one and need no batching.
- **Static.** Any change of $A$ forces a rebuild, since one item can change the shape of the whole Cartesian tree.
- **Space.** $\Theta(n)$ words, several times the size of the input; for $2n + o(n)$ bits see the [Fischer-Heun structure](/fischer-heun-rmq/).
- **Comparisons only in preprocessing.** Queries compare depths, which are small integers, not items of $A$.

## Variants and improvements

- **Skip the tour.** Fischer and Heun showed that the Cartesian tree is not needed explicitly: blocks of the original array are classified by the shape of their Cartesian tree, a number below $4^b$ computed with a stack, which gives the same $O(n)$ and $O(1)$ bounds with less space and is faster in practice.
- **The $O(n \log n)$ version.** Section 3 of the paper uses only the sparse table, which is simpler and often faster for $n$ up to a few million.
- **Blocks with in-block scans.** Practical codes use blocks of 32 or 64 items, a sparse table over them, and for queries inside a block a bit mask of a monotonic stack, which answers with a few bit operations.
- **LCA directly.** For a tree given as input, skip the Cartesian tree and use the Euler tour of the tree, which is the [Euler tour LCA](/euler-tour-lca/) with the ±1 RMQ in place of a sparse table.
- **Disjoint blocks for other operations.** For operations that are not idempotent, the [disjoint sparse table](/disjoint-sparse-table/) and the [sqrt tree](/sqrt-tree/) give constant or near-constant queries with more space.

## When to use it

Use it when the theory needs linear preprocessing and constant queries, as in suffix tree and suffix array algorithms that ask for many lowest common ancestors or longest common prefixes, or when $n$ is so large that the $n \lg n$ words of a sparse table do not fit. For most programs the plain sparse table, or blocks of 64 with a sparse table on top, is simpler and as fast. The method only applies to static arrays; with updates, use a [segment tree](/segment-tree/).

## Pitfalls

- **Ties.** The Cartesian tree must put the leftmost minimum at the root, which means popping the stack only while the top is *greater* than the new item. Popping on equality makes the answer the rightmost minimum, which breaks code that expects the leftmost.
- **The order of the first visits.** $F[l]$ can be larger than $F[r]$ for $l < r$, as in the example; swap them.
- **The size of the tour.** The ±1 array has $2n - 1$ items, so the block size and the table sizes depend on $m$, not on $n$.
- **Small inputs.** For $m < 4$ the formula gives $b = 1$, where every block is one item; the code must still work, with empty signatures.
- **Recursion.** A recursive depth-first walk of a Cartesian tree overflows the stack for sorted input, where the tree is a path of depth $n$; use an explicit stack.

## Implementations

## History

Harel and Tarjan (1984) gave the first lowest common ancestor algorithm with linear preprocessing and constant queries, and Gabow, Bentley and Tarjan (1984) linked range minima and lowest common ancestors through the Cartesian tree. Schieber and Vishkin (1988) simplified the method, and Berkman, Breslauer, Galil, Schieber and Vishkin gave a parallel algorithm. Bender and Farach-Colton (2000), in *The LCA Problem Revisited*, showed that the parallel algorithm, made sequential, becomes short and practical: the ±1 RMQ with blocks of half-logarithmic size and the table of normalized blocks, and they argued against the belief that optimal LCA algorithms cannot be implemented.

## References
