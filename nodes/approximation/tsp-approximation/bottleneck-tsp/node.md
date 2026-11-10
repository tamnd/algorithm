---
tag: MJMN97
kind: problem
slug: bottleneck-tsp
name: Bottleneck TSP
aliases:
- min-max TSP
- bottleneck traveling salesman problem
area: approximation/tsp-approximation
level: advanced
summary: Find a tour whose most costly edge is as cheap as possible. It is NP-hard; for metric costs the ratio 2 of Parker and Rardin is best possible unless P = NP.
prereqs: [traveling-salesman-problem, hamiltonian-cycle-problem, biconnected-graph, approximation-ratio]
see_also: [bottleneck-tsp-approximation, minimum-bottleneck-spanning-tree, graph-square, metric-tsp, bottleneck-matching, k-center-problem, binary-search-on-answer, hamiltonian-cycle-np-completeness]
sources:
  - paper: doi:10.1016/0167-6377(84)90077-4
    title: R. Gary Parker and Ronald L. Rardin, Guaranteed performance heuristics for the bottleneck traveling salesman problem, Operations Research Letters 2(6), 1984
    locator: pages 269 to 272 (the 2-approximation and the hardness of 2 minus epsilon)
  - title: Dorit S. Hochbaum and David B. Shmoys, A unified approach to approximation algorithms for bottleneck problems, Journal of the ACM 33(3), 1986
    locator: pages 533 to 550 (bottleneck problems by thresholds and powers of graphs)
  - title: Herbert Fleischner, The square of every two-connected graph is Hamiltonian, Journal of Combinatorial Theory, Series B 16, 1974
    locator: pages 29 to 34
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Appendix A, Sections A1 (graph theory, Hamiltonian circuit) and A2 (network design, the traveling salesman problems)
---

The bottleneck TSP asks for a tour that visits each vertex once and makes its most costly edge as cheap as possible, so the objective is the maximum of the edge costs, not their sum. It is NP-hard, because a graph has a Hamiltonian cycle exactly when costs 1 on its edges and 2 elsewhere give the value 1. For costs with the triangle inequality, [Parker and Rardin](/bottleneck-tsp-approximation/) (1984) found a tour within a factor 2 of OPT, and no ratio below 2 is possible unless P = NP. The lower bound in all of this is the least threshold at which the cheap edges form a [biconnected graph](/biconnected-graph/).

## In plain words

A plane must visit each of a set of airports once and come back, and it can fly only so far without fuel. The total distance does not matter here. What matters is the longest single flight, because that decides which plane can make the trip. So you look for the round trip whose longest leg is as short as possible.

This is a different goal from the usual salesman problem, and the best routes for the two goals can be different. It is still hard to solve exactly. But when direct flights are never longer than detours, a fast method finds a round trip whose longest leg is at most twice the best possible, and no fast method can promise better.

## Definition

**Input.** A complete graph on $n \ge 3$ vertices with costs $c_e \ge 0$ on the edges.

**Output.** A tour $H$, a Hamiltonian cycle of the complete graph.

**Goal.** Minimize the *bottleneck* $b(H) = \max_{e \in H} c_e$. OPT is the least bottleneck of a tour and ALG the bottleneck of the returned tour. The convention is ALG $\le \rho \cdot \text{OPT}$ with $\rho \ge 1$, in the worst case.

**Threshold graphs.** For a number $t$, let $G(t)$ be the graph on all vertices with the edges of cost at most $t$. A tour has bottleneck at most $t$ exactly when it is a Hamiltonian cycle of $G(t)$. So

$$\text{OPT} = \min \{ t : G(t) \text{ has a Hamiltonian cycle} \},$$

and only the at most $\binom{n}{2}$ distinct costs need to be tried. The objective depends only on the order of the costs, not on their values: any increasing change of all costs keeps the optimal tours.

**Lower bounds (proved here).** Let $t_1$ be the least $t$ for which $G(t)$ is connected, and $t_2$ the least $t$ for which $G(t)$ is biconnected (2-connected). Then $t_1 \le t_2 \le \text{OPT}$. A tour is a 2-connected spanning subgraph, since removing any one vertex from a cycle leaves a path, so $G(\text{OPT})$, which contains an optimal tour, is biconnected and $t_2 \le \text{OPT}$. A biconnected graph is connected, so $t_1 \le t_2$. The value $t_1$ is the largest edge of a [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/), for example of any minimum spanning tree.

## Variants

- **Metric bottleneck TSP.** The costs satisfy the triangle inequality. This is the case with a constant ratio.
- **Maximum scatter TSP.** Maximize the *least* edge of the tour, for example to keep consecutive drill holes or welds far apart so that the material does not overheat.
- **Bottleneck path and asymmetric versions.** A Hamiltonian path, or a directed graph, with the same min-max objective.
- **Balanced and lexicographic versions.** Minimize the largest edge, and among those the sum, or minimize the gap between the largest and the least edge.
- **Related bottleneck problems.** The [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/) and the [bottleneck matching](/bottleneck-matching/) are polynomial; the [$k$-center problem](/k-center-problem/) is the classical bottleneck covering problem, with the same factor 2 and the same kind of threshold method.

## Examples

**Six points.** The points $A(2,4)$, $B(1,1)$, $C(2,5)$, $D(0,1)$, $E(5,1)$ and $F(3,2)$ with the Manhattan distance. All values were found by trying all tours.

| quantity | value |
|---|---|
| $t_1$, the largest edge of a minimum spanning tree ($AC$, $AF$, $BF$, $BD$, $EF$) | 3 |
| $t_2$, the least $t$ with $G(t)$ biconnected | 4 |
| OPT, the least bottleneck of a tour | 5 |
| the [Parker-Rardin tour](/bottleneck-tsp-approximation/) $A\,F\,E\,D\,C\,B$ | 6 $\le 2 t_2 = 8$ |

$G(4)$ is biconnected but has no Hamiltonian cycle, so $t_2 < \text{OPT}$ here.

**The two objectives differ.** On the same points, the least total cost of a tour is 18. The tour $A\,B\,D\,E\,F\,C$ costs 18 and has bottleneck 5, so it is optimal for both objectives, but the tour $A\,C\,D\,B\,E\,F$ also costs 18 and has bottleneck 6. In the other direction, the tour $A\,B\,C\,F\,E\,D$ has the optimal bottleneck 5 but costs 26. So an optimal tour for the sum can be bad for the bottleneck, and the reverse.

**Points on a line (proved here).** For points $x_1 < x_2 < \cdots < x_n$ on a line, the zigzag tour $x_1, x_3, x_5, \ldots$ out and $\ldots, x_6, x_4, x_2$ back is optimal, and

$$\text{OPT} = \max_{1 \le i \le n-2} (x_{i+2} - x_i).$$

*Proof.* The zigzag tour uses only edges between points two places apart, plus $x_1 x_2$ and $x_{n-1} x_n$, which are shorter, so its bottleneck is the right side. For the lower bound, fix $i$ and split the points into $L = \{x_1, \ldots, x_i\}$, the single point $x_{i+1}$, and $R = \{x_{i+2}, \ldots, x_n\}$, both nonempty. A cycle through all points goes from the side of $L$ to the side of $R$ and back, so it changes sides at least twice. A change that does not use a direct edge from $L$ to $R$ must pass through $x_{i+1}$, and $x_{i+1}$ has only two edges, so it serves at most one change. So the tour has an edge from $L$ to $R$, of length at least $x_{i+2} - x_i$. $\blacksquare$ For the points $0, 1, 3, 4, 8, 9, 10$ this gives OPT $= 5$, from the pairs $(3, 8)$ and $(4, 9)$, and a search over all tours agrees.

## Known algorithms

| algorithm | ratio | time | status |
|---|---|---|---|
| [Parker and Rardin](/bottleneck-tsp-approximation/): the square of the least biconnected $G(t)$ | 2 for metric costs, best possible | $O(n^2 \log n)$ | proved on that page |
| threshold search with a Hamiltonian cycle test | exact | $O(\log n)$ tests, each exponential | exact algorithm |
| [Held-Karp dynamic program](/held-karp-algorithm/) with max in place of sum | exact | $O(n^2 2^n)$ | exact algorithm |
| zigzag tour | exact for points on a line | $O(n \log n)$ | proved on this page |

The threshold search uses [binary search on the answer](/binary-search-on-answer/) over the sorted distinct costs. The tests for connection and biconnection take linear time each, by depth-first search ([Hopcroft and Tarjan](/hopcroft-tarjan-biconnectivity/)), so $t_1$ and $t_2$ are fast to compute.

## Bounds

**NP-hardness (proved here).** Given a graph $G$, set $c_e = 1$ on its edges and $c_e = 2$ on the other pairs. These costs satisfy the triangle inequality, and OPT $= 1$ exactly when $G$ has a [Hamiltonian cycle](/hamiltonian-cycle-problem/); otherwise OPT $= 2$. $\blacksquare$

**No ratio below 2 for metric costs (proved here; Parker and Rardin 1984).** In the instance above, OPT is 1 or 2. An algorithm with ratio $\rho < 2$ returns bottleneck $\le \rho < 2$, so bottleneck 1, exactly when $G$ is Hamiltonian. So a polynomial $\rho$-approximation with $\rho < 2$ decides Hamiltonian cycle, and P = NP. $\blacksquare$

**No ratio at all without the triangle inequality (proved here).** Use costs 1 on edges and $\rho + 1$ on non-edges. Then OPT is 1 or $\rho + 1$, and a $\rho$-approximation tells the two cases apart. $\blacksquare$

**The ratio 2 (cited here, proved on the algorithm page).** For metric costs, Fleischner's theorem (1974) says that the [square](/graph-square/) of a biconnected graph has a Hamiltonian cycle. Each edge of the square of $G(t_2)$ joins two vertices at distance at most 2 in $G(t_2)$, so by the triangle inequality it costs at most $2 t_2 \le 2 \cdot \text{OPT}$. Hochbaum and Shmoys (1986) put this in a general method: find the least threshold whose graph has a property that each optimal solution forces, then pay a factor for a power of that graph.

**The lower bound is tight within 2.** For $K_{2,3}$ with cost 1 on its six edges and cost 2 on the other four pairs, $G(1) = K_{2,3}$ is biconnected, so $t_2 = 1$, but $K_{2,3}$ has no Hamiltonian cycle, so OPT $= 2 = 2 t_2$.

## Reductions

- **From Hamiltonian cycle.** The costs 1 and 2 above show NP-hardness and the hardness of $2 - \varepsilon$.
- **To Hamiltonian cycle.** OPT is the least threshold $t$ for which $G(t)$ is Hamiltonian, so the bottleneck TSP is a sequence of $O(\log n)$ Hamiltonian cycle tests.
- **To the sum TSP, exactly.** Sort the distinct costs as $a_1 < a_2 < \cdots < a_k$ and give an edge of cost $a_j$ the new cost $(n + 1)^{j}$. A sum of $n$ new costs below $(n + 1)^{j + 1}$ uses only edges with index at most $j$, so a tour of least new sum also has the least bottleneck. The new costs have $O(k \log n)$ digits, which is polynomial, but they break the triangle inequality, so this keeps optimality and not ratios.

## Applications

- **Range limits.** Tours of a vehicle, a drone or an electric car that must recharge at each stop, where the longest leg must be within the range.
- **Fairness and waiting times.** Visiting customers or sensors in a cycle so that the longest wait between two consecutive visits is short.
- **Manufacturing.** In the maximum scatter version, keeping consecutive operations far apart, as in riveting and welding sequences.
- **Theory.** A clean example of a threshold method with a matching hardness bound, next to [$k$-center](/k-center-problem/) and the [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/).

## References
