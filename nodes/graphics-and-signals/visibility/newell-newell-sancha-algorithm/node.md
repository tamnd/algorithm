---
tag: GJTAMY
kind: algorithm
slug: newell-newell-sancha-algorithm
name: Newell-Newell-Sancha algorithm
aliases:
- Newell's algorithm
- Newell-Newell-Sancha depth sort
area: graphics-and-signals/visibility
level: advanced
summary: A depth sort that tests pairs of polygons whose depth ranges overlap, moves a polygon forward when it must be painted earlier, and splits polygons in a cycle, then paints back to front.
solves: [hidden-surface-removal]
model: real-ram
complexity:
  vars: {n: the number of polygons, m: the number of fragments after the splits, P: "the number of covered pixels, summed over all fragments"}
  time: {worst: O(m^3 + P), best: Θ(n^2 + P)}
  space: {extra: Θ(m)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1972
  people: [Martin E. Newell, Richard G. Newell, Tom L. Sancha]
  note: Newell, Newell and Sancha gave the method at the ACM Annual Conference in 1972. It sorts by depth, repairs the order with a sequence of cheap tests, and splits polygons where no order exists.
prereqs: [painters-algorithm, convex-polygon, hidden-surface-removal]
see_also: [bsp-tree-visibility, bsp-tree, z-buffer, warnock-algorithm, watkins-scanline-algorithm, object-space-vs-image-space, separating-axis-theorem, sutherland-hodgman]
sources:
  - paper: doi:10.1145/800193.569954
    title: M. E. Newell, R. G. Newell and T. L. Sancha, A solution to the hidden surface problem, Proceedings of the ACM Annual Conference 1972, pages 443 to 450
    locator: the whole paper
  - paper: doi:10.1145/356625.356626
    title: Ivan E. Sutherland, Robert F. Sproull and Robert A. Schumacker, A characterization of ten hidden-surface algorithms, ACM Computing Surveys 6(1), 1974, pages 1 to 55
    locator: the section on the Newell, Newell and Sancha algorithm
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, 1990
    locator: Chapter 15, Section 15.5 (list-priority algorithms, the depth-sort algorithm)
---

The Newell-Newell-Sancha algorithm is a [painter's algorithm](/painters-algorithm/) that repairs the depth order before it paints. It sorts the polygons by their farthest depth. Then it tests the farthest polygon $P$ against each polygon $Q$ that $P$ could hide, with a sequence of tests from cheap to expensive. If $P$ hides a part of $Q$, the method moves $Q$ forward, and if the polygons form a cycle, it splits one of them along the plane of another. The output is a valid back-to-front order of fragments, so the painted image is correct at each pixel. The method is from 1972 and is one of the first [hidden surface](/hidden-surface-removal/) methods that is correct for each scene of planar polygons.

## In plain words

The plain painter's algorithm sorts the pieces of a scene from far to near and paints them in that order. This fails when two pieces overlap in depth, because one number per piece cannot tell which piece is in front.

This method checks the order before it paints. It takes the piece at the far end of the list and asks: does this piece cover a part of a later piece from the front? A series of quick questions usually gives the answer "no". Then the piece is painted. If the answer is "yes", the later piece must be painted first, so it goes to the front of the list. If the pieces go round in a ring, no order is correct. Then the method cuts one piece in two along the plane of another piece, and it tries again with the smaller pieces.

## The problem

The input is a list of $n$ planar [convex polygons](/convex-polygon/) in screen space, and an image of $W \times H$ [pixels](/pixel/). The viewer looks down the $z$ axis from $z = +\infty$, so a larger $z$ is nearer. The plane of each polygon is not parallel to the $z$ axis, so it has a depth $z_p(x, y)$ over its projection. Pixel $(i, j)$ is a point sample at $(i + \tfrac12, j + \tfrac12)$, and a polygon covers it when the sample lies in the closed projection of the polygon. The output is, at each pixel, a polygon of largest depth among those that cover it, or the background.

Write $f \succ g$ (*$f$ obscures $g$*) when there is a point $c$ in both closed projections with $z_f(c) > z_g(c)$. An order is *valid* when no fragment obscures a later fragment. The method makes a valid order of fragments of the input polygons; then painting in that order solves the problem.

## The algorithm

Each polygon has a plane $n \cdot X = d$ with $n_z > 0$, so $n \cdot v - d > 0$ means that the point $v$ is on the side of the viewer. For the front polygon $P$ and another polygon $Q$, the tests below run in order. Each test that is true proves that $P$ does not obscure $Q$, and stops the sequence.

- **T0.** The farthest depth of $Q$ is at least the nearest depth of $P$.
- **T1, T2.** The $x$ extents, or the $y$ extents, of $P$ and $Q$ do not meet.
- **T3.** Each vertex of $P$ is on the far side of the plane of $Q$, or on it.
- **T4.** Each vertex of $Q$ is on the near side of the plane of $P$, or on it.
- **T5.** The projections of $P$ and $Q$ do not meet. The implementation clips the projection of $P$ by the edges of $Q$, as in [Sutherland-Hodgman](/sutherland-hodgman/); a [separating axis](/separating-axis-theorem/) test also works.
- **T6.** At each vertex of the common projection, $z_P \le z_Q$.

If T0 to T6 are all false, then $P \succ Q$. Tests T0 to T5 are those of Newell, Newell and Sancha. Test T6 is an exact final test that this page adds: the difference $z_P - z_Q$ is an affine function, so its maximum on the convex common region is at a vertex. With T6, the relation that the tests compute is exactly $\succ$, and the proofs below are short.

```pseudo id=main
NEWELL-NEWELL-SANCHA(polygons, W, H)
L1  L ← the polygons sorted by their farthest depth, farthest first; no polygon is marked
L2  while L is not empty do
L3      P ← the first element of L
L4      Q ← the first element of L after P with P ≻ Q, by the tests T0 to T6, or none
L5      if Q is none then move P from L to the output; continue
L6      if (Q is behind the plane of P, or P is in front of the plane of Q) and Q is not marked then
            mark Q, move Q to the front of L; continue                ▷ reorder
L7      if Q crosses the plane of P then replace Q in L by its two pieces
L8      else if P crosses the plane of Q then replace P in L by its two pieces
L9      else split some R in L that crosses the plane of another S in L, by the plane of S
L10     unmark all elements of L
L11 paint the output from the first to the last element
```

Line L6 is the *swap test*: it checks that $Q$ may go before $P$. A mark records that $Q$ was moved to the front once. If a marked polygon must move again, the polygons in front form a cycle, and lines L7 to L9 split a polygon. "Crosses the plane" means that the polygon has a vertex strictly on each side, so both pieces have positive area. Line L9 is a fallback for a cycle in which $P$ and $Q$ do not cross the plane of each other; some other pair then crosses. Line L10 clears the marks after each split, because the old cycle may be gone. Line L11 is the painting of the [painter's algorithm](/painters-algorithm/).

## Example

Take an image of $8 \times 6$ pixels and two rectangles that cross. $A$ has the corners $(0, 0)$ to $(8, 6)$ on the plane $z = y$, and $B$ has the same corners on the plane $z = 6 - y$. They meet on the line $y = 3$, $z = 3$. Both have the farthest depth 0, and the stable sort keeps $A$ first.

| step | list L | action |
|---|---|---|
| 1 | A, B | T0 to T6 fail for $(A, B)$: at $(0, 6)$, $z_A = 6 > z_B = 0$. The swap test fails, because $B$ crosses the plane of $A$. Line L7 splits $B$ into $B_f$ (the part $y \le 3$, in front of the plane of $A$) and $B_b$ (the part $y \ge 3$) |
| 2 | A, $B_f$, $B_b$ | $A \succ B_b$; the swap test passes, so $B_b$ is marked and moved to the front |
| 3 | $B_b$\*, A, $B_f$ | $B_b$ obscures nothing later: output $B_b$ |
| 4 | A, $B_f$ | T4 is true: $B_f$ is in front of the plane of $A$. Output $A$ |
| 5 | $B_f$ | output $B_f$ |

The order is $B_b, A, B_f$. The painted image shows $B$ in the rows $j = 0, 1, 2$, where $z_B = 6 - y > y$, and $A$ in the rows $j = 3, 4, 5$. This is equal to a per-pixel depth test.

The failure of the plain sort on the [painter's algorithm](/painters-algorithm/) page needs no split. There $D$ lies on $z = x$ and the square $E$ is at $z = 5$. The list is $D, E$. Test T6 finds $z_D = 7 > 5$ at the vertex $(7, 1)$ of the common region, so $D \succ E$. The swap test passes: the vertices of $E$ with $x = 5$ are on the plane of $D$ and those with $x = 7$ are behind it. So $E$ is marked and goes to the front, and the order is $E, D$.

For the three strips of that page that overlap in a cycle, the method makes two splits. The output has 5 fragments, and the painted image is correct.

## Correctness

The tests T0 to T6 decide $P \succ Q$ exactly. The invariant is that no output fragment obscures a later output fragment or a fragment that is still in $L$. Line L5 keeps it, because $P$ obscures no fragment of $L$, and a split keeps it, because a piece of $g$ is obscured only if $g$ is. The marked fragments form a prefix of $L$, and each one is obscured by the next one. So a marked $Q$ at line L4 closes a cycle $Q \succ \cdots \succ P \succ Q$. A set of fragments in which no fragment crosses the plane of another has a valid order, by an autopartition as in a [BSP tree](/bsp-tree/). So in a cycle some fragment crosses the plane of another, and lines L7 to L9 can always split. Each fragment is a union of faces of the arrangement of the other planes in its plane, so the number of splits is finite, and between two splits each fragment is moved at most once. The full proofs are below.

## Complexity

Let $m$ be the number of fragments at the end. A fragment of polygon $p$ is a union of faces of the arrangement of at most $n - 1$ lines in the plane of $p$, and such an arrangement has at most $1 + (n-1) + \binom{n-1}{2}$ faces. So $m = O(n^3)$. This worst case needs many polygons that cross the planes of others; for most scenes $m$ is close to $n$.

Each iteration of the loop tests $P$ against at most $m - 1$ fragments. The proof bounds the number of iterations by $O(m^2)$: at most $m$ splits, and at most $m$ moves and $m$ outputs between two splits. So the time of the loop is $O(m^3)$ tests in the worst case, and each test takes time linear in the number of vertices. When no two depth ranges overlap, each front polygon passes test T0 against all others, and the time is $\Theta(n^2)$ tests plus the sort. The original method keeps the list in order of farthest depth and tests $P$ only against the polygons that follow it in that order while their farthest depth is less than the nearest depth of $P$; then this case takes $\Theta(n \log n)$ time. The painting of line L11 takes time proportional to $P$, the number of covered pixels summed over the fragments, with scan conversion.

The extra space is $\Theta(m)$ for the list and the fragments.

## Properties

- **Exact.** In exact arithmetic the output is correct at each pixel, for each scene of planar convex polygons. With floating point, the side tests near a plane need a tolerance, and the splits create new vertices with rounding errors.
- **Object space.** The tests and splits work on polygons, and the result does not depend on the resolution. Only line L11 uses pixels. See [object space and image space](/object-space-vs-image-space/).
- **View dependent.** The order is valid only for the viewpoint of the screen space transform. A new viewpoint needs a new run.
- **Back to front.** The order can blend translucent polygons in the correct order, which a [z-buffer](/z-buffer/) cannot do.

## Variants and improvements

- **Other key choices.** Sort by the nearest depth, or by the centroid depth. The tests repair the order in each case.
- **Only the conservative tests.** Without test T6, the tests T0 to T5 can report that $P$ may obscure $Q$ when the polygons only touch, or when $Q$ is nearer at each common point. Such false reports can make a cycle in which no polygon crosses the plane of another, so no split helps. The proofs on this page then do not apply, and an implementation needs an extra rule for this case. Test T6 costs one clip, so it is cheap to add.
- **BSP trees.** Build a [BSP tree](/bsp-tree/) once with the splits, and get a valid order for each viewpoint by a traversal. See [BSP tree visibility](/bsp-tree-visibility/). This replaces the tests at each frame by one test per node.
- **Front to back.** Reverse the order, and write only pixels that are still empty. See the variants of the [painter's algorithm](/painters-algorithm/).

## When to use it

Use the method when you need an exact back-to-front order for one viewpoint, for example to blend translucent polygons, to make vector output such as PostScript or SVG with no depth buffer, or for a plotter. For interactive rendering of an opaque scene, use the [z-buffer](/z-buffer/). For a static scene and a moving viewer, use a [BSP tree](/bsp-tree-visibility/).

## Pitfalls

- **Moving a polygon forward more than once.** If line L6 does not check the mark, two polygons in a cycle swap again and again, and the loop does not stop. Check the mark, and split when a marked polygon must move.
- **Splitting by the wrong plane.** When the swap test fails, $Q$ crosses the plane of $P$, so line L7 splits $Q$ by the plane of $P$. A split of $Q$ by an unrelated plane does not remove the overlap with $P$.
- **Strict and closed side tests.** Tests T3 and T4 must accept a vertex on the plane. With strict tests, two faces of a mesh that share an edge fail T3 and T4, and the method does slow tests, or splits without need, for each such pair.
- **Touching polygons in tests T1, T2 and T5.** If the extents touch, the closed projections meet, and a pixel sample on the common edge is covered by both. Report "the projections meet" in this case, or a pixel on the edge can get the wrong polygon.
- **Rounding in the splits.** A new vertex from a split in floating point is not on the plane of the cut. Use a tolerance in the side tests, or exact arithmetic as in the implementation.

## Implementations

## History

Martin Newell, Richard Newell and Tom Sancha published the method in 1972, when they worked at the CADCentre in Cambridge. Their paper gave the depth sort, the tests on the extents, the planes and the projections, and the split of polygons that overlap in a cycle. Sutherland, Sproull and Schumacker described it in 1974 in their survey of ten hidden surface algorithms, as a priority method that works mostly in object space. Fuchs, Kedem and Naylor in 1980 moved the splits to a preprocessing step with the [BSP tree](/bsp-tree/).

## References
