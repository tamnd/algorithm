---
tag: 8J2ZHT
kind: definition
slug: flow-network
name: Flow network
aliases:
- capacitated network
area: graphs/flows-and-cuts
level: intro
summary: A directed graph with edge capacities and designated source and sink.
prereqs: [directed-graph, weighted-graph]
see_also: [s-t-flow, flow-conservation, cut, cut-capacity, residual-graph, max-flow-problem, min-cut-problem, circulation-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.1, Flow networks (the definition, the rule against antiparallel edges, and networks with several sources and sinks)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.1, The Maximum-Flow Problem and the Ford-Fulkerson Algorithm (flow networks and flows)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (flows, cuts and the reductions of undirected and vertex-capacitated networks)
  - paper: doi:10.4153/CJM-1956-045-5
    title: L. R. Ford Jr. and D. R. Fulkerson, Maximal flow through a network, Canadian Journal of Mathematics 8, 399 to 404 (1956)
    locator: the whole paper (the network with capacities, a source and a sink)
---

A flow network is a [directed graph](/directed-graph/) in which each edge has a nonnegative capacity, together with two distinct vertices: a source $s$, where the flow starts, and a sink $t$, where it ends. It is the input of the [maximum flow problem](/max-flow-problem/) and of the [minimum cut problem](/min-cut-problem/), and the frame in which [s-t flows](/s-t-flow/), [cuts](/cut/) and [residual graphs](/residual-graph/) are defined. The capacity of an edge is the largest amount of flow that the edge can carry.

## Definition

A **flow network** is a tuple $N = (G, c, s, t)$ where

- $G = (V, E)$ is a finite directed graph with $n = |V|$ vertices and $m = |E|$ edges;
- $c : E \to \mathbb{R}_{\ge 0}$ gives each edge $e$ a **capacity** $c(e) \ge 0$;
- $s \in V$ is the **source** and $t \in V$ is the **sink**, with $s \ne t$.

It is convenient to extend $c$ to all ordered pairs: $c(u, v) = 0$ when $(u, v) \notin E$. With this convention a zero-capacity edge and a missing edge are the same for every question about flows.

**Capacities.** The general definition allows any nonnegative real capacities. Many results need more. The [integrality theorem](/flow-integrality-theorem/) and the termination of the [Ford-Fulkerson method](/ford-fulkerson/) need integer (or rational) capacities. Some authors also allow $c(e) = \infty$; an infinite edge can be replaced by an edge whose capacity is the sum of all finite capacities plus one, which no minimum cut can use.

**Direction.** The edges are directed. An undirected edge $\{u, v\}$ of capacity $c$ stands for two directed edges $(u, v)$ and $(v, u)$, each of capacity $c$. A flow on the two edges that goes both ways can be cancelled to a flow that goes one way only, so this replacement keeps the maximum flow value and the minimum cut value.

**Antiparallel edges.** Two edges $(u, v)$ and $(v, u)$ are *antiparallel*. CLRS forbids them in a flow network, to keep one residual edge per ordered pair. A network with antiparallel edges is turned into one without them by splitting one edge $(u, v)$ into $(u, x)$ and $(x, v)$ through a new vertex $x$, both with capacity $c(u, v)$. Implementations usually keep the antiparallel edges and give each edge its own reverse residual edge instead; this is the convention of the pages in this area unless a page says otherwise. Parallel edges (two edges $(u, v)$) can be merged by adding their capacities.

**Assumptions in many texts.** Some books also assume that no edge enters $s$, no edge leaves $t$, and each vertex lies on some path from $s$ to $t$. None of these is needed for the definitions on this site. Edges into $s$ or out of $t$ can carry flow in an [s-t flow](/s-t-flow/), but they never help a maximum flow, and the cut capacity ignores edges that go from the sink side to the source side.

**Several sources and sinks.** A network with sources $s_1, \ldots, s_k$ and sinks $t_1, \ldots, t_\ell$ becomes a flow network by adding a super-source $s$ with edges $(s, s_i)$ and a super-sink $t$ with edges $(t_j, t)$ of capacity $\infty$ (or of the supply of $s_i$ and the demand of $t_j$, when those are given).

## Examples and non-examples

**A small network.** Take $V = \{s, a, b, c, d, t\}$ and the nine edges

| edge | $s a$ | $s c$ | $a b$ | $a c$ | $a d$ | $c d$ | $d b$ | $b t$ | $d t$ |
|---|---|---|---|---|---|---|---|---|---|
| capacity | 10 | 10 | 4 | 2 | 8 | 9 | 6 | 10 | 10 |

The capacities are integers, there are no antiparallel edges, and every vertex lies on a path from $s$ to $t$. The [maximum flow](/max-flow-problem/) has value 19, and the [cut](/cut/) $(\{s, c\}, \{a, b, d, t\})$ has [capacity](/cut-capacity/) $c(s, a) + c(c, d) = 10 + 9 = 19$, so it is a minimum cut. The other pages of this area use this network as their running example.

**A network with no path from $s$ to $t$.** $V = \{s, a, t\}$ with the edges $(s, a)$ of capacity 5 and $(t, a)$ of capacity 5. This is a valid flow network. Each flow has value 0, and the cut $(\{s, a\}, \{t\})$ has capacity 0, because no edge leaves $\{s, a\}$.

**A zero-capacity edge.** Adding $(a, t)$ with capacity 0 to the last network gives a path $s \to a \to t$ in $G$, but no flow can use it. The network is still valid and the maximum flow is still 0. An algorithm that looks for paths in $G$ instead of in the [residual graph](/residual-graph/) with positive residual capacity gets this case wrong.

**Antiparallel edges.** $V = \{s, a, b, t\}$ with $(s, a)$ 3, $(a, b)$ 2, $(b, a)$ 1, $(b, t)$ 2 and $(s, b)$ 1. The pair $(a, b), (b, a)$ is antiparallel. In the CLRS form, $(b, a)$ becomes $(b, x)$ and $(x, a)$ with capacity 1. The maximum flow value is 2 in both forms: all flow into $t$ must cross $(b, t)$, which has capacity 2.

**Real capacities.** Capacities $c(s, a) = \sqrt 2$ and $c(a, t) = 1$ give a valid network with maximum flow value 1. The value of a maximum flow is always the minimum of a finite set of cut capacities, so it is a sum of capacities and need not be an integer when the capacities are not.

**Non-example: $s = t$.** With $s = t$ there is no cut that separates them, and the value of a flow is not defined. The definition requires $s \ne t$.

**Non-example: a negative capacity.** $c(e) < 0$ makes the feasible set empty, since a flow needs $0 \le f(e) \le c(e)$. Lower bounds on the flow of an edge belong to a different model, the [circulation with demands](/circulation-problem/).

**Non-example: capacities on vertices.** A limit on the flow through a vertex is not part of this definition. It is reduced to an edge capacity by splitting the vertex, as on the page [vertex capacities](/vertex-capacities-flow/).

## Related definitions

- An [s-t flow](/s-t-flow/) is an assignment of values to the edges of a flow network that respects the capacities and [flow conservation](/flow-conservation/).
- A [cut](/cut/) splits the vertices into a side with $s$ and a side with $t$; its [capacity](/cut-capacity/) is the total capacity of the edges from the first side to the second.
- The [residual graph](/residual-graph/) of a flow holds the remaining capacities and the reverse edges that undo flow.
- The [max-flow min-cut theorem](/max-flow-min-cut-theorem/) says that the largest flow value equals the smallest cut capacity in every flow network.
- A [circulation](/circulation-problem/) generalizes the network: it has lower bounds on the edges and supplies and demands on the vertices instead of one source and one sink.
- The [min-cost flow problem](/min-cost-flow-problem/) adds a cost per unit of flow on each edge.

## References
