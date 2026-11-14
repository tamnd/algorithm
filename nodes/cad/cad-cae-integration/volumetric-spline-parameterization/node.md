---
tag: Z78FFY
kind: problem
slug: volumetric-spline-parameterization
name: Volumetric spline parameterization
aliases:
- analysis-suitable volume parameterization
- trivariate spline construction
area: cad/cad-cae-integration
level: research
summary: Build a trivariate spline map of a solid from its boundary with a positive Jacobian and good quality, the main gap between B-rep CAD and isogeometric analysis.
prereqs: [isogeometric-analysis, b-spline, bernstein-polynomials]
see_also: [scaled-jacobian, hexahedral-mesh-generation, coons-patch, de-casteljau-algorithm, high-order-mesh-generation, t-spline, isogeometric-boundary-element-method, finite-cell-method]
sources:
  - paper: doi:10.1016/j.cma.2009.09.010
    title: E. Cohen, T. Martin, R. M. Kirby, T. Lyche and R. F. Riesenfeld, Analysis-aware modeling, understanding quality considerations in modeling for isogeometric analysis, Computer Methods in Applied Mechanics and Engineering 199(5-8), 2010, 334 to 356
    locator: the whole paper (how the parameterization of a domain affects the analysis, and the quality criteria for a volume model)
  - paper: doi:10.1016/j.cma.2011.03.005
    title: G. Xu, B. Mourrain, R. Duvigneau and A. Galligo, Parameterization of computational domain in isogeometric analysis, methods and comparison, Computer Methods in Applied Mechanics and Engineering 200(23-24), 2011, 2021 to 2031
    locator: the whole paper, the sufficient condition of injectivity by positive Bernstein coefficients of the Jacobian and the comparison of construction methods
  - paper: doi:10.1016/j.cagd.2008.09.008
    title: T. Martin, E. Cohen and R. M. Kirby, Volumetric parameterization and trivariate B-spline fitting using harmonic functions, Computer Aided Geometric Design 26(6), 2009, 648 to 664
    locator: the whole paper, a volume parameterization of a genus zero solid by harmonic functions and its fit by a trivariate B-spline
  - paper: doi:10.1016/j.jcp.2012.08.051
    title: A. Johnen, J.-F. Remacle and C. Geuzaine, Geometrical validity of curvilinear finite elements, Journal of Computational Physics 233, 2013, 359 to 372
    locator: the whole paper, the Bernstein form of the Jacobian determinant of a curved element and its adaptive subdivision to prove or disprove validity
  - paper: doi:10.1016/j.cma.2004.10.008
    title: T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis, CAD, finite elements, NURBS, exact geometry and mesh refinement, Computer Methods in Applied Mechanics and Engineering 194(39-41), 2005, 4135 to 4195
    locator: the isogeometric idea, which needs a spline map of the whole domain and not only of its boundary
---

Volumetric spline parameterization is the problem of turning the boundary of a solid, as a CAD system stores it, into a spline map of the whole solid that [isogeometric analysis](/isogeometric-analysis/) can use. A CAD model is a boundary representation: a set of trimmed surfaces that enclose the solid. Isogeometric analysis of a solid needs more, a map $x : [0, 1]^3 \to \Omega$, or several such patches, whose basis is also the analysis basis. The map must be one to one, which in practice means a positive Jacobian determinant, and of good quality, because the shape of the map enters the error and the conditioning of the analysis. This step has no general solution and is the main gap between CAD and isogeometric analysis of solids. Boundary methods, such as the [isogeometric boundary element method](/isogeometric-boundary-element-method/), and immersed methods, such as the [finite cell method](/finite-cell-method/), avoid it.

## In plain words

A CAD system describes a solid by its skin: a set of smooth curved sheets that fit together. To compute stresses inside the solid with the same smooth functions, you need more than the skin. You need a way to fill the inside, a stretched and bent block of rubber that fills the solid exactly, with every point of the block going to exactly one point of the solid.

The map must not fold over itself anywhere, or the computation fails. It should also not squeeze some regions much more than others, or the results get worse. Most solids are too complex for a single block, so they must be cut into several blocks that fit together. Finding such a filling is easy for simple shapes and still an open problem for general ones.

## Definition

**Input.** A closed boundary representation of a solid $\Omega \subset \mathbb{R}^3$: spline surfaces, possibly trimmed, that enclose $\Omega$. In 2D the input is a closed spline curve that bounds a planar domain.

**Output.** A spline map $x(\xi) = \sum_i N_i(\xi) P_i$ from $\hat\Omega = [0, 1]^3$ (or several patches $x_k : [0, 1]^3 \to \Omega_k$ with $\bigcup_k \Omega_k = \Omega$) with:

1. **Boundary match.** The faces of the parameter cube map onto the given boundary surfaces, exactly or within a tolerance.
2. **Validity.** $x$ is a bijection from $\hat\Omega$ onto $\Omega$, and $\det J(\xi) > 0$ everywhere, with $J = \partial x / \partial \xi$.
3. **Conformity** for several patches: neighboring patches share their faces, with matching control points or with a weak coupling.
4. **Quality.** A measure such as the smallest [scaled Jacobian](/scaled-jacobian/), $\min \det J / (|x_{\xi_1}| \, |x_{\xi_2}| \, |x_{\xi_3}|)$, or a distortion energy, is as good as possible.

*Analysis-suitable* means that the result can go to analysis unchanged: valid, of acceptable quality, and, for T-spline volumes, with a basis that is linearly independent.

**The Jacobian of a spline map.** For a tensor product B-spline map of degrees $(p, q, r)$, each column of $J$ has degree one less in one direction, so on each element $\det J$ is a polynomial of degree $(3p - 1, 3q - 1, 3r - 1)$. In 2D it has degree $(2p - 1, 2q - 1)$. For a NURBS map, $\det J$ is a polynomial divided by a positive power of the weight function, so its sign is that of a polynomial. Within an element, this polynomial can be written in the tensor product [Bernstein basis](/bernstein-polynomials/) of its degree, with coefficients $c_\beta$.

**Theorem (a sufficient condition).** If all Bernstein coefficients of $\det J$ on an element are positive, then $\det J \ge \min_\beta c_\beta > 0$ on that element.

*Proof.* The tensor product Bernstein polynomials $B_\beta$ of the element are non-negative and sum to 1. So $\det J = \sum_\beta c_\beta B_\beta \ge (\min_\beta c_\beta) \sum_\beta B_\beta = \min_\beta c_\beta$. $\square$

The value of $\det J$ lies in the convex hull of its coefficients, and the corner coefficients equal the values at the corners of the element. So a negative corner coefficient proves that the map is invalid. A positive $\det J$ alone shows that the map is locally one to one. Together with a one to one map of the boundary of a domain that is topologically a ball, it gives a bijection, by a classical result of topology that this page does not prove.

**The condition is not necessary.** See the second example below: a valid map whose Jacobian has negative Bernstein coefficients.

## Variants

- **Planar parameterization.** The 2D form: a bivariate map of a planar domain from its boundary curves. It is the test bed for most methods.
- **Single patch or multi-patch.** One map from a cube, or a decomposition into many patches, which must agree on shared faces.
- **Fixed or free boundary.** The boundary control points may be fixed to the CAD data, or they may be refit to the boundary within a tolerance.
- **The basis.** Tensor product B-splines and NURBS, volume [T-splines](/t-spline/), or hierarchical splines with local refinement.
- **Trimmed input.** The boundary surfaces are trimmed CAD faces, so the faces of the cube must first be mapped onto untrimmed boundary pieces.

## Examples

**A quarter annulus, exact.** The region between the circles of radius $1$ and $2$ in the first quadrant is the exact NURBS map of degree $(2, 1)$ that joins the quarter circle of radius 1 to the one of radius 2 by straight lines. Its Jacobian is positive, and its scaled Jacobian is 1, because the lines of the map are radii and circles.

**A valid map with negative Bernstein coefficients.** Let $g(u)$ be the quadratic Bézier function with the coefficients $(1, -0.8, 1)$, so $g(u) = 1 - 3.6 u + 3.6 u^2$, whose minimum is $g(\tfrac12) = 0.1 > 0$. Define the map of degree $(2, 1)$

$$ x(u, v) = \bigl(u, \; v \, g(u)\bigr), \qquad (u, v) \in [0, 1]^2, $$

with the control points $(0, 0)$, $(\tfrac12, 0)$, $(1, 0)$ on the bottom row and $(0, 1)$, $(\tfrac12, -0.8)$, $(1, 1)$ on the top row. It is the ruled surface between the bottom edge and the curve $y = g(x)$, that is a [Coons patch](/coons-patch/) of the domain $\{0 \le x \le 1, \ 0 \le y \le g(x)\}$. Then $J = \begin{pmatrix} 1 & 0 \\ v g'(u) & g(u) \end{pmatrix}$ and $\det J = g(u) \ge 0.1$, and the map is clearly a bijection onto the domain. The middle top control point lies below the bottom edge, so the control net is folded, and in the Bernstein basis of degree $(3, 1)$ the coefficients of $\det J$ in $u$ are $(1, -0.2, -0.2, 1)$ for both values of the $v$ index. Two are negative, but the map is valid. So positive coefficients are sufficient and not necessary.

**Subdivision closes the gap.** Split the element at $u = \tfrac12$ with the [de Casteljau algorithm](/de-casteljau-algorithm/). The coefficients become $(1, 0.4, 0.1, 0.1)$ on the left half and $(0.1, 0.1, 0.4, 1)$ on the right half. All are positive, so the test now proves validity, and the bound $\min c_\beta = 0.1$ equals the true minimum. Since the Bernstein coefficients converge to the values of the function as the elements shrink, a strictly positive $\det J$ always passes the test after enough subdivisions. Johnen, Remacle and Geuzaine (2013) use this adaptive scheme to certify curved finite elements.

**A reflex corner cannot be a patch corner.** At a corner of the parameter square, $x_u$ and $x_v$ are the tangents of the two boundary curves that meet there, fixed by the boundary data. If the inner angle of the domain at that point is $\theta$, then $\det J = |x_u| \, |x_v| \sin \theta$. For a reflex corner, $\pi < \theta < 2\pi$, this is negative, whatever the inner control points are. So no single patch map of an L-shaped domain can put the reflex corner at a corner of the square. It must lie inside an edge of the square, at a knot of multiplicity $p$ so that the boundary can have a kink there.

## Known algorithms

- **Transfinite interpolation.** A Coons patch, or its 3D form, interpolates the boundary linearly into the interior. It is cheap and works for nearly convex domains, but it folds for strongly non-convex ones.
- **Harmonic maps.** Solve Laplace equations for the map or its inverse with the boundary as data. In 2D, by the theorem of Radó, Kneser and Choquet, a harmonic map from the disk onto a convex domain with a one to one boundary map is a diffeomorphism. Martin, Cohen and Kirby (2009) build volume maps of genus zero solids from harmonic functions and fit trivariate B-splines to them. A spline fit can lose the validity that the exact harmonic map has.
- **Optimization.** Choose the inner control points to minimize a distortion energy, such as the Winslow or a Liao functional, or to maximize the smallest $\det J$, with the positivity of the Bernstein coefficients as constraints. Xu, Mourrain, Duvigneau and Galligo (2011) compare such methods.
- **Decomposition into patches.** Cut the solid into simple pieces, by sweeps, polycubes or a coarse [hexahedral mesh](/hexahedral-mesh-generation/), and fit a patch or a T-spline volume to each piece.
- **Validity certification.** Bernstein coefficients of $\det J$ with adaptive subdivision, as in the examples, together with a lower bound on the scaled Jacobian from the same coefficients.

## Bounds

- **Topology.** A single patch map from the cube that is a bijection exists only if $\Omega$ is topologically a ball. A solid with a hole, such as a torus, needs several patches or a periodic parameter domain.
- **Corners.** As the example proves, every corner of a patch must sit at a boundary point with inner angle below $\pi$. In 3D the same argument applies to the corners and the edges of the cube. This rules out many placements of the patch corners before any optimization.
- **No general guarantee.** No known method builds a valid volumetric spline map for every boundary representation of a ball-shaped solid, with given degrees and a given number of control points. With a fixed boundary and a fixed basis, a valid choice of the inner control points may not exist. Then only refinement or a different patch layout helps.
- **Cost of certification.** The Bernstein form of $\det J$ of a $(p, q, r)$ element has $3p \cdot 3q \cdot 3r = 27 pqr$ coefficients. They follow from the coefficients of the map by products of Bernstein forms, at a cost polynomial in $p$, $q$ and $r$ per element in the [real RAM](/real-ram/) model. The number of subdivisions that a positive $\det J$ needs grows as its minimum approaches zero.

## Reductions

- **To hexahedral meshing.** The Bézier elements of a multi-patch spline volume form a hexahedral mesh of the solid, and a hexahedral mesh gives a multi-patch trilinear volume. So finding a multi-patch layout is as hard as [hexahedral mesh generation](/hexahedral-mesh-generation/), which is open in general.
- **To polynomial positivity.** Checking validity reduces to deciding $\det J > 0$ on a box, which the Bernstein test with subdivision decides for strictly positive or strictly negative minima.
- **To quality measures.** The quality goals are those of [high-order mesh generation](/high-order-mesh-generation/) and of the [mesh quality measures](/mesh-quality-measures/), applied to one large curved element per patch.

## Applications

- Isogeometric analysis of solids: stress analysis of mechanical parts, heat flow, and fluid flow in ducts and around bodies where the fluid domain is the volume.
- Shape optimization with spline volumes, where the volume map must stay valid as the boundary moves; see [isogeometric shape optimization](/isogeometric-shape-optimization/).
- Volumetric models for manufacturing with graded materials, where the material is defined in the parameter domain.
- Curved high-order meshes: a valid volume map gives a curved hexahedral mesh for standard finite element codes.

## References
