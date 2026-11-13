---
tag: 80S2K0
kind: problem
slug: minkowski-sum
name: Minkowski sum
aliases:
- Minkowski addition
- Minkowski sum of polygons
- convolution of polygons
area: geometry/polygons
level: core
summary: The set of all vector sums of points from two polygons; used for collision detection and motion planning.
prereqs: [polygon, convex-polygon, simple-polygon, point-and-vector]
see_also: [minkowski-sum-convex-polygons, configuration-space, motion-planning, convex-collision-detection, convex-decomposition, offset-curve, support-function, polygon-with-holes]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 13, Robot Motion Planning, Sections 13.3 (Minkowski sums, the convex case, the pseudodisc property and the O(nm) bound) and 13.4 (translational motion planning)
  - paper: "Klara Kedem, Ron Livne, János Pach and Micha Sharir, On the union of Jordan regions and collision-free translational motion amidst polygonal obstacles, Discrete and Computational Geometry 1(1), 1986, 59 to 71"
    locator: the linear bound on the union of pseudodiscs and its use for sums of a convex polygon with polygonal obstacles
  - paper: "Tomás Lozano-Pérez, Spatial planning: a configuration space approach, IEEE Transactions on Computers C-32(2), 1983, 108 to 120"
    locator: configuration space obstacles as Minkowski sums
  - paper: "Pankaj K. Agarwal, Eyal Flato and Dan Halperin, Polygon decomposition for efficient construction of Minkowski sums, Computational Geometry 21(1 to 2), 2002, 39 to 61"
    locator: the decomposition method and the experiments with different convex decompositions
  - paper: "Ron Wein, Exact and efficient construction of planar Minkowski sums using the convolution method, Proceedings of the 14th European Symposium on Algorithms, LNCS 4168, 2006, 829 to 840"
    locator: the convolution cycles and the winding number characterization of the sum
---

The Minkowski sum of two sets $A$ and $B$ in the plane is $A \oplus B = \{a + b : a \in A, b \in B\}$. For polygons, the problem is to compute the boundary of $P \oplus Q$ from the vertex lists of $P$ and $Q$. When both are convex, the sum is a convex polygon with at most $n + m$ vertices, computed in linear time by [merging the edge sequences](/minkowski-sum-convex-polygons/). When one is not convex, the sum can have $\Theta(nm)$ vertices, and when neither is, $\Theta(n^2 m^2)$, with holes. Minkowski sums turn questions about moving shapes into questions about points: a translating robot $R$ hits an obstacle $P$ exactly when its reference point is in $P \oplus (-R)$, the [configuration space](/configuration-space/) obstacle.

## In plain words

Put a small shape on a large one, so that a chosen point of the small shape stays on the large shape, and move it to every possible place. The area covered by the small shape is the sum.

For two convex shapes, the sum is a convex shape whose sides are the sides of both, sorted by direction. For shapes with dents, the sum can fill in narrow gaps and can even enclose a hole. The sum is the main tool for planning the motion of a robot that slides without turning: grow every obstacle by the shape of the robot, and then the robot is a single point that must avoid the grown obstacles.

## Definition

**Notation.** A polygon is a cyclic list of vertices $v_0, \ldots, v_{n-1}$ with edges $v_i v_{i+1}$, indices modulo $n$. A point is $p = (x, y)$, and $\operatorname{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$. We identify a polygon with its closed region. $P$ has $n$ vertices and $Q$ has $m$.

**Minkowski sum.** $P \oplus Q = \{p + q : p \in P, q \in Q\}$. Also $-Q = \{-q : q \in Q\}$, and $P \ominus Q = \{x : x + Q \subseteq P\}$ is the Minkowski difference, or erosion.

**Input.** Two polygons $P$ and $Q$, given by their vertices in counterclockwise order, each simple or convex, with integer or rational coordinates.

**Output.** The boundary of $P \oplus Q$: an outer boundary cycle and the boundary cycles of its holes, each as a list of vertices. When $P$ and $Q$ are convex, this is a single convex polygon.

**Basic properties.** For all sets $A, B, C$ and points $t$:

- $A \oplus B = B \oplus A$ and $(A \oplus B) \oplus C = A \oplus (B \oplus C)$.
- $(A \cup B) \oplus C = (A \oplus C) \cup (B \oplus C)$. This is the reason that decomposing into convex pieces works.
- $(A + t) \oplus B = (A \oplus B) + t$, and $A \oplus \{t\} = A + t$.
- If $A$ and $B$ are convex, so is $A \oplus B$, and for convex polygons $P \oplus Q$ is the [convex hull](/convex-hull/) of the $nm$ sums of vertices.
- $A \cap B \ne \emptyset$ if and only if $0 \in A \oplus (-B)$, and the distance between $A$ and $B$ is the distance from $0$ to $A \oplus (-B)$.

## Variants

- **Convex and convex.** Both polygons are convex. The sum is convex with at most $n + m$ vertices; see [Minkowski sum of convex polygons](/minkowski-sum-convex-polygons/).
- **Convex and nonconvex.** A convex robot among polygonal obstacles, the main case in motion planning.
- **Nonconvex and nonconvex.** The general case, for example in nesting problems, where the boundary of $P \oplus (-Q)$ is called the no-fit polygon.
- **Polygons with holes and sets of polygons.** Sums of a [polygon with holes](/polygon-with-holes/), or of a union of obstacles, by the distributive law.
- **Offsetting.** The sum with a disk of radius $r$ grows a polygon by $r$, with circular arcs at convex vertices; see [offset curve](/offset-curve/) and [curve offsetting](/curve-offsetting/). The erosion by a disk shrinks it.
- **Minkowski difference.** $P \ominus Q$ is the set of positions where a translate of $Q$ fits inside $P$. It equals the complement of $\overline{P} \oplus (-Q)$, where $\overline{P}$ is the complement of $P$.
- **Higher dimensions.** For convex polytopes in three dimensions the sum has $O(nm)$ faces in the worst case, and for nonconvex polyhedra $O(n^3 m^3)$.
- **Images.** In mathematical morphology, the sum of a binary image with a small structuring element is the dilation, and the difference is the erosion.

## Examples

**Two convex polygons.** For the triangle $(0,0), (2,0), (0,2)$ and the unit square with lowest vertex $(3,1)$, the sum is the pentagon $(3,1), (6,1), (6,2), (4,4), (3,4)$. It has $3 + 4 - 2 = 5$ vertices, because two pairs of edges have the same direction and join.

**A segment and a polygon.** For $Q$ the segment from $(0,0)$ to $(0,1)$, the sum $P \oplus Q$ is the region swept by $P$ when it moves up by one unit.

**A sum with a hole.** Let $P$ be the square $[0,8]^2$ with a square cavity $[2,6]^2$ that opens to the right through a channel $[6,8] \times [4,5]$:

$$P = (0,0), (8,0), (8,4), (6,4), (6,2), (2,2), (2,6), (6,6), (6,5), (8,5), (8,8), (0,8),$$

a simple polygon of area 46. Add the vertical segment $Q$ from $(0,0)$ to $(0,1)$. The channel has height 1, so its part of the sum is filled, and the mouth of the cavity closes. The floor of the cavity moves up by 1. The sum is the rectangle $[0,8] \times [0,9]$ minus the hole $(2,6) \times (3,6)$, of area $72 - 12 = 60$. So the sum of a simple polygon and a segment need not be simple; it can have a hole.

## Known algorithms

| inputs | method | time | output size |
|---|---|---|---|
| convex and convex | [merge of edge sequences](/minkowski-sum-convex-polygons/) | $O(n + m)$ | $\le n + m$ |
| convex ($n$) and simple ($m$) | triangulate $Q$, add $P$ to each triangle, union of $m - 2$ pseudodiscs | $O(nm \log^2(nm))$ by divide and conquer | $O(nm)$ |
| simple and simple | [convex decomposition](/convex-decomposition/) of both, pairwise convex sums, union | $O(n^2 m^2 \log(nm))$ in the worst case | $O(n^2 m^2)$ |
| simple and simple | convolution cycles and winding numbers (Guibas, Ramshaw and Stolfi; Wein) | output sensitive in practice | $O(n^2 m^2)$ |

**Decomposition.** By the distributive law, if $P = \bigcup_i P_i$ and $Q = \bigcup_j Q_j$ with convex pieces, then $P \oplus Q = \bigcup_{i,j} (P_i \oplus Q_j)$. Each pairwise sum takes linear time, and the union is computed by a sweep or by divide and conquer. For a convex $P$ and a triangulated $Q$, the sums $P \oplus T_j$ of $P$ with triangles with disjoint interiors are *pseudodiscs*: the boundaries of any two cross at most twice. Kedem, Livne, Pach and Sharir proved that the union of $k$ pseudodiscs has $O(k)$ vertices on its boundary, which gives the $O(nm)$ bound. Agarwal, Flato and Halperin showed in experiments that the choice of the decomposition matters a lot in practice.

**Convolution.** The convolution of $P$ and $Q$ is a closed polygonal curve made of the segments $p_i + e$ for each vertex $p_i$ of $P$ and each edge $e$ of $Q$ whose direction lies between the directions of the two edges at $p_i$, and symmetrically. It has $O(nm)$ segments. The sum $P \oplus Q$ is the set of points around which the convolution has positive [winding number](/winding-number-algorithm/), so the sum is found by computing the arrangement of the convolution segments and the winding number of each face. CGAL computes planar Minkowski sums this way, with a reduced convolution that drops segments that cannot be on the boundary.

## Bounds

- **Convex and convex.** At most $n + m$ vertices, with equality when the polygons are strictly convex and have no two edges with the same direction.
- **Convex and simple.** $\Theta(nm)$ in the worst case. A convex $n$-gon plus a comb with $\Theta(m)$ narrow teeth and wide gaps gives a sum whose boundary follows $\Theta(n)$ edges of a copy of $P$ inside each of the $\Theta(m)$ gaps.
- **Simple and simple.** $\Theta(n^2 m^2)$ in the worst case. Two combs placed at right angles produce a grid of $\Theta(nm)$ by $\Theta(nm)$ crossing strips, with $\Theta(n^2 m^2)$ holes.
- **Lower bound for computing.** For convex polygons, $\Omega(n + m)$ time, as every vertex can appear in the output.

## Reductions

- **Collision tests to point location.** A translate $R + t$ of a robot meets an obstacle $P$ if and only if $t \in P \oplus (-R)$. So translational motion planning reduces to moving a point among the obstacles $P_i \oplus (-R)$; see [motion planning](/motion-planning/).
- **Intersection and distance to a point query.** Two convex polygons intersect if and only if $0 \in P \oplus (-Q)$, which [point in convex polygon](/point-in-convex-polygon/) decides. The distance between them is the distance from $0$ to that sum. Methods based on [support functions](/support-function/), such as [GJK](/gjk-algorithm/), answer these questions without building the sum, as $h_{P \oplus Q} = h_P + h_Q$.
- **Nonconvex to convex.** The distributive law reduces general sums to sums of convex pieces and a union.
- **Offsetting.** The offset of a polygon by $r$ is its sum with a disk, which reduces to the sum with a regular polygon that approximates the disk, or is computed exactly with arcs.

## Applications

- **Robot motion planning.** Configuration space obstacles for a translating robot, from Lozano-Pérez's work on spatial planning.
- **Collision detection and physics.** Intersection, distance and penetration depth between convex shapes; see [convex collision detection](/convex-collision-detection/).
- **Packing and nesting.** Placing parts on a sheet of material without overlap; the no-fit polygon of two parts is the boundary of $P \oplus (-Q)$.
- **CNC machining and offsetting.** Tool paths are offsets of the part outline by the tool radius.
- **Geographic information systems.** Buffer zones around regions are sums with a disk.
- **Image processing.** Dilation and erosion in mathematical morphology.

## References
