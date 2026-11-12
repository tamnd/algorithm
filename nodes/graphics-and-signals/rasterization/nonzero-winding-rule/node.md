---
tag: J090FB
kind: definition
slug: nonzero-winding-rule
name: Nonzero winding rule
aliases:
- winding fill rule
area: graphics-and-signals/rasterization
level: intro
summary: A point is inside a closed path when the path winds around it a nonzero number of times, counting each turn with its direction.
prereqs: [polygon, point-in-polygon]
see_also: [even-odd-fill-rule, winding-number-algorithm, crossing-number-algorithm, polygon-scan-conversion, scanline-polygon-fill, stencil-buffer, polygon-with-holes]
sources:
  - book: isbn:9780201379228
    title: Adobe Systems, PostScript Language Reference, third edition, Addison-Wesley, 1999
    locator: Section 4.5.2, Filling (Nonzero Winding Number Rule, with Figure 4.3)
  - url: https://svgwg.org/svg2-draft/painting.html
    title: Scalable Vector Graphics (SVG) 2, Chapter 13, Painting
    locator: Section 13.4.2, Winding rule, the fill-rule property (the value nonzero, which is the initial value)
  - paper: doi:10.1016/S0925-7721(01)00012-8
    title: Kai Hormann and Alexander Agathos, The point in polygon problem for arbitrary polygons, Computational Geometry 20(3), 2001
    locator: the definition of the winding number of a closed polygon and its computation by signed crossings
  - url: https://registry.khronos.org/OpenGL-Refpages/gl4/html/glStencilOp.xhtml
    title: Khronos Group, OpenGL 4 Reference Pages, glStencilOp
    locator: the operations GL_INCR_WRAP and GL_DECR_WRAP, which count windings in a stencil buffer
---

The nonzero winding rule decides which points a closed path encloses by the winding number. A point is inside when the path goes around it a nonzero number of times, where turns in one direction count $+1$ and turns in the other direction count $-1$. Unlike the [even-odd fill rule](/even-odd-fill-rule/), it depends on the direction of each ring: a hole must run the other way around from the ring that holds it. It is the default fill rule of SVG and of the PostScript `fill` operator, and the WINDING mode of Windows GDI.

## Definition

Let $P$ be a closed path made of one or more closed rings of segments, and let $x$ be a point that is not on $P$. The **winding number** $w(x)$ is the total angle that the direction from $x$ to a point of $P$ turns through while the point runs once along each ring, divided by $2\pi$. It is an integer. The point $x$ is **inside $P$ under the nonzero rule** when $w(x) \ne 0$.

The same number comes from a ray. Choose a ray from $x$ that passes through no vertex of $P$ and contains no edge. Each edge that crosses the ray adds $+1$ if it crosses from right to left as seen along the ray, and $-1$ if it crosses from left to right. The sum is $w(x)$, for every such ray. This is how the [winding number algorithm](/winding-number-algorithm/) and [scanline polygon fill](/scanline-polygon-fill/) compute it.

Three properties follow.

- **Direction matters.** Reversing a ring negates its part of $w(x)$. Reversing all rings gives the same inside.
- **Union of rings with one direction.** If all rings are simple and run in the same direction, each point inside $k$ of them has $|w(x)| = k$, so the inside is the union of their interiors.
- **Holes by reversal.** A simple ring inside another, with the opposite direction, gives $w(x) = 0$ in the inner region, so it cuts a hole. With the same direction it gives $|w(x)| = 2$, and the region stays filled.

For a raster, the rule is applied at pixel centers $(i + 1/2, j + 1/2)$, as in the OpenGL and Direct3D 10 rules. A pixel is a point sample, not a little square. A center on the path needs a tie rule, such as the [top-left fill rule](/top-left-fill-rule/); [polygon scan conversion](/polygon-scan-conversion/) shifts the center by $(\varepsilon, \varepsilon^2)$ for a tiny $\varepsilon > 0$. With integer or rational vertices, each signed crossing is an exact sign test. With [IEEE 754](/ieee-754/) floating point, a crossing near a vertex can be counted twice or not at all, which changes $w$ by one on a whole span. A counter of $s$ bits, as in a [stencil buffer](/stencil-buffer/), keeps $w(x)$ only modulo $2^s$, so a point with $w(x) = 2^s$ looks outside.

## Examples and non-examples

- **A simple polygon.** For a simple ring, $w(x)$ is $\pm 1$ inside and 0 outside, so the rule gives the Jordan interior, as does the even-odd rule.
- **A five-point star.** For the star $(5, 0)$, $(8, 10)$, $(0, 4)$, $(10, 4)$, $(2, 10)$, a ray from $(5, 5)$ to the right crosses the edges from $(5, 0)$ to $(8, 10)$ and from $(10, 4)$ to $(2, 10)$, both in the same direction, so $|w| = 2$. The middle pentagon is inside, and the whole star is filled, with no hole.
- **A square with an inner ring.** The square with corners $(0, 0)$ and $(8, 8)$ and a second ring around the square with corners $(2, 2)$ and $(6, 6)$ has a hole only when the inner ring runs the other way around. With the same direction the full square is filled.
- **Two overlapping squares.** With the same direction, the overlap has $|w| = 2$ and is inside, so the result is the union. With opposite directions, the overlap has $w = 0$ and is outside.
- **Non-example.** The inner region of a hole has $w = 0$, so it is outside, even though the path surrounds it.
- **Non-example.** A point on the path has no winding number. Only a tie rule decides it.

## Related definitions

- The [even-odd fill rule](/even-odd-fill-rule/) marks $x$ inside when $w(x)$ is odd. The two rules differ exactly at the points where $w(x)$ is even and not 0.
- Other rules use the same number: $w(x) > 0$, $w(x) < 0$, or $|w(x)| \ge 2$. The tessellator of the OpenGL utility library (GLU) offers these as POSITIVE, NEGATIVE and ABS_GEQ_TWO, besides ODD and NONZERO. The last one selects the overlap of shapes.
- The [winding number algorithm](/winding-number-algorithm/) in geometry computes $w(x)$ for one query point. This page is the rule that defines the filled set.
- The [crossing number algorithm](/crossing-number-algorithm/) counts crossings without signs, so it decides only the even-odd rule.
- A [polygon with holes](/polygon-with-holes/) is often stored with the outer ring in one direction and the holes in the other, so that both rules give the same set.
- The [stencil buffer](/stencil-buffer/) computes $w$ at each pixel with wrapping increments and decrements, and [scanline polygon fill](/scanline-polygon-fill/) keeps a running sum of edge directions along each row.

## References
