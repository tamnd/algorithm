---
tag: SNCJ9Y
kind: problem
slug: min-cost-flow-lp-formulation
name: Minimum-cost flow as a linear program
aliases:
- min-cost flow LP
- transshipment LP
- minimum cost network flow linear program
area: optimization/linear-programming
level: core
summary: Expresses minimum-cost flow as a linear program that minimizes total edge cost subject to capacity and conservation constraints.
prereqs: [min-cost-flow-problem, dual-linear-program]
see_also: [min-cost-flow-problem, max-flow-linear-program, shortest-paths-lp-formulation, network-simplex, potential-function-reduced-costs, complementary-slackness, assignment-problem, total-unimodularity]
sources:
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications, Prentice Hall, 1993
    locator: Chapter 9, Minimum cost flows, basic algorithms (the linear programming formulation, its dual, reduced cost and complementary slackness optimality conditions)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 7.2, Formulation of the network flow problem, and Section 7.6, Duality in network flow problems
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 12, Minimum-cost flows and circulations, and Chapter 13, Path and flow polyhedra and total unimodularity
  - paper: doi:10.1007/BF02579369
    title: Éva Tardos, A strongly polynomial minimum cost circulation algorithm, Combinatorica 5, 247 to 255 (1985)
    locator: the first strongly polynomial algorithm for minimum cost circulation
---

The [minimum cost flow problem](/min-cost-flow-problem/) is the linear program that sends given supplies to given demands through a network at the least total cost: one variable per arc, a conservation equation per node with the supply or demand on the right, and capacity bounds. It contains the [maximum flow](/max-flow-linear-program/), [shortest path](/shortest-paths-lp-formulation/), [assignment](/assignment-problem/) and transportation problems as special cases. Its constraint matrix is the node-arc [incidence matrix](/incidence-matrix/), which is [totally unimodular](/total-unimodularity/), so integral supplies and capacities give integral optimal flows, and integral costs give integral optimal duals. The dual has one potential $\pi_v$ per node, and the reduced costs $c_e - \pi_u + \pi_v$ that it defines are the optimality test used by the [network simplex method](/network-simplex/), [successive shortest paths](/successive-shortest-path/) and [cycle canceling](/cycle-canceling/).

## In plain words

Some places have goods, some places need goods, and roads join them. Each road has a limit and a cost per unit. Ship everything at the lowest total cost. With one unknown per road, the rules are linear: each road carries between nothing and its limit, and at each place the goods that leave minus the goods that arrive equal what the place supplies. So the task is a linear program. Its partner problem puts a price on the goods at each place. A road is worth using only if the price difference along it at least pays for the road. When all roads obey this rule, the shipping plan is the cheapest one.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ nodes and $m$ arcs, costs $c \in \mathbb{Q}^E$, capacities $u \in \mathbb{Q}_{\ge 0}^E$, and supplies $b \in \mathbb{Q}^V$ with $\sum_v b_v = 0$. A node with $b_v > 0$ is a supply node, and one with $b_v < 0$ is a demand node.

**The program.** With $\delta^{\text{out}}(v)$ and $\delta^{\text{in}}(v)$ the arcs leaving and entering $v$,

$$\begin{aligned} \min\ & \sum_{e \in E} c_e f_e \\ \text{s.t.}\ & \sum_{e \in \delta^{\text{out}}(v)} f_e - \sum_{e \in \delta^{\text{in}}(v)} f_e = b_v && v \in V, \\ & 0 \le f_e \le u_e && e \in E. \end{aligned}$$

In matrix form, $\min c^\top f$ subject to $N f = b$, $0 \le f \le u$, where $N_{v,e} = 1$ if $e$ leaves $v$ and $-1$ if $e$ enters $v$.

**Output.** An optimal flow $f$, or a proof that no feasible flow exists (an infeasible program), or a proof that the cost is unbounded below (a cycle of negative cost with no capacity limit).

**The rows are dependent.** The rows of $N$ sum to zero, so one equation is implied by the others. For a connected graph, $N$ has rank $n - 1$, and any $n - 1$ of its rows are independent. A basis of the program is a spanning tree of $G$.

**The dual.** Give the equation of node $v$ a free multiplier $\pi_v$ and the upper bound of arc $e$, written $-f_e \ge -u_e$, a multiplier $z_e \ge 0$. The [dual linear program](/dual-linear-program/) is

$$\max \sum_{v \in V} b_v \pi_v - \sum_{e \in E} u_e z_e \quad\text{s.t.}\quad \pi_u - \pi_v - z_e \le c_e \ \ (e = (u, v) \in E), \qquad z \ge 0.$$

Write $c^\pi_e = c_e - \pi_u + \pi_v$ for the *reduced cost* of arc $e = (u, v)$. For fixed $\pi$, the best choice is $z_e = \max(0, -c^\pi_e)$, so the dual is the unconstrained concave problem $\max_\pi \sum_v b_v \pi_v - \sum_e u_e \max(0, -c^\pi_e)$. Adding a constant to every $\pi_v$ changes nothing, which matches the redundant row.

**Optimality conditions.** By [complementary slackness](/complementary-slackness/), a feasible $f$ is optimal exactly when some $\pi$ satisfies, for every arc $e$:

| reduced cost | required flow |
|---|---|
| $c^\pi_e > 0$ | $f_e = 0$ |
| $c^\pi_e < 0$ | $f_e = u_e$ |
| $c^\pi_e = 0$ | any $f_e$ in $[0, u_e]$ |

In the [residual graph](/residual-graph/) of $f$, where the reverse of $e$ has cost $-c_e$, these conditions say that every residual arc has nonnegative reduced cost. That holds for some $\pi$ exactly when the residual graph has no negative cycle, which is the negative cycle optimality condition; see [reduced costs with potentials](/potential-function-reduced-costs/).

**Integrality.** $N$ is totally unimodular, and so is the matrix of the program with its bound rows. Hence, if $b$ and $u$ are integral, every vertex of the feasible region is integral, and if $c$ is integral, every vertex of the dual region is integral. An LP method that returns a vertex returns an integral flow.

## Variants

- **Lower bounds.** $\ell_e \le f_e \le u_e$. Substitute $f_e = \ell_e + f'_e$ and adjust $b$ at the ends of $e$.
- **Circulation.** $b = 0$. Every minimum cost flow problem becomes a [circulation problem](/circulation-problem/) by adding a node that collects the supplies and demands.
- **Uncapacitated transshipment.** No upper bounds. The dual becomes $\max b^\top \pi$ subject to $\pi_u - \pi_v \le c_{uv}$.
- **Transportation.** A bipartite graph from supply nodes to demand nodes, with no capacities. The LP of Hitchcock (1941), Kantorovich and Koopmans.
- **Assignment.** A transportation problem with all supplies and demands equal to 1. Integrality makes its LP relaxation exact, and the [Hungarian algorithm](/hungarian-algorithm/) is a primal-dual method on this LP.
- **Shortest path.** One unit of supply at $s$ and one of demand at $t$, no capacities; see [shortest paths as an LP](/shortest-paths-lp-formulation/).
- **Maximum flow.** Costs 0 on all arcs plus an arc $(t, s)$ of cost $-1$, as a circulation; see [max flow as an LP](/max-flow-linear-program/).
- **Convex costs.** A convex piecewise linear cost on an arc becomes several parallel arcs with increasing costs.
- **Gains and several commodities.** Generalized flows (each arc multiplies the flow by a factor) and [multicommodity flows](/multi-commodity-flow-problem/) are still LPs, but their matrices are not totally unimodular, and their vertices can be fractional.

## Examples

**A four-node network.** Node 1 supplies 4 units and node 4 demands them. The arcs, each with capacity and cost per unit:

| arc | $1 \to 2$ | $1 \to 3$ | $2 \to 3$ | $2 \to 4$ | $3 \to 4$ |
|---|---|---|---|---|---|
| capacity $u_e$ | 4 | 2 | 2 | 3 | 5 |
| cost $c_e$ | 2 | 2 | 1 | 3 | 1 |

The program is $\min 2f_{12} + 2f_{13} + f_{23} + 3f_{24} + f_{34}$ subject to $f_{12} + f_{13} = 4$, $f_{23} + f_{24} - f_{12} = 0$, $f_{34} - f_{13} - f_{23} = 0$, $-f_{24} - f_{34} = -4$, and the bounds.

- *The primal.* Exact enumeration gives 5 vertices, all integral, with costs 14, 16, 18, 18 and 19. The unique optimum is $f = (f_{12}, f_{13}, f_{23}, f_{24}, f_{34}) = (2, 2, 2, 0, 4)$, with cost 14: two units along $1 \to 3 \to 4$ (cost 3 per unit) and two along $1 \to 2 \to 3 \to 4$ (cost 4 per unit). The path $1 \to 2 \to 4$ costs 5 per unit and is not used.
- *The dual.* With $\pi_4 = 0$, the optimal dual vertices are $\pi = (4, 2, 1, 0)$ and $\pi = (5, 3, 1, 0)$. For $\pi = (4, 2, 1, 0)$ the reduced costs are $(0, -1, 0, 1, 0)$, so $z = (0, 1, 0, 0, 0)$, and the dual value is $4 \cdot 4 - 2 \cdot 1 = 14$, equal to the primal cost.
- *The conditions.* Arc $1 \to 3$ has reduced cost $-1 < 0$ and is full; arc $2 \to 4$ has reduced cost $1 > 0$ and is empty; arcs $1 \to 2$ and $3 \to 4$ are strictly between their bounds and have reduced cost 0. Arc $2 \to 3$ is full with reduced cost 0, which is allowed.
- *Meaning of $\pi$.* $\pi_v - \pi_4$ is the marginal cost of one more unit of supply at $v$ that node 4 must absorb. At node 2 the two dual vertices give 2 and 3, and both are right, on different sides. Adding a unit of supply at node 2 costs 3, because it must use $2 \to 4$ ($2 \to 3$ is full). Taking a unit of supply away from node 2 saves 2, because one unit less then moves along $2 \to 3 \to 4$. The two dual vertices are the two one-sided [shadow prices](/shadow-price/) of a degenerate optimum.

**An unbounded program.** If a cycle has negative total cost and every arc on it has no capacity limit, pushing flow around the cycle lowers the cost without end. The dual is then infeasible: summing the dual constraints $\pi_u - \pi_v \le c_{uv}$ around the cycle gives $0 \le$ the cycle cost $< 0$.

## Known algorithms

| algorithm | idea in LP terms | time |
|---|---|---|
| General LP methods ([simplex](/simplex-method/), [interior point](/interior-point-method/)) | solve the program as is | polynomial with interior point methods; vertex solutions are integral |
| [Network simplex](/network-simplex/) | the primal simplex method with spanning tree bases and potentials as multipliers | fast in practice; polynomial pivot rules exist (Orlin, 1997) |
| [Cycle canceling](/cycle-canceling/) (Klein, 1967) | keep a feasible flow, cancel negative cycles of the residual graph | pseudo-polynomial; strongly polynomial with minimum mean cycles (Goldberg and Tarjan, 1989) |
| [Successive shortest paths](/successive-shortest-path/) | keep the reduced cost conditions (dual feasibility), augment along shortest paths until primal feasible | $O(B \cdot S)$ for total supply $B$ and shortest path time $S$ |
| Primal-dual and the [Hungarian algorithm](/hungarian-algorithm/) | raise dual potentials, then route flow on zero reduced cost arcs | polynomial for assignment, $O(n^3)$ |
| Tardos (1985), Orlin (1993) | strongly polynomial scaling | $O(m \log n\, (m + n \log n))$ for Orlin's method |
| Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva (2022) | interior point method on this LP with dynamic data structures | $m^{1 + o(1)}$ for integral data bounded by a polynomial in $m$ |

The combinatorial algorithms are LP algorithms in disguise. Successive shortest paths is a dual method: it keeps $c^\pi \ge 0$ on the residual graph and moves toward primal feasibility. Cycle canceling is a primal method: it keeps a feasible flow and moves along improving directions, which are cycles. The network simplex method is the simplex method itself, specialized.

## Bounds

- **Size.** $m$ variables, $n$ equations of rank $n - 1$ for a connected graph, and $m$ upper bounds. Each column has exactly two nonzeros in the equations, $+1$ and $-1$.
- **Integrality.** Integral $b$ and $u$ give integral primal vertices; integral $c$ gives integral dual vertices. So an integral problem has an integral optimal flow and integral optimal potentials.
- **Bases.** A basis is a spanning tree, so the program has at most as many bases as $G$ has spanning trees.
- **Feasibility.** A feasible flow exists exactly when every set $S$ of nodes satisfies $\sum_{v \in S} b_v \le u(\delta^{\text{out}}(S))$ (Gale's theorem), which is [Farkas' lemma](/farkas-lemma/) for this program.
- **Strong polynomiality.** Unlike general LP, minimum cost flow has strongly polynomial algorithms, whose number of operations does not depend on the sizes of the numbers (Tardos, 1985).

## Reductions

- **To LP.** The program above, with $m$ variables and $n + m$ constraints.
- **From shortest path, max flow, assignment and transportation.** Each is a special case, listed under Variants; the integrality of the minimum cost flow LP gives integrality for all of them.
- **Dual problem.** The dual with $b$ in the objective and differences $\pi_u - \pi_v$ in the constraints is a problem on potentials. With $u = \infty$ it is a system of [difference constraints](/difference-constraints/) with an objective, and minimum cost tension problems in scheduling have exactly this form.
- **To circulation.** Adding a super node turns supplies and demands into a circulation with lower bounds.

## Applications

- Transportation and distribution planning, from Kantorovich's and Hitchcock's first models to modern logistics.
- Assignment of workers to jobs, and bipartite weighted matching.
- Optimal transport between discrete distributions, such as the earth mover's distance, as a transportation LP.
- Project scheduling with time-cost trade-offs, through the dual on potentials.
- Subproblems of larger LPs and of [Lagrangian relaxations](/lagrangian-duality/) whose network part keeps integrality.
- The node prices of the dual as economic prices: the price difference between two places is at most the cost of moving a unit between them, with equality where goods move.

## References
