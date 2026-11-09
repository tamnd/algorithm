---
tag: PH6AGD
kind: problem
slug: shortest-paths-lp-formulation
name: Shortest paths as a linear program
aliases:
- shortest path LP
- linear programming formulation of shortest paths
area: optimization/linear-programming
level: core
summary: Expresses single-pair shortest paths as a linear program using distance variables and edge constraints.
prereqs: [single-pair-shortest-path, dual-linear-program]
see_also: [single-pair-shortest-path, min-cost-flow-lp-formulation, difference-constraints, bellman-ford, dijkstra, shortest-path-optimality-conditions, negative-cycle, potential-function-reduced-costs]
sources:
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Section 29.2, Formulating problems as linear programs (shortest paths), and Section 24.4, Difference constraints and shortest paths
  - book: isbn:9780486402581
    title: Christos H. Papadimitriou and Kenneth Steiglitz, Combinatorial Optimization, Algorithms and Complexity, Dover, 1998
    locator: Chapter 6, Primal-dual algorithms for max-flow and shortest path (the shortest path LP, its dual, and Dijkstra's algorithm as a primal-dual method)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 7.9, The shortest path problem (the formulation as a network flow problem and its dual)
---

The [single-pair shortest path problem](/single-pair-shortest-path/) is a linear program with one distance variable $d_v$ per vertex: maximize $d_t$ subject to $d_v \le d_u + w(u, v)$ for every edge and $d_s = 0$. The edge constraints say that no edge can be relaxed, and the largest $d_t$ that obeys them is the shortest path distance $\delta(s, t)$. Its [dual linear program](/dual-linear-program/) sends one unit of flow from $s$ to $t$ at minimum cost, a special case of [minimum cost flow](/min-cost-flow-lp-formulation/), and its optimal vertices are the shortest paths themselves. A negative cycle anywhere in the graph makes the program infeasible, and a sink that $s$ cannot reach makes it unbounded. The [optimality conditions](/shortest-path-optimality-conditions/) of shortest paths, [difference constraints](/difference-constraints/) and [reduced costs with potentials](/potential-function-reduced-costs/) are all read off this pair of programs.

## In plain words

Give every place a number, its claimed distance from the start, with the start at zero. Add one rule per road: the number at the end of a road may be at most the number at its start plus the road's length. These rules never allow a claimed distance that is longer than the real shortest distance, because you can follow a shortest route road by road. The true distances obey all the rules. So the largest number that the target can get is its true distance. The partner problem is to send one unit of goods from the start to the target at the lowest cost per road, and its best answer is a shortest route.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, edge weights $w \in \mathbb{Q}^E$, a source $s$ and a target $t$.

**The program.**

$$\max\ d_t \quad\text{s.t.}\quad d_v - d_u \le w(u, v) \ \ ((u, v) \in E), \qquad d_s = 0,$$

with $d \in \mathbb{R}^V$ free. This is the form of CLRS. Each constraint is a [difference constraint](/difference-constraints/), and the constraint matrix is the transpose of the node-arc [incidence matrix](/incidence-matrix/).

**Why maximize.** Two facts give $\max d_t = \delta(s, t)$ when $t$ is reachable from $s$ and the graph has no negative cycle.

1. *Every feasible $d$ is a lower bound.* If $s = v_0, v_1, \ldots, v_k = t$ is a path, adding the constraints along it gives $d_t - d_s \le \sum_i w(v_{i-1}, v_i)$. So $d_t$ is at most the length of every $s$-$t$ path, and at most $\delta(s, t)$.
2. *The distances are feasible.* $d_v = \delta(s, v)$ satisfies every constraint by the triangle inequality $\delta(s, v) \le \delta(s, u) + w(u, v)$, as long as these values are finite (the four cases below treat the vertices that $s$ cannot reach).

Minimizing $d_t$ instead would be wrong: the constraints are upper bounds only, so the minimum is $-\infty$. The edge constraints push the distances down, and the objective pushes $d_t$ back up until a chain of tight constraints, a shortest path, stops it.

**The dual.** Give the constraint of edge $e$ a multiplier $x_e \ge 0$, and eliminate $d_s = 0$. The column of the free variable $d_v$, $v \ne s$, has $+1$ in the rows of the edges that enter $v$ and $-1$ in the rows of the edges that leave $v$, so the dual is

$$\min \sum_{e \in E} w_e x_e \quad\text{s.t.}\quad \sum_{e \in \delta^{\text{in}}(v)} x_e - \sum_{e \in \delta^{\text{out}}(v)} x_e = [v = t] \ \ (v \ne s), \qquad x \ge 0.$$

This is a flow of value 1 from $s$ to $t$ with cost $w$ and no capacities, a [minimum cost flow](/min-cost-flow-lp-formulation/) problem. Its matrix is totally unimodular, its vertices are the indicator vectors of simple $s$-$t$ paths, and its extreme rays are the directed cycles.

**The four cases.** By [LP duality](/lp-duality/):

| graph | primal (distances) | dual (unit flow) |
|---|---|---|
| $t$ reachable, no negative cycle | optimal, $d_t = \delta(s, t)$ | optimal, a shortest path |
| $t$ reachable, a negative cycle somewhere | infeasible | unbounded |
| $t$ not reachable, no negative cycle | unbounded | infeasible |
| $t$ not reachable, a negative cycle somewhere | infeasible | infeasible |

A negative cycle $C$ makes the primal infeasible because adding its constraints gives $0 \le w(C) < 0$. If there is none, potentials from a [Bellman-Ford](/bellman-ford/) run from a new vertex joined to all vertices by weight 0 edges, shifted so that $d_s = 0$, satisfy all constraints. If $t$ is not reachable, raising $d$ by the same large amount on every vertex that $s$ cannot reach keeps all constraints, because no edge goes from a reachable vertex to an unreachable one.

**Complementary slackness.** For optimal $d$ and a shortest path $P$ (the dual vertex $x = \mathbf{1}_P$), [complementary slackness](/complementary-slackness/) says that every edge of $P$ is tight: $d_v = d_u + w(u, v)$. These are the [shortest path optimality conditions](/shortest-path-optimality-conditions/), and tight edges form the subgraph in which every $s$-$t$ path is shortest.

## Variants

- **Single source.** Maximize $\sum_v d_v$ over the same constraints. Each $d_v$ is at most $\delta(s, v)$ and the vector $\delta(s, \cdot)$ is feasible, so the unique optimum gives all distances at once when every vertex is reachable. The dual is a minimum cost flow with supply $n - 1$ at $s$ and demand 1 at every other vertex, whose vertex solutions are shortest path trees. With the single objective $d_t$, a vertex off every shortest $s$-$t$ path can take any value below its distance.
- **Flow form as the primal.** Many texts take the unit flow program as the primal, $\min w^\top x$ with $x$ a unit $s$-$t$ flow, and the distance program as its dual. The two pages say the same thing.
- **All pairs.** One distance program per source, or one program in $n^2$ variables $d_{uv}$ with the triangle inequalities; this is rarely useful in practice.
- **Potentials only.** Without the objective, the constraints $d_v - d_u \le w(u, v)$ form a system of [difference constraints](/difference-constraints/). It is feasible exactly when there is no negative cycle, and the feasible $d$ are the feasible [potentials](/potential-function-reduced-costs/) that make all reduced costs $w(u, v) + d_u - d_v$ nonnegative.
- **Restricting to relevant vertices.** If the program should give $\delta(s, t)$ whenever it is finite, keep only the vertices that lie on some $s$-$t$ walk. Then the program is infeasible exactly when $\delta(s, t) = -\infty$.

## Examples

**A small graph.** Take the edges $s \to a$ (weight 4), $s \to b$ (2), $b \to a$ (1), $a \to t$ (1) and $b \to t$ (5). The program is

$$\max d_t \quad\text{s.t.}\quad d_a \le 4,\ \ d_b \le 2,\ \ d_a \le d_b + 1,\ \ d_t \le d_a + 1,\ \ d_t \le d_b + 5.$$

- *Primal.* Exact enumeration gives the unique optimum $(d_a, d_b, d_t) = (3, 2, 4)$. Here $d_t = 4$ forces $d_a \ge 3$, then $d_a \le d_b + 1 \le 3$ forces $d_a = 3$ and $d_b = 2$, so every vertex sits at its distance.
- *Dual.* The dual has three vertices, one per $s$-$t$ path: $s \to b \to t$ with cost 7, $s \to a \to t$ with cost 5, and $s \to b \to a \to t$ with cost 4. The minimum, 4, equals the primal maximum, as [strong duality](/strong-duality/) requires.
- *Complementary slackness.* The edges $s \to b$, $b \to a$ and $a \to t$ of the shortest path are tight at $d = (3, 2, 4)$. The edges $s \to a$ (slack 1) and $b \to t$ (slack 3) are not tight, and carry no dual flow.

**A negative cycle.** Add the edge $a \to b$ with weight $-2$. The cycle $b \to a \to b$ has weight $1 - 2 = -1$, and the constraints $d_a \le d_b + 1$ and $d_b \le d_a - 2$ add up to $0 \le -1$. The program is infeasible, and its dual is unbounded: route the unit along a path and add any amount of flow around the cycle.

**An unreachable negative cycle.** Keep the original graph and add two new vertices $p$ and $q$ with the edges $p \to q$ (weight 1) and $q \to p$ (weight $-3$), not connected to the rest. The distance from $s$ to $t$ is still 4, and [Bellman-Ford](/bellman-ford/) from $s$ reports no negative cycle, but the program is infeasible. This is why one should drop the vertices that are not on an $s$-$t$ walk before solving.

## Known algorithms

| method | in LP terms | time |
|---|---|---|
| General LP methods | solve the program directly | polynomial, but slower than the graph methods |
| [Bellman-Ford](/bellman-ford/) | starts with $d$ above the optimum (infinite except at $s$) and repairs one violated constraint at a time by [edge relaxation](/edge-relaxation/), so $d_v \ge \delta(s, v)$ always holds; it stops at a feasible $d$, which is then optimal | $O(nm)$ |
| [Dijkstra](/dijkstra/) | the primal-dual method on this pair: it raises the dual potentials and adds tight edges one at a time; needs $w \ge 0$ | $O(m + n \log n)$ with a Fibonacci heap |
| [Network simplex](/network-simplex/) on the dual flow program | spanning tree bases are shortest path tree candidates, and pivots are edge relaxations that change the tree | polynomial pivot rules exist |
| Reweighting with potentials | a feasible $d$ for the difference constraints turns all weights nonnegative, so that Dijkstra applies | one Bellman-Ford run, then Dijkstra |

**Why the graph methods are fast.** The edge constraints have only two variables each, with coefficients $+1$ and $-1$. For such systems a violated constraint can be fixed by changing one variable, and the order of the fixes, by distance in Dijkstra's method or in rounds in Bellman-Ford, bounds the total work. A general LP method does not see this structure.

## Bounds

- **Size.** $n - 1$ free variables and $m$ constraints with two nonzeros each, $+1$ and $-1$.
- **Integrality.** The matrix is totally unimodular. Integral weights give an integral optimal $d$, and the dual vertices are $0$-$1$ path vectors.
- **Optimal faces.** The primal optimum need not be unique: only the vertices on shortest $s$-$t$ paths are pinned to their distances. The optimal dual solutions are the convex combinations of shortest paths plus any nonnegative flow on cycles of weight 0, so the dual optimum is unique exactly when the shortest path is unique and no cycle has weight 0.
- **Complexity.** The single-pair problem has no known algorithm that is faster in the worst case than single-source. For general real weights, Bellman-Ford's $O(nm)$ was first beaten by Fineman (2024). For integral weights, the almost-linear time minimum cost flow algorithm, an interior point method on the dual flow program, also gives negative weight shortest paths in $m^{1 + o(1)}$ time.

## Reductions

- **Shortest path to LP.** The program above.
- **Shortest path to minimum cost flow.** The dual: one unit from $s$ to $t$; see [minimum cost flow as an LP](/min-cost-flow-lp-formulation/).
- **Difference constraints to shortest paths.** A system $x_j - x_i \le b_k$ is feasible exactly when the constraint graph has no negative cycle, and the distances from an added source give a solution (CLRS 24.4). This is the same LP read in the other direction.
- **Negative cycle detection to LP feasibility.** The graph has a negative cycle exactly when the distance constraints without an objective are infeasible, and a [Farkas](/farkas-lemma/) certificate of infeasibility is a nonnegative combination of edge rows that sums to $0 \le$ a negative number. Its weights form a circulation of negative cost, and every such circulation contains a negative cycle.

## Applications

- Proofs: the LP view gives short proofs of the shortest path optimality conditions and of the correctness of Bellman-Ford and Dijkstra through duality.
- Potentials: a feasible $d$ is a set of node potentials that makes all reduced costs nonnegative, which is what Johnson's all-pairs algorithm and [successive shortest paths](/successive-shortest-path/) use.
- Modeling: shortest paths with extra linear side constraints, such as a resource budget, are LPs and integer programs built on this one; the side constraints break total unimodularity.
- Scheduling: earliest and latest start times in a project network are optimal $d$ for difference constraints from precedence relations.

## References
