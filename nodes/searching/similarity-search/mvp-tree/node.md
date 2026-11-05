---
tag: WR0RGE
kind: data-structure
slug: mvp-tree
name: Multi-vantage-point tree
aliases:
- MVP-tree
area: searching/similarity-search
level: advanced
summary: A vantage-point tree that uses several vantage points per node to reduce distance computations.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of objects, m: the number of rings per vantage point, k: the leaf capacity, p: the number of path distances kept per object}
  time: {build: O(n log n), range: O(n)}
  space: {total: O(n (p + m^2))}
properties: {deterministic: false, recursive: true}
history:
  year: 1997
  people: [Tolga Bozkaya, Meral Özsoyoglu]
  note: Bozkaya and Özsoyoglu introduced the MVP-tree at SIGMOD 1997 and extended its analysis in ACM Transactions on Database Systems in 1999.
prereqs: [vantage-point-tree, pivot-based-indexing, triangle-inequality]
see_also: [vantage-point-tree, pivot-based-indexing, m-tree, gnat, metric-space-indexing, similarity-range-query]
sources:
  - paper: doi:10.1145/253260.253345
    title: Tolga Bozkaya and Meral Özsoyoglu, Distance-based indexing for high-dimensional metric spaces, Proceedings of the ACM SIGMOD International Conference on Management of Data, 1997
    locator: pages 357 to 368 (Section 4, the mvp-tree with two vantage points per node, m partitions per vantage point, leaves of k objects with their distances to the leaf vantage points and the PATH array of p distances, and the range search)
  - paper: doi:10.1145/328939.328959
    title: Tolga Bozkaya and Meral Özsoyoglu, Indexing large metric spaces for similarity search queries, ACM Transactions on Database Systems 24(3), 1999
    locator: pages 361 to 404 (the extended version with the analysis and the experiments on images and on high-dimensional vectors)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 5, the MVP-tree among the pivot-based tree indexes)
---

A multi-vantage-point tree, or MVP-tree, is a [vantage-point tree](/vantage-point-tree/) for objects of a [metric space](/metric-space/) with two changes that save distance evaluations at query time. Each internal node has two vantage points instead of one: the first splits the objects into $m$ rings by their distance to it, and the second splits each ring into $m$ again, so the node has $m^2$ children while the query pays only 2 evaluations. And each object in a leaf keeps its distances to the leaf's two vantage points and to the first $p$ vantage points on its path from the root, which the search uses as a [pivot table](/pivot-based-indexing/) to exclude objects without computing their distance. Bozkaya and Özsoyoglu introduced it in 1997.

## In plain words

A vantage-point tree uses one landmark per node and splits the objects into "near" and "far". It pays one distance measurement per node on the way down. The MVP-tree asks more from each measurement. It uses two landmarks per node. The first one splits the objects into several bands by their distance to it, and the second splits each band again. So a node has many children, the tree is short, and the query measures only two distances per node.

The distances measured while the tree is built are not thrown away. Each object at the bottom remembers its distances to the landmarks above it. When a query reaches the bottom, it already knows its own distances to the same landmarks. If, for some landmark, the two numbers differ by more than the search radius, the object cannot be an answer, and it is skipped without measuring.

## The abstract type

The MVP-tree is a static [similarity index](/similarity-index/): it is built from a finite set $P$ of $n$ objects of a metric space $(U, d)$, and it answers [range queries](/similarity-range-query/) $R(q, r) = \{x \in P : d(q, x) \le r\}$. It uses only a function that computes $d$, and its cost is counted in evaluations of $d$. Nearest neighbor queries run the range search with a radius that shrinks, as in the vantage-point tree.

## Representation

The parameters are $m \ge 2$, the number of rings per vantage point; $k \ge 1$, the leaf capacity; and $p \ge 0$, the number of path distances kept per object.

- An **internal node** holds two vantage points $v_1$ and $v_2$; $m$ intervals $I_1, \ldots, I_m$, where $I_i$ is the range of $d(\cdot, v_1)$ over the objects of ring $i$; for each $i$, $m$ intervals $J_{i,1}, \ldots, J_{i,m}$ of $d(\cdot, v_2)$ over the objects of subring $(i, j)$; and $m^2$ children, child $(i, j)$ holding subring $(i, j)$.
- A **leaf** holds two vantage points $v_1$ and $v_2$, and at most $k$ entries. An entry is an object $x$ with $D_1(x) = d(x, v_1)$, $D_2(x) = d(x, v_2)$ and $\mathrm{PATH}(x)$, the list of its distances to the vantage points of its ancestors, in the order $v_1, v_2$ from the root down, cut after $p$ values.

Every object of $P$ is a vantage point or an entry of exactly one node. Bozkaya and Özsoyoglu store the $m - 1$ cutoff values of each split; the intervals used here contain the same information and give slightly tighter pruning.

## Operations

```pseudo id=main
BUILD(S)                                     ▷ S a list of objects, each with a PATH list, empty at the root
L1  if |S| ≤ k + 2 then
L2      return a leaf: v1 ← CHOOSE(S), v2 ← the farthest from v1, and for each other x the entry (x, d(x, v1), d(x, v2), PATH(x))
L3  v1 ← CHOOSE(S); for each other x: compute d(x, v1) and append it to PATH(x) if |PATH(x)| < p
L4  split the others by the rank of d(·, v1) into m rings of sizes as equal as possible; record the intervals I1 .. Im
L5  v2 ← the object farthest from v1 in the largest ring, removed from its ring
L6  for each x left: compute d(x, v2), append it to PATH(x) if |PATH(x)| < p; split each ring i by the rank of d(·, v2) into m subrings; record the intervals J(i, j)
L7  return the internal node (v1, v2, I, J, BUILD(subring (i, j)) for all i, j)

RANGE(N, q, r, Q)                            ▷ Q is the list of distances from q to the vantage points above N, cut after p
L8  if N is a leaf then
L9      t1 ← d(q, N.v1), t2 ← d(q, N.v2); report each of v1, v2 within r
L10     for each entry (x, D1, D2, PATH) of N do
L11         if |t1 − D1| > r or |t2 − D2| > r then skip x
L12         if |Q[i] − PATH[i]| > r for some i ≤ |PATH| then skip x
L13         if d(q, x) ≤ r then report x
L14 t1 ← d(q, N.v1), t2 ← d(q, N.v2); report each of v1, v2 within r
L15 Q′ ← Q followed by t1, t2, cut after p
L16 for each ring i with Ii meeting [t1 − r, t1 + r] do
L17     for each subring j with J(i, j) meeting [t2 − r, t2 + r] do
L18         RANGE(child (i, j), q, r, Q′)
```

An interval $[a, b]$ meets $[t - r, t + r]$ when $t + r \ge a$ and $t - r \le b$. Lines L11 and L12 are the pivot filter of the [pivot-based indexing](/pivot-based-indexing/) page, with the leaf vantage points and the path vantage points as pivots: they cost no evaluation. CHOOSE is random in the implementation, or picks an object far from the others.

## Example

Take $m = 2$, $k = 2$ and $p = 2$, the Euclidean distance, and twelve points of the plane: $a = (1, 1)$, $b = (2, 6)$, $c = (4, 4)$, $d = (5, 1)$, $e = (6, 7)$, $f = (8, 3)$, $g = (9, 8)$, $h = (3, 9)$, $i = (7, 5)$, $j = (0, 4)$, $k = (10, 2)$, $l = (6, 2)$. CHOOSE takes the first object of its list.

| step | what happens | result |
|---|---|---|
| root, L3 to L4 | $v_1 = a$; the 11 others by distance to $a$: $j$ 3.1623, $d$ 4, $c$ 4.2426, $b$ and $l$ 5.0990 form ring 1; $i$, $f$, $e$, $h$, $k$, $g$ form ring 2 | $I_1 = [3.1623, 5.0990]$, $I_2 = [7.2111, 10.6301]$ |
| root, L5 | ring 2 is larger; its object farthest from $a$ is $g$, at 10.6301 | $v_2 = g$ |
| root, L6 | by distance to $g$, ring 1 splits into $\{c, l\}$ and $\{b, d, j\}$, ring 2 into $\{e, i\}$ and $\{f, h, k\}$ | $J_{1,1} = [6.4031, 6.7082]$, $J_{1,2} = [7.2801, 9.8489]$, $J_{2,1} = [3.1623, 3.6056]$, $J_{2,2} = [5.0990, 6.0828]$ |
| leaves | $\{c, l\}$: vantage points $c$, $l$, no entry. $\{b, d, j\}$: vantage points $b$, $d$, entry $j$ with $D_1 = 2.8284$, $D_2 = 5.8310$, PATH $= (3.1623, 9.8489)$. $\{e, i\}$: no entry. $\{f, h, k\}$: vantage points $f$, $h$, entry $k$ with $D_1 = 2.2361$, $D_2 = 9.8995$, PATH $= (9.0554, 6.0828)$ | 4 leaves |

The build makes 29 evaluations.

Range query $q = (5, 5)$, $r = 2$. At the root, $t_1 = d(q, a) = 5.6569$ and $t_2 = d(q, g) = 5$, and the query path is $Q' = (5.6569, 5)$. The window $[3.6569, 7.6569]$ meets $I_1$ and $I_2$; the window $[3, 7]$ meets $J_{1,1}$, $J_{2,1}$ and $J_{2,2}$ but not $J_{1,2}$, so the leaf $\{b, d, j\}$ is skipped. In $\{c, l\}$: $c$ at 1.4142 is an answer, $l$ at 3.1623 is not. In $\{e, i\}$: $e$ at 2.2361 is not, $i$ at 2 is. In $\{f, h, k\}$: $t_1 = d(q, f) = 3.6056$ and $t_2 = d(q, h) = 4.4721$; for $k$, $|t_1 - D_1| = 1.3695 \le 2$ but $|t_2 - D_2| = 5.4274 > 2$, so $k$ is skipped without an evaluation. The answer is $\{c, i\}$, after 8 evaluations instead of 12.

## Correctness

**Invariants.** Every object of a subtree has its distance to $v_1$ in the interval of its ring and its distance to $v_2$ in the interval of its subring, because the intervals are taken as the minimum and maximum over the ring and the subring. For every entry $x$ of a leaf, $D_1(x)$ and $D_2(x)$ are its distances to the leaf's vantage points, and $\mathrm{PATH}(x)[i]$ is its distance to the $i$-th vantage point on the path from the root, because line L3 and line L6 append one value per vantage point above it. The query list $Q$ that RANGE passes to a node lists the distances from $q$ to the same vantage points in the same order.

**Range is exact.** A child is skipped only if its ring interval or its subring interval misses the window; if $d(\cdot, v_1)$ lies in $[a, b]$ and $t_1 + r < a$, then every object $x$ of the ring has $d(q, x) \ge d(x, v_1) - d(q, v_1) > r$, and in the same way when $t_1 - r > b$ or for $v_2$. An entry is skipped in line L11 or line L12 only when $|d(q, u) - d(x, u)| > r$ for some vantage point $u$, and then $d(q, x) > r$ by the [triangle inequality](/triangle-inequality/). Every other object is tested exactly in line L9 or line L13, and each object is in one node. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/) with an oracle for $d$. Costs are evaluations of $d$; the time adds the sorting in lines L4 and L6.

| operation | cost | case |
|---|---|---|
| height | at most $\lceil \log_{m^2} n \rceil + 1$ levels | worst, by the splits by rank |
| build | at most $2n$ evaluations per level, $O(n \log_{m^2} n)$ in total; $O(n \log^2 n)$ time with sorting | worst |
| range | $n$ evaluations | worst; 2 per visited node plus the entries that pass the filter |
| space | $O(n (p + m^2))$ | $p$ path distances per object and $2m + 2m^2$ interval ends per internal node |

The worst case $n$ for a query is unavoidable in the evaluation model, by the adversary of the [range query](/similarity-range-query/) page. The gain over the vantage-point tree is in the constant: a binary vp-tree pays one evaluation per node and halves the set; an MVP-tree with $m = 2$ pays 2 evaluations per node and divides it by 4, and $m = 3$ divides it by 9. In the experiments of Bozkaya and Özsoyoglu on high-dimensional vectors and on images, the MVP-tree used notably fewer evaluations than the vp-tree, with most of the gain from the path distances in the leaves.

## Variants

- **More vantage points per node.** The construction generalizes to $v$ vantage points per node with $m^v$ children; two is the case studied in the paper.
- **Larger leaves.** Large $k$ with a large $p$ turns the leaves into small pivot tables, which is where most of the saving happens; the internal nodes then only route the query.
- **Choice of the second vantage point.** Taking $v_2$ far from $v_1$ gives two different views of the data; Bozkaya and Özsoyoglu take the leaf's second vantage point as the object farthest from the first.
- **Nearest neighbor queries.** Run RANGE with $r = \tau$, the distance of the best object so far, visit the children nearest to $q$ first, and shrink $\tau$ when a better object turns up.
- **Dynamic sets.** The tree is static; for insertions and deletions with a balanced paged layout use the [M-tree](/m-tree/).

## When to use it

Use an MVP-tree for exact range queries over a static set in a metric space with an expensive distance, when the memory for $p$ numbers per object is available: images under a perceptual distance, strings under the [edit distance](/edit-distance/), protein structures. Compared with a plain [vantage-point tree](/vantage-point-tree/) it trades $O(np)$ memory and a more complex build for fewer evaluations per query. Compared with a flat [pivot table](/pivot-based-indexing/), it scans only the leaves it reaches, so its extra arithmetic per query is smaller.

## Pitfalls

- **Mismatched path order.** The query list $Q$ and the PATH of each entry must list the distances to the same vantage points in the same order, including the cut after $p$ values. A mismatch makes line L12 compare unrelated numbers and skip true answers.
- **Overwritten distances.** The distances to the internal vantage points are needed in PATH; reusing the same fields for the distances to the leaf vantage points must not erase them.
- **Empty rings.** With few objects or many equal distances, a ring or subring can be empty; its child must be skipped, not visited with an undefined interval.
- **A distance that is not a metric.** Lines L11, L12, L16 and L17 rely on the triangle inequality.
- **Too large a fan-out.** With large $m$ the rings get thin, the window $[t - r, t + r]$ meets many of them, and the search visits most children for 2 evaluations each with little pruning.

## Implementations

## History

Bozkaya and Özsoyoglu presented the MVP-tree at SIGMOD 1997, after studying the vantage-point trees of Uhlmann and Yianilos, and gave the extended version with experiments on images and on high-dimensional vectors in ACM Transactions on Database Systems in 1999. The idea of keeping precomputed distances to a few pivots in the leaves comes from the pivot tables of AESA and LAESA.

## References
