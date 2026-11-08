---
tag: GRDZEW
kind: definition
slug: upper-and-lower-hull
name: Upper and lower hull
aliases:
- upper hull
- lower hull
- upper convex hull
- lower convex hull
area: geometry/convex-hulls
level: intro
summary: The two monotone chains of a planar hull between its leftmost and rightmost points.
prereqs: [convex-hull, orientation-test]
see_also: [andrew-monotone-chain, kirkpatrick-seidel, divide-and-conquer-convex-hull, dynamic-convex-hull, convex-hull-trick, support-function, paraboloid-lifting-map, supporting-hyperplane]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 1, Section 1.1 (the upper hull and the lower hull in the incremental hull algorithm), and Chapter 8, Section 8.2, Duality
  - paper: doi:10.1016/0020-0190(79)90072-3
    title: A. M. Andrew, Another efficient algorithm for convex hulls in two dimensions, Information Processing Letters 9(5), 1979
    locator: the whole paper (the hull computed as an upper and a lower chain)
  - paper: doi:10.1137/0215021
    title: David G. Kirkpatrick and Raimund Seidel, The ultimate planar convex hull algorithm?, SIAM Journal on Computing 15(1), 1986
    locator: the reduction of the hull to the upper hull and the lower hull
---

The upper hull of a finite planar point set $P$ is the part of the boundary of its [convex hull](/convex-hull/) that goes from the leftmost point to the rightmost point over the top, and the lower hull is the part that goes along the bottom. Each chain is monotone in $x$, so its vertices sorted by $x$ are already in boundary order, and the full hull is the lower hull followed by the reversed upper hull. Many planar hull algorithms compute the two chains separately because a chain needs only one kind of turn test and has no wrap-around.

## Definition

Notation: $P$ is a finite set of $n$ points $p = (x, y)$ in the plane, $h$ is the number of vertices of $\operatorname{conv} P$, and $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive for a counterclockwise turn (see [orientation test](/orientation-test/)). Points are compared lexicographically: $p < q$ when $p_x < q_x$, or $p_x = q_x$ and $p_y < q_y$.

Let $P$ have at least two distinct points, and let $a$ and $b$ be the lexicographically smallest and largest points of $P$. Both are vertices of $\operatorname{conv} P$, and they split its boundary into two paths from $a$ to $b$.

- The **lower hull** of $P$ is the path from $a$ to $b$ that runs counterclockwise around $\operatorname{conv} P$. Its vertices, from $a$ to $b$, are increasing in lexicographic order, and each three consecutive vertices have $\mathrm{orient} > 0$.
- The **upper hull** of $P$ is the path from $a$ to $b$ that runs clockwise around $\operatorname{conv} P$. Its vertices, from $a$ to $b$, are increasing in lexicographic order, and each three consecutive vertices have $\mathrm{orient} < 0$.

If all points of $P$ are collinear, both chains are the segment $ab$. Otherwise the vertex counts satisfy $h = h_U + h_L - 2$, since $a$ and $b$ are on both chains.

**As functions.** For $x$ between $a_x$ and $b_x$, let $U(x) = \max\{y : (x, y) \in \operatorname{conv} P\}$ and $L(x) = \min\{y : (x, y) \in \operatorname{conv} P\}$. Then $U$ is concave, $L$ is convex, both are piecewise linear, and $\operatorname{conv} P = \{(x, y) : a_x \le x \le b_x,\ L(x) \le y \le U(x)\}$. The upper hull is the graph of $U$, and the lower hull is the graph of $L$, except for vertical sides: if several points of $P$ have $x = a_x$, the vertical side at the left end belongs to the upper hull, and if several have $x = b_x$, the vertical side at the right end belongs to the lower hull. This follows from the lexicographic choice of $a$ and $b$.

**Edge test.** For $p < q$ in $P$, the segment $pq$ lies on the upper hull if and only if $\mathrm{orient}(p, q, r) \le 0$ for every $r \in P$, that is, no point of $P$ lies strictly above the line through $p$ and $q$ (strictly to its left for a vertical line). It is an edge between consecutive vertices if, in addition, every $r$ with $\mathrm{orient}(p, q, r) = 0$ lies on the closed segment $pq$. The lower hull has the same test with $\ge 0$. This is the triple check that tests of planar hull programs use.

*Proof.* If all points are on or below the line $\ell$ through $p$ and $q$, then $\ell$ is a [supporting line](/supporting-hyperplane/) of $\operatorname{conv} P$, so $\operatorname{conv} P \cap \ell$ is a segment of the boundary, and it contains $pq$. The outer normal of $\ell$ points up (or left for a vertical $\ell$), so this boundary segment is on the clockwise path from $a$ to $b$. Conversely, an edge of the upper hull lies on a supporting line with $\operatorname{conv} P$ below it. $\square$

**Directions.** A point $p \in P$ other than $a$ and $b$ is a vertex of the upper hull if and only if $p$ is the only maximizer of $\langle u, \cdot \rangle$ over $P$ for some direction $u$ with $u_y > 0$. So the upper hull is the set of points that the [support function](/support-function/) $h_P(u)$ reaches for directions that point up.

**Duality.** Map the point $p = (p_x, p_y)$ to the line $p^* : y = p_x\, x - p_y$. For each $x$, $\min_{p \in P} (p_x\, x - p_y) = -h_P(-x, 1)$, so the lower envelope of the dual lines is the support function in the upward directions. If no two points of $P$ share an $x$-coordinate, the lines on the lower envelope, from left to right, are the duals of the upper hull vertices from right to left, and the envelope breaks from $p^*$ to $q^*$ at $x$ equal to the slope of the hull edge $pq$. The lower hull corresponds in the same way to the upper envelope. This is the link between hulls and the [convex hull trick](/convex-hull-trick/).

## Examples and non-examples

- **A worked set.** Let $P = \{(0,2), (1,5), (2,1), (3,3), (4,6), (5,0), (6,4), (7,2), (3,-1)\}$. Then $a = (0,2)$ and $b = (7,2)$.
  - Upper hull: $(0,2), (1,5), (4,6), (6,4), (7,2)$, so $h_U = 5$.
  - Lower hull: $(0,2), (3,-1), (5,0), (7,2)$, so $h_L = 4$, and $h = 5 + 4 - 2 = 7$.
  - The edge test over all pairs $p < q$ finds exactly the four upper edges $(0,2)(1,5)$, $(1,5)(4,6)$, $(4,6)(6,4)$ and $(6,4)(7,2)$.
  - $U(0) = 2$, $U(2) = 16/3$, $U(3) = 17/3$, $U(5) = 5$ and $U(7) = 2$.
- **Duality on the same set.** The lower envelope of the lines $y = p_x x - p_y$ is attained by the line of $(7,2)$ at $x = -3$ (value $-23$), of $(4,6)$ at $x = 0$ (value $-6$), of $(1,5)$ at $x = 1$ and $x = 2$, and of $(0,2)$ at $x = 5$ (value $-2$). At $x = -1$, the lines of $(4,6)$ and $(6,4)$ tie at $-10$, because the hull edge between them has slope $-1$. The interior points $(2,1)$, $(3,3)$ and the lower-hull points never attain it.
- **Vertical sides.** For the rectangle corners $(0,0)$, $(4,0)$, $(0,2)$, $(4,2)$ with extra points $(2,0)$, $(2,2)$ and $(2,1)$, the lower hull is $(0,0), (4,0), (4,2)$ and the upper hull is $(0,0), (0,2), (4,2)$. The left side is upper and the right side is lower, and the collinear points $(2,0)$ and $(2,2)$ are not vertices.
- **Non-example: the top point at each $x$.** In the worked set, $(3,3)$ is the highest point with $x = 3$, but it is not on the upper hull, since $U(3) = 17/3 > 3$. The upper hull is not the set of column maxima.
- **Non-example: a split at other vertices.** In the worked set, the counterclockwise boundary path from the lowest point $(3,-1)$ to the highest point $(4,6)$ is $(3,-1), (5,0), (7,2), (6,4), (4,6)$. It is monotone in $y$ but not in $x$, since $x$ goes up to $7$ and back down to $4$. Only the split at the lexicographic extremes $a$ and $b$ gives two $x$-monotone chains.

## Related definitions

- [Convex hull](/convex-hull/) and [convex hull problem](/convex-hull-problem/): the full boundary, which is the lower hull followed by the reversed upper hull.
- [Andrew's monotone chain](/andrew-monotone-chain/): sorts once and builds each chain with a stack.
- [Kirkpatrick-Seidel algorithm](/kirkpatrick-seidel/) and [divide-and-conquer hull](/divide-and-conquer-convex-hull/): find the bridges of the upper hull and the lower hull.
- [Dynamic convex hull](/dynamic-convex-hull/): keeps the upper hull and the lower hull in two separate trees.
- [Support function](/support-function/) and [convex hull trick](/convex-hull-trick/): the upper hull answers maximum queries in upward directions, and a lower envelope of lines is its dual.
- [Paraboloid lifting map](/paraboloid-lifting-map/): the lower hull of lifted points one dimension up gives the Delaunay triangulation.

## References
