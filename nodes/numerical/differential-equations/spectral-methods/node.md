---
tag: MAFVSH
kind: technique
slug: spectral-methods
name: Spectral methods
aliases:
- pseudospectral methods
- spectral collocation
- Fourier spectral method
- Chebyshev spectral method
area: numerical/differential-equations
level: advanced
summary: "Approximate the solution by a global expansion in smooth basis functions, such as Fourier modes or Chebyshev polynomials. For smooth solutions the error decays faster than any power of N."
prereqs: [trigonometric-interpolation, chebyshev-interpolation, finite-differences, method-of-lines]
see_also: [fast-fourier-transform, chebyshev-nodes, galerkin-method, finite-element-method, gibbs-phenomenon, aliasing, poisson-equation, heat-equation]
sources:
  - book: isbn:9780898714654
    title: Lloyd N. Trefethen, Spectral Methods in MATLAB, SIAM, 2000
    locator: Chapter 1 (differentiation matrices), Chapter 3 (periodic grids, DFT and FFT), Chapter 4 (smoothness and spectral accuracy), Chapter 6 (Chebyshev differentiation matrices), Chapter 7 (boundary value problems), Chapter 10 (time-stepping and stability regions)
  - book: isbn:9780486411835
    title: John P. Boyd, Chebyshev and Fourier Spectral Methods, second edition, Dover, 2001
    locator: Chapter 2 (convergence of spectral series), Chapter 3 (Galerkin and collocation), Chapter 11 (aliasing and the 2/3 rule)
  - book: isbn:9783540307259
    title: Claudio Canuto, M. Yousuff Hussaini, Alfio Quarteroni and Thomas A. Zang, Spectral Methods, Fundamentals in Single Domains, Springer, 2006
    locator: Chapter 2 (polynomial approximation, Fourier, Chebyshev and Legendre), Chapter 3 (Galerkin, collocation and tau methods), Chapter 5 (approximation theory and error estimates)
  - book: isbn:9780898710236
    title: David Gottlieb and Steven A. Orszag, Numerical Analysis of Spectral Methods, Theory and Applications, SIAM, 1977
    locator: Chapters 3 and 4 (Galerkin, tau and collocation methods), Chapter 8 (stability)
  - paper: "Steven A. Orszag, On the elimination of aliasing in finite-difference schemes by filtering high-wavenumber components, Journal of the Atmospheric Sciences 28 (1971) 1074"
    locator: the 2/3 rule for dealiasing quadratic nonlinearities
---

Spectral methods approximate the solution of a differential equation by a finite expansion $u_N(x) = \sum_{k} \hat u_k \phi_k(x)$ in global, infinitely smooth basis functions: Fourier modes $e^{ikx}$ for periodic problems and Chebyshev or Legendre polynomials on an interval. The equation is imposed by Galerkin projection, by the tau method, or by collocation at $N + 1$ grid points (the pseudospectral method). Each basis function spans the whole domain, so derivatives at a point use all the data. In exchange, for smooth solutions the error decreases faster than any power of $1/N$, and geometrically for analytic solutions. Twenty to forty points per dimension then reach accuracy that finite differences need thousands of points for. The cost is dense matrices or FFTs, and a strong demand for smoothness and simple geometry.

## In plain words

A finite difference method estimates a slope from a few neighbouring values, like drawing a short straight line through three points. A spectral method fits one smooth curve through all the points at once and differentiates that curve.

If the true solution is smooth, the single global curve is an extremely good fit, and doubling the number of points can multiply the number of correct digits rather than add a fixed amount. The price is that every point talks to every other point, so the matrices are full, and that any jump or corner in the solution spoils the fit everywhere with ripples. Spectral methods are the tool of choice for smooth problems on simple shapes, such as boxes, discs and spheres.

## When it applies

- **The solution is smooth.** Spectral accuracy needs many derivatives; for analytic solutions the error decays like $e^{-cN}$. With a discontinuity in $u$ or a low derivative, convergence drops to an algebraic rate and Gibbs oscillations appear.
- **The geometry is simple.** A periodic interval or box (Fourier), an interval or tensor-product box (Chebyshev, Legendre), a disc or sphere (Fourier in angle with Chebyshev in radius, or spherical harmonics). Complicated geometries need spectral element methods.
- **The coefficients are smooth.** Constant coefficients give diagonal operators in Fourier space; smooth variable coefficients and polynomial nonlinearities are handled by collocation (products in physical space).
- **The problem is linear or mildly nonlinear in a few variables.** Typical uses are turbulence simulations in periodic boxes, weather and climate models on the sphere, eigenvalue problems, and stability analysis.

## The template

Collocation (pseudospectral) form for a linear problem $\mathcal L u = g$ with boundary conditions, or $u_t = \mathcal L u + \mathcal N(u)$ by the [method of lines](/method-of-lines/):

```pseudo id=main
SPECTRAL-COLLOCATION(L, g, N)
L1  choose a basis and its grid: x_j = 2πj/N (Fourier) or x_j = cos(πj/N), j = 0..N (Chebyshev)
L2  build the differentiation matrix D with (D v)_j = p'(x_j), p the interpolant of v
L3  replace each derivative in L by a power of D and each coefficient a(x) by diag(a(x_j))
L4  replace the rows of boundary points by the boundary conditions (or remove them)
L5  solve the dense system L_N v = g(x_j)       ▷ or integrate v' = L_N v + N(v) in time
L6  interpolate v by p for values between grid points
```

For Fourier grids, line L2 is applied without forming $D$: transform with the [FFT](/fast-fourier-transform/), multiply the coefficient of $e^{ikx}$ by $ik$ (and the mode $k = N/2$ by 0 for even $N$), and transform back, in $\Theta(N\log N)$. The Chebyshev matrix has the closed form $D_{ij} = \frac{c_i}{c_j}\frac{(-1)^{i+j}}{x_i - x_j}$ for $i \ne j$ with $c_0 = c_N = 2$ and $c_j = 1$ otherwise, and the diagonal is best set to minus the row sum (Trefethen, Chapter 6).

**Error theory (proved in the cited books).** For trigonometric interpolation on $N$ points:

- if $u$ is $2\pi$-periodic and analytic in the strip $|\operatorname{Im} x| < a$, then the spectral derivative has error $O(e^{-a'N})$ for every $a' < a$;
- if $u$ has $m - 1$ continuous derivatives and an $m$-th derivative of bounded variation, the error of the $\nu$-th spectral derivative is $O(N^{\nu - m})$.

For Chebyshev interpolation, analyticity in the Bernstein ellipse with parameter $\rho > 1$ gives $O(\rho^{-N})$. (Trefethen, Chapter 4 and Chapter 5; Canuto et al., Chapter 5.)

## Classic examples

**Fourier differentiation.** For $u(x) = e^{\sin x}$ on $N$ equispaced points in $[0, 2\pi)$, the maximum error of the spectral derivative and of the second-order central difference are (observed):

| $N$ | spectral | central difference | spectral, $u = \lvert\sin x\rvert^3$ |
|---|---|---|---|
| 8 | 4.3e-3 | 3.4e-1 | 6.1e-2 |
| 16 | 1.8e-7 | 9.4e-2 | 1.7e-2 |
| 24 | 9.6e-13 | 4.5e-2 | 7.7e-3 |
| 32 | 3.1e-14 | 2.6e-2 | 4.4e-3 |

The spectral error for the entire function $e^{\sin x}$ falls geometrically to rounding level at $N = 32$, while the difference error falls by 4 per doubling. For $|\sin x|^3$, whose third derivative jumps, the spectral error falls only like $N^{-2}$, as the theory predicts with $m = 3$, $\nu = 1$.

**Chebyshev collocation for a boundary value problem.** Solve $u'' = e^{4x}$ on $[-1, 1]$, $u(\pm1) = 0$, with exact solution $u = (e^{4x} - x\sinh 4 - \cosh 4)/16$ (Trefethen, Chapter 7). Square the Chebyshev matrix, strike the boundary rows and columns, and solve. The maximum errors at the grid points are $1.0 \times 10^{-1}$, $2.2 \times 10^{-4}$, $1.1 \times 10^{-7}$, $1.9 \times 10^{-11}$ and $1.1 \times 10^{-14}$ for $N = 4, 8, 12, 16, 20$. The second-order three-point difference scheme with $M = 128$ intervals still has error $6.8 \times 10^{-4}$ (all observed).

**Heat and Poisson equations on periodic domains.** For $u_t = u_{xx}$ with periodic data, the Fourier Galerkin method decouples into $\hat u_k' = -k^2\hat u_k$, solved exactly. The [Poisson equation](/poisson-equation/) $-\Delta u = f$ on a periodic box is solved by dividing each Fourier coefficient by $|k|^2$, in $\Theta(N^d\log N)$ for $N^d$ points.

**Navier-Stokes turbulence.** Direct numerical simulation of isotropic turbulence in a periodic box (Orszag and Patterson 1972) uses Fourier collocation with the 2/3 dealiasing rule and an explicit or semi-implicit time stepper; it remains a standard tool.

## Variations

- **Galerkin, tau and collocation.** Galerkin projects the residual onto the basis; tau replaces the highest-mode equations by the boundary conditions; collocation makes the residual vanish at grid points. Collocation is simplest for variable coefficients and nonlinear terms.
- **Bases.** Fourier for periodic problems; Chebyshev (FFT-friendly, clustered nodes); Legendre (natural for Galerkin, orthogonal in the plain $L^2$ inner product); Hermite and Laguerre or mapped Chebyshev for unbounded domains; spherical harmonics on the sphere.
- **Spectral element and hp finite element methods** split the domain into elements, each with a high-degree polynomial, which combines geometric flexibility with spectral convergence inside elements.
- **Sparse spectral methods** (ultraspherical method of Olver and Townsend) use different bases for the solution and the residual, so that the matrices become banded and well conditioned.
- **Adaptive degree**: Chebfun chooses $N$ automatically by watching the decay of the Chebyshev coefficients.

## Pitfalls

- **Gibbs phenomenon.** A jump in $u$ gives oscillations of about 9 percent of the jump next to it and only $O(1/N)$ convergence away from it; shocks need filtering, shock capturing or other methods.
- **Aliasing.** Products of two resolved functions contain modes beyond the grid, which fold back onto low modes and can cause nonlinear instability. Padding to $3N/2$ points, or zeroing the top third of the modes (the 2/3 rule), removes aliasing for quadratic terms.
- **Time step restrictions.** The Chebyshev second-derivative matrix with Dirichlet conditions has largest eigenvalue about $-0.048N^4$ (observed: $-0.0484N^4$ at $N = 16$, $-0.0476N^4$ at $N = 32$), because the nodes cluster with spacing $O(N^{-2})$ near the ends. Explicit time stepping of the heat equation then needs $\Delta t = O(N^{-4})$, and of advection $\Delta t = O(N^{-2})$; implicit or semi-implicit schemes are used instead.
- **Conditioning and rounding.** Chebyshev differentiation matrices have norms of order $N^2$ per derivative, so rounding errors grow like $N^2\varepsilon$ in first derivatives; compute the diagonal as the negative row sum.
- **Dense linear algebra.** Collocation matrices are full: $\Theta(N^3)$ to solve in one dimension and far more in several, unless fast transforms, sparse bases or iterative solvers with good preconditioners are used.
- **Wrong basis for the boundary.** Fourier series for a nonperiodic function converge slowly because of the jump at the ends of the period.

## Exercises

1. Show that the Fourier spectral derivative of $\sin(mx)$ on $N$ points is exact for $|m| < N/2$, and find what it returns for $m = N/2$.
2. Build the Chebyshev matrix for $N = 2$ and check that it differentiates $1$, $x$ and $x^2$ exactly at the nodes $1, 0, -1$.
3. Solve $u'' - 4u = 0$, $u(-1) = 0$, $u(1) = 1$ by Chebyshev collocation and plot the error against $N$ on a log scale. Estimate the geometric rate.
4. Apply the Fourier derivative to the square wave $\operatorname{sgn}(\sin x)$ and measure the overshoot as $N$ grows.

## References
