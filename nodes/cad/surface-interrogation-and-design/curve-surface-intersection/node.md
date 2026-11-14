---
tag: DYYWZ3
kind: problem
slug: curve-surface-intersection
name: Curve surface intersection
aliases:
- curve and surface intersection
area: cad/surface-interrogation-and-design
level: core
summary: Find all points where a parametric curve meets a parametric or implicit surface, the step that feeds lattice methods, ray tracing of patches and edge splitting.
prereqs: [parametric-surface, implicit-surface, curve-intersection]
see_also: [surface-surface-intersection, lattice-evaluation-intersection, implicitization, interval-projected-polyhedron, bezier-clipping, ray-object-intersection, real-root-isolation, minimum-distance-between-surfaces]
sources:
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 5, Section 5.7, Curve/surface intersection, with 5.7.1 (a rational polynomial curve against an implicit algebraic surface, by substitution) and 5.7.2 (against a rational polynomial surface, by implicitization, by subdivision and by the interval projected polyhedron method)
  - paper: doi:10.1016/0734-189X(84)90140-3
    title: Thomas W. Sederberg, David C. Anderson and Ronald N. Goldman, Implicit representation of parametric curves and surfaces, Computer Vision, Graphics, and Image Processing 28(1), 72 to 84, 1984
    locator: the whole paper (implicit equations of rational curves and surfaces by resultants, and their use to turn a parametric intersection into the roots of one polynomial)
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the chapters on Bézier curves and tensor product Bézier patches (the convex hull property and subdivision that the subdivision methods use; general locator)
---

Curve surface intersection asks for every point where a curve $c(\tau)$ meets a surface, given as a parametric patch $r(u, v)$ or as the zero set of a polynomial $f(x, y, z)$. In the parametric case the answer is the set of solutions of the three equations $c(\tau) = r(u, v)$ in three unknowns, so the points are isolated except when the curve lies in the surface. The problem is a building block: lattice methods for [surface surface intersection](/surface-surface-intersection/) intersect many curves with one surface, a ray tracer intersects rays with patches, and a modeler splits the edges of a B-rep where they cross a face. The hard parts are to find every point, including those where the curve only touches the surface, and to tell touching from crossing.

## In plain words

A wire passes through a curved sheet. You want every spot where the wire meets the sheet. The wire is drawn by a formula with one number, the sheet by a formula with two numbers, and a meeting point is where both formulas give the same point in space. That is three equations, one for each direction in space, in three unknown numbers, so the answer is usually a few separate points.

Most points are clean crossings, where the wire goes from one side of the sheet to the other. Some are touching points, where the wire just grazes the sheet and stays on one side. Those are hard to find, because a small change in the shape turns one touching point into two crossings or into none. In the worst case the wire lies inside the sheet for a while, and the answer is a piece of curve.

## Definition

**Input.** A regular curve $c : [a, b] \to \mathbb{R}^3$, polynomial or rational, such as a [Bézier curve](/bezier-curve/), a [B-spline](/b-spline/) or a [NURBS](/nurbs/) curve. A surface, either a regular parametric patch $r : \Omega \to \mathbb{R}^3$ on a box $\Omega$, or an implicit surface $\{x : f(x) = 0\}$ for a polynomial $f$. A tolerance $\varepsilon > 0$ for the numerical case.

**Output.** All parameter values $\tau \in [a, b]$, with the matching $(u, v) \in \Omega$ in the parametric case, at which the curve meets the surface:

$$F(\tau, u, v) = c(\tau) - r(u, v) = 0 \qquad \text{or} \qquad g(\tau) = f(c(\tau)) = 0,$$

each point with its type: *transversal* when the curve crosses the surface there, *tangential* when the tangent $c'(\tau)$ lies in the tangent plane of the surface. If the curve lies in the surface over an interval, that interval is reported as an *overlap*. In the numerical version each reported point is within $\varepsilon$ of a true point, and the true points and the reported ones are in one to one correspondence.

**When a point is regular.** At a point of the parametric case the Jacobian of $F$ is the $3 \times 3$ matrix with columns $c'(\tau)$, $-r_u$, $-r_v$, and

$$\det \big[\, c', \; -r_u, \; -r_v \,\big] = c' \cdot (r_u \times r_v).$$

*Proof.* Negating two columns leaves a determinant unchanged, so the determinant equals $\det[c', r_u, r_v]$, which is the triple product $c' \cdot (r_u \times r_v)$. $\square$

Since $r_u \times r_v$ is a nonzero multiple of the normal $N$, the Jacobian is nonsingular exactly when $c' \cdot N \ne 0$, that is, at a transversal point. So transversal points are regular solutions of the system: they are isolated, they move continuously when the curve and the surface move a little, and [Newton's method for systems](/newton-method-for-systems/) converges quadratically to them. Tangential points are singular solutions, with none of these properties. In the implicit case the same holds with $g'(\tau) = \nabla f \cdot c'(\tau)$.

## Variants

- **Rational polynomial curve and implicit algebraic surface.** Substitute: $g(\tau) = f(c(\tau))$ is one polynomial in one unknown, and the problem is the real roots of $g$ in $[a, b]$. This is the easy case, treated by Patrikalakis and Maekawa in Section 5.7.1.
- **Rational polynomial curve and rational polynomial surface.** The general CAD case, three equations in three unknowns, Section 5.7.2. It reduces to the first case by [implicitization](/implicitization/) of the patch, at the cost of a high degree.
- **Line and surface.** The curve is a line or a ray. This is ray casting of a surface, see [ray object intersection](/ray-object-intersection/). It is also the directional variant of [point projection](/point-projection-onto-a-surface/).
- **Isoparametric curve.** The curve is a parameter line of a second surface, $\tau \mapsto r_2(\tau, v_0)$. Lattice methods for surface intersection solve many of these, see [lattice evaluation intersection](/lattice-evaluation-intersection/).
- **Plane curves.** With a curve and a curve in the plane, the problem is [curve intersection](/curve-intersection/), two equations in two unknowns.

## Examples

- **A twisted cubic and a plane.** The curve $c(\tau) = (\tau, \tau^2, \tau^3)$ meets the plane $x + y + z = 1$ where $\tau^3 + \tau^2 + \tau - 1 = 0$. The derivative $3\tau^2 + 2\tau + 1$ has no real root, so the cubic is increasing and has exactly one real root, $\tau \approx 0.543689$, at the point $(0.543689, 0.295598, 0.160713)$. There $c' \cdot (1, 1, 1) = 3\tau^2 + 2\tau + 1 \approx 2.974 \ne 0$, so the point is transversal.
- **A line through a bump.** Let $r(u, v) = (3u, 3v, 27 u (1 - u) v (1 - v))$, the bicubic bump with control points $(i, j, z_{ij})$, $z_{ij} = 3$ for the four inner points and $0$ for the others. The line $c(\tau) = (\tau, 1.5, 1)$ forces $v = \tfrac12$ and $u = \tau / 3$, and then $\tfrac{27}{4} u (1 - u) = 1$, so $u (1 - u) = \tfrac{4}{27}$ and $u = \tfrac12 (1 \pm \sqrt{11/27})$. The two points are at $u \approx 0.180858$ and $u \approx 0.819142$, so $\tau \approx 0.542573$ and $\tau \approx 2.457427$. Both are transversal: the slope of the bump along the line is $\tfrac{27}{4}(1 - 2u) \approx \pm 4.308$, not $0$.
- **A tangential point.** The line $(\tau, 1.5, \tfrac{27}{16})$ through the top of the same bump gives $u (1 - u) = \tfrac14$, a double root at $u = \tfrac12$. The line touches the bump at its top, and raising the line by any amount removes the point, while lowering it splits the point in two.
- **An overlap.** The line $(\tau, 0, 0)$ lies in the bump along the edge $v = 0$, where the height is $0$. Every $\tau \in [0, 3]$ is a solution.
- **A line and a sphere.** The line $p + \tau d$ with $|d| = 1$ meets the sphere $|x|^2 = R^2$ where $\tau^2 + 2 (p \cdot d) \tau + |p|^2 - R^2 = 0$, two points, one tangential point or none by the sign of the discriminant $(p \cdot d)^2 - |p|^2 + R^2$.

## Known algorithms

- **Substitution and root isolation.** For an implicit surface, form $g = f \circ c$ and find its real roots with [real root isolation](/real-root-isolation/), a [Sturm sequence](/sturm-sequence/), or [Bézier clipping](/bezier-clipping/) on the Bernstein form of $g$. With exact rational coefficients this is a certified method, and the multiplicity of each root tells crossings from touchings.
- **Implicitization.** Compute the implicit equation of the patch by a [resultant](/resultant/), as Sederberg, Anderson and Goldman (1984) proposed, and substitute the curve. The degree is high, up to $18$ for a bicubic patch, and the coefficients grow, so this is used mostly for low degrees.
- **Subdivision.** Split the curve and the patch with the [de Casteljau algorithm](/de-casteljau-algorithm/) and discard pairs whose [convex hulls](/convex-hull-property/), or bounding boxes, do not overlap. When the pieces are flat enough, intersect a segment with a pair of triangles and refine with Newton. It is robust for transversal points and slow near tangential ones.
- **Interval projected polyhedron.** Write the three equations in Bernstein form over the box of $(\tau, u, v)$ and use the [interval projected polyhedron](/interval-projected-polyhedron/) method, which finds all roots in the box with outward rounding. Patrikalakis and Maekawa, Section 5.7.2.3.
- **Bézier clipping.** The clipping idea of [Bézier clipping](/bezier-clipping/) extends from two curves to a ray and a patch: project the patch onto two planes that contain the ray, which gives two equations in $(u, v)$, and clip the parameter box with the convex hulls of the projected control points.
- **Newton.** From a start point on each intersection, Newton on $F = 0$ converges quadratically at transversal points. It is the refinement step of the other methods, and on its own it misses points that have no start.

## Bounds

**Degree bound, implicit surface.** If $c$ is a polynomial curve of degree $d$ and $f$ has degree $k$, then $g = f \circ c$ has degree at most $kd$, so the curve meets the surface in at most $kd$ points unless $g$ is the zero polynomial, in which case the whole curve lies in the surface. For a rational curve $c = P / w$ of degree $d$, the numerator $w^k f(P / w)$ of $g$, the homogenized $f$ evaluated at $(P, w)$, has degree at most $kd$, with the same conclusion. A line meets a quadric in at most $2$ points, and a cubic curve meets a quadric in at most $6$.

*Proof.* Each monomial of $f$ of degree $j \le k$ becomes a product of $j$ coordinates of $c$, of degree at most $jd \le kd$. In the rational case multiply each monomial by $w^{k - j}$. A nonzero polynomial of degree at most $kd$ has at most $kd$ roots. $\square$

**Degree bound, parametric patch.** A rational tensor product patch of bidegree $(m, n)$ has an implicit equation of degree at most $2mn$, so a rational curve of degree $d$ meets it in at most $2mnd$ points, or lies in its implicit surface. For a bicubic patch and a line this is $18$. The patch bound counts the points where a general line meets the patch, as the solutions in $\mathbb{P}^1 \times \mathbb{P}^1$ of two equations of bidegree $(m, n)$, of which there are $2mn$ by Bézout's theorem for bidegree systems. That theorem is cited here, not proved. Base points lower the degree.

**Stability.** Transversal points are regular solutions, as proved above, so they persist and move continuously under small changes of the data, by the implicit function theorem. A tangential point of multiplicity $2$ can split into two transversal points or vanish under an arbitrarily small change, as the line through the top of the bump shows. So no method that works with a fixed precision can decide whether a tangential point exists, and certified methods report it as a box that may hold zero, one or two points.

## Reductions

- **To one polynomial.** With an implicit surface, the problem is the real roots of one polynomial in one unknown.
- **To a square system.** In the parametric case it is three polynomial equations in three unknowns over a box, a case of [systems of nonlinear equations](/systems-of-nonlinear-equations/).
- **From curve intersection in the plane.** Two plane curves $c_1(\tau)$ and $c_2(\sigma)$ meet where the curve $(c_1(\tau), 0)$ meets the surface $(c_2(\sigma), z)$, a cylinder over $c_2$, so curve surface intersection solves [curve intersection](/curve-intersection/).
- **To surface intersection.** Lattice methods reduce [surface surface intersection](/surface-surface-intersection/) to many curve surface problems along the parameter lines of one surface.
- **To distance.** The curve meets the surface exactly when the [minimum distance](/minimum-distance-between-surfaces/) between them is $0$.

## Applications

- **Ray tracing of patches.** Each ray is a line, so rendering trimmed NURBS models directly needs a line and patch intersection per ray.
- **Boolean operations.** An edge of one solid is split where it crosses a face of the other, and the new vertices of the result are curve surface intersections.
- **Lattice methods.** Intersecting the parameter lines of one patch with the other gives points on the intersection curve of two surfaces, see [lattice evaluation intersection](/lattice-evaluation-intersection/).
- **Start points for marching.** The points where the boundary curves of one patch meet the other surface are the start points of the open branches of an intersection curve, used by [marching](/marching-surface-intersection/).
- **Machining and inspection.** A probe or a tool moves along a line, and its first contact with the part is a line and surface intersection.

## References
