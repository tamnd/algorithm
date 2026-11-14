---
tag: 4T694Y
kind: technique
slug: reflection-lines
name: Reflection lines
aliases:
- reflection line analysis
- zebra stripes
area: cad/surface-interrogation-and-design
level: core
summary: Shows the mirror image of a family of parallel light lines in a surface, so a designer sees breaks in tangent or curvature continuity as kinks, after Klass.
prereqs: [isophote, parametric-continuity]
see_also: [isophote, curvature-comb, tangent-plane-continuity, marching-squares, lines-of-curvature, energy-based-surface-fairing]
sources:
  - paper: "Reinhold Klass, Correction of local surface irregularities using reflection lines, Computer-Aided Design 12(2), 73 to 77, 1980"
    title: Klass 1980
    locator: the definition of reflection lines for an eye point and a family of parallel light lines, and their use to find and correct surface irregularities
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 8, Curve and Surface Interrogation (Section 8.1.2.3, reflection lines)
  - paper: doi:10.1109/38.156013
    title: "Hans Hagen, Stefanie Hahmann and coauthors, Surface interrogation algorithms, IEEE Computer Graphics and Applications 12(5), 1992"
    locator: reflection lines as an interrogation tool, and the statement that they lose one order of continuity with respect to the surface
---

Reflection lines are the curves on a surface where a fixed eye sees the mirror images of a family of parallel straight light lines, as on the polished body of a car in a hall with rows of strip lights. Klass introduced them in 1980 as a way to inspect and correct car body surfaces. They are a diagnostic, not an algorithm: they show the normal field of the surface in a form that the eye judges well, and a designer reads them. Because a reflection line depends on the normal, it is one order less smooth than the surface, so a jump in curvature shows as a kink and a jump in the tangent plane shows as a break.

## In plain words

Put a shiny object under a ceiling with long parallel strip lights and look at it. On a flat mirror the strips look like straight lines. On a smooth curved panel they bend, but they bend smoothly. Where two panels meet with a sudden change in how sharply they bend, the reflected strips turn a corner, and where the panels meet at an angle the strips break apart. The eye is very good at seeing such corners and breaks, even when the change is too small to see in the shape. A program imitates this: for each point of the surface it follows the line of sight, bounces it off the surface like light off a mirror, and records which strip it hits. Drawing the boundaries between strips gives the reflection lines.

## When it applies

- The surface is given with its normals: a parametric patch, a set of patches, or a fine mesh with good normals.
- The question is about smoothness: are two patches tangent ($G^1$) or curvature continuous ($G^2$) along their common boundary, and are there small waves inside a patch?
- The answer is wanted as a picture for a person, at interactive speed, and not as a number. For a number, such as the size of a curvature jump, compute curvatures directly.
- The result depends on the eye position and on the light lines, so a check must use several set-ups. A defect can be invisible in one of them.

## The template

This page uses the unit normal $n = r_u \times r_v / |r_u \times r_v|$ of a surface $r(u, v)$, and $H = (k_1 + k_2)/2$ for this $n$. Reflection lines do not depend on the sign of $n$, because the mirror formula below is even in $n$.

**Set-up.** An eye point $E$. A light plane $\Pi = \{x : m \cdot x = h\}$ with unit normal $m$. A unit direction $d$ in $\Pi$, and a unit vector $e$ in $\Pi$ orthogonal to $d$. The light lines are $\{x \in \Pi : (x - q_0) \cdot e = \lambda\}$ for a base point $q_0 \in \Pi$ and the levels $\lambda = \lambda_0 + j \delta$, $j \in \mathbb{Z}$.

**The function.** For a surface point $P = r(u, v)$ with normal $n$:

1. The view direction is $w = (P - E)/|P - E|$.
2. The mirror direction is $\rho = w - 2 (w \cdot n)\, n$.
3. If $m \cdot \rho \ne 0$ and $t = (h - m \cdot P)/(m \cdot \rho) > 0$, the reflected ray meets $\Pi$ at $Q = P + t \rho$, and $g(u, v) = (Q - q_0) \cdot e$. Otherwise $P$ sees no light line, and $g$ is undefined.

The *reflection line* of level $\lambda$ is $\{r(u, v) : g(u, v) = \lambda\}$.

**Drawing.** Evaluate $g$ on a grid of each patch and extract the level curves of the levels $\lambda_j$ with [marching squares](/marching-squares/), or trace them with a predictor and corrector step. The *zebra* display instead colours each point by the parity of $\lfloor (g - \lambda_0)/\delta \rfloor$, which gives alternating light and dark stripes whose edges are the reflection lines. A renderer gets the same picture from an environment map with stripes.

**Reading.** Look at the lines where they cross patch boundaries. A smooth crossing means no visible defect for this set-up. A kink means a jump in curvature, and a break means a jump in the tangent plane. Then move the eye or turn the light lines and look again.

**Continuity.** $g$ is a smooth function of $P$ and $n$ where it is defined. So the [isophote](/isophote/) theorem carries over, with $f = n \cdot l$ replaced by $g$, and with the same proof: on a surface that is $G^k$ across a boundary, $k \ge 2$, the reflection lines are $G^{k-1}$ where $\nabla g \ne 0$. For $k = 1$, $g$ is continuous across the boundary, its tangential derivative $a$ along the boundary is the same on both sides, and a reflection line that crosses transversally ($a \ne 0$) has a corner exactly when the one-sided cross derivatives $b^\pm$ differ. In a reparametrization that makes the union $C^1$, the position terms of $b^\pm$ agree, so $b^+ - b^- = \partial_n g \cdot (n^+_v - n^-_v)$, which involves only the jump of the derivative of the normal. At a crease $g$ itself jumps.

## Classic examples

### A plane mirror gives straight lines

Let the surface be a plane and $E'$ the mirror image of $E$ in it. A ray from $E$ to $P$ reflects into the ray from $P$ in the direction $P - E'$. So $P$ lies on the reflection line of a light line $\ell$ if and only if $E'$, $P$ and a point of $\ell$ are collinear, that is, if $P$ lies in the plane through $E'$ and $\ell$. The reflection line is the intersection of two planes, a straight line. A defect of a flat panel therefore shows as a bend in a straight line.

### A curvature jump, seen from three directions

Take the $C^1$ surface $z = y^2 + \max(x, 0)^2$ near the origin, whose curvature in the $x$ direction jumps from $0$ to $2$ across $x = 0$. Put the eye at $E = (0, -3, 3)$, the light plane at $z = 5$, and the point of interest at the origin, where $n = (0, 0, 1)$ on both sides, $w = (0, 1, -1)/\sqrt 2$, $\rho = (0, 1, 1)/\sqrt 2$ and $Q = (0, 5, 5)$. Let $\nabla g^\pm = (g_x, g_y)$ be the one-sided gradients at the origin; the boundary direction is $y$.

| light lines parallel to | $g$ | $\nabla g^-$ | $\nabla g^+$ | what the picture shows at the origin |
|---|---|---|---|---|
| the $x$ axis | $Q_y$ | $(0, -112/3)$ | $(0, -112/3)$ | no kink: the jump is hidden |
| the $y$ axis | $Q_x$ | $(8/3, 0)$ | $(-52/3, 0)$ | the line through the origin is tangent to the boundary |
| the diagonal $x = -y$ | $(Q_x + Q_y)/\sqrt 2$ | $(8, -112)/(3\sqrt 2)$ | $(-52, -112)/(3\sqrt 2)$ | a kink of about $29.0°$ |

The second row follows by hand. On $y = 0$ to first order in $x$, the left side has $n = (0, 0, 1)$, $\rho \propto (x, 3, 3)$ and $Q_x = x + \frac{5}{3} x = \frac{8}{3} x$. The right side has $n \approx (-2x, 0, 1)$, $\rho \approx (x/(3\sqrt 2) - 2\sqrt 2 x,\ 1/\sqrt 2,\ 1/\sqrt 2)$, $t = 5\sqrt 2$, and $Q_x = x + 5\sqrt 2 \cdot x (1/(3\sqrt 2) - 2\sqrt 2) = -\frac{52}{3} x$. In the third row the level curves are orthogonal to the gradients, and the angle between $(8, -112)$ and $(-52, -112)$ is $\arccos(12128/\sqrt{12608 \cdot 15248}) \approx 28.99°$. The surface and the eye are symmetric under $x \mapsto -x$ on the left, which makes $\partial g / \partial x = 0$ in the first row. One set-up is not enough.

### Car body inspection

The original use, after Klass: a designer looks at reflection lines on a car body model, finds the places where they wiggle or kink, and changes control points there until the lines are smooth. The same check, as zebra stripes, is a standard display of surface modelers today.

## Variations

- **Isophotes.** Lines of constant $n \cdot l$. They need only a light direction and do not depend on the eye; see [isophote](/isophote/).
- **Highlight lines.** Points whose normal line meets a fixed straight light line. Like reflection lines they lose one order of continuity, and they do not depend on the eye.
- **Zebra stripes and environment maps.** The raster form of reflection lines, drawn by a renderer from a striped environment map, at the cost of the accuracy of the mesh normals.
- **Light lines at infinity.** As $h \to \infty$ with $E$ fixed, $g/h \to (\rho \cdot e)/(m \cdot \rho)$, which depends only on $n$ and on the view direction $w$.
- **Fairing with reflection lines.** Klass also used reflection lines to correct the irregularities that they show, by changing the surface until the lines have the wanted shape. [Energy based fairing](/energy-based-surface-fairing/) is the usual numerical alternative.

## Pitfalls

- **Hidden defects.** The corner at a curvature jump has size proportional to $\partial_n g \cdot (n^+_v - n^-_v)$, which is zero for some set-ups, as the first row of the table shows. Always look with at least two directions of the light lines.
- **Lines along the boundary.** Where a reflection line runs along a patch boundary ($a = 0$), there is no crossing to judge.
- **Artifacts of the drawing.** Marching squares on a coarse grid draws a polygon, and its corners are not defects of the surface. A zebra image of a coarse mesh shows kinks at the mesh edges, even for a $G^2$ surface, when the normals are interpolated linearly. Refine the grid or the mesh before reading a kink as a defect.
- **Missing parts.** Points whose reflected ray does not reach the light plane ($t \le 0$ or $m \cdot \rho = 0$) have no reflection line. A blank region is not a defect.
- **Wrong normals.** A patch with a reversed normal does not change the lines, but a normal that is wrong in direction, for example a normal from a degenerate corner of a patch, gives false kinks.

## Exercises

1. Show that the mirror direction $\rho = w - 2(w \cdot n) n$ is a unit vector and that it does not change when $n$ is replaced by $-n$.
2. For the plane $z = 0$, $E = (0, -3, 3)$ and the light plane $z = 5$ with lines parallel to the $x$ axis, find the reflection line of level $\lambda = 5$. (Answer: the line $y = 0$, $z = 0$, since $E' = (0, -3, -3)$ and the plane through $E'$ and the light line $\{y = 5, z = 5\}$ is $y = z$.)
3. Show that for $k = 1$ the tangential derivatives of $g$ on the two sides of a $G^1$ boundary agree, and that the position terms of the cross derivatives cancel in $b^+ - b^-$.
4. In the third row of the table, rotate the light lines by an angle $\phi$ in the plane $z = 5$. For which $\phi$ does the kink at the origin disappear? (Answer: only for lines parallel to the $x$ axis, the first row. From the table, the jump of $\partial Q/\partial x$ across the boundary is $(-52/3 - 8/3, 0, 0) = (-20, 0, 0)$, and the jump of $\partial g/\partial x$ is its dot product with $e$, which is zero only for $e = \pm(0, 1, 0)$.)

## References
