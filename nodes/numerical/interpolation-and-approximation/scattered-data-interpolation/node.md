---
tag: WBSRZE
kind: problem
slug: scattered-data-interpolation
name: Scattered data interpolation
aliases:
- Scattered data approximation
- Meshfree interpolation
- Interpolation of irregularly spaced data
area: numerical/interpolation-and-approximation
level: advanced
summary: Interpolate values at arbitrary, unstructured points with no grid. The space of interpolants must depend on the points, which leads to triangulations, distance weights, kernels and kriging.
prereqs: [multivariate-interpolation]
see_also: [radial-basis-function-interpolation, shepard-interpolation, kriging, nearest-neighbor-interpolation, voronoi-diagram, kd-tree, smoothing-spline, curse-of-dimensionality]
sources:
  - book: isbn:9780521843355
    title: Holger Wendland, Scattered Data Approximation, Cambridge University Press, 2005
    locator: Chapter 1, Applications and motivations; Chapter 2, Haar spaces and multivariate polynomials; Chapters 4 (moving least squares), 11 (error estimates) and 12 (stability), for fill and separation distances
  - book: isbn:9789812706348
    title: Gregory E. Fasshauer, Meshfree Approximation Methods with MATLAB, World Scientific, 2007
    locator: the introductory chapters on scattered data interpolation and the comparison of RBF, Shepard and moving least squares methods
  - paper: "Richard Franke, Scattered data interpolation, tests of some methods, Mathematics of Computation 38 (1982) 181-200"
    locator: the test functions (including Franke's function) and the comparison of 29 methods
  - paper: "Robin Sibson, A brief description of natural neighbour interpolation, in Interpreting Multivariate Data, Wiley (1981) 21-36"
    locator: natural neighbour coordinates from the Voronoi diagram
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Delaunay triangulations (height interpolation of terrains), and Chapter 7, Voronoi diagrams
---

Scattered data interpolation asks for a function of several variables that takes given values at points with no structure: survey stations, sensor locations, samples of a simulation. Because no fixed space of functions interpolates on every point set in two or more dimensions, every method builds its approximating space from the points themselves, by triangulating them, by weighting by distance, or by placing a kernel at each point. The methods differ widely in accuracy, smoothness, cost and robustness.

## In plain words

Imagine weather stations spread unevenly over a country, each reporting a temperature, and you need a temperature map. There is no grid to lean on, so the map must be built from the station positions themselves.

You can split the country into triangles with stations at the corners and tilt a flat sheet over each triangle. You can average the stations with more weight on near ones. Or you can put a smooth bump at each station and adjust the bump heights so the map passes through every reading. The last option is usually the most accurate and the most expensive.

## Definition

Notation on the interpolation pages: $\Omega \subset \mathbb{R}^d$ is a bounded domain; $X = \{x_1, \ldots, x_N\} \subset \Omega$ are distinct sites with values $y_i = f(x_i)$. The **fill distance** is $h = \sup_{x \in \Omega} \min_i \|x - x_i\|$, the radius of the largest ball in $\Omega$ with no site; the **separation distance** is $q = \tfrac12 \min_{i \ne j} \|x_i - x_j\|$; the sites are **quasi-uniform** when $h / q$ stays bounded as $N$ grows.

**Problem.** Given $X$ and $y$, find a function $s : \Omega \to \mathbb{R}$, from a class chosen with $X$, with $s(x_i) = y_i$ for $i = 1, \ldots, N$, and make $\|f - s\|$ small for $f$ in a given smoothness class.

**Why the space must depend on the sites.** For any fixed $N$-dimensional space of continuous functions on a domain in $\mathbb{R}^d$ with $d \ge 2$, some set of $N$ distinct sites makes the interpolation matrix singular (Mairhuber-Curtis theorem; see [multivariate interpolation](/multivariate-interpolation/)). So polynomial interpolation of fixed degree cannot be the general method.

## Variants

- **Approximation instead of interpolation.** Noisy data call for smoothing: [smoothing splines](/smoothing-spline/), regularized kernels, least squares or moving least squares.
- **Hermite data** (values and gradients) and **vector fields** (divergence-free kernels).
- **Data on manifolds:** the sphere (geodesy, climate), surfaces in $\mathbb{R}^3$.
- **Very large $N$** ($10^6$ and more, from lidar and point clouds): local and hierarchical methods only.
- **Implicit surface reconstruction:** fit a function that is zero on a point cloud and nonzero off it, then extract its zero set.
- **Statistical setting:** treat $f$ as a random field and predict it ([kriging](/kriging/)), with error estimates.

## Examples

**Comparison on Franke's function.** On $[0, 1]^2$ with $N$ Halton points, maximum errors on a $30 \times 30$ grid in $[0.05, 0.95]^2$:

| $N$ | fill distance $h$ | nearest neighbor | Shepard $p = 2$ | local Shepard | thin-plate RBF | multiquadric, $\varepsilon = 3$ |
|---|---|---|---|---|---|---|
| 25 | 0.21 | 0.38 | 0.38 | 0.30 | 0.35 | 0.28 |
| 100 | 0.097 | 0.25 | 0.31 | 0.16 | $1.8 \times 10^{-2}$ | $1.7 \times 10^{-2}$ |
| 400 | 0.049 | 0.15 | 0.22 | $5.3 \times 10^{-2}$ | $4.2 \times 10^{-3}$ | $1.0 \times 10^{-5}$ |

([Nearest neighbor](/nearest-neighbor-interpolation/) and Shepard values are first-order or worse; the thin-plate spline is about second order on this range; the multiquadric converges much faster but needs a well-chosen shape parameter.) The fill distance roughly halves when $N$ quadruples, as $h \approx N^{-1/2}$ in two dimensions; the separation distance shrinks faster for Halton points ($q = 0.060, 0.020, 0.0073$), so the matrices of kernel methods become worse conditioned.

**A singular polynomial problem.** Six sites on a circle cannot be interpolated uniquely by quadratics in two variables, because $x^2 + y^2 - 1$ vanishes at all of them. A thin-plate spline through the same six sites with any data exists and is unique.

## Known algorithms

- **[Nearest neighbor interpolation](/nearest-neighbor-interpolation/):** piecewise constant on Voronoi cells, $O(\log N)$ per query with a [k-d tree](/kd-tree/); discontinuous, first order.
- **Triangulation methods:** build the Delaunay triangulation ($O(N \log N)$ in the plane), then interpolate linearly on each triangle (continuous, second order, exact on linear functions), or with Clough-Tocher or Powell-Sabin macro elements for $C^1$ surfaces.
- **Natural neighbor interpolation** (Sibson 1981): weights from areas stolen from Voronoi cells; $C^1$ except at the sites, exact on linear functions, local.
- **[Shepard's method](/shepard-interpolation/)** and the modified local quadratic Shepard method: distance-weighted averages, no linear system.
- **Moving least squares:** a local weighted polynomial fit at each evaluation point; reproduces polynomials of the fitted degree.
- **[Radial basis functions](/radial-basis-function-interpolation/):** one kernel per site plus a polynomial tail; uniquely solvable, highest accuracy; $\Theta(N^3)$ dense setup or fast methods.
- **[Kriging](/kriging/):** RBF interpolation with a covariance kernel estimated from the data, giving a variance with each prediction.
- **Multilevel B-splines and quadtree methods:** approximate scattered data by splines on a hierarchy of grids.

## Bounds

- **Error in terms of fill distance (proved).** For kernels with Sobolev native space of order $\tau > d/2$ and $f$ in that space, $\|f - s\|_\infty = O(h^{\tau - d/2})$, and up to twice that rate for $f$ in a smaller space (Schaback's doubling argument); for Gaussians and multiquadrics, spectral rates in $h$ for very smooth $f$. Moving least squares and local polynomial methods of degree $m$ give $O(h^{m+1})$ for $f \in C^{m+1}$.
- **Information-based lower bound.** For functions with $k$ bounded derivatives, no method using $N$ values can beat $N^{-k/d}$ in the worst case; with quasi-uniform sites, $h \approx N^{-1/d}$, so the kernel bounds above are optimal in order. This is the [curse of dimensionality](/curse-of-dimensionality/) for scattered data.
- **Stability (proved).** The smallest eigenvalue of a positive definite kernel matrix is bounded below in terms of $q$ alone, and decreases as $q \to 0$, exponentially fast for Gaussians. Good error bounds and good conditioning cannot both hold (Schaback's uncertainty principle).
- **Shepard (proved).** Global inverse distance weighting with $p > d + 1$ converges only like $O(h)$; with $p \le d$ it does not converge in general (Farwig 1986).

## Reductions

- **To computational geometry.** Triangulation and natural neighbor methods reduce to Delaunay triangulations and [Voronoi diagrams](/voronoi-diagram/); local methods to fixed-radius or $k$-nearest-neighbor queries ([nearest neighbor search](/nearest-neighbor-search/)).
- **To dense linear algebra.** Kernel methods reduce to symmetric (conditionally) positive definite systems; fast multipole and hierarchical matrices reduce their cost.
- **Gridded data as a special case.** On a grid, [tensor-product interpolation](/tensor-product-interpolation/) is cheaper and as accurate; scattered data methods are for when no grid is available.
- **Kriging and RBF.** Simple kriging with covariance $C$ is RBF interpolation with kernel $C$; universal kriging adds the polynomial tail.

## Applications

- Geostatistics, mining and hydrology (ore grades, groundwater levels), meteorology and climate (station data to fields).
- Terrain models from survey points and lidar; surface reconstruction from 3D scans.
- Mesh deformation and fluid-structure coupling, where values move between non-matching meshes.
- Surrogate models and response surfaces from scattered runs of expensive simulations in engineering design.
- Image warping and registration from landmark correspondences (thin-plate splines in medical imaging).

## References
