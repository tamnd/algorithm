---
tag: 9WA3CF
kind: problem
slug: poisson-equation
name: Poisson equation
aliases:
- Laplace equation
- Poisson problem
- Dirichlet problem for the Laplacian
area: numerical/differential-equations
level: intro
summary: "The elliptic PDE -Δu = f with boundary data; the Laplace equation when f = 0. The 5-point scheme has error O(Δx^2), and multigrid solves it in time linear in the unknowns."
model: real-ram
prereqs: [pde-classification, boundary-conditions, finite-differences]
see_also: [heat-equation, finite-difference-method, finite-element-method, multigrid-method, sparse-linear-systems, discrete-sine-transform, sturm-liouville-problem, spectral-methods]
sources:
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 2 (the one-dimensional problem, Green's function, stability and convergence), Chapter 3 (the 5-point Laplacian, its accuracy and stability), Chapter 4 (Jacobi, Gauss-Seidel, SOR, conjugate gradients and multigrid on this problem)
  - book: isbn:9780821849743
    title: Lawrence C. Evans, Partial Differential Equations, second edition, American Mathematical Society, 2010
    locator: Section 2.2 (Laplace's equation, maximum principle, Green's function), Section 6.2 (weak solutions by the Lax-Milgram theorem)
  - book: isbn:9780521607933
    title: K. W. Morton and D. F. Mayers, Numerical Solution of Partial Differential Equations, second edition, Cambridge University Press, 2005
    locator: Chapter 6 (linear second-order elliptic equations, the discrete maximum principle and the error bound by a comparison function)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 12 (elliptic equations and difference schemes), Chapter 13 (linear iterative methods)
  - paper: doi:10.1137/0710032
    title: Alan George, Nested dissection of a regular finite element mesh, SIAM Journal on Numerical Analysis 10(2) (1973) 345-363
    locator: the O(N^(3/2)) operation count and O(N log N) fill for a regular two-dimensional mesh
---

The Poisson equation is the elliptic [partial differential equation](/pde-classification/) $-\Delta u = f$ on a domain $\Omega$, with [boundary conditions](/boundary-conditions/) on $\partial\Omega$. With $f = 0$ it is the Laplace equation. It describes steady states: the temperature in a body with heat sources, the electric potential of a charge density, the pressure in an incompressible flow. It is the model problem of numerical analysis for elliptic equations, and the standard test for [sparse linear solvers](/sparse-linear-systems/).

## In plain words

Think of a thin metal plate. Its edge is held at known temperatures, and some places inside are heated. After a long time the temperature stops changing. At that moment the temperature at each point is the average of the temperatures around it, plus a small extra amount where heat is put in. The Poisson equation states this balance.

To compute the answer, put a grid on the plate. Write one equation for each grid point: its value equals the average of its four neighbours, plus the local source. This gives one large set of linear equations, one unknown for each point. Most of the work is to solve this set quickly. Simple sweeps that replace each value by the average of its neighbours converge, but slowly on a fine grid. Better solvers use the fast Fourier transform or a hierarchy of grids.

## Definition

**Notation.** $\Omega \subset \mathbb{R}^m$ is a bounded open domain, $\Delta u = \sum_{i=1}^m \partial^2 u / \partial x_i^2$ is the Laplacian, and $f$ is a given function on $\Omega$. On a grid we write $\Delta x$ for the mesh width, $x_j = j \Delta x$, and $U_{ij} \approx u(x_i, y_j)$. Errors are measured in the max norm $\|e\|_\infty = \max_{ij} |e_{ij}|$ over the grid points.

**The Dirichlet problem.** Given $f$ on $\Omega$ and $g$ on $\partial\Omega$, find $u$ with

$$-\Delta u = f \quad \text{in } \Omega, \qquad u = g \quad \text{on } \partial\Omega.$$

**The Neumann problem.** Replace the boundary condition by $\partial u / \partial n = g$, the outward normal derivative. By the divergence theorem $\int_\Omega f \, dx = -\int_\Omega \Delta u \, dx = -\int_{\partial\Omega} g \, dS$. So the Neumann problem has a solution only when $\int_\Omega f\,dx + \int_{\partial\Omega} g\,dS = 0$, and then the solution is unique only up to an additive constant.

**Uniqueness for the Dirichlet problem.** Let $u_1$ and $u_2$ be two solutions in $C^2(\Omega) \cap C^1(\bar\Omega)$ and $w = u_1 - u_2$. Then $-\Delta w = 0$ in $\Omega$ and $w = 0$ on $\partial\Omega$. Green's first identity gives $\int_\Omega |\nabla w|^2 dx = -\int_\Omega w \Delta w \, dx + \int_{\partial\Omega} w\, \partial w / \partial n \, dS = 0$. So $\nabla w = 0$, $w$ is constant on each component of $\Omega$, and the boundary value makes it $0$. $\square$

**Maximum principle.** If $\Delta u \ge 0$ in a bounded domain and $u \in C^2(\Omega) \cap C(\bar\Omega)$, then $\max_{\bar\Omega} u = \max_{\partial\Omega} u$ (Evans, Section 2.2). For the Laplace equation both the maximum and the minimum are on the boundary, so a harmonic function with boundary values in $[a, b]$ takes values in $[a, b]$.

**Weak form and existence.** Multiply by a test function $v$ that vanishes on $\partial\Omega$ and integrate by parts: $\int_\Omega \nabla u \cdot \nabla v \, dx = \int_\Omega f v \, dx$. For $f \in L^2(\Omega)$ and $g = 0$, the Lax-Milgram theorem gives exactly one $u \in H^1_0(\Omega)$ that satisfies this for each $v \in H^1_0(\Omega)$ (Evans, Section 6.2). This form is the base of the [finite element method](/finite-element-method/) and the [Galerkin method](/galerkin-method/).

**One dimension.** On $(0, 1)$ the problem $-u'' = f$, $u(0) = u(1) = 0$ has the solution $u(x) = \int_0^1 G(x, s) f(s)\, ds$ with the Green's function $G(x, s) = s(1 - x)$ for $s \le x$ and $G(x, s) = x(1 - s)$ for $s \ge x$. Since $G \ge 0$ and $\int_0^1 G(x, s)\, ds = x(1 - x)/2 \le 1/8$, the solution satisfies $\|u\|_\infty \le \|f\|_\infty / 8$.

**The 5-point scheme.** On the unit square with $\Delta x = 1/M$, replace $-\Delta u$ at each interior point by

$$-\Delta_h U_{ij} = \frac{4 U_{ij} - U_{i-1,j} - U_{i+1,j} - U_{i,j-1} - U_{i,j+1}}{\Delta x^2} = f_{ij}, \qquad 1 \le i, j \le M - 1,$$

with $U = g$ at the boundary points. This is a linear system with $N = (M - 1)^2$ unknowns, a symmetric positive definite matrix and at most 5 nonzeros in each row. By Taylor's theorem the truncation error $\tau_{ij} = -\Delta_h u(x_i, y_j) - f_{ij}$ satisfies $|\tau_{ij}| \le \frac{\Delta x^2}{12}(M_{xxxx} + M_{yyyy})$, where $M_{xxxx} = \max |\partial_x^4 u|$ and $M_{yyyy} = \max |\partial_y^4 u|$, when $u \in C^4(\bar\Omega)$.

**Discrete maximum principle and the error bound.** If $-\Delta_h V \le 0$ at each interior point, then $V$ takes its maximum at a boundary point: at an interior maximum, $V_{ij}$ is at most the mean of its four neighbours, so all four are equal to the maximum, and the argument repeats until it reaches the boundary. Let $e = u - U$ on the grid. Then $-\Delta_h e = \tau$ and $e = 0$ on the boundary. Put $\varphi(x, y) = ((x - \frac12)^2 + (y - \frac12)^2)/4$. The scheme is exact on quadratics, so $\Delta_h \varphi = 1$, and $0 \le \varphi \le \frac18$ on the square. The grid function $V = e + \|\tau\|_\infty \varphi$ has $-\Delta_h V = \tau - \|\tau\|_\infty \le 0$, so $e \le V \le \|\tau\|_\infty / 8$. The same argument for $-e$ gives

$$\|u - U\|_\infty \le \frac{\|\tau\|_\infty}{8} \le \frac{\Delta x^2}{96}\,(M_{xxxx} + M_{yyyy}).$$

This is a proved, non-asymptotic bound (Morton and Mayers, Chapter 6). It needs $u \in C^4$. With corners or rough $f$ the solution is less smooth and the observed order is lower.

**The computational task.** Given $\Omega$, $f$, $g$ and a mesh, compute $U$ and report the error in a stated norm. The cost is the time to set up and solve the linear system.

## Variants

- **Variable coefficients.** $-\nabla \cdot (a(x) \nabla u) = f$ with $a(x) \ge a_0 > 0$. The 5-point scheme becomes a weighted average with the same sparsity.
- **Helmholtz and screened Poisson equations.** $-\Delta u + c u = f$. For $c > 0$ the problem stays positive definite. For $c = -k^2 < 0$ it is indefinite and much harder to solve iteratively.
- **Robin and mixed conditions.** $a u + b\, \partial u / \partial n = g$, or Dirichlet data on one part of the boundary and Neumann data on the rest.
- **Periodic problem.** On a torus, the problem has a solution only when $\int f = 0$, and [spectral methods](/spectral-methods/) solve it exactly for trigonometric data.
- **Poisson eigenproblem.** $-\Delta u = \lambda u$ with $u = 0$ on the boundary. In one dimension this is the simplest [Sturm-Liouville problem](/sturm-liouville-problem/).
- **Ill-posed non-example.** The Cauchy problem $u_{xx} + u_{yy} = 0$, $u(x, 0) = 0$, $u_y(x, 0) = \sin(kx)/k$ has the solution $u = \sin(kx) \sinh(ky)/k^2$. The data tend to $0$ as $k \to \infty$, but $u(x, 1)$ grows like $e^k/k^2$. Elliptic equations need data on the whole boundary, not initial data on part of it (Hadamard's example).

## Examples

**One dimension.** Take $-u'' = \pi^2 \sin(\pi x)$ on $(0, 1)$, $u(0) = u(1) = 0$, with the solution $u = \sin(\pi x)$. With $M = 4$ the three unknowns solve a tridiagonal system, and $U = (0.744604, 1.053029, 0.744604)$ against $u = (0.707107, 1, 0.707107)$. The max errors for $M = 4, 8, 16, 32, 64$ are $5.303 \cdot 10^{-2}$, $1.295 \cdot 10^{-2}$, $3.219 \cdot 10^{-3}$, $8.036 \cdot 10^{-4}$ and $2.008 \cdot 10^{-4}$. Each halving of $\Delta x$ divides the error by about 4, so the order is 2. The bound $\pi^4 \Delta x^2 / 96$ gives $6.342 \cdot 10^{-2}$ for $M = 4$ and $2.477 \cdot 10^{-4}$ for $M = 64$, which is about 25 % above the true error.

**Two dimensions.** Take $u = \sin(\pi x)\sin(\pi y)$ on the unit square, so $f = 2\pi^2 u$ and $g = 0$. The grid function $\sin(\pi x_i)\sin(\pi y_j)$ is an eigenvector of $-\Delta_h$ with the eigenvalue $\lambda_h = \frac{8}{\Delta x^2} \sin^2 \frac{\pi \Delta x}{2}$. So the discrete solution is $U_{ij} = c\, u(x_i, y_j)$ with $c = 2\pi^2 / \lambda_h$, and the max error is $|c - 1|$. For $M = 4$, $c = 1.053029$. For $M = 4, 8, 16, 32$ the errors are $5.303 \cdot 10^{-2}$, $1.295 \cdot 10^{-2}$, $3.219 \cdot 10^{-3}$, $8.036 \cdot 10^{-4}$, the same as in one dimension, because $c$ depends only on the one-dimensional ratio.

**A polynomial solution.** For $f = 1$ in one dimension the solution is $u = x(1 - x)/2$. Its fourth derivative is $0$, so $\tau = 0$ and the scheme gives $u$ exactly at the grid points, for every $M$.

**Iterative solvers on the model problem.** For the 5-point scheme on the unit square the [Jacobi method](/jacobi-method/) has the spectral radius $\cos(\pi \Delta x)$, [Gauss-Seidel](/gauss-seidel-method/) has $\cos^2(\pi \Delta x)$, and [SOR](/successive-over-relaxation/) with the optimal $\omega = 2/(1 + \sin \pi\Delta x)$ has $\omega - 1$ (LeVeque, Chapter 4). To reduce the error by $10^{-6}$ with $M = 32$ ($N = 961$ unknowns), Jacobi needs 2863 sweeps, Gauss-Seidel 1432 and optimal SOR ($\omega = 1.8215$) 71. With $M = 64$ ($N = 3969$) the counts are 11463, 5732 and 141: Jacobi and Gauss-Seidel grow like $\Delta x^{-2}$, and SOR like $\Delta x^{-1}$.

## Known algorithms

Costs are for the 5-point scheme in two dimensions with $N = (M - 1)^2$ unknowns, in the [real RAM](/real-ram/) model.

| method | time | note |
|---|---|---|
| banded [Cholesky](/cholesky-decomposition/) | $O(N^2)$ | bandwidth $M$ in the natural order, storage $O(N^{3/2})$ |
| [nested dissection](/nested-dissection/) | $O(N^{3/2})$ | fill $O(N \log N)$; George (1973) |
| Jacobi, Gauss-Seidel | $O(N^2 \log(1/\varepsilon))$ | $O(\Delta x^{-2})$ sweeps of cost $O(N)$ |
| optimal SOR | $O(N^{3/2} \log(1/\varepsilon))$ | $O(\Delta x^{-1})$ sweeps |
| [conjugate gradients](/conjugate-gradient-method/) | $O(N^{3/2} \log(1/\varepsilon))$ | condition number $\cot^2(\pi \Delta x / 2) \approx 4/(\pi^2 \Delta x^2)$ |
| fast Poisson solver ([discrete sine transform](/discrete-sine-transform/)) | $O(N \log N)$ | rectangle, constant coefficients |
| full [multigrid](/multigrid-method/) | $O(N)$ | to the level of the discretization error |

The fast Poisson solver diagonalizes $-\Delta_h$: its eigenvectors are the products of sine vectors, with eigenvalues $\frac{4}{\Delta x^2}\left(\sin^2 \frac{p\pi\Delta x}{2} + \sin^2\frac{q\pi\Delta x}{2}\right)$, $1 \le p, q \le M - 1$. A sine transform in each direction, a division by the eigenvalues, and an inverse transform solve the system. [Finite element](/finite-element-method/) methods handle curved boundaries. [Spectral methods](/spectral-methods/) give exponential accuracy for smooth data on simple domains.

## Bounds

- **Accuracy.** The 5-point scheme has $\|u - U\|_\infty \le \frac{\Delta x^2}{96}(M_{xxxx} + M_{yyyy})$ on the unit square when $u \in C^4$ (proved above). The 9-point scheme reaches order 4 when $f$ is replaced by a corrected right-hand side (LeVeque, Section 3.5).
- **Conditioning.** The 2-norm condition number of $-\Delta_h$ is $\cot^2(\pi\Delta x/2)$, which grows like $\Delta x^{-2}$. The matrix is ill conditioned, but the solution is not sensitive in the max norm: the discrete maximum principle gives $\|U\|_\infty \le \frac18 \|f\|_\infty$ for zero boundary data.
- **A lower bound.** Each of the $N$ unknowns depends on $f$ at every grid point, and the output has $N$ numbers, so any method needs $\Omega(N)$ time. Multigrid is optimal up to a constant factor.

## Reductions

- **To a sparse linear system.** The discretization gives a symmetric positive definite system with 5 nonzeros in each row. Every [sparse linear system](/sparse-linear-systems/) method applies.
- **From the heat equation.** The steady state of the [heat equation](/heat-equation/) $u_t = \Delta u + f$ solves the Poisson equation. Jacobi's method is forward Euler on the semi-discrete heat equation with the largest stable time step.
- **From implicit time steps.** Each step of [backward Euler](/backward-euler-method/) or [Crank-Nicolson](/crank-nicolson-method/) for the heat equation solves a screened Poisson problem $(I - \Delta t\, \Delta_h) U^{n+1} = \ldots$.
- **To the eigenproblem.** Separation of variables reduces the Poisson problem on a rectangle to the eigenfunctions of $-d^2/dx^2$, the sine functions.

## Applications

- **Electrostatics and gravity.** The potential of a charge or mass density $\rho$ solves $-\Delta \phi = \rho / \varepsilon_0$ or $\Delta \phi = 4\pi G \rho$.
- **Incompressible flow.** Projection methods for the [Navier-Stokes equations](/navier-stokes-equations/) solve a Poisson equation for the pressure in each time step. This is often the most expensive part of the solver.
- **Steady heat conduction and diffusion.** Temperature with sources, concentration of a diffusing species at equilibrium.
- **Image processing.** Poisson image editing and gradient-domain methods find the image whose gradient is closest to a given field, which is a Poisson equation.
- **Mesh generation.** Elliptic grid generators solve Laplace equations for the grid coordinates, which gives smooth meshes by the maximum principle.

## References
