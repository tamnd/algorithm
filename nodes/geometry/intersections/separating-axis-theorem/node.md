---
tag: NQ2MTE
kind: theorem
slug: separating-axis-theorem
name: Separating axis theorem
aliases:
- sat
- separating-axis-test
area: geometry/intersections
level: advanced
summary: Two convex polygons are disjoint exactly when the projections on some edge normal of one of them are disjoint; for polyhedra, face normals and cross products of edges suffice.
prereqs: [convex-set, supporting-hyperplane, dot-product]
see_also: [convex-collision-detection, gjk-algorithm, minkowski-sum-convex-polygons, support-function, convex-polygon-intersection, collision-detection, rotating-calipers, axis-aligned-bounding-box]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 2.5.1, Separating hyperplane theorem (the proof by a closest pair of points, and the strict version for compact sets)
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 5, Section 5.2.1, Separating-axis test (the candidate axes for polygons and polyhedra, and the 15 axes for two oriented boxes)
  - paper: doi:10.1145/237170.237244
    title: Stefan Gottschalk, Ming C. Lin and Dinesh Manocha, OBBTree, a hierarchical structure for rapid interference detection, SIGGRAPH 1996
    locator: the overlap test of two oriented bounding boxes with 15 candidate separating axes
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 13, Section 13.3, Minkowski sums (the edges of the Minkowski sum of two convex polygons come from the edges of the two polygons)
---

The separating axis theorem says that two compact convex sets in $\mathbb{R}^d$ are disjoint if and only if there is a direction $u$, the axis, on which their orthogonal projections are disjoint intervals. For two convex polygons the theorem gives a finite list: it is enough to try the outer normals of the edges of both polygons. For two convex polyhedra the list is the face normals of both and the cross products of an edge direction of one with an edge direction of the other. This turns the overlap test into a finite number of interval comparisons, and it is the standard test for boxes and convex shapes in collision detection.

## Statement

**Notation.** For a nonempty compact set $K \subset \mathbb{R}^d$ and a vector $u$, the *support function* is $h_K(u) = \max_{x \in K} u \cdot x$, and the projection of $K$ on $u$ is the interval $[-h_K(-u), h_K(u)]$ of values $u \cdot x$. An *axis* $u \ne 0$ *separates* $K$ and $L$ if these intervals are disjoint, that is $h_K(u) < -h_L(-u)$ or $h_L(u) < -h_K(-u)$. $K - L = \{x - y : x \in K, y \in L\}$ is the Minkowski difference. A *convex polygon* is the convex hull of finitely many points of $\mathbb{R}^2$ with nonempty interior; its edges have outer normals $n_1, \dots, n_m$.

**Theorem.**

1. (*General form.*) Nonempty compact convex sets $K, L \subset \mathbb{R}^d$ are disjoint if and only if some axis separates them.
2. (*Polygons.*) Convex polygons $P$ and $Q$ are disjoint if and only if some outer edge normal of $P$ or of $Q$ separates them.
3. (*Polyhedra.*) Convex polyhedra $P$ and $Q$ in $\mathbb{R}^3$ with nonempty interior are disjoint if and only if one of these vectors separates them: an outer face normal of $P$ or of $Q$, or $a \times b \ne 0$ for an edge direction $a$ of $P$ and an edge direction $b$ of $Q$.

## In plain words

Two convex shapes do not touch exactly when you can shine a light from some side and see a gap between their shadows on a wall. The direction of the light is the axis. For general convex shapes there are infinitely many directions to try, but for shapes with flat sides only a few directions matter.

For two convex polygons, you only need to try the directions at right angles to the sides of the two polygons. If none of them shows a gap, the polygons overlap. For three-dimensional boxes and other convex solids, you also try the directions at right angles to one edge of each solid.

## Proof

**Lemma 1.** $K \cap L = \emptyset$ if and only if $0 \notin M = K - L$, and $h_M(u) = h_K(u) + h_L(-u)$. So $u$ separates $K$ and $L$ if and only if $h_M(u) < 0$ or $h_M(-u) < 0$.

*Proof.* $x = y$ with $x \in K$, $y \in L$ means $0 = x - y \in M$. The maximum of $u \cdot (x - y)$ over independent $x \in K$, $y \in L$ is $\max u \cdot x + \max (-u) \cdot y$. The condition $h_K(u) < -h_L(-u)$ is $h_M(u) < 0$, and the other condition is the same with $-u$. $\square$

**Proof of 1.** If an axis separates $K$ and $L$, the two projections are disjoint, so the sets are disjoint. Conversely, let $K \cap L = \emptyset$. $M$ is compact and convex, as the image of the compact convex set $K \times L$ under a linear map, and $0 \notin M$ by Lemma 1. Let $m$ be the point of $M$ nearest to $0$, which exists since $M$ is compact; $m \ne 0$. For any $z \in M$ and $t \in (0, 1]$, the point $m + t (z - m)$ is in $M$, so $|m + t (z - m)|^2 \ge |m|^2$, which gives $2 t\, m \cdot (z - m) + t^2 |z - m|^2 \ge 0$, and with $t \to 0$, $m \cdot z \ge |m|^2$. So $h_M(-m) = \max_z (-m \cdot z) \le -|m|^2 < 0$, and the axis $u = -m$ separates $K$ and $L$ by Lemma 1. $\square$

**Lemma 2.** For a convex polygon or polyhedron $M$ with nonempty interior, $0 \notin M$ if and only if $h_M(n) < 0$ for some outer facet normal $n$ of $M$ (an edge normal in the plane, a face normal in space).

*Proof.* Such an $M$ is the intersection of the closed half-spaces $\{x : n \cdot x \le h_M(n)\}$ of its facets, so $0 \notin M$ if and only if $0 = n \cdot 0 > h_M(n)$ for some facet normal $n$. $\square$

**Lemma 3.** For convex polytopes $P$ and $R$ and a vector $u$, the face of $P + R$ where $u \cdot x$ is maximal is $F_P(u) + F_R(u)$, the sum of the faces of $P$ and $R$ where $u \cdot x$ is maximal.

*Proof.* $u \cdot (p + r) = u \cdot p + u \cdot r$ is maximal over $p \in P$, $r \in R$ exactly when both terms are maximal. $\square$

**Proof of 2.** If an edge normal separates, the polygons are disjoint by part 1. Conversely, let $P \cap Q = \emptyset$, and let $M = P + (-Q) = P - Q$; it is a convex polygon with nonempty interior, since $P$ has one. By Lemma 1, $0 \notin M$, and by Lemma 2, $h_M(n) < 0$ for an outer edge normal $n$ of $M$. By Lemma 3 the edge $F_M(n)$ is $F_P(n) + F_{-Q}(n)$. A sum of two points is a point, so one of the two faces is a segment: $n$ is an outer edge normal of $P$, or of $-Q$. The outer edge normals of $-Q$ are the negatives of those of $Q$. By Lemma 1, $h_M(n) < 0$ means that $n$ separates $P$ and $Q$, and an axis separates if and only if its negative does. So an edge normal of $P$ or of $Q$ separates. $\square$

**Proof of 3.** The same argument gives a face normal $n$ of $M = P - Q$ with $h_M(n) < 0$, and the 2-dimensional face $F_M(n) = F_P(n) + F_{-Q}(n)$. A sum of a point or a segment with a point, or of two parallel segments, has dimension at most $1$. So one of three cases holds: $F_P(n)$ is a face of $P$, so $n$ is a face normal of $P$; $F_{-Q}(n)$ is a face of $-Q$, so $\pm n$ is a face normal of $Q$; or both are non-parallel segments, edges with directions $a$ of $P$ and $b$ of $Q$, and then $n$ is orthogonal to both, so $n$ is a positive multiple of $a \times b$ or $-(a \times b)$. In each case the listed vector or its negative is $n$ up to a positive factor, and separates. The converse is part 1. $\blacksquare$

## Consequences

- **A finite test for polygons.** Two convex polygons with $m$ and $k$ edges are disjoint if and only if one of the $m + k$ edge normals separates them. Projecting both polygons on one axis costs $O(m + k)$, so the plain test costs $O((m + k)^2)$; with [rotating calipers](/rotating-calipers/) or the [linear-time polygon intersection](/convex-polygon-intersection/) the decision takes $O(m + k)$.
- **Fifteen axes for two boxes.** Two oriented boxes in 3D have 3 face normals each and 3 edge directions each, so 3 + 3 + 9 = 15 axes decide overlap. Two [axis-aligned boxes](/axis-aligned-bounding-box/) need only the 3 coordinate axes, since all 9 cross products are coordinate axes too.
- **A certificate.** A separating axis is a short proof of disjointness that a simulation can store and test first in the next time step, since objects move little between steps.
- **Penetration depth for polygons.** If no axis separates, the axis of the smallest overlap of the projections gives the minimum translation that separates the polygons, which is the distance from $0$ to the boundary of $P - Q$, by the same Lemma 2.
- **The GJK view.** Part 1 with the Minkowski difference is also the basis of the [GJK algorithm](/gjk-algorithm/), which searches $P - Q$ for the point nearest the origin instead of trying all axes.

## Tightness

- **Convexity is needed.** An L-shaped polygon and a small square in the inner corner of the L can be disjoint while every axis shows overlapping projections, because the projection of the L fills the gap.
- **The edge normals cannot be dropped.** For the triangle $P$ with vertices $(0, 0), (2, 0), (0, 2)$ and the square $Q = [1.5, 2.5]^2$, the only separating axes among the edge normals are $\pm(1, 1)$, the normal of the edge from $(2, 0)$ to $(0, 2)$; the coordinate axes, which are the normals of $Q$ and of the other edges of $P$, show overlap. So both lists, of $P$ and of $Q$, are needed in general.
- **The cross products are needed in 3D.** Two boxes can be close edge to edge so that no face normal separates them, and only an edge cross product does; this is why the box test has 15 axes and not 6.
- **Compactness for strict separation.** For closed convex sets that are not bounded, the projections can be disjoint but touch in the limit, and two disjoint closed convex sets need not have a strictly separating hyperplane: $\{(x, y) : x > 0, y \ge 1 / x\}$ and the half-plane $y \le 0$ have distance $0$.

## History

The separation of disjoint convex sets by a hyperplane goes back to Minkowski's work on convex bodies around 1900 and is a basic tool of convex analysis and optimization. The finite axis lists for polygons and polyhedra follow from the structure of Minkowski sums of polytopes. In computer graphics, Gottschalk, Lin and Manocha used the 15-axis test for oriented bounding boxes in the OBBTree of 1996, and the name "separating axis theorem" became common in game physics, as in Ericson's book of 2005.

## References
