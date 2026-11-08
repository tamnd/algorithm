---
tag: T8RETN
kind: algorithm
slug: gauss-radau-quadrature
name: Gauss-Radau quadrature
aliases:
- Radau rule
- Radau quadrature
- Gauss-Radau rule
area: numerical/quadrature
level: advanced
summary: Gaussian variant that forces one endpoint to be a node. With n nodes it is exact to degree 2n-2, its weights are positive, and the nodes come from a modified Jacobi matrix.
solves: [numerical-integration]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes, including the fixed endpoint"}
  time: {worst: "O(n^2)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "n"}
properties: {deterministic: true, degree_of_precision: "2n-2", positive_weights: true, includes_one_endpoint: true}
history:
  year: 1880
  people: [Rodolphe Radau, Gene H. Golub]
  note: Radau published the rules with one prescribed endpoint in 1880. Golub (1973) showed how to compute them from a Jacobi matrix with a modified last diagonal entry.
prereqs: [gaussian-quadrature]
see_also: [gauss-lobatto-quadrature, gauss-quadrature-theorem, golub-welsch-algorithm, gauss-legendre-quadrature, gauss-nodes-and-weights, legendre-polynomials, degree-of-precision, gauss-laguerre-quadrature]
sources:
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Chapter 1, Section 1.4 (Gauss-Radau formulae) and Chapter 3, Section 3.1 (computation of Gauss-Radau rules by a modified Jacobi matrix)
  - paper: "Gene H. Golub, Some modified matrix eigenvalue problems, SIAM Review 15(2) (1973) 318-334"
    locator: the Radau and Lobatto modifications of the Jacobi matrix
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, the sections on Gauss-type rules with preassigned abscissas (Radau and Lobatto rules)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.3 (Gaussian quadrature and its variants with fixed endpoints)
  - paper: "Rodolphe Radau, Étude sur les formules d'approximation qui servent à calculer la valeur numérique d'une intégrale définie, Journal de Mathématiques Pures et Appliquées 3e série, 6 (1880) 283-336"
    locator: the rules with one prescribed endpoint
---

Gauss-Radau quadrature is the variant of [Gaussian quadrature](/gaussian-quadrature/) in which one endpoint of the interval is prescribed as a node and the other $n - 1$ nodes and all $n$ weights are chosen for the highest degree of precision. Giving up one free node costs one degree: the rule is exact for all polynomials of degree at most $2n - 2$. The free nodes are the zeros of the orthogonal polynomial of degree $n - 1$ for the weight $(x - c)w(x)$, and all weights are positive. This page computes the rule for any weight from Golub's modified Jacobi matrix, with Sturm bisection and eigenvector weights in $O(n^2)$ operations.

## In plain words

Sometimes the value of a function at one end of the interval is known or needed anyway, for example the starting value of a time step. A Radau rule uses that value as one of its sample points and places the remaining points as cleverly as possible. With $n$ points in all it is exact for polynomials up to degree $2n - 2$, one less than a full Gauss rule and much more than equally spaced points give. The rule is lopsided: the points are denser toward the free end, and the weight at the fixed end is small.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,w(x)\,dx$; $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$, where $n$ counts all nodes, the fixed one included; $E_n(f) = I(f) - Q_n(f)$; $d$ is the [degree of precision](/degree-of-precision/). The monic orthogonal polynomials of $w$ satisfy $\pi_{k+1} = (x - \alpha_k)\pi_k - \beta_k\pi_{k-1}$ with $\beta_0 = \int w$.

Given $n \ge 1$, a weight $w$ by its recurrence coefficients $\alpha_k, \beta_k$ ($k < n$), and a fixed node $c$ that is a finite endpoint of the support of $w$, find nodes $x_1 < \cdots < x_n$ with $c$ among them and weights $w_i$ such that $d = 2n - 2$. The default is $w = 1$ on $[-1, 1]$ with $c = -1$ (Legendre-Radau), mapped to $[a, b]$ affinely. For the Legendre case there are closed forms: the free nodes are the zeros of $(P_{n-1}(x) + P_n(x))/(1 + x)$, the fixed weight is $2/n^2$, and the free weights are $(1 - x_j)/(n^2 P_{n-1}(x_j)^2)$.

## The algorithm

The node polynomial $\tilde\pi_n = (x - \alpha')\pi_{n-1} - \beta_{n-1}\pi_{n-2}$ is $\pi_n$ with the last recurrence coefficient $\alpha_{n-1}$ replaced by $\alpha'$, chosen so that $\tilde\pi_n(c) = 0$. Its matrix is the Jacobi matrix with one modified diagonal entry.

```pseudo id=main
GAUSS-RADAU(α, β, n, c)                    ▷ c a finite endpoint of the support of w
L1  if n = 1 then return node c with weight β_0
L2  r ← π_(n−1)(c)/π_(n−2)(c) by the ratio recurrence r_1 = c − α_0, r_(k+1) = c − α_k − β_k/r_k
L3  α' ← c − β_(n−1)/r
L4  J̃ ← the Jacobi matrix J_n with its last diagonal entry α_(n−1) replaced by α'
L5  nodes ← eigenvalues of J̃ by Sturm bisection; weight of x_j ← β_0 / |v(x_j)|^2, where v_0 = 1 and v follows the recurrence
L6  replace the computed node nearest c by c exactly
L7  return the nodes and weights
```

Line L2 uses ratios because $\pi_k(c)$ itself overflows or underflows for large $k$; since all zeros of $\pi_k$ are inside the interval, no ratio is $0$ or infinite. Line L3 is the condition $\tilde\pi_n(c) = 0$ divided by $\pi_{n-1}(c)$. In line L5 the eigenvector of $\tilde J$ for the eigenvalue $x_j$ starts with $v_0 = 1$ and follows the recurrence $v_{k+1} = ((x_j - \alpha_k)v_k - \sqrt{\beta_k}\,v_{k-1})/\sqrt{\beta_{k+1}}$, which does not involve $\alpha'$; the weight is $\beta_0$ times the squared first component of the unit eigenvector, as in the [Golub-Welsch algorithm](/golub-welsch-algorithm/). Line L6 removes the rounding error of the fixed node, so a function such as $\sqrt{x}$ on $[0, 1]$ is evaluated exactly at $0$.

## Example

Take $w = 1$ on $[-1, 1]$, $c = -1$ and $n = 3$. The coefficients are $\alpha_k = 0$, $\beta_1 = \frac13$, $\beta_2 = \frac{4}{15}$. Line L2 gives $r_1 = -1$ and $r_2 = -1 - \frac{1/3}{-1} = -\frac23$, and line L3 gives $\alpha' = -1 - \frac{4/15}{-2/3} = -\frac35$. So

$$\tilde J = \begin{pmatrix} 0 & 1/\sqrt3 & 0 \\ 1/\sqrt3 & 0 & 2/\sqrt{15} \\ 0 & 2/\sqrt{15} & -3/5 \end{pmatrix}, \qquad \det(xI - \tilde J) = x^3 + \tfrac35 x^2 - \tfrac35 x - \tfrac15 = (x + 1)\bigl(x^2 - \tfrac25 x - \tfrac15\bigr).$$

| node | value | $\lvert v \rvert^2$ | weight $2/\lvert v \rvert^2$ | closed form |
|---|---|---|---|---|
| $-1$ | $-1$ | $9$ | $0.2222222$ | $\tfrac29$ |
| $\frac{1 - \sqrt6}{5}$ | $-0.2898979$ | $1.951274$ | $1.0249717$ | $\frac{16 + \sqrt6}{18}$ |
| $\frac{1 + \sqrt6}{5}$ | $0.6898979$ | $2.656726$ | $0.7528061$ | $\frac{16 - \sqrt6}{18}$ |

The rule integrates $1, x, x^2, x^3, x^4$ exactly, so $d = 4 = 2n - 2$. For $x^5$ it gives $Q_3(x^5) = -0.1066667$ while $I(x^5) = 0$, so $E_3(x^5) = \frac{8}{75}$. This matches the error formula below: $c_3 = \frac{2^5 \cdot 3 \cdot (2!)^4}{(5!)^3} = \frac{1}{1125}$ times $(x^5)^{(5)} = 120$ is $\frac{8}{75}$.

Measured on $[0, 1]$ with the node at $0$: for $e^x$ the errors are $7.5 \times 10^{-3}$, $3.3 \times 10^{-8}$ and below $10^{-15}$ for $n = 2, 4, 8$. For $\sqrt{x}$ they are $6.4 \times 10^{-3}$, $7.8 \times 10^{-4}$ and $9.7 \times 10^{-5}$ for $n = 4, 8, 16$, the rate $n^{-3}$.

## Correctness

The modified polynomial $\tilde\pi_n = \pi_n + (\alpha_{n-1} - \alpha')\pi_{n-1}$ vanishes at $c$ and is orthogonal to all polynomials of degree $n - 2$. Writing $\tilde\pi_n = (x - c)q$ shows that $q$ is the orthogonal polynomial of degree $n - 1$ for the weight $(x - c)w$, so its zeros are real, simple and interior. Dividing any $f$ of degree $2n - 2$ by $\tilde\pi_n$ proves exactness, and $(x - c)q^2$ shows that degree $2n - 1$ fails. The weights are positive by applying the rule to $\ell_j^2$ and to $q^2$. Since $\det(xI - \tilde J) = \tilde\pi_n$, and the rows of the orthogonal eigenvector matrix are orthonormal, the eigenvector weights integrate all products $p_k p_m$, $k, m < n$, exactly and so are the Radau weights. The full proof, with the error term, is in [the correctness proof](proofs/correctness.md).

**Error (proved).** For $f \in C^{2n-1}$ on a finite $[a, b]$ with $c = a$,

$$E_n(f) = \frac{f^{(2n-1)}(\xi)}{(2n-1)!}\int_a^b (x - a)\,q(x)^2\,w(x)\,dx.$$

For Legendre-Radau on $[-1, 1]$ with $c = -1$ this reads $E_n(f) = \frac{2^{2n-1}\,n\,((n-1)!)^4}{((2n-1)!)^3}\, f^{(2n-1)}(\xi)$. For $n = 2$: nodes $-1, \frac13$, weights $\frac12, \frac32$, and $E_2(x^3) = \frac49$.

## Complexity

- **Evaluations.** $n$ per application of the rule, one of them at the endpoint.
- **Building the rule.** Line L2 costs $O(n)$. Line L5 costs $O(n)$ per Sturm count, at most about 107 counts per node in double precision, and $O(n)$ per weight: $O(n^2)$ in all, with $\Theta(n)$ space. A QR-based eigensolver gives the same $O(n^2)$.
- **Rate.** For analytic $f$ the error falls geometrically, like that of the Gauss rule with about one node less.

## Properties

- **Degree $2n - 2$**, the highest possible for an $n$-point rule with one prescribed endpoint.
- **Positive weights** summing to $\int w$; hence convergence for all continuous $f$ on a finite interval and no amplification of rounding errors.
- **One endpoint included**, the other not. For Legendre-Radau the fixed weight is $2/n^2$, small, so a large endpoint value has little influence.
- **Right-endpoint version.** With $c = 1$ the nodes are mirrored and the weights reversed; the error constant changes sign.
- **Stiff accuracy.** In Radau IIA Runge-Kutta methods the last stage is at the right end of the step, which makes the methods stiffly accurate; the stages are the right-Radau nodes mapped to $[0, 1]$.

## Variants and improvements

- **Gauss-Lobatto.** Fix both endpoints, degree $2n - 3$; see [Gauss-Lobatto quadrature](/gauss-lobatto-quadrature/).
- **Radau rules for other weights.** The same code with Laguerre coefficients gives Laguerre-Radau rules with the node $0$; for $n = 3$ the nodes are $0, 3 \mp \sqrt3$ and the weight at $0$ is $\frac13$.
- **Fixed node outside the interval.** Golub's construction also works for $c$ outside $[a, b]$; the weight $(x - c)w$ keeps a fixed sign there.
- **Newton on the closed form.** For Legendre-Radau, Newton's method on $P_{n-1} + P_n$ with the recurrence costs $O(n)$ per step, like the [Gauss-Legendre](/gauss-legendre-quadrature/) code.
- **Collocation.** Radau IA and IIA Runge-Kutta methods (Butcher, Ehle) use left and right Radau nodes as stages; Radau IIA with $s$ stages has order $2s - 1$.

## When to use it

Use a Radau rule when one endpoint value is available for free or must be part of the rule: the left end of a time step in collocation methods, the endpoint of a panel in a composite rule that shares nodes with its neighbour, or an integrand whose behaviour at one end is known. When neither endpoint matters, use the full Gauss rule; when both do, use Gauss-Lobatto.

## Pitfalls

- **A singular endpoint as the fixed node.** For $\log x$ on $[0, 1]$, the left-Radau rule evaluates $\log 0$ and fails; put the fixed node at the other end or use the plain Gauss rule.
- **Counting nodes.** Some books count only the free nodes, so their "$n$-point Radau rule" has $n + 1$ points and degree $2n$. This page counts all nodes, as on all quadrature pages.
- **The fixed node inside the interval.** If $c$ is a zero of $\pi_{n-1}$, line L3 divides by zero; if $c$ is inside $(a, b)$, the weight $(x - c)w$ changes sign, and the nodes may be complex or the weights negative. The construction needs $c$ at an end of the support or outside it.
- **Rounding at the fixed node.** Bisection returns $c$ only up to rounding; without line L6 a rule on $[0, 1]$ may evaluate $f$ at $-10^{-17}$, which breaks $\sqrt{x}$ or $\log x$.
- **Forgetting the sign of the error.** With $c = -1$ the error constant is positive; with $c = 1$ it is negative. One-sided bounds built from a pair of left and right Radau rules depend on this.

## Implementations

## History

Rodolphe Radau, an astronomer, published in 1880 a study of approximate integration formulas that included the rules with one prescribed endpoint, building on the work of Gauss, Jacobi and Christoffel. The rules became important again in the 1960s and 1970s as the stages of implicit Runge-Kutta methods (Butcher 1964, Ehle 1969), and Radau IIA methods are the basis of Hairer and Wanner's RADAU5 code for stiff equations. Golub (1973) gave the modified Jacobi matrix construction used on this page.

## References
