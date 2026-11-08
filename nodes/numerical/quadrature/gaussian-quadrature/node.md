---
tag: CMS5QF
kind: algorithm
slug: gaussian-quadrature
name: Gaussian quadrature
aliases:
- Gauss quadrature
- Gauss-type quadrature
- Gauss-Christoffel quadrature
area: numerical/quadrature
level: advanced
summary: An n-point rule whose nodes are the zeros of the orthogonal polynomial of the weight, with positive weights, exact to degree 2n-1. Built here from the three-term recurrence.
solves: [numerical-integration, gauss-nodes-and-weights]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes"}
  time: {worst: "O(n^2)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "n"}
properties: {deterministic: true, degree_of_precision: "2n-1", positive_weights: true, nested: false, needs_recurrence_coefficients: true}
history:
  year: 1814
  people: [Carl Friedrich Gauss, Carl Gustav Jacob Jacobi, Elwin Bruno Christoffel, Gene H. Golub, John H. Welsch, Walter Gautschi]
  note: Gauss found the rules for w = 1 in 1814. Jacobi proved them by orthogonality in 1826 and Christoffel extended them to general weights in 1858. Golub and Welsch (1969) turned the computation into a tridiagonal eigenproblem.
prereqs: [gauss-quadrature-theorem, orthogonal-polynomials]
see_also: [gauss-legendre-quadrature, golub-welsch-algorithm, gauss-nodes-and-weights, gauss-kronrod-quadrature, clenshaw-curtis-quadrature, sturm-sequence-eigenvalue-count, tridiagonal-eigenproblem, legendre-polynomials]
sources:
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Chapter 1, Section 1.4 (Gauss-type quadrature rules); Chapter 3, Section 3.1 (computation of Gauss-type rules from the Jacobi matrix); Chapter 2 for computing the recurrence coefficients
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, the section on integration rules of Gauss type (Section 2.7), and Chapter 3 for the Gauss-Laguerre and Gauss-Hermite rules
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 19, Clenshaw-Curtis and Gauss quadrature (convergence for analytic and for differentiable integrands)
  - paper: "Gene H. Golub and John H. Welsch, Calculation of Gauss quadrature rules, Mathematics of Computation 23 (1969) 221-230"
    locator: the Jacobi matrix, its eigenvalues as nodes and the first eigenvector components as weights
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 10, Numerical integration II (Gauss quadrature, its error and its convergence)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.3, Gaussian numerical integration
  - paper: "Nicholas Hale and Alex Townsend, Fast and accurate computation of Gauss-Legendre and Gauss-Jacobi quadrature nodes and weights, SIAM Journal on Scientific Computing 35(2) (2013) A652-A674"
    locator: Newton iteration with asymptotic initial guesses, O(n) work for all n nodes
---

Gaussian quadrature approximates $I(f) = \int_a^b f(x)\,w(x)\,dx$ by $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$, with the $n$ nodes at the zeros of the degree-$n$ [orthogonal polynomial](/orthogonal-polynomials/) of the weight function $w$ and with weights that make the rule interpolatory. By the [Gauss quadrature theorem](/gauss-quadrature-theorem/) the rule is exact for all polynomials of degree at most $2n - 1$, which is the most any $n$-point rule can reach, and its weights are positive. This page computes the rule for any weight from the three-term recurrence of its orthogonal polynomials, with [Sturm-count bisection](/sturm-sequence-eigenvalue-count/) for the nodes and the Christoffel formula for the weights, in $O(n^2)$ operations. For a smooth $f$ the error falls geometrically in $n$.

## In plain words

A quadrature rule samples a function at a few points and adds up the samples with weights. If the points are fixed in advance, as in the trapezoidal or Simpson rules, the weights alone can make the rule exact for polynomials up to about the number of points. Gaussian quadrature also chooses the points, and that doubles the reach: with $n$ points it is exact up to degree $2n - 1$. The best points are the roots of a special polynomial that depends on the integral being computed. The method finds those roots, computes the weights, and then the integral costs only $n$ function values. For smooth functions a few dozen points often give full machine accuracy.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,w(x)\,dx$; $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$, where $n$ always counts nodes; $E_n(f) = I(f) - Q_n(f)$; $d$ is the [degree of precision](/degree-of-precision/). The weight function is $w$, and the Gauss weights are $w_i$ (written $\lambda_i$ in the proofs).

The weight $w \ge 0$ on $(a, b)$ (finite or infinite) must be positive on a set of positive measure and have finite moments. It enters only through the coefficients of the recurrence of its monic orthogonal polynomials,

$$\pi_{k+1}(x) = (x - \alpha_k)\,\pi_k(x) - \beta_k\,\pi_{k-1}(x), \qquad \pi_0 = 1,\ \pi_{-1} = 0,$$

with $\beta_k > 0$ and the convention $\beta_0 = \int_a^b w$. The input is $n \ge 1$ and $\alpha_0, \ldots, \alpha_{n-1}$, $\beta_0, \ldots, \beta_{n-1}$. The output is the nodes $x_1 < \cdots < x_n$ and the weights $w_1, \ldots, w_n$ of the Gauss rule; applying the rule to $f$ then costs $n$ evaluations.

| weight $w$ | interval | $\alpha_k$ | $\beta_0$ | $\beta_k$, $k \ge 1$ | rule |
|---|---|---|---|---|---|
| $1$ | $[-1, 1]$ | $0$ | $2$ | $k^2/(4k^2 - 1)$ | [Gauss-Legendre](/gauss-legendre-quadrature/) |
| $(1 - x^2)^{-1/2}$ | $[-1, 1]$ | $0$ | $\pi$ | $\tfrac12$ for $k = 1$, else $\tfrac14$ | Gauss-Chebyshev |
| $(1 - x)^{\alpha}(1 + x)^{\beta}$ | $[-1, 1]$ | see the page | | | [Gauss-Jacobi](/gauss-jacobi-quadrature/) |
| $x^{a} e^{-x}$ | $[0, \infty)$ | $2k + a + 1$ | $\Gamma(a + 1)$ | $k(k + a)$ | [Gauss-Laguerre](/gauss-laguerre-quadrature/) |
| $e^{-x^2}$ | $(-\infty, \infty)$ | $0$ | $\sqrt{\pi}$ | $k/2$ | [Gauss-Hermite](/gauss-hermite-quadrature/) |

For a nonclassical weight, the coefficients can be computed from moments or from a discretization of $w$ (Gautschi, Chapter 2); that step is outside this page.

## The algorithm

Let $J_n$ be the symmetric tridiagonal Jacobi matrix with diagonal $\alpha_0, \ldots, \alpha_{n-1}$ and off-diagonal $\sqrt{\beta_1}, \ldots, \sqrt{\beta_{n-1}}$. Its characteristic polynomial is $\pi_n$, so its eigenvalues are the nodes. $\mathrm{COUNT}(x)$ is the number of eigenvalues below $x$: it is the number of negative values among $d_0 = \alpha_0 - x$, $d_k = \alpha_k - x - \beta_k/d_{k-1}$. The orthonormal polynomials $p_k$ satisfy $p_0 = 1/\sqrt{\beta_0}$ and $\sqrt{\beta_{k+1}}\,p_{k+1} = (x - \alpha_k)p_k - \sqrt{\beta_k}\,p_{k-1}$.

```pseudo id=main
GAUSS(α, β, n)                              ▷ n ≥ 1, β_0 = ∫w, β_k > 0
L1  if n < 1 or some β_k ≤ 0 then error
L2  [lo, hi] ← the Gershgorin interval of J_n
L3  for j ← 1 to n do
L4      (l, r) ← (max(lo, x_(j−1)), hi)           ▷ x_0 means lo
L5      while r − l is above the floating-point resolution do
L6          m ← (l + r)/2
L7          if COUNT(m) ≥ j then r ← m else l ← m
L8      x_j ← (l + r)/2
L9      compute p_0(x_j), …, p_(n−1)(x_j) by the recurrence
L10     w_j ← 1 / Σ_k p_k(x_j)^2                   ▷ Christoffel formula, summed with fsum
L11 return (x_1, …, x_n), (w_1, …, w_n)
```

Line L2 gives an interval that holds every eigenvalue, so $\mathrm{COUNT}(lo) = 0$ and $\mathrm{COUNT}(hi) = n$. Lines L5 to L7 keep $\mathrm{COUNT}(l) < j \le \mathrm{COUNT}(r)$, so the $j$-th node stays in $[l, r)$ while the bracket halves. The loop stops when the width is below $4u\max(|l|, |r|)$ or below $u^2(hi - lo)$, with $u = 2^{-53}$; the second test bounds the work by 107 counts per node and handles a node at $0$. Line L4 starts each search at the previous node, since the nodes are found in increasing order. Lines L9 and L10 use the identity $\sum_{k<n} p_k(x_j)^2 = 1/w_j$, which holds because the rule is exact on all products $p_k p_m$ with $k, m < n$. To integrate over $[a, b]$ with $w = 1$, map the Gauss-Legendre rule by $x \mapsto \tfrac{a+b}{2} + \tfrac{b-a}{2}x$ and multiply the weights by $\tfrac{b-a}{2}$; this also covers $b < a$ and gives $0$ for $a = b$.

## Example

Take $w = 1$ on $[-1, 1]$ and $n = 3$. The coefficients are $\alpha_k = 0$, $\beta_0 = 2$, $\beta_1 = \tfrac13$, $\beta_2 = \tfrac{4}{15}$, so

$$J_3 = \begin{pmatrix} 0 & 1/\sqrt{3} & 0 \\ 1/\sqrt{3} & 0 & 2/\sqrt{15} \\ 0 & 2/\sqrt{15} & 0 \end{pmatrix}, \qquad \det(xI - J_3) = x^3 - \tfrac35 x = \pi_3(x).$$

Its Gershgorin interval is $[-1.094, 1.094]$, and bisection finds the eigenvalues $-\sqrt{3/5}, 0, \sqrt{3/5}$. With $p_0 = 1/\sqrt2$, $p_1 = \sqrt{3/2}\,x$, $p_2 = \sqrt{5/8}\,(3x^2 - 1)$:

| node $x_j$ | $p_0^2$ | $p_1^2$ | $p_2^2$ | $\sum_k p_k^2$ | weight $1/\sum$ |
|---|---|---|---|---|---|
| $-\sqrt{3/5} \approx -0.7745967$ | $\tfrac12$ | $\tfrac{9}{10}$ | $\tfrac25$ | $\tfrac95$ | $\tfrac59$ |
| $0$ | $\tfrac12$ | $0$ | $\tfrac58$ | $\tfrac98$ | $\tfrac89$ |
| $\sqrt{3/5} \approx 0.7745967$ | $\tfrac12$ | $\tfrac{9}{10}$ | $\tfrac25$ | $\tfrac95$ | $\tfrac59$ |

The weights add up to $2 = \beta_0$. The rule integrates $x^k$ exactly for $k \le 5$ and gives $Q_3(x^6) = 2 \cdot \tfrac59 \cdot \tfrac{27}{125} = \tfrac{6}{25}$ against $I(x^6) = \tfrac27$, an error of $\tfrac{8}{175} = \beta_0\beta_1\beta_2\beta_3$, the squared norm of $\pi_3$.

The second table gives $|E_n(f)|$ of the mapped Gauss-Legendre rule for some test integrals. Each rule costs $n$ evaluations.

| $f$ on $[a, b]$ | $n = 4$ | $n = 8$ | $n = 16$ | $n = 32$ | $n = 64$ | rate |
|---|---|---|---|---|---|---|
| $e^x$ on $[-1, 1]$ | $3.0 \times 10^{-7}$ | $< 10^{-16}$ | $< 10^{-16}$ | $4.4 \times 10^{-16}$ | $8.9 \times 10^{-16}$ | faster than geometric |
| $1/(1 + x^2)$ on $[-1, 1]$ | $2.2 \times 10^{-3}$ | $1.9 \times 10^{-6}$ | $1.5 \times 10^{-12}$ | $4.4 \times 10^{-16}$ | $4.4 \times 10^{-16}$ | $(1 + \sqrt2)^{-2n}$ |
| $\cos 20x$ on $[-1, 1]$ | $1.0$ | $1.3$ | $5.4 \times 10^{-5}$ | $3.3 \times 10^{-16}$ | $1.2 \times 10^{-16}$ | none until $n \approx 20$ |
| $\lvert x \rvert$ on $[-1, 1]$ | $4.3 \times 10^{-2}$ | $1.2 \times 10^{-2}$ | $3.0 \times 10^{-3}$ | $7.8 \times 10^{-4}$ | $2.0 \times 10^{-4}$ | $n^{-2}$ |
| $\sqrt{x}$ on $[0, 1]$ | $1.2 \times 10^{-3}$ | $1.7 \times 10^{-4}$ | $2.3 \times 10^{-5}$ | $3.0 \times 10^{-6}$ | $3.8 \times 10^{-7}$ | $n^{-3}$ |
| $\log x$ on $[0, 1]$ | $3.2 \times 10^{-2}$ | $8.8 \times 10^{-3}$ | $2.3 \times 10^{-3}$ | $6.0 \times 10^{-4}$ | $1.5 \times 10^{-4}$ | $n^{-2}$ |
| $x^{-1/2}$ on $[0, 1]$ | $1.9 \times 10^{-1}$ | $1.0 \times 10^{-1}$ | $5.3 \times 10^{-2}$ | $2.7 \times 10^{-2}$ | $1.4 \times 10^{-2}$ | $n^{-1}$ |

For $1/(1+x^2)$, the poles at $\pm i$ lie on the Bernstein ellipse with $\rho = 1 + \sqrt2$, and the error falls by about $\rho^2 \approx 5.8$ per added node, as the bound $O(\rho^{-2n})$ predicts. The nodes are interior, so $\log x$ and $x^{-1/2}$ are never evaluated at $0$, but the convergence is slow. With the weight in the rule instead, the singularity costs nothing: Gauss-Laguerre with $w = x^{-1/2}e^{-x}$ and $n = 30$ gives $\int_0^\infty x^{-1/2}e^{-x}\cos x\,dx = \sqrt{\pi}\,2^{-1/4}\cos(\pi/8)$ to $10^{-14}$. Gauss-Hermite with $n = 20$ gives $\int e^{-x^2}\cos x\,dx = \sqrt\pi\, e^{-1/4}$ to $10^{-15}$.

## Correctness

The characteristic polynomial of $J_n$ satisfies the same recurrence as $\pi_n$, so the eigenvalues of $J_n$ are the zeros of $\pi_n$, the Gauss nodes; they are simple because $J_n$ is unreduced. The values $d_k$ are the pivots of $J_n - xI = LDL^T$, so by Sylvester's law of inertia $\mathrm{COUNT}(x)$ is the number of nodes below $x$, and bisection keeps the $j$-th node in its bracket. For the weights, exactness of the rule on $p_k p_m$ gives $P \Lambda P^T = I$ with $P_{kj} = p_k(x_j)$, hence $P^T P = \Lambda^{-1}$, whose diagonal is the Christoffel formula. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The cost model counts evaluations of $f$ and, separately, the floating-point operations that build the rule.

- **Evaluations.** Applying the rule costs exactly $n$ evaluations of $f$, independent of $f$.
- **Building the rule.** Each count costs $O(n)$, each node takes at most 107 counts, and lines L9 and L10 cost $O(n)$. So the rule costs $O(n^2)$ operations and $\Theta(n)$ space. In the implementation $n = 200$ takes about 0.4 seconds in pure Python.
- **Other methods.** The [Golub-Welsch algorithm](/golub-welsch-algorithm/) also costs $O(n^2)$, through the QR algorithm on $J_n$. For Gauss-Legendre and Gauss-Jacobi, Newton's method from asymptotic starting values costs $O(1)$ per node and $O(n)$ in all (Hale and Townsend 2013), and explicit asymptotic formulas avoid the iteration (Bogaert 2014). See [computing Gaussian nodes and weights](/gauss-nodes-and-weights/).
- **Rate in $n$.** For $w = 1$ and $f$ analytic in the Bernstein ellipse $E_\rho$ with $|f| \le M$, $|E_n(f)| \le \frac{64}{15} M\rho^{2-2n}/(\rho^2 - 1)$ (proved on the [theorem page](/gauss-quadrature-theorem/)). For $f$ with $f^{(k-1)}$ absolutely continuous and $f^{(k)}$ of bounded variation $V$, the error is $O(V n^{-k})$ (Trefethen, Chapter 19). For $|x|$ ($k = 1$) this proves $O(n^{-1})$, and the measured rate $n^{-2}$ is better. The rates $n^{-3}$ for $\sqrt{x}$, $n^{-2}$ for $\log x$ and $n^{-1}$ for $x^{-1/2}$ are measured.

## Properties

- **Degree of precision $2n - 1$.** No $n$-point rule does better.
- **Positive weights, summing to $\int w$.** So $\sum |w_i| = \int w$ for all $n$, the rule converges for every continuous $f$ on a finite interval, and a perturbation $\delta$ in each value $f(x_i)$ changes $Q_n(f)$ by at most $\delta \int w$.
- **Interior nodes.** No node is at a finite endpoint, so a finite singularity of $f$ at an end is not evaluated.
- **Not nested.** The $n$-point and the $2n$-point rules in general share no nodes, so refining from $n$ to $2n$ wastes the old values. [Gauss-Kronrod](/gauss-kronrod-quadrature/) rules and [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) rules address this.
- **Floating point.** Bisection gives each node with an absolute error of order $u\|J_n\|$, and the weights have a relative error of order $nu$. With positive weights, summing $\sum w_i f(x_i)$ has no cancellation from the weights; the attainable accuracy is about $u \sum w_i |f(x_i)|$, and summation with `math.fsum` removes the growth with $n$.

## Variants and improvements

- **Fixed endpoint nodes.** [Gauss-Radau](/gauss-radau-quadrature/) fixes one endpoint (degree $2n - 2$) and [Gauss-Lobatto](/gauss-lobatto-quadrature/) fixes both (degree $2n - 3$). They come from modified Jacobi matrices.
- **Golub-Welsch.** Compute the eigenvalues and the first components of the eigenvectors of $J_n$ with the [QR algorithm](/qr-algorithm/); the weights are $\beta_0 v_{1j}^2$.
- **Newton with asymptotics.** For large $n$ (thousands to millions of nodes), start Newton's method from asymptotic formulas for the zeros and evaluate $p_n$ by recurrence or by asymptotic expansions; Glaser, Liu and Rokhlin (2007), Hale and Townsend (2013), Bogaert (2014).
- **Gauss-Kronrod extension.** Add $n + 1$ nodes to reuse the $n$ Gauss values and get an error estimate; this is the panel rule of QUADPACK.
- **Composite Gauss.** Apply an $n$-point rule on each of $m$ panels of width $h = (b - a)/m$; for $f \in C^{2n}$ the error is $O(h^{2n})$. See [composite quadrature](/composite-quadrature/).
- **Nonclassical weights.** Compute $\alpha_k, \beta_k$ with the discretized Stieltjes procedure or the modified Chebyshev algorithm (Gautschi, Chapter 2), then use this page unchanged.

## When to use it

Use Gaussian quadrature when $f$ is smooth (ideally analytic) on the whole interval, when the integral has a known weight that carries the difficulty (an endpoint singularity $x^a$, an infinite interval with $e^{-x}$ or $e^{-x^2}$), or when each evaluation of $f$ is expensive and $n$ is fixed in advance. For $w = 1$, [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) reaches about the same accuracy for most $f$ with nested nodes. When $f$ has kinks or singularities at unknown points, use [adaptive quadrature](/adaptive-quadrature/), possibly with Gauss-Kronrod panels.

## Pitfalls

- **Expecting $2n - 1$ to mean twice the accuracy of Clenshaw-Curtis.** For most analytic $f$ the two errors are close, because the Chebyshev coefficients of $f$ above degree $n$ dominate both; the factor of 2 shows only for $f$ analytic in a large region, such as entire functions (Trefethen, Chapter 19).
- **Singular integrands with $w = 1$.** The rule never touches $x = 0$, so $x^{-1/2}$ on $[0, 1]$ returns a finite number, but the error is $O(n^{-1})$. Put the singularity in the weight (Gauss-Jacobi) or substitute first ([improper integration](/improper-integration/)).
- **Oscillatory integrands.** $\cos \omega x$ on $[-1, 1]$ needs about $\pi$ nodes per wavelength in the middle of the interval before the error drops; with $\omega = 20$ the 8-node rule has error $1.3$. For large $\omega$ use [Filon](/filon-quadrature/) or other [oscillatory](/oscillatory-integration/) methods.
- **Computing the nodes as roots of $\pi_n$ in the monomial basis.** The coefficients are badly conditioned and overflow for moderate $n$; use the recurrence or the Jacobi matrix.
- **Computing weights from a Vandermonde system.** Solving $\sum_i w_i x_i^k = \int x^k w$ for $k < n$ is ill-conditioned (see [Vandermonde matrix](/vandermonde-matrix/)); the Christoffel formula is stable.
- **Large $n$ for Laguerre or Hermite.** The smallest weights underflow below $10^{-308}$ for $n$ of a few hundred, and the largest nodes grow like $4n$ and $\sqrt{2n}$. Underflow is harmless when $f$ grows slowly, but $f(x_i)$ may overflow at the far nodes.
- **Odd symmetry and the node at $0$.** For a symmetric weight and odd $n$ the middle node is $0$; a relative stopping test alone would bisect into the subnormal range. Line L5 also stops at an absolute width.

## Implementations

## History

Gauss published the rules for $w = 1$ in 1814, derived through continued fractions. Jacobi (1826) gave the proof by orthogonality and identified the nodes as the zeros of the Legendre polynomial. Christoffel (1858) extended the rules to general weight functions, and the weights carry his name. For a century the nodes and weights were computed by hand and tabulated. Golub and Welsch (1969) reduced their computation to the symmetric tridiagonal eigenproblem, which made Gauss rules of any order and any weight routine. Gautschi's work on the computation of recurrence coefficients extended the method to nonclassical weights, and from 2007 Newton methods with asymptotics brought the cost down to $O(n)$.

## References
