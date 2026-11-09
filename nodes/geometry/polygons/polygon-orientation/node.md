---
tag: 2K9ZKE
kind: concept
slug: polygon-orientation
name: Polygon orientation
aliases:
- winding order
- clockwise and counterclockwise orientation
- signed area sign
- vertex order of a polygon
area: geometry/polygons
level: intro
summary: Whether a polygon's vertices are listed clockwise or counterclockwise, determined by the sign of its signed area.
prereqs: [simple-polygon, orientation-test, shoelace-formula]
see_also: [shoelace-formula, orientation-test, polygon-with-holes, winding-number-algorithm, convex-hull, sutherland-hodgman, ear-clipping, nonzero-winding-rule]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.3, the area of a polygon as a signed sum, positive for counterclockwise order
  - url: https://www.rfc-editor.org/rfc/rfc7946
    title: H. Butler and others, The GeoJSON Format, RFC 7946, 2016
    locator: Section 3.1.6, Polygon (exterior rings counterclockwise and holes clockwise, the right-hand rule)
  - book: isbn:9780201848403
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 15, back-face culling by the orientation of a projected polygon
---

The orientation of a [simple polygon](/simple-polygon/) says in which direction its vertex list goes around it: counterclockwise, with the inside on the left of every edge, or clockwise, with the inside on the right. It is the sign of the signed area from the [shoelace formula](/shoelace-formula/), positive for counterclockwise, and it is also the sign of the [orientation test](/orientation-test/) at the lowest-leftmost vertex, which costs $O(1)$ once that vertex is found. Many algorithms require one orientation and silently fail on the other, and file formats fix a convention so that outer boundaries and holes can be told apart. Reversing the vertex list reverses the orientation; a rotation keeps it and a reflection reverses it.

## In plain words

Walk along the edge of a field, keeping it on your left hand. You go around it counterclockwise when seen from above. If you keep the field on your right hand instead, you go clockwise. A list of corners describes one of these two walks, and the orientation tells which one.

The shoelace sum gives twice the area with a sign: positive for the counterclockwise walk and negative for the clockwise one. There is also a quicker test. Look at the corner farthest to the left, and if there are several, the lowest of them. The walk must turn there, and it turns left exactly when it goes counterclockwise.

## The idea

Let $P = (v_0, \ldots, v_{n-1})$ be a simple polygon. It is **counterclockwise** (positively oriented) if $\operatorname{int} P$ lies to the left of each directed edge $v_i v_{i+1}$, and **clockwise** otherwise. Let

$$A(P) = \frac12 \sum_{i=0}^{n-1} v_i \times v_{i+1}, \qquad p \times q = x_p y_q - x_q y_p,$$

be the signed area. Then $A(P) = +\operatorname{area}(P)$ when $P$ is counterclockwise and $-\operatorname{area}(P)$ when it is clockwise; the proof is on the [shoelace formula](/shoelace-formula/) page. As the area of a simple polygon with $n \ge 3$ distinct vertices is positive, the sign of $A(P)$ is the orientation.

**The extreme vertex test.** Let $v_i$ be the lexicographically smallest vertex, the leftmost and among those the lowest. Then $\mathrm{orient}(v_{i-1}, v_i, v_{i+1}) \ne 0$, and it is positive exactly when $P$ is counterclockwise.

*Proof.* All of $P$ lies in $S = \{x > x_i\} \cup \{x = x_i,\, y \ge y_i\}$. The set $S \setminus \{v_i\}$ lies in an open half-plane whose boundary line passes through $v_i$: take the line through $v_i$ with a slightly negative slope, steep enough that all other vertices are on its right. So the interior angle at $v_i$ is less than $\pi$, and the three points are not collinear (collinear with both neighbors on the same side of $v_i$ would be a fold, which a simple polygon does not have). At a vertex whose interior angle is less than $\pi$, the boundary turns toward the interior: left when the interior is on the left, right when it is on the right. $\square$

Finding $v_i$ takes $n - 1$ comparisons, and the test is one orientation, so the orientation of a simple polygon costs $\Theta(n)$ either way. The extreme vertex test needs fewer multiplications; the shoelace sum also gives the area. On integer input both are exact.

**Effect of transformations.** Reversing the list maps each term $v_i \times v_{i+1}$ to its negative, so it negates $A(P)$. A [rotation](/vector-rotation/) or a translation keeps every cross product of differences, so it keeps the orientation. A [reflection](/point-projection-and-reflection/) negates every orientation test, so it reverses the orientation: mirroring a counterclockwise polygon gives a clockwise list.

**Polygons that are not simple.** For a polygon that crosses itself, "clockwise" has no meaning in general. The signed area is still $\iint w_P(q)\, dq$, where $w_P$ is the [winding number](/winding-number-algorithm/), and its sign tells which way the boundary winds on balance. A figure eight with two equal lobes has signed area 0. The extreme vertex test then says only which way the boundary turns at that vertex.

**Convex polygons.** For a [convex polygon](/convex-polygon/) every turn has the sign of the orientation, so the test at any vertex where the turn is not zero gives the answer.

## Examples

| polygon | vertices | twice the signed area | lowest-leftmost vertex test | orientation |
| --- | --- | --- | --- | --- |
| triangle | $(0,0), (4,0), (0,3)$ | 12 | $\mathrm{orient}((0,3), (0,0), (4,0)) = 12$ | counterclockwise |
| same, reversed | $(0,3), (4,0), (0,0)$ | $-12$ | $\mathrm{orient}((4,0), (0,0), (0,3)) = -12$ | clockwise |
| concave pentagon | $(0,0), (6,0), (6,4), (3,1), (0,4)$ | 30 | $\mathrm{orient}((0,4), (0,0), (6,0)) = 24$ | counterclockwise |
| bowtie (not simple) | $(0,0), (2,2), (2,0), (0,2)$ | 0 | $\mathrm{orient}((0,2), (0,0), (2,2)) = 4$ | not defined |

- **The pentagon.** At the reflex vertex $(3,1)$ the turn is to the right, $\mathrm{orient}((6,4), (3,1), (0,4)) = -18$, opposite to the orientation, so a test at an arbitrary vertex can be wrong. At the lowest-leftmost vertex $(0,0)$ the test is right.
- **A polygon with a hole.** The square $(0,0), (4,0), (4,4), (0,4)$ with twice the signed area 32 and the hole $(1,1), (1,3), (3,3), (3,1)$ with twice the signed area $-8$: the outer contour is counterclockwise and the hole clockwise, and the total $32 - 8 = 24$ is twice the area of the region.
- **The bowtie.** Its two triangular lobes have winding numbers $+1$ and $-1$, so the signed area is 0, while the boundary turns left at the leftmost vertex, the corner of the counterclockwise lobe.

## Where it is used

- **[Convex hull](/convex-hull/) algorithms.** The output is usually counterclockwise, and the [Graham scan](/graham-scan/) and [monotone chain](/andrew-monotone-chain/) keep only left turns.
- **[Polygon with holes](/polygon-with-holes/).** The outer contour is counterclockwise and the holes clockwise, so that the region is on the left of every edge and the signed areas add up. GeoJSON fixes this convention; some other formats use the opposite one.
- **Clipping.** [Sutherland-Hodgman](/sutherland-hodgman/) keeps the left side of each clip edge, so the clip polygon must be counterclockwise. [Weiler-Atherton](/weiler-atherton-algorithm/) needs both polygons in the same orientation to classify entering and leaving crossings.
- **Triangulation.** [Ear clipping](/ear-clipping/) recognizes a convex vertex by a left turn, which assumes counterclockwise order.
- **Fill rules.** The [nonzero winding rule](/nonzero-winding-rule/) depends on the orientation of each contour: a hole drawn in the same direction as its outer contour is filled instead of left empty.
- **Rendering.** In 3D graphics a triangle whose projection on the screen is clockwise faces away from the viewer and can be skipped (back-face culling).

## References
