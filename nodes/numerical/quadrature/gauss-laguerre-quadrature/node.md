---
tag: B0FCH8
kind: algorithm
slug: gauss-laguerre-quadrature
name: Gauss-Laguerre quadrature
aliases:
- Laguerre rule
- Gauss-Laguerre rule
- generalized Gauss-Laguerre quadrature
area: numerical/quadrature
level: advanced
summary: "Gaussian rule for integrals over [0, inf) with the weight x^a e^(-x). Exact for degree 2n-1 times the weight, it converges fast when the rest of the integrand grows at most like a polynomial."
solves: [numerical-integration]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes"}
  time: {worst: "O(n^2)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "n"}
properties: {deterministic: true, degree_of_precision: "2n-1", positive_weights: true, infinite_interval: true}
history:
  year: 1879
  people: [Edmond Laguerre, Gene H. Golub, John H. Welsch]
  note: Laguerre studied the polynomials orthogonal for e^(-x) on the half-line in 1879. Golub and Welsch (1969) gave the eigenvalue method that computes the rule for any n.
prereqs: [gaussian-quadrature]
see_also: [gauss-hermite-quadrature, gauss-jacobi-quadrature, improper-integration, golub-welsch-algorithm, gauss-quadrature-theorem, gauss-radau-quadrature, orthogonal-polynomials, tanh-sinh-quadrature]
sources:
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Chapter 1, Table 1.1 (recurrence coefficients of the generalized Laguerre weight) and Chapter 3, Section 3.1
  - paper: "Gene H. Golub and John H. Welsch, Calculation of Gauss quadrature rules, Mathematics of Computation 23(106) (1969) 221-230"
    locator: the eigenvalue method, with the Laguerre weight among the examples
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 3, integration over infinite intervals with Gauss-Laguerre rules
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.3 (Gaussian quadrature with the Laguerre weight)
---

Gauss-Laguerre quadrature is the [Gaussian quadrature](/gaussian-quadrature/) rule for the weight $w(x) = x^a e^{-x}$ on $(0, \infty)$, with $a > -1$ ($a = 0$ is the classical case). With $n$ nodes it integrates $f\,w$ exactly whenever $f$ is a polynomial of degree at most $2n - 1$, all weights are positive, and the nodes spread out to about $4n$. It is the natural rule for Laplace transforms, expectations of exponential and gamma random variables, and other integrals in which the exponential decay is explicit. When $f$ is smooth and grows at most like a polynomial, convergence is fast; when the integrand decays only algebraically, it is slow. This page computes the rule by the Golub-Welsch method in $O(n^2)$ operations, keeping the weights as logarithms because they underflow for large $n$.

## In plain words

Many integrals run from zero to infinity and contain a factor that dies off exponentially, like the probability that a lifetime exceeds some value. A Gauss-Laguerre rule builds that exponential decay into its design: it samples the rest of the integrand at a few well-chosen points, some close to zero and some far out, and adds the samples with weights that already account for the decay. If the rest of the integrand is smooth and does not grow too fast, a handful of points gives many correct digits. If the integrand does not really decay exponentially, the rule is a poor choice.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_0^\infty f(x)\,w(x)\,dx$, here with $w(x) = x^a e^{-x}$; $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$, where $n$ counts nodes; $E_n(f) = I(f) - Q_n(f)$; $d$ is the [degree of precision](/degree-of-precision/). The monic Laguerre polynomials satisfy $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k\pi_{k-1}$ with

$$\alpha_k = 2k + a + 1, \qquad \beta_0 = \Gamma(a + 1), \qquad \beta_k = k(k + a) \quad (k \ge 1).$$

Given $n \ge 1$ and $a > -1$, find nodes $0 < x_1 < \cdots < x_n$ and weights $w_i > 0$ with $d = 2n - 1$. Two derived uses: an integral $\int_0^\infty g(x)\,dx$ without an explicit weight is written as $\int_0^\infty e^{-x}\bigl(e^x g(x)\bigr)dx$, which gives the *modified weights* $w_i e^{x_i}$; and an integrand that decays like $e^{-cx}$ is matched by the substitution $x = t/c$.

## The algorithm

```pseudo id=main
GAUSS-LAGUERRE(n, a)
L1  if n < 1 or a ≤ −1 then error
L2  α_k ← 2k + a + 1, β_k ← k(k + a) for k < n; log β_0 ← log Γ(a + 1)
L3  J ← the n × n symmetric tridiagonal matrix with diagonal α_k and off-diagonal √β_k
L4  nodes ← eigenvalues of J by Sturm bisection, in increasing order
L5  for each node x_j: v_0 = 1, v follows the recurrence (rescaled when large); log w_j ← log β_0 − log |v|^2
L6  return the nodes and the log weights
```

Lines L3 to L5 are the [Golub-Welsch algorithm](/golub-welsch-algorithm/) with the eigenvectors produced by the three-term recurrence. The eigenvector components $v_k$ grow like $e^{x_j/2}$ at the largest nodes, so line L5 rescales $v$ by $10^{-100}$ whenever it exceeds $10^{100}$ and keeps the scale in a logarithm. The weights themselves are $\exp(\log w_j)$; the modified weights are $\exp(\log w_j + x_j)$, which never overflow when formed this way.

## Example

Take $a = 0$ and $n = 2$. Line L2 gives $\alpha_0 = 1$, $\alpha_1 = 3$, $\beta_0 = 1$, $\beta_1 = 1$. So

$$J = \begin{pmatrix} 1 & 1 \\ 1 & 3 \end{pmatrix}, \qquad \det(xI - J) = x^2 - 4x + 2, \qquad x_{1,2} = 2 \mp \sqrt2.$$

The eigenvector is $v = (1, x_j - 1)$, so $w_j = 1/(1 + (x_j - 1)^2)$:

| node | value | weight | closed form |
|---|---|---|---|
| $2 - \sqrt2$ | $0.5857864$ | $0.8535534$ | $\frac{2 + \sqrt2}{4}$ |
| $2 + \sqrt2$ | $3.4142136$ | $0.1464466$ | $\frac{2 - \sqrt2}{4}$ |

The rule reproduces $\int_0^\infty x^k e^{-x}dx = k!$ for $k \le 3$: for example $w_1 x_1^3 + w_2 x_2^3 = 6$. For $x^4$ it gives $20$ instead of $24$, and $E_2(x^4) = 4 = (2!)^2$, as the error formula below predicts.

Measured with $a = 0$:

| integral | value | $n = 4$ | $n = 16$ | $n = 64$ |
|---|---|---|---|---|
| $\int_0^\infty \frac{e^{-x}}{1 + x}dx$ | $0.5963473623$ | $3.0 \times 10^{-3}$ | $1.4 \times 10^{-6}$ | $1.8 \times 10^{-13}$ |
| $\int_0^\infty e^{-x}\cos x\,dx$ | $\frac12$ | $2.5 \times 10^{-3}$ | $4.2 \times 10^{-11}$ | rounding |
| $\int_0^\infty e^{-x}\sqrt{x}\,dx$ | $\frac{\sqrt\pi}{2}$ | $1.3 \times 10^{-2}$ | $1.6 \times 10^{-3}$ | $2.0 \times 10^{-4}$ |
| $\int_0^\infty e^{-x^2}dx$, modified weights | $\frac{\sqrt\pi}{2}$ | $3.9 \times 10^{-2}$ | $1.8 \times 10^{-4}$ | $9.1 \times 10^{-11}$ |
| $\int_0^\infty \frac{dx}{1 + x^2}$, modified weights | $\frac\pi2$ | $7.0 \times 10^{-2}$ | $1.7 \times 10^{-2}$ | $4.1 \times 10^{-3}$ |

The first row falls roughly like $e^{-4\sqrt n}$, faster than any power but not geometrically (an observation, not a theorem proved here). The square root at $0$ gives the rate $n^{-3/2}$; moved into the weight ($a = \frac12$), the same integral is exact with one node. The last row decays only algebraically and the rule converges like $n^{-1}$.

## Correctness

The weight has finite moments $\Gamma(k + a + 1)$, so the [Gauss quadrature theorem](/gauss-quadrature-theorem/) applies. The coefficients of line L2 come from the classical recurrence of the Laguerre polynomials after scaling to monic form. The eigenvalues of $J$ are the zeros of $\pi_n$, the orthonormality of the eigenvector matrix makes $\beta_0/\lvert v \rvert^2$ the Gauss weight, and the rescaling in line L5 multiplies $v$ by known constants, so the log weights are exact up to rounding. The details are in [the correctness proof](proofs/correctness.md).

**Error (proved).** If $f \in C^{2n}[0, \infty)$ with $\lvert f^{(2n)} \rvert \le M$, then

$$\lvert E_n(f) \rvert \le \frac{M\, n!\,\Gamma(n + a + 1)}{(2n)!}, \qquad\text{which for } a = 0 \text{ is } \frac{(n!)^2}{(2n)!}M \approx \sqrt{\pi n}\,4^{-n} M,$$

and $E_n(f) \ge 0$ if $f^{(2n)} \ge 0$. The bound is attained by $f = x^{2n}$. Many useful integrands, such as $1/(1 + x)$, have derivatives that grow like $(2n)!$, so the bound says little and the observed subgeometric rate is the honest guide.

## Complexity

- **Evaluations.** $n$, all in $(0, \infty)$, the largest near $4n$ (about $3.84n$ at $n = 200$; asymptotically $4n$).
- **Building the rule.** $O(n)$ per Sturm count, about 107 counts per node, $O(n)$ per weight: $O(n^2)$ operations, $\Theta(n)$ space. In pure Python $n = 200$ takes about $0.4$ seconds.
- **Underflow.** The smallest weight is about $e^{-x_n}$; for $n = 200$ its logarithm is $-764$, below the double-precision underflow threshold, so the weight is $0$ while its logarithm is still exact.

## Properties

- **Degree $2n - 1$** with respect to $x^a e^{-x}$; positive weights summing to $\Gamma(a + 1)$.
- **Nodes spread out.** The smallest node is about $\frac{j_{a,1}^2}{4n}$ (asymptotically, with $j_{a,1}$ the first zero of the Bessel function $J_a$), the largest about $4n$. A larger $n$ samples both closer to $0$ and much farther out.
- **Weights decay exponentially.** Only about the first half of the nodes carry weights above the rounding level of $e^{-x}$-type integrands; the rest contribute nothing in double precision.
- **The rule is not nested.** Rules for $n$ and $2n$ share no nodes, so an error estimate by comparison costs $3n$ evaluations.

## Variants and improvements

- **Generalized rules.** $a \ne 0$ absorbs an algebraic factor $x^a$ at the origin, as Gauss-Jacobi does on a finite interval; see [Gauss-Jacobi quadrature](/gauss-jacobi-quadrature/).
- **Scaling.** For $\int_0^\infty e^{-cx} f(x)\,dx$ substitute $x = t/c$. Matching $c$ to the true decay rate matters more than a large $n$.
- **Gauss-Laguerre-Radau.** Fixing the node $0$ gives degree $2n - 2$; see [Gauss-Radau quadrature](/gauss-radau-quadrature/).
- **Truncation plus a finite rule.** For integrands that are not exponentially decaying, truncate the interval or map $(0, \infty)$ to a finite one and use Gauss-Legendre or [tanh-sinh](/tanh-sinh-quadrature/); see [improper integration](/improper-integration/).
- **Large $n$.** Asymptotic and Newton-based methods compute nodes and weights in $O(n)$ operations, and only the nodes whose weights do not underflow need to be computed.

## When to use it

Use Gauss-Laguerre when the integrand is $e^{-cx}$ times a smooth function with at most polynomial growth on $(0, \infty)$: Laplace transforms, moments of exponential and gamma distributions, and radial integrals in physics. With $a \ne 0$ it also absorbs an $x^a$ factor at $0$. If the decay is algebraic, or the smooth factor oscillates or varies on a scale much smaller than $1/c$, use a mapping or subdivision instead.

## Pitfalls

- **Algebraic decay.** With modified weights, $\int_0^\infty \frac{dx}{1 + x^2}$ converges only like $n^{-1}$; the rule assumes exponential decay.
- **Overflow in modified weights.** Computing $w_i e^{x_i}$ as a product overflows to $\infty \cdot 0$ for large $n$; form it as $\exp(\log w_i + x_i)$.
- **The wrong decay rate.** For $e^{-10x}f(x)$ without rescaling, almost all nodes sit where the integrand is negligible, and accuracy is poor.
- **Endpoint behaviour in $f$.** A factor $\sqrt{x}$ or $\log x$ in $f$ costs the fast rate ($n^{-3/2}$ for $\sqrt{x}$); put algebraic factors into the weight via $a$.
- **Kinks inside the interval.** $\int_0^\infty e^{-x}\lvert x - 1 \rvert dx = \frac2e$ has errors $0.042$, $0.0058$, $0.0023$ for $n = 8, 32, 128$, not monotone in between; split the interval at the kink.
- **Large-$n$ cost.** Doubling $n$ to check accuracy moves the nodes to new places and wastes all previous evaluations.

## Implementations

## History

Edmond Laguerre studied the polynomials orthogonal for $e^{-x}$ on $(0, \infty)$ in 1879, in connection with continued fractions for $\int_x^\infty e^{-t}/t\,dt$; the generalized polynomials with the factor $x^a$ were introduced by Sonine. Tables of Gauss-Laguerre nodes and weights were computed for desk calculation in the mid-twentieth century, and Golub and Welsch (1969) turned the computation into a symmetric tridiagonal eigenvalue problem that handles any $n$.

## References
