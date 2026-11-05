---
tag: DN2MY5
kind: problem
slug: max-flow-problem
name: Maximum flow problem
aliases:
- max-flow
- maximum flow
area: graphs/flows-and-cuts
level: intro
summary: Find a feasible s-t flow of maximum value in a capacitated network.
prereqs: [s-t-flow, flow-network]
see_also: [min-cut-problem, max-flow-min-cut-theorem, residual-graph, ford-fulkerson, dinic, push-relabel, min-cost-flow-problem, bipartite-matching]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 24, Maximum Flow (Section 24.1 for the problem and the networks with several sources and sinks, Section 24.2 for Ford-Fulkerson and Edmonds-Karp, Section 24.3 for bipartite matching, and the chapter notes for the history of the bounds)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Chapter 7, Network Flow (Sections 7.1 to 7.3 for the problem and the augmenting-path algorithms, Section 7.4 for preflow-push, Sections 7.5 to 7.12 for the applications)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapters 6 to 8, Maximum Flows (basic ideas, polynomial algorithms, additional topics)
  - paper: doi:10.4153/CJM-1956-045-5
    title: L. R. Ford Jr. and D. R. Fulkerson, Maximal flow through a network, Canadian Journal of Mathematics 8, 399 to 404 (1956)
    locator: the whole paper (the problem, the minimal cut theorem, and the labeling method)
  - url: "https://arxiv.org/abs/2203.00671"
    locator: Li Chen, Rasmus Kyng, Yang P. Liu, Richard Peng, Maximilian Probst Gutenberg and Sushant Sachdeva, Maximum Flow and Minimum-Cost Flow in Almost-Linear Time, FOCS 2022 (the main theorem, m^(1+o(1)) time for integer capacities)
  - paper: doi:10.1145/2488608.2488705
    title: James B. Orlin, Max flows in O(nm) time, or better, STOC 2013, 765 to 774
    locator: the main result (O(nm) time, combined with King, Rao and Tarjan for dense graphs)
---

The maximum flow problem asks, for a [flow network](/flow-network/) with a source $s$ and a sink $t$, for an [$s$-$t$ flow](/s-t-flow/) of the largest possible value. Its dual is the [minimum $s$-$t$ cut problem](/min-cut-problem/), and the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) says that the two optima are equal. It is solved in polynomial time by augmenting paths ([Ford-Fulkerson](/ford-fulkerson/), [Edmonds-Karp](/edmonds-karp/), [Dinic](/dinic/)), by [push-relabel](/push-relabel/), and since 2022 in almost-linear time. Many problems reduce to it, among them [bipartite matching](/bipartite-matching/), [disjoint paths](/edge-disjoint-paths/) and [image segmentation](/image-segmentation-graph-cuts/).

## In plain words

A network of one-way pipes joins a source of water to a drain. Each pipe has a limit on how much water per second it can carry. At each joint, the water that comes in must also go out. How much water per second can you move from the source to the drain, and how should each pipe be used?

The answer is limited by the narrow places of the network. If you split the joints into a source part and a drain part, all water must cross the pipes that go from the first part to the second. So the total of their limits is a ceiling. The main theorem of the area says that the best plan always reaches the lowest such ceiling.

## Definition

**Input.** A flow network $N = (G, c, s, t)$: a finite directed graph $G = (V, E)$ with $n = |V|$ and $m = |E|$, capacities $c : E \to \mathbb{R}_{\ge 0}$, and two vertices $s \ne t$. Parallel edges, antiparallel edges and edges of capacity 0 are allowed. Capacities are real unless a variant says otherwise; many bounds below assume integers in $\{0, 1, \ldots, U\}$.

**Output.** An $s$-$t$ flow $f : E \to \mathbb{R}$, with $0 \le f(e) \le c(e)$ and conservation at each $v \notin \{s, t\}$, such that

$$|f| = f^{\mathrm{out}}(s) - f^{\mathrm{in}}(s)$$

is the largest over all $s$-$t$ flows. The value of such a flow is written $f^{*}$ or $\mathrm{maxflow}(N)$.

**A maximum exists.** The set of flows is a polytope in $\mathbb{R}^{E}$: it is defined by finitely many linear inequalities and equations, it holds the zero flow, and it lies in the box $\prod_e [0, c(e)]$. So it is nonempty and compact, and the linear function $|f|$ reaches its maximum on it. With integer capacities, some maximum flow is integral; this is the [integrality theorem](/integrality-theorem/).

**Linear program.** In matrix form the problem is: maximize $\sum_{e \in \delta^{\mathrm{out}}(s)} x_e - \sum_{e \in \delta^{\mathrm{in}}(s)} x_e$ subject to $\sum_{e \in \delta^{\mathrm{in}}(v)} x_e = \sum_{e \in \delta^{\mathrm{out}}(v)} x_e$ for $v \notin \{s, t\}$ and $0 \le x_e \le c(e)$. See the [max-flow LP formulation](/max-flow-lp-formulation/) and [max-flow min-cut duality](/min-cut-max-flow-duality/).

## Variants

- **Value only, or a flow, or a cut.** Some uses need only $f^{*}$; most algorithms return a flow, and a [minimum cut](/min-cut-problem/) follows from it in $O(n + m)$ time.
- **Decision version.** Given $k$, is there a flow of value at least $k$? It is in P.
- **Integer capacities.** The algorithms then return an integral maximum flow, which the combinatorial reductions need.
- **Unit capacities.** Each $c(e) = 1$. The maximum is the number of [edge-disjoint paths](/edge-disjoint-paths/). Dinic's algorithm runs in $O(m \min(\sqrt{m}, n^{2/3}))$ time here.
- **Undirected networks.** Replace each undirected edge of capacity $k$ by two opposite directed edges of capacity $k$. A maximum flow never needs to use both of them in a positive amount, as the two flows can be cancelled.
- **Several sources and sinks.** Add a super source with an edge of capacity $\infty$ to each source, and a super sink in the same way.
- **Vertex capacities.** Split each vertex into an in-copy and an out-copy: [vertex capacities](/vertex-capacities-flow/).
- **Lower bounds on edges.** The feasibility question becomes a [circulation problem](/circulation-problem/).
- **Costs.** The cheapest flow of a given value: the [min-cost flow problem](/min-cost-flow-problem/).
- **Several commodities.** [Multi-commodity flow](/multi-commodity-flow-problem/), which is a different and harder problem.
- **Changing networks.** [Parametric](/parametric-max-flow-problem/) and [dynamic](/dynamic-max-flow-problem/) maximum flow.

## Examples

The running example has the vertices $s, a, b, c, d, t$ and the edges $s \to a$ (10), $s \to b$ (10), $a \to b$ (2), $a \to c$ (4), $a \to d$ (8), $b \to d$ (9), $d \to c$ (6), $c \to t$ (10), $d \to t$ (10).

| edge | $s a$ | $s b$ | $a b$ | $a c$ | $a d$ | $b d$ | $d c$ | $c t$ | $d t$ |
|---|---|---|---|---|---|---|---|---|---|
| capacity | 10 | 10 | 2 | 4 | 8 | 9 | 6 | 10 | 10 |
| a maximum flow | 10 | 9 | 0 | 4 | 6 | 9 | 5 | 9 | 10 |

The value is $f^{*} = 19$. The cut $S = \{s, b\}$ has capacity $c(s, a) + c(b, d) = 10 + 9 = 19$; the edge $a \to b$ enters $S$ and does not count. So no flow is larger.

- **An antiparallel edge.** Add $b \to a$ (5). The flow can now use $s \to b \to a$, and $f^{*}$ rises to 20, the capacity of the cut $\{s\}$.
- **Zero-capacity edges.** Set $c(c, t) = c(d, t) = 0$. Then $t$ has no entering edge of positive capacity, and $f^{*} = 0$; the zero flow is a maximum flow, and $S = V \setminus \{t\}$ is a minimum cut of capacity 0.
- **No $s$-$t$ path.** If $G$ has no directed path from $s$ to $t$ at all, $f^{*} = 0$ and the set of vertices that $s$ reaches is the source side of a cut of capacity 0.
- **Irrational capacities.** With real capacities, the generic Ford-Fulkerson method can run forever and converge to a value below $f^{*}$; small networks with one capacity equal to $(\sqrt{5} - 1)/2$ show this. The polynomial algorithms below do not have this problem.

## Known algorithms

The bounds are for the worst case, with $n$ vertices, $m$ edges and, where named, integer capacities at most $U$. The model is the [word RAM](/word-ram/); for the strongly polynomial algorithms, the [real RAM](/real-ram/) with additions and comparisons works too.

| algorithm | time | capacities |
|---|---|---|
| [Ford-Fulkerson](/ford-fulkerson/), any augmenting paths | $O(m f^{*})$ | integer |
| [Edmonds-Karp](/edmonds-karp/), shortest augmenting paths | $O(n m^2)$ | real |
| [Maximum-capacity augmenting path](/maximum-capacity-augmenting-path/) | $O(m^2 \log n \log(mU))$ | integer |
| [Capacity scaling](/capacity-scaling/) | $O(m^2 \log U)$ | integer |
| [Dinic](/dinic/), [blocking flows](/blocking-flow/) | $O(n^2 m)$ | real |
| [MPM](/mpm-algorithm/) | $O(n^3)$ | real |
| [Push-relabel](/push-relabel/), generic | $O(n^2 m)$ | real |
| Push-relabel, FIFO | $O(n^3)$ | real |
| Push-relabel with [dynamic trees](/dynamic-tree/) | $O(n m \log(n^2 / m))$ | real |
| Orlin, with King, Rao and Tarjan | $O(n m)$ | real |
| [Almost-linear max flow](/almost-linear-max-flow/) | $m^{1 + o(1)} \log U$ | integer |

## Bounds

**Upper bounds.** For real capacities, the best strongly polynomial bound is $O(nm)$: Orlin (2013) for sparse graphs, and King, Rao and Tarjan (1994) for the dense case. For integer capacities, Goldberg and Rao (1998) reached $O(\min(n^{2/3}, m^{1/2})\, m \log(n^2/m) \log U)$, and Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva (2022) reached $m^{1 + o(1)} \log U$ with a randomized interior-point method; deterministic versions followed.

**Lower bound.** Each correct algorithm reads $\Omega(n + m)$ of the input in the worst case: an edge that it never reads could be a new $s$-$t$ path of large capacity. So the almost-linear bound is optimal up to the $m^{o(1)}$ factor. No better lower bound is known in a general model.

## Reductions

- **Max flow to LP.** The linear program above, with $m$ variables. Its dual is the min-cut LP.
- **Max flow to min-cost circulation.** Add an edge $t \to s$ of infinite capacity and cost $-1$, and give the other edges cost 0. A minimum-cost circulation then maximizes the flow on $t \to s$.
- **Bipartite matching to max flow.** Source to each left vertex, each allowed pair from left to right, each right vertex to the sink, all with capacity 1. An integral maximum flow is a [maximum matching](/bipartite-matching/). The same unit networks give [edge-disjoint paths](/edge-disjoint-paths/) and, with vertex splitting, [vertex-disjoint paths](/vertex-disjoint-paths/).
- **Min $s$-$t$ cut from max flow**, in $O(n + m)$ extra time, by one search in the [residual graph](/residual-graph/).
- **Maximum-weight closure to min cut.** The [maximum-weight closure](/maximum-weight-closure/) problem, and with it project selection, is one minimum cut.

## Applications

- Matching and assignment: [bipartite matching](/bipartite-matching/), [survey design](/survey-design-problem/) and [airline scheduling](/airline-scheduling/).
- Elimination arguments in sports: [baseball elimination](/baseball-elimination/).
- Computer vision: [image segmentation by graph cuts](/image-segmentation-graph-cuts/).
- Network reliability: [edge connectivity](/edge-connectivity/) and the [Gomory-Hu tree](/gomory-hu-tree/).
- Open-pit mining and project selection through [maximum-weight closure](/maximum-weight-closure/).

## References
