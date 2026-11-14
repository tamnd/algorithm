---
tag: TZQ375
kind: problem
slug: scan-chain-ordering
name: Scan chain ordering
aliases:
- scan chain reordering
- scan stitching
area: eda/test-and-diagnosis
level: advanced
summary: Order the flip-flops of each scan chain after placement so that the scan wiring is shortest, a travelling salesman problem with ends and hold constraints.
prereqs: [scan-design, traveling-salesman-problem]
see_also: [hamiltonian-path-problem, asymmetric-tsp, vehicle-routing-problem, setup-and-hold-constraints, clock-tree-synthesis, placement-problem, half-perimeter-wirelength, np-hard]
sources:
  - paper: doi:10.1109/TEST.1998.743172
    title: Samy Makar, A layout-based approach for ordering scan chain flip-flops, Proceedings of the International Test Conference, 341 to 347, 1998
    locator: the ordering of scan flip-flops from their placed positions as a traveling salesman path, with heuristics and the constraints of clock domains
  - paper: "M. Hirech, J. Beausang and X. Gu, A new approach to scan chain reordering using physical design information, Proceedings of the International Test Conference, 348 to 355, 1998"
    title: M. Hirech, J. Beausang and X. Gu, A new approach to scan chain reordering using physical design information, Proceedings of the International Test Conference, 348 to 355, 1998
    locator: reordering scan chains after placement, with the scan-in and scan-out pins as fixed ends
  - paper: "A. Itai, C. H. Papadimitriou and J. L. Szwarcfiter, Hamilton paths in grid graphs, SIAM Journal on Computing 11(4), 676 to 686, 1982"
    title: A. Itai, C. H. Papadimitriou and J. L. Szwarcfiter, Hamilton paths in grid graphs, SIAM Journal on Computing 11(4), 676 to 686, 1982
    locator: the NP-completeness of the Hamilton circuit problem for grid graphs
  - book: isbn:9780123705976
    title: Laung-Terng Wang, Cheng-Wen Wu and Xiaoqing Wen, VLSI Test Principles and Architectures, Morgan Kaufmann, 2006
    locator: the chapter on design for testability (scan chain stitching and reordering after placement)
---

Scan chain ordering chooses, after placement, the order in which the flip-flops of a [scan design](/scan-design/) are linked into chains. For test, any order works: the tester shifts the patterns through whatever order is chosen. For the layout, the order fixes the scan wires, one from the scan-in pin to the first flip-flop, one from each flip-flop to the next, and one from the last to the scan-out pin. Making their total length least is a shortest Hamiltonian path between two fixed ends, so the problem is a form of the [traveling salesman problem](/traveling-salesman-problem/) and is [NP-hard](/np-hard/) even with Manhattan distances on a grid. Real instances add constraints: chains of equal length, flip-flops of one clock domain together, and no hold-time violation on any scan wire.

## In plain words

After the chip is laid out, every storage cell that is part of a test chain sits at a fixed spot. The test chain must visit every cell once, start at the input pin and end at the output pin. The order does not matter for testing, so we pick the order whose wires are shortest. This is like a delivery route that must start at one depot, end at another and visit every customer once, with the customers being the cells. Finding the very best route is hard when there are many cells, so tools use good routes found quickly.

## Definition

**Input.** Points $s$ (the scan-in pin), $e$ (the scan-out pin) and $x_1, \ldots, x_n$ (the placed scan flip-flops), and a distance $d(p, q) \ge 0$ for the wire from $p$ to $q$. On a chip $d$ is usually the Manhattan distance $|p_x - q_x| + |p_y - q_y|$, which is a lower bound on a routed two-pin wire.

**Output.** A permutation $\pi$ of $\{1, \ldots, n\}$, the order of the chain.

**Goal.** Minimize the wire length
$$W(\pi) = d(s, x_{\pi(1)}) + \sum_{i=1}^{n-1} d(x_{\pi(i)}, x_{\pi(i+1)}) + d(x_{\pi(n)}, e).$$

**This is a shortest Hamiltonian path with fixed ends.** Let $G$ be the complete graph on $\{s, e, x_1, \ldots, x_n\}$ with edge weights $d$. A permutation $\pi$ is the same thing as a Hamiltonian path of $G$ from $s$ to $e$, namely $s, x_{\pi(1)}, \ldots, x_{\pi(n)}, e$, since such a path visits each $x_i$ exactly once between its fixed ends, and $W(\pi)$ is the weight of that path. So the orders of least wire length are exactly the shortest Hamiltonian $s$-$e$ paths of $G$.

**And a traveling salesman tour.** Merge $s$ and $e$ into one depot $o$ with the costs $c(o, x_i) = d(s, x_i)$ for leaving and $c(x_i, o) = d(x_i, e)$ for returning, and $c(x_i, x_j) = d(x_i, x_j)$. A tour $o, x_{\pi(1)}, \ldots, x_{\pi(n)}, o$ costs exactly $W(\pi)$, and every tour has this form after rotating it to start at $o$. So the problem is an [asymmetric TSP](/asymmetric-tsp/) on $n + 1$ cities. A symmetric form keeps $s$ and $e$ apart and sets the weight of the edge $s$-$e$ to $-M$ for a large $M$, so that every optimal tour uses that edge, and removing it leaves the path.

## Variants

- **Several chains.** With $c$ chains, each with its own pins, the flip-flops must also be split into $c$ groups. Test time grows with the longest chain, so the groups must have equal size, within one. This is close to the [vehicle routing problem](/vehicle-routing-problem/) with equal loads.
- **Clock domains and edges.** Flip-flops on different clocks, or on rising and falling edges of one clock, should be kept in separate chains or separate segments, with a lockup latch at each crossing. The order is then a path inside each group, plus an order of the groups.
- **Hold constraints.** A scan wire has no logic, so a short wire between two flip-flops whose clocks arrive with skew can violate the [hold constraint](/setup-and-hold-constraints/). Some pairs must not be neighbors, or need a delay buffer, which turns some edge weights into infinite or penalized ones.
- **Reordering with partial freedom.** Some flip-flops must keep a fixed order, for example those of a shift register already wired in the logic, which are treated as one city with an entry and an exit point.
- **Routing congestion.** The scan wires compete with the functional wires for routing tracks, so the cost may weight wires through crowded regions more.

## Examples

Take the pins $s = (0, 0)$ and $e = (10, 0)$ and five flip-flops $A = (2, 3)$, $B = (8, 1)$, $C = (5, 4)$, $D = (3, 0)$ and $E = (7, 5)$, with Manhattan distance.

| order | wire lengths | total |
|---|---|---|
| $A, B, C, D, E$ (the netlist order) | 5 + 8 + 6 + 6 + 9 + 8 | 42 |
| $D, A, C, E, B$ (the best) | 3 + 4 + 4 + 3 + 5 + 3 | 22 |

Of the $5! = 120$ orders, $D, A, C, E, B$ is the only one of length 22, and the worst one is 52. The netlist order, as written by synthesis, ignores the layout, so its wires cross the block several times.

## Known algorithms

- [Nearest neighbor heuristic](/nearest-neighbor-heuristic/)
- [2-opt](/two-opt/), [3-opt](/three-opt/) and [Or-opt](/or-opt/)
- [Lin-Kernighan](/lin-kernighan/)
- [Christofides' algorithm](/christofides-algorithm/), adapted to paths
- [Held-Karp](/held-karp-algorithm/), exact for small groups

## Bounds

- **Hardness.** Deciding whether the wire length can be at most a given number is NP-complete, even when the points lie on an integer grid and $d$ is the Manhattan distance. Let $H$ be a grid graph, that is a finite set of grid points with edges between points at distance 1, and let $u, v$ be two of its points. Put $s = u$, $e = v$ and one flip-flop at every other point of $H$. Every distance between distinct grid points is at least 1, and an order has $n + 1$ wires, so $W(\pi) \ge n + 1$, with equality exactly when every wire joins neighbors of $H$, that is when the order is a Hamiltonian path of $H$ from $u$ to $v$. A graph with at least 3 points has a Hamilton circuit exactly when, for some edge $uv$, it has a Hamiltonian path from $u$ to $v$. Itai, Papadimitriou and Szwarcfiter (1982) showed that the Hamilton circuit problem is NP-complete for grid graphs, so a polynomial algorithm for scan ordering, run once per edge, would decide an NP-complete problem.
- **Lower bounds.** The path $s, x_{\pi(1)}, \ldots, x_{\pi(n)}, e$ is a spanning tree of all $n + 2$ points, so $W(\pi)$ is at least the weight of a [minimum spanning tree](/minimum-spanning-tree/) of $\{s, e, x_1, \ldots, x_n\}$. This bound is quick to compute and shows how far a heuristic order can be from the best.
- **Approximation.** With a metric $d$, Hoogeveen (1991) showed that Christofides' method adapted to a path with two fixed ends is within a factor $5/3$, and Zenklusen (2019) gave a factor $3/2$, as for tours. In practice, tools use local search, whose results are compared with the lower bound above.
- **Exact.** Dynamic programming over subsets solves $n$ flip-flops in $O(2^n n^2)$ time, so only for small groups, such as the cells of one region after partitioning.

## Reductions

- Scan chain ordering is a shortest Hamiltonian path with fixed ends, and an [asymmetric TSP](/asymmetric-tsp/) with one depot, as shown in the definition. Every TSP method applies.
- The [Hamiltonian path problem](/hamiltonian-path-problem/) in grid graphs reduces to it, as in the hardness bound, so it is not easier than general metric path TSP in the worst case.
- With $c$ chains of equal length it contains a balanced partition of the points, as in [vehicle routing](/vehicle-routing-problem/).

## Applications

- **Physical design flows.** Synthesis inserts scan in an arbitrary order. After [placement](/placement-problem/), the tool removes the scan connections, orders the flip-flops by region, and reconnects them. The result is checked again for hold time after [clock tree synthesis](/clock-tree-synthesis/).
- **Test compression.** With scan compression, the chains are short and many, so ordering is mostly a partition of the flip-flops into nearby groups of equal size, with a short path inside each group.
- **Low-power test.** Some methods order the flip-flops so that neighbors in the chain often hold equal values in the test patterns, which reduces switching during shift. The cost then mixes wire length with a count of transitions.

## References
