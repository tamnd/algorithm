---
tag: F3GHE4
kind: algorithm
slug: nearest-neighbor-tsp
name: Nearest-neighbor heuristic for TSP
aliases:
- greedy nearest neighbour tour
area: approximation/tsp-approximation
level: intro
summary: Walks to a closest unvisited city until all are visited; on metric instances its worst-case ratio is Θ(log n), with the upper bound (1/2)(⌈lg n⌉ + 1).
solves: [metric-tsp]
model: word-ram
complexity:
  vars: {n: the number of cities}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1977
  people: [Daniel J. Rosenkrantz, Richard E. Stearns, Philip M. Lewis II]
  note: The rule is much older; Rosenkrantz, Stearns and Lewis gave the first worst-case analysis, and Hougardy and Wilde (2014) gave simple grid instances that show the order log n.
prereqs: [metric-tsp, triangle-inequality, nearest-neighbor-heuristic]
see_also: [greedy-edge-heuristic, nearest-insertion, double-tree-algorithm, christofides-algorithm, two-opt, or-opt, space-filling-curve-tsp, metric-tsp-inapproximability]
sources:
  - paper: doi:10.1137/0206041
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3), 1977
    locator: pages 563 to 581 (the nearest neighbor bound and its lower-bound family)
  - title: Stefan Hougardy and Mirko Wilde, On the nearest neighbor rule for the metric traveling salesman problem, arXiv 1401.2071, 2014
    locator: Theorem 2.1 and the construction of the graphs G_k
  - title: Cor A. J. Hurkens and Gerhard J. Woeginger, On the nearest neighbor rule for the traveling salesman problem, Operations Research Letters 32(1), 2004
    locator: the main theorems (graphic and Euclidean lower bounds)
  - title: David S. Johnson and Lyle A. McGeoch, The traveling salesman problem, a case study in local optimization, in Aarts and Lenstra (eds.), Local Search in Combinatorial Optimization, Wiley, 1997
    locator: Section 2 (tour construction heuristics, the nearest neighbor results)
---

The nearest-neighbor heuristic builds a tour for the [metric TSP](/metric-tsp/): it starts at a city and goes to a closest unvisited city until no city is left, and then it goes back to the start. On each metric instance the tour costs at most $\frac{1}{2}(\lceil \lg n \rceil + 1) \cdot \text{OPT}$, and grid instances show that no constant bound holds, so the worst-case ratio is $\Theta(\log n)$. This page gives the full analysis. The rule itself, its variants and its behavior on random points are on the page [nearest-neighbor heuristic](/nearest-neighbor-heuristic/).

## In plain words

A traveler is in one city and must visit all the others. At each step she goes to the closest city that she has not seen yet. At the end she goes home.

Each step looks good, but the last steps can be bad. The traveler can leave a few cities behind in one corner and come back for them from far away. On the right map this happens again and again at many scales, and the trip becomes many times longer than the best trip.

There is still a limit. Two cities that are both left by long steps are far apart, so the best trip must also be long. When you count this at each scale, the trip is at most about half the number of scales times the best trip, and the number of scales grows like the logarithm of the number of cities.

## The problem

The input is a set $V$ of $n$ cities and a cost $d(u, v) = d(v, u) \ge 0$ for each pair, with the [triangle inequality](/triangle-inequality/). The output is a tour, an order of all cities, and its cost includes the edge from the last city back to the first. OPT is the least cost of a tour and ALG is the cost of the tour that the algorithm returns. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem, and $\rho$ is the [approximation ratio](/approximation-ratio/). The bound on this page is a worst-case bound for each instance, not an expected bound.

## The algorithm

```pseudo id=main
NEAREST-NEIGHBOR(V, d, s)                ▷ s is the start city
L1  mark all cities as unvisited
L2  H ← (s); mark s as visited; here ← s
L3  while some city is unvisited do
L4      v ← an unvisited city with the least d(here, v)   ▷ ties: a fixed rule
L5      append v to H; mark v as visited
L6      here ← v
L7  return H                             ▷ the tour visits H in order and returns to s
```

Line L4 scans all unvisited cities, so each step costs $O(n)$. The implementation breaks ties by a rank array: by the city number when no rank is given. The analysis holds for each start city and each tie rule.

## Example

The smallest grid of Hougardy and Wilde has 10 points in two rows, $(x, y)$ with $0 \le x \le 4$ and $y \in \{0, 1\}$, and the cost is the Manhattan distance. This is also the shortest path metric of the grid graph. The run starts at $(0, 0)$, and each tie goes against the algorithm.

| step | from | to | cost | closest unvisited cities |
|---|---|---|---|---|
| 1 | (0,0) | (0,1) | 1 | (0,1) and (1,0) tie |
| 2 | (0,1) | (1,1) | 1 | |
| 3 | (1,1) | (1,0) | 1 | (1,0) and (2,1) tie |
| 4 | (1,0) | (2,0) | 1 | |
| 5 | (2,0) | (3,0) | 1 | (3,0) and (2,1) tie |
| 6 | (3,0) | (4,0) | 1 | (4,0) and (3,1) tie |
| 7 | (4,0) | (4,1) | 1 | |
| 8 | (4,1) | (3,1) | 1 | |
| 9 | (3,1) | (2,1) | 1 | |
| close | (2,1) | (0,0) | 3 | |

ALG $= 9 + 3 = 12$. The boundary of the grid is a tour of 10 unit edges and each cost is at least 1, so OPT $= 10$ and ALG/OPT $= 1.2$. The bound of the theorem is $\frac{1}{2}(\lceil \lg 10 \rceil + 1) = 2.5$. The run left the point $(2, 1)$ in the middle and ended there, so the return trip is long. In the larger grids the same trap repeats at each scale.

## Correctness

**Theorem (Rosenkrantz, Stearns and Lewis 1977).** For metric costs and $n \ge 2$, the nearest-neighbor tour satisfies

$$\text{ALG} \le \tfrac{1}{2}\left(\lceil \lg n \rceil + 1\right) \cdot \text{OPT}.$$

For a city $p$, let $\ell_p$ be the cost of the tour edge that leaves $p$, so ALG $= \sum_p \ell_p$. The proof has three steps.

1. **The greedy property.** For two cities $p$ and $q$, $d(p, q) \ge \min(\ell_p, \ell_q)$. When the algorithm left the city of the two that it visited first, the other city was still a candidate.
2. **Two lower bounds on OPT.** One edge: $\ell_p \le \text{OPT}/2$, because an optimal tour holds two disjoint paths between $p$ and its successor. A subset: each set $S$ of cities has a tour of cost at most OPT, by shortcuts along an optimal tour.
3. **Charging at each scale.** Sort the values so that $\ell_1 \ge \ell_2 \ge \cdots \ge \ell_n$. Take the $2k$ cities with the largest values. In a tour of these cities, charge each edge to its end with the smaller value. Each city takes at most two charges, so $\text{OPT} \ge 2 \sum_{i=k+1}^{\min(2k,n)} \ell_i$. The sum over $k = 1, 2, 4, \ldots, 2^{\lceil \lg n \rceil - 1}$, plus $\text{OPT} \ge 2 \ell_1$, gives the theorem.

The full proof is in the proof file.

**Tightness up to a constant.** Hougardy and Wilde (2014) build a grid $G_k$ with two rows and $W_k = 8 \cdot 2^k - 3$ columns, so $n = 16 \cdot 2^k - 6$. $G_{k+1}$ is two copies of $G_k$ with three columns between them. The path in $G_{k+1}$ runs the path of the left copy, which ends in the middle of that copy, jumps to the free columns, walks into the right copy, runs its path, and jumps back to the middle of $G_{k+1}$. With the Manhattan metric each step goes to a closest unvisited point, and the tour costs $(16 + 4k) 2^k - 4$ while OPT $= n$. So

$$\frac{\text{ALG}}{\text{OPT}} \ge \frac{k + 4}{4} = \frac{\lg(n + 6)}{4}.$$

The same paper gives Euclidean and rectilinear versions of the family. Earlier families give ratios of about $\frac{1}{3} \lg n$ (Rosenkrantz, Stearns and Lewis), and Hurkens and Woeginger (2004) give about $\frac{1}{4} \lg n$ for graphic instances and $(\sqrt{3} - \frac{3}{2})(\lg n - 2)$ for Euclidean instances. So the worst-case ratio is $\Theta(\log n)$, and no constant bound holds.

**Hardness.** The $\Theta(\log n)$ ratio is a property of this rule. [Christofides' algorithm](/christofides-algorithm/) gets 3/2 on the same instances. No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality, Lemma 2 of the proof fails, and no polynomial algorithm has a constant ratio unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **Time.** There are $n - 1$ steps, and line L4 scans at most $n$ cities in each step. This is $\Theta(n^2)$ in the worst case on a cost matrix, in the [word RAM](/word-ram/) with costs that fit in a word. Each pair of cities is read at most one time, so this is linear in the size of the matrix.
- **Space.** $\Theta(n)$ extra space for the visited marks and the tour.
- **Geometric inputs.** For points in the plane, a [k-d tree](/kd-tree/) with deletions answers each query of line L4. This is fast in practice on spread-out points, but it gives no better worst-case bound.

## Properties

- **Deterministic.** With a fixed start and a fixed tie rule, the output depends only on the input.
- **Any start, any tie rule.** The bound holds for each choice. Running from all $n$ starts and keeping the best tour costs $\Theta(n^3)$ time, and the theorem gives no better bound for it.
- **A certificate in each run.** The values $\ell_p$ give $\text{OPT} \ge 2 \max_p \ell_p$ and the charging bounds, so a run can report a lower bound on OPT at no extra cost.
- **Not a local optimum.** The tour often has crossing edges in the plane, so [2-opt](/two-opt/) improves it.

## Variants and improvements

- **Insertion rules.** [Nearest insertion](/nearest-insertion/) and [cheapest insertion](/cheapest-insertion/) grow a cycle instead of a path and get the ratio 2.
- **Greedy edge.** The [greedy edge heuristic](/greedy-edge-heuristic/) adds the cheapest edge that keeps a set of paths. It also has a $\Theta(\log n)$ worst case, but it gives better tours on random points.
- **Proved constant ratios.** The [double-tree algorithm](/double-tree-algorithm/) gets 2, and Christofides' algorithm gets 3/2.
- **Local search after.** [2-opt](/two-opt/), [Or-opt](/or-opt/) and [Lin-Kernighan](/lin-kernighan/) start well from a nearest-neighbor tour.

## When to use it

Use the nearest-neighbor heuristic as a fast start tour for a local search, or when you need a tour with very little code. Do not use it when you need a proved constant factor; use the double-tree algorithm or Christofides' algorithm. On uniform random points in the plane, Johnson and McGeoch (1997) report tours about 25 percent above the Held-Karp lower bound; this is a measured value, not a bound.

## Pitfalls

- **The closing edge.** The last edge back to the start is often the longest edge of the tour, as in the example. A cost function that sums only $n - 1$ edges reports a value that is too small, and the bound of the theorem is about the closed tour.
- **Non-metric costs.** Without the triangle inequality, the greedy choices give no bound at all.
- **Ties.** A fixed tie rule makes the output reproducible, but the bound is the same for all rules. Do not expect a tie rule to remove the bad cases: Hougardy and Wilde also give Euclidean versions of the grids.
- **A quadratic scan in a large instance.** For a million points the scan of line L4 is too slow; use a spatial index.

## Implementations

## History

The nearest-neighbor rule is one of the oldest tour construction rules, and it was in use well before its worst case was known. Rosenkrantz, Stearns and Lewis (1977) proved the upper bound $\frac{1}{2}(\lceil \lg n \rceil + 1)$ and gave instances with a ratio of order $\log n$. Johnson and Papadimitriou, and later Hurkens and Woeginger (2004), gave simpler families, also in the Euclidean plane. Hougardy and Wilde (2014) gave the two-row grids of this page, which are graphic, Euclidean and rectilinear at the same time.

## References
