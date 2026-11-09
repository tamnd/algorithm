---
tag: BBD60J
kind: data-structure
slug: regular-triangulation
name: Regular triangulation
aliases:
- weighted Delaunay triangulation
- power triangulation
area: geometry/voronoi-and-delaunay
level: advanced
summary: Generalized Delaunay triangulation of weighted points, dual to the power diagram.
model: real-ram
complexity:
  vars: {n: the number of sites}
  time: {build: O(n log n), insert: O(n)}
  space: {extra: O(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [power-diagram, delaunay-triangulation, bowyer-watson-algorithm]
see_also: [paraboloid-lifting-map, convex-hull-3d, alpha-shape, weighted-voronoi-diagram, lawson-flip-algorithm, delaunay-triangulation-construction, triangulation-of-point-set, quad-edge-data-structure]
sources:
  - paper: "F. Aurenhammer, Power diagrams: properties, algorithms and applications, SIAM Journal on Computing 16(1), 1987, 78-96"
    locator: the lifting of weighted points and the duality between the power diagram and its triangulation
  - paper: "H. Edelsbrunner and N. R. Shah, Incremental topological flipping works for regular triangulations, Algorithmica 15(3), 1996, 223-241"
    locator: the randomized incremental flip algorithm for regular triangulations and its expected running time
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: the chapter on weighted Delaunay triangulations
  - book: isbn:9781498711395
    title: J. E. Goodman, J. O'Rourke and C. D. Toth (editors), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: the chapter on Voronoi diagrams and Delaunay triangulations (power diagrams and regular triangulations)
---

The regular triangulation of a set of weighted points in the plane is the triangulation that you get when you lift each site $p$ with weight $w_p$ to the point $(p, |p|^2 - w_p)$ in space and project the lower convex hull back to the plane. With all weights zero, the lifted points lie on the paraboloid and the result is the [Delaunay triangulation](/delaunay-triangulation/). It is the dual of the [power diagram](/power-diagram/): two sites are joined when their power cells share an edge. A site whose lifted point is above the lower hull is *redundant* and is not a vertex. The structure is built in $O(n \log n)$ time, and the weighted form of the [Bowyer-Watson algorithm](/bowyer-watson-algorithm/) inserts sites one at a time.

## In plain words

Put every site on a vertical stick. Without weights, the stick height comes from a fixed bowl shape. A weight pulls the site down: a heavy site sits lower than the bowl. Now push a large flat sheet up from below until it hugs the lowest sticks. The sheet bends only at stick tops, and its creases, seen from above, form triangles. These triangles are the regular triangulation.

A site whose stick top stays above the sheet does not touch it. That site gets no triangle. It is hidden by heavier neighbours.

When all weights are equal, the result is the usual Delaunay triangulation.

## The abstract type

The structure holds distinct sites $p = (x, y)$ with integer coordinates and integer weights $w_p$, which can be negative. It supports:

- $\mathrm{insert}(p, w)$: add a site with its weight; return false if $p$ is already a site, and keep the first weight.
- $\mathrm{triangles}()$: the triangles as counterclockwise triples of sites, or the empty list while all sites are on one line.
- $\mathrm{vertices}()$: the sites that are vertices of some triangle.

Notation: $P$ is the set of sites, $n = |P|$, $h$ is the number of sites on the boundary of the convex hull, $d$ is the degree of a vertex, $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle. The **height** of a site is $z_p = |p|^2 - w_p$ and its **lifted point** is $\hat{p} = (p, z_p)$.

**Definitions.** For a counterclockwise triangle $t = (a, b, c)$ of sites, let $f_t$ be the affine function of the plane with $f_t = z$ at $a$, $b$ and $c$; its graph is the plane through $\hat{a}$, $\hat{b}$, $\hat{c}$. A **regular triangulation** of $P$ is a set of counterclockwise triangles whose vertices are sites, which tile the convex hull of $P$ edge to edge, and such that $f_t(q) \le z_q$ for every triangle $t$ and every site $q$: no lifted site is strictly below the plane of a triangle. Let $L$ be the lower convex hull of the lifted sites, seen as a function on the convex hull of $P$. A site $q$ is **redundant** when $z_q > L_q(q)$, where $L_q$ is the lower hull of the other lifted sites: $\hat{q}$ is strictly above the hull of the others.

The **power test** of a counterclockwise triangle $(a, b, c)$ and a point $d$ is the sign of

$$\det \begin{pmatrix} a_x - d_x & a_y - d_y & |a - d|^2 - w_a + w_d \\ b_x - d_x & b_y - d_y & |b - d|^2 - w_b + w_d \\ c_x - d_x & c_y - d_y & |c - d|^2 - w_c + w_d \end{pmatrix}.$$

It is positive exactly when $z_d < f_t(d)$, that is, when $\hat{d}$ is strictly below the plane of the triangle. With all weights equal it is $\mathrm{incircle}(a, b, c, d)$. On integer input it is computed exactly.

**Properties.** These are proved in [the correctness proof](proofs/correctness/), except the size bound, which follows from the count for triangulations.

- **Lower hull.** In a regular triangulation $T$, the function that is $f_t$ on each triangle $t$ equals $L$. So the triangles are the projection of the lower hull, cut into triangles where a face has more than three corners.
- **Vertices.** Every site whose lifted point is strictly below the lower hull of the others, $z_q < L_q(q)$, is a vertex, and so is every site outside the hull of the others; no redundant site is a vertex. A site with $z_q = L_q(q)$, whose lifted point is on the hull of the others, may or may not be a vertex.
- **Uniqueness.** If no four lifted sites lie on one plane, the regular triangulation is unique.
- **Duality with the power diagram.** For each triangle $t$, the point $x_t$ with $f_t(y) = 2 x_t \cdot y + \beta$ has the same power distance $|x_t - p|^2 - w_p$ to the three vertices of $t$ and no smaller power distance to any other site. So $x_t$ is a vertex of the [power diagram](/power-diagram/), shared by the cells of the three vertices.
- **Delaunay case.** With equal weights, $z_q - f_t(q)$ has the sign of $-\mathrm{incircle}(a, b, c, q)$, no site is redundant, and a regular triangulation is a Delaunay triangulation.
- **Size.** With $m \ge 3$ vertices, not all on one line, of which $h'$ are on the hull boundary, there are $2m - 2 - h'$ triangles and $3m - 3 - h'$ edges, by [Euler's formula](/euler-formula/).

**General position.** No assumption is made. When four lifted sites lie on one plane, or a lifted site lies on the hull of the others without being a corner, the regular triangulation is not unique, and the code returns one of them, which depends on the insertion order. Sites on one line give no triangle. Duplicate sites are ignored.

## Representation

The code stores the triangles in a dictionary from an identifier to a counterclockwise triple of site indices, and a dictionary from each directed edge $(u, v)$ to the triangle that holds it. Each boundary edge of the hull has a **ghost triangle** $(u, v, G)$ with a symbolic vertex $G$, as in the [Bowyer-Watson algorithm](/bowyer-watson-algorithm/). So each directed edge has its reverse in exactly one other triangle, and the neighbour across an edge is one dictionary lookup. A ghost $(u, v, G)$ stands for the region outside the hull edge $u \to v$, which has the hull on its right.

A triangle $t$ is **in conflict** with a new site $p$ in these cases.

- **Real triangle.** The power test of $t$ and $p$ is positive: $\hat{p}$ is strictly below the plane of $t$.
- **Ghost $(u, v, G)$.** $\mathrm{orient}(u, v, p) > 0$, so $p$ is strictly outside the hull edge; or $\mathrm{orient}(u, v, p) = 0$ and $\hat{p}$ is strictly below the line through $\hat{u}$ and $\hat{v}$. This is the limit of the real test when $G$ is a point far outside with a very large height.

A full structure stores the same data in a [quad-edge structure](/quad-edge-data-structure/) or a triangle array with neighbour pointers, and keeps a history DAG or a point location structure to find the first conflict.

## Operations

```pseudo id=main
REGULAR-INSERT(T, p, w)
L1  if p is already a site then return false
L2  if T has no triangle yet then make a triangle of the first three sites not on one line, with three ghosts, insert the other sites, and return
L3  t ← a triangle of T in conflict with p
L4  if there is no such t then return            ▷ p is redundant now
L5  C ← all triangles in conflict with p that are reached from t through shared edges
L6  E ← the directed edges of triangles in C whose neighbour is not in C
L7  delete the triangles of C from T
L8  for each edge (a, b) in E add the triangle (a, b, p)
```

- **Line L2.** While all sites are on one line, the code only stores them. The first site off that line gives the first triangle, and the code then inserts the other stored sites with lines L3 to L8.
- **Line L3.** The code scans all triangles, in $O(n)$ time. A history DAG, as in the [randomized incremental Delaunay construction](/delaunay-triangulation-construction/), finds a conflict in $O(\log n)$ expected time.
- **Line L4.** No triangle is in conflict exactly when $p$ is inside the hull and $\hat{p}$ is on or above the lower hull. Then $p$ is stored but is not a vertex.
- **Lines L5 and L6.** The conflict set is connected, so a depth-first search finds it. Its border edges all have $p$ strictly on the cavity side.
- **Line L7.** All triangles at an old vertex may be in conflict. Then that vertex is not on the border, and it disappears: the new site has made it redundant. This is the case that the unweighted algorithm never meets.
- **Line L8.** The border edges at $G$ give the ghosts of the new hull edges at $p$.

## Example

Take the five sites of the [power diagram](/power-diagram/) example, inserted in this order: $(0,0)$ with weight $16$, $(6,0)$ with weight $9$, $(3,5)$ with weight $16$, $(7,6)$ with weight $0$ and $(3,2)$ with weight $0$. Their heights $z = |p|^2 - w$ are $-16$, $27$, $18$, $85$ and $13$.

- **L2.** The first triangle is $(0,0), (6,0), (3,5)$. Its plane is $f(x, y) = \frac{43}{6} x + \frac{5}{2} y - 16$.
- **L3 to L8 for $(7,6)$.** The real triangle has $f(7, 6) = \frac{295}{6} < 85$, so it is not in conflict. The ghost of the hull edge $(3,5) \to (6,0)$ has $\mathrm{orient}((3,5), (6,0), (7,6)) = 23 > 0$, so it is the whole cavity. The new triangle is $(3,5), (6,0), (7,6)$, with the plane $g(x, y) = \frac{344}{23} x + \frac{165}{23} y - \frac{1443}{23}$, and $g(0, 0) = -\frac{1443}{23} < -16$, so the old site $(0,0)$ is above it.
- **L3 and L4 for $(3,2)$.** The site is inside the first triangle, and $f(3, 2) = \frac{21}{2} < 13$, so its lifted point is above the plane. No triangle is in conflict, and $(3,2)$ is redundant.

The result is the two triangles $(0,0), (6,0), (3,5)$ and $(3,5), (6,0), (7,6)$ with four vertices. The unweighted Delaunay triangulation of the same points has $(3,2)$ as a vertex. The points $x_t$ of the two triangles are half the gradients of $f$ and $g$: $(\frac{43}{12}, \frac{5}{4})$ and $(\frac{172}{23}, \frac{165}{46})$, the two vertices of the power diagram.

## Correctness

**Theorem.** Let $S$ be the distinct sites inserted, each with its first weight. If $S$ lies on one line, $\mathrm{triangles}()$ is empty. Otherwise, after every insertion, the stored triangles form a regular triangulation of the sites inserted so far, so the final structure is a regular triangulation of $S$; its vertices include every site whose lifted point is strictly below the lower hull of the others, and no redundant site.

The proof follows the one for the Bowyer-Watson algorithm, with $|q|^2$ replaced by the height $z_q$. The invariant is that the triangles tile the hull and that no lifted site is below a triangle's plane. Then the function made of the planes is the maximum of the planes, so it is convex. This shows that no triangle is in conflict when $\hat{p}$ is on or above it, that the conflict set is connected, and that $p$ sees every border edge from the cavity side, so the fan from $p$ tiles the cavity. The new edges are locally regular, so the new function is convex. It is also below the old one, which keeps the vertices that disappear and the old redundant sites above the new planes. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Insertion in this code.** $O(n)$ time per insertion for the scan of line L3, plus the size of the cavity, which is $O(n)$. So $n$ insertions take $O(n^2)$ worst-case time. A redundant site costs only the scan.
- **Randomized incremental.** With a random insertion order and a history DAG or conflict lists, the expected total time is $O(n \log n)$ and the expected total number of created triangles is $O(n)$ (Edelsbrunner and Shah, cited here). The backwards analysis is that of the [Bowyer-Watson page](/bowyer-watson-algorithm/): a redundant site creates nothing, and a random vertex of a triangulation has fewer than $6$ incident triangles on average.
- **Through the 3D hull.** The lower hull of the $n$ lifted points takes $O(n \log n)$ worst-case time with a [3D convex hull](/convex-hull-3d/) algorithm. This is optimal in the algebraic computation tree model, because equal weights give the Delaunay triangulation ([lower bound](/voronoi-construction-lower-bound/)).
- **Single insertion.** One insertion can change $\Theta(n)$ triangles in the worst case, for example a heavy site that makes all others redundant.
- **Space.** $O(n)$: at most $2n$ real and ghost triangles.

## Variants

- **Edge flips.** Insert the site into the triangle that holds it, then flip edges that are not locally regular, as in the [Lawson flip algorithm](/lawson-flip-algorithm/). A redundant vertex of degree $3$ is removed by a $3$-to-$1$ flip, which edge flips alone cannot do. Edelsbrunner and Shah proved that this incremental flipping always reaches the regular triangulation.
- **Weighted alpha shapes.** The [alpha shape](/alpha-shape/) of a union of disks or balls is a subcomplex of the regular triangulation, used for the area and volume of molecules.
- **Higher dimensions.** The definition is the same in $\mathbb{R}^d$, through the lower hull in $\mathbb{R}^{d+1}$, and the worst-case size is that of a convex hull in $\mathbb{R}^{d+1}$, $O(n^{\lceil d/2 \rceil})$ simplices.
- **Regular subdivisions.** Any height function on a point set, not only $|p|^2 - w_p$, defines a subdivision by the same lower-hull projection. Every height function arises from some weights, since $w_p = |p|^2 - z_p$, so these are the same objects.
- **Unweighted case.** All weights equal gives the [Delaunay triangulation](/delaunay-triangulation/), and the power test becomes the incircle test.

## When to use it

Use the regular triangulation when sites have sizes: atoms in a molecule, disks in a packing, or mesh vertices that must keep a protected region. It is the triangulation for weighted alpha shapes, for the union of balls, for sliver removal by weight pumping in Delaunay meshing, and for the dual of a power diagram in optimal transport. If all weights are equal, use a plain Delaunay algorithm, which needs no redundancy handling.

## Pitfalls

- **Redundant sites.** A site may not be a vertex, and an old vertex may vanish when a heavy site is inserted. Code that assumes every site is a vertex, or that the vertex set only grows, breaks.
- **Hull edges with collinear sites.** A new site on the line of a hull edge may still be in conflict with its ghost, through the lifted line. Ignoring this case leaves a vertex inside a hull edge.
- **Starting point of the walk.** A site need not lie in its own power cell, so the power diagram cannot locate it by its own position.
- **Weights are squared radii.** The height is $|p|^2 - r^2$ for a disk of radius $r$.
- **Floating-point power tests.** The power test is a degree-four polynomial in the input. Rounding gives wrong signs near degenerate cases, and then the cavity is not connected. Exact integers avoid this.

## Implementations

## History

F. Aurenhammer in 1987 described the lifting of weighted points, the power diagram, and the dual triangulation. The name regular comes from regular subdivisions, the subdivisions of a point set given by projecting the lower hull of points lifted to arbitrary heights, which Gel'fand, Kapranov and Zelevinsky studied in algebraic geometry. H. Edelsbrunner and N. R. Shah showed in 1996 that randomized incremental flipping builds the regular triangulation in any dimension, in $O(n \log n)$ expected time in the plane. Weighted Delaunay triangulations became standard tools in molecular geometry and in mesh generation.

## References
