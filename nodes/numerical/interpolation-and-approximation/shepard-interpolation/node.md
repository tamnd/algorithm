---
tag: GAEMZW
kind: algorithm
slug: shepard-interpolation
name: Shepard interpolation
aliases:
- Inverse distance weighting
- IDW
- Shepard's method
area: numerical/interpolation-and-approximation
level: advanced
summary: Weighted average of data with weights inversely proportional to distance raised to a power. Simple, needs no linear system, and stays within the data range, but it only reproduces constants.
solves: [scattered-data-interpolation]
model: real-ram
complexity:
  vars: {N: the number of data points, d: the dimension, k: the number of points within the radius}
  time: {setup: Θ(1), evaluate_global: Θ(N d), evaluate_local_with_kd_tree: O(k d + log N)}
  space: {extra: Θ(1)}
  flops: {evaluate_global: "3 N d + 4 N"}
properties: {deterministic: true, recursive: false, interpolates: true, reproduces_constants: true, reproduces_linear: false, convex_combination: true, needs_linear_solve: false}
history:
  year: 1968
  people: [Donald Shepard]
  note: Shepard proposed the method in 1968 for irregularly spaced geographic data; Franke and Nielson (1980) gave the local modified version.
prereqs: [scattered-data-interpolation]
see_also: [radial-basis-function-interpolation, nearest-neighbor-interpolation, kriging, kd-tree, nearest-neighbor-search, voronoi-diagram, multivariate-interpolation, piecewise-linear-interpolation]
sources:
  - paper: "Donald Shepard, A two-dimensional interpolation function for irregularly-spaced data, Proceedings of the 23rd ACM National Conference (1968) 517-524"
    locator: the inverse distance weighted average and its local and gradient-corrected variants
  - paper: "William J. Gordon and James A. Wixom, Shepard's method of metric interpolation to bivariate and multivariate interpolation, Mathematics of Computation 32 (1978) 253-264"
    locator: smoothness at the nodes and flat spots
  - paper: "Richard Franke and Gregory Nielson, Smooth interpolation of large sets of scattered data, International Journal for Numerical Methods in Engineering 15 (1980) 1691-1704"
    locator: the modified (local) quadratic Shepard method and the Franke-Little weights
  - paper: "Richard Franke, Scattered data interpolation, tests of some methods, Mathematics of Computation 38 (1982) 181-200"
    locator: comparison of Shepard-type methods with radial basis functions and triangulation methods on test functions
  - paper: "Rudolf Farwig, Rate of convergence of Shepard's global interpolation formula, Mathematics of Computation 46 (1986) 577-590"
    locator: the dependence of the convergence order on the power p and the dimension d
  - book: isbn:9780521843355
    title: Holger Wendland, Scattered Data Approximation, Cambridge University Press, 2005
    locator: Chapter 4, Moving least squares (Shepard's method as the moving least squares approximation of degree zero)
---

Shepard interpolation, also called inverse distance weighting (IDW), estimates a function at a point as a weighted average of the data values, with weights that grow without bound as the point approaches a data site. It works in any dimension on arbitrarily scattered points, needs no triangulation and no linear system, and the result never leaves the range of the data. Its weaknesses are low accuracy, flat spots at every data point, and a global dependence on far-away data that the local variants remove.

## In plain words

To guess a value where you have not measured, take the measurements you have and average them, giving more say to nearby ones. Shepard's rule makes the say of each measurement equal to one over its distance raised to some power, usually two. At a measured spot that measurement gets all the say, so the guess matches the data exactly.

The guess can never be higher than the highest measurement or lower than the lowest, which keeps it safe. But it is also crude: it cannot follow a steady slope, and it levels off around each measured point.

## The problem

Notation on the interpolation pages: data sites $x_1, \ldots, x_N \in \mathbb{R}^d$ with values $y_i = f(x_i)$; $\|\cdot\|$ is the Euclidean norm; $p > 0$ is the power.

**Shepard's interpolant.** For $x$ not a data site,
$$s(x) = \frac{\sum_{i=1}^{N} w_i(x)\, y_i}{\sum_{i=1}^{N} w_i(x)}, \qquad w_i(x) = \|x - x_i\|^{-p},$$
and $s(x_i) = y_i$. Equivalently $s = \sum_i u_i y_i$ with the cardinal functions $u_i = w_i / \sum_j w_j$, which are nonnegative and sum to 1.

**Local version (Franke and Little).** With a radius $R$, use $w_i(x) = \big((R - r_i)_+ / (R\, r_i)\big)^2$ with $r_i = \|x - x_i\|$, so that only data within distance $R$ contribute. The interpolant is then undefined where no data site lies within $R$.

## The algorithm

```pseudo id=main
SHEPARD(x_1..x_N, y_1..y_N, x, p)
L1  for i = 1..N: r_i ← ‖x − x_i‖
L2  if some r_i = 0: return y_i (the mean, if several sites coincide with x)
L3  w_i ← r_i^(−p) for i = 1..N
L4  return (Σ_i w_i y_i) / (Σ_i w_i)
```

The implementation works with squared distances, so for even $p$ it needs no square roots and is exact in rational arithmetic. In the local version line L3 uses the Franke-Little weights and skips sites with $r_i \ge R$; a spatial index such as a [k-d tree](/kd-tree/) finds those sites without scanning all $N$.

## Example

**One dimension, by hand.** Sites $0, 1, 2$ with values $0, 1, 2$ (the line $f(x) = x$), $p = 2$, at $x = \tfrac12$: the distances are $\tfrac12, \tfrac12, \tfrac32$, the weights $4, 4, \tfrac49$, and
$$s(\tfrac12) = \frac{0 \cdot 4 + 1 \cdot 4 + 2 \cdot \tfrac49}{4 + 4 + \tfrac49} = \frac{44/9}{76/9} = \frac{11}{19} \approx 0.579,$$
not $\tfrac12$: Shepard's method does not reproduce linear functions. With the two sites $0, 1$ and values $0, 1$ alone, $s(\tfrac13) = \tfrac{9/4}{9 + 9/4} = \tfrac15$, pulled toward the nearer value.

**Franke's test function on $[0, 1]^2$.** With $N$ Halton points and errors measured on a $30 \times 30$ grid in $[0.05, 0.95]^2$:

| $N$ | $p = 1$ | $p = 2$ | $p = 3$ | $p = 4$ | local, $R = 5/\sqrt{N}$ |
|---|---|---|---|---|---|
| 25 | 0.56 | 0.38 | 0.28 | 0.26 | 0.30 |
| 100 | 0.56 | 0.31 | 0.18 | 0.14 | 0.16 |
| 400 | 0.55 | 0.22 | 0.086 | 0.060 | 0.053 |
| 1600 | 0.55 | 0.20 | 0.054 | 0.036 | 0.027 |

With $p \le d = 2$ the far data dominate and the error barely decreases; with $p = 4$ and in the local version the error roughly halves when the spacing halves, which is first-order convergence. For comparison, thin-plate spline [RBF interpolation](/radial-basis-function-interpolation/) on the same 400 points has error $4.2 \times 10^{-3}$.

## Correctness

Each $w_i$ is positive away from the sites, so the denominator is positive and $s(x)$ is a convex combination of the $y_i$; hence $\min_i y_i \le s(x) \le \max_i y_i$, and constants are reproduced. At a site, line L2 returns the data value. The interpolant is continuous at the sites: as $x \to x_k$, $w_k(x) \to \infty$ while the other weights stay bounded, so $u_k(x) \to 1$ and $s(x) \to y_k$. The proof below gives the details, including the flat spots for $p > 1$.

## Complexity

- **Setup:** none. All the work happens at evaluation.
- **Global evaluation:** $\Theta(N d)$ per point: $3d$ flops per site for the squared distance, plus the power and two multiply-adds. Evaluating at $M$ points costs $\Theta(M N d)$, which is the bottleneck for large data sets.
- **Local evaluation:** with a [k-d tree](/kd-tree/) built in $O(N \log N)$, a query that finds $k$ sites within $R$ costs $O(\log N + k)$ in typical low-dimensional cases.

## Properties

- **Interpolates** and is **continuous** for every $p > 0$; for $p > 0$ it is infinitely differentiable away from the sites, and for even integer $p$ everywhere (Gordon and Wixom).
- **Flat spots.** For $p > 1$ the gradient of $s$ is zero at every site, whatever the data; for $0 < p \le 1$ the interpolant has corners or cusps there.
- **Bounded by the data** (a discrete maximum principle), so no overshoot: useful for densities and concentrations that must stay in range.
- **Reproduces constants only.** It is the moving least squares approximation of degree 0 with weights $w_i$, so its approximation order is at most first order.
- **Convergence (proved, Farwig 1986):** for quasi-uniform sites of spacing $h$, the global method converges like $O(h)$ when $p > d + 1$, more slowly for $d < p \le d + 1$, and not in general for $p \le d$, because the total weight of far sites then dominates. The table above shows all three regimes.
- **Local and linear in the data.** $s$ depends linearly on the $y_i$; the local version also depends only on nearby data.

## Variants and improvements

- **Modified quadratic Shepard (Franke and Nielson 1980; Renka 1988).** Replace each $y_i$ by a local quadratic $Q_i(x)$ fitted by least squares to neighbors with $Q_i(x_i) = y_i$, and blend them with local weights: $s = \sum_i u_i(x) Q_i(x)$. This reproduces quadratics, removes the flat spots and is much more accurate.
- **Gradient corrections.** Shepard's original paper already added estimated slopes to reduce flat spots.
- **Moving least squares.** Fit a polynomial of degree $m$ at each evaluation point with distance weights; degree 0 is Shepard's method.
- **Partition of unity methods.** The normalized weights $u_i$ form a partition of unity and serve to blend local approximants of any kind.
- **Kriging and RBFs.** When accuracy matters, solve a linear system instead: [kriging](/kriging/) and [radial basis functions](/radial-basis-function-interpolation/) reach higher orders.

## When to use it

Use Shepard interpolation for quick, robust estimates from scattered points when the values must stay within the data range and moderate accuracy is enough: mapping rainfall or pollution from stations, filling gaps in geographic grids, and as a cheap baseline. Use the local version for large data sets. Avoid it when derivatives or high accuracy are needed, or when data are dense and smooth, where RBF, kriging or piecewise polynomial methods on a triangulation are better.

## Pitfalls

- **Flat spots** at the data sites give "bull's-eye" contour patterns around each station.
- **Choice of $p$.** $p = 2$ in two dimensions sits on the boundary where far data dominate; the result tends to the global mean between sites as data get dense. Use $p > d$, or the local version.
- **Clustered data.** A tight cluster of sites acts as a heavy single site; Shepard has no notion of redundancy, unlike kriging.
- **No extrapolation of trends.** Outside the data, $s$ tends to the mean of the data, not to the trend.
- **Empty neighborhoods.** The local version is undefined where no site lies within $R$; choose $R$ from the data spacing or use the $k$ nearest sites.
- **Rounding near a site.** Very close to a site, $r_i^{-p}$ may overflow; testing for an exact hit (line L2) is not enough, so scale the weights by the smallest distance first in production code.

## Implementations

## History

Donald Shepard introduced the method in 1968 to interpolate irregularly spaced geographic data for the Harvard Laboratory for Computer Graphics, together with local and gradient-corrected versions. Gordon and Wixom (1978) analysed its smoothness, Franke and Nielson (1980) introduced the modified local quadratic version, and Franke's 1982 comparison of scattered data methods made Shepard's method a standard baseline. Farwig (1986) settled its convergence rates.

## References
