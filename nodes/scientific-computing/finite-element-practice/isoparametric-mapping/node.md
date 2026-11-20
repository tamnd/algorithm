---
tag: VR6JGK
kind: technique
slug: isoparametric-mapping
name: Isoparametric mapping
aliases:
- isoparametric element
area: scientific-computing/finite-element-practice
level: core
summary: Maps a reference element to each physical element with the same shape functions used for the solution, which allows curved boundaries.
prereqs: [lagrange-finite-element, ciarlet-finite-element, gaussian-quadrature]
see_also: [finite-element-assembly, isogeometric-analysis, patch-test, mesh-generation, deformation-gradient, invertible-finite-elements, brittle-fracture, bramble-hilbert-lemma]
sources:
  - paper: doi:10.1016/0020-7683(68)90031-0
    title: J. Ergatoudis, B. M. Irons and O. C. Zienkiewicz, Curved, isoparametric, quadrilateral elements for finite element analysis, International Journal of Solids and Structures 4(1) (1968) 31-42
  - paper: doi:10.1016/0045-7825(72)90006-0
    title: P. G. Ciarlet and P.-A. Raviart, Interpolation theory over curved elements, with applications to finite element methods, Computer Methods in Applied Mechanics and Engineering 1(2) (1972) 217-249
  - book: isbn:9780898715149
    title: Philippe G. Ciarlet, The Finite Element Method for Elliptic Problems, SIAM Classics in Applied Mathematics 40, 2002
    locator: Chapter 4 (isoparametric finite elements and problems on curved domains)
  - book: isbn:9780486411811
    title: Thomas J. R. Hughes, The Finite Element Method, Linear Static and Dynamic Finite Element Analysis, Dover, 2000
    locator: Chapter 3 (isoparametric elements and elementary programming concepts)
---

An isoparametric mapping maps a fixed reference cell $\hat K$ onto each physical cell $K$ with the same shape functions that represent the solution: $F_K(\hat x) = \sum_j x_j\,\hat\phi_j(\hat x)$, where $x_j$ are the coordinates of the nodes of $K$. With quadratic or higher shape functions the cells can have curved edges that follow a curved boundary, and with bilinear ones a code can use general quadrilaterals. Because the geometry and the solution use one basis, the element represents every linear function exactly, so it passes the [patch test](/patch-test/). The map is valid only if its Jacobian keeps one sign over the reference cell.

## In plain words

You compute everything on one simple master shape, a unit square or a unit triangle, and then stretch and bend it into each real cell of the mesh. The rule for stretching uses the same building blocks that describe the unknown field on the cell. So if those blocks can bend, the cell edges can bend too, and the mesh can follow a round hole or a curved wing. The same choice also makes sure that a simple uniform state, such as a constant stretch, comes out exactly right on any mesh. One check is essential: the stretched cell must not fold over itself. If it folds, the computed areas become negative and the results are wrong.

## When it applies

- **Curved boundaries.** For elements of degree $k \ge 2$, a polygonal approximation of a curved boundary has a geometric error of order $h^2$, and that error limits the accuracy. Isoparametric cells of degree $k$ along the boundary approximate it to order $h^{k+1}$ and keep the optimal rates (Ciarlet and Raviart, 1972).
- **Quadrilateral and hexahedral meshes.** A Q1 cell that is not a parallelogram has no affine map from the unit square, so a bilinear isoparametric map is the standard way to define it.
- **Lagrangian solid mechanics.** The same interpolation of node positions gives the [deformation gradient](/deformation-gradient/) in large-deformation codes.

The technique needs a reference element with a nodal basis, node positions that give a positive Jacobian everywhere in $\hat K$, and a quadrature rule on $\hat K$, because the integrands are no longer polynomials.

## The template

The Jacobian is $J(\hat x) = \sum_j x_j\,\hat\nabla\hat\phi_j(\hat x)^\top$, a $d \times d$ matrix. Physical gradients are $\nabla\phi_j = J^{-\top}\hat\nabla\hat\phi_j$, and $dx = |\det J|\,d\hat x$.

```pseudo id=main
ISOPARAMETRIC-ELEMENT(x_1 .. x_n, kappa, f, rule (xi_q, w_q))   ▷ x_j are the nodes of K
L1  A_K <- 0 (n by n), b_K <- 0 (length n)
L2  for each quadrature point xi_q with weight w_q in the rule on K-hat do
L3      evaluate phi-hat_j(xi_q) and grad-hat phi-hat_j(xi_q) for j = 1 .. n
L4      x_q <- sum_j x_j phi-hat_j(xi_q);  J <- sum_j x_j grad-hat phi-hat_j(xi_q)^T   ▷ same basis as u_h
L5      if det J <= 0 then report an inverted element and stop
L6      G <- J^(-T) [grad-hat phi-hat_1 .. grad-hat phi-hat_n]   ▷ physical gradients, d by n
L7      A_K <- A_K + w_q det J kappa(x_q) G^T G
L8      b_K <- b_K + w_q det J f(x_q) [phi-hat_1(xi_q) .. phi-hat_n(xi_q)]^T
L9  return A_K, b_K
```

The local matrix then goes into the global one by [finite element assembly](/finite-element-assembly/), with no change: the map affects only how the element integrals are computed.

**Why linear functions are exact.** The Lagrange basis satisfies $\sum_j\hat\phi_j = 1$, and the map gives $\sum_j x_j\hat\phi_j(\hat x) = x$. For $u = a + b\cdot x$ the nodal values $u_j = a + b\cdot x_j$ therefore give $\sum_j u_j\hat\phi_j(\hat x) = a + b\cdot F_K(\hat x) = u$. So every linear function lies in the isoparametric space, on any mesh of valid cells. A mesh of such cells reproduces a constant gradient exactly, which is the patch test.

## Classic examples

**A bilinear trapezoid.** Map $[0,1]^2$ with the Q1 basis $(1-\xi)(1-\eta)$, $\xi(1-\eta)$, $\xi\eta$, $(1-\xi)\eta$ onto the cell with nodes $(0,0)$, $(2,0)$, $(1,1)$, $(0,1)$ in the same order. Then $x = 2\xi - \xi\eta$ and $y = \eta$, so

$$J = \begin{pmatrix} 2 - \eta & -\xi \\ 0 & 1\end{pmatrix}, \qquad \det J = 2 - \eta \in [1, 2].$$

The area is $\int_0^1\int_0^1 (2 - \eta)\,d\xi\,d\eta = \tfrac32$, which is the area of the trapezoid with parallel sides 2 and 1 and height 1. Since $\det J$ is not constant, the entries of $J^{-\top}$ are rational functions, and Gauss quadrature computes $A_K$ only approximately. Codes use a $2 \times 2$ Gauss rule for this cell.

**A reentrant quadrilateral.** With the nodes $(0,0)$, $(1,0)$, $(\tfrac14, \tfrac14)$, $(0,1)$ the same map gives $\det J = 1 - \tfrac34(\xi + \eta)$. Its values at the four corners are $1$, $\tfrac14$, $-\tfrac12$ and $\tfrac14$, so the map folds near the corner $(\tfrac14, \tfrac14)$, which is a reflex corner. For a bilinear map $\det J$ is an affine function of $\xi$ and $\eta$, so it is positive on the whole square if and only if it is positive at the four corners, which holds if and only if the quadrilateral is convex.

**A curved boundary edge.** A P2 triangle with vertices $(0,0)$, $(1,0)$, $(0,1)$ and the node of the outer edge moved to $(\tfrac{\sqrt2}2, \tfrac{\sqrt2}2)$ on the unit circle approximates a quarter of the unit disk. The outer edge becomes a parabola whose tangent at the moved node is parallel to the chord. By Archimedes' rule its segment has $\tfrac43$ of the area of the triangle on the chord with apex at that node, which is $\tfrac43\cdot\tfrac{\sqrt2 - 1}2$. The total area is $\tfrac12 + \tfrac23(\sqrt2 - 1) \approx 0.77614$, against $\pi/4 \approx 0.78540$, an error of 1.2 percent. The straight triangle has area $0.5$, an error of 36 percent.

**The quarter-point element.** On one edge of a P2 element, map $\xi \in [0,1]$ with the end nodes at $0$ and $1$ and the middle node at $m$: $x(\xi) = \xi(2\xi - 1) + 4m\,\xi(1 - \xi)$. Then $x'(\xi) = 4\xi - 1 + 4m(1 - 2\xi)$ is affine, with $x'(0) = 4m - 1$ and $x'(1) = 3 - 4m$, so the map is valid exactly for $\tfrac14 < m < \tfrac34$. At $m = \tfrac14$ we get $x = \xi^2$, so $\xi = \sqrt x$, and a quadratic in $\xi$ contains the term $\sqrt x$. This is the square-root singularity of the displacement near a crack tip, and crack codes in [fracture mechanics](/brittle-fracture/) place the middle nodes of the cells at the tip at the quarter points on purpose.

## Variations

- **Subparametric elements.** The map has a lower degree than the solution, for example affine maps for the interior cells of a P2 mesh. They still reproduce linear functions, and they save work.
- **Superparametric elements.** The map has a higher degree than the solution. The constant and linear functions are no longer in the space in general, so these elements can fail the patch test.
- **Transfinite or blending maps.** Interpolate an exact boundary curve into the cell instead of a polynomial through nodes, as in the Gordon-Hall construction.
- **[Isogeometric analysis](/isogeometric-analysis/).** Uses the spline or NURBS basis of the CAD model for both geometry and solution. This keeps the isoparametric idea and makes the geometry exact.

## Pitfalls

- **Checking only the corners of curved cells.** For a P2 triangle, $\det J$ is a polynomial of degree 2, and it can be negative inside the cell while it is positive at all nodes. Robust checks bound it with its Bernstein coefficients or sample it at the quadrature points. Mesh generators that move boundary nodes onto curves often create such cells. See [invertible finite elements](/invertible-finite-elements/) for the same problem in simulation.
- **Using $|\det J|$ without checking the sign.** The absolute value hides an inverted cell, and the code computes a positive but meaningless matrix.
- **Using $J^{-1}$ in place of $J^{-\top}$.** The physical gradient is $J^{-\top}\hat\nabla\hat\phi$. The two agree only when $J$ is symmetric, so the error shows up only on sheared cells.
- **Too few quadrature points.** The stiffness integrand is rational on non-affine cells. A rule that is too weak can give a singular matrix (hourglass modes on Q1 with one point) or lose the convergence order.
- **Strong distortion.** On quadrilateral meshes that do not tend to parallelograms under refinement, the mapped space does not contain all of $\mathcal{P}_k$ in physical coordinates. Arnold, Boffi and Falk showed in 2002 that the serendipity elements then lose convergence order.

## Exercises

1. Show that a bilinear map of $[0,1]^2$ is valid if and only if the four nodes form a convex quadrilateral in the right order. *Hint:* $\det J$ is affine in $(\xi, \eta)$, and its value at a corner is twice the signed area of the triangle formed by that corner and its two neighbors.
2. For the trapezoid above, compute $J^{-\top}$ and the physical gradient of the basis function $\xi\eta$ at $(\xi, \eta) = (\tfrac12, \tfrac12)$. *Answer:* $J^{-\top} = \frac1{2 - \eta}\begin{pmatrix} 1 & 0 \\ \xi & 2 - \eta\end{pmatrix}$, and at the point the gradient is $(\tfrac13, \tfrac23)$.
3. For the quarter-point edge with $m = \tfrac14$, show that the derivative in $x$ of a P2 function behaves like $x^{-1/2}$ near $x = 0$, and that a strain of size $r^{-1/2}$ near a crack tip in 2D still has finite energy. *Answer:* $u = a + b\xi + c\xi^2 = a + b\sqrt x + cx$, so $du/dx = b/(2\sqrt x) + c$. In polar coordinates $\int_0^{2\pi}\int_0^1 (r^{-1/2})^2\,r\,dr\,d\theta = 2\pi$.
4. Prove that a superparametric element, with a P2 map and P1 shape functions on the reference cell, does not contain the function $x$ when its edge is curved. *Answer:* $x \circ F_K$ is the first component of $F_K$, which is quadratic and not linear in $\hat x$, so it is not in $\mathcal{P}_1(\hat K)$.

## References
