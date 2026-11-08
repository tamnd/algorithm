---
tag: 4NBTQ5
kind: algorithm
slug: gauss-lobatto-quadrature
name: Gauss-Lobatto quadrature
aliases:
- Lobatto rule
- Lobatto quadrature
- Gauss-Lobatto-Legendre rule
area: numerical/quadrature
level: advanced
summary: Gaussian variant that forces both endpoints to be nodes. With n nodes it is exact to degree 2n-3, its weights are positive, and composite versions share endpoints between panels.
solves: [numerical-integration]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes, including both endpoints", m: "the number of panels in the composite rule"}
  time: {worst: "O(n^2)"}
  space: {extra: Θ(n)}
  evaluations: {single: "n", composite: "m(n-1)+1"}
properties: {deterministic: true, degree_of_precision: "2n-3", positive_weights: true, includes_both_endpoints: true}
history:
  year: 1852
  people: [Rehuel Lobatto, Gene H. Golub]
  note: Lobatto described the rules with both endpoints as nodes in 1852. Golub (1973) showed how to compute them from a Jacobi matrix with modified last row and column.
prereqs: [gaussian-quadrature]
see_also: [gauss-radau-quadrature, gauss-quadrature-theorem, golub-welsch-algorithm, gauss-legendre-quadrature, simpsons-rule, composite-quadrature, adaptive-quadrature, legendre-polynomials]
sources:
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Chapter 1, Section 1.4 (Gauss-Lobatto formulae) and Chapter 3, Section 3.1 (computation by a modified Jacobi matrix)
  - paper: "Gene H. Golub, Some modified matrix eigenvalue problems, SIAM Review 15(2) (1973) 318-334"
    locator: the Radau and Lobatto modifications of the Jacobi matrix
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, the sections on Gauss-type rules with preassigned abscissas (Lobatto rules and their error terms)
  - paper: "Walter Gander and Walter Gautschi, Adaptive quadrature, revisited, BIT Numerical Mathematics 40(1) (2000) 84-101"
    locator: the adaptive Gauss-Lobatto routine adaptlob with its Kronrod extension
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.3 (Gaussian quadrature and its variants with fixed endpoints)
---

Gauss-Lobatto quadrature is the variant of [Gaussian quadrature](/gaussian-quadrature/) in which both endpoints of a finite interval are prescribed as nodes and the other $n - 2$ nodes and all $n$ weights are chosen for the highest degree of precision. Fixing two nodes costs two degrees: the rule is exact for all polynomials of degree at most $2n - 3$. The interior nodes are the zeros of the orthogonal polynomial of degree $n - 2$ for the weight $(x - a)(b - x)w(x)$, and all weights are positive. The three-point Legendre-Lobatto rule is Simpson's rule. This page computes the rule for any weight from Golub's modified Jacobi matrix, with Sturm bisection and eigenvector weights in $O(n^2)$ operations.

## In plain words

Many methods sample a function at the ends of each piece anyway, so it is natural to ask for the best rule that uses both ends. A Lobatto rule keeps the two endpoint values and places the remaining points as cleverly as possible. With $n$ points it is exact for polynomials up to degree $2n - 3$, only two less than a full Gauss rule. Because neighbouring pieces share their endpoints, a chain of Lobatto rules needs one sample fewer per piece than a chain of Gauss rules of the same size.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,w(x)\,dx$; $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$, where $n$ counts all nodes, both endpoints included; $E_n(f) = I(f) - Q_n(f)$; $d$ is the [degree of precision](/degree-of-precision/). For composite rules $h = (b - a)/m$ with $m$ panels. The monic orthogonal polynomials of $w$ satisfy $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k\pi_{k-1}$ with $\beta_0 = \int w$.

Given $n \ge 2$, a weight $w$ on a finite interval $(a, b)$ by its recurrence coefficients $\alpha_k, \beta_k$ ($k \le n - 2$), find nodes $a = x_1 < \cdots < x_n = b$ and weights $w_i$ such that $d = 2n - 3$. The default is $w = 1$ on $[-1, 1]$ (Legendre-Lobatto), mapped to $[a, b]$ affinely. For this case there are closed forms: the interior nodes are the zeros of $P_{n-1}'$, the endpoint weights are $\frac{2}{n(n-1)}$, and the interior weights are $\frac{2}{n(n-1)P_{n-1}(x_j)^2}$, where $P_k$ are the [Legendre polynomials](/legendre-polynomials/).

## The algorithm

The node polynomial $\tilde\pi_n = (x - \alpha')\pi_{n-1} - \beta'\pi_{n-2}$ is $\pi_n$ with the last two recurrence coefficients replaced so that $\tilde\pi_n(a) = \tilde\pi_n(b) = 0$. Its matrix is the Jacobi matrix with a modified last diagonal and last off-diagonal entry. Write $r_c = \pi_{n-1}(c)/\pi_{n-2}(c)$.

```pseudo id=main
GAUSS-LOBATTO(α, β, n, a, b)               ▷ n ≥ 2; a < b the ends of the support of w
L1  r_a, r_b ← π_(n−1)(c)/π_(n−2)(c) at c = a and c = b, by r_1 = c − α_0, r_(k+1) = c − α_k − β_k/r_k
L2  β' ← (a − b)/(1/r_a − 1/r_b)
L3  α' ← a − β'/r_a
L4  J̃ ← J_n with last diagonal entry α' and last off-diagonal entry √β'
L5  nodes ← eigenvalues of J̃ by Sturm bisection; weight of x_j ← β_0 / |v(x_j)|^2, where v_0 = 1 and v follows the recurrence
L6  set the first node to a and the last node to b exactly
L7  return the nodes and weights
```

Line L1 uses ratios because $\pi_k(c)$ overflows or underflows for large $k$; since all zeros of $\pi_k$ lie inside $(a, b)$, $r_a < 0 < r_b$ and no ratio is $0$ or infinite. Lines L2 and L3 solve the two linear conditions $\tilde\pi_n(a) = \tilde\pi_n(b) = 0$ after dividing by $\pi_{n-2}$; the signs of $r_a$ and $r_b$ make $\beta' > 0$, so $\tilde J$ is again a symmetric Jacobi matrix. In line L5 the eigenvector recurrence $v_{k+1} = ((x_j - \alpha_k)v_k - \sqrt{\beta_k}\,v_{k-1})/\sqrt{\beta_{k+1}}$ uses $\sqrt{\beta'}$ in its last step; the weight is $\beta_0$ times the squared first component of the unit eigenvector, as in the [Golub-Welsch algorithm](/golub-welsch-algorithm/). Line L6 removes the rounding error in the endpoints, so the integrand is evaluated exactly at $a$ and $b$.

## Example

Take $w = 1$ on $[-1, 1]$ and $n = 4$. The coefficients are $\alpha_k = 0$, $\beta_1 = \frac13$, $\beta_2 = \frac{4}{15}$. Line L1 gives $r_1(1) = 1$, $r_2(1) = 1 - \frac13 = \frac23$, $r_3(1) = 1 - \frac{4/15}{2/3} = \frac35$, and by symmetry $r_a = -\frac35$, $r_b = \frac35$. Line L2 gives $\beta' = \frac{-2}{-5/3 - 5/3} = \frac35$ and line L3 gives $\alpha' = -1 - \frac{3/5}{-3/5} = 0$. So

$$\tilde J = \begin{pmatrix} 0 & 1/\sqrt3 & 0 & 0 \\ 1/\sqrt3 & 0 & 2/\sqrt{15} & 0 \\ 0 & 2/\sqrt{15} & 0 & \sqrt{3/5} \\ 0 & 0 & \sqrt{3/5} & 0 \end{pmatrix}, \qquad \det(xI - \tilde J) = x^4 - \tfrac65 x^2 + \tfrac15 = (x^2 - 1)\bigl(x^2 - \tfrac15\bigr).$$

| node | $v$ | $\lvert v \rvert^2$ | weight $2/\lvert v \rvert^2$ |
|---|---|---|---|
| $\pm 1$ | $(1, \pm\sqrt3, \sqrt5, \pm\sqrt3)$ | $12$ | $\tfrac16$ |
| $\pm 1/\sqrt5$ | $(1, \pm\sqrt{3/5}, -1/\sqrt5, \mp\sqrt{3/5})$ | $\tfrac{12}{5}$ | $\tfrac56$ |

The rule $\frac16 f(-1) + \frac56 f(-\frac{1}{\sqrt5}) + \frac56 f(\frac{1}{\sqrt5}) + \frac16 f(1)$ integrates $1, x, \ldots, x^5$ exactly, so $d = 5 = 2n - 3$. For $x^6$ it gives $\frac13 + \frac{5}{3}\cdot\frac{1}{125} = \frac{26}{75}$ while $I(x^6) = \frac27$, so $E_4(x^6) = -\frac{32}{525}$, which is $c_4 \cdot 6!$ with $c_4 = -\frac{2}{23625}$ from the error formula below.

Measured on $[0, 1]$ with the mapped Legendre-Lobatto rule: for $e^x$ the errors are $5.8 \times 10^{-4}$, $1.1 \times 10^{-6}$, $1.2 \times 10^{-9}$, $7.8 \times 10^{-13}$ for $n = 3, 4, 5, 6$, and at rounding level for $n = 8$. For $\sqrt{x}$ they are $9.8 \times 10^{-3}$, $9.6 \times 10^{-4}$, $1.1 \times 10^{-4}$, $1.3 \times 10^{-5}$ for $n = 4, 8, 16, 32$, the rate $n^{-3}$. For the Runge function $1/(1 + 25x^2)$ on $[-1, 1]$ they are $0.26$, $0.062$, $2.7 \times 10^{-3}$, $4.6 \times 10^{-6}$, geometric once $n$ is large enough.

## Correctness

The two conditions of lines L2 and L3 make $\tilde\pi_n$ vanish at $a$ and $b$, and $\tilde\pi_n$ differs from $\pi_n$ by multiples of $\pi_{n-1}$ and $\pi_{n-2}$, so it is orthogonal to all polynomials of degree $n - 3$. Writing $\tilde\pi_n = (x - a)(x - b)q$ shows that $q$ is the orthogonal polynomial of degree $n - 2$ for the weight $(x - a)(b - x)w$, so its zeros are real, simple and interior. Dividing any $f$ of degree $2n - 3$ by $\tilde\pi_n$ proves exactness, and $(x - a)(x - b)q^2$ shows that degree $2n - 2$ fails. The weights are positive by applying the rule to nonnegative polynomials of degree at most $2n - 3$ that vanish at all nodes but one. Since $\det(xI - \tilde J) = \tilde\pi_n$ and the rows of the orthogonal eigenvector matrix are orthonormal, the eigenvector weights integrate all polynomials of degree $2n - 3$ exactly and so are the Lobatto weights. The full proof, with the error term, is in [the correctness proof](proofs/correctness.md).

**Error (proved).** For $f \in C^{2n-2}[a, b]$,

$$E_n(f) = \frac{f^{(2n-2)}(\xi)}{(2n-2)!}\int_a^b (x - a)(x - b)\,q(x)^2\,w(x)\,dx, \qquad \xi \in [a, b],$$

and the integral is negative. For Legendre-Lobatto on $[-1, 1]$ this reads $E_n(f) = c_n f^{(2n-2)}(\xi)$ with $c_n = -\frac{n(n-1)^3\,2^{2n-1}\,((n-2)!)^4}{(2n-1)\,((2n-2)!)^3}$. For $n = 3$, $c_3 = -\frac{1}{90}$, the constant of Simpson's rule; on an interval of length $b - a$ the constant scales by $((b - a)/2)^{2n-1}$. The general formula is proved; the closed form of $c_n$ is the classical evaluation, checked by the test file for $n \le 12$.

## Complexity

- **Evaluations.** $n$ for one application. A composite rule with $m$ panels needs $m(n - 1) + 1$, because neighbouring panels share an endpoint. A composite Gauss rule of the same degree $2n - 3$ uses $n - 1$ points per panel, $m(n - 1)$ in all, so at equal degree the costs are nearly equal; the endpoint values pay off when they are needed elsewhere.
- **Building the rule.** Line L1 costs $O(n)$. Line L5 costs $O(n)$ per Sturm count, at most about 107 counts per node in double precision, and $O(n)$ per weight: $O(n^2)$ operations in all and $\Theta(n)$ space. In pure Python $n = 200$ takes about $0.7$ seconds; Newton's method on the closed form is faster for large $n$.
- **Rate.** For $f$ analytic inside a Bernstein ellipse with parameter $\rho$, the error falls like that of the Gauss rule with $n - 1$ points, geometrically in $n$ (asymptotic, not proved on this page).

## Properties

- **Degree $2n - 3$**, the highest possible for an $n$-point rule containing both endpoints.
- **Positive weights** summing to $\int w$; hence convergence for every continuous $f$ and no amplification of rounding errors.
- **Endpoint weights are small.** For Legendre-Lobatto they are $\frac{2}{n(n-1)}$, so a large endpoint value has little influence, but it must be finite.
- **Symmetry.** For an even weight on $[-1, 1]$ the nodes are symmetric and the weights equal in pairs.
- **Small cases.** $n = 2$ is the trapezoidal rule, $n = 3$ is Simpson's rule, $n = 4$ is the rule of the example.
- **Sign of the error.** The error constant is negative: for $f$ with $f^{(2n-2)} > 0$ on $[a, b]$ the rule overestimates.

## Variants and improvements

- **Gauss-Radau.** Fix one endpoint, degree $2n - 2$; see [Gauss-Radau quadrature](/gauss-radau-quadrature/).
- **Other weights.** The same code with Chebyshev coefficients gives the Chebyshev-Lobatto rule: nodes $\cos(j\pi/(n-1))$, weights $\frac{\pi}{n-1}$ inside and half that at the ends. With Jacobi coefficients it gives Gauss-Lobatto-Jacobi rules.
- **Newton on the closed form.** For Legendre-Lobatto, Newton's method on $P_{n-1}'$ with starting values near the Chebyshev extreme points costs $O(n)$ per node.
- **Adaptive Lobatto.** Gander and Gautschi (2000) use a 4-point Lobatto rule with a 7-point Kronrod extension as the panel rule of an adaptive method (adaptlob); the seven Kronrod points become the endpoints of six subintervals, so their values are reused after a split.
- **Spectral elements and collocation.** Lobatto nodes are the collocation points of spectral element methods (the mass matrix is diagonal under Lobatto quadrature), and Lobatto IIIA, IIIB and IIIC Runge-Kutta methods use them as stages.

## When to use it

Use a Lobatto rule when the endpoint values are needed or come for free: composite and [adaptive quadrature](/adaptive-quadrature/) where panels share endpoints, collocation and spectral element methods that must match values across element boundaries, and time stepping that needs the solution at both ends of a step. When endpoints carry a singularity or are expensive, use the Gauss rule, which has two more degrees for the same number of points.

## Pitfalls

- **Endpoint singularities.** $\log x$ or $x^{-1/2}$ on $[0, 1]$ cannot be handled: the rule evaluates the integrand at $0$. Use Gauss or a [substitution](/improper-integration/) instead.
- **Counting nodes.** Some books count only interior nodes, so their "$n$-point Lobatto rule" has $n + 2$ points and degree $2n + 1$. This page counts all nodes.
- **Infinite intervals.** A Lobatto rule needs two finite endpoints; for a half-line use a Radau rule.
- **Endpoints inside the support.** If $a$ or $b$ is a zero of $\pi_{n-1}$, line L2 divides by zero; if they lie inside the support of $w$, $\beta'$ can be negative and the rule complex or with negative weights. The code checks $\beta' > 0$.
- **Rounding at the endpoints.** Without line L6 bisection returns the endpoints only up to rounding, and a rule on $[0, 1]$ may evaluate $f$ at $-10^{-17}$.
- **Comparing with Gauss at equal cost.** For a single panel, $n$ Lobatto points give two degrees less than $n$ Gauss points. In a composite rule the shared endpoints recover one point per panel, which brings the cost at equal degree level with Gauss, not below it.

## Implementations

## History

Rehuel Lobatto, a Dutch mathematician, described integration rules with both endpoints as nodes in his 1852 lessons on integral calculus. Radau (1880) treated them together with the one-endpoint rules. They became standard in the 1960s and 1970s as the stages of Lobatto Runge-Kutta methods (Butcher, Ehle, Chipman) and later as the nodes of spectral element methods. Golub (1973) gave the modified Jacobi matrix construction used on this page, and Gander and Gautschi (2000) made a Gauss-Lobatto rule with a Kronrod extension the basis of an adaptive integrator.

## References
