---
tag: 5ZV0HM
kind: concept
slug: mesh-quality-measures
name: Mesh quality measures
aliases:
- element quality metric
- Knupp quality metrics
area: cad/mesh-generation-for-analysis
level: core
summary: Numbers such as the minimum angle, aspect ratio, radius ratio and scaled Jacobian that rate how well an element serves interpolation and the stiffness matrix.
prereqs: [triangulation, tetrahedralization, finite-element-method]
see_also: [radius-edge-ratio, scaled-jacobian, sliver-tetrahedron, maximum-angle-condition, mesh-sizing-function, optimization-based-mesh-smoothing, mesh-untangling, mesh-generation]
sources:
  - paper: "Jonathan Richard Shewchuk, What is a good linear element? Interpolation, conditioning, and quality measures, Proceedings of the 11th International Meshing Roundtable, Sandia National Laboratories, 2002, 115 to 126"
    locator: the link of each measure to interpolation error and to the conditioning of the stiffness matrix, and the list of triangle and tetrahedron measures (general locator)
  - paper: doi:10.1137/S1064827500371499
    title: Patrick M. Knupp, Algebraic mesh quality metrics, SIAM Journal on Scientific Computing 23(1), 2001, 193 to 218
    locator: quality metrics built from the corner Jacobian matrices relative to an ideal element, their invariance, and the equivalence of the condition number and mean ratio metrics
  - paper: doi:10.1007/BF01955874
    title: Anwei Liu and Barry Joe, Relationship between tetrahedron shape measures, BIT 34(2), 1994, 268 to 287
    locator: the minimum solid angle, the radius ratio and the mean ratio of a tetrahedron, their maximum only at the regular tetrahedron, and power bounds between each pair
  - paper: doi:10.1137/0713021
    title: Ivo Babuška and A. K. Aziz, On the angle condition in the finite element method, SIAM Journal on Numerical Analysis 13(2), 1976, 214 to 226
    locator: the maximum angle condition for linear interpolation on triangles
---

A mesh quality measure is a number computed from the shape of one element that rates how well the element serves a [finite element](/finite-element-method/) computation. Common measures are the smallest and largest angles, the [radius-edge ratio](/radius-edge-ratio/), the aspect ratio, the radius ratio, the mean ratio and the [scaled Jacobian](/scaled-jacobian/). Each measure has a range, an ideal value that the regular element reaches, and a set of bad shapes that it detects. No single measure detects every defect, so mesh generators, smoothers and solvers each choose the measures that match the errors they care about.

## In plain words

A mesh cuts a region into many small triangles or tetrahedra, and a simulation computes on each piece. Some pieces help the computation and some hurt it. A thin, flat piece can make the computed answer wrong, or it can make the equations hard to solve. A quality measure is a score for one piece. It is best for a perfectly even piece, and it gets worse as the piece gets stretched, flat or turned inside out. Different scores notice different problems. One score sees a very short side, another sees a corner that is almost a straight line, another sees a piece with almost no volume. Mesh programs compute these scores to decide which pieces to split, which points to move, and whether the mesh is good enough to use.

## The idea

**Two separate harms.** Shewchuk's analysis of linear elements separates two effects. The first is interpolation error: the piecewise linear interpolant of a smooth function has a gradient error that grows without bound when an angle of a triangle tends to $180°$. The [maximum angle condition](/maximum-angle-condition/) of Babuška and Aziz makes this exact. The second is conditioning: the stiffness matrix of the Laplacian has entries that are cotangents of angles (the [cotangent Laplacian](/cotangent-laplacian/)), so a small angle makes a large entry and raises the [condition number](/condition-number/). A triangle with one small angle and no large angle is harmless for the error but bad for conditioning. A triangle with an angle near $180°$ is bad for both. A measure is useful when it tracks the harm that matters for the task.

**Ranges and ideal values.** The table lists common measures for a triangle with edges $\ell_1, \ell_2, \ell_3$, area $A$, inradius $r$, circumradius $R$ and angles $\theta_i$. Each one is invariant under translations, rotations, reflections (except the signed scaled Jacobian) and uniform scaling, so it depends only on the shape.

| Measure | Formula | Range | Ideal | Detects | Misses |
| --- | --- | --- | --- | --- | --- |
| minimum angle | $\theta_{\min}$ | $(0°, 60°]$ | $60°$ | small angles | nothing in the plane |
| maximum angle | $\theta_{\max}$ | $[60°, 180°)$ | $60°$ | large angles | needles with no large angle |
| radius-edge ratio | $R / \ell_{\min}$ | $[1/\sqrt{3}, \infty)$ | $1/\sqrt{3}$ | small angles | nothing in the plane |
| edge ratio | $\ell_{\max} / \ell_{\min}$ | $[1, \infty)$ | $1$ | stretching | flat obtuse triangles |
| aspect ratio | $\sqrt{3}\, \ell_{\max}^2 / (4A)$ | $[1, \infty)$ | $1$ | every degeneracy | nothing |
| radius ratio | $2 r / R$ | $(0, 1]$ | $1$ | every degeneracy | nothing |
| mean ratio | $4\sqrt{3} A / \sum \ell_i^2$ | $(0, 1]$ | $1$ | every degeneracy | nothing |
| scaled Jacobian | $\frac{2}{\sqrt{3}} \min_i \sin \theta_i$ | $[-\frac{2}{\sqrt{3}}, 1]$ | $1$ | inversion, small and large angles | nothing |

The aspect ratio here is the longest edge over the shortest altitude, $\ell_{\max} / h_{\min} = \ell_{\max}^2 / (2A)$, times $\sqrt{3}/2$ so that the ideal value is 1. Other books use other normalizations, so a reported number needs its formula.

**Proofs of the ideal values.** In each case the ideal value is reached exactly by the equilateral triangle.

- *Minimum and maximum angle.* The angles add up to $180°$, so $\theta_{\min} \le 60° \le \theta_{\max}$, with equality only when all three angles are $60°$.
- *Aspect ratio.* Let $\theta$ be the smallest angle, between the edges $b$ and $c$. Then $A = \frac{1}{2} b c \sin \theta \le \frac{1}{2} \ell_{\max}^2 \sin 60°$, so $\sqrt{3}\, \ell_{\max}^2 / (4A) \ge 1$. Equality needs $b = c = \ell_{\max}$ and $\theta = 60°$.
- *Mean ratio.* This is Weitzenböck's inequality. With the angle $\alpha$ between $b$ and $c$, $a^2 = b^2 + c^2 - 2 b c \cos \alpha$ and $4\sqrt{3} A = 2\sqrt{3}\, b c \sin \alpha$. So $a^2 + b^2 + c^2 - 4 \sqrt{3} A = 2(b^2 + c^2) - 4 b c \cos(\alpha - 60°) \ge 2 (b - c)^2 \ge 0$. Equality needs $b = c$ and $\alpha = 60°$.
- *Radius ratio.* Euler's identity $|OI|^2 = R(R - 2r)$, for the circumcenter $O$ and the incenter $I$, gives $R \ge 2r$, with equality exactly when $O = I$, which holds only for the equilateral triangle.
- *Radius-edge ratio and scaled Jacobian.* These are proved on their own pages.

Each of the last four measures tends to its worst value whenever $A / \ell_{\max}^2 \to 0$, that is, for every flattening. The edge ratio does not: the flat triangle $(-1, 0), (1, 0), (0, 0.1)$ has edge ratio about $1.99$.

**Tetrahedra.** In space the same names apply with $V$ for the volume. The radius ratio is $3 r / R$, the mean ratio of Liu and Joe is $12 (3V)^{2/3} / \sum_{i<j} \ell_{ij}^2$, and the minimum and maximum dihedral angles replace the angles. Here the measures split into two groups. The radius-edge ratio and the edge ratio do not detect [slivers](/sliver-tetrahedron/), because a sliver has no short edge. The radius ratio, the mean ratio, the dihedral angles, the volume-edge ratio and the scaled Jacobian all tend to their worst values for slivers. Liu and Joe proved that the minimum solid angle, the radius ratio and the mean ratio of a tetrahedron are equivalent: each one is bounded above and below by constant multiples of powers of the other, and each one is at its best only for the regular tetrahedron.

**The radius ratio bound in any dimension.** For a $d$-simplex with inradius $r$ and circumradius $R$, $R \ge d\, r$, with equality only for the regular simplex. Proof. Let $H_i$ be the hyperplane of facet $i$, with area $A_i$, and let $s_i(x)$ be the signed distance from $x$ to $H_i$, positive on the side of the simplex. Cutting the simplex into cones from a point $x$ gives $\sum_i A_i s_i(x) = d V$ for every $x$, since both sides are affine in $x$ and agree inside the simplex. At the incenter all $s_i = r$, so $d V = r \sum_i A_i$. The homothety with center at the centroid and ratio $-1/d$ maps each vertex to the centroid $g_i$ of the opposite facet, so it maps the circumsphere to a sphere of radius $R/d$ with center $q$ that passes through every $g_i$. Then $s_i(q) \le |q - g_i| = R / d$ for each $i$, and so $r \sum_i A_i = \sum_i A_i s_i(q) \le (R/d) \sum_i A_i$. For equality, every facet must touch the sphere of radius $R/d$ at its centroid, so that sphere is the insphere. The tangent segments from one vertex to a sphere have equal lengths, so each vertex is at the same distance from the centroids of the facets that contain it. In the plane this makes the three sides equal. For a tetrahedron, the squared distance from $v_i$ to the centroid of the face $v_i v_j v_k$ is $(2 \ell_{ij}^2 + 2 \ell_{ik}^2 - \ell_{jk}^2)/9$, and the equal-distance conditions are a linear system of rank 5 in the six squared edge lengths, so all six are equal. $\blacksquare$

**The algebraic framework.** Knupp builds measures from the Jacobian matrix $A_p$ at each corner $p$, the matrix of edge vectors at $p$. With $W$ the same matrix for the ideal element, $T = A_p W^{-1}$ is the map from the ideal corner to the actual one. Then $\det T$ measures size and inversion, the condition number $|T|_F\, |T^{-1}|_F / d$ measures shape, and $d \, (\det T)^{2/d} / |T|_F^2$ is the mean ratio. These are invariant under rotations and uniform scaling of the element, and Knupp proved that the condition number and the mean ratio are equivalent measures of shape. The same framework covers quadrilaterals and hexahedra, where the scaled Jacobian, the minimum over the corners of $\det T$ for normalized edges, is the usual first check.

## Examples

The table gives each measure for five shapes. Ideal values are in the first row.

| Shape | $\theta_{\min}$ | $\theta_{\max}$ | radius-edge | edge ratio | aspect | radius ratio | mean ratio | scaled Jacobian |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| equilateral | $60°$ | $60°$ | $0.577$ | $1$ | $1$ | $1$ | $1$ | $1$ |
| right isosceles | $45°$ | $90°$ | $0.707$ | $1.414$ | $1.732$ | $0.828$ | $0.866$ | $0.816$ |
| needle $(0,0), (1,0), (0,0.1)$ | $5.71°$ | $90°$ | $5.02$ | $10.05$ | $8.75$ | $0.189$ | $0.172$ | $0.115$ |
| flat $(-1,0), (1,0), (0,0.1)$ | $5.71°$ | $168.58°$ | $5.02$ | $1.99$ | $17.3$ | $0.020$ | $0.115$ | $0.115$ |

The needle and the flat triangle have the same smallest angle, so the minimum angle, the radius-edge ratio and the scaled Jacobian rank them equally. Only the flat one has a large angle, which is the one that spoils the gradient. The radius ratio and the aspect ratio rank the flat triangle much worse, the edge ratio ranks it better.

For tetrahedra, the regular one, the sliver $T_{0.01}$ of the [radius-edge ratio](/radius-edge-ratio/) page, and a cap of height $0.1$ over an equilateral triangle inscribed in the unit circle give:

| Shape | radius-edge | edge ratio | radius ratio | mean ratio | dihedral angles |
| --- | --- | --- | --- | --- | --- |
| regular | $0.612$ | $1$ | $1$ | $1$ | all $70.53°$ |
| sliver $T_{0.01}$ | $0.707$ | $1.414$ | $0.030$ | $0.088$ | $1.62°$ to $177.71°$ |
| cap | $5.02$ | $1.72$ | $0.029$ | $0.256$ | $11.31°$ to $160.44°$ |

The radius-edge ratio and the edge ratio rate the sliver almost as well as the regular tetrahedron. The radius ratio and the dihedral angles show that it is almost flat.

## Where it is used

- **Mesh generation.** [Delaunay refinement](/delaunay-refinement/) splits every triangle whose radius-edge ratio exceeds a bound $B$. In two dimensions this gives a proved lower bound on the smallest angle. In three dimensions it gives a proved radius-edge bound only, and slivers are removed afterwards by [sliver exudation](/sliver-exudation/) or by improvement steps.
- **Mesh improvement.** [Optimization-based mesh smoothing](/optimization-based-mesh-smoothing/) moves a vertex to maximize the worst quality of the elements around it, often the mean ratio or the scaled Jacobian. [Mesh untangling](/mesh-untangling/) first makes every element valid. [Laplacian smoothing](/laplacian-smoothing/) uses no measure and can make elements worse.
- **Methods with no guarantee.** For the [advancing front method](/advancing-front-mesh-generation/), [paving](/paving/) and most hexahedral meshers, the quality is only measured after the fact, by the minimum, the mean and a histogram of a chosen measure over the mesh.
- **Structured grids.** [Structured grid generation](/structured-grid-generation/) reports the minimum scaled Jacobian, the skew and the ratio of neighboring cell sizes. A non-positive Jacobian means that the grid has folded.
- **Sizing.** A [mesh sizing function](/mesh-sizing-function/) says how large an element should be, and the quality measures say how well shaped it is. They are separate requirements.

## References
