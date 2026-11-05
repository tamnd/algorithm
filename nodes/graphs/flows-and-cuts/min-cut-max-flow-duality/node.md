---
tag: 4KTEHX
kind: concept
slug: min-cut-max-flow-duality
name: Max-flow min-cut duality
aliases:
- LP duality of max flow
area: graphs/flows-and-cuts
level: intro
summary: The max-flow and min-cut problems are LP primal and dual, giving certificates of optimality.
prereqs: [max-flow-problem, min-cut-problem, lp-duality]
see_also: [max-flow-min-cut-theorem, max-flow-lp-formulation, strong-duality, complementary-slackness, integrality-theorem, total-unimodularity, multicut-problem, sparsest-cut-problem]
sources:
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 7, Linear programming and reductions (Section 7.2 on flows in networks, and Section 7.4 on duality, with max flow as the example)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 10, Maximum flow, and Chapter 13, Path and flow polyhedra and total unimodularity
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 9, Minimum Cost Flows, Basic Algorithms (the linear programming dual of a network flow problem, node potentials, and complementary slackness)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer (2001)
    locator: Chapter 12, Introduction to LP-duality (the max-flow min-cut LP pair and its integrality), and Chapter 20, Multicut in general graphs
---

Max-flow min-cut duality is the fact that the [maximum flow problem](/max-flow-problem/), written as a linear program, has as its [LP dual](/lp-duality/) a linear program whose optimal solutions include the incidence vectors of [minimum $s$-$t$ cuts](/min-cut-problem/). [Weak duality](/weak-duality/) is the bound "flow at most cut", [strong duality](/strong-duality/) is the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), and [complementary slackness](/complementary-slackness/) says which edges a minimum cut must saturate. The view explains why a flow and a cut certify each other, and it is the template for the approximate min-max theorems of [multicut](/multicut-problem/) and [sparsest cut](/sparsest-cut-problem/).

## In plain words

There are two ways to argue about how much can pass from a source to a sink. One person proposes a plan for sending goods. Another person proposes a set of links to block, and notes that every route must use one of them. The first plan shows that "at least this much" is possible, and the block shows that "at most this much" is possible.

Duality says these two kinds of argument always meet: the best plan and the cheapest block have the same value. It also says what the meeting looks like. Every blocked link that leads away from the source side is full, and every link that leads back into the source side is empty. So when someone hands you a plan and a block with the same value, you can check both in one pass, without trusting how they were found.

## The idea

**Setting.** $G = (V, E)$ is a finite directed graph, possibly with parallel and antiparallel edges, with real capacities $c(e) \ge 0$ and $s \ne t$. To keep the LP short, add a new edge $r = (t, s)$ with no upper bound and ask for a circulation that maximizes the flow on $r$; the flow on $r$ is the value of the $s$-$t$ flow on the other edges.

**Primal (flow).** Variables $x_e$ for $e \in E \cup \{r\}$.

$$\max\ x_r \quad \text{s.t.} \quad \sum_{e \in \delta^{\mathrm{in}}(v)} x_e - \sum_{e \in \delta^{\mathrm{out}}(v)} x_e = 0 \ \ (v \in V), \qquad 0 \le x_e \le c(e)\ \ (e \in E), \qquad x_r \ge 0.$$

**Dual (fractional cut).** One free variable $p_v$ for each conservation row, and one variable $d_e \ge 0$ for each bound $x_e \le c(e)$. The column of $x_e$, $e = (u, v)$, has $+1$ in row $v$ and $-1$ in row $u$; the column of $x_r$ has $+1$ in row $s$ and $-1$ in row $t$. Taking the dual by the usual rules gives

$$\min\ \sum_{e \in E} c(e)\, d_e \quad \text{s.t.} \quad d_e \ge p_u - p_v \ \ (e = (u, v) \in E), \qquad p_s - p_t \ge 1, \qquad d \ge 0.$$

Read $p$ as a height: the source stands at least one unit above the sink, and an edge pays $c(e)$ for each unit of height it descends.

**Cuts are dual solutions.** For an $s$-$t$ cut $S$, set $p_v = 1$ for $v \in S$, $p_v = 0$ otherwise, $d_e = 1$ for the edges from $S$ to $V \setminus S$, and $d_e = 0$ for the rest. This is feasible, and its objective is the cut capacity $c(S)$. So the dual optimum is at most the minimum cut.

**Every dual solution rounds to a cut that is no worse.** Let $(p, d)$ be feasible. Shift all $p_v$ by the same constant so that $p_t = 0$; this keeps feasibility, and then $p_s \ge 1$. For $\theta \in (0, 1]$ let $S_\theta = \{ v : p_v \ge \theta \}$. Then $s \in S_\theta$ and $t \notin S_\theta$. An edge $(u, v)$ goes from $S_\theta$ to its complement exactly when $p_v < \theta \le p_u$. If $\theta$ is uniform on $(0, 1]$, this happens with probability at most $\max(0, p_u - p_v) \le d_e$. So the expected capacity of $S_\theta$ is at most $\sum_e c(e) d_e$, and some $\theta$ gives a cut whose capacity is at most the dual objective. Only the finitely many values $\theta \in \{p_v\} \cap (0, 1]$ give different sets, so the best one is found by trying them.

**Together.** The dual optimum equals the minimum cut capacity. LP strong duality then gives max flow equal to min cut, a second proof of the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). The dual also has an integral optimum by [total unimodularity](/total-unimodularity/); the rounding above makes this explicit.

**Complementary slackness.** A feasible flow $x$ and a feasible dual $(p, d)$ are both optimal exactly when

- $d_e > 0$ implies $x_e = c(e)$: each edge that the cut pays for is full;
- $x_e > 0$ implies $d_e = p_u - p_v$: an edge with flow does not descend less than it pays for, and for a 0-1 cut this means an edge with flow never climbs from $V \setminus S$ back into $S$.

For a 0-1 solution from a cut $S$ these are the conditions "edges out of $S$ are full, edges into $S$ are empty" of the max-flow min-cut proof.

**Path form.** Another primal uses one variable per $s$-$t$ path $P$: maximize $\sum_P y_P$ subject to $\sum_{P \ni e} y_P \le c(e)$. Its dual is: minimize $\sum_e c(e) \ell_e$ over lengths $\ell \ge 0$ such that every $s$-$t$ path has length at least 1. This "distance" view is the one that extends to several commodities, where the rounding step loses a factor, which is the source of the $O(\log k)$ gaps of [multicut](/multicut-problem/) and [sparsest cut](/sparsest-cut-problem/).

## Examples

The network has the edges $s \to a$ (3), $s \to b$ (2), $a \to b$ (1), $a \to t$ (2), $b \to t$ (3).

- **Primal.** The flow $x = (3, 2, 1, 2, 3)$ in the order of the edges above has value 5.
- **An integral dual.** $p = 1$ on $\{s\}$ and 0 elsewhere, with $d = 1$ on $s \to a$ and $s \to b$. The objective is $3 + 2 = 5$, so both are optimal.
- **A fractional optimal dual.** $p_s = 1$, $p_a = p_b = \frac12$, $p_t = 0$, with $d = \frac12$ on $s \to a$, $s \to b$, $a \to t$, $b \to t$ and $d_{ab} = 0$. The objective is $\frac32 + 1 + 1 + \frac32 = 5$, also optimal. Rounding with $\theta \le \frac12$ gives $S = \{s, a, b\}$ of capacity $2 + 3 = 5$, and with $\theta > \frac12$ it gives $S = \{s\}$ of capacity 5. Complementary slackness holds: all edges with $d_e > 0$ are full, and on $a \to b$, which carries 1, $d_{ab} = 0 = p_a - p_b$.
- **A zero-capacity edge** contributes $c(e) d_e = 0$ for every $d_e$, so the dual can set $d_e$ as large as needed; the edge never limits the cut.
- **No $s$-$t$ path.** Let $R$ be the set of vertices that $s$ reaches. Set $p = 1$ on $R$ and 0 elsewhere. No edge leaves $R$, so $d = 0$ is feasible, and the dual optimum is 0, which matches the zero flow.

## Where it is used

- **Certificates.** A flow and a cut of the same value prove optimality in $O(m)$ time to check; see the [minimum cut problem](/min-cut-problem/).
- **Minimum-cost flow.** The dual variables $p$ become node potentials and reduced costs; see the [min-cost flow problem](/min-cost-flow-problem/), [successive shortest paths](/successive-shortest-path/) and the [network simplex method](/network-simplex/).
- **Continuous algorithms.** Interior-point methods for flows solve the primal and the dual together; see [electrical flows](/electrical-flow/) and the [almost-linear max-flow algorithm](/almost-linear-max-flow/).
- **Approximation.** The rounding by a random threshold is the simplest case of LP rounding by region growing, used for [multicut](/multicut-problem/) and [multiway cut](/multiway-cut-problem/), and the path-form dual is the starting point of [sparsest cut](/sparsest-cut-problem/) approximations.

## References
