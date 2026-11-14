---
tag: WD40CR
kind: theorem
slug: maximum-angle-condition
name: Babuska-Aziz maximum angle condition
aliases:
- maximum angle condition
area: cad/mesh-generation-for-analysis
level: advanced
summary: Linear finite element interpolation on triangles converges in H^1 if all angles stay bounded away from 180 degrees, so small angles alone are harmless.
prereqs: [finite-element-method, lagrange-interpolation, triangulation]
see_also: [mesh-quality-measures, radius-edge-ratio, sliver-tetrahedron, galerkin-method, delaunay-refinement, anisotropic-mesh-adaptation, boundary-layer-mesh-generation, cotangent-laplacian]
sources:
  - paper: doi:10.1137/0713021
    title: Ivo Babuška and A. K. Aziz, On the angle condition in the finite element method, SIAM Journal on Numerical Analysis 13(2), 1976, 214 to 226
    locator: the H1 interpolation estimate for triangles whose angles are at most a fixed gamma below pi, and the example that shows the bound fails as the largest angle tends to pi (general locator)
  - paper: "J. L. Synge, The Hypercircle in Mathematical Physics, Cambridge University Press, 1957"
    locator: Section 3.8, linear interpolation on triangles under a bound on the largest angle (section number as cited by later authors)
  - paper: "Miloš Zlámal, On the finite element method, Numerische Mathematik 12, 1968, 394 to 409"
    locator: the minimum angle condition for triangular elements
  - paper: "Michal Křížek, On the maximum angle condition for linear tetrahedral elements, SIAM Journal on Numerical Analysis 29(2), 1992, 513 to 520"
    locator: the condition for tetrahedra, with the dihedral angles and the face angles bounded away from pi
  - paper: "Antti Hannukainen, Sergey Korotov and Michal Křížek, The maximum angle condition is not necessary for convergence of the finite element method, Numerische Mathematik 120, 2012, 79 to 88"
    locator: a family of meshes that violates the condition while the finite element solutions still converge
  - paper: "Jonathan Richard Shewchuk, What is a good linear element? Interpolation, conditioning, and quality measures, Proceedings of the 11th International Meshing Roundtable, Sandia National Laboratories, 2002, 115 to 126"
    locator: large angles and interpolation error against small angles and conditioning (general locator)
---

The maximum angle condition says that piecewise linear interpolation on triangles approximates gradients well as long as no angle of any triangle comes close to $180°$. The error bound depends on the largest angle, not on the smallest, so long thin triangles with a small angle and no large angle are allowed. Babuška and Aziz proved it in 1976 for the $H^1$ norm that governs the [finite element method](/finite-element-method/), and it replaced the older minimum angle condition. It explains why a mesh needs no large angles for accuracy, while small angles hurt only the conditioning of the linear system.

## Statement

Let $T$ be a closed triangle with diameter $h_T$ (its longest edge). For a continuous $u$ on $T$, let $\Pi_T u$ be the linear function that agrees with $u$ at the three vertices, the [Lagrange interpolant](/lagrange-interpolation/) of degree 1. Write $|v|_{1,T}^2 = \int_T |\nabla v|^2$ and $|u|_{2,T}^2 = \int_T (u_{xx}^2 + 2 u_{xy}^2 + u_{yy}^2)$ for the Sobolev seminorms, and $H^2(T)$ for the functions with square integrable derivatives up to order 2. In two dimensions every $u \in H^2(T)$ is continuous, so $\Pi_T u$ is defined.

**Theorem (Babuška and Aziz).** For every angle $\gamma < \pi$ there is a constant $C(\gamma)$ such that, for every triangle $T$ whose angles are all at most $\gamma$ and every $u \in H^2(T)$,

$$|u - \Pi_T u|_{1,T} \le C(\gamma) \, h_T \, |u|_{2,T}.$$

The constant depends only on $\gamma$. It does not depend on the smallest angle of $T$, on its shape otherwise, or on its size.

**Theorem (pointwise form).** Let $T$ have largest angle $\theta_{\max} \le \gamma < \pi$, and let $u$ be twice continuously differentiable on $T$ with $\|D^2 u(x)\| \le M$ for all $x \in T$, where $\| \cdot \|$ is the operator norm of the Hessian matrix. Then

$$\max_{x \in T} |\nabla (u - \Pi_T u)(x)| \le \frac{2 M h_T}{\sin \theta_{\max}} \le \frac{2 M h_T}{\min(\sin \gamma, \sqrt{3}/2)}.$$

## In plain words

To approximate a curved surface by flat triangles, you match the surface at the corners of each triangle. The heights then come out close, but the slopes can be badly wrong. The slopes go wrong when a triangle has one corner that is almost a straight line, because then the triangle cannot see the surface bend across its short side. A triangle that is only very thin, with one sharp corner but no wide corner, is fine for slopes. So for accurate slopes the rule is to avoid wide corners, not sharp ones. Sharp corners cause a different problem: they make the equations of the simulation harder to solve accurately.

## Proof

The $H^1$ form is the theorem of Babuška and Aziz. Its proof is long, and we cite it. The pointwise form shows the same mechanism with an elementary proof, which follows.

Let $w = u - \Pi_T u$. Then $w$ is zero at the three vertices of $T$, and, since $\Pi_T u$ is linear, $D^2 w = D^2 u$. For any two points $x, y$ of $T$, apply the mean value inequality to $\nabla w$ along the segment from $y$ to $x$, which lies in $T$ because $T$ is convex:

$$|\nabla w(x) - \nabla w(y)| \le M |x - y| \le M h_T.$$

Let $p$ be the vertex with the largest angle $\theta = \theta_{\max}$, and let $q_1$, $q_2$ be the other two vertices. Let $t_i = (q_i - p)/|q_i - p|$ be the unit vectors along the two edges at $p$, so the angle between $t_1$ and $t_2$ is $\theta$. The function $s \mapsto w(p + s t_1)$ is zero at $s = 0$ and at $s = |q_1 - p|$. By Rolle's theorem its derivative is zero at some point between, so there is a point $\xi_1$ on the edge $p q_1$ with $\nabla w(\xi_1) \cdot t_1 = 0$. In the same way there is $\xi_2$ on $p q_2$ with $\nabla w(\xi_2) \cdot t_2 = 0$. For every $x \in T$ and $i = 1, 2$,

$$|\nabla w(x) \cdot t_i| = |(\nabla w(x) - \nabla w(\xi_i)) \cdot t_i| \le M h_T.$$

Now let $g = \nabla w(x)$. The vectors $t_1$, $t_2$ form a basis of the plane, because $0 < \theta < \pi$. Let $d_1$, $d_2$ be the dual basis, with $d_i \cdot t_j = 1$ if $i = j$ and $0$ otherwise. Then $d_1$ is perpendicular to $t_2$ and $d_1 \cdot t_1 = 1$, so $|d_1| \sin \theta = 1$, and the same holds for $d_2$. Since $g = (g \cdot t_1) d_1 + (g \cdot t_2) d_2$,

$$|g| \le \frac{|g \cdot t_1| + |g \cdot t_2|}{\sin \theta} \le \frac{2 M h_T}{\sin \theta}.$$

Finally, the largest angle of a triangle is at least $\pi/3$, so $\theta \in [\pi/3, \gamma]$. The sine is concave on $[0, \pi]$, so on this interval it is at least its smaller endpoint value, $\min(\sin(\pi/3), \sin \gamma)$. $\blacksquare$

The proof uses only the two edges at the largest angle, and the only place where the shape enters is $1/\sin \theta_{\max}$. A small angle elsewhere in the triangle changes nothing. Integration of the pointwise bound over $T$ gives $|w|_{1,T} \le 2 M h_T |T|^{1/2} / \sin \theta_{\max}$ for $u \in C^2(T)$, which is the $H^1$ estimate with $M |T|^{1/2}$ in place of $|u|_{2,T}$.

## Consequences

**Convergence of linear elements.** For an elliptic problem with a coercive bilinear form, Céa's lemma for the [Galerkin method](/galerkin-method/) bounds the energy error of the finite element solution $u_h$ by a constant times the best approximation error from the finite element space. The global interpolant of $u$ is in that space. So if every triangle of every mesh in a family has all its angles at most $\gamma < \pi$, then $|u - u_h|_1 \le C h |u|_2$ with $h$ the largest diameter, and the method converges at first order as $h \to 0$ for $u \in H^2$.

**The minimum angle condition is stronger than needed.** Zlámal's condition asks that every angle be at least some $\theta_0 > 0$. That implies the maximum angle condition with $\gamma = \pi - 2\theta_0$. The converse fails: right triangles with legs $1$ and $\varepsilon$ satisfy the maximum angle condition with $\gamma = \pi/2$ for every $\varepsilon$, and have a smallest angle that tends to 0.

**Anisotropic meshes.** Long thin triangles with no large angle are allowed. This is the basis of [anisotropic mesh adaptation](/anisotropic-mesh-adaptation/) and of [boundary layer meshes](/boundary-layer-mesh-generation/), where elements are much longer along the flow than across it. Such meshes need the stretched triangles to be close to right triangles, not obtuse.

**Small angles still cost something.** The stiffness matrix of the Laplacian for linear triangles has off-diagonal entries $-\frac{1}{2}(\cot \alpha + \cot \beta)$, the [cotangent Laplacian](/cotangent-laplacian/). A small angle $\alpha$ makes $\cot \alpha$ large, which raises the [condition number](/condition-number/) of the matrix. So a small angle is harmless for the interpolation error but not for the solver. This is why [mesh quality measures](/mesh-quality-measures/) track both.

**Meshers.** [Delaunay refinement](/delaunay-refinement/) bounds the smallest angle by $\theta_0$, and so the largest angle by $\pi - 2\theta_0$; it meets the condition with room to spare. In three dimensions, Křížek proved the analogous condition for tetrahedra: all dihedral angles and all face angles at most $\gamma < \pi$. A [sliver tetrahedron](/sliver-tetrahedron/) has dihedral angles near $\pi$ and violates it.

## Tightness

**A large angle makes the gradient error unbounded.** Let $T_\varepsilon$ have vertices $(-1, 0)$, $(1, 0)$, $(0, \varepsilon)$ and let $u = x^2$. Then $\Pi u = 1 - y/\varepsilon$, since this is 1 at the first two vertices and 0 at the third. So $\nabla(u - \Pi u) = (2x, 1/\varepsilon)$, and its size is at least $1/\varepsilon$ everywhere on $T_\varepsilon$, while $h = 2$ and $M = 2$ stay fixed. The largest angle is at $(0, \varepsilon)$, with $\sin \theta_{\max} = 2\varepsilon / (1 + \varepsilon^2)$, so the pointwise bound is $4(1 + \varepsilon^2)/\varepsilon$. The true maximum, $\sqrt{4 + 1/\varepsilon^2}$, is within a factor of 4 of it as $\varepsilon \to 0$, so the dependence on $\theta_{\max}$ cannot be removed. In the $H^1$ form, $\int_{T_\varepsilon} x^2 = \varepsilon/6$, so $|u - \Pi u|_{1}^2 = 2\varepsilon/3 + 1/\varepsilon$, and $|u|_{2}^2 = 4\varepsilon$. The ratio $|u - \Pi u|_1 / (h |u|_2) = \frac{1}{2}\sqrt{1/6 + 1/(4\varepsilon^2)}$ tends to infinity, so no constant $C$ works for all triangles once $\gamma$ may approach $\pi$.

**A small angle alone is harmless.** Let $S_\varepsilon$ have vertices $(0, 0)$, $(1, 0)$, $(0, \varepsilon)$, with angles $90°$, $\arctan \varepsilon$ and $90° - \arctan \varepsilon$. Linear functions are reproduced exactly, so it is enough to check the three quadratic monomials.

| $u$ | $\Pi u$ | $\nabla (u - \Pi u)$ | largest size on $S_\varepsilon$ |
| --- | --- | --- | --- |
| $x^2$ | $x$ | $(2x - 1, 0)$ | $1$ |
| $y^2$ | $\varepsilon y$ | $(0, 2y - \varepsilon)$ | $\varepsilon$ |
| $x y$ | $0$ | $(y, x)$ | $1$ |

All three errors stay bounded as $\varepsilon \to 0$, although the smallest angle tends to 0. The pointwise theorem gives the bound $2 M \sqrt{1 + \varepsilon^2}$ with $\sin \theta_{\max} = 1$.

**The condition is sufficient, not necessary.** Hannukainen, Korotov and Křížek built families of meshes in which some triangles have angles that tend to $\pi$, and for which the finite element solutions still converge. The bad triangles there are few enough that the global error does not see them. The condition is about each triangle's interpolation error, not about the convergence of every mesh family.

## History

Synge stated a bound on the largest angle for linear interpolation on triangles in his 1957 book on the hypercircle method. Zlámal in 1968 proved convergence of linear finite elements under a lower bound on all angles, and Ženíšek found the same condition independently in the same year. In 1976 Babuška and Aziz proved the $H^1$ interpolation estimate under a bound on the largest angle only, and showed by the example of $u = x^2$ on flat triangles that the condition cannot be dropped from the estimate. Other authors proved related results independently in the same year. Křížek extended the condition to tetrahedra in 1992. Hannukainen, Korotov and Křížek showed in 2012 that the condition is not necessary for the convergence of the finite element method.

## References
