---
tag: PDEVFT
kind: problem
slug: euclidean-tsp
name: Euclidean TSP
aliases:
- Euclidean traveling salesman problem
- planar Euclidean TSP
- geometric TSP
area: approximation/tsp-approximation
level: advanced
summary: The TSP on n points in the plane or in fixed dimension d with Euclidean distances. It is NP-hard, but unlike metric TSP it has a PTAS (Arora 1998, Mitchell 1999).
prereqs: [metric-tsp, ptas, euclidean-minimum-spanning-tree]
see_also: [arora-euclidean-tsp-ptas, mitchell-euclidean-tsp-ptas, portal-based-dissection, mitchell-guillotine-ptas, karp-partitioning-tsp, space-filling-curve-tsp, two-opt, christofides-algorithm]
sources:
  - paper: doi:10.1016/0304-3975(77)90012-3
    title: Christos H. Papadimitriou, The Euclidean traveling salesman problem is NP-complete, Theoretical Computer Science 4(3), 1977
    locator: pages 237 to 244
  - paper: doi:10.1145/290179.290180
    title: Sanjeev Arora, Polynomial time approximation schemes for Euclidean traveling salesman and other geometric problems, Journal of the ACM 45(5), 1998
    locator: pages 753 to 782
  - title: Joseph S. B. Mitchell, Guillotine subdivisions approximate polygonal subdivisions, a simple polynomial-time approximation scheme for geometric TSP, k-MST, and related problems, SIAM Journal on Computing 28(4), 1999
    locator: pages 1298 to 1309
  - title: Jillian Beardwood, J. H. Halton and John M. Hammersley, The shortest path through many points, Proceedings of the Cambridge Philosophical Society 55(4), 1959
    locator: pages 299 to 327 (the tour length of n random points grows like a constant times the square root of n)
  - title: Alon Itai, Christos H. Papadimitriou and Jayme L. Szwarcfiter, Hamilton paths in grid graphs, SIAM Journal on Computing 11(4), 1982
    locator: pages 676 to 686 (Hamiltonian cycle is NP-complete in grid graphs)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 10, Section 10.1 (the Euclidean TSP and its approximation scheme)
---

The Euclidean TSP is the [metric TSP](/metric-tsp/) on $n$ points in the plane, or in $\mathbb{R}^d$, where the cost of an edge is the straight-line distance. It is NP-hard (Papadimitriou 1977), but the geometry makes it easier to approximate than the general metric case: for each fixed $d$ and each $\varepsilon > 0$ there is a polynomial algorithm with ratio $1 + \varepsilon$, a [PTAS](/ptas/) found by Arora (1998) and by Mitchell (1999). The metric TSP has no PTAS unless P = NP. An optimal Euclidean tour never crosses itself, and for random points its length grows like a constant times $\sqrt{n}$.

## In plain words

Put pins on a flat map and stretch a string from pin to pin, so that it passes each pin once and comes back to the start. The goal is the shortest string. The distance between two pins is the straight line between them.

This is still a hard problem: no fast method is known that always finds the shortest string. But straight-line distances have much structure. A best route never crosses itself, and far-away parts of the map have little effect on each other. With this, a method can cut the map into squares, solve small pieces and glue them, and get a route as close to the shortest as you ask, for example within one percent. The time grows fast when you ask for more precision, but it stays polynomial in the number of pins.

## Definition

**Input.** Points $p_1, \ldots, p_n \in \mathbb{R}^d$, with $n \ge 3$ and $d \ge 2$ fixed. The cost of the pair $(i, j)$ is $c_{ij} = \lVert p_i - p_j \rVert_2$, the Euclidean distance. This cost is a metric, so the problem is a special case of the [metric TSP](/metric-tsp/).

**Output.** A tour: a cyclic order of the $n$ points. Its cost is the sum of the distances between consecutive points.

**Goal.** Minimize the cost. OPT is the least cost, ALG the cost of the returned tour, and a $(1 + \varepsilon)$-approximation returns ALG $\le (1 + \varepsilon) \cdot \text{OPT}$.

**The input model.** Coordinates are rationals or integers. The costs are square roots, so the cost of a tour is a sum of square roots. No polynomial method is known that compares two such sums exactly. For this reason the decision version "is there a tour of cost at most $L$?" is NP-hard but is not known to be in NP. Many papers instead round distances up to integers, or move the points to an integer grid first, as Arora's scheme does.

**No crossings (proved here).** Assume the points are not all on one line. *An optimal tour has no two edges that cross.* Proof: let the tour contain the edges $ab$ and $pq$ in the order $a \to b \to \cdots \to p \to q \to \cdots$, and let the segments cross at an inner point $x$ of both, with the four points not on one line. Replace $ab$ and $pq$ by $ap$ and $bq$ and reverse the part from $b$ to $p$; the result is again one tour (this is a [2-opt](/two-opt/) move). By the triangle inequality, $\lVert a - p \rVert \le \lVert a - x \rVert + \lVert x - p \rVert$ and $\lVert b - q \rVert \le \lVert b - x \rVert + \lVert x - q \rVert$, and the right sides add up to $\lVert a - b \rVert + \lVert p - q \rVert$, because $x$ lies on both segments. Equality in the first inequality would put $p$ on the line through $a$ and $x$, which is the line through $a$ and $b$, and then the two segments are on one line, which is not a proper crossing. So the new tour is strictly shorter, and the old one was not optimal. $\blacksquare$ A standard consequence, by the Jordan curve theorem, is that an optimal tour visits the corners of the [convex hull](/convex-hull/) in their order around the hull.

## Variants

- **Dimension.** For each fixed $d$ the PTAS works, with a running time that grows very fast in $d$. When $d$ grows like $\log n$, the problem is APX-hard (Trevisan 2000), so no PTAS is expected.
- **Other norms.** The rectilinear TSP uses the $\ell_1$ norm (Manhattan distance), and Arora's method also covers other fixed $\ell_p$ norms.
- **Euclidean path TSP and multiple tours.** The same dissection method gives schemes for paths with fixed ends and for several tours from a depot ([vehicle routing](/vehicle-routing-problem/) with small capacities).
- **Related geometric problems.** The [Euclidean Steiner tree problem](/euclidean-steiner-tree-problem/), the $k$-median problem ([Arora's $k$-median scheme](/arora-euclidean-k-median-ptas/)) and the $k$-MST have schemes of the same kind.
- **Random points.** Points chosen uniformly in the unit square. Here the question is the typical value of OPT and fast algorithms that are close to it with high probability, such as [Karp's partitioning](/karp-partitioning-tsp/).
- **Bitonic tours.** Tours that go from left to right and come back. The best [bitonic tour](/bitonic-tsp/) is found exactly by dynamic programming in $O(n^2)$ time, but it can be much longer than OPT.

## Examples

**Four corners of a square.** For $(0,0)$, $(1,0)$, $(1,1)$, $(0,1)$, the tour around the square costs 4, and the tour that takes the two diagonals costs $2 + 2\sqrt{2} \approx 4.828$. The two diagonals cross, and the 2-opt move of the proof turns the second tour into the first.

**Eight points.** The points are $A(0,0)$, $B(4,0)$, $C(6,3)$, $D(3,2)$, $E(5,6)$, $F(1,5)$, $G(2,3)$ and $H(7,1)$. The values were computed by a script, with OPT by trying all tours.

| method | tour | cost | cost / OPT | crossings |
|---|---|---|---|---|
| [Euclidean MST](/euclidean-minimum-spanning-tree/) (a lower bound) | | 18.053 | 0.754 | |
| subtour LP, the [Held-Karp bound](/held-karp-bound/) | integral here | 23.940 | 1 | |
| [double tree](/double-tree-algorithm/) | $A\,D\,B\,C\,E\,H\,G\,F$ | 30.715 | 1.283 | 1 |
| the same, after one uncrossing move | $A\,D\,B\,H\,E\,C\,G\,F$ | 28.886 | 1.207 | 0 |
| [Christofides](/christofides-algorithm/) | $A\,D\,C\,H\,E\,F\,G\,B$ | 28.354 | 1.184 | 1 |
| the same, after one uncrossing move | $A\,G\,F\,E\,H\,C\,D\,B$ | 26.984 | 1.127 | 0 |
| optimal | $A\,B\,H\,C\,E\,F\,G\,D$ | 23.940 | 1 | 0 |

The convex hull is $A, B, H, E, F$, and the optimal tour visits these five points in this order. The two uncrossed tours show that "no crossings" is necessary for optimality but not sufficient.

## Known algorithms

| algorithm | ratio | time | status |
|---|---|---|---|
| [double tree](/double-tree-algorithm/) with the [Euclidean MST](/euclidean-minimum-spanning-tree/) | 2 | $O(n \log n)$ in the plane | proved on that page |
| [Christofides](/christofides-algorithm/) | $3/2$ | dominated by the geometric matching | proved on that page |
| [Arora's PTAS](/arora-euclidean-tsp-ptas/) | $1 + \varepsilon$ | $n (\log n)^{O(1/\varepsilon)}$ in the plane, randomized | cited |
| [Mitchell's PTAS](/mitchell-euclidean-tsp-ptas/) | $1 + \varepsilon$ | $n^{O(1/\varepsilon)}$ in the plane | cited |
| Rao and Smith (1998) | $1 + \varepsilon$ | $2^{(d/\varepsilon)^{O(d)}} n + (d/\varepsilon)^{O(d)} n \log n$ | cited |
| [Karp's partitioning](/karp-partitioning-tsp/) | $1 + \varepsilon$ with high probability on random points | near linear for fixed $\varepsilon$ | cited |
| [space-filling curve](/space-filling-curve-tsp/), [greedy edge](/greedy-edge-heuristic/), [insertion](/farthest-insertion/) | heuristics | $O(n \log n)$ to $O(n^2)$ | fast in practice |
| [2-opt](/two-opt/), [Or-opt](/or-opt/), [Lin-Kernighan](/lin-kernighan/), [LKH](/lin-kernighan-helsgaun/) | local search | per pass | best in practice |
| exact (de Berg, Bodlaender, Kisfaludi-Bak and Kolay 2018) | 1 | $2^{O(\sqrt{n})}$ in the plane | cited |

The schemes of Arora and Mitchell rest on two ideas: [portal-based dissection](/portal-based-dissection/) of a [quadtree](/quadtree/) and [guillotine subdivisions](/mitchell-guillotine-ptas/). Both show that some tour within $1 + \varepsilon$ of OPT crosses each cell boundary only a few times, so a dynamic program over the cells finds it.

## Bounds

**Hardness.** The Euclidean TSP in the plane is NP-hard (Papadimitriou 1977, and independently Garey, Graham and Johnson 1976). A short proof from a cited result: Itai, Papadimitriou and Szwarcfiter (1982) proved that Hamiltonian cycle is NP-complete in *grid graphs*, the induced subgraphs of the integer grid. Take the $n$ vertices of a grid graph as points. Two points are at distance 1 exactly when they are adjacent, and otherwise at distance at least $\sqrt{2}$. So OPT $= n$ if the graph has a Hamiltonian cycle, and OPT $\ge n - 1 + \sqrt{2}$ if not. A $(1 + \varepsilon)$-approximation with $\varepsilon = 0.4/n$ tells the two cases apart, because $(1 + 0.4/n) \cdot n = n + 0.4 < n - 1 + \sqrt{2}$. So an algorithm with time polynomial in $n$ and $1/\varepsilon$ (an FPTAS) would decide Hamiltonian cycle in grid graphs, and no FPTAS exists unless P = NP. $\blacksquare$ A PTAS is therefore the best kind of scheme that the worst case allows in fixed dimension. The exact algorithm of de Berg et al. is tight under the exponential time hypothesis: no $2^{o(\sqrt{n})}$ algorithm exists unless ETH fails.

**Lower bounds on OPT.** The Euclidean MST costs at most $(1 - 1/n) \cdot \text{OPT}$ (see [MST lower bound](/mst-lower-bound-for-tsp/)), and it can be computed in $O(n \log n)$ time in the plane from the [Delaunay triangulation](/delaunay-triangulation/). The [Held-Karp bound](/held-karp-bound/) is closer: on random uniform points it is typically within about one percent of OPT.

**Random points (cited).** Beardwood, Halton and Hammersley (1959) proved that for $n$ points drawn uniformly and independently from a region of area $A$ in the plane, $\text{OPT}/\sqrt{nA}$ tends to a constant $\beta$ with probability 1. The value of $\beta$ is not known exactly; computations estimate $\beta \approx 0.7124$.

**Worst case in the unit square.** For any $n$ points in the unit square, OPT $= O(\sqrt{n})$. A simple proof: cut the square into $k = \lceil \sqrt{n} \rceil$ vertical strips of width $1/k$, visit the points of each strip from bottom to top, take the strips from left to right, and return to the start. A move has length at most $|\Delta x| + |\Delta y|$. Inside each strip the vertical parts add up to at most 1, and each of the $k$ moves to the next strip or back to the start has a vertical part at most 1, so the vertical parts add up to at most $2k$. Each move other than the last one stays in a strip or goes to the next strip, so its horizontal part is at most $2/k$, and the last one has a horizontal part at most 1. So OPT $\le 2k + 2n/k + 1 = O(\sqrt{n})$. The bound is tight up to the constant, for $n$ points on a grid.

## Reductions

- **To metric TSP.** Every Euclidean instance is a metric instance, so all metric algorithms apply, with the same ratios.
- **From Hamiltonian cycle in grid graphs.** The proof under Bounds: the vertices of a grid graph, as points, have a tour of cost $n$ exactly when the graph has a Hamiltonian cycle. Papadimitriou's original proof reduces from exact cover.
- **To a grid.** Arora's scheme first moves the points to a grid of size $O(n/\varepsilon)$ and removes points that fall together. This changes OPT by at most a factor $1 + O(\varepsilon)$, and after it all costs are polynomially bounded.
- **To dynamic programming.** The structure theorem of the schemes reduces the search to tours that cross each cell of a randomly shifted quadtree at few portals, and then a dynamic program over the cells solves it.

## Applications

- **Drilling and plotting.** The order of holes on a circuit board, or of moves of a pen or a laser, is a Euclidean or rectilinear TSP.
- **Logistics in the plane.** Delivery routes when travel is close to straight-line distance.
- **Astronomy and microscopy.** The order in which a telescope or a microscope visits targets, where the cost is the time to move between them.
- **Theory.** The Euclidean TSP is the main example of a geometric problem with a PTAS, and its methods carry over to Steiner trees, $k$-median and other problems.

## References
