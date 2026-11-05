---
tag: P6QNDH
kind: problem
slug: edge-connectivity
name: Edge connectivity
aliases:
- k-edge-connectivity
- Line connectivity
area: graphs/connectivity
level: core
summary: Compute the minimum number of edges whose removal disconnects the graph.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m + n² log n)}
prereqs: [k-edge-connected-graph, cut, max-flow-problem]
see_also: [bridge-finding, global-min-cut-problem, stoer-wagner, nagamochi-ibaraki, karger-min-cut, menger-theorem, vertex-connectivity, gomory-hu-tree]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 1.4, Connectivity (the edge-connectivity and the inequality between vertex connectivity, edge-connectivity and minimum degree), and Section 3.3, Menger's theorem
  - paper: doi:10.1137/0204043
    title: Shimon Even and Robert E. Tarjan, Network flow and testing graph connectivity, SIAM Journal on Computing 4(4), 507 to 518 (1975)
    locator: the edge connectivity test in O(V^(5/3) E) time with Dinic's algorithm on unit capacities
  - paper: doi:10.1145/263867.263872
    title: Mechthild Stoer and Frank Wagner, A simple min-cut algorithm, Journal of the ACM 44(4), 585 to 591 (1997)
    locator: the whole paper (minimum cut of a weighted undirected graph in O(nm + n^2 log n) time without flows)
  - paper: "Ken-ichi Kawarabayashi and Mikkel Thorup, Deterministic edge connectivity in near-linear time, Journal of the ACM 66(1), Article 4 (2019); arXiv:1411.5123"
    locator: the main theorem (deterministic near-linear time for simple graphs)
---

Edge connectivity is the problem of finding $\lambda(G)$, the least number of edges whose removal disconnects an [undirected graph](/undirected-graph/) $G$, and usually also a set of that many edges. It equals the size of a smallest [cut](/cut/), so it is the unweighted case of the [global minimum cut problem](/global-min-cut-problem/). By [Menger's theorem](/menger-theorem/), $\lambda(G) \ge k$ exactly when each two vertices are joined by $k$ edge-disjoint paths, which makes $\lambda(G)$ the number of link failures that a network survives. It can be found with $n - 1$ [maximum flow](/max-flow-problem/) computations, or without flows in $O(nm + n^2 \log n)$ time by the [Stoer-Wagner algorithm](/stoer-wagner/).

## In plain words

A network of computers is joined by cables. How many cables must break before some computer can no longer reach some other one? That number is the edge connectivity. A network with a single weak cable has the value 1. A ring has the value 2, because one break still leaves the other way round.

The answer is always at most the number of cables at the computer with the fewest cables: cut all of those, and that computer is alone. It can be smaller, when a thin bundle of cables joins two big parts.

To find it, one can ask, for one fixed computer and each other computer, how many paths without a shared cable join them, and take the smallest answer. Faster methods merge computers step by step and never compute a flow.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n = |V| \ge 2$ vertices and a multiset $E$ of $m$ edges. Parallel edges are allowed and each copy counts. [Self-loops](/self-loop/) are allowed and never matter, because removing a loop never disconnects a graph.

**Output.** The number

$$\lambda(G) = \min \{\, |F| : F \subseteq E, \ G - F \text{ is not connected} \,\}$$

and a set $F$ that reaches the minimum. Here $G - F$ keeps all vertices. If $G$ is not connected, $\lambda(G) = 0$ with $F = \emptyset$.

**The cut form.** For $\emptyset \neq S \subsetneq V$, let $\delta(S)$ be the multiset of edges with exactly one end in $S$. Then

$$\lambda(G) = \min_{\emptyset \neq S \subsetneq V} |\delta(S)|.$$

*Proof.* Removing $\delta(S)$ leaves no edge between $S$ and $V \setminus S$, so $G - \delta(S)$ is not connected and $\lambda(G) \le |\delta(S)|$. Conversely, let $F$ disconnect $G$, and let $S$ be the vertex set of one component of $G - F$. Then $S \neq V$, and every edge of $\delta(S)$ is in $F$, since an edge of $G - F$ cannot leave a component. So $|\delta(S)| \le |F|$. $\square$

A graph is [k-edge-connected](/k-edge-connected-graph/) exactly when $\lambda(G) \ge k$. For two vertices $s \neq t$, the *local* edge connectivity $\lambda(s, t)$ is the least $|\delta(S)|$ over the sets $S$ with $s \in S$ and $t \notin S$. By Menger's theorem it is the largest number of edge-disjoint $s$-$t$ paths, and it is the value of a maximum $s$-$t$ flow with capacity 1 on each edge in each direction. By the cut form, $\lambda(G) = \min_{s \neq t} \lambda(s, t)$.

**Whitney's inequality.** Let $\kappa(G)$ be the [vertex connectivity](/vertex-connectivity/) and $\delta_{\min}(G)$ the least number of distinct neighbours of a vertex. For each graph with $n \ge 2$,

$$\kappa(G) \le \lambda(G) \le \delta_{\min}(G) \text{ for simple graphs, and } \kappa(G) \le \lambda(G) \text{ always.}$$

*Proof.* $\lambda(G) \le |\delta(\{v\})|$, which is the degree of $v$ without loops, and in a simple graph this is the number of neighbours of $v$. For $\kappa \le \lambda$, it is enough to treat the simple graph $H$ that keeps one copy of each edge: $H$ has the same $\kappa$, and $\lambda(H) \le \lambda(G)$. Take a smallest cut $F = \delta(S)$ of $H$. If each vertex of $S$ is adjacent to each vertex outside $S$, then $|F| = |S| \cdot |V \setminus S| \ge n - 1 \ge \kappa(H)$. Otherwise pick $x \in S$ and $y \notin S$ that are not adjacent. Build a vertex set $T$: for each edge of $F$, put into $T$ its end in $S$ if that end is not $x$, and its end outside $S$ otherwise. Then $|T| \le |F|$, and $x, y \notin T$ because no edge of $F$ joins $x$ to $y$. Each $x$-$y$ path uses an edge $\{a, b\}$ of $F$ with $a \in S$; if $a \neq x$ then $a \in T$, and if $a = x$ then $b \in T$. So $T$ separates $x$ from $y$, and $\kappa(H) \le |T| \le |F| = \lambda(H)$. $\square$

## Variants

- **Decision.** Is $\lambda(G) \ge k$? For $k = 1$ this is connectivity, and for $k = 2$ it asks for a connected graph with no [bridge](/bridge/); both take $O(n + m)$ time.
- **Local.** Compute $\lambda(s, t)$ for given $s$ and $t$. This is one unit-capacity [max flow](/max-flow-problem/); see [edge-disjoint paths](/edge-disjoint-paths/).
- **All pairs.** Compute $\lambda(s, t)$ for all pairs. A [Gomory-Hu tree](/gomory-hu-tree/) stores all of them with $n - 1$ flow computations.
- **Weighted.** Each edge has a non-negative weight, and the answer is the least total weight of a cut. This is the [global minimum cut problem](/global-min-cut-problem/).
- **Directed.** The least number of edges whose removal leaves a directed graph not [strongly connected](/strongly-connected-graph/). Fix $s$; the answer is $\min_t \min(\lambda(s, t), \lambda(t, s))$, with directed flows. See [directed global min cut](/directed-global-min-cut-problem/).
- **Sparse certificate.** Find a subgraph with at most $k(n - 1)$ edges that is $k$-edge-connected exactly when $G$ is. See the [Nagamochi-Ibaraki certificate](/nagamochi-ibaraki-certificate/).

## Examples

| graph | $n$ | $m$ | $\kappa$ | $\lambda$ | $\delta_{\min}$ | a smallest cut |
|---|---|---|---|---|---|---|
| a tree | $n$ | $n - 1$ | 1 | 1 | 1 | any edge |
| the cycle $C_5$ | 5 | 5 | 2 | 2 | 2 | two edges of the cycle |
| the [complete graph](/complete-graph/) $K_4$ | 4 | 6 | 3 | 3 | 3 | the three edges at one vertex |
| the Petersen graph | 10 | 15 | 3 | 3 | 3 | the three edges at one vertex |
| two vertices with 3 parallel edges | 2 | 3 | 1 | 3 | 1 | all three copies |
| two disjoint triangles | 6 | 6 | 0 | 0 | 2 | the empty set |

**The two inequalities can be strict.** Take two copies of $K_4$ on the vertices $0, 1, 2, 3$ and $4, 5, 6, 7$, and add the edges $\{3, 4\}$ and $\{3, 5\}$. The graph has 14 edges. The vertex 3 is an [articulation point](/articulation-point/), so $\kappa = 1$. The cut $\delta(\{0, 1, 2, 3\})$ has the 2 edges $\{3, 4\}$ and $\{3, 5\}$, and no single edge is a bridge, so $\lambda = 2$. Each vertex has at least 3 neighbours, so $\delta_{\min} = 3$. So $1 < 2 < 3$.

**A flow computation.** In the same graph, take $s = 0$. Then $\lambda(0, t) = 3$ for $t \in \{1, 2, 3\}$ and $\lambda(0, t) = 2$ for $t \in \{4, 5, 6, 7\}$, so the minimum over $t$ is 2, as the cut form says.

## Known algorithms

| method | time | remark |
|---|---|---|
| all cuts $\delta(S)$ | $O(2^n m)$ | brute force from the cut form |
| $n - 1$ flows from a fixed $s$ | $n - 1$ unit-capacity max flows | correct because a smallest cut separates $s$ from some $t$ |
| the same with [Dinic's algorithm](/dinic/) (Even and Tarjan, 1975) | $O(n^{5/3} m)$ | each unit-capacity flow costs $O(n^{2/3} m)$ |
| [Nagamochi-Ibaraki](/nagamochi-ibaraki/) and [Stoer-Wagner](/stoer-wagner/) | $O(nm + n^2 \log n)$ | no flows; works with weights |
| [Karger's contraction](/karger-min-cut/) and [Karger-Stein](/karger-stein/) | $O(n^2 \log^3 n)$ with high probability for Karger-Stein | randomized, Monte Carlo |
| Kawarabayashi and Thorup (2019) | near-linear, deterministic | for simple unweighted graphs |

The reason the flow method is correct: let $\delta(S)$ be a smallest cut and fix any $s$. If $s \in S$, pick $t \notin S$; if $s \notin S$, pick $t \in S$. Then $\delta(S)$ separates $s$ from $t$, so $\lambda(s, t) \le \lambda(G)$, and $\lambda(s, t) \ge \lambda(G)$ always holds. So the minimum over the $n - 1$ choices of $t$ is $\lambda(G)$.

## Bounds

**Upper bound.** $O(nm + n^2 \log n)$ deterministic time in the [word RAM](/word-ram/) model, by Stoer-Wagner or Nagamochi-Ibaraki, also with weights. For simple unweighted graphs, deterministic near-linear time is known (Kawarabayashi and Thorup).

**Lower bound.** Each deterministic algorithm reads $\Omega(n + m)$ list entries in the worst case, already for the test $\lambda(G) \ge 1$, which asks whether $G$ is connected. *Proof.* Let $G$ be two disjoint copies $A$ and $B$ of a graph with no bridge: a cycle of length $n/2$ for the term $n$, or a [complete graph](/complete-graph/) for the term $m$. If the algorithm reads neither list entry of an edge $\{a_1, a_2\}$ of $A$ and neither entry of an edge $\{b_1, b_2\}$ of $B$, rewrite these four entries so that the edges become $\{a_1, b_2\}$ and $\{b_1, a_2\}$. The new graph is connected, since $A$ and $B$ stay connected after one edge is removed, but the algorithm sees the same entries. So it reads an entry of each edge of $A$ or of each edge of $B$, which is half of the edges. $\square$ The same swap argument appears on the [connected components](/connected-components/) page.

## Reductions

- **To max flow.** $n - 1$ unit-capacity flows, as above. Each undirected edge becomes two opposite arcs of capacity 1.
- **To the global min cut.** Give each edge the weight 1 (parallel edges add up), and run any global min cut algorithm.
- **From $\lambda \ge k$ to a sparse graph.** Replace $G$ by a Nagamochi-Ibaraki certificate with at most $k(n - 1)$ edges in $O(m)$ time, then test the smaller graph. This turns $m$ into $O(kn)$ in each bound above.
- **Vertex connectivity is the harder problem.** It needs flows on a graph with split vertices; see [vertex connectivity](/vertex-connectivity/) and the [Even-Tarjan algorithm](/even-tarjan-vertex-connectivity/).

## Applications

- Network reliability: $\lambda(G) - 1$ links may fail at once and the network stays connected.
- [Strong orientation](/strong-orientation/): a graph can be made strongly connected with one-way edges if and only if $\lambda \ge 2$.
- Clustering and [image segmentation](/image-segmentation-graph-cuts/), where small cuts split the data into natural parts.
- Bounds in other proofs: by Whitney's inequality, a lower bound on $\kappa$ gives one on $\lambda$, and an upper bound on the minimum degree gives one on both.

## References
