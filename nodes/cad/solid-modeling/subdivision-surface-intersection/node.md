---
tag: V3H0YK
kind: algorithm
slug: subdivision-surface-intersection
name: Subdivision surface intersection
aliases:
- recursive subdivision intersection
area: cad/solid-modeling
level: core
summary: Intersects two Bezier patches by splitting them with de Casteljau's algorithm and dropping pairs whose boxes do not overlap, until the pieces are flat.
solves: [surface-surface-intersection]
model: real-ram
complexity:
  vars: {k: the number of halvings after which every piece is flat, n: the number of control points of a patch, d: the sum of the two degrees of a patch, r: the number of output leaves}
  time: {worst: O(16^k n d)}
  space: {extra: O(k n + r)}
properties: {deterministic: true, recursive: true, exact: false}
history:
  year: 1980
  people: [J. M. Lane, R. F. Riesenfeld]
  note: Lane and Riesenfeld developed subdivision for Bezier and B-spline curves and surfaces and showed that it gives algorithms for curve and surface intersection and for display.
prereqs: [surface-surface-intersection, bezier-patch, de-casteljau-algorithm, convex-hull-property]
see_also: [marching-surface-intersection, bezier-clipping, curve-intersection, axis-aligned-bounding-box, bounding-volume-hierarchy, interval-arithmetic, orientation-test, catastrophic-cancellation]
sources:
  - paper: doi:10.1109/TPAMI.1980.4766968
    title: J. M. Lane and R. F. Riesenfeld, A theoretical development for the computer generation and display of piecewise polynomial surfaces, IEEE Transactions on Pattern Analysis and Machine Intelligence 2(1), 35 to 46, 1980
    locator: the whole paper (subdivision of Bezier and B-spline curves and surfaces, the convex hull test, and the intersection algorithms that follow from them)
  - paper: doi:10.1109/38.180122
    title: Nicholas M. Patrikalakis, Surface-to-surface intersections, IEEE Computer Graphics and Applications 13(1), 89 to 95, 1993
    locator: the section on subdivision methods and their comparison with marching
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 5, Intersection problems, Section 5.8 on surface to surface intersection, the part on subdivision methods
  - paper: doi:10.1016/0167-8396(88)90029-5
    title: Thomas W. Sederberg and Ray J. Meyers, Loop detection in surface patch intersections, Computer Aided Geometric Design 5(2), 161 to 171, 1988
    locator: the normal cone test, which tells when a pair of pieces from a subdivision can hold no closed loop
---

Subdivision intersects two [Bézier patches](/bezier-patch/) by divide and conquer. It compares the bounding boxes of the two control nets: if they do not overlap, the patches cannot meet, by the [convex hull property](/convex-hull-property/), and the pair is dropped. Otherwise the larger patch is split into four quarters with [de Casteljau's algorithm](/de-casteljau-algorithm/), and the method recurses on the new pairs, until both pieces are flat and their corner triangles can be intersected directly. Lane and Riesenfeld developed the method in 1980, and it is the robust partner of [marching](/marching-surface-intersection/): it never drops a piece that holds an intersection point, but its output is a set of short segments, not an ordered curve.

## In plain words

Two curved sheets are each held inside a box that is easy to compute from their control points. If the two boxes do not touch, the sheets do not touch, and there is nothing more to do. If the boxes touch, cut one sheet into four smaller sheets. Each small sheet has a smaller box, so now more of the empty space can be thrown away.

Keep cutting the pairs that still touch. Pieces become flatter as they get smaller, and when both pieces of a pair are nearly flat, treat them as two flat tiles and intersect the tiles. The little segments from all the tiles, put together, approximate the curve where the sheets cross.

A piece of the curve can never be thrown away, because a box is only dropped when it is empty of the other sheet.

## The problem

The input is two tensor-product Bézier patches $P(u, v)$ and $Q(s, t)$ over $[0, 1]^2$, given by their control nets, and a flatness tolerance $\varepsilon > 0$. The output is a list of *leaves*: pairs of parameter rectangles $(R_P, R_Q)$ whose pieces still overlap, each with the segments where the corner triangles of the two pieces meet. The task is the [surface surface intersection](/surface-surface-intersection/) problem, with the requirement that no intersection point is lost: every point $P(u, v) = Q(s, t)$ must have $(u, v) \in R_P$ and $(s, t) \in R_Q$ for some leaf. Coincident and touching patches are allowed inputs. The page uses exact rational control points, so every comparison is decided without error.

## The algorithm

```pseudo id=main
SUBDIVIDE(P, Q, ε)
L1  if box(P) and box(Q) do not overlap then return          ▷ convex hull property
L2  if P is not flat and (Q is flat or box(P) is at least as large as box(Q)) then
L3      for each quarter P_k of P, by de Casteljau at the midpoints, do SUBDIVIDE(P_k, Q, ε)
L4  else if Q is not flat then
L5      for each quarter Q_k of Q do SUBDIVIDE(P, Q_k, ε)
L6  else intersect the two corner triangles of P with the two of Q
L7      output the leaf (R_P, R_Q) with the segments found at L6
```

The box of a piece is the axis-aligned box of its control points; two boxes overlap when their coordinate ranges overlap in all three axes, with touching counted as overlap. A piece is *flat* when every control point lies within $\varepsilon$ of the plane through three of its corners, $a = P_{00}$, $b = P_{p0}$ and $c = P_{0q}$. The normal of that plane is $n = (b - a) \times (c - a)$, by the right-hand rule, which points the same way as the outward normal $P_u \times P_v$ of the patch. A quarter is computed by splitting each column of the control net at $u = 1/2$ and then each row at $v = 1/2$; the four new nets describe the patch over the four quarters of its rectangle, exactly.

Line L2 splits the piece with the larger box, so the two pieces stay of similar size, and never splits a flat piece. A flat piece is never split again, so a plane patch stays whole. The corner triangles of a piece with corners $a, b, c, d$ are $abc$ and $acd$. Line L6 intersects each triangle of one piece with each triangle of the other by the standard test: the signs of $n_1 \cdot (x - a_1)$ at the vertices of the second triangle, and the other way round, decide whether the planes separate them, and the cut segments are clipped against each other along the line $n_1 \times n_2$. Two coplanar triangles are flagged instead of cut. The implementation also stops at a depth cap and outputs such pieces as leaves marked not flat, so that a degenerate input cannot recurse for ever.

## Example

Let $P$ be the saddle $z = uv$, the bilinear patch with control points $(0, 0, 0)$, $(1, 0, 0)$, $(0, 1, 0)$ and $(1, 1, 1)$, and let $Q$ be the plane patch $z = 1/4$ over the unit square. They meet in the hyperbola arc $uv = 1/4$ for $1/4 \le u \le 1$. Take $\varepsilon = 1/16$. Because $P$ is bilinear, the $z$ range of its box over $[u_0, u_1] \times [v_0, v_1]$ is exactly $[u_0 v_0, u_1 v_1]$, so the trace can be checked by hand.

| level | pairs tested at L1 | dropped | result |
|---|---|---|---|
| 0 | the whole $P$ with $Q$ | 0 | $Q$ is flat; $P$ is not: $(1, 1, 1)$ is at distance $1$ from the plane $z = 0$ of the other corners; split $P$ |
| 1 | four quarters of side $1/2$ | 0 | the $z$ ranges $[0, 1/4]$, $[0, 1/2]$, $[0, 1/2]$ and $[1/4, 1]$ all reach $z = 1/4$; in each quarter the fourth corner is $1/4$ above the plane of the other three in $z$, and more than $1/16$ from it; split all |
| 2 | sixteen pieces of side $1/4$ | 8 | eight boxes reach $z = 1/4$; the fourth corner is now $1/16$ above the plane in $z$, so at most $1/16$ from it, and all eight are flat leaves |

The eight dropped pieces include $[0, 1/4]^2$, with $z \le 1/16$, and $[3/4, 1]^2$, with $z \ge 9/16$. Three kept pieces only touch the plane, at the points $(1/2, 1/2)$, $(1/4, 1)$ and $(1, 1/4)$ of the curve, and are kept because touching counts as overlap. In all, line L1 runs $21$ times and line L6 runs $8 \times 4 = 32$ triangle tests, which give $22$ segments. For the leaf $[1/4, 1/2] \times [1/2, 3/4]$ the segments run from $(1/2, 1/2, 1/4)$ to $(3/8, 5/8, 1/4)$ to $(1/3, 3/4, 1/4)$. The end points are on the curve, and the middle point has $xy = 15/64$, off by $1/64$. With $\varepsilon = 1/64$ and $1/256$ the method keeps $14$ and $26$ leaves of side $1/8$ and $1/16$, and the largest error $|xy - 1/4|$ of a segment point is $1/256$ and $1/1024$, a quarter of $\varepsilon$ in each case.

## Correctness

The pieces of a patch over a rectangle are Bézier patches whose control nets come from de Casteljau's algorithm, and each lies in the convex hull of its control points, because the Bernstein polynomials are nonnegative and sum to one. So if a point $x = P(u, v) = Q(s, t)$ has its parameters in the rectangles of a pair, $x$ is in both boxes, and line L1 does not drop the pair. The four quarters cover the rectangle, so the parameters of $x$ are in one of the new pairs. By induction on the recursion, every intersection point is in the rectangles of an output leaf, whatever the input, as long as the recursion ends. It ends because of the depth cap, and for regular patches, where $P_u \times P_v \ne 0$, it ends without the cap: a piece of side $h$ is within $C h^2$ of its corner plane, so pieces become flat after a bounded number of halvings. In a flat leaf, both pieces lie within $\varepsilon$ of their corner planes. The [full proof](proofs/correctness.md) gives the details.

What is proved is that no intersection point is lost and that the recursion ends. How close the segments are to the true curve is measured on the example, not proved: a leaf can hold no intersection at all, because boxes are larger than the pieces, and its triangles can still meet or miss.

## Complexity

The costs are in the [real RAM](/real-ram/). Splitting a patch with $n$ control points and degrees $p$ and $q$ costs $O(n(p + q)) = O(nd)$, and a box or a flatness test costs $O(n)$. The pair tree has four children at each split, and each of the two patches is split at most $k$ times along a path, so it has at most $16^k$ nodes in the worst case, which gives $O(16^k n d)$ time. This worst case is reached by coincident patches, where every pair overlaps. For two regular patches that cross along a curve, only the pairs near the curve survive, and the number of leaves grows like the length of the curve divided by the side of a leaf, about $\varepsilon^{-1/2}$, as the example shows. The extra space is $O(kn)$ for the recursion and $O(r)$ for the $r$ leaves. With rational arithmetic, each halving adds a few bits to each coordinate.

## Properties

- **Nothing is lost.** Every intersection point is in some leaf, for every input, including touching and coincident patches. This is the main reason to use subdivision.
- **Unordered output.** The leaves come in the order of the recursion, not along the curve. Joining the segments into curves is a separate step.
- **False leaves.** A leaf can hold no intersection, because a box can overlap the other piece while the patch does not. The triangle test of line L6 usually removes such leaves from the curve, since it finds no segment.
- **Exact decisions, approximate curve.** With rational control points every box test and every sign is decided exactly, but the segments are only an approximation of the curve, with error that shrinks like the square of the leaf size.

## Variants and improvements

- **Better bounding volumes.** Axis-aligned boxes are cheap but loose; a large tilted flat patch has a box that covers much empty space. Oriented boxes, slabs normal to a fixed direction, or the convex hull itself drop more pairs. [Bézier clipping](/bezier-clipping/) uses a fat plane around one patch to cut away a range of the other patch's parameters at each step, not just a half.
- **A hierarchy.** Storing the pieces of each patch in a [bounding volume hierarchy](/bounding-volume-hierarchy/) lets one patch be tested against many others, as in a Boolean operation on two models.
- **Hybrid with marching.** Subdivide only until the [loop test](/surface-surface-intersection/) of Sederberg and Meyers shows that no pair holds a closed loop, then intersect the boundaries of the pieces to get start points, and trace the curve with [marching](/marching-surface-intersection/). This gives an ordered, accurate curve that has no missed branch.
- **B-splines and NURBS.** Insert knots to split a B-spline patch into Bézier patches, or split it directly by knot insertion; for rational patches the convex hull property holds when all weights are positive.
- **Interval and exact versions.** In floating point, round the boxes outward with [interval arithmetic](/interval-arithmetic/), so that the convex hull argument still holds.

## When to use it

Use subdivision when no part of the intersection may be missed: to find all components and small loops, to find start points for marching, or for coincident and touching patches, where marching fails. Use [marching](/marching-surface-intersection/) when start points are known and the curve must be accurate and ordered, and use the [problem page](/surface-surface-intersection/) for the full list of methods. Plain subdivision to a fine tolerance is slow and gives a large unordered output, so production systems use it as the first stage of a hybrid.

## Pitfalls

- **Rounding drops pieces.** The convex hull argument holds only if the box contains the control points exactly. A box computed in floating point can be slightly too small and drop a pair that only touches, like the three touching pieces of the example, and the point where they touch is then lost. Round the boxes outward, or use exact arithmetic as here.
- **Signs in the triangle test.** Line L6 branches on the signs of $n_1 \cdot (x - a_1)$, which is an [orientation test](/orientation-test/), and in floating point near-zero values suffer from [catastrophic cancellation](/catastrophic-cancellation/). The fix is exact rational arithmetic, as in the implementation, or a floating-point filter that falls back to exact arithmetic when the value is too close to zero.
- **Degenerate corners.** When three corners of a piece are collinear, for example at a collapsed edge, the corner plane is not defined, the piece is never flat, and the recursion runs to the depth cap. Use the best-fitting plane of the control points, or a cap and a flag as here.
- **Tangential contact.** Where the patches touch along a curve, every pair along it overlaps at every level, and the number of leaves grows like $\varepsilon^{-1}$, not $\varepsilon^{-1/2}$.
- **Gaps between segments.** Segments from adjacent leaves need not share end points, since each leaf uses its own triangles. A curve fit from the segments must join them within a tolerance.

## Implementations

## History

Lane and Riesenfeld published the theory of subdivision for Bézier and B-spline curves and surfaces in 1980, and showed that it gives algorithms for curve and surface intersection as well as for display. Sederberg and Meyers added the loop test in 1988, so that a subdivision could stop as soon as no closed loop could hide in a pair. Patrikalakis's survey of 1993 compared subdivision with lattice, analytic and marching methods and with hybrids that combine them.

## References
