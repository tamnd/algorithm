---
tag: MNGCC1
kind: definition
slug: isophote
name: Isophote
aliases:
- isophote analysis
- isophote line
area: cad/surface-interrogation-and-design
level: core
summary: A curve on a surface where the angle between the normal and a light direction is constant. Kinks or jumps in isophotes reveal curvature or tangent discontinuities.
prereqs: [parametric-surface, parametric-continuity]
see_also: [reflection-lines, curvature-comb, lambertian-reflectance, silhouette-curve-of-a-surface, tangent-plane-continuity, marching-squares, umbilic-point]
sources:
  - paper: doi:10.1016/0167-8396(84)90028-1
    title: "Thomas Poeschl, Detecting surface irregularities using isophotes, Computer Aided Geometric Design 1(2), 1984"
    locator: pp. 163 to 168 (isophotes as lines of equal light intensity, and their use to detect irregularities of surfaces)
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 8, Curve and Surface Interrogation (Section 8.1.2.2, isophotes)
  - paper: doi:10.1109/38.156013
    title: "Hans Hagen, Stefanie Hahmann and coauthors, Surface interrogation algorithms, IEEE Computer Graphics and Applications 12(5), 1992"
    locator: isophotes and reflection lines as interrogation tools, and the statement that they lose one order of continuity with respect to the surface
---

An isophote of a surface is a curve on it along which the unit normal makes a constant angle with a fixed light direction, so that the surface has constant brightness along it under a directional light and a matte material. A family of isophotes for several angles shows the shading of the surface as a set of contour lines. Isophotes are a diagnostic, not an algorithm: they display a property of the normal field, and a designer reads them to find places where the surface is not smooth enough. They lose one order of smoothness with respect to the surface, so a break in curvature shows as a kink in the isophotes, and a break in the tangent plane shows as a jump.

## Definition

Let $r : D \to \mathbb{R}^3$ be a regular parametric surface with unit normal $n = r_u \times r_v / |r_u \times r_v|$. The mean curvature $H = (k_1 + k_2)/2$ is taken with respect to this $n$; this page needs only $n$. Let $l$ be a fixed unit vector, the light direction, and put

$$f(u, v) = n(u, v) \cdot l = \cos \angle(n, l).$$

For $c \in [-1, 1]$, the *isophote* of level $c$ is the set $\{ r(u, v) : f(u, v) = c \}$. Under the [Lambertian](/lambertian-reflectance/) model with a directional light, the brightness at a point is proportional to $\max(0, f)$, so an isophote with $c > 0$ is a curve of constant brightness. An *isophote family* is the set of isophotes for levels $c_j = \cos \theta_j$ with equally spaced angles $\theta_j$, often drawn as alternating light and dark bands. Some systems use $|f|$, so that the result does not depend on the orientation of $n$.

The isophotes depend only on $n$ and $l$: they do not change when the surface is translated or scaled, and they do not depend on the position of the eye. The isophote of level $0$ is the set where $n \perp l$, which is the [silhouette curve](/silhouette-curve-of-a-surface/) for a parallel view along $l$.

### Regularity on a smooth surface

**Theorem.** Let $r$ be of class $C^k$ with $k \ge 2$. Then $f$ is of class $C^{k-1}$. Near a point where $f = c$ and $\nabla f \ne 0$, the isophote of level $c$ is a regular curve of class $C^{k-1}$.

*Proof.* $r_u \times r_v$ is $C^{k-1}$ and not zero, so $n$ and $f$ are $C^{k-1}$. Since $k - 1 \ge 1$ and $\nabla f \ne 0$, the implicit function theorem gives a $C^{k-1}$ regular parametrization of $\{f = c\}$ near the point, and its image under the $C^k$ immersion $r$ is a regular $C^{k-1}$ curve. $\square$

The gradient is $\nabla f = (n_u \cdot l,\ n_v \cdot l)$. Both $n_u$ and $n_v$ are tangent to the surface, so $\nabla f = 0$ exactly when the tangential part of $l$ is orthogonal to the image of the differential of $n$. Where $K \ne 0$ this image is the whole tangent plane, so $\nabla f = 0$ only where $n = \pm l$, at the brightest and darkest points, where an isophote shrinks to a point or crosses itself. On a planar region $f$ is constant, and there are no isophote curves at all, only a region with one level.

### Regularity across a boundary between patches

Let two patches meet along a common boundary curve with $G^k$ continuity, $k \ge 1$, in the sense of [geometric continuity](/parametric-continuity/): after a regular reparametrization of one patch, the union is a $C^k$ surface near the boundary, and each patch is $C^\infty$ up to the boundary.

**Theorem.** (a) If $k \ge 2$, then near a boundary point with $\nabla f \ne 0$ each isophote is a $G^{k-1}$ curve. (b) If $k = 1$, the isophotes are continuous across the boundary but in general have a corner there. (c) If the surface has a crease ($G^0$ but not $G^1$), the isophotes are in general not continuous across the boundary.

*Proof.* (a) Apply the theorem above to the reparametrized $C^k$ union. Its isophotes are $C^{k-1}$ regular curves, so they are $G^{k-1}$ as point sets.

(b) Reparametrize so that the union is $C^1$ and the boundary is $v = 0$, with patch $-$ in $v \le 0$ and patch $+$ in $v \ge 0$. The normal is continuous, so $f$ is continuous, and each one-sided function $f^\pm$ is smooth up to $v = 0$. On the boundary $f^- = f^+$, so the tangential derivatives agree: $f^-_u = f^+_u = a$. The cross derivatives $b^\pm = f^\pm_v = n^\pm_v \cdot l$ may differ. Let $p$ be a boundary point with $f(p) = c$ and $a \ne 0$. By the implicit function theorem, applied on each side to a smooth extension of $f^\pm$, the isophote on side $\pm$ is a smooth curve that leaves $p$ transversally to the boundary with tangent $t^\pm = (-b^\pm, a)$ in the parameter plane. So the isophote is continuous at $p$. Because $r_u$ and $r_v$ are continuous across $v = 0$, $t^-$ and $t^+$ give parallel tangents in space if and only if they are parallel in the plane, that is, if and only if

$$\det(t^-, t^+) = -b^- a + b^+ a = a\, (b^+ - b^-) = 0.$$

So an isophote that crosses the boundary transversally ($a \ne 0$) has a corner exactly when $b^+ \ne b^-$. If $a = 0$, both one-sided isophotes are tangent to the boundary at $p$. The jump $b^+ - b^- = (n^+_v - n^-_v) \cdot l$ involves only the tangential part of $l$, because $n^\pm_v$ are both tangent to the common tangent plane. Where the curvature jumps, $n^+_v \ne n^-_v$, and the jump is nonzero for every light direction except those whose tangential part is orthogonal to $n^+_v - n^-_v$.

(c) At a crease the one-sided normals $n^-$ and $n^+$ differ at a boundary point $p$, so $f^-(p) \ne f^+(p)$ for every $l$ outside the plane $\{l : l \cdot (n^+ - n^-) = 0\}$. Then the isophotes that arrive at $p$ from the two sides have different levels, and an isophote that reaches the boundary from one side does not continue at the same point on the other side. $\square$

Hagen and his coauthors state the rule for parametric continuity: the isophotes of a $C^k$ surface are $C^{k-1}$. The version above uses geometric continuity, and part (b) says exactly when the order is lost.

## Examples and non-examples

### A curvature jump gives a corner

Let $z = y^2 + \max(x, 0)^2$, with the chart $r(x, y) = (x, y, z)$, the upward normal $n = (-z_x, -z_y, 1)/w$, $w = \sqrt{1 + z_x^2 + z_y^2}$, and $l = (1, 1, 1)/\sqrt 3$. The surface is $C^1$ across $x = 0$, and the curvature in the $x$ direction jumps from $0$ to $2$ there.

- On the left, $x \le 0$: $f = (1 - 2y)/(\sqrt 3 \sqrt{1 + 4y^2})$ does not depend on $x$, so every isophote is a line $y = \text{const}$.
- On the right, $x \ge 0$: $f = (1 - 2x - 2y)/(\sqrt 3 \sqrt{1 + 4x^2 + 4y^2})$.

At the origin, $f = 1/\sqrt 3$ on both sides, and the gradient of the denominator is zero there, so $\nabla f^- = (0, -2/\sqrt 3)$ and $\nabla f^+ = (-2/\sqrt 3, -2/\sqrt 3)$. The isophote of level $1/\sqrt 3$ arrives from the left along $y = 0$, with direction $(1, 0)$, and leaves on the right with direction $(1, -1)/\sqrt 2$. Since $r_x = (1, 0, 0)$ and $r_y = (0, 1, 0)$ at the origin, the corner in space is $45°$. In the notation of the proof, the boundary direction is $y$, $a = -2/\sqrt 3$, and the cross derivatives are $0$ and $-2/\sqrt 3$.

### A smooth surface gives smooth isophotes

On the paraboloid $z = x^2 + y^2$, which is $C^\infty$, with $l = (0, 0, 1)$, $f = 1/\sqrt{1 + 4x^2 + 4y^2}$, and the isophotes are the circles $x^2 + y^2 = (1/c^2 - 1)/4$ for $0 < c < 1$. At $c = 1$ the isophote is the single point at the origin, where $n = l$ and $\nabla f = 0$.

### Non-example: a crease

Let $z = y^2 + \max(x, 0)$, which has a crease along $x = 0$, with the same $l$. On the left, $f = (1 - 2y)/(\sqrt 3 \sqrt{1 + 4y^2})$, and on the right $n = (-1, -2y, 1)/\sqrt{2 + 4y^2}$ and $f = -2y/(\sqrt 3 \sqrt{2 + 4y^2})$. The isophote of level $1/\sqrt 3$ reaches the crease at $y = 0$ from the left. On the right the level $1/\sqrt 3$ would need $-2y = \sqrt{2 + 4y^2}$, which has no solution, since $4y^2 < 2 + 4y^2$. So this isophote ends at the crease.

### Non-example: a plane

On a plane $f$ is constant, so for a given $l$ the plane is one whole region of one level, and isophotes carry no information. The same holds on any part of a surface where the normal is constant.

## Related definitions

- **Reflection lines.** Mirror images of straight light lines in the surface. They depend on the eye position as well as on the normal; see [reflection lines](/reflection-lines/).
- **Highlight lines.** Points where the surface normal meets a fixed line light source, a variant that also depends only on positions and normals.
- **Silhouette curve.** The isophote of level $0$; see [silhouette curve of a surface](/silhouette-curve-of-a-surface/).
- **Curvature comb.** The analogous diagnostic for curves; see [curvature comb](/curvature-comb/).
- **Tangent plane continuity.** The $G^1$ condition between patches that part (b) of the theorem assumes; see [tangent plane continuity](/tangent-plane-continuity/).
- **Computing isophotes.** A program samples $f$ on a grid of the parameter domain and extracts level curves by [marching squares](/marching-squares/), or traces each level curve with a predictor and corrector step on $f = c$. Both are standard contouring methods; the isophote itself is the diagnostic that they draw.

## References
