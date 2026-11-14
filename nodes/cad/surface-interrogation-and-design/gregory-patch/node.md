---
tag: T032P8
kind: definition
slug: gregory-patch
name: Gregory patch
aliases:
- rational Gregory patch
area: cad/surface-interrogation-and-design
level: advanced
summary: A bicubic patch with two inner control points at each corner, blended by rational weights, so that the cross derivative of each edge can be set independently.
prereqs: [bezier-patch, twist-compatibility, coons-patch]
see_also: [twist-compatibility, tangent-plane-continuity, n-sided-patch, vertex-blend, coons-patch, bezier-patch, generalized-bezier-patch]
sources:
  - paper: doi:10.1016/B978-0-12-079050-0.50009-6
    title: "J. A. Gregory, Smooth interpolation without twist constraints, in R. E. Barnhill and R. F. Riesenfeld (eds.), Computer Aided Geometric Design, Academic Press, 1974, pp. 71 to 87"
    locator: the Coons type interpolant whose corner twists are rational blends of the two twists given by the edges
  - paper: doi:10.1145/800059.801160
    title: "Hiroaki Chiyokura and Fumihiko Kimura, Design of solids with free-form surfaces, Computer Graphics 17(3), SIGGRAPH 1983"
    locator: the Gregory patch in Bezier form, with twenty control points, and its use for G1 joins in a solid modeler (general locator)
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 22, Coons Patches (Boolean sums, twists and their compatibility)
---

A Gregory patch is a four sided patch that is a bicubic [Bezier patch](/bezier-patch/) except at its four inner control points: each of them is split into two points, and a rational blend of the parameters picks one point near each of the two edges at that corner. So the cross derivative along each edge depends only on that edge and its own two inner points, and the four edges can be joined with $G^1$ continuity to four independent neighbours. Gregory introduced the rational corner blend in 1974 for Coons type interpolants, and Chiyokura and Kimura gave the form with twenty control points in 1983. The patch is a rational function of $u$ and $v$, which is the reason for the name rational Gregory patch.

## Definition

Let $B_i(t) = \binom{3}{i} t^i (1 - t)^{3 - i}$ be the cubic Bernstein polynomials. A *Gregory patch* has twelve boundary control points $P_{ij}$, those with $i \in \{0, 3\}$ or $j \in \{0, 3\}$, and eight inner control points $P^u_{ij}$ and $P^v_{ij}$ for $i, j \in \{1, 2\}$. Here $P^u_{ij}$ is the inner point that serves the nearby edge along which $u$ varies ($v = 0$ or $v = 1$), and $P^v_{ij}$ serves the nearby edge along which $v$ varies ($u = 0$ or $u = 1$). For $(u, v)$ in the open square put

$$P_{11}(u, v) = \frac{u P^u_{11} + v P^v_{11}}{u + v}, \qquad P_{12}(u, v) = \frac{u P^u_{12} + (1 - v) P^v_{12}}{u + 1 - v},$$

$$P_{21}(u, v) = \frac{(1 - u) P^u_{21} + v P^v_{21}}{1 - u + v}, \qquad P_{22}(u, v) = \frac{(1 - u) P^u_{22} + (1 - v) P^v_{22}}{2 - u - v},$$

and

$$r(u, v) = \sum_{i=0}^{3} \sum_{j=0}^{3} B_i(u) B_j(v) P_{ij}(u, v),$$

where the twelve boundary points are constant. Each $P_{ij}(u, v)$ for $i, j \in \{1, 2\}$ is a convex combination of its two points, so it is bounded, and $B_i(u) B_j(v) \to 0$ at the corners for these $i, j$. So $r$ extends continuously to the closed square, with the four corners equal to $P_{00}, P_{03}, P_{30}, P_{33}$.

**Theorem (independent edges).** The boundary curve $r(u, 0)$ is the cubic Bezier curve of $P_{00}, \dots, P_{30}$, and the cross derivative along it is

$$r_v(u, 0) = 3 \sum_{i=0}^{3} B_i(u) \bigl(Q_{i1} - P_{i0}\bigr), \qquad Q_{01} = P_{01},\ Q_{11} = P^u_{11},\ Q_{21} = P^u_{21},\ Q_{31} = P_{31}.$$

So it is the cross derivative of the bicubic Bezier patch whose inner points near this edge are $P^u_{11}$ and $P^u_{21}$, and it does not depend on any $P^v$ point or on the other inner points. The same holds for the other three edges, with the $P^v$ points on the edges $u = 0$ and $u = 1$.

*Proof.* At $v = 0$, $B_j(0) = 0$ for $j \ge 1$, so $r(u, 0) = \sum_i B_i(u) P_{i0}$. Differentiate in $v$ by the product rule:

$$r_v(u, 0) = \sum_{i, j} B_i(u) \bigl[B_j'(0) P_{ij}(u, 0) + B_j(0)\, \partial_v P_{ij}(u, 0)\bigr].$$

The second term is zero: for $j \ge 1$ because $B_j(0) = 0$, and for $j = 0$ because the boundary points do not depend on $v$. For $0 < u < 1$ the derivatives $\partial_v P_{ij}$ exist and are bounded near $v = 0$, so the product rule is valid. In the first term, $B_0'(0) = -3$, $B_1'(0) = 3$ and $B_j'(0) = 0$ for $j \ge 2$, so only the rows $j = 0$ and $j = 1$ remain. In row $j = 1$, $P_{11}(u, 0) = u P^u_{11}/u = P^u_{11}$ and $P_{21}(u, 0) = (1 - u) P^u_{21}/(1 - u) = P^u_{21}$. This gives the formula for $0 < u < 1$, and both sides are continuous in $u$ on $[0, 1]$. The other edges follow in the same way. $\square$

**Consequence.** To join the patch to a neighbour across the edge $v = 0$ with [tangent plane continuity](/tangent-plane-continuity/), choose $P^u_{11}$ and $P^u_{21}$ so that this cross derivative satisfies the $G^1$ condition with the neighbour. The choice does not change the other three edges. At the corner $(0, 0)$ the edge $v = 0$ gives the twist $9 (P^u_{11} - P_{10} - P_{01} + P_{00})$, and the edge $u = 0$ gives $9 (P^v_{11} - P_{10} - P_{01} + P_{00})$. These are the two twists of [twist compatibility](/twist-compatibility/), and the patch takes both, so it needs no compatibility condition. The price is smoothness at the corner points: there the mixed derivative of $r$ has no limit when $P^u_{11} \ne P^v_{11}$, which the theorem on the twist compatibility page shows to be unavoidable.

## Examples and non-examples

**Incompatible twists.** Take $P_{ij} = (i, j, 0)$ for all boundary points and all inner points, except $P^u_{11} = (1, 1, 1)$. By the theorem, along $v = 0$ the cross derivative is $r_v(u, 0) = (0, 3, 3 B_1(u)) = (0, 3, 9u(1 - u)^2)$, while along $u = 0$ it is $r_u(0, v) = (3, 0, 0)$. The height $z$ therefore has $z_{vu} = 9$ from the first edge and $z_{uv} = 0$ from the second at the corner $(0, 0)$, which no polynomial patch can have. The Gregory patch has them both. Its centre is $r(1/2, 1/2) = (3/2, 3/2, z)$ with $z = B_1(1/2)^2 \cdot \frac{1}{2} = \frac{9}{64} \cdot \frac{1}{2} = \frac{9}{128}$, since only the $P_{11}$ term has a height and the blend gives it the weight $u/(u + v) = 1/2$.

**A bicubic Bezier patch.** If $P^u_{ij} = P^v_{ij}$ for all four inner positions, every blend is constant and the Gregory patch is the bicubic Bezier patch with these inner points. So bicubic Bezier patches are the Gregory patches with compatible twists of this special form.

**Not a polynomial patch.** If $P^u_{11} \ne P^v_{11}$, the patch is not a polynomial, and it is not $C^2$ at the corner $(0, 0)$, by the twist compatibility theorem. Inside the open square it is $C^\infty$, since the denominators $u + v$, $u + 1 - v$, $1 - u + v$ and $2 - u - v$ are positive there.

**A pitfall at the corners.** A program that evaluates the formula at a corner divides $0$ by $0$. The value at the corner is the corner point, and derivatives near the corners must be taken from the limits or from points just inside.

## Related definitions

- **The Gregory square.** Gregory's 1974 construction is a Coons type Boolean sum of Hermite interpolants on all four edges, in which each corner twist is replaced by a rational blend of the two twists given by the edges, as on the [twist compatibility](/twist-compatibility/) page. The Bezier form above applies the same rational corner blend to the inner control points of a bicubic patch.
- **[Coons patch](/coons-patch/).** The Boolean sum construction that the Gregory square modifies at the corners.
- **[n-sided patches](/n-sided-patch/).** Triangular and multi-sided patches often use the same idea: each edge has its own cross derivative data, and rational functions blend the data of the edges so that each edge sees only its own. The [generalized Bezier patch](/generalized-bezier-patch/) does this with rational weights on its control points.
- **[Vertex blends](/vertex-blend/).** Where several blends meet, the corner region is a multi-sided hole, and Gregory type patches are one way to fill it.

## References
