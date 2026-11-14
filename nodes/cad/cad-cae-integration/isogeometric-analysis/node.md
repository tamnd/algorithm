---
tag: DY74MN
kind: concept
slug: isogeometric-analysis
name: Isogeometric analysis
aliases:
- IGA
area: cad/cad-cae-integration
level: core
summary: Hughes, Cottrell and Bazilevs's analysis that uses the NURBS or spline basis of the CAD model as the finite element basis, so the geometry stays exact under refinement.
prereqs: [b-spline, nurbs, galerkin-method, finite-element-method]
see_also: [k-refinement, bezier-extraction, isogeometric-quadrature, nurbs-approximation-estimates, t-spline, truncated-hierarchical-b-spline, isogeometric-collocation, trimmed-isogeometric-analysis]
sources:
  - paper: doi:10.1016/j.cma.2004.10.008
    title: "T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis: CAD, finite elements, NURBS, exact geometry and mesh refinement, Computer Methods in Applied Mechanics and Engineering 194(39-41), 2005, 4135 to 4195"
    locator: the whole paper, the founding paper with the isoparametric use of NURBS, patches, h-, p- and k-refinement and the first numerical tests
  - book: isbn:9780470748732
    title: "J. Austin Cottrell, Thomas J. R. Hughes and Yuri Bazilevs, Isogeometric Analysis: Toward Integration of CAD and FEA, Wiley, 2009"
    locator: Chapters 1 to 3 (from CAD to analysis, NURBS as a basis, the analysis framework and refinement)
  - paper: doi:10.1142/S0218202506001455
    title: Y. Bazilevs, L. Beirão da Veiga, J. A. Cottrell, T. J. R. Hughes and G. Sangalli, Isogeometric analysis, approximation, stability and error estimates for h-refined meshes, Mathematical Models and Methods in Applied Sciences 16(7), 2006, 1031 to 1090
    locator: Section 3 (approximation estimates for NURBS spaces under h-refinement)
  - paper: doi:10.1016/j.cma.2005.09.027
    title: J. A. Cottrell, A. Reali, Y. Bazilevs and T. J. R. Hughes, Isogeometric analysis of structural vibrations, Computer Methods in Applied Mechanics and Engineering 195(41-43), 2006, 5257 to 5296
    locator: the comparison of the discrete spectra of smooth splines and C0 finite elements
  - paper: doi:10.1017/S096249291400004X
    title: L. Beirão da Veiga, A. Buffa, G. Sangalli and R. Vázquez, Mathematical analysis of variational isogeometric methods, Acta Numerica 23, 2014, 157 to 287
    locator: the survey of the theory, spline spaces, local refinement and stability
---

Isogeometric analysis is the [finite element method](/finite-element-method/) run on the basis that a CAD system already uses to describe the shape. Hughes, Cottrell and Bazilevs proposed it in 2005. The geometry is a [NURBS](/nurbs/) or other spline map from a parameter domain, and the unknown field is written in the same basis. So the mesh is the CAD model itself, and refinement never changes the shape. This page gives the overall idea and points to the pages that treat each part.

## In plain words

In ordinary simulation an engineer takes the smooth shape from the design program and replaces it with many small flat or slightly curved pieces, the mesh. This step is slow, it needs a person for hard parts, and the mesh is only close to the true shape.

Isogeometric analysis skips that step. The design program already writes the shape as a sum of smooth bump functions times control points. The simulation uses the same bump functions to write the temperature, the displacement or any other unknown. To get a more accurate answer it cuts the bumps into smaller ones, or makes them of higher degree, in a way that leaves the shape exactly as it was. The smooth bumps also give smooth answers, which helps for thin shells and for vibration problems.

## The idea

**One basis for shape and field.** A patch is a map from the parameter box $\hat\Omega = (0, 1)^d$ to the physical domain,

$$x(\xi) = \sum_{i} R_i(\xi)\, P_i, \qquad R_i = \frac{w_i B_i}{\sum_j w_j B_j},$$

where the $B_i$ are tensor product [B-splines](/b-spline/) on [knot vectors](/knot-vector/), the $w_i > 0$ are weights and the $P_i$ are [control points](/control-points/). The discrete field is

$$u_h(x(\xi)) = \sum_i R_i(\xi)\, u_i .$$

This is the isoparametric idea of classical finite elements turned around. There, the geometry is fitted to the basis of the field. Here, the field is fitted to the basis of the geometry. The coefficients $u_i$ are values at control points, not at nodes, and in general $u_h$ does not interpolate them.

**Elements are knot spans.** The nonempty boxes between distinct knots are the elements. Each basis function is supported on a few neighbouring elements, $(p+1)^d$ of them for a basis of degree $p$ with simple knots, and on each element only $(p+1)^d$ functions are nonzero. The basis is a [partition of unity](/partition-of-unity/) and nonnegative, as in finite elements.

**Galerkin or collocation.** The weak form is discretised by the [Galerkin method](/galerkin-method/): find $u_h$ in the span of the $R_i \circ x^{-1}$ that satisfies the weak equation for every test function in that span. The integrals are computed element by element after a change of variables to the parameter domain, which needs a quadrature fitted to splines, see [isogeometric quadrature](/isogeometric-quadrature/). [Isogeometric collocation](/isogeometric-collocation/) instead enforces the strong equation at chosen points, which uses the smoothness of the basis.

**Refinement keeps the geometry.** Three kinds of refinement enrich the space and keep the map $x$ the same function:

- *h-refinement* inserts knots, by [Boehm knot insertion](/boehm-knot-insertion/) or the [Oslo algorithm](/oslo-algorithm/).
- *p-refinement* raises the degree and keeps the smoothness at the old knots.
- *k-refinement* raises the degree first and then inserts knots, so the new knots get maximal smoothness. It is described on [k-refinement](/k-refinement/).

All three work because the old space is a subspace of the new one, so the old geometry has an exact representation in the new basis. The geometry is fixed on the coarsest mesh, and refinement only changes the space for the field.

**Rates.** Under h-refinement with the degree fixed, NURBS spaces of degree $p$ approximate as well as finite elements of degree $p$: an $H^k$ error of order $h^{p+1-k}$ for smooth functions. The exact statement, with its geometry dependent constant, is on [NURBS approximation estimates](/nurbs-approximation-estimates/).

**Link to finite element codes.** [Bezier extraction](/bezier-extraction/) writes the spline basis on each element as a fixed matrix times the [Bernstein polynomials](/bernstein-polynomials/). With it, an existing finite element code can run isogeometric analysis with only an element-wise matrix as new data.

**Local refinement.** A tensor product mesh refines whole knot lines across the patch. For adaptivity several spline spaces allow local refinement:

- [T-splines](/t-spline/), restricted to [analysis-suitable T-splines](/analysis-suitable-t-spline/) so that the basis is [linearly independent](/t-spline-linear-independence/), with a [local refinement algorithm](/t-spline-local-refinement/).
- [Hierarchical B-splines](/hierarchical-b-spline/) and their [truncated form](/truncated-hierarchical-b-spline/).
- [LR B-splines](/lr-b-spline/).
- [PHT-splines](/pht-spline/), which are $C^1$ cubic splines on a hierarchical T-mesh.

**Geometry that is not a set of patches.** CAD solids are often trimmed surfaces and not volumes. That leads to [trimmed isogeometric analysis](/trimmed-isogeometric-analysis/), to immersed methods such as [immersogeometric analysis](/immersogeometric-analysis/), to [volumetric spline parameterization](/volumetric-spline-parameterization/) of the interior, and to the [isogeometric boundary element method](/isogeometric-boundary-element-method/), which needs only the boundary.

## Examples

**The geometry is exact on the coarsest mesh.** The quarter of the unit circle is a quadratic NURBS curve with knots $0, 0, 0, 1, 1, 1$, control points $(1, 0)$, $(1, 1)$, $(0, 1)$ and weights $1$, $\tfrac{\sqrt2}{2}$, $1$. With one element, this curve is the exact arc. Inserting the knot $\tfrac12$ gives four control points and two elements, and the curve is still the same arc. A finite element mesh of the arc with quadratic Lagrange elements only interpolates it at the nodes, and its geometric error goes to zero with refinement but is never zero.

**A Poisson problem solved exactly.** Solve $-u'' = 1$ on $(0, 1)$ with $u(0) = u(1) = 0$. Take the map $x = \xi$ (control points at the Greville abscissae $0, \tfrac14, \tfrac34, 1$) and quadratic B-splines on $0, 0, 0, \tfrac12, 1, 1, 1$, four functions on two elements. The two boundary coefficients are zero, so there are two unknowns. The exact solution $u(x) = \tfrac12 x (1 - x)$ is a quadratic polynomial, so it lies in the space, and the Galerkin solution, the best approximation in the energy norm, equals it. Its coefficients are $0, \tfrac18, \tfrac18, 0$. At $x = \tfrac12$ both middle functions equal $\tfrac12$, so $u_h(\tfrac12) = \tfrac18$, the exact value. With the same two unknowns, $C^0$ linear elements on three elements get the nodal values right but not the values between nodes.

**Smoothness and the count of unknowns.** In one dimension, $C^{p-1}$ splines of degree $p$ on $n$ elements have $n + p$ functions, and $C^0$ elements of degree $p$ have $p n + 1$. For $p = 3$ and $n = 100$ that is $103$ against $301$. The count in general, and what it costs to get it, is on [k-refinement](/k-refinement/).

**Vibrations.** Cottrell, Reali, Bazilevs and Hughes (2006) showed that the discrete frequencies of a vibrating rod with smooth splines stay close to the exact ones over most of the spectrum. With $C^0$ elements of higher degree the upper part of the spectrum splits into optical branches with large errors. This is a measured and analysed property of the uniform one-dimensional case.

## Where it is used

- Thin shells, where the Kirchhoff-Love theory needs $C^1$ functions that classical elements do not give, see [isogeometric Kirchhoff-Love shells](/isogeometric-kirchhoff-love-shell/).
- Structural vibration and wave problems, for the spectral behaviour above.
- Contact, where the smooth surface gives smooth normals.
- Fluid and fluid-structure interaction, including heart valves with the immersed form of the method.
- [Shape optimization](/isogeometric-shape-optimization/), where the design variables are the control points of the CAD model.
- Phase field and other higher order equations, such as Cahn-Hilliard, which need $H^2$ conforming spaces.

## References
