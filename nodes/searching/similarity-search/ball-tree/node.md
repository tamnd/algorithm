---
tag: DT55WY
kind: data-structure
slug: ball-tree
name: Ball tree
aliases:
- Omohundro ball tree
- balltree
- metric ball tree
area: searching/similarity-search
level: advanced
summary: Binary tree of hyperspheres that supports nearest-neighbor search in general metric spaces.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of points, b: the leaf size, E: the time of one distance evaluation, K: the number of reported points}
  time: {build: O(n log n E), knn: O(n E), range: O(n E)}
  space: {total: O(n)}
history:
  year: 1989
  people: [Stephen M. Omohundro, Jeffrey K. Uhlmann]
  note: Omohundro described ball trees, binary trees of nested balls, in a technical report of 1989; Uhlmann described metric trees with ball partitioning for general metric spaces in 1991.
prereqs: [metric-space, triangle-inequality, kd-tree]
see_also: [vantage-point-tree, cover-tree, m-tree, gnat, bk-tree, kd-tree-nearest-neighbor-search, metric-space-indexing, minimum-enclosing-ball]
sources:
  - paper: doi:10.1016/0020-0190(91)90074-R
    title: Jeffrey K. Uhlmann, Satisfying general proximity/similarity queries with metric trees, Information Processing Letters 40(4), 1991
    locator: pages 175 to 179 (metric trees that split by balls around a pivot and prune by the triangle inequality)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, Section 4.5 (distance-based indexing, with ball partitioning, the ball tree of Omohundro and the metric trees of Uhlmann)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (the pruning rule d(q, c) − r(c) for a ball with center c and covering radius r(c), and the survey of ball-based indexes)
---

A ball tree is a binary tree for points in a [metric space](/metric-space/) in which each node covers its points by a ball: a center $c$ and a covering radius $\rho$ such that every point of the subtree is within $\rho$ of $c$. A query prunes a node when $\delta(q, c) - \rho$ is no smaller than the best distance found so far, since by the [triangle inequality](/triangle-inequality/) no point in the ball can be closer. Unlike the [k-d tree](/kd-tree/), it uses only distances, so it works for any metric, and its balls adapt to data that lie near a low-dimensional surface. Built by splitting at the median along two far-apart pivots, it has height $\lceil \lg(n/b) \rceil + 1$ for leaves of at most $b$ points and takes $O(n \log n)$ distance evaluations to build; queries take $O(n)$ evaluations in the worst case. Omohundro described ball trees in 1989.

## In plain words

Draw a circle around all the points. Split the points into two halves, and draw a smaller circle around each half. Keep splitting until each circle holds only a few points. That nested set of circles is the tree.

To find the point nearest a query, go into the circle whose center is closer first. Once you have found a fairly close point, skip any circle whose edge is farther from the query than that point: nothing inside it can be closer. The circles need only distances, so the same idea works for words, sets, or any other things that have a proper distance.

## The abstract type

A ball tree implements a [similarity index](/similarity-index/) over a set $S$ of $n$ points of a metric space $(M, \delta)$: `build(S)`, `knn(q, k)`, which returns the $k$ points of $S$ nearest to $q$, and `range(q, r)`, which returns the points within $r$ of $q$. Its cost is counted in evaluations of $\delta$.

## Representation

Each node $t$ has a center $t.c \in S$ and a radius $t.\rho \ge 0$. A leaf holds a list $t.points$ of at most $b$ points; an inner node has two children $t.left$ and $t.right$.

**Invariant (R).** Every point $x$ in the subtree of $t$ has $\delta(t.c, x) \le t.\rho$.

**Invariant (S).** The two children of an inner node with $s$ points hold $\lfloor s/2 \rfloor$ and $\lceil s/2 \rceil$ points.

Here the center is a point of the subtree, which works in every metric space. In $\mathbb{R}^d$ the center is often the centroid, which gives smaller balls; the radius is again the largest distance from it. Each point is stored in exactly one leaf.

## Operations

```pseudo id=main
BUILD(S)
L1  if |S| ≤ b then return a leaf with the points S, center and radius as in L2
L2  c ← any point of S; ρ ← max over x ∈ S of δ(c, x)
L3  a ← the point of S farthest from c; z ← the point of S farthest from a
L4  sort S by δ(x, a) − δ(x, z); S1 ← the first ⌊|S|/2⌋ points, S2 ← the rest
L5  return a node with center c, radius ρ, children BUILD(S1) and BUILD(S2)

KNN(t, q, k)                               ▷ H holds the k best pairs found; τ is the k-th distance, or ∞
L6  if δ(q, t.c) − t.ρ ≥ τ then return
L7  if t is a leaf then offer (δ(q, x), x) to H for each x ∈ t.points; return
L8  visit the child whose center is nearer to q first, then the other, with KNN
```

Line L3 picks two pivots that are far apart, in two linear scans; line L4 sends each point to the side of the pivot it is relatively closer to. A median split by this key keeps (S), so the tree is balanced, whatever the metric. Line L6 is the pruning test, and line L8 the order that finds good candidates early, as in the [k-d tree nearest neighbor search](/kd-tree-nearest-neighbor-search/).

**Range query** visits the tree in the same way, with a fixed radius:

```pseudo id=range
RANGE(t, q, r)
L9  if δ(q, t.c) − t.ρ > r then return
L10 if t is a leaf then report each x ∈ t.points with δ(q, x) ≤ r
L11 else RANGE(t.left, q, r); RANGE(t.right, q, r)
```

Insertion goes down to the child whose center is nearer, raises the radii on the way, and splits a leaf that overflows; it does not keep (S), so trees built by insertion can be unbalanced.

## Example

Take the eight points $(1,1), (2,3), (3,1), (6,5), (7,7), (8,4), (2,2), (7,5)$ in the plane, with the Euclidean distance and $b = 2$. At the root, $c = (1,1)$, and the farthest point is $(7,7)$ at $\sqrt{72} \approx 8.49$, which is the radius. The pivots are $a = (7,7)$ and then $z = (1,1)$, the point farthest from $a$. The key $\delta(x, a) - \delta(x, z)$ is negative for the four points near $(7,7)$ and positive for the others, so the split is $\{(7,7), (6,5), (8,4), (7,5)\}$ and $\{(2,3), (3,1), (2,2), (1,1)\}$. Repeating gives:

```
center (1,1), radius 8.49
├─ center (7,7), radius 3.16
│  ├─ leaf (8,4), (7,5)         center (8,4), radius 1.41
│  └─ leaf (6,5), (7,7)         center (6,5), radius 2.24
└─ center (2,3), radius 2.24
   ├─ leaf (3,1), (1,1)         center (3,1), radius 2.00
   └─ leaf (2,2), (2,3)         center (2,2), radius 1.00
```

The nearest neighbor of $q = (6,6)$, with $k = 1$:

| node | $\delta(q, c)$ | $\delta(q, c) - \rho$ | $\tau$ before | action |
|---|---|---|---|---|
| root | 7.07 | $-1.42$ | $\infty$ | children at 1.41 and 5.00: left first |
| ball (7,7) | 1.41 | $-1.75$ | $\infty$ | children at 2.83 and 1.00: leaf (6,5) first |
| leaf (6,5) | 1.00 | $-1.24$ | $\infty$ | distances 1.00 and 1.41; $\tau = 1$ |
| leaf (8,4) | 2.83 | 1.41 | 1 | pruned |
| ball (2,3) | 5.00 | 2.76 | 1 | pruned |

The answer is $(6,5)$ at distance 1. Two of the four leaves were never opened.

## Correctness

**Build.** Line L2 sets the radius to the largest distance from the center, so (R) holds at each node. Line L4 makes (S) true.

**Pruning is safe.** For a point $x$ in the subtree of $t$, the triangle inequality and (R) give $\delta(q, x) \ge \delta(q, t.c) - \delta(t.c, x) \ge \delta(q, t.c) - t.\rho$. So if line L6 prunes $t$, no point of $t$ is strictly closer than the current $k$-th distance, and the final $k$ distances are the true ones. For RANGE, a point of a pruned node is at distance more than $r$. The full proof is in `proofs/correctness.md`.

## Complexity

The model is the [real RAM](/real-ram/) with a distance oracle of cost $E$.

- **Height.** By (S), a node at depth $j$ holds at most $\lceil n / 2^j \rceil$ points, so leaves are reached by depth $\lceil \lg(n/b) \rceil$, and the height is at most $\lceil \lg(n/b) \rceil + 1$ levels.
- **Build.** At one depth the subsets are disjoint, and lines L2 to L4 take $O(|S|)$ distance evaluations each, so a level takes $O(n)$ evaluations and the build $O(n \log n)$. Sorting adds $O(n \log^2 n)$ comparisons; a linear-time median selection in place of the sort brings the total to $O(n \log n)$.
- **Queries.** In the worst case every node is visited: $O(n)$ evaluations, for example when the points lie on a sphere around $q$. On data of low [intrinsic dimension](/intrinsic-dimensionality/), most nodes are pruned; there is no worst-case bound of the kind the [cover tree](/cover-tree/) gives.
- **Space.** $O(n)$: each point is in one leaf, and there are fewer than $2n/b + 1$ nodes.

| operation | distance evaluations | case |
|---|---|---|
| build | $O(n \log n)$ | worst, with linear-time selection |
| knn$(q, k)$ | $O(n)$ | worst |
| range$(q, r)$ | $O(n)$ | worst |
| space | $O(n)$ | total |

## Variants

- **Centroid centers in $\mathbb{R}^d$.** Use the mean of the points as the center; the [minimum enclosing ball](/minimum-enclosing-ball/) gives the smallest radius but costs more to build.
- **Vantage-point tree.** A [vantage-point tree](/vantage-point-tree/) splits by one ball around a pivot: the points inside the median distance and those outside.
- **M-tree.** The [M-tree](/m-tree/) is a balanced, disk-based ball tree with insertion and node splits, in the style of a B-tree.
- **Dual-tree algorithms.** For all nearest neighbors or kernel sums, two ball trees are walked together and pairs of nodes are pruned at once.
- **Anchors hierarchy and other builds.** Bottom-up builds merge nearby balls; they give tighter balls at a higher build cost.

## When to use it

Use a ball tree for nearest neighbor and range queries in moderate dimension (up to a few tens), for non-Euclidean metrics, or for data that lie near a low-dimensional surface in a high-dimensional space, where the k-d tree's axis-aligned cells waste effort. It is the second exact index, after the k-d tree, in common machine learning libraries for [k-nearest neighbors](/k-nearest-neighbors/). In high intrinsic dimension it degrades to a scan with extra overhead; then use an approximate index such as [HNSW](/hnsw/).

## Pitfalls

- **Strict pruning against ties.** Prune with $\delta(q, c) - \rho \ge \tau$ only when ties may be returned in any order; for a range query, prune only when the bound is strictly greater than $r$, or boundary points are lost.
- **Not a metric.** The pruning needs the triangle inequality. Squared Euclidean distance is not a metric; prune with the plain distance.
- **Large leaves or tiny leaves.** Leaves of one point waste a distance evaluation on each center; very large leaves are scanned in full. Leaf sizes of 10 to 40 are typical.
- **Radius from an old center.** After moving a center or inserting a point, the radius must be recomputed, or (R) breaks.

## Implementations

## History

Omohundro described ball trees, with several build methods, in a technical report at the International Computer Science Institute in Berkeley in 1989. Uhlmann gave metric trees with ball and generalized hyperplane partitioning for general metric spaces in 1991. Chávez, Navarro, Baeza-Yates and Marroquín later placed both among the clustering-based metric indexes.

## References
