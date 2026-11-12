---
tag: QY3NX9
kind: problem
slug: polygon-window-clipping
name: Polygon window clipping
aliases:
- polygon clipping to rectangle
area: graphics-and-signals/rasterization
level: core
summary: Cut a polygon to an axis-aligned rectangle, the window, so that only the part inside the window remains and can be filled.
model: real-ram
complexity:
  vars: {n: the number of polygon vertices}
  time: {worst: Θ(n)}
prereqs: [polygon, line-clipping]
see_also: [sutherland-hodgman, polygon-clipping, line-clipping, convex-polygon-intersection, weiler-atherton-algorithm, polygon-scan-conversion, triangle-rasterization, nonzero-winding-rule]
sources:
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Section 3.14, Clipping Polygons, and Section 19.1, Clipping
  - paper: doi:10.1145/360767.360802
    title: Ivan E. Sutherland and Gary W. Hodgman, Reentrant polygon clipping, Communications of the ACM 17(1), 32 to 42 (1974)
    locator: the clipping of a polygon against one window side at a time, and the pipeline of clipping stages
  - paper: "You-Dong Liang and Brian A. Barsky, An analysis and algorithm for polygon clipping, Communications of the ACM 26(11), 868 to 877 (1983)"
    locator: the clipping of a polygon to an upright rectangle by the parameters of its edges
  - paper: doi:10.1145/274363.274364
    title: Günther Greiner and Kai Hormann, Efficient clipping of arbitrary polygons, ACM Transactions on Graphics 17(2), 71 to 83 (1998)
    locator: Section 1 (the clipping of a polygon to a convex window, and the degenerate edges it can leave)
---

Polygon window clipping asks for the part of a polygon that lies inside an axis-aligned rectangle, the window. The result is a region, often with more than one piece, and its boundary has parts of the polygon edges, parts of the window sides, and window corners. Renderers clip each polygon to the window or the view volume before [polygon scan conversion](/polygon-scan-conversion/), so that no work is spent on pixels outside it. It is the special case of [polygon clipping](/polygon-clipping/) in geometry where the clip polygon is a rectangle.

## In plain words

You have a shape with straight sides, and you look at it through a window. You want the shape that you see: the part inside the window, with new sides where the window cuts it.

Clipping each side of the shape as a separate line is not enough. Where the shape covers a corner of the window, the corner must become a corner of the result, but no side of the shape passes through it. And a shape that goes out of the window and comes back in can leave two or more separate pieces.

## Definition

The input is a polygon $P$, given as one or more closed lists of vertices, and a window $W = [x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}]$. The polygon can be concave, can have holes, and can cross itself. Its inside is the set of points that a fill rule marks: the [even-odd fill rule](/even-odd-fill-rule/) or the [nonzero winding rule](/nonzero-winding-rule/). The output is a polygon $P'$ whose inside, under the same rule, is the inside of $P$ intersected with $W$.

Two output forms are in use:

- **Separate pieces.** $P'$ is a list of simple polygons, one for each connected piece, with holes where needed. This is the form for outlines, area computations and later Boolean operations.
- **One list with bridges.** $P'$ is one closed list for each input list. Where the result has several pieces, the list runs along a window side from one piece to the next and back, so two of its edges lie on top of each other. The winding number of $P'$ equals that of $P$ at each point inside $W$ that is off the boundary, so a filler gives the right pixels, but an outline shows the bridges.

The model is the [real RAM](/real-ram/). With rational vertices and a rational window, each new vertex is rational and needs one division. With [IEEE 754](/ieee-754/) floating point, a new vertex can be a little outside the window; a robust program sets its coordinate on the window side to the exact boundary value.

For rasterization, the pixels are point samples at the centers $(i + 1/2, j + 1/2)$, as in the OpenGL and Direct3D 10 rules. When the window is the image rectangle, each pixel center is strictly inside it, so clipping before [polygon scan conversion](/polygon-scan-conversion/) changes no pixel. It only removes work.

## Variants

- **Convex window.** The window is a convex polygon with $m$ sides, as for a viewport after a rotation.
- **View volume.** In three dimensions the window is the view frustum, and the renderer clips triangles in homogeneous coordinates before the divide. Each clip plane adds at most one vertex to a convex polygon, so a triangle clipped by six planes has at most nine vertices.
- **Guard band.** A GPU can skip the side planes and rasterize inside a larger rectangle, the guard band, and clip only against the near plane and the band.
- **Exterior clipping.** The program keeps the part outside the window.
- **Arbitrary clip polygon.** The window is any polygon. This is the general [polygon clipping](/polygon-clipping/) problem of geometry, with union, intersection and difference.

## Examples

All examples use the window $W = [0, 10]^2$ unless they say otherwise.

**A triangle over a corner.** Clip the triangle with vertices $(-2, -2)$, $(13, 3)$ and $(3, 13)$, of area 100. No vertex of the triangle is in $W$. The result is the heptagon $(2, 10)$, $(0, 4)$, $(0, 0)$, $(4, 0)$, $(10, 2)$, $(10, 6)$, $(6, 10)$, of area 80. Six of its vertices are crossings of triangle edges with window sides, and $(0, 0)$ is a window corner inside the triangle.

**A U shape that leaves two pieces.** Clip the U shape $(1, 1)$, $(9, 1)$, $(9, 9)$, $(7, 9)$, $(7, 3)$, $(3, 3)$, $(3, 9)$, $(1, 9)$ to the window $[0, 10] \times [5, 10]$. In separate pieces, the result is the two rectangles $[1, 3] \times [5, 9]$ and $[7, 9] \times [5, 9]$, of total area 16. In one list, the result is $(1, 5)$, $(9, 5)$, $(9, 9)$, $(7, 9)$, $(7, 5)$, $(3, 5)$, $(3, 9)$, $(1, 9)$. Its edges from $(1, 5)$ to $(9, 5)$ and from $(7, 5)$ to $(3, 5)$ overlap between $x = 3$ and $x = 7$: this is the bridge. The shoelace area of the list is also 16, because the bridge has no area.

**Fully inside and fully outside.** A polygon inside $W$ is its own result. A polygon whose vertices are all left of $W$ has an empty result. A polygon that contains $W$ gives $W$ itself, with four corners and no vertex of the input.

## Known algorithms

- The [Sutherland-Hodgman algorithm](/sutherland-hodgman/) clips the polygon against one window side at a time and gives one list with bridges. Against a rectangle it takes $O(n)$ time. Its page in geometry has the details and the proofs.
- The polygon method of Liang and Barsky (1983) uses the entering and leaving parameters of each edge, as in [Liang-Barsky line clipping](/liang-barsky-line-clipping/), and adds window corners where the boundary turns around one.
- The [Weiler-Atherton algorithm](/weiler-atherton-algorithm/), the [Greiner-Hormann algorithm](/greiner-hormann-algorithm/) and [Vatti clipping](/vatti-clipping/) handle any clip polygon and give separate pieces.
- For a convex input polygon, the result is a [convex polygon intersection](/convex-polygon-intersection/), with no bridges.

## Bounds

Reading the input takes $\Omega(n)$ time. Against a rectangle, the exact result has at most $3n + 4$ vertices: at most $n$ input vertices, at most two crossings for each edge, because an edge meets the boundary of a convex window in at most two points, and at most four window corners. Sutherland-Hodgman reaches $\Theta(n)$ time for a rectangle. For a convex window with $m$ sides, one side at a time gives $O(nm^2)$ time in the worst case for a general input, because bridges can pick up window corners at each stage; see the [Sutherland-Hodgman](/sutherland-hodgman/) page.

## Reductions

- Clipping one polygon edge to one window side is [line clipping](/line-clipping/) against a half-plane.
- Polygon window clipping is the intersection case of [polygon clipping](/polygon-clipping/) with a rectangle as the second polygon.
- A scanline filler can do the clipping itself: [scanline polygon fill](/scanline-polygon-fill/) skips rows outside the image and cuts each span to the image columns. This gives the same pixels as clipping first.

## Applications

- The [graphics pipeline](/graphics-pipeline/) clips triangles to the view volume before [triangle rasterization](/triangle-rasterization/).
- Window systems and map viewers clip filled shapes to the visible area.
- Tiled renderers clip or bin polygons to screen tiles, and printers clip a page to the printable area.

## References
