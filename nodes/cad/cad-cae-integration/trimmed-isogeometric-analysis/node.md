---
tag: TD2T9P
kind: technique
slug: trimmed-isogeometric-analysis
name: Trimmed isogeometric analysis
aliases:
- analysis of trimmed CAD models
area: cad/cad-cae-integration
level: research
summary: Analyses trimmed NURBS models directly by integrating over cut elements, stabilising small cuts and imposing conditions weakly, as Marussig and Hughes reviewed.
prereqs: [isogeometric-analysis, trimmed-surface, nurbs]
see_also: [finite-cell-method, immersogeometric-analysis, cut-finite-element-method, isogeometric-boundary-element-method, isogeometric-kirchhoff-love-shell, isogeometric-quadrature, condition-number, adaptive-quadrature]
sources:
  - paper: doi:10.1007/s11831-017-9220-9
    title: B. Marussig and T. J. R. Hughes, A review of trimming in isogeometric analysis, challenges, data exchange and simulation aspects, Archives of Computational Methods in Engineering 25(4), 2018, 1059 to 1127
    locator: the whole review (trimming in CAD and its data exchange, the classification of the analysis approaches, integration of cut elements, weak boundary conditions, stability and coupling)
  - paper: doi:10.1016/j.cma.2009.05.004
    title: H.-J. Kim, Y.-D. Seo and S.-K. Youn, Isogeometric analysis for trimmed CAD surfaces, Computer Methods in Applied Mechanics and Engineering 198(37-40), 2009, 2982 to 2995
    locator: the integration of trimmed elements by subdivision in the parameter domain and the planar test problems
  - paper: doi:10.1016/j.cma.2012.05.021
    title: R. Schmidt, R. Wüchner and K.-U. Bletzinger, Isogeometric analysis of trimmed NURBS geometries, Computer Methods in Applied Mechanics and Engineering 241-244, 2012, 93 to 111
    locator: trimmed shells and membranes, with the integration of trimmed elements and the treatment of trimmed boundaries
  - paper: doi:10.1016/j.cma.2013.10.009
    title: M. Ruess, D. Schillinger, A. I. Özcan and E. Rank, Weak coupling for isogeometric analysis of non-matching and trimmed multi-patch geometries, Computer Methods in Applied Mechanics and Engineering 269, 2014, 46 to 71
    locator: Nitsche coupling of trimmed patches and the choice of the stabilization parameter
  - paper: doi:10.1007/BF02995904
    title: J. Nitsche, Über ein Variationsprinzip zur Lösung von Dirichlet-Problemen bei Verwendung von Teilräumen, die keinen Randbedingungen unterworfen sind, Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg 36, 1971, 9 to 15
    locator: the weak imposition of Dirichlet conditions that is now called Nitsche's method
  - paper: doi:10.1137/S0036142900373208
    title: K. Höllig, U. Reif and J. Wipper, Weighted extended B-spline approximation of Dirichlet problems, SIAM Journal on Numerical Analysis 39(2), 2001, 442 to 462
    locator: extended B-splines, which tie the B-splines with small support in the domain to inner ones and so remove the small cut problem
---

Trimmed isogeometric analysis computes directly on a [trimmed](/trimmed-surface/) CAD model. In a CAD system, almost every surface is a tensor product [NURBS](/nurbs/) patch on a parameter rectangle, together with trimming curves in that rectangle that cut away the parts that are not used. Boolean operations, fillets and holes all make trims, so the visible face is almost never the full patch. Standard [isogeometric analysis](/isogeometric-analysis/) needs the full patch, with its boundary on the knot lines. Trimmed analysis keeps the full patch and its basis, and restricts the computation to the trimmed region: it integrates over the cut elements, removes the functions that do not reach the region, imposes the boundary conditions of the trimmed edges weakly, stabilizes elements that are cut very small, and couples patches whose trimmed edges do not match. Marussig and Hughes (2018) review the field. The trimming curves come from the CAD model and the mesh is the patch's own knot mesh, so this is not an immersed method with a separate background mesh: it is about trimmed patches. The [finite cell method](/finite-cell-method/), [immersogeometric analysis](/immersogeometric-analysis/) and [CutFEM](/cut-finite-element-method/) cut a background mesh with a boundary instead, and use the same tools for the cut elements.

## In plain words

A CAD face is a smooth sheet with holes and edges cut out by curves, like a sheet of dough with shapes cut out. The sheet itself is simple, a stretched rectangle, but the cut shape is not.

You could build a new mesh that follows the cuts, but that is slow and loses the exact shape. Instead, trimmed analysis keeps the simple sheet and its grid, and only throws away what is outside the cut. Grid cells fully inside are used as they are. Cells fully outside are dropped. Cells crossed by a cut are used only on their inside part, which needs a careful sum over a curved piece. Conditions at the cut edges cannot be built into the basis, so they are added to the equations as extra terms. Cells cut into tiny slivers make the equations hard to solve, so they need special care.

## When it applies

- The geometry is a trimmed NURBS model from CAD: each face is a patch $S : [0, 1]^2 \to \mathbb{R}^3$ (or a volume patch) plus closed trimming curves in the parameter square that bound the active region $\hat\Omega$.
- The analysis uses the patch basis, as in isogeometric analysis, for shells (see the [isogeometric Kirchhoff-Love shell](/isogeometric-kirchhoff-love-shell/)), membranes, planar problems, or the faces of a boundary method (see the [isogeometric boundary element method](/isogeometric-boundary-element-method/)).
- The problem is posed in weak form, so that integrals over the trimmed region and its boundary can stand in for a fitted mesh.
- For solids, a volume parameterization is also needed. A trimmed boundary representation alone does not give one, which is why boundary methods and immersed methods are the usual partners for solids.

## The template

```pseudo id=main
TRIMMED-IGA(patch S with basis {R_j}, trimming curves c_k, weak form)
L1  classify each knot element of the parameter square as inside, outside or cut by the curves c_k
L2  keep the functions R_j whose support meets the active region; drop the rest
L3  for each inside element: use the standard Gauss rule
L4  for each cut element: build a rule on its active part (subdivide with curved edges, or a quadtree, or moment fitting)
L5  impose the conditions on trimmed edges weakly (Nitsche or penalty terms on the curves c_k)
L6  stabilize the functions with a small active support (extension, merging, scaling or a ghost penalty)
L7  couple non-matching patches weakly along their trimmed edges
L8  assemble and solve the global system
```

**Step L1, classification.** The trimming curves are in the parameter square, so the test is 2D even for a surface in 3D. An element is cut when a curve crosses it. Curves that pass through a corner or run along a knot line need a tolerance.

**Step L4, integration on a cut element.** The active part of a cut element is bounded by knot lines and pieces of the trimming curves. The common choices are:

- **Subdivision with curved edges.** Split the active part into triangles or quadrilaterals, each with at most one curved edge on the trimming curve, map each by a blending of its edges, and apply a Gauss rule in each piece. With the exact trimming curve the region is exact, and the rule converges as for a smooth map. Kim, Seo and Youn (2009) and Schmidt, Wüchner and Bletzinger (2012) use forms of this.
- **Quadtree.** Bisect the cut element recursively and use Gauss rules on the leaves inside, as in [adaptive quadrature](/adaptive-quadrature/). It is robust but converges only to first order in the leaf size near the curve.
- **Boundary integrals.** By the divergence theorem, $\int_A x^a y^b \, dA$ over the active part $A$ is a line integral over its boundary, for example $\int_A 1 \, dA = \frac12 \oint_{\partial A} (x \, dy - y \, dx)$. A polynomial integrand on an element turns into 1D integrals along the trimming curve.

The integrand of the stiffness matrix is a polynomial times rational factors of the geometry map, so all three are approximate, and the [isogeometric quadrature](/isogeometric-quadrature/) rules for full elements do not apply directly.

**Step L5, weak conditions.** A trimmed edge does not lie on a knot line, so no set of control values gives prescribed boundary values. Nitsche's method (1971), defined here for the model problem $-\Delta u = f$ in $\Omega$, $u = g$ on the trimmed part $\Gamma_D$, finds $u_h$ in the untrimmed space with, for all test functions $v_h$,

$$ \int_\Omega \nabla u_h \cdot \nabla v_h - \int_{\Gamma_D} (\partial_n u_h) v_h - \int_{\Gamma_D} (\partial_n v_h)(u_h - g) + \frac{\beta}{h} \int_{\Gamma_D} (u_h - g) v_h = \int_\Omega f v_h. $$

The second term comes from integration by parts. The third term keeps the form symmetric and vanishes for the exact solution, and the last term, with a parameter $\beta > 0$, gives stability. The exact solution satisfies the equation, so the method is consistent. It is stable if $\beta$ is larger than a constant times the ratio $\|\partial_n v_h\|^2_{L^2(\Gamma_D)} h / \|\nabla v_h\|^2_{L^2(\Omega)}$ over the discrete space. On a cut element this ratio grows when the active part shrinks, which is one face of the small cut problem.

**Step L6, small cuts.** See Classic examples for why they matter. The remedies are: drop functions whose active support is below a threshold; tie them to nearby inner functions, as the extended B-splines of Höllig, Reif and Wipper (2001) do; scale the system by its diagonal; or add a ghost penalty as in [CutFEM](/cut-finite-element-method/).

**Step L7, coupling.** The trimmed edges of two faces of a CAD solid meet in space but not in the parameter domains, and their meshes do not match. Ruess, Schillinger, Özcan and Rank (2014) couple such patches with Nitsche terms on the interface curve. Mortar methods and penalties are the other choices.

## Classic examples

**A plate with a hole.** A square patch trimmed by a circle is the standard test: the stress of an infinite plate with a circular hole under tension has a closed form, and its restriction to a quarter plate gives exact boundary data. The trimmed patch keeps the rectangle's simple basis, and only the elements cut by the circle need special rules.

**Why small cuts break the system.** Take uniform B-splines of degree $p$ and element size $h$, and let the domain end at a point that cuts the element $[\xi, \xi + h]$ at the fraction $\epsilon \in (0, 1)$. One basis function $N$ has its support start at $\xi$, so only the piece $[\xi, \xi + \epsilon h]$ of its support is active. On that piece, $N(x) = ((x - \xi)/h)^p / p!$, the first piece of the uniform B-spline. So its diagonal entries of the mass and the stiffness matrix are

$$ \int_\xi^{\xi + \epsilon h} N^2 \, dx = \frac{h \, \epsilon^{2p+1}}{(p!)^2 (2p+1)}, \qquad \int_\xi^{\xi + \epsilon h} (N')^2 \, dx = \frac{\epsilon^{2p-1}}{h \, ((p-1)!)^2 (2p-1)}. $$

For $p = 2$, $h = 0.1$ and $\epsilon = 0.01$ these are $5 \times 10^{-13}$ and $3.3 \times 10^{-6}$, while the entries of an uncut function are of order $h$ and $1/h$. The [condition number](/condition-number/) of a symmetric positive definite matrix is at least the ratio of its largest to its smallest diagonal entry, so it grows at least like $\epsilon^{-(2p+1)}$ for the mass matrix and $\epsilon^{-(2p-1)}$ for the stiffness matrix as the cut moves. The cut position is fixed by the CAD model and cannot be chosen, so such cuts occur in practice. The formulas were checked against Gauss integration of the B-spline for $\epsilon = 0.5$, $0.1$ and $0.01$.

**Trimmed shells.** Schmidt, Wüchner and Bletzinger (2012) analyze trimmed NURBS shells and membranes with the patch basis, which together with the rotation-free shell lets a CAD surface model go to analysis without a mesh.

## Variations

- **Reconstruction instead of trimming.** Rebuild each trimmed face as untrimmed patches, or as a [T-spline](/t-spline/) without trims, and use standard isogeometric analysis. This changes the geometry slightly and is hard to do automatically.
- **Local reparameterization.** Replace each cut element by a new patch fitted to the trimming curve, so that standard quadrature applies on it.
- **Immersed methods for solids.** Use the trimmed boundary only for the geometry and an untrimmed volume background mesh for the analysis, as in the [finite cell method](/finite-cell-method/) and [immersogeometric analysis](/immersogeometric-analysis/).
- **Boundary methods.** Use only the trimmed surfaces, as in the [isogeometric boundary element method](/isogeometric-boundary-element-method/).

## Pitfalls

- **Small cuts.** The example shows a condition number that grows like $\epsilon^{-(2p-1)}$ or worse. Stabilize, or the solver fails for some CAD models and not for others.
- **The Nitsche parameter.** A fixed $\beta$ can be too small on a small cut element, and then the form is not coercive. Compute $\beta$ per element from a local eigenvalue problem, or stabilize the cut elements first.
- **Gaps and overlaps.** CAD trimming curves are approximations within a tolerance. Two faces meet only up to that tolerance, and a trimming curve in the parameter domain and its image curve in space do not agree exactly. Coupling and integration must allow small gaps.
- **Quadrature cost.** Cut elements need many more points than inside elements, and the subdivision of a cut element is the most fragile code of the method.
- **Degenerate parameterizations.** A trimmed region can include a point where the patch map is singular, such as the pole of a sphere patch, if the untrimmed patch has one. Check the Jacobian over the active region.

## Exercises

1. A unit square element is trimmed so that the quarter disk of radius $\tfrac12$ at the origin is removed. Compute the active area with the boundary formula $\frac12 \oint (x \, dy - y \, dx)$. *Answer:* $1 - \pi/16 \approx 0.8037$.
2. Prove the formula $\int_\xi^{\xi + \epsilon h} N^2 \, dx = h \epsilon^{2p+1} / ((p!)^2 (2p+1))$ from $N(x) = ((x - \xi)/h)^p / p!$.
3. Show that the Nitsche form above is symmetric and that the exact solution satisfies it for every test function.
4. Explain why a cut element whose active part is large does not need stabilization, and give a threshold on $\epsilon$ at which the diagonal entry of the stiffness matrix for $p = 2$ falls below $10^{-3}$ of an uncut one. *Hint:* an uncut quadratic B-spline has the diagonal entry $\int (N')^2 = 1/h$; solve $\epsilon^3 / 3 \approx 10^{-3}$, about $\epsilon \approx 0.14$.
5. Why is trimmed analysis of a CAD solid not enough to build a volume basis, and which two other methods avoid the volume parameterization?

## References
