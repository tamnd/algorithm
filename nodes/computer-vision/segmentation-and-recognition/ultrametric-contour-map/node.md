---
tag: 6B2NMJ
kind: algorithm
slug: ultrametric-contour-map
name: Contour detection and hierarchical segmentation
aliases:
- gPb-OWT-UCM
- ultrametric contour map
area: computer-vision/segmentation-and-recognition
level: advanced
summary: A boundary map whose thresholds give a nested hierarchy of segmentations. Build it from regions and edge strengths by merging the pair with the weakest mean boundary first.
solves: [image-segmentation]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, R: the number of initial regions}
  time: {worst: O(W H + R^2 log R), average: O(W H + R^2 log R), best: O(W H + R log R)}
  space: {extra: O(W H + R^2)}
properties: {deterministic: true, greedy: true, hierarchical: true, closed_contours: true}
history:
  year: 2006
  people: [Pablo Arbelaez, Michael Maire, Charless Fowlkes, Jitendra Malik]
  note: Arbelaez defined the ultrametric contour map in 2006. Arbelaez, Maire, Fowlkes and Malik built it on gPb contours and an oriented watershed in 2011.
prereqs: [image-segmentation, ultrametric, edge-detection]
see_also: [watershed-segmentation, agglomerative-clustering, single-linkage-clustering, dendrogram, minimum-spanning-tree, boundary-f-measure, felzenszwalb-segmentation, normalized-cut]
sources:
  - paper: doi:10.1109/CVPRW.2006.48
    title: Pablo Arbelaez, Boundary extraction in natural images using ultrametric contour maps, CVPR Workshop on Perceptual Organization in Computer Vision, 2006
    locator: Definition of the ultrametric contour map and its construction by region merging
  - paper: doi:10.1109/TPAMI.2010.161
    title: Pablo Arbelaez, Michael Maire, Charless Fowlkes and Jitendra Malik, Contour detection and hierarchical image segmentation, IEEE TPAMI 33(5), 898-916, 2011
    locator: "Section 4.1 (oriented watershed transform), Section 4.2 (ultrametric contour map, equations 15 and 16)"
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 7.5, Segmentation
---

An ultrametric contour map (UCM) is a boundary map of an image with one property: if you keep only the boundaries stronger than a threshold $t$, the boundaries close into regions, and the regions for a larger $t$ are unions of the regions for a smaller $t$. So one map stores a whole hierarchy of [segmentations](/image-segmentation/), from fine to coarse. Arbelaez defined the UCM in 2006. The name of this page is the title of the 2011 paper of Arbelaez, Maire, Fowlkes and Malik, whose pipeline (often called gPb-OWT-UCM) is the best known way to build one: a contour detector gives the strengths, an oriented watershed gives the first regions, and greedy merging gives the UCM. This page is about the last step and the map that it makes. A [watershed](/watershed-segmentation/) gives one partition, not a hierarchy. Plain [agglomerative clustering](/agglomerative-clustering/) of pixels makes a [dendrogram](/dendrogram/) too, but its distances do not come from the strength of the shared boundary.

## In plain words

Draw the borders of many small regions on a map, in pencil of many shades. A light line is a weak border and a dark line is a strong border. Now look for the lightest border between two neighbor regions and rub it out, so that the two regions become one. The new region has new borders with its neighbors, and each of those gets the average shade of its pieces. Do this again and again, until one region is left.

Write down, on each border piece, the moment when it was rubbed out. That number is the map. If you hide every piece with a number below some value, you see exactly the regions that existed at that moment. A low value shows many small regions. A high value shows a few large ones. Every border you see is closed, because it was the edge of a real region.

## The problem

The input is a grid of $W \times H$ pixels with an initial label map, and a strength $E(e) \ge 0$ on each grid edge $e$ between two 4-neighbor pixels. A pixel is $(u, v)$, where $u$ is the column and $v$ is the row. The boundaries of this page lie on the grid edges between pixels, so a region boundary has no width.

The output is a value $\mathrm{UCM}(e)$ on each grid edge with these properties:
- For each threshold $t$, the connected components of the pixels, with the grid edges of value at most $t$ as links, form a partition $\mathcal{P}(t)$.
- If $t \le t'$, each region of $\mathcal{P}(t)$ lies inside one region of $\mathcal{P}(t')$.
- The edges inside one initial region have value 0, so $\mathcal{P}(0)$ is the initial partition or a coarser one.

The distance $d(p, q)$, the least $t$ at which $p$ and $q$ share a region, is then an ultrametric: $d(p, r) \le \max(d(p, q), d(q, r))$. This is where the name comes from. See [ultrametric](/ultrametric/) for the general notion.

## The algorithm

Arbelaez et al. (2011, Section 4.2) build the UCM by greedy merging on a graph whose nodes are the regions and whose edges are the common boundaries. The weight of an edge is the dissimilarity of the two regions, which they take as the average strength of their common boundary. The procedure below is that greedy merge on the grid edges. $S[a, b]$ is the sum of the strengths of the grid edges between regions $a$ and $b$, and $n[a, b]$ is their number.

```pseudo id=main
UCM(lab, E)                 ▷ lab: initial labels; E: strength of each grid edge
L1  give each 4-connected component of lab its own region id; R ← their number
L2  for each grid edge e = (p, q) whose pixels are in two regions a ≠ b do
L3      S[a, b] ← S[a, b] + E(e); n[a, b] ← n[a, b] + 1
L4  Q ← min-heap of (S[a, b] / n[a, b], a, b) over the adjacent pairs with a < b
L5  while Q is not empty do
L6      pop (m, a, b) from Q; if a or b is no longer live then go to L5
L7      make the new region c = a ∪ b at level m; a and b are no longer live
L8      UCM(e) ← m for each grid edge e between a and b
L9      for each live region r next to a or b do
L10         S[c, r] ← S[a, r] + S[b, r]; n[c, r] ← n[a, r] + n[b, r]; push (S[c, r] / n[c, r], r, c)
L11 UCM(e) ← 0 for each grid edge e inside one region of L1
L12 return UCM
```

Each region id is used once, so a heap entry is out of date exactly when one of its regions has merged, and line L6 drops it. Ties go to the smallest pair $(a, b)$; the new region gets the next free id.

## Example

The grid is $4 \times 4$ with four initial regions of $2 \times 2$ pixels, $A$ and $B$ on top and $C$ and $D$ below. Each boundary has two grid edges. The strengths are 0.2 and 0.4 between $A$ and $B$, 0.6 and 0.6 between $C$ and $D$, 0.9 and 0.7 between $A$ and $C$, and 0.5 and 0.9 between $B$ and $D$.

```text
A A | B B
A A | B B
---------
C C | D D
C C | D D
```

| step | mean strengths of the live pairs | merge | level |
|---|---|---|---|
| 1 | AB 0.3, CD 0.6, BD 0.7, AC 0.8 | $A \cup B = E$ | 0.3 |
| 2 | CD 0.6, ED 0.7, EC 0.8 | $C \cup D = F$ | 0.6 |
| 3 | EF $= (0.9 + 0.7 + 0.5 + 0.9) / 4 = 0.75$ | $E \cup F$ | 0.75 |

The UCM is 0.3 on the two edges between $A$ and $B$, 0.6 on the two edges between $C$ and $D$, and 0.75 on the four horizontal edges in the middle. A threshold below 0.3 gives 4 regions, a threshold in $[0.3, 0.6)$ gives 3, one in $[0.6, 0.75)$ gives 2, and one of 0.75 or more gives 1. The middle edges had strengths 0.9, 0.7, 0.5 and 0.9, but they all get 0.75: the UCM value of an edge is the level of a merge, not its input strength. The test file checks these numbers with exact fractions.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The main steps:
- The records always hold the true sums $S$ and $n$ of the current regions, because a grid edge between $c = a \cup b$ and $r$ lies between $a$ and $r$ or between $b$ and $r$, and not both.
- Each accepted pop is the least mean over the live pairs. After a merge at level $m$, the mean of a new pair $(c, r)$ is a weighted mean of the old means of $(a, r)$ and $(b, r)$, which are at least $m$. So the merge levels never go down.
- Because the levels never go down, the merges at level at most $t$ are a prefix of the merge sequence. By induction on that prefix, the components of the edges with value at most $t$ are exactly the regions after those merges (Theorem 1 of the proof). So every threshold gives closed contours and the partitions are nested.
- Nesting gives the ultrametric inequality, and $d(p, q)$ is the minimax value over paths from $p$ to $q$ of the largest UCM value on the path.

With the mean as the dissimilarity, monotone levels need the argument above. Arbelaez et al. make the same point for their dissimilarity (Section 4.2). A rule that can lower the dissimilarity after a merge would break the hierarchy.

## Complexity

Let $R$ be the number of initial regions. Lines L1 to L4 take $O(WH)$ time. The region adjacency graph is planar, so it has at most $3R - 6$ edges when $R \ge 3$, before and after each merge. A merge of $a$ and $b$ costs $O((\deg a + \deg b) \log R)$ for the records and the heap. A degree can be as large as $R - 1$, so the merges cost $O(R^2 \log R)$ in the worst case, and $O(R \log R)$ when every degree stays bounded by a constant. Line L10 adds the shorter list of grid edge pairs to the longer one, so the lists cost $O(R \log R)$ in total. The total is $O(WH + R^2 \log R)$ time and $O(WH + R^2)$ extra space, in the [real-RAM](/real-ram/) model. In practice the initial regions come from a watershed and $R$ is much smaller than $WH$.

The pipeline of Arbelaez et al. spends far more time on the contour detector (gPb) than on the merging. Its spectral part solves a generalized eigenproblem on a pixel affinity graph. That cost is outside this page.

## Properties

- **Hierarchy.** One map stores $R$ nested partitions, one for each merge level, and the threshold picks one.
- **Closed contours.** Every threshold gives boundaries that are unions of closed region boundaries. A raw edge map, such as the output of the [Canny detector](/canny-edge-detector/), has no such property.
- **Ultrametric.** The distance $d(p, q)$ satisfies the ultrametric inequality, and it equals the minimax path value of the UCM.
- **Greedy.** The merge order is fixed by the means. No step is undone, so an error in the initial regions or an early wrong merge stays in the hierarchy.
- **Deterministic.** With a fixed tie rule the output depends only on the input.

## Variants and improvements

- **The gPb-OWT-UCM pipeline** (Arbelaez et al. 2011). The strengths come from gPb, which combines local brightness, color and texture gradients at several scales with a spectral signal from the eigenvectors of a pixel affinity matrix, in the style of [normalized cuts](/normalized-cut/). The oriented watershed transform (OWT, Section 4.1) runs a watershed on the contour signal and then gives each watershed arc the strength of the contour at the orientation of that arc, which removes artifacts of the plain watershed. The UCM step is the greedy merge above.
- **Other dissimilarities.** If the dissimilarity is the minimum strength on the common boundary, the merge is [single-linkage clustering](/single-linkage-clustering/) on the region graph, and the hierarchy is the one of a [minimum spanning tree](/minimum-spanning-tree/). Mean and minimum both give monotone levels, because a merge cannot lower them. Single linkage is known to chain regions through one weak spot of a boundary; the mean is less sensitive to one weak edge.
- **Region features.** Other merge criteria use region statistics, such as color histograms. Such a criterion can give a lower dissimilarity after a merge. Then the levels must be forced to be monotone, for example by taking the running maximum, or the map is not an ultrametric.
- **Graph-based segmentation.** [Felzenszwalb-Huttenlocher segmentation](/felzenszwalb-segmentation/) also merges regions greedily along a minimum spanning tree order, but it returns one partition for one parameter value.

## When to use it

Use a UCM when a later step needs regions at several scales, for example when an object detector or a user picks the scale per object, or when you must report a segmentation benchmark over all thresholds. Use it when closed region boundaries matter, because a thresholded edge map can have gaps. Do not use it when you need one partition from a learned semantic model; the hierarchy carries no class labels. Do not use it when the initial regions already merge two objects, because merging cannot split them.

## Pitfalls

- **The UCM is not the input.** A UCM value is a merge level. An edge with a high input strength can get a low value if it sits between two regions whose mean boundary is weak, and the reverse.
- **Monotone levels are not free.** If you change the merge criterion, check that a merge can never lower the dissimilarity of a remaining pair. If it can, the thresholds stop giving nested partitions.
- **Ties and rounding.** Two pairs with the same mean can merge in either order, and floating point sums in a different order can change which mean is smaller. Fix a tie rule, and test with exact fractions.
- **Where the boundary lies.** This page puts boundaries on the grid edges between pixels. Many codes put them on pixels, which makes boundaries one pixel thick and needs care at junctions. The code of Arbelaez et al. stores the map on a grid of doubled resolution for this reason.
- **Threshold direction.** A region boundary at threshold $t$ is the set of edges with value strictly above $t$. Off-by-one errors in this test merge or split regions at exactly the merge levels.
- **Connectivity.** The initial regions must be connected. A label that appears in two separate places must give two regions, as line L1 does; otherwise a "region" can be adjacent to itself.

## Implementations

The Python code in `impl/python/ultrametric_contour_map.py` implements lines L1 to L12 on a given label map and given edge strengths. It does not compute gPb or the oriented watershed. Strengths can be int, float or Fraction. The tests compare the merge sequence with a naive method that recomputes all means before each merge, check that the levels never go down, check Theorem 1 at every level, and check the ultrametric inequality and the minimax path form by Floyd-Warshall on small grids.

## History

Arbelaez (2006) defined the ultrametric contour map as a boundary representation of a hierarchy of regions, and built it by merging regions of an initial partition. Arbelaez, Maire, Fowlkes and Malik (2011) combined it with the gPb contour detector and the oriented watershed transform, and evaluated the result on the Berkeley segmentation data sets with the [boundary F-measure](/boundary-f-measure/) and region measures. The link between ultrametrics and hierarchical clustering is older and comes from numerical taxonomy.

## References
