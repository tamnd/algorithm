---
tag: 2RGWRA
kind: problem
slug: nearest-neighbor-search
name: Nearest neighbor search
aliases:
- NN search
- closest point query
- post-office problem
area: searching/similarity-search
level: intro
summary: Given a set of points and a query point, find the point closest to the query.
prereqs: [metric-space, euclidean-distance]
see_also: [k-nearest-neighbor-search, brute-force-nearest-neighbor-search, voronoi-diagram, kd-tree-nearest-neighbor-search, approximate-nearest-neighbor-search, similarity-index, locality-sensitive-hashing, post-office-problem]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.5, Retrieval on Secondary Keys (the post-office problem)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 7, Voronoi Diagrams (the post office problem; the diagram of n sites has O(n) size and is built in O(n log n) time) and Chapter 6, Point Location (O(log n) expected query time with O(n) expected space)
  - paper: doi:10.1145/293347.293348
    title: Sunil Arya, David M. Mount, Nathan S. Netanyahu, Ruth Silverman and Angela Y. Wu, An optimal algorithm for approximate nearest neighbor searching in fixed dimensions, Journal of the ACM 45(6), 1998
    locator: pages 891 to 923 (the balanced box-decomposition tree, with O(dn log n) preprocessing, O(dn) space and O(c log n) query time for a factor 1 + ε, where c depends on d and ε)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 2, the nearest neighbor query in a metric space and the cost model in distance evaluations)
  - paper: doi:10.4086/toc.2012.v008a014
    title: Sariel Har-Peled, Piotr Indyk and Rajeev Motwani, Approximate nearest neighbor, towards removing the curse of dimensionality, Theory of Computing 8, 2012
    locator: pages 321 to 350 (the reduction of c-approximate nearest neighbor to the approximate near neighbor decision problem, and locality-sensitive hashing)
---

Nearest neighbor search asks, for a finite set $P$ of $n$ points in a [metric space](/metric-space/) and a query point $q$, for a point of $P$ at the least distance from $q$. It is the case $k = 1$ of [k-nearest neighbor search](/k-nearest-neighbor-search/), and Knuth calls it the [post-office problem](/post-office-problem/). A scan solves it with $n$ distance evaluations; in the plane a [Voronoi diagram](/voronoi-diagram/) with point location answers in $O(\log n)$ time; in high dimensions no exact method is much faster than the scan, so large systems solve the [approximate](/approximate-nearest-neighbor-search/) problem.

## In plain words

A town has a few post offices. A person at some house wants to know which post office is the closest. The simple way is to measure the distance to every post office and take the smallest. When many people ask, it pays to prepare a map that cuts the town into areas, one for each post office, such that every house in an area is closest to that area's office. Then each question is only "in which area is this house?".

The same question appears with other kinds of points: the most similar photo, the closest word to a misspelled word, the closest color in a small palette. With many numbers per point, good maps become too large, and fast methods accept an answer that is almost the closest.

## Definition

**Input.** A metric space $(M, d)$, a finite nonempty set $P \subseteq M$ of $n$ points, and a query $q \in M$.

**Output.** A point $p^* \in P$ with

$$d(q, p^*) = \min_{p \in P} d(q, p).$$

The value $d^*(q) = d(q, p^*)$ is unique; the point is not unique when several points share the least distance, and then any of them is correct.

**Data structure setting.** $P$ is given first and preprocessed into an index. Queries arrive one at a time. The costs are the preprocessing time, the space and the query time. In a general metric space the cost is often counted in evaluations of $d$; in $\mathbb{R}^k$ it is time on the [real RAM](/real-ram/), and it depends on both $n$ and $k$.

## Variants

- **$k$ nearest neighbors.** Return the $k$ closest points. See [k-nearest neighbor search](/k-nearest-neighbor-search/).
- **$c$-approximate nearest neighbor.** For a fixed $c > 1$, return any $p \in P$ with $d(q, p) \le c \cdot d^*(q)$. See [c-approximate nearest neighbor](/c-approximate-nearest-neighbor/) and [approximate nearest neighbor search](/approximate-nearest-neighbor-search/).
- **$r$-near neighbor (decision form).** For a fixed radius $r$, return a point $p$ with $d(q, p) \le r$ if one exists, and report "none" otherwise. The *$(r, c)$-near neighbor* problem relaxes it: if some point is within $r$, return a point within $cr$; otherwise it may return anything within $cr$ or "none".
- **Range query.** Report every point within distance $r$. See [similarity range query](/similarity-range-query/) and [fixed-radius near neighbors](/fixed-radius-near-neighbors/).
- **All nearest neighbors.** Find the nearest neighbor of every point of $P$ among the others. See [all nearest neighbors](/all-nearest-neighbors/) and the [nearest neighbor graph](/nearest-neighbor-graph/).
- **Reverse nearest neighbors.** Find the points of $P$ whose nearest neighbor is $q$. See [reverse nearest neighbor search](/reverse-nearest-neighbor-search/).
- **Largest similarity.** With a similarity instead of a distance, such as the inner product, find the most similar point. See [maximum inner product search](/maximum-inner-product-search/).

## Examples

Let $P = \{(0,0), (4,0), (2,3), (5,4), (1,5)\}$ in the plane with the Euclidean distance.

| query | distances to (0,0), (4,0), (2,3), (5,4), (1,5) | nearest | $d^*$ |
|---|---|---|---|
| $(3, 1)$ | 3.1623, 1.4142, 2.2361, 3.6056, 4.4721 | (4,0) | 1.4142 |
| $(2, 2)$ | 2.8284, 2.8284, 1, 3.6056, 3.1623 | (2,3) | 1 |

- For $q = (3, 1)$ and $c = 2$, the 2-approximate answers are the points within $2 \times 1.4142 = 2.8284$: both $(4,0)$ and $(2,3)$ are correct.
- For $q = (3, 1)$ and $r = 2$, the $r$-near neighbor answer is $(4,0)$, the only point within 2. For $r = 1$ the answer is "none".
- On the line, with $P = \{2, 5, 9, 14\}$ sorted and $q = 10$, [binary search](/binary-search/) finds that $q$ lies between 9 and 14, and the nearer of the two, 9, is the answer. On the line the nearest point is always one of the two neighbors of $q$ in sorted order.

## Known algorithms

- **[Brute-force nearest neighbor search](/brute-force-nearest-neighbor-search/).** $n$ distance evaluations, $O(nk)$ time in $\mathbb{R}^k$, no preprocessing. It works in every metric space.
- **One dimension.** Sort $P$ in $O(n \log n)$ time; then a query takes $O(\log n)$ time by binary search, as in the example.
- **The plane.** Build the [Voronoi diagram](/voronoi-diagram/) of $P$ in $O(n \log n)$ time; it has $O(n)$ size. A [planar point location](/planar-point-location/) structure on it, such as [Kirkpatrick's](/kirkpatrick-point-location/) or a [trapezoidal map](/trapezoidal-map/), answers a query in $O(\log n)$ time, worst case for Kirkpatrick and expected for the randomized trapezoidal map, with $O(n)$ space.
- **Fixed dimension $k \ge 3$.** The same approach works in principle, but the Voronoi diagram of $n$ points in $\mathbb{R}^k$ can have $\Theta(n^{\lceil k/2 \rceil})$ faces, by the [Voronoi complexity theorem](/voronoi-complexity-theorem/), so the space grows quickly with $k$.
- **Trees with pruning.** The [k-d tree](/kd-tree/) with [branch and bound](/kd-tree-nearest-neighbor-search/), and metric trees such as the [vantage-point tree](/vantage-point-tree/), the [M-tree](/m-tree/), the [ball tree](/ball-tree/) and the [cover tree](/cover-tree/). They prune with the [triangle inequality](/triangle-inequality/). Their worst case is $\Theta(n)$ per query, and they are fast when the dimension, or the [intrinsic dimensionality](/intrinsic-dimensionality/), is low.
- **Approximate, fixed dimension.** Arya, Mount, Netanyahu, Silverman and Wu build a balanced box-decomposition tree in $O(kn \log n)$ time and $O(kn)$ space. It returns a $(1 + \varepsilon)$-approximate nearest neighbor, deterministically, in $O(c_{k,\varepsilon} \log n)$ time, where $c_{k,\varepsilon}$ depends only on $k$ and $\varepsilon$ and grows exponentially in $k$.
- **Approximate, high dimension.** [Locality-sensitive hashing](/locality-sensitive-hashing/) solves the $(r, c)$-near neighbor problem with $O(n^{\rho})$ distance evaluations per query, for some $\rho < 1$ that depends on $c$ and the metric, and a constant success probability. Graph indexes such as [HNSW](/hnsw/) and [navigable small world graphs](/navigable-small-world/) are fast in practice but have no worst-case guarantee.

## Bounds

**Without preprocessing.** Each exact algorithm evaluates the distance to all $n$ points on some input: a point that is not examined could be equal to $q$. So the scan is optimal, with $\Theta(n)$ distance evaluations.

**A general metric space.** Even with unlimited preprocessing, an exact or $c$-approximate query needs $n$ distance evaluations in the worst case when $d$ is a black box. The adversary proof is on the page [similarity index](/similarity-index/). Fast exact queries need more structure, such as coordinates or a low intrinsic dimension.

**With preprocessing in $\mathbb{R}^k$.** A query needs $\Omega(\log n)$ time in a decision tree model with tests of bounded fan-in, since the query $q = p$ must reach a leaf that names $p$, for each of the $n$ points. In one dimension and in the plane, the methods above meet this bound with $O(n)$ space.

**High dimensions.** Under the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), no algorithm answers $n$ exact queries on $n$ points of $\{0, 1\}^k$ with the [Hamming distance](/hamming-distance/), for $k = c \log n$, in total time $O(n^{2 - \varepsilon})$, preprocessing included. The reduction from [orthogonal vectors](/orthogonal-vectors/) is on the page [k-nearest neighbor search](/k-nearest-neighbor-search/), and it uses only $k = 1$.

## Reductions

- **Exact search to the decision form.** Let the distances be integers in $\{0, 1, \ldots, D\}$, as for the Hamming or the edit distance. The predicate "some point lies within $r$" is monotone in $r$: true for $r \ge d^*(q)$ and false for $r < d^*(q)$. So a binary search over $r$ finds $d^*(q)$, and a point at that distance, with $\lceil \lg (D + 1) \rceil + 1$ queries to $r$-near neighbor structures built for each $r \in \{0, \ldots, D\}$.
- **Approximate search to the decision form.** With $(r, c)$-near neighbor structures for the radii $r_0, c\,r_0, c^2 r_0, \ldots$, the first radius at which a structure returns a point gives a $c^2$-approximate answer, provided $d^*(q) \ge r_0$ and the largest radius is at least $d^*(q)$: if the first success is at radius $c^i r_0$ with $i \ge 1$, the structure at $c^{i-1} r_0$ reported "none", so $d^*(q) > c^{i-1} r_0$, and the answer is within $c \cdot c^i r_0 < c^2 d^*(q)$. Har-Peled, Indyk and Motwani remove the dependence on the ratio of the largest to the smallest distance with only polylogarithmic overhead.
- **Closest pair.** The [closest pair of points](/closest-pair-of-points/) is the shortest edge between a point and its nearest neighbor among the others, so it reduces to [all nearest neighbors](/all-nearest-neighbors/).
- **Inner products.** [Maximum inner product search](/maximum-inner-product-search/) reduces to nearest neighbor search by adding one coordinate to each point, so that all points have the same norm.

## Applications

- **Classification.** The 1-nearest neighbor rule labels a new example with the label of the closest training example; see [k-nearest neighbors](/k-nearest-neighbors/).
- **Quantization and compression.** [Vector quantization](/vector-quantization/) encodes each vector by its nearest codeword, and color quantization maps each pixel to the nearest palette color.
- **Heuristics.** The [nearest neighbor heuristic for the TSP](/nearest-neighbor-tsp/) moves to the nearest unvisited city at each step.
- **Retrieval.** Find the closest document, image or song to a query by the distance between embedding vectors.
- **Spelling and record linkage.** Find the closest dictionary word to a misspelled word under the [edit distance](/edit-distance/).

## References
