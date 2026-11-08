---
tag: NJK30H
kind: algorithm
slug: lagrange-interpolation
name: Lagrange interpolation
aliases:
- Lagrange form of the interpolating polynomial
- Lagrange polynomial
- Lagrange interpolation formula
area: numerical/interpolation-and-approximation
level: intro
summary: Write the interpolating polynomial through (x_i, y_i) as the sum of y_i times the basis polynomial l_i, which is 1 at x_i and 0 at the other nodes. Direct evaluation costs O(n^2) per point.
solves: [interpolation-problem]
model: real-ram
complexity:
  vars: {n: "the degree bound, with n + 1 distinct nodes"}
  time: {per_point: Θ(n^2)}
  space: {extra: Θ(1)}
  flops: {per_point: "4n^2 + 6n + 2"}
properties: {deterministic: true, recursive: false, exact_on_polynomials: true}
history:
  year: 1795
  people: [Edward Waring, Leonhard Euler, Joseph-Louis Lagrange]
  note: Waring published the formula in 1779, Euler used it in 1783, and Lagrange gave it in his lectures at the École normale in 1795.
prereqs: [interpolation-problem, polynomial]
see_also: [barycentric-interpolation, newton-interpolation, neville-algorithm, interpolating-polynomial-uniqueness, polynomial-interpolation-error-theorem, lebesgue-constant, runge-phenomenon, chebyshev-nodes]
sources:
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 6, Polynomial interpolation (the Lagrange form and the error theorem)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.1, Polynomial interpolation theory (the Lagrange formula and the error formula)
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 5, Barycentric interpolation formula (the Lagrange form and its O(n) rewriting), and Chapter 15, Lebesgue constants
  - paper: doi:10.1093/imanum/24.4.547
    title: "Nicholas J. Higham, The numerical stability of barycentric Lagrange interpolation, IMA Journal of Numerical Analysis 24(4) (2004) 547-556"
    locator: the rounding error analysis of the Lagrange and barycentric formulas
  - paper: doi:10.1137/S0036144502417715
    title: "Jean-Paul Berrut and Lloyd N. Trefethen, Barycentric Lagrange interpolation, SIAM Review 46(3) (2004) 501-517"
    locator: Sections 1 to 3, the Lagrange formula, its drawbacks and the barycentric forms
  - paper: "Edward Waring, Problems concerning interpolations, Philosophical Transactions of the Royal Society of London 69 (1779) 59-67"
    locator: the interpolation formula later named after Lagrange
  - paper: "Erik Meijering, A chronology of interpolation: from ancient astronomy to modern signal and image processing, Proceedings of the IEEE 90(3) (2002) 319-342"
    locator: the section on the seventeenth and eighteenth centuries (Waring, Euler and Lagrange)
---

Lagrange interpolation writes the polynomial $p_n$ of degree at most $n$ through the points $(x_0, y_0), \ldots, (x_n, y_n)$ as $p_n(x) = \sum_i y_i\, \ell_i(x)$, where each basis polynomial $\ell_i$ equals 1 at $x_i$ and 0 at every other node. It solves the polynomial case of the [interpolation problem](/interpolation-problem/) with no linear system, and it shows at once that the interpolant exists. Evaluated directly, it costs $\Theta(n^2)$ operations per point and is backward stable in the data; the [barycentric form](/barycentric-interpolation/) is the same polynomial at $O(n)$ per point.

## In plain words

Suppose you know the value of a curve at a few points and want one polynomial that passes through all of them. Lagrange's idea is to build one helper polynomial for each point. The helper for a point is 1 at that point and 0 at all the others; it is a product of simple factors, each of which is zero at one of the other points. Multiply each helper by the value you want at its point and add them up. At any given point, all the helpers but one are zero, and the remaining one is 1, so the sum takes exactly the required value there.

## The problem

The input is a list of $n + 1$ distinct nodes $x_0, \ldots, x_n$ (in any order), the values $y_0, \ldots, y_n$, and a point $t$. The output is $p_n(t)$, where $p_n$ is the unique polynomial of degree at most $n$ with $p_n(x_i) = y_i$ for all $i$ (see the [uniqueness theorem](/interpolating-polynomial-uniqueness/)).

Notation on the interpolation pages: $f$ is a function on $[a, b]$, usually $[-1, 1]$, with data $y_i = f(x_i)$; $\omega(x) = \prod_{i=0}^{n} (x - x_i)$ is the node polynomial; $\Lambda_n = \max_{x \in [a, b]} \sum_i |\ell_i(x)|$ is the [Lebesgue constant](/lebesgue-constant/). Costs are arithmetic operations on the [real RAM](/real-ram/); rounding errors are analyzed in the [standard floating-point model](/floating-point-model/) with unit roundoff $u$.

## The algorithm

The Lagrange basis polynomials are
$$\ell_i(x) = \prod_{\substack{j = 0 \\ j \ne i}}^{n} \frac{x - x_j}{x_i - x_j}, \qquad p_n(x) = \sum_{i=0}^{n} y_i\, \ell_i(x).$$

```pseudo id=main
LAGRANGE(x, y, t)                         ▷ x[0 .. n] distinct, y[0 .. n]
L1  p ← 0
L2  for i ← 0 to n do
L3      ℓ ← 1
L4      for j ← 0 to n do
L5          if j ≠ i then ℓ ← ℓ · (t − x[j]) / (x[i] − x[j])
L6      p ← p + y[i] · ℓ
L7  return p
```

The inner loop of lines L4 and L5 builds the value $\ell_i(t)$ as a running product of $n$ factors. Line L6 adds the term $y_i \ell_i(t)$. Nothing depends on the order of the nodes. If $t$ equals a node $x_k$, the factor for $j = k$ is an exact zero in every $\ell_i$ with $i \ne k$, so the result is exactly $y_k$, also in floating point.

## Example

Take the nodes $0, 1, 2, 4$ with the data $y_i = 2^{x_i}$, that is $1, 2, 4, 16$, and evaluate at $t = 3$. Here $n = 3$ and $\omega(3) = 3 \cdot 2 \cdot 1 \cdot (-1) = -6$.

| $i$ | $x_i$ | $y_i$ | $\ell_i(3)$ | $y_i\, \ell_i(3)$ | $p$ after line L6 |
|---|---|---|---|---|---|
| 0 | 0 | 1 | $\frac{(3-1)(3-2)(3-4)}{(0-1)(0-2)(0-4)} = \frac{1}{4}$ | $\frac{1}{4}$ | $\frac{1}{4}$ |
| 1 | 1 | 2 | $\frac{(3-0)(3-2)(3-4)}{(1-0)(1-2)(1-4)} = -1$ | $-2$ | $-\frac{7}{4}$ |
| 2 | 2 | 4 | $\frac{(3-0)(3-1)(3-4)}{(2-0)(2-1)(2-4)} = \frac{3}{2}$ | $6$ | $\frac{17}{4}$ |
| 3 | 4 | 16 | $\frac{(3-0)(3-1)(3-2)}{(4-0)(4-1)(4-2)} = \frac{1}{4}$ | $4$ | $\frac{33}{4}$ |

So $p_3(3) = 33/4 = 8.25$, while $2^3 = 8$. The four values $\ell_i(3)$ sum to 1, as they must (the data $y_i = 1$ give $p_n = 1$). The error $f(3) - p_3(3) = -1/4$ agrees with the error formula below: $f^{(4)}(\xi) = (\ln 2)^4\, 2^{\xi}$, and $-\tfrac{1}{4} = \tfrac{(\ln 2)^4 2^{\xi}}{24} \cdot (-6)$ gives $2^{\xi} = (\ln 2)^{-4} \approx 4.33$, so $\xi \approx 2.11$, inside $[0, 4]$.

## Correctness

Each $\ell_i$ is a product of $n$ linear factors, so it has degree at most $n$, and $\ell_i(x_k) = \delta_{ik}$: for $k \ne i$ the factor $j = k$ vanishes, and for $k = i$ every factor is 1. So $\sum_i y_i \ell_i$ lies in $\mathcal{P}_n$ and takes the value $y_k$ at $x_k$. Any two polynomials of degree at most $n$ that agree at $n + 1$ points are equal, so this is $p_n$. The loops of lines L2 to L6 compute exactly this sum. The [full proof](proofs/correctness.md) also proves the rounding error bound of the next section.

**Error of the interpolant.** If $f \in C^{n+1}[a, b]$ and all nodes lie in $[a, b]$, then for every $x \in [a, b]$ there is a $\xi$ in the smallest interval that holds $x$ and the nodes with
$$f(x) - p_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}\, \omega(x).$$
This is the [interpolation error theorem](/polynomial-interpolation-error-theorem/), proved by Rolle's theorem applied $n + 1$ times (Süli and Mayers, Chapter 6; Atkinson, Section 3.1). It is a proved bound, not an estimate: $|f(x) - p_n(x)| \le \max |f^{(n+1)}| \, |\omega(x)| / (n+1)!$. For $f = e^x$ on $[-1, 1]$ the maximum is $e$, and for $f = \sin x$ it is 1.

## Complexity

For each of the $n + 1$ values of $i$, line L5 runs $n$ times with two subtractions, one division and one multiplication, and line L6 does one multiplication and one addition. The total is $(n + 1)(4n + 2) = 4n^2 + 6n + 2$ operations per evaluation point, that is $\Theta(n^2)$ in every case. The extra space is $\Theta(1)$.

Evaluating at $m$ points costs $\Theta(m n^2)$. The products $\prod_{j \ne i} (x_i - x_j)$ do not depend on $t$; computing them once in $O(n^2)$ and writing $p_n(t) = \omega(t) \sum_i w_i y_i/(t - x_i)$ with $w_i = 1/\prod_{j \ne i}(x_i - x_j)$ brings the cost to $O(n)$ per point. That rewriting is the [barycentric formula](/barycentric-interpolation/).

**Rounding errors.** In the standard model, with no underflow or overflow, the computed value satisfies $\hat p = \sum_i y_i \ell_i(t)(1 + \theta_i)$ with $|\theta_i| \le \gamma_{5n+1} = (5n+1)u/(1 - (5n+1)u)$. So $\hat p$ is the exact interpolant of data perturbed by a relative amount of order $n u$, and
$$|\hat p - p_n(t)| \le \gamma_{5n+1} \sum_i |y_i \ell_i(t)| \le \gamma_{5n+1}\, \Lambda_n \max_i |y_i|.$$
The method is backward stable in the data; its forward error is as good as the conditioning $\Lambda_n$ of the problem allows. Higham (2004) gives the same kind of analysis for the first barycentric form.

## Properties

- **Exact on polynomials.** If the data come from a polynomial of degree at most $n$, the result is that polynomial; with `Fraction` arithmetic it is exact.
- **Order free.** The nodes need not be sorted; the result does not depend on their order in exact arithmetic.
- **Not incremental.** Adding a node changes every $\ell_i$. The [Newton form](/newton-interpolation/) and the barycentric weights can be updated in $O(n)$ per new node.
- **Linear in the data.** $p_n$ depends linearly on $y$, which gives quadrature weights $\int \ell_i$ ([interpolatory quadrature](/interpolatory-quadrature/)) and the Lebesgue function $\sum_i |\ell_i(x)|$.
- **Partition of unity.** $\sum_i \ell_i(x) = 1$ for all $x$, since the data $y_i = 1$ are reproduced.

## Variants and improvements

- **Barycentric forms.** $p_n(t) = \omega(t) \sum_i \frac{w_i y_i}{t - x_i}$ (first form) and $p_n(t) = \sum_i \frac{w_i y_i}{t - x_i} \big/ \sum_i \frac{w_i}{t - x_i}$ (second form). Both cost $O(n)$ per point after $O(n^2)$ for the weights. See [barycentric interpolation](/barycentric-interpolation/).
- **Neville's algorithm.** Builds $p_n(t)$ from interpolants on fewer nodes, which also gives error estimates; see [Neville's algorithm](/neville-algorithm/).
- **Newton form.** Coefficients by [divided differences](/divided-differences/), then nested evaluation; see [Newton interpolation](/newton-interpolation/).
- **Hermite data.** When derivatives are also given, the basis changes; see [Hermite interpolation](/hermite-interpolation/).
- **Exact fields.** Over $\mathbb{Q}$ or a finite field the same formula gives the coefficients; [fast interpolation](/fast-interpolation/) does it in $O(M(n) \log n)$.

## When to use it

Use the Lagrange form to prove things (existence, linearity, quadrature weights) and to evaluate a low-degree interpolant at a few points. For many evaluation points or a high degree, use the second barycentric form, which is $O(n)$ per point and handles the same data. For a degree above about 10 on a real interval, choose the nodes with care: [Chebyshev points](/chebyshev-nodes/) keep $\Lambda_n$ below $\tfrac{2}{\pi}\log(n+1) + 1$, while equispaced nodes give an exponentially large $\Lambda_n$ and the [Runge phenomenon](/runge-phenomenon/).

## Pitfalls

- **Repeated nodes.** If two nodes are equal, the denominator $x_i - x_j$ in line L5 is zero. Check that the nodes are distinct before the loop; for repeated nodes with derivative data, use [Hermite interpolation](/hermite-interpolation/).
- **Equispaced nodes of high degree.** For $f(x) = 1/(1 + 25 x^2)$ on $[-1, 1]$, the maximum error of the interpolant on a fine grid is about $1.9$ for 11 equispaced nodes and about $60$ for 21; at the Chebyshev points of the first kind it is about $0.11$ and $0.015$. This divergence is a property of the nodes, not of the formula or of rounding.
- **Converting to monomial coefficients.** Expanding $p_n$ into $\sum c_k x^k$ and then using [Horner's rule](/horner-rule/) brings in the ill-conditioned monomial basis; the [Vandermonde matrix](/vandermonde-matrix/) on $[-1, 1]$ has a condition number that grows exponentially in $n$. Evaluate the Lagrange or barycentric form directly.
- **Recomputing the denominators.** Line L5 recomputes $x_i - x_j$ for each evaluation point. For many points, store the weights $w_i$ once.

## Implementations

## History

Edward Waring published the formula in 1779. Euler used it in 1783, and Lagrange presented it in his lectures at the École normale in 1795; the name of Lagrange stuck. Meijering's chronology traces these steps. The rounding error analysis of the Lagrange and barycentric forms is due to Higham (2004), and Berrut and Trefethen (2004) argued for the barycentric form as the standard way to evaluate the Lagrange interpolant.

## References
