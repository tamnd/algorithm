---
tag: 9TX46V
kind: concept
slug: paraboloid-lifting-map
name: Paraboloid lifting map
aliases:
- paraboloid lifting
- lifting map
- parabolic lifting
area: geometry/voronoi-and-delaunay
level: core
summary: Maps each site (x,y) to (x,y,x^2+y^2); lower convex hull faces project to the Delaunay triangulation.
prereqs: [in-circle-test, convex-hull-3d, delaunay-triangulation]
see_also: [upper-and-lower-hull, regular-triangulation, power-diagram, farthest-point-voronoi-diagram, order-k-voronoi-diagram, higher-dimensional-delaunay, circular-range-searching, lawson-flip-algorithm]
sources:
  - paper: "K. Q. Brown, Voronoi diagrams from convex hulls, Information Processing Letters 9(5), 1979, 223-228"
    locator: the transformation of a Voronoi diagram in the plane into a convex hull in space
  - paper: "H. Edelsbrunner and R. Seidel, Voronoi diagrams and arrangements, Discrete and Computational Geometry 1, 1986, 25-44"
    locator: the paraboloid, tangent planes and the reduction of Voronoi diagrams of all orders to arrangements of planes
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 11 (Voronoi diagrams revisited, the lifting to the paraboloid and the lower convex hull)
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 2 (the parabolic lifting map and the Delaunay subdivision as the projection of the lower hull)
---

The paraboloid lifting map sends a point $p = (x, y)$ of the plane to $\lambda(p) = (x, y, x^2 + y^2)$, a point of the paraboloid $z = x^2 + y^2$ in space. It turns circles into planes: a point is inside a circle exactly when its lifted point is below a certain plane. So the [in-circle test](/in-circle-test/) becomes an orientation test in space, and the [Delaunay triangulation](/delaunay-triangulation/) of a point set becomes the projection of the lower [convex hull](/convex-hull-3d/) of the lifted points. The same map, with tangent planes in place of lifted points, turns the Voronoi diagram into the projection of an upper envelope of planes.

## In plain words

Put a large bowl over the flat map, with its lowest point at the origin. Push every site straight up until it touches the bowl. Now a flat sheet that cuts the bowl cuts it along a curve that looks like a circle from above. The sites inside that circle are exactly the sites whose bowl points are under the sheet.

Lay a stiff cloth under all the bowl points and pull it up tight from below. The cloth folds into flat triangles with corners at the bowl points. Seen from above, these triangles are the Delaunay triangles, because no bowl point is under the flat piece of any triangle, so no site is inside its circle.

This turns a question about circles in the plane into a question about convex shapes in space, where good tools already exist.

## The idea

Notation: $P$ is a finite set of $n$ points in the plane, not all on one line, with $h$ of them on the boundary of its convex hull $\mathrm{conv}(P)$; a point is $p = (x, y)$ and $|p|^2 = x^2 + y^2$; $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise; $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside the circle through $a$, $b$, $c$. General position is not assumed: cocircular points are allowed throughout.

**Lemma 1 (circles are planes).** Let $g(q) = 2 o \cdot q + c$ be the height function of a non-vertical plane, with $o$ a point of the plane and $c$ a number, and let $r^2 = c + |o|^2$. For every point $q$,

$$g(q) - |q|^2 = r^2 - |q - o|^2.$$

So the lifted point $\lambda(q)$ is strictly below the plane exactly when $q$ is strictly inside the circle with center $o$ and squared radius $r^2$, on the plane exactly when $q$ is on that circle, and above it otherwise; if $r^2 \le 0$ there is no point strictly inside. Every circle with center $o$ and radius $r$ comes from exactly one such plane, with $c = r^2 - |o|^2$.

*Proof.* Expand $|q - o|^2 = |q|^2 - 2 o \cdot q + |o|^2$. $\square$

For a triangle $abc$ with $\mathrm{orient}(a, b, c) \ne 0$, let $g_{abc}$ be the affine function with $g_{abc} = |\cdot|^2$ at $a$, $b$ and $c$, the height of the plane through $\lambda(a)$, $\lambda(b)$, $\lambda(c)$. By Lemma 1 its circle is the circumcircle of $abc$, so $d$ is strictly inside it exactly when $\lambda(d)$ is strictly below that plane. This is the identity behind the in-circle determinant.

**The lower hull as a function.** Let $K = \mathrm{conv}(\lambda(P))$ and, for $q \in \mathrm{conv}(P)$, let $F(q) = \min\{ z : (q, z) \in K \}$. The graph of $F$ is the lower boundary of $K$. $F$ is convex, because $K$ is convex, and $F(q)$ is the least value of $\sum_i \mu_i |p_i|^2$ over the ways to write $q = \sum_i \mu_i p_i$ with $\mu_i \ge 0$ and $\sum_i \mu_i = 1$.

**Lemma 2.** (a) If $g$ is affine and $g(p) \le |p|^2$ for all $p \in P$, then $g \le F$ on $\mathrm{conv}(P)$. (b) $F(p) = |p|^2$ for every $p \in P$. (c) If $F$ equals an affine function $g$ on a set with nonempty interior, then $g \le F$ on $\mathrm{conv}(P)$.

*Proof.* (a) For $q = \sum_i \mu_i p_i$, $g(q) = \sum_i \mu_i g(p_i) \le \sum_i \mu_i |p_i|^2$; take the least right side. (b) $F(p) \le |p|^2$ by the choice $\mu = $ the unit vector at $p$. The tangent function $g(q) = 2 p \cdot q - |p|^2$ has $|q|^2 - g(q) = |q - p|^2 \ge 0$, so by (a) $F(p) \ge g(p) = |p|^2$. (c) Let $U$ be an open set where $F = g$, take $u \in U$ and $q \in \mathrm{conv}(P)$, and let $\phi(t) = F(u + t (q - u)) - g(u + t (q - u))$ for $t \in [0, 1]$. It is convex, and it is zero for small $t \ge 0$, so it is zero at $0$ with slope $0$ from the right, and by convexity $\phi(1) \ge \phi(0) = 0$. $\square$

**Theorem (Delaunay is the lower hull).** Let $t = abc$ be a triangle with corners in $P$ and $\mathrm{orient}(a, b, c) \ne 0$.

1. $t$ has the [empty circle property](/empty-circle-property/) exactly when $F = g_{abc}$ on $t$, that is, when the lifted triangle lies on the lower boundary of $K$.
2. A triangulation $T$ of $P$ is a Delaunay triangulation exactly when the function that is affine on each triangle of $T$ and equals $|\cdot|^2$ at the points of $P$ is equal to $F$.
3. Let the **Delaunay subdivision** be the projection of the faces of the lower boundary of $K$. Its faces are convex polygons that cover $\mathrm{conv}(P)$ with disjoint interiors, every point of $P$ is a vertex, and the corners of each face are the points of $P$ on one circle with no point of $P$ inside. The Delaunay triangulations of $P$ are exactly the triangulations obtained by cutting each face into triangles with its own corners. In particular, at least one exists, and if no four points of $P$ are on one circle, it is unique.

*Proof.* (1) If $t$ is Delaunay, then $\lambda(p)$ is not strictly below the plane of $t$ for any $p \in P$ by Lemma 1, so $g_{abc} \le |\cdot|^2$ on $P$, and $g_{abc} \le F$ by Lemma 2(a). On $t$, a point $q = \alpha a + \beta b + \gamma c$ has $F(q) \le \alpha |a|^2 + \beta |b|^2 + \gamma |c|^2 = g_{abc}(q)$. So $F = g_{abc}$ on $t$. Conversely, if $F = g_{abc}$ on $t$, Lemma 2(c) and (b) give $g_{abc}(p) \le F(p) = |p|^2$ for every $p \in P$, so no $p$ is strictly inside the circumcircle.

(2) Apply (1) to each triangle of $T$. The interpolating function is $g_{abc}$ on the triangle $abc$, so it equals $F$ on all of $\mathrm{conv}(P)$ exactly when every triangle is Delaunay.

(3) $P$ is not on one line, so $K$ has a lower boundary over the interior of $\mathrm{conv}(P)$, made of faces of $K$ that are not vertical, and it projects one to one onto $\mathrm{conv}(P)$ because it is the graph of $F$. A line meets the paraboloid in at most two points, so no three lifted points are on one line, and every lifted point is a vertex of $K$ by Lemma 2(b) and the tangent function, which touches $\lambda(P)$ only at $\lambda(p)$. Hence each edge of $K$ holds exactly two lifted points, its ends. A lower face lies in a non-vertical plane with all of $K$ on or above it; by Lemma 1 the projected corners are on one circle with no point of $P$ inside. Cutting each lower face into triangles with its corners gives triangles that meet edge to edge, because two faces share only an edge of $K$ or a vertex, and an edge holds no lifted point except its ends; so it is a triangulation of $P$, and by (2) it is Delaunay. Conversely, let $T$ be Delaunay. By (1), each triangle of $T$ lifts into the lower boundary, inside the plane of one lower face, so it is inside that face, and its corners are corners of that face. So $T$ cuts each face into triangles with its own corners. If no four points are on one circle, each face has three corners, since four corners would be cocircular, and the cutting is unique. $\square$

**Voronoi diagrams by tangent planes.** For $p \in P$ let $h_p(q) = 2 p \cdot q - |p|^2$, the tangent plane of the paraboloid at $\lambda(p)$. Then $|q - p|^2 = |q|^2 - h_p(q)$ for every $q$, so $p$ is a nearest site of $q$ exactly when $h_p(q)$ is the largest of the values $h_{p'}(q)$. The [Voronoi diagram](/voronoi-diagram/) is the projection of the upper envelope of the $n$ planes $h_p$, a convex polyhedral surface. The planes $h_p$ and the points $\lambda(p)$ are dual to each other under the polarity of the paraboloid, which is the [Voronoi-Delaunay duality](/voronoi-delaunay-duality/) in space.

**Variants of the same map.**

- **Weights.** Lifting $p$ to height $|p|^2 - w_p$ gives the [regular triangulation](/regular-triangulation/) as the lower hull and the [power diagram](/power-diagram/) as the upper envelope of $h_p + w_p$.
- **Upper hull.** The upper boundary of $K$ projects to the dual of the [farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/), and the lower envelope of the planes $h_p$ gives that diagram itself.
- **Levels.** The $k$-th highest plane among the $h_p$ at $q$ belongs to the $k$-th nearest site, so the cells of the [order-k Voronoi diagram](/order-k-voronoi-diagram/) are the projections of the regions where the set of the $k$ highest planes does not change; they are read off the $k$-level of the arrangement of these planes.
- **Dimension.** In $\mathbb{R}^d$ the map $p \mapsto (p, |p|^2)$ works in the same way, with $d + 1$ coordinates ([higher-dimensional Delaunay](/higher-dimensional-delaunay/)).

## Examples

**One quadrilateral.** Take $(0,0)$, $(4,0)$, $(5,5)$, $(0,4)$. The lifted points are $(0,0,0)$, $(4,0,16)$, $(5,5,50)$, $(0,4,16)$.

| triangle | plane $z = g(q)$ | fourth point | fourth lifted point | circle |
| --- | --- | --- | --- | --- |
| $(0,0), (4,0), (0,4)$ | $z = 4x + 4y$ | $(5,5)$ | $50 > 40$, above | center $(2,2)$, $r^2 = 8$, empty |
| $(4,0), (5,5), (0,4)$ | $z = \frac{17}{3} x + \frac{17}{3} y - \frac{20}{3}$ | $(0,0)$ | $0 > -\frac{20}{3}$, above | center $(\frac{17}{6}, \frac{17}{6})$, $r^2 = \frac{169}{18}$, empty |
| $(0,0), (4,0), (5,5)$ | $z = 4x + 6y$ | $(0,4)$ | $16 < 24$, below | center $(2,3)$, $r^2 = 13$, not empty |

The first two planes form the lower boundary of $K$, and the diagonal from $(4,0)$ to $(0,4)$ is the Delaunay edge. In each row the center is half the coefficients of $x$ and $y$, and $r^2 = c + |o|^2$, as Lemma 1 says: for the last row, $0 + 4 + 9 = 13$.

**A square.** The corners $(0,0)$, $(1,0)$, $(1,1)$, $(0,1)$ lift to points on the plane $z = x + y$, so the lower boundary has one face with four corners. Both diagonals give a Delaunay triangulation, as the theorem says for a face with four cocircular corners. On the $3 \times 3$ integer grid, the lower boundary has four square faces, and there are $2^4 = 16$ Delaunay triangulations.

**Tangent planes.** For sites $(0,0)$ and $(4,0)$, $h_{(0,0)} = 0$ and $h_{(4,0)} = 8x - 16$. The second is larger exactly when $x > 2$, so the bisector is the line $x = 2$.

## Where it is used

- **Delaunay triangulations from 3D hulls.** Any algorithm for the [3D convex hull](/convex-hull-3d/) builds the Delaunay triangulation in the same time, for example $O(n \log n)$ expected time by randomized incremental construction. Many proofs for Delaunay algorithms, such as the correctness of the [Bowyer-Watson algorithm](/bowyer-watson-algorithm/), use the lifted picture.
- **Flips.** Each flip of the [Lawson flip algorithm](/lawson-flip-algorithm/) replaces two lifted triangles by the two lower ones on the same four points, so the lifted surface only goes down. This is why the algorithm stops after at most $\binom{n}{2}$ flips.
- **Exact predicates.** The in-circle test is the orientation test of four lifted points, so one exact determinant routine serves both.
- **Range searching.** A query "which points are in this disc" becomes "which lifted points are below this plane", so [circular range searching](/circular-range-searching/) reduces to halfspace range searching in one dimension more.
- **Weighted and higher-order diagrams.** [Power diagrams](/power-diagram/), [regular triangulations](/regular-triangulation/), [farthest-point](/farthest-point-voronoi-diagram/) and [order-k](/order-k-voronoi-diagram/) diagrams all come from the same picture.

## References
