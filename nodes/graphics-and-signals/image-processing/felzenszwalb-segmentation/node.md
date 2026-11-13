---
tag: SE60TX
kind: algorithm
slug: felzenszwalb-segmentation
name: Felzenszwalb-Huttenlocher graph-based segmentation
aliases:
- graph-based image segmentation
- efficient graph-based image segmentation
- Felzenszwalb segmentation
area: graphics-and-signals/image-processing
level: advanced
summary: Scan the edges of a pixel graph by weight like Kruskal's algorithm and merge two components when the edge is no heavier than their internal difference plus k/size.
solves: [image-segmentation]
model: word-ram
complexity:
  vars: {m: the number of edges, n: the number of nodes}
  time: {worst: O(m log m), average: O(m log m), best: O(m log m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, greedy: true, not_too_fine: true, not_too_coarse: true, order_independent: true, parameters: k}
history:
  year: 2004
  people: [Pedro F. Felzenszwalb, Daniel P. Huttenlocher]
  note: Felzenszwalb and Huttenlocher defined the boundary predicate, gave the Kruskal-like algorithm and proved that its result is neither too fine nor too coarse, in the International Journal of Computer Vision in 2004.
prereqs: [kruskal, disjoint-set, image-segmentation]
see_also: [minimum-spanning-tree, single-linkage-clustering, maximum-spacing-k-clustering, image-segmentation-graph-cuts, normalized-cut, slic-superpixels, watershed-segmentation, gaussian-filter]
sources:
  - paper: doi:10.1023/B:VISI.0000022288.19776.77
    title: Pedro F. Felzenszwalb and Daniel P. Huttenlocher, Efficient graph-based image segmentation, International Journal of Computer Vision 59(2), 167 to 181, 2004
    locator: Section 3.1 (Int, Dif, MInt and the predicate D), Section 4 (Algorithm 1, Lemma 1, Theorems 1 to 3, running time), Section 5 (grid graphs, σ = 0.8, k = 150 and 300) and the Appendix (NP-hardness with quantiles)
  - paper: doi:10.1109/T-C.1971.223083
    title: Charles T. Zahn, Graph-theoretical methods for detecting and describing gestalt clusters, IEEE Transactions on Computers C-20(1), 68 to 86, 1971
    locator: clustering by cutting inconsistent edges of the minimum spanning tree
  - paper: doi:10.1090/S0002-9939-1956-0078686-7
    title: Joseph B. Kruskal, On the shortest spanning subtree of a graph and the traveling salesman problem, Proceedings of the American Mathematical Society 7(1), 48 to 50, 1956
    locator: the edge-by-edge construction of a minimum spanning tree in order of weight
  - book: isbn:9781848829343
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, Springer, 2011
    locator: Chapter 5, Segmentation, Section 5.2, Split and merge (graph-based segmentation)
---

The Felzenszwalb-Huttenlocher algorithm segments an image by building a graph on the pixels and merging components in the order of [Kruskal's algorithm](/kruskal/). Each pixel is a node, neighboring pixels are joined by an edge whose weight is their difference in intensity or color, and the edges are taken from lightest to heaviest. An edge between two components merges them when its weight is at most the internal difference of each component, the largest edge of its [minimum spanning tree](/minimum-spanning-tree/), plus a slack $k/|C|$ that is large for small components. So a region with much internal variation, like grass, accepts large differences, while a smooth region, like sky, is split at small ones. The algorithm is greedy, but the paper proves that its result is neither too fine nor too coarse for the boundary predicate it uses, and that it does not depend on the order of equal-weight edges. It runs in $O(m \log m)$ time for $m$ edges, nearly linear, and it is a common way to make an initial over-segmentation for an [image segmentation](/image-segmentation/) pipeline.

## In plain words

Think of the picture as a map of pixels, with a number on each pair of neighbors that says how different they look. Start with every pixel alone. Then walk through the pairs from the most similar to the least similar. For each pair that lies in two different groups, ask: is this difference small compared with the differences already inside each group? If yes, join the two groups. A group of noisy pixels has seen large differences inside, so it accepts large ones at its border too. A smooth group has seen only small differences, so a clear step stops it. Tiny groups get extra room to grow, and one number, k, sets how much. Larger k gives larger regions.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ nodes, $m$ edges and a weight $w(e) \ge 0$ on each edge, and a constant $k \ge 0$. For an image, $V$ is the set of pixels, $E$ joins 8-connected neighbors (any neighborhood works), and $w$ is the absolute intensity difference, often after a light [Gaussian smoothing](/gaussian-filter/). The output is a segmentation: a partition of $V$ into components, each connected in $G$.

For a component $C$, the internal difference is the largest weight in a minimum spanning tree of $C$ (using the edges of $E$ inside $C$):

$$\mathrm{Int}(C) = \max_{e \in \mathrm{MST}(C, E)} w(e), \qquad \mathrm{Int}(\{v\}) = 0.$$

For two components, the difference is the smallest weight of an edge between them, or $\infty$ if there is none:

$$\mathrm{Dif}(C_1, C_2) = \min_{v_i \in C_1,\, v_j \in C_2,\, (v_i, v_j) \in E} w(v_i, v_j).$$

With $\tau(C) = k/|C|$, the minimum internal difference is $\mathrm{MInt}(C_1, C_2) = \min\bigl(\mathrm{Int}(C_1) + \tau(C_1),\ \mathrm{Int}(C_2) + \tau(C_2)\bigr)$, and the predicate $D(C_1, C_2)$, "there is evidence for a boundary", is true when $\mathrm{Dif}(C_1, C_2) > \mathrm{MInt}(C_1, C_2)$.

A segmentation is too fine if some pair of its components has no evidence for a boundary, that is $D$ is false for them. It is too coarse if some proper refinement of it (split one or more components into connected parts) is not too fine. The goal is a segmentation that is neither. Such a segmentation always exists, but it need not be unique.

## The algorithm

```pseudo id=main
FH-SEGMENT(V, E, k)
L1  sort E by weight, non-decreasing
L2  for each v ∈ V do MAKE-SET(v);  Int(v) ← 0;  size(v) ← 1
L3  for each edge (u, v) of E in sorted order do
L4      a ← FIND(u);  b ← FIND(v)
L5      if a = b then continue
L6      if w(u, v) ≤ min(Int(a) + k/size(a), Int(b) + k/size(b)) then
L7          c ← UNION(a, b);  size(c) ← size(a) + size(b)
L8          Int(c) ← w(u, v)
L9  return the sets of the forest
```

The forest is a [disjoint-set](/disjoint-set/) structure with union by size or rank and path compression. Line L8 is the reason the method is fast: the edge that causes a merge is the lightest edge between the two components and is heavier than every edge already used, so it is the new largest edge of the minimum spanning tree. Int therefore costs one assignment per merge instead of a tree search. The merging edges are exactly the edges that Kruskal's algorithm would pick for the minimum spanning tree of each final component. The difference from Kruskal is only the test at line L6: Kruskal merges at every edge between two components, and this algorithm stops a component from growing once the next edge is too heavy for it.

The implementation keeps $k/|C|$ as an exact fraction, so integer weights give exact decisions. The authors' released code adds an optional pass after line L9 that joins any component smaller than a minimum size to a neighbor, in sorted edge order. That pass ignores the predicate and loses the guarantees below.

## Example

Take the $4 \times 2$ gray image with rows $(10, 11, 30, 31)$ and $(12, 10, 33, 30)$, 4-connectivity and $k = 10$. Name the pixels $a, b, c, d$ in the top row and $e, f, g, h$ below. The ten edges in sorted order, and what lines L4 to L8 do with them:

| edge | $w$ | sizes | Int | MInt | action |
|---|---|---|---|---|---|
| $a b$ | 1 | 1, 1 | 0, 0 | 10 | merge, Int = 1 |
| $b f$ | 1 | 2, 1 | 1, 0 | min(1 + 5, 0 + 10) = 6 | merge |
| $c d$ | 1 | 1, 1 | 0, 0 | 10 | merge |
| $d h$ | 1 | 2, 1 | 1, 0 | 6 | merge |
| $a e$ | 2 | 3, 1 | 1, 0 | min(1 + 10/3, 10) = 13/3 | merge, Int = 2 |
| $e f$ | 2 | | | | same set |
| $c g$ | 3 | 3, 1 | 1, 0 | 13/3 | merge, Int = 3 |
| $g h$ | 3 | | | | same set |
| $b c$ | 19 | 4, 4 | 2, 3 | min(2 + 5/2, 3 + 5/2) = 9/2 | reject |
| $f g$ | 23 | 4, 4 | 2, 3 | 9/2 | reject |

The result is two regions, the left half $\{a, b, e, f\}$ and the right half $\{c, d, g, h\}$, separated by the step of about 20 gray levels. The parameter sets the scale. With $k = 1$ the edges of weight 2 and 3 are rejected too: $a e$ meets $\mathrm{MInt} = \min(1 + 1/3, 0 + 1) = 1$, so $e$ and $g$ stay alone and there are four regions. The two halves merge only when $2 + k/4 \ge 19$, that is from $k = 68$ on.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It first shows Lemma 1 of the paper: when an edge between two different components is rejected, one of the two components is already final, because its threshold $\mathrm{Int} + \tau$ is below the rejected weight and all later edges are at least as heavy. From this, the edge that merges two components is the lightest edge between them, which gives line L8 and the link to Kruskal. Then it proves the three theorems. The result is not too fine: if two final components had no boundary evidence, the first edge between them would have been accepted. It is not too coarse: in any proper refinement, the lightest edge that the refinement cuts inside a component was accepted by the algorithm, so it shows no boundary evidence for the two parts it joins. And swapping two adjacent edges of equal weight never changes the result, so any non-decreasing order gives the same segmentation. The tests check the implementation against a direct evaluation of Int, Dif and the predicate on explicit sets, and check both theorems by trying all refinements of small graphs.

## Complexity

- Sorting at line L1 costs $O(m \log m)$. For small integer weights, such as 8-bit differences, a counting sort costs $O(m + W)$ for weights in $0..W$.
- Lines L3 to L8 do at most three disjoint-set operations and constant extra work per edge: $O(m\, \alpha(n))$, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/).
- Space is $\Theta(n)$ for the forest and $\Theta(m)$ for the sorted edge list.

On a grid with 4 or 8 neighbors, $m < 4n$, so the whole method costs $O(n \log n)$, or $O(n\, \alpha(n))$ with counting sort.

## Properties

- **Neither too fine nor too coarse.** The output satisfies both global conditions of the predicate $D$, although each decision is local and greedy.
- **Independent of the order of equal weights.** Any non-decreasing order of the edges gives the same partition.
- **Adaptive.** The threshold for a border grows with the variation inside the region. High-variation regions are kept whole and low-variation regions keep their detail, which a fixed threshold on edge weights, as in Zahn's method, cannot do.
- **k is a scale, not a size.** Larger $k$ favors larger regions, but small regions survive when their border is strong enough.
- **Regions are connected.** Every component is joined by its own merging edges, so it is connected in the graph.
- **Sensitive to single weak edges.** $\mathrm{Dif}$ is a minimum. One low-contrast pixel pair on a border, for example from blur or noise, can let two regions leak into each other.

## Variants and improvements

- **Other graphs.** The paper also uses a nearest-neighbor graph on feature points $(x, y, r, g, b)$ with Euclidean weights, which can join similar pixels that are far apart in the image.
- **Color.** The paper runs the algorithm once on each of the red, green and blue planes and keeps two neighboring pixels together only when all three runs do. A single run with a color distance as the weight is the simpler alternative, and the implementation here supports it.
- **Other threshold functions.** Any non-negative $\tau(C)$ keeps the guarantees, for example one that is large for long thin regions so that they get merged.
- **Quantiles.** Replacing the minimum in $\mathrm{Dif}$ by the median or another quantile would make it robust to single weak edges, but the paper proves that finding a segmentation that is neither too fine nor too coarse then becomes NP-hard.
- **Minimum region size.** The postprocessing pass described above removes tiny regions. Superpixel methods such as [SLIC](/slic-superpixels/) give more regular regions instead.

## When to use it

Use it to cut an image quickly into many regions that respect strong edges, as a first step for later merging, for object proposal methods, or as superpixels for a [graph cut](/image-segmentation-graph-cuts/) or a classifier. It has one parameter, runs in nearly linear time, and handles textured regions better than a plain threshold on edge weights. Do not use it when the regions must have regular shape and size; [SLIC](/slic-superpixels/) gives compact superpixels. Do not use it alone when weak or blurred borders matter, because one weak edge is enough to join two regions. For a global criterion that balances the size of the parts against the cut, use the [normalized cut](/normalized-cut/), which is much slower. If the test at line L6 is replaced by a fixed cut-off on the weight, the method becomes [single-linkage clustering](/single-linkage-clustering/), which is optimal for [maximum spacing](/maximum-spacing-k-clustering/) but either splits a textured region or joins two smooth ones.

## Pitfalls

- **Strict versus non-strict test.** Line L6 merges when the weight equals MInt. A strict test changes the results on images with integer values, where ties are common.
- **Reading k as a minimum size.** It is not. Use the postprocessing pass when a minimum size is required, and accept that it ignores the predicate.
- **Skipping the smoothing.** Without a light blur, quantization noise gives many one-pixel regions along edges. The paper always uses a Gaussian with $\sigma = 0.8$.
- **Thin border regions.** A one or two pixel band with values halfway between two regions often ends as its own region. This is common to all grid-graph methods.
- **Resolution dependence.** Since $\tau = k/|C|$ counts pixels, the same $k$ gives coarser results on a smaller image. The paper uses $k = 150$ for $128 \times 128$ images and $k = 300$ for $320 \times 240$ and larger.
- **Float ties.** With float weights from a color distance, nearly equal weights sort in arbitrary order. The result is order independent only for exactly equal weights, so rounding can still change it.

## Implementations

## History

Charles Zahn proposed in 1971 to cluster points and segment images by cutting the inconsistent edges of a minimum spanning tree, edges much heavier than the edges near them. Pedro Felzenszwalb and Daniel Huttenlocher gave an early form of their method at CVPR in 1998 and the full version in the International Journal of Computer Vision in 2004. They replaced Zahn's local rule with the predicate on internal and boundary differences, proved the not too fine and not too coarse properties and the order independence, and showed that the quantile version of the predicate is NP-hard. Their code was released with the paper, and the algorithm became a standard source of initial regions, for example in the selective search method for object proposals.

## References
