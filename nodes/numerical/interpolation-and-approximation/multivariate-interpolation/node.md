---
tag: W1XP93
kind: problem
slug: multivariate-interpolation
name: Multivariate interpolation
aliases:
- Multidimensional interpolation
- Interpolation in several variables
area: numerical/interpolation-and-approximation
level: advanced
summary: Interpolate a function of several variables from values at points in R^d. Unlike in one dimension, no fixed space works for all point sets, so either the points or the space must be adapted.
prereqs: [polynomial-interpolation, interpolation-problem]
see_also: [tensor-product-interpolation, scattered-data-interpolation, smolyak-sparse-grids, radial-basis-function-interpolation, bilinear-interpolation, curse-of-dimensionality, kriging, stone-weierstrass-theorem]
sources:
  - book: isbn:9780521843355
    title: Holger Wendland, Scattered Data Approximation, Cambridge University Press, 2005
    locator: Chapter 2, Haar spaces and multivariate polynomials (the Mairhuber-Curtis theorem, dimension counts, unisolvent sets)
  - paper: "Mariano Gasca and Thomas Sauer, Polynomial interpolation in several variables, Advances in Computational Mathematics 12 (2000) 377-410"
    locator: survey of unisolvence, geometric characterizations, Newton and Lagrange forms, and the least interpolant
  - paper: "John C. Mairhuber, On Haar's theorem concerning Chebychev approximation problems having unique solutions, Proceedings of the American Mathematical Society 7 (1956) 609-615"
    locator: no Haar spaces of dimension at least 2 in higher dimensions
  - paper: "K. C. Chung and T. H. Yao, On lattices admitting unique Lagrange interpolations, SIAM Journal on Numerical Analysis 14 (1977) 735-743"
    locator: the geometric characterization condition for unisolvent point sets
  - paper: "Len Bos, Marco Caliari, Stefano De Marchi, Marco Vianello and Yuan Xu, Bivariate Lagrange interpolation at the Padua points: the generating curve approach, Journal of Approximation Theory 143 (2006) 15-25"
    locator: unisolvence of the Padua points for total degree n and the growth of their Lebesgue constant
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Delaunay triangulations (piecewise linear interpolation of terrains)
---

Multivariate interpolation asks for a function of several variables that takes prescribed values at given points of $\mathbb{R}^d$. In one dimension, polynomials of degree $n$ interpolate at any $n + 1$ distinct points. In two or more dimensions no such universal space exists: for any fixed space of functions, some sets of distinct points make the interpolation problem singular. Practical methods therefore either fix the points (grids, sparse grids, special point sets) or let the space depend on the points (piecewise functions on a triangulation, radial basis functions, kriging).

## In plain words

On a line, any set of distinct points can be passed through by a polynomial of the right degree. In the plane this fails: six points on a circle cannot be fitted by a general quadratic surface in a unique way, because the circle's own equation can be added to any solution without changing the values at the points.

So one of two things must give. Either you choose where to measure, for example on a regular grid, and use matching formulas built from one-dimensional pieces, or you accept whatever points you have and build formulas from those points, for example from bumps centered at each one. The cost of the grid approach grows very fast with the number of variables.

## Definition

Notation on the interpolation pages: $\Omega \subseteq \mathbb{R}^d$ is the domain, $x_1, \ldots, x_N \in \Omega$ are distinct points with values $y_i = f(x_i)$; $V$ is an $N$-dimensional space of functions with basis $\varphi_1, \ldots, \varphi_N$; $\mathcal{P}_n^d$ is the space of polynomials in $d$ variables of total degree at most $n$, of dimension $\binom{n + d}{d}$.

**Problem.** Find $s \in V$ with $s(x_i) = y_i$ for $i = 1, \ldots, N$. Writing $s = \sum_j c_j \varphi_j$, this is the linear system $A c = y$ with the generalized Vandermonde matrix $A_{ij} = \varphi_j(x_i)$. The point set is **unisolvent** for $V$ if $A$ is nonsingular, equivalently, if the only $s \in V$ vanishing at all $x_i$ is $s = 0$.

**Haar spaces and the obstruction.** $V$ is a **Haar space** on $\Omega$ if every set of $N$ distinct points in $\Omega$ is unisolvent. On an interval, $\mathcal{P}_n$ is a Haar space. The **Mairhuber-Curtis theorem** (Mairhuber 1956; Curtis 1959) says that if $\Omega \subseteq \mathbb{R}^d$, $d \ge 2$, contains an interior point, then there is no Haar space on $\Omega$ of dimension $N \ge 2$. The reason: two points can be swapped by moving them continuously around each other without collision, which reverses the sign of $\det A$, so $\det A$ vanishes somewhere along the way.

## Variants

- **Gridded data.** Points form a Cartesian product $X_1 \times \cdots \times X_d$; the problem separates into one-dimensional problems ([tensor-product interpolation](/tensor-product-interpolation/), [bilinear](/bilinear-interpolation/) and [bicubic](/bicubic-interpolation/) interpolation).
- **Sparse grids.** Unions of small anisotropic grids, chosen to reduce the number of points ([Smolyak sparse grids](/smolyak-sparse-grids/)).
- **Scattered data.** Points given arbitrarily ([scattered data interpolation](/scattered-data-interpolation/)); the space must depend on the points.
- **Polynomial interpolation of total degree $n$** at $\binom{n+d}{d}$ points, which must be unisolvent; special unisolvent sets with good stability (Padua points in the square, Fekete points).
- **Hermite and Birkhoff data:** derivatives as well as values, as in finite elements and Kergin interpolation.
- **Approximation instead of interpolation:** least squares, smoothing and moving least squares when data are noisy or too many.

## Examples

**Six points on a circle are not unisolvent for quadratics.** $\mathcal{P}_2^2 = \operatorname{span}\{1, x, y, x^2, xy, y^2\}$ has dimension 6. For the points $(1, 0)$, $(0, 1)$, $(-1, 0)$, $(0, -1)$, $(\tfrac35, \tfrac45)$, $(-\tfrac45, \tfrac35)$ on the unit circle, the $6 \times 6$ matrix has determinant exactly 0, because $x^2 + y^2 - 1 \in \mathcal{P}_2^2$ vanishes at all of them. Replacing the last point by $(\tfrac12, \tfrac12)$ gives determinant $0.96$ and a unique interpolant. In general, $N$ points are unisolvent for $\mathcal{P}_n^d$ only if they do not lie on an algebraic hypersurface of degree at most $n$.

**Counting points.** The number of coefficients grows quickly with $d$, much faster for tensor-product degree $n$ in each variable than for total degree $n$:

| $d$ | $n$ | total degree $\binom{n+d}{d}$ | tensor degree $(n + 1)^d$ |
|---|---|---|---|
| 2 | 10 | 66 | 121 |
| 3 | 10 | 286 | 1331 |
| 5 | 6 | 462 | 16807 |
| 10 | 4 | 1001 | 9765625 |

**Tensor-product Chebyshev interpolation in 2D.** On $[-1, 1]^2$, with $n + 1$ Chebyshev points in each direction, maximum errors over 400 random points are:

| function | $n = 10$ | $n = 20$ | $n = 40$ | $n = 80$ |
|---|---|---|---|---|
| $e^{x + 2y} \cos(xy)$ | $3.3 \times 10^{-7}$ | $7.1 \times 10^{-15}$ | $5.3 \times 10^{-15}$ | $5.3 \times 10^{-15}$ |
| $1/(1 + 25(x^2 + y^2))$ | 0.14 | $1.7 \times 10^{-2}$ | $2.9 \times 10^{-4}$ | $1.1 \times 10^{-7}$ |
| $\tanh(10(x + y))$ | 0.33 | $8.9 \times 10^{-2}$ | $3.8 \times 10^{-3}$ | $9.0 \times 10^{-6}$ |

The entire function converges as fast as in one dimension, but every row needs $(n + 1)^2$ samples, and a feature along a diagonal, as in the last row, is not aligned with the grid.

## Known algorithms

- **[Tensor-product interpolation](/tensor-product-interpolation/)** on grids: one-dimensional rules in each direction, $N = (n + 1)^d$ samples; a global rule costs $O(N)$ per evaluation, contracting one coordinate at a time, and a local rule of $p$ points per direction costs $O(p^d)$.
- **[Smolyak sparse grids](/smolyak-sparse-grids/):** combinations of small tensor grids with $O(n (\log n)^{d-1})$ points instead of $n^d$.
- **Piecewise linear on a triangulation:** Delaunay triangulation in $O(N \log N)$ in the plane, then linear interpolation in each triangle; continuous, exact on linear functions.
- **Natural neighbor (Sibson) interpolation** from Voronoi diagrams; $C^1$ away from the data.
- **[Radial basis functions](/radial-basis-function-interpolation/) and [kriging](/kriging/):** $s(x) = \sum_j c_j \phi(\|x - x_j\|)$, nonsingular for positive definite kernels and every point set, with $O(N^3)$ dense setup.
- **[Shepard's method](/shepard-interpolation/):** inverse distance weighting; no linear system, low accuracy.
- **Polynomial methods:** generalized Vandermonde systems at unisolvent sets, the multivariate Newton form on lattices satisfying the Chung-Yao geometric condition, and the de Boor-Ron least interpolant, which always exists and chooses the polynomial space from the points.

## Bounds

- **Lebesgue constants.** For tensor products, the Lebesgue constant is the product of the one-dimensional ones; with Chebyshev points it is $\Lambda_n^d$, about $(\tfrac{2}{\pi} \log n)^d$ ($2.42$, $2.87$, $3.31$ in one dimension for $n = 10, 20, 40$, so $5.9$, $8.2$, $11.0$ in two). For total degree $n$ at the Padua points in the square, the Lebesgue constant grows like $O(\log^2 n)$ (Bos, Caliari, De Marchi, Vianello and Xu).
- **Curse of dimensionality.** For functions with $k$ bounded derivatives in $d$ variables, the best worst-case error of any method using $N$ values is of order $N^{-k/d}$; the number of points for accuracy $\varepsilon$ grows like $\varepsilon^{-d/k}$ ([curse of dimensionality](/curse-of-dimensionality/)). Piecewise linear sparse grids reach $O(N^{-2} (\log N)^{3(d-1)})$ for functions with bounded mixed second derivatives (Bungartz and Griebel 2004).
- **Fill distance.** For scattered data, errors are bounded in terms of the fill distance $h = \sup_{x \in \Omega} \min_i \|x - x_i\|$, for example $O(h^{\tau - d/2})$ in the maximum norm for kernels whose native space is the Sobolev space of order $\tau > d/2$.
- **Existence of approximations.** Multivariate polynomials are dense in $C(K)$ for compact $K$ ([Stone-Weierstrass theorem](/stone-weierstrass-theorem/)); interpolation at badly chosen points need not converge, as in one dimension.

## Reductions

- **To one dimension.** Tensor-product data reduce to repeated one-dimensional interpolation, one coordinate at a time.
- **To linear algebra.** Every linear method is a generalized Vandermonde system $Ac = y$; unisolvence is $\det A \ne 0$.
- **To computational geometry.** Piecewise methods need a triangulation or Voronoi diagram, or nearest neighbor queries in a [k-d tree](/kd-tree/).
- **From one dimension.** The univariate case $d = 1$ is [polynomial interpolation](/polynomial-interpolation/) and its piecewise relatives.

## Applications

- Terrain and geophysical surfaces from survey points; meteorological fields from station data.
- Image and volume resampling, texture lookup and color lookup tables (bilinear, bicubic and trilinear on grids).
- Surrogate models for expensive simulations and response surfaces in design and uncertainty quantification.
- Finite element shape functions and spectral methods on tensor-product domains.
- Lookup tables for physical properties of several variables in engineering codes.

## References
