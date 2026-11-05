---
tag: J6A8S0
kind: problem
slug: constrained-shortest-path
name: Resource-constrained shortest path
aliases:
- constrained shortest path
- resource-constrained shortest path
area: graphs/shortest-paths
level: advanced
summary: Shortest s-t path subject to an additional resource budget constraint; NP-hard in general.
prereqs: [single-pair-shortest-path, knapsack-problem, np-hard]
see_also: [multi-objective-shortest-path, pareto-optimality, lagrangian-relaxation, fptas, pseudo-polynomial-time, k-shortest-paths, vehicle-routing-problem, column-generation]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Appendix A2, Network design, problem ND30, Shortest weight-constrained path (NP-complete, pseudo-polynomial)
  - paper: doi:10.1016/0022-247x(66)90020-5
    title: Hans C. Joksch, The shortest route problem with constraints, Journal of Mathematical Analysis and Applications 14(2), 191 to 197 (1966)
    locator: the whole paper (the dynamic program over the resource budget)
  - paper: doi:10.1002/net.3230100403
    title: Gabriel Y. Handler and Israel Zang, A dual algorithm for the constrained shortest path problem, Networks 10(4), 293 to 309 (1980)
    locator: the whole paper (Lagrangian relaxation of the budget and closing the gap by k-shortest paths)
  - paper: doi:10.1287/moor.17.1.36
    title: Refael Hassin, Approximation schemes for the restricted shortest path problem, Mathematics of Operations Research 17(1), 36 to 42 (1992)
    locator: the whole paper (the first fully polynomial approximation schemes)
  - paper: doi:10.1016/s0167-6377(01)00069-4
    title: Dean H. Lorenz and Danny Raz, A simple efficient approximation scheme for the restricted shortest path problem, Operations Research Letters 28(5), 213 to 219 (2001)
    locator: the whole paper (an FPTAS in O(mn(log log n + 1/ε)) time)
  - paper: doi:10.1007/0-387-25486-2_2
    title: Stefan Irnich and Guy Desaulniers, Shortest path problems with resource constraints, in Column Generation, Springer, 33 to 65 (2005)
    locator: the whole chapter (resource extension functions, labeling algorithms with dominance, and the use as the pricing problem of vehicle routing)
---

The resource-constrained shortest-path problem asks for a cheapest path from $s$ to $t$ whose total use of a second quantity, the *resource*, stays within a budget. Each edge has a cost and a resource use, for example money and travel time, or travel time and fuel. Without the budget, this is the ordinary [single-pair shortest-path problem](/single-pair-shortest-path/); with it, the problem is [NP-hard](/np-hard/), by a direct reduction from the [knapsack problem](/knapsack-problem/). It is NP-hard only in the weak sense: a [dynamic program](/dynamic-programming/) over the budget runs in [pseudo-polynomial time](/pseudo-polynomial-time/), and there are [fully polynomial approximation schemes](/fptas/). It is the pricing problem inside [column generation](/column-generation/) for [vehicle routing](/vehicle-routing-problem/), where it is solved millions of times.

## In plain words

You want the cheapest way from one city to another, but you also have a deadline. Each road has a toll and a driving time. The cheapest route might take too long, and the fastest might cost a lot.

The task is to find the cheapest route that still arrives in time. You can no longer just keep the cheapest way to each city, because a slightly more expensive way that is much faster might be the one you need later. So you have to remember several trade-offs per city, and in bad cases there are very many of them.

This makes the problem hard in general. It becomes manageable when the times are small whole numbers, because then you only track one cheapest cost for each city and each possible time used.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ vertices and $m$ edges; for each edge a cost $c(u, v)$ and a resource use $r(u, v)$; vertices $s$ and $t$; and a budget $R$.

**Output.** A simple path $P$ from $s$ to $t$ with $r(P) = \sum_{e \in P} r(e) \le R$ that minimizes $c(P) = \sum_{e \in P} c(e)$, or the answer that no path with $r(P) \le R$ exists, in which case the optimum is $+\infty$.

**Decision version.** Given also a bound $C$, is there an $s$-$t$ path with $r(P) \le R$ and $c(P) \le C$? This is SHORTEST WEIGHT-CONSTRAINED PATH in Garey and Johnson's list.

**Weight assumptions.** The standard problem has nonnegative costs and nonnegative resource uses, both real; the pseudo-polynomial algorithms need integer resource uses (or integer costs). Under these assumptions a walk can be shortened to a simple path without raising its cost or its resource use, so it does not matter whether walks or paths are allowed, and cycles of any kind are harmless. If costs may be negative, the problem changes: with walks allowed and a negative-cost cycle of zero resource use reachable on the way to $t$, the optimum is $-\infty$; with simple paths required, negative costs already make the problem without any budget contain the [longest path problem](/longest-path-problem/), which is strongly NP-hard. If $t$ is not reachable from $s$, or every $s$-$t$ path uses more than $R$, the answer is "infeasible".

## Variants

- **Several resources.** $k$ resources with $k$ budgets. For fixed $k$ the dynamic program stays pseudo-polynomial, over a $k$-dimensional grid of budgets.
- **Resource windows.** The resource (often time) must lie in a window $[a_v, b_v]$ at each vertex, waiting being allowed, as in routing with time windows. This is the shortest-path problem with resource constraints (SPPRC) of Irnich and Desaulniers, where general *resource extension functions* replace sums.
- **Elementary SPPRC.** In column generation the costs are reduced costs and may be negative, and the path must be elementary (no repeated vertex); this version is strongly NP-hard.
- **Bicriteria.** Find all Pareto-optimal paths for (cost, resource), as in the [multi-objective shortest-path problem](/multi-objective-shortest-path/); the constrained problem picks one point of this [Pareto front](/pareto-optimality/).
- **Restricted shortest path.** The name used in networking (delay-constrained least-cost routing), where the resource is delay.

## Examples

**A gap between cheap and fast.** The vertices are $s, a, b, t$ and each edge has (cost, time): $s \to a$ (1, 10), $a \to t$ (1, 10), $s \to b$ (10, 3), $b \to t$ (2, 2), $a \to b$ (1, 1). The three $s$-$t$ paths are:

| path | cost | time |
|---|---|---|
| $s, a, t$ | 2 | 20 |
| $s, a, b, t$ | 4 | 13 |
| $s, b, t$ | 12 | 5 |

With $R = 20$ the answer is $s, a, t$ of cost 2, the ordinary cheapest path. With $R = 15$ it is $s, a, b, t$ of cost 4. With $R = 10$ only $s, b, t$ is feasible, cost 12. With $R = 4$ no path is feasible and the answer is "infeasible". At the vertex $b$ the two partial paths $s, a, b$ (2, 11) and $s, b$ (10, 3) are both needed: neither is better in both cost and time.

**Lagrangian bound.** For $R = 15$, relax the budget with a multiplier $\lambda \ge 0$: $L(\lambda) = \min_P \big(c(P) + \lambda (r(P) - R)\big)$, an ordinary shortest-path problem with weights $c + \lambda r$. The three paths give $2 + 5\lambda$, $4 - 2\lambda$ and $12 - 10\lambda$; the best bound is at $\lambda = 2/7$, where $L = 24/7 \approx 3.43$. It is below the optimum 4, so the relaxation has a *duality gap*. At $\lambda = 2/7$ the paths $s, a, t$ and $s, a, b, t$ tie for the least $c + \lambda r$, and the second is feasible, so it is the answer here; in general Handler and Zang close the gap by enumerating paths in order of $c + \lambda r$ with [k shortest paths](/k-shortest-paths/).

**Unreachable target.** If the edges into $t$ are removed, there is no $s$-$t$ path at all, and the answer is "infeasible" for every budget, the same as when the budget is too small.

**Knapsack as a path.** Items with values $v_1, \ldots, v_k$ and sizes $a_1, \ldots, a_k$, capacity $A$. Build a chain $u_0, u_1, \ldots, u_k$ with two edges from $u_{i-1}$ to $u_i$: "take" with cost 0 and resource $a_i$, and "skip" with cost $v_i$ and resource 0. An $s$-$t$ path from $u_0$ to $u_k$ is a choice of items; its resource is the total size taken and its cost the total value skipped. With $R = A$, the cheapest feasible path skips the least value, so it takes the most value that fits. (Subdivide the parallel edges if the graph must be simple.)

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| dynamic program over the budget (Joksch 1966) | $O(R\,m)$ for positive integer resources | $D[v][\rho]$ = least cost to reach $v$ using at most $\rho$; resource 0 edges need a Dijkstra pass per budget value |
| dynamic program over the cost | $O(C\,m)$ for positive integer costs, $C$ the optimum | least resource for each cost value; the basis of the approximation schemes |
| label setting with dominance | exponential worst case | keep at each vertex only the Pareto-optimal (cost, resource) labels; fast in practice |
| Lagrangian relaxation plus $k$ shortest paths (Handler and Zang 1980) | exponential worst case | bound by $\max_\lambda L(\lambda)$, then enumerate paths by $c + \lambda r$ |
| FPTAS (Hassin 1992; Lorenz and Raz 2001) | $O(mn(\log\log n + 1/\varepsilon))$ for Lorenz and Raz | a feasible path of cost at most $(1 + \varepsilon)$ times the optimum |

With zero costs or the budget set to $\infty$, the problem is plain shortest paths and [Dijkstra's algorithm](/dijkstra/) applies.

## Bounds

The decision version is NP-complete (Garey and Johnson, ND30), by the knapsack reduction above, even when the graph is a chain with parallel edges. It is weakly NP-hard: the budget dynamic program is polynomial when $R$ is bounded by a polynomial in $n$, and the cost dynamic program with scaling gives an FPTAS. So unless P = NP, there is no polynomial-time exact algorithm, but the single-resource problem with nonnegative integer data is not strongly NP-hard unless P = NP. The elementary variant with negative costs is strongly NP-hard, since it contains the longest path problem.

## Reductions

- **From knapsack.** The chain construction above maps a 0-1 knapsack instance to a constrained shortest-path instance of the same size; the [partition problem](/partition-problem/) and [subset sum](/subset-sum-problem/) also reduce through it.
- **To knapsack-style dynamic programming.** Expanding each vertex into copies $(v, \rho)$ for $\rho = 0, \ldots, R$ gives a layered graph with $n(R + 1)$ vertices in which ordinary shortest paths solve the problem; this is the budget dynamic program.
- **To bicriteria shortest paths.** The answer is a point of the Pareto front of (cost, resource) paths.
- **Lagrangian relaxation to shortest paths.** Moving the budget into the objective gives a [Lagrangian](/lagrangian-relaxation/) problem that is a plain shortest-path problem for each $\lambda$.

## Applications

- **Vehicle routing.** The pricing subproblem of column generation for vehicle routing with time windows is an elementary SPPRC.
- **Network routing.** Least-cost routes under a delay bound (quality of service).
- **Crew scheduling.** Pairings of flights must obey limits on duty time and rest, modelled as resources.
- **Travel planning.** Cheapest trip within a time limit, or fastest trip within a price limit.

## References
