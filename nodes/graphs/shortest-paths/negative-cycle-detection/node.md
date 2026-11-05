---
tag: HZW2DP
kind: problem
slug: negative-cycle-detection
name: Negative cycle detection
aliases:
- detecting negative cycles
area: graphs/shortest-paths
level: intro
summary: Decide whether a directed graph contains a negative-weight cycle, and find one if so.
prereqs: [negative-cycle, bellman-ford, edge-relaxation]
see_also: [negative-cycle, bellman-ford, spfa, tarjan-subtree-disassembly, karp-minimum-mean-cycle, currency-arbitrage-detection, johnson, potential-function-reduced-costs]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.1, The Bellman-Ford algorithm (the final check of all edges), and Section 22.5 (the predecessor-subgraph property and the exercises on finding the cycle)
  - paper: doi:10.1007/s101070050058
    title: Boris V. Cherkassky and Andrew V. Goldberg, Negative-cycle detection algorithms, Mathematical Programming 85(2), 277 to 311 (1999)
    locator: Sections 2 to 4 (the cycle detection strategies, including walk to the root and subtree disassembly)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 5, Section 5.5, Detecting negative cycles
  - paper: doi:10.1016/0012-365X(78)90011-0
    title: Richard M. Karp, A characterization of the minimum cycle mean in a digraph, Discrete Mathematics 23(3), 309 to 311 (1978)
    locator: the theorem and the O(nm) algorithm
  - url: "https://arxiv.org/abs/2203.03456"
    locator: Aaron Bernstein, Danupon Nanongkai and Christian Wulff-Nilsen, Negative-Weight Single-Source Shortest Paths in Near-linear Time, FOCS 2022 (the main theorem, which also reports a negative cycle)
---

Negative cycle detection is the problem of deciding whether a directed graph with real or integer edge weights has a [negative cycle](/negative-cycle/), and of returning one when it does. It is the part of the [single-source shortest paths](/single-source-shortest-paths/) problem that makes negative edges hard: when no negative cycle exists, the distances are finite and [Bellman-Ford](/bellman-ford/) computes them, and when one exists, some distances are $-\infty$. Bellman-Ford with one extra pass solves it in $O(nm)$ time. For integer weights it is solvable in near-linear time.

## In plain words

Each road in a network has a cost, and some costs are negative, as a refund or a gain. A loop of roads whose costs add up to less than zero is a problem: if you drive around it, you gain each time, so there is no cheapest route. The task is to find out if such a loop exists, and to show one.

The classic method keeps a best-known cost for each place, starting at zero. It goes over all roads and lowers a cost when a road gives a cheaper way in. Without a bad loop, the costs stop changing after a number of passes equal to the number of places. If something still gets cheaper after that, a bad loop exists, and following the record of who lowered whom leads back into it.

## Definition

**Input.** A directed graph $G = (V, E)$ with $n = |V|$, $m = |E|$, and weights $w : E \to \mathbb{R}$. Edges may be negative. Self-loops are allowed.

**Output.** Either the answer "no negative cycle", which means $\sum_{i=1}^{k} w(v_{i-1}, v_i) \ge 0$ for every directed cycle $\langle v_0, \ldots, v_k = v_0 \rangle$, or a cycle $C$ with $w(C) < 0$.

A certificate for the answer "no" is a [potential](/potential-function-reduced-costs/) $h : V \to \mathbb{R}$ with $w(u, v) + h(u) - h(v) \ge 0$ for each $(u, v) \in E$. It proves the answer: the sum over a cycle of these reduced weights is $w(C)$, because the terms $h$ cancel, so $w(C) \ge 0$. A certificate for "yes" is the cycle itself. One of the two always exists; the extra-source construction below shows it.

## Variants

- **Reachable from a source.** Decide whether a negative cycle is reachable from a given vertex $s$. This is what Bellman-Ford from $s$ answers, and it is the question that matters for distances from $s$.
- **Whole graph.** Decide for the whole graph. Add a new vertex $q$ and arcs $q \to v$ of weight 0 for each $v$, and ask the first variant from $q$. Equivalently, start all labels at 0 instead of $\infty$.
- **Integer weights.** $w(e) \in \mathbb{Z}$ and $w(e) \ge -W$. Scaling algorithms use $W$.
- **Minimum mean cycle.** Find a cycle $C$ that minimizes $w(C) / |C|$. A negative cycle exists if and only if this minimum is negative.
- **Arbitrage.** Rates $r(u, v) > 0$, and the question is whether some cycle has $\prod r > 1$. With $w = -\ln r$ this is negative cycle detection; see [currency arbitrage detection](/currency-arbitrage-detection/).

## Examples

All examples use the graph of CLRS Figure 22.4 on $s, t, x, y, z$ with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7). All labels start at 0, which is the whole-graph variant, and each pass relaxes the arcs in this order.

| graph | passes until no change | answer | certificate |
|---|---|---|---|
| as given | 4 (the fourth makes no change) | no negative cycle | $h = (-7, -5, -3, 0, -9)$ on $(s, t, x, y, z)$ |
| $x \to t$ set to $-6$ | the fifth pass still changes a label | negative cycle | $z \to x \to t \to z$, weight $7 - 6 - 4 = -3$ |
| as given, plus $a \to b$ (1) and $b \to a$ ($-3$) | the seventh pass still changes a label | negative cycle | $a \to b \to a$, weight $-2$ |

In the second row, $t \to x \to t$ (weight $-1$) is also negative; the parent walk returns the first cycle that it meets, which is a different one. In the third row, Bellman-Ford from $s$ alone answers "no", because nothing enters $\{a, b\}$ from $s$: the distances from $s$ stay $(0, 2, 4, 7, -2)$ and $\delta(s, a) = \delta(s, b) = +\infty$.

**Finding the cycle.** When pass $n$ still lowers the label of a vertex $v$, set $v \leftarrow \mathrm{parent}(v)$ $n$ times. The vertex reached lies on a cycle of the parent pointers. Follow the parents from it until it repeats: the vertices met, in reverse order, form a negative cycle. The proof uses the fact that each cycle of the parent graph has negative weight (CLRS Section 22.5, in the proof of the predecessor-subgraph property).

## Known algorithms

- [Bellman-Ford](/bellman-ford/) with one more pass: $O(nm)$ time in the worst case, real weights.
- [SPFA](/spfa/), the queue-based Bellman-Ford, with a count of the edges on the current path of each vertex: $O(nm)$ in the worst case.
- [Tarjan's subtree disassembly](/tarjan-subtree-disassembly/): Bellman-Ford that finds a cycle as soon as the parent graph gets one; $O(nm)$ in the worst case and among the fastest in the experiments of Cherkassky and Goldberg.
- [Floyd-Warshall](/floyd-warshall/): $O(n^3)$; a negative cycle exists if and only if some diagonal entry becomes negative.
- [Karp's minimum mean cycle](/karp-minimum-mean-cycle/): $O(nm)$; gives the least mean, so it also decides the question.
- [Goldberg's scaling algorithm](/goldberg-scaling-sssp/): $O(\sqrt{n}\, m \log W)$ for integer weights at least $-W$.
- [Near-linear negative-weight SSSP](/near-linear-negative-sssp/) (Bernstein, Nanongkai and Wulff-Nilsen 2022): $O(m \log^8 n \log W)$ expected time for integer weights, and it returns a negative cycle when one exists.

## Bounds

**Upper bounds.** For real weights, $O(nm)$ by Bellman-Ford stood from the 1950s. Fineman (STOC 2024) gave the first strongly polynomial improvement, a randomized algorithm in $\tilde O(m n^{8/9})$ time, and later work lowered the exponent further. For integer weights at least $-W$, the bound is $O(m \log^8 n \log W)$ expected (Bernstein, Nanongkai and Wulff-Nilsen), with later improvements of the logarithmic factors.

**Lower bound.** Each algorithm must read every edge in the worst case: if it never reads the weight of some arc $e$, that weight can be set to a very negative number that makes a cycle through $e$ negative, or left large. So $\Omega(n + m)$ time is needed in any model where reading a weight is a step. No better lower bound is known for general algorithms.

**Certificates.** The output can be checked in $O(n + m)$ time: sum the weights of the cycle, or check $w(u, v) + h(u) - h(v) \ge 0$ on every arc.

## Reductions

- **To single-source shortest paths.** Add the vertex $q$ and arcs $q \to v$ of weight 0, and run any SSSP algorithm that reports negative cycles, from $q$. This costs $O(n)$ extra edges.
- **From single-source shortest paths.** Conversely, once there is no negative cycle, the distances from $q$ are a potential $h$. With it, the reduced weights are nonnegative, and [Dijkstra's algorithm](/dijkstra/) gives the distances from any source. This is the idea of [Johnson's algorithm](/johnson/).
- **Arbitrage.** A cycle of exchange rates with product above 1 is a negative cycle under $w = -\ln r$, as in [currency arbitrage](/currency-arbitrage/).
- **Feasibility of difference constraints.** A system $x_v - x_u \le w(u, v)$ is feasible if and only if its constraint graph has no negative cycle; see [difference constraints](/difference-constraints/).

## Applications

- Checking that a system of [difference constraints](/difference-constraints/) from scheduling or timing analysis is feasible.
- Finding arbitrage in currency markets.
- [Cycle canceling](/cycle-canceling/) for [minimum-cost flow](/min-cost-flow-problem/): a flow is optimal if and only if its residual graph has no negative cycle.
- Checking that a set of computed distances is valid before a program uses it.

## References
