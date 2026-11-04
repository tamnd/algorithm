---
tag: BJJ7QW
kind: technique
slug: vertex-splitting
name: Vertex splitting
aliases:
- node splitting
area: techniques/reductions-and-transforms
level: core
summary: Replacing each vertex by an in-copy and out-copy joined by an edge, so vertex capacities become edge capacities in a flow network.
prereqs: [flow-network, max-flow-problem, directed-graph, max-flow-min-cut-theorem]
see_also: [vertex-capacities-flow, vertex-disjoint-paths, edge-disjoint-paths, menger-theorem, vertex-cut, vertex-connectivity, flow-decomposition, minimum-path-cover-problem]
sources:
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications, Prentice Hall, 1993
    locator: Section 2.4, Network transformations (node splitting)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Chapter 7, Network flow (disjoint paths, and the exercises on node capacities)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 24, Maximum flow (the exercise on flow networks with vertex capacities)
---

Vertex splitting is a [reduction](/reduction/) that turns a limit on a vertex into a limit on an edge. Each vertex $v$ is replaced by two vertices $v_{\text{in}}$ and $v_{\text{out}}$ joined by one edge $v_{\text{in}} \to v_{\text{out}}$; every edge that entered $v$ now enters $v_{\text{in}}$, and every edge that left $v$ now leaves $v_{\text{out}}$. All flow through $v$ must then use the new edge, so its capacity acts as the [capacity of the vertex](/vertex-capacities-flow/). With it, any [maximum flow](/max-flow-problem/) algorithm handles vertex capacities, finds [vertex-disjoint paths](/vertex-disjoint-paths/), and computes a minimum [vertex cut](/vertex-cut/).

## In plain words

Flow algorithms limit how much can pass along each road, but not how much can pass through each town. To limit a town, cut it in two halves: an arrival half and a departure half. All roads that came into the town now come into the arrival half. All roads that left the town now leave from the departure half. Join the two halves with one new road, and give that road the limit of the town. Now anything that passes through the town must use the new road, so the town limit is a road limit, and the usual flow algorithm handles it. The same trick, with a limit of one for each town, makes paths that never share a town.

## When it applies

- A [flow network](/flow-network/) has a limit on the total flow that passes through some vertices, as well as (or instead of) limits on the edges.
- You want paths that share no internal vertex, rather than paths that share no edge: [Menger's theorem](/menger-theorem/) in its vertex form, [vertex connectivity](/vertex-connectivity/), or routing with node failures.
- You want a minimum set of vertices whose removal separates $s$ from $t$.
- A vertex has a cost or a weight, and the algorithm you want to use handles only costs on edges, as in min-cost flow with node costs or shortest paths with node weights.

## The template

The input is a directed graph $G = (V, E)$ with source $s$, sink $t$, edge capacities $c(e) \in \mathbb{Z}_{\ge 0} \cup \{\infty\}$ and vertex capacities $c(v) \in \mathbb{Z}_{\ge 0} \cup \{\infty\}$ for $v \in V \setminus \{s, t\}$. The source and the sink are not split. For uniform notation, write $s_{\text{out}} = s$ and $t_{\text{in}} = t$.

```pseudo id=main
SPLIT(G, s, t, c)
L1  V' ← {s, t};  E' ← ∅
L2  for each vertex v ∉ {s, t} do
L3      add v_in and v_out to V'
L4      add the edge v_in → v_out with capacity c(v) to E'   ▷ the vertex limit
L5  for each edge (u, v) ∈ E do
L6      add u_out → v_in with capacity c(u, v) to E'        ▷ the edge limit
L7  return G' = (V', E')
```

Then run a max-flow algorithm on $G'$ from $s$ to $t$. $G'$ has $2n - 2$ vertices and $m + n - 2$ edges, so the bound of the max-flow algorithm changes only by a constant factor. An edge of $G$ that enters $s$ becomes an edge into $s$, and an edge that leaves $t$ becomes an edge out of $t$.

A *flow with vertex capacities* in $G$ is a function $f : E \to \mathbb{R}_{\ge 0}$ with $f(e) \le c(e)$ for every edge, conservation $f^{\text{in}}(v) = f^{\text{out}}(v)$ at every $v \ne s, t$, and $f^{\text{in}}(v) \le c(v)$ at every $v \ne s, t$. Here $f^{\text{in}}(v)$ is the sum of $f$ over the edges into $v$ and $f^{\text{out}}(v)$ the sum over the edges out of $v$. Its value $v(f)$ is $f^{\text{out}}(s) - f^{\text{in}}(s)$.

**Lemma (correspondence).** The map $\Phi$ with

$$\Phi(f)(u_{\text{out}}, v_{\text{in}}) = f(u, v), \qquad \Phi(f)(v_{\text{in}}, v_{\text{out}}) = f^{\text{in}}(v)$$

is a bijection from the flows with vertex capacities in $G$ to the flows in $G'$. It keeps the value, and it maps integer flows to integer flows. Hence the maximum flow value of $G$ with vertex capacities equals the maximum flow value of $G'$.

*Proof.* Let $f$ be a flow with vertex capacities in $G$ and $f' = \Phi(f)$. Edge capacities: $f'(u_{\text{out}}, v_{\text{in}}) = f(u, v) \le c(u, v)$, and $f'(v_{\text{in}}, v_{\text{out}}) = f^{\text{in}}(v) \le c(v)$. Conservation at $v_{\text{in}}$: the edges into $v_{\text{in}}$ are the images of the edges into $v$, so the flow in is $f^{\text{in}}(v)$, and the only edge out carries $f^{\text{in}}(v)$. Conservation at $v_{\text{out}}$: the only edge in carries $f^{\text{in}}(v)$, and the edges out are the images of the edges out of $v$, which carry $f^{\text{out}}(v) = f^{\text{in}}(v)$ in total. The edges at $s$ are the images of the edges at $s$ with the same values, so $v(f') = v(f)$.

Conversely, let $f'$ be a flow in $G'$ and define $f(u, v) = f'(u_{\text{out}}, v_{\text{in}})$. Then $f(u, v) \le c(u, v)$. For $v \ne s, t$, conservation at $v_{\text{in}}$ gives $f^{\text{in}}(v) = f'(v_{\text{in}}, v_{\text{out}}) \le c(v)$, and conservation at $v_{\text{out}}$ gives $f'(v_{\text{in}}, v_{\text{out}}) = f^{\text{out}}(v)$. So $f$ is a flow with vertex capacities, and $\Phi(f) = f'$, because the value of $f'$ on each internal edge is forced by conservation at $v_{\text{in}}$. The two maps are inverse to each other, and both keep integer values. $\square$

**Corollary (cuts).** By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) in $G'$, the maximum flow value with vertex capacities equals the minimum of $\sum_{e \in F} c(e) + \sum_{v \in U} c(v)$ over sets $F \subseteq E$ and $U \subseteq V \setminus \{s, t\}$ whose removal leaves no $s$-$t$ path in $G$. Each edge of $G'$ is either the image $u_{\text{out}} \to v_{\text{in}}$ of an edge $(u, v)$ or the internal edge $v_{\text{in}} \to v_{\text{out}}$ of a vertex $v$. The $s$-$t$ paths of $G$ and of $G'$ correspond one to one, with $v$ on the path in $G$ exactly when $v_{\text{in}} \to v_{\text{out}}$ is on the path in $G'$. So a set of edges of $G'$ meets every $s$-$t$ path of $G'$ exactly when the matching sets $F$ and $U$ meet every $s$-$t$ path of $G$, and the edges that leave the source side of a minimum cut form such a set.

### Vertex-disjoint paths

Give every internal edge capacity $1$ and every original edge capacity $1$ (or $\infty$). An integer maximum flow in $G'$ of value $k$ splits, by [flow decomposition](/flow-decomposition/), into $k$ paths from $s$ to $t$ and some cycles. Each internal edge $v_{\text{in}} \to v_{\text{out}}$ carries at most $1$, so at most one of the paths passes through $v$. Contracting each pair $v_{\text{in}}, v_{\text{out}}$ back to $v$ gives $k$ paths in $G$ that share no vertex other than $s$ and $t$. Conversely, $k$ such paths in $G$ give an integer flow of value $k$ in $G'$. So the maximum number of [vertex-disjoint paths](/vertex-disjoint-paths/) is a maximum flow value. With $\infty$ on the original edges and $s, t$ not adjacent, the minimum cut uses only internal edges, and the corollary gives the vertex form of Menger's theorem: the maximum number of internally vertex-disjoint $s$-$t$ paths equals the minimum size of a vertex set that separates $s$ from $t$.

### Worked example: vertex capacities

The graph $G$ has edges with capacities $s{\to}a\ 5$, $s{\to}b\ 4$, $a{\to}c\ 3$, $a{\to}d\ 4$, $b{\to}c\ 4$, $b{\to}d\ 2$, $c{\to}t\ 6$, $d{\to}t\ 5$, and vertex capacities $c(a) = 4$, $c(b) = 3$, $c(c) = 4$, $c(d) = 6$. Without the vertex capacities the maximum flow is $9$, the total capacity out of $s$. The split graph $G'$ has $10$ vertices and $12$ edges, and its maximum flow is $7$:

| edge of $G'$ | capacity | flow |
|---|---|---|
| $s \to a_{\text{in}}$ | 5 | 4 |
| $s \to b_{\text{in}}$ | 4 | 3 |
| $a_{\text{in}} \to a_{\text{out}}$ | 4 | 4 |
| $b_{\text{in}} \to b_{\text{out}}$ | 3 | 3 |
| $a_{\text{out}} \to c_{\text{in}}$ | 3 | 3 |
| $a_{\text{out}} \to d_{\text{in}}$ | 4 | 1 |
| $b_{\text{out}} \to c_{\text{in}}$ | 4 | 1 |
| $b_{\text{out}} \to d_{\text{in}}$ | 2 | 2 |
| $c_{\text{in}} \to c_{\text{out}}$ | 4 | 4 |
| $d_{\text{in}} \to d_{\text{out}}$ | 6 | 3 |
| $c_{\text{out}} \to t$ | 6 | 4 |
| $d_{\text{out}} \to t$ | 5 | 3 |

The minimum cut of $G'$ is $\{a_{\text{in}} \to a_{\text{out}},\ b_{\text{in}} \to b_{\text{out}}\}$ with capacity $4 + 3 = 7$. In $G$ it means: removing the vertices $a$ and $b$ separates $s$ from $t$, at cost $7$.

### Worked example: edge-disjoint is not vertex-disjoint

Take the "bow tie" with edges $s{\to}a$, $s{\to}b$, $a{\to}v$, $b{\to}v$, $v{\to}c$, $v{\to}d$, $c{\to}t$, $d{\to}t$. With unit edge capacities the maximum flow is $2$: the paths $s, a, v, c, t$ and $s, b, v, d, t$ share no edge. Both pass through $v$. After splitting with unit vertex capacities and $\infty$ on the original edges ($12$ vertices, $13$ edges), the maximum flow is $1$, and $\{v\}$ is a minimum vertex cut.

## Classic examples

- **[Vertex capacities in flow networks](/vertex-capacities-flow/).** The direct use: split, then run any max-flow algorithm.
- **[Vertex-disjoint paths](/vertex-disjoint-paths/) and [Menger's theorem](/menger-theorem/).** Unit vertex capacities turn the edge-disjoint version ([edge-disjoint paths](/edge-disjoint-paths/)) into the vertex-disjoint one.
- **[Vertex connectivity](/vertex-connectivity/).** The [Even-Tarjan algorithm](/even-tarjan-vertex-connectivity/) computes the vertex connectivity of a graph with max-flow computations on the split graph, one for each of a set of pairs of non-adjacent vertices.
- **[Minimum path cover](/minimum-path-cover-problem/) in a DAG.** The same split, with $v_{\text{out}}$ on the left and $v_{\text{in}}$ on the right and no internal edge, gives a bipartite graph, and a [maximum matching](/path-cover-by-bipartite-matching/) in it gives the cover.
- **Node costs.** For [min-cost flow](/min-cost-flow-problem/) or shortest paths with a cost on each vertex, put the cost on the internal edge.

## Variations

- **Undirected graphs.** Replace each undirected edge $\{u, v\}$ of capacity $c$ by the two arcs $u_{\text{out}} \to v_{\text{in}}$ and $v_{\text{out}} \to u_{\text{in}}$, each of capacity $c$. The internal edge stays directed from $v_{\text{in}}$ to $v_{\text{out}}$.
- **Only vertex limits.** When the edges have no limit, give the original edges capacity $\infty$ (or any number at least the total vertex capacity), so that a minimum cut never uses them.
- **Lower bounds on vertices.** A lower bound $\ell(v)$ on the flow through $v$ becomes a lower bound on the internal edge, and the usual reduction for edge lower bounds applies.
- **Splitting only some vertices.** Only the vertices with a finite capacity or a cost need to be split. The others can stay as single vertices.

## Pitfalls

- **Do not limit the source or the sink.** If $s$ and $t$ are split with a finite internal capacity, that capacity bounds the flow value. Keep them whole, as in the template, or give their internal edges capacity $\infty$.
- **Edges go out of $u_{\text{out}}$ and into $v_{\text{in}}$.** An edge $u_{\text{in}} \to v_{\text{in}}$ or $u_{\text{out}} \to v_{\text{out}}$ lets flow skip a vertex limit.
- **Undirected internal edges.** In an undirected graph, making the edge between $v_{\text{in}}$ and $v_{\text{out}}$ undirected, or joining $u$ and $v$ by one undirected edge between copies, lets flow bypass the vertex. Turn each undirected edge into two arcs first, then split as in the template.
- **Adjacent $s$ and $t$.** With unit vertex capacities and $\infty$ on the edges, an edge $s \to t$ gives infinite flow, and no vertex set separates $s$ from $t$. Menger's vertex form assumes that $s$ and $t$ are not adjacent. To count disjoint paths, give the edge $s \to t$ capacity $1$, so that it counts as one path.
- **Vertex capacity counts the flow through, not the degree.** The internal edge limits $f^{\text{in}}(v)$, the total that passes $v$. It does not limit the number of edges at $v$ that carry flow.
- **Counting paths needs an integer flow.** Use an algorithm that returns an integer maximum flow (any augmenting path method does, by the [integrality theorem](/flow-integrality-theorem/)) before decomposing it into paths.

## Exercises

1. In the first worked example, change $c(a)$ to $\infty$. What is the new maximum flow, and which cut proves it?
2. Prove that the minimum number of vertices whose removal separates non-adjacent vertices $s$ and $t$ in an undirected graph equals the maximum number of internally vertex-disjoint $s$-$t$ paths, using the split graph.
3. A graph has a cost on each vertex and on each edge. Reduce the cheapest $s$-$t$ path to a shortest path problem with costs on edges only.
4. Give a directed graph in which the maximum number of edge-disjoint $s$-$t$ paths is $k$ and the maximum number of vertex-disjoint ones is $1$, for any $k \ge 1$.
5. Show that splitting only the vertices with finite capacity gives the same maximum flow value as splitting all of them.

## References
