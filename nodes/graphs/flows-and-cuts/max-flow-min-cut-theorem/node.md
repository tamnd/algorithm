---
tag: Q5M02Y
kind: theorem
slug: max-flow-min-cut-theorem
name: Max-flow min-cut theorem
aliases:
- Ford-Fulkerson theorem
area: graphs/flows-and-cuts
level: intro
summary: The value of a maximum s-t flow equals the capacity of a minimum s-t cut.
prereqs: [s-t-flow, cut-capacity, residual-graph]
see_also: [max-flow-problem, min-cut-problem, min-cut-max-flow-duality, integrality-theorem, menger-theorem, ford-fulkerson, konig-theorem, multi-commodity-flow-problem]
sources:
  - paper: doi:10.4153/CJM-1956-045-5
    title: L. R. Ford Jr. and D. R. Fulkerson, Maximal flow through a network, Canadian Journal of Mathematics 8, 399 to 404 (1956)
    locator: the whole paper (the minimal cut theorem)
  - paper: doi:10.1109/TIT.1956.1056816
    title: P. Elias, A. Feinstein and C. E. Shannon, A note on the maximum flow through a network, IRE Transactions on Information Theory 2(4), 117 to 119 (1956)
    locator: the whole note (an independent proof of the theorem)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.2, The Ford-Fulkerson method (the max-flow min-cut theorem with its three equivalent conditions)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.2, Maximum Flows and Minimum Cuts in a Network
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 10, Maximum flow (the max-flow min-cut theorem and its history in the chapter notes)
---

The max-flow min-cut theorem says that in every [flow network](/flow-network/) the largest value of an [$s$-$t$ flow](/s-t-flow/) equals the smallest [capacity](/cut-capacity/) of an $s$-$t$ [cut](/cut/). One direction, that no flow exceeds any cut, is a short counting argument; the other direction is shown by the [residual graph](/residual-graph/) of a maximum flow, which yields a cut of the same capacity. The theorem is the base of the [Ford-Fulkerson method](/ford-fulkerson/), it gives a certificate of optimality for both problems, and it is the special case of [linear programming duality](/min-cut-max-flow-duality/) for flows.

## Statement

Let $N = (G, c, s, t)$ be a flow network: $G = (V, E)$ is a finite directed graph, $c : E \to \mathbb{R}_{\ge 0}$ is real-valued, and $s \ne t$. Parallel edges, antiparallel edges and edges of capacity 0 are allowed; an undirected network is the directed network with two opposite edges for each undirected edge. For $S \subseteq V$ with $s \in S$, $t \notin S$, let $c(S)$ be the sum of $c(e)$ over the edges $e$ from $S$ to $V \setminus S$.

**Theorem.** The maximum of $|f|$ over all $s$-$t$ flows $f$ exists, the minimum of $c(S)$ over all $s$-$t$ cuts exists, and

$$\max_{f} |f| = \min_{S} c(S).$$

**Equivalent conditions.** For an $s$-$t$ flow $f$, these three statements are equivalent:

1. $f$ is a maximum flow;
2. the residual graph $G_f$ has no directed $s$-$t$ path;
3. $|f| = c(S)$ for some $s$-$t$ cut $S$.

## In plain words

Picture a set of one-way pipes from a source to a drain. If you draw a line that splits the joints into a source side and a drain side, all water must cross the pipes that point from the source side to the drain side. So the total of their limits caps the flow. This is true for every such line.

The theorem says that the best flow always meets the tightest line exactly. When the flow cannot be improved, the joints that can still get more water from the source form one side of a line, and every pipe that leaves that side is full, while every pipe that comes back into it is empty. That line has exactly the value of the flow.

## Proof

**Step 1 (weak duality).** Let $f$ be a flow and $S$ a cut, with $T = V \setminus S$. Sum $f^{\mathrm{out}}(v) - f^{\mathrm{in}}(v)$ over $v \in S$. By conservation, each $v \in S \setminus \{s\}$ adds 0, and $s$ adds $|f|$. An edge with both ends in $S$ adds $+f(e)$ at its tail and $-f(e)$ at its head, so it cancels. Hence

$$|f| = \sum_{e \in E(S, T)} f(e) - \sum_{e \in E(T, S)} f(e) \le \sum_{e \in E(S, T)} c(e) - 0 = c(S),$$

using $f(e) \le c(e)$ on edges from $S$ to $T$ and $f(e) \ge 0$ on edges from $T$ to $S$. Equality holds if and only if every edge from $S$ to $T$ is full and every edge from $T$ to $S$ is empty.

**Step 2 (both optima exist).** There are finitely many cuts, so a minimum cut exists. The set of flows is the set of $x \in \mathbb{R}^E$ that meet finitely many linear equations and the bounds $0 \le x_e \le c(e)$. It is closed and bounded, and it holds the zero flow, so it is a nonempty compact set. The value $|f|$ is a linear, hence continuous, function of $f$, so it reaches a maximum on this set.

**Step 3 ((1) implies (2)).** If $G_f$ has an $s$-$t$ path $P$, let $\delta$ be the least residual capacity on $P$; $\delta > 0$ because $G_f$ holds only edges of positive residual capacity. The augmentation lemma of the [residual graph](/residual-graph/) page gives a flow of value $|f| + \delta > |f|$, so $f$ is not maximum.

**Step 4 ((2) implies (3)).** Assume $G_f$ has no $s$-$t$ path, and let $S$ be the set of vertices that $s$ reaches in $G_f$. Then $s \in S$ and $t \notin S$, so $S$ is a cut. Take an edge $e = (u, v)$ with $u \in S$, $v \in T$. If $f(e) < c(e)$, the forward residual edge $(u, v)$ is in $G_f$, so $s$ reaches $v$, a contradiction; hence $f(e) = c(e)$. Take an edge $e = (v, u)$ with $v \in T$, $u \in S$. If $f(e) > 0$, the backward residual edge $(u, v)$ is in $G_f$, again a contradiction; hence $f(e) = 0$. These are the conditions for equality in Step 1, so $|f| = c(S)$.

**Step 5 ((3) implies (1)).** If $|f| = c(S)$, then for every flow $g$, Step 1 gives $|g| \le c(S) = |f|$. So $f$ is maximum.

**Step 6 (the equation).** By Step 2 a maximum flow $f^{*}$ exists. By Steps 3 and 4, there is a cut $S^{*}$ with $c(S^{*}) = |f^{*}|$. By Step 1, $c(S) \ge |f^{*}|$ for every cut $S$, so $S^{*}$ is a minimum cut and $\max_f |f| = |f^{*}| = c(S^{*}) = \min_S c(S)$. $\blacksquare$

The proof does not need integer capacities. It also does not depend on any algorithm: Step 2 uses compactness, not the termination of augmenting paths, which can fail for irrational capacities.

## Consequences

- **Certificates.** A flow $f$ and a cut $S$ with $|f| = c(S)$ prove each other optimal. After any [maximum flow algorithm](/max-flow-problem/), one search in $G_f$ produces the cut, which solves the [minimum cut problem](/min-cut-problem/) in $O(n + m)$ more time.
- **Termination test of augmenting-path methods.** [Ford-Fulkerson](/ford-fulkerson/), [Edmonds-Karp](/edmonds-karp/) and [Dinic](/dinic/) stop when no augmenting path exists; Step 4 shows the flow is then maximum.
- **Integrality.** With integer capacities, Ford-Fulkerson keeps the flow integral and stops, so some maximum flow is integral: the [integrality theorem](/integrality-theorem/).
- **Menger's theorem.** With unit capacities and integrality, the largest number of edge-disjoint $s$-$t$ paths equals the smallest number of edges that separate $s$ from $t$: [Menger's theorem](/menger-theorem/). With [vertex splitting](/vertex-capacities-flow/), the vertex form follows.
- **König's theorem.** On the unit network of a bipartite graph, the theorem gives that a maximum matching has the size of a minimum vertex cover: [König's theorem](/konig-theorem/).
- **Hoffman's circulation theorem** follows by adding a source and a sink: [Hoffman's theorem](/hoffman-circulation-theorem/).
- **LP duality.** The theorem is the statement that the [max-flow LP](/max-flow-lp-formulation/) and its dual have the same optimum, where the dual has an integral optimal solution: [max-flow min-cut duality](/min-cut-max-flow-duality/).

## Tightness

The inequality of Step 1 is strict for every cut that is not minimum, and it holds with equality only at a maximum flow, so the equation cannot be stated with a weaker or a stronger side. Examples that check the edge cases:

- In the network $s \to a$ (10), $s \to b$ (10), $a \to b$ (2), $a \to c$ (4), $a \to d$ (8), $b \to d$ (9), $d \to c$ (6), $c \to t$ (10), $d \to t$ (10), both sides equal 19, and the only minimum cut is $S = \{s, b\}$. Its edge $a \to b$, from $T$ to $S$, carries 0 in every maximum flow, as Step 1 demands.
- If $t$ is not reachable from $s$, or reachable only through edges of capacity 0, both sides are 0.

The theorem does not extend to several commodities. In $K_{3,2}$ with sides $\{a, b, c\}$ and $\{x, y\}$, unit capacities on the six undirected edges, and a demand of 1 between each of the pairs $ab$, $ac$, $bc$ and $xy$, each cut has at least as much capacity as the demand it separates, so the cut ratio is 1. But each unit of each commodity uses at least two edges, and the six edges hold 6 units, so the largest common fraction of all four demands that can be routed is at most $6 / 8 = 3/4$. See the [multi-commodity flow problem](/multi-commodity-flow-problem/).

## History

Ford and Fulkerson proved the theorem in a RAND report of 1954, published in 1956, together with the augmenting-path method. Elias, Feinstein and Shannon published an independent proof in 1956.

## References
