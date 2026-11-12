---
tag: TPVQDP
kind: algorithm
slug: bvh-construction
name: BVH construction
aliases: [top-down BVH build]
area: graphics-and-signals/ray-tracing
level: advanced
summary: Build a bounding volume hierarchy top down by splitting each set of primitives in two at the bin boundary of least surface area heuristic cost, until a leaf is cheaper than any split.
model: real-ram
complexity:
  vars: {n: the number of primitives, K: the number of bins (a constant)}
  time: {best: O(n log n), worst: O(n^2)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2007
  people: [Ingo Wald]
  note: Wald put the centroids into a fixed number of bins per axis and evaluated the SAH only at the bin boundaries, which made SAH builds fast enough for scenes that change every frame.
prereqs: [bounding-volume-hierarchy, surface-area-heuristic]
see_also: [lbvh-construction, spatial-splits, bvh-refitting, bvh-traversal, bounding-interval-hierarchy, kd-tree-traversal, quickselect, greedy-algorithm]
sources:
  - paper: doi:10.1109/RT.2007.4342588
    title: Ingo Wald, On fast construction of SAH-based bounding volume hierarchies, IEEE Symposium on Interactive Ray Tracing 2007, 33 to 40
    locator: the binned build, with the centroid bins, the two sweeps over the bins and the cost of one level
  - paper: doi:10.1109/MCG.1987.276983
    title: Jeffrey Goldsmith and John Salmon, Automatic creation of object hierarchies for ray tracing, IEEE Computer Graphics and Applications 7(5), 1987, 14 to 20
    locator: the surface area ratio as the chance that a ray that hits a parent volume hits a child volume
  - paper: doi:10.1007/BF01911006
    title: J. David MacDonald and Kellogg S. Booth, Heuristics for ray tracing using space subdivision, The Visual Computer 6(3), 1990, 153 to 166
    locator: the surface area cost of a split and the greedy top-down choice of the split plane
  - paper: doi:10.1145/1189762.1206075
    title: Ingo Wald, Solomon Boulos and Peter Shirley, Ray tracing deformable scenes using dynamic bounding volume hierarchies, ACM Transactions on Graphics 26(1), 2007
    locator: the full SAH sweep over the sorted centroids for BVHs, and the rebuild against refit trade-off
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Chapter 4, Section 4.3 Bounding Volume Hierarchies, the subsections on BVH construction and on the surface area heuristic with buckets
---

BVH construction builds a [bounding volume hierarchy](/bounding-volume-hierarchy/) over a set of primitives from the top down. It starts with all the primitives at the root, splits them into two sets, and repeats on each set, so each node gets the box of the primitives below it. The common rule for the split is the [surface area heuristic](/surface-area-heuristic/) (SAH) with binning, due to Wald (2007): put the centroids into $K$ equal bins along each axis, try the $K - 1$ bin boundaries of each axis, take the one of least SAH cost, and stop with a leaf when a leaf is not more costly than the best split. The cost is $O(n)$ per level of the tree, which gives $O(n \log n)$ for a balanced tree and $O(n^2)$ in the worst case.

## In plain words

You have a big pile of small parts, and you want to pack them into boxes inside boxes, so that a ray can skip whole boxes at a time. Look at the pile and cut it in two. Pack each half in its own box. Then cut each half again, and so on, until each box holds only a few parts.

The skill is where to cut. A good cut gives two small boxes, because a small box is hit by fewer rays, and it puts many parts in the box that rays hit less often. The SAH puts a number on this. To find a good cut quickly, line the parts up along one direction, sort them into a few buckets, and try only the cuts between buckets.

## The problem

The input is a nonempty set $P$ of $n$ primitives, each with a box $b(p)$ and a centroid $c(p)$, the number $K \ge 2$ of bins, the largest leaf size $m$, and the costs $c_t$ of a traversal step and $c_i$ of a primitive test. The output is a binary tree in which each primitive is in exactly one leaf and each node stores the box of the primitives below it, stored in depth-first order with a list of references. Among such trees we want one with a low SAH cost, the expected cost of a random ray (see the [SAH](/surface-area-heuristic/)). For a node with set $S$ and a split into $L$ and $R$, the local cost is

$$\mathrm{cost}(L, R) = c_t + c_i \frac{A(B(L))\,|L| + A(B(R))\,|R|}{A(B(S))},$$

where $B$ is the box of a set and $A$ its surface area. A leaf costs $c_i |S|$.

## The algorithm

The bin of $p$ on axis $a$ is $k_a(p) = \min(K - 1, \lfloor K (c_a(p) - C_a^-)/(C_a^+ - C_a^-) \rfloor)$, where $[C^-, C^+]$ is the box of the centroids of $S$. A candidate $(a, j)$ puts the bins $0, \ldots, j - 1$ into $L$ and the bins $j, \ldots, K - 1$ into $R$.

```pseudo id=main
BUILD(P, K, m)
L1  refs ← the list of all primitives; tasks ← [(all of refs, no parent)]
L2  while tasks is not empty do pop a task with the set S
L3      make a node with the box B(S), as a child of the parent of the task
L4      if |S| = 1 or all the centroids of S are equal then the node is a leaf; continue
L5      for each axis a with C_a^- < C_a^+ do put each p of S into bin k_a(p), with the box and count of each bin
L6          sweep the bins from the right: the box and count of bins j to K − 1, for j = K − 1 down to 1
L7          sweep from the left: for j = 1 to K − 1, the box and count of bins 0 to j − 1, and A(L)|L| + A(R)|R|
L8          keep the (a, j) of least A(L)|L| + A(R)|R| with L and R not empty
L9      if |S| ≤ m and c_i |S| ≤ cost(L, R) of that (a, j) then the node is a leaf; continue
L10     partition the range of S in refs into L (bin below j on axis a), then R
L11     push the task R, then the task L, as the children of the node
```

Line L6 and line L7 are the two sweeps of Wald: one pass over the bins in each direction gives the box and count of both sides of every boundary, so all $K - 1$ candidates of an axis cost $O(K)$ after the $O(|S|)$ binning of line L5. Line L11 pushes $L$ last, so it is popped next and the nodes come out in depth-first order with each left child right after its parent.

## Example

Six triangles lie in a row along the x axis. The triangle at $c$ has the corners $(c, 0, 0)$, $(c + 1, 1, 0)$ and $(c, 0, 1)$, so its box is $[c, c + 1] \times [0, 1] \times [0, 1]$ with area 6, and its centroid has $x = c + 1/3$. The values are $c = 0, 1, 2, 3, 4, 18$, with $K = 4$, $m = 4$ and $c_t = c_i = 1$. All the centroids have $y = z = 1/3$, so only the x axis has candidates.

| node | $S$ (by $c$) | bins 0, 1, 2, 3 | best boundary | $A(L)\lvert L\rvert + A(R)\lvert R\rvert$ | $A(B(S))$ | split cost | leaf cost | line L9 |
|---|---|---|---|---|---|---|---|---|
| 0 | 0, 1, 2, 3, 4, 18 | {0, 1, 2, 3, 4}, {}, {}, {18} | $j = 1$ | $22 \cdot 5 + 6 \cdot 1 = 116$ | 78 | $1 + 116/78 \approx 2.49$ | 6 | split |
| 1 | 0, 1, 2, 3, 4 | {0}, {1}, {2}, {3, 4} | $j = 2$ | $10 \cdot 2 + 14 \cdot 3 = 62$ | 22 | $1 + 62/22 \approx 3.82$ | 5 | split |
| 2 | 0, 1 | {0}, {}, {}, {1} | $j = 1$ | $6 + 6 = 12$ | 10 | $1 + 12/10 = 2.2$ | 2 | leaf |
| 3 | 2, 3, 4 | {2}, {}, {3}, {4} | $j = 1$ | $6 \cdot 1 + 10 \cdot 2 = 26$ | 14 | $1 + 26/14 \approx 2.86$ | 3 | split |
| 4 | 2 | | | | | | | leaf, line L4 |
| 5 | 3, 4 | {3}, {}, {}, {4} | $j = 1$ | 12 | 10 | 2.2 | 2 | leaf |
| 6 | 18 | | | | | | | leaf, line L4 |

At the root, the boundaries $j = 1, 2, 3$ give the same split, since bins 1 and 2 are empty, and line L8 keeps the first. At node 1 the boundaries $j = 2$ and $j = 3$ both give 62, and again the first is kept. The SAH split at the root puts the far triangle alone. An object median split, $\{0, 1, 2\}$ against $\{3, 4, 18\}$, gives $14 \cdot 3 + 66 \cdot 3 = 240$ and the cost $1 + 240/78 \approx 4.08$, because its right box $[3, 19]$ is long and mostly empty.

## Correctness

Claim: the build ends, each primitive is in exactly one leaf, each box is the union of the boxes of the primitives below it, and each split is a binned candidate of least cost at its node.

The build ends because each split is valid. On an axis with $C_a^- < C_a^+$, the least centroid falls into bin 0 and the largest into bin $K - 1$, so the candidate $j = 1$ has both sides nonempty and line L8 finds a valid one. Line L10 only reorders the range of $S$ in refs, so the ranges of the leaves partition refs, and refs stays a permutation of $P$. Line L3 forms the box from the primitives in the range. The two sweeps compute each side as a union of whole bins, which is exact because union is associative. The full proof is in [proofs/correctness.md](proofs/correctness.md).

Containment and cover are all that [BVH traversal](/bvh-traversal/) needs for exact answers. The SAH only changes the speed.

## Complexity

The model is the [real RAM](/real-ram/), with $K$ a constant. A node with $|S|$ primitives costs $O(|S| + K)$ for its box, its centroid box, the binning on three axes, the sweeps and the partition. The nodes at one depth hold disjoint sets, so one level of the tree costs $O(n)$. With a depth of $O(\log n)$ the build costs $O(n \log n)$, the bound that Wald states; since a binary tree with leaves of bounded size has depth at least $\log_2 (n/m)$, this is also the best case.

The depth is not always logarithmic. The bins are equal in width, and when the centroids are far apart in scale, most of them fall into bin 0. With centroids at $x = 2^i + 1/3$ for $i = 0, \ldots, n - 1$ and $K = 16$, each split takes off only a few of the largest, so the depth grows linearly in $n$ and the build costs $\Theta(n^2)$. The tests check that the depth grows linearly. The extra space is $O(n)$ for the nodes, the refs and the task stack, plus $O(K)$ for the bins.

## Properties

- **Greedy.** Each split is the best for its node if its children became leaves. The tree as a whole need not have the least SAH cost.
- **Approximates the full sweep.** A full SAH sweep tries all $|S| - 1$ splits of the centroids sorted on each axis. With 8 to 32 bins, binning finds splits close to it in quality at a much lower cost.
- **Tight boxes.** Each node gets the box of its own primitives, not the half of its parent's box.
- **Deterministic.** The order of the axes and of the boundaries breaks ties.

## Variants and improvements

- **Median split.** Split at the median centroid on the longest axis, with a linear-time [median finding](/median-finding/) in $O(n)$ per level, or with [quickselect](/quickselect/) in expected $O(n)$. The depth is $O(\log n)$, so the build is $O(n \log n)$ in the worst case, but the trees are worse for rays.
- **Full sweep SAH.** Sort the centroids on each axis and sweep all splits. With three presorted lists kept in order through the splits it costs $O(n \log n)$, the method of Wald and Havran (2006) for kd-trees and of Wald, Boulos and Shirley (2007) for BVHs.
- **Spatial splits.** [Spatial splits](/spatial-splits/) also allow a cut through the primitives, with a reference in both children, to remove overlap.
- **Linear BVH.** The [LBVH](/lbvh-construction/) sorts the primitives by [Morton code](/morton-encoding/) and builds the tree from the sorted order in parallel; HLBVH uses the SAH only near the root.
- **Bottom-up builds.** Agglomerative clustering merges the closest pair of clusters again and again. It can give better trees, at a higher build cost.
- **Parallel builds.** The two children of a node are independent tasks, and the binning of a large node is a reduction over its primitives.
- **Refit or rebuild.** When the primitives move, [BVH refitting](/bvh-refitting/) keeps the tree and only recomputes the boxes in $O(n)$; a rebuild is needed when the quality drops too much.

## When to use it

Use a binned SAH build for static scenes and for scenes that are rebuilt every frame, on a CPU. It is the default of most offline renderers and of PBRT. When the build must be as fast as possible, on a GPU or for millions of moving primitives, use the [LBVH](/lbvh-construction/) and accept a worse tree. When a scene has large triangles that overlap many others, add [spatial splits](/spatial-splits/). When only the positions change and the motion is small, [refit](/bvh-refitting/) instead of building again.

## Pitfalls

- **Bin index out of range.** The centroid at $C_a^+$ gives $\lfloor K \cdot 1 \rfloor = K$. Line L5 must clamp it to $K - 1$ with the min in $k_a(p)$; without the clamp it writes past the last bin.
- **An axis with zero centroid extent.** Line L5 must skip an axis with $C_a^- = C_a^+$, else the bin formula divides by zero. If all three axes have zero extent, line L4 must stop with a leaf; a fallback to a median split would loop on equal centroids.
- **An empty side.** A boundary with all centroids on one side gives a cost equal to $c_t + c_i |S|$ and no split. Line L8 must skip it, or the task is pushed again with the same set and the build never ends.
- **Binning the boxes instead of the centroids.** The bins must be computed from the centroid box $C$, not from the box $B(S)$. With $B(S)$, the centroids can all fall into the middle bins, and fewer useful candidates remain.
- **Area of a flat box.** A box of a set of triangles in one plane has volume 0 but positive area. A cost based on volume would make every such split free.
- **Leaf test without a size bound.** Line L9 makes a leaf only when $|S| \le m$. Without the bound, a set of large overlapping triangles that no split helps can make one leaf with thousands of primitives.

## Implementations

## History

Goldsmith and Salmon (1987) gave the surface area ratio as the measure of the chance that a ray that meets a parent volume also meets a child, and used it for a build that inserts objects one at a time. MacDonald and Booth (1990) made the SAH the rule for a greedy top-down split choice in spatial subdivisions. Havran and others used it for kd-trees in the following decade, and Wald and Havran (2006) showed an $O(n \log n)$ SAH kd-tree build. Wald, Boulos and Shirley (2007) used a full sweep for BVHs of deformable scenes, and Wald (2007) introduced the binned build, which made SAH BVHs fast enough to rebuild at interactive rates and is now the standard top-down method.

## References
