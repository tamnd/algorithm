---
tag: S37CZP
kind: algorithm
slug: stochastic-collocation-method
name: Stochastic collocation method
aliases:
- sparse grid stochastic collocation
- sparse grid collocation
area: scientific-computing/uncertainty-quantification
level: advanced
summary: Solves the deterministic model at nodes of a sparse grid in parameter space and interpolates, a non-intrusive and spectrally accurate surrogate.
solves: [forward-uncertainty-propagation]
model: real-ram
complexity:
  vars: {d: "the number of inputs", L: "the Smolyak level", N: "the number of distinct sparse grid nodes, O(2^L L^(d-1))", T: "the number of tensor grid points summed over all combination terms", C: "the cost of one model run"}
  time: {worst: O(N C + d T)}
  space: {extra: O(N)}
properties: {deterministic: true, intrusive: false, exact: false}
history:
  year: 2005
  people: [Dongbin Xiu, Jan S. Hesthaven, Ivo Babuska, Fabio Nobile, Raul Tempone, Clayton G. Webster]
  note: Xiu and Hesthaven proposed collocation on sparse grids for random inputs in 2005. Babuska, Nobile and Tempone analyzed the tensor form for elliptic problems in 2007, and Nobile, Tempone and Webster the Smolyak form in 2008. The grids themselves go back to Smolyak in 1963.
prereqs: [smolyak-sparse-grids, clenshaw-curtis-quadrature, lagrange-interpolation]
see_also: [sparse-grid-quadrature, tensor-product-interpolation, non-intrusive-spectral-projection, stochastic-galerkin-method, polynomial-chaos-expansion, curse-of-dimensionality, lebesgue-constant, collocation-method]
sources:
  - paper: doi:10.1137/040615201
    title: Dongbin Xiu and Jan S. Hesthaven, High-order collocation methods for differential equations with random inputs, SIAM Journal on Scientific Computing 27(3), 2005, 1118-1139
    locator: the collocation of a model with random inputs at the nodes of tensor and Smolyak sparse grids, with the moments from the matching quadrature
  - paper: doi:10.1137/050645142
    title: Ivo Babuska, Fabio Nobile and Raul Tempone, A stochastic collocation method for elliptic partial differential equations with random input data, SIAM Journal on Numerical Analysis 45(3), 2007, 1005-1034
    locator: the tensor Gauss collocation method and its exponential convergence for solutions analytic in the parameters
  - paper: doi:10.1137/060663660
    title: Fabio Nobile, Raul Tempone and Clayton G. Webster, A sparse grid stochastic collocation method for partial differential equations with random input data, SIAM Journal on Numerical Analysis 46(5), 2008, 2309-2345
    locator: the error analysis of Smolyak collocation on Clenshaw-Curtis and Gauss nodes, with the rate in terms of the number of nodes
  - paper: doi:10.1023/A:1018977404843
    title: Volker Barthelmann, Erich Novak and Klaus Ritter, High dimensional polynomial interpolation on sparse grids, Advances in Computational Mathematics 12(4), 2000, 273-288
    locator: the exactness of the Smolyak operator on sums of tensor polynomial spaces, its interpolation property for nested nodes, and the error bounds for Clenshaw-Curtis sparse grids
---

The stochastic collocation method builds a polynomial surrogate of a model with random inputs by running the model at the nodes of a sparse grid in the input space and interpolating. Each run is an ordinary deterministic solve, so the method is non-intrusive, like [spectral projection](/non-intrusive-spectral-projection/), but its output is an interpolant rather than a set of chaos coefficients. The grid is the [Smolyak sparse grid](/smolyak-sparse-grids/) built from nested [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) nodes, so the number of runs grows like $2^L L^{d-1}$ with the level $L$ instead of $(2^L + 1)^d$ for a full [tensor grid](/tensor-product-interpolation/). The same grid gives a [sparse quadrature](/sparse-grid-quadrature/) for the mean and the variance. For outputs that are analytic in the inputs, the error falls faster than any power of the number of runs in low dimension, and still fast in moderate dimension.

## In plain words

You have a slow model with a few uncertain inputs, and you want a fast formula that copies it. Pick a set of input points, run the model at each, and draw the smooth polynomial that passes exactly through all the results. A full grid of points along every input axis gets too large fast: 17 points per axis in 5 inputs is 1.4 million runs. A sparse grid keeps mainly the points near the axes and few of the points that change all inputs at the same time, because smooth models seldom need those. In 3 inputs, 177 points do the work of 4913. Averages come for free: each grid point has a weight, and the average of the model is the weighted sum of the runs.

## The problem

The inputs $\xi_1, \ldots, \xi_d$ are independent and uniform on $[-1, 1]$ (other laws follow by a change of variables). The model output is $Q = q(\xi)$, where $q$ is continuous and can only be evaluated. Find a surrogate $A_L q$, a polynomial in $\xi$ that is cheap to evaluate, that equals $q$ at the nodes of a given grid, and that converges to $q$ uniformly as the level $L$ grows. Also find approximations of $\mathbb{E}[Q]$ and $\mathrm{Var}[Q]$ from the same runs.

## The algorithm

The one dimensional rule of level $l$ has $m(0) = 1$ node, the midpoint, and $m(l) = 2^l + 1$ nodes $x_j = -\cos(\pi j / 2^l)$ for $l \ge 1$. These levels are nested: every node of level $l - 1$ is a node of level $l$. Let $U_l$ be Lagrange interpolation on the level $l$ nodes and $Q_l$ the Clenshaw-Curtis rule on them.

```pseudo id=main
STOCHASTIC-COLLOCATION(q, d, L)
L1  T ← {(κ_l, l) : l ∈ ℕ^d, L-d+1 ≤ |l| ≤ L},  κ_l = (-1)^(L-|l|) · C(d-1, L-|l|)
L2  H ← union over (κ_l, l) ∈ T of the tensor grids X_{l_1} × ... × X_{l_d}
L3  for each node x ∈ H:  y_x ← q(x)                         ▷ one run per distinct node
L4  A_L q(ξ) = Σ_{(κ_l, l) ∈ T} κ_l (U_{l_1} ⊗ ... ⊗ U_{l_d}) y (ξ)
L5  w_x ← Σ_{(κ_l, l) ∈ T, x in grid l} κ_l · Π_k (Clenshaw-Curtis weight of x_k at level l_k)
L6  return A_L q,  mean Σ_x w_x y_x,  variance Σ_x w_x y_x^2 - mean^2
```

Line L1 lists the terms of the Smolyak combination formula. Only the levels with $|l|$ in the top $d$ layers appear, with integer coefficients that sum to 1. Line L2 collects the distinct nodes; because the levels are nested, the grids of different terms share many nodes, and the reference code stores each node once, keyed by its exact angle $j / 2^l$ as a fraction. Line L3 is the only place that runs the model, and the runs are independent. Line L4 is the surrogate: each term is a tensor Lagrange interpolant that reads its values from the shared table. Line L5 gives each node its sparse quadrature weight; some of these weights are negative. Line L6 returns the moments of the quadrature. The variance uses the quadrature of $q^2$, which is less accurate than the surrogate itself, because $q^2$ is rougher than $q$.

## Example

For $d = 2$ the grids have 1, 5, 13, 29 and 65 nodes at levels 0 to 4, and for $d = 3$ they have 1, 7, 25, 69 and 177. The Ishigami function $Q = \sin x_1 + 7 \sin^2 x_2 + 0.1\, x_3^4 \sin x_1$ with $x_k = \pi \xi_k$ has mean 3.5 and variance 13.844588. The surrogate error is the root mean square error at 300 random points divided by the standard deviation. The numbers are deterministic, except the surrogate error, which is a measurement with seed 5.

| $L$ | runs | full tensor grid | error of mean | variance | error of variance | surrogate error |
|---|---|---|---|---|---|---|
| 2 | 25 | 125 | 1.14 | 5.22626 | 8.62 | 0.91 |
| 3 | 69 | 729 | $1.1 \times 10^{-3}$ | 20.06157 | 6.22 | 0.24 |
| 4 | 177 | 4913 | $1.1 \times 10^{-9}$ | 17.32732 | 3.48 | $5.4 \times 10^{-2}$ |
| 5 | 441 | 35937 | $4 \times 10^{-16}$ | 13.67727 | 0.167 | $1.2 \times 10^{-4}$ |
| 6 | 1073 | 274625 | $4 \times 10^{-16}$ | 13.84443 | $1.6 \times 10^{-4}$ | $5.2 \times 10^{-12}$ |
| 7 | 2561 | 2146689 | 0 | 13.84459 | $1.7 \times 10^{-10}$ | $5.2 \times 10^{-15}$ |

The mean is exact to rounding from level 5. The variance lags by about one level, because it integrates $q^2$. At level 6 the surrogate matches the function to 12 digits with 1073 runs, where the full tensor grid of the same one dimensional level has 274625 nodes. At low levels the variance can be far too large, since negative weights make $\sum w_x y_x^2 - \text{mean}^2$ an unreliable estimate.

## Correctness

Write $\Delta_l = U_l - U_{l-1}$ with $U_{-1} = 0$. Expanding the differences shows that the combination formula equals $A_L = \sum_{|l| \le L} \Delta_{l_1} \otimes \cdots \otimes \Delta_{l_d}$. Two theorems follow, both proved in the proof file. First, with nested nodes, $A_L q$ interpolates $q$ at every node of the sparse grid. Second, $A_L$ reproduces every polynomial in $\sum_{|l| \le L} \mathbb{P}_{m(l_1) - 1} \otimes \cdots \otimes \mathbb{P}_{m(l_d) - 1}$, which contains all polynomials of total degree at most $L$, and many of higher degree. The same argument with the one dimensional rules, which are exact for degree $2l + 1$ at least, shows that the sparse quadrature of level $L$ is exact for all polynomials of total degree at most $2L + 1$; the tests check this and that a monomial of degree $2L + 2$ fails. Barthelmann, Novak and Ritter proved the exactness and interpolation statements and gave error bounds for Clenshaw-Curtis sparse grids. For outputs analytic in the inputs, Nobile, Tempone and Webster proved convergence rates in terms of the number of nodes.

## Complexity

In the [real RAM](/real-ram/) model, the number of distinct nodes is $N = O(2^L L^{d-1})$ for fixed $d$, and line L3 costs $N C$. Lines L4 to L6 work term by term; let $T$ be the number of tensor grid points summed over all terms, counted with repetition. The weights of line L5 cost $O(d T)$, and the moments $O(N)$. One evaluation of the surrogate costs $O(d T)$ plus the one dimensional Lagrange values. The total for building and moments is $O(N C + d T)$, and the table of runs takes $O(N)$ space. For $d = 3$ and $L = 6$ the reference code needs about a second in Python, mostly to evaluate the surrogate at the test points.

## Properties

- **Non-intrusive.** One deterministic run per node.
- **Interpolatory (theorem, nested nodes).** The surrogate equals the model at every node.
- **Polynomial exactness (theorem).** Total degree $L$ for interpolation and $2L + 1$ for the quadrature.
- **Hierarchical.** With nested nodes, raising the level reuses all previous runs.
- **Deterministic.** No sampling error; the error is interpolation error.
- **Negative weights.** The sparse quadrature has negative weights: for $d = 2$ and $d = 3$ at levels 2 to 4, between 5 and 69 nodes have a negative weight (measured with the reference code). So the variance estimate can be inaccurate or even negative.
- **Moderate dimension.** The node count still grows with $d$; sparse grids push the practical limit to roughly ten to twenty inputs for smooth outputs.

## Variants and improvements

- **Tensor Gauss collocation.** Babuska, Nobile and Tempone used full tensor grids of Gauss points, which interpolate on $m^d$ nodes and give the moments by Gauss quadrature; good for very few inputs.
- **Anisotropic grids.** Weight the levels by input, $\sum_k g_k l_k \le L$, to spend more nodes on the important inputs.
- **Adaptive sparse grids.** Add the difference terms $\Delta_l$ with the largest hierarchical surpluses one at a time, as in dimension adaptive quadrature.
- **Local bases.** Piecewise linear hierarchical bases on sparse grids handle outputs with kinks or jumps, where global polynomials oscillate.
- **Conversion to chaos.** The surrogate can be expanded in a chaos basis to get the Sobol indices, as the sparse pseudospectral method does with the same runs.
- **Leja and Gauss-Patterson nodes.** Other nested families with slower growth per level, for a finer choice of grid size.

## When to use it

Use stochastic collocation when the model is a black box, the inputs are few to moderate in number, and the output is smooth in the inputs, and you want a surrogate that you can evaluate anywhere. It shares the grid with [sparse grid quadrature](/sparse-grid-quadrature/), so it gives the mean at no extra cost. Prefer [spectral projection](/non-intrusive-spectral-projection/) or [regression](/regression-polynomial-chaos/) when you need chaos coefficients and Sobol indices directly, the [stochastic Galerkin method](/stochastic-galerkin-method/) when you can change the solver and want one coupled solve, and [Monte Carlo integration](/monte-carlo-integration/) when the output is not smooth or the dimension is high.

## Pitfalls

- **Non-smooth outputs.** A jump or a kink in $q$ causes Gibbs oscillations of the global interpolant and slow convergence. Use a local basis or an adaptive grid.
- **Variance from low levels.** $Q_L[q^2] - Q_L[q]^2$ can be badly wrong, as at $L = 2$ to 4 in the example. Check the variance at two consecutive levels, or integrate the square of the surrogate on a finer rule.
- **Non-nested nodes.** With non-nested nodes, such as Gauss points, the combination formula is not interpolatory and the grids of different terms share few nodes, so the run count rises.
- **Equally spaced nodes.** Equally spaced nodes give a fast growing [Lebesgue constant](/lebesgue-constant/) and the [Runge phenomenon](/runge-phenomenon/). Use Clenshaw-Curtis or Leja points.
- **Wrong input map.** For non-uniform inputs, map them to $[-1, 1]$ first, or use nodes and weights for their own law; mixing the two gives wrong moments.

## Implementations

## History

Smolyak introduced the combination of tensor products of one dimensional rules in 1963, and sparse grids were developed for quadrature and interpolation in the 1990s, with the analysis of Clenshaw-Curtis sparse grid interpolation by Barthelmann, Novak and Ritter in 2000. Xiu and Hesthaven proposed collocation at the nodes of tensor and sparse grids as a high order non-intrusive alternative to the [stochastic Galerkin method](/stochastic-galerkin-method/) in 2005. Babuska, Nobile and Tempone analyzed tensor Gauss collocation for elliptic problems with random coefficients in 2007, and Nobile, Tempone and Webster gave the error analysis of the sparse grid form in 2008, followed by anisotropic and adaptive versions.

## References
