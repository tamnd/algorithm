---
tag: 03WMHA
kind: algorithm
slug: boundary-element-method
name: Boundary element method
aliases:
- BEM
- boundary integral equation method
- boundary integral method
area: scientific-computing/finite-element-practice
level: core
summary: Reformulates a linear PDE as an integral equation on the boundary and discretizes only the boundary, giving a dense system with fewer unknowns.
solves: [poisson-equation]
model: real-ram
complexity:
  vars: {m: the number of boundary elements, p: the number of interior points where the solution is evaluated}
  time: {worst: "Θ(m^3 + p m)"}
  space: {extra: "Θ(m^2)"}
properties: {deterministic: true, iterative: false, dense_system: true, needs_fundamental_solution: true, unknowns_on_boundary_only: true}
history:
  year: 1963
  people: [M. A. Jaswon, G. T. Symm, F. J. Rizzo, C. A. Brebbia]
  note: Jaswon and Symm in 1963 solved potential problems numerically with boundary integral equations. Rizzo in 1967 did the same for elastostatics, and Brebbia's books from 1978 made the name boundary element method common.
prereqs: [poisson-equation, finite-element-method, gauss-legendre-quadrature]
see_also: [fast-multipole-method, gmres, finite-difference-method, extended-finite-element-method, virtual-element-method, patch-test]
sources:
  - paper: doi:10.1098/rspa.1963.0152
    title: M. A. Jaswon, Integral equation methods in potential theory. I, Proceedings of the Royal Society of London A 275(1360) (1963) 23-32
    locator: the boundary integral equations of potential theory with the single and double layer
  - paper: doi:10.1098/rspa.1963.0153
    title: G. T. Symm, Integral equation methods in potential theory. II, Proceedings of the Royal Society of London A 275(1360) (1963) 33-46
    locator: the numerical solution with piecewise constant densities and collocation at boundary points
  - paper: doi:10.1090/qam/99907
    title: F. J. Rizzo, An integral equation approach to boundary value problems of classical elastostatics, Quarterly of Applied Mathematics 25(1) (1967) 83-95
    locator: the direct boundary integral formulation of elastostatics, with the boundary displacements and tractions as unknowns
  - book: isbn:9780387313122
    title: Olaf Steinbach, Numerical Approximation Methods for Elliptic Boundary Value Problems, Finite and Boundary Elements, Springer, 2008
    locator: the representation formula, the boundary integral operators and their mapping properties, the ellipticity of the 2D single layer operator after scaling, and the boundary element methods
  - paper: doi:10.1016/0021-9991(87)90140-9
    title: L. Greengard and V. Rokhlin, A fast algorithm for particle simulations, Journal of Computational Physics 73(2) (1987) 325-348
    locator: the fast multipole method, which applies the dense boundary element matrix in nearly linear time
---

The boundary element method solves a linear partial differential equation with a known fundamental solution, such as the Laplace equation, by working only on the boundary of the domain. Green's identity turns the equation into an integral equation that relates the boundary values $u$ and the normal derivatives $q = \partial u/\partial n$. The method cuts the boundary into $m$ elements, takes $u$ and $q$ as constant (or polynomial) on each, and enforces the integral equation at one point per element (collocation) or in the mean (Galerkin). Where $u$ is given it solves for $q$ and the other way round. The values inside the domain then come from the same integrals. In two dimensions the unknowns are on a curve, so a mesh with $m$ elements does the work of an area mesh with about $m^2$ elements. The price is a dense matrix with weakly singular entries, which costs $\Theta(m^2)$ memory and $\Theta(m^3)$ time for direct elimination unless a fast method such as the [fast multipole method](/fast-multipole-method/) applies it.

## In plain words

To know the temperature everywhere inside a metal plate at rest, it is enough to know the temperature and the heat flow along its edge. A formula, which comes from the way heat spreads from a single point, gives the inside from the edge. The boundary element method uses this formula backwards. On each piece of the edge, either the temperature or the heat flow is known, and the formula, applied at the edge itself, gives one equation per piece for the unknown values. Solving these equations completes the information on the edge. After that, the formula gives the temperature at any inside point you ask for. Only the edge is cut into pieces, never the inside.

## The problem

**Input.** A bounded domain $\Omega \subset \mathbb R^2$ with a polygonal boundary $\Gamma$, traversed counterclockwise, and for each part of $\Gamma$ either the value $u$ (Dirichlet) or the outward normal derivative $q = \partial u/\partial n$ (Neumann). A list of interior points.

**Output.** Approximations of the missing boundary data and of $u$ at the interior points, where $u$ is the solution of $\Delta u = 0$ in $\Omega$ with the given data.

**The integral equation.** With the fundamental solution $G(x, y) = -\frac{1}{2\pi}\ln|x - y|$ of $-\Delta$, Green's second identity gives for $x \in \Omega$

$$u(x) = \int_\Gamma G(x, y)\,q(y)\,ds_y - \int_\Gamma \frac{\partial G}{\partial n_y}(x, y)\,u(y)\,ds_y,$$

and for $x$ at a smooth point of $\Gamma$

$$\tfrac12 u(x) + \int_\Gamma \frac{\partial G}{\partial n_y}(x, y)\,u(y)\,ds_y = \int_\Gamma G(x, y)\,q(y)\,ds_y.$$

The first integral on the right is the single layer, and the integral on the left is the double layer. A nonzero source term $f$ in the [Poisson equation](/poisson-equation/) adds a domain integral of $G f$, or a particular solution can absorb it.

## The algorithm

```pseudo id=main
BEM-LAPLACE-2D(boundary, data)
L1  cut the boundary into m straight elements; x_i = midpoint of element i
L2  for i = 1 to m, for j = 1 to m
L3      G[i, j] <- integral over element j of G(x_i, y) ds_y                 ▷ closed form, weakly singular if i = j
L4      H[i, j] <- integral over element j of dG/dn_y(x_i, y) ds_y + 1/2 [i = j]
L5  in H u = G q, move the columns of the known values to the right side: A z = b
L6  solve A z = b by Gaussian elimination
L7  for each interior point x: u(x) <- sum over j of g_j(x) q_j - h_j(x) u_j
L8  return u and q on the boundary and the interior values
```

**Closed forms for a straight element.** Let the element run from $a$ to $b$ with length $L$, unit tangent $t$ and outward normal $n$. Write $s_0 = (x - a)\cdot t$ and $d = (x - a)\cdot n$. Then

$$\int_0^L \ln\sqrt{(s - s_0)^2 + d^2}\,ds = F(L - s_0) - F(-s_0), \qquad F(w) = \tfrac12 w \ln(w^2 + d^2) - w + d \arctan(w/d),$$

with $F(w) = w\ln|w| - w$ when $d = 0$. The double layer integral is $-\frac{1}{2\pi}$ times the signed angle $\theta_j(x)$ under which the element is seen from $x$, and it is zero when $x$ is on the line of the element. So line L3 is exact also for $i = j$, where it gives $\frac{1}{2\pi}\,L\,(1 - \ln(L/2))$, and the diagonal of line L4 is exactly $\tfrac12$.

**Collocation at midpoints.** The midpoint of a straight element is a smooth point of $\Gamma$, so the factor $\tfrac12$ is right there, also on a polygon with corners. At a corner with interior angle $\phi$ the factor would be $\phi/(2\pi)$.

## Example

**One element per side.** Take the unit square, one element per side in the order bottom, right, top, left, and $u = x$. The midpoints are $(\tfrac12, 0)$, $(1, \tfrac12)$, $(\tfrac12, 1)$ and $(0, \tfrac12)$, so the given values are $u = (\tfrac12, 1, \tfrac12, 0)$. Line L3 gives the diagonal $G_{ii} = (1 + \ln 2)/(2\pi) = 0.269473$, $G = 0.053294$ for two adjacent sides and $G = -0.006186$ for opposite sides. From the midpoint of a side, an adjacent side is seen under the angle $\arctan 2$, and the opposite side under $2\arctan\tfrac12$. So line L4 gives $H_{ii} = \tfrac12$, $H = -\arctan(2)/(2\pi) = -0.176208$ for adjacent sides and $H = -2\arctan(\tfrac12)/(2\pi) = -0.147584$ for opposite sides. Each row of $H$ sums to $\tfrac12 - (2\arctan 2 + 2\arctan\tfrac12)/(2\pi) = 0$.

By symmetry $q$ is zero on the bottom and the top and $q_{\rm left} = -q_{\rm right}$. The row of the right side then reads

$$\tfrac12 \cdot 1 - 0.176208 \cdot \tfrac12 \cdot 2 = (0.269473 + 0.006186)\,q_{\rm right},$$

so $q_{\rm right} = 0.323792/0.275659 = 1.17461$. The exact flux is $1$. The interior value at the centre is exactly $\tfrac12$, by symmetry.

**Convergence on the square.** For $u = e^x \sin y$ with Dirichlet data on all four sides, the error at the centre is $1.6 \times 10^{-4}$, $3.3 \times 10^{-5}$, $7.4 \times 10^{-6}$ and $1.7 \times 10^{-6}$ with 4, 8, 16 and 32 elements per side, which is second order. With $u$ given on the bottom and the top and $q$ on the two other sides, the centre error is $1.6 \times 10^{-4}$ with 16 elements per side, and it also falls at a rate close to 2. On the elements in the middle third of each side, the flux error is below $2 \times 10^{-3}$ with 32 elements per side. On the element next to a corner it stays near $0.24$ for every mesh: the flux jumps at the corner, and constant elements with collocation at the midpoints do not resolve this.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **The boundary integral equation holds for every harmonic $u$ (theorem).** It follows from Green's second identity on $\Omega$ minus a small disc around $x$, with the factor $\tfrac12$ from the half disc at a smooth boundary point.
- **The closed forms of lines L3 and L4 are exact (theorem).** They come from the antiderivative of $\ln r$ along a line and from the angle formula for the double layer.
- **Each row of $H$ sums to zero (theorem).** The angles under which the other elements are seen from a midpoint add up to $\pi$. So a constant $u$ gives $H u = 0$, and if $G$ is nonsingular the computed flux of a constant is exactly zero.
- **Solvability and convergence (cited).** In two dimensions the single layer operator is elliptic on the right space when the diameter of $\Omega$ is less than 1. Then Galerkin boundary elements converge with the optimal rates (Steinbach 2008). For midpoint collocation with constant elements the analysis is more delicate. The second order at interior points above is a measurement.

## Complexity

In the [real-RAM model](/real-ram/), lines L2 to L4 compute $m^2$ entries of two matrices, each in constant time, so $\Theta(m^2)$ time and space. Line L6 is dense Gaussian elimination, $\Theta(m^3)$ time. Line L7 costs $\Theta(m)$ per interior point. In total, $\Theta(m^3 + p m)$ time and $\Theta(m^2)$ extra space. An iterative solver such as [GMRES](/gmres/) with $k$ iterations costs $\Theta(k m^2)$, and with the fast multipole method one matrix vector product costs about $\Theta(m)$ for a fixed accuracy, so large problems are solved in nearly linear time.

## Properties

- **One dimension less.** Only the boundary is meshed. For exterior problems, such as the field around a body in all of space, no truncation of the domain is needed, because $G$ already satisfies the condition at infinity.
- **Dense and not symmetric.** Collocation gives a dense nonsymmetric matrix. Galerkin boundary elements give a symmetric system for the single layer equation, at the price of double integrals.
- **Exact interior representation.** Once $u$ and $q$ are known on $\Gamma$, line L7 gives $u$ and its derivatives at any interior point with no interpolation, and the result is harmonic.
- **Needs a fundamental solution.** The method works for the Laplace, Helmholtz, Stokes and linear elasticity equations with constant coefficients. Variable coefficients and nonlinear terms bring back domain integrals.

## Variants and improvements

- **Galerkin boundary elements.** Test the integral equation with the basis functions. This gives the full stability and convergence theory, symmetric systems for the symmetric formulation, and better accuracy near corners.
- **Higher order elements.** Linear or quadratic $u$ and $q$ on curved elements. At corners, two values of $q$ per node (double nodes) handle the jump of the normal.
- **Indirect method.** Write $u$ as a single or double layer potential of an unknown density, solve for the density, then evaluate. A second kind equation with the double layer is well conditioned.
- **Fast methods.** The fast multipole method, hierarchical matrices and panel clustering apply or compress the dense matrix in nearly linear time and memory.
- **Coupling with finite elements.** Finite elements in a bounded region with nonlinear material and boundary elements for the linear exterior.

## When to use it

Use it for linear problems with constant coefficients on domains whose boundary is much smaller than their volume: exterior acoustics and electromagnetics, potential flow around bodies, electrostatics, and fracture and contact problems where only surface values matter. Use finite elements for nonlinear materials, variable coefficients or when the whole field is needed on a fine grid. For more than a few thousand elements, a fast method is necessary, because the dense matrix grows with $m^2$.

## Pitfalls

- **The 2D single layer at scale 1.** On the unit circle, $\int_\Gamma \ln|x - y|\,ds_y = 0$ for $x$ on $\Gamma$, so the constant density is in the kernel of the single layer and $G$ is nearly singular. In general this happens when the logarithmic capacity of $\Gamma$ is 1. Scale the domain so that its diameter is less than 1. The reference test shows the row sums of $G$ are below $2 \times 10^{-3}$ on the unit circle and about $0.347$ on the circle of radius $\tfrac12$.
- **Near singular integrals.** For interior points close to the boundary, or for thin domains, the kernels vary fast along nearby elements and low order quadrature fails. Use the closed forms or adaptive quadrature.
- **Corners.** The normal jumps at a corner, so $q$ is discontinuous there. Constant elements on each side handle this, but the flux next to a corner converges slowly or not at all in the maximum norm.
- **Orientation.** The sign of the double layer depends on the direction of the normal. A clockwise boundary flips every $H_{ij}$ with $i \ne j$, and the solution is wrong with no error message. The row sum test catches it.
- **Cost of the dense matrix.** With $m = 10^5$ elements the matrix has $10^{10}$ entries. Without a fast method the method is limited to small problems.

## Implementations

## History

Jaswon and Symm in 1963 wrote potential problems as boundary integral equations and solved them on a computer with piecewise constant densities. Rizzo in 1967 did the same for elastostatics with the direct formulation, which uses the boundary values themselves as unknowns. Brebbia in 1978 named it the boundary element method and showed its relation to finite elements. The fast multipole method of Greengard and Rokhlin from 1987 removed the quadratic cost of the dense matrix and made large problems possible.

## References
