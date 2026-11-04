---
tag: G93DHE
kind: data-structure
slug: ss-tree
name: SS-tree
aliases:
- similarity search tree
area: data-structures/spatial-structures
level: research
summary: Tree of bounding spheres for high-dimensional similarity search.
implements: [spatial-index]
model: external-memory-model
complexity:
  vars: {n: the number of stored points, d: the number of dimensions, M: the most entries in a node, m: the fewest entries in a non-root node, h: the height of the tree, k: the number of neighbors asked for}
  time: {search: O(n d), knn: O(n (d + log n)), insert: O(h (d M + M log M)), delete: O(n d + m h^2 (d M + M log M))}
  space: {total: O(n d)}
history:
  year: 1996
  people: [David A. White, Ramesh Jain]
  note: White and Jain introduced the SS-tree at the IEEE International Conference on Data Engineering in 1996, for similarity search in image and video databases.
prereqs: [r-tree, nearest-neighbor-search]
see_also: [sr-tree, r-star-tree, x-tree, ball-tree, m-tree, k-nearest-neighbor-search, curse-of-dimensionality, best-first-search]
sources:
  - paper: "David A. White and Ramesh Jain, Similarity indexing with the SS-tree, Proceedings of the 12th International Conference on Data Engineering (ICDE), 1996, pp. 516 to 523"
    locator: the bounding spheres around centroids, the insertion by nearest centroid, the split on the dimension of highest variance, the forced reinsert, and the comparison with the R*-tree on nearest neighbor queries
  - paper: doi:10.1145/253260.253347
    title: Norio Katayama and Shin'ichi Satoh, The SR-tree, an index structure for high-dimensional nearest neighbor queries, Proceedings of ACM SIGMOD 1997, pp. 369 to 380
    locator: the analysis of the SS-tree (spheres with large volume but short diameter) and the experiments that compare it with the R*-tree and the SR-tree
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data, the section on sphere-based and other bounding shapes, including the SS-tree and the SR-tree
---

The SS-tree, or similarity search tree, is a balanced tree like the [R-tree](/r-tree/), in which each node is bounded by a sphere instead of a rectangle. The sphere of a node has its center at the *centroid*, the mean, of all the points below it, and a radius large enough to hold them all. A new point goes into the child whose centroid is nearest, and a full node is split on the coordinate along which its entries vary most. Spheres are described by $d + 1$ numbers instead of $2d$, so nodes hold more entries in high dimensions, and the nearest centroid rule makes groups of points that are close together, which suits nearest neighbor search. White and Jain introduced it in 1996 for searching images and videos by feature vectors.

## In plain words

You have many points, perhaps one for each picture in a collection, each point a list of numbers that describes the picture. You want to find the pictures most like a given one, that is, the nearest points.

The SS-tree puts points that are close together into a group, and draws a ball around each group: the center of the ball is the average of the points, and the ball is just large enough to hold them. Groups go into bigger groups with bigger balls. To find the nearest points, you look first into the balls nearest to your point, and you skip a ball when even its nearest edge is farther away than the points you already have.

## The abstract type

The SS-tree implements a [spatial index](/spatial-index/) for points in $\mathbb{R}^d$ with the Euclidean distance: `insert(p, id)`, `delete(p, id)`, `ball(q, r)`, which reports the points within distance $r$ of $q$, and `knn(q, k)`, the [$k$ nearest neighbors](/k-nearest-neighbor-search/) of $q$.

## Representation

Each node holds up to $M$ entries: a leaf holds points with their ids, and an internal node holds child nodes. Each node also stores its *centroid* $c$, the number $n_u$ of points below it, and a radius $\rho$. For a leaf, $c$ is the mean of its points and $\rho$ is the largest distance from $c$ to a point. For an internal node, $c = \frac{1}{n_u} \sum_v n_v c_v$ over its children $v$, which is again the mean of all points below, and $\rho = \max_v (\lVert c - c_v \rVert + \rho_v)$.

**Invariant (S).** (1) Every leaf is at the same depth. (2) Every node other than the root has between $m$ and $M$ entries; an internal root has at least 2. (3) Each node stores the mean $c$ of the points below it and their number. (4) Every point below a node lies within distance $\rho$ of its $c$.

Part (4) holds by the triangle inequality: a point $p$ below child $v$ has $\lVert p - c \rVert \le \lVert p - c_v \rVert + \lVert c_v - c \rVert \le \rho_v + \lVert c_v - c \rVert \le \rho$. The sphere is not the smallest sphere that holds the points (a [minimum enclosing ball](/minimum-enclosing-ball/)), but it is cheap to keep up to date.

## Operations

```pseudo id=main
INSERT(e, level)                                   ▷ e is a point (level 0) or a subtree
L1  u ← root; while height(u) > level:
L2      u ← the child of u whose centroid is nearest to e
L3  add e to u
L4  for u and each ancestor, from the bottom: if it has M + 1 entries then SPLIT it; recompute it:
L5      a leaf: c ← mean of its points; ρ ← largest distance from c to a point
L6      an internal node: c ← mean of the child centroids weighted by their counts; ρ ← max over children (|c − c_v| + ρ_v)
SPLIT(u)
L7  axis ← the coordinate in which the centroids of the entries of u have the largest variance
L8  sort the entries by that coordinate; cut at k, m ≤ k ≤ M + 1 − m, where var(first k) + var(rest) is least
L9  if u is the root then make a new root with the two halves
L10 else add the second half to the parent of u
```

```pseudo id=other
DELETE(p, id)
L11 find a leaf with (p, id) by searching the spheres that contain p; remove it
L12 condense as in the R-tree: going up, remove each node with fewer than m entries and keep its entries
L13 reinsert each kept entry at its height, with INSERT
L14 while the root is internal with one child, make the child the root
BALL(q, r)
L15 skip a node if |q − c| − ρ > r; else report the points of a leaf within r, or search the children
KNN(q, k)
L16 a priority queue of nodes and points by their lower bound, starting with the root; until k points are out:
L17     pop the least; if it is a point, output it
L18     else push its entries: a point with its distance, a child v with max(0, |q − c_v| − ρ_v)
```

**Choose subtree.** The SS-tree goes into the child with the nearest centroid, not the one whose sphere grows least. This puts a point into the group it is most like.

**Split.** The coordinate of highest variance is the one along which the entries spread most, and the cut that minimizes the sum of the variances of the two sides gives two tight groups. The paper does not fix a minimum fill in the same way for every case; the implementation uses $m$, as the R-tree does, so that both halves have at least $m$ entries.

**Forced reinsert.** Like the [R*-tree](/r-star-tree/), the SS-tree of the paper, on its first overflow at a level during an insertion, removes the entries farthest from the centroid and inserts them again, before it splits. The implementation here leaves this out; it does not change correctness.

**Nearest neighbors.** The best-first search of KNN uses $\max(0, \lVert q - c \rVert - \rho)$, the distance from $q$ to the sphere, as a lower bound on the distance from $q$ to every point below a node. Points come out of the queue in order of distance, and the search stops after $k$.

## Example

Take $M = 4$ and $m = 2$ in the plane, and insert a $(1, 1)$, b $(2, 3)$, c $(3, 1)$, d $(8, 8)$, e $(9, 6)$, f $(7, 7)$, g $(2, 8)$ and h $(4, 4)$.

**Insert a to e.** The root leaf gets 5 points and splits. The variance of $x$ in 1, 2, 3, 8, 9 is 10.64 and that of $y$ in 1, 3, 1, 8, 6 is 7.76, so the split is on $x$. With the points sorted by $x$, the cuts are:

| cut | left | right | var(left) + var(right) |
|---|---|---|---|
| $k = 2$ | a, b | c, d, e | $0.25 + 6.89 = 7.14$ |
| $k = 3$ | a, b, c | d, e | $0.67 + 0.25 = 0.92$ |

The cut $k = 3$ wins. The leaves are $\{a, b, c\}$, with centroid $(2, 1.67)$ and radius $1.33$, and $\{d, e\}$, with centroid $(8.5, 7)$ and radius $1.12$. The root has centroid $(4.6, 3.8)$, the mean of all five points.

**Insert f, g and h.** f $(7, 7)$ is nearest to the centroid $(8.5, 7)$ and goes right, which moves that centroid to $(8, 7)$. g $(2, 8)$ is at distance $\sqrt{37} \approx 6.08$ from $(8, 7)$ and $6.33$ from $(2, 1.67)$, so it also goes right, though it lies far to the left. h $(4, 4)$ goes left. The leaves are $\{a, b, c, h\}$, centroid $(2.5, 2.25)$, radius $2.31$, and $\{d, e, f, g\}$, centroid $(6.5, 7.25)$, radius $4.56$. The point g makes the right sphere large: the nearest centroid rule does not look at the radius.

**Queries.** KNN($(5, 5)$, 3) pops the root and pushes its two leaves, with lower bounds $3.72 - 2.31 = 1.41$ for the left leaf and $\max(0, 2.70 - 4.56) = 0$ for the right one. It pops the right leaf and pushes f ($2.83$), e ($4.12$), d ($4.24$) and g ($4.24$). It pops the left leaf ($1.41$) and pushes h ($1.414$), b ($3.61$), c ($4.47$) and a ($5.66$). Then it pops h, f and b, which are the answer. BALL($(3, 3)$, 2) reports b, c and h.

**Delete d, e and f.** After d and e, the right leaf has f and g. Deleting f leaves g alone, under $m = 2$: the leaf is removed and g is inserted again, into the remaining leaf, which then has a, b, c, g, h and splits. The variance is now larger in $y$ (6.64) than in $x$ (1.04), and the best cut gives $\{a, c\}$ and $\{b, h, g\}$.

## Correctness

The SS-tree keeps the R-tree's shape rules, (1) and (2), by the same argument as the R-tree: INSERT adds an entry at the right height, a split gives two nodes with at least $m$ entries since the cut has $m \le k \le M + 1 - m$, and the condensation of DELETE reinserts every entry of a removed node at its height. Parts (3) and (4) hold because every node whose set of points changes is on the path that is recomputed, by lines L5 and L6, from the bottom up. The searches are correct because the sphere bound of part (4) gives a lower bound on the distance from $q$ to each point below a node: BALL never skips a node with a point within $r$, and KNN outputs points in order of distance, since the lower bounds of the queue never exceed the true distances of the points below. The full proof is in the proofs folder.

## Complexity

The model is the [external memory model](/external-memory-model/) with one node per page, or the RAM with $O(d)$ for each distance.

- **Search.** In the worst case every node is visited: $O(n d)$ for BALL. KNN also uses a heap of up to $O(n)$ entries, $O(n (d + \log n))$. In low dimensions and on clustered data, a query visits few nodes; in high dimensions, most nodes have lower bounds below the $k$-th distance, and the search reads most of the tree, as for any tree of this kind (the [curse of dimensionality](/curse-of-dimensionality/)).
- **Insert.** The descent compares $O(M)$ centroids per level at $O(d)$ each, the recomputation costs $O(d M)$ per level, and a split costs a sort, $O(M \log M)$, plus $O(d M)$ for the variances with prefix sums. So $O(h (d M + M \log M))$.
- **Delete.** Finding the point can visit every node whose sphere contains it, $O(n d)$ in the worst case. Up to $m h$ entries are reinserted, each at the cost of an insertion.
- **Space.** $O(n d)$. A node stores $d + 2$ numbers, against $2d$ for a rectangle, so a page holds more entries for large $d$.

| operation | time | case |
|---|---|---|
| ball query | $O(n d)$ | worst |
| $k$ nearest neighbors | $O(n (d + \log n))$ | worst |
| insert | $O(h (d M + M \log M))$ | worst |
| delete | $O(n d + m h^2 (d M + M \log M))$ | worst |
| space | $O(n d)$ | total |

## Variants

- **SS+-tree.** Kurniawati, Jin and Shepherd proposed in 1997 a version that splits with a k-means clustering of the entries and uses a tighter sphere.
- **SR-tree.** The [SR-tree](/sr-tree/) of Katayama and Satoh keeps a bounding rectangle with each sphere, and bounds a node by their intersection, which has both a small volume and a short diameter.
- **Ball tree and M-tree.** The [ball tree](/ball-tree/) is a static binary tree of balls; the [M-tree](/m-tree/) uses balls around stored objects in any [metric space](/metric-space/), with only the distance function.
- **Smaller spheres.** The sphere of a node can be shrunk by using the distance to each point below, at the cost of reading the subtree, or by a minimum enclosing ball of the child spheres.

## When to use it

Use the SS-tree for nearest neighbor search on points of moderate dimension, about 5 to 20, such as feature vectors of images, when the data changes and the query is "find the most similar". In the experiments of White and Jain it beat the R*-tree on such queries. For more dimensions, every tree degrades; use the [X-tree](/x-tree/), a scan of compressed vectors, or [approximate nearest neighbor](/approximate-nearest-neighbor/) methods. For window queries on rectangles, use an R-tree.

## Pitfalls

- **Large spheres.** A sphere around a group is much larger in volume than the box around it in high dimensions, so a sphere can overlap many others. The radius rule above also gives spheres larger than the smallest. This is the weakness the SR-tree addresses.
- **The radius rule.** The radius must cover the child spheres, $\lVert c - c_v \rVert + \rho_v$, not only the child centroids, or part (4) fails and queries miss points.
- **Stale centroids.** A centroid must be recomputed from the counts after every change below it; forgetting the weights makes it the mean of the child centroids, which is not the mean of the points.
- **Floating point.** Recomputing means and distances many times adds rounding error. Compare with a small tolerance when testing whether a point is inside a sphere.

## Implementations

## History

In the 1990s, systems for searching images by their content described each image by a feature vector of tens of numbers, and needed nearest neighbor search on them. White and Jain, at the University of California, San Diego, proposed the SS-tree in 1996, building on the R*-tree but with spheres, centroids and a split by variance, and showed that it beat the R*-tree on such data. Katayama and Satoh then showed in 1997 that spheres have short diameters but large volumes, and proposed the SR-tree, which uses both spheres and rectangles.

## References
