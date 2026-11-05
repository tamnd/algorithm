---
tag: T6CYYV
kind: definition
slug: k-vertex-connected-graph
name: k-vertex-connected graph
aliases:
- k-connected graph
area: graphs/connectivity
level: advanced
summary: A graph that stays connected after removing any fewer than k vertices.
prereqs: [vertex-cut, connected-graph]
see_also: [vertex-connectivity, k-edge-connected-graph, biconnected-graph, menger-theorem, even-tarjan-vertex-connectivity, nagamochi-ibaraki-certificate, articulation-point, complete-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 1.4, Connectivity (the definition of k-connected and of the connectivity), and Section 3.3, Menger's theorem (the global version)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 4.1, Cuts and connectivity (connectivity and Harary graphs), and Section 4.2, k-connected graphs (Whitney's theorem and the expansion lemma)
  - paper: doi:10.1137/0204034
    title: Shimon Even, An algorithm for determining whether the connectivity of a graph is at least k, SIAM Journal on Computing 4(3), 393 to 396 (1975)
    locator: the whole paper (the test with maximum flows)
  - paper: doi:10.1137/0202012
    title: John E. Hopcroft and Robert E. Tarjan, Dividing a graph into triconnected components, SIAM Journal on Computing 2(3), 135 to 158 (1973)
    locator: the linear-time test for 3-connectivity
---

A graph is $k$-vertex-connected, or $k$-connected, if it has more than $k$ vertices and stays [connected](/connected-graph/) whenever fewer than $k$ vertices are removed. The largest such $k$ is the [vertex connectivity](/vertex-connectivity/) $\kappa(G)$. 1-connected means connected with at least two vertices, and 2-connected means [biconnected](/biconnected-graph/). By Whitney's form of [Menger's theorem](/menger-theorem/), $k$-connected means that every two vertices are joined by $k$ paths that share no inner vertex, so a network with this property survives the failure of any $k - 1$ nodes. It is a stronger property than being [$k$-edge-connected](/k-edge-connected-graph/).

## Definition

Let $G = (V, E)$ be an undirected graph with $n = |V|$. Parallel edges and [self-loops](/self-loop/) are allowed but play no part: the definition depends only on which pairs of distinct vertices are adjacent. For $X \subseteq V$, $G - X$ is $G$ without the vertices of $X$ and their edges. Let $k \ge 0$.

$G$ is **$k$-connected** if $n > k$ and $G - X$ is connected for every set $X \subseteq V$ with $|X| < k$.

A set $X$ such that $G - X$ is not connected is a [vertex cut](/vertex-cut/), or separating set. So, for $n > k$, $G$ is $k$-connected exactly when it has no vertex cut with fewer than $k$ vertices.

**Connectivity.** $\kappa(G)$ is the largest $k$ such that $G$ is $k$-connected. If $G$ is not complete, $\kappa(G)$ is the least size of a vertex cut. For the [complete graph](/complete-graph/), $\kappa(K_n) = n - 1$: it has no vertex cut, and the condition $n > k$ stops $k$ at $n - 1$. A graph is $k$-connected exactly when $\kappa(G) \ge k$, so a $k$-connected graph is also $j$-connected for every $j < k$.

**Theorem (Whitney, 1932; the global form of Menger's theorem).** A graph with $n > k$ is $k$-connected if and only if every two distinct vertices are joined by $k$ paths that pairwise share only their ends.

One direction is short: if $X$ has fewer than $k$ vertices and $u, v \notin X$, then at least one of $k$ such $u$-$v$ paths avoids $X$, since each vertex of $X$ is an inner vertex of at most one of them. For adjacent $u$ and $v$ the edge $uv$ is one of the paths. The other direction is Menger's theorem (Diestel, Section 3.3).

**Basic facts.**

- **Degree.** If $G$ is $k$-connected and $v$ is a vertex, removing the neighbours of $v$ separates $v$ unless they are all other vertices, and in that case $n - 1 \ge k$. So $v$ has at least $k$ distinct neighbours, the minimum degree $\delta(G)$ is at least $k$, and $G$ has at least $\lceil kn/2 \rceil$ edges that are not loops or parallel copies. The Harary graphs reach this bound for every $2 \le k < n$.
- **Whitney's inequality.** $\kappa(G) \le \lambda(G) \le \delta(G)$, where $\lambda$ is the [edge connectivity](/edge-connectivity/). So $k$-connected implies $k$-edge-connected. The converse fails: two triangles that share one vertex have $\lambda = 2$ and $\kappa = 1$.
- **Expansion.** If $G$ is $k$-connected and $G'$ adds a new vertex $y$ with at least $k$ neighbours in $G$, then $G'$ is $k$-connected. *Proof.* $G'$ has more than $k + 1$ vertices. Let $|X| < k$. If $y \in X$, then $G' - X = G - (X \setminus \{y\})$, which is connected. If $y \notin X$, then $G - X$ is connected and $y$ has a neighbour outside $X$, so $G' - X$ is connected. $\square$
- **Small $k$.** Every graph with $n \ge 1$ is 0-connected. $G$ is 1-connected if and only if it is connected with $n \ge 2$, and 2-connected if and only if it is [biconnected](/biconnected-graph/): connected, $n \ge 3$, and no [articulation point](/articulation-point/).
- **Parallel edges do not help.** Two vertices with any number of parallel edges form a 1-connected graph, not a 2-connected one. This differs from [$k$-edge-connectivity](/k-edge-connected-graph/), where parallel edges count.

**Testing.** For $k = 1$, one search; for $k = 2$, one [depth-first search](/depth-first-search/) with the [Hopcroft-Tarjan algorithm](/hopcroft-tarjan-biconnectivity/); for $k = 3$, the linear-time triconnectivity algorithm of Hopcroft and Tarjan (1973). For general $k$, the test uses maximum flows in a graph where each vertex is split into an in-copy and an out-copy joined by an arc of capacity 1: Even (1975) tests $\kappa(G) \ge k$ in this way, and the [Even-Tarjan algorithm](/even-tarjan-vertex-connectivity/) computes $\kappa(G)$ itself. The [Nagamochi-Ibaraki certificate](/nagamochi-ibaraki-certificate/) keeps $k$-connectivity with at most $k(n - 1)$ edges, so a test can run on a sparse graph.

## Examples and non-examples

| graph | $\kappa$ | why |
|---|---|---|
| a tree with $n \ge 2$ vertices | 1 | each inner vertex is an articulation point; a single edge is $K_2$ |
| a cycle $C_n$, $n \ge 3$ | 2 | removing one vertex leaves a path; removing two non-adjacent vertices splits it |
| the [complete graph](/complete-graph/) $K_n$ | $n - 1$ | no vertex cut at all |
| the complete bipartite graph $K_{a,b}$, $1 \le a \le b$, $b \ge 2$ | $a$ | the smaller side is a vertex cut, and every smaller set leaves a connected graph |
| the wheel: a cycle $C_{n-1}$ plus a centre joined to all, $n \ge 5$ | 3 | the centre and two non-adjacent cycle vertices form a cut |
| the hypercube $Q_d$, $d \ge 1$ | $d$ | $d$-regular, and $d$ internally disjoint paths join each pair |
| the Petersen graph | 3 | 3-regular, and no two vertices separate it |
| two copies of $K_4$ joined by the edges $\{3, 4\}$ and $\{3, 5\}$ | 1 | the vertex 3 is an articulation point, although $\lambda = 2$ and $\delta = 3$ |

Non-examples:

- $K_k$ is not $k$-connected, by the condition $n > k$, although removing fewer than $k$ of its vertices always leaves it connected.
- A graph with an articulation point is not 2-connected, however dense it is elsewhere.
- Two vertices joined by many parallel edges are not 2-connected.

## Related definitions

- [Vertex connectivity](/vertex-connectivity/): the number $\kappa(G)$ and the problem of computing it.
- [Vertex cut](/vertex-cut/): the sets whose removal disconnects the graph.
- [k-edge-connected graph](/k-edge-connected-graph/): the edge version, a weaker property for the same $k$.
- [Biconnected graph](/biconnected-graph/): the case $k = 2$. The case $k = 3$ is called *triconnected*; by Steinitz's theorem, the 3-connected planar simple graphs are exactly the graphs of convex polyhedra.
- [Menger's theorem](/menger-theorem/): the link between vertex cuts and disjoint paths.
- [Even-Tarjan vertex connectivity](/even-tarjan-vertex-connectivity/): computes $\kappa(G)$ with maximum flows.

## References
