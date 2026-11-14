---
tag: 65W7NA
kind: definition
slug: coupler-curve
name: Coupler curve
aliases:
- coupler point curve
area: cad/mechanism-and-assembly-design
level: core
summary: The path traced by a point fixed on the coupler of a linkage, an algebraic curve of degree six for a four-bar, used to design path generators.
prereqs: [four-bar-linkage]
see_also: [roberts-chebyshev-theorem, path-generation, nine-point-path-synthesis, instant-center-of-velocity, resultant, kempe-universality-theorem, grashof-condition, watt-and-stephenson-six-bar]
sources:
  - book: isbn:9780198561248
    title: Kenneth H. Hunt, Kinematic Geometry of Mechanisms, Oxford University Press, 1978
    locator: Chapter 7, the coupler curves of the planar four-bar (degree, circularity, double points), with the algebraic curves of Chapter 4 (general locator; no page number confirmed)
  - paper: "Samuel Roberts, On three-bar motion in plane space, Proceedings of the London Mathematical Society, s1-7 (1875), 14 to 23"
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Section 3.6 (p. 124, coupler curves) and Section 3.8 (p. 141, straight-line mechanisms)
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 2 (pp. 15 to 53), the coupler curve of the planar 4R linkage
---

A coupler curve is the path of a point fixed to the coupler of a linkage as the linkage moves. For a [four-bar linkage](/four-bar-linkage/) the coupler is the floating link, and a point on it, or on a plate rigidly attached to it, traces a closed curve that can be oval, kidney shaped, have a long nearly straight part, cross itself in a figure eight, or have sharp points. Every such curve lies on an algebraic curve of degree 6 that passes three times through each of the two circular points at infinity, so it is called tricircular. The variety of shapes is why four-bars are used as path generators.

This page is about the curve traced by one linkage. The [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/) is about which other linkages trace the same curve, and shows that every four-bar coupler curve is traced by exactly three four-bars.

## Definition

Use the notation of the four-bar page: ground pivots $O_2 = (0, 0)$ and $O_4 = (d, 0)$, input $a$ from $O_2$ to $A$, coupler $b$ from $A$ to $B$, output $c$ from $O_4$ to $B$. A **coupler point** $P$ is a point fixed in the plane of the coupler. In complex numbers it is given by one complex constant $z$:

$$P = A + z (B - A),$$

so $|P - A| = |z| b$ and the angle from $AB$ to $AP$ is $\arg z$. The **coupler curve** of $P$ is the set of positions of $P$ over all configurations of the linkage, on all circuits. Each circuit gives one closed branch of the curve. A Grashof linkage with $s + l < p + q$ has two circuits and its coupler curve has two branches, which may overlap in the plane; a non-Grashof linkage has one.

For a linkage with more links, such as a [Watt or Stephenson six-bar](/watt-and-stephenson-six-bar/), the coupler curve of a point on any floating link is defined in the same way, and its degree is in general higher.

### The equation and its degree

Write the coupler in the frame of $P$. Let $u = e^{i\psi}$ give the orientation of the coupler, and let $\alpha$, $\beta$ and $\gamma$ be the constants with

$$A = P + \alpha u, \qquad B = P + \beta e^{i\gamma} u,$$

so $\alpha = |A - P|$, $\beta = |B - P|$, and $|\beta e^{i\gamma} - \alpha| = b$. Assume $P \ne A$ and $P \ne B$, so $\alpha, \beta > 0$.

**Claim.** With $P = X = x + iy$, $w_1 = X - O_2$, $w_2 = X - O_4$, $m_1 = \alpha w_1$, $m_2 = \beta e^{-i\gamma} w_2$, $r_1 = a^2 - \alpha^2 - |w_1|^2$, $r_2 = c^2 - \beta^2 - |w_2|^2$ and $D = \operatorname{Im}(\overline{m_1} m_2)$, every point of the coupler curve satisfies

$$E(x, y) = |r_1 m_2 - r_2 m_1|^2 - 4 D^2 = 0,$$

and $E$ is a real polynomial of degree exactly 6, whose part of degree 6 is $b^2 (x^2 + y^2)^3$. Conversely, a real point with $E = 0$ and $D \ne 0$ is on the coupler curve.

*Proof.* The two link conditions are $|A - O_2|^2 = a^2$ and $|B - O_4|^2 = c^2$. Expand the first: $|w_1 + \alpha u|^2 = |w_1|^2 + \alpha^2 + 2\alpha\operatorname{Re}(\overline{w_1} u) = a^2$, that is $2\operatorname{Re}(\overline{m_1} u) = r_1$. In the same way the second is $2\operatorname{Re}(\overline{m_2} u) = r_2$. With $u = (u_x, u_y)$ and $m_k = (m_{kx}, m_{ky})$, these are two real linear equations $m_{kx} u_x + m_{ky} u_y = r_k/2$ with determinant $D$. By Cramer's rule, $u_x = (r_1 m_{2y} - r_2 m_{1y})/(2D)$ and $u_y = (r_2 m_{1x} - r_1 m_{2x})/(2D)$. The vector $(u_x, u_y)$ is the vector $r_1 m_2 - r_2 m_1$ turned by $-90°$ and divided by $2D$, so $|u|^2 = 1$ gives $|r_1 m_2 - r_2 m_1|^2 = 4D^2$. If $D = 0$, the two equations are dependent; then their solvability gives $r_1 m_2 = r_2 m_1$, and $E = 0$ again. So every point of the curve satisfies $E = 0$. If $D \ne 0$ and $E = 0$, Cramer's rule gives a unit $u$, hence $A$ and $B$ with the right link lengths, so the point is on the curve.

For the degree: $m_k$ has degree 1 in $x, y$, and $r_k$ has degree 2 with part of degree 2 equal to $-|X|^2$. So $D$ has degree 2, $D^2$ degree 4, and $r_1 m_2 - r_2 m_1$ has degree 3, with part of degree 3 equal to $-|X|^2 X (\beta e^{-i\gamma} - \alpha)$. Its squared absolute value has part of degree 6 equal to $|X|^6 |\beta e^{i\gamma} - \alpha|^2 = b^2 (x^2 + y^2)^3$, which is not zero. $\blacksquare$

The elimination of $u$ here could also be done with a [resultant](/resultant/) after the half-angle substitution, but the Cramer form shows the degree directly.

### The curve is tricircular

The two circular points at infinity are $I = (1 : i : 0)$ and $\bar I = (1 : -i : 0)$, the points that every circle passes through. A curve of degree $2k$ that passes $k$ times through each of them is called $k$-circular: a circle is 1-circular, a coupler curve is 3-circular.

**Claim.** The projective closure of $E = 0$ has a point of multiplicity exactly 3 at each circular point.

*Proof.* Use the coordinates $X = x + iy$ and $\bar X = x - iy$, treated as independent. Then $w_k$ and $m_k$ have degree 1 in $X$ and 0 in $\bar X$, $\overline{m_k}$ has degree 0 in $X$ and 1 in $\bar X$, and $r_k$ has degree at most 1 in each. So $r_1 m_2 - r_2 m_1$ has degree at most 2 in $X$ and 1 in $\bar X$, its conjugate at most 1 in $X$ and 2 in $\bar X$, and their product, the first term of $E$, has degree at most 3 in each of $X$ and $\bar X$. The same holds for $D^2$, since $D = (\overline{m_1} m_2 - m_1 \overline{m_2})/(2i)$ has degree at most 1 in each. Homogenize with a third coordinate $W$ to a form $F(X, \bar X, W)$ of degree 6. The circular point $I$ has $X = x + iy = 1 + i \cdot i = 0$ and $W = 0$, so it is $(X : \bar X : W) = (0 : 1 : 0)$. Set $\bar X = 1$: every term of $F$ has degree at most 3 in $\bar X$, hence degree at least 3 in $X$ and $W$ together, so $I$ is a point of multiplicity at least 3. The term $b^2 X^3 \bar X^3$ of $F$ gives the term $b^2 X^3$ of degree exactly 3, so the multiplicity is exactly 3. The point $\bar I$ is the same with $X$ and $\bar X$ swapped. $\blacksquare$

### What is cited, not proved here

The facts below are proved in Hunt, Chapter 7, and are not proved on this page. For a general choice of the lengths and of $P$, the polynomial $E$ is irreducible and the curve has genus 1. By the genus formula for a curve of degree 6, the two triple points use up 6 of the 10 possible double points, and the curve has 3 more double points in the finite plane. Each can be a real crossing, a real isolated point, a cusp, or one of a pair of complex conjugate points. Special cases reduce: if $P = A$ the curve is a circle about $O_2$, and if $P = B$ a circle about $O_4$, which is why the claim above needs $\alpha, \beta > 0$.

## Examples and non-examples

**A straight-line linkage (Hoeken's linkage).** Take $a = 1$, $b = 2.5$, $c = 2.5$, $d = 2$, a crank-rocker since $1 + 2.5 < 2 + 2.5$, and the coupler point $P = A + 2(B - A)$, on the line $AB$ at distance 5 from $A$. Three exact configurations show the straight part:

| $\theta_2$ | $A$ | $B$ | $P$ |
|---|---|---|---|
| $90°$ | $(0, 1)$ | $(2, 2.5)$ | $(4, 4)$ |
| $180°$ | $(-1, 0)$ | $(0.5, 2)$ | $(2, 4)$ |
| $270°$ | $(0, -1)$ | $(0, 1.5)$ | $(0, 4)$ |

Each row checks by hand: for example at $\theta_2 = 180°$, $|B - A| = |(1.5, 2)| = 2.5$ and $|B - O_4| = |(-1.5, 2)| = 2.5$. A sweep of $\theta_2$ from $90°$ to $270°$ in steps of $0.001°$ on the open branch moves $P$ from $(4, 4)$ to $(0, 4)$, and the largest distance of $P$ from the line $y = 4$ is $0.00975$, about $0.24\%$ of the length of the segment. This is a measured value, not a proved bound. The coupler curve of degree 6 contains no segment of a line, so the straight part can only be approximate.

**A curve with a cusp.** The coupler point has zero velocity exactly when it coincides with the [instant center](/instant-center-of-velocity/) $P_{13}$ of the coupler at that moment, the intersection of the lines $O_2A$ and $O_4B$. At such an instant the coupler curve in general has a cusp. Choosing $P$ on the moving centrode of the coupler gives a curve with a cusp, which is used for a dwell or a pick-and-place motion.

**A figure eight.** Watt's straight-line linkage has two equal rockers, pivoted on opposite sides and joined by a short coupler, with $P$ at the middle of the coupler. Its coupler curve is a figure eight: the crossing is one of the three real double points, and the two long sides near the crossing are almost straight.

**Non-example: the path of $A$ or $B$.** The pins $A$ and $B$ are coupler points too, but their paths are circles, arcs of the input and output circles. The degree 6 claim needs $P$ off the two pins.

**Non-example: a slider-crank.** In the [slider-crank mechanism](/slider-crank-mechanism/), the curve of a point on the rod is of degree 4 in general, not 6, because one of the two circles is replaced by a line. The two circular points are double, not triple, points of it.

**Non-example: the whole plane.** No four-bar coupler curve fills a region or is an arbitrary curve. Every bounded part of a plane algebraic curve can be traced by some linkage with more links, by the [Kempe universality theorem](/kempe-universality-theorem/), but a four-bar has only nine parameters and its curves are a 9-parameter family of sextics.

## Related definitions

- [Four-bar linkage](/four-bar-linkage/): the mechanism and its configuration space, of which the coupler curve is an image.
- [Roberts-Chebyshev theorem](/roberts-chebyshev-theorem/): the three cognate four-bars that trace the same coupler curve.
- [Path generation](/path-generation/) and [nine-point path synthesis](/nine-point-path-synthesis/): the design problem of finding a four-bar whose coupler curve passes through given points. Nine points match the nine parameters.
- [Instant center of velocity](/instant-center-of-velocity/): the instant center of the coupler gives the direction of the tangent to the coupler curve, perpendicular to the line from $P_{13}$ to $P$, and the cusps.
- [Kempe universality theorem](/kempe-universality-theorem/): linkages with more links trace every bounded part of an algebraic curve.
- [Resultant](/resultant/): another way to eliminate the coupler angle from the two link equations.

### Parameters

A four-bar coupler curve depends on the two ground pivots (4 numbers), the lengths $a$, $b$, $c$ (3 numbers) and the coupler point $z$ (2 numbers), so 9 numbers. This is why nine points of the plane are the most through which a four-bar coupler curve can be made to pass in general.

### History

Coupler curves were studied in the 19th century as three-bar curves, since the ground was not counted as a bar. Samuel Roberts showed in 1875 that one such curve is traced by three different linkages, and he and Cayley, in a long paper of 1876, studied the degree and the singular points of these curves. Atlases of coupler curves, such as that of Hrones and Nelson (1951), were long used by designers to pick a linkage by the shape of its curve.

## References
