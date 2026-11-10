---
tag: ZCN8SR
kind: algorithm
slug: cheapest-insertion
name: Cheapest insertion
aliases:
- cheapest insertion TSP
area: approximation/tsp-approximation
level: core
summary: Grows a cycle by adding the city and the position with the least extra cost; on metric instances the tour costs at most 2(1 − 1/n) OPT, and this is tight.
solves: [metric-tsp]
model: word-ram
complexity:
  vars: {n: the number of cities}
  time: {worst: Θ(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1977
  people: [Daniel J. Rosenkrantz, Richard E. Stearns, Philip M. Lewis II]
  note: Rosenkrantz, Stearns and Lewis proved the ratio 2 for cheapest insertion together with nearest insertion.
prereqs: [metric-tsp, triangle-inequality, minimum-spanning-tree, mst-lower-bound-for-tsp]
see_also: [nearest-insertion, farthest-insertion, nearest-neighbor-tsp, greedy-edge-heuristic, double-tree-algorithm, christofides-algorithm, or-opt]
sources:
  - paper: doi:10.1137/0206041
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3), 1977
    locator: pages 563 to 581 (cheapest insertion, its bound 2 and its running time)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.4 (the nearest addition algorithm and the MST bound)
  - title: Yossi Azar, Lower bounds for insertion methods for TSP, Combinatorics, Probability and Computing 3, 1994
    locator: pages 285 to 292
---

Cheapest insertion builds a tour for the [metric TSP](/metric-tsp/). It keeps a cycle through some of the cities, and at each step it looks at all pairs of a city outside the cycle and an edge of the cycle, and it makes the insertion that adds the least cost. The tour costs at most two times a [minimum spanning tree](/minimum-spanning-tree/), so at most $2(1 - 1/n) \cdot \text{OPT}$, and a family on cycle graphs reaches this bound exactly. The plain version runs in $\Theta(n^3)$ time.

## In plain words

You plan a round trip one city at a time. Begin with one city. At each step, try each city that is not in the trip yet, at each place in the trip, and make the insertion that makes the trip grow least.

This is a greedy choice, and it can still go wrong. But each step is at most as costly as a detour to the closest city outside the trip, there and back. These closest distances never add up to more than the cheapest network that connects all cities, for each order in which the cities come in. The best round trip costs more than that network, so the trip is never more than two times the best one.

## The problem

The input is a set $V$ of $n$ cities with a cost $d(u, v) = d(v, u) \ge 0$ for each pair, and the costs satisfy the [triangle inequality](/triangle-inequality/). The output is a tour of all cities, and its cost includes the closing edge. OPT is the least cost of a tour and ALG is the cost of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. The bound on this page is a worst-case bound for each instance.

## The algorithm

```pseudo id=main
CHEAPEST-INSERTION(V, d, s)
L1  H ← the cycle (s)                          ▷ one city, cost 0
L2  while H does not hold all cities do
L3      for each city k not in H and each edge (a, b) of H do
L4          keep the pair with the least d(a, k) + d(k, b) − d(a, b)
L5      put the kept city k between the kept a and b
L6  return H
```

When $H$ has one city $s$, the only position makes the cycle $s, k$, of cost $2\,d(s, k)$. Lines L3 and L4 choose the city and the position at the same time. This is the difference from [nearest insertion](/nearest-insertion/), which first picks the city closest to the cycle and then its position.

## Example

The six cities of the nearest insertion page lie in the plane with the Manhattan distance: $A(0,0)$, $B(2,0)$, $C(5,1)$, $D(4,4)$, $E(1,3)$ and $F(6,3)$. The run starts at $A$, and ties go to the earlier city and the earlier position.

| step | city added | increase | $a_t$, the distance to the cycle | cycle | cost |
|---|---|---|---|---|---|
| 1 | $B$ | 4 | 2 | $A\,B$ | 4 |
| 2 | $E$ | 6 | 4 | $A\,E\,B$ | 10 |
| 3 | $C$ | 6 | 4 | $A\,E\,C\,B$ | 16 |
| 4 | $D$ | 2 | 3 | $A\,E\,D\,C\,B$ | 18 |
| 5 | $F$ | 2 | 3 | $A\,E\,D\,F\,C\,B$ | 20 |

At step 2 both $C$ and $E$ are at distance 4 from the cycle $A\,B$, but $E$ costs $4 + 4 - 2 = 6$ and $C$ costs $6 + 4 - 2 = 8$, so the run takes $E$. Nearest insertion took $C$ here. Each increase is at most $2 a_t$, and the values $a_t$ sum to $2 + 4 + 4 + 3 + 3 = 16$, the cost of a minimum spanning tree. Here ALG $= 20 =$ OPT.

## Correctness

**Theorem (Rosenkrantz, Stearns and Lewis 1977).** For metric costs, cheapest insertion returns a tour with ALG $\le 2\,c(T) \le 2(1 - 1/n) \cdot \text{OPT}$, where $T$ is a minimum spanning tree. The bound holds for each start city and each tie rule.

Let $S_t$ be the set of cities in the cycle after $t - 1$ steps and $a_t = d(S_t, V \setminus S_t)$, the least cost of an edge out of $S_t$. The proof has three steps.

1. **One step costs at most $2 a_t$.** Let $u \in S_t$ and $k \notin S_t$ with $d(u, k) = a_t$. To put $k$ right after $u$ costs at most $2\,d(u, k)$ by the triangle inequality, and the cheapest pair costs at most this.
2. **The cut values sum to at most $c(T)$.** This holds for each nested chain $S_1 \subset \cdots \subset S_n$, not only for Prim's order. For each threshold $x$, the steps with $a_t > x$ cut $V$ along components of the graph of edges of cost at most $x$, so there are at most as many of them as edges of $T$ of cost more than $x$. Integration over $x$ gives $\sum_t a_t \le c(T)$.
3. **The lower bound on OPT.** $c(T) \le (1 - 1/n) \cdot \text{OPT}$, the [MST lower bound](/mst-lower-bound-for-tsp/).

The full proof is in the proof file.

**Tightness.** On the cycle graph $C_n$ with unit edges, $n \ge 6$ even and $h = n/2 - 1$, add the cities $1, \ldots, n - 1$ in this order: city $k$ goes right after city 0 when $k \le h$ or $k = n - 1$, and right after city $h$ otherwise. At each step each pair costs at least 2 and the chosen pair costs exactly 2. So ALG $= 2(n - 1)$, OPT $= n$, and ALG/OPT $= 2(1 - 1/n)$. The ties go against the algorithm. This is the same family as for nearest insertion.

**Hardness.** The ratio 2 is a property of this rule. [Christofides' algorithm](/christofides-algorithm/) gets 3/2, and no polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **The plain version.** Step $t$ looks at $(n - t)\,t$ pairs, so the total is $\sum_t (n - t)\,t = \Theta(n^3)$ time in the [word RAM](/word-ram/), with $\Theta(n)$ extra space.
- **A faster version.** Keep, for each city outside the cycle, its cheapest position. An insertion of $k$ between $a$ and $b$ removes one edge and adds two, so most of these values change only by a comparison with the two new edges; the cities whose best edge was $(a, b)$ need a new scan. With a priority queue over the cities, Rosenkrantz, Stearns and Lewis give $O(n^2 \log n)$ time.
- **Compared to nearest insertion.** Nearest insertion takes $\Theta(n^2)$ time and has the same worst-case bound.

## Properties

- **Deterministic.** With fixed tie rules, the output depends only on the input.
- **A certificate in each run.** The run can compute the values $a_t$ in the same loop; their sum is a lower bound on OPT by Lemma 2 and the MST bound, so ALG$/\sum_t a_t$ bounds the ratio of this tour.
- **The order is not Prim's order.** Unlike nearest insertion, the chain $S_t$ is not the order of a tree algorithm, as step 2 of the example shows. The proof needs the stronger Lemma 2 for this reason.
- **Each step is cheapest, the tour need not be.** In the tight family each step is a cheapest pair, and the tour still costs $2(1 - 1/n) \cdot \text{OPT}$.

## Variants and improvements

- **[Nearest insertion](/nearest-insertion/).** The same bound in $\Theta(n^2)$ time.
- **[Farthest insertion](/farthest-insertion/).** Take the city farthest from the cycle, at its cheapest position. It often gives better tours, but no constant bound is proved.
- **Arbitrary and random insertion.** Any selection rule with the cheapest position gives a ratio at most $\lceil \lg n \rceil + 1$ (Rosenkrantz, Stearns and Lewis). Azar (1994) gives lower bounds that grow with $n$ for arbitrary insertion.
- **Convex hull start.** For points in the plane, start from the convex hull instead of one city and then insert by the cheapest pair. The proof above does not cover this variant, because the first cycle is not built by insertions.
- **Local search after.** [Or-opt](/or-opt/) moves short segments to their cheapest positions, which is the same move as an insertion applied to a finished tour.

## When to use it

Use cheapest insertion when you need the factor 2 and good tours on small instances, and the cubic time is no problem. For large instances, use nearest insertion, which has the same bound, or the [greedy edge heuristic](/greedy-edge-heuristic/), which has no constant bound but is fast. For a better bound, use Christofides' algorithm, and for better tours, use a local search such as [2-opt](/two-opt/) after the construction.

## Pitfalls

- **The two-city cycle.** The cycle $s, k$ uses the edge $sk$ two times. With a third city $v$, both positions of the two-city cycle are the same edge, and each costs $d(s, v) + d(v, k) - d(s, k)$.
- **Stale best positions.** In the faster version, an insertion removes the edge $(a, b)$. Each outside city whose best position was $(a, b)$ needs a full new scan; a check of only the two new edges gives wrong choices.
- **Non-metric costs.** Step 1 of the proof needs the triangle inequality. The greedy choice itself gives no bound.
- **Floating point ties.** With real coordinates, two pairs can have the same increase up to rounding. A fixed tie rule on exact values keeps the run reproducible across machines.

## Implementations

## History

Cheapest insertion is one of the classical construction rules from the 1960s and 1970s. Rosenkrantz, Stearns and Lewis (1977) proved the ratio 2 for it and for nearest insertion, and gave instances close to 2. Azar (1994) gave lower bounds for the methods with other selection rules, and they show that the bound 2 does not hold for all insertion orders.

## References
