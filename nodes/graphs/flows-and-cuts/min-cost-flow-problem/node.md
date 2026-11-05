---
tag: JJQ4RB
kind: problem
slug: min-cost-flow-problem
name: Minimum-cost flow problem
aliases:
- min-cost max-flow
- min-cost flow
area: graphs/flows-and-cuts
level: core
summary: Find a flow of given value (or a feasible flow) minimizing total edge cost.
prereqs: [max-flow-problem, residual-graph, single-source-shortest-paths, negative-cycle]
see_also: [successive-shortest-path, cycle-canceling, cost-scaling, network-simplex, min-cost-flow-lp-formulation, assignment-problem, potential-function-reduced-costs, integrality-theorem]
sources:
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 9, Minimum Cost Flows, Basic Algorithms (optimality conditions, cycle canceling, successive shortest paths), Chapter 10, Polynomial Algorithms, and Chapter 11, Network Simplex Algorithms
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 12, Minimum-cost flows and circulations
  - paper: doi:10.1007/BF02579369
    title: Éva Tardos, A strongly polynomial minimum cost circulation algorithm, Combinatorica 5(3), 247 to 255 (1985)
    locator: the whole paper (the first strongly polynomial algorithm)
  - paper: doi:10.1287/opre.41.2.338
    title: James B. Orlin, A faster strongly polynomial minimum cost flow algorithm, Operations Research 41(2), 338 to 350 (1993)
    locator: the whole paper (the O(m log n (m + n log n)) bound)
  - paper: doi:10.1145/76359.76368
    title: Andrew V. Goldberg and Robert E. Tarjan, Finding minimum-cost circulations by canceling negative cycles, Journal of the ACM 36(4), 873 to 886 (1989)
    locator: the whole paper (canceling minimum mean cycles is strongly polynomial)
  - paper: url:https://arxiv.org/abs/2203.00671
    title: Li Chen, Rasmus Kyng, Yang P. Liu, Richard Peng, Maximilian Probst Gutenberg and Sushant Sachdeva, Maximum flow and minimum-cost flow in almost-linear time (2022)
    locator: the main theorem (minimum-cost flow with polynomially bounded integer capacities, demands and costs in m^(1+o(1)) time)
---

The minimum-cost flow problem asks for a flow in a directed network that meets given supplies and demands, stays within the capacities, and has the least total cost, where each edge charges a fixed cost per unit of flow. It contains [shortest paths](/single-source-shortest-paths/), [maximum flow](/max-flow-problem/), the [assignment problem](/assignment-problem/) and transportation problems as special cases, and it is a linear program whose constraint matrix is [totally unimodular](/total-unimodularity/), so integer data give an integral optimum. A flow is optimal exactly when its [residual graph](/residual-graph/) has no [negative cycle](/negative-cycle/). Classical algorithms are [successive shortest paths](/successive-shortest-path/), [cycle canceling](/cycle-canceling/), [cost scaling](/cost-scaling/) and the [network simplex method](/network-simplex/); the fastest known runs in almost-linear time.

## In plain words

Goods sit in some warehouses and are wanted in some shops. Roads join the places, each road can carry only so much, and each unit on a road costs a fixed price. Plan how much goes on each road so that every shop gets what it wants, at the lowest total price.

The plan is the best one exactly when no "detour" helps: there is no loop of changes, such as moving one unit off an expensive road and onto a cheaper route around it, that would save money. The usual methods either build the plan unit by unit along the cheapest route, or start from any plan and keep finding money-saving loops.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ vertices and $m$ edges; for each edge $e$ a capacity $u(e) \in \mathbb{R}_{\ge 0} \cup \{\infty\}$ and a cost $c(e) \in \mathbb{R}$, which may be negative; and a supply $b(v) \in \mathbb{R}$ at each vertex with $\sum_v b(v) = 0$. A vertex with $b(v) > 0$ is a source of $b(v)$ units, one with $b(v) < 0$ a sink. Parallel edges with different costs and antiparallel edges are allowed; self-loops are dropped, or kept with a free choice of flow if their cost is negative and their capacity finite. Integer capacities, supplies and costs are the usual setting of the algorithms.

**Output.** A flow $x : E \to \mathbb{R}$ that minimizes $\sum_e c(e)\, x(e)$ subject to

$$\sum_{e \in \delta^{\mathrm{out}}(v)} x(e) - \sum_{e \in \delta^{\mathrm{in}}(v)} x(e) = b(v) \quad (v \in V), \qquad 0 \le x(e) \le u(e) \quad (e \in E),$$

or a report that no feasible flow exists, or that the cost is unbounded below (only possible with a negative-cost cycle of infinite capacity). Its LP form is the [min-cost flow LP](/min-cost-flow-lp-formulation/).

**The $s$-$t$ form.** Given $s$, $t$ and a value $d$, set $b(s) = d$, $b(t) = -d$ and $b = 0$ elsewhere. *Min-cost max-flow* takes $d$ to be the maximum flow value.

**Residual graph.** For a feasible $x$, each edge $e = (v, w)$ gives a forward residual edge $(v, w)$ of capacity $u(e) - x(e)$ and cost $c(e)$, and a backward residual edge $(w, v)$ of capacity $x(e)$ and cost $-c(e)$; only edges of positive capacity are kept. Antiparallel edges stay separate: $(v, w)$ and $(w, v)$ each get their own pair.

**Theorem (negative cycle optimality).** A feasible flow $x$ has least cost if and only if $G_x$ has no directed cycle of negative total cost.

*Proof.* If $G_x$ has a negative cycle $C$, pushing $\min_{r \in C} u_x(r) > 0$ units around $C$ keeps all supplies and lowers the cost. Conversely, let $x'$ be feasible with lower cost. For each edge put $x'(e) - x(e)$ on the forward residual edge if it is positive and $x(e) - x'(e)$ on the backward one otherwise. This is a circulation $h$ in $G_x$ within the residual capacities, with cost $c(x') - c(x) < 0$. A circulation splits into cycle flows ([flow decomposition](/flow-decomposition/)), so one of these cycles has negative cost. $\square$

**Reduced cost optimality.** Equivalently, $x$ is optimal if and only if there are potentials $\pi : V \to \mathbb{R}$ with reduced costs $c^{\pi}(v, w) = c(v, w) + \pi(v) - \pi(w) \ge 0$ on every residual edge. From a flow with no negative cycle, shortest-path distances in $G_x$ give such $\pi$; conversely, nonnegative reduced costs make every cycle cost nonnegative, because the potentials cancel around a cycle. The potentials are the dual variables of the LP; see [reduced costs](/potential-function-reduced-costs/) and [shortest-path optimality conditions](/shortest-path-optimality-conditions/).

## Variants

- **Min-cost circulation.** All $b(v) = 0$, often with lower bounds $\ell(e) \le x(e)$. Every variant above reduces to it, and it is the form used by cycle canceling and cost scaling.
- **Transshipment.** No capacities, only supplies and costs.
- **Transportation and the [assignment problem](/assignment-problem/).** A bipartite graph with sources on one side and sinks on the other; with unit supplies it is weighted bipartite matching, solved by the [Hungarian algorithm](/hungarian-algorithm/).
- **Lower bounds.** $\ell(e) \le x(e) \le u(e)$: shift by $\ell$ and adjust the supplies at the two ends.
- **Convex costs.** A convex piecewise-linear cost on an edge splits into parallel edges of increasing costs; convex separable costs in general need other methods.
- **Concave or fixed costs.** A fixed charge for using an edge at all makes the problem NP-hard.
- **Several commodities.** The [multi-commodity flow problem](/multi-commodity-flow-problem/) loses total unimodularity.

## Examples

The network has the edges, with (capacity, cost): $s \to a$ (3, 1), $s \to b$ (2, 4), $a \to b$ (2, 1), $a \to t$ (2, 5), $b \to t$ (3, 1). The cheapest flow of value $d$, found by exhaustive search over integer flows, is:

| $d$ | flow on $sa, sb, ab, at, bt$ | cost | added cost |
|---|---|---|---|
| 1 | 1, 0, 1, 0, 1 | 3 | 3 |
| 2 | 2, 0, 2, 0, 2 | 6 | 3 |
| 3 | 2, 1, 2, 0, 3 | 11 | 5 |
| 4 | 3, 1, 2, 1, 3 | 17 | 6 |
| 5 | 3, 2, 1, 2, 3 | 25 | 8 |

The added cost per unit grows, so the cost is a convex function of $d$. The fifth unit takes the path $s, b, a, t$, which uses the backward residual edge $b \to a$ of cost $-1$: it moves one unit off $a \to b$. The maximum flow is 5, so the min-cost maximum flow costs 25. For $d = 6$ there is no feasible flow.

At $d = 4$ the flow is optimal: the residual cycles, such as $s, b, a, s$ with cost $4 - 1 - 1 = 2$ and $t, b, a, t$ with cost $-1 - 1 + 5 = 3$, all have nonnegative cost.

**Zero capacity.** An edge $s \to t$ of capacity 0 and cost $-100$ never carries flow and changes nothing.

**No $s$-$t$ path.** With only $s \to a$ and $b \to t$, every $d > 0$ is infeasible, and $d = 0$ has cost 0.

**Negative cycle.** The edges $a \to b$ (cost $-2$) and $b \to a$ (cost 1), both of infinite capacity, form a negative cycle with antiparallel edges: the cost is unbounded below. With capacity 4 on each, the optimal circulation puts 4 on both, for cost $-4$.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| [cycle canceling](/cycle-canceling/) (Klein 1967) | $O(n m^2 C U)$ | pseudo-polynomial with Bellman-Ford |
| [successive shortest paths](/successive-shortest-path/) | $O(d (m + n \log n))$ | $d$ augmentations with Dijkstra |
| capacity scaling (Edmonds-Karp 1972) | $O(m \log U (m + n \log n))$ | weakly polynomial |
| canceling minimum mean cycles (Goldberg-Tarjan 1989) | polynomial in $n$, $m$ | strongly polynomial |
| [cost scaling](/cost-scaling/) (Goldberg-Tarjan 1990) | $O(n^2 m \log(nC))$ | push-relabel style |
| Tardos 1985 | polynomial in $n$, $m$ | first strongly polynomial |
| Orlin 1993 | $O(m \log n (m + n \log n))$ | strongly polynomial |
| [network simplex](/network-simplex/) | polynomial with Orlin's rule | fast in practice |
| Chen et al. 2022 | $m^{1 + o(1)}$ | polynomially bounded integer data |

Here $U$ is the largest capacity or supply and $C$ the largest absolute cost, for integer data.

## Bounds

The problem is a linear program, so it is solvable in polynomial time by general LP methods, and strongly polynomial algorithms exist (Tardos; Orlin). For integer data, the almost-linear algorithm matches the input size up to $m^{o(1)}$ and logarithmic factors. The incidence matrix is totally unimodular, so with integer capacities and supplies some optimal flow is integral, whatever the costs; see the [integrality theorem](/integrality-theorem/). The trivial lower bound is $\Omega(n + m)$.

## Reductions

- **Shortest path.** Supply 1 at $s$, demand 1 at $t$, infinite capacities: the optimal flow is a shortest path when there is no negative cycle.
- **Maximum flow.** Add an edge $t \to s$ of infinite capacity and cost $-1$, give all other edges cost 0, and ask for a min-cost circulation.
- **Assignment and weighted bipartite matching.** Unit supplies on one side and unit demands on the other.
- **Supplies to $s$-$t$ form.** Add a super-source with edges to each supply vertex of capacity $b(v)$, and a super-sink in the same way; a feasible flow exists if and only if the maximum flow saturates them.
- **Feasibility to maximum flow.** Whether any feasible flow exists, ignoring costs, is one maximum flow by the previous reduction.

## Applications

- Transportation and distribution planning, the origin of the problem.
- Assignment of workers to jobs, and weighted bipartite matching.
- Scheduling with deadlines and machine capacities, and crew scheduling.
- Discrete optimal transport between two histograms, and earth mover's distance.
- Minimum-cost edge-disjoint paths, which is $d$ units with unit capacities.

## References
