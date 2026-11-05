---
tag: GE79TV
kind: data-structure
slug: m-tree
name: M-tree
aliases:
- metric tree
- metric tree M-tree
area: searching/similarity-search
level: advanced
summary: Balanced metric-space tree that stores covering balls and supports dynamic insertion.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of objects, M: the node capacity, h: the height}
  time: {insert: O(M^2 h), range: O(n), knn: O(n log n), height: O(log n)}
  space: {total: Θ(n)}
properties: {deterministic: true, online: true, external: true}
history:
  year: 1997
  people: [Paolo Ciaccia, Marco Patella, Pavel Zezula]
  note: Ciaccia, Patella and Zezula introduced the M-tree at VLDB 1997 as a paged, balanced, dynamic index for metric spaces in the style of the B-tree and the R-tree.
prereqs: [metric-space, triangle-inequality, r-tree]
see_also: [vantage-point-tree, mvp-tree, ball-tree, r-tree, pivot-based-indexing, metric-space-indexing, similarity-range-query, k-nearest-neighbor-search]
sources:
  - paper: "Paolo Ciaccia, Marco Patella and Pavel Zezula, M-tree, an efficient access method for similarity search in metric spaces, Proceedings of the 23rd International Conference on Very Large Data Bases (VLDB), 1997"
    locator: pages 426 to 435 (routing and leaf entries with covering radii and distances to the parent, the range and k-NN searches with the pruning by the parent distance, insertion, the split with promotion policies such as mM_RAD and the generalized hyperplane and balanced partitions)
  - book: isbn:9780387291468
    title: Pavel Zezula, Giuseppe Amato, Vlastislav Dohnal and Michal Batko, Similarity Search, The Metric Space Approach, Springer, 2006
    locator: Chapter 2, Survey of Existing Approaches (the M-tree and its variants, including the Slim-tree and the PM-tree)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data, Section 4.5, Distance-Based Indexing Methods (the M-tree among the ball partitioning methods)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 5, the M-tree among the clustering-based indexes, with covering radii)
---

The M-tree is a balanced tree of balls for objects of a [metric space](/metric-space/), built like a B-tree by insertions at the leaves and splits that move up toward the root. Each internal entry holds a *routing object* $o$, a *covering radius* $r(o)$ such that every object of its subtree lies within $r(o)$ of $o$, and the distance from $o$ to the routing object of its parent. A [range query](/similarity-range-query/) skips a subtree when its ball cannot meet the query ball, $d(q, o) > r + r(o)$, and often skips it without computing $d(q, o)$, from the parent distance and the [triangle inequality](/triangle-inequality/). Unlike the [vantage-point tree](/vantage-point-tree/), it accepts insertions without a rebuild, and its nodes fit disk pages. Ciaccia, Patella and Zezula introduced it in 1997.

## In plain words

Think of an [R-tree](/r-tree/), but with circles instead of rectangles, and with only a distance function instead of coordinates. Every node of the tree is a group of objects with a center and a radius large enough to cover the whole group. Groups contain smaller groups, down to the leaves, which hold the objects.

To add an object, go down from the top, each time into the group whose center is closest, growing a radius if needed. When a leaf is full, cut it into two groups around two new centers and tell the parent, which may in turn be full and be cut. To answer a query, go down only into groups whose circle touches the circle around the query. Each entry also remembers its distance to its parent's center, which often shows that it is too far without measuring anything.

## The abstract type

The M-tree is a dynamic [similarity index](/similarity-index/) over a metric space $(U, d)$: it supports INSERT of an object, range queries $R(q, r)$ and [k-nearest neighbor](/k-nearest-neighbor-search/) queries. It uses only a function that computes $d$, and the cost of an operation is counted in evaluations of $d$ and in node accesses, which are disk reads when the nodes are pages.

## Representation

The capacity $M \ge 2$ is the most entries a node holds.

- A **leaf entry** is $(x, d_p)$: a stored object $x$ and its distance $d_p = d(x, o_p)$ to the routing object $o_p$ of the parent entry.
- A **routing entry** is $(o, r(o), \mathrm{child}, d_p)$: a routing object $o$, a covering radius $r(o) \ge 0$, a pointer to the child node, and $d_p = d(o, o_p)$.
- The entries of the root have no parent, and no $d_p$.

The invariants are:

1. **Covering.** For each routing entry, $d(o, y) \le r(o)$ for every object $y$ stored in the subtree of its child.
2. **Parent distances.** Each stored $d_p$ equals the distance to the routing object of the parent entry.
3. **Balance.** All leaves are at the same depth, and every node holds at most $M$ entries.

The routing objects are stored objects promoted at splits, so they are copies; the same object can be a routing object at several levels and also in a leaf.

## Operations

```pseudo id=main
RANGE(N, q, r, dqp)                          ▷ dqp = d(q, routing object of N), or none at the root
L1  for each entry e of N do
L2      if dqp ≠ none and |dqp − e.dp| > r + e.radius then continue      ▷ skipped with no evaluation
L3      de ← d(q, e.obj)
L4      if N is a leaf then
L5          if de ≤ r then report e.obj
L6      else if de ≤ r + e.radius then
L7          RANGE(e.child, q, r, de)

KNN(q, k)                                    ▷ B: a max-heap of at most k (distance, object); τ ← ∞; PQ ← {(0, root, none)}
L8  while PQ is not empty do
L9      (dmin, N, dqp) ← the element of PQ with the least dmin, removed
L10     if dmin > τ then stop
L11     for each entry e of N do
L12         if dqp ≠ none and |dqp − e.dp| − e.radius > τ then continue
L13         de ← d(q, e.obj)
L14         if N is a leaf: if |B| < k or de < τ then add (de, e.obj) to B, drop the farthest if |B| > k, and τ ← the largest distance in B once |B| = k
L15         else if max(de − e.radius, 0) ≤ τ then add (max(de − e.radius, 0), e.child, de) to PQ
L16 return B in order of distance

INSERT(x)
L17 if INSERT-AT(root, x, none, none) returns two entries then root ← a new internal node holding them

INSERT-AT(N, x, p, dxp)                      ▷ p = routing object of N, dxp = d(x, p)
L18 if N is a leaf then add the entry (x, dxp) to N
    else
L19     compute d(x, e.obj) for every entry e of N
L20     if some e has d(x, e.obj) ≤ e.radius then e ← the nearest such entry
L21     else e ← the entry with the least d(x, e.obj) − e.radius; e.radius ← d(x, e.obj)
L22     if INSERT-AT(e.child, x, e.obj, d(x, e.obj)) returns e1, e2 then replace e by e1 and e2, with ei.dp ← d(ei.obj, p)
L23 if N has more than M entries then return SPLIT(N)

SPLIT(N)                                     ▷ N has M + 1 entries
L24 compute d between all pairs of entries of N
L25 for each pair (o1, o2): partition the entries by turns, each taking its nearest free entry; ri ← max over its part of d(oi, e.obj) + e.radius; keep the pair with the least max(r1, r2)
L26 make two nodes of the kind of N with the two parts, and set each entry's dp to its distance to its oi
L27 return the routing entries (o1, r1, node 1) and (o2, r2, node 2)
```

Line L2 is the cheap test: by the triangle inequality, $d(q, e.\mathrm{obj}) \ge |d(q, o_p) - d(e.\mathrm{obj}, o_p)|$, so if this lower bound exceeds $r + r(e)$, no object of the ball of $e$ is within $r$ of $q$. KNN is a best-first search: PQ orders the subtrees by the least possible distance $\max(d(q, o) - r(o), 0)$ of an object inside, and $\tau$ is the $k$-th best distance found so far. Line L21 enlarges the radius only as much as needed to cover $x$. SPLIT uses the mM_RAD promotion with the balanced partition of the paper; other policies are in Variants.

## Example

Take $M = 4$, the Euclidean distance, and insert twelve points in the order $a = (1, 1)$, $b = (2, 6)$, $c = (4, 4)$, $d = (5, 1)$, $e = (6, 7)$, $f = (8, 3)$, $g = (9, 8)$, $h = (3, 9)$, $i = (7, 5)$, $j = (0, 4)$, $k = (10, 2)$, $l = (6, 2)$.

| insert | evaluations | what happens |
|---|---|---|
| $a$ to $d$ | 0 | the root leaf fills up: $[a, b, c, d]$ |
| $e$ | 10 | overflow; of the 10 pairs, $(c, d)$ gives the least larger radius: $c$ with $\{c, b, e\}$, $r = 3.6056$, and $d$ with $\{d, a\}$, $r = 4$; the root becomes internal |
| $f$ | 2 | $d(f, d) = 3.6056 \le 4$: into the leaf of $d$ |
| $g$ | 2 | no ball covers it; $d(g, c) - 3.6056 = 2.7975$ is least, so the radius of $c$ grows to 6.4031 |
| $h$ | 12 | into the leaf of $c$, which overflows: $b$ with $\{b, c, h\}$, $r = 3.1623$, and $e$ with $\{e, g\}$, $r = 3.1623$ |
| $i$, $j$, $k$ | 3 each | $i$ to $e$, $j$ to $b$; $k$ is covered by no ball and the radius of $d$ grows to 5.0990 |
| $l$ | 13 | into the leaf of $d$, which overflows: $d$ with $\{d, l, a\}$, $r = 4$, and $f$ with $\{f, k\}$, $r = 2.2361$ |

The final root has four routing entries: $b$ (radius 3.1623) over $\{b, c, h, j\}$, $e$ (3.1623) over $\{e, g, i\}$, $d$ (4) over $\{d, l, a\}$ and $f$ (2.2361) over $\{f, k\}$, each leaf entry with its distance to its routing object.

Range query $q = (9, 3)$, $r = 1.5$. At the root, $d(q, b) = 7.6158 > 1.5 + 3.1623$ and $d(q, e) = 5 > 4.6623$, so both are skipped; $d(q, d) = 4.4721 \le 5.5$ and $d(q, f) = 1 \le 3.7361$, so both are visited. In the leaf of $d$, with $d_{qp} = 4.4721$: $d$ itself has $d_p = 0$ and $|4.4721 - 0| > 1.5$; $l$ has $d_p = 1.4142$ and $|4.4721 - 1.4142| = 3.0579 > 1.5$; both are skipped by line L2 without an evaluation, and $a$, with $d_p = 4$, passes the test and is evaluated at 8.2462. In the leaf of $f$, with $d_{qp} = 1$: $f$ at distance 1 and $k$ at 1.4142 pass and are answers. The result is $\{f, k\}$, after 7 evaluations instead of 12. KNN with $k = 2$ returns $f$ and $k$, also after 7.

## Correctness

**The invariants are kept.** INSERT-AT adds $x$ below a routing entry only after line L20 found $d(x, o) \le r(o)$ or line L21 raised $r(o)$ to $d(x, o)$, so covering holds for every ancestor of the new leaf entry. A split builds new routing entries whose radii are $\max(d(o_i, e) + r(e))$ over their parts, which covers the subtrees by the triangle inequality; the entries above them still cover the same set of objects. Lines L22 and L26 set the parent distances of the entries whose parent changed. Splits only add a level at the root, so all leaves stay at one depth.

**RANGE and KNN are exact.** A subtree is skipped in line L2 or L6 only when $d(q, o) > r + r(o)$ or its lower bound $|d_{qp} - d_p|$ does; then every object $y$ in the ball has $d(q, y) \ge d(q, o) - r(o) > r$. KNN skips a subtree only when its least possible distance exceeds the current $\tau$, which only decreases, and stops when the least $d_{\min}$ in PQ exceeds $\tau$, so no unvisited object can improve $B$. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/) with an oracle for $d$; costs are evaluations of $d$, and node accesses when the nodes are pages. With the balanced partition, every node except the root holds at least $b = \lfloor (M + 1)/2 \rfloor$ entries, as in a B-tree.

| operation | cost | case |
|---|---|---|
| height $h$ | at most $1 + \log_b (n/2)$ levels for $M \ge 3$ | worst, balanced partition, insertions only |
| insert | $M h$ evaluations to descend, plus $\binom{M+1}{2} + 2$ per split, at most one split per level: $O(M^2 h)$ | worst |
| range | at most one evaluation per entry, $O(n)$ | worst |
| k-NN | $O(n)$ evaluations and $O(n \log n)$ time for the priority queue | worst |
| space | $\Theta(n)$ entries, $O(n/b)$ nodes | worst |

The worst case $\Omega(n)$ evaluations for a query holds for every index in this model, by the adversary of the [range query](/similarity-range-query/) page. In practice the cost depends on the overlap of the balls and on the [intrinsic dimension](/intrinsic-dimensionality/): the M-tree has no control over overlap, and in high intrinsic dimension most balls meet the query ball. Ciaccia, Patella and Zezula report that the test of line L2 saves a large share of the evaluations, and that the build makes far fewer evaluations than a static index that compares all pairs.

## Variants

- **Promotion policies.** mM_RAD tries all pairs and minimizes the larger radius; m_RAD minimizes the sum; M_LB_DIST keeps the old routing object and promotes the object farthest from it, using only stored distances; RANDOM and SAMPLING trade quality for speed.
- **Partition policies.** The generalized hyperplane sends each entry to the nearer promoted object and gives smaller balls but no fill guarantee; the balanced partition, used here, guarantees half-full nodes.
- **Bulk loading.** Building from a known set by clustering, top-down, gives better balls than insertions one by one.
- **Slim-tree.** Adds a minimum spanning tree split and the slim-down step, which moves entries to reduce overlap.
- **PM-tree.** Adds a few global pivots, as in [pivot-based indexing](/pivot-based-indexing/), and stores for each ball the interval of its distances to them, which cuts the balls into rings and prunes more.
- **Deletion.** Not part of the original design; it can be done by removing the entry and, when a node becomes too small, reinserting its entries.

## When to use it

Use an M-tree for exact range and nearest neighbor queries in a metric space with an expensive distance when the data changes over time, or does not fit in memory: it grows by insertions, keeps balance, and its nodes are disk pages. For a static set in memory, a [vantage-point tree](/vantage-point-tree/), an [MVP-tree](/mvp-tree/) or a [pivot table](/pivot-based-indexing/) often uses fewer evaluations. For vectors in low dimension, an [R-tree](/r-tree/) or a [k-d tree](/kd-tree/) uses the coordinates and does better.

## Pitfalls

- **Radii that do not cover.** A split must take $r_i = \max(d(o_i, e) + r(e))$ over routing entries, not $\max d(o_i, e)$; the second is right only in leaves. A radius that is too small makes RANGE miss answers.
- **Stale parent distances.** After a split, the entries moved to new nodes have a new parent, and their $d_p$ must be recomputed; the entries promoted into the parent need their distance to the parent's routing object.
- **The test of line L2 at the root.** Root entries have no parent distance, so the test must be skipped there.
- **Overlap.** Insertion order affects the balls. Inserting sorted data, or using the hyperplane partition with small $M$, can give large overlapping balls and queries that visit most of the tree.
- **A distance that is not a metric.** All pruning rules rely on the triangle inequality.

## Implementations

## History

Ciaccia, Patella and Zezula presented the M-tree at VLDB 1997, with the range and nearest neighbor algorithms, the test with stored parent distances, and an experimental comparison of split policies. It followed the B-tree and the R-tree in design, and the [vantage-point tree](/vantage-point-tree/) and the gh-tree in the use of the triangle inequality. The Slim-tree (2000) and the PM-tree (2004) are among its many descendants.

## References
