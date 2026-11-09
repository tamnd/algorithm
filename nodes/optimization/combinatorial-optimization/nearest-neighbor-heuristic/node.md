---
tag: 0YM2MN
kind: algorithm
slug: nearest-neighbor-heuristic
name: Nearest neighbor heuristic for TSP
aliases:
- greedy tour construction
- nearest neighbour heuristic
- NN tour
area: optimization/combinatorial-optimization
level: intro
summary: Repeatedly travel to the closest unvisited city.
solves: [traveling-salesman-problem]
model: word-ram
complexity:
  vars: {n: the number of cities}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1977
  people: [Daniel J. Rosenkrantz, Richard E. Stearns, Philip M. Lewis II]
  note: The rule is older than its analysis. Rosenkrantz, Stearns and Lewis proved the logarithmic bound for metric costs in 1977.
prereqs: [traveling-salesman-problem, metric-tsp, greedy-algorithm]
see_also: [nearest-neighbor-tsp, greedy-edge-heuristic, nearest-insertion, two-opt, christofides-algorithm, metric-tsp, approximation-ratio, clarke-wright-savings]
sources:
  - paper: doi:10.1137/0206041
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3), 563 to 581, 1977
    locator: the section on the nearest neighbor method, the upper bound (lg n rounded up + 1)/2 and the family of instances with ratio above (1/3) lg(n + 1) + 4/9
  - paper: "David S. Johnson and Christos H. Papadimitriou, Performance guarantees for heuristics, Chapter 5 in E. L. Lawler, J. K. Lenstra, A. H. G. Rinnooy Kan and D. B. Shmoys (editors), The Traveling Salesman Problem, Wiley, 1985"
    locator: the section on the nearest neighbor rule and other tour construction heuristics
  - paper: "David S. Johnson and Lyle A. McGeoch, The traveling salesman problem, a case study in local optimization, in E. H. L. Aarts and J. K. Lenstra (editors), Local Search in Combinatorial Optimization, Wiley, 1997, 215 to 310"
    locator: the section on tour construction heuristics (nearest neighbor and greedy) and their measured excess over the Held-Karp bound
  - paper: doi:10.1016/S0166-218X(01)00195-0
    title: Gregory Gutin, Anders Yeo and Alexey Zverovich, Traveling salesman should not be greedy, domination analysis of greedy-type heuristics for the TSP, Discrete Applied Mathematics 117(1 to 3), 81 to 86, 2002
    locator: the theorem that the nearest neighbor rule can return the unique worst tour
  - paper: doi:10.1145/321958.321975
    title: Sartaj Sahni and Teofilo Gonzalez, P-complete approximation problems, Journal of the ACM 23(3), 555 to 565, 1976
    locator: the general TSP has no constant ratio unless P = NP
---

The nearest neighbor heuristic builds a [traveling salesman](/traveling-salesman-problem/) tour by starting at one city and always moving to the closest city not yet visited; after the last city it returns to the start. It takes $\Theta(n^2)$ time on a cost matrix. With [metric](/metric-tsp/) costs its tour is at most $\frac{1}{2}(\lceil \lg n \rceil + 1)$ times the optimum, and Rosenkrantz, Stearns and Lewis (1977) gave instances where the ratio grows as $\frac{1}{3}\lg n$, so the worst-case [approximation ratio](/approximation-ratio/) is $\Theta(\log n)$. Without the triangle inequality it can be arbitrarily bad.

## In plain words

You are in a town and must visit every other town once and then go home. The rule is simple: from where you stand, go to the closest town that you have not seen yet. Repeat until no town is left, then drive home.

The rule is fast and usually gives a trip that is some 10 to 25 percent too long. Its weak point is the end. Early on, it eats up all the near towns, and the towns it skipped are left for the end, so the last legs and the drive home can be long. On bad maps the trip can be longer than the best one by a factor that grows slowly with the number of towns.

## The problem

The input is $n$ cities with costs $c(u, v) = c(v, u) \ge 0$ and a start city $s$. The output is a tour, an order of all cities that begins at $s$, closed by the edge back to $s$. The goal of the [traveling salesman problem](/traveling-salesman-problem/) is a tour of least total cost. The heuristic does not guarantee this. Its guarantee is a ratio to the optimum, and only for [metric costs](/metric-tsp/).

## The algorithm

```pseudo id=main
NEAREST-NEIGHBOR-TOUR(c, n, s)
L1  tour ← [s], mark s visited
L2  cur ← s
L3  repeat n − 1 times
L4      next ← nil
L5      for each city j do
L6          if j is unvisited and (next = nil or c(cur, j) < c(cur, next)) then next ← j
L7      append next to tour, mark next visited
L8      cur ← next
L9  return tour                          ▷ the tour is closed by the edge (cur, s)
```

Lines L4 to L6 scan all cities and keep the closest unvisited one. With the strict test in line L6, ties go to the city that comes first in the scan.

## Example

Put five cities on a line at the positions $0, 1, -2, 5, -10$, with cost $c(x, y) = |x - y|$, and start at 0.

| step | current | unvisited cities with their costs | next | edge cost | total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 (1), −2 (2), 5 (5), −10 (10) | 1 | 1 | 1 |
| 2 | 1 | −2 (3), 5 (4), −10 (11) | −2 | 3 | 4 |
| 3 | −2 | 5 (7), −10 (8) | 5 | 7 | 11 |
| 4 | 5 | −10 (15) | −10 | 15 | 26 |
| close | −10 | | 0 | 10 | 36 |

The tour zigzags: 0, 1, −2, 5, −10, 0, with cost 36. Every tour must go from the leftmost to the rightmost city and back, so the optimum is $2 \cdot (5 - (-10)) = 30$, and the ratio is $1.2$. The bound of the theorem for $n = 5$ is $\frac{1}{2}(3 + 1) = 2$.

On the 5-city grid instance of the [traveling salesman problem](/traveling-salesman-problem/) page, the rule from city A goes A, E, B, C, D, A with cost 16, which is optimal there.

## Correctness

The output is always a tour: each iteration of line L3 adds one unvisited city (one exists, because fewer than $n$ cities are visited), so after $n - 1$ iterations every city is in the list exactly once.

**Theorem (Rosenkrantz, Stearns and Lewis).** If the costs satisfy the triangle inequality, the tour costs at most $\frac{1}{2}(\lceil \lg n \rceil + 1) \cdot \mathrm{OPT}$.

The proof uses two facts. Let $\ell_i$ be the cost of the tour edge that leaves city $i$. First, $c(i, j) \ge \min(\ell_i, \ell_j)$ for all $i \ne j$: whichever of the two the tour visits first, the other was still unvisited then, so line L6 chose an edge no longer than $c(i, j)$. Second, $\ell_i \le \mathrm{OPT}/2$, because the optimal tour gives two paths between any two cities. Then for each $k = 1, 2, 4, \ldots$, shortcut the optimal tour to the $\min(2k, n)$ cities with the largest $\ell$. The shortcut tour costs at most $\mathrm{OPT}$, and each of its edges costs at least the smaller $\ell$ of its ends. So $\mathrm{OPT} \ge 2 \sum_{i=k+1}^{\min(2k, n)} \ell_{(i)}$, where $\ell_{(1)} \ge \ell_{(2)} \ge \cdots$ are the sorted values. Adding these $\lceil \lg n \rceil$ inequalities and $\ell_{(1)} \le \mathrm{OPT}/2$ gives the bound. The full proof is in the proof file below.

## Complexity

- **Time.** Line L3 runs $n - 1$ times, and the scan of lines L5 and L6 takes $\Theta(n)$ each time. Total $\Theta(n^2)$, in every case, because the scan does not stop early. This is linear in the size of the cost matrix.
- **Space.** $\Theta(n)$ extra, for the visited marks and the tour.
- **Points in the plane.** When the costs are distances between points, a spatial index such as a k-d tree with deletion finds the closest unvisited point without a full scan, and this is much faster in practice for large $n$.
- **Repeated nearest neighbor.** Running the rule from every start and keeping the best tour takes $\Theta(n^3)$.

## Properties

- **Ratio, metric costs.** At most $\frac{1}{2}(\lceil \lg n \rceil + 1)$. Rosenkrantz, Stearns and Lewis built metric instances with ratio larger than $\frac{1}{3}\lg(n+1) + \frac{4}{9}$ for infinitely many $n$, so the ratio is $\Theta(\log n)$. It is not a constant-factor [approximation algorithm](/approximation-ratio/), in contrast to [nearest insertion](/nearest-insertion/) (ratio 2) and [Christofides' algorithm](/christofides-algorithm/) (ratio $3/2$).
- **Ratio, general costs.** Unbounded. With $c(0,1) = c(1,2) = c(2,3) = 1$, $c(0,2) = c(1,3) = 2$ and $c(0,3) = M$, the rule from city 0 goes 0, 1, 2, 3 and pays $3 + M$, while the tour 0, 1, 3, 2 costs 6. This agrees with the theorem of Sahni and Gonzalez that no polynomial-time algorithm has a bounded ratio for general costs unless P = NP.
- **Domination.** Gutin, Yeo and Zverovich (2002) showed that there are instances of arbitrarily large size on which the rule returns the unique worst tour.
- **Depends on the start.** Different start cities give different tours. With the tie rule fixed, the output is deterministic.
- **Measured behavior.** We ran 300 instances of 10 points drawn uniformly from the unit square (Python `random.Random(20261109)`), with Euclidean costs and the optimum from the [Held-Karp algorithm](/held-karp-algorithm/). The rule from a fixed start had mean ratio 1.116, median 1.103, maximum 1.452, and found the optimum in 9.7 percent of the instances. The best of the 10 starts had mean ratio 1.026, maximum 1.213, and was optimal in 42.7 percent. Johnson and McGeoch (1997) report an excess of about 25 percent over the Held-Karp bound for large random uniform instances.

## Variants and improvements

- **Repeated nearest neighbor.** Run from every start, keep the best. Cost $\Theta(n^3)$, much better tours in practice, same worst-case order.
- **Nearest neighbor followed by local search.** The tour is a common start for [2-opt](/two-opt/), [Or-opt](/or-opt/) or [Lin-Kernighan](/lin-kernighan/), which remove the long closing edges.
- **[Greedy edge](/greedy-edge-heuristic/).** Add the cheapest edges overall that keep degrees at most 2 and create no short cycle. In the experiments of Johnson and McGeoch its tours are usually better than those of nearest neighbor.
- **[Nearest insertion](/nearest-insertion/) and [cheapest insertion](/cheapest-insertion/).** Grow a cycle instead of a path. These have ratio 2 for metric costs.
- **Asymmetric costs.** The same rule applies with $c(cur, j)$ in the direction of travel.

## When to use it

Use it when a valid tour is needed fast and simply, or as the starting tour for [local search](/local-search/), [simulated annealing](/simulated-annealing/) or a [large neighborhood search](/large-neighborhood-search/). Do not use it alone when quality matters: [2-opt](/two-opt/) on top of it costs little and removes most of the excess. Do not use it when a guaranteed ratio is required: use [Christofides' algorithm](/christofides-algorithm/) for metric costs.

## Pitfalls

- **Forgetting the closing edge.** The cost of the tour includes the edge from the last city back to the start, and this edge is often the longest.
- **Assuming a ratio without the triangle inequality.** The logarithmic bound needs metric costs. On general costs the rule can pick a cheap path that forces a very expensive last edge.
- **Quadratic work hidden in a nearest-point query.** Removing visited cities from a list by search costs $\Theta(n)$ per step on top of the scan. Use a visited array, as in line L6.
- **Floating-point ties.** With real coordinates two cities can be equally close up to rounding, and different machines can choose differently. Fix a tie rule, as the strict test of line L6 does.

## Implementations

## History

The nearest neighbor rule is one of the first tour construction methods, and it was used long before it was analyzed. Rosenkrantz, Stearns and Lewis (1977) proved the logarithmic upper bound for metric costs and the matching lower bound family, in the same paper where they proved ratio 2 for nearest and cheapest insertion. Johnson and Papadimitriou (1985) surveyed these guarantees, and Johnson and McGeoch (1997) measured the rule on large random and real instances. Gutin, Yeo and Zverovich (2002) showed that it can return the worst possible tour.

## References
