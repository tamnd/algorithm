---
tag: PT0SHC
kind: algorithm
slug: bottleneck-tsp-approximation
name: Bottleneck TSP 2-approximation
aliases:
- threshold 2-approximation for bottleneck TSP
- Parker-Rardin algorithm
area: approximation/tsp-approximation
level: advanced
summary: Finds the least threshold t with a biconnected graph of cheap edges and a Hamiltonian cycle in its square; for metric costs the largest edge is at most 2t, at most twice the optimum.
solves: [bottleneck-tsp]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n^2 log n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1984
  people: [R. Gary Parker, Ronald L. Rardin]
  note: Parker and Rardin gave the 2-approximation in 1984 from Fleischner's theorem; Hochbaum and Shmoys (1986) put it in a general method for bottleneck problems.
prereqs: [bottleneck-tsp, biconnected-graph, graph-square, hamiltonian-cycle, triangle-inequality, binary-search-on-answer]
see_also: [minimum-bottleneck-spanning-tree, hopcroft-tarjan-biconnectivity, articulation-point, gonzalez-k-center, double-tree-algorithm, hamiltonian-cycle-np-completeness]
sources:
  - paper: doi:10.1016/0167-6377(84)90077-4
    title: R. Gary Parker and Ronald L. Rardin, Guaranteed performance heuristics for the bottleneck traveling salesman problem, Operations Research Letters 2(6), 1984
    locator: pages 269 to 272
  - title: Dorit S. Hochbaum and David B. Shmoys, A unified approach to approximation algorithms for bottleneck problems, Journal of the ACM 33(3), 1986
    locator: pages 533 to 550
  - title: Herbert Fleischner, The square of every two-connected graph is Hamiltonian, Journal of Combinatorial Theory, Series B 16, 1974
    locator: pages 29 to 34
  - title: Stephen Alstrup, Agelos Georgakopoulos, Eva Rotenberg and Carsten Thomassen, A Hamiltonian cycle in the square of a 2-connected graph in linear time, Proceedings of SODA 2018
    locator: pages 1645 to 1649
---

The bottleneck TSP 2-approximation of Parker and Rardin (1984) solves the metric [bottleneck TSP](/bottleneck-tsp/), where the goal is a tour whose most costly edge is as cheap as possible. It finds the least threshold $t$ for which the edges of cost at most $t$ form a [biconnected graph](/biconnected-graph/) $G(t)$, and returns a Hamiltonian cycle of the [square](/graph-square/) of $G(t)$. Each edge of that cycle costs at most $2t$, and $t \le \text{OPT}$, so the ratio is 2 on each instance. No polynomial algorithm has a ratio below 2 unless P = NP, so this is best possible.

## In plain words

A salesman must visit each city one time and come home, and he cares only about his longest single drive, not about the total. Try a limit on the length of a drive, and keep only the roads within the limit.

A round trip has a special shape: if any one city closes, the other cities are still connected along the trip. So the best limit must give a road network that also survives the loss of any one city. Find the smallest limit with this property. The best trip cannot use a smaller limit.

Now allow drives that pass one city in between. A theorem says that such a network always has a round trip. Each of these drives is at most two drives within the limit, so it is at most two times the limit, and so at most two times the best.

## The problem

The input is a set $V$ of $n \ge 3$ vertices with symmetric non-negative costs $c$ that satisfy the [triangle inequality](/triangle-inequality/). A tour is a cycle through all vertices, and its *bottleneck* is the largest cost of one of its $n$ edges. OPT is the least bottleneck of a tour and ALG is the bottleneck of the output, with ALG $\le \rho \cdot$ OPT for a ratio $\rho$. For a threshold $t$, $G(t)$ is the graph on $V$ with the edges $\{u, v\}$ of cost $c(u, v) \le t$.

## The algorithm

```pseudo id=main
BOTTLENECK-TSP-2(V, c)                     ▷ n ≥ 3
L1  t[1] < t[2] < ... < t[q] ← the distinct costs of the pairs, sorted
L2  lo ← 1, hi ← q
L3  while lo < hi do
L4      mid ← ⌊(lo + hi)/2⌋; if G(t[mid]) is biconnected then hi ← mid else lo ← mid + 1
L5  t ← t[lo]                              ▷ the least t with G(t) biconnected
L6  S ← the square of G(t)                 ▷ u, v adjacent if their distance in G(t) is 1 or 2
L7  H ← a Hamiltonian cycle of S           ▷ it exists by Fleischner's theorem
L8  return H and t
```

Lines L1 to L5 are a [binary search on the answer](/binary-search-on-answer/). It is correct because biconnectivity is monotone: if $G(t)$ is biconnected, so is $G(t')$ for each $t' > t$, because it has more edges. $G(t[q])$ is the complete graph, which is biconnected for $n \ge 3$. Line L4 tests biconnectivity with the [Hopcroft-Tarjan algorithm](/hopcroft-tarjan-biconnectivity/), which finds the [articulation points](/articulation-point/) in linear time. Line L7 uses an algorithm for Fleischner's theorem; Alstrup, Georgakopoulos, Rotenberg and Thomassen (2018) do it in linear time. The implementation on this page tests biconnectivity by removing each vertex in turn, and finds the cycle of line L7 by an exact dynamic program over subsets, so it is for small $n$ only.

## Example

Six points with the Manhattan distance: $A(2,4)$, $B(1,1)$, $C(2,5)$, $D(0,1)$, $E(5,1)$ and $F(3,2)$.

|  | $A$ | $B$ | $C$ | $D$ | $E$ | $F$ |
|---|---|---|---|---|---|---|
| $A$ | 0 | 4 | 1 | 5 | 6 | 3 |
| $B$ | 4 | 0 | 5 | 1 | 4 | 3 |
| $C$ | 1 | 5 | 0 | 6 | 7 | 4 |
| $D$ | 5 | 1 | 6 | 0 | 5 | 4 |
| $E$ | 6 | 4 | 7 | 5 | 0 | 3 |
| $F$ | 3 | 3 | 4 | 4 | 3 | 0 |

The distinct costs are $1, 3, 4, 5, 6, 7$. The binary search runs as follows.

| step | lo, hi | mid | threshold | $G$ biconnected? |
|---|---|---|---|---|
| 1 | 1, 6 | 3 | 4 | yes: no vertex is a cut vertex |
| 2 | 1, 3 | 2 | 3 | no: the edges $AC$, $BD$, $AF$, $BF$, $EF$ make $F$ a cut vertex |
| 3 | 3, 3 | | | stop with $t = 4$ |

$G(4)$ has the nine edges $AC$, $BD$ (cost 1), $AF$, $BF$, $EF$ (cost 3) and $AB$, $BE$, $CF$, $DF$ (cost 4). It has no Hamiltonian cycle, so OPT $> 4$; an optimal tour is $A\,B\,C\,F\,E\,D$ with bottleneck 5. The square $S$ adds, for example, the edge $CD$ through $F$. Line L7 returns the cycle $A\,F\,E\,D\,C\,B$, with the edge costs $3, 3, 5, 6, 5, 4$. So ALG $= 6$, and the bound promises at most $2t = 8$. The ratio on this instance is $6/5 = 1.2$.

## Correctness

**Theorem.** For metric costs and $n \ge 3$, BOTTLENECK-TSP-2 returns a tour $H$ whose bottleneck is at most $2t \le 2 \cdot \text{OPT}$. The ratio holds on each instance; the algorithm is deterministic.

The analysis has three steps.

1. **The lower bound on OPT.** An optimal tour uses only edges of cost at most OPT, so it is a Hamiltonian cycle of $G(\text{OPT})$. A graph with a Hamiltonian cycle is biconnected, because a cycle stays connected when one vertex is removed. OPT is one of the costs, so the search of lines L1 to L5 gives $t \le \text{OPT}$. This is the only lower bound on OPT that the analysis uses.
2. **The cycle exists.** By Fleischner's theorem (1974), the square of each biconnected graph has a Hamiltonian cycle. This theorem is cited here, not proved.
3. **Each edge is cheap.** An edge $\{u, v\}$ of $S$ is an edge of $G(t)$, of cost at most $t$, or there is a $w$ with $c(u, w) \le t$ and $c(w, v) \le t$. By the triangle inequality $c(u, v) \le 2t$.

The full proof is in the proof file.

**Tightness.** Both steps of the analysis are tight. The lower bound $t$ can be half of OPT: on the complete bipartite graph $K_{2,3}$, give the edges cost 1 and the other pairs cost 2. $G(1) = K_{2,3}$ is biconnected, so $t = 1$, but it has no Hamiltonian cycle, so OPT $= 2$. The upper bound $2t$ can be reached when $t = \text{OPT}$: on the cycle $C_6$ with its path metric, $t = \text{OPT} = 1$, and the square of $C_6$ has the Hamiltonian cycle $0\,2\,4\,5\,3\,1$ with bottleneck 2. Line L7 is free to return it, because the analysis does not prefer any cycle of $S$.

**Hardness.** No polynomial algorithm has a ratio $2 - \varepsilon$ for metric bottleneck TSP, for any $\varepsilon > 0$, unless P = NP. Take a graph $G$ and give its edges cost 1 and the other pairs cost 2. Costs 1 and 2 always satisfy the triangle inequality. OPT is 1 if $G$ has a [Hamiltonian cycle](/hamiltonian-cycle-np-completeness/) and 2 if not, so a ratio below 2 decides an NP-complete problem. Without the triangle inequality, use the cost $M$ instead of 2 for any large $M$: no ratio at all is possible unless P = NP.

## Complexity

- **Line L1.** Sorting the $\binom{n}{2}$ costs takes $O(n^2 \log n)$ time.
- **Lines L2 to L5.** The search makes $O(\log n)$ tests, because $q \le n^2$. Each test builds $G(t)$ and runs Hopcroft-Tarjan in $O(n^2)$ time, so the search takes $O(n^2 \log n)$.
- **Lines L6 and L7.** The square has $O(n^2)$ edges and takes $O(n^3)$ time to build with plain lists, or less with matrix products; the linear-time algorithm of Alstrup et al. finds the cycle without building $S$ in full.
- **Total.** $O(n^2 \log n)$ time with the linear-time cycle algorithm, in the [word RAM](/word-ram/), and $O(n^2)$ space.

## Properties

- **Best possible.** The ratio 2 matches the hardness bound, so no polynomial algorithm does better unless P = NP.
- **Uses only the order of the costs.** The threshold $t$ and the graph $S$ depend only on which costs are at most $t$. The bound $2t$ uses the triangle inequality only for the edges of $S$.
- **A bound for each run.** The run computes $t \le \text{OPT}$, so ALG$/t$ bounds the ratio on that instance.
- **The bottleneck spanning tree is weaker.** The least $t$ with $G(t)$ connected is the cost of a [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/). It is also at most OPT, but its square need not be Hamiltonian, and its cube gives only ratio 3.

## Variants and improvements

- **The cube of a connected graph.** The cube of each connected graph is Hamiltonian, and a cycle in the cube of a spanning tree is easy to find. With the least $t$ for which $G(t)$ is connected, this gives a simpler 3-approximation.
- **The general method.** Hochbaum and Shmoys (1986) use the same plan for many bottleneck problems: find the least threshold with a necessary property, and then use a power of the threshold graph. The [Gonzalez k-center algorithm](/gonzalez-k-center/) gets ratio 2 for $k$-center in the same spirit.
- **Exact algorithm.** Replace the biconnectivity test by a Hamiltonicity test: the least $t$ for which $G(t)$ has a Hamiltonian cycle is OPT. With a dynamic program over subsets this takes $O(2^n n^2 \log n)$ time.
- **The sum version.** For the usual TSP that minimizes the sum of the costs, see [metric TSP](/metric-tsp/) and [Christofides' algorithm](/christofides-algorithm/).

## When to use it

Use this algorithm when the worst single edge of a tour matters more than the total, for example when the longest leg of a route must fit a fuel range or a time limit. It gives the best possible ratio in polynomial time. For small instances, the exact threshold search with a Hamiltonicity test is also practical.

## Pitfalls

- **Testing connectivity instead of biconnectivity in line L4.** The least $t$ with $G(t)$ connected is also a lower bound, but the square of a connected graph is not always Hamiltonian. The tree made of three paths of two edges with a common end has a square with no Hamiltonian cycle, so line L7 can fail.
- **Costs that are not metric.** Step 3 of the analysis needs the triangle inequality. Without it, an edge of the square can cost much more than $2t$.
- **Searching over arbitrary numbers.** The search of lines L2 to L5 must run over the distinct costs, not over an interval of reals, or it can miss the exact least threshold.
- **Small $n$.** For $n \le 2$ there is no cycle in the usual sense, and $G(t)$ is never biconnected by the usual definition. Handle these cases first.

## Implementations

## History

Fleischner proved in 1974 that the square of each 2-connected graph is Hamiltonian, which answered a question of Nash-Williams and Plummer. Parker and Rardin (1984) used it to get the 2-approximation for the metric bottleneck TSP and showed that 2 is best possible. Hochbaum and Shmoys (1986) gave a unified method for bottleneck problems that includes this result. Lau gave a polynomial algorithm for the cycle of Fleischner's theorem in the early 1980s, and Alstrup, Georgakopoulos, Rotenberg and Thomassen (2018) made it linear.

## References
