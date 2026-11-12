---
tag: 6V2V16
kind: definition
slug: top-left-fill-rule
name: Top-left fill rule
aliases:
- top-left rule
- top-left convention
area: graphics-and-signals/rasterization
level: advanced
summary: A tie rule for a pixel center exactly on a triangle edge, which gives each center on a shared edge to exactly one of the two triangles.
prereqs: [edge-function, pixel]
see_also: [pineda-rasterization, triangle-rasterization, scanline-polygon-fill, conservative-rasterization, multisample-antialiasing, alpha-blending, even-odd-fill-rule]
sources:
  - url: https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3d10-graphics-programming-guide-rasterizer-stage-rules
    title: Microsoft, Rasterization Rules (Direct3D 11), Direct3D 11 Graphics documentation
    locator: Triangle Rasterization Rules (without multisampling), the definitions of a top edge and a left edge
  - url: https://docs.huihoo.com/opengl/glspec1.1/node54.html
    title: Mark Segal and Kurt Akeley, The OpenGL Graphics System, A Specification, version 1.1
    locator: Section 3.5.1, Basic Polygon Rasterization (a fragment center on a common edge is produced by exactly one of the two polygons)
  - url: https://fgiesen.wordpress.com/2013/02/08/triangle-rasterization-in-practice/
    title: Fabian Giesen, Triangle rasterization in practice, The ryg blog, 2013
    locator: the section on the fill rule (the rule as a bias on the edge function)
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 8, Section 8.1.2, Dealing with Pixels on Triangle Edges (a tie rule with an off-screen point)
  - paper: doi:10.1145/378456.378457
    title: Juan Pineda, A parallel algorithm for polygon rasterization, Computer Graphics (SIGGRAPH 88 Proceedings) 22(4), 17 to 20, 1988
    locator: the whole paper (the inside test with edge functions, and the treatment of points with E equal to zero)
---

The top-left fill rule is the tie rule for a pixel center that lies exactly on an edge of a triangle: the center is inside the triangle if the edge is a *top edge* or a *left edge* of that triangle, and outside otherwise. Direct3D 10 and later fix this rule. The OpenGL specification requires only its consequence, that a fragment center on an edge shared by two polygons is produced by exactly one of them. With exact [edge functions](/edge-function/), the rule makes a mesh of triangles cover each [pixel](/pixel/) center inside the mesh exactly once: no double draws and no cracks.

## Definition

Screen coordinates have $x$ to the right and $y$ down. A pixel is a point sample at its center, not a little square, and the center of pixel $(i, j)$ is $(i + \tfrac12, j + \tfrac12)$, as in the Direct3D 10 and OpenGL rules. Let $T = (v_0, v_1, v_2)$ be a triangle with signed area $S \ne 0$. If $S < 0$, swap $v_1$ and $v_2$, so that the three edge functions $E_k = A_k x + B_k y + C_k$ are positive inside $T$.

**Top and left edges.** An edge of $T$ with constants $(A, B)$ is

- a **top edge** if $A = 0$ and $B > 0$: the edge is exactly horizontal and the inside of $T$ is below it, so it is above the other two edges;
- a **left edge** if $A > 0$: the edge is not horizontal and the inside of $T$ is to its right, so it is on the left side of $T$;
- **top-left** if it is a top edge or a left edge, that is, if $A > 0$, or $A = 0$ and $B > 0$.

These are the Direct3D definitions written with the edge constants. The vector $(A, B)$ is the normal that points into $T$. A horizontal edge has $A = 0$, and its normal points down ($B > 0$) exactly when the third vertex is below it. A non-horizontal edge is on the left of $T$ exactly when its inner normal has a positive $x$ part. A triangle has one or two left edges and at most one top edge.

**The rule.** A point $p$ is **covered** by $T$ if, for each $k = 0, 1, 2$,

$$E_k(p) > 0, \quad \text{or} \quad E_k(p) = 0 \text{ and edge } k \text{ is top-left.}$$

So a center on a top or left edge is in, and a center on a bottom or right edge is out. A center at a vertex is on two edges, and it is in only if both are top-left.

**Integer form.** With integer edge functions, $E > 0$ is the same as $E - 1 \ge 0$. Let $\mathrm{bias}_k = 0$ if edge $k$ is top-left and $-1$ otherwise. Then $p$ is covered if and only if $E_k(p) + \mathrm{bias}_k \ge 0$ for all $k$. A rasterizer adds the bias to $C_k$ once per triangle and then tests only signs, as in [Pineda rasterization](/pineda-rasterization/).

**Theorem (correctness of the top-left fill rule).** Let $T_1, \ldots, T_m$ be triangles with $S \ne 0$ and pairwise disjoint interiors, with the edge functions computed exactly. Let $U = T_1 \cup \cdots \cup T_m$.

1. Each point $p$ is covered by at most one $T_i$.
2. If $p$ is in the interior of $U$, then $p$ is covered by exactly one $T_i$.

So each pixel center on an edge shared by two triangles goes to exactly one of them, and the same holds at a vertex shared by many triangles.

*Proof.* Let $d(\varepsilon) = (\varepsilon, \varepsilon^2)$.

*Step 1: the rule is a strict test at a moved point.* Fix a triangle and an edge with constants $(A, B) \ne (0, 0)$. By property 4 of the [edge function](/edge-function/),

$$E(p + d(\varepsilon)) = E(p) + A\varepsilon + B\varepsilon^2 .$$

If $E(p) \ne 0$, this has the sign of $E(p)$ for each $\varepsilon$ with $0 < \varepsilon < \varepsilon_1$, for some $\varepsilon_1 > 0$, because $|A\varepsilon + B\varepsilon^2| \to 0$. If $E(p) = 0$ and $A \ne 0$, the value is $\varepsilon (A + B\varepsilon)$, which has the sign of $A$ for small $\varepsilon$. If $E(p) = 0$ and $A = 0$, then $B \ne 0$ and the value is $B\varepsilon^2$, which has the sign of $B$. In each case, for small $\varepsilon > 0$, $E(p + d(\varepsilon)) > 0$ holds exactly when $E(p) > 0$, or $E(p) = 0$ and the edge is top-left. There are $3m$ edges, so there is one $\varepsilon_0 > 0$ that works for all of them. For $0 < \varepsilon < \varepsilon_0$: $p$ is covered by $T_i$ if and only if $p + d(\varepsilon)$ is in the interior of $T_i$.

*Step 2: at most one.* The interiors are disjoint, so $p + d(\varepsilon)$ is in at most one interior, and by step 1, $p$ is covered by at most one $T_i$.

*Step 3: at least one.* For each of the $3m$ edge lines, $\varepsilon \mapsto E(p) + A\varepsilon + B\varepsilon^2$ is a polynomial that is not zero, so it has finitely many roots. Make $\varepsilon_0$ smaller than each positive root. If $p$ is in the interior of $U$, make $\varepsilon_0$ so small that $p + d(\varepsilon) \in U$. Then $p + d(\varepsilon)$ is in some closed triangle $T_i$ and on none of the edge lines, so it is in the interior of $T_i$, and by step 1, $T_i$ covers $p$. $\blacksquare$

The proof shows what the rule is: it samples each triangle at a point an infinitely small step to the right of the center, and a much smaller step below it. Other moves of the same form give other correct rules: $(-\varepsilon, \varepsilon^2)$ gives a top-right rule, and $(\varepsilon, -\varepsilon^2)$ gives a bottom-left rule. The theorem needs only disjoint interiors and a union that covers the center. It holds for T-junctions, where a vertex of one triangle is in the middle of an edge of another, as long as the vertex is exactly on that edge in the snapped coordinates.

## Examples and non-examples

**Two triangles that share a diagonal.** In pixel units, let $T_1 = (0.5, 0.5), (4.5, 0.5), (0.5, 4.5)$ and $T_2 = (4.5, 0.5), (4.5, 4.5), (0.5, 4.5)$. They share the diagonal $x + y = 5$, which goes through the centers of pixels $(3, 1)$, $(2, 2)$ and $(1, 3)$, and the vertices are pixel centers too.

| edge | in $T_1$ | in $T_2$ |
| --- | --- | --- |
| $y = 0.5$ | top edge: in | not an edge |
| $x = 0.5$ | left edge: in | not an edge |
| $x + y = 5$ | right edge: out | left edge: in |
| $x = 4.5$ | not an edge | right edge: out |
| $y = 4.5$ | not an edge | bottom edge: out |

$T_1$ covers the 10 pixels $(i, j)$ with $i + j \le 3$, and $T_2$ covers the 6 pixels with $i + j \ge 4$ and $i, j \le 3$. Together they cover the 16 pixels of the block $0 \le i, j \le 3$, each once. The centers on the right column $x = 4.5$ and the bottom row $y = 4.5$ are left for the triangles to the right and below, so a grid of such squares also covers each center once.

**A vertex shared by a fan.** Put a vertex at the center $(2.5, 2.5)$ of pixel $(2, 2)$, and join it to the 8 points $(0.5, 0.5), (2.5, 0.5), (4.5, 0.5), (4.5, 2.5), (4.5, 4.5), (2.5, 4.5), (0.5, 4.5), (0.5, 2.5)$ to make 8 triangles. Only the triangle with the vertices $(2.5, 2.5)$, $(4.5, 2.5)$ and $(4.5, 4.5)$ covers pixel $(2, 2)$: it is the one that holds the point a tiny step right and below the center. The 8 triangles cover the 16 pixels of the block $0 \le i, j \le 3$, each once.

**Non-example: all edges in or all edges out.** The test $E_k \ge 0$ for all $k$ draws the centers on the diagonal of the first example in both triangles. With [alpha blending](/alpha-blending/), a double draw shows as a dark or bright seam. The test $E_k > 0$ for all $k$ draws them in neither, which shows as a crack of background pixels.

**Non-example: floating point edge functions.** The rule needs the exact sign of $E$, and in particular the exact case $E = 0$. The [edge function](/edge-function/) page gives a binary64 example where the two triangles of a shared edge both compute a positive value at the same point. The rule cannot repair this, because neither computed value is zero. Exact integer coordinates or exact predicates come first.

**Non-example: a T-junction that snapping breaks.** In exact numbers, the point $t = (1, \tfrac13)$ is on the edge from $(0, 0)$ to $(3, 1)$. With 256 subpixel steps per pixel, $t$ snaps to $(256, 85)$ and the edge to $(0, 0)$ to $(768, 256)$, and the edge function of the snapped edge at the snapped $t$ is $768 \cdot 85 - 256 \cdot 256 = -256 \ne 0$. The two sides of the junction now overlap or leave a thin gap, so the hypothesis of the theorem fails. A center in the gap is drawn by no triangle. The fix is in the mesh: split the long edge at $t$ so that both sides share the same snapped vertices.

## Related definitions

- [Edge function](/edge-function/): the exact value whose zero case the rule decides.
- [Pineda rasterization](/pineda-rasterization/) and [triangle rasterization](/triangle-rasterization/): the algorithm and the problem that use the rule.
- [Scanline polygon fill](/scanline-polygon-fill/): a span from $x_l$ to $x_r$ that includes a center at $x_l$ and excludes a center at $x_r$, on the rows from $y_{\min}$ (included) to $y_{\max}$ (excluded), gives the same pixels as the top-left rule for a triangle. The [Gouraud shading](/gouraud-shading/) page uses this form.
- [Even-odd](/even-odd-fill-rule/) and [nonzero winding](/nonzero-winding-rule/) rules: they define which points are inside a polygon that crosses itself. The top-left rule is a different kind of rule: it decides only the points on edges.
- [Multisample antialiasing](/multisample-antialiasing/): the rule applies to each sample position, not only to the pixel center.
- [Conservative rasterization](/conservative-rasterization/): a mode that covers each pixel the triangle touches. Direct3D 12 leaves the fill rule on its edges to the implementation.

## References
