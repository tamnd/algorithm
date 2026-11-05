---
tag: DSS4VS
kind: problem
slug: edge-disjoint-paths
name: Edge-disjoint paths
aliases:
- Undirected edge-disjoint paths
area: graphs/flows-and-cuts
level: core
summary: Finds the largest number of paths between two vertices that share no edge, which equals the minimum cut and is solved by maximum flow.
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: "O(m min(m^(1/2), n^(2/3)))"}
prereqs: [max-flow-problem, flow-integrality-theorem, flow-decomposition]
see_also: [menger-theorem, vertex-disjoint-paths, edge-connectivity, dinic, ford-fulkerson, multi-commodity-flow-problem, bipartite-matching, min-cut-problem]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.6, Disjoint Paths in Directed and Undirected Graphs (the reduction to maximum flow, Menger's theorem, and the undirected case)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 11, Applications of Flows and Cuts (edge-disjoint paths)
  - paper: doi:10.1137/0204043
    title: Shimon Even and Robert Endre Tarjan, Network flow and testing graph connectivity, SIAM Journal on Computing 4(4), 507 to 518 (1975)
    locator: the bound for Dinic's algorithm on networks with unit capacities
  - paper: doi:10.1016/0304-3975(80)90009-2
    title: Steven Fortune, John Hopcroft and James Wyllie, The directed subgraph homeomorphism problem, Theoretical Computer Science 10(2), 111 to 121 (1980)
    locator: the NP-completeness of two disjoint paths for two terminal pairs in directed graphs
---

The edge-disjoint paths problem asks for the largest number of paths from a vertex $s$ to a vertex $t$ such that no edge lies on two of them. Give every edge capacity 1: an integral [maximum flow](/max-flow-problem/) of value $k$ splits into $k$ such paths, and $k$ edge-disjoint paths give a flow of value $k$, so the answer is the maximum flow value. By the max-flow min-cut theorem it also equals the least number of edges whose removal separates $t$ from $s$, which is [Menger's theorem](/menger-theorem/). The same method works for undirected graphs, after one small repair for edges used in both directions.

## In plain words

You want to send messages from one computer to another over several routes, so that cutting any one cable kills at most one route. How many such routes can you have?

Give each cable room for one message and push as many messages as possible from the start to the end, using a maximum flow method. Each message then follows a route, and no cable carries two messages, so the routes share no cable. The answer matches a simple limit: if cutting some set of cables cuts off the end from the start, every route uses one of those cables, so there are at most as many routes as cut cables. The flow method always reaches that limit.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, and two vertices $s \ne t$. Parallel edges are allowed and count as different edges; antiparallel edges $(u, v)$ and $(v, u)$ are two different edges. Self-loops never lie on a path and can be ignored.

**Output.** A largest set of directed s-t paths $P_1, \dots, P_k$ such that no edge lies on two of them, and its size $k = \lambda(s, t)$. The paths may share vertices.

**Undirected version.** $G$ is undirected and each edge can be used in either direction, but by at most one path. Replace each edge $\{u, v\}$ by the two arcs $(u, v)$ and $(v, u)$, each of capacity 1.

**Capacities.** The basic problem has unit capacities, an integer case. If an edge $e$ may be shared by up to $c(e)$ paths, give it integer capacity $c(e)$; this is the same as $c(e)$ parallel copies.

**Theorem (Menger, edge form).** The largest number of edge-disjoint s-t paths equals the least number of edges whose removal leaves no s-t path. It follows from max-flow min-cut and the [integrality theorem](/flow-integrality-theorem/).

## Variants

- **Vertex-disjoint paths.** Paths must share no vertex other than $s$ and $t$. Split each vertex into an in-copy and an out-copy joined by an edge of capacity 1; see [vertex-disjoint paths](/vertex-disjoint-paths/).
- **Shortest disjoint paths.** Find $k$ edge-disjoint paths of least total length: a [min-cost flow](/min-cost-flow-problem/) of value $k$ with unit capacities, solved by Suurballe's algorithm for $k = 2$.
- **Many terminal pairs.** Given pairs $(s_1, t_1), \dots, (s_k, t_k)$, connect each pair by its own path, with all paths edge-disjoint. This is an integral [multi-commodity flow](/multi-commodity-flow-problem/). In directed graphs it is NP-complete already for $k = 2$ (Fortune, Hopcroft and Wyllie, 1980), and it is NP-complete in undirected graphs when $k$ is part of the input. For fixed $k$ in undirected graphs, the graph minor theory of Robertson and Seymour gives a polynomial algorithm.
- **Edge connectivity.** The least $\lambda(s, t)$ over all pairs is the [edge connectivity](/edge-connectivity/) of the graph.

## Examples

**Greedy fails, flow succeeds.** Take the directed edges $s x_1$, $s x_2$, $x_1 y_1$, $x_1 y_2$, $x_2 y_1$, $y_1 t$, $y_2 t$. If we first pick the path $s\,x_1\,y_1\,t$ and delete its edges, no second path is left: $x_2$ can only reach $y_1$, and $y_1 t$ is used. The maximum flow undoes this choice through the backward arc $(y_1, x_1)$, with the augmenting path $s\,x_2\,y_1\,x_1\,y_2\,t$. The final flow has value 2, and it splits into $s\,x_1\,y_2\,t$ and $s\,x_2\,y_1\,t$. The two edges into $t$ form a cut of size 2, so 2 is optimal.

**An undirected graph and the repair.** Take the undirected edges $s a$, $s b$, $a b$, $a t$, $b t$, giving 10 arcs. A maximum flow may route $s\,a\,b\,t$ and $s\,b\,a\,t$, using both arcs $(a, b)$ and $(b, a)$ of the one edge $a b$. These two paths are edge-disjoint as directed paths but share the undirected edge $\{a, b\}$. Remove one unit from both arcs: conservation still holds at $a$ and $b$, the value stays 2, and the flow becomes $s\,a\,t$ and $s\,b\,t$. In general, whenever an undirected edge carries flow both ways, cancel both; afterwards each edge carries flow in at most one direction, and the decomposition gives paths that share no undirected edge.

**Antiparallel directed edges are different edges.** In a directed graph with edges $s a$, $a b$, $b a$, $a t$, $s b$, $b t$, a path may use $(a, b)$ and another may use $(b, a)$, and they are edge-disjoint; the answer is 2. Do not merge $(a, b)$ and $(b, a)$ into one edge.

**No path.** With the edges $s a$ and $t a$ only, $t$ is not reachable, the answer is 0, and the empty set of edges is a cut. An edge that the instance allows to be shared by 0 paths (capacity 0) is the same as no edge.

**Edge-disjoint is weaker than vertex-disjoint.** The directed edges $s a$, $a v$, $s v$, $v b$, $b t$, $v t$, two triangles that meet at $v$, give 2 edge-disjoint s-t paths ($s\,v\,t$ and $s\,a\,v\,b\,t$), but only 1 vertex-disjoint one, since every path passes through $v$.

## Known algorithms

- **[Ford-Fulkerson](/ford-fulkerson/) with unit capacities.** Each augmenting path adds 1, and $k \le \deg^+(s)$, so $O(km) \subseteq O(nm)$ time for a simple graph.
- **[Dinic's algorithm](/dinic/).** With unit capacities each phase costs $O(m)$, and Even and Tarjan showed there are $O(\min(\sqrt m, n^{2/3}))$ phases: $O(m \min(\sqrt m, n^{2/3}))$ time.
- **Extracting the paths.** Given the 0-1 flow, follow flow edges from $s$, marking each edge used. Every walk reaches $t$, because conservation lets it leave every vertex it enters. A walk may repeat a vertex; cut out the cycle to get a path. All $k$ paths take $O(m)$ time together, as in [flow decomposition](/flow-decomposition/).
- **The minimum cut.** The set $S$ of vertices reachable from $s$ in the final [residual graph](/residual-graph/) gives a cut of $k$ edges, the certificate of optimality.
- **General maximum flow codes**, including the almost-linear algorithm of Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva, apply directly.

## Bounds

The unit capacity bound $O(m \min(\sqrt m, n^{2/3}))$ of Even and Tarjan (1975), also found by Karzanov, was the best for decades; maximum flow algorithms in $m^{1 + o(1)}$ time now solve the problem in almost-linear time. The trivial lower bound is $\Omega(n + m)$, to read the graph.

## Reductions

- **To maximum flow.** Unit capacities, source $s$, sink $t$. Correctness: an integral flow of value $k$ decomposes into $k$ paths and some cycles, each edge used once; conversely, $k$ disjoint paths give an integral flow of value $k$.
- **To Menger's theorem.** The minimum cut of the unit network is the least number of edges separating $t$ from $s$.
- **From bipartite matching.** The network of [bipartite matching](/bipartite-matching/) is a unit network; its edge-disjoint paths are its matching edges, and they are also vertex-disjoint.
- **To edge connectivity.** For an undirected graph and any fixed $s$, the edge connectivity is $\min_{t \ne s} \lambda(s, t)$, so $n - 1$ instances of this problem compute it.

## Applications

Fault-tolerant routing in communication networks (how many cables must fail before two sites lose contact), network reliability measures, the computation of [edge connectivity](/edge-connectivity/), and track or route assignment problems where each track holds one train.

## References
