---
tag: 6C247H
kind: technique
slug: vertex-capacities-flow
name: Vertex capacities in flow networks
aliases:
- Vertex capacities
area: graphs/flows-and-cuts
level: core
summary: Models limits on the flow through a vertex by splitting each vertex into an in-node and an out-node joined by an edge with that capacity.
prereqs: [max-flow-problem, flow-network, min-cut-problem]
see_also: [vertex-splitting, vertex-disjoint-paths, menger-theorem, vertex-cut, vertex-connectivity, path-cover-by-bipartite-matching, edge-disjoint-paths, max-flow-min-cut-theorem]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 11, Applications of Flows and Cuts (vertex capacities and vertex-disjoint paths)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 2, Paths, Trees, and Cycles (network transformations, node splitting)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 9, Disjoint paths (the vertex-disjoint form of Menger's theorem, derived from the arc-disjoint form)
---

A flow network with vertex capacities limits the total flow that may pass through each vertex, in addition to or instead of limits on the edges. The standard technique is [vertex splitting](/vertex-splitting/): replace each vertex $v$ by an in-copy $v_{\mathrm{in}}$ and an out-copy $v_{\mathrm{out}}$, joined by one edge whose capacity is the vertex capacity, and send every edge into $v$ to $v_{\mathrm{in}}$ and every edge out of $v$ from $v_{\mathrm{out}}$. A [maximum flow](/max-flow-problem/) of the new network is a maximum flow of the old one that respects the vertex limits, and a [minimum cut](/min-cut-problem/) of the new network may cut vertices as well as edges. This gives [vertex-disjoint paths](/vertex-disjoint-paths/), the vertex form of [Menger's theorem](/menger-theorem/), and minimum [vertex cuts](/vertex-cut/).

## In plain words

Sometimes the bottleneck is not a road but a town: a junction that can only handle so many cars per hour, or a router with a limited speed. Flow networks only put limits on links, not on points.

The trick is to turn each town into a short road. Cut the town in two halves: an entrance where all incoming roads arrive, and an exit where all outgoing roads leave. Join entrance to exit by one new road with the town's limit. Every car that passes through the town now uses that road, so the town's limit becomes a road limit, and the usual flow methods apply.

## When it applies

- The network is directed, or undirected with each edge replaced by two opposite directed edges.
- Each vertex $v$ may have a capacity $c(v) \ge 0$, real or integer, on the flow that passes through it; vertices without one get $\infty$. Edges may keep their own capacities.
- The question is about flow value, disjoint paths, or the cheapest set of vertices and edges that separates $s$ from $t$.
- The capacity of $s$ and $t$ themselves is usually $\infty$. If it is finite, it bounds the total flow, and the split handles it the same way.

The technique does not apply when the vertex limit depends on the direction of passage, or when it limits inflow and outflow separately in a way that is not the same number; then split into more copies.

## The template

```pseudo id=main
VERTEX-CAPACITATED-MAX-FLOW(G, c_E, c_V, s, t)
L1  for each vertex v of G do
L2      add vertices v_in and v_out to G′, and the edge v_in → v_out with capacity c_V(v)  (∞ if v has no limit)
L3  for each edge (u, v) of G do
L4      add the edge u_out → v_in to G′ with capacity c_E(u, v)
L5  f′ ← a maximum flow of G′ from s_in to t_out
L6  for each edge (u, v) of G do f(u, v) ← f′(u_out → v_in)
L7  return f; the throughput of v is f′(v_in → v_out)
```

$G'$ has $2n$ vertices and $n + m$ edges. Parallel edges of $G$ stay parallel in $G'$. An antiparallel pair $(u, v)$, $(v, u)$ becomes $u_{\mathrm{out}} \to v_{\mathrm{in}}$ and $v_{\mathrm{out}} \to u_{\mathrm{in}}$, which are no longer antiparallel; each keeps its own flow. A self-loop $(v, v)$ becomes $v_{\mathrm{out}} \to v_{\mathrm{in}}$, which closes a cycle with the split edge and can carry no useful flow; drop it.

**Why it works.** *Flows.* Let $f$ be a flow in $G$ that obeys the edge capacities and puts at most $c_V(v)$ through each $v \ne s, t$. Define $f'$ by $f'(u_{\mathrm{out}} \to v_{\mathrm{in}}) = f(u, v)$ and $f'(v_{\mathrm{in}} \to v_{\mathrm{out}})$ equal to the inflow of $v$ (which equals its outflow). Conservation at $v_{\mathrm{in}}$ and at $v_{\mathrm{out}}$ is conservation at $v$, and the split edge obeys its capacity. At $s$ and $t$ set the split edge to the outflow of $s$ and the inflow of $t$, with no edges into $s$ or out of $t$ carrying flow in an optimal solution (otherwise cancel). Conversely, each flow $f'$ of $G'$ gives $f$ by line L6, with throughput $f'(v_{\mathrm{in}} \to v_{\mathrm{out}}) \le c_V(v)$. The values agree. So the maximum values agree.

*Cuts.* A finite cut of $G'$ cuts some split edges, which are vertices of $G$, and some edges $u_{\mathrm{out}} \to v_{\mathrm{in}}$, which are edges of $G$. Removing those vertices and edges from $G$ leaves no $s$-$t$ path. So the max-flow min-cut theorem of $G'$ reads: the maximum flow under vertex and edge capacities equals the minimum total capacity of a set of vertices and edges whose removal separates $s$ from $t$. To cut only vertices, give the edges capacity $\infty$.

## Classic examples

**The running example.** Take $s \to a$ (3), $s \to b$ (2), $a \to b$ (1), $a \to t$ (2), $b \to t$ (3), whose maximum flow is 5 without vertex limits. With $c_V(a) = 2$, the maximum flow is 4: the cut cuts the split edge $a_{\mathrm{in}} \to a_{\mathrm{out}}$ (2) and the edge $s \to b$ (2). With $c_V(a) = 0$, all flow avoids $a$, and the maximum is 2 through $s \to b$. With $c_V(a) = c_V(b) = 0$, there is no $s$-$t$ path in $G'$, and the maximum is 0.

**[Vertex-disjoint paths](/vertex-disjoint-paths/).** Give every vertex other than $s$ and $t$ capacity 1 and every edge capacity 1 (or $\infty$). An integral flow of value $k$ is $k$ $s$-$t$ paths that share no inner vertex. With the max-flow min-cut theorem this is Menger's theorem for vertices: the largest number of such paths equals the smallest vertex cut, when $s$ and $t$ are not adjacent.

**[Vertex connectivity](/vertex-connectivity/).** The vertex connectivity of a graph is the least vertex cut over pairs of non-adjacent vertices, found with split flows.

**Minimum-weight vertex separator.** With vertex weights as capacities and $\infty$ on edges, a minimum cut is a cheapest set of vertices whose removal separates $s$ from $t$.

**Path covers of a DAG.** The [minimum path cover](/path-cover-by-bipartite-matching/) of a directed acyclic graph splits each vertex into an out-copy and an in-copy and matches them, the same construction without the split edge.

## Variations

- **Lower bounds on vertices.** A vertex that must carry at least $\ell(v)$ gets a split edge with bounds $[\ell(v), c_V(v)]$, handled as a [circulation with lower bounds](/circulation-problem/).
- **Vertex costs.** In a [minimum-cost flow](/min-cost-flow-problem/), a cost per unit through $v$ goes on the split edge.
- **Undirected graphs.** Replace each edge $\{u, v\}$ by $u_{\mathrm{out}} \to v_{\mathrm{in}}$ and $v_{\mathrm{out}} \to u_{\mathrm{in}}$. Flow in both directions through the same edge can be cancelled, so this models an undirected capacity correctly.
- **Separate in and out limits.** Split into three copies: in, middle, out.

## Pitfalls

- **Splitting $s$ and $t$ with capacity 1.** In disjoint path problems, $s$ and $t$ are shared by all paths; their split edges need $\infty$. Otherwise the answer is at most 1.
- **Using the wrong ends.** The source of $G'$ is $s_{\mathrm{in}}$ (or $s_{\mathrm{out}}$ if $s$ is unlimited) and the sink is $t_{\mathrm{out}}$ (or $t_{\mathrm{in}}$). Edges must go from out-copies to in-copies; an edge $u_{\mathrm{in}} \to v_{\mathrm{in}}$ bypasses the limit of $u$.
- **Adjacent $s$ and $t$.** An edge $s \to t$ needs no inner vertex, so no vertex cut separates them. The vertex form of Menger's theorem assumes they are not adjacent.
- **A vertex capacity of 0.** Its split edge has capacity 0, which simply blocks the vertex. This is correct, and it is how to delete a vertex without rebuilding the graph.
- **Reading the cut.** A minimum cut of $G'$ is a mix of vertices and edges. To report only vertices, give the edges capacity $\infty$ first.

## References
