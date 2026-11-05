---
tag: 7KRE5V
kind: theorem
slug: integrality-theorem
name: Integrality theorem for flows
aliases:
- integral flow theorem
area: graphs/flows-and-cuts
level: intro
summary: If all capacities are integers, some maximum flow is integral.
prereqs: [max-flow-min-cut-theorem, ford-fulkerson]
see_also: [flow-integrality-theorem, total-unimodularity, max-flow-problem, min-cost-flow-problem, circulation-problem, menger-theorem, bipartite-matching, multi-commodity-flow-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.2 (the integrality of the flow found by Ford-Fulkerson) and Section 24.3, Maximum bipartite matching (the integrality theorem and its use for matching)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.2, Maximum Flows and Minimum Cuts in a Network (integer-valued maximum flows), and Section 7.7, Extensions to the Maximum-Flow Problem (integrality with demands and lower bounds)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 13, Path and flow polyhedra and total unimodularity (the incidence matrix of a directed graph is totally unimodular, and the integrality of flow polyhedra)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 9, Minimum Cost Flows, Basic Algorithms (the integrality property of minimum cost flow problems)
  - paper: doi:10.1137/0205048
    title: S. Even, A. Itai and A. Shamir, On the complexity of timetable and multicommodity flow problems, SIAM Journal on Computing 5(4), 691 to 703 (1976)
    locator: the result on integral two-commodity flow
---

The integrality theorem for flows says that when every capacity of a [flow network](/flow-network/) is an integer, some [maximum flow](/max-flow-problem/) gives an integer to every edge, and the [Ford-Fulkerson method](/ford-fulkerson/) finds one. A stronger form says that every flow problem with integer bounds and integer supplies (circulation, transshipment, [minimum-cost flow](/min-cost-flow-problem/)) has an integral optimal solution when it has an optimal solution at all, because the incidence matrix of a directed graph is [totally unimodular](/total-unimodularity/). This is what lets flows solve combinatorial problems: an integral flow of a unit network is a set of paths, a matching or an assignment. The page [flow integrality theorem](/flow-integrality-theorem/) treats the maximum-flow case alone.

## Statement

Let $G = (V, E)$ be a finite directed graph, possibly with parallel and antiparallel edges, and let $s \ne t$ be vertices.

**Theorem A (maximum flow).** If every capacity $c(e)$ is a nonnegative integer, then there is a maximum $s$-$t$ flow $f$ with $f(e) \in \mathbb{Z}$ for each edge $e$. Every run of the Ford-Fulkerson method from the zero flow stops after at most $f^{*}$ augmentations and returns such a flow. In particular the maximum value $f^{*}$ is an integer.

**Theorem B (general form).** Let $N$ be the $V \times E$ incidence matrix of $G$: in the column of $e = (u, v)$, $N_{v e} = 1$, $N_{u e} = -1$, and the other entries are 0. Let $b \in \mathbb{Z}^{V}$ and $\ell, u \in (\mathbb{Z} \cup \{\pm\infty\})^{E}$. Every vertex of the polyhedron

$$P = \{ x \in \mathbb{R}^E : N x = b,\ \ell \le x \le u \}$$

is integral. So if a linear function $a^{\top} x$ has a minimum over $P$ and $P$ has a vertex, the minimum is reached at an integral $x$.

Theorem B covers maximum flow (add an edge $t \to s$ with no upper bound, set $b = 0$, and maximize the flow on it), circulations with integer lower bounds, transshipment with integer supplies, and minimum-cost flow with any real costs. A self-loop has a zero column and changes nothing; drop it first.

## In plain words

Suppose every pipe can carry a whole number of units. The theorem says that you never need to split a unit to get the best total: some best plan sends a whole number of units through each pipe. The usual method finds it, because it starts with nothing and adds a whole number of units each time it finds a free route.

This matters because many puzzles become flow problems when you give each pipe a limit of one. Then a whole-number plan says "use this pipe" or "do not use it", and so it is a real choice of routes, of pairs or of tasks. A plan with halves would have no such meaning.

## Proof

**Proof of Theorem A.** Run Ford-Fulkerson from $f = 0$. We claim that before each step, $f$ is integral. This holds at the start. If $f$ is integral, each residual capacity $c(e) - f(e)$ or $f(e)$ is an integer, so the bottleneck $\delta$ of an augmenting path is a positive integer, $\delta \ge 1$, and the new flow, which adds or subtracts $\delta$ on some edges, is integral. Each step raises $|f|$ by $\delta \ge 1$, and $|f| \le c(\{s\})$, the capacity of the cut $\{s\}$, for each flow. So the method stops after at most $f^{*} \le c(\{s\})$ steps. It stops only when the residual graph has no $s$-$t$ path, and then $f$ is maximum by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). So $f$ is an integral maximum flow. $\square$

**Lemma (total unimodularity).** Every square submatrix $M$ of $N$ has $\det M \in \{-1, 0, 1\}$.

*Proof.* By induction on the order $k$ of $M$. For $k = 1$, the entries of $N$ are in $\{-1, 0, 1\}$. Let $k \ge 2$. Each column of $M$ is part of a column of $N$, so it has at most one $+1$ and at most one $-1$. Case 1: some column of $M$ is zero; then $\det M = 0$. Case 2: some column has exactly one nonzero entry; expand along it to get $\det M = \pm \det M'$ with $M'$ of order $k - 1$, which is in $\{-1, 0, 1\}$ by the hypothesis. Case 3: each column has one $+1$ and one $-1$; then the sum of all rows of $M$ is the zero vector, the rows are linearly dependent, and $\det M = 0$. $\square$

**Proof of Theorem B.** Let $x$ be a vertex of $P$. Let $J$ be the set of edges with $\ell_e < x_e < u_e$; on the other edges $x_e$ equals a finite integer bound. Because $x$ is a vertex, it is the only point of $P$ that agrees with it on $E \setminus J$ and keeps the same tight bounds; so the system $N_J y = b - N_{E \setminus J} x_{E \setminus J}$ has the unique solution $y = x_J$, and the columns of $N_J$ are linearly independent. Pick $|J|$ rows of $N_J$ that are linearly independent; they form a square nonsingular submatrix $B$, and $x_J$ is the unique solution of $B y = b'$, where $b'$ is the matching part of $b - N_{E \setminus J} x_{E \setminus J}$. The vector $b'$ is integral, since $b$, $N$ and $x_{E \setminus J}$ are. By the lemma, $\det B = \pm 1$. By Cramer's rule, $y_j = \det B_j / \det B$, where $B_j$ is $B$ with column $j$ replaced by $b'$; $\det B_j$ is an integer, so $y_j$ is an integer. So $x$ is integral. When a linear function has a minimum over a polyhedron that has a vertex, some vertex reaches the minimum, which is a basic theorem of [linear programming](/linear-programming-problem/). $\blacksquare$

## Consequences

- **Matching and covers.** An integral maximum flow of the unit network of a bipartite graph is a [maximum matching](/bipartite-matching/). With the max-flow min-cut theorem this gives [König's theorem](/konig-theorem/) and [Hall's theorem](/hall-theorem/).
- **Disjoint paths.** An integral flow of value $k$ in a unit network splits into $k$ [edge-disjoint paths](/edge-disjoint-paths/), which gives [Menger's theorem](/menger-theorem/); with [vertex splitting](/vertex-capacities-flow/) it gives [vertex-disjoint paths](/vertex-disjoint-paths/).
- **Assignments with quotas.** [Survey design](/survey-design-problem/), [airline scheduling](/airline-scheduling/) and [baseball elimination](/baseball-elimination/) read an assignment from an integral flow with lower and upper bounds, which Theorem B allows.
- **Minimum-cost flow.** With integer capacities and supplies, [successive shortest paths](/successive-shortest-path/), [cycle canceling](/cycle-canceling/) and the [network simplex method](/network-simplex/) keep the flow integral; Theorem B shows that nothing is lost by this.
- **Integral decomposition.** An integral flow splits into integral path and cycle flows: [flow decomposition](/flow-decomposition/).

## Tightness

- **Not every maximum flow is integral.** In the network $s \to a$ (1), $a \to b$ (1), $a \to c$ (1), $b \to t$ (1), $c \to t$ (1), the flow with $\frac12$ on each of $a \to b$, $a \to c$, $b \to t$, $c \to t$ and 1 on $s \to a$ is a maximum flow of value 1. The theorem promises only that some maximum flow is integral. A solver that is not built on integral steps, such as an interior-point method, can return this fractional one.
- **Integer capacities are needed.** With the single edge $s \to t$ of capacity $\frac12$, the only maximum flow is $\frac12$.
- **One commodity is needed.** Take the undirected cycle $a, b, c, d$ with unit capacities and two commodities, from $a$ to $c$ and from $b$ to $d$, each with demand 1. Sending half of each commodity each way around the cycle loads each edge with exactly 1, so a fractional solution exists. An integral one does not: each commodity needs a whole path of two edges, and each of the four pairs of such paths shares an edge. The constraint matrix of a [multi-commodity flow](/multi-commodity-flow-problem/) is not totally unimodular, and the integral two-commodity problem is NP-complete (Even, Itai and Shamir).
- **The edge cases of Theorem A.** If a capacity is 0, the flow on that edge is 0, an integer. If $t$ is not reachable from $s$, the zero flow is the integral maximum flow and the method makes no augmentation.

## History

The integrality of the flow found by the labeling method is part of the work of Ford and Fulkerson in the 1950s. The fact that the incidence matrix of a directed graph is totally unimodular goes back to Poincaré, and the link between total unimodularity and integral polyhedra is the Hoffman-Kruskal theorem of 1956; Schrijver's book gives the history.

## References
