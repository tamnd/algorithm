---
tag: JQJKYF
kind: problem
slug: line-clipping
name: Line clipping
aliases:
- clipping a line segment to a window
area: graphics-and-signals/rasterization
level: intro
summary: Find the part of a line segment that lies inside a rectangular clip window. The answer is empty, one point or one segment.
model: real-ram
complexity:
  vars: {n: the number of segments}
  time: {worst: Θ(n)}
prereqs: [line-line-intersection]
see_also: [cohen-sutherland-line-clipping, liang-barsky-line-clipping, polygon-window-clipping, line-rasterization, graphics-pipeline, half-plane-intersection, sutherland-hodgman, bezier-clipping]
sources:
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Section 3.2.3, Additional Issues (starting at the edge of a clip rectangle), Section 3.11, Clipping in a Raster World, and Section 3.12, Clipping Lines
  - paper: doi:10.1145/357332.357333
    title: You-Dong Liang and Brian A. Barsky, A new concept and method for line clipping, ACM Transactions on Graphics 3(1), 1 to 22 (1984)
    locator: the statement of the problem in parameter form, and the comparison with earlier methods
  - paper: doi:10.1016/0097-8493(78)90021-3
    title: Mike Cyrus and Jay Beck, Generalized two- and three-dimensional clipping, Computers and Graphics 3(1), 23 to 28 (1978)
    locator: clipping a segment against a convex polygon or a convex polyhedron
  - book: "William M. Newman and Robert F. Sproull, Principles of Interactive Computer Graphics, McGraw-Hill, 1973"
    locator: the chapter on clipping and windowing
---

Line clipping asks for the part of a line segment that lies inside a clip window, most often an axis-aligned rectangle. The part is the intersection of two convex sets, so it is empty, one point or one segment. A renderer clips every segment before it draws it, so that it draws no pixel outside the window and does no work for invisible parts. The two classic methods for a rectangle are [Cohen-Sutherland line clipping](/cohen-sutherland-line-clipping/) and [Liang-Barsky line clipping](/liang-barsky-line-clipping/).

## In plain words

You look at a drawing through a window. Some lines in the drawing go past the edge of the window, and you want to see only the parts inside it. For each line you want the first point and the last point where it is inside the window.

Some lines are fully inside, and you keep them as they are. Some are fully outside, and you throw them away. The hard lines go in and out through the sides of the window, and for these you must find where they cross the sides. A line can also miss the window even when its two ends are on different sides of it, because it can pass by a corner.

## Definition

The input is a segment from $P = (x_P, y_P)$ to $Q = (x_Q, y_Q)$ and a window $W = [x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}]$ with $x_{\min} \le x_{\max}$ and $y_{\min} \le y_{\max}$. Write the segment as $P + t\,(Q - P)$ for $t \in [0, 1]$. The output is the set of points of the segment that are in $W$.

A point is in $W$ when it satisfies four linear inequalities, one for each side. Each inequality holds for $t$ in a closed half-line, so the inside parameters form one closed interval $[t_0, t_1]$, or no parameter at all. The output is the segment from $P + t_0 (Q - P)$ to $P + t_1 (Q - P)$, in the direction from $P$ to $Q$. It is a single point when $t_0 = t_1$.

This page uses a closed window: a point on a side of $W$ is inside. With an open window, a segment that only touches the boundary is rejected. The two conventions differ only on the boundary.

The model is the [real RAM](/real-ram/) with exact rational numbers. With rational input, each end point of the output is rational and needs one division. With [IEEE 754](/ieee-754/) floating point, a computed crossing point can fall a little outside the window, or a little inside it, after rounding. A robust program sets the coordinate of the clipped side to the exact boundary value, so that the point is on the side, and it computes only the other coordinate by division. Tests in exact rational or integer arithmetic, or with [interval arithmetic](/interval-arithmetic/), remove the problem.

The window is in continuous coordinates. When the segment is then drawn on a pixel grid, the pixels are point samples at the centers $(i + 1/2, j + 1/2)$, not little squares, as in the OpenGL and Direct3D 10 rules. A clipped segment must start from its exact crossing point. If a program rounds the crossing point to a pixel first and then draws a new line from there, the pixels it draws can differ from the pixels of the full line in the window. Foley and his coauthors discuss this in Section 3.2.3.

## Variants

- **Convex polygon window.** The window is a convex polygon with $m$ sides. Each side gives one inequality in $t$, so the inside parameters are still one interval. The method of Cyrus and Beck solves this case.
- **Three dimensions.** The window is a box or a convex polyhedron, such as the view volume of a camera. A renderer clips in homogeneous coordinates before the perspective divide, against six planes.
- **Concave window.** The output can be many segments, one for each piece of the segment inside the window.
- **External clipping.** The program keeps the parts outside the window, for example to draw around a dialog box.
- **Lines and rays.** The input is an infinite line or a ray in place of a segment. Only the range of $t$ changes.
- **Many segments, one window.** The window is fixed and many segments arrive. Methods can spend more work on the window once, so that each segment costs less.

## Examples

All the examples use the window $W = [0, 10] \times [0, 10]$.

| Segment from $P$ to $Q$ | Output | Comment |
|---|---|---|
| $(2, 3)$ to $(8, 6)$ | $(2, 3)$ to $(8, 6)$ | both end points inside |
| $(11, 2)$ to $(13, 9)$ | empty | both end points right of the window |
| $(-3, -1)$ to $(13, 11)$ | $(0, 5/4)$ to $(10, 35/4)$ | $t_0 = 3/16$, $t_1 = 13/16$ |
| $(-2, 8)$ to $(3, 14)$ | empty | the ends are left and above, and the segment passes the corner |
| $(-5, 5)$ to $(5, 15)$ | the point $(0, 10)$ | the segment touches the corner |
| $(-3, 10)$ to $(13, 10)$ | $(0, 10)$ to $(10, 10)$ | the segment lies on the top side |

The fourth row shows why a simple test of the end points is not enough. The point $(-2, 8)$ is only left of the window, and $(3, 14)$ is only above it. No single side has both points outside it, but the line crosses $x = 0$ at $y = 52/5$, which is above the window, and it crosses $y = 10$ at $x = -1/3$, which is left of it.

## Known algorithms

- [Cohen-Sutherland line clipping](/cohen-sutherland-line-clipping/) gives each end point a 4-bit region code. It accepts or rejects many segments with two bit operations, and cuts the others at one side at a time.
- [Liang-Barsky line clipping](/liang-barsky-line-clipping/) writes the four inequalities in the parameter $t$ and computes $t_0$ and $t_1$ directly, with at most four divisions.
- The Cyrus-Beck method (1978) clips against any convex polygon in $O(m)$ time for $m$ sides, with one inequality for each side. Liang-Barsky is its special case for a rectangle.
- The Nicholl-Lee-Nicholl method (1987) splits the plane around one end point into regions, so that it never computes a crossing point that it later throws away.
- The midpoint subdivision of Sproull and Sutherland (1968) halves the segment again and again. It needs only additions and shifts, and it was built in hardware.

## Bounds

For a rectangle, each segment takes $O(1)$ time, so $n$ segments take $\Theta(n)$ time. Each end point of the output needs at most one division and a constant number of comparisons. For a convex window with $m$ sides, a direct method takes $\Theta(m)$ time for each segment. If the window is stored once as an array of vertices in order, a binary search finds the two crossings of a line in $O(\log m)$ time.

## Reductions

- Line clipping is a linear program in one variable. The values $t_0$ and $t_1$ are the minimum and the maximum of $t$ under four linear constraints and $0 \le t \le 1$. See the [linear programming problem](/linear-programming-problem/).
- The window is the intersection of four half-planes, so line clipping is the intersection of a segment with a [half-plane intersection](/half-plane-intersection/).
- Clipping to one side is the intersection of a segment with a line. See [line-line intersection](/line-line-intersection/).

## Applications

- The [graphics pipeline](/graphics-pipeline/) clips lines to the view volume before the [viewport transform](/viewport-transform/) and [line rasterization](/line-rasterization/).
- [Polygon window clipping](/polygon-window-clipping/) uses the clipping of one edge against one side as its basic step. The [Sutherland-Hodgman algorithm](/sutherland-hodgman/) in geometry does this for each side in turn.
- Window systems, maps and CAD programs clip lines to the visible area. The general Boolean operations on two polygons are a different problem: see [polygon clipping](/polygon-clipping/).

[Bézier clipping](/bezier-clipping/) shares only the word. It is a method that finds the intersections of a curve with a line or another curve, and it does not cut segments to a window.

## References
