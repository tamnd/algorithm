---
tag: 44VXTB
kind: problem
slug: fixed-radius-near-neighbors
name: Fixed-radius near neighbors
aliases:
- Fixed-radius near-neighbors
- all points within distance r
- all-pairs within distance
- fixed-radius nearest neighbor search
- fixed-radius nearest neighbors
- radius search
- range search in a metric space
- ε-neighbor search
area: searching/similarity-search
level: core
summary: Report all stored points within a fixed distance r of the query.
prereqs: [metric-space, k-nearest-neighbor-search]
see_also: [similarity-range-query, k-nearest-neighbor-search, approximate-nearest-neighbor-search, kd-tree, closest-pair-of-points, dbscan, hash-table, element-distinctness]
sources:
  - paper: doi:10.1016/0020-0190(77)90070-9
    title: Jon Louis Bentley, Donald F. Stanat and E. Hollins Williams Jr., The complexity of finding fixed-radius near neighbors, Information Processing Letters 6(6), 1977
    locator: pages 209 to 212 (the cell method, which hashes points into cells of the radius and checks neighboring cells)
  - paper: doi:10.1145/800061.808735
    title: Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC), 1983
    locator: pages 80 to 86 (the bound by the number of connected components, applied to element distinctness and similar problems)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 2, the range query (q, r) in a metric space)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Orthogonal Range Searching (the k-d tree reports the points in a box in O(n^(1-1/d) + K) time)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, Section 4.5 (range queries with distance-based indexes)
---

The fixed-radius near neighbors problem asks, for a set $P$ of $n$ points in a [metric space](/metric-space/), a radius $r$ and a query $q$, for all points of $P$ within distance $r$ of $q$; the all-pairs form asks for all pairs of points of $P$ within distance $r$ of each other. Unlike [k-nearest neighbor search](/k-nearest-neighbor-search/), the output size $K$ is not fixed, so good bounds have the form $f(n) + O(K)$. In $\mathbb{R}^d$ for fixed $d$, the grid method of Bentley, Stanat and Williams hashes points into cells of side about $r$ and reports all $K$ close pairs in $O(n + K)$ expected time on a real RAM with the floor function. It is the core step of [DBSCAN](/dbscan/), of particle simulations, and of [similarity joins](/all-pairs-similarity-search/).

## In plain words

You have many points and a distance limit. For a query point, you want every stored point that is at most that far from it. In the second form, you want every pair of stored points that are at most that far from each other.

A fast way in the plane is to lay a grid of square cells about as wide as the limit. Two points that are close lie in the same cell or in cells next to each other. So for each point you look only in a few cells near it, and not at all the points.

## Definition

Let $(M, \delta)$ be a metric space, $P \subseteq M$ with $|P| = n$, and $r \ge 0$.

- **Query form.** Preprocess $P$. For a query $q \in M$, report the set $B(q, r) \cap P = \{p \in P : \delta(q, p) \le r\}$. This is also called a range query or [similarity range query](/similarity-range-query/).
- **All-pairs form.** Report the set $E_r(P) = \{\{p, p'\} \subseteq P : p \ne p', \delta(p, p') \le r\}$, with $K = |E_r(P)|$.
- **Decision form.** Decide whether $E_r(P)$ is empty, that is, whether two points lie within $r$.

The graph on $P$ with edge set $E_r(P)$ is the unit disk graph for $r$ in the plane, or the $\varepsilon$-neighborhood graph in machine learning.

## Variants

- **Fixed or varying radius.** In the fixed form $r$ is known at preprocessing time, which allows a grid tuned to $r$. When $r$ changes for each query, the problem is the general metric range query of [metric space indexing](/metric-space-indexing/).
- **Approximate form.** Report every point within $r$ and possibly some points within $cr$, for $c > 1$. LSH families give this with sublinear time per reported point in high dimension.
- **Other distances.** For the $\ell_\infty$ distance the ball is a box, and the problem is orthogonal range searching. For Jaccard or cosine similarity with a threshold, the all-pairs form is [all-pairs similarity search](/all-pairs-similarity-search/).
- **Counting.** Report only $|B(q, r) \cap P|$ or $K$, as in density estimates.

## Examples

- **On a line.** Let $P = \{1, 2, 4, 7, 8\}$ and $r = 1.5$. The close pairs are $\{1, 2\}$ and $\{7, 8\}$, so $K = 2$. For the query $q = 3$, the answer is $\{2, 4\}$. For $r = 0$ the all-pairs form asks for equal points, which is [element distinctness](/element-distinctness/).
- **The grid in the plane.** Let $r = 2$ and use cells of side $s = r/\sqrt 2 \approx 1.414$, so that two points in one cell are always within $r$. The points $(0.5, 0.5)$ and $(1.0, 1.2)$ share cell $(0, 0)$ and form a pair without a distance test. The point $(3.0, 0.4)$ lies in cell $(2, 0)$, two cells away along the first axis; its distance to $(1.0, 1.2)$ is about $2.15 > 2$, so the test of neighboring cells rejects it.

## Known algorithms

**Scan.** Compute $\delta(q, p)$ for every $p$: $O(n)$ distances per query and $O(n^2)$ for all pairs. It is optimal without preprocessing and works in every metric space.

**Grid method (Bentley, Stanat and Williams).** In $\mathbb{R}^d$ with the Euclidean distance, use cells of side $s = r/\sqrt d$, so a cell has diameter $r$. Map each point $x$ to the cell $\lfloor x/s \rfloor$ (coordinate by coordinate) and store the nonempty cells in a [hash table](/hash-table/). A point within $r$ of $x$ lies in a cell whose index differs from that of $x$ by at most $\lceil \sqrt d \rceil$ in each coordinate, so it is among $N_d = (2\lceil \sqrt d \rceil + 1)^d$ cells. For all pairs, compare the points of each cell with those of its neighbor cells.

**Claim.** The grid method reports all $K$ pairs in $O(N_d (n + K))$ expected time.

*Proof.* Every pair within $r$ lies in neighbor cells, so it is found. The work is the number of tested pairs, $\sum |A| |B|$ over pairs of neighbor cells $(A, B)$. By $|A||B| \le (|A|^2 + |B|^2)/2$ and since each cell has fewer than $N_d$ neighbors, this is at most $N_d \sum_A |A|^2$. Each cell has diameter at most $r$, so all $\binom{|A|}{2}$ pairs in it are close, and $\sum_A |A|^2 = \sum_A |A| + 2 \sum_A \binom{|A|}{2} \le n + 2K$. Building the table takes $O(nd)$ expected time. $\square$

For fixed $d$ this is $O(n + K)$. The constant $N_d$ grows like $(2\sqrt d)^d$, so the method suits $d \le 3$ or so; with cells of side $r$ instead, only $3^d$ cells are probed, but a cell may then hold many points that are not close, and the $O(n + K)$ bound is lost.

**Trees.** A [k-d tree](/kd-tree/) answers a query with the bounding box of the ball and then tests distances; for the box itself it reports the $K'$ points inside in $O(n^{1 - 1/d} + K')$ time in the worst case. In general metric spaces, [ball trees](/ball-tree/), [BK-trees](/bk-tree/), [vantage-point trees](/vantage-point-tree/) and [GNAT](/gnat/) prune by the [triangle inequality](/triangle-inequality/), with no worst-case guarantee better than the scan.

**Exact high-dimensional joins.** For sparse vectors and a similarity threshold, [prefix filtering](/prefix-filtering/) and [All-Pairs](/allpairs/) prune pairs that cannot pass the threshold.

## Bounds

- **Output.** Any algorithm needs $\Omega(K)$ time to report $K$ pairs, and $\Omega(n)$ to read the input.
- **Algebraic decision trees.** In the [algebraic decision tree](/algebraic-decision-tree/) model, the decision form for $n$ real numbers needs $\Omega(n \log n)$ time for every fixed $r \ge 0$. *Proof.* Let $W = \{x \in \mathbb{R}^n : |x_i - x_j| > r \text{ for all } i \ne j\}$. Points of $W$ with different orders of the coordinates lie in different connected components, because a path from one order to another must pass through a point with $x_i = x_j$, which is not in $W$. So $W$ has at least $n!$ components, and Ben-Or's theorem gives depth $\Omega(\log n!) = \Omega(n \log n)$. $\square$
- **Escaping the bound.** The grid method beats this bound because it uses the floor function and hashing, which the algebraic decision tree model does not have. With $K = 0$ it decides the decision form in $O(n)$ expected time for fixed $d$, which is consistent: the models differ.
- **High dimension.** For $d = c \log n$ in the Hamming space, the decision form contains [orthogonal vectors](/orthogonal-vectors/) through the reduction on the [k-nearest neighbor search](/k-nearest-neighbor-search/) page, so under the [SETH](/strong-exponential-time-hypothesis/) it has no $O(n^{2-\varepsilon})$ algorithm.

## Reductions

- **To and from k-nearest neighbors.** A query of this problem decides whether the nearest neighbor of $q$ is within $r$. In turn, the $k$ nearest neighbors are found by a search over $r$ with counting queries.
- **Closest pair.** The [closest pair of points](/closest-pair-of-points/) is at distance at most $r$ if and only if $K > 0$; randomized closest pair algorithms use a grid of the current best distance in the same way.
- **Element distinctness.** The case $r = 0$ is [element distinctness](/element-distinctness/), which gives the lower bound above.
- **Similarity joins.** For a similarity $s$ with threshold $t$, the pairs with $s \ge t$ are the pairs within distance $r$ of a related metric, for example $1 - J$ for [Jaccard similarity](/jaccard-similarity/).

## Applications

- **Clustering.** [DBSCAN](/dbscan/) runs one range query of radius $\varepsilon$ for each point.
- **Simulation.** Molecular dynamics and particle methods use cell lists, the grid method, to find all particle pairs within the cutoff radius of the force at each time step.
- **Graph building.** The $\varepsilon$-neighborhood graph, an alternative to the [k-nearest neighbor graph](/k-nearest-neighbor-graph/), is the all-pairs output.
- **Near-duplicate detection.** All pairs of documents with similarity above a threshold, through [all-pairs similarity search](/all-pairs-similarity-search/).

## References
