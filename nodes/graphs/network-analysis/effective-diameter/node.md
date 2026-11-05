---
tag: 5RWQ1K
kind: definition
slug: effective-diameter
name: Effective diameter
aliases:
- 90-percentile effective diameter
area: graphs/network-analysis
level: advanced
summary: Smallest distance within which 90 percent of connected pairs lie.
prereqs: [neighborhood-function, breadth-first-search, eccentricity]
see_also: [neighborhood-function, anf-algorithm, network-diameter-estimation, small-world-network, eccentricity, breadth-first-search, erdos-renyi-model, degree-distribution]
sources:
  - paper: doi:10.1145/1217299.1217301
    title: Jure Leskovec, Jon Kleinberg and Christos Faloutsos, Graph evolution, densification and shrinking diameters, ACM Transactions on Knowledge Discovery from Data 1(1), article 2 (2007)
    locator: Section 3 (the definition of the effective diameter as the 90th percentile of the distances between connected pairs, with linear interpolation, and the observation that it shrinks over time in real networks)
  - paper: doi:10.1145/775047.775059
    title: Christopher R. Palmer, Phillip B. Gibbons and Christos Faloutsos, ANF, a fast and scalable tool for data mining in massive graphs, Proceedings of the 8th ACM SIGKDD Conference (KDD 2002), 81 to 90
    locator: the definitions of the neighbourhood function, the hop plot and the effective diameter
  - paper: doi:10.1145/1963405.1963493
    title: Paolo Boldi, Marco Rosa and Sebastiano Vigna, HyperANF, approximating the neighbourhood function of very large graphs on a budget, Proceedings of the 20th International Conference on World Wide Web (WWW 2011), 625 to 634
    locator: the distance distribution and the effective diameter computed from the estimated neighbourhood function
---

The **effective diameter** of a graph is the smallest distance $h$ such that at least 90 percent of the pairs of vertices that are connected at all are at distance at most $h$. The [diameter](/eccentricity/), the largest distance, is decided by a single far pair and can jump when one long path is added; the effective diameter is a percentile of the whole distance distribution and changes little. It is read from the [neighbourhood function](/neighborhood-function/), which the [ANF algorithm](/anf-algorithm/) and its successors estimate for very large graphs. Leskovec, Kleinberg and Faloutsos used it in 2007 to show that the typical distances in growing real networks shrink over time.

## Definition

Let $G = (V, E)$ be a graph, directed or undirected, without weights, and let $\mathrm{dist}(u, v)$ be the number of arcs on a shortest path from $u$ to $v$, or $\infty$ if $v$ is not reachable from $u$. Let

$$P = \{(u, v) \in V \times V : u \ne v,\ \mathrm{dist}(u, v) < \infty\}$$

be the set of **connected ordered pairs**, and assume $P \ne \emptyset$. For $h \ge 0$, let $g(h)$ be the fraction of pairs in $P$ with $\mathrm{dist}(u, v) \le h$. So $g$ does not decrease, $g(0) = 0$, and $g(h) = 1$ from the largest finite distance on.

The **effective diameter** for the quantile $q \in (0, 1]$, usually $q = 0.9$, is the smallest integer $h$ with $g(h) \ge q$.

Leskovec, Kleinberg and Faloutsos use a **smoothed** value: they join the points $(h, g(h))$ for $h = 0, 1, 2, \ldots$ by straight lines and take the point where this piecewise linear function first reaches $q$. If $h$ is the integer effective diameter, the smoothed value is

$$(h - 1) + \frac{q - g(h-1)}{g(h) - g(h-1)},$$

a real number in $(h - 1, h]$.

Some points of the definition:

- **Disconnected graphs.** Pairs with no path are left out of $P$. The effective diameter of a disconnected graph is therefore a percentile of the finite distances only; it does not say how many pairs are unreachable.
- **Directed graphs.** The pairs are ordered and $\mathrm{dist}$ follows the arcs. For an undirected graph each unordered pair is counted twice, which does not change any fraction.
- **Pairs of a vertex with itself.** Some authors include the $n$ pairs $(v, v)$ at distance 0, as the neighbourhood function $N(h) = \sum_v |\{u : \mathrm{dist}(v, u) \le h\}|$ does. This changes the value slightly, as the example below shows, so the convention should be stated.
- **Weights.** For weighted graphs, the same percentile of the weighted distances can be used, with the interpolation done on the empirical distribution of the distances. The usual definition is for unweighted graphs.
- **Ties.** There are no choices to make: $g$ is a function of the distances.

## Examples and non-examples

Let $G_7$ be the undirected graph with the vertices 0 to 6 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. Breadth-first search from each vertex gives the numbers of ordered pairs at the distances 1, 2, 3 and 4: 18, 10, 10 and 4, so $|P| = 42$ and the diameter is 4.

| $h$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| pairs at distance at most $h$ | 0 | 18 | 28 | 38 | 42 |
| $g(h)$ | 0 | 0.429 | 0.667 | 0.905 | 1 |

The 90 percent mark is $0.9 \cdot 42 = 37.8$ pairs. Since $28 < 37.8 \le 38$, the effective diameter is 3, and the smoothed value is $2 + (37.8 - 28)/(38 - 28) = 2.98$. If the 7 pairs $(v, v)$ are included, the total is 49, the mark is $44.1$, the counts become $7, 25, 35, 45, 49$, and the smoothed value is $2 + (44.1 - 35)/10 = 2.91$; the integer value is still 3.

- **Star.** A star with 10 leaves has 20 ordered pairs at distance 1 and 90 at distance 2. The mark is $0.9 \cdot 110 = 99$, so the effective diameter is 2, equal to the diameter, and the smoothed value is $1 + (99 - 20)/90 \approx 1.88$.
- **Path.** The path with 10 vertices has $2(10 - d)$ ordered pairs at distance $d$ for $d = 1, \ldots, 9$, 90 pairs in all. The mark is 81, reached at $d = 7$ (cumulative 78 at 6 and 84 at 7), so the effective diameter is 7 while the diameter is 9, and the smoothed value is $6 + 3/6 = 6.5$. A long thin graph has its far pairs in the top 10 percent, which the effective diameter ignores.
- **Disconnected.** The disjoint union of a triangle and a path with 4 vertices has 12 connected ordered pairs at distance 1, 4 at distance 2 and 2 at distance 3, 18 in all. The mark is $16.2$, so the effective diameter is 3 and the smoothed value is $2 + 0.2/2 = 2.1$. The 24 pairs across the two parts are ignored.
- **Not a diameter bound.** The effective diameter is at most the diameter of the largest component, and can be much smaller: adding a long path of $k$ vertices to a large dense graph raises the diameter by about $k$ but changes the effective diameter little when the new pairs are a small part of all pairs.
- **Not defined.** A graph without edges has $P = \emptyset$, and the effective diameter is not defined.

In a random graph from the [Erdős-Rényi model](/erdos-renyi-model/) with average degree $c > 1$, most distances in the giant component are close to $\ln n / \ln c$, so the effective diameter grows like $\log n$. Leskovec, Kleinberg and Faloutsos found that in several real networks that grow over time the effective diameter decreases instead, a property not produced by the earlier growth models.

## Related definitions

- [Neighbourhood function](/neighborhood-function/): the counts $N(h)$, from which $g$ and the effective diameter are read; its plot against $h$ is the hop plot.
- [Eccentricity](/eccentricity/) and the diameter: the largest distance from a vertex and in the graph, which the effective diameter replaces by a percentile.
- [Network diameter estimation](/network-diameter-estimation/) and the [ANF algorithm](/anf-algorithm/): ways to estimate the distance distribution of graphs too large for a [breadth-first search](/breadth-first-search/) from every vertex.
- [Small-world network](/small-world-network/): networks with a small typical distance, for which the effective diameter is a standard measure.

## References
