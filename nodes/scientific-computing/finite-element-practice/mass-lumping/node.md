---
tag: 74GYE7
kind: technique
slug: mass-lumping
name: Mass lumping
aliases:
- lumped mass matrix
area: scientific-computing/finite-element-practice
level: core
summary: Replaces the consistent mass matrix by a diagonal one, by row sums or nodal quadrature, so explicit time stepping needs no linear solve.
prereqs: [finite-element-assembly, lagrange-finite-element]
see_also: [corotational-fem, modal-reduction, brittle-fracture, heat-equation, wave-equation, spectral-element-method, gauss-lobatto-quadrature, method-of-lines]
sources:
  - book: isbn:9783540331216
    title: Vidar Thomée, Galerkin Finite Element Methods for Parabolic Problems, second edition, Springer, 2006
    locator: Chapter 15 (the method of lumped masses)
  - paper: doi:10.1002/eqe.4290040305
    title: E. Hinton, T. Rock and O. C. Zienkiewicz, A note on mass lumping and related processes in the finite element method, Earthquake Engineering and Structural Dynamics 4(3) (1976) 245-249
    locator: diagonal scaling of the consistent mass matrix
  - paper: doi:10.1137/S0036142997329554
    title: G. Cohen, P. Joly, J. E. Roberts and N. Tordjman, Higher order triangular finite elements with mass lumping for the wave equation, SIAM Journal on Numerical Analysis 38(6) (2001) 2047-2078
    locator: enriched triangular elements and positive quadrature at the nodes
---

Mass lumping replaces the consistent mass matrix $M_{ij} = (\phi_j, \phi_i)$ of a finite element method by a diagonal matrix $M_L$, most often by adding each row onto the diagonal or by using a quadrature rule whose points are the nodes. With a diagonal mass matrix an explicit time step for the heat or wave equation costs only a division per unknown, with no linear solve. For P1 elements lumping keeps the convergence order of the consistent method and also allows a larger stable time step. For P2 triangles the row sums at the vertices are zero, so row-sum lumping fails and special elements with positive nodal quadrature are needed.

## In plain words

In a finite element model the mass of the material is spread smoothly over each cell, so the motion of one point drags its neighbors along. Writing this down gives a table of masses that couples every point to its neighbors, and each time step must then solve a system of equations. Mass lumping moves all the mass of each cell onto its corner points, as if the material were a set of beads joined by springs. Then each point has its own mass, and a time step is just a division at each point. For the simplest elements this change costs no accuracy at all. For more refined elements it must be done with care, because a corner can end up with no mass or even a negative mass.

## When it applies

- **Explicit time stepping.** The [method of lines](/method-of-lines/) gives $M\dot U + KU = F$ for the [heat equation](/heat-equation/) and $M\ddot U + KU = F$ for the [wave equation](/wave-equation/) and elastodynamics. Forward Euler and central differences need $M^{-1}$ in every step, which is trivial only for a diagonal $M$.
- **Positivity.** For backward Euler on the heat equation with P1 elements, the consistent mass matrix can give negative values from nonnegative data for small time steps. The lumped matrix keeps nonnegativity on meshes without obtuse angles.
- **Eigenvalue problems.** $Kx = \lambda Mx$ with a diagonal $M$ becomes a standard symmetric problem for $M^{-1/2}KM^{-1/2}$.

Lumping needs a positive diagonal. Row sums give one for P1 and Q1 elements and for spectral elements with Gauss-Lobatto nodes, but not for P2 triangles or tetrahedra.

## The template

```pseudo id=main
LUMP(cells, ELEMENT-MASS, method)          ▷ returns the diagonal m of M_L
L1  m <- zero vector of length N
L2  for each cell K with local-to-global map g do
L3      M_K <- ELEMENT-MASS(K)              ▷ consistent element mass, exact quadrature
L4      if method = row sum then w_r <- sum_s M_K[r, s] for each local r
L5      if method = diagonal scaling then w_r <- M_K[r, r] |K| / (sum_s M_K[s, s])
L6      if method = nodal quadrature then w_r <- the weight of the rule at node r
L7      for each local r do m[g[r]] <- m[g[r]] + w_r
L8  if some m_i <= 0 then report that this lumping is not usable for the element
L9  return m

EXPLICIT-WAVE-STEP(U_old, U, m, K, F, dt)  ▷ central differences for M U'' + K U = F
L10 return 2 U - U_old + dt^2 (F - K U) / m   ▷ division entry by entry
```

For Lagrange elements the row sum of the element mass is $\int_K \phi_r$, because the basis functions add up to $1$. So row-sum lumping gives each node the integral of its basis function, and all three methods keep the total mass $\sum_i m_i = |\Omega|$ (with density $1$).

**P1 in one dimension.** On a cell of length $h$, $M_K = \frac h6\begin{pmatrix} 2 & 1 \\ 1 & 2\end{pmatrix}$ has row sums $h/2$. On a uniform mesh an interior row of $M$ is $\frac h6(1, 4, 1)$, and the lumped matrix has $h$ on the diagonal, with $h/2$ at the two end nodes. The trapezoidal rule at the nodes gives the same matrix. With the lumped mass, the P1 system $M_L\dot U + KU = 0$ is the standard second-order finite difference scheme $\dot U_j = (U_{j+1} - 2U_j + U_{j-1})/h^2$.

**P1 triangles.** The row sums of $M_K = \frac{|K|}{12}(1 + \delta_{rs})$ are $|K|/3$, the weights of the vertex quadrature rule, which is exact for linear functions.

## Classic examples

**The order is kept for P1.** Take $u_t = u_{xx}$ on $(0, 1)$ with zero boundary values and $u(0) = \sin(\pi x)$, so $u = e^{-\pi^2t}\sin(\pi x)$. On a uniform P1 mesh the nodal values of $\sin(\pi x)$ form an eigenvector of $K$ and of both mass matrices, and the semi-discrete solution decays like $e^{-\lambda_h t}$ with $\theta = \pi h$ and

$$\lambda_{\mathrm{consistent}} = \frac{6(1 - \cos\theta)}{h^2(2 + \cos\theta)}, \qquad \lambda_{\mathrm{lumped}} = \frac{2(1 - \cos\theta)}{h^2}, \qquad \lambda_{\mathrm{average}} = \frac{12(1 - \cos\theta)}{h^2(5 + \cos\theta)} .$$

| $h$ | $\lambda_{\mathrm{lumped}} - \pi^2$ | $\lambda_{\mathrm{consistent}} - \pi^2$ | $\lambda_{\mathrm{average}} - \pi^2$ |
|---|---|---|---|
| 1/8 | -1.262e-01 | 1.275e-01 | -9.839e-04 |
| 1/16 | -3.167e-02 | 3.175e-02 | -6.122e-05 |
| 1/32 | -7.925e-03 | 7.930e-03 | -3.822e-06 |

Both errors fall by a factor 4 per halving of $h$, with opposite signs, since $\lambda_{\mathrm{lumped}} = \pi^2(1 - \theta^2/12 + \cdots)$ and $\lambda_{\mathrm{consistent}} = \pi^2(1 + \theta^2/12 + \cdots)$. This is the one-mode case of the general result in Thomée's Chapter 15: for P1 elements the lumped mass method has the same $O(h^2)$ error in $L^2$ and $O(h)$ in $H^1$ as the standard Galerkin method. The average of the two mass matrices cancels the leading terms and gives $O(h^4)$ for this mode.

**A larger time step for waves.** For the 1D wave equation with central differences, the step is stable for $dt \le 2/\sqrt{\lambda_{\max}}$, where $\lambda_{\max}$ is the largest eigenvalue of $M^{-1}K$. At the highest mode, $\theta = \pi$, the stiffness symbol is $4/h$, the consistent mass symbol is $h/3$ and the lumped one is $h$. So $\lambda_{\max} = 12/h^2$ with the consistent mass and $4/h^2$ with the lumped mass, and the stable steps are $dt \le h/\sqrt3$ and $dt \le h$. Lumping allows a step $\sqrt3$ times larger, the CFL limit of the finite difference scheme.

**Deformable bodies in graphics.** [Corotational FEM](/corotational-fem/) codes give each node a mass equal to a share of the rest area or volume of its cells, which is row-sum lumping for linear elements, and [modal reduction](/modal-reduction/) uses the diagonal mass to turn $Kx = \lambda Mx$ into a standard eigenvalue problem. [Brittle fracture](/brittle-fracture/) codes that split elements at run time also prefer lumped masses, because the mass of new nodes is easy to redistribute.

**Spectral elements.** On $\mathcal{Q}_k$ cells with Gauss-Lobatto-Legendre nodes, the Gauss-Lobatto rule at the nodes gives a diagonal mass with positive weights. The rule is exact for degree $2k - 1$, not $2k$, but the [spectral element method](/spectral-element-method/) keeps its full order, and this is why it uses those nodes. See [Gauss-Lobatto quadrature](/gauss-lobatto-quadrature/).

## Variations

- **Row-sum lumping.** $m_i = \sum_j M_{ij} = \int_\Omega\phi_i$. Simple, keeps the total mass, and fails when some $\int\phi_i \le 0$.
- **Diagonal scaling (HRZ).** Hinton, Rock and Zienkiewicz (1976) take the diagonal of each $M_K$ and scale it so that it adds up to the mass of the cell. The weights are always positive. For P2 triangles they are $|K|/19$ at the vertices and $16|K|/57$ at the edge midpoints, and for P2 tetrahedra $|K|/36$ and $4|K|/27$.
- **Nodal quadrature.** Use a quadrature rule whose points are the nodes. It gives a diagonal mass when the basis is nodal, and it keeps the order when the rule is accurate enough and its weights are positive. For P2 triangles no such rule exists on the six nodes, so the element is enriched: the P2 element plus the cubic bubble $\lambda_1\lambda_2\lambda_3$ has seven nodes, and the rule with weights $|K|/20$ at the vertices, $2|K|/15$ at the midpoints and $9|K|/20$ at the centroid is exact for cubics. Cohen, Joly, Roberts and Tordjman (2001) built such enriched triangles up to higher degree for the wave equation.
- **Average mass.** $\tfrac12(M + M_L)$ is not diagonal, but it reduces the dispersion error of the wave equation from $O(h^2)$ to $O(h^4)$ in 1D, as the table shows.

## Pitfalls

- **Row sums for P2.** On a triangle, the row sum for a vertex is $\int_K\lambda_r(2\lambda_r - 1) = 2\cdot\frac{|K|}6 - \frac{|K|}3 = 0$, and for an edge midpoint it is $\int_K 4\lambda_r\lambda_s = |K|/3$. The lumped matrix is singular. On a tetrahedron the vertex row sum is $2\cdot\frac{|K|}{10} - \frac{|K|}4 = -|K|/20$, a negative mass. Line L8 exists to catch this.
- **Lumping the stiffness.** Only the mass matrix may be lumped. Lumping $K$ destroys consistency, since its rows add up to zero.
- **Lumping where no time step needs it.** For implicit time stepping the solve with $M + dt\,K$ costs the same whether $M$ is lumped or not, and the consistent mass is more accurate for the waves the mesh resolves well.
- **Taking the 1D result as general.** The $\sqrt3$ gain in time step and the exact match with finite differences are 1D facts. In 2D and 3D the gain depends on the element and the mesh, so compute $\lambda_{\max}$ or bound it element by element.

## Exercises

1. Show that for any Lagrange element the row sum of $M_K$ in row $r$ is $\int_K\phi^K_r$. *Answer:* $\sum_s(\phi^K_s, \phi^K_r)_K = (\sum_s\phi^K_s, \phi^K_r)_K = (1, \phi^K_r)_K$.
2. Compute the row sums of the P2 mass matrix on an interval of length $h$, $\frac h{30}\begin{pmatrix} 4 & 2 & -1 \\ 2 & 16 & 2 \\ -1 & 2 & 4\end{pmatrix}$, and compare them with Simpson's rule. *Answer:* $h/6$, $2h/3$, $h/6$, which are Simpson's weights, so in 1D row-sum lumping of P2 works.
3. Check that the seven-point rule with weights $\tfrac1{20}$, $\tfrac2{15}$, $\tfrac9{20}$ (times $|K|$) integrates $\lambda_1\lambda_2\lambda_3$ exactly. *Answer:* only the centroid contributes, $\tfrac9{20}\cdot\tfrac1{27} = \tfrac1{60}$, and the exact value is $\tfrac{1!\,1!\,1!\,2!}{5!} = \tfrac1{60}$.
4. Derive the HRZ weights for the P2 triangle. *Answer:* the diagonal entries are $|K|/30$ at the vertices and $8|K|/45$ at the midpoints, which add up to $19|K|/30$, so the scale factor is $30/19$.

## References
