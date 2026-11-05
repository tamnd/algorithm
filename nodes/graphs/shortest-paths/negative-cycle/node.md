---
tag: Z4CS42
kind: definition
slug: negative-cycle
name: Negative cycle
aliases:
- negative-weight cycle
area: graphs/shortest-paths
level: intro
summary: A directed cycle whose total weight is negative; it makes shortest paths through it undefined.
prereqs: [shortest-path, weighted-graph, simple-cycle, walk]
see_also: [negative-cycle-detection, bellman-ford, shortest-path, potential-function-reduced-costs, currency-arbitrage, karp-minimum-mean-cycle, shortest-path-optimality-conditions]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, introduction (negative-weight edges and cycles), and Section 22.1 (Bellman-Ford returns FALSE when a negative cycle is reachable)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 5, Shortest paths, label-correcting algorithms (optimality conditions and the detection of negative cycles)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths (the section on negative edges)
---

A negative cycle is a directed cycle in a [weighted graph](/weighted-graph/) whose edge weights add up to a number below zero. When a walk from $s$ to $t$ can reach such a cycle, it can go around it again and again, so the [shortest path](/shortest-path/) weight $\delta(s, t)$ is $-\infty$ and no shortest path exists. Algorithms that accept negative edges, such as [Bellman-Ford](/bellman-ford/), must therefore also [detect negative cycles](/negative-cycle-detection/). A graph has no negative cycle exactly when it has a potential that makes all weights nonnegative, which is the base of [Johnson's algorithm](/johnson/).

## Definition

Let $G = (V, E)$ be a directed graph with weights $w : E \to \mathbb{R}$. A *cycle* is a closed walk $C = \langle v_0, v_1, \ldots, v_k \rangle$ with $k \ge 1$, $v_k = v_0$ and $v_0, \ldots, v_{k-1}$ distinct. A self-loop is a cycle with $k = 1$. Its weight is $w(C) = \sum_{i=1}^{k} w(v_{i-1}, v_i)$.

$C$ is a *negative cycle* when $w(C) < 0$. A negative cycle is *reachable from* $s$ when some vertex of $C$ is reachable from $s$.

**Closed walks.** A closed walk of negative weight always contains a negative cycle. *Proof.* Take a closed walk $P$ with $w(P) < 0$ and the least number of edges. If $P$ repeats no vertex except its ends, it is a cycle. Otherwise some vertex $x$ occurs twice inside $P$, and $P$ splits at the two occurrences into two closed walks $P_1$ and $P_2$, each with fewer edges, and $w(P_1) + w(P_2) = w(P) < 0$. So one of them has negative weight, which contradicts the choice of $P$. $\square$ So "no negative cycle" and "no closed walk of negative weight" mean the same.

**The effect on distances.** For a source $s$ and a vertex $v$:

$$\delta(s, v) = -\infty \iff \text{some negative cycle } C \text{ has a vertex } x \text{ with } s \leadsto x \text{ and } x \leadsto v.$$

*Proof.* If such $C$ and $x$ exist, then for each $j \ge 0$ the walk "from $s$ to $x$, then $j$ times around $C$, then from $x$ to $v$" has weight $a + j \, w(C) + b$ for fixed $a$ and $b$, and this tends to $-\infty$. Conversely, if no walk from $s$ to $v$ meets a negative cycle, the [shortest path](/shortest-path/) page shows that $\delta(s, v)$ is the least weight of a simple path, which is finite or $+\infty$. $\square$

**Weight assumptions.** With nonnegative weights a negative cycle cannot exist. With integer weights a negative cycle has weight at most $-1$. Pages that say "no negative cycles" allow negative edges and assume $w(C) \ge 0$ for each cycle; a cycle of weight exactly 0 is allowed.

## Examples and non-examples

Take the graph of CLRS Figure 22.4 on $s, t, x, y, z$ with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7).

- **Non-example: negative edges, no negative cycle.** The graph has three negative arcs, but its eight simple cycles have weights 0, 1, 3, 3, 4, 18, 22 and 25. So every distance from $s$ is finite: $\delta(s, \cdot) = (0, 2, 4, 7, -2)$ for $(s, t, x, y, z)$.
- **Non-example: a zero cycle.** The cycle $s \to y \to x \to t \to z \to s$ has weight $7 - 3 - 2 - 4 + 2 = 0$. It is not negative. Going around it does not change a weight, and the distances stay finite.
- **Example.** Change the arc $x \to t$ to weight $-6$. The cycle $t \to x \to t$ now has weight $5 - 6 = -1$. Every vertex is reachable from $t$, so $\delta(s, v) = -\infty$ for all five vertices. Bellman-Ford finds an arc that can still be relaxed after $n - 1 = 4$ rounds and reports the cycle.
- **Example: a self-loop.** One arc $v \to v$ of weight $-1$ is a negative cycle of one edge. A code that skips self-loops when it builds the graph hides it.
- **Example: an unreachable negative cycle.** Add the vertices $a$ and $b$ with arcs $a \to b$ ($1$) and $b \to a$ ($-3$). The cycle has weight $-2$, but no arc enters it from $s$. The distances from $s$ do not change, and Bellman-Ford from $s$ does not report it. To find every negative cycle, add a new source with an arc of weight 0 to each vertex.
- **Example: arbitrage.** Exchange rates USD to EUR 0.9, EUR to GBP 0.8 and GBP to USD 1.4 multiply to $1.008 > 1$. With weights $-\ln r$, the cycle has weight $-\ln 0.9 - \ln 0.8 - \ln 1.4 \approx -0.00797 < 0$. A negative cycle here is a [currency arbitrage](/currency-arbitrage/).
- **Example: an undirected negative edge.** An undirected edge $\{u, v\}$ of weight $-1$, read as the two arcs $u \to v$ and $v \to u$, gives the negative cycle $u \to v \to u$ of weight $-2$.

## Related definitions

- [Shortest path](/shortest-path/): the distance $\delta$ is $-\infty$ exactly in the case above.
- [Negative cycle detection](/negative-cycle-detection/): the problem of deciding whether a negative cycle exists and finding one.
- [Potential function and reduced costs](/potential-function-reduced-costs/): a potential $h$ with $w(u, v) + h(u) - h(v) \ge 0$ on every arc exists if and only if there is no negative cycle.
- [Shortest-path optimality conditions](/shortest-path-optimality-conditions/): with a negative cycle, no finite labels satisfy the conditions on the cycle.
- [Minimum mean cycle](/minimum-mean-cycle-problem/): a negative cycle exists if and only if the least mean weight of a cycle is negative; [Karp's algorithm](/karp-minimum-mean-cycle/) computes it.
- [Simple cycle](/simple-cycle/): the undirected notion, which requires at least three vertices.

## References
