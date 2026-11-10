---
tag: D6Y1F9
kind: algorithm
slug: greedy-edge-heuristic
name: Greedy edge heuristic
aliases:
- multi-fragment heuristic
- greedy matching heuristic
area: approximation/tsp-approximation
level: core
summary: Keeps the cheapest edges that leave all degrees at most 2 and close no short cycle; on metric instances the worst-case ratio is Θ(log n), with the upper bound (1/2)(⌈lg n⌉ + 1).
solves: [metric-tsp]
model: word-ram
complexity:
  vars: {n: the number of cities}
  time: {worst: Θ(n^2 log n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1984
  people: [Hoon Liong Ong, J. B. Moore, Alan M. Frieze, Jon L. Bentley]
  note: Ong and Moore proved the upper bound; Frieze (1979) and Brecklinghaus and Hougardy (2015) gave lower-bound families; Bentley (1990s) made the method fast on large geometric instances.
prereqs: [metric-tsp, triangle-inequality, disjoint-set, kruskal]
see_also: [nearest-neighbor-tsp, nearest-insertion, clarke-wright-savings, christofides-algorithm, two-opt, lin-kernighan, kd-tree]
sources:
  - paper: doi:10.1016/0167-6377(84)90078-6
    title: Hoon Liong Ong and J. B. Moore, Worst-case analysis of two travelling salesman heuristics, Operations Research Letters 2(6), 1984
    locator: pages 273 to 277 (the greedy bound and the savings bound)
  - paper: doi:10.1016/j.orl.2015.02.009
    title: Judith Brecklinghaus and Stefan Hougardy, The approximation ratio of the greedy algorithm for the metric traveling salesman problem, Operations Research Letters 43(3), 2015
    locator: the main theorem (the ratio Θ(log n), also for graphic, Euclidean and rectilinear instances)
  - paper: doi:10.1137/0206041
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3), 1977
    locator: pages 563 to 581 (the charging lemma that the proof uses)
  - title: David S. Johnson and Lyle A. McGeoch, The traveling salesman problem, a case study in local optimization, in Aarts and Lenstra (eds.), Local Search in Combinatorial Optimization, Wiley, 1997
    locator: Section 2 (the greedy heuristic, Table 1 for random uniform instances)
---

The greedy edge heuristic builds a tour for the [metric TSP](/metric-tsp/) from the edges, not from a walk. It scans all pairs of cities from cheapest to most costly, and it keeps a pair when both cities still have fewer than two kept pairs and the pair closes no cycle, except the last pair that closes the tour. On metric instances the tour costs at most $\frac{1}{2}(\lceil \lg n \rceil + 1) \cdot \text{OPT}$, the same bound as for the [nearest-neighbor heuristic](/nearest-neighbor-tsp/), and families of instances show that the ratio is $\Theta(\log n)$. In practice it gives better tours than the nearest-neighbor heuristic.

## In plain words

Think of all the roads between the cities, sorted from shortest to longest. Go down the list. Take a road if both of its cities still have room, which means fewer than two roads each, and if the road does not close a loop too early. Skip it if not.

The chosen roads first form many short pieces of trip. The pieces grow and join, and at the end the last road closes one big loop through all cities.

Each choice is the cheapest one that is still allowed. Like the nearest-neighbor rule, this can leave a few cities to be joined at the end by long roads. The same counting argument shows that this costs at most a logarithmic factor.

## The problem

The input is a set $V$ of $n$ cities with a cost $d(u, v) = d(v, u) \ge 0$ for each pair, and the costs satisfy the [triangle inequality](/triangle-inequality/). The output is a tour of all cities, and its cost includes the closing edge. OPT is the least cost of a tour and ALG is the cost of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. The bound on this page is a worst-case bound for each instance.

## The algorithm

```pseudo id=main
GREEDY-EDGE(V, d)
L1  E ← all pairs {u, v}, sorted by d(u, v)
L2  deg[v] ← 0 for each city; each city is its own fragment   ▷ a disjoint-set structure
L3  for each pair {u, v} in E, in order do
L4      if deg[u] = 2 or deg[v] = 2 then skip the pair
L5      if u and v are in one fragment and fewer than n − 1 pairs are kept then skip the pair
L6      keep {u, v}; deg[u] ← deg[u] + 1; deg[v] ← deg[v] + 1; merge the fragments of u and v
L7      if n pairs are kept then stop
L8  return the cycle of the kept pairs
```

Line L5 uses a [disjoint-set](/disjoint-set/) structure, as in [Kruskal's algorithm](/kruskal/). The kept pairs are always a set of paths, called fragments, until the last pair. When $n - 1$ pairs are kept there is one path through all cities, and the only pair that passes line L4 is the pair of its two ends; line L5 lets it close the tour.

## Example

The six cities of the [nearest insertion](/nearest-insertion/) page lie in the plane with the Manhattan distance: $A(0,0)$, $B(2,0)$, $C(5,1)$, $D(4,4)$, $E(1,3)$ and $F(6,3)$. The sorted pairs begin with $AB$ (2), $CF$ (3), $DF$ (3), $AE$ (4), $BC$ (4), $BE$ (4), $CD$ (4) and $DE$ (4). Ties go to the pair that comes first in the alphabet.

| pair | cost | action | fragments after the step |
|---|---|---|---|
| $AB$ | 2 | keep | $A\,B$ |
| $CF$ | 3 | keep | $A\,B$; $C\,F$ |
| $DF$ | 3 | keep | $A\,B$; $C\,F\,D$ |
| $AE$ | 4 | keep | $E\,A\,B$; $C\,F\,D$ |
| $BC$ | 4 | keep | $E\,A\,B\,C\,F\,D$ |
| $BE$ | 4 | skip, $B$ has degree 2 | |
| $CD$ | 4 | skip, $C$ has degree 2 | |
| $DE$ | 4 | keep, closes the tour | $E\,A\,B\,C\,F\,D\,E$ |

The tour costs $2 + 3 + 3 + 4 + 4 + 4 = 20$, which is OPT for these cities. On other inputs greedy is worse. A seeded search over 8 points of a $7 \times 7$ grid with the Manhattan distance gives an instance with ALG $= 26$ and OPT $= 18$, a ratio $13/9$; the test file holds it.

**Measured behavior.** On 300 seeded instances of 10 uniform random points in the unit square with the Euclidean distance, the greedy tour was on average 7.42 percent above OPT, and at most 1.337 times OPT. On the same instances the nearest-neighbor tour was 10.4 percent above OPT. Johnson and McGeoch (1997) report greedy tours about 14 to 20 percent above the Held-Karp lower bound on large random uniform instances, against about 25 percent for nearest neighbor. These are measured values, not bounds.

## Correctness

**Theorem (Ong and Moore 1984).** For metric costs, the greedy edge tour satisfies

$$\text{ALG} \le \tfrac{1}{2}(\lceil \lg n \rceil + 1) \cdot \text{OPT}.$$

Orient the final tour in either direction, and let $\ell_p$ be the cost of the tour edge that leaves $p$, so ALG $= \sum_p \ell_p$. The proof has three steps.

1. **The greedy property.** For two cities $p, q$, $d(p, q) \ge \min(\ell_p, \ell_q)$. Look at the time when the pair $\{p, q\}$ was scanned. If it was kept, it leaves $p$ or $q$. If $p$ already had degree 2, both its edges are cheaper. If the pair would close a short cycle, then $p$ and $q$ were the two ends of a fragment, all of whose edges are cheaper, and the orientation leaves $p$ or $q$ along that fragment.
2. **One edge.** $\ell_p \le \text{OPT}/2$, because an optimal tour holds two disjoint paths between $p$ and its successor.
3. **Charging.** These are the two lemmas of the [nearest-neighbor analysis](/nearest-neighbor-tsp/), and the charging argument of Rosenkrantz, Stearns and Lewis at the scales $1, 2, 4, \ldots$ gives the bound.

The full proof is in the proof file, and it also shows that the scan always ends with a tour.

**Lower bounds.** Frieze (1979) gave metric instances with ratio of order $\log n / (3 \log \log n)$. Brecklinghaus and Hougardy (2015) gave instances with ratio of order $\log n$, also for graphic, Euclidean and rectilinear instances. So the worst-case ratio on metric instances is $\Theta(\log n)$. The test file does not build these families; it holds the small instance with ratio $13/9$.

**Hardness.** [Christofides' algorithm](/christofides-algorithm/) gets 3/2. No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **Sorting.** Line L1 sorts $n(n - 1)/2$ pairs in $\Theta(n^2 \log n)$ time and keeps them in $\Theta(n^2)$ space.
- **The scan.** Each pair costs $O(1)$ for line L4 and $O(\alpha(n))$ amortized for line L5, with a disjoint-set structure with union by rank and path compression, so the scan costs $O(n^2 \alpha(n))$.
- **Total.** $\Theta(n^2 \log n)$ time in the worst case in the [word RAM](/word-ram/).

For points in the plane, Bentley's implementation uses a [k-d tree](/kd-tree/) and a priority queue of nearest-neighbor candidates instead of all pairs. Its running time on uniform random points is close to $O(n \log n)$ in practice; this is a measured result, not a worst-case bound.

## Properties

- **Deterministic.** With a fixed order of equal costs, the output depends only on the input.
- **Kruskal with a degree limit.** Without line L4 and with line L5 always on, the scan is Kruskal's algorithm and gives a minimum spanning tree. The degree limit of 2 makes the result a set of paths.
- **A greedy matching.** The alias greedy matching comes from this view: the kept set is a greedy maximal subgraph of degree at most 2 without short cycles.
- **Not a local optimum.** The tour is usually not 2-optimal, and [2-opt](/two-opt/) or [Lin-Kernighan](/lin-kernighan/) improve it. Johnson and McGeoch found greedy to be a good start for these local searches.

## Variants and improvements

- **Clarke-Wright savings.** The [savings heuristic](/clarke-wright-savings/) uses the same scan on the savings $d(h, u) + d(h, v) - d(u, v)$ for a hub $h$. Ong and Moore proved the bound $\lceil \lg n \rceil + 1$ for it.
- **Candidate lists.** Scan only the $k$ nearest neighbors of each city, and fall back to a full search only to join the last fragments. This is the usual form for large instances.
- **[Nearest-neighbor heuristic](/nearest-neighbor-tsp/).** One fragment that grows at one end. The same worst-case bound, and worse tours in practice.
- **Christofides' algorithm.** The proved ratio 3/2, at the cost of a matching.

## When to use it

Use the greedy edge heuristic as the start tour of a local search on large instances, where it is fast and gives better tours than nearest neighbor. Do not use it when you need a proved constant factor. Then use the [double-tree algorithm](/double-tree-algorithm/) (factor 2), [nearest insertion](/nearest-insertion/) (factor 2) or Christofides' algorithm (factor 3/2).

## Pitfalls

- **The closing pair.** Line L5 must allow the pair that closes the tour when $n - 1$ pairs are kept. Code that always rejects a pair inside one fragment never closes the tour.
- **The degree test before the cycle test.** A pair inside one fragment between an end and an inner city is skipped by line L4. Only the two ends of a fragment can make a short cycle.
- **Memory.** The sorted list of all pairs takes $\Theta(n^2)$ space. For $10^5$ cities this is too much; use candidate lists.
- **Non-metric costs.** The greedy property holds for all costs, but the bound $\ell_p \le \text{OPT}/2$ needs the triangle inequality.

## Implementations

## History

The greedy rule for the TSP is old, and it is close to Kruskal's algorithm (1956). Frieze (1979) gave instances with a ratio of order $\log n / \log \log n$. Ong and Moore (1984) proved the upper bound $\frac{1}{2}(\lceil \lg n \rceil + 1)$ for greedy and $\lceil \lg n \rceil + 1$ for the savings method. Bentley (1990, 1992) gave fast geometric versions and called the method multi-fragment. Brecklinghaus and Hougardy (2015) closed the gap and showed the order $\log n$.

## References
