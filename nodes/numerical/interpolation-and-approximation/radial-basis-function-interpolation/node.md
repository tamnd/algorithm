---
tag: QJTKQ6
kind: algorithm
slug: radial-basis-function-interpolation
name: Radial basis function interpolation
aliases:
- RBF interpolation
- Radial basis function method
- Kernel interpolation
area: numerical/interpolation-and-approximation
level: advanced
summary: Interpolant is a sum of radially symmetric kernels centred at the data points, plus a low-degree polynomial. It works on scattered points in any dimension and is uniquely solvable for usual kernels.
solves: [scattered-data-interpolation]
model: real-ram
complexity:
  vars: {N: the number of data points, d: the dimension, M: the number of tail polynomials}
  time: {setup: Θ(N^3 + N^2 d), evaluate: Θ(N d + M)}
  space: {extra: Θ(N^2)}
  flops: {setup: "(2/3) N^3 + 3 N^2 d"}
properties: {deterministic: true, recursive: false, interpolates: true, unique_for_standard_kernels: true, works_in_any_dimension: true, reproduces_tail_polynomials: true, dense_linear_system: true}
history:
  year: 1971
  people: [Rolland Hardy, Jean Duchon, Charles Micchelli]
  note: Hardy introduced multiquadrics for topography in 1971; Duchon's thin-plate splines (1976) gave the variational theory, and Micchelli (1986) proved unique solvability for the standard kernels.
prereqs: [scattered-data-interpolation, gaussian-elimination]
see_also: [kriging, shepard-interpolation, cubic-spline-interpolation, smoothing-spline, multivariate-interpolation, curse-of-dimensionality, kd-tree, polynomial-interpolation]
sources:
  - book: isbn:9780521843355
    title: Holger Wendland, Scattered Data Approximation, Cambridge University Press, 2005
    locator: Chapter 6, Positive definite functions; Chapter 8, Conditionally positive definite functions; Chapter 10, Native spaces; Chapter 11, Error estimates for radial basis function interpolation; Chapter 12, Stability
  - book: isbn:9789812706348
    title: Gregory E. Fasshauer, Meshfree Approximation Methods with MATLAB, World Scientific, 2007
    locator: the chapters on RBF interpolation with polynomial reproduction, the choice of shape parameter and the trade-off between accuracy and conditioning
  - paper: "Rolland L. Hardy, Multiquadric equations of topography and other irregular surfaces, Journal of Geophysical Research 76 (1971) 1905-1915"
    locator: the multiquadric interpolant
  - paper: "Charles A. Micchelli, Interpolation of scattered data, distance matrices and conditionally positive definite functions, Constructive Approximation 2 (1986) 11-22"
    locator: nonsingularity of the interpolation matrices for multiquadrics, distance matrices and conditionally positive definite kernels
  - paper: "Jean Duchon, Splines minimizing rotation-invariant semi-norms in Sobolev spaces, in Constructive Theory of Functions of Several Variables, Lecture Notes in Mathematics 571, Springer (1977) 85-100"
    locator: thin-plate and polyharmonic splines as minimizers of a bending energy
  - paper: "Richard Franke, Scattered data interpolation, tests of some methods, Mathematics of Computation 38 (1982) 181-200"
    locator: the comparison in which multiquadrics and thin-plate splines were the most accurate methods
---

Radial basis function (RBF) interpolation fits scattered data in any number of dimensions with a sum of translates of a single radial function, one centered at each data point, usually plus a low-degree polynomial. The coefficients solve one linear system. For the standard kernels (Gaussians, multiquadrics, thin-plate splines, odd powers) the system is uniquely solvable for every set of distinct points, which sidesteps the obstruction that no fixed polynomial space works for scattered points in two or more dimensions. Smooth kernels give very high accuracy, but the system then becomes badly conditioned, and its dense $N \times N$ matrix limits the method to moderate $N$ without special fast algorithms.

## In plain words

Put a smooth bump, or a bowl, at every data point. All the bumps have the same shape and depend only on distance from their center, so the method works the same way in any direction and any dimension. Then choose how tall each bump is so that their total passes exactly through every data value. That choice is one system of equations, with one unknown per data point.

For the usual bump shapes, this system always has exactly one solution, however the points are scattered. Wide, smooth bumps give very accurate results but make the system hard to solve precisely. Narrow bumps are easy to solve for but less accurate.

## The problem

Notation on the interpolation pages: distinct data sites $x_1, \ldots, x_N \in \mathbb{R}^d$ with values $y_i = f(x_i)$; $\phi : [0, \infty) \to \mathbb{R}$ is the radial function with shape parameter $\varepsilon > 0$ where it applies; $p_1, \ldots, p_M$ is a basis of the polynomials of total degree at most $m - 1$ on $\mathbb{R}^d$ ($M = 0$ if $m = 0$); $h$ is the fill distance, the largest distance from a point of the domain to the nearest site.

**The interpolant.**
$$s(x) = \sum_{j=1}^{N} c_j\, \phi(\|x - x_j\|) + \sum_{k=1}^{M} d_k\, p_k(x), \qquad s(x_i) = y_i, \qquad \sum_{j=1}^{N} c_j\, p_k(x_j) = 0 \ (k = 1, \ldots, M).$$
In matrix form, with $A_{ij} = \phi(\|x_i - x_j\|)$ and $P_{ik} = p_k(x_i)$,
$$\begin{pmatrix} A & P \\ P^{T} & 0 \end{pmatrix} \begin{pmatrix} c \\ d \end{pmatrix} = \begin{pmatrix} y \\ 0 \end{pmatrix}.$$

**Standard kernels** and the tail degree $m - 1$ that guarantees unique solvability:

| kernel | $\phi(r)$ | order $m$ | tail |
|---|---|---|---|
| Gaussian | $e^{-(\varepsilon r)^2}$ | 0 | none |
| inverse multiquadric | $(1 + (\varepsilon r)^2)^{-1/2}$ | 0 | none |
| multiquadric (Hardy) | $(1 + (\varepsilon r)^2)^{1/2}$ | 1 | constant |
| linear | $r$ | 1 | constant |
| thin-plate spline | $r^2 \log r$ | 2 | linear |
| cubic | $r^3$ | 2 | linear |

## The algorithm

```pseudo id=main
RBF-FIT(x_1..x_N, y_1..y_N, φ, tail degree m − 1)
L1  A[i][j] ← φ(‖x_i − x_j‖) for i, j = 1..N
L2  P[i][k] ← p_k(x_i) for i = 1..N, k = 1..M
L3  solve [[A, P], [Pᵀ, 0]] · [c; d] = [y; 0]
L4  return (c, d)
RBF-EVAL(c, d, x)
L5  return Σ_j c_j φ(‖x − x_j‖) + Σ_k d_k p_k(x)
```

The implementation solves line L3 by Gaussian elimination with partial pivoting. For positive definite kernels without a tail, Cholesky factorization of $A$ is the natural choice; with a tail, one can eliminate the polynomial part first by a QR factorization of $P$ and solve a positive definite system on its null space.

## Example

**One dimension, linear kernel, by hand.** Sites $0, 1, 3$ with values $0, 1, 0$ and $\phi(r) = r$ with a constant tail. A function $\sum_j c_j |x - x_j| + d$ is a broken line whose slope jumps by $2c_j$ at $x_j$, and the side condition $\sum c_j = 0$ makes it constant outside $[0, 3]$. The slopes through the data are $0, 1, -\tfrac12, 0$, so the jumps give $c = (\tfrac12, -\tfrac34, \tfrac14)$; then $s(0) = d = 0$ and
$$s(x) = \tfrac12 |x| - \tfrac34 |x - 1| + \tfrac14 |x - 3|,$$
the [piecewise linear interpolant](/piecewise-linear-interpolation/). In the same way, $r^3$ with a linear tail gives exactly the natural [cubic spline](/cubic-spline-interpolation/) in one dimension; the tests check both identities in exact arithmetic.

**Franke's function on $[0, 1]^2$.** With $N$ Halton points and errors on a $30 \times 30$ grid in $[0.05, 0.95]^2$:

| $N$ | thin-plate | multiquadric, $\varepsilon = 3$ | Gaussian, $\varepsilon = 6$ | Gaussian, $\varepsilon = 3$ | Shepard, $p = 2$ |
|---|---|---|---|---|---|
| 25 | 0.35 | 0.28 | 0.50 | 0.18 | 0.37 |
| 100 | $1.8 \times 10^{-2}$ | $1.7 \times 10^{-2}$ | $3.9 \times 10^{-2}$ | 0.29 | 0.31 |
| 400 | $4.2 \times 10^{-3}$ | $1.0 \times 10^{-5}$ | $1.2 \times 10^{-4}$ | 0.16 | 0.22 |

The thin-plate spline converges at an algebraic rate, the multiquadric and the Gaussian with $\varepsilon = 6$ much faster. The Gaussian with $\varepsilon = 3$ fails: its largest coefficient is $2.2 \times 10^{6}$ at $N = 100$ and $6.7 \times 10^{12}$ at $N = 400$, and rounding errors swamp the result.

**The shape parameter and conditioning.** For $1/(x - 1.05)$ at 21 equispaced points in $[-1, 1]$ with multiquadrics, the residual at the nodes after solving the system in double precision, and the largest coefficient, are:

| $\varepsilon$ | 0.5 | 1 | 2 | 5 | 10 |
|---|---|---|---|---|---|
| residual | $3.6 \times 10^{-2}$ | $9.1 \times 10^{-6}$ | $1.1 \times 10^{-10}$ | $4.7 \times 10^{-13}$ | $1.4 \times 10^{-13}$ |
| $\max_j \lvert c_j \rvert$ | $8.4 \times 10^{13}$ | $1.4 \times 10^{10}$ | $2.1 \times 10^{5}$ | 280 | 28 |

## Correctness

If the system in line L3 is nonsingular, its solution satisfies $s(x_i) = y_i$ by the first block of rows, and line L5 evaluates $s$. Nonsingularity holds for distinct sites when $\phi$ is conditionally positive definite of order $m$ and the sites are unisolvent for polynomials of degree $m - 1$: if $Ac + Pd = 0$ and $P^T c = 0$, then $c^T A c = -c^T P d = 0$, which forces $c = 0$, and then $Pd = 0$ forces $d = 0$. The Gaussian and inverse multiquadric are positive definite by Bochner's theorem, the others conditionally positive definite (Micchelli 1986). Polynomials of degree $m - 1$ are reproduced exactly. The full argument is in the correctness proof below.

## Complexity

- **Setup:** forming $A$ costs $\Theta(N^2 d)$ and the dense solve $\tfrac23 N^3$ flops by LU ($\tfrac13 N^3$ by Cholesky for positive definite kernels); storage $\Theta(N^2)$.
- **Evaluation:** $\Theta(N d)$ per point.
- **Fast methods:** compactly supported kernels (Wendland functions) give sparse matrices; fast multipole and hierarchical matrix methods evaluate and solve for polyharmonic kernels in about $O(N \log N)$; partition of unity and domain decomposition methods combine many small local RBF fits.

## Properties

- **Unique solvability** for every set of distinct sites (with unisolvent sites for the tail), in every dimension: the space depends on the sites, so the Mairhuber-Curtis obstruction does not apply.
- **Polynomial reproduction** of the tail degree, exactly.
- **Optimality (proved).** The interpolant has the least native-space norm among all interpolants. For thin-plate splines in 2D this norm is the bending energy $\int (f_{xx}^2 + 2 f_{xy}^2 + f_{yy}^2)$ (Duchon), and for $r^3$ in 1D it is $\int (f'')^2$, the natural spline property.
- **Error bounds (proved).** For $f$ in the native space, $|f(x) - s(x)| \le P(x) \|f\|_{\mathcal{N}}$ with the power function $P$. For kernels whose native space is the Sobolev space $H^\tau$, $\tau > d/2$, this gives $O(h^{\tau - d/2})$; for thin-plate splines in 2D, $O(h)$ for functions in the native space; for Gaussians and multiquadrics, spectral rates $O(e^{-c |\log h| / h})$ and $O(e^{-c/h})$ for very smooth $f$ (Madych and Nelson).
- **Trade-off (proved).** Better error bounds go with smaller eigenvalues of $A$, hence worse conditioning (Schaback's uncertainty principle, 1995). The tables above show it.
- **Flat limit (observed and proved in cases).** As $\varepsilon \to 0$, smooth RBF interpolants often converge to a polynomial interpolant, in one dimension to the Lagrange polynomial (Driscoll and Fornberg 2002), although the system becomes singular in the limit.

## Variants and improvements

- **Stable bases for small $\varepsilon$:** Contour-Padé, RBF-QR and RBF-GA (Fornberg and coauthors) compute the same interpolant through a better-conditioned basis.
- **Compactly supported kernels** (Wendland 1995): piecewise polynomial $\phi$ with support radius $\delta$, sparse $A$, positive definite in a fixed dimension.
- **Smoothing:** solve $(A + \lambda I) c + Pd = y$ for noisy data ([smoothing spline](/smoothing-spline/) in the thin-plate case); this is also [kriging](/kriging/) with a nugget.
- **RBF-generated finite differences (RBF-FD):** local RBF stencils for derivatives on scattered nodes, used for PDEs on irregular domains and the sphere.
- **Greedy and multilevel methods:** choose centers adaptively, or fit residuals on finer levels with narrower kernels.
- **Shape parameter selection:** leave-one-out cross-validation (Rippa's formula costs one factorization), or maximum likelihood when the kernel is a covariance.

## When to use it

Use RBF interpolation for scattered data in two or more dimensions when accuracy matters and $N$ is up to a few thousand for dense solvers: surface reconstruction, geophysical and meteorological fields, mesh deformation, surrogate models of expensive computations, and meshfree PDE methods. Prefer thin-plate or cubic kernels when you want no shape parameter and robust conditioning; Gaussians and multiquadrics when $f$ is smooth and you can choose $\varepsilon$ with care. For gridded data use [tensor-product](/tensor-product-interpolation/) methods; for very large $N$ use local or fast methods.

## Pitfalls

- **Ill-conditioning.** Small $\varepsilon$ or dense points make $A$ nearly singular; the coefficients become huge, as in the tables above. Watch the coefficient size and the residual, or use a stable basis.
- **Shape parameter by eye.** The best $\varepsilon$ depends on $f$ and $N$; a fixed $\varepsilon$ that works for 100 points may fail for 400. Use cross-validation.
- **Missing tail.** Thin-plate, cubic and multiquadric kernels need the polynomial tail and the side conditions to be well posed; without them, systems for multiquadrics are still nonsingular but the thin-plate system can be singular.
- **Degenerate sites for the tail.** Collinear sites in 2D are not unisolvent for linear polynomials, so the thin-plate system is singular; the implementation reports it.
- **Repeated sites** make $A$ singular; merge them or use smoothing.
- **Overshoot.** Near jumps the interpolant oscillates and leaves the data range, unlike [Shepard's method](/shepard-interpolation/).
- **Cost growth.** $N^3$ setup and $N^2$ storage limit dense solvers to about $10^4$ points.
- **Edge effects.** Errors are largest near the boundary of the convex hull of the sites, and extrapolation is unreliable.

## Implementations

## History

Hardy (1971) introduced multiquadrics to fit topographic surfaces from scattered survey points. Duchon (1976, 1977) derived thin-plate and polyharmonic splines from a variational principle, extending the natural cubic spline to several variables, and Meinguet developed their numerical use. Franke's 1982 comparison of scattered data methods found multiquadrics and thin-plate splines the most accurate, which drew wide attention. Micchelli (1986) proved that the interpolation matrices are nonsingular for distinct points, using Schoenberg's theory of positive definite and completely monotone functions (1938). Madych and Nelson, Wu and Schaback, and others built the error theory in the early 1990s, and Wendland (1995) introduced compactly supported kernels.

## References
