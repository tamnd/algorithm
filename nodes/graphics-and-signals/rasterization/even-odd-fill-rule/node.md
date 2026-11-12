---
tag: F5AZ5P
kind: definition
slug: even-odd-fill-rule
name: Even-odd fill rule
aliases:
- alternate fill rule
area: graphics-and-signals/rasterization
level: intro
summary: A point is inside a closed path when a ray from it crosses the path an odd number of times, so when its winding number is odd.
prereqs: [polygon, point-in-polygon]
see_also: [nonzero-winding-rule, crossing-number-algorithm, winding-number-algorithm, polygon-scan-conversion, scanline-polygon-fill, stencil-buffer, jordan-curve-theorem]
sources:
  - book: isbn:9780201379228
    title: Adobe Systems, PostScript Language Reference, third edition, Addison-Wesley, 1999
    locator: Section 4.5.2, Filling (Even-Odd Rule, with Figure 4.4), and Section 4.5.3, Insideness Testing
  - url: https://svgwg.org/svg2-draft/painting.html
    title: Scalable Vector Graphics (SVG) 2, Chapter 13, Painting
    locator: Section 13.4.2, Winding rule, the fill-rule property (the value evenodd)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Section 3.6, Filling Polygons (the odd parity rule along a scan line)
  - paper: doi:10.1016/S0925-7721(01)00012-8
    title: Kai Hormann and Alexander Agathos, The point in polygon problem for arbitrary polygons, Computational Geometry 20(3), 2001
    locator: the relation between the crossing number and the winding number
---

The even-odd fill rule decides which points a closed path encloses by parity. A point is inside when a ray from it to infinity crosses the path an odd number of times, which is the same as an odd [winding number](/winding-number-algorithm/). It does not depend on the direction of the rings, and each edge of the path separates inside from outside. It is the `evenodd` value of the SVG `fill-rule` property, the `eofill` operator of PostScript and the ALTERNATE mode of Windows GDI.

## Definition

Let $P$ be a closed path made of one or more closed rings of segments. Let $x$ be a point that is not on $P$. Choose a ray from $x$ that passes through no vertex of $P$ and contains no edge, and let $c(x)$ be the number of edges of $P$ that the ray crosses. The point $x$ is **inside $P$ under the even-odd rule** when $c(x)$ is odd.

The parity of $c(x)$ does not depend on the ray. Let $w(x)$ be the winding number of $P$ around $x$. Each crossing adds $+1$ or $-1$ to $w(x)$, by the direction in which the edge crosses the ray. So $c(x) \equiv w(x) \pmod 2$, and $x$ is inside exactly when $w(x)$ is odd.

Two properties follow.

- **Direction does not matter.** Reversing a ring changes the sign of its part of $w(x)$, which does not change the parity.
- **Every edge is a border.** Moving $x$ across one edge changes $c(x)$ by one, so the inside is on exactly one side of each edge, near each point of the edge that is on no other edge. Two edges that lie on top of each other cancel.

For rings $R_1, \dots, R_k$ that are each simple, the inside is the symmetric difference of their Jordan interiors: a point is inside when it is in an odd number of them.

For a raster, the rule is applied at pixel centers $(i + 1/2, j + 1/2)$, as in the OpenGL and Direct3D 10 rules. A pixel is a point sample, not a little square. A center on the path needs a tie rule, such as the [top-left fill rule](/top-left-fill-rule/). [Polygon scan conversion](/polygon-scan-conversion/) shifts the center by $(\varepsilon, \varepsilon^2)$ for a tiny $\varepsilon > 0$, which moves it off every edge. With integer or rational vertices, the parity test is an exact sign computation. With [IEEE 754](/ieee-754/) floating point, a crossing near a vertex can be counted twice or not at all, which flips the parity of a whole span.

## Examples and non-examples

- **A simple polygon.** For a simple ring, $w(x)$ is $\pm 1$ inside and 0 outside, so the even-odd rule gives the Jordan interior, as does the [nonzero winding rule](/nonzero-winding-rule/). See the [Jordan curve theorem](/jordan-curve-theorem/).
- **A five-point star.** For the star $(5, 0)$, $(8, 10)$, $(0, 4)$, $(10, 4)$, $(2, 10)$, the tips have winding number $\pm 1$ and the pentagon in the middle has $\pm 2$. Under the even-odd rule, the middle is outside, and the star is drawn as five separate tips. A ray from the point $(5, 5)$ to the right crosses the edges from $(5, 0)$ to $(8, 10)$ and from $(10, 4)$ to $(2, 10)$, so $c = 2$.
- **A square with a hole.** The square with corners $(0, 0)$ and $(8, 8)$, with a second ring around the square with corners $(2, 2)$ and $(6, 6)$, has a hole under this rule, whatever the directions of the rings.
- **Two overlapping squares.** Two squares that overlap give the exclusive or of their insides: the overlap is outside, even when both rings run in the same direction.
- **Non-example.** A point with winding number 2, such as the middle of the star or of two overlapping squares with the same direction, is outside under the even-odd rule, but inside under the nonzero rule.
- **Non-example.** A point on the path is neither inside nor outside by this definition. Only a tie rule decides it.

## Related definitions

- The [nonzero winding rule](/nonzero-winding-rule/) marks $x$ inside when $w(x) \ne 0$. The two rules give the same set exactly when no point off the path has an even winding number other than 0, such as 2 or $-2$.
- The [crossing number algorithm](/crossing-number-algorithm/) in geometry is the algorithm that counts crossings for one query point. This page is the rule that defines the set, and the algorithm decides it for one point.
- The [winding number algorithm](/winding-number-algorithm/) computes $w(x)$, from which both rules follow.
- [Scanline polygon fill](/scanline-polygon-fill/) applies the rule along a row by filling every second interval between sorted crossings. The [stencil buffer](/stencil-buffer/) applies it with the INVERT operation on one bit.
- [Point in polygon](/point-in-polygon/) is the query problem. For a simple polygon the two rules agree, so the rule matters only for paths that cross themselves or have several rings.

## References
