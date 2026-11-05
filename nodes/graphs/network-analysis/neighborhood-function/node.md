---
tag: 92DX1P
kind: definition
slug: neighborhood-function
name: Neighbourhood function
aliases:
- hop plot
area: graphs/network-analysis
level: advanced
summary: For each h, the number of node pairs within distance h.
prereqs: [graph, shortest-path, breadth-first-search]
see_also: [effective-diameter, anf-algorithm, network-diameter-estimation, eccentricity, harmonic-centrality, small-world-network, flajolet-martin-sketch, all-pairs-shortest-paths]
sources:
  - paper: doi:10.1145/775047.775059
    title: Christopher R. Palmer, Phillip B. Gibbons and Christos Faloutsos, ANF, a fast and scalable tool for data mining in massive graphs, Proceedings of the 8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2002), 81 to 90
    locator: the definitions of the neighbourhood function N(h) and the individual neighbourhood function, and their uses in data mining
  - paper: doi:10.1145/316194.316229
    title: Michalis Faloutsos, Petros Faloutsos and Christos Faloutsos, On power-law relationships of the Internet topology, ACM SIGCOMM Computer Communication Review 29(4), 251 to 262 (1999)
    locator: the hop plot (the number of pairs within h hops) and the hop-plot exponent of the Internet graphs
  - paper: doi:10.1145/1963405.1963493
    title: Paolo Boldi, Marco Rosa and Sebastiano Vigna, HyperANF, approximating the neighbourhood function of very large graphs on a budget, Proceedings of the 20th International Conference on World Wide Web (WWW 2011), 625 to 634
    locator: the neighbourhood function, the distance distribution derived from it, and the statistics read from it, such as the average distance and the effective diameter
---

The neighbourhood function of a graph gives, for each distance $h = 0, 1, 2, \ldots$, the number $N(h)$ of ordered pairs of [vertices](/vertex/) $(u, v)$ such that $v$ can be reached from $u$ in at most $h$ steps. It is the cumulative form of the distribution of [shortest-path](/shortest-path/) distances, so the diameter, the average distance and the [effective diameter](/effective-diameter/) can all be read from it. Its plot is the *hop plot*. Computing it exactly needs a [breadth-first search](/breadth-first-search/) from every vertex, so for large graphs it is estimated by the [ANF algorithm](/anf-algorithm/) and its successors.

## Definition

Let $G = (V, E)$ be a graph with $n$ vertices, directed or undirected, without weights. Let $\mathrm{dist}(u, v)$ be the number of edges on a shortest path from $u$ to $v$, with $\mathrm{dist}(u, u) = 0$ and $\mathrm{dist}(u, v) = \infty$ when $v$ is not reachable from $u$. For a vertex $u$ and $h \ge 0$, the **ball** of radius $h$ is $B_h(u) = \{v \in V : \mathrm{dist}(u, v) \le h\}$.

- The **individual neighbourhood function** of $u$ is $N(u, h) = |B_h(u)|$.
- The **neighbourhood function** of $G$ is
$$N(h) = \sum_{u \in V} N(u, h) = |\{(u, v) \in V \times V : \mathrm{dist}(u, v) \le h\}|.$$

Palmer, Gibbons and Faloutsos also define $N(h)$ for two sets of vertices, counting only the pairs with $u$ in the first set and $v$ in the second.

Points of the definition:

- **Pairs and self-pairs.** The pairs are ordered, and the pairs $(u, u)$ are counted, so $N(0) = n$. For an undirected simple graph, $N(1) = n + 2m$. Some authors leave out the self-pairs, which subtracts $n$ from every value.
- **Shape.** $N$ does not decrease. It stops growing at the largest finite distance, and its final value $N(\infty)$ is the number of pairs $(u, v)$ with $v$ reachable from $u$.
- **Disconnected graphs.** Pairs with no path never count, so $N(\infty) < n^2$ when $G$ is not strongly connected. For an undirected graph with components of sizes $c_1, \ldots, c_r$, $N(\infty) = \sum_i c_i^2$. Statistics read from $N$ are then taken over the reachable pairs only.
- **Directed graphs.** The balls follow the direction of the arcs. The neighbourhood function of the graph with all arcs reversed is the same, since it counts the same pairs in the other order, but the individual functions differ.
- **Weights.** The definition counts hops. With edge lengths, $h$ becomes a real threshold, and the function is a step function of $h$.
- **Ties.** The definition counts pairs and needs no tie rule.

**What can be read from it.** With $N(-1) = 0$ and $P = N(\infty) - n$, the number of reachable pairs of distinct vertices:

- the *distance distribution*: the number of ordered pairs at distance exactly $h$ is $N(h) - N(h-1)$;
- the *diameter* of the reachable pairs: the largest $h$ with $N(h) > N(h - 1)$;
- the *average distance*: $\frac{1}{P} \sum_{h \ge 1} h \,(N(h) - N(h-1))$;
- the *effective diameter*: the smallest $h$ with $N(h) - n \ge 0.9 P$, or its interpolated form;
- the *hop-plot exponent*: Faloutsos, Faloutsos and Faloutsos observed that, on the Internet graphs they studied, $N(h)$ grew roughly as $h^{H}$ for small $h$, and called $H$ the hop-plot exponent.

## Examples and non-examples

**A small graph.** Take the undirected graph on the vertices 0 to 6 with the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, so $n = 7$ and $m = 9$.

| $h$ | $N(u, h)$ for $u = 0, \ldots, 6$ | $N(h)$ | pairs at distance $h$ |
|---|---|---|---|
| 0 | 1, 1, 1, 1, 1, 1, 1 | 7 | 7 |
| 1 | 3, 4, 4, 4, 4, 3, 3 | 25 | 18 |
| 2 | 4, 5, 5, 7, 6, 4, 4 | 35 | 10 |
| 3 | 5, 7, 7, 7, 7, 6, 6 | 45 | 10 |
| 4 | 7, 7, 7, 7, 7, 7, 7 | 49 | 4 |

The graph is connected, so $N(\infty) = 49 = 7^2$ and $P = 42$. The diameter is 4, since $N$ grows last at $h = 4$; the average distance is $(18 \cdot 1 + 10 \cdot 2 + 10 \cdot 3 + 4 \cdot 4)/42 = 84/42 = 2$; and the effective diameter is 3, since $N(2) - 7 = 28 < 0.9 \cdot 42 = 37.8 \le N(3) - 7 = 38$. Vertex 3 has $N(3, 2) = 7$: it reaches the whole graph in 2 steps, so its [eccentricity](/eccentricity/) is 2, the smallest of all vertices.

**A disconnected graph.** Add an eighth vertex with no edges. Then every $N(h)$ grows by 1, and $N(\infty) = 50 = 7^2 + 1^2$, not $8^2 = 64$. The diameter, average distance and effective diameter of the reachable pairs do not change.

**A complete graph.** For $K_n$, $N(0) = n$ and $N(h) = n^2$ for every $h \ge 1$.

**Non-example: the number of walks.** The number of [walks](/walk/) of length at most $h$ between two vertices, the sum of the entries of $I + A + \cdots + A^h$, also grows with $h$, but counts each pair many times; the neighbourhood function counts each pair once.

## Related definitions

- **[Effective diameter](/effective-diameter/).** The 90th percentile of the distance distribution, read from $N$.
- **[Eccentricity](/eccentricity/).** The eccentricity of $u$ is the smallest $h$ with $N(u, h) = N(u, \infty)$; the diameter is the largest eccentricity.
- **[Harmonic centrality](/harmonic-centrality/).** The harmonic centrality of $u$ is $\sum_{h \ge 1} (N(u, h) - N(u, h-1))/h$, so it is a function of the individual neighbourhood function.
- **[ANF algorithm](/anf-algorithm/).** Estimates all $N(u, h)$ with [Flajolet-Martin sketches](/flajolet-martin-sketch/) in $O(n + m)$ word operations per value of $h$; HyperANF uses HyperLogLog counters instead.
- **[Network diameter estimation](/network-diameter-estimation/).** The problem of estimating $N$, the diameter and related statistics on graphs too large for exact [all-pairs](/all-pairs-shortest-paths/) search.
- **[Small-world networks](/small-world-network/).** In such networks $N(h)$ reaches most of $N(\infty)$ at a value of $h$ that grows like $\log n$.

## References
