---
tag: 56Q4XY
kind: algorithm
slug: karp-partitioning-tsp
name: Karp's partitioning algorithm for Euclidean TSP
aliases:
- Karp partitioning scheme
area: approximation/tsp-approximation
level: advanced
summary: Cuts the square into cells, solves each cell exactly and joins the cell tours; the error is additive O(kL), so on random points the ratio goes to 1 as the cells grow.
solves: [euclidean-tsp]
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of cells on one side, t: the most points in one cell}
  time: {worst: O(k^2 + n t 2^t)}
  space: {extra: O(n + t 2^t)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1977
  people: [Richard M. Karp, Jillian Beardwood, John H. Halton, John M. Hammersley]
  note: Karp proved that the scheme is within 1 + ε of OPT almost surely on random points, using the law of Beardwood, Halton and Hammersley (1959).
prereqs: [euclidean-tsp, held-karp-algorithm, eulerian-circuit, triangle-inequality]
see_also: [space-filling-curve-tsp, arora-euclidean-tsp-ptas, mitchell-euclidean-tsp-ptas, quadtree, kd-tree, law-of-large-numbers, christofides-algorithm]
sources:
  - paper: doi:10.1287/moor.2.3.209
    title: Richard M. Karp, Probabilistic analysis of partitioning algorithms for the traveling-salesman problem in the plane, Mathematics of Operations Research 2(3), 1977
    locator: pages 209 to 224 (the partitioning scheme, the cell lemma and the almost sure bound)
  - paper: doi:10.1017/S0305004100034095
    title: Jillian Beardwood, John H. Halton and John M. Hammersley, The shortest path through many points, Proceedings of the Cambridge Philosophical Society 55(4), 1959
    locator: pages 299 to 327 (the limit OPT / sqrt(n) to a constant almost surely)
  - title: J. Michael Steele, Probability Theory and Combinatorial Optimization, SIAM, 1997
    locator: Chapter 2 (the BHH theorem and partitioning)
---

Karp's partitioning scheme is a divide and conquer method for the [Euclidean TSP](/euclidean-tsp/). It cuts the square that holds the points into small cells, finds an optimal tour of the points in each cell by the [Held-Karp dynamic program](/held-karp-algorithm/), and joins the cell tours into one tour. The error is additive: it is at most a constant times the total length of the cell boundaries, and it does not depend on the points. On random uniform points, OPT grows like $\sqrt{n}$, so with cells of $t$ points the relative error is of order $1/\sqrt{t}$. Karp (1977) used this to show that, for each $\varepsilon > 0$, a polynomial algorithm gives a tour within $1 + \varepsilon$ of OPT almost surely as $n$ grows.

## In plain words

Cut the map into a grid of small squares. In each small square there are only a few cities, so you can find the best trip through them by trying all possibilities in a clever way.

Then join the small trips. Go through the squares row by row, like a snake, and from the end of one small trip go to the start of the next.

Where does the extra cost come from? Only from the borders of the squares. A best trip that crosses a border can be repaired along that border, and the joins run along the snake. So the extra cost is at most a fixed multiple of the total border length.

For many random cities the best trip is long, and the border cost is small next to it. So the trip is almost the best.

## The problem

The input is a set $S$ of $n$ points in the plane with the Euclidean distance. The output is a tour of all points. OPT is the length of a shortest tour and ALG is the length of the returned tour. The convention for a minimization problem is ALG $\le \rho \cdot$ OPT. The bound on this page is not a ratio: it is an additive worst-case bound ALG $\le$ OPT $+ c \cdot kL$ for each instance, where $L$ is the side of the bounding square. The ratio near 1 is an almost sure statement for random points.

## The algorithm

This page uses a fixed $k \times k$ grid, which is the simplest form of the scheme. Karp's own form cuts at medians, alternately in $x$ and in $y$, until each cell holds at most $t$ points.

```pseudo id=main
KARP-PARTITION(S, k)
L1  cut the bounding square of S into k × k half-open cells, and put each point in its cell
L2  for each nonempty cell C, in snake order (left to right in even rows, right to left in odd rows) do
L3      T_C ← an optimal tour of S ∩ C, by the Held-Karp dynamic program
L4      cut T_C open before a point p_C, and append the path from p_C to the tour so far
L5  return the tour, closed from its last point to its first point
```

Any choice of $p_C$ in line L4 keeps the bound. The implementation takes the point of $C$ that is nearest to the end of the tour so far. It refuses a cell with more points than a fixed limit, because the time of line L3 is exponential in the size of the cell.

## Example

Take the six cities $A(0,0)$, $B(2,0)$, $C(5,1)$, $D(4,4)$, $E(1,3)$ and $F(6,3)$ of the [nearest insertion](/nearest-insertion/) page, with the Euclidean distance, and $k = 2$. The bounding square is $[0, 6]^2$, so the cells have side 3.

| cell | points | position in the snake |
|---|---|---|
| lower left | $A$, $B$ | 1 |
| lower right | $C$ | 2 |
| upper right | $D$, $F$ | 3 |
| upper left | $E$ | 4 |

The first cell gives the path $A\,B$. The second cell adds $C$. In the third cell, $F$ is nearer to $C$ than $D$, so the path is $F\,D$. The last cell adds $E$. The tour is $A\,B\,C\,F\,D\,E$, of length $2 + \sqrt{10} + \sqrt{5} + \sqrt{5} + \sqrt{10} + \sqrt{10} \approx 15.959$, which is OPT here. On small inputs the additive bound of the theorem is much larger than OPT, so it says nothing; the scheme is meant for large $n$.

**Measured behavior.** On 1000 seeded uniform points in the unit square with $k = 18$, so about 3 points in each cell, the tour has length about $1.04 \sqrt{n}$. On 4000 points with $k = 37$ it is about $1.019 \sqrt{n}$. For comparison, OPT is about $0.7124 \sqrt{n}$ for large $n$ (a numerical estimate of the BHH constant), and a little more for these $n$ because of the boundary. So with the small cells that an exact solver in Python allows, the joins cost much, and the tour is far from OPT. The ratio goes to 1 only when the cells hold many points. These are measured values, not bounds.

## Correctness

**Theorem.** For each point set with bounding square of side $L$ and each $k \ge 1$,

$$\text{OPT} \le \text{ALG} \le \text{OPT} + \left((7 + \sqrt{2})\, k + \sqrt{2}\right) L.$$

For $k = 1$ the tour is optimal. The proof has three steps.

1. **The cell lemma.** For a cell $C$, let $\lambda(C)$ be the length of the part of an optimal tour inside $C$. Then $\text{OPT}(S \cap C) \le \lambda(C) + \frac{3}{2}\operatorname{per}(C)$: add the whole boundary of $C$ and the cheaper half of its arcs between the crossing points, which makes all degrees even, and take shortcuts on an [Eulerian circuit](/eulerian-circuit/). Over all cells the $\lambda(C)$ add up to OPT, and the perimeters add up to at most $4kL$.
2. **The join.** Leaving out the edge before $p_C$ and jumping to the next cell costs, by the triangle inequality, at most the distance between the points $p_C$ of consecutive cells.
3. **The snake.** Consecutive cells in snake order are neighbors, so these distances add up to at most $(1 + \sqrt{2})\, kL + \sqrt{2}\, L$.

The full proof is in the proof file.

**Random points.** Let the points be uniform in the unit square. By the theorem of Beardwood, Halton and Hammersley (1959), $\text{OPT}/\sqrt{n} \to \beta$ almost surely. With $k$ near $\sqrt{n/t}$, the additive error is of order $\sqrt{n/t}$, so the ratio is $1 + O(1/\sqrt{t})$. Karp (1977) proved that, for each $\varepsilon > 0$, his scheme with a fixed $t$ gives ALG $\le (1 + \varepsilon) \cdot$ OPT almost surely as $n \to \infty$. That theorem is quoted; the proof file gives the argument for the grid form as a sketch.

**No worst-case ratio.** The bound is additive. If the points lie in clusters, OPT can be much smaller than $kL$, and then the theorem gives no constant ratio. So this is not an approximation algorithm in the worst-case sense. For a worst-case $1 + \varepsilon$ guarantee in the plane, use [Arora's PTAS](/arora-euclidean-tsp-ptas/) or [Mitchell's PTAS](/mitchell-euclidean-tsp-ptas/).

**Hardness.** Euclidean TSP is NP-hard (Papadimitriou 1977), so the cells must stay small for polynomial time. For [metric TSP](/metric-tsp/), no polynomial algorithm has a ratio below $123/122$ unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). Without the triangle inequality no constant ratio is possible unless P = NP ([general TSP inapproximability](/general-tsp-inapproximability/)).

## Complexity

- **Cells.** Line L1 costs $O(n + k^2)$, and the snake order of line L2 costs $O(k^2)$.
- **Exact cell tours.** The Held-Karp program costs $O(t_C^2\, 2^{t_C})$ for a cell with $t_C$ points. With at most $t$ points in each cell this is $O(n\, t\, 2^t)$ in total, and $O(t\, 2^t)$ space for one cell at a time.
- **The join.** Line L4 costs $O(t_C)$ for each cell.
- **Karp's form.** The median cuts cost $O(n \log n)$, and each cell holds at most $t$ points, so the total is $O(n \log n + n\, t\, 2^t)$, polynomial for $t = O(\log n)$.

The model is the [real RAM](/real-ram/) with the floor function for the cells.

## Properties

- **Deterministic.** The analysis for random points is about the input, not about random choices in the algorithm.
- **Additive error.** The error depends only on the cells, not on the points.
- **Exact on one cell.** With $k = 1$ it is the Held-Karp algorithm.
- **Parallel.** The cells are independent until the join.

## Variants and improvements

- **Median cuts.** Karp's form cuts each rectangle at the median point, so the cells have at most $t$ points each, and the time is fixed for a fixed $t$.
- **Better cell solvers.** Use a heuristic in each cell, for example [Lin-Kernighan](/lin-kernighan/), and allow large cells. The cell lemma then holds with the cost of the heuristic.
- **Better joins.** Improve the joined tour with [2-opt](/two-opt/) or [Or-opt](/or-opt/) moves near the cell borders.
- **Fixed dissections with a guarantee.** [Arora's PTAS](/arora-euclidean-tsp-ptas/) also cuts the square into cells, but it controls the crossings of the borders with portals and a random shift, and this gives a worst-case $1 + \varepsilon$.
- **Space-filling curves.** The [space-filling curve heuristic](/space-filling-curve-tsp/) orders the cells by a curve and does no exact work.

## When to use it

Use partitioning on very large uniform instances, where each part can be solved well and in parallel. Use it to explain why random Euclidean instances are easier than the worst case. Do not use it on clustered points, where the borders cost much compared to OPT.

## Pitfalls

- **Cell sizes.** A fixed grid can put many points in one cell. The exact solver then takes too long. Cut at medians, or limit the cell size.
- **Additive, not relative.** The bound $O(kL)$ is not a ratio. Do not quote it as a constant factor.
- **Almost sure, not worst case.** Karp's $1 + \varepsilon$ holds with probability 1 for random points as $n$ grows, not for each input.
- **The boundary term.** For finite $n$, OPT$/\sqrt{n}$ in the unit square is larger than $\beta$, because of the points near the boundary.

## Implementations

## History

Beardwood, Halton and Hammersley (1959) proved that the length of an optimal tour through $n$ random points in a region of area $A$ is $\beta \sqrt{nA}$ to first order, almost surely. Karp (1977) used this to analyze partitioning: the cell lemma bounds the error by the boundary length, and so the scheme is within $1 + \varepsilon$ of OPT almost surely. This was one of the first probabilistic analyses of an approximation algorithm, and it showed that random Euclidean TSP instances are easy to approximate long before Arora (1996) and Mitchell (1996) gave worst-case schemes.

## References
