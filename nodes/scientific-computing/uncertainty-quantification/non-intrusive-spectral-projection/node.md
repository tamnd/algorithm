---
tag: K2M34Y
kind: algorithm
slug: non-intrusive-spectral-projection
name: Non-intrusive spectral projection
aliases:
- pseudospectral projection
- NISP
- discrete spectral projection
- quadrature-based polynomial chaos
area: scientific-computing/uncertainty-quantification
level: core
summary: Computes polynomial chaos coefficients as projections evaluated by quadrature over model runs at the quadrature nodes.
solves: [forward-uncertainty-propagation]
model: real-ram
complexity:
  vars: {d: "the number of inputs", m: "the number of Gauss points per input", p: "the total degree", P: "the number of chaos terms (d+p choose p)", C: "the cost of one model run"}
  time: {worst: O(m^d (C + d P))}
  space: {extra: O(P + d m)}
properties: {deterministic: true, intrusive: false, exact: false}
history:
  year: 2003
  people: [Matthew T. Reagan, Habib N. Najm, Roger G. Ghanem, Omar M. Knio]
  note: Reagan, Najm, Ghanem and Knio named the method in 2003, for reacting flow codes that could not be rewritten. The quadrature rules go back to Gauss, and their computation from the recurrence to Golub and Welsch in 1969.
prereqs: [gaussian-quadrature, orthogonal-polynomials, polynomial-chaos-expansion]
see_also: [gauss-hermite-quadrature, gauss-legendre-quadrature, golub-welsch-algorithm, sparse-grid-quadrature, regression-polynomial-chaos, stochastic-galerkin-method, stochastic-collocation-method, sobol-indices]
sources:
  - paper: doi:10.1016/S0010-2180(02)00503-5
    title: Matthew T. Reagan, Habib N. Najm, Roger G. Ghanem and Omar M. Knio, Uncertainty quantification in reacting-flow simulations through non-intrusive spectral projection, Combustion and Flame 132(3), 2003, 545-555
    locator: the non-intrusive spectral projection of a legacy code by quadrature over runs at the nodes
  - book: isbn:9789048135196
    title: Olivier P. Le Maitre and Omar M. Knio, Spectral Methods for Uncertainty Quantification, Springer, 2010
    locator: Chapter 3 (non-intrusive methods, including the projection by quadrature and its sparse grid forms)
  - paper: doi:10.1090/S0025-5718-69-99647-1
    title: Gene H. Golub and John H. Welsch, Calculation of Gauss quadrature rules, Mathematics of Computation 23(106), 1969, 221-230
    locator: the Gauss nodes as eigenvalues of the Jacobi matrix and the weights from the first eigenvector components
  - paper: doi:10.1016/j.ress.2007.04.002
    title: Bruno Sudret, Global sensitivity analysis using polynomial chaos expansions, Reliability Engineering and System Safety 93(7), 2008, 964-979
    locator: the Sobol indices as sums of squared chaos coefficients
  - paper: doi:10.1016/j.cma.2012.03.019
    title: Paul G. Constantine, Michael S. Eldred and Eric T. Phipps, Sparse pseudospectral approximation method, Computer Methods in Applied Mechanics and Engineering 229-232, 2012, 1-12
    locator: the aliasing error of projection with Smolyak quadrature and the sparse pseudospectral method that avoids it
---

Non-intrusive spectral projection (NISP) computes the coefficients of a [polynomial chaos expansion](/polynomial-chaos-expansion/) of a model output by numerical integration. For an orthonormal basis, the coefficient of $\Psi_\alpha$ is the projection $c_\alpha = \mathbb{E}[q(\xi) \Psi_\alpha(\xi)]$. NISP replaces each expectation by a [Gauss quadrature](/gaussian-quadrature/) rule for the input law, so it needs the model only at the quadrature nodes, as a black box. One set of runs gives all coefficients, and from them the mean, the variance and the [Sobol indices](/sobol-indices/). With a tensor rule of $m$ points per input, the coefficients of degree up to $p$ are exact for every polynomial output of total degree $p$ when $m \ge p + 1$. For a smooth output they converge exponentially. The price is the $m^d$ runs of the tensor grid, so the plain method serves only a few inputs.

## In plain words

You want to write a model output as a sum of special polynomials of the random inputs, and you need the weight of each polynomial. Each weight is an average: the average of the output times that polynomial. You cannot compute the average exactly, but you can estimate it well from a few carefully chosen input values and weights, a Gauss rule. So you run the model at those input values, and you compute every weight from the same set of runs. The model itself does not change, which is why the method is called non-intrusive. For one input, ten runs are often enough. For several inputs, the rule uses every combination of the points, so the number of runs multiplies with each new input.

## The problem

The input $\xi = (\xi_1, \ldots, \xi_d)$ has independent components with laws $\rho_1, \ldots, \rho_d$, on a probability space $(\Omega, \mathcal{F}, \mathbb{P})$. The model output is $Q = q(\xi)$, square integrable, and $q$ can only be evaluated. The basis is $\Psi_\alpha(\xi) = \prod_k \psi^{(k)}_{\alpha_k}(\xi_k)$, where $\psi^{(k)}_0, \psi^{(k)}_1, \ldots$ are the orthonormal polynomials of $\rho_k$: the normalized probabilists' Hermite polynomials $\mathrm{He}_n / \sqrt{n!}$ for a standard normal input, and $\sqrt{2n+1}\, P_n$ with the [Legendre polynomials](/legendre-polynomials/) $P_n$ for a uniform input on $[-1, 1]$. The index set is the total degree set $\Lambda = \{\alpha : |\alpha| \le p\}$, with $P = \binom{d+p}{p}$ terms. The output is the vector of coefficients $c_\alpha$, $\alpha \in \Lambda$, and the moments and Sobol indices of the expansion $q_p = \sum_\alpha c_\alpha \Psi_\alpha$.

## The algorithm

```pseudo id=main
NISP(q, ρ_1..ρ_d, p, m)
L1  for k ← 1 to d: (x^k_j, w^k_j), j = 1..m ← Gauss rule of ρ_k     ▷ Golub-Welsch
L2  Λ ← all α ∈ ℕ^d with |α| ≤ p;  c_α ← 0 for α ∈ Λ
L3  for each node x = (x^1_{j_1}, ..., x^d_{j_d}) with weight w = w^1_{j_1} ⋯ w^d_{j_d} do
L4      y ← q(x)                                                    ▷ one model run
L5      for each α ∈ Λ: c_α ← c_α + w y Ψ_α(x)
L6  return c, mean c_0, variance Σ_{α ≠ 0} c_α^2
```

Line L1 builds an $m$ point rule for each input law. The [Golub-Welsch algorithm](/golub-welsch-algorithm/) gets it from the three term recurrence $x \psi_{n-1} = b_n \psi_n + b_{n-1} \psi_{n-2}$: the nodes are the eigenvalues of the symmetric tridiagonal Jacobi matrix with off-diagonal $b_1, \ldots, b_{m-1}$, and the weights are the squared first components of its unit eigenvectors. For the orthonormal Hermite family $b_n = \sqrt{n}$, and for the orthonormal Legendre family $b_n = n / \sqrt{4n^2 - 1}$. The weights sum to 1, because $\rho_k$ is a probability law. The [Gauss-Hermite quadrature](/gauss-hermite-quadrature/) page uses the physicists' weight $e^{-x^2}$; its nodes are those here divided by $\sqrt{2}$, and its weights are those here times $\sqrt{\pi}$. Line L3 visits the $m^d$ nodes of the tensor rule. Line L4 is the only call to the model, and the runs are independent, so they can run in parallel. Line L5 accumulates every coefficient from the same run. Line L6 reads the moments off the coefficients by orthonormality; the Sobol index of a set of inputs is the sum of $c_\alpha^2$ over the $\alpha$ whose nonzero entries are exactly those inputs, divided by the variance.

## Example

**One Gaussian input.** Let $Q = e^{\xi}$ with $\xi \sim N(0, 1)$. The exact mean is $e^{1/2} = 1.6487213$, the exact variance is $e^2 - e = 4.6707743$, and the exact coefficients are $c_n = e^{1/2} / \sqrt{n!}$. The run takes $p = m - 1$. The values are deterministic.

| $m$ (runs) | mean | error of mean | variance | error of variance | $c_{m-1}$ | exact $c_{m-1}$ |
|---|---|---|---|---|---|---|
| 2 | 1.5430806 | $1.06 \times 10^{-1}$ | 1.381098 | 3.29 | 1.1752 | 1.6487 |
| 3 | 1.6381925 | $1.05 \times 10^{-2}$ | 3.312833 | 1.36 | 0.9025 | 1.1658 |
| 4 | 1.6479690 | $7.52 \times 10^{-4}$ | 4.279512 | $3.91 \times 10^{-1}$ | 0.5480 | 0.6731 |
| 5 | 1.6486794 | $4.18 \times 10^{-5}$ | 4.583510 | $8.73 \times 10^{-2}$ | 0.2835 | 0.3365 |
| 6 | 1.6487194 | $1.90 \times 10^{-6}$ | 4.654858 | $1.59 \times 10^{-2}$ | 0.1299 | 0.1505 |
| 8 | 1.6487213 | $2.45 \times 10^{-9}$ | 4.670446 | $3.29 \times 10^{-4}$ | 0.02072 | 0.02322 |

With $m = 2$ the nodes are $\pm 1$ with weights $1/2$, so the mean is $\cosh 1$. The mean converges much faster than the top coefficient. The rule integrates $e^{\xi} \Psi_n$ well for small $n$, but for $n = m - 1$ the integrand has a high degree part that the rule cannot see. This error is called aliasing.

**The Ishigami function.** Let $Q = \sin x_1 + 7 \sin^2 x_2 + 0.1\, x_3^4 \sin x_1$ with $x_k = \pi \xi_k$ and $\xi_k$ uniform on $[-1, 1]$, with the Legendre basis and $m = p + 1$:

| $p$ | runs | $P$ | mean | variance | $S_1$ | $S_2$ | $S_{T3}$ |
|---|---|---|---|---|---|---|---|
| 4 | 125 | 35 | 3.441659 | 17.16952 | 0.2489 | 0.6415 | 0.1096 |
| 6 | 343 | 84 | 3.499702 | 14.80586 | 0.2935 | 0.4878 | 0.2187 |
| 8 | 729 | 165 | 3.500000 | 13.88491 | 0.3130 | 0.4442 | 0.2428 |
| 10 | 1331 | 286 | 3.500000 | 13.84513 | 0.3139 | 0.4424 | 0.2437 |
| 12 | 2197 | 455 | 3.500000 | 13.84459 | 0.3139 | 0.4424 | 0.2437 |
| exact | | | 3.5 | 13.84459 | 0.3139 | 0.4424 | 0.2437 |

At $p = 4$ the variance is too large, not too small, which can only come from aliasing: a truncated exact expansion always has a smaller variance than the function. $S_3$ is zero to rounding at every degree, because $x_3$ enters only together with $x_1$.

## Correctness

The claim is that the coefficients are exact projections whenever the tensor rule integrates $q \Psi_\alpha$ exactly. An $m$ point Gauss rule is exact for polynomials of degree at most $2m - 1$, and the tensor rule is exact for polynomials whose degree in each variable is at most $2m - 1$. So if $q$ is a polynomial of total degree at most $p$ and $m \ge p + 1$, then $q \Psi_\alpha$ has degree at most $2p \le 2m - 2$ in each variable, and NISP returns the exact expansion. For a general $q = \sum_\beta c_\beta \Psi_\beta$, the computed coefficient is $\tilde c_\alpha = c_\alpha + \sum_{\beta \notin \Lambda} c_\beta\, Q_m[\Psi_\alpha \Psi_\beta]$, where $Q_m$ is the rule. The second term is the aliasing error. For uniform inputs and a continuous $q$, it tends to zero as $m$ grows, because Gauss rules on a bounded interval converge for every continuous integrand. The proof file proves the Golub-Welsch formulas, the exactness and the aliasing formula.

## Complexity

In the [real RAM](/real-ram/) model, line L1 costs $O(d m^3)$ with the Jacobi eigenvalue method of the reference code. The loop of lines L3 to L5 runs $m^d$ times, and each pass costs one model run $C$, $O(d p)$ for the one dimensional basis values, and $O(d P)$ for the products and sums. The total is $O(m^d (C + d P))$ time and $O(P + d m)$ extra space; the runs are not stored. In practice $C$ dominates everything else. With $m = p + 1$ and $d = 5$, $p = 4$, the tensor grid has 3125 nodes for 126 coefficients. [Sparse grid quadrature](/sparse-grid-quadrature/) reduces the node count to a number that grows only polynomially in $d$ for fixed accuracy level.

## Properties

- **Non-intrusive.** The model is a black box. Its existing solver runs unchanged at each node.
- **Exact for polynomials (theorem).** With $m \ge p + 1$, every polynomial in the span of $\Psi_\alpha$, $\alpha \in \Lambda$, is recovered exactly, and NISP is then a projection onto that span.
- **Embarrassingly parallel.** The $m^d$ runs are independent.
- **Deterministic.** No sampling error; the error is truncation plus aliasing.
- **Exponential convergence (theorem for analytic outputs).** For uniform inputs, if $q$ is analytic in a neighborhood of $[-1, 1]^d$, the quadrature error and the truncation error both decay exponentially in $m$ and $p$. For Gaussian inputs, the decay also needs growth conditions on $q$; the example above shows it for $e^{\xi}$.
- **Curse of dimensionality.** The tensor grid has $m^d$ nodes.

## Variants and improvements

- **Sparse grid projection.** Replace the tensor rule by a Smolyak [sparse grid](/sparse-grid-quadrature/). The direct use of a sparse quadrature in line L5 aliases even some coefficients inside the index set; Constantine, Eldred and Phipps showed that a combination of tensor projections, the sparse pseudospectral approximation method, avoids this.
- **Other input laws.** Gauss-Laguerre for gamma and Gauss-Jacobi for beta inputs, or rules built from the recurrence of an arbitrary law; see [generalized polynomial chaos](/generalized-polynomial-chaos/).
- **Nested rules.** Gauss-Kronrod-Patterson or Clenshaw-Curtis points reuse the runs of a coarse rule when the level rises.
- **Least squares instead of quadrature.** [Regression-based polynomial chaos](/regression-polynomial-chaos/) fits the coefficients to runs at random points and does not need a structured grid.
- **Anisotropic grids.** Different $m$ for inputs of different importance, chosen from a first coarse run.

## When to use it

Use NISP when the model is a black box, the number of inputs is small (up to about four with tensor grids, more with sparse grids), and the output is smooth in the inputs. It is the simplest way to get a polynomial chaos expansion from an existing code. Use [regression-based polynomial chaos](/regression-polynomial-chaos/) when the runs come from a given design or when the grid would be too large, [sparse polynomial chaos](/sparse-polynomial-chaos/) when only a few coefficients matter, and [stochastic collocation](/stochastic-collocation-method/) when you need an interpolating surrogate on a sparse grid. Use [Monte Carlo integration](/monte-carlo-integration/) when the output is not smooth, for example an indicator of failure.

## Pitfalls

- **Too few points for the degree.** With $m < p + 1$, the high coefficients are mostly aliasing. Keep $m \ge p + 1$, and check the size of the last coefficients.
- **A variance that is too large.** The variance from aliased coefficients can be larger than the true variance, as at $p = 4$ in the Ishigami example. A variance that falls as $m$ grows is a sign of aliasing.
- **Wrong weight convention.** To use a Gauss-Hermite table for the weight $e^{-x^2}$ with the standard normal law, multiply its nodes by $\sqrt{2}$ and its weights by $1/\sqrt{\pi}$. Without the change, the moments are wrong.
- **Non-smooth outputs.** A jump or a kink in $q$ makes the coefficients decay slowly, and the expansion shows Gibbs oscillations. Split the input domain or use a sampling method.
- **Dependent inputs.** The tensor rule and the product basis need independent inputs. Map dependent inputs to independent ones first, for example by a Rosenblatt or Nataf transform.

## Implementations

## History

Projection onto orthogonal polynomials by Gauss quadrature is classical numerical analysis; Golub and Welsch showed in 1969 how to compute the rules from the recurrence by an eigenvalue problem. In uncertainty quantification, the intrusive [stochastic Galerkin method](/stochastic-galerkin-method/) of Ghanem and Spanos came first. Reagan, Najm, Ghanem and Knio used the quadrature form in 2003 to propagate uncertain rate constants through reacting flow codes that could not be rewritten, and named it non-intrusive spectral projection. Sparse grid forms followed, and Constantine, Eldred and Phipps gave the sparse pseudospectral approximation method in 2012 to remove the aliasing of direct sparse quadrature.

## References
