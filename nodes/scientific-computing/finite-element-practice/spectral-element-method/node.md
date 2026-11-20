---
tag: 6Q7T79
kind: algorithm
slug: spectral-element-method
name: Spectral element method
aliases:
- SEM
area: scientific-computing/finite-element-practice
level: advanced
summary: Uses high degree tensor product polynomials on quadrilaterals or hexahedra with Gauss-Lobatto nodes, giving a diagonal mass matrix and spectral accuracy.
model: real-ram
complexity:
  vars: {E: the number of elements, N: the polynomial degree}
  time: {average: "Θ(E N^3)"}
  space: {extra: "Θ(E N^2)"}
properties: {deterministic: true, diagonal_mass_matrix: true, spectral_accuracy: true, conforming: true}
history:
  year: 1984
  people: [Anthony T. Patera, Yvon Maday]
  note: Patera introduced the spectral element method for fluid flow in 1984 with Chebyshev points, and the Legendre form with Gauss-Lobatto-Legendre nodes followed with Maday.
prereqs: [finite-element-method, gauss-lobatto-quadrature, lagrange-interpolation]
see_also: [hp-finite-element-method, spectral-methods, legendre-polynomials, mass-lumping, static-condensation, conjugate-gradient-method, barycentric-interpolation, chebyshev-nodes]
sources:
  - paper: doi:10.1016/0021-9991(84)90128-1
    title: "Anthony T. Patera, A spectral element method for fluid dynamics: Laminar flow in a channel expansion, Journal of Computational Physics 54(3) (1984) 468-488"
    locator: the method, with Chebyshev expansions on each element
  - book: isbn:9780521453097
    title: Michel O. Deville, Paul F. Fischer and Ernest H. Mund, High-Order Methods for Incompressible Fluid Flow, Cambridge University Press (2002)
    locator: the Legendre spectral element method, the GLL quadrature, the diagonal mass and the tensor product operators
  - book: isbn:9780198528692
    title: George Em Karniadakis and Spencer J. Sherwin, Spectral/hp Element Methods for Computational Fluid Dynamics, 2nd edition, Oxford University Press (2005)
    locator: nodal and modal bases, sum factorization and the cost of high order operators
---

The spectral element method (SEM) is a finite element method of high degree. The domain is cut into a few large quadrilaterals or hexahedra, and on each one the solution is a tensor product polynomial of degree $N$ in each direction, stored by its values at the Gauss-Lobatto-Legendre (GLL) nodes. All integrals use the GLL quadrature on the same nodes. This one choice has three effects. The mass matrix is diagonal, so explicit time stepping needs no linear solve. The stiffness matrix is exact in 1D and the operators factor into small 1D matrices on tensor product elements. And for smooth solutions the error falls exponentially in $N$, which is called spectral accuracy. The method was made for fluid dynamics, and codes such as Nek5000 use it for turbulent flow, acoustics and seismic waves.

## In plain words

Cut the domain into a few big pieces. On each piece, use one polynomial of high degree, and store it by its values at special points that crowd toward the ends of the piece. The same points are used to compute all the integrals. Because the points and the integration rule match, the mass matrix has only diagonal entries, which makes time steps cheap. Because the degree is high, a smooth solution is very accurate with few unknowns: each extra degree removes a fixed fraction of the error. In 2D and 3D the polynomial on a square or a cube is a product of 1D ones, so all the work reduces to small 1D matrix operations.

## The problem

**Input.** The 1D model problem $-u'' + cu = f$ on $(a, b)$ with $u(a) = u(b) = 0$ and $c \ge 0$, a mesh $a = x_0 < x_1 < \cdots < x_E = b$ of $E$ elements, and a degree $N \ge 1$.

**Output.** The values of the discrete solution $u_N$ at all GLL nodes of all elements. Between the nodes, $u_N$ is the Lagrange interpolant on each element.

## The algorithm

```pseudo id=main
SEM-1D(mesh, N, f, c)
L1  (xi, w) <- GLL nodes and weights of degree N on [-1, 1]; D <- the derivative matrix, D_ij = l_j'(xi_i)
L2  for each element e of length h do
L3      K_e <- (2 / h) D^T diag(w) D; M_e <- (h / 2) diag(w); F_e <- (h / 2) w * f(x_e)    ▷ the mass is diagonal
L4      add K_e + c M_e to A and F_e to F, sharing the end node with the neighbor
L5  solve A U = F on the interior nodes                  ▷ U = 0 at a and b
L6  return U
```

The GLL nodes are $-1$, $1$ and the roots of $P_N'$, where $P_N$ is the [Legendre polynomial](/legendre-polynomials/) of degree $N$. The weights are $w_j = 2/(N(N+1)P_N(\xi_j)^2)$. The code finds the nodes with a Newton type iteration started at the Chebyshev-Lobatto points, and it builds $D$ from the barycentric weights.

**Tensor products.** On a square element of degree $N$, the nodes are the pairs $(\xi_i, \xi_j)$, the mass is $\operatorname{diag}(w)\otimes\operatorname{diag}(w)$, and the stiffness for $-\Delta$ on the reference square is $\hat K\otimes\hat M + \hat M\otimes\hat K$ with the 1D matrices $\hat K = D^{\mathsf T}\operatorname{diag}(w)D$ and $\hat M = \operatorname{diag}(w)$. Applying such an operator to a vector by 1D matrix products, called sum factorization, costs $O(N^{d+1})$ per element in $d$ dimensions, not the $O(N^{2d})$ of a stored element matrix. So large SEM codes never form the global matrix. They use the [conjugate gradient method](/conjugate-gradient-method/) with matrix-free products.

## Example

**By hand.** Take one element $[0, 1]$, $N = 2$, $c = 0$ and $f = 1$, so $u = x(1 - x)/2$. The GLL nodes are $-1, 0, 1$ with weights $\tfrac13, \tfrac43, \tfrac13$, and
$$D = \begin{pmatrix} -\tfrac32 & 2 & -\tfrac12 \\ -\tfrac12 & 0 & \tfrac12 \\ \tfrac12 & -2 & \tfrac32 \end{pmatrix}.$$
With $h = 1$, the only interior node is $x = \tfrac12$. Its stiffness entry is $2\sum_q w_qD_{q1}^2 = 2(\tfrac13\cdot4 + \tfrac43\cdot0 + \tfrac13\cdot4) = \tfrac{16}{3}$, and its load is $\tfrac12\cdot\tfrac43\cdot1 = \tfrac23$. So $U = \tfrac{2/3}{16/3} = \tfrac18 = u(\tfrac12)$. The answer is exact, because $u$ is a quadratic. The diagonal mass entry at that node would be $\tfrac12\cdot\tfrac43 = \tfrac23$.

**Measured.** For $-u'' + u = f$ on $(0, 1)$ with $u = e^x\sin(\pi x)$, the reference code gives these maximum errors over 98 points.

| Elements $E$ | Degree $N$ | Unknowns | Max error |
|---|---|---|---|
| 1 | 4 | 3 | $1.6 \times 10^{-2}$ |
| 1 | 8 | 7 | $1.1 \times 10^{-6}$ |
| 1 | 12 | 11 | $4.5 \times 10^{-11}$ |
| 1 | 14 | 13 | $2.0 \times 10^{-13}$ |
| 2 | 8 | 15 | $5.4 \times 10^{-9}$ |
| 4 | 2 | 7 | $6.3 \times 10^{-3}$ |
| 8 | 2 | 15 | $8.0 \times 10^{-4}$ |
| 16 | 2 | 31 | $1.0 \times 10^{-4}$ |
| 32 | 2 | 63 | $1.2 \times 10^{-5}$ |

At a fixed degree $N = 2$ the error falls like $h^3 = h^{N+1}$, a factor of 8 per halving. At a fixed mesh, each increase of $N$ by 4 removes 4 to 5 digits. With 13 unknowns the error is near roundoff, while $N = 2$ needs 63 unknowns for $10^{-5}$.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). The GLL rule with $N + 1$ nodes is exact for polynomials of degree $2N - 1$: split a polynomial as a multiple of $(1 - x^2)P_N'$ plus a remainder of degree $N$, and the first part integrates to 0 by the orthogonality of $P_N$. The stiffness integrand $\ell_i'\ell_j'$ has degree $2N - 2$, so line L3 gives the exact stiffness. The mass integrand $\ell_i\ell_j$ has degree $2N$, one too many, and the rule gives $w_i\delta_{ij}$, which is the row sum of the exact mass matrix. The assembled matrix is symmetric positive definite, so line L5 has one solution, and it is the Galerkin solution with the mass and the load integrated by the GLL rule. Strang's lemma then bounds the error by the best approximation and the quadrature errors, which decay exponentially in $N$ for analytic data.

## Complexity

The 1D code forms the element matrices in $O(N^3)$ each and solves the global system densely, which is fine for the small sizes in the tests. A banded solve of the global 1D system costs $\Theta(EN^3)$, since the bandwidth is $N$, and that is the bound in the front matter. The memory for the element matrices is $\Theta(EN^2)$. In $d$ dimensions, one matrix-free operator application costs $\Theta(EN^{d+1})$ by sum factorization, and the diagonal mass makes an explicit time step cost the same.

## Properties

- **Diagonal mass.** The GLL mass matrix is diagonal with positive entries, and it equals the row sum [mass lumping](/mass-lumping/) of the exact mass matrix.
- **Spectral accuracy.** For analytic solutions on a fixed mesh, the error decays like $\rho^{-N}$ with $\rho > 1$. For a solution in $H^s$, the error in $H^1$ decays like $N^{1-s}$, with no upper limit on the rate.
- **Exact 1D stiffness.** The rule integrates $\ell_i'\ell_j'$ exactly. In 2D the factor $\hat M$ in $\hat K\otimes\hat M$ is the diagonal GLL mass, so the 2D stiffness is not exact, but the error is of the same size as the quadrature error in the mass.
- **Low dissipation and dispersion.** For wave problems, the phase error of high degree elements is much smaller than for low order elements at the same number of unknowns per wavelength.
- **Conforming.** The basis is continuous across elements, so the method is a conforming Galerkin method up to the quadrature.

## Variants and improvements

- **Chebyshev spectral elements.** Patera's original method used Chebyshev points and expansions on each element. The Legendre form is now standard because the GLL rule gives the diagonal mass and a symmetric system.
- **Modal bases.** The [hp finite element method](/hp-finite-element-method/) often uses integrated Legendre polynomials instead of nodal values. They span the same space and allow a different degree on each element.
- **Static condensation.** The interior nodes of each element can be removed by [static condensation](/static-condensation/), which leaves a system on the element boundaries only.
- **Spectral element in time domain for waves.** In seismology the method with explicit time stepping is the standard for global wave propagation, because the diagonal mass makes each step cheap.
- **Discontinuous variants.** Discontinuous Galerkin spectral element methods use the same nodes but allow jumps between elements, with fluxes at the faces.
- **Triangles and tetrahedra.** Tensor product structure is lost on simplices. Special node sets and collapsed coordinate bases extend the method, at a higher cost.

## When to use it

Use the spectral element method for problems with smooth solutions where high accuracy matters per unknown: incompressible and turbulent flow, acoustics, and seismic waves. The diagonal mass makes it a natural choice for explicit time stepping, and the tensor product structure makes it fast on modern hardware. Use global [spectral methods](/spectral-methods/) instead on simple periodic or box domains, and use low order finite elements or hp refinement when the solution has singularities or the geometry needs many small elements.

## Pitfalls

- **Under integration of the mass.** The diagonal mass comes from a rule that is not exact for $\ell_i\ell_j$. This is part of the method and does not reduce the spectral rate, but it means the mass is not the exact $L^2$ product.
- **Aliasing in nonlinear terms.** Products like $u\,\partial_xu$ integrated on the GLL nodes create aliasing errors that can make a flow simulation unstable. Codes use over-integration or filtering.
- **Conditioning.** The condition number of the stiffness matrix grows like $N^3$ in 1D on a fixed mesh for this nodal basis. Iterative solvers need preconditioners made for high degree.
- **Singularities.** A corner singularity limits the rate to algebraic, as for every polynomial method. Grade the mesh toward the singularity, as in hp-FEM.
- **Node computation.** For large $N$, compute the GLL nodes and weights with a stable iteration, not by finding the roots of a polynomial given by its coefficients.
- **Curved elements.** On a curved element the Jacobian is not constant, the integrands are not polynomials, and the GLL rule is no longer exact for the stiffness. The method still converges, but the exactness claims do not hold.

## Implementations

## History

Anthony Patera introduced the spectral element method in 1984 for the incompressible Navier-Stokes equations, combining the geometric flexibility of finite elements with the accuracy of spectral methods. His first version used Chebyshev expansions. With Yvon Maday he developed the Legendre version with GLL nodes and its error analysis in the late 1980s, and Paul Fischer and others built the parallel code that became Nek5000. In the 1990s Dimitri Komatitsch and Jean-Pierre Vilotte brought the method to seismology, where it is now the standard for global wave propagation.

## References
