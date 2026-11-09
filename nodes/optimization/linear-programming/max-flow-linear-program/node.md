---
tag: 0CTT72
kind: concept
slug: max-flow-linear-program
name: Maximum flow as a linear program
aliases:
- Max-flow as linear program
- max-flow LP
- maximum flow LP and its dual
area: optimization/linear-programming
level: core
summary: Expresses the maximum flow problem as a linear program with capacity and conservation constraints, whose dual is the minimum cut problem.
prereqs: [max-flow-problem, dual-linear-program]
see_also: [max-flow-lp-formulation, min-cut-max-flow-duality, max-flow-min-cut-theorem, min-cut-problem, total-unimodularity, complementary-slackness, min-cost-flow-lp-formulation, shadow-price]
sources:
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Section 29.2, Formulating problems as linear programs (the maximum flow linear program)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 7.5, The maximum flow problem, and Section 7.6, Duality in network flow problems
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 10, Maximum flow (the max-flow min-cut theorem), and Chapter 13, Path and flow polyhedra and total unimodularity
---

The [maximum flow problem](/max-flow-problem/) is a linear program: one variable per arc, a capacity bound on each variable, a conservation equation at each node other than the source and the sink, and the net flow out of the source as the objective. Its [dual linear program](/dual-linear-program/) has a potential $\pi_v$ per node and a variable $d_e$ per arc, and its optimal solutions include the indicator vectors of [minimum $s$-$t$ cuts](/min-cut-problem/). So [weak duality](/weak-duality/) is the bound "flow value at most cut capacity", and [strong duality](/strong-duality/) is the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). This page derives the dual and shows why its optimum is a cut. How to solve max flow with an LP solver, and why the answer can be taken integral, is the subject of the companion page [max flow as an LP problem](/max-flow-lp-formulation/); the graph view of the same duality is on [max-flow min-cut duality](/min-cut-max-flow-duality/).

## In plain words

Think of a network of pipes from a source to a sink, each pipe with a limit. Choose an amount for each pipe. Each amount must stay within its pipe's limit, and at every junction the water in must equal the water out. Make the total that leaves the source as large as possible. All of these rules are linear, so this is a linear program. Every linear program has a partner problem that gives upper bounds on its best value. For the flow problem, the partner chooses a group of junctions that holds the source but not the sink, and it pays the limits of the pipes that leave the group. That is a cut, and the best cut equals the best flow.

## The idea

**The primal.** Let $G = (V, E)$ be a directed graph with source $s$, sink $t$ and capacities $c_e \ge 0$. Write $\delta^{\text{out}}(v)$ and $\delta^{\text{in}}(v)$ for the arcs that leave and enter $v$. The flow LP is

$$\begin{aligned} \max\ & \sum_{e \in \delta^{\text{out}}(s)} f_e - \sum_{e \in \delta^{\text{in}}(s)} f_e \\ \text{s.t.}\ & \sum_{e \in \delta^{\text{in}}(v)} f_e - \sum_{e \in \delta^{\text{out}}(v)} f_e = 0 && v \in V \setminus \{s, t\}, \\ & f_e \le c_e && e \in E, \\ & f_e \ge 0 && e \in E. \end{aligned}$$

It has $m = |E|$ variables, $n - 2$ equations and $m$ capacity rows. It is always feasible ($f = 0$) and bounded (the objective is at most the sum of the capacities of the arcs out of $s$), so by [LP duality](/lp-duality/) it has an optimum and so does its dual. In matrix form, with the node-arc [incidence matrix](/incidence-matrix/) $N$ ($N_{v,e} = 1$ if $e$ leaves $v$, $-1$ if $e$ enters $v$) and $N'$ the rows of $N$ for $v \ne s, t$, it reads $\max N_s f$ subject to $N' f = 0$, $0 \le f \le c$.

**The dual, step by step.** Follow the dualization rules of the [dual linear program](/dual-linear-program/) page.

1. Give the conservation equation of node $v$ a multiplier $\pi_v$. The row is an equation, so $\pi_v$ is free.
2. Give the capacity row of arc $e$ a multiplier $d_e \ge 0$. The dual objective is $\sum_e c_e d_e$, to be minimized.
3. Each primal variable $f_e \ge 0$ gives one dual constraint of the form "column of $f_e$ times multipliers $\ge$ objective coefficient of $f_e$". For $e = (u, v)$ the column of $f_e$ has $-1$ in the row of $u$ (the arc leaves $u$), $+1$ in the row of $v$, and $+1$ in its capacity row, so the constraint is
$$-\pi_u + \pi_v + d_e \ \ge\ [u = s] - [v = s],$$
where a term $\pi_s$ or $\pi_t$ is absent because $s$ and $t$ have no row.
4. Put $\pi_s = 1$ and $\pi_t = 0$. Then the four cases ($u$ or $v$ equal to $s$, to $t$, or to neither) all read $d_e \ge \pi_u - \pi_v$.

The dual is therefore

$$\min \sum_{e \in E} c_e d_e \quad\text{s.t.}\quad d_{uv} \ge \pi_u - \pi_v \ \ ((u, v) \in E), \qquad d \ge 0, \qquad \pi_s = 1,\ \pi_t = 0.$$

Read $\pi_v$ as the height of node $v$ and $d_e$ as the drop that arc $e$ is charged for. The source sits at height 1, the sink at height 0, and the program pays $c_e$ for each unit of downward drop along arc $e$.

**Cuts are dual solutions.** For a set $S$ with $s \in S$ and $t \notin S$, put $\pi_v = 1$ on $S$, $\pi_v = 0$ off $S$, and $d_e = 1$ exactly on the arcs that leave $S$. This is dual feasible, and its value is the capacity $c(S)$ of the cut. With weak duality this gives, for every flow $f$ and every cut $S$,

$$\operatorname{val}(f) \ \le\ c(S),$$

which is also easy to see directly: the value equals the flow out of $S$ minus the flow into $S$.

**Some dual optimum is a cut.** The converse needs an argument, since the dual also has fractional solutions.

- *Bounding $\pi$.* Replace each $\pi_v$ by $\min(1, \max(0, \pi_v))$. Clipping to $[0, 1]$ is monotone and does not increase distances, so the new difference $\pi_u - \pi_v$ is at most $\max(0, \pi_u - \pi_v)$ of the old values, and the same $d$ stays feasible. So the dual keeps its optimal value if we add $0 \le \pi \le 1$. The new feasible set contains no line, so the optimum is attained at a vertex.
- *Integral vertices.* The constraint matrix in the variables $(\pi, d)$ is built from the transpose of $N'$, an identity block and bound rows. The incidence matrix of a directed graph is [totally unimodular](/total-unimodularity/), and adding identity rows and columns keeps this property. The right-hand sides are $0$ and $\pm 1$, so every vertex has integral coordinates, and here that means $\pi \in \{0, 1\}^V$ and, at an optimum with $c > 0$, $d_e = \max(0, \pi_u - \pi_v) \in \{0, 1\}$.
- *Reading off the cut.* Let $S = \{v : \pi_v = 1\}$. It contains $s$ and not $t$, and $d_e = 1$ exactly on the arcs that leave $S$. So the dual value is $c(S)$.

With [strong duality](/strong-duality/), the maximum flow value equals the minimum cut capacity. Another proof of the last step, threshold rounding of a fractional $\pi$ at a random level, is on the [max-flow min-cut duality](/min-cut-max-flow-duality/) page; it shows that every optimal $\pi$ is an average of cuts.

**Complementary slackness.** For an optimal flow $f$ and an optimal cut $S$, [complementary slackness](/complementary-slackness/) says: if $d_e > 0$ then the capacity row of $e$ is tight, so every arc leaving $S$ is saturated; and if $f_e > 0$ then $d_e = \pi_u - \pi_v$, which is $-1 < 0$ for an arc entering $S$, impossible for $d_e \ge 0$, so every arc entering $S$ carries no flow. These are the two conditions that the residual graph test of [Ford-Fulkerson](/ford-fulkerson/) checks.

**What the dual sees.** The dual is the LP relaxation of the min cut problem, and the computation above shows that the relaxation is exact. With integer capacities, the primal is exact as well: by the same total unimodularity, it has an integral optimal flow. That half is the topic of [max flow as an LP problem](/max-flow-lp-formulation/).

## Examples

**A network with three minimum cuts.** Take the arcs $s \to a$ (capacity 4), $s \to b$ (2), $a \to b$ (3), $a \to t$ (1) and $b \to t$ (5). The primal is

$$\begin{aligned} \max\ & f_{sa} + f_{sb} \\ \text{s.t.}\ & f_{sa} - f_{ab} - f_{at} = 0 && (a), \\ & f_{sb} + f_{ab} - f_{bt} = 0 && (b), \\ & 0 \le f \le (4, 2, 3, 1, 5), \end{aligned}$$

and the dual is

$$\begin{aligned} \min\ & 4 d_{sa} + 2 d_{sb} + 3 d_{ab} + d_{at} + 5 d_{bt} \\ \text{s.t.}\ & d_{sa} \ge 1 - \pi_a,\ \ d_{sb} \ge 1 - \pi_b,\ \ d_{ab} \ge \pi_a - \pi_b,\ \ d_{at} \ge \pi_a,\ \ d_{bt} \ge \pi_b,\ \ d \ge 0. \end{aligned}$$

Exact enumeration of the vertices gives:

- The unique optimal flow is $f = (4, 2, 3, 1, 5)$, with value 6. Every arc is saturated.
- The optimal dual vertices are the three cuts $S = \{s\}$ (arcs $sa, sb$: $4 + 2 = 6$), $S = \{s, a\}$ (arcs $sb, ab, at$: $2 + 3 + 1 = 6$) and $S = \{s, a, b\}$ (arcs $at, bt$: $1 + 5 = 6$).
- Their average $\pi = (\pi_a, \pi_b) = (2/3, 1/3)$, $d = (1/3, 2/3, 1/3, 2/3, 1/3)$ is also optimal, with value $(4 + 4 + 3 + 2 + 5)/3 = 6$, but it is not a cut. Cutting $\pi$ at a level in $(0, 1/3)$, $(1/3, 2/3)$ or $(2/3, 1)$ gives back the three cuts.
- Complementary slackness holds for each cut: each arc that leaves one of the three sets is saturated, and no arc enters any of them.

**The dual of a single path.** For the path $s \to a \to t$ with capacities 3 and 5, the dual is $\min 3 d_{sa} + 5 d_{at}$ with $d_{sa} \ge 1 - \pi_a$ and $d_{at} \ge \pi_a$. Then $d_{sa} + d_{at} \ge 1$: the dual must put a total drop of 1 on the path, and it puts it on the cheaper arc. The value is 3, the bottleneck capacity. In general the dual constraints imply $\sum_{e \in P} d_e \ge 1$ for every $s$-$t$ path $P$, which is the dual of the path form of the flow LP.

**Shadow prices.** In the first example, raising $c_{sa}$ from 4 to 5 does not raise the maximum flow, because $s \to a$ is not in the cut $\{s, a\}$ or $\{s, a, b\}$. The [shadow price](/shadow-price/) of an arc capacity is 1 for an increase only if the arc lies in every minimum cut. Here no arc is in all three cuts, so no single capacity increase helps.

## Where it is used

- Proving the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) and its relatives ([Menger's theorem](/menger-theorem/), [König's theorem](/konig-theorem/)) from LP duality and total unimodularity.
- Certificates: a flow and a cut with the same value prove each other optimal, which is how solvers and tests check a max-flow answer.
- Solving max flow with a general LP solver, and the integrality of its answer: see [max flow as an LP problem](/max-flow-lp-formulation/).
- The base for other network LPs: [minimum cost flow](/min-cost-flow-lp-formulation/) adds costs and supplies, [shortest paths](/shortest-paths-lp-formulation/) is the minimum cost flow of one unit, and [multicommodity flow](/multi-commodity-flow-problem/) adds one flow per commodity and loses integrality.
- Approximation algorithms: the fractional dual with a length $d_e$ per arc is the starting point of the LP rounding methods for [multicut](/multicut-problem/) and [sparsest cut](/sparsest-cut-problem/), where the relaxation is no longer exact.
- Sensitivity: the [shadow prices](/shadow-price/) of the capacity rows are cut indicators, and they tell which capacity increases raise the maximum flow.

## References
