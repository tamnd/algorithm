---
tag: PAMZX2
kind: algorithm
slug: finite-element-method
name: Finite element method
aliases:
- FEM
- finite element analysis
- P1 finite elements
- Courant elements
area: numerical/differential-equations
level: advanced
summary: "Galerkin method with piecewise polynomial basis functions on a mesh: assemble a sparse stiffness matrix element by element and solve. For P1 and the Poisson problem the H1 error is O(h)."
solves: [poisson-equation, bvp-boundary-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of mesh nodes of a shape-regular quasi-uniform triangulation in 2D", M: "the number of triangles, about 2N", ε: "the relative tolerance of conjugate gradients"}
  time: {worst: "O(N^1.5 log(1/ε))"}
  space: {extra: "Θ(N)"}
  evaluations: {worst: "3M"}
properties: {deterministic: true, conforming: true, symmetric_positive_definite: true, order: "1", h1_order: "1", l2_order: "2"}
history:
  year: 1943
  people: [Richard Courant, M. J. Turner, Ray W. Clough, H. C. Martin, L. J. Topp, Jean Céa]
  note: Courant (1943) used piecewise linear functions on triangles in the Rayleigh-Ritz method; engineers led by Turner, Clough, Martin and Topp (1956) developed element stiffness assembly for aircraft structures, Clough named it in 1960, and the error analysis (Céa 1964, Strang and Fix 1973) followed.
prereqs: [galerkin-method, poisson-equation, sparse-matrix]
see_also: [finite-difference-method, finite-volume-method, spectral-methods, conjugate-gradient-method, multigrid-method, boundary-conditions, collocation-method, method-of-lines]
sources:
  - book: isbn:9780387759333
    title: Susanne C. Brenner and L. Ridgway Scott, The Mathematical Theory of Finite Element Methods, third edition, Springer, 2008
    locator: Chapter 0 (one-dimensional model, Galerkin orthogonality), Chapter 2 (Lax-Milgram theorem, Céa's lemma), Chapter 3 (construction of finite element spaces), Chapter 4 (Bramble-Hilbert lemma, interpolation estimates), Chapter 5 (H1 and L2 error estimates, duality argument)
  - book: isbn:9780898715149
    title: Philippe G. Ciarlet, The Finite Element Method for Elliptic Problems, SIAM Classics in Applied Mathematics 40, 2002
    locator: Chapter 2 (Céa's lemma, triangles of type 1), Chapter 3 (convergence of conforming methods, Aubin-Nitsche lemma)
  - paper: doi:10.1090/S0002-9904-1943-07818-4
    title: R. Courant, Variational methods for the solution of problems of equilibrium and vibrations, Bulletin of the American Mathematical Society 49(1) (1943) 1-23
    locator: the appendix with piecewise linear trial functions on a triangulation
  - paper: doi:10.2514/8.3664
    title: M. J. Turner, R. W. Clough, H. C. Martin and L. J. Topp, Stiffness and deflection analysis of complex structures, Journal of the Aeronautical Sciences 23(9) (1956) 805-823
    locator: element stiffness matrices for triangular plate elements and the direct stiffness assembly
  - paper: doi:10.5802/aif.181
    title: Jean Céa, Approximation variationnelle des problèmes aux limites, Annales de l'Institut Fourier 14(2) (1964) 345-444
    locator: the quasi-optimality estimate now called Céa's lemma
---

The finite element method solves a boundary value problem by writing it in weak form and applying the [Galerkin method](/galerkin-method/) with a basis of piecewise polynomial functions on a mesh, each nonzero only on the few elements around one node. Because of that locality, the stiffness matrix is sparse and can be built element by element: compute a small matrix for each element and add it into the global matrix (assembly). For the [Poisson equation](/poisson-equation/) $-\Delta u = f$ with piecewise linear (P1) elements on triangles, the matrix is symmetric positive definite, and the error is $O(h)$ in the energy norm and $O(h^2)$ in $L^2$ for $u \in H^2$ on a convex polygon. FEM handles curved and irregular domains, local refinement and natural boundary conditions more easily than finite differences.

## In plain words

To find the shape of a stretched membrane, or the temperature in a metal plate, the method cuts the region into many small triangles. On each triangle the unknown is approximated by a flat tilted plane, and the planes join along shared edges into one continuous tent-like surface, fixed by its heights at the corners. Instead of demanding that the equation hold exactly at every point, which no such surface can do, it asks that the equation hold on average against each tent function. That gives one linear equation per corner. Each triangle contributes a small three-by-three piece to these equations, and the pieces are added up into a large but mostly empty system, which a computer solves quickly. Smaller triangles give a better answer, and triangles can be made small only where the answer changes fast.

## The problem

Let $\Omega \subset \mathbb{R}^2$ be a polygon, $f \in L^2(\Omega)$ and $g$ the restriction to $\partial\Omega$ of a function in $H^1(\Omega)$. Find $u$ with $-\Delta u = f$ in $\Omega$ and $u = g$ on $\partial\Omega$. The weak form: find $u \in H^1(\Omega)$ with $u = g$ on $\partial\Omega$ and

$$a(u, v) := \int_\Omega \nabla u \cdot \nabla v \, dx = \int_\Omega f v \, dx =: \ell(v) \quad \text{for all } v \in H^1_0(\Omega).$$

By the Lax-Milgram theorem it has a unique solution. Given a triangulation $\mathcal{T}_h$ of $\Omega$ with nodes $x_1, \ldots, x_N$ and maximum triangle diameter $h$, let $V_h$ be the continuous functions that are linear on each triangle, with the nodal basis $\varphi_i(x_j) = \delta_{ij}$. The P1 finite element solution is $u_h = \sum_j U_j\varphi_j \in V_h$ with $U_j = g(x_j)$ at boundary nodes and $a(u_h, \varphi_i) = \ell(\varphi_i)$ for every interior node $i$. In matrix form $KU = F$ with $K_{ij} = a(\varphi_j, \varphi_i)$ and $F_i = \ell(\varphi_i)$, the latter computed by a quadrature rule. The cost is counted in evaluations of $f$ and in arithmetic operations, with the mesh given.

## The algorithm

On a triangle with vertices $(x_k, y_k)$, $k = 1, 2, 3$, and area $A$, the local basis functions have constant gradients $\nabla\varphi_k = (b_k, c_k)/(2A)$ with $b_1 = y_2 - y_3$, $c_1 = x_3 - x_2$ and cyclic permutations, so the element stiffness matrix is $K^e_{kl} = (b_kb_l + c_kc_l)/(4A)$. The load uses the edge-midpoint rule, exact for quadratic integrands: $F^e_k = \frac{A}{6}\big(f(m_{kl}) + f(m_{km})\big)$, where $m_{kl}, m_{km}$ are the midpoints of the two edges at vertex $k$.

```pseudo id=main
FEM-POISSON(nodes, triangles, boundary, f, g)
L1  K ← sparse N × N zero matrix, F ← zero vector of length N
L2  for each triangle e with vertices v1, v2, v3 do
L3      compute area A and the 3 × 3 element matrix K^e and load F^e
L4      for k, l ← 1 to 3 do K[v_k][v_l] ← K[v_k][v_l] + K^e[k][l]
L5      for k ← 1 to 3 do F[v_k] ← F[v_k] + F^e[k]
L6  for each boundary node v do U[v] ← g(v)
L7  for each interior node i do F[i] ← F[i] − Σ over boundary nodes v of K[i][v] U[v]
L8  solve K_II U_I = F_I by conjugate gradients     ▷ K_II: interior rows and columns
L9  return U
```

Lines L1 to L5 compute $K_{ij} = \sum_e a_e(\varphi_j, \varphi_i)$, since $\varphi_i$ restricted to a triangle is a local basis function there or zero. Lines L6 and L7 impose the Dirichlet condition by moving the known boundary values to the right-hand side. Line L8 solves a symmetric positive definite system; sparse Cholesky or [multigrid](/multigrid-method/) can replace [conjugate gradients](/conjugate-gradient-method/).

## Example

**One interior node.** The unit square split into $2 \times 2$ cells, each cut by its diagonal from lower left to upper right, gives 9 nodes, 8 triangles of area $1/8$, and one interior node $c = (\tfrac12, \tfrac12)$, which belongs to 6 triangles. Take $f = 1$ and $g = 0$. The reference triangle with vertices $(0,0), (h,0), (0,h)$ has

$$K^e = \begin{pmatrix} 1 & -\tfrac12 & -\tfrac12 \\ -\tfrac12 & \tfrac12 & 0 \\ -\tfrac12 & 0 & \tfrac12 \end{pmatrix}$$

for every $h$, since the stiffness matrix of a triangle is invariant under scaling. Adding the contributions of the 6 triangles at $c$ gives the row $K_{cc} = 4$, $-1$ for the four axis neighbours and $0$ for the two diagonal ones: the five-point Laplacian stencil. The load is $F_c = 6 \cdot \frac{1/8}{6}(1 + 1) = \frac14$. So $4U_c = \frac14$ and $U_c = \frac{1}{16} = 0.0625$, computed exactly with fractions by the implementation. The exact value of the solution at the centre is about $0.0737$.

**Convergence.** For $u = \sin\pi x\sin\pi y$ on the unit square with $f = 2\pi^2\sin\pi x\sin\pi y$, uniform $m \times m$ meshes give

| $m$ | max error at nodes | ratio | energy error | ratio | CG iterations |
|---|---|---|---|---|---|
| 4 | 5.181e-2 | | 0.849 | | 2 |
| 8 | 1.288e-2 | 4.02 | 0.433 | 1.96 | 6 |
| 16 | 3.214e-3 | 4.01 | 0.218 | 1.99 | 26 |
| 32 | 8.033e-4 | 4.00 | 0.109 | 2.00 | 56 |
| 64 | 2.008e-4 | 4.00 | 0.0545 | 2.00 | 114 |

The energy error is computed as $\sqrt{|u|_1^2 - U^TKU}$ with $|u|_1^2 = \pi^2/2$, which equals $|u - u_h|_1$ up to the small quadrature error in the load. It halves with $h$ as the theory predicts; the nodal error falls by 4, faster than the general $L^\infty$ bound, a superconvergence effect of this uniform mesh. The CG iteration count doubles with $m$, matching a condition number of order $h^{-2}$. With $f = 0$ and linear boundary data the method reproduces the linear function exactly on any mesh (the patch test), which the tests check exactly with fractions on randomly perturbed meshes.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that assembly produces $K_{ij} = a(\varphi_j, \varphi_i)$, that the reduced matrix $K_{II}$ is symmetric positive definite whenever every connected part of the mesh touches the boundary, so $u_h$ exists and is unique, and Céa's lemma: with exact load, $|u - u_h|_1 = \min_{v \in V_h, v = g \text{ at boundary nodes}} |u - v|_1$, the Galerkin solution is the best approximation in the energy norm. Combined with the interpolation estimate $|u - I_hu|_1 \le Ch|u|_2$ for shape-regular meshes (Brenner and Scott 2008, Chapter 4), this gives $|u - u_h|_1 \le Ch|u|_2$, and the Aubin-Nitsche duality argument gives $\|u - u_h\|_{L^2} \le Ch^2|u|_2$ on convex polygons (Chapter 5). The page proves the first three facts and cites the two estimates.

## Complexity

Assembly costs $\Theta(M)$ operations and $3M$ evaluations of $f$ for $M$ triangles, and the matrix has $O(N)$ nonzeros (7 per row on the structured mesh). On a shape-regular quasi-uniform 2D mesh the condition number of $K_{II}$ is $\Theta(h^{-2}) = \Theta(N)$, so conjugate gradients needs $O(\sqrt N \log(1/\varepsilon))$ iterations of $O(N)$ work each: $O(N^{1.5}\log(1/\varepsilon))$ in total. Sparse Cholesky with nested dissection also costs $O(N^{1.5})$ in 2D, and multigrid or multigrid-preconditioned CG brings the solve to $O(N)$ for a fixed accuracy relative to the discretization error. Memory is $\Theta(N)$.

## Properties

- **Conforming and Galerkin.** $V_h \subset H^1$, so the discrete problem inherits symmetry and coercivity, and the error is quasi-optimal.
- **Energy norm order 1, $L^2$ order 2** for P1 when $u \in H^2$; degree $k$ elements give orders $k$ and $k + 1$ for $u \in H^{k+1}$.
- **Discrete maximum principle** holds for P1 when all angles are at most $\pi/2$ (then off-diagonal entries are $\le 0$), but can fail on obtuse meshes.
- **Natural boundary conditions** (Neumann, Robin) enter the weak form as boundary integrals with no special treatment at nodes.
- **Exact on linear functions** (patch test) on any mesh.

## Variants and improvements

- **Higher-order Lagrange elements** (P2, P3) on triangles and tensor-product elements (Q1, Q2) on quadrilaterals, with isoparametric maps for curved boundaries.
- **Adaptive FEM.** A posteriori error estimators drive local mesh refinement, recovering optimal rates for singular solutions such as those at reentrant corners.
- **hp-FEM.** Combine mesh refinement with increasing degree; exponential convergence for piecewise analytic solutions.
- **Mixed methods** (Raviart-Thomas) for flux variables and saddle-point problems such as Stokes flow; they need the inf-sup condition.
- **Discontinuous Galerkin.** Drops continuity between elements, coupling them by numerical fluxes; well suited to hyperbolic problems and close to [finite volume methods](/finite-volume-method/).
- **Time-dependent problems.** Discretize in space by FEM and in time by an ODE solver: the [method of lines](/method-of-lines/), giving $MU' + KU = F$ with mass matrix $M$.
- **Stabilized methods** (SUPG) for convection-dominated problems, where plain Galerkin oscillates.

## When to use it

Use FEM for elliptic and parabolic problems on complicated geometries, with variable or discontinuous coefficients, with natural boundary conditions, or when local mesh refinement is needed: structural mechanics, heat conduction, electromagnetics, groundwater flow. On a rectangle with smooth data, [finite differences](/finite-difference-method/) are simpler and P1 FEM often gives the same matrix. For smooth solutions on simple domains [spectral methods](/spectral-methods/) converge much faster. For conservation laws with shocks, finite volume methods are more natural.

## Pitfalls

- **Degenerate or badly shaped triangles.** Very small or very large angles inflate the constant in the error bound (large angles) or the condition number (small angles); mesh generators enforce angle bounds.
- **Wrong orientation handling.** With signed areas, clockwise triangles give a negative area; the element matrix must use $|A|$.
- **Inconsistent quadrature.** A load rule that is too crude can lower the order; one-point rules are enough for P1 in $H^1$ but cost accuracy in $L^2$ for rough meshes.
- **Imposing Dirichlet values by overwriting rows only.** Replacing a row by the identity without moving the column contributions to the right-hand side destroys symmetry, so CG may fail.
- **Expecting $O(h^2)$ on nonconvex domains.** At reentrant corners $u \notin H^2$ and uniform refinement gives lower rates; refine toward the corner.
- **Floating Neumann problems.** With pure Neumann data $K$ is singular; fix one value or add the mean-zero constraint.

## Implementations

## History

Courant (1943) proposed piecewise linear trial functions on a triangulation within the Rayleigh-Ritz method for torsion problems. Independently, engineers at Boeing and Berkeley, Turner, Clough, Martin and Topp (1956), built structural analysis on element stiffness matrices assembled into a global system, and Clough coined the name finite element method in 1960. Mathematical analysis followed in the 1960s: Céa (1964) proved quasi-optimality, and the interpolation and duality estimates were systematized by Strang and Fix (1973) and Ciarlet (1978).

## References
