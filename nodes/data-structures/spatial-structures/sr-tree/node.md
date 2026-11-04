---
tag: PJ11JW
kind: data-structure
slug: sr-tree
name: SR-tree
aliases:
- sphere-rectangle tree
area: data-structures/spatial-structures
level: research
summary: High-dimensional index that stores both a bounding rectangle and a bounding sphere per node.
implements: [spatial-index]
model: external-memory-model
complexity:
  vars: {n: the number of stored points, d: the number of dimensions, M: the most entries in a node, m: the fewest entries in a non-root node, h: the height of the tree, k: the number of neighbors asked for}
  time: {search: O(n d), knn: O(n (d + log n)), insert: O(h (d M + M log M)), delete: O(n d + m h^2 (d M + M log M))}
  space: {total: O(n d)}
history:
  year: 1997
  people: [Norio Katayama, Shin'ichi Satoh]
  note: Katayama and Satoh introduced the SR-tree at ACM SIGMOD 1997, combining the bounding spheres of the SS-tree with the bounding rectangles of the R*-tree.
prereqs: [ss-tree, r-tree]
see_also: [ss-tree, r-star-tree, x-tree, minimum-bounding-rectangle, k-nearest-neighbor-search, curse-of-dimensionality, best-first-search, ball-tree]
sources:
  - paper: doi:10.1145/253260.253347
    title: Norio Katayama and Shin'ichi Satoh, The SR-tree, an index structure for high-dimensional nearest neighbor queries, Proceedings of ACM SIGMOD 1997, pp. 369 to 380
    locator: the comparison of spheres and rectangles in volume and diameter, the region as the intersection of a sphere and a rectangle, the radius formula, the insertion and split taken from the SS-tree, the distance from a point to a region, and the experiments against the SS-tree and the R*-tree
  - paper: "David A. White and Ramesh Jain, Similarity indexing with the SS-tree, Proceedings of the 12th International Conference on Data Engineering (ICDE), 1996, pp. 516 to 523"
    locator: the SS-tree with its centroids, its insertion by nearest centroid and its split on the dimension of highest variance, which the SR-tree reuses
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data, the section on sphere-based and other bounding shapes, including the SS-tree and the SR-tree
---

The SR-tree, or sphere-rectangle tree, is an index for nearest neighbor search on points in many dimensions. It has the shape and the insertion rules of the [SS-tree](/ss-tree/), but each node keeps both a bounding sphere, around the centroid of its points, and a bounding rectangle, the [MBR](/minimum-bounding-rectangle/) of its points. The region of the node is the intersection of the two. Katayama and Satoh, who introduced it in 1997, observed that in high dimensions a rectangle has a small volume but a long diagonal, and a sphere a short diameter but a large volume. The intersection is small in both senses, so a query reaches fewer nodes. The rectangles also let the tree use a smaller radius for the spheres.

## In plain words

To search a collection of points for the ones nearest to a question, a tree puts close points into groups and draws a shape around each group. The search skips a group when its shape is far from the question. So the shapes should be small.

A box around a group is small in volume but can be long from corner to corner. A ball around a group has a short width but a large volume. The SR-tree keeps both shapes for every group. A point of the group must be in the box and in the ball, so the search can use whichever of the two is farther from the question. The box also helps to make the ball smaller.

## The abstract type

The SR-tree implements a [spatial index](/spatial-index/) for points in $\mathbb{R}^d$ with the Euclidean distance: `insert(p, id)`, `delete(p, id)`, `ball(q, r)`, which reports the points within distance $r$ of $q$, and `knn(q, k)`, the [$k$ nearest neighbors](/k-nearest-neighbor-search/) of $q$.

## Representation

Each node holds up to $M$ entries: points with their ids in a leaf, child nodes in an internal node. Each node $u$ keeps:

- the centroid $c_u$, the mean of the points below it, and their number $n_u$;
- the rectangle $R_u = [\ell_u, h_u]$, the MBR of the points below;
- a radius $\rho_u$, such that the sphere $S_u$ of radius $\rho_u$ around $c_u$ holds the points below.

For a leaf, $\rho_u$ is the largest distance from $c_u$ to a point. For an internal node, the radius is

$$\rho_u = \max_{v} \min\left(\lVert c_u - c_v \rVert + \rho_v, \ \operatorname{far}(c_u, R_v)\right),$$

where $v$ runs over the children and $\operatorname{far}(c, R)$ is the distance from $c$ to the farthest corner of $R$. Both terms bound the distance from $c_u$ to each point below $v$: the first since the point is in $S_v$, the second since it is in $R_v$. So the smaller of the two is also a bound. The SS-tree uses only the first term.

**Invariant (SR).** (1) Every leaf is at the same depth. (2) Every node other than the root has between $m$ and $M$ entries; an internal root has at least 2. (3) $c_u$ is the mean and $n_u$ the number of the points below $u$, and $R_u$ is their MBR. (4) Every point below $u$ lies in $S_u \cap R_u$.

**Distance to a region.** For a query $q$, the distance to a node is bounded below by

$$\operatorname{mindist}(q, u) = \max\left(\lVert q - c_u \rVert - \rho_u, \ \operatorname{dist}(q, R_u)\right),$$

where $\operatorname{dist}(q, R)$ is the distance from $q$ to the nearest point of the rectangle. Each term is a lower bound on the distance from $q$ to the points below $u$, so the larger is a lower bound too. It is not the exact distance to $S_u \cap R_u$, which is harder to compute, but it is never larger than that distance.

## Operations

```pseudo id=main
INSERT(e, level)                                    ▷ as in the SS-tree
L1  u ← root; while height(u) > level:
L2      u ← the child of u whose centroid is nearest to e
L3  add e to u
L4  for u and each ancestor, from the bottom: if it has M + 1 entries then SPLIT it; recompute it:
L5      a leaf: c ← mean of its points; ρ ← largest distance from c to a point; R ← MBR of its points
L6      an internal node: c ← mean of the child centroids weighted by their counts; R ← MBR of the child rectangles
L7          ρ ← max over children v of min(|c − c_v| + ρ_v, far(c, R_v))
SPLIT(u)
L8  as in the SS-tree: sort by the coordinate of highest variance, and cut where the sum of the variances is least
DELETE(p, id)
L9  find a leaf with (p, id) through the nodes with mindist(p, u) = 0; remove it
L10 condense: going up, remove each node with fewer than m entries, and keep its entries
L11 reinsert each kept entry at its height
L12 while the root is internal with one child, make the child the root
BALL(q, r)
L13 skip a node if mindist(q, u) > r; else report the points of a leaf within r, or search the children
KNN(q, k)
L14 best-first search with keys mindist(q, u) for nodes and the distance for points; stop after k points
L15 mindist(q, u) = max(|q − c_u| − ρ_u, dist(q, R_u))
```

**Insertion and split.** The SR-tree uses the rules of the SS-tree without change: insertion by nearest centroid, the split on the coordinate of highest variance, and, in the paper, the forced reinsert on the first overflow at a level. The implementation leaves out the forced reinsert, which does not change correctness. Only the recomputation of a node changes: it now also keeps the rectangle, and the radius uses it.

**Fanout.** An entry of an internal node stores a sphere ($d + 1$ numbers), a rectangle ($2d$ numbers) and a count, about $3d$ numbers in all. So with a fixed page size, an SR-tree node holds about a third as many entries as an SS-tree node and two thirds as many as an R*-tree node. The paper found that the smaller regions more than pay for the lower fanout for nearest neighbor queries.

## Example

Take the points of the SS-tree example, with $M = 4$ and $m = 2$: a $(1, 1)$, b $(2, 3)$, c $(3, 1)$, d $(8, 8)$, e $(9, 6)$, f $(7, 7)$, g $(2, 8)$ and h $(4, 4)$. Insertion and splits are as in the SS-tree, so the leaves are again $\{a, b, c, h\}$ and $\{d, e, f, g\}$.

| node | centroid | radius | rectangle |
|---|---|---|---|
| left leaf | $(2.5, 2.25)$ | $2.31$ | $[1, 4] \times [1, 4]$ |
| right leaf | $(6.5, 7.25)$ | $4.56$ | $[2, 9] \times [6, 8]$ |
| root | $(4.5, 4.75)$ | $5.55$ | $[1, 9] \times [1, 8]$ |

**The radius of the root.** For the left leaf, the sphere term is $\lVert (4.5, 4.75) - (2.5, 2.25) \rVert + 2.31 = 3.20 + 2.31 = 5.51$, and the farthest corner of $[1, 4] \times [1, 4]$ from the root centroid is $(1, 1)$, at $5.13$; the smaller is $5.13$. For the right leaf, the sphere term is $3.20 + 4.56 = 7.76$, and the farthest corner of $[2, 9] \times [6, 8]$ is $(9, 8)$, at $5.55$; the smaller is $5.55$. So $\rho = 5.55$. The SS-tree, with the sphere terms only, has $\rho = 7.76$.

**Lower bounds.** For $q = (5, 5)$ and the right leaf, the sphere bound is $\lVert q - (6.5, 7.25) \rVert - 4.56 = 2.70 - 4.56 < 0$, but $q$ is at distance $1$ from the rectangle $[2, 9] \times [6, 8]$; so mindist is $1$, where the SS-tree has $0$. For the root, from $q = (0, 10)$ the sphere bound is $6.92 - 5.55 = 1.36$ and the rectangle bound $\sqrt{5} = 2.24$, so the rectangle gives the bound; from $q = (10, 0)$, the sphere bound is $7.27 - 5.55 = 1.72$ and the rectangle bound $\sqrt{2} = 1.41$, so the sphere gives it.

**Queries.** KNN($(5, 5)$, 3) returns h, f and b, at $1.41$, $2.83$ and $3.61$, as in the SS-tree, and BALL($(3, 3)$, 2) returns b, c and h. Deleting d, e and f gives the leaves $\{a, c\}$ and $\{b, g, h\}$, as in the SS-tree.

## Correctness

The shape rules (1) and (2) hold by the argument of the SS-tree and the R-tree, since the SR-tree inserts, splits and condenses in the same way. Part (3) holds since every node whose points change is recomputed from the bottom up, and the mean and the MBR of a union are computed from those of the parts. Part (4) holds by the radius formula: each of the two terms bounds the distance from the centroid to every point below the child. Then mindist is a lower bound on the distance from $q$ to every point below a node, so BALL never skips a node with a point within $r$, and the best-first search outputs the points in order of distance. The full proof is in the proofs folder.

## Complexity

The costs are those of the [SS-tree](/ss-tree/), with $O(d)$ more work per entry for the rectangle, which does not change the bounds. The model is the [external memory model](/external-memory-model/) with one node per page, or the RAM with $O(d)$ for each distance.

- **Search.** In the worst case every node is visited: $O(n d)$ for BALL, and $O(n (d + \log n))$ for KNN with its heap. The gain of the SR-tree is in the number of nodes read in practice.
- **Insert.** $O(h (d M + M \log M))$: the descent, the recomputations, and the splits along one path.
- **Delete.** $O(n d)$ to find the point in the worst case, plus up to $m h$ reinsertions.
- **Space.** $O(n d)$. The internal nodes are larger than in the SS-tree, about $3d$ numbers per entry.

| operation | time | case |
|---|---|---|
| ball query | $O(n d)$ | worst |
| $k$ nearest neighbors | $O(n (d + \log n))$ | worst |
| insert | $O(h (d M + M \log M))$ | worst |
| delete | $O(n d + m h^2 (d M + M \log M))$ | worst |
| space | $O(n d)$ | total |

## Variants

- **SS-tree.** The [SS-tree](/ss-tree/) is the SR-tree without rectangles. It has a larger fanout and larger regions.
- **R*-tree.** The [R*-tree](/r-star-tree/) keeps only rectangles. The SR-tree paper reports that its rectangles have small volumes but long diagonals in high dimensions.
- **X-tree.** The [X-tree](/x-tree/) keeps rectangles and avoids overlap by supernodes. The SR-tree and the X-tree were proposed about the same time for the same kind of data.
- **Other bounding shapes.** The A-tree stores the rectangles of the children relative to the parent with few bits; other trees use ellipsoids or convex hulls. All trade the size of an entry against the tightness of the region.

## When to use it

Use the SR-tree for nearest neighbor search on points in moderately high dimensions, about 10 to 50, in a disk-based index, especially when the data is clustered, as with real image features. In the experiments of Katayama and Satoh, it read fewer pages and used less CPU time than the SS-tree and the R*-tree for such queries, and the gain was larger on real data than on uniform data. For very high dimensions or very large data, [approximate nearest neighbor](/approximate-nearest-neighbor/) methods are usually faster.

## Pitfalls

- **The radius formula.** Both terms must cover the child's points. Using the distance from the centroid to the center of the child's rectangle, or to its nearest corner, gives a radius that is too small, and queries miss points.
- **mindist is not the exact distance.** The maximum of the two bounds is below the true distance to the intersection. It is a correct bound for pruning, but do not use it as the distance in a test that needs the exact value.
- **Fanout.** In very high dimensions the entries become large, and a page may hold only a few. Choose the page size with the dimension in mind.
- **Keep the rectangle exact.** The rectangle of a node must be recomputed from the children after a split or a delete, not only grown; a stale large rectangle is correct but loses the gain.

## Implementations

## History

Katayama and Satoh, at the National Center for Science Information Systems in Tokyo, studied in 1997 why the SS-tree beat the R*-tree on nearest neighbor queries on some data and not on other data. They found that rectangles have small volume and long diameter, and spheres the reverse, in high dimensions, and that both properties matter. Their SR-tree combined the two and was faster than both in their experiments. The same years saw the X-tree (1996), the TV-tree, and the VA-file (1998), which showed that for very high dimensions a scan of compressed vectors can beat all these trees.

## References
