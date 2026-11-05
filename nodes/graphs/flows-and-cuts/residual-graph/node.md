---
tag: 1G3HX1
kind: concept
slug: residual-graph
name: Residual graph
aliases:
- residual network
area: graphs/flows-and-cuts
level: intro
summary: Graph of remaining capacities, with reverse edges that allow undoing flow.
prereqs: [s-t-flow, flow-network]
see_also: [augmenting-path-flow, ford-fulkerson, edmonds-karp, level-graph, max-flow-min-cut-theorem, min-cut-problem, successive-shortest-path, push-relabel]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.2, The Ford-Fulkerson method (residual networks, augmentation of a flow by a residual flow, and augmenting paths)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.1, The Maximum-Flow Problem and the Ford-Fulkerson Algorithm (the residual graph, forward and backward edges, and the augment procedure)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Section 2.4, Network transformations (residual networks), and Chapter 6, Maximum Flows, Basic Ideas
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (residual graphs in the proof of the max-flow min-cut theorem)
---

The residual graph $G_f$ of an [$s$-$t$ flow](/s-t-flow/) $f$ in a [flow network](/flow-network/) is the directed graph of the changes that $f$ still permits. Each edge with room left gives a *forward* residual edge, and each edge with flow on it gives a *backward* residual edge that can send flow back and so undo it. An $s$-$t$ path in $G_f$ is an [augmenting path](/augmenting-path-flow/), and $f$ is a maximum flow exactly when no such path exists. Every augmenting-path and preflow algorithm for maximum flow, and the shortest-path methods for minimum-cost flow, work on this graph.

## In plain words

Think of pipes that already carry some water. For each pipe you can ask two questions. How much more can it carry in its own direction? And how much of what it carries could you take back? The first answer is the room that is left. The second answer is the amount that already flows, because taking water back means sending less through the pipe.

The residual graph draws one arrow for each nonzero answer. The first kind of arrow points the same way as the pipe. The second kind points the opposite way. If you can walk along arrows from the source to the sink, you can push more water through and the current plan is not the best. If you cannot, the plan is already the best one.

## The idea

**Assumptions.** $N = (G, c, s, t)$ is a flow network with $G = (V, E)$ directed, $n = |V|$, $m = |E|$, and real capacities $c(e) \ge 0$. Parallel edges, antiparallel edges and edges of capacity 0 are allowed. The flow $f$ meets the capacity constraint and conservation.

**Definition.** For each edge $e = (u, v) \in E$ there are two candidate residual edges:

- the forward edge $e^{+} = (u, v)$ with residual capacity $c_f(e^{+}) = c(e) - f(e)$;
- the backward edge $e^{-} = (v, u)$ with residual capacity $c_f(e^{-}) = f(e)$.

The residual graph $G_f = (V, E_f)$ keeps each candidate whose residual capacity is positive. Both values are at least 0 by the capacity constraint, and $c_f(e^{+}) + c_f(e^{-}) = c(e)$. So $|E_f| \le 2m$, and $G_f$ is built in $O(n + m)$ time.

**Antiparallel edges.** The definition works edge by edge. If $E$ holds both $e_1 = (u, v)$ and $e_2 = (v, u)$, then $G_f$ can hold up to two edges from $u$ to $v$ (namely $e_1^{+}$ and $e_2^{-}$) and up to two from $v$ to $u$. These are parallel residual edges, and an algorithm treats them as separate. A book that merges them uses $c_f(u, v) = c(u, v) - f(u, v) + f(v, u)$, which is the sum of the two. Both views give the same augmenting paths and the same maximum flow. In code, the usual layout stores edge $2i$ as $e_i^{+}$ and edge $2i + 1$ as $e_i^{-}$, so the partner of residual edge $j$ is $j \oplus 1$, and the network needs no merging.

**Augmentation.** Let $P$ be an $s$-$t$ path in $G_f$ and let $0 < \delta \le \min_{r \in P} c_f(r)$. Define $f'$ by $f'(e) = f(e) + \delta$ when $e^{+} \in P$, $f'(e) = f(e) - \delta$ when $e^{-} \in P$, and $f'(e) = f(e)$ otherwise. A simple path uses each residual edge at most once. If $P$ used both $e^{+} = (u, v)$ and $e^{-} = (v, u)$, it would visit $u$ or $v$ twice, which a simple path does not do. So each original edge changes at most once.

**Lemma (augmentation).** $f'$ is an $s$-$t$ flow, and $|f'| = |f| + \delta$.

*Proof.* Capacity: if $e^{+} \in P$, then $f'(e) = f(e) + \delta \le f(e) + c(e) - f(e) = c(e)$, and $f'(e) \ge f(e) \ge 0$. If $e^{-} \in P$, then $f'(e) = f(e) - \delta \ge 0$, and $f'(e) \le c(e)$. Conservation: take $v \notin \{s, t\}$ on $P$, entered by residual edge $r_1$ and left by $r_2$. Entering by a forward edge raises $f^{\mathrm{in}}(v)$ by $\delta$; entering by a backward edge of an edge out of $v$ lowers $f^{\mathrm{out}}(v)$ by $\delta$. Leaving by a forward edge raises $f^{\mathrm{out}}(v)$; leaving by a backward edge of an edge into $v$ lowers $f^{\mathrm{in}}(v)$. In all four cases, $f^{\mathrm{in}}(v) - f^{\mathrm{out}}(v)$ changes by $+\delta - \delta = 0$. Value: $P$ leaves $s$ once and never enters it. Its first edge either raises $f^{\mathrm{out}}(s)$ or lowers $f^{\mathrm{in}}(s)$ by $\delta$, so $|f|$ grows by $\delta$. $\square$

**Lemma (optimality).** $f$ is a maximum flow if and only if $G_f$ has no $s$-$t$ path. In that case, the set $S$ of vertices that $s$ reaches in $G_f$ is the source side of a [minimum cut](/min-cut-problem/).

*Proof.* If $G_f$ has an $s$-$t$ path, augmentation gives a larger flow. If it has none, $t \notin S$. Each edge $(u, v)$ with $u \in S$, $v \notin S$ has $c_f(e^{+}) = 0$, so $f(e) = c(e)$. Each edge $(v, u)$ with $v \notin S$, $u \in S$ has $c_f(e^{-}) = 0$, so $f(e) = 0$. By the cut lemma of the [$s$-$t$ flow](/s-t-flow/) page, $|f|$ equals the capacity of $(S, V \setminus S)$, which bounds every flow. So $f$ is maximum and the cut is minimum. $\square$

This is the core of the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). A stronger form holds: for each flow $f^{*}$, the function $f^{*} - f$, read as forward residual flow where it is positive and backward residual flow where it is negative, is a feasible flow in $G_f$ of value $|f^{*}| - |f|$. So the residual graph of $f$ holds all the ways to reach any other flow.

**Costs.** When each edge also has a cost $a(e)$, the forward edge gets cost $a(e)$ and the backward edge gets cost $-a(e)$, because undoing a unit saves its cost. A flow of a given value has minimum cost if and only if $G_f$ has no cycle of negative cost; see the [min-cost flow problem](/min-cost-flow-problem/).

## Examples

**A backward edge is needed.** The network has the edges $s \to a$, $s \to b$, $a \to b$, $a \to t$, $b \to t$, each of capacity 1. Send 1 unit along the path $s \to a \to b \to t$. The residual graph is:

| original edge | flow | forward residual | backward residual |
|---|---|---|---|
| $s \to a$ | 1 | none | $a \to s$, 1 |
| $s \to b$ | 0 | $s \to b$, 1 | none |
| $a \to b$ | 1 | none | $b \to a$, 1 |
| $a \to t$ | 0 | $a \to t$, 1 | none |
| $b \to t$ | 1 | none | $t \to b$, 1 |

The only $s$-$t$ path in $G_f$ is $s \to b \to a \to t$, with bottleneck 1. It uses the backward edge $b \to a$, which removes the unit from $a \to b$. The new flow is 1 on $s \to a$, $s \to b$, $a \to t$, $b \to t$ and 0 on $a \to b$, with value 2. Now $s$ reaches no vertex in $G_f$ (both edges out of $s$ are full), so $S = \{s\}$, and the cut $\{s\}$ of capacity 2 proves the flow is maximum. Without backward edges, the first choice of path would get stuck at value 1.

**Antiparallel edges.** Take $e_1 = (u, v)$ with $c = 3$, $f = 1$ and $e_2 = (v, u)$ with $c = 2$, $f = 2$. The residual edges are $e_1^{+} = (u, v)$ with 2, $e_1^{-} = (v, u)$ with 1, and $e_2^{-} = (u, v)$ with 2; $e_2^{+}$ has residual capacity 0 and is absent. So $u$ can send 4 more to $v$ in total, and $v$ can send 1 to $u$, which matches the merged formula $3 - 1 + 2 = 4$ and $2 - 2 + 1 = 1$.

**A zero-capacity edge** has $c(e) = 0$, so $f(e) = 0$ and both residual capacities are 0. It never appears in $G_f$.

**No $s$-$t$ path.** If $G$ has no $s$-$t$ path through edges of positive capacity, then $G_0$, the residual graph of the zero flow, has none either. The zero flow is maximum, and $S$ is the set that $s$ reaches.

## Where it is used

- [Ford-Fulkerson](/ford-fulkerson/), [Edmonds-Karp](/edmonds-karp/), [capacity scaling](/capacity-scaling/) and the [maximum-capacity augmenting path](/maximum-capacity-augmenting-path/) rule search $G_f$ for augmenting paths.
- [Dinic's algorithm](/dinic/) and the [MPM algorithm](/mpm-algorithm/) find [blocking flows](/blocking-flow/) in the [level graph](/level-graph/), a subgraph of $G_f$.
- [Push-relabel](/push-relabel/) pushes [preflow](/preflow/) along residual edges whose ends differ in height by one.
- Finding a [minimum $s$-$t$ cut](/min-cut-problem/) after a maximum flow: the set that $s$ reaches in $G_f$.
- [Successive shortest paths](/successive-shortest-path/) and [cycle canceling](/cycle-canceling/) for minimum-cost flow use the residual graph with costs.

## References
