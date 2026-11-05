---
tag: D20SDM
kind: definition
slug: s-t-flow
name: s-t flow
area: graphs/flows-and-cuts
level: intro
summary: An assignment of nonnegative values to the edges of a network that respects capacities and conserves flow at every vertex except source and sink.
prereqs: [flow-network, directed-graph]
see_also: [flow-conservation, max-flow-problem, residual-graph, cut-capacity, flow-decomposition, circulation-problem, preflow]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.1, Flow networks (the capacity constraint, flow conservation, the value of a flow, and the reduction of antiparallel edges)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.1, The Maximum-Flow Problem and the Ford-Fulkerson Algorithm (the definition of an s-t flow and its value)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 6, Maximum Flows, Basic Ideas (the flow formulation with mass balance constraints)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (flows, the value of a flow, and the cut lemma)
---

An $s$-$t$ flow in a [flow network](/flow-network/) is a value on each edge that never exceeds the edge's capacity and that obeys [flow conservation](/flow-conservation/) at every vertex other than the source $s$ and the sink $t$. Its value is the net amount that leaves $s$. The object is the feasible solution of the [maximum flow problem](/max-flow-problem/), and the [residual graph](/residual-graph/), [augmenting paths](/augmenting-path-flow/) and [cuts](/cut-capacity/) are all defined in terms of it.

## Definition

A *flow network* is a tuple $N = (G, c, s, t)$. Here $G = (V, E)$ is a finite [directed graph](/directed-graph/), $c : E \to \mathbb{R}_{\ge 0}$ gives each edge a capacity, and $s, t \in V$ with $s \ne t$. On this page:

- **Capacities are real.** Every statement holds for real capacities. When all capacities are integers, the network is called *integral*; this matters for the [integrality theorem](/integrality-theorem/), not for the definition.
- **The graph is directed.** An undirected edge $\{u, v\}$ of capacity $k$ is modeled by the two edges $(u, v)$ and $(v, u)$, each of capacity $k$.
- **Parallel and antiparallel edges are allowed.** The flow is a function on edges, not on pairs of vertices, so the two edges $(u, v)$ and $(v, u)$ carry two separate values. Some books (CLRS) forbid antiparallel edges and remove one of them by putting a new vertex in its middle; this gives an equivalent network.
- **Edges of capacity 0 are allowed.** They carry no flow.

For a function $f : E \to \mathbb{R}$ and a vertex $v$, write

$$f^{\mathrm{in}}(v) = \sum_{e = (u, v) \in E} f(e), \qquad f^{\mathrm{out}}(v) = \sum_{e = (v, w) \in E} f(e).$$

The function $f$ is an **$s$-$t$ flow** when it meets both of these conditions:

1. **Capacity constraint.** $0 \le f(e) \le c(e)$ for each $e \in E$.
2. **Conservation.** $f^{\mathrm{in}}(v) = f^{\mathrm{out}}(v)$ for each $v \in V \setminus \{s, t\}$.

The **value** of $f$ is $|f| = f^{\mathrm{out}}(s) - f^{\mathrm{in}}(s)$. A self-loop $(v, v)$ adds the same amount to $f^{\mathrm{in}}(v)$ and $f^{\mathrm{out}}(v)$, so it never changes conservation or the value; algorithms can drop loops.

**Lemma 1 (the value is also measured at the sink).** For each $s$-$t$ flow $f$, $|f| = f^{\mathrm{in}}(t) - f^{\mathrm{out}}(t)$.

*Proof.* Each edge $(u, w)$ adds $f(u, w)$ once to $f^{\mathrm{out}}(u)$ and once to $f^{\mathrm{in}}(w)$. So $\sum_{v \in V} \bigl(f^{\mathrm{out}}(v) - f^{\mathrm{in}}(v)\bigr) = 0$. By conservation, each term with $v \notin \{s, t\}$ is 0. What is left is $\bigl(f^{\mathrm{out}}(s) - f^{\mathrm{in}}(s)\bigr) + \bigl(f^{\mathrm{out}}(t) - f^{\mathrm{in}}(t)\bigr) = 0$. $\square$

**Lemma 2 (the flow across a cut).** Let $S \subseteq V$ with $s \in S$ and $t \notin S$, and $T = V \setminus S$. Then

$$|f| = \sum_{(u, w) \in E,\ u \in S,\ w \in T} f(u, w) \; - \sum_{(u, w) \in E,\ u \in T,\ w \in S} f(u, w).$$

*Proof.* Sum $f^{\mathrm{out}}(v) - f^{\mathrm{in}}(v)$ over $v \in S$. By conservation and $t \notin S$, the sum is $|f|$. An edge with both ends in $S$ adds $+f(e)$ at its tail and $-f(e)$ at its head, so it cancels. An edge from $S$ to $T$ adds $+f(e)$ once, and an edge from $T$ to $S$ adds $-f(e)$ once. $\square$

Lemma 2 with the capacity constraint gives $|f| \le \sum_{u \in S, w \in T} c(u, w)$, the [capacity of the cut](/cut-capacity/). This is the easy half of the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).

## Examples and non-examples

The examples use the network with vertices $s, a, b, t$ and the edges $s \to a$ (3), $s \to b$ (2), $a \to b$ (1), $a \to t$ (2), $b \to t$ (3), where the number is the capacity.

| $f(s,a)$ | $f(s,b)$ | $f(a,b)$ | $f(a,t)$ | $f(b,t)$ | is it an $s$-$t$ flow? | value |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | yes, the zero flow | 0 |
| 2 | 0 | 0 | 2 | 0 | yes | 2 |
| 3 | 2 | 1 | 2 | 3 | yes, and it is maximum | 5 |
| 3 | 2 | 0 | 2 | 2 | no: at $a$, 3 enters and 2 leaves | |
| 3 | 2 | 0 | 3 | 2 | no: $f(a, t) = 3 > 2$, though conservation holds | |
| 2 | 1 | $-1$ | 3 | 0 | no: $f(a, b) < 0$, and $f(a, t) > 2$ | |

The third row is maximum because the cut $S = \{s\}$ has capacity $3 + 2 = 5$, so by Lemma 2 no flow has a larger value. The value at the sink is $2 + 3 = 5$ as well, as Lemma 1 says.

- **A cycle of flow.** Add the edges $a \to c$ (4) and $c \to a$ (4) with a new vertex $c$. Put 4 units on both, and 0 on the other edges. This is an $s$-$t$ flow of value 0: it is a circulation that does not touch $s$ or $t$.
- **Antiparallel edges.** In the same network with $c$, putting 4 on $a \to c$ and 1 on $c \to a$ breaks conservation at $c$ (4 in, 1 out). The two edges carry separate values; they do not cancel each other.
- **A negative value.** In the network with the edges $t \to a$ (1) and $a \to s$ (1), the flow with 1 unit on both edges is an $s$-$t$ flow of value $0 - 1 = -1$. The definition allows it. A maximum flow never needs it: the zero flow is better.
- **A zero-capacity edge.** If $c(a, t) = 0$, the capacity constraint forces $f(a, t) = 0$, and the largest value drops from 5 to 3. The cut $S = \{s, a\}$ now has capacity $c(s, b) + c(a, b) + c(a, t) = 2 + 1 + 0 = 3$, and the flow with $f(s, a) = 1$, $f(s, b) = 2$, $f(a, b) = 1$, $f(b, t) = 3$ reaches it. The edge is still part of the graph, but it is never used.
- **No $s$-$t$ path.** If $t$ has no entering edge of positive capacity, take $S = V \setminus \{t\}$ in Lemma 2. The only edges from $S$ to $T$ have capacity 0, so each $s$-$t$ flow has value at most 0.

## Related definitions

- **Flow conservation.** Condition 2, studied on its own: [flow conservation](/flow-conservation/).
- **Net flow (skew-symmetric) form.** Some texts define $f : V \times V \to \mathbb{R}$ with $f(u, v) = -f(v, u)$. That form merges the two edges of an antiparallel pair into one number. It gives the same maximum values, but the per-edge form on this page keeps the two edges apart.
- **Circulation.** A flow with conservation at every vertex, $s$ and $t$ included, often with lower bounds on the edges: the [circulation problem](/circulation-problem/).
- **Preflow.** A relaxation that allows more flow to enter a vertex than leaves it: [preflow](/preflow/).
- **Residual graph.** The edges along which a flow can still change: [residual graph](/residual-graph/).
- **Cut and its capacity.** The upper bound of Lemma 2: [cut](/cut/) and [cut capacity](/cut-capacity/).
- **Integral flow.** A flow with $f(e) \in \mathbb{Z}$ for each edge; see the [integrality theorem](/integrality-theorem/).
- **Decomposition.** Each $s$-$t$ flow of nonnegative value is a sum of path flows and cycle flows: [flow decomposition](/flow-decomposition/).

## References
