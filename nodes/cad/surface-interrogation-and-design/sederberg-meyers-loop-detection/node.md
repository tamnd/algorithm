---
tag: DRKHX0
kind: theorem
slug: sederberg-meyers-loop-detection
name: Sederberg-Meyers loop detection
aliases:
- loop detection criterion for surface intersection
area: cad/surface-interrogation-and-design
level: advanced
summary: If a plane through the origin meets the tangent cones of two patches only at the origin, the patches cannot meet in a closed loop, so subdivision can stop without missing small loops.
prereqs: [parametric-surface, surface-surface-intersection]
see_also: [subdivision-surface-intersection, marching-surface-intersection, tangential-surface-intersection, curve-surface-intersection, interval-projected-polyhedron, bezier-clipping, convex-hull-property]
sources:
  - paper: doi:10.1016/0167-8396(88)90029-5
    title: Thomas W. Sederberg and Ray J. Meyers, Loop detection in surface patch intersections, Computer Aided Geometric Design 5(2), 161 to 171, 1988
    locator: the loop test with cones that bound the normals and the tangent planes of two patches (general locator; the exact wording of the test is not restated here)
  - paper: doi:10.1016/0010-4485(89)90058-4
    title: Thomas W. Sederberg, H. N. Christiansen and S. Katz, Improved test for closed loops in surface intersections, Computer-Aided Design 21(8), 505 to 508, 1989
    locator: the whole paper (a closed intersection loop of two patches forces a line that is normal to both patches)
  - paper: doi:10.1145/112515.112543
    title: Michael E. Hohmeyer, A surface intersection algorithm based on loop detection, Proceedings of the First ACM Symposium on Solid Modeling Foundations and CAD/CAM Applications, 197 to 207, 1991
    locator: the whole paper (general locator)
  - paper: doi:10.1016/0167-8396(94)00016-L
    title: Deok-Soo Kim, Panos Y. Papalambros and Tony C. Woo, Tangent, normal, and visibility cones on Bezier surfaces, Computer Aided Geometric Design 12(3), 305 to 320, 1995
    locator: the definitions of the tangent cone and the normal cone of a Bezier surface and their computation (general locator)
  - book: isbn:9780691048338
    title: John W. Milnor, Topology from the Differentiable Viewpoint, Princeton University Press, 1997 (first edition 1965)
    locator: Appendix, Classifying 1-manifolds, p. 55
---

The Sederberg-Meyers loop test tells when two surface patches cannot meet in a closed loop. It looks at the cone of all tangent planes of each patch. If one plane through the origin meets the two cones only at the origin, there is no loop, and every branch of the intersection runs to the boundary of a patch. A [subdivision](/subdivision-surface-intersection/) method uses the test to stop splitting a pair of pieces, because the boundary curves then give a start point on every branch.

## Statement

A *patch* is a set $S = x(D)$, where $D$ is a closed rectangle and $x$ is a $C^1$ map on an open set that contains $D$, one to one on $D$, with $x_u \times x_v \ne 0$. Its *tangent plane* at $p = x(u, v)$ is the plane $T(p)$ through the origin spanned by $x_u$ and $x_v$, and its unit normal $N(p)$ is normal to $T(p)$. The *tangent cone* of the patch is the union $K = \bigcup_{p \in S} T(p)$ of all its tangent planes. A *closed curve* in a set is a $C^1$ map $c$ from a circle into the set with $c' \ne 0$ everywhere.

For two lines through the origin, $\angle(\ell, m) \in [0^\circ, 90^\circ]$ is the angle between them.

**Theorem.** Let $S_1$ and $S_2$ be patches with tangent cones $K_1$ and $K_2$. Assume that there is a vector $w \ne 0$ with

$$w^\perp \cap K_1 \cap K_2 = \{0\}.$$

1. *No loop.* No closed curve lies in $S_1 \cap S_2$.
2. *Branches reach the boundary.* At every common point the tangent planes differ. If the patches are $C^\infty$, every connected component of the set of common points that are interior to both patches is a $C^1$ curve that is not closed, and its limit points at both ends lie on the boundary of $S_1$ or of $S_2$.

**Corollary (normal cones).** Let $a_1$ and $a_2$ be unit vectors, let $\varphi = \angle(a_1, a_2)$, and assume that $\angle(N_i(p), a_i) \le \alpha_i$ for every point $p$ of $S_i$, for $i = 1, 2$. If

$$\alpha_1 + \alpha_2 < \varphi,$$

the hypothesis of the theorem holds with $w = a_1 \times a_2$, so the patches do not meet in a closed curve. The condition says that the double cones $\{v : \angle(v, a_i) \le \alpha_i\}$ meet only at the origin.

## In plain words

Every surface has, at each point, a flat plane that just touches it. Collect all these touching planes of one patch, moved to a common point. They fill a region of directions in which the patch can run.

If two patches meet in a closed loop, the loop runs in a direction that both patches allow, and it turns all the way round. So it runs in every direction of some flat plane, at least once. The test looks for one flat plane that has no direction that both patches allow. If such a plane exists, a closed loop is not possible.

In a subdivision method, this means that a pair of small pieces can only meet in curves that start and end on the edges of the pieces. To find all of them, it is sufficient to look along the edges.

## Proof

**Part 1.** Let $c$ be a closed curve in $S_1 \cap S_2$. For each $i$, the curve $c$ lies in $S_i = x_i(D_i)$, and $x_i$ is a $C^1$ embedding of a neighborhood of $D_i$, so $c'(t)$ is in the tangent plane $T_i(c(t))$. Thus

$$c'(t) \in T_1(c(t)) \cap T_2(c(t)) \subseteq K_1 \cap K_2 \quad \text{for every } t.$$

The function $h(t) = w \cdot c(t)$ is continuous on a circle, so it has a maximum at some $t_0$. As $h$ is differentiable, $h'(t_0) = w \cdot c'(t_0) = 0$, so $c'(t_0) \in w^\perp \cap K_1 \cap K_2 = \{0\}$. This is not possible, because $c' \ne 0$.

**Part 2.** Assume $T_1(p) = T_2(p) = T$ at a common point $p$. Two planes through the origin in $\mathbb{R}^3$ meet in at least a line, so $T \cap w^\perp$ holds a vector $v \ne 0$. Then $v \in T_1(p) \cap T_2(p) \subseteq K_1 \cap K_2$, against the hypothesis. So the tangent planes differ at every common point.

Now let the patches be $C^\infty$, and let $M$ be the set of common points that are interior points of both patches. Near $p \in M$, write $S_2$ as the zero set of a $C^\infty$ function $g$ with $\nabla g(p) \ne 0$, so that $T_2(p) = \nabla g(p)^\perp$. Since $T_1(p) \ne T_2(p)$, the plane $T_1(p)$ is not in $\nabla g(p)^\perp$, so the restriction of $g$ to $S_1$ has a nonzero differential at $p$. By the implicit function theorem, $M$ is a smooth curve near $p$. So $M$ is a smooth 1-manifold, and each connected component is diffeomorphic to a circle or to an open interval [Milnor, Appendix]. A component that is a circle is a closed curve in $S_1 \cap S_2$, which part 1 excludes. So each component is the image of a smooth embedding $\gamma$ of an open interval $(t_-, t_+)$.

Let $q$ be a limit point of $\gamma(t_k)$ with $t_k \to t_+$; it exists because $S_1 \cap S_2$ is compact, and $q \in S_1 \cap S_2$. If $q \in M$, then near $q$ the set $M$ is one arc, so $\gamma(t_k)$ for large $k$ lies on the component of $q$, which is then the component of $\gamma$. As $\gamma$ is a homeomorphism onto its image, $t_k$ tends to $\gamma^{-1}(q)$, which is less than $t_+$. That is a contradiction, so $q \notin M$, and $q$ is a boundary point of $S_1$ or of $S_2$. The same holds at $t_-$. $\square$

**Corollary.** As $\varphi > 0$, the vectors $a_1$ and $a_2$ are independent, $w = a_1 \times a_2 \ne 0$, and $w^\perp$ is the plane $P$ spanned by $a_1$ and $a_2$. The angle $\angle$ between lines is a metric, so it satisfies the triangle inequality. Let $v \ne 0$ be in $P \cap K_1 \cap K_2$, and let $\ell$ be its line. As $v \in K_1$, $v$ lies in some $T_1(p)$, so $\angle(\ell, N_1(p)) = 90^\circ$, and

$$90^\circ \le \angle(\ell, a_1) + \angle(a_1, N_1(p)) \le \angle(\ell, a_1) + \alpha_1.$$

Let $m_i$ be the line in $P$ normal to $a_i$. In the plane $P$, $\angle(\ell, m_1) = 90^\circ - \angle(\ell, a_1) \le \alpha_1$, and in the same way $\angle(\ell, m_2) \le \alpha_2$. The quarter turn in $P$ maps $a_i$ to $m_i$, so $\angle(m_1, m_2) = \varphi$. Then

$$\varphi = \angle(m_1, m_2) \le \angle(m_1, \ell) + \angle(\ell, m_2) \le \alpha_1 + \alpha_2,$$

against the assumption. So $P \cap K_1 \cap K_2 = \{0\}$.

For the last sentence: if $v$ is in both double cones, $\varphi \le \angle(v, a_1) + \angle(v, a_2) \le \alpha_1 + \alpha_2$. Conversely, if $\alpha_1 + \alpha_2 \ge \varphi$, the line in $P$ between $a_1$ and $a_2$ at the angle $\min(\alpha_1, \varphi)$ from $a_1$ is at the angle $\varphi - \min(\alpha_1, \varphi) \le \alpha_2$ from $a_2$, so it lies in both cones. $\blacksquare$

## Consequences

- **A stop test for subdivision.** For a pair of pieces from a [subdivision](/subdivision-surface-intersection/), bound the normals of each piece by a cone with axis $a_i$ and half angle $\alpha_i$. For a Bézier piece, such a cone can be computed from the control points of its normal patch (Kim, Papalambros and Woo). If $\alpha_1 + \alpha_2 < \varphi$, the pair holds no closed loop, so it is not split again.
- **Start points from the boundary.** When the test passes, part 2 shows that every branch inside the pair has its ends on the boundary curves of the pieces. A [curve surface intersection](/curve-surface-intersection/) of each boundary curve of one piece with the other piece finds a point on every branch, and [marching](/marching-surface-intersection/) from these points traces them all. This is the hybrid method of the [surface surface intersection](/surface-surface-intersection/) page.
- **When the test passes.** Choose $a_i$ as the normal at a point of the piece, and $\alpha_i$ as the largest angle from it. As two pieces shrink to points $p$ and $q$ with $\angle(N_1(p), N_2(q)) > 0$, continuity of the normals gives $\alpha_1, \alpha_2 \to 0$ and $\varphi \to \angle(N_1(p), N_2(q))$, so the test passes after finitely many splits. It never passes for a pair that holds a point where the normals of the two patches are parallel, because then the two double cones share that normal line. Such points are the [tangential intersections](/tangential-surface-intersection/), which need other methods.
- **No disk is needed.** The proof of part 1 uses only the height function $w \cdot c$. It does not use that a loop bounds a disk on each patch, so it holds for any embedded $C^1$ surfaces, also for pieces that are not simply connected.

## Tightness

- **The constant is sharp.** Take $a_1 \cdot a_2 \ge 0$, and let $0 < \delta < \alpha_1 - \varphi$. The plane $x \cdot a_2 = \cos \delta$ cuts the unit sphere in a circle of angular radius $\delta$ about $a_2$, and every point of the circle is within the angle $\varphi + \delta < \alpha_1$ of $a_1$. Let $S_1$ be a patch of the sphere that holds the circle and lies in the cap of angular radius $\alpha_1$ about $a_1$, so that its normals are within $\alpha_1$ of $a_1$. Let $S_2$ be a square of the plane that holds the circle, so that $\alpha_2 = 0$. The circle is a closed loop of $S_1 \cap S_2$. So for every $\alpha_1 > 0$ and every $\varphi < \alpha_1$ there are patches with $\alpha_2 = 0$ and a loop, and the strict inequality cannot be weakened.
- **Disjoint normal sets are not enough for general pieces.** Part 1 of the theorem uses only that $c'$ lies in the tangent planes, so it holds for any embedded $C^1$ surfaces. The cylinder $x^2 + y^2 = 1$, $|z| \le 2$ has only horizontal normals, and the plane $z = x / 10$ has normals that are nearly vertical. No normal line of one is a normal line of the other, but the two meet in a closed ellipse. The tangent planes of the cylinder are all the vertical planes, whose union is all of $\mathbb{R}^3$, so the hypothesis of the theorem fails, as it must. The cylinder is not a disk. For two patches that are disks, Sederberg, Christiansen and Katz proved that a closed loop forces a line normal to both patches, which is a different test (cited, not proved here).
- **Oriented normals are not enough.** A patch of the unit sphere in $z > 0$ that holds the circle $z = 1/2$, with outward normals, and a square of the plane $z = 1/2$ that holds the circle, with normal $(0, 0, -1)$, have disjoint sets of unit normals, and they meet in the circle. The test must use lines, not unit vectors.
- **The converse fails.** Two parallel planes have $\varphi = 0$, so the test fails, but they do not meet at all. The condition is sufficient, not necessary.

## History

Sederberg and Meyers published a loop test for surface patch intersection in 1988. It uses cones that bound the normals and the tangent planes of the two patches, so that a [subdivision](/subdivision-surface-intersection/) can stop on a pair that cannot hold a small closed loop. The theorem on this page is a form of that test with tangent cones, with a full proof; the exact wording of the 1988 test is not restated. In 1989 Sederberg, Christiansen and Katz gave an improved test: if two patches meet in a closed loop, some line is normal to both patches. Hohmeyer built a full surface intersection algorithm on loop detection in 1991, and Kim, Papalambros and Woo studied the computation of tangent and normal cones of Bézier surfaces in 1995.

## References
