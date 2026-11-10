---
tag: CF8E6R
kind: algorithm
slug: space-filling-curve-tsp
name: Space-filling curve heuristic for Euclidean TSP
aliases:
- Platzman-Bartholdi heuristic
area: approximation/tsp-approximation
level: intro
summary: Sorts the points by their position on a space-filling curve and visits them in that order; O(n log n) time and a worst-case ratio of order log n.
solves: [euclidean-tsp]
model: word-ram
complexity:
  vars: {n: the number of points}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1982
  people: [John J. Bartholdi III, Loren K. Platzman, Dimitris Bertsimas, Michelangelo Grigni]
  note: Bartholdi and Platzman used the Sierpinski curve for routing; Platzman and Bartholdi (1989) proved the O(log n) ratio, and Bertsimas and Grigni (1989) showed that the order log n is reached.
prereqs: [euclidean-tsp, space-filling-curve, hilbert-curve, quadtree]
see_also: [nearest-neighbor-tsp, karp-partitioning-tsp, arora-euclidean-tsp-ptas, z-order-curve, christofides-algorithm, two-opt]
sources:
  - paper: doi:10.1145/76359.76361
    title: Loren K. Platzman and John J. Bartholdi III, Spacefilling curves and the planar travelling salesman problem, Journal of the ACM 36(4), 1989
    locator: pages 719 to 737 (the O(log n) worst-case ratio and the average-case analysis for the Sierpinski curve)
  - title: John J. Bartholdi III and Loren K. Platzman, An O(N log N) planar travelling salesman heuristic based on spacefilling curves, Operations Research Letters 1(4), 1982
    locator: pages 121 to 125 (the heuristic)
  - title: Dimitris Bertsimas and Michelangelo Grigni, Worst-case examples for the spacefilling curve heuristic for the Euclidean traveling salesman problem, Operations Research Letters 8(5), 1989
    locator: pages 241 to 244 (point sets with ratio of order log n)
---

The space-filling curve heuristic builds a tour for the [Euclidean TSP](/euclidean-tsp/) without looking at any distance. It lays a [space-filling curve](/space-filling-curve/) over the square that holds the points, finds the position of each point on the curve, and visits the points in the order of these positions. The work is one sort, so the time is $O(n \log n)$, and the tour of a set of points can be updated by one insertion when a point is added. The worst-case ratio to OPT is of order $\log n$. On random uniform points the tour is a constant factor above OPT.

## In plain words

Draw one long line that winds through every small square of a map, and never crosses itself. The [Hilbert curve](/hilbert-curve/) is such a line. It fills one quarter of the map first, then the next quarter, and so on, and inside each quarter it does the same on a smaller scale.

Now walk along this line and visit the cities in the order that the line meets them. Cities that are close on the line are close on the map.

The rule is fast. It needs only one sort, and it never measures a distance. The price is that the reverse is false: two cities that are close on the map can be far apart on the line. Then the walk goes away and comes back later, and this can cost a logarithmic factor.

## The problem

The input is a set $P$ of $n$ points in the plane with the Euclidean distance. The output is a tour of all points, and its length includes the closing edge. OPT is the length of a shortest tour and ALG is the length of the returned tour. The convention is ALG $\le \rho \cdot$ OPT for a minimization problem. The bound on this page is a worst-case bound for each point set; the average-case values for random points are given separately.

## The algorithm

The implementation uses the Hilbert curve. Platzman and Bartholdi used the Sierpinski curve, which is a curve of the same kind on triangles.

```pseudo id=main
SPACE-FILLING-CURVE-TOUR(P, r)
L1  put the bounding square of P on a 2^r × 2^r grid; let c(p) be the grid cell of each point p
L2  h(p) ← the position of c(p) on the Hilbert curve of order r, for each point p
L3  sort P by h(p), and by input order for equal h; return this order as the tour
```

Line L2 reads two bits of each coordinate at each of the $r$ levels and turns or mirrors the coordinates for the next level, so it costs $O(r)$ word operations. The proof needs $2^r \ge n$. The implementation uses $r = 24$ by default.

## Example

Take the six cities $A(0,0)$, $B(2,0)$, $C(5,1)$, $D(4,4)$, $E(1,3)$ and $F(6,3)$ of the [nearest insertion](/nearest-insertion/) page, now with the Euclidean distance. Put them on the $8 \times 8$ grid of the square $[0, 8]^2$, with $r = 3$, so each city is in the cell of its two coordinates.

| city | cell | Hilbert position |
|---|---|---|
| $A$ | (0, 0) | 0 |
| $B$ | (2, 0) | 4 |
| $E$ | (1, 3) | 12 |
| $D$ | (4, 4) | 32 |
| $F$ | (6, 3) | 51 |
| $C$ | (5, 1) | 56 |

The tour is $A\,B\,E\,D\,F\,C$. Its edges have lengths $2$, $\sqrt{10}$, $\sqrt{10}$, $\sqrt{5}$, $\sqrt{5}$ and $\sqrt{26}$, so ALG $\approx 17.896$. OPT $\approx 15.959$, so the ratio is about 1.121. The curve visits the left half first, so it goes from $B$ up to $E$ and leaves $C$, which is near $B$, to the end.

**Measured behavior.** On 300 seeded instances of 10 uniform random points in the unit square, the Hilbert tour was on average 11.89 percent above OPT, and at most 1.505 times OPT. On the same instances the [nearest-neighbor tour](/nearest-neighbor-tsp/) was 10.4 percent above OPT. Platzman and Bartholdi report that for many uniform random points the Sierpinski tour is about 25 percent longer than OPT. For $n = 2^M$ points on one row of the grid, at the height $2/3$ of the square, the measured ratio of the Hilbert tour grows from 1.0 at $M = 2$ to 2.822 at $M = 10$, about 0.23 for each doubling of $n$. These are measured values, not bounds.

## Correctness

**Theorem.** For $n \ge 2$ points and a grid with $2^r \ge n$, the Hilbert curve tour satisfies

$$\text{ALG} \le \left(9\sqrt{2}\,\lceil \lg n \rceil + \sqrt{2}\right) \cdot \text{OPT}.$$

Platzman and Bartholdi (1989) proved a bound of order $\log n$ for the Sierpinski curve. The theorem on this page is the same order for the Hilbert curve, with a constant that is easy to check and not the best one. Scale the points so that their bounding square has side 1. The proof has three steps.

1. **Nesting.** The curve visits all cells of each dyadic square, of each level $k$, at consecutive positions. So two consecutive points whose smallest common dyadic square has level $k$ are at distance at most $\sqrt{2} \cdot 2^{-k}$, and there are at most $m_{k+1} - 1$ such pairs, where $m_{k+1}$ is the number of nonempty squares at level $k + 1$.
2. **A lower bound at each level.** Color the squares of level $k + 1$ with 9 colors by their row and column modulo 3. Points in different squares of one color are at distance at least twice the side, so OPT is at least $2/9$ of $m_{k+1}$ times the side. Each of the levels $0$ to $\lceil \lg n \rceil - 1$ then costs at most $9 \sqrt{2} \cdot \text{OPT}$.
3. **Deep levels.** The at most $n - 1$ edges at the deeper levels are each at most $\sqrt{2}/n$, and the closing edge is at most $\sqrt{2}$. Together they are below $\sqrt{2} \cdot \text{OPT}$, since OPT $\ge 2$.

The full proof is in the proof file.

**Lower bounds.** Bertsimas and Grigni (1989) gave point sets on which the Sierpinski curve tour is $\Omega(\log n)$ times OPT, so the order $\log n$ cannot be improved for that curve. That result is quoted here. For the Hilbert curve, the test file measures the row family above, whose ratio grows with $\log n$; this is a measured trend, not a proof.

**Hardness.** Euclidean TSP is NP-hard (Papadimitriou 1977), but unlike [metric TSP](/metric-tsp/) it has a [PTAS](/ptas/): see [Arora's scheme](/arora-euclidean-tsp-ptas/) and [Mitchell's scheme](/mitchell-euclidean-tsp-ptas/). For metric TSP, no polynomial algorithm has a ratio below $123/122$ unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **Cells and positions.** Lines L1 and L2 cost $O(r)$ word operations for each point, $O(nr)$ in total. With $r = \lceil \lg n \rceil$, the grid is fine enough for the theorem, and this is $O(n \log n)$.
- **Sort.** Line L3 is one comparison sort, $\Theta(n \log n)$ in the worst case. With integer keys of $2r$ bits, a radix sort gives $O(n)$ for fixed $r$.
- **Space.** $\Theta(n)$ for the keys and the order.

The model is the [word RAM](/word-ram/) with coordinates and keys in $O(1)$ words. Line L1 needs the floor of a real number, which the plain [real RAM](/real-ram/) does not have.

## Properties

- **Deterministic.** Equal positions keep the input order.
- **No distances.** The rule never computes a distance, so it works for any input that can be put on a grid.
- **Fast updates.** To add or remove a point, insert or delete its key in a sorted structure. The tour changes only near that point. This is why Bartholdi and Platzman used it for routes that change each day.
- **Locality in one direction.** Points close on the curve are close in the plane: the distance is at most about the square root of the curve distance. The reverse is false, and this is the reason for the log factor.
- **Not a local optimum.** The tour often has crossings, and [2-opt](/two-opt/) improves it.

## Variants and improvements

- **Other curves.** The Sierpinski curve, the Hilbert curve and the [Z-order curve](/z-order-curve/) all work, because the proof uses only that each dyadic square is one interval of the curve.
- **Higher dimensions.** The same rule works in $\mathbb{R}^d$ with a $d$-dimensional curve, with the time $O(n \log n)$.
- **Improvement after the sort.** Use the curve tour as the start of [2-opt](/two-opt/), [Or-opt](/or-opt/) or [Lin-Kernighan](/lin-kernighan/).
- **Partitioning.** [Karp's partitioning scheme](/karp-partitioning-tsp/) also cuts the square into cells, but it solves each cell exactly and gets a ratio near 1 on random points.
- **A guaranteed ratio.** For a factor $1 + \varepsilon$, use [Arora's PTAS](/arora-euclidean-tsp-ptas/), which also uses a dyadic subdivision of the square.

## When to use it

Use the space-filling curve heuristic when $n$ is very large, when time or memory is very short, or when points come and go and the tour must be updated fast. Do not use it alone when tour quality matters, because the [nearest-neighbor](/nearest-neighbor-tsp/), greedy and insertion rules give shorter tours. Use it as a fast start for a local search.

## Pitfalls

- **A coarse grid.** If $2^r < n$, many points can share one cell, and their order inside the cell is arbitrary. Use $r \ge \lceil \lg n \rceil$, and more when the points are not spread out.
- **The bounding square, not the bounding box.** Scale both axes by the same factor. If the box is scaled to a square, the curve no longer follows the real distances.
- **Points on the far edge.** A point with $x$ equal to the largest coordinate falls just outside the last cell. Clamp it into the last cell, as the implementation does.
- **Bit order in the curve.** The Hilbert curve needs a turn or a mirror of the coordinates at each level. Code that only interleaves the bits gives the Z-order curve, which is still correct but jumps more.

## Implementations

## History

Bartholdi and Platzman (1982) proposed the heuristic with the Sierpinski curve, and they used it for routes of meals on wheels in Atlanta, where cards were sorted by the curve position. Platzman and Bartholdi (1989) proved the $O(\log n)$ worst-case ratio and studied the average case for uniform random points. Bertsimas and Grigni (1989) showed that the order $\log n$ is reached. The heuristic is now a standard fast start for local search on very large geometric instances.

## References
