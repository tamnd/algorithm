---
tag: 7Z4A5T
kind: definition
slug: k-core
name: k-core
aliases:
- core decomposition
area: graphs/network-analysis
level: core
summary: Maximal subgraph in which every node has degree at least k.
prereqs: [graph, degree, induced-subgraph]
see_also: [k-core-decomposition, batagelj-zaversnik-algorithm, degeneracy, degeneracy-ordering, core-periphery-structure, dynamic-k-core-decomposition, clique-number, greedy-coloring]
sources:
  - paper: doi:10.1016/0378-8733(83)90028-X
    title: Stephen B. Seidman, Network structure and minimum degree, Social Networks 5(3), 269 to 287 (1983)
    locator: the definition of the k-core and the nesting of the cores
  - paper: doi:10.1145/2402.322385
    title: David W. Matula and Leland L. Beck, Smallest-last ordering and clustering and graph coloring algorithms, Journal of the ACM 30(3), 417 to 427 (1983)
    locator: the smallest-last ordering and its relation to the largest minimum degree of a subgraph
  - paper: doi:10.1007/s11634-010-0079-y
    title: Vladimir Batagelj and Matjaž Zaversnik, Fast algorithms for determining (generalized) core groups in social networks, Advances in Data Analysis and Classification 5(2), 129 to 145 (2011)
    locator: the definitions of cores and core numbers, their properties, and the generalized cores for vertex functions
  - paper: doi:10.1007/s00778-019-00587-4
    title: Fragkiskos D. Malliaros, Christos Giatsidis, Apostolos N. Papadopoulos and Michalis Vazirgiannis, The core decomposition of networks, theory, algorithms and applications, The VLDB Journal 29, 61 to 92 (2020)
    locator: Section 2 (definitions for undirected, directed and weighted graphs)
---

The **k-core** of a graph is its largest [induced subgraph](/induced-subgraph/) in which every vertex has [degree](/degree/) at least $k$. It is unique, it can be empty, and the $k$-cores for $k = 0, 1, 2, \ldots$ are nested, each inside the one before. The largest $k$ for which a vertex is in the $k$-core is its **core number**, and the largest $k$ with a non-empty $k$-core is the [degeneracy](/degeneracy/) of the graph. Finding all core numbers is the [k-core decomposition](/k-core-decomposition/) problem, which takes linear time.

## Definition

Let $G = (V, E)$ be an undirected graph without self-loops, and let $k \ge 0$ be an integer. For $S \subseteq V$, write $\deg_S(v)$ for the number of neighbours of $v$ in $S$. A set $S$ is **$k$-dense** when $\deg_S(v) \ge k$ for each $v \in S$. The empty set is $k$-dense.

The **$k$-core** of $G$ is the subgraph induced by the union of all $k$-dense sets,

$$C_k(G) = G\Big[\bigcup \{ S \subseteq V : S \text{ is } k\text{-dense} \}\Big].$$

**It is the largest $k$-dense set.** If $S$ and $T$ are $k$-dense, then so is $S \cup T$: a vertex $v \in S$ has $\deg_{S \cup T}(v) \ge \deg_S(v) \ge k$, and the same holds for $v \in T$. So the union of all $k$-dense sets is $k$-dense, and it contains every $k$-dense set. In particular the $k$-core is unique, and it is the unique *maximal* subgraph with minimum degree at least $k$.

**Peeling gives it.** Delete, again and again, a vertex of degree less than $k$ in the remaining graph, until no such vertex is left. The remaining set $R$ is $k$-dense. And no vertex of a $k$-dense set $S$ is ever deleted: before the first deletion of a vertex of $S$, all of $S$ remains, so that vertex has at least $k$ neighbours left. So $R$ contains every $k$-dense set, and $R$ is the $k$-core, whatever the order of the deletions.

**Core number.** The core number of $v$ is $\mathrm{core}(v) = \max\{k : v \in C_k(G)\}$. Since a $(k+1)$-dense set is $k$-dense, $C_0(G) \supseteq C_1(G) \supseteq C_2(G) \supseteq \cdots$, and $v \in C_k(G)$ exactly when $k \le \mathrm{core}(v)$. The set of vertices with core number exactly $k$ is the **$k$-shell**.

**Basic facts.**

- $\mathrm{core}(v) \le \deg(v)$, since $v$ has at most $\deg(v)$ neighbours in any set.
- $C_0(G) = G$, and $C_1(G)$ is $G$ without its isolated vertices.
- The [degeneracy](/degeneracy/) $\delta^*(G) = \max_v \mathrm{core}(v)$ equals $\max_{H} \delta(H)$, the largest minimum degree of a subgraph $H$ of $G$. Hence a greedy colouring in the reverse of the peeling order uses at most $\delta^*(G) + 1$ colours, and the [clique number](/clique-number/) is at most $\delta^*(G) + 1$.
- The $k$-core need not be connected. Some authors call each connected component of $C_k(G)$ a $k$-core; this page uses Seidman's definition, with the whole subgraph.

**Multigraphs and weights.** In a [multigraph](/multigraph/), $\deg_S(v)$ counts the edges with multiplicity, and the definition and proofs above stay the same. For a weighted graph, the *generalized cores* of Batagelj and Zaversnik replace $\deg_S(v)$ by a function $p(v, S)$ that does not decrease when $S$ grows, for example the sum of the weights of the edges from $v$ into $S$. The union argument above uses only this monotonicity, so these cores are unique too, and peeling still finds them.

**Directed graphs.** There is no single standard. The *in-core* uses in-degrees inside $S$, the *out-core* uses out-degrees, and the $(k, l)$-core asks for in-degree at least $k$ and out-degree at least $l$. Each of these is a generalized core in the sense above, so it is unique and peeling finds it.

**Ties.** Many vertices share a core number, and in large networks a few values hold most of the vertices. The core number is a coarse score: to rank vertices inside one shell, another measure is needed.

## Examples and non-examples

**A worked example.** Take the vertices 0 to 9 and the 14 edges: the [complete graph](/complete-graph/) on $\{0, 1, 2, 3\}$, then $\{0,4\}$, $\{1,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, $\{6,8\}$, $\{3,8\}$, $\{5,9\}$, and vertex 7 alone. The degrees of $0, 1, \ldots, 9$ are $4, 4, 3, 4, 4, 3, 3, 0, 2, 1$.

| $k$ | the $k$-core | its size |
|---|---|---|
| 0 | all vertices | 10 |
| 1 | all but 7 | 9 |
| 2 | $\{0, 1, 2, 3, 4, 5, 6, 8\}$ | 8 |
| 3 | $\{0, 1, 2, 3\}$ | 4 |
| 4 | empty | 0 |

For $k = 2$, peeling deletes 7 and 9; then 5 has degree 2 and 8 has degree 2, so nothing more goes. For $k = 3$, peeling deletes 7, 8 (degree 2), 9, then 5 (its degree drops to 2), then 6 (its neighbours left are only 4), then 4 (only 0 and 1 are left). The core numbers of $0, 1, \ldots, 9$ are $3, 3, 3, 3, 2, 2, 2, 0, 2, 1$, and the degeneracy is 3.

Vertex 4 has degree 4 but core number 2, while vertex 2 has degree 3 and core number 3: the core number depends on whether the neighbours are themselves well connected, not only on their count.

**Small families.** A tree with at least one edge has degeneracy 1: its 1-core is the whole tree minus isolated vertices, and its 2-core is empty, since every non-empty forest has a vertex of degree at most 1. A cycle is its own 2-core. The complete graph $K_n$ is its own $(n-1)$-core. In a [planar graph](/planar-graph/) every subgraph has a vertex of degree at most 5, so the 6-core is empty.

**Non-examples.**

- In the example, the triangle $\{4, 5, 6\}$ has minimum degree 2, but it is not the 2-core: it is not maximal, since $\{0, \ldots, 6, 8\}$ is 2-dense and contains it.
- The set of vertices of degree at least $k$ in $G$ is not the $k$-core. In the example, the vertices of degree at least 3 are $\{0, 1, 2, 3, 4, 5, 6\}$, and in the subgraph they induce, vertex 5 has only the neighbours 4 and 6.
- A [clique](/clique/) on $k + 1$ vertices is $k$-dense, but the $k$-core is usually much larger than any clique, and need not contain a clique of size $k + 1$: a cycle of length 5 is a 2-core with no triangle.

## Related definitions

- [k-core decomposition](/k-core-decomposition/): the problem of computing all core numbers, and the [Batagelj-Zaversnik algorithm](/batagelj-zaversnik-algorithm/) that solves it in $O(n + m)$ time.
- [Degeneracy](/degeneracy/) and the [degeneracy ordering](/degeneracy-ordering/): the largest core number, and the peeling order that proves it.
- [Core-periphery structure](/core-periphery-structure/): a dense core and a sparse periphery, which the inner cores often detect.
- [Dynamic k-core decomposition](/dynamic-k-core-decomposition/): keeping core numbers under edge updates.
- *$k$-truss*: the largest subgraph in which each edge lies in at least $k - 2$ triangles of the subgraph, a finer notion built on [triangle counting](/triangle-counting/).

## References
