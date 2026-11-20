---
tag: EYHGHZ
kind: algorithm
slug: virtual-element-method
name: Virtual element method
aliases:
- VEM
area: scientific-computing/finite-element-practice
level: research
summary: A Galerkin method on general polygonal meshes whose basis functions are never computed; projections onto polynomials give the stiffness matrix.
solves: [poisson-equation]
model: real-ram
complexity:
  vars: {n: the number of vertices, e: the number of polygons, m: the largest number of vertices of a polygon, i: the number of conjugate gradient iterations}
  time: {worst: "Θ((i + 1) e m^2)"}
  space: {extra: "Θ(n + e m^2)"}
properties: {deterministic: true, iterative: true, polygonal_meshes: true, basis_functions_computed: false, passes_patch_test: true, symmetric_positive_definite: true, needs_stabilization: true}
history:
  year: 2013
  people: [L. Beirão da Veiga, F. Brezzi, A. Cangiani, G. Manzini, L. D. Marini, A. Russo]
  note: The method grew out of mimetic finite differences. Beirão da Veiga, Brezzi, Cangiani, Manzini, Marini and Russo stated its basic principles in 2013 as a Galerkin method with a virtual local space.
prereqs: [galerkin-method, finite-element-method, lagrange-finite-element]
see_also: [patch-test, extended-finite-element-method, mixed-finite-element-method, discontinuous-galerkin-method, voronoi-diagram, star-shaped-polygon, cea-lemma, conjugate-gradient-method]
sources:
  - paper: doi:10.1137/040613950
    title: F. Brezzi, K. Lipnikov and M. Shashkov, Convergence of the mimetic finite difference method for diffusion problems on polyhedral meshes, SIAM Journal on Numerical Analysis 43(5) (2005) 1872-1896
    locator: the mimetic finite difference method for diffusion on polyhedral meshes that the order 1 virtual element method grew out of
  - paper: doi:10.1142/S0218202512500492
    title: L. Beirão da Veiga, F. Brezzi, A. Cangiani, G. Manzini, L. D. Marini and A. Russo, Basic principles of virtual element methods, Mathematical Models and Methods in Applied Sciences 23(1) (2013) 199-214
    locator: the local virtual space, the degrees of freedom, the consistency and stability conditions and the abstract error estimate
  - paper: doi:10.1142/S021820251440003X
    title: L. Beirão da Veiga, F. Brezzi, L. D. Marini and A. Russo, The hitchhiker's guide to the virtual element method, Mathematical Models and Methods in Applied Sciences 24(8) (2014) 1541-1573
    locator: the matrices D, B and G, the projection, the dofi-dofi stabilization and the load term, written for implementation
  - paper: doi:10.1007/s11075-016-0235-3
    title: O. J. Sutton, The virtual element method in 50 lines of MATLAB, Numerical Algorithms 75(4) (2017) 1141-1159
    locator: a complete implementation of the order 1 method on polygonal meshes with the same matrices and stabilization
  - paper: doi:10.1017/S0962492922000095
    title: L. Beirão da Veiga, F. Brezzi, L. D. Marini and A. Russo, The virtual element method, Acta Numerica 32 (2023) 123-202
    locator: the survey of the theory, the error estimates on star shaped polygons, the choices of stabilization and the extensions
---

The virtual element method (VEM) is a Galerkin method on meshes of general polygons in 2D or polyhedra in 3D. On each polygon, the local space contains the polynomials of degree $k$ and other functions that are defined as solutions of a local partial differential equation, so their values inside the polygon are never known. The method needs only the degrees of freedom, which for $k = 1$ are the values at the vertices. From them it computes exactly the projection of each function onto the polynomials, and builds the stiffness matrix from two parts. The consistency part is the energy of the projections and is exact when one of the arguments is a polynomial. The stability part is a cheap symmetric form that controls the rest. The method passes the [patch test](/patch-test/) on any polygonal mesh, it accepts nonconvex polygons and collinear vertices (hanging nodes), and on a triangle with $k = 1$ it is the standard linear finite element.

## In plain words

Standard finite elements need simple shapes such as triangles and squares, because each needs a formula for its basis functions. A mesh of general polygons, with any number of sides, is easier to make and to change, but formulas for its basis functions are hard to find. The virtual element method avoids them. It never asks what a basis function looks like inside a polygon. It only asks for a best straight fit of each function, and this fit comes from the values at the corners. The energy of the fits gives most of the stiffness matrix. A small extra term stops the parts that the fit cannot see from going free.

## The problem

**Input.** A polygon $\Omega$ in the plane, a mesh of $\Omega$ by $e$ polygons that meet edge to edge (each polygon star shaped with respect to a disc, with vertices listed counterclockwise), a source $f$ and boundary values $g$.

**Output.** Values $u_I$ at the $n$ vertices of the mesh and, on each polygon $E$, a linear polynomial $\Pi^\nabla_E u_h$, which approximate the solution of $-\Delta u = f$ in $\Omega$ with $u = g$ on $\partial\Omega$.

**The local space.** For $k = 1$,

$$V_E = \{v \in H^1(E) : \Delta v = 0 \text{ in } E,\ v \text{ is continuous on } \partial E \text{ and linear on each edge}\}.$$

A function in $V_E$ is fixed by its values at the vertices of $E$, because the harmonic function with given boundary values is unique. $V_E$ contains the linear polynomials. On a triangle $V_E$ is exactly the set of linear polynomials. On other polygons the basis functions $\varphi_i$ (with $\varphi_i(v_j) = \delta_{ij}$) are not polynomials and the method does not compute them.

**The projection.** $\Pi^\nabla_E v$ is the linear polynomial with

$$\int_E \nabla \Pi^\nabla_E v \cdot \nabla p\,dx = \int_E \nabla v \cdot \nabla p\,dx \ \text{ for all linear } p, \qquad \frac1m \sum_{i=1}^m \Pi^\nabla_E v(v_i) = \frac1m \sum_{i=1}^m v(v_i).$$

The right side is computable: since $\Delta p = 0$ and $\nabla p$ is constant, $\int_E \nabla v \cdot \nabla p = \int_{\partial E} v\,\nabla p \cdot n\,ds$, and $v$ is linear on each edge, so the trapezoid rule on each edge is exact.

## The algorithm

Use the scaled monomials $m_1 = 1$, $m_2 = (x - x_E)/h_E$ and $m_3 = (y - y_E)/h_E$, where $h_E$ is the diameter and $(x_E, y_E)$ the average of the vertices. Write $e_i$ for the edge from vertex $i$ to vertex $i + 1$, $|e_i|$ for its length and $n_i$ for its outward unit normal.

```pseudo id=main
VEM-1(points, polygons, f, g, tau)
L1  for each polygon E with vertices v_1, ..., v_m: h <- diameter, (x_E, y_E) <- average of the vertices
L2      D[i, a] <- m_a(v_i) for i = 1..m, a = 1..3
L3      B[1, i] <- 1/m;  B[a, i] <- (|e_{i-1}| n_{i-1} + |e_i| n_i) . grad m_a / 2 for a = 2, 3
L4      G <- B D;  P* <- G^{-1} B;  P <- D P*                     ▷ P* gives the coefficients of the projection
L5      K_E <- (P*)^T G~ P* + tau (I - P)^T (I - P);  F_E[i] <- integral over E of f times (P* e_i) . m
L6  add K_E and F_E into the global matrix K and vector F
L7  set u = g at the boundary vertices and solve K u = F for the others by conjugate gradients
L8  return the vertex values u and the projections P* u_E on each polygon
```

Here $\tilde G$ is $G$ with its first row set to zero, so $\tilde G_{ab} = \int_E \nabla m_a \cdot \nabla m_b$, which is $|E|/h_E^2$ on the diagonal for $a, b \ge 2$ and zero elsewhere. Row $a \ge 2$ of $B$ holds $\int_E \nabla\varphi_i \cdot \nabla m_a$, computed from the boundary integral above: the trapezoid rule gives vertex $i$ half of each of its two edges. The load uses $\Pi^\nabla_E \varphi_i$, a known linear function, in place of the unknown $\varphi_i$, and the reference code integrates it with a 7 point rule on the triangles from the vertex average to each edge. The dofi-dofi stabilization of line L5 is $\tau$ times the Euclidean inner product of the vertex values of $(I - \Pi)v$ and $(I - \Pi)w$. In 2D with $k = 1$ it has the right scaling for any polygon size, and $\tau = 1$ is the common choice.

## Example

**The unit square.** Take the vertices $(0, 0)$, $(1, 0)$, $(1, 1)$ and $(0, 1)$. Then $h = \sqrt 2$, the centre is $(\tfrac12, \tfrac12)$, and with $s = 1/(2\sqrt 2)$

$$D = \begin{pmatrix} 1 & -s & -s \\ 1 & s & -s \\ 1 & s & s \\ 1 & -s & s \end{pmatrix}, \qquad B = \begin{pmatrix} \frac14 & \frac14 & \frac14 & \frac14 \\ -s & s & s & -s \\ -s & -s & s & s \end{pmatrix}, \qquad G = BD = \begin{pmatrix} 1 & 0 & 0 \\ 0 & \frac12 & 0 \\ 0 & 0 & \frac12 \end{pmatrix}.$$

For vertex 1, the edges $e_4$ and $e_1$ have $|e|\,n = (-1, 0)$ and $(0, -1)$, and half their sum dotted with $\nabla m_2 = (1/h, 0)$ is $-1/(2h) = -s$. The diagonal of $G$ is $|E|/h^2 = \tfrac12$. So $P^* = G^{-1}B$ has the rows $\tfrac14(1, 1, 1, 1)$, $2s(-1, 1, 1, -1)$ and $2s(-1, -1, 1, 1)$. The consistency part is

$$(P^*)^\top \tilde G P^* = \frac12\begin{pmatrix} 1 & 0 & -1 & 0 \\ 0 & 1 & 0 & -1 \\ -1 & 0 & 1 & 0 \\ 0 & -1 & 0 & 1 \end{pmatrix}.$$

It does not see the hourglass mode $w = (1, -1, 1, -1)$: the projection of $w$ is zero. So $I - P = \tfrac14 w w^\top$, and with $\tau = 1$ the stabilization adds $\tfrac14 w w^\top$. The result has $\tfrac34$ on the diagonal and $-\tfrac14$ in every other entry. The bilinear element on the same square has $\tfrac23$ on the diagonal, $-\tfrac16$ for neighbours and $-\tfrac13$ for the opposite vertex. Both matrices give the same energy to every linear field, which is what the patch test needs, and differ only on the hourglass mode.

**A triangle.** On the triangle $(0, 0)$, $(1, 0)$, $(0, 1)$, $P = I$, so the stabilization is zero for every $\tau$ and $K_E$ is the linear finite element matrix with rows $(1, -\tfrac12, -\tfrac12)$, $(-\tfrac12, \tfrac12, 0)$ and $(-\tfrac12, 0, \tfrac12)$. The reference test checks this with $\tau = 7$.

**Convergence.** The reference tests solve $-\Delta u = 2\pi^2 \sin\pi x \sin\pi y$ with $u = 0$ on the boundary of the unit square. The meshes have $n \times n$ cells. On the distorted mesh the interior grid nodes move by up to $0.2/n$ in each direction, and each cell edge gets a midpoint node with probability $\tfrac12$, so the cells have 4 to 8 vertices with collinear ones. The errors are those of the projections.

| cells per side | squares, $L^2$ | squares, $H^1$ | distorted, vertices | distorted, $L^2$ | distorted, $H^1$ |
|---|---|---|---|---|---|
| 4 | $0.0492$ | $0.699$ | 39 | $0.0529$ | $0.720$ |
| 8 | $0.0123$ | $0.354$ | 153 | $0.0132$ | $0.362$ |
| 16 | $0.00307$ | $0.178$ | 575 | $0.00336$ | $0.184$ |
| 32 | $0.000767$ | $0.0890$ | 2146 | $0.000845$ | $0.0921$ |

The observed orders at the finest step are $2.00$ in $L^2$ and $1.00$ in $H^1$ on squares. On the distorted polygons they are between $1.97$ and $2.01$ in $L^2$ and between $0.97$ and $1.00$ in $H^1$. These are the orders of linear finite elements. The largest vertex error on the distorted meshes converges with order between $1.6$ and $1.8$.

**The stabilization changes the answer.** On the distorted mesh with 8 cells per side, $\tau = 0.25$, $1$ and $4$ give $H^1$ errors $0.369$, $0.368$ and $0.396$ and $L^2$ errors $0.0092$, $0.0135$ and $0.0380$. The rates do not depend on $\tau$, but the constants do.

## Correctness

The [proof](proofs/correctness.md) shows four facts. First, $G$ is nonsingular, and $P^*$ gives the exact coefficients of $\Pi^\nabla_E v$ from the vertex values of $v$, because the boundary integral with the trapezoid rule is exact for functions that are linear on each edge. Second (consistency), $a^h_E(v, p) = \int_E \nabla v \cdot \nabla p$ for every $v \in V_E$ and every linear $p$: the stabilization vanishes on $p$, and the consistency part is the energy of the projection, which equals the energy of $v$ against $p$. Third (stability), for $\tau > 0$, $a^h_E(v, v) = 0$ only for constants, so the global matrix is symmetric positive definite on the free vertices. Fourth (the patch test), if $f = 0$ and $g$ is linear, the vertex values of $g$ solve the discrete system, so the method is exact on any mesh. The proof also gives the abstract error estimate, which bounds the energy error by interpolation and polynomial approximation errors. The bounds on these errors for star shaped polygons, which give order $h$ in $H^1$ and $h^2$ in $L^2$, are cited from the 2013 paper and the 2023 survey.

## Complexity

For a polygon with $m$ vertices, lines L2 to L4 cost $\Theta(m)$, the products in line L5 cost $\Theta(m^2)$, and the load with $7m$ quadrature points costs $\Theta(m^2)$. Assembly therefore costs $\Theta(e m^2)$ time, and the global matrix has $\Theta(e m^2)$ nonzero entries. Each conjugate gradient iteration costs one product with it, so the total time is $\Theta((i + 1)\,e\,m^2)$. On quasi uniform meshes the condition number grows like $h^{-2}$, so $i$ grows like $\sqrt n$ for a fixed tolerance, and a direct sparse solver or a multigrid preconditioner does better on large problems. The memory is $\Theta(n + e m^2)$.

## Properties

- **Any polygon.** The same code handles triangles, quadrilaterals, Voronoi cells, nonconvex star shaped cells and cells with collinear vertices. A hanging node is just one more vertex.
- **Exact on linear fields.** The patch test holds on every mesh and for every $\tau > 0$, because the consistency part is exact and the stabilization vanishes on polynomials.
- **No basis functions.** Only vertex coordinates and values enter the matrices. No mapping to a reference element and no quadrature of the unknown basis functions is needed for the stiffness.
- **Reduces to finite elements on triangles.** For $k = 1$ on a triangle, the local space is linear, the stabilization vanishes and the method is the linear Lagrange element.
- **The stabilization is a choice.** The consistency part fixes the matrix on polynomials only. The stabilization changes the matrix on the other functions and the error constants, but not the rates, as long as it is bounded above and below by the energy on the functions with zero projection.

## Variants and improvements

- **Higher order.** For degree $k$, the unknowns are the vertex values, $k - 1$ values on each edge and the moments against polynomials of degree $k - 2$ inside. The projection then also needs these moments.
- **Enhanced spaces.** A modified local space makes the $L^2$ projection onto polynomials of degree $k$ computable, which gives a better load term and is needed for reaction and time dependent terms.
- **Other stabilizations.** The trace stabilization integrates the tangential derivative along the boundary, and the diagonal recipe scales each vertex term by the diagonal of the consistency part. These are more robust for elements with very short edges or high aspect ratios.
- **Other equations.** Linear and nonlinear elasticity, plates, Stokes flow, Maxwell equations and mixed forms have virtual elements. The H(div) and H(curl) versions connect with the [mixed finite element method](/mixed-finite-element-method/).
- **Related methods.** Mimetic finite differences have the same algebra for $k = 1$, and polygonal finite elements with generalized barycentric coordinates compute the basis functions that VEM avoids. The [discontinuous Galerkin method](/discontinuous-galerkin-method/) also works on polygons but has more unknowns.

## When to use it

Use it when the mesh is naturally polygonal: Voronoi meshes of [Voronoi diagrams](/voronoi-diagram/), agglomerated or coarsened meshes, meshes of fractured or layered media, meshes that are cut by an interface, and adaptive meshes with hanging nodes. It is also useful in fracture and topology optimization, where elements are cut or merged during the computation. On simplex meshes, standard finite elements are simpler and do the same job.

## Pitfalls

- **Polygons that are not star shaped.** The theory needs each polygon to be star shaped with respect to a disc of radius comparable to its diameter. Very thin polygons, or tiny edges next to long ones, can make the default stabilization too weak or too strong.
- **Forgetting the stabilization.** With $\tau = 0$ the matrix is singular on the functions with zero projection, such as the hourglass mode of a square. The global matrix can then be singular or very badly conditioned.
- **The answer depends on $\tau$.** In the reference test, $\tau = 4$ gives an $L^2$ error 4 times larger than $\tau = 0.25$. Do not tune $\tau$ to the test problem. Use a recipe with a fixed scaling.
- **Errors of the virtual function.** $u_h$ is not known inside a polygon. Measure errors with $\Pi^\nabla u_h$ or with the vertex values, and say which. Post processing that needs pointwise values must use the projection.
- **Clockwise polygons.** The formulas of line L3 assume counterclockwise vertices. A clockwise polygon flips the sign of rows 2 and 3 of $B$ and of the block of $G$ that holds $|E|/h^2$, so $P^*$ stays the same but the consistency part changes sign and $K_E$ is indefinite. Check the sign of the [polygon area](/polygon-area/) first.
- **Edge conformity.** Two neighbouring polygons must list the same vertices on their common edge. A hanging node that only one polygon lists makes the method nonconforming and the patch test fails.

## Implementations

## History

Mimetic finite difference methods for diffusion on polyhedral meshes, developed in the 2000s by Brezzi, Lipnikov, Shashkov, Manzini and others, already had the algebra of the order 1 method. Beirão da Veiga, Brezzi, Cangiani, Manzini, Marini and Russo in 2013 recast it as a Galerkin method with a virtual local space and called it the virtual element method. The hitchhiker's guide of 2014 gave the matrix formulas for implementation, and Sutton in 2017 published a short MATLAB code that made the method widely known. The survey of Beirão da Veiga, Brezzi, Marini and Russo in Acta Numerica 2023 describes the theory and the many extensions.

## References
