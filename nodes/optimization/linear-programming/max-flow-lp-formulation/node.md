---
tag: THFKJZ
kind: problem
slug: max-flow-lp-formulation
name: Maximum flow as a linear program
aliases:
- solving max flow by linear programming
- max flow LP formulation
area: optimization/linear-programming
level: core
summary: Expresses the maximum flow problem as a linear program with capacity constraints and flow conservation equalities.
prereqs: [max-flow-linear-program, total-unimodularity]
see_also: [max-flow-linear-program, min-cut-max-flow-duality, flow-integrality-theorem, integrality-theorem, network-simplex, interior-point-method, flow-decomposition, multi-commodity-flow-problem]
sources:
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Section 29.2, Formulating problems as linear programs (maximum flow, and multicommodity flow)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 13, Path and flow polyhedra and total unimodularity (integrality of the flow polyhedron)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications, Prentice Hall, 1993
    locator: Chapter 6, Maximum flows, basic ideas, and Chapter 11, Minimum cost flows, network simplex algorithms (spanning tree solutions and integrality)
  - url: https://arxiv.org/abs/2203.00671
    title: Li Chen, Rasmus Kyng, Yang P. Liu, Richard Peng, Maximilian Probst Gutenberg and Sushant Sachdeva, Maximum flow and minimum-cost flow in almost-linear time, FOCS 2022
    locator: the main theorem (an interior point method on the flow linear program with dynamic data structures)
---

Solving the [maximum flow problem](/max-flow-problem/) as a linear program means writing it with one variable per arc, capacity bounds and conservation equations, handing it to an LP method, and reading a maximum flow off the answer. The formulation and its dual, the minimum cut, are derived on the companion page [max flow as a linear program](/max-flow-linear-program/). This page is about the computation: the size of the program, what different LP methods return, and why, with integer capacities, the answer can always be taken to be an integral flow. The reason is that the constraint matrix is [totally unimodular](/total-unimodularity/), so every vertex of the feasible region is integral; the [simplex method](/simplex-method/) returns a vertex, while an [interior point method](/interior-point-method/) can return a fractional optimum that needs one rounding pass.

## In plain words

You can solve a flow problem with a general tool for linear programs instead of a special flow algorithm. You write one unknown per pipe, add the limits and the balance rules, and ask the tool for the largest total. One worry is that the tool may answer with fractions, such as half a truck on a road, even when every limit is a whole number. For flow problems this worry goes away. The corners of the allowed region are all whole-number flows, and a method that walks from corner to corner always stops at one. A method that moves through the inside can stop between two best corners, but a short clean-up step pushes it onto one of them.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n$ nodes and $m$ arcs, a source $s$, a sink $t$, and capacities $c \in \mathbb{Q}_{\ge 0}^E$.

**The program.** With $\delta^{\text{in}}(v)$ and $\delta^{\text{out}}(v)$ the arcs entering and leaving $v$,

$$\begin{aligned} \max\ & \sum_{e \in \delta^{\text{out}}(s)} f_e - \sum_{e \in \delta^{\text{in}}(s)} f_e \\ \text{s.t.}\ & \sum_{e \in \delta^{\text{in}}(v)} f_e = \sum_{e \in \delta^{\text{out}}(v)} f_e && v \in V \setminus \{s, t\}, \\ & 0 \le f_e \le c_e && e \in E. \end{aligned}$$

In matrix form this is $\max N_s f$ subject to $N' f = 0$, $0 \le f \le c$, where $N$ is the node-arc [incidence matrix](/incidence-matrix/) and $N'$ its rows for $v \ne s, t$.

**Output.** An optimal $f$, which is a maximum flow, and its value. If $c$ is integral, an optimal $f$ that is integral as well.

**Integrality.** If $c$ is integral, every vertex of the feasible region $F = \{f : N' f = 0,\ 0 \le f \le c\}$ is integral. The constraint matrix of $F$ consists of the rows of $N'$, their negatives and the rows $\pm I$; the incidence matrix of a directed graph is totally unimodular, and these operations keep that property. A vertex is the unique solution of $m$ linearly independent tight rows, so by Cramer's rule its coordinates are integers. Since $F$ is a nonempty polytope, the optimum is attained at a vertex, which is the [flow integrality theorem](/flow-integrality-theorem/) in LP form. The same holds for the dual, whose integral optima are the minimum cuts.

**Vertices as forests.** A feasible flow $f$ is a vertex of $F$ exactly when the arcs with $0 < f_e < c_e$ contain no cycle of the underlying undirected graph. If they contain a cycle, pushing $\pm\varepsilon$ around it gives two feasible flows with midpoint $f$. If they do not, the tight rows fix every coordinate. This is the basis structure of the [network simplex method](/network-simplex/): a basis is a spanning forest, and nonbasic arcs sit at 0 or at capacity.

## Variants

- **Circulation form.** Add an arc $r = (t, s)$ with no capacity, require conservation at every node, and maximize $f_r$. All rows are then of the same type, which makes the dual cleaner; see [max-flow min-cut duality](/min-cut-max-flow-duality/).
- **Path form.** One variable $x_P \ge 0$ per $s$-$t$ path, $\max \sum_P x_P$ subject to $\sum_{P \ni e} x_P \le c_e$. It has exponentially many variables, and [column generation](/column-generation/) solves it with a shortest path as the pricing problem. Every arc flow decomposes into path flows by [flow decomposition](/flow-decomposition/), so both forms have the same value.
- **Undirected graphs.** Replace each edge by two opposite arcs of the same capacity, or use a free variable $f_e$ with $-c_e \le f_e \le c_e$.
- **Lower bounds and several terminals.** Lower bounds $\ell \le f \le c$ and several sources and sinks keep the matrix totally unimodular, so integral data still give integral vertices; the program may now be infeasible.
- **Side constraints.** Extra linear constraints, such as a budget across several arcs, are easy to add to the LP but usually destroy total unimodularity, and the combinatorial flow algorithms no longer apply.
- **Multicommodity flow.** One flow per commodity with a shared capacity per arc ([multicommodity flow](/multi-commodity-flow-problem/)). The LP is still polynomial to solve, but its vertices can be fractional, and the integral version is NP-hard.

## Examples

**A fractional optimum.** Take the arcs $s \to a$, $a \to t$, $a \to b$, $b \to t$, all of capacity 1. The program is $\max f_{sa}$ subject to $f_{sa} = f_{at} + f_{ab}$, $f_{ab} = f_{bt}$ and $0 \le f \le 1$. Exact enumeration gives three vertices, $(f_{sa}, f_{at}, f_{ab}, f_{bt}) = (0, 0, 0, 0)$, $(1, 1, 0, 0)$ and $(1, 0, 1, 1)$, all integral. The optimal set is the segment

$$f_{sa} = 1,\quad f_{at} = \theta,\quad f_{ab} = f_{bt} = 1 - \theta,\qquad 0 \le \theta \le 1.$$

- The simplex method stops at a vertex, $\theta = 0$ or $\theta = 1$: an integral flow along one path.
- A path-following interior point method converges to the analytic center of the optimal face, which is $\theta = 1/2$: half a unit on each path. This is optimal but not integral.
- *Rounding.* The arcs with fractional flow, $a \to t$, $a \to b$ and $b \to t$, form a cycle of the underlying undirected graph. Pushing $1/2$ more unit along $a \to t$ and $1/2$ unit less along $a \to b \to t$ keeps every conservation equation and the value, and it reaches the vertex $\theta = 1$.

**An integral answer with a unique optimum.** For the network $s \to a$ (4), $s \to b$ (2), $a \to b$ (3), $a \to t$ (1), $b \to t$ (5) of the [companion page](/max-flow-linear-program/), the LP has 8 vertices, all integral, and a unique optimum $f = (4, 2, 3, 1, 5)$ of value 6. Every method returns it. The dual has three optimal cuts and fractional optima between them, so here the choice of method matters for the cut and not for the flow.

**Size.** For a graph with 1000 nodes and 10000 arcs, the program has 10000 variables, 998 equations and 10000 upper bounds. Bound constraints are handled implicitly by the bounded simplex method and by interior point methods, so the working matrix is $998 \times 10000$ with two nonzeros per column.

## Known algorithms

| method | answer | time |
|---|---|---|
| [Simplex method](/simplex-method/), bounded-variable form | an optimal vertex, integral for integral $c$ | exponential in the worst case for general pivot rules; fast in practice |
| [Network simplex](/network-simplex/) | the simplex method on spanning tree bases, with integer arithmetic | a primal network simplex rule of Goldfarb and Hao takes at most $nm$ pivots and $O(n^2 m)$ time |
| [Ellipsoid method](/ellipsoid-method/) | a rational optimum, polynomial in the bit length | polynomial, not practical |
| [Interior point method](/interior-point-method/) | an approximate optimum, often in the relative interior of the optimal face; round to a vertex after | $O(\sqrt{m} \log(1/\varepsilon))$ iterations, each a linear system with a Laplacian-like matrix |
| Interior point method with dynamic data structures (Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva, 2022) | an exact integral maximum flow | $m^{1 + o(1)}$ for integral capacities bounded by a polynomial in $m$ |
| Combinatorial methods: [Ford-Fulkerson](/ford-fulkerson/), [Edmonds-Karp](/edmonds-karp/), [Dinic](/dinic/), [push-relabel](/push-relabel/) | an integral maximum flow and a minimum cut | $O(nm^2)$ for Edmonds-Karp, $O(n^2 m)$ for Dinic and push-relabel |

**Rounding a fractional optimum to a vertex.** Given an optimal $f$ with integral $c$:

1. Let $H$ be the set of arcs with fractional $f_e$.
2. While $H$ contains a cycle $C$ of the underlying undirected graph, push flow around $C$ in one of its two directions until the flow of some arc of $C$ becomes an integer. Conservation and the value do not change, so $f$ stays optimal, and $H$ loses at least one arc.
3. When $H$ is a forest, it is empty. A leaf $v \ne s, t$ of $H$ would have one fractional arc and integral other arcs, so conservation at $v$ would fail. So all leaves are $s$ or $t$, and a nonempty forest then has a path from $s$ to $t$ with exactly one fractional arc at $s$, which makes the value fractional. But the maximum flow value equals an integral cut capacity.

Each push removes an arc from $H$, so there are at most $m$ pushes, and the pass costs $O(m^2)$ time with a depth-first search for each cycle. LP solvers call this step *crossover*; for general LPs it is a sequence of simplex pivots, and for flows it is this cycle pushing.

**Why combinatorial methods still win.** The simplex method on this LP is close to an augmenting path method: in the circulation form, a pivot pushes flow around the cycle that the entering arc closes in the basis tree, and a pivot that raises the value is an augmenting $s$-$t$ path closed by the return arc $(t, s)$. The special methods exploit the graph structure that a general LP code ignores, and they return a minimum cut for free. A general solver is the right choice when the flow is one part of a larger LP or has side constraints.

## Bounds

- **Size.** $m$ variables, $n - 2$ equations and $m$ upper bounds. Each column has at most two nonzeros in the equations, both $\pm 1$.
- **Integrality.** For integral $c$, all vertices of the feasible region and of the dual feasible region (with $0 \le \pi \le 1$) are integral. Rational $c$ with common denominator $q$ give vertices in $(1/q)\mathbb{Z}^E$.
- **Vertex count.** The number of vertices can be exponential in $n$. With unit capacities, the indicator vector of every set of arc-disjoint $s$-$t$ paths is a vertex, so a network of $k$ internally disjoint paths has at least $2^k$ vertices.
- **Optimal value.** The value is at most $\sum_{e \in \delta^{\text{out}}(s)} c_e$, and it equals the minimum cut capacity by [strong duality](/strong-duality/).
- **Time.** Max flow is solvable in $m^{1 + o(1)}$ time for integral capacities bounded by a polynomial in $m$, by an interior point method on this LP; no general LP algorithm is known to be that fast on general LPs.

## Reductions

- **Max flow to LP.** The program above, of linear size.
- **Bipartite matching to max flow to LP.** A unit capacity network from a bipartite graph has integral vertices, so the LP relaxation of [bipartite matching](/bipartite-matching/) is exact; this is the LP proof of [König's theorem](/konig-theorem/).
- **Max flow to minimum cost circulation.** Add the arc $(t, s)$ with cost $-1$ and give the other arcs cost 0; see [minimum cost flow as an LP](/min-cost-flow-lp-formulation/).
- **Min cut from the LP.** The dual of the program is the min cut LP. An optimal basis of the primal gives integral dual prices without a second solve, and cutting them at any level strictly between 0 and 1 gives a minimum cut. Simpler still, the nodes reachable from $s$ in the [residual graph](/residual-graph/) of any maximum flow form a minimum cut.

## Applications

- Modeling: max flow problems with side constraints, or as a block inside a larger LP, such as a production plan with a transport network.
- Teaching and verification: the LP gives an independent check of a combinatorial max flow code, and the dual certifies the answer.
- Integrality: the LP proof that integral capacities give an integral maximum flow, and through it [Menger's theorem](/menger-theorem/) and König's theorem.
- Fast algorithms: the almost-linear time algorithms for max flow and [minimum cost flow](/min-cost-flow-problem/) are interior point methods on this LP.

## References
