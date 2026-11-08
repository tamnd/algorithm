---
tag: VYBGF4
kind: algorithm
slug: gauss-hermite-quadrature
name: Gauss-Hermite quadrature
aliases:
- Hermite rule
- Gauss-Hermite rule
area: numerical/quadrature
level: advanced
summary: "Gaussian rule for integrals over the real line with the weight e^(-x^2). It computes normal expectations with a few nodes when the integrand is smooth and grows at most polynomially."
solves: [numerical-integration]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes"}
  time: {worst: "O(n^2)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "n"}
properties: {deterministic: true, degree_of_precision: "2n-1", positive_weights: true, infinite_interval: true, symmetric: true}
history:
  year: 1864
  people: [Charles Hermite, Pafnuty Chebyshev, Gene H. Golub, John H. Welsch]
  note: Chebyshev (1859) and Hermite (1864) studied the polynomials orthogonal for e^(-x^2). Golub and Welsch (1969) gave the eigenvalue method that computes the rule for any n.
prereqs: [gaussian-quadrature]
see_also: [gauss-laguerre-quadrature, gauss-jacobi-quadrature, golub-welsch-algorithm, gauss-quadrature-theorem, improper-integration, monte-carlo-integration, sparse-grid-quadrature, orthogonal-polynomials]
sources:
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Chapter 1, Table 1.1 (recurrence coefficients of the Hermite weight) and Chapter 3, Section 3.1
  - paper: "Gene H. Golub and John H. Welsch, Calculation of Gauss quadrature rules, Mathematics of Computation 23(106) (1969) 221-230"
    locator: the eigenvalue method, with the Hermite weight among the examples
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 3, integration over infinite intervals with Gauss-Hermite rules
  - paper: "Alex Townsend, Thomas Trogdon and Sheehan Olver, Fast computation of Gauss quadrature nodes and weights on the whole real line, IMA Journal of Numerical Analysis 36(1) (2016) 337-358"
    locator: the O(n) method for large n
---

Gauss-Hermite quadrature is the [Gaussian quadrature](/gaussian-quadrature/) rule for the weight $w(x) = e^{-x^2}$ on the whole real line. With $n$ nodes it integrates $f\,w$ exactly whenever $f$ is a polynomial of degree at most $2n - 1$; the nodes are symmetric about $0$, lie within about $\pm\sqrt{2n}$, and all weights are positive. After the substitution $x = (X - \mu)/(\sqrt2\sigma)$ it computes expectations $\mathbb E[f(X)]$ for a normal random variable $X$, which is its main use in statistics, finance and uncertainty quantification. Convergence is fast when $f$ is smooth and grows at most like a polynomial, and slow for kinks, jumps and algebraically decaying integrands. This page computes the rule by the Golub-Welsch method in $O(n^2)$ operations, keeping the weights as logarithms because they underflow for large $n$.

## In plain words

Averages over a bell-curve distribution appear everywhere: expected payoffs, likelihoods with random effects, the spread of a model output when an input is uncertain. A Gauss-Hermite rule computes such an average from a few well-chosen sample points, placed symmetrically around the centre of the bell curve, with weights that already include the bell shape. If the quantity being averaged is smooth, a dozen points often give full accuracy. If it has a corner, like an option payoff, or does not fall off fast, many more points are needed.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_{-\infty}^\infty f(x)\,w(x)\,dx$, here with $w(x) = e^{-x^2}$; $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$, where $n$ counts nodes; $E_n(f) = I(f) - Q_n(f)$; $d$ is the [degree of precision](/degree-of-precision/). The monic Hermite polynomials satisfy $\pi_{k+1} = x\pi_k - \frac{k}{2}\pi_{k-1}$, that is

$$\alpha_k = 0, \qquad \beta_0 = \sqrt\pi, \qquad \beta_k = \frac{k}{2} \quad (k \ge 1).$$

Given $n \ge 1$, find nodes $x_1 < \cdots < x_n$ and weights $w_i > 0$ with $d = 2n - 1$. Two derived uses: for $X \sim N(\mu, \sigma^2)$,

$$\mathbb E[f(X)] = \frac{1}{\sqrt\pi}\int_{-\infty}^\infty e^{-x^2} f(\mu + \sqrt2\,\sigma x)\,dx \approx \frac{1}{\sqrt\pi}\sum_{i=1}^n w_i\, f(\mu + \sqrt2\,\sigma x_i),$$

and an integral $\int g\,dx$ without an explicit weight uses the *modified weights* $w_i e^{x_i^2}$.

## The algorithm

```pseudo id=main
GAUSS-HERMITE(n)
L1  if n < 1 then error
L2  α_k ← 0, β_k ← k/2 for k < n; log β_0 ← (1/2) log π
L3  J ← the n × n symmetric tridiagonal matrix with zero diagonal and off-diagonal √(k/2)
L4  nodes ← eigenvalues of J by Sturm bisection, in increasing order
L5  for each node x_j: v_0 = 1, v follows the recurrence (rescaled when large); log w_j ← log β_0 − log |v|^2
L6  symmetrize: average each pair (x_j, −x_(n+1−j)) and its log weights; set the middle node to 0 if n is odd
L7  return the nodes and the log weights
```

Lines L3 to L5 are the [Golub-Welsch algorithm](/golub-welsch-algorithm/) with eigenvectors from the three-term recurrence. Line L5 rescales $v$ by $10^{-100}$ whenever it exceeds $10^{100}$, so a weight below the underflow threshold still has a correct logarithm. Line L6 uses the symmetry of the exact rule: averaging cannot make either computed value worse, and it makes odd integrands integrate to exactly $0$.

## Example

Take $n = 3$. Line L2 gives $\beta_1 = \frac12$, $\beta_2 = 1$. So

$$J = \begin{pmatrix} 0 & \sqrt{1/2} & 0 \\ \sqrt{1/2} & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}, \qquad \det(xI - J) = x^3 - \tfrac32 x, \qquad x \in \{0, \pm\sqrt{3/2}\}.$$

The eigenvector recurrence gives $v_0 = 1$, $v_1 = \sqrt2\,x$ and $v_2 = \sqrt2\,x^2 - \sqrt{1/2}$:

| node | $v$ | $\lvert v \rvert^2$ | weight $\sqrt\pi/\lvert v \rvert^2$ |
|---|---|---|---|
| $0$ | $(1, 0, -1/\sqrt2)$ | $\frac32$ | $\frac{2\sqrt\pi}{3} = 1.1816359$ |
| $\pm\sqrt{3/2}$ | $(1, \pm\sqrt3, \sqrt2)$ | $6$ | $\frac{\sqrt\pi}{6} = 0.2954090$ |

For $X \sim N(0, 1)$ this rule gives $\mathbb E[X^4] = \frac{1}{\sqrt\pi}\cdot 2\cdot\frac{\sqrt\pi}{6}\cdot(\sqrt2\sqrt{3/2})^4 = 3$, exact, since degree $4 \le 2n - 1$. For $x^6$ the error is $E_3(x^6) = \frac{\sqrt\pi\,3!}{2^3} = \frac{3\sqrt\pi}{4}$, as the error formula below predicts.

Measured:

| integral | value | $n = 8$ | $n = 32$ | $n = 128$ |
|---|---|---|---|---|
| $\int e^{-x^2}\frac{1}{1 + x^2}dx$ | $\pi e\,\mathrm{erfc}(1)$ | $4.1 \times 10^{-3}$ | $1.6 \times 10^{-6}$ | $2.0 \times 10^{-13}$ |
| $\int e^{-x^2}\cos 5x\,dx$ | $\sqrt\pi e^{-25/4}$ | $0.10$ | rounding | rounding |
| $\int e^{-x^2}\lvert x \rvert dx$ | $1$ | $5.4 \times 10^{-2}$ | $1.3 \times 10^{-2}$ | $3.2 \times 10^{-3}$ |
| $\int \frac{dx}{1 + x^4}$, modified weights | $\frac{\pi}{\sqrt2}$ | $2.2 \times 10^{-2}$ | $1.5 \times 10^{-3}$ | $1.7 \times 10^{-4}$ |

$\mathbb E[e^Z]$ for $Z \sim N(0, 1)$ has error $7.5 \times 10^{-4}$ at $n = 4$, $2.4 \times 10^{-9}$ at $n = 8$ and is at rounding level at $n = 16$. The first row falls roughly like $e^{-2.8\sqrt n}$ (observed), the kink $\lvert x \rvert$ like $n^{-1}$. For $\cos 5x$ the rule is useless until the nodes resolve the oscillation (error $2.4 \times 10^{-6}$ at $n = 16$).

## Correctness

The weight has finite moments, so the [Gauss quadrature theorem](/gauss-quadrature-theorem/) applies. The coefficients of line L2 come from the recurrence $H_{k+1} = 2xH_k - 2kH_{k-1}$ of the Hermite polynomials after division by the leading coefficient $2^{k+1}$. The eigenvalues of $J$ are the zeros of $\pi_n$, and the orthonormality of the eigenvector matrix makes $\sqrt\pi/\lvert v \rvert^2$ the Gauss weight. Since $\pi_n(-x) = (-1)^n\pi_n(x)$, the exact rule is symmetric, so the averaging of line L6 does not increase the error. The details are in [the correctness proof](proofs/correctness.md).

**Error (proved).** If $f \in C^{2n}(\mathbb R)$ with $\lvert f^{(2n)} \rvert \le M$, then

$$\lvert E_n(f) \rvert \le \frac{\sqrt\pi\,n!}{2^n\,(2n)!}\,M,$$

and $E_n(f) \ge 0$ when $f^{(2n)} \ge 0$; $f = x^{2n}$ attains the bound. For integrands such as $1/(1 + x^2)$, whose derivatives grow like $(2n)!$, the bound is useless, and convergence is subgeometric; the observed $e^{-c\sqrt n}$ behaviour is a measurement, not a theorem proved here.

## Complexity

- **Evaluations.** $n$, symmetric about $0$, the largest near $\sqrt{2n}$ (19.34 at $n = 200$, against $\sqrt{401} = 20.02$; asymptotically $\sqrt{2n}$).
- **Building the rule.** $O(n)$ per Sturm count, about 107 counts per node, $O(n)$ per weight: $O(n^2)$ operations, $\Theta(n)$ space. In pure Python $n = 200$ takes about $0.12$ seconds. Townsend, Trogdon and Olver (2016) give an $O(n)$ method for large $n$.
- **Underflow.** The extreme weights are about $e^{-x_n^2}$; at $n = 200$ the log weight is $-374.5$, and at $n = 400$ it is $-767$, below the underflow threshold, so those weights are $0$ in double precision while their logarithms are exact.
- **Dimension.** In $d$ dimensions a tensor product needs $n^d$ evaluations; [sparse grids](/sparse-grid-quadrature/) or [Monte Carlo](/monte-carlo-integration/) take over for large $d$.

## Properties

- **Degree $2n - 1$** with respect to $e^{-x^2}$; positive weights summing to $\sqrt\pi$.
- **Symmetry.** Nodes are symmetric, weights equal in pairs, and $0$ is a node exactly when $n$ is odd.
- **Not nested.** Rules for different $n$ share at most the node $0$, so comparing $n$ with $2n$ costs $3n$ evaluations.
- **Nodes spread like $\sqrt{2n}$.** The spacing near $0$ is about $\pi/\sqrt{2n}$, so resolving an oscillation $\cos \omega x$ needs $n$ of order $\omega^2/2$ (a heuristic; at $\omega = 5$ the error is $0.10$ at $n = 8$ and $2.4 \times 10^{-6}$ at $n = 16$).
- **Probabilists' form.** For the weight $e^{-x^2/2}/\sqrt{2\pi}$ the nodes are $\sqrt2$ times these and the weights are divided by $\sqrt\pi$.

## Variants and improvements

- **Shifted and scaled rules.** For a likelihood or posterior that peaks at $\hat\mu$ with curvature $\hat\sigma$, centre the rule there (adaptive Gauss-Hermite quadrature, as used for generalized linear mixed models). This matters far more than a larger $n$.
- **Gauss-Laguerre and Gauss-Jacobi.** The analogues on the half-line and on a finite interval; see [Gauss-Laguerre](/gauss-laguerre-quadrature/) and [Gauss-Jacobi](/gauss-jacobi-quadrature/).
- **Generalized Hermite weights.** $\lvert x \rvert^{2\gamma} e^{-x^2}$ with $\gamma > -\frac12$ has $\beta_k = \frac{k}{2}$ for even $k$ and $\frac{k}{2} + \gamma$ for odd $k$, and the same eigen-solver applies.
- **Sparse grids and Smolyak rules.** In several dimensions, nested Gauss-Hermite-like rules (Genz-Keister) are combined on [sparse grids](/sparse-grid-quadrature/).
- **Truncated trapezoidal rule.** For entire integrands with Gaussian decay, the equispaced trapezoidal rule on the real line converges geometrically too and is nested; see [trapezoidal rule](/trapezoidal-rule/).

## When to use it

Use Gauss-Hermite for expectations of smooth functions of normal random variables and for integrals over the real line with explicit Gaussian decay: moments, likelihood integrals with normal random effects, stochastic collocation, the expected value of smooth model outputs. For integrands with kinks or jumps (option payoffs, indicator functions) split the integral at the kink, or use a smoothed form; for heavy tails use a mapping to a finite interval instead.

## Pitfalls

- **Kinks and jumps.** The call payoff $\mathbb E[\max(Z - 1, 0)] = 0.0833\ldots$ has errors $8.4 \times 10^{-3}$, $7.1 \times 10^{-4}$, $9.6 \times 10^{-4}$ for $n = 12, 50, 200$, not even monotone; split at the kink $Z = 1$ and use a rule on each half-line.
- **Wrong centre or scale.** If $f$ varies on a scale far from $1$ or is centred far from $0$, most nodes are wasted. Shift and scale first.
- **The $\sqrt2$ factor.** For $N(\mu, \sigma^2)$ the substitution is $\mu + \sqrt2\,\sigma x_i$, and the sum is divided by $\sqrt\pi$; forgetting either gives a wrong answer without a warning.
- **Modified weights.** $w_i e^{x_i^2}$ computed as a product overflows to $\infty\cdot 0$ for large $n$; form it as $\exp(\log w_i + x_i^2)$. With modified weights, algebraically decaying integrands such as $1/(1 + x^4)$ converge slowly.
- **Fast growth.** If $f$ grows like $e^{c x^2}$ with $c \ge 1$, the integral diverges and the rule returns a finite number anyway.
- **Large $n$ does not help much.** The extreme nodes carry negligible weight; for $n$ above a few hundred, most of the work goes into nodes whose weights underflow.

## Implementations

## History

The polynomials orthogonal for $e^{-x^2}$ were studied by Laplace in probability, by Chebyshev in 1859 and by Hermite in 1864, whose name they carry. Gauss-Hermite rules became standard tools for normal expectations once tables were available in the mid-twentieth century. Golub and Welsch (1969) computed them as the eigenvalues and eigenvector components of the Jacobi matrix, and Townsend, Trogdon and Olver (2016) gave an $O(n)$ asymptotic method for very large $n$.

## References
