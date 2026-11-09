---
tag: 6R4SPJ
kind: definition
slug: nearest-neighbor-graph
name: Nearest neighbor graph
aliases:
- k-NN graph
- k-nearest-neighbor graph
- NNG
area: geometry/proximity
level: intro
summary: Directed graph with an edge from each point to each of its k nearest neighbors.
prereqs: [euclidean-distance, directed-graph, functional-graph]
see_also: [all-nearest-neighbors, k-nearest-neighbor-graph, k-nearest-neighbor-graph-construction, proximity-graphs, euclidean-minimum-spanning-tree, relative-neighborhood-graph, delaunay-triangulation, reverse-nearest-neighbor]
sources:
  - paper: doi:10.1007/PL00009293
    title: David Eppstein, Michael S. Paterson and F. Frances Yao, On nearest-neighbor graphs, Discrete and Computational Geometry 17(3), 1997
    locator: Section 1 and Section 2 (the definition of the nearest neighbor graph and the k-nearest neighbor graph, the bounded in-degree, and the structure of the components)
  - paper: doi:10.1007/BF02187718
    title: Pravin M. Vaidya, An O(n log n) algorithm for the all-nearest-neighbors problem, Discrete and Computational Geometry 4(2), 1989
    locator: the whole paper (the k nearest neighbors of every point in O(kn log n) time in fixed dimension)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5 and Chapter 6 (all nearest neighbors from the Voronoi diagram, and the nearest neighbor relation)
---

The nearest neighbor graph of a finite point set $P$ is the [directed graph](/directed-graph/) with an edge from each point to its nearest other point of $P$. The $k$-nearest neighbor graph has an edge from each point to each of its $k$ nearest other points. With distinct distances the first graph is a [functional graph](/functional-graph/) whose cycles all have length 2, and its undirected version is a forest inside the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/). It is the output of the [all nearest neighbors](/all-nearest-neighbors/) problem and the smallest of the [proximity graphs](/proximity-graphs/).

## Definition

Let $P \subset \mathbb{R}^d$ be a finite set of $n \ge 2$ distinct points and $\|p - q\|$ the [Euclidean distance](/euclidean-distance/). For $p \in P$ the **nearest neighbor distance** is $r(p) = \min_{q \in P \setminus \{p\}} \|p - q\|$, and $q \ne p$ is a **nearest neighbor** of $p$ when $\|p - q\| = r(p)$.

The **nearest neighbor graph** $\mathrm{NNG}(P)$ has vertex set $P$ and a directed edge $p \to q$ for each nearest neighbor $q$ of $p$. If ties are broken by a fixed rule so that each point keeps exactly one nearest neighbor $\mathrm{nn}(p)$, the graph has out-degree exactly 1.

For $1 \le k \le n - 1$, order the other points of $P$ by distance from $p$ and break ties by a fixed rule. The **$k$-nearest neighbor graph** $k\text{-NNG}(P)$ has an edge $p \to q$ for each of the first $k$ points $q$ of this order. Without a tie rule, the common convention puts in every $q$ with $\|p - q\|$ at most the $k$-th smallest distance from $p$.

The **undirected** version keeps the edge $\{p, q\}$ when $p \to q$ or $q \to p$. The **mutual** version keeps it only when both edges exist.

**Structure with distinct distances.** Assume that all $\binom{n}{2}$ distances are distinct. Then:

1. *Every cycle of $\mathrm{NNG}(P)$ has length 2.* Each vertex has out-degree 1. On a cycle $p_1 \to p_2 \to \cdots \to p_m \to p_1$ with $m \ge 3$, $p_{i+1}$ chose $p_{i+2}$ over $p_i$, so $\|p_{i+1} - p_{i+2}\| < \|p_i - p_{i+1}\|$ (indices mod $m$). Going once around the cycle gives $\|p_1 - p_2\| < \|p_1 - p_2\|$, a contradiction. So each weakly connected component is a tree with one mutual pair, and the undirected graph is a forest.
2. *Every edge belongs to the Euclidean minimum spanning tree.* The edge from $p$ to $\mathrm{nn}(p)$ is the unique lightest edge across the cut $\{p\}, P \setminus \{p\}$, so by the [cut property](/cut-property/) it is in the minimum spanning tree, which is unique here.
3. *In the plane, the in-degree is at most 5.* If $q_1 \ne q_2$ both have $p$ as nearest neighbor, then $\|q_1 - p\| < \|q_1 - q_2\|$ and $\|q_2 - p\| < \|q_1 - q_2\|$. So $q_1 q_2$ is the strictly longest side of the triangle $q_1 p q_2$, and the angle at $p$ is strictly larger than $60°$. Six or more such points would need six angles of more than $60°$ around $p$, which sum to more than $360°$. Without the assumption of distinct distances the same argument gives angles of at least $60°$ and in-degree at most 6, as at the centre of a regular hexagon.

## Examples and non-examples

- **A small set with a tie.** Take $P = \{(0,0), (1,0), (3,0), (3,2), (6,1), (7,3)\}$, numbered 0 to 5. The squared nearest neighbor distances are $1, 1, 4, 4, 5, 5$. The edges are $0 \to 1$, $1 \to 0$, $3 \to 2$, $4 \to 5$, $5 \to 4$, and point 2 has two nearest neighbors at squared distance 4: point 1 and point 3. With all ties kept, point 2 has out-degree 2. With the rule "smallest index wins", $2 \to 1$, and the components are $\{0, 1, 2, 3\}$ with the mutual pair $\{0, 1\}$, and $\{4, 5\}$.
- **The 2-NN graph of the same set.** The two nearest points are $0: \{1, 2\}$, $1: \{0, 2\}$, $2: \{1, 3\}$, $3: \{2, 1\}$, $4: \{5\}$ and then a tie between $2$ and $3$ at squared distance $10$, and $5: \{4, 3\}$. So $k$-NN graphs have ties at the $k$-th place too, and a library must say how it breaks them.
- **Points on a line with equal gaps.** For $P = \{0, 1, 2, 3\}$ on the $x$-axis, each inner point has two nearest neighbors. Any tie rule gives a different functional graph, so "the" nearest neighbor graph is not defined without a rule.
- **A non-example: the graph is not symmetric.** In the first example $3 \to 2$ but not $2 \to 3$ under the index rule. A $k$-NN graph is a directed graph; its undirected version is a different object.
- **A non-example: it is not connected.** The first example has two components. The [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) is the smallest connected proximity graph; the nearest neighbor graph is only a forest inside it.

## Related definitions

- [All nearest neighbors](/all-nearest-neighbors/): the problem of computing this graph, in $O(n \log n)$ time in fixed dimension.
- [k-nearest neighbor graph](/k-nearest-neighbor-graph/) and its [construction](/k-nearest-neighbor-graph-construction/): the same object as used in machine learning, for large $k$ and high dimension.
- [Reverse nearest neighbor](/reverse-nearest-neighbor/): the points $q$ with $q \to p$, the in-neighbours of $p$ in this graph.
- [Proximity graphs](/proximity-graphs/): with distinct distances, $\mathrm{NNG} \subseteq$ [EMST](/euclidean-minimum-spanning-tree/) $\subseteq$ [relative neighborhood graph](/relative-neighborhood-graph/) $\subseteq$ [Gabriel graph](/gabriel-graph/) $\subseteq$ [Delaunay triangulation](/delaunay-triangulation/).
- [Functional graph](/functional-graph/): a directed graph with out-degree 1, the shape of the graph with a tie rule.

## References
