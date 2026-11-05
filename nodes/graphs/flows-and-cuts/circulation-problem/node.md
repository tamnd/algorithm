---
tag: DKY4J6
kind: problem
slug: circulation-problem
name: Circulation with demands problem
aliases:
- flow with lower bounds
- feasible circulation
area: graphs/flows-and-cuts
level: core
summary: Find a flow satisfying lower and upper bounds and given supplies and demands.
prereqs: [flow-network, flow-conservation, max-flow-problem]
see_also: [hoffman-circulation-theorem, airline-scheduling, survey-design-problem, min-cost-flow-problem, flow-integrality-theorem, cycle-canceling, flow-decomposition]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.7, Extensions to the Maximum-Flow Problem (circulations with demands, the reduction to maximum flow, and circulations with demands and lower bounds)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 6, Maximum Flows, Basic Ideas (feasible flow problems and flows with lower bounds)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 11, Applications of Flows and Cuts (flows with balance constraints and with lower bounds)
---

The circulation with demands problem asks for a flow on a directed graph that obeys a lower and an upper bound on each edge and has a prescribed net inflow at each vertex. Vertices with negative demand are supplies and those with positive demand are sinks. It has no single source and sink, but one [maximum flow](/max-flow-problem/) computation on a network with an added super-source and super-sink solves it, and [Hoffman's circulation theorem](/hoffman-circulation-theorem/) says exactly when a solution exists. It is the model behind [airline scheduling](/airline-scheduling/), [survey design](/survey-design-problem/) and many other feasibility questions.

## In plain words

Some towns produce goods, some need goods, and one-way roads join them. Each road has a limit, and some roads also have a minimum that a contract demands. Can you ship goods so that each producer sends exactly what it makes, each consumer gets exactly what it needs, each other town passes on what it gets, and each road stays between its minimum and its limit?

First send the minimum along each road that has one, and note what each town now owes or holds. Then add one master source that feeds every town with goods to give, and one master sink that collects from every town that still needs goods. A plan exists exactly when the largest flow from the master source to the master sink fills all the roads out of the master source.

## Definition

**Input.** A directed graph $G = (V, E)$, a lower bound $\ell(e)$ and an upper bound (capacity) $c(e)$ on each edge with $0 \le \ell(e) \le c(e)$, and a demand $d(v)$ for each vertex. All numbers are reals; when they are integers, see the integrality note below. Antiparallel and parallel edges are allowed and are separate edges, each with its own bounds.

**Output.** A *feasible circulation*: a function $f : E \to \mathbb{R}$ with

$$\ell(e) \le f(e) \le c(e) \quad \text{for each } e \in E, \qquad f^{\text{in}}(v) - f^{\text{out}}(v) = d(v) \quad \text{for each } v \in V,$$

or the answer that none exists. Here $f^{\text{in}}(v)$ and $f^{\text{out}}(v)$ are the sums of $f$ over the edges into and out of $v$. A vertex with $d(v) > 0$ takes in $d(v)$ more than it sends (a sink); a vertex with $d(v) < 0$ sends $-d(v)$ more than it takes in (a source). Kleinberg and Tardos use this sign convention; Ahuja, Magnanti and Orlin use $b(v) = -d(v)$ and call a positive $b(v)$ a supply.

**A necessary condition.** Summing the conservation equations over all $v$, each edge adds $f(e)$ once at its head and subtracts it once at its tail, so $\sum_v d(v) = 0$. If the demands do not sum to 0, there is no feasible circulation.

**Integrality.** If all $\ell$, $c$ and $d$ are integers and a feasible circulation exists, an integer-valued one exists. This follows from the reduction below and the [integrality theorem](/flow-integrality-theorem/).

## Variants

- **Circulation without demands.** $d \equiv 0$: conservation at every vertex. With $\ell \equiv 0$ the zero function is feasible, so the question is only interesting with lower bounds or with costs.
- **Demands without lower bounds.** $\ell \equiv 0$. This is the transshipment feasibility problem.
- **Maximum flow as a circulation.** Add an edge $(t, s)$ with $\ell = 0$ and $c = \infty$; a maximum s-t flow is a circulation that maximizes $f(t, s)$. With a lower bound $\ell(t, s) = k$ the question "is there a flow of value at least $k$" becomes a feasibility question.
- **Minimum-cost circulation.** Each edge also has a cost per unit, and the goal is a feasible circulation of least total cost. This is equivalent to the [min-cost flow problem](/min-cost-flow-problem/), and [cycle canceling](/cycle-canceling/) solves it.
- **Minimum flow with lower bounds.** Find an s-t flow of least value that meets all lower bounds. It is solved by a feasible flow followed by a maximum flow from $t$ to $s$ in the residual graph.

## Examples

**A feasible instance.** The vertices are $a, b, c, d$ with $d(a) = -3$, $d(b) = -3$, $d(c) = 2$, $d(d) = 4$, which sum to 0. The edges, with $[\ell, c]$:

| edge | $a b$ | $a c$ | $b c$ | $b d$ | $c d$ |
|---|---|---|---|---|---|
| bounds | [0, 2] | [1, 3] | [0, 2] | [2, 4] | [0, 3] |

*Remove the lower bounds.* Send $\ell(e)$ on each edge first. This gives $L(v) = \sum_{e \text{ into } v} \ell(e) - \sum_{e \text{ out of } v} \ell(e)$: $L(a) = -1$, $L(b) = -2$, $L(c) = 1$, $L(d) = 2$. The remaining demands are $d'(v) = d(v) - L(v)$: $d'(a) = -2$, $d'(b) = -1$, $d'(c) = 1$, $d'(d) = 2$, and the capacities become $c(e) - \ell(e)$: 2, 2, 2, 2, 3.

*Reduce to maximum flow.* Add $s^*$ with edges $(s^*, a)$ of capacity 2 and $(s^*, b)$ of capacity 1, and $t^*$ with edges $(c, t^*)$ of capacity 1 and $(d, t^*)$ of capacity 2. The total positive demand is $D = 3$. A maximum flow has value 3, so a circulation exists. Adding back the lower bounds gives $f(a, b) = 1$, $f(a, c) = 2$, $f(b, c) = 0$, $f(b, d) = 4$, $f(c, d) = 0$. Check: $a$ sends $1 + 2 = 3$; $b$ takes 1 and sends 4, net $-3$; $c$ takes 2; $d$ takes 4.

**An infeasible instance.** Change $d(c)$ to 0, $d(d)$ to 6 and the capacity of $c d$ to 1. The demands still sum to 0, but $d$ can receive at most $c(b, d) + c(c, d) = 4 + 1 = 5 < 6$. The maximum flow in the reduced network is 3, below $D = 4$, and the set $\{a, b, c\}$ reachable from $s^*$ in the final residual graph (with $s^*$) is the source side of the violated cut condition of [Hoffman's theorem](/hoffman-circulation-theorem/).

**Demands that do not sum to zero.** $d(a) = -1$, $d(b) = 2$ with one edge $a b$ of capacity 5: no circulation, since $-1 + 2 \ne 0$.

**Lower bounds alone can be infeasible.** One vertex pair with edges $a b$ of bounds $[2, 3]$ and $b a$ of bounds $[0, 1]$ and $d \equiv 0$: the antiparallel edge $b a$ must return all that $a b$ carries, but it carries at most 1 while $a b$ carries at least 2. Infeasible.

**A zero-capacity edge** with $\ell = c = 0$ is the same as no edge. An edge with $\ell = c > 0$ fixes the flow on it; it moves $\ell$ units of demand from its head to its tail and leaves an edge of capacity 0.

**Real values.** $d(a) = -\sqrt 2$, $d(b) = \sqrt 2$, one edge $a b$ with bounds $[0, 2]$: the circulation $f(a, b) = \sqrt 2$ is feasible.

## Known algorithms

- **Reduction to one maximum flow.** As in the example: remove the lower bounds, add $s^*$ and $t^*$, and run any maximum flow algorithm, such as [Dinic's algorithm](/dinic/), [push-relabel](/push-relabel/) or the [almost-linear algorithm](/almost-linear-max-flow/). A feasible circulation exists if and only if the maximum flow value is $D = \sum_{d'(v) > 0} d'(v)$. The reduction adds $O(n)$ edges and takes $O(n + m)$ time.
- **Minimum-cost solvers.** [Cycle canceling](/cycle-canceling/), [cost scaling](/cost-scaling/), [network simplex](/network-simplex/) and [successive shortest paths](/successive-shortest-path/) find a feasible circulation of least cost, which in particular decides feasibility.

**Why the reduction is correct.** Write $g = f - \ell$. Then $\ell \le f \le c$ is $0 \le g \le c - \ell$, and conservation becomes $g^{\text{in}}(v) - g^{\text{out}}(v) = d(v) - L(v) = d'(v)$. So feasible circulations $f$ match feasible $g$ for $(c - \ell, d')$. Given such a $g$, set the flow on $(s^*, v)$ to $-d'(v)$ for $d'(v) < 0$ and on $(v, t^*)$ to $d'(v)$ for $d'(v) > 0$: this is an $s^*$-$t^*$ flow of value $D$, which saturates the cut $\{s^*\}$, so it is maximum. Conversely, a flow of value $D$ saturates every edge at $s^*$ and $t^*$, and dropping $s^*$ and $t^*$ leaves a $g$ with the demands $d'$. Since $\sum_v d'(v) = \sum_v d(v) - \sum_v L(v) = 0$, the total supply equals $D$ too.

## Bounds

Feasibility reduces to one maximum flow in linear time. Conversely, the decision version of maximum flow (is there an s-t flow of value at least $k$?) is a feasibility instance, with the edge $(t, s)$ of lower bound $k$. So the problem is as hard as maximum flow and no harder, and the best bounds are those of maximum flow: $O(nm)$ by Orlin's algorithm (2013) and $m^{1 + o(1)}$ by the [almost-linear algorithm](/almost-linear-max-flow/) of Chen, Kyng, Liu, Peng, Probst Gutenberg and Sachdeva (2022) for integer data. The trivial lower bound is $\Omega(n + m)$, to read the input.

## Reductions

- **To maximum flow**: given above.
- **Bipartite b-matching and transportation feasibility**: supplies on one side, demands on the other, and capacities on the edges, is a circulation with demands without lower bounds.
- **[Airline scheduling](/airline-scheduling/)**: each flight is an edge with lower bound 1 and capacity 1, planes are supply.
- **[Survey design](/survey-design-problem/)**: lower and upper bounds on how many questions each customer answers and how many answers each product gets.
- **Matrix rounding**: rounding each entry and each row and column sum of a real matrix up or down, keeping the sums consistent, is a circulation with lower bounds.

## Applications

Scheduling of crews and vehicles, project staffing with minimum and maximum workloads, matrix rounding in statistics tables, and checking whether given supplies can meet given demands in a transport or power network.

## References
