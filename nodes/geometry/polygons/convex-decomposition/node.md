---
tag: 3PK18N
kind: problem
slug: convex-decomposition
name: Convex decomposition of a polygon
aliases:
- convex partition of polygon
- convex polygon partition
- minimum convex partition
area: geometry/polygons
level: core
summary: Partition a simple polygon into the fewest convex pieces; the optimal version is NP-hard for polygons with holes.
prereqs: [simple-polygon, convex-polygon, polygon-triangulation, np-hard]
see_also: [hertel-mehlhorn, polygon-triangulation, monotone-polygon-partition, minkowski-sum, convex-collision-detection, rectilinear-polygon, polygon-with-holes, art-gallery-problem]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.5 (convex partitioning, the lower bound of Chazelle, the Hertel and Mehlhorn algorithm, and the table of optimal partition results)
  - paper: "Bernard Chazelle and David P. Dobkin, Optimal convex decompositions, in Godfried T. Toussaint (editor), Computational Geometry, North-Holland, 1985, 63 to 133"
    locator: the optimal partition with Steiner points in O(n + r^3) time, and the reflex vertex lower bound
  - paper: "Stefan Hertel and Kurt Mehlhorn, Fast triangulation of the plane with respect to simple polygons, Information and Control 64, 1985, 52 to 76"
    locator: the removal of inessential diagonals and the bound of four times the optimum
  - paper: "J. Mark Keil, Decomposing a polygon into simpler components, SIAM Journal on Computing 14(4), 1985, 799 to 817"
    locator: the dynamic programming algorithm for the optimal partition without Steiner points in O(r^2 n log n) time
  - paper: "Daniel H. Greene, The decomposition of polygons into convex parts, in Franco P. Preparata (editor), Computational Geometry, Advances in Computing Research 1, JAI Press, 1983, 235 to 259"
    locator: the first polynomial algorithm for the optimal partition without Steiner points, in O(r^2 n^2) time
  - paper: "J. Mark Keil and Jack Snoeyink, On the time bound for convex decomposition of simple polygons, International Journal of Computational Geometry and Applications 12(3), 2002, 181 to 192"
    locator: the O(n + r^2 min(r^2, n)) bound for the optimal partition without Steiner points
  - paper: "Andrzej Lingas, The power of non-rectilinear holes, Proceedings of the 9th International Colloquium on Automata, Languages and Programming, LNCS 140, Springer, 1982, 369 to 383"
    locator: the NP-hardness of minimum convex partition for polygons with holes
  - paper: "Joseph C. Culberson and Robert A. Reckhow, Covering polygons is hard, Journal of Algorithms 17(1), 1994, 2 to 44"
    locator: the NP-hardness of covering a simple polygon with the fewest convex pieces
---

A convex decomposition of a polygon $P$ is a set of [convex polygons](/convex-polygon/) with disjoint interiors whose union is $P$. Any [triangulation](/polygon-triangulation/) is one, with $n - 2$ pieces, but the usual goal is to use few pieces. For a [simple polygon](/simple-polygon/) with $r$ reflex vertices, the fewest pieces lie between $\lceil r/2 \rceil + 1$ and $r + 1$. The optimum can be found in polynomial time: in $O(n + r^3)$ when cuts may end anywhere (Chazelle and Dobkin), and in $O(n + r^2 \min(r^2, n))$ when the cuts must be diagonals between vertices (Keil and Snoeyink). For polygons with holes the problem is NP-hard. In practice the simple [Hertel and Mehlhorn](/hertel-mehlhorn/) heuristic, which deletes unneeded diagonals from a triangulation, is used; it never uses more than four times the optimum.

## In plain words

Cut a polygon into pieces that have no dents, using as few pieces as possible. Every dent, that is, every corner that points into the polygon, must be cut through, or it stays a dent of some piece. One straight cut can deal with at most two dents, one at each end, so a polygon with many dents needs many pieces.

There are two versions. In one, every cut must join two corners of the polygon. In the other, cuts may stop anywhere inside, which sometimes saves pieces. Both versions can be solved exactly for a polygon without holes, but with holes the problem becomes intractable. A quick method that is good enough in practice is to cut the polygon into triangles and then glue triangles back together whenever the result has no dent.

## Definition

**Notation.** $P$ is a simple polygon, or a [polygon with holes](/polygon-with-holes/), with $n$ vertices in total. A vertex is *reflex* if its interior angle is greater than $\pi$, and $r$ is the number of reflex vertices. A *diagonal* is a segment between two vertices that lies in $P$ and meets the boundary only at its endpoints. A *Steiner point* is a point that is not a vertex of $P$.

**Convex partition.** A finite set of convex polygons $C_1, \ldots, C_k$ whose union is $P$ and whose interiors are pairwise disjoint.

**Input.** The vertex lists of $P$, with exact coordinates.

**Output, without Steiner points.** A set $D$ of diagonals that do not cross, such that every face of $P$ cut along $D$ is convex, with $|D|$ as small as possible. For a simple polygon there are $|D| + 1$ pieces.

**Output, with Steiner points.** A convex partition of $P$ with the fewest pieces, where the pieces may have vertices anywhere in $P$.

**Resolving a reflex vertex.** In any convex partition, every reflex vertex $v$ of $P$ must be the endpoint of at least one cut, and the cuts at $v$ must split its interior angle into parts of at most $\pi$ each. As the angle is less than $2\pi$, one cut suffices if it points into the wedge between the extensions of the two edges at $v$.

**Bounds on the optimum.** For a simple polygon, the fewest pieces $c^*$ satisfy

$$\lceil r/2 \rceil + 1 \;\le\; c^* \;\le\; r + 1.$$

*Upper bound.* Take the reflex vertices one at a time and extend a cut from each into its wedge until it hits the boundary or an earlier cut. Each cut splits one piece into two and resolves its vertex, and no cut creates a new reflex angle, since it ends on a straight segment. So $r$ cuts give $r + 1$ convex pieces. *Lower bound for diagonals.* Every reflex vertex is an endpoint of some diagonal, and a diagonal has two endpoints, so $|D| \ge \lceil r/2 \rceil$. Chazelle proved the same bound $c^* \ge \lceil r/2 \rceil + 1$ when Steiner points are allowed.

**Covering.** In the related *convex cover* problem the pieces may overlap. A cover can use fewer pieces than any partition.

## Variants

- **Without or with Steiner points.** Allowing Steiner points can reduce the number of pieces; see the second example.
- **Fewest pieces or least total cut length.** Instead of the number of pieces, minimize the total length of the cuts, a measure used in mesh generation.
- **Polygons with holes.** The minimum is NP-hard, with or without Steiner points (Lingas).
- **Convex cover.** Overlap allowed. NP-hard even for simple polygons (Culberson and Reckhow), and later shown to be complete for the existential theory of the reals.
- **Rectilinear polygons into rectangles.** Partitioning a [rectilinear polygon](/rectilinear-polygon/) into the fewest rectangles is solved in polynomial time by a maximum matching between horizontal and vertical chords, even with holes.
- **Approximate convex decomposition.** Pieces need only be nearly convex, measured by a concavity bound. This gives far fewer pieces for detailed shapes and is common in physics simulation, especially in three dimensions.
- **Convex pieces of bounded size.** Physics engines often require convex pieces with at most a fixed number of vertices.

## Examples

**An L-shape.** $(0,0), (4,0), (4,2), (2,2), (2,4), (0,4)$ has one reflex vertex, $(2,2)$. The diagonal from $(2,2)$ to $(0,0)$ splits it into the convex quadrilaterals $(0,0), (4,0), (4,2), (2,2)$ and $(0,0), (2,2), (2,4), (0,4)$. As $r = 1$, two pieces is optimal.

**Steiner points help.** Take the triangle $A = (0,0)$, $B = (30,0)$, $C = (15,25)$ with a thin notch cut into each side, in a pinwheel pattern:

$$(0,0), (4,0), (11,6), (6,0), (30,0), (27,5), (22,8), (24,10), (15,25), (9,15), (10,12), (6,10).$$

The tips $(11,6)$, $(22,8)$ and $(10,12)$ of the notches are the three reflex vertices. With the Steiner point $O = (15,10)$, the three cuts from the tips to $O$ give three convex hexagons:

- $(11,6), (6,0), (30,0), (27,5), (22,8), (15,10)$,
- $(22,8), (24,10), (15,25), (9,15), (10,12), (15,10)$,
- $(10,12), (6,10), (0,0), (4,0), (11,6), (15,10)$.

This meets the lower bound $\lceil 3/2 \rceil + 1 = 3$. With diagonals only, the narrow wedge at each tip contains neither of the other two tips, so no diagonal resolves two tips at once and three diagonals are needed; the best partition uses three diagonals, for example from $(11,6)$ to $(30,0)$, from $(11,6)$ to $(10,12)$ and from $(22,8)$ to $(10,12)$, and has four pieces, which is the upper bound $r + 1$.

## Known algorithms

| version | method | time | pieces |
|---|---|---|---|
| any convex partition | [triangulation](/polygon-triangulation/) | $O(n \log n)$, or $O(n)$ | $n - 2$ |
| diagonals, approximate | [Hertel and Mehlhorn](/hertel-mehlhorn/): delete inessential diagonals of a triangulation | $O(n)$ after triangulation | at most $2r + 1$, below $4 c^*$ |
| diagonals, optimal | dynamic programming (Greene) | $O(r^2 n^2)$ | optimal |
| diagonals, optimal | dynamic programming (Keil) | $O(r^2 n \log n)$ | optimal |
| diagonals, optimal | Keil and Snoeyink | $O(n + r^2 \min(r^2, n))$ | optimal |
| Steiner points, optimal | Chazelle and Dobkin | $O(n + r^3)$ | optimal |
| Steiner points, approximate | one cut from each reflex vertex | $O(nr)$ by direct ray shooting | at most $r + 1$ |
| with holes, optimal | NP-hard (Lingas) | | |

**Hertel and Mehlhorn.** Start from any triangulation. A diagonal is *inessential* if removing it leaves a convex piece, that is, if neither endpoint becomes reflex in the merged piece. Remove inessential diagonals one at a time, in any order, until every remaining diagonal is essential. At a reflex vertex at most two diagonals can be essential, and a diagonal between two convex vertices of $P$ is never essential, so at most $2r$ diagonals remain and there are at most $2r + 1$ pieces. Since $c^* \ge \lceil r/2 \rceil + 1$, this is less than $4 c^*$. With a [doubly connected edge list](/doubly-connected-edge-list/) each test takes $O(1)$ time, so the whole method is linear after the triangulation.

**Dynamic programming.** The optimal algorithms without Steiner points consider subpolygons cut off by a diagonal from a reflex vertex, and for each store the best partitions together with the few pieces that touch the cutting diagonal, which decide whether pieces can be merged across it. Chazelle and Dobkin's algorithm for Steiner points also considers patterns of cuts in which the cuts from several reflex vertices meet at Steiner points, as in the pinwheel above, and shows that only patterns of a restricted form need to be searched.

## Bounds

- **Number of pieces.** $\lceil r/2 \rceil + 1 \le c^* \le r + 1$ for a simple polygon, both with and without Steiner points. Both ends are attained. The L-shape meets both. The pinwheel example meets the lower bound with Steiner points and the upper bound with diagonals only.
- **Ratio.** Hertel and Mehlhorn's heuristic uses fewer than $4 c^*$ pieces. Triangulation can use far more, $n - 2$ pieces for a convex polygon that needs one.
- **Time.** $\Omega(n)$ to read the input. The best exact algorithms are polynomial in $r$ and nearly linear in $n$ when $r$ is small.
- **Hardness.** NP-hard for polygons with holes, so no polynomial algorithm is expected there.

## Reductions

- **Triangulation gives a convex partition.** Every triangulation is a convex partition, which is the starting point of Hertel and Mehlhorn's method.
- **Minkowski sums and collision tests reduce to convex pieces.** For $P = \bigcup_i P_i$, $P \oplus Q = \bigcup_i (P_i \oplus Q)$, and each convex sum takes linear time by [merging edges](/minkowski-sum-convex-polygons/); see [Minkowski sum](/minkowski-sum/). Likewise, two polygons intersect if and only if some pair of convex pieces intersects, which [convex collision detection](/convex-collision-detection/) tests quickly.
- **Guarding.** A convex partition with $k$ pieces gives $k$ guards for the [art gallery problem](/art-gallery-problem/), one inside each piece, since a convex piece is seen from any of its points.

## Applications

- **Physics engines and collision detection.** Many engines handle only convex shapes, so concave bodies are decomposed into convex pieces first.
- **Minkowski sums and motion planning.** The decomposition method for Minkowski sums of nonconvex polygons; Agarwal, Flato and Halperin found that the quality of the decomposition matters much for the running time.
- **Mesh generation and finite elements.** Convex cells with few vertices are a first step towards good meshes.
- **Shape analysis and pattern recognition.** A decomposition into convex parts serves as a description of a shape.
- **Graphics.** Rendering pipelines that fill only convex polygons need a decomposition of concave ones.

## References
