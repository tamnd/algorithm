---
tag: 8M3GQ1
kind: definition
slug: metric-space
name: Metric space
aliases:
- metric
area: searching/similarity-search
level: intro
summary: A set with a distance function that is non-negative, symmetric, zero only on equal points, and satisfies the triangle inequality.
prereqs: [euclidean-distance]
see_also: [triangle-inequality, metric-space-indexing, similarity-range-query, nearest-neighbor-search, ultrametric, intrinsic-dimensionality, edit-distance, jaccard-similarity]
sources:
  - book: isbn:9780131816299
    title: James R. Munkres, Topology, second edition, Prentice Hall, 2000
    locator: Chapter 2, Section 20, The Metric Topology (the definition of a metric, the balls, and the metrics of R^n)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321, Section 2 (the metric axioms, the range query and the nearest neighbor query, and the examples of metric spaces used in search)
  - book: isbn:9780387291468
    title: Pavel Zezula, Giuseppe Amato, Vlastislav Dohnal and Michal Batko, Similarity Search, The Metric Space Approach, Springer, 2006
    locator: Chapter 1, Foundations of Metric Space Searching (the metric postulates, the variants pseudo-metric, quasi-metric, semi-metric and super-metric, and the distance functions such as Minkowski, edit and Jaccard)
---

A metric space is a set $M$ together with a distance function $d : M \times M \to \mathbb{R}$ that is zero exactly on equal points, symmetric, and obeys the [triangle inequality](/triangle-inequality/). The plane with the [Euclidean distance](/euclidean-distance/) is the model case, but strings with the [edit distance](/edit-distance/), sets with the [Jaccard distance](/jaccard-similarity/) and the vertices of a graph with the [shortest path](/shortest-path/) distance are metric spaces too. Similarity search in a metric space uses only the distance function and its axioms, so one index, for example a [vantage-point tree](/vantage-point-tree/), works for all of them.

## Definition

A **metric** on a set $M$ is a function $d : M \times M \to \mathbb{R}$ such that for all $x, y, z \in M$:

$$
\begin{aligned}
&(\text{M1}) \quad d(x, y) = 0 \iff x = y && \text{(identity of indiscernibles)}\\
&(\text{M2}) \quad d(x, y) = d(y, x) && \text{(symmetry)}\\
&(\text{M3}) \quad d(x, z) \le d(x, y) + d(y, z) && \text{(triangle inequality)}
\end{aligned}
$$

The pair $(M, d)$ is a **metric space**. Many books also list non-negativity, $d(x, y) \ge 0$, as an axiom. It follows from the three above: by (M1), (M3) with $z = x$ and (M2), $0 = d(x, x) \le d(x, y) + d(y, x) = 2\, d(x, y)$.

The **closed ball** of center $q \in M$ and radius $r \ge 0$ is $B(q, r) = \{x \in M : d(q, x) \le r\}$. The **diameter** of a nonempty set $S \subseteq M$ is $\sup_{x, y \in S} d(x, y)$. Every subset $S \subseteq M$ with the restriction of $d$ is again a metric space. This is the setting of search: the data set $P$ is a finite subset of a larger space $M$ that also holds the queries.

**Weaker axioms.** Each axiom can be dropped, and the result has a name.

- A **pseudometric** keeps (M2) and (M3) but allows $d(x, y) = 0$ for $x \ne y$. Grouping the points at distance 0 gives a metric on the groups.
- A **quasimetric** keeps (M1) and (M3) but not (M2). A road network with one-way streets is an example.
- A **semimetric** keeps (M1) and (M2) but not (M3). Search indexes cannot prune with it.
- An **ultrametric** is a metric with the stronger rule $d(x, z) \le \max(d(x, y), d(y, z))$. See [ultrametric](/ultrametric/).

**In the computer.** A search algorithm in a general metric space treats $d$ as a black box. It cannot add points, take averages or look at coordinates. Its cost is counted as the number of evaluations of $d$, because one evaluation, for example an edit distance between two long strings, often costs much more than the rest of the work.

## Examples and non-examples

**The $\ell_p$ distances on $\mathbb{R}^k$.** For $p \ge 1$, $d_p(x, y) = (\sum_{i=1}^{k} |x_i - y_i|^p)^{1/p}$, and $d_\infty(x, y) = \max_i |x_i - y_i|$. The triangle inequality for $d_p$ is the Minkowski inequality. Take $x = (0, 0)$, $y = (3, 4)$ and $z = (6, 0)$.

| distance | $d(x, y)$ | $d(y, z)$ | $d(x, z)$ | $d(x, y) + d(y, z)$ |
|---|---|---|---|---|
| $d_1$ (Manhattan) | 7 | 7 | 6 | 14 |
| $d_2$ (Euclidean) | 5 | 5 | 6 | 10 |
| $d_\infty$ (Chebyshev) | 4 | 4 | 6 | 8 |

The three metrics disagree on which pair is closest: under $d_\infty$ the pair $x, y$ is closer than $x, z$, and under $d_1$ it is farther. A nearest neighbor answer depends on the metric.

**Strings.** The [Hamming distance](/hamming-distance/) between two strings of the same length counts the positions where they differ: "karolin" and "kathrin" are at distance 3. The [edit distance](/edit-distance/) with unit costs for insertion, deletion and substitution is a metric on all strings: "kitten" and "sitting" are at distance 3. Each edit operation has an inverse of the same cost, which gives (M2), and two edit sequences in a row give (M3).

**Sets.** The Jaccard distance $1 - |A \cap B| / |A \cup B|$ is a metric on finite sets. The page [Jaccard similarity](/jaccard-similarity/) proves it.

**Graphs.** In a connected undirected graph with positive edge weights, the length of a shortest path is a metric on the vertices. Positive weights give (M1), an undirected graph gives (M2), and joining a shortest path from $x$ to $y$ with one from $y$ to $z$ gives a path from $x$ to $z$, which gives (M3). On a weighted tree this is a [tree metric](/tree-metric/).

**The discrete metric.** $d(x, y) = 1$ for $x \ne y$ and $d(x, x) = 0$ is a metric on any set. Every ball of radius less than 1 holds only its center, so no index can prune: this is the worst case for metric search.

**Angles.** For nonzero vectors, the angle $\theta(x, y) = \arccos(x \cdot y / (\lVert x \rVert \lVert y \rVert))$ is a pseudometric: it is 0 for $x$ and $2x$. On the unit sphere it is a metric, the geodesic distance.

**Non-example: the squared Euclidean distance.** On the line, with $x = 0$, $y = 1$ and $z = 2$, $d_2(x, z)^2 = 4$ but $d_2(x, y)^2 + d_2(y, z)^2 = 2$. So (M3) fails. Algorithms that work with squared distances to save a square root must take the root before they use the triangle inequality.

**Non-example: $\ell_p$ with $0 < p < 1$.** With $p = 1/2$, $x = (0, 0)$, $y = (1, 0)$ and $z = (1, 1)$, the formula gives $d(x, y) = d(y, z) = 1$ and $d(x, z) = (1 + 1)^2 = 4 > 2$.

**Non-example: the cosine distance.** $1 - \cos\theta$ breaks (M3). For three unit vectors at angles 0, 45 and 90 degrees, the outer pair is at $1 - \cos 90^\circ = 1$, and the two inner pairs sum to $2(1 - \cos 45^\circ) \approx 0.5858$. The angle $\theta$ itself, or the Euclidean distance $\sqrt{2 - 2\cos\theta}$ between unit vectors, is a metric. See [cosine similarity](/cosine-similarity/).

**Non-example: the Kullback-Leibler divergence.** For the distributions $P = (0.5, 0.5)$ and $Q = (0.9, 0.1)$, $D(P \| Q) \approx 0.5108$ and $D(Q \| P) \approx 0.3681$ (natural logarithm). It is not symmetric.

**Non-example: the inner product.** A similarity such as $x \cdot y$ is not a distance at all: $x \cdot x$ is not the largest value of $x \cdot y$ when $y$ is a longer vector in the same direction. This is why [maximum inner product search](/maximum-inner-product-search/) needs its own methods.

## Related definitions

- **[Triangle inequality](/triangle-inequality/)**: the axiom (M3) and its consequence $|d(x, z) - d(y, z)| \le d(x, y)$, which gives every lower bound that a metric index uses to prune.
- **[Metric space indexing](/metric-space-indexing/)**: data structures that answer queries in $(M, d)$ with few evaluations of $d$.
- **[Similarity range query](/similarity-range-query/)** and **[nearest neighbor search](/nearest-neighbor-search/)**: report $P \cap B(q, r)$, or a point of $P$ at the least distance from $q$.
- **[Intrinsic dimensionality](/intrinsic-dimensionality/)**: measures of how many dimensions a finite metric space behaves as if it had, which decide how well metric indexes work.
- **[Ultrametric](/ultrametric/)** and **[tree metric](/tree-metric/)**: special metrics with more structure, from hierarchical clustering and from phylogenetics.
- **[Hausdorff distance](/hausdorff-distance/)**: a metric on the nonempty compact subsets of a metric space.
- **[Metric tree embedding](/metric-tree-embedding/)**: maps a finite metric space into a tree metric with small expected distortion.

## References
