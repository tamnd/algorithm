---
tag: SA7T00
kind: definition
slug: cut-capacity
name: Cut capacity
aliases:
- capacity of a cut
area: graphs/flows-and-cuts
level: intro
summary: The sum of capacities of edges going from the source side to the sink side of a cut.
prereqs: [cut, flow-network]
see_also: [flow-conservation, s-t-flow, min-cut-problem, max-flow-min-cut-theorem, global-min-cut-problem, submodular-function]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.2, The Ford-Fulkerson method (cuts of flow networks, the capacity of a cut, and the bound of a flow value by a cut capacity)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.2, Maximum Flows and Minimum Cuts in a Network
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts (cuts, their capacity and the easy half of the maxflow-mincut theorem)
---

The capacity of an s-t [cut](/cut/) $(S, \bar S)$ in a [flow network](/flow-network/) is the sum of the capacities of the edges that go from the source side $S$ to the sink side $\bar S$. Edges that go the other way do not count. Every [s-t flow](/s-t-flow/) has value at most the capacity of every s-t cut, and the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) says that the largest flow value equals the smallest cut capacity.

## Definition

Let $N = (G, c, s, t)$ be a flow network with $G = (V, E)$ and $c : E \to \mathbb{R}_{\ge 0}$, and let $(S, \bar S)$ be an s-t cut, so $s \in S$ and $t \in \bar S = V \setminus S$. The **capacity** of the cut is

$$c(S, \bar S) = \sum_{(u, v) \in E,\ u \in S,\ v \in \bar S} c(u, v) = \sum_{e \in \delta^{+}(S)} c(e).$$

A **minimum s-t cut** is an s-t cut whose capacity is least among all $2^{n-2}$ s-t cuts. It always exists, since the set of s-t cuts is finite and nonempty.

**Directed graphs.** Only the edges in $\delta^+(S)$ count. An edge $(v, u)$ with $v \in \bar S$ and $u \in S$ adds nothing, whatever its capacity. So $c(S, \bar S) \ne c(\bar S, S)$ in general.

**Undirected graphs.** An undirected edge of capacity $c$ is two directed edges of capacity $c$, so exactly one of them leaves $S$ when the edge crosses the cut. The capacity is then $\sum_{e \in \delta(S)} c(e)$, and it is symmetric: $c(S, \bar S) = c(\bar S, S)$.

**Integer or real capacities.** The definition works for any nonnegative real capacities. With integer capacities each cut capacity is an integer, which is why the minimum cut value, and so the maximum flow value, is then an integer.

**Antiparallel and parallel edges.** Each edge counts on its own. If $(u, v)$ and $(v, u)$ both exist with $u \in S$, $v \in \bar S$, only $c(u, v)$ counts. Parallel edges $(u, v)$ add up.

**The weak duality bound.** Let $f$ be an s-t flow. By [flow conservation](/flow-conservation/), $|f| = f(S, \bar S) - f(\bar S, S)$, where $f(X, Y)$ is the total flow on edges from $X$ to $Y$. Since $f(\bar S, S) \ge 0$ and $f(e) \le c(e)$ on each edge,

$$|f| \le f(S, \bar S) \le c(S, \bar S).$$

Equality holds exactly when every edge of $\delta^+(S)$ is saturated ($f(e) = c(e)$) and every edge of $\delta^-(S)$ is empty ($f(e) = 0$). When equality holds, $f$ is a maximum flow and $(S, \bar S)$ is a minimum cut, because no flow can exceed this cut and no cut can be below this flow.

**Submodularity.** The function $\kappa(S) = c(S, \bar S)$ on the subsets of $V$ is [submodular](/submodular-function/): for all $X, Y \subseteq V$,

$$\kappa(X) + \kappa(Y) \ge \kappa(X \cap Y) + \kappa(X \cup Y).$$

*Proof.* Each edge $(u, v)$ adds $c(u, v) \ge 0$ to a term exactly when its tail is in the set and its head is not. Check each edge by where its ends lie. If $u \in X \cap Y$ and $v \notin X \cup Y$, the edge counts in all four terms. If $u \in X \cap Y$ and $v$ is in exactly one of $X$, $Y$, it counts once on the left (in the term whose set does not hold $v$) and once on the right (in $\kappa(X \cap Y)$). If $u$ is in exactly one set, say $X$, and $v \notin X \cup Y$, it counts once on the left ($\kappa(X)$) and once on the right ($\kappa(X \cup Y)$). If $u \in X \setminus Y$ and $v \in Y \setminus X$, it counts once on the left ($\kappa(X)$) and not on the right. In all other placements it counts in no term on the right. So each edge adds at least as much to the left side as to the right side. $\square$

A consequence: if $X$ and $Y$ are both minimum s-t cuts, then $X \cap Y$ and $X \cup Y$ are s-t cuts with $\kappa(X \cap Y) + \kappa(X \cup Y) \le 2\lambda$, where $\lambda$ is the minimum, so both are minimum cuts too. The minimum s-t cuts are closed under union and intersection, and there is a unique minimum cut with the smallest source side and a unique one with the largest.

## Examples and non-examples

The network is the running example: $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10. Its 16 s-t cuts have these capacities, by source side minus $s$:

| $S \setminus \{s\}$ | capacity | $S \setminus \{s\}$ | capacity |
|---|---|---|---|
| none | 20 | $\{b, c\}$ | 29 |
| $\{a\}$ | 24 | $\{b, d\}$ | 40 |
| $\{b\}$ | 30 | $\{c, d\}$ | 26 |
| $\{c\}$ | 19 | $\{a, b, c\}$ | 27 |
| $\{d\}$ | 36 | $\{a, b, d\}$ | 32 |
| $\{a, b\}$ | 30 | $\{a, c, d\}$ | 20 |
| $\{a, c\}$ | 21 | $\{b, c, d\}$ | 30 |
| $\{a, d\}$ | 32 | $\{a, b, c, d\}$ | 20 |

The minimum is 19, reached only by $S = \{s, c\}$. The edge $a c$ points from $\bar S$ into $S$ there and does not count. If it were counted, the cut would cost 21 and the bound would fail to be tight; the [maximum flow](/max-flow-problem/) has value 19.

**A zero-capacity edge.** Adding $(s, t)$ with capacity 0 adds 0 to every cut, so no cut capacity changes.

**No path from $s$ to $t$.** In $s \to a$ (5), $t \to a$ (5), the cut $S = \{s, a\}$ has capacity 0 and the cut $S = \{s\}$ has capacity 5. The minimum is 0, and so the maximum flow value is 0.

**Antiparallel edges.** In $s \to a$ (3), $a \to b$ (2), $b \to a$ (1), $b \to t$ (2), $s \to b$ (1), the cut $S = \{s, a\}$ has capacity $c(a, b) + c(s, b) = 2 + 1 = 3$; the edge $b \to a$ enters $S$ and adds nothing. The cut $S = \{s, a, b\}$ has capacity 2, the minimum.

**Real capacities.** With $c(s, a) = \sqrt 2$ and $c(a, t) = 1$, the cuts $\{s\}$ and $\{s, a\}$ have capacities $\sqrt 2$ and 1, so the minimum is 1.

**Non-example: the number of crossing edges.** The capacity is a weighted sum, not a count. In the running network, $S = \{s\}$ has 2 leaving edges and capacity 20, while $S = \{s, c\}$ also has 2 leaving edges and capacity 19. With all capacities 1 the two notions agree, which is the setting of [edge-disjoint paths](/edge-disjoint-paths/).

**Non-example: the net capacity.** The quantity $\sum_{\delta^+(S)} c - \sum_{\delta^-(S)} c$ is not the cut capacity. For $S = \{s, c\}$ it is $19 - 2 = 17$, which is below the maximum flow value 19 and is not an upper bound on flows.

## Related definitions

- A [cut](/cut/) and its cut set $\delta^+(S)$ are defined on their own page.
- [Flow conservation](/flow-conservation/) gives the identity $|f| = f(S, \bar S) - f(\bar S, S)$ that the bound uses.
- The [minimum s-t cut problem](/min-cut-problem/) asks for the least capacity, and the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) equates it with the maximum flow value.
- The [global minimum cut problem](/global-min-cut-problem/) minimizes the capacity over all cuts with no fixed $s$ and $t$.
- The capacity function is a standard example of a [submodular function](/submodular-function/).

## References
