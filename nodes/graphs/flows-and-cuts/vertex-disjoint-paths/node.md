---
tag: S1FZT0
kind: problem
slug: vertex-disjoint-paths
name: Vertex-disjoint paths
aliases:
- Node-disjoint paths
area: graphs/flows-and-cuts
level: core
summary: Finds the largest number of paths between two vertices that share no internal vertex, equal to the minimum vertex cut by Menger's theorem.
prereqs: [vertex-capacities-flow, max-flow-problem, menger-theorem]
see_also: [edge-disjoint-paths, vertex-cut, vertex-connectivity, k-vertex-connected-graph, bipartite-matching, integrality-theorem, hopcroft-karp]
sources:
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 9, Disjoint paths (Menger's theorem in its vertex-disjoint forms and the algorithms that find the paths)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 11, Applications of Flows and Cuts (vertex capacities and vertex-disjoint paths)
  - paper: doi:10.1137/0204043
    title: Shimon Even and Robert Endre Tarjan, Network flow and testing graph connectivity, SIAM Journal on Computing 4(4), 507 to 518 (1975)
    locator: the whole paper (Dinic's algorithm on networks with unit vertex capacities takes O(n^(1/2)) phases, and vertex connectivity testing)
  - paper: doi:10.1016/0304-3975(80)90009-2
    title: Steven Fortune, John Hopcroft and James Wyllie, The directed subgraph homeomorphism problem, Theoretical Computer Science 10(2), 111 to 121 (1980)
    locator: the whole paper (two vertex-disjoint paths between two given pairs in a directed graph is NP-complete)
  - paper: doi:10.1006/jctb.1995.1006
    title: Neil Robertson and Paul D. Seymour, Graph Minors XIII, The disjoint paths problem, Journal of Combinatorial Theory, Series B 63(1), 65 to 110 (1995)
    locator: the whole paper (k vertex-disjoint paths between given pairs in an undirected graph, polynomial for fixed k)
---

The vertex-disjoint paths problem asks for the largest number of paths from a vertex $s$ to a vertex $t$ such that no two of them share a vertex other than $s$ and $t$. By the vertex form of [Menger's theorem](/menger-theorem/), for non-adjacent $s$ and $t$ this number equals the smallest number of vertices whose removal separates $t$ from $s$, a minimum [vertex cut](/vertex-cut/). Both are found by one [maximum flow](/max-flow-problem/) after [splitting each vertex](/vertex-capacities-flow/) into an in-copy and an out-copy joined by an edge of capacity 1. The version with several source-sink pairs is much harder: NP-complete in directed graphs already for two pairs.

## In plain words

You want several routes from one place to another such that no two routes pass through the same town on the way, so that closing any one town ruins at most one route. How many such routes can you find?

The answer is limited by bottleneck towns. If closing some set of towns cuts every route, then each route passes through one of them, and since routes share no town, there are at most as many routes as towns in the set. Menger's theorem says this bound is always reached by the best set. The way to find the routes is to turn each town into a one-lane road and ask for the largest flow.

## Definition

**Input.** A graph $G = (V, E)$, directed or undirected, with $n$ vertices and $m$ edges, and two vertices $s \ne t$. Parallel edges and antiparallel edges do not matter, since only vertices are shared; self-loops are ignored.

**Output.** A largest set of $s$-$t$ paths $P_1, \ldots, P_k$ that are *internally vertex-disjoint*: every vertex other than $s$ and $t$ lies on at most one of them. Write $\kappa(s, t)$ for the largest $k$.

**Edge $s t$.** If $s \to t$ is an edge, it is a path with no inner vertex and it is disjoint from every other path; it is counted once. Menger's theorem is stated for non-adjacent $s$ and $t$, because no vertex set separates adjacent vertices.

**Menger's theorem (vertex form).** If $s$ and $t$ are distinct and not adjacent, $\kappa(s, t)$ equals the least size of a set $X \subseteq V \setminus \{s, t\}$ such that $G - X$ has no $s$-$t$ path.

*Proof by flows.* Build $G'$: each $v \notin \{s, t\}$ becomes $v_{\mathrm{in}} \to v_{\mathrm{out}}$ with capacity 1, each edge $(u, v)$ becomes $u_{\mathrm{out}} \to v_{\mathrm{in}}$ with capacity $\infty$ (an undirected edge gives both directions), and $s$, $t$ are not split. An integral flow of value $k$ in $G'$ decomposes into $k$ paths, and each inner vertex carries at most 1, so the paths are internally vertex-disjoint in $G$; the converse is clear. A finite cut of $G'$ cuts only split edges, since all other edges have capacity $\infty$; the cut vertices form a separating set $X$ of the same size, and conversely each separating set gives such a cut. The max-flow min-cut theorem with the [integrality theorem](/integrality-theorem/) gives the equality. Finiteness holds because $s$ and $t$ are not adjacent: every $s$-$t$ path of $G'$ uses a split edge. $\square$

## Variants

- **[Edge-disjoint paths](/edge-disjoint-paths/).** Paths may share vertices but not edges; plain unit edge capacities. Vertex-disjoint paths are also edge-disjoint, so $\kappa(s, t)$ is at most the edge version.
- **Set to set.** Disjoint paths from a set $A$ to a set $B$, also by flows with a super-source and a super-sink; the fan lemma is the case $|A| = 1$.
- **Shortest disjoint paths.** $k$ disjoint paths of least total length, by [minimum-cost flow](/min-cost-flow-problem/) on the split graph, or by Suurballe's method for $k = 2$.
- **Given pairs.** Disjoint paths from $s_i$ to $t_i$ for $i = 1, \ldots, k$, with different pairs. In directed graphs this is NP-complete already for $k = 2$ (Fortune, Hopcroft and Wyllie); in undirected graphs it is polynomial for each fixed $k$ (Robertson and Seymour) and NP-complete when $k$ is part of the input.
- **[Vertex connectivity](/vertex-connectivity/).** The least $\kappa(s, t)$ over non-adjacent pairs; a graph is [$k$-vertex-connected](/k-vertex-connected-graph/) when it is at least $k$.

## Examples

**Edge-disjoint is not vertex-disjoint.** The directed graph has edges $s \to a$, $s \to b$, $a \to c$, $b \to c$, $c \to d$, $c \to e$, $d \to t$, $e \to t$. There are two edge-disjoint paths, $s, a, c, d, t$ and $s, b, c, e, t$, but both pass through $c$, so $\kappa(s, t) = 1$, and $X = \{c\}$ is a vertex cut of size 1.

**Two disjoint paths.** In the network $s \to a$, $s \to b$, $a \to b$, $a \to t$, $b \to t$, the paths $s, a, t$ and $s, b, t$ are disjoint, and $X = \{a, b\}$ separates; $\kappa(s, t) = 2$. The edge $a \to b$ does not help.

**Antiparallel edges.** Adding $b \to a$ changes nothing: $\kappa$ depends only on which vertices can follow which.

**No $s$-$t$ path.** Then $\kappa(s, t) = 0$ and $X = \emptyset$ separates.

**A vertex of capacity 0.** Forbidding a vertex $v$ from all paths is the same as giving its split edge capacity 0, or deleting it.

## Known algorithms

- **Augmenting paths on the split graph.** Each augmentation finds one more path in $O(n + m)$, so $k$ paths take $O(k(n + m))$, at most $O(n (n + m))$.
- **Dinic on unit vertex capacities.** Even and Tarjan showed that [Dinic's algorithm](/dinic/) needs only $O(\sqrt{n})$ phases when each vertex carries at most one unit, for $O(\sqrt{n}\, m)$ time; [Hopcroft-Karp](/hopcroft-karp/) is the bipartite case.
- **Faster maximum flow.** Any [max-flow algorithm](/max-flow-problem/) on the split graph, including the almost-linear one.
- **Vertex connectivity.** Running the above for selected pairs gives the vertex connectivity; see [vertex connectivity](/vertex-connectivity/).

## Bounds

Two vertex-disjoint paths are found in $O(n + m)$ time by two augmentations, and $k$ paths in $O(k (n + m))$. The value $\kappa(s, t)$ is at most $\min(\deg^{\mathrm{out}}(s), \deg^{\mathrm{in}}(t), n - 2)$ when $s$ and $t$ are not adjacent. The pair version with $k$ in the input is NP-complete in undirected graphs, and the directed version with two pairs is NP-complete.

## Reductions

- **To maximum flow** by vertex splitting, as above.
- **Bipartite matching to vertex-disjoint paths.** Add $s$ joined to one side and $t$ joined to the other; a matching of size $k$ is $k$ vertex-disjoint $s$-$t$ paths of length 3. This is how [bipartite matching](/bipartite-matching/) is solved by flows, and König's theorem is Menger's theorem on this graph.
- **Vertex-disjoint to edge-disjoint.** The split graph turns vertex-disjoint paths into edge-disjoint paths through the split edges.

## Applications

- Fault-tolerant routing: $k$ vertex-disjoint routes survive the failure of any $k - 1$ routers.
- Testing whether a network is $k$-vertex-connected.
- Proving the vertex form of Menger's theorem, and from it König's and Hall's theorems.
- Layout and wiring problems, which often ask for disjoint paths between given pairs.

## References
