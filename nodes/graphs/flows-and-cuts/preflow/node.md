---
tag: FWV02C
kind: concept
slug: preflow
name: Preflow
aliases:
- preflow with excess
area: graphs/flows-and-cuts
level: advanced
summary: A flow relaxing conservation so each vertex may hold nonnegative excess.
prereqs: [s-t-flow, residual-graph, flow-conservation]
see_also: [push-relabel, mpm-algorithm, hao-orlin, distance-labeling, min-cut-problem, max-flow-min-cut-theorem, parametric-max-flow-problem]
sources:
  - paper: doi:10.1145/48014.61051
    title: Andrew V. Goldberg and Robert E. Tarjan, A new approach to the maximum-flow problem, Journal of the ACM 35(4), 921 to 940 (1988)
    locator: the sections on preflows, valid labelings and the generic algorithm (the lemmas that an active vertex can reach the source and that the labels stay below 2n)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 26.4, Push-relabel algorithms (preflows, height functions, and the lemmas on residual paths to the source)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 7, Maximum Flows, Polynomial Algorithms (preflow-push algorithms and distance labels)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 10, Maximum flow (the push-relabel method)
---

A preflow in a [flow network](/flow-network/) is an assignment of flow to edges that respects the capacities but relaxes [conservation](/flow-conservation/): every vertex other than the source may receive more than it sends, and the surplus is its *excess*. A preflow with no excess at any inner vertex is an [$s$-$t$ flow](/s-t-flow/). Preflows are the state of the [push-relabel](/push-relabel/) method and of the [MPM algorithm](/mpm-algorithm/): they let flow be moved one edge at a time, without first finding a whole augmenting path. With a valid labeling of the vertices, a preflow certifies a [minimum cut](/min-cut-problem/) even before it becomes a flow.

## In plain words

Imagine pouring water into a system of pipes from the source as fast as the first pipes allow. Water reaches the junctions faster than it can leave them, so it collects there in small tanks. That is a preflow: every pipe is within its limit, but junctions may hold water.

Methods that use preflows then work locally: a junction with water in its tank pushes some of it into a pipe that still has room, ideally one leading downhill toward the drain. Water that can never reach the drain is sent back to the source. When no junction holds water any more, what remains is an ordinary flow.

## The idea

**Setting.** $G = (V, E)$ is a directed graph with capacities $c : E \to \mathbb{R}_{\ge 0}$ (real; integer when a bound on the number of steps is wanted), a source $s$ and a sink $t \ne s$. Parallel and antiparallel edges are allowed; an antiparallel pair keeps two separate edges and two separate residual pairs. An edge of capacity 0 carries 0.

**Definition.** A preflow is a function $f : E \to \mathbb{R}$ with $0 \le f(e) \le c(e)$ for every edge and

$$e_f(v) = \sum_{e \in \delta^{\mathrm{in}}(v)} f(e) - \sum_{e \in \delta^{\mathrm{out}}(v)} f(e) \ge 0 \qquad \text{for every } v \ne s.$$

The number $e_f(v)$ is the excess of $v$. A vertex $v \notin \{s, t\}$ with $e_f(v) > 0$ is *active*. The [residual graph](/residual-graph/) $G_f$ is defined as for flows.

**Lemma 1 (no active vertex means a flow).** If no vertex is active, $f$ is an $s$-$t$ flow, of value $e_f(t)$.

*Proof.* Conservation holds at every $v \notin \{s, t\}$ because $e_f(v) = 0$. Summing $e_f$ over all vertices gives 0, since each edge adds $+f(e)$ at its head and $-f(e)$ at its tail; so $e_f(t) = -e_f(s)$, the net outflow of $s$. $\square$

**Lemma 2 (excess at the sink is bounded by every cut).** For every $s$-$t$ cut $S$, $e_f(t) \le c(S)$.

*Proof.* Let $T = V \setminus S$. Summing $e_f(v)$ over $v \in T$, edges inside $T$ cancel, and $\sum_{v \in T} e_f(v) = f(S, T) - f(T, S) \le c(S)$. Each term on the left is at least 0, and one of them is $e_f(t)$. $\square$

So the largest excess that a preflow can bring to $t$ is the maximum flow value; a maximum flow is a preflow that reaches it.

**Lemma 3 (excess can return to the source).** If $e_f(v) > 0$ and $v \ne s$, then $G_f$ has a path from $v$ to $s$.

*Proof.* Let $U$ be the set of vertices that $v$ reaches in $G_f$, and suppose $s \notin U$. No residual edge leaves $U$, so every edge from $U$ to $V \setminus U$ is full and every edge from $V \setminus U$ into $U$ is empty. Then $\sum_{u \in U} e_f(u) = f(V \setminus U, U) - f(U, V \setminus U) = -c(U, V \setminus U) \le 0$. But every term is at least 0 and $e_f(v) > 0$, a contradiction. $\square$

**Valid labelings.** A labeling $h : V \to \mathbb{Z}_{\ge 0}$ is *valid* for $f$ if $h(s) = n$, $h(t) = 0$, and $h(u) \le h(w) + 1$ for every residual edge $(u, w)$ of $G_f$.

**Lemma 4 (a valid labeling cuts $s$ from $t$).** If $f$ has a valid labeling, $G_f$ has no $s$-$t$ path. *Proof.* Along a residual path each edge lowers $h$ by at most 1. A simple $s$-$t$ path has at most $n - 1$ edges, so it can lower $h$ by at most $n - 1$, but $h(s) - h(t) = n$. $\square$

**Consequences.** If a preflow has a valid labeling and no active vertex, it is a maximum flow, by Lemmas 1 and 4 and the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). By Lemma 3 and validity, an active vertex $v$ has $h(v) \le h(s) + n - 1 = 2n - 1$, which bounds the labels in push-relabel. And if the vertices that can reach $t$ in $G_f$ form a set $R$ with $s \notin R$, then $S = V \setminus R$ is a cut whose edges out are all full and whose edges in are all empty, so $c(S) = f(S, R) - f(R, S) = \sum_{v \in R} e_f(v)$; if moreover only $t$ has excess in $R$, then $e_f(t) = c(S)$, and $S$ is a minimum cut before the excess is returned.

## Examples

**The initial preflow.** In the network $s \to a$ (3), $s \to b$ (2), $a \to b$ (1), $a \to t$ (2), $b \to t$ (3), saturate the edges out of $s$: $f(s, a) = 3$, $f(s, b) = 2$, and 0 elsewhere. Then $e_f(a) = 3$ and $e_f(b) = 2$, both active, and $e_f(t) = 0$. The labeling $h(s) = 4$, $h(a) = h(b) = h(t) = 0$ is valid: the residual edges out of $s$ are gone, and every other residual edge goes between vertices of label 0.

| step | action | $e_f(a)$ | $e_f(b)$ | $e_f(t)$ |
|---|---|---|---|---|
| 0 | saturate the edges out of $s$ | 3 | 2 | 0 |
| 1 | relabel $a$ to 1, push 2 along $a \to t$ | 1 | 2 | 2 |
| 2 | push 1 along $a \to b$ | 0 | 3 | 2 |
| 3 | relabel $b$ to 1, push 3 along $b \to t$ | 0 | 0 | 5 |

After step 3 no vertex is active, and $f$ is a maximum flow of value 5.

**Excess that cannot reach the sink.** With $s \to a$ (5) and $a \to t$ (2), the initial preflow gives $e_f(a) = 5$; after pushing 2 to $t$, $a$ keeps 3 and $G_f$ has no path from $a$ to $t$. The set of vertices that reach $t$ is $\{t\}$, so $S = \{s, a\}$ is a minimum cut of capacity 2 = $e_f(t)$, already known. The remaining 3 units go back along the backward edge $a \to s$, as Lemma 3 promises.

**Zero capacity and no path.** An edge of capacity 0 carries 0 in every preflow and has no forward residual edge. If $t$ is not reachable from $s$, every preflow has $e_f(t) = 0$ by Lemma 2 with $S$ the set reachable from $s$, and all excess returns to $s$.

## Where it is used

- **[Push-relabel](/push-relabel/)** keeps a preflow and a valid labeling; pushes and relabels preserve both, and the method stops when no vertex is active.
- **The [MPM algorithm](/mpm-algorithm/)** and Karzanov's blocking flow method push preflows through a level graph.
- **Minimum cuts without a full flow.** The first phase of push-relabel stops when no active vertex can reach $t$; the cut is then known, which saves the time of returning the excess. The [Hao-Orlin algorithm](/hao-orlin/) uses this to find all $n - 1$ cuts of a global minimum cut search in one run.
- **[Parametric maximum flow](/parametric-max-flow-problem/).** Gallo, Grigoriadis and Tarjan keep a preflow while capacities change monotonically.
- **Pseudoflows.** Hochbaum's pseudoflow algorithm drops even the sign condition on the excess.

## References
