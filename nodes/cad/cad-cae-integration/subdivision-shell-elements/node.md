---
tag: VM8MHD
kind: model
slug: subdivision-shell-elements
name: Subdivision surface shell elements
aliases:
- Cirak-Ortiz-Schroder subdivision shells
area: cad/cad-cae-integration
level: research
summary: Cirak, Ortiz and Schroder's thin shell finite elements on Loop subdivision surfaces, which give the smooth basis bending needs without rotation unknowns.
prereqs: [loop-subdivision, subdivision-surface, fundamental-forms]
see_also: [isogeometric-kirchhoff-love-shell, catmull-clark-subdivision, isogeometric-analysis, finite-element-method, galerkin-method, surface-curvature, nurbs]
sources:
  - paper: doi:10.1002/(SICI)1097-0207(20000430)47:12<2039::AID-NME872>3.0.CO;2-1
    title: F. Cirak, M. Ortiz and P. Schröder, Subdivision surfaces, a new paradigm for thin-shell finite-element analysis, International Journal for Numerical Methods in Engineering 47(12), 2000, 2039 to 2072
    locator: the whole paper (the Loop basis as shape functions, the Kirchhoff-Love energy, the treatment of boundaries and the linear benchmark tests)
  - paper: doi:10.1002/nme.182
    title: F. Cirak and M. Ortiz, Fully C1-conforming subdivision elements for finite deformation thin-shell analysis, International Journal for Numerical Methods in Engineering 51(7), 2001, 813 to 833
    locator: the extension to large deformations
  - paper: doi:10.1023/A:1016685104156
    title: U. Reif and P. Schröder, Curvature integrability of subdivision surfaces, Advances in Computational Mathematics 14(2), 2001, 157 to 174
    locator: the result that the curvature of Loop and similar subdivision surfaces is square integrable near extraordinary vertices, so that the bending energy is finite
  - paper: doi:10.1016/j.cma.2009.08.013
    title: J. Kiendl, K.-U. Bletzinger, J. Linhard and R. Wüchner, Isogeometric shell analysis with Kirchhoff-Love elements, Computer Methods in Applied Mechanics and Engineering 198(49-52), 2009, 3902 to 3914
    locator: the same rotation-free model later built on NURBS patches
---

Subdivision shell elements, from Cirak, Ortiz and Schröder (2000), discretize a thin shell with the Kirchhoff-Love model and use the basis functions of [Loop subdivision](/loop-subdivision/) as shape functions. The control mesh is a triangle mesh of any topology. Its vertices carry the unknowns, three displacement components per vertex, and the limit surface of the mesh is the shell midsurface. The Loop limit surface is $C^2$ away from a finite set of vertices and tangent plane continuous at those vertices, and its curvature is square integrable. So the bending energy, which holds second derivatives, is finite for every displacement of the space, and no rotation unknowns are needed. This was the first rotation-free shell method with a smooth basis on a surface of arbitrary topology, nine years before the NURBS form of the [isogeometric Kirchhoff-Love shell](/isogeometric-kirchhoff-love-shell/). It is also one of the first uses of the CAD representation itself as the analysis basis, the idea that [isogeometric analysis](/isogeometric-analysis/) later made general.

## The machine

The "machine" of a shell model is its representation of the midsurface and the displacement, and its assumptions.

**The representation.** A triangle mesh with vertex positions $X_I$ is the control mesh. Loop subdivision refines it, and the limit of the refinement is a surface $X(\theta) = \sum_I N_I(\theta) X_I$, where $N_I$ is the limit function of vertex $I$: the limit surface of the mesh in which vertex $I$ has the value 1 and all other vertices 0. Each triangle of the control mesh is one element, with parameters $\theta = (\theta^1, \theta^2)$ on a reference triangle. The displacement uses the same functions, $u(\theta) = \sum_I N_I(\theta) u_I$.

- **A regular element.** If the three vertices of a triangle all have valence 6, the limit surface over it is a quartic box spline, a polynomial of degree 4 in $\theta$, and it depends on the 12 vertices of the 1-rings of the three corners. So 12 basis functions are non-zero on the element.
- **An irregular element.** If one corner has valence $N \ne 6$, the element depends on $N + 6$ vertices, and the surface over it is not one polynomial. It is a union of infinitely many polynomial pieces that shrink toward the extraordinary vertex. It is evaluated by repeated subdivision near the vertex, or in closed form with the eigenvectors of the subdivision matrix. The paper assumes at most one extraordinary corner per triangle, which one step of subdivision of the input mesh ensures.
- **Support.** $N_I$ is non-zero only on the triangles of the 2-ring of vertex $I$, 24 triangles when the vertices are regular.

The metric and the curvature of the midsurface, the strains and the energy are those of the Kirchhoff-Love model on the [isogeometric Kirchhoff-Love shell](/isogeometric-kirchhoff-love-shell/) page, with the Loop functions in place of NURBS.

**Assumptions.** The model takes these as given.

- **Kirchhoff-Love kinematics and a thin shell.** Normals stay normal and straight, so there is no transverse shear and the normal follows from the midsurface.
- **Linear elastic material** with small strains. The 2000 paper treats small displacements, and Cirak and Ortiz (2001) extend the method to finite deformations.
- **The shell midsurface is a Loop limit surface.** Geometry from CAD in NURBS form must first be converted to a triangle control mesh, which in general changes the geometry.
- **Boundaries.** Near a boundary the 2-ring of a vertex is not complete. The paper adds a layer of extra triangles outside the boundary, whose vertices are set from the boundary vertices. A clamped edge then fixes these extra vertices as well, which fixes the normal rotation.

## What it counts

The model counts the strain energy of the shell: the membrane energy of the change of the first fundamental form and the bending energy of the change of the second fundamental form, see [fundamental forms](/fundamental-forms/). The unknowns are the three displacement components of each control vertex, so $3 V$ unknowns for $V$ vertices, against five per node for a shell element with rotations. The element matrices are integrated with a Gauss rule on each triangle, and each entry couples two vertices whose 2-rings overlap, so the stiffness matrix is sparse with about 19 non-zero $3 \times 3$ blocks per row in a regular mesh (the vertices at most two edges away, $1 + 6 + 12$). The equations are a [Galerkin method](/galerkin-method/) for the shell.

## Relation to other models

- **[Isogeometric Kirchhoff-Love shell](/isogeometric-kirchhoff-love-shell/).** The same energy and the same rotation-free idea, on NURBS patches. NURBS give the exact CAD geometry, exact conics and trimming, but need patch coupling for $C^1$ across patches. Subdivision gives one smooth surface of any topology without patches, but no exact conics, no trimming, and a lower smoothness at extraordinary vertices.
- **[Catmull-Clark subdivision](/catmull-clark-subdivision/).** The same construction works with quadrilateral control meshes. The regular Catmull-Clark patch is a bicubic B-spline patch, so it connects directly to the spline basis of isogeometric analysis.
- **Classical shell elements.** $C^0$ elements with rotation unknowns (Reissner-Mindlin type) avoid the second derivatives at the cost of five unknowns per node and of shear locking for thin shells. $C^1$ triangles exist but need high degree.
- **[Subdivision surfaces](/subdivision-surface/) in geometry.** The analysis uses the limit surface, not the refined meshes. The refinement is only a way to evaluate the basis.

## Known results in the model

**The basis is smooth enough for bending.** On a regular element the limit surface is a quartic box spline, which is $C^2$. At an extraordinary vertex the Loop surface is tangent plane continuous. Reif and Schröder (2001) prove that its curvature is square integrable, so the limit functions $N_I$ have second derivatives in $L^2$. By the 1D lemma on the [isogeometric Kirchhoff-Love shell](/isogeometric-kirchhoff-love-shell/) page, a piecewise smooth function has square integrable second derivatives only if its gradient has no jumps, and the Loop basis meets this. So the bending energy is finite on the whole space and the method is conforming. This is a cited result, not proved here.

**Partition of unity and reproduction.** The Loop rules are affine combinations, so $\sum_I N_I = 1$, and a rigid translation of all vertices translates the limit surface. So rigid translations cost no energy, a basic test of a shell element.

**Local support and sparsity.** On a regular mesh each basis function has its support in the 24 triangles of the 2-ring, and each element has 12 non-zero basis functions, counted by the 1-rings of its three corners. These counts follow from the Loop rules, which use only the 1-ring of a vertex.

**Error.** The quartic box spline reproduces polynomials of degree 3 in the plane on regular meshes. For smooth solutions on regular meshes the error in the energy norm is then expected to decrease like $h^2$ (one order lower in $H^2$ than the degree 3 that is reproduced). Near extraordinary vertices the approximation is weaker. The paper reports convergence on standard linear benchmark tests of thin shells. These rates are measured in the literature and are not proved here.

**Large deformation.** Cirak and Ortiz (2001) use the same basis for finite deformations with the large displacement form of the same strains, again without rotation variables.

## References
