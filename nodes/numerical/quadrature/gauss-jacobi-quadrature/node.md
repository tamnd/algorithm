---
tag: 47J4QB
kind: algorithm
slug: gauss-jacobi-quadrature
name: Gauss-Jacobi quadrature
aliases:
- Jacobi rule
- Gauss-Jacobi rule
area: numerical/quadrature
level: advanced
summary: "Gaussian rule for weights (1-x)^a (1+x)^b on [-1,1], with a, b > -1. The weight absorbs algebraic endpoint singularities, so smooth factors converge fast; Legendre and Chebyshev are special cases."
solves: [numerical-integration]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes"}
  time: {worst: "O(n^2)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "n"}
properties: {deterministic: true, degree_of_precision: "2n-1", positive_weights: true, open: true}
history:
  year: 1859
  people: [Carl Gustav Jacob Jacobi, Elwin Bruno Christoffel, Gene H. Golub, John H. Welsch]
  note: Jacobi linked Gauss's rule to orthogonal polynomials in 1826, and the polynomials for the weight (1-x)^a (1+x)^b carry his name from his 1859 posthumous paper. Golub and Welsch (1969) gave the eigenvalue method.
prereqs: [gaussian-quadrature]
see_also: [gauss-legendre-quadrature, golub-welsch-algorithm, gauss-quadrature-theorem, gauss-radau-quadrature, gauss-lobatto-quadrature, improper-integration, chebyshev-nodes, orthogonal-polynomials]
sources:
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Chapter 1, Table 1.1 (recurrence coefficients of the classical weights, Jacobi case) and Chapter 3, Section 3.1
  - paper: "Gene H. Golub and John H. Welsch, Calculation of Gauss quadrature rules, Mathematics of Computation 23(106) (1969) 221-230"
    locator: the eigenvalue method and its tables for the Jacobi weight
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, the section on Gauss-Jacobi rules and Chapter 3 on singular integrands
  - url: https://doi.org/10.1137/120889873
    title: "Nicholas Hale and Alex Townsend, Fast and accurate computation of Gauss-Legendre and Gauss-Jacobi quadrature nodes and weights, SIAM Journal on Scientific Computing 35(2) (2013) A652-A674"
    locator: the O(n) asymptotic method for large n
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 19 (Clenshaw-Curtis and Gauss quadrature)
---

Gauss-Jacobi quadrature is the [Gaussian quadrature](/gaussian-quadrature/) rule for the weight $w(x) = (1 - x)^a (1 + x)^b$ on $(-1, 1)$ with $a, b > -1$. With $n$ nodes it integrates $f\,w$ exactly whenever $f$ is a polynomial of degree at most $2n - 1$, all weights are positive, and no node lies at an endpoint. Its main use is the integral of a smooth function times an algebraic endpoint singularity such as $x^{-1/2}$ or $\sqrt{1 - x}$: the singular factor goes into the weight, and the rule converges as fast as Gauss-Legendre does on a smooth integrand. The cases $a = b = 0$ (Legendre) and $a = b = \pm\frac12$ (Chebyshev) are special cases. This page computes the rule from the explicit recurrence coefficients by the Golub-Welsch method, in $O(n^2)$ operations.

## In plain words

Some integrands are smooth except for a factor that blows up or has an infinite slope at an end of the interval, like one over a square root. Ordinary rules converge very slowly on such integrands, because the singular factor is not like a polynomial. Gauss-Jacobi rules treat that factor as part of the problem: the sample points and weights are designed for it, and only the smooth remaining factor is sampled. The result converges as fast as if the singularity were not there. The price is that each kind of singularity needs its own rule.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_{-1}^1 f(x)\,w(x)\,dx$, here with $w(x) = (1 - x)^a (1 + x)^b$; $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$, where $n$ counts nodes; $E_n(f) = I(f) - Q_n(f)$; $d$ is the [degree of precision](/degree-of-precision/). The monic Jacobi polynomials satisfy $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k\pi_{k-1}$ with $\beta_0 = \int w$.

Given $n \ge 1$ and $a, b > -1$, find nodes $x_1 < \cdots < x_n$ in $(-1, 1)$ and weights $w_i$ with $d = 2n - 1$. On an interval $[l, r]$ the affine map gives

$$\int_l^r (r - x)^a (x - l)^b f(x)\,dx = \Bigl(\frac{r - l}{2}\Bigr)^{a+b+1} \sum_{i=1}^n w_i\, f\Bigl(l + \frac{r - l}{2}(x_i + 1)\Bigr).$$

The recurrence coefficients are known in closed form: $\beta_0 = 2^{a+b+1}\frac{\Gamma(a+1)\Gamma(b+1)}{\Gamma(a+b+2)}$, $\alpha_0 = \frac{b - a}{a + b + 2}$, $\beta_1 = \frac{4(a+1)(b+1)}{(a+b+2)^2(a+b+3)}$, and for larger $k$

$$\alpha_k = \frac{b^2 - a^2}{(2k + a + b)(2k + a + b + 2)}, \qquad \beta_k = \frac{4k(k + a)(k + b)(k + a + b)}{(2k + a + b)^2(2k + a + b + 1)(2k + a + b - 1)}.$$

## The algorithm

```pseudo id=main
GAUSS-JACOBI(n, a, b)
L1  if n < 1 or a ≤ −1 or b ≤ −1 then error
L2  α_k, β_k ← the closed forms above for k < n, with α_0, β_0, β_1 from their own formulas
L3  J ← the n × n symmetric tridiagonal matrix with diagonal α_k and off-diagonal √β_k
L4  nodes ← eigenvalues of J by Sturm bisection, in increasing order
L5  for each node x_j: v_0 = 1, v follows the recurrence (rescaled when large); log w_j ← log β_0 − log |v|^2
L6  return the nodes and w_j = exp(log w_j)
```

Line L2 uses separate formulas for $\alpha_0$ and $\beta_1$ because the general ones have the factors $a + b$ and $a + b + 1$ in both numerator and denominator, which vanish for the Legendre and Chebyshev cases; $\beta_0$ is computed with `lgamma` so that large $a, b$ do not overflow. Lines L3 to L5 are the [Golub-Welsch algorithm](/golub-welsch-algorithm/) with the eigenvectors produced by the three-term recurrence; working with $\log w_j$ keeps very small weights near the endpoints from turning into $0/\infty$.

## Example

Take $a = 0$, $b = 1$, the weight $1 + x$, and $n = 2$. Line L2 gives $\beta_0 = 2$, $\alpha_0 = \frac13$, $\alpha_1 = \frac{1}{15}$, $\beta_1 = \frac29$. So

$$J = \begin{pmatrix} 1/3 & \sqrt2/3 \\ \sqrt2/3 & 1/15 \end{pmatrix}, \qquad \det(xI - J) = x^2 - \tfrac25 x - \tfrac15,$$

with zeros $x_{1,2} = \frac{1 \mp \sqrt6}{5}$. The eigenvector is $v = \bigl(1, \frac{3(x_j - 1/3)}{\sqrt2}\bigr)$, so $w_j = 2/(1 + \frac92(x_j - \frac13)^2)$:

| node | value | weight | closed form |
|---|---|---|---|
| $\frac{1 - \sqrt6}{5}$ | $-0.2898979$ | $0.7278345$ | $1 - \frac{\sqrt6}{9}$ |
| $\frac{1 + \sqrt6}{5}$ | $0.6898979$ | $1.2721655$ | $1 + \frac{\sqrt6}{9}$ |

The rule is exact for $(1 + x)f$ with $f$ a cubic: for example $\int_{-1}^1 (1 + x)x^2\,dx = \frac23$, and $w_1 x_1^2 + w_2 x_2^2 = \frac23$. These nodes are the free nodes of the three-point [Gauss-Radau](/gauss-radau-quadrature/) rule with the node $-1$: the Radau construction factors out exactly the weight $1 + x$.

Measured: $\int_0^1 x^{-1/2} e^x\,dx = 2.9253034918\ldots$ with $a = 0$, $b = -\frac12$ has errors $1.3 \times 10^{-1}$, $7.6 \times 10^{-4}$, $1.6 \times 10^{-6}$, $1.9 \times 10^{-9}$ for $n = 1, 2, 3, 4$ and is at rounding level by $n = 6$. Gauss-Legendre applied to the whole integrand $x^{-1/2} e^x$ has errors $0.19$, $0.053$, $0.013$, $0.0034$ for $n = 4, 16, 64, 256$, the rate $n^{-1}$. With $a = b = -\frac12$, $\int_{-1}^1 \frac{\cos x}{\sqrt{1 - x^2}}dx = \pi J_0(1)$ has error $5.9 \times 10^{-7}$ at $n = 4$ and $3 \times 10^{-12}$ at $n = 6$.

## Correctness

The weight is positive with finite moments because $a, b > -1$, so the [Gauss quadrature theorem](/gauss-quadrature-theorem/) applies. The coefficients $\alpha_0$ and $\beta_1$ are the mean and variance of $x = 2t - 1$ for $t$ Beta-distributed, $\beta_0$ is a Beta integral, and the others follow from Szegő's three-term recurrence for $P_m^{(a,b)}$ by dividing by the leading coefficients. The eigenvalues of $J$ are the zeros of $\pi_n$, and the orthonormality of the eigenvector matrix shows that $\beta_0/\lvert v \rvert^2$ is the Gauss weight. The details are in [the correctness proof](proofs/correctness.md).

**Error (proved).** For $f \in C^{2n}[-1, 1]$,

$$E_n(f) = \frac{f^{(2n)}(\xi)}{(2n)!}\,\beta_0\beta_1\cdots\beta_n, \qquad \beta_0\cdots\beta_n = \frac{2^{2n+a+b+1}\,n!\,\Gamma(n+a+1)\Gamma(n+b+1)\Gamma(n+a+b+1)}{(2n+a+b+1)\,\Gamma(2n+a+b+1)^2}.$$

The hypothesis is on $f$ only, not on $f\,w$. **Rate (proved, for analytic $f$).** If $f$ is analytic inside the Bernstein ellipse $E_\rho$, the error decays like $\rho^{-2n}$ up to a constant, by the same argument as for Gauss-Legendre: $E_n$ vanishes on polynomials of degree $2n - 1$, the weights are positive with sum $\beta_0$, so $\lvert E_n(f) \rvert \le 2\beta_0 \inf_{\deg p \le 2n-1} \lVert f - p \rVert_\infty$, and Chebyshev truncation bounds the best approximation.

## Complexity

- **Evaluations.** $n$, none at the endpoints, so the integrand may be undefined there.
- **Building the rule.** $O(n)$ for the coefficients, $O(n)$ per Sturm count with about 107 counts per node, and $O(n)$ per weight: $O(n^2)$ operations and $\Theta(n)$ space. In pure Python $n = 200$ takes about $0.12$ seconds.
- **Large $n$.** Hale and Townsend (2013) compute nodes and weights in $O(n)$ operations from asymptotic expansions with Newton refinement, accurate to near machine precision.

## Properties

- **Degree $2n - 1$** with respect to the weight $w$; the rule is open.
- **Positive weights** summing to $\beta_0$; convergence for every continuous $f$, and no amplification of rounding errors in $f$ beyond a factor $\beta_0$.
- **Symmetry.** For $a = b$ the nodes are symmetric about $0$ and $\alpha_k = 0$; swapping $a$ and $b$ mirrors the rule.
- **Closed forms.** $a = b = -\frac12$: nodes $\cos\frac{(2j-1)\pi}{2n}$, weights $\frac{\pi}{n}$. $a = b = \frac12$: nodes $\cos\frac{j\pi}{n+1}$, weights $\frac{\pi}{n+1}\sin^2\frac{j\pi}{n+1}$.
- **Relation to Radau and Lobatto.** The free nodes of a Legendre-Radau rule are the Gauss-Jacobi nodes with $(a, b) = (0, 1)$ or $(1, 0)$; the interior Legendre-Lobatto nodes are those with $a = b = 1$.

## Variants and improvements

- **Generalized Gauss-Laguerre and Gauss-Hermite.** The analogous rules for singular weights on infinite intervals; see [Gauss-Laguerre](/gauss-laguerre-quadrature/) and [Gauss-Hermite](/gauss-hermite-quadrature/).
- **Gauss-Jacobi-Radau and -Lobatto rules.** The modified-matrix constructions of the Radau and Lobatto pages work with these coefficients.
- **Logarithmic weights.** For $\log x$ singularities there is no classical recurrence; the coefficients are computed numerically from modified moments (Gautschi, Chapter 2) and then the same eigen-solver applies.
- **Asymptotic methods.** Newton's method on $P_n^{(a,b)}$ evaluated by the recurrence costs $O(n^2)$; with asymptotic expansions (Hale and Townsend) it is $O(n)$.

## When to use it

Use Gauss-Jacobi when the integrand is a smooth function times known powers $(1 - x)^a (1 + x)^b$, such as $\int_0^1 x^{-1/2} g(x)\,dx$ or integrals with square-root edges in fracture mechanics and potential theory. If the exponents are unknown or the singularity is logarithmic, use a variable transformation, [tanh-sinh quadrature](/tanh-sinh-quadrature/), or adaptive subdivision toward the endpoint; see [improper integration](/improper-integration/).

## Pitfalls

- **Putting the singular factor in $f$.** If the weight is $1$ and $f$ carries $x^{-1/2}$, the rule is Gauss-Legendre and converges like $n^{-1}$. The exponents must match the singularity.
- **The wrong side.** In $(1 - x)^a (1 + x)^b$ the exponent $a$ belongs to the right end $x = 1$. Mixing them up integrates the wrong function, without any warning.
- **Exponents near $-1$.** As $a \to -1$ the weight is barely integrable, $\beta_0$ grows like $1/(a + 1)$, and the weight concentrates at the endpoint; the rule stays correct but relative accuracy depends on how $f$ behaves there.
- **Overflow in $\Gamma$ ratios.** Computing $\beta_0$ with `gamma` instead of `lgamma` overflows for $a + b$ above about $170$.
- **Reversed intervals.** $(r - x)^a$ is not defined for $x > r$, so the mapped rule needs $l \le r$; the code raises an error rather than guessing a sign.
- **Error estimates.** A single rule gives no error estimate; compare $n$ and $2n$ or use an adaptive method.

## Implementations

## History

Jacobi (1826) recognised that the nodes of Gauss's rule are the zeros of the Legendre polynomials, and the polynomials orthogonal with respect to $(1 - x)^a (1 + x)^b$ are named after him, from a paper published posthumously in 1859. Christoffel (1858) extended Gauss's construction to general weights and gave the weight formula that bears his name. Golub and Welsch (1969) computed the nodes and weights as eigenvalues and eigenvector components of the Jacobi matrix, which remains the standard method for moderate $n$, and Hale and Townsend (2013) gave an $O(n)$ asymptotic method for large $n$.

## References
