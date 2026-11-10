---
tag: AVDTNJ
kind: algorithm
slug: farthest-insertion
name: Farthest insertion
aliases:
- farthest insertion TSP
area: approximation/tsp-approximation
level: core
summary: Grows a cycle by adding the city farthest from it at its cheapest position; good tours in practice, a proved bound of only ⌈lg n⌉ + 1, and a metric lower bound of 6.5.
solves: [metric-tsp]
model: word-ram
complexity:
  vars: {n: the number of cities}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1977
  people: [Daniel J. Rosenkrantz, Richard E. Stearns, Philip M. Lewis II, Cor A. J. Hurkens]
  note: Rosenkrantz, Stearns and Lewis proved the bound ⌈lg n⌉ + 1 for all insertion orders; Hurkens (1992) gave metric instances with ratio 6.5.
prereqs: [metric-tsp, triangle-inequality, nearest-insertion]
see_also: [cheapest-insertion, nearest-neighbor-tsp, greedy-edge-heuristic, christofides-algorithm, or-opt, two-opt, lin-kernighan]
sources:
  - paper: doi:10.1137/0206041
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3), 1977
    locator: pages 563 to 581 (insertion methods, the bound ⌈lg n⌉ + 1 for any insertion order)
  - title: Cor A. J. Hurkens, Nasty TSP instances for farthest insertion, Proceedings of the 2nd Conference on Integer Programming and Combinatorial Optimization (IPCO), 1992
    locator: pages 346 to 352
  - title: Yossi Azar, Lower bounds for insertion methods for TSP, Combinatorics, Probability and Computing 3, 1994
    locator: pages 285 to 292
---

Farthest insertion builds a tour for the [metric TSP](/metric-tsp/). It keeps a cycle, and at each step it adds the city that is farthest from the cycle, at the position where the cycle grows least. On random points it gives some of the best tours of the simple construction rules. But its proved worst-case bound is only $(\lceil \lg n \rceil + 1) \cdot \text{OPT}$, the bound for every insertion order, and there are metric instances with ratio 6.5. No constant upper bound is known.

## In plain words

You plan a round trip one city at a time. Begin with one city. At each step, find the city that is farthest from the trip so far, and put it into the trip where it adds the least distance.

The far cities come first, so the trip soon has the rough outline of the whole map. The cities that come later lie between cities of the trip, and they usually add little. This is why the method works well in practice.

The proof of a good bound does not work for this rule. A far city can cost a lot to add, and nothing ties these costs to the best trip as tightly as for the nearest rule. What we can prove is the weak bound that holds for every insertion order.

## The problem

The input is a set $V$ of $n$ cities with a cost $d(u, v) = d(v, u) \ge 0$ for each pair, and the costs satisfy the [triangle inequality](/triangle-inequality/). The output is a tour of all cities, and its cost includes the closing edge. OPT is the least cost of a tour and ALG is the cost of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. The bounds on this page are worst-case bounds for each instance. The numbers for random points are measured, not proved.

## The algorithm

```pseudo id=main
FARTHEST-INSERTION(V, d, s)
L1  H ← the cycle (s)                          ▷ one city, cost 0
L2  for each city v do far[v] ← d(s, v)        ▷ distance from v to the closest city of H
L3  while H does not hold all cities do
L4      k ← a city not in H with the largest far[k]
L5      (a, b) ← an edge of H with the least d(a, k) + d(k, b) − d(a, b)
L6      put k between a and b in H
L7      for each city v do far[v] ← min(far[v], d(k, v))
L8  return H
```

The only change from [nearest insertion](/nearest-insertion/) is the largest value in line L4 in place of the least. The value far[v] is still the distance to the closest city of the cycle, and line L7 is the same update.

## Example

The six cities of the nearest insertion page lie in the plane with the Manhattan distance: $A(0,0)$, $B(2,0)$, $C(5,1)$, $D(4,4)$, $E(1,3)$ and $F(6,3)$. The run starts at $A$, and ties go to the earlier city and the earlier position.

| step | city added | distance to the cycle | increase | cycle | cost |
|---|---|---|---|---|---|
| 1 | $F$ | 9 | 18 | $A\,F$ | 18 |
| 2 | $E$ | 4 | 0 | $A\,E\,F$ | 18 |
| 3 | $C$ | 3 | 0 | $A\,E\,F\,C$ | 18 |
| 4 | $D$ | 3 | 2 | $A\,E\,D\,F\,C$ | 20 |
| 5 | $B$ | 2 | 0 | $A\,E\,D\,F\,C\,B$ | 20 |

The first step takes the farthest city $F$ and builds a cycle of cost 18 that already spans the map. Three of the next four steps cost nothing, because the new city lies on a shortest Manhattan path between two neighbors of the cycle. The tour costs 20, which is OPT.

**Measured behavior.** On 300 seeded instances of 10 uniform random points in the unit square, with the Euclidean distance and OPT from the [Held-Karp algorithm](/held-karp-algorithm/), the average excess over OPT was 0.67 percent for farthest insertion, 4.92 percent for cheapest insertion, 5.75 percent for nearest insertion and 10.4 percent for the [nearest-neighbor heuristic](/nearest-neighbor-tsp/). The worst ratio of farthest insertion in this sample was 1.111. These are measurements on small instances, not bounds.

## Correctness

**Theorem (Rosenkrantz, Stearns and Lewis 1977).** For metric costs, each insertion method that puts each city at a cheapest position, and so farthest insertion, returns a tour with

$$\text{ALG} \le (\lceil \lg n \rceil + 1) \cdot \text{OPT}.$$

Let $c_k$ be the increase when the city $k$ is added, and $\ell_k = c_k/2$. The proof has two steps.

1. **The half increases behave like nearest-neighbor edges.** If $p$ is in the cycle when $q$ is added, the position next to $p$ costs at most $2\,d(p, q)$. So $d(p, q) \ge \min(\ell_p, \ell_q)$ for all $p \ne q$, and $\ell_k \le d(s, k) \le \text{OPT}/2$.
2. **The charging bound.** These two facts are the two lemmas of the [nearest-neighbor analysis](/nearest-neighbor-tsp/). Its charging argument at the scales $1, 2, 4, \ldots$ gives $\sum_k \ell_k \le \frac{1}{2}(\lceil \lg n \rceil + 1) \cdot \text{OPT}$, so ALG $\le (\lceil \lg n \rceil + 1) \cdot \text{OPT}$.

The full proof is in the proof file. The proof does not use the farthest rule at all. The bound 2 for nearest and cheapest insertion needs each step to cost at most two times the distance from the cycle to the closest outside city. The farthest city can cost much more, so that proof does not apply.

**Lower bounds.** Hurkens (1992) gives metric instances where farthest insertion has ratio 6.5, and Euclidean instances in the plane with a ratio of about 2.43. A seeded search over 8 points of a $7 \times 7$ grid with the Manhattan distance gives an instance with ALG $= 28$ and OPT $= 18$, a ratio $14/9 \approx 1.56$; the test file holds it. So the good averages above hide bad cases, and farthest insertion is not a 2-approximation.

**Open question.** It is not known whether farthest insertion has a constant ratio on metric instances. The gap is between 6.5 and $\lceil \lg n \rceil + 1$.

**Hardness.** No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **Selection.** Lines L4 and L7 scan $n$ cities per step, $\Theta(n^2)$ in total.
- **Insertion.** Line L5 scans the edges of the cycle, $O(n)$ per step and $\Theta(n^2)$ in total.
- **Total.** $\Theta(n^2)$ time in the worst case in the [word RAM](/word-ram/), linear in the size of the cost matrix, and $\Theta(n)$ extra space.

## Properties

- **Deterministic.** With fixed tie rules, the output depends only on the input.
- **The far cities first.** The first city added is a city farthest from $s$, and the early cycles span the whole instance. In the plane the early cycle is close to the outline of the point set.
- **No certificate.** Unlike nearest insertion, the run does not compute a lower bound on OPT. The value $2 \max_k d(s, k)$ is a weak lower bound.

## Variants and improvements

- **[Nearest insertion](/nearest-insertion/) and [cheapest insertion](/cheapest-insertion/).** The proved ratio 2, but worse tours on random points in the measurement above.
- **Random insertion.** Pick the next city at random. The proof gives the same bound $\lceil \lg n \rceil + 1$. For arbitrary insertion orders, Azar (1994) gives lower bounds that grow with $n$.
- **Convex hull start.** In the plane, start with the convex hull. This is a common practical start, and the analysis above does not cover it.
- **Local search after.** [Or-opt](/or-opt/), [2-opt](/two-opt/) and [Lin-Kernighan](/lin-kernighan/) improve the tour further. The bound $\lceil \lg n \rceil + 1$ stays, because a local search never makes the tour longer.

## When to use it

Use farthest insertion when you want a good tour from a short program, and a proved bound is not needed. In the measurement above it was the best of the four simple rules. When you need a proved factor, use [nearest insertion](/nearest-insertion/) (factor 2) or [Christofides' algorithm](/christofides-algorithm/) (factor 3/2), and keep the farthest insertion tour if it is shorter. Then the result has both the proved bound and the practical quality.

## Pitfalls

- **Farthest from what.** The distance in line L4 is the distance to the closest city of the cycle, not to the farthest city of the cycle and not to the last city added. Other choices are different heuristics.
- **The claim of ratio 2.** The proof of the factor 2 for nearest insertion does not carry over. Do not state a constant ratio for farthest insertion: Hurkens's instances have ratio 6.5.
- **The update in line L7.** The value far[v] must go down with each new city. Code that keeps the distance to the start city only selects by a different rule.
- **Non-metric costs.** The proof needs the triangle inequality. With other costs the greedy steps give no bound.

## Implementations

## History

Farthest insertion is one of the classical construction rules. Rosenkrantz, Stearns and Lewis (1977) proved the bound $\lceil \lg n \rceil + 1$ for all insertion orders and the factor 2 for the nearest and cheapest rules, but no constant factor for the farthest rule. Hurkens (1992) gave the instances with ratio 6.5 for metric costs and a smaller ratio in the plane. The question of a constant ratio is still open.

## References
