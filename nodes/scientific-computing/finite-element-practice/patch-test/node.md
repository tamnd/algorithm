---
tag: SGRJZ0
kind: technique
slug: patch-test
name: Patch test
area: scientific-computing/finite-element-practice
level: core
summary: Checks that a small patch of distorted elements reproduces a linear exact solution to rounding error. It finds consistency errors in elements and codes, but passing it does not prove convergence.
prereqs: [finite-element-method, lagrange-finite-element, isoparametric-mapping]
see_also: [finite-element-assembly, gaussian-quadrature, cea-lemma, mixed-finite-element-method, virtual-element-method, element-free-galerkin-method, extended-finite-element-method, lax-equivalence-theorem]
sources:
  - paper: doi:10.1016/B978-0-12-068650-6.50025-3
    title: B. M. Irons and A. Razzaque, Experience with the patch test for convergence of finite elements, in A. K. Aziz (editor), The Mathematical Foundations of the Finite Element Method with Applications to Partial Differential Equations, Academic Press, 1972, 557-587
    locator: the statement of the patch test and its use on conforming and nonconforming elements
  - paper: doi:10.1002/nme.1620150203
    title: F. Stummel, The limitations of the patch test, International Journal for Numerical Methods in Engineering 15(2) (1980) 177-188
    locator: a nonconforming element that passes the patch test and does not converge
  - paper: doi:10.1137/0716037
    title: F. Stummel, The generalized patch test, SIAM Journal on Numerical Analysis 16(3) (1979) 449-471
    locator: the generalized patch test, which with approximability is necessary and sufficient for convergence of nonconforming elements
  - paper: doi:10.1002/nme.1620220105
    title: R. L. Taylor, J. C. Simo, O. C. Zienkiewicz and A. C. H. Chan, The patch test, a condition for assessing FEM convergence, International Journal for Numerical Methods in Engineering 22(1) (1986) 39-62
    locator: tests A, B and C, the single element test and the stability part of the patch test
  - paper: doi:10.1002/nme.1620100602
    title: R. L. Taylor, P. J. Beresford and E. L. Wilson, A non-conforming element for stress analysis, International Journal for Numerical Methods in Engineering 10(6) (1976) 1211-1219
    locator: the incompatible modes element changed so that it passes the patch test on general quadrilaterals
  - paper: doi:10.1016/0168-874X(85)90003-4
    title: R. H. MacNeal and R. L. Harder, A proposed standard set of problems to test finite element accuracy, Finite Elements in Analysis and Design 1(1) (1985) 3-20
    locator: the standard five element patch on a 0.24 by 0.12 rectangle
  - book: isbn:9781856176330
    title: O. C. Zienkiewicz, R. L. Taylor and J. Z. Zhu, The Finite Element Method, Its Basis and Fundamentals, seventh edition, Butterworth-Heinemann, 2013
    locator: the chapter on the patch test, reduced integration and nonconforming elements
---

The patch test checks a finite element, or a whole finite element code, on a small problem whose exact solution the element must reproduce. Take a patch of a few elements with at least one interior node and with distorted shapes. Choose an exact solution in the space that the element must contain, usually a linear field, which has a constant gradient (constant strain in elasticity). Prescribe its values on the boundary of the patch and solve for the interior nodes. The element passes if the computed values and the computed gradients equal the exact ones to rounding error. A conforming element with exact integration always passes. The test finds errors of consistency: wrong shape functions, wrong quadrature, a wrong Jacobian, or nonconforming shape functions whose jumps between elements do not cancel. Passing is not a proof of convergence. Stummel gave a nonconforming element that passes and does not converge, and the test also says nothing about stability unless it includes the stability part of Taylor and coauthors.

## In plain words

When the mesh gets finer, the true solution looks flatter and flatter inside each small group of elements. A good element must get a perfectly flat solution exactly right, or its error will not go away when the mesh is refined. The patch test checks this. Build a few elements of odd shapes around one inner point. Fix the outer edge to the values of a flat solution. Solve, and look at the inner point and at the computed slopes. If they are not right to the last digits, something is wrong in the element: in its shape functions, in its numerical integration, or in how its pieces join. The test is small, fast and should be in the automatic tests of every finite element code.

## When it applies

- A new element type, a new quadrature rule, a new mapping from the reference element, or new code that assembles the stiffness matrix.
- Nonconforming elements, whose shape functions are not continuous between elements, and elements with incompatible modes or assumed strains. For these the test is a real check of consistency, not a formality.
- Methods without a standard mesh: mesh-free methods, the [extended finite element method](/extended-finite-element-method/), the [virtual element method](/virtual-element-method/) and contact or interface discretizations.
- Any problem where the element must contain an exact polynomial space. For second order equations this is the linear functions. For plate bending in Kirchhoff theory it is the quadratic functions.

## The template

1. **Choose the patch.** Use at least one interior node, and elements that are not parallelograms, of mixed size and with all the node types of the element (corner, edge and interior nodes). Bugs that cancel on regular meshes appear on distorted ones.
2. **Choose the exact solution.** Take a polynomial of the degree that the element must reproduce, for example $u = a + b x + c y$, with zero body force. Repeat with each basic field ($1$, $x$, $y$ and, in elasticity, each strain component) so that no error can cancel.
3. **Test A (all nodes given).** Put the exact nodal values at every node and compute the residual $K u - f$ at the interior nodes. It must be zero. This test needs no solve.
4. **Test B (boundary nodes given).** Prescribe the exact values on the boundary nodes, solve for the interior nodes and compare. This is the usual form.
5. **Test C (natural boundary conditions).** Fix only enough values to remove the rigid motions, apply the boundary tractions of the exact solution, and solve. This test also checks that the stiffness matrix has no spurious zero energy modes.
6. **Compare.** Compare the nodal values and the gradients or stresses at the quadrature points with the exact ones. The difference must be at the level of rounding error, for example below $10^{-10}$ relative. A difference of $10^{-4}$ is a failure, not a near pass.

The idea behind the test: if a smooth solution is replaced by its linear Taylor polynomial on each patch, the remaining error goes to zero with the mesh size. An element that cannot reproduce the linear part has an error that does not go to zero, so a failure of the test means a consistency error of order one.

## Classic examples

**Linear triangles pass (exact numbers).** Take the unit square with the interior node $p = (\tfrac25, \tfrac35)$ joined to the four corners, which gives four triangles with areas $\tfrac3{10}, \tfrac3{10}, \tfrac15, \tfrac15$. For the Laplace equation the row of the stiffness matrix for $p$ is

$$K_{pp} = \tfrac{25}{6}, \quad K_{p,(0,0)} = -1, \quad K_{p,(1,0)} = -\tfrac23, \quad K_{p,(1,1)} = -1, \quad K_{p,(0,1)} = -\tfrac32.$$

The row sums to zero, so a constant passes. For $u = 1 + 2x + 3y$ the corner values are $1, 3, 6, 4$, and the interior equation gives $u_p = (1 + 2 + 6 + 6)/(25/6) = \tfrac{18}{5}$, which is the exact value $1 + \tfrac45 + \tfrac95$. The reason is general: the row for $p$ applied to a linear $u$ is $\int \nabla\phi_p \cdot \nabla u = \nabla u \cdot \int \nabla\phi_p = 0$, because $\phi_p$ vanishes on the boundary of the patch.

**Bilinear quadrilaterals and the Jacobian.** The MacNeal and Harder patch has the corners of a $0.24 \times 0.12$ rectangle and the interior nodes $(0.04, 0.02)$, $(0.18, 0.03)$, $(0.16, 0.08)$, $(0.08, 0.08)$, with five quadrilaterals. With $u = 1 + 2x + 3y$ and 2 by 2 Gauss quadrature, the isoparametric bilinear element gives the four interior values $1.14, 1.45, 1.56, 1.40$ with an error of $2 \times 10^{-16}$. A common shortcut evaluates the Jacobian only at the element centre. It is exact on parallelograms, but on this patch it gives $1.1046, 1.4737, 1.6456, 1.3358$, an error of $0.086$. It fails the test and it does not converge on distorted meshes.

**Incompatible modes.** Wilson's element adds to the bilinear quadrilateral two internal modes that are not continuous between elements. It passes on parallelograms and fails on general quadrilaterals. Taylor, Beresford and Wilson in 1976 changed the way the derivatives of the internal modes are integrated, so that their integral over each element is zero. Then the element passes on any shape.

**Nonconforming linear triangles.** The Crouzeix Raviart element has its nodes at the edge midpoints, so it is not continuous. The jump across each edge has mean value zero, so the boundary terms of the integration by parts cancel for linear fields, and the element passes.

**Reduced integration.** The bilinear quadrilateral with one quadrature point passes tests A and B. In test C its stiffness matrix is singular, because of the hourglass modes, which have zero energy at the centre. The stability part of the test finds this.

**Mesh-free methods.** The [element-free Galerkin method](/element-free-galerkin-method/) with simple nodal integration fails the linear patch test. Background cell quadrature with enough points, or a smoothed nodal integration, makes it pass.

## Variations

- **Higher order patch test.** For an element of degree $k$, use all polynomials of degree $k$ as exact solutions.
- **Single element test.** Check one element alone for the right number of zero energy modes (the rigid motions only) and for the rank of its stiffness matrix.
- **Weak patch test.** Some nonconforming elements fail on a fixed patch, but the error goes to zero as the patch shrinks. This is called passing the test in the weak sense. It still allows convergence, more slowly.
- **Generalized patch test of Stummel.** A mathematical condition on the jumps of the nonconforming functions. Together with approximability it is necessary and sufficient for convergence.
- **Patch tests for contact and interfaces.** Two meshes that do not match across a flat interface must transmit a constant stress exactly. Mortar methods pass and simple node to segment contact does not.
- **Standard benchmark sets.** The MacNeal and Harder set adds bending, twist and distortion problems to the patch test, for elements that must also work well, not only converge.

## Pitfalls

- **Regular meshes only.** A patch of squares or parallelograms hides errors in the Jacobian and in the quadrature. Always distort.
- **Only nodal values.** Check the stresses at the quadrature points too. An error in the recovery of stresses does not show in the nodal values.
- **Passing is not sufficient.** Stummel's example passes and does not converge. Also check stability (test C) and the convergence rate on a smooth problem with a refined mesh.
- **Tolerance too loose.** The test is exact. An error of $10^{-6}$ on a well conditioned patch is a bug.
- **Body forces.** The exact solution must match the loads. A linear field with a nonzero body force is not a solution, and the test then fails for the wrong reason.
- **Only one exact field.** An error in the $y$ derivative does not show with $u = x$. Use each basic field.

## Exercises

1. Prove that every conforming element whose space contains the linear functions passes test A with exact integration. Hint: for an interior node $p$, the row of $K$ applied to a linear $u$ is $\nabla u \cdot \int \nabla\phi_p\,dx$. Use the divergence theorem on the support of $\phi_p$.
2. In the first example, move the interior node to $(\tfrac12, \tfrac12)$. Show that $K_{pp} = 4$, that each corner gives $-1$, and that $u_p$ is the mean of the four corner values. Check that this equals $u(\tfrac12, \tfrac12)$ for every linear $u$.
3. Explain why the shortcut with the Jacobian at the centre is exact on a parallelogram. Hint: the map from the reference square to a parallelogram is affine.
4. For the bilinear square with one quadrature point at the centre, find the nodal vector $(1, -1, 1, -1)$ times a constant. Show that its gradient is zero at the centre but not elsewhere, so the one point stiffness matrix has a zero energy mode that is not a rigid motion.
5. For the Crouzeix Raviart element, show that the jump of a piecewise linear function across an edge, if the function is continuous at the midpoint, has mean value zero on the edge. Use this to show that the element passes test A.

## References
