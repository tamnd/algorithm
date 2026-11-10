---
tag: F86NNE
kind: algorithm
slug: nearest-insertion
name: Nearest insertion
aliases:
- nearest insertion TSP
area: approximation/tsp-approximation
level: core
summary: Grows a cycle by adding the city closest to it at its cheapest position; the cities come in Prim's order, so the tour costs at most 2(1 − 1/n) OPT on metric instances, and this is tight.
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
  note: Rosenkrantz, Stearns and Lewis proved the ratio 2 for nearest and cheapest insertion by the link to minimum spanning trees.
prereqs: [metric-tsp, triangle-inequality, prim, mst-lower-bound-for-tsp]
see_also: [cheapest-insertion, farthest-insertion, nearest-neighbor-tsp, double-tree-algorithm, christofides-algorithm, or-opt, two-opt]
sources:
  - paper: doi:10.1137/0206041
    title: Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3), 1977
    locator: pages 563 to 581 (the insertion methods, the bound 2 for nearest and cheapest insertion)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.4 (the nearest addition algorithm and its link to Prim's algorithm)
  - title: Yossi Azar, Lower bounds for insertion methods for TSP, Combinatorics, Probability and Computing 3, 1994
    locator: pages 285 to 292 (lower bounds for arbitrary and random insertion)
---

Nearest insertion builds a tour for the [metric TSP](/metric-tsp/). It keeps a cycle through some of the cities, and at each step it adds the city closest to the cycle, at the position where the cycle grows least. The cities come in the order of [Prim's algorithm](/prim/), so the tour costs at most two times a minimum spanning tree, which is at most $2(1 - 1/n) \cdot \text{OPT}$. A family on cycle graphs reaches this bound exactly, and the algorithm runs in $\Theta(n^2)$ time.

## In plain words

You plan a round trip one city at a time. Begin with one city. At each step, look at all cities that are not in the trip yet, and take the one that is closest to some city of the trip. Put it into the trip where it adds the least distance.

The new city is close to some city of the trip, so a detour from that city to the new city and back costs at most two times that short distance. The short distances that you pick are exactly the roads of the cheapest network that connects all cities. The best round trip costs more than that network, so your trip is never worse than two times the best one.

## The problem

The input is a set $V$ of $n$ cities with a cost $d(u, v) = d(v, u) \ge 0$ for each pair, and the costs satisfy the [triangle inequality](/triangle-inequality/). The output is a tour of all cities; its cost includes the closing edge. OPT is the least cost of a tour and ALG is the cost of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. The bound on this page holds for each instance; it is a worst-case bound, not an expected one.

## The algorithm

```pseudo id=main
NEAREST-INSERTION(V, d, s)
L1  H ← the cycle (s)                         ▷ one city, cost 0
L2  for each city v do near[v] ← d(s, v)       ▷ distance from v to the cycle
L3  while H does not hold all cities do
L4      k ← a city not in H with the least near[k]
L5      (a, b) ← an edge of H with the least d(a, k) + d(k, b) − d(a, b)
L6      put k between a and b in H
L7      for each city v do near[v] ← min(near[v], d(k, v))
L8  return H
```

Line L4 is the selection rule, and line L5 is the insertion rule. When $H$ has one city $s$, line L5 makes the cycle $s, k$ of cost $2\,d(s, k)$. The array near is the key array of Prim's algorithm, and line L7 is its update.

## Example

Six cities lie in the plane with the Manhattan distance: $A(0,0)$, $B(2,0)$, $C(5,1)$, $D(4,4)$, $E(1,3)$ and $F(6,3)$. The run starts at $A$, and ties go to the earlier city and the earlier position.

| step | city added | distance to the cycle | increase | cycle | cost |
|---|---|---|---|---|---|
| 1 | $B$ | 2 | 4 | $A\,B$ | 4 |
| 2 | $C$ | 4 | 8 | $A\,C\,B$ | 12 |
| 3 | $F$ | 3 | 6 | $A\,F\,C\,B$ | 18 |
| 4 | $D$ | 3 | 2 | $A\,D\,F\,C\,B$ | 20 |
| 5 | $E$ | 4 | 0 | $A\,E\,D\,F\,C\,B$ | 20 |

At step 5, $E$ lies on a shortest Manhattan path from $A$ to $D$, so it costs nothing. The distances in the third column are $2 + 4 + 3 + 3 + 4 = 16$, the cost of a minimum spanning tree: they are the edges $AB$, $BC$, $CF$, $FD$ and $DE$ that Prim's algorithm picks. The bound is $2 \cdot 16 = 32$, and here ALG $= 20 =$ OPT.

## Correctness

**Theorem (Rosenkrantz, Stearns and Lewis 1977).** For metric costs, nearest insertion returns a tour with ALG $\le 2\,c(T) \le 2(1 - 1/n) \cdot \text{OPT}$, where $T$ is a minimum spanning tree. The bound holds for each start city and each tie rule.

The proof has three steps.

1. **One insertion.** Let $k$ be the new city and $j$ the closest city of the cycle, and let $j'$ follow $j$ on the cycle. To put $k$ between $j$ and $j'$ costs $d(j, k) + d(k, j') - d(j, j') \le 2\,d(j, k)$ by the triangle inequality. The cheapest position costs at most this.
2. **Prim's order.** The distances $d(k, S)$ of the chosen cities are the edges that Prim's algorithm adds, so their sum is $c(T)$. Thus ALG $\le 2\,c(T)$.
3. **The lower bound on OPT.** An optimal tour without its most costly edge is a spanning path, so $c(T) \le (1 - 1/n) \cdot \text{OPT}$. This is the [MST lower bound](/mst-lower-bound-for-tsp/).

The full proof is in the proof file.

**Tightness.** Take the cycle graph $C_n$ with unit edges, $n$ even and at least 6, and its shortest path metric; OPT $= n$. Let $h = n/2 - 1$. Add the cities $1, 2, \ldots, n - 1$ in this order: city $k$ goes right after city 0 when $k \le h$ or $k = n - 1$, and right after city $h$ otherwise. Each step adds a closest city at a cheapest position and raises the cost by 2, so ALG $= 2(n - 1)$ and ALG/OPT $= 2(1 - 1/n)$. The bound of the theorem is exact. The ties in this family go against the algorithm. The proof file proves each step.

**Hardness.** The ratio 2 is a property of this rule. [Christofides' algorithm](/christofides-algorithm/) gets 3/2. No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality, step 1 fails, and no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **Selection.** Lines L4 and L7 scan $n$ cities, so they cost $O(n)$ per step and $\Theta(n^2)$ in total.
- **Insertion.** Line L5 scans the $t$ edges of the cycle, so it costs $O(n)$ per step and $\Theta(n^2)$ in total.
- **Total.** $\Theta(n^2)$ time in the worst case in the [word RAM](/word-ram/), which is linear in the size of the cost matrix, and $\Theta(n)$ extra space.

The cycle is a list, so line L6 costs $O(n)$ for an array insert. A [doubly linked list](/doubly-linked-list/) makes it $O(1)$, but the scan of line L5 keeps the step at $O(n)$.

## Properties

- **Deterministic.** With fixed tie rules, the output depends only on the input.
- **A certificate in each run.** The run computes $c(T)$ in line L4. So ALG$/c(T)$, which is at most 2, bounds the ratio of this tour on this instance.
- **The selection rule carries the proof.** The proof needs the city closest to the cycle, but it does not need the cheapest position: it needs only the position next to the closest city. So the bound 2 holds for each insertion rule that is at least as good as that position.
- **Not a local optimum.** In the plane the tour can have crossing edges. Rosenkrantz, Stearns and Lewis show that their bad tours for this rule can be $k$-optimal for large $k$, so a local search does not always repair them.

## Variants and improvements

- **[Cheapest insertion](/cheapest-insertion/).** Pick the pair of city and position with the least increase. The ratio is also $2(1 - 1/n)$, by a more general form of step 2, but the run is slower.
- **[Farthest insertion](/farthest-insertion/).** Pick the city farthest from the cycle. It often gives better tours in practice, but no constant bound is proved for it.
- **Arbitrary and random insertion.** Any selection rule with the cheapest position gives a ratio at most $\lceil \lg n \rceil + 1$ (Rosenkrantz, Stearns and Lewis). Azar (1994) shows that arbitrary insertion can have a ratio of order $\log \log n / \log \log \log n$, so a constant bound fails for it.
- **Double tree.** The [double-tree algorithm](/double-tree-algorithm/) gets the same bound $2(1 - 1/n)$ from the same tree.

## When to use it

Use nearest insertion when you need a proved factor 2 from a short and simple loop, with no tree and no Euler circuit. It is a good start tour for [Or-opt](/or-opt/) and [2-opt](/two-opt/). If you need only a good tour and no bound, farthest insertion or the [greedy edge heuristic](/greedy-edge-heuristic/) is usually better. If you need a better bound, use Christofides' algorithm.

## Pitfalls

- **Selection by insertion cost.** If line L4 takes the city with the least increase instead of the least distance, the algorithm is cheapest insertion, which is correct but slower. If it takes the city with the least distance to one fixed city, the proof fails.
- **The two-city cycle.** The cycle $s, k$ uses the edge $sk$ two times. Code that treats it as one edge gets the wrong cost and the wrong increases at the next step.
- **Non-metric costs.** Step 1 of the proof needs the triangle inequality. Compute shortest path costs first when the input is a sparse graph.
- **Array inserts.** An insert into the middle of an array costs $O(n)$. This keeps the total $\Theta(n^2)$, but in a variant with a faster line L5 it becomes the bottleneck.

## Implementations

## History

Insertion methods were in use in the 1960s. Rosenkrantz, Stearns and Lewis (1977) gave the first worst-case analysis. They showed the ratio 2 for nearest and cheapest insertion through Prim's algorithm, the bound $\lceil \lg n \rceil + 1$ for any insertion order, and instances where nearest insertion is close to 2. Azar (1994) gave lower bounds for arbitrary and random insertion.

## References
