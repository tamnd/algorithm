---
tag: F55GRP
kind: definition
slug: tangent-plane-continuity
name: Tangent plane continuity between patches
aliases:
- G1 continuity of surfaces
- G1 patch join
area: cad/surface-interrogation-and-design
level: core
summary: Two patches that share a boundary curve are G1 when their tangent planes and normals agree along it, which holds exactly when a reparametrization makes the join C1.
prereqs: [parametric-surface, parametric-continuity, fundamental-forms]
see_also: [twist-compatibility, gregory-patch, n-sided-patch, coons-patch, bezier-patch, reflection-lines, surface-curvature, vertex-blend]
sources:
  - paper: "Tony D. DeRose, Necessary and sufficient conditions for tangent plane continuity of Bezier surfaces, Computer Aided Geometric Design 7(1-4), 165 to 179, 1990"
    title: DeRose 1990
    locator: the tangent plane condition along a common boundary as a linear dependence of the two cross derivatives and the boundary tangent, and its form for Bezier control points
  - paper: "Ding-yuan Liu, GC1 continuity conditions between two adjacent rational Bezier surface patches, Computer Aided Geometric Design 7(1-4), 151 to 163, 1990"
    title: Liu 1990
    locator: the same conditions for rational Bezier patches
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 2-4, the tangent plane of a regular surface and its independence of the parametrization
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the chapters on Bezier patches and on smooth joins of patches
---

Two parametric patches that share a boundary curve meet with *tangent plane continuity*, or $G^1$ continuity, when at every point of the boundary they have the same tangent plane and the same oriented normal. It is the surface version of the $G^1$ condition for curves on the [parametric continuity](/parametric-continuity/) page. It is weaker than $C^1$, because the two cross derivatives need not be equal, and it is the condition that matters for the shape: a $G^1$ join looks smooth, and any $G^1$ join becomes $C^1$ after a change of the parameters of one patch.

## Definition

Let $a(u, v)$ and $b(u, v)$ be regular patches, so $a_u \times a_v \ne 0$ and $b_u \times b_v \ne 0$, with the unit normals $n_a = a_u \times a_v / |a_u \times a_v|$ and $n_b = b_u \times b_v / |b_u \times b_v|$. Suppose they meet with $C^0$ continuity along a common boundary curve, with the same parametrization on both sides:

$$a(1, v) = b(0, v) = c(v), \qquad 0 \le v \le 1,$$

so $a$ is on the side $u \le 1$ and $b$ on the side $u \ge 0$. Then $a_v(1, v) = b_v(0, v) = c'(v)$, and $c'(v) \ne 0$ because both patches are regular. The patches are *tangent plane continuous*, or $G^1$, along $c$ if $n_a(1, v) = n_b(0, v)$ for every $v$.

**Theorem.** The patches are $G^1$ along $c$ if and only if there are functions $\alpha(v) > 0$ and $\beta(v)$ with

$$b_u(0, v) = \alpha(v)\, a_u(1, v) + \beta(v)\, c'(v) \quad \text{for all } v. \tag{1}$$

Equivalently, $\det[a_u(1, v), b_u(0, v), c'(v)] = 0$ and the $u$ derivatives point to the same side of the boundary.

*Proof.* At a point of the boundary the tangent plane of $a$ is spanned by $a_u$ and $a_v = c'$, and the tangent plane of $b$ by $b_u$ and $c'$. Both spans are planes, since the patches are regular. They are the same plane if and only if $b_u$ lies in the span of $a_u$ and $c'$, that is, $b_u = \alpha a_u + \beta c'$ for some real $\alpha$ and $\beta$, and $\alpha \ne 0$ because $b_u$ and $c'$ are independent. Then $b_u \times b_v = (\alpha a_u + \beta c') \times c' = \alpha\, a_u \times c' = \alpha\, a_u \times a_v$. So the two unit normals are equal when $\alpha > 0$ and opposite when $\alpha < 0$. $\square$

**Reparametrization.** If $\alpha$ and $\beta$ in (1) are smooth, put $\tilde b(u, v) = b(u / \alpha(v),\ v - u \beta(v) / \alpha(v))$. On $u = 0$ this is $b(0, v) = c(v)$, and by the chain rule $\tilde b_u(0, v) = (b_u - \beta c') / \alpha = a_u(1, v)$. The Jacobian of the change of parameters at $u = 0$ has determinant $1/\alpha \ne 0$, so near the boundary $\tilde b$ is the same surface as $b$, and $a$ and $\tilde b$ join with $C^1$ continuity. Conversely, a $C^1$ join of regular patches is $G^1$, with $\alpha = 1$ and $\beta = 0$. So $G^1$ is the condition "$C^1$ after a reparametrization", in the same way as for curves.

**Bezier form.** Let $a$ and $b$ be [Bezier patches](/bezier-patch/) of bidegree $(m, n)$ with control points $a_{i,j}$ and $b_{i,j}$, and with $a_{m,j} = b_{0,j}$. Then $a_u(1, v) = m \sum_j (a_{m,j} - a_{m-1,j}) B^n_j(v)$ and $b_u(0, v) = m \sum_j (b_{1,j} - b_{0,j}) B^n_j(v)$. So the simplest sufficient condition, with a constant $\alpha > 0$ and $\beta = 0$, is

$$b_{1,j} - b_{0,j} = \alpha\, (a_{m,j} - a_{m-1,j}), \qquad j = 0, \dots, n:$$

each triple $a_{m-1,j}, a_{m,j}, b_{1,j}$ lies on one line, with the same ratio of lengths for every $j$. This condition is not necessary. DeRose gives the necessary and sufficient conditions on the control points, with polynomial $\alpha$ and $\beta$ of the right degrees.

## Examples and non-examples

**$G^1$ but not $C^1$.** Let $a(u, v) = (u, v, 0)$ and $b(u, v) = (1 + 2u,\ v + u,\ u^2)$ for $0 \le u, v \le 1$. They share the boundary $c(v) = (1, v, 0)$, with $c' = (0, 1, 0)$. Here $a_u = (1, 0, 0)$ and $b_u(0, v) = (2, 1, 0) = 2 a_u + 1 \cdot c'$, so (1) holds with $\alpha = 2$ and $\beta = 1$, and both normals are $(0, 0, 1)$ on the boundary. The join is not $C^1$, since $b_u \ne a_u$. The reparametrization above gives $\tilde b(u, v) = b(u/2, v - u/2) = (1 + u,\ v,\ u^2/4)$, which joins $a$ with $C^1$ continuity.

**A crease.** With $b(u, v) = (1 + u, v, u)$ instead, $b_u = (1, 0, 1)$ is not in the plane $z = 0$. The normal of $b$ is $(-1, 0, 1)/\sqrt 2$, so the two patches meet at an angle of $45°$. This is $C^0$ and not $G^1$.

**A fold.** With $b(u, v) = (1 - u, v, u^2)$, $b_u(0, v) = (-1, 0, 0) = -a_u$. The tangent planes are the same set, but $\alpha = -1 < 0$ and $b_u \times b_v = (0, 0, -1)$. The second patch turns back over the first, so the union has a cusp edge. The definition excludes this case through the sign of $\alpha$.

**A Coons patch network.** Bilinearly blended [Coons patches](/coons-patch/) that share boundary curves are in general only $C^0$ across them, because the patch takes only positions from the boundary. To get $G^1$, the patch must also take cross derivatives, as the bicubically blended Coons patch and the [Gregory patch](/gregory-patch/) do.

**A corner of four patches.** Condition (1) is a condition along one edge. Where several patches meet at a corner, the conditions of the edges are coupled through the twist vectors $r_{uv}$ at the corner, and they can contradict each other for polynomial patches. This is the subject of [twist compatibility](/twist-compatibility/), and it is why [n-sided patches](/n-sided-patch/) and [vertex blends](/vertex-blend/) are hard.

**Seeing it.** A $G^1$ join that is not $G^2$ has a jump in normal curvature. [Reflection lines](/reflection-lines/) cross it with a kink, and they cross a crease with a break.

## Related definitions

- **$C^1$ continuity.** The stronger condition $b_u(0, v) = a_u(1, v)$. It depends on the parametrization, and $G^1$ does not.
- **$G^2$, curvature continuity.** The two patches are $G^1$ and, at each point of the boundary, the normal curvature in every tangent direction is the same on both sides, so the second fundamental forms agree for the common normal. See [surface curvature](/surface-curvature/) and [fundamental forms](/fundamental-forms/).
- **$G^k$ continuity of curves.** The curve version, with the beta constraints, is on the [parametric continuity](/parametric-continuity/) page. A cross section curve of a $G^1$ surface join through a boundary point is $G^1$ there.
- **Normal continuity.** For regular patches with a $C^0$ join, $G^1$ is the same as continuity of the unit normal field across the boundary.

## References
