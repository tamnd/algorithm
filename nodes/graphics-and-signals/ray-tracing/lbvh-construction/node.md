---
tag: PTNB7Y
kind: algorithm
slug: lbvh-construction
name: Linear BVH construction
aliases: [LBVH, HLBVH]
area: graphics-and-signals/ray-tracing
level: advanced
summary: Build a BVH by sorting the primitives on the Morton codes of their centroids with a radix sort, deriving each internal node on its own from the sorted keys, and then forming the boxes bottom up.
model: real-ram
complexity:
  vars: {n: the number of primitives}
  time: {best: O(n), worst: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2009
  people: [Christian Lauterbach, Michael Garland, Shubhabrata Sengupta, David Luebke, Dinesh Manocha]
  note: Lauterbach et al. sorted the primitives along a Morton curve and read the tree off the bits of the codes, so that a GPU could build a BVH in a few milliseconds; Karras (2012) made every internal node independent.
prereqs: [bounding-volume-hierarchy, morton-encoding, radix-sort]
see_also: [bvh-construction, surface-area-heuristic, bvh-refitting, z-order-curve, parallel-radix-sort, leading-zero-count, bvh-traversal, simt-model]
sources:
  - paper: doi:10.1111/j.1467-8659.2009.01377.x
    title: Christian Lauterbach, Michael Garland, Shubhabrata Sengupta, David Luebke and Dinesh Manocha, Fast BVH construction on GPUs, Computer Graphics Forum 28(2), Eurographics 2009, 375 to 384
    locator: the LBVH (Morton codes of the centroids, the sort, the tree from the bits of the codes) and the hybrid with LBVH splits in the upper levels and SAH splits below
  - paper: doi:10.2312/EGGH/HPG12/033-037
    title: Tero Karras, Maximizing parallelism in the construction of BVHs, octrees, and k-d trees, High Performance Graphics 2012, 33 to 37
    locator: the binary radix tree, the numbering of internal nodes by one end of their range, the direction, range and split search of each node, distinct keys by appending the index, and the bottom-up boxes with atomic counters
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 4, Section 4.3.3 Linear Bounding Volume Hierarchies (Morton codes of the centroids, the radix sort, treelets, and the SAH over the treelets as in HLBVH)
---

Linear BVH construction (LBVH) builds a [bounding volume hierarchy](/bounding-volume-hierarchy/) without any search for a good split. It maps the centroid of each primitive to a cell of a $1024^3$ grid, takes the [Morton code](/morton-encoding/) of the cell, and sorts the primitives by code with a [radix sort](/radix-sort/). Nearby primitives are then mostly nearby in the sorted order, and the tree is the binary radix tree of the codes: each node splits where the highest differing bit of its range changes. Karras (2012) showed that each of the $n - 1$ internal nodes can be found on its own from the sorted keys with two binary searches, so the whole build is a few parallel passes. The boxes are then formed bottom up. The tree is worse for rays than an SAH tree, but on a GPU it is built in a few milliseconds for millions of primitives, so it suits scenes that change every frame.

## In plain words

Lay a fine grid over the scene and number its cells along a curve that goes back and forth in a fixed pattern, the Z-order curve. Cells with close numbers are mostly close in space. Give each triangle the number of the cell that holds its center, and sort the triangles by that number.

Now the sorted list tells you the tree. The first bit of the number says which half of the scene a triangle is in, so all triangles with first bit 0 go left and the rest go right. The next bit splits each half again, and so on. Each node of the tree can find its own range in the list by looking at where the bits change, without waiting for any other node. That is why the method is fast on many cores.

## The problem

The input is a nonempty set of $n$ primitives with boxes and centroids. The output is a binary tree in which each primitive is in exactly one leaf and each node stores the box of the primitives below it. Unlike in [BVH construction](/bvh-construction/) with the [SAH](/surface-area-heuristic/), no cost is minimized: the shape of the tree is fixed by the sorted Morton codes. The goal is a short build time with a high degree of parallelism.

## The algorithm

Let $\delta(i, j)$ be the length of the common prefix of the keys $k_i$ and $k_j$, found with one [leading zero count](/leading-zero-count/) of $k_i \oplus k_j$, and $\delta(i, j) = -1$ if $j$ is outside $[0, n - 1]$. Internal node $i$ has a range of leaves that starts or ends at $i$; the root is node 0.

```pseudo id=main
LBVH(P)
L1  C ← the box of the centroids; for each p: code[p] ← MORTON(the cell of its centroid in C, 10 bits per axis)
L2  key[p] ← code[p] · 2^b + p, with 2^b ≥ n                         ▷ distinct keys
L3  sort the primitives by key with a radix sort; leaf k is the k-th primitive
L4  for each internal node i = 0, …, n − 2, in parallel do
L5      d ← sign(δ(i, i + 1) − δ(i, i − 1))                           ▷ the direction of the range
L6      δmin ← δ(i, i − d); lmax ← 2; while δ(i, i + lmax · d) > δmin do lmax ← 2 · lmax
L7      l ← 0; for t ← lmax/2, lmax/4, …, 1 do if δ(i, i + (l + t) · d) > δmin then l ← l + t
L8      j ← i + l · d; δnode ← δ(i, j)                                ▷ the other end of the range
L9      s ← 0; for t ← ⌈l/2⌉, ⌈l/4⌉, …, 1 do if δ(i, i + (s + t) · d) > δnode then s ← s + t
L10     γ ← i + s · d + min(d, 0)                                       ▷ the split
L11     left(i) ← leaf γ if min(i, j) = γ, else node γ; right(i) ← leaf γ + 1 if max(i, j) = γ + 1, else node γ + 1
L12 from each leaf, in parallel, walk up the parent links; at each node the first walk stops, and the second sets its box to the union of the boxes of its two children and goes on
```

Line L2 makes the keys distinct, which lines L5 to L10 need; Karras appends the index in the same way. Line L5 looks at which neighbor shares the longer prefix: the range of node $i$ extends toward that one. Lines L6 and L7 are an exponential search and a binary search for the farthest $j$ whose common prefix with $k_i$ is longer than that with the other neighbor. Line L9 is a binary search for the position where the highest differing bit of the range changes. Line L12 is done on a GPU with one atomic counter per node.

## Example

Karras (2012) uses eight keys of 5 bits: $k_0, \ldots, k_7$ = 00001, 00010, 00100, 00101, 10011, 11000, 11001, 11110. The table gives each internal node; I$x$ is internal node $x$ and L$x$ is leaf $x$.

| $i$ | $\delta(i, i - 1)$ | $\delta(i, i + 1)$ | $d$ | $\delta_{min}$ | $j$ | $\delta_{node}$ | $\gamma$ | range | left | right |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | $-1$ | 3 | $+1$ | $-1$ | 7 | 0 | 3 | $[0, 7]$ | I3 | I4 |
| 1 | 3 | 2 | $-1$ | 2 | 0 | 3 | 0 | $[0, 1]$ | L0 | L1 |
| 2 | 2 | 4 | $+1$ | 2 | 3 | 4 | 2 | $[2, 3]$ | L2 | L3 |
| 3 | 4 | 0 | $-1$ | 0 | 0 | 2 | 1 | $[0, 3]$ | I1 | I2 |
| 4 | 0 | 1 | $+1$ | 0 | 7 | 1 | 4 | $[4, 7]$ | L4 | I5 |
| 5 | 1 | 4 | $+1$ | 1 | 7 | 2 | 6 | $[5, 7]$ | I6 | L7 |
| 6 | 4 | 2 | $-1$ | 2 | 5 | 4 | 5 | $[5, 6]$ | L5 | L6 |

Take node 3. Its neighbors share 4 bits on the left (00100 and 00101) and 0 bits on the right (00101 and 10011), so the range goes left and $\delta_{min} = 0$. The farthest key to the left that shares more than 0 bits with 00101 is $k_0 = 00001$, so $j = 0$ and $\delta_{node} = \delta(3, 0) = 2$. The split is where the third bit changes, between $k_1 = 00010$ and $k_2 = 00100$, so $\gamma = 1$. Its children are the nodes 1 and 2, whose ranges $[0, 1]$ and $[2, 3]$ end and start at 1 and 2. The tests check this table and compare the hierarchy on random keys with a top-down build that splits each range at its highest differing bit.

## Correctness

Claim: the arrays left and right form the binary radix tree of the sorted keys with root 0, each primitive is in exactly one leaf, and each box is the union of the boxes of the leaves below it.

By the sorted order, the common prefix of $k_a$ and $k_b$ is the least of the prefixes of the adjacent pairs between them. So in each range the highest differing bit changes exactly once, and the radix tree splits there. A range is a node of that tree exactly when all adjacent prefixes inside are longer than those at its two ends. The searches of lines L6 to L10 find, for node $i$, the longest such range that ends at $i$ and its split, and no two nodes find the same range, so the $n - 1$ nodes are the $n - 1$ internal ranges. The child of a range at a split $\gamma$ is found by node $\gamma$ or $\gamma + 1$, as line L11 says. The full proof is in [proofs/correctness.md](proofs/correctness.md). The leaves are the $n$ sorted keys, so the cover is exact, and the bottom-up pass of line L12 computes each box after both of its children.

## Complexity

The model is the [real RAM](/real-ram/), with bit operations and a leading zero count on keys of $30 + \lceil \log_2 n \rceil$ bits in $O(1)$, as on a [word RAM](/word-ram/). Lines L1 and L2 cost $O(n)$. A radix sort with digits of $\lceil \log_2 n \rceil$ bits needs a constant number of passes for keys of $30 + \lceil \log_2 n \rceil$ bits, so line L3 costs $O(n)$. Node $i$ in lines L5 to L10 costs $O(\log \ell_i)$, where $\ell_i$ is the length of its range. The sum is $O(n)$ when the tree is balanced, and $O(n \log n)$ in the worst case, a chain whose ranges have the lengths $n, n - 1, \ldots, 2$. Line L12 visits each node twice, $O(n)$. The extra space is $O(n)$.

On a parallel machine, each of the loops is one pass with $n$ threads: the depth of lines L4 to L11 is $O(\log n)$, and the depth of line L12 is the height of the tree. The [parallel radix sort](/parallel-radix-sort/) is built from [prefix sums](/all-prefix-sums/).

## Properties

- **No cost model.** The tree depends only on the sorted codes, so it can be poor: a split at the middle of a cell of the grid can cut a cluster of nearby primitives, and a large primitive is placed by its centroid only.
- **Height.** The height is at most the key length, $30 + \lceil \log_2 n \rceil$, since each level fixes at least one more bit. It is not $O(\log n)$ for clustered input.
- **Leaves of one primitive.** Each leaf holds one primitive. Collapsing small subtrees into leaves is a separate pass.
- **Deterministic.** The index in the key breaks ties between equal codes, so the tree does not depend on the order of the threads.
- **Exact cover.** Each primitive is in exactly one leaf, and the boxes are the tight unions.

## Variants and improvements

- **Lauterbach et al. (2009).** The first LBVH built the hierarchy top down, one bit level at a time, by finding the first index in each range whose bit is 1; their hybrid used LBVH splits for the upper levels and SAH splits for the lower levels.
- **HLBVH.** Pantaleoni and Luebke (2010) grouped the primitives by the top bits of their codes into clusters, built the levels inside each cluster from the lower bits, and built the top of the tree over the clusters with the SAH. PBRT builds treelets in this way.
- **Karras (2012).** The node numbering of this page, in which every internal node is independent. The same hierarchy gives octrees and k-d trees.
- **Merged hierarchy and boxes.** Later methods build the hierarchy and the boxes in one bottom-up pass, which saves the separate searches.
- **Treelet restructuring.** Karras and Aila (2013) improve an LBVH by optimizing small subtrees for the SAH in parallel, to get close to SAH quality at a small extra cost.
- **Longer codes.** 63-bit codes with 21 bits per axis reduce the number of equal codes in large or uneven scenes.

## When to use it

Use an LBVH on a GPU, or when the scene changes too much each frame for [refitting](/bvh-refitting/), and the build time counts as much as the trace time. For a scene that is traced with many rays per build, a [binned SAH build](/bvh-construction/) or an LBVH followed by a restructuring pass gives faster tracing. For a static scene built once, use the SAH, with [spatial splits](/spatial-splits/) for scenes with large triangles.

## Pitfalls

- **Equal Morton codes.** Two centroids in the same grid cell give equal codes. Without line L2, $\delta(i, i + 1) = \delta(i, i - 1)$ can happen, line L5 gets $d = 0$, and the searches fail. Append the index, or compare indices when the codes are equal.
- **Wrong rounding in line L9.** The steps must be $\lceil l/2 \rceil, \lceil l/4 \rceil, \ldots, 1$. With $\lfloor l/2 \rfloor$, an odd $l$ loses the last position, and the split can be one too far left.
- **Out-of-range $\delta$.** $\delta(i, j)$ for $j < 0$ or $j \ge n$ must be $-1$, less than every real prefix length. Without it, lines L6 and L7 read outside the array.
- **Quantizing with the box of the primitives.** Line L1 must use the box of the centroids. With the larger box of the primitives, the centroids use only part of the grid and more of them share a cell.
- **The upper end of the grid.** The centroid on the upper face of $C$ maps to cell 1024. Clamp it to 1023, or the code overflows into the bits of the next axis.
- **A data race in line L12.** On a GPU, the first walk to reach a node must stop, and the second must read the box of the other child only after the first wrote it. This needs an atomic counter and a memory fence.

## Implementations

## History

Morton (1966) introduced the interleaved bit order for a file of map cells. Lauterbach, Garland, Sengupta, Luebke and Manocha (2009) used it to build BVHs on GPUs: sort by Morton code, then read the tree from the bits. Pantaleoni and Luebke (2010) added the two-level HLBVH with the SAH at the top. Karras (2012) numbered the internal nodes by one end of their ranges, so that every node of the radix tree, and of the derived octree and k-d tree, can be built at once. Karras and Aila (2013) then showed how to improve such a tree in parallel toward SAH quality.

## References
