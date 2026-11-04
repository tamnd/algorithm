---
tag: Q47HS8
kind: problem
slug: spatial-join
name: Spatial join
aliases:
- spatial overlay join
area: data-structures/spatial-structures
level: advanced
summary: Given two sets of spatial objects, report all pairs whose geometries intersect or satisfy a spatial predicate.
prereqs: [minimum-bounding-rectangle, spatial-index]
see_also: [rectangle-intersection-reporting, rectangle-intersection-sweep, r-tree, nested-loop-join, hash-join, sort-merge-join, uniform-grid, z-order-curve]
sources:
  - paper: doi:10.1145/170035.170075
    title: Thomas Brinkhoff, Hans-Peter Kriegel and Bernhard Seeger, Efficient processing of spatial joins using R-trees, Proceedings of ACM SIGMOD 1993, pp. 237 to 246
    locator: the synchronized traversal of two R-trees, the restriction of the search space to the intersection of the two node boxes, and the plane sweep of the entries of two nodes
  - paper: doi:10.1145/233269.233338
    title: Jignesh M. Patel and David J. DeWitt, Partition based spatial-merge join, Proceedings of ACM SIGMOD 1996, pp. 259 to 270
    locator: the partitioning of both inputs by a grid of tiles mapped to partitions, the plane sweep join of each pair of partitions, and the removal of duplicate pairs
  - paper: doi:10.1145/1206049.1206056
    title: Edwin H. Jacox and Hanan Samet, Spatial join techniques, ACM Transactions on Database Systems 32(1), 2007
    locator: the survey of the filter and refine framework, of internal memory joins (nested loop, plane sweep, grids), and of external memory joins with and without indexes
  - paper: "Lars Arge, Octavian Procopiuc, Sridhar Ramaswamy, Torsten Suel and Jeffrey Scott Vitter, Scalable sweeping-based spatial join, Proceedings of the 24th International Conference on Very Large Data Bases (VLDB), 1998, pp. 570 to 581"
    locator: the I/O-optimal rectangle join by distribution sweeping, and the experiments against PBSM and the R-tree join
  - paper: "Jack A. Orenstein, Spatial query processing in an object-oriented database system, Proceedings of ACM SIGMOD 1986, pp. 326 to 336"
    locator: the spatial join by z-order elements, a merge of two sorted lists of z-values
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: the sections on spatial joins and on the plane sweep for rectangle intersection
---

A spatial join takes two sets of spatial objects, $R$ and $S$, and a spatial predicate, and reports every pair $(r, s) \in R \times S$ for which the predicate holds. The usual predicate is *intersects*; others are *contains*, *within distance* $\varepsilon$, and *is a nearest neighbor of*. An example is "every road that crosses a river". It is the join of relational databases with a geometric condition in place of equality, so the hash and sort methods of an [equi-join](/hash-join/) do not apply directly, and the [nested loop](/nested-loop-join/) costs $|R| \cdot |S|$ tests. Practical methods first join the [minimum bounding rectangles](/minimum-bounding-rectangle/) of the objects, a *filter* step, and then test the exact shapes of the candidate pairs, a *refine* step.

## In plain words

You have two maps, one of roads and one of lakes, and you want every road that touches a lake. Testing every road against every lake is slow when each map has a million shapes.

So you work in two steps. First you draw a box around each shape and find the pairs whose boxes touch. Boxes are cheap to compare, and you can sort them, put them in a grid, or put them in a tree, so that most far apart pairs are never compared at all. Then you take only these candidate pairs and check if the real shapes touch.

## Definition

**Input.** Two finite sets $R$ and $S$ of objects in $\mathbb{R}^d$, usually $d = 2$, and a predicate $\theta(r, s)$. For the *intersection join*, the objects are closed sets and $\theta(r, s)$ holds when $r \cap s \ne \emptyset$.

**Output.** The set $J = \{(r, s) \in R \times S : \theta(r, s)\}$, each pair once. Let $n = |R| + |S|$ and $k = |J|$.

**MBR join.** The *filter* problem is the intersection join on the MBRs: report each pair $(r, s)$ with $\operatorname{MBR}(r) \cap \operatorname{MBR}(s) \ne \emptyset$. If $r$ and $s$ meet, so do their MBRs, so the MBR join gives a superset $C \supseteq J$, the *candidates*, and the *refine* step tests each pair of $C$ on the exact shapes. The filter step is a purely combinatorial problem on axis-parallel boxes; the refine step depends on the shapes, for example polygons with many vertices.

## Variants

- **Self-join.** $R = S$: report the pairs of one set that meet, with $r \ne s$ and each unordered pair once. This is [rectangle intersection reporting](/rectangle-intersection-reporting/) when the objects are boxes.
- **Distance join.** $\theta(r, s)$ is $\operatorname{dist}(r, s) \le \varepsilon$. Enlarging every box of $R$ by $\varepsilon$ reduces the filter step to an intersection join. For points this is the [fixed radius near neighbors](/fixed-radius-near-neighbors/) problem on two sets.
- **k nearest neighbor join and closest pairs.** Report, for each $r$, the $k$ nearest $s$, or report the $k$ closest pairs of $R \times S$. These are not joins with a fixed predicate, and are solved by best-first searches over two indexes.
- **Containment and topological predicates.** "$r$ contains $s$", "$r$ touches $s$", and the predicates of the DE-9IM model. The filter step still uses the MBRs, with tests suited to each predicate: if $r$ contains $s$, the MBR of $r$ contains the MBR of $s$.
- **Multiway join.** Three or more sets, for example road, river and town. It is computed as a sequence of two-way joins or by a synchronized traversal of several indexes.
- **With or without indexes.** Both sets have an index (often [R-trees](/r-tree/)), one set has an index, or neither. The best method differs in each case.
- **Internal or external memory.** If the sets do not fit in memory, the cost is counted in page reads, in the [external memory model](/external-memory-model/).

## Examples

**Roads and lakes.** Take these boxes, as $[x_1, x_2] \times [y_1, y_2]$:

| road | box | lake | box |
|---|---|---|---|
| $r_1$ | $[0, 4] \times [0, 1]$ | $s_1$ | $[1, 3] \times [0, 3]$ |
| $r_2$ | $[3, 5] \times [2, 6]$ | $s_2$ | $[4, 7] \times [2, 4]$ |
| $r_3$ | $[6, 9] \times [1, 3]$ | $s_3$ | $[0, 2] \times [6, 7]$ |
| $r_4$ | $[1, 2] \times [5, 8]$ | $s_4$ | $[8, 9] \times [7, 9]$ |

The MBR join is $\{(r_1, s_1), (r_2, s_1), (r_2, s_2), (r_3, s_2), (r_4, s_3)\}$, 5 of the 16 pairs. The nested loop makes 16 box tests to find them.

**Plane sweep.** Sort the 8 boxes by $x_1$: $r_1$ (0), $s_3$ (0), $r_4$ (1), $s_1$ (1), $r_2$ (3), $s_2$ (4), $r_3$ (6), $s_4$ (8). Sweep a vertical line from left to right and keep, for each set, the *active* boxes, whose $x$ range contains the line. When a box starts, remove the active boxes of the other set that ended before it, and test the $y$ ranges against those that remain.

| starts | active of the other set | $y$ tests | pairs found |
|---|---|---|---|
| $r_1$ | none | 0 | |
| $s_3$ | $r_1$ | 1 | |
| $r_4$ | $s_3$ | 1 | $(r_4, s_3)$ |
| $s_1$ | $r_1$, $r_4$ | 2 | $(r_1, s_1)$ |
| $r_2$ | $s_1$ ($s_3$ ended at 2) | 1 | $(r_2, s_1)$ |
| $s_2$ | $r_1$, $r_2$ ($r_4$ ended at 2) | 2 | $(r_2, s_2)$ |
| $r_3$ | $s_2$ ($s_1$ ended at 3) | 1 | $(r_3, s_2)$ |
| $s_4$ | $r_3$ ($r_2$ ended at 5) | 1 | |

The sweep makes 9 tests instead of 16. Each pair that meets is found when the box that starts later starts, since then the other box is active and their $y$ ranges meet.

**Grid partitioning.** Use a grid of $5 \times 5$ cells and put each box in every cell it meets. Cell $(0, 0)$, for $[0, 5) \times [0, 5)$, gets $r_1, r_2, s_1, s_2$; cell $(0, 1)$ gets $r_2, r_4, s_3$; cell $(1, 0)$ gets $r_2, r_3, s_2$; cell $(1, 1)$ gets $r_2, s_4$. Join each cell by itself. The pair $(r_2, s_2)$ is found in cells $(0, 0)$ and $(1, 0)$. To report it once, report a pair only in the cell that holds the lower left corner of the intersection of the two boxes: for $(r_2, s_2)$ that corner is $(4, 2)$, in cell $(0, 0)$. This is the duplicate rule of [uniform grid](/uniform-grid/) and [spatial hashing](/spatial-hashing/) queries.

## Known algorithms

| algorithm | time or I/O | setting |
|---|---|---|
| [nested loop join](/nested-loop-join/) | $O(\lvert R \rvert \lvert S \rvert)$ | any predicate, no index |
| index nested loop | $\lvert R \rvert$ window queries on an index of $S$ | one index |
| plane sweep with sorted lists | $O(n \log n + t)$, $t$ tests (up to $\lvert R \rvert \lvert S \rvert$) | internal memory |
| plane sweep with an [interval tree](/interval-tree/) | $O(n \log n + k)$ | internal memory, boxes in the plane |
| R-tree synchronized traversal (Brinkhoff, Kriegel and Seeger) | no worst-case bound beyond $O(\lvert R \rvert \lvert S \rvert)$ | two R-trees |
| partition based spatial merge join, PBSM (Patel and DeWitt) | no worst-case bound; linear I/O in practice | no index |
| z-order merge (Orenstein) | a merge of two sorted lists of z-values | no index, or B-trees on z-values |
| distribution sweeping (Arge and others) | $O(\frac{n}{B} \log_{M/B} \frac{n}{B} + \frac{k}{B})$ I/Os | external memory |

**Plane sweep.** Sorting by $x_1$ and testing the $y$ ranges against the active boxes of the other set is the method of the example. With the active boxes in lists it is simple and fast on real data; with the active $y$ intervals in an interval tree, each start finds its pairs in $O(\log n + \text{output})$, which gives the optimal bound. See [rectangle intersection by sweep](/rectangle-intersection-sweep/).

**Synchronized R-tree traversal.** If both sets have R-trees, join the two roots: for each pair of entries, one from each node, whose boxes meet, join the two children, down to the leaves. Brinkhoff, Kriegel and Seeger added two refinements: only entries that meet the intersection of the two node boxes can take part, and the pairs of entries of two nodes are found by a plane sweep, not by a nested loop. They also order the page reads to reduce buffer misses.

**Partitioning.** Without indexes, partition both sets in the same way and join the parts. PBSM divides space into many tiles of a grid, maps the tiles to a few partitions so that each partition fits in memory, writes each object to every partition it meets, and joins each pair of partitions by a plane sweep, with duplicates removed. Spatial hash joins and the [z-order](/z-order-curve/) merge of Orenstein are other partition methods; the latter turns the join into a merge of two lists sorted by z-value, as in a [sort merge join](/sort-merge-join/).

## Bounds

**Output.** Any algorithm must write the $k$ pairs, and $k$ can be as large as $|R| \cdot |S|$, for example when all boxes contain one point. So output-sensitive bounds are the goal.

**Lower bound $\Omega(n \log n + k)$.** In the algebraic decision tree model, deciding whether two sets of $n/2$ real numbers are disjoint takes $\Omega(n \log n)$ comparisons, by Ben-Or's theorem: the set of disjoint inputs has $\Omega((n/2)!^2)$ connected parts. Map each number to the box $[x, x] \times [0, 0]$. The join is empty if and only if the two sets are disjoint, so a join algorithm decides set disjointness, and needs $\Omega(n \log n)$ time. Adding the $k$ of the output gives $\Omega(n \log n + k)$.

**Upper bound $O(n \log n + k)$ in the plane.** The plane sweep with an interval tree (or a segment tree) of the active $y$ intervals, one tree for each set, meets the lower bound. In $d$ dimensions, rectangle intersection reporting takes $O(n \log^{d-1} n + k)$ time with sweeps over range or segment trees.

**External memory.** With memory of $M$ items and pages of $B$, the sort bound $\Theta(\frac{n}{B} \log_{M/B} \frac{n}{B})$ plus $k/B$ to write the output is optimal for the rectangle join, and distribution sweeping attains it, as shown by Arge and others. The R-tree join and PBSM have no such guarantee: an object that meets many tiles is copied many times, and an R-tree with much overlap compares many node pairs.

## Reductions

- **To rectangle intersection reporting.** The MBR join of $R$ and $S$ is the bichromatic case of [rectangle intersection reporting](/rectangle-intersection-reporting/): give each box a color, and report only pairs of different colors. Any algorithm for the self-join gives one for the join, at the cost of the pairs of one color.
- **From set disjointness.** As in the lower bound, which shows that the join is at least as hard as sorting.
- **Distance join to intersection join.** Enlarge each box of $R$ by $\varepsilon$ in every direction; then two objects within distance $\varepsilon$ have boxes that meet.
- **To a one-dimensional join.** With a space filling curve, each box is covered by a few cells of the [z-order curve](/z-order-curve/), and two boxes can meet only if one cell is a prefix of the other. The join becomes a merge of sorted lists of cell keys, which a relational system can run with its own sort merge join.
- **To many small joins.** Partitioning by a grid or by a [quadtree](/quadtree/) splits the join into independent joins of the parts, which is how parallel systems run it.

## Applications

Spatial databases and geographic information systems run spatial joins for map overlay, for example soil types against land parcels, and for queries such as "the towns within 10 km of a river". PostGIS and other systems compute a join with an index nested loop or a synchronized traversal of R-trees on the MBRs, followed by the exact test. Collision detection in games and physics engines solves a self-join of moving objects in each frame, with a sweep and prune on one axis, a [uniform grid](/uniform-grid/) or [spatial hashing](/spatial-hashing/). Large scale systems such as those built on MapReduce partition the space by a grid and join each part on a different machine, as PBSM does on one machine.

## References
