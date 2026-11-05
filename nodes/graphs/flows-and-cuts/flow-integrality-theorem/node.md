---
tag: TMS9BG
kind: theorem
slug: flow-integrality-theorem
name: Integrality theorem for flows
aliases:
- Integrality property
area: graphs/flows-and-cuts
level: core
summary: Theorem stating that if all edge capacities are integers, some maximum flow assigns an integer value to every edge.
prereqs: [ford-fulkerson, s-t-flow, max-flow-problem]
see_also: [max-flow-min-cut-theorem, total-unimodularity, flow-decomposition, edge-disjoint-paths, bipartite-matching, menger-theorem, circulation-problem, min-cost-flow-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.3, Maximum bipartite matching (the integrality theorem and its use for matchings)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.2, Maximum Flows and Minimum Cuts in a Network (the integrality of the flow found by Ford-Fulkerson), and Section 7.7 (integrality for circulations with demands and lower bounds)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (the integrality theorem) and Chapter 11, Applications of Flows and Cuts
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 6, Maximum Flows, Basic Ideas (the integrality property) and Chapter 11, Network Simplex Algorithms (integrality of basic solutions)
---

The integrality theorem says that in a [flow network](/flow-network/) whose capacities are all integers, some [maximum flow](/max-flow-problem/) is integral: its value on every edge is an integer. The [Ford-Fulkerson algorithm](/ford-fulkerson/) finds such a flow. The theorem is what makes flows a tool for combinatorics: a maximum flow in a network built from a graph can be read as a set of edges or paths, which gives [bipartite matching](/bipartite-matching/), [edge-disjoint paths](/edge-disjoint-paths/) and [Menger's theorem](/menger-theorem/).

## Statement

Let $N = (G, c, s, t)$ be a flow network with $G = (V, E)$ directed, $s \ne t$, and $c(e) \in \mathbb{Z}_{\ge 0}$ for each edge. Antiparallel and parallel edges are allowed, each with its own flow value.

**Theorem (integrality).** (1) The maximum flow value $F$ is an integer. (2) There is a maximum s-t flow $f$ with $f(e) \in \mathbb{Z}$ for each $e \in E$. (3) The Ford-Fulkerson method, started from the zero flow, with any rule for choosing augmenting paths, ends after at most $F$ augmentations with such a flow.

**Extension (circulations).** If $\ell(e)$, $c(e)$ and the demands $d(v)$ of a [circulation problem](/circulation-problem/) are integers and a feasible circulation exists, then an integral feasible circulation exists. If edge costs are also given, some minimum-cost feasible circulation is integral.

The theorem says that *some* maximum flow is integral, not that each one is.

## In plain words

When every pipe has a whole-number limit, you never need to split a unit of water to get the most through. The augmenting path method starts with nothing and adds, at each step, the smallest spare room on a route. Spare room is always a whole number, because it starts as a whole number and only ever changes by whole numbers. So every step adds a whole number to every pipe, and the final best answer uses only whole numbers.

This is useful because whole numbers can mean things. A flow of 0 or 1 on an edge can mean "this edge is used" or "not used", so a best flow becomes a best set of edges, pairs or routes.

## Proof

We prove (3); it implies (1) and (2).

Run Ford-Fulkerson from $f = 0$. It keeps a residual capacity $c_f(e^+) = c(e) - f(e)$ on the forward arc and $c_f(e^-) = f(e)$ on the backward arc of each edge $e$, and in each round it picks an s-t path $P$ in the [residual graph](/residual-graph/), sets $\Delta = \min_{x \in P} c_f(x)$, and moves $\Delta$ from each arc of $P$ to its reverse.

*Claim: before each round, $f$ is an s-t flow and every $f(e)$ and every $c_f(x)$ is an integer.* At the start, $f = 0$ and $c_f(e^+) = c(e) \in \mathbb{Z}$, $c_f(e^-) = 0$. Suppose the claim holds before a round. Then $\Delta$ is the minimum of a finite nonempty set of integers, so $\Delta \in \mathbb{Z}$, and $\Delta \ge 1$ because each arc of $G_f$ has positive residual capacity. The round adds or subtracts $\Delta$ on some arcs and some flow values, so they stay integers. The new $f$ is an s-t flow by the augmentation lemma on the page [augmenting path](/augmenting-path-flow/), and its value is $|f| + \Delta$.

*Termination.* Each value is at most $c(\{s\}, V \setminus \{s\})$, a finite integer, and each round raises the value by $\Delta \ge 1$. So there are finitely many rounds; more precisely, at most $F$, since the value starts at 0 and never exceeds $F$.

*Optimality.* When no augmenting path is left, let $S$ be the set of vertices reachable from $s$ in $G_f$. Every edge from $S$ to $V \setminus S$ is full and every edge from $V \setminus S$ to $S$ is empty, so $|f| = c(S, V \setminus S)$, which bounds every flow value. Hence $f$ is a maximum flow. This is Lemma 2 of [augmenting path](/augmenting-path-flow/).

So the final $f$ is a maximum flow with integer values, which is (2) and (3). Its value $F = |f|$ is a sum and difference of integers, which is (1). $\square$

*The circulation extension.* The reduction on the page [circulation problem](/circulation-problem/) maps an instance with integer $\ell$, $c$, $d$ to a maximum flow instance with integer capacities $c - \ell$ and integer edges at $s^*$ and $t^*$. A feasible circulation exists if and only if the maximum flow saturates all edges out of $s^*$. By the theorem, an integral maximum flow $g$ then exists, and $f = g + \ell$ is an integral feasible circulation. For costs, the [cycle-canceling](/cycle-canceling/) method started from this integral circulation cancels each negative cycle by its integer bottleneck, so it keeps the flow integral and ends at an integral optimum.

*Another proof.* The node-arc [incidence matrix](/incidence-matrix/) of a directed graph is [totally unimodular](/total-unimodularity/), so each vertex of the polytope $\{f : Bf = b,\ 0 \le f \le c\}$ is integral when $b$ and $c$ are integral. A linear objective that has a finite optimum reaches it at a vertex. This gives the same result for all the linear objectives at once.

## Consequences

- **Bipartite matching.** In the network with unit capacities built from a bipartite graph, an integral flow of value $k$ is a matching of size $k$, so a maximum flow gives a maximum [bipartite matching](/bipartite-matching/). [König's theorem](/konig-theorem/) and [Hall's theorem](/hall-theorem/) follow from max-flow min-cut with integrality.
- **Disjoint paths.** With unit capacities, an integral maximum flow decomposes by [flow decomposition](/flow-decomposition/) into $F$ edge-disjoint s-t paths. With max-flow min-cut this is [Menger's theorem](/menger-theorem/), and it solves the [edge-disjoint paths](/edge-disjoint-paths/) and [vertex-disjoint paths](/vertex-disjoint-paths/) problems.
- **Applications by rounding.** [Baseball elimination](/baseball-elimination/), [airline scheduling](/airline-scheduling/), the [survey design problem](/survey-design-problem/) and matrix rounding all need an integral answer, and the theorem shows that solving the flow problem is enough.
- **Rational capacities.** Multiplying by a common denominator $D$ gives a maximum flow whose values are multiples of $1/D$.

## Tightness

**Not every maximum flow is integral.** Take $s \to v$ of capacity 1 and two parallel edges $v \to t$ of capacity 1 each. The flow $f(s, v) = 1$ with $1/2$ on each parallel edge is a maximum flow, and it is not integral. The theorem only promises that some maximum flow is integral, and that the augmenting path methods find one. Interior point methods and other continuous methods can return fractional maximum flows on integer networks; they need a rounding step, for example by [flow decomposition](/flow-decomposition/) and cycle cancelling, to get an integral one.

**Integer capacities are needed.** With $c(s, a) = c(a, t) = 1/2$ the only maximum flow has value $1/2$ on both edges.

**More than one commodity.** For [multi-commodity flow](/multi-commodity-flow-problem/) the statement fails: with integer capacities a feasible fractional multi-commodity flow can exist while no integral one does, and deciding whether an integral two-commodity flow exists is NP-complete (Even, Itai and Shamir, 1976).

**Extra side constraints.** Adding even one more linear constraint to a flow problem, such as a budget on the total cost of a maximum flow, can destroy the integrality of the optimum vertex.

## History

Ford and Fulkerson stated the integrality of maximal flows with integer capacities as part of their theory of network flows in the 1950s; it follows from their augmenting path method, and their 1962 book Flows in Networks uses it to derive combinatorial theorems such as those of König, Hall and Menger. The view through total unimodularity goes back to Hoffman and Kruskal (1956).

## References
