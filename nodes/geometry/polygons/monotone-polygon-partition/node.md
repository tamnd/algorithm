---
tag: 65XP42
kind: problem
slug: monotone-polygon-partition
name: Monotone polygon partition
aliases:
- monotone decomposition of polygon
- partition into monotone pieces
- MakeMonotone
- polygon regularization
area: geometry/polygons
level: core
summary: Partition a simple polygon into monotone pieces with diagonals, in O(n log n).
prereqs: [monotone-polygon, simple-polygon, sweep-line-technique]
see_also: [monotone-polygon-triangulation, polygon-triangulation, trapezoidal-map, seidel-polygon-triangulation, chazelle-polygon-triangulation, monotone-subdivision, polygon-with-holes, convex-decomposition]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Section 3.2 (the algorithm MakeMonotone, the helper of an edge, and the O(n log n) bound) and Section 3.3 (triangulating the monotone pieces)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.1 (monotone partitioning through a trapezoidalization and interior cusps)
  - paper: "Der-Tsai Lee and Franco P. Preparata, Location of a point in a planar subdivision and its applications, SIAM Journal on Computing 6(3), 1977, 594 to 606"
    locator: the regularization of a planar subdivision into monotone regions by a plane sweep in O(n log n) time
  - paper: "Michael R. Garey, David S. Johnson, Franco P. Preparata and Robert E. Tarjan, Triangulating a simple polygon, Information Processing Letters 7(4), 1978, 175 to 179"
    locator: the partition into monotone pieces followed by linear time triangulation of each piece
  - paper: "Alain Fournier and Delfin Y. Montuno, Triangulating simple polygons and equivalent problems, ACM Transactions on Graphics 3(2), 1984, 153 to 174"
    locator: the linear time equivalence of trapezoidal decomposition, monotone partition and triangulation
  - paper: doi:10.1007/BF02574703
    title: Bernard Chazelle, Triangulating a simple polygon in linear time, Discrete and Computational Geometry 6, 1991, 485 to 524
    locator: the linear time trapezoidal decomposition, which gives a monotone partition in linear time
  - paper: "Takao Asano, Tetsuo Asano and Ron Y. Pinter, Polygon triangulation: efficiency and minimality, Journal of Algorithms 7(2), 1986, 221 to 231"
    locator: the Omega(n log n) lower bound for triangulating polygons with holes
---

The monotone polygon partition problem asks to cut a [simple polygon](/simple-polygon/) into [monotone polygons](/monotone-polygon/) by adding diagonals, segments between two vertices that run inside the polygon. It is the first step of the classic $O(n \log n)$ triangulation: each monotone piece is then [triangulated](/monotone-polygon-triangulation/) in linear time. A top to bottom [sweep](/sweep-line-technique/), due in this form to Lee and Preparata, finds the obstacles to monotonicity, the split and merge vertices, and adds one diagonal at each. It runs in $O(n \log n)$ time, and also works for polygons with holes. For a simple polygon without holes the problem can be solved in linear time through Chazelle's triangulation.

## In plain words

A polygon is easy to handle when every horizontal line cuts it in one piece. Dents that point up or down spoil this: a horizontal line through a dent meets the polygon on both sides of it.

The fix is to cut the polygon along straight cuts from corner to corner, until no piece has such a dent. Sweep a horizontal line from the top down. When the line reaches the tip of a dent that points down into the polygon from above, or the tip of one that points up, connect that tip to a nearby corner that the sweep remembers for the region next to it. Each cut removes the dent. The pieces that remain are monotone, and each one is easy to cut into triangles.

## Definition

**Notation.** The input is a polygon $P$ with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order, indices modulo $n$, so that the interior is to the left of each edge $e_i = v_i v_{i+1}$. A point $p$ is *above* a point $q$ if $p_y > q_y$, or $p_y = q_y$ and $p_x < q_x$; this tie rule acts like a rotation of the plane by an infinitely small angle and makes all vertex heights distinct. A *diagonal* is a segment between two vertices that are not adjacent, whose relative interior lies in the interior of $P$.

**Vertex types.** A vertex $v$ is a *split vertex* if both neighbors are below it and the interior angle at $v$ is greater than $\pi$, and a *merge vertex* if both neighbors are above it and the interior angle is greater than $\pi$. With integer coordinates the angle test is the sign of $(v - u) \times (w - v)$ for the neighbors $u$ before and $w$ after $v$, negative for a reflex vertex. A polygon with no split vertex and no merge vertex is $y$-monotone.

**Input.** A simple polygon $P$, or a [polygon with holes](/polygon-with-holes/), with $n$ vertices in total, given as vertex lists with exact coordinates.

**Output.** A set $D$ of diagonals that do not cross each other, such that every face of $P$ cut along $D$ is a $y$-monotone polygon. The output is usually given as a [doubly connected edge list](/doubly-connected-edge-list/) of the pieces.

**Counting.** Each diagonal of a simple polygon cuts one piece into two, so $|D|$ diagonals give $|D| + 1$ pieces. Every split vertex and every merge vertex must be an endpoint of some diagonal, as otherwise it remains a split or merge vertex of its piece. A diagonal has two endpoints, so if the polygon has $s$ split vertices and $m$ merge vertices, every solution has $|D| \ge \lceil (s + m)/2 \rceil$. The sweep below uses at most $s + m$ diagonals. Each split or merge vertex is reflex, so $s + m \le r$ for $r$ reflex vertices.

## Variants

- **Fixed direction.** The standard problem: all pieces monotone with respect to one given direction, usually the $y$-axis.
- **Polygons with holes.** The top vertex of each hole is a split vertex and its bottom vertex is a merge vertex, so the sweep connects every hole to the rest of the boundary. The same algorithm works, with $n$ the total number of vertices.
- **Planar subdivisions.** Lee and Preparata *regularize* a planar straight line graph by adding edges, so that every face becomes monotone; this is the preprocessing of the chain method of point location and of [monotone subdivisions](/monotone-subdivision/) in general.
- **Monotone mountains.** A finer partition into monotone pieces one of whose chains is a single edge; it comes directly from a [trapezoidal decomposition](/trapezoidal-map/), and each mountain is triangulated by cutting off its convex vertices.
- **Fewest pieces.** Minimizing $|D|$ for a fixed direction, or allowing each piece its own direction of monotonicity, gives harder optimization problems; the sweep does not minimize the number of pieces.
- **Steiner points.** If cuts may end at new points on the boundary, the horizontal segments of a trapezoidal decomposition can also be used as cuts.

## Examples

**A comb.** The comb $(0,0), (5,0), (5,3), (4,3), (4,1), (3,1), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ has three teeth pointing up and two merge vertices, $(4,1)$ and $(2,1)$, at the bottoms of the gaps between the teeth. Swept from the top, the merge vertex $(2,1)$ is connected to $(3,1)$, the next vertex that the sweep meets in the region next to it, and $(4,1)$ is connected to the end vertex $(0,0)$. The three pieces are the right tooth with the bottom right part, $(0,0), (5,0), (5,3), (4,3), (4,1)$; the middle tooth, $(3,1), (3,3), (2,3), (2,1)$; and the left part, $(4,1), (3,1), (2,1), (1,1), (1,3), (0,3), (0,0)$. Each is $y$-monotone. The diagonal from $(2,1)$ to $(3,1)$ is horizontal and is collinear with boundary edges at both ends, which is allowed: it meets the boundary only at its endpoints.

**One diagonal for two vertices.** The polygon $(1,0), (2,0), (2,1), (3,1), (3,3), (1,2), (0,2)$ has a split vertex $(2,1)$ and a merge vertex $(1,2)$. The merge vertex is processed first and becomes the remembered vertex of the edge to its left; at the split vertex, the sweep connects to it. So the single diagonal from $(2,1)$ to $(1,2)$ removes both, and the pieces are $(1,0), (2,0), (2,1), (1,2), (0,2)$ and $(2,1), (3,1), (3,3), (1,2)$. This meets the lower bound $\lceil 2/2 \rceil = 1$.

**Already monotone.** A convex polygon, or any $y$-monotone polygon without horizontal edges, has no split or merge vertices, and the sweep adds nothing. With horizontal edges the tie rule may still flag a vertex: in the mirrored L-shape $(0,0), (4,0), (4,4), (3,4), (3,2), (0,2)$, which is $y$-monotone, the reflex vertex $(3,2)$ counts as a merge vertex, and the sweep adds the diagonal from $(3,2)$ to $(0,0)$.

## Known algorithms

| method | time | space | notes |
|---|---|---|---|
| plane sweep with helpers (Lee and Preparata; de Berg et al.) | $O(n \log n)$ | $O(n)$ | holes allowed; at most $s + m$ diagonals |
| from a trapezoidal decomposition (Fournier and Montuno) | $O(n)$ after the decomposition | $O(n)$ | randomized $O(n \log^* n)$ expected with [Seidel](/seidel-polygon-triangulation/) |
| from [Chazelle's triangulation](/chazelle-polygon-triangulation/) | $O(n)$ | $O(n)$ | simple polygons only; of theoretical interest |

**The sweep.** The algorithm sorts the vertices from top to bottom in the order *above*, and moves a horizontal sweep line down through them. The status is a [balanced search tree](/balanced-binary-search-tree/) of the edges that cross the sweep line and have the interior of $P$ to their right, ordered from left to right. Each such edge $e$ stores a *helper*: the lowest vertex above the sweep line that lies between $e$ and the next boundary edge to its right, so that the horizontal segment from the helper to $e$ lies inside $P$. At each vertex $v_i$:

- *start vertex:* insert $e_i$ with helper $v_i$;
- *end vertex:* if the helper of $e_{i-1}$ is a merge vertex, add the diagonal from $v_i$ to it; delete $e_{i-1}$;
- *split vertex:* find the edge $e_j$ directly left of $v_i$, add the diagonal from $v_i$ to the helper of $e_j$, set the helper of $e_j$ to $v_i$, and insert $e_i$ with helper $v_i$;
- *merge vertex:* if the helper of $e_{i-1}$ is a merge vertex, connect $v_i$ to it; delete $e_{i-1}$; find the edge $e_j$ directly left of $v_i$, connect $v_i$ to its helper if that is a merge vertex, and set the helper of $e_j$ to $v_i$;
- *regular vertex:* if the interior lies to the right of $v_i$, handle $e_{i-1}$ as at an end vertex and insert $e_i$ with helper $v_i$; otherwise handle the edge directly left of $v_i$ as at a merge vertex.

A split vertex looks up for its diagonal, to the helper, which is the lowest vertex between the two edges that surround it. A merge vertex looks down: it waits as a helper until the next vertex that replaces it, which is the highest vertex below it in the same region, and is connected to that vertex. The diagonals never cross each other or the boundary because each one lies in the trapezoid between two consecutive edges of the status. With the tie rule all heights are distinct, so horizontal edges need no special case. Sorting takes $O(n \log n)$ time and each event does $O(1)$ tree operations of $O(\log n)$ time each.

**Through a trapezoidal decomposition.** Draw from each vertex the horizontal segments to the nearest boundary to the left and to the right. Each trapezoid of the result has one vertex of $P$ on its top side and one on its bottom side. A trapezoid whose two vertices are not on a common edge of $P$ contributes a diagonal between them, and these diagonals cut $P$ into monotone pieces. This turns any trapezoidal decomposition algorithm into a monotone partition algorithm with $O(n)$ extra time, and Chazelle's linear time decomposition gives an $O(n)$ bound for simple polygons.

## Bounds

- **Simple polygons.** $\Theta(n)$: the input must be read, and Chazelle's algorithm gives the upper bound. The practical algorithms take $O(n \log n)$ or $O(n \log^* n)$ expected time.
- **Polygons with holes.** $\Theta(n \log n)$ in the algebraic decision tree model. The upper bound is the sweep. For the lower bound, a monotone partition followed by the linear time triangulation of each piece triangulates the polygon, and Asano, Asano and Pinter proved that triangulating a polygon with holes needs $\Omega(n \log n)$ time; the triangulation step adds only $O(n)$ comparisons and [orientation tests](/orientation-test/).
- **Number of diagonals.** Between $\lceil (s + m)/2 \rceil$ and $s + m$ for the sweep; in the worst case $\Theta(n)$, as in a comb with $\Theta(n)$ teeth.

## Reductions

- **Triangulation reduces to monotone partition.** Partition, then triangulate each monotone piece with a stack in linear time; this gives the $O(n \log n)$ [polygon triangulation](/polygon-triangulation/) of Garey, Johnson, Preparata and Tarjan.
- **Monotone partition reduces to trapezoidal decomposition**, by the diagonals described above, and trapezoidal decomposition reduces to triangulation in linear time. Fournier and Montuno showed that the three problems are equivalent up to linear time.
- **Point location.** Regularizing a planar subdivision makes its faces monotone, which the chain method and the [slab method](/slab-method-point-location/) use; see [planar point location](/planar-point-location/).

## Applications

- **Triangulation.** The main use, as the first step of the $O(n \log n)$ triangulation in textbooks and libraries.
- **Point location.** Regularized monotone subdivisions are the input of chain based point location structures.
- **Scan conversion and filling.** A monotone piece is filled one scanline at a time with two edge pointers, so partitioning a complex polygon into monotone pieces simplifies [scanline polygon fill](/scanline-polygon-fill/).
- **Other decompositions.** A monotone partition is a step towards [convex decompositions](/convex-decomposition/), and the diagonals of a triangulation computed this way are the input of Hertel and Mehlhorn's convex partition.

## References
