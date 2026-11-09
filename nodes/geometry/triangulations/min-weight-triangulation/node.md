---
tag: KQ1JFN
kind: problem
slug: min-weight-triangulation
name: Minimum-weight triangulation
aliases:
- Minimum weight triangulation (MWT)
- MWT
- optimal triangulation
area: geometry/triangulations
level: advanced
summary: Find a triangulation of a point set minimising total edge length; NP-hard.
model: real-ram
prereqs: [triangulation-of-point-set, polygon-triangulation-dp, greedy-triangulation]
see_also: [optimal-polygon-triangulation, delaunay-triangulation, minimum-steiner-triangulation, flip-graph, euclidean-minimum-spanning-tree, max-min-angle-triangulation, interval-dp, number-of-triangulations]
sources:
  - paper: doi:10.1145/1346330.1346336
    title: Wolfgang Mulzer and Günter Rote, Minimum-weight triangulation is NP-hard, Journal of the ACM 55(2), article 11 (2008)
    locator: the reduction from planar 1-in-3 satisfiability with wire, variable and clause gadgets
  - paper: "Peter D. Gilbert, New results in planar triangulations, report R-850, Coordinated Science Laboratory, University of Illinois at Urbana-Champaign (1979)"
    locator: the O(n^3) dynamic program for simple polygons (report number to be checked)
  - paper: "G. T. Klincsek, Minimal triangulations of polygonal domains, Annals of Discrete Mathematics 9, 121 to 123 (1980)"
    locator: the O(n^3) dynamic program for polygons
  - paper: "Christos Levcopoulos and Drago Krznaric, Quasi-greedy triangulations approximating the minimum weight triangulation, Journal of Algorithms 27(2), 303 to 338 (1998)"
    locator: the first constant-factor approximation in O(n log n) time
  - paper: "Jan Remy and Angelika Steger, A quasi-polynomial time approximation scheme for minimum weight triangulation, Journal of the ACM 56(3), article 15 (2009)"
    locator: the QPTAS
  - paper: "Glenn K. Manacher and Albert L. Zobrist, Neither the greedy nor the Delaunay triangulation of a planar point set approximates the optimal triangulation, Information Processing Letters 9(1), 31 to 34 (1979)"
    locator: the lower bounds on the ratio for the two heuristics
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1 or 2 exercises on minimum weight triangulations of polygons (exercise numbers to be checked)
---

The minimum weight triangulation (MWT) of a finite point set in the plane is a [triangulation](/triangulation-of-point-set/) whose total edge length is as small as possible. It was one of the long-standing open problems in Garey and Johnson's list of problems of unknown complexity, until Mulzer and Rote proved in 2006 that it is NP-hard. For the vertices of a simple polygon, with only diagonals allowed, the problem is easy: an $O(n^3)$ [dynamic program](/polygon-triangulation-dp/) solves it exactly. The obvious heuristics, the [greedy](/greedy-triangulation/) and the [Delaunay triangulation](/delaunay-triangulation/), can be far from optimal, but a constant-factor approximation and a quasi-polynomial approximation scheme exist.

## In plain words

You have dots on a sheet and want to connect them into triangles while using as little ink as possible: the sum of the lengths of all lines should be smallest. For dots around the edge of a shape with no dots inside, a computer can try all the ways cleverly, piece by piece, and find the best quickly. For dots scattered everywhere, no fast exact method is known, and the problem is as hard as the hardest search problems. Simple rules, such as always taking the shortest line next, can waste a lot of ink.

## Definition

**Input.** A set $S$ of $n$ points in the plane.

**Output.** A triangulation $T$ of $S$ minimizing the **weight** $w(T) = \sum_{pq \in T} |pq|$, the sum of the Euclidean lengths of its edges.

All triangulations of $S$ share the edges of the convex hull, so minimizing the total length is the same as minimizing the length of the interior edges. The decision version asks whether $w(T) \le K$ for some triangulation; it is not known to be in NP, because comparing sums of square roots exactly is not known to be possible in polynomial time.

## Variants

- **Simple polygons.** Triangulate a simple polygon by diagonals with minimum total length. Solved in $O(n^3)$ time by the [polygon triangulation DP](/polygon-triangulation-dp/), for any weight function of the triangles, not only length; see [optimal polygon triangulation](/optimal-polygon-triangulation/).
- **Convex polygons.** The same DP, with every pair a diagonal. Whether $O(n^3)$ can be improved for the length weight is open; for special weights such as matrix chain costs, $O(n \log n)$ is known.
- **Few inner points.** If only $k$ points lie strictly inside the hull, the problem is fixed-parameter tractable in $k$ (Hoffmann and Okamoto; bound to be checked).
- **Steiner points allowed.** The minimum weight Steiner triangulation may add points; it can be much lighter, and its complexity is open. See [minimum Steiner triangulation](/minimum-steiner-triangulation/), which counts triangles instead.
- **Other weights.** Minimizing the largest edge length is solved in $O(n^2)$ time by Edelsbrunner and Tan, and maximizing the smallest angle is solved by the Delaunay triangulation; see [max-min angle triangulation](/max-min-angle-triangulation/).

## Examples

- **A convex quadrilateral.** The MWT uses the shorter diagonal.
- **Greedy is not optimal.** For $p_0 = (0,4)$, $p_1 = (1,8)$, $p_2 = (3,0)$, $p_3 = (1,7)$, $p_4 = (6,0)$ there are 3 triangulations. The MWT uses the interior edges $p_0 p_3$, $p_1 p_3$, $p_1 p_2$, $p_2 p_3$, with total weight about $41.25$. The [greedy triangulation](/greedy-triangulation/) takes the slightly shorter $p_0 p_4$ first and ends with $p_0 p_3$, $p_1 p_3$, $p_0 p_4$, $p_3 p_4$ and weight about $41.53$.
- **A polygon.** For the notched rectangle $(0,0)$, $(6,0)$, $(6,4)$, $(4,4)$, $(3,1)$, $(2,4)$, $(0,4)$ the DP finds the four diagonals from the notch vertex $(3,1)$ to $(0,0)$, $(6,0)$, $(6,4)$ and $(0,4)$, of total length $2\sqrt{10} + 6\sqrt{2} \approx 14.81$, among the 4 triangulations of the polygon.
- **Delaunay is not optimal.** Kirkpatrick gave point sets on which the Delaunay triangulation weighs $\Omega(n)$ times the minimum: thin triangles are cheap, and the Delaunay triangulation avoids them.

## Known algorithms

| method | guarantee | time |
|---|---|---|
| polygon DP (Gilbert; Klincsek) | exact, simple polygons | $O(n^3)$ |
| [greedy triangulation](/greedy-triangulation/) | $\Theta(\sqrt{n})$ times optimal in the worst case; $O(1)$ for convex polygons | $O(n \log n)$ |
| Delaunay triangulation | $\Omega(n)$ times optimal in the worst case | $O(n \log n)$ |
| Plaisted and Hong | $O(\log n)$ times optimal | polynomial |
| quasi-greedy (Levcopoulos and Krznaric) | $O(1)$ times optimal | $O(n \log n)$ |
| Remy and Steger | $1 + \varepsilon$ for every $\varepsilon > 0$ | $n^{O(\log^8 n)}$ (to be checked) |
| LMT-skeleton plus DP on the gaps | exact when the skeleton is connected | fast in practice on random points |

**Exact methods in practice.** Some edges are provably in every MWT: the edges of the $\beta$-skeleton for $\beta \ge \sqrt{2}$ (Keil), and the edges certified by the LMT-skeleton heuristic of Dickerson and Montague. On random points these edges almost always form a connected graph, and the remaining polygonal holes are filled by the polygon DP. This solves instances with millions of points exactly, even though the problem is NP-hard.

## Bounds

- **Hardness.** NP-hard (Mulzer and Rote, 2006 conference version, 2008 journal version). The proof reduces planar 1-in-3 satisfiability with gadgets whose correctness is checked by computer, with exact arithmetic over the square roots of the gadget coordinates.
- **Membership in NP.** Open, as for other problems whose objective is a sum of square roots.
- **Approximation.** A quasi-polynomial time approximation scheme exists, so the problem is not APX-hard unless NP has quasi-polynomial algorithms. Whether a polynomial time approximation scheme exists is open.
- **Polygons.** $O(n^3)$ time and $O(n^2)$ space; no subcubic algorithm is known for the length weight.

## Reductions

- **From planar 1-in-3 SAT.** Mulzer and Rote build wires from clusters of points whose MWT has exactly two light states, and join them in clause gadgets so that a light triangulation exists if and only if the formula is satisfiable.
- **To the polygon DP.** Any set of edges known to lie in some MWT, if it cuts the hull into simple polygons, reduces the rest of the problem to independent polygon DPs.

## Applications

- **Terrain and surface reconstruction.** Short edges were thought to give good interpolation; this motivated the problem in the 1970s, though the Delaunay triangulation is preferred today.
- **Optimal polygon triangulation.** The polygon DP is the textbook example of interval dynamic programming, close to matrix chain multiplication; see [interval DP](/interval-dp/).
- **Benchmarks for exact optimization.** The MWT of large random point sets is a standard test case for combining structural pruning with dynamic programming.

## References
