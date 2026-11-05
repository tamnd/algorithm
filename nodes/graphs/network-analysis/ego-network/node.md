---
tag: DQVX2R
kind: definition
slug: ego-network
name: Ego network
aliases:
- egocentric network
- ego graph
area: graphs/network-analysis
level: intro
summary: The subgraph induced by one vertex, the ego, and its neighbours, the alters.
prereqs: [neighborhood, induced-subgraph]
see_also: [clustering-coefficient, degree-centrality, betweenness-centrality, structural-holes, weak-ties, breadth-first-search]
sources:
  - paper: doi:10.1016/j.socnet.2004.11.007
    title: Martin Everett and Stephen P. Borgatti, Ego network betweenness, Social Networks 27(1), 31 to 38 (2005)
    locator: the whole paper (the definition of the ego network, ego betweenness, and its rank correlation with betweenness in the whole network)
  - paper: doi:10.1016/S0378-8733(02)00016-3
    title: Peter V. Marsden, Egocentric and sociocentric measures of network centrality, Social Networks 24(4), 407 to 422 (2002)
    locator: the whole paper (centrality computed from ego network data compared with the whole network)
  - book: isbn:9780674843714
    title: Ronald S. Burt, Structural Holes, The Social Structure of Competition, Harvard University Press, 1992
    locator: Chapter 1 (redundant contacts, effective size and constraint of an ego network)
---

The ego network of a [vertex](/vertex/) $v$ is the [induced subgraph](/induced-subgraph/) on $v$ and its neighbours. The vertex $v$ is the *ego*, its neighbours are the *alters*, and the ego network keeps the edges among the alters as well as the edges to the ego. Survey data in sociology is often of this kind, because one can ask a person about their contacts and about the ties among them, but not about the whole network. Many local measures, such as the [clustering coefficient](/clustering-coefficient/) and Burt's effective size, are functions of the ego network alone.

## Definition

Let $G = (V, E)$ be a graph and $v \in V$. Let $N(v)$ be the [neighborhood](/neighborhood/) of $v$ and $N[v] = N(v) \cup \{v\}$ the closed neighborhood. The **ego network** of $v$ is

$$\mathrm{Ego}(v) = G[N[v]],$$

the subgraph with the vertex set $N[v]$ and every edge of $G$ whose two ends are in $N[v]$. It has $d(v) + 1$ vertices, $d(v)$ edges at the ego, and $T(v)$ edges among the alters, where $T(v)$ is the number of triangles at $v$.

**Radius $r$.** The ego network of radius $r \ge 1$ is $G[B_r(v)]$, where $B_r(v) = \{u : d(v, u) \le r\}$ is the ball of radius $r$ around $v$. Radius 1 is the default.

**Directed graphs.** For a directed graph, the alters can be the out-neighbours, the in-neighbours, or both, and the choice must be stated. The induced subgraph keeps all arcs among the chosen vertices, in their directions.

**Weighted graphs.** The ego network keeps the weights of its edges. A weight is not used to choose the alters, unless a cut-off on the weight is stated.

**Disconnected graphs and isolated vertices.** The ego network sees only the component of $v$, so no special rule is needed. An isolated vertex has the ego network with one vertex and no edge. Measures that divide by the number of pairs of alters are undefined when $d(v) < 2$.

**Measures on the ego network.** Let $k = d(v)$ and $t = T(v)$, the number of ties among the alters.

- *Size* $k$ and *density among the alters* $t / \binom{k}{2}$, which is the local [clustering coefficient](/clustering-coefficient/) of $v$.
- *Effective size* (Burt): the number of alters minus their redundancy. For a graph without weights, it reduces to $k - 2t/k$, the number of alters minus the mean number of ties that an alter has to other alters.
- *Ego betweenness* (Everett and Borgatti): the [betweenness centrality](/betweenness-centrality/) of $v$ computed inside $\mathrm{Ego}(v)$. Each pair of non-adjacent alters $x, y$ adds $1/c_{xy}$, where $c_{xy}$ is the number of their common neighbours in the ego network, the ego among them. Paths inside the ego network between non-adjacent alters have length 2, so this is the full betweenness of $v$ there.

**Cost.** With the adjacency lists in hash sets, building $\mathrm{Ego}(v)$ takes $O\bigl(\sum_{u \in N[v]} d(u)\bigr)$ expected time: for each vertex of $N[v]$, keep the neighbours that are in $N[v]$. The ego network of radius $r$ is found by a [breadth-first search](/breadth-first-search/) from $v$ that stops at depth $r$.

## Examples and non-examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$.

| ego | alters | ties among alters $t$ | density | effective size $k - 2t/k$ | ego betweenness |
|---|---|---|---|---|---|
| 1 | 0, 2, 3 | $\{0,2\}$, $\{2,3\}$ | 2/3 | 3 - 4/3 = 5/3 | 1/2 |
| 3 | 1, 2, 4 | $\{1,2\}$ | 1/3 | 3 - 2/3 = 7/3 | 2 |
| 4 | 3, 5, 6 | $\{5,6\}$ | 1/3 | 3 - 2/3 = 7/3 | 2 |

For ego 1, the only non-adjacent pair of alters is $\{0, 3\}$, and it has two common neighbours in $\mathrm{Ego}(1)$, the vertices 1 and 2, so the ego betweenness is 1/2. For ego 3, the pairs $\{1, 4\}$ and $\{2, 4\}$ each depend on 3 alone, which gives 2. All three egos have degree 3, but the ego measures single out 3 and 4 as the brokers between the two groups. The full [betweenness](/betweenness-centrality/) of 3 and 4 in the whole graph is 9 and 8, and of 1 it is 2, so the order is the same here.

**Radius 2.** The ego network of radius 2 of vertex 0 is the induced subgraph on $\{0, 1, 2, 3\}$. Vertex 4 is at distance 3 from 0, so it is not included.

**Non-examples.**

- The subgraph made of the ego and the edges at the ego only, a star, is not the ego network. It drops the ties among the alters, which most ego measures need.
- The neighbourhood $N(v)$ alone, without $v$, is not the ego network. Its induced subgraph $G[N(v)]$ is sometimes called the *link* or the open ego network, and its density is the clustering coefficient of $v$.
- The [connected component](/connected-components/) of $v$ is not its ego network, unless every vertex of the component is a neighbour of $v$. In the example, the component of 0 is the whole graph, while $\mathrm{Ego}(0)$ is the triangle $\{0, 1, 2\}$.

## Related definitions

- [Neighborhood](/neighborhood/) and [induced subgraph](/induced-subgraph/): the parts of the definition.
- [Clustering coefficient](/clustering-coefficient/): the density among the alters.
- [Structural holes](/structural-holes/): Burt's theory of brokers, measured on ego networks.
- [Weak ties](/weak-ties/): ties to alters outside the dense part of the ego network.
- [Degree centrality](/degree-centrality/): the size of the ego network minus 1.

## References
