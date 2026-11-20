---
tag: MZG7P5
kind: algorithm
slug: regression-polynomial-chaos
name: Regression-based polynomial chaos
aliases:
- least-squares polynomial chaos
- point collocation polynomial chaos
- polynomial chaos regression
area: scientific-computing/uncertainty-quantification
level: core
summary: Fits polynomial chaos coefficients by least squares to model runs at random or designed inputs, with more runs than coefficients.
solves: [forward-uncertainty-propagation]
model: real-ram
complexity:
  vars: {d: "the number of inputs", p: "the total degree", P: "the number of chaos terms (d+p choose p)", N: "the number of model runs (N >= P)", C: "the cost of one model run"}
  time: {worst: O(N (C + P^2))}
  space: {extra: O(N P)}
properties: {deterministic: false, intrusive: false, exact: false}
history:
  year: 2013
  people: [Albert Cohen, Mark A. Davenport, Dany Leviatan, Geraud Blatman, Bruno Sudret]
  note: Least squares is due to Legendre and Gauss. Its use for chaos coefficients spread in the 2000s; Blatman and Sudret made the leave-one-out error the standard check in 2011, and Cohen, Davenport and Leviatan proved in 2013 how many random runs make the fit stable.
prereqs: [polynomial-chaos-expansion, least-squares-problem, normal-equations]
see_also: [non-intrusive-spectral-projection, sparse-polynomial-chaos, hat-matrix, cross-validation, ordinary-least-squares, cholesky-decomposition, sobol-indices, latin-hypercube-sampling]
sources:
  - paper: doi:10.1007/s10208-013-9142-3
    title: Albert Cohen, Mark A. Davenport and Dany Leviatan, On the stability and accuracy of least squares approximations, Foundations of Computational Mathematics 13(5), 2013, 819-834
    locator: the stability condition on the number of random samples, K(P) at most a constant times N / log N, for the empirical Gram matrix to be close to the identity
  - paper: doi:10.1016/j.jcp.2010.12.021
    title: Geraud Blatman and Bruno Sudret, Adaptive sparse polynomial chaos expansion based on least angle regression, Journal of Computational Physics 230(6), 2011, 2345-2367
    locator: the leave-one-out error of a least-squares chaos expansion computed from the hat matrix diagonal
  - paper: doi:10.1016/j.ress.2007.04.002
    title: Bruno Sudret, Global sensitivity analysis using polynomial chaos expansions, Reliability Engineering and System Safety 93(7), 2008, 964-979
    locator: the Sobol indices as sums of squared chaos coefficients, with the regression estimate of the coefficients
  - book: isbn:9789048135196
    title: Olivier P. Le Maitre and Omar M. Knio, Spectral Methods for Uncertainty Quantification, Springer, 2010
    locator: Chapter 3 (non-intrusive methods)
---

Regression-based polynomial chaos fits the coefficients of a [polynomial chaos expansion](/polynomial-chaos-expansion/) to a set of model runs by [least squares](/least-squares-problem/). It draws $N$ input points, runs the model at each, and chooses the coefficients that minimize the sum of squared differences between the expansion and the outputs. Unlike [spectral projection by quadrature](/non-intrusive-spectral-projection/), it accepts any set of points, so the runs can come from random sampling, a [Latin hypercube](/latin-hypercube-sampling/) or an existing database. The number of runs must exceed the number of coefficients $P$; a common rule of thumb (a heuristic, not a theorem) is $N = 2P$ to $3P$. The leave-one-out error, computed from one fit by the [hat matrix](/hat-matrix/) identity, measures how well the expansion predicts new runs.

## In plain words

You want a polynomial formula that copies a slow model, so that you can compute averages and sensitivities from the formula instead of the model. Run the model at a few hundred random inputs. Then pick the polynomial that passes as close as possible to all the outputs, in the sense of the smallest total squared miss. This is ordinary curve fitting with special polynomials, and one linear solve gives all the coefficients. To check the fit, leave out one run, fit again, and see how badly the new fit predicts the run you left out; average this over all runs. A simple formula gives this average from the single fit, so you do not need to refit. Take about two or three times as many runs as there are coefficients.

## The problem

The input $\xi = (\xi_1, \ldots, \xi_d)$ has independent components with laws $\rho_1, \ldots, \rho_d$. The output $Q = q(\xi)$ is square integrable, and $q$ can only be evaluated. The basis $\Psi_\alpha(\xi) = \prod_k \psi^{(k)}_{\alpha_k}(\xi_k)$ is orthonormal for the law of $\xi$, and the index set is $\Lambda = \{\alpha : |\alpha| \le p\}$ with $P = \binom{d+p}{p}$ terms. Given $N \ge P$ points $x_1, \ldots, x_N$ and the outputs $y_i = q(x_i)$, find

$$c = \arg\min_{c \in \mathbb{R}^P} \sum_{i=1}^{N} \Big(y_i - \sum_{\alpha \in \Lambda} c_\alpha \Psi_\alpha(x_i)\Big)^2,$$

together with an estimate of the error of $q_p = \sum_\alpha c_\alpha \Psi_\alpha$ on new inputs. The moments and the [Sobol indices](/sobol-indices/) then follow from $c$ as for any orthonormal expansion.

## The algorithm

```pseudo id=main
REGRESSION-PCE(q, ρ, p, N)
L1  Λ ← all α ∈ ℕ^d with |α| ≤ p;  P ← |Λ|;  require N ≥ P
L2  draw x_1, ..., x_N independently from ρ
L3  y_i ← q(x_i) for i = 1..N                                ▷ N model runs
L4  A[i, α] ← Ψ_α(x_i)                                       ▷ N × P design matrix
L5  solve (A^T A) c = A^T y by Cholesky
L6  h_i ← A_i (A^T A)^{-1} A_i^T;  ε_LOO ← (1/N) Σ_i ((y_i - A_i c) / (1 - h_i))^2 / Var(y)
L7  return c, ε_LOO
```

Line L1 builds the total degree set. Line L2 draws the points from the input law, which makes $\frac{1}{N} A^{\mathsf T} A$ an unbiased estimate of the identity, because $\mathbb{E}[\Psi_\alpha \Psi_\beta] = \delta_{\alpha\beta}$. Line L3 is the only place that runs the model, and the runs are independent. Line L4 evaluates the one dimensional polynomials by their recurrence and multiplies them. Line L5 solves the [normal equations](/normal-equations/) with the [Cholesky decomposition](/cholesky-decomposition/) of the $P \times P$ Gram matrix; when $A$ is ill conditioned, a [QR decomposition](/qr-decomposition/) of $A$ is the safer choice. Line L6 computes the leverages $h_i$, the diagonal of the hat matrix $H = A (A^{\mathsf T} A)^{-1} A^{\mathsf T}$, from the same Cholesky factor: $h_i = \|L^{-1} A_i^{\mathsf T}\|^2$. The ratio $(y_i - A_i c)/(1 - h_i)$ is exactly the error at $x_i$ of the fit without run $i$, so $\varepsilon_{\mathrm{LOO}}$ is the leave-one-out mean squared error, divided by the sample variance of the outputs.

## Example

The Ishigami function $Q = \sin x_1 + 7 \sin^2 x_2 + 0.1\, x_3^4 \sin x_1$ with $x_k = \pi \xi_k$ and $\xi_k$ uniform on $[-1, 1]$ has mean 3.5, variance 13.84459, $S_1 = 0.3139$ and total index $S_{T3} = 0.2437$. The fit uses the Legendre basis of total degree $p = 8$, so $P = 165$, and random uniform points. Each row of the table is a measurement over the five seeds 0 to 4. The validation error is the mean squared error on 2000 fresh random points divided by the variance.

| $N$ | $N/P$ | mean, range over seeds | $S_1$, range | median $\varepsilon_{\mathrm{LOO}}$ | median validation error |
|---|---|---|---|---|---|
| 167 | 1.01 | -0.34 to 4.37 | 0.023 to 0.272 | 5.5 | 2.3 |
| 247 | 1.5 | 3.482 to 3.564 | 0.304 to 0.316 | $8.5 \times 10^{-3}$ | $1.2 \times 10^{-2}$ |
| 330 | 2 | 3.457 to 3.504 | 0.309 to 0.314 | $3.2 \times 10^{-3}$ | $3.3 \times 10^{-3}$ |
| 495 | 3 | 3.486 to 3.503 | 0.311 to 0.314 | $1.2 \times 10^{-3}$ | $1.5 \times 10^{-3}$ |

With almost as many runs as coefficients, the fit is useless: a relative error above 1 means that the expansion is worse than the constant mean. From $N = 1.5 P$ on, the error falls fast, and the leave-one-out error tracks the validation error within a factor of about 2 without any extra runs. For comparison, the tensor Gauss rule of [spectral projection](/non-intrusive-spectral-projection/) needs 729 runs at $p = 8$.

## Correctness

If the design matrix $A$ has full column rank, then $A^{\mathsf T} A$ is symmetric positive definite, the Cholesky factor exists, and the solution of line L5 is the unique minimizer: for any $c'$, $\|A c' - y\|^2 = \|A c - y\|^2 + \|A (c' - c)\|^2$ because the residual is orthogonal to the columns of $A$. If $q$ lies in the span of $\Psi_\alpha$, $\alpha \in \Lambda$, then $y = A c^*$, and the minimizer is $c^*$ itself, with a zero residual. With random points, full rank holds with probability 1 for polynomial bases and $N \ge P$ (the zero set of a nonzero polynomial has measure zero). The leave-one-out identity follows from the [Sherman-Morrison formula](/sherman-morrison-formula/) applied to $A^{\mathsf T} A - A_i^{\mathsf T} A_i$. The proof file gives these steps in full.

Stability is a theorem only for enough runs. Let $K(\Lambda) = \sup_\xi \sum_{\alpha \in \Lambda} \Psi_\alpha(\xi)^2$. Cohen, Davenport and Leviatan proved that if $K(\Lambda) \le \kappa N / \log N$ with an explicit constant $\kappa$ depending on a chosen $r > 0$, then with probability at least $1 - 2 N^{-r}$ the empirical Gram matrix $\frac{1}{N} A^{\mathsf T} A$ has all eigenvalues in $[1/2, 3/2]$, and for a bounded $q$ the expected error of the fit, truncated at the bound, is close to the best approximation error in $\Lambda$, plus a term of order $N^{-r}$. For the Legendre basis $K = P^2$ in one dimension, so the theorem asks for $N$ of order $P^2 \log P$ uniform samples; the $2P$ to $3P$ rule is a heuristic that works for smooth outputs, as the example shows, but has no such guarantee.

## Complexity

In the [real RAM](/real-ram/) model, line L3 costs $N C$. Line L4 costs $O(N (d p + d P))$. The Gram matrix costs $O(N P^2)$, the Cholesky factor $O(P^3)$, and the leverages $O(N P^2)$ by $N$ triangular solves. Since $N \ge P$, the total is $O(N (C + P^2))$ time, and the design matrix takes $O(N P)$ space. For $p = 8$, $d = 3$ and $N = 495$ the reference code takes well under a second in Python; for an expensive model, $N C$ dominates.

## Properties

- **Non-intrusive and design free.** Any point set works, including runs that exist already.
- **Exact for polynomials (theorem).** If $q$ is in the span of the basis and $A$ has full column rank, the fit is exact.
- **Randomized.** With random points, the coefficients are random; repeated fits with new seeds show the spread, as in the example.
- **Free error estimate.** The leave-one-out error comes from one fit, by the hat matrix identity.
- **Needs more runs than terms.** $N \ge P$ is necessary; $N$ close to $P$ gives a badly conditioned fit.
- **Curse of dimensionality.** $P$ grows like $d^p / p!$ for fixed $p$, and $N$ grows with it.

## Variants and improvements

- **Weighted least squares.** Draw the points from a sampling law adapted to the basis, such as the Chebyshev law for Legendre polynomials, and weight the rows by the density ratio. With the sampling law proportional to $\sum_\alpha \Psi_\alpha^2\, \rho$, the quantity $K$ of the stability theorem becomes $P$, so the run count it needs falls to order $P \log P$.
- **Designed points.** Latin hypercube, quasi-Monte Carlo points or D-optimal subsets of a candidate set give better conditioned fits than plain random points for the same $N$.
- **Sparse fits.** When $N < P$, or when most coefficients are small, use [sparse polynomial chaos](/sparse-polynomial-chaos/) by l1 minimization, least angle regression or [orthogonal matching pursuit](/orthogonal-matching-pursuit/), and choose the basis by the leave-one-out error.
- **Regularized fits.** [Ridge regression](/ridge-regression/) adds a penalty $\lambda \|c\|^2$ and keeps the solve stable when $N$ is close to $P$.
- **Gradient-enhanced regression.** If the model also returns derivatives, add rows for $\partial q / \partial \xi_k$; each run then gives $d + 1$ equations.

## When to use it

Use regression when the model is a black box, when the runs come from a given design or a database, or when a tensor quadrature grid would be too large. It is the usual choice for moderate dimension (up to about ten inputs) with a smooth output. Use [spectral projection](/non-intrusive-spectral-projection/) when the dimension is small and you can choose the points freely, [sparse polynomial chaos](/sparse-polynomial-chaos/) when runs are fewer than coefficients, and [Monte Carlo integration](/monte-carlo-integration/) when the output is not smooth.

## Pitfalls

- **Too few runs.** At $N \approx P$ the Gram matrix is nearly singular, and the coefficients are dominated by noise in the fit, as the first row of the example shows.
- **Unbounded bases.** With Gaussian inputs, Hermite polynomials grow fast, and a few points in the tails get large leverage. Check that the leverages $h_i$ are not close to 1, and consider weighted sampling.
- **Normal equations square the condition number.** The condition number of $A^{\mathsf T} A$ is the square of that of $A$. For high degrees, use QR on $A$.
- **Trusting the training residual.** The residual of the fit always falls as $p$ grows; the leave-one-out error does not, and it is the one to use to pick $p$.
- **Leverage equal to 1.** If $h_i = 1$, removing run $i$ makes $A$ rank deficient and the leave-one-out formula divides by zero. Such a run is the only one that fixes some coefficient.

## Implementations

## History

The method of least squares goes back to Legendre in 1805 and to Gauss. Regression fits of polynomial chaos coefficients to random model runs came into use in the early 2000s as a non-intrusive alternative to the [stochastic Galerkin method](/stochastic-galerkin-method/) and to quadrature. Blatman and Sudret made the leave-one-out error from the hat matrix the standard check, and used it in 2011 to build sparse expansions by least angle regression. Cohen, Davenport and Leviatan gave in 2013 the first sharp theorem on how many random runs a stable least-squares fit needs, which started the work on optimal weighted sampling.

## References
