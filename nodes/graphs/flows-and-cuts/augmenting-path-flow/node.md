---
tag: 3X0TQT
kind: concept
slug: augmenting-path-flow
name: Augmenting path
aliases:
- flow-augmenting path
area: graphs/flows-and-cuts
level: intro
summary: An s-t path in the residual graph along which flow can be increased.
prereqs: [s-t-flow, residual-graph]
see_also: [ford-fulkerson, edmonds-karp, fattest-augmenting-path, capacity-scaling, max-flow-min-cut-theorem, augmenting-path, blocking-flow, dinic]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.2, The Ford-Fulkerson method (residual networks, augmenting paths, the residual capacity of a path, and the lemma that augmenting keeps a flow and raises its value)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.1 (the residual graph and augmenting paths) and Section 7.2 (no augmenting path implies a maximum flow)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (residual graphs and augmenting paths, and the proof of the maxflow-mincut theorem)
  - paper: doi:10.4153/CJM-1956-045-5
    title: L. R. Ford Jr. and D. R. Fulkerson, Maximal flow through a network, Canadian Journal of Mathematics 8, 399 to 404 (1956)
    locator: the whole paper
---

An augmenting path for an [s-t flow](/s-t-flow/) $f$ is a simple path from the source $s$ to the sink $t$ in the [residual graph](/residual-graph/) $G_f$, so a path on which each edge can still take more flow forward or give back flow that it already carries. Pushing the smallest residual capacity of the path along it gives a new flow of larger value. A flow is maximum exactly when it has no augmenting path, and this fact is the core of the [Ford-Fulkerson method](/ford-fulkerson/) and the proof of the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).

## In plain words

Picture pipes from a source to a drain, each with a limit, and some water already flowing. You look for a route from the source to the drain that can take a bit more water. On a pipe that is not full, you can send more in its own direction. On a pipe that already carries water, you can also go against its direction: you send less water through it, and the water you held back can go another way.

The amount you can add on the route is set by its tightest step. After you add it, at least one step of the route is full or empty, and the total that reaches the drain grows by that amount. When no such route is left, the flow is as large as it can be. The proof of this fact also shows the narrowest place of the network.

## The idea

Let $N = (G, c, s, t)$ be a [flow network](/flow-network/) with $G = (V, E)$ directed and capacities $c(e) \ge 0$, real or integer. Let $f$ be an s-t flow. Antiparallel edges are allowed; each edge $e = (u, v)$ has its own pair of residual edges.

**Residual edges.** For each edge $e = (u, v) \in E$, the residual graph $G_f$ has

- a *forward* edge $e^{+} = (u, v)$ with residual capacity $c_f(e^{+}) = c(e) - f(e)$, if this is positive;
- a *backward* edge $e^{-} = (v, u)$ with residual capacity $c_f(e^{-}) = f(e)$, if this is positive.

A zero-capacity edge with zero flow has no residual edge at all.

**Augmenting path.** An augmenting path is a simple path $P$ from $s$ to $t$ in $G_f$. Its *bottleneck*, or residual capacity, is

$$c_f(P) = \min_{x \in P} c_f(x) > 0.$$

**Augmentation.** For $0 < \Delta \le c_f(P)$, define $f'$ by $f'(e) = f(e) + \Delta$ when $e^{+} \in P$, $f'(e) = f(e) - \Delta$ when $e^{-} \in P$, and $f'(e) = f(e)$ otherwise. Since $P$ is simple, it uses at most one of $e^+$ and $e^-$ for each $e$ (a path with a step from $u$ to $v$ and a step from $v$ to $u$ visits one of them twice).

**Lemma 1 (augmentation is a flow of larger value).** $f'$ is an s-t flow and $|f'| = |f| + \Delta$.

*Proof.* Capacity: on a forward edge, $f(e) + \Delta \le f(e) + (c(e) - f(e)) = c(e)$; on a backward edge, $f(e) - \Delta \ge f(e) - f(e) = 0$; other edges keep their values. Conservation: let $v \ne s, t$ be on $P$, entered by residual edge $x$ and left by residual edge $y$. Each of $x$ and $y$ changes the excess of $v$ by $\pm \Delta$. Entering $v$ along a forward edge raises the flow into $v$ by $\Delta$; entering along a backward edge $e^-$ with $e = (v, w)$ lowers the flow out of $v$ by $\Delta$. In both cases the excess of $v$ rises by $\Delta$. In the same way leaving $v$ along $y$, forward or backward, lowers the excess by $\Delta$. So the excess of $v$ stays 0. Vertices off $P$ are not touched. Value: $P$ leaves $s$ once and never returns. Its first edge either raises the flow on an edge out of $s$ or lowers the flow on an edge into $s$; both raise $|f| = f^{\text{out}}(s) - f^{\text{in}}(s)$ by $\Delta$. $\square$

**Lemma 2 (no augmenting path means maximum).** If $G_f$ has no path from $s$ to $t$, let $S$ be the set of vertices reachable from $s$ in $G_f$. Then $(S, V \setminus S)$ is an s-t [cut](/cut/) with $|f| = c(S, V \setminus S)$, so $f$ is a maximum flow and the cut is a minimum cut.

*Proof.* $s \in S$ and $t \notin S$ by assumption. Take an edge $e = (u, v)$ with $u \in S$, $v \notin S$. If $f(e) < c(e)$, the forward edge $(u, v)$ is in $G_f$ and $v$ would be reachable, so $f(e) = c(e)$. Take an edge $e = (v, u)$ with $v \notin S$, $u \in S$. If $f(e) > 0$, the backward edge $(u, v)$ is in $G_f$, again a contradiction, so $f(e) = 0$. By [flow conservation](/flow-conservation/), $|f| = f(S, \bar S) - f(\bar S, S) = c(S, \bar S) - 0$. Every flow has value at most every [cut capacity](/cut-capacity/), so $f$ is maximum and the cut is minimum. $\square$

The converse of Lemma 2 follows from Lemma 1: if an augmenting path exists, $f$ is not maximum. So **a flow is maximum if and only if it has no augmenting path**. With Lemma 2, every network has a flow and a cut of equal value once some maximum flow exists; a maximum flow exists because the set of flows is a compact polytope and the value is linear. This is the max-flow min-cut theorem.

**Why backward edges matter.** Without backward edges, a greedy choice of paths can block the flow forever. The backward edge lets a later path undo flow that an earlier path sent the wrong way.

**Choice of the path.** Lemma 1 holds for any augmenting path, and the choice changes only the number of augmentations. Shortest paths give the [Edmonds-Karp algorithm](/edmonds-karp/), widest paths give the [fattest augmenting path](/fattest-augmenting-path/) rule, paths of bottleneck at least a threshold give [capacity scaling](/capacity-scaling/), and many shortest paths at once give the [blocking flows](/blocking-flow/) of [Dinic's algorithm](/dinic/).

## Examples

**A path that uses a backward edge.** The network has the edges $s a$, $s b$, $a b$, $a t$, $b t$, each of capacity 1. Start with $f = 0$ and augment along $s\,a\,b\,t$ with $\Delta = 1$. Now $f(s, a) = f(a, b) = f(b, t) = 1$. In $G_f$, the edges out of $s$ are only $(s, b)$; from $b$ the only residual edge is the backward edge $(b, a)$ of $a b$; from $a$ the edge $(a, t)$ is free. So the next augmenting path is $s\,b\,a\,t$ with bottleneck 1. It cancels the flow on $a b$. The result sends 1 along $s\,a\,t$ and 1 along $s\,b\,t$, value 2. Now $G_f$ has no edge out of $s$, so $S = \{s\}$ and the cut $\{s\}$ has capacity 2, matching the flow. A method that only follows forward edges would stop at value 1 after the first path.

**The running network.** Take $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10, and augment along shortest paths:

| step | augmenting path | bottleneck | value after |
|---|---|---|---|
| 1 | $s\,a\,b\,t$ | 4 | 4 |
| 2 | $s\,a\,d\,t$ | 6 | 10 |
| 3 | $s\,c\,d\,t$ | 4 | 14 |
| 4 | $s\,c\,d\,b\,t$ | 5 | 19 |

After step 4, the residual graph has the edges out of $s$ only to $c$ (residual 1), and from $c$ only back to $s$; the edge $c d$ is full, and $a c$ carries no flow so $c$ has no backward edge to $a$. So $S = \{s, c\}$ and the cut has capacity $10 + 9 = 19$, the value of the flow.

**Zero capacity and no path.** In the network $s \to a$ (5), $a \to t$ (0), the graph has a path from $s$ to $t$, but $G_0$ has no residual edge for $(a, t)$. So the zero flow has no augmenting path and is maximum, with $S = \{s, a\}$ of capacity 0. In $s \to a$ (5), $t \to a$ (5), there is no path at all, and the same holds.

**Antiparallel edges.** In $s \to a$ (3), $a \to b$ (2), $b \to a$ (1), $b \to t$ (2), the residual graph of $f = 0$ has the forward edges $(a, b)$ and $(b, a)$ of the two edges. After pushing 2 along $s\,a\,b\,t$, the edge $a b$ has a backward residual edge $(b, a)$ of capacity 2 and the edge $b a$ still has its own forward residual edge $(b, a)$ of capacity 1. They are two distinct residual edges with the same ends; an implementation that merges them into one entry must add their capacities, $2 + 1 = 3$.

**Real capacities.** With $c(s, a) = \sqrt 2$ and $c(a, t) = 1$, the path $s\,a\,t$ has bottleneck 1. After it, $(a, t)$ is full and $S = \{s, a\}$ has capacity 1.

## Where it is used

- The [Ford-Fulkerson method](/ford-fulkerson/) repeats augmentation until no augmenting path is left; Lemma 2 is its correctness proof.
- The [max-flow min-cut theorem](/max-flow-min-cut-theorem/) is proved by Lemma 2, and the [integrality theorem](/flow-integrality-theorem/) by Lemma 1 with integer bottlenecks.
- [Edmonds-Karp](/edmonds-karp/), the [fattest path](/fattest-augmenting-path/) rule and [capacity scaling](/capacity-scaling/) are rules for picking the path.
- [Dinic's algorithm](/dinic/) augments along many shortest paths in a [level graph](/level-graph/) at once.
- In matching, an [augmenting path](/augmenting-path/) alternates between unmatched and matched edges; it is the augmenting path of the flow network of a [bipartite matching](/bipartite-matching/) problem.
- [Successive shortest paths](/successive-shortest-path/) for [min-cost flow](/min-cost-flow-problem/) augment along paths of least cost in the residual graph.

## References
