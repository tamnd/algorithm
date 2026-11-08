---
tag: 6W7GGA
kind: algorithm
slug: barycentric-interpolation
name: Barycentric interpolation
aliases:
- Barycentric Lagrange formula
- barycentric formula
- second barycentric form
- true barycentric formula
- modified Lagrange formula
area: numerical/interpolation-and-approximation
level: core
summary: Evaluate the interpolating polynomial as a ratio of two sums with barycentric weights w_j. The weights cost O(n^2) once (O(n) at Chebyshev points), each value O(n), and it is stable.
solves: [interpolation-problem]
model: floating-point-model
complexity:
  vars: {n: "the degree bound, with n + 1 distinct nodes"}
  time: {setup: Θ(n^2), per_point: Θ(n), add_node: Θ(n)}
  space: {extra: Θ(n)}
  flops: {setup: "2n^2 + 2n", per_point: "5n + 6"}
properties: {deterministic: true, recursive: false, exact_on_polynomials: true, stable_in_floating_point: true}
history:
  year: 1945
  people: [W. J. Taylor, Herbert E. Salzer, Heinz Rutishauser, Nicholas J. Higham, Jean-Paul Berrut, Lloyd N. Trefethen]
  note: Taylor gave the formula for equally spaced points in 1945, Salzer the simple weights for Chebyshev points in 1972, and Higham proved its numerical stability in 2004.
prereqs: [lagrange-interpolation, interpolating-polynomial-uniqueness]
see_also: [lagrange-interpolation, chebyshev-interpolation, chebyshev-nodes, newton-interpolation, neville-algorithm, lebesgue-constant, rational-approximation, vandermonde-matrix]
sources:
  - paper: doi:10.1137/S0036144502417715
    title: "Jean-Paul Berrut and Lloyd N. Trefethen, Barycentric Lagrange interpolation, SIAM Review 46(3) (2004) 501-517"
    locator: Sections 3 and 4 (the first and second barycentric forms and their cost), Section 5 (explicit weights for Chebyshev points), Section 7 (stability) and Section 10 (history)
  - paper: doi:10.1093/imanum/24.4.547
    title: "Nicholas J. Higham, The numerical stability of barycentric Lagrange interpolation, IMA Journal of Numerical Analysis 24(4) (2004) 547-556"
    locator: the backward stability of the first form and the forward error bound for the second form in terms of the Lebesgue constant
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 5, Barycentric interpolation formula (Theorems 5.1 and 5.2 and the weights for Chebyshev points)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Lemma 3.1 (the quantities theta_k and gamma_k used in the rounding error analysis) and Chapter 4 (summation)
  - paper: "Herbert E. Salzer, Lagrangian interpolation at the Chebyshev points x_(n,nu) = cos(nu pi/n), nu = 0(1)n; some unnoted advantages, The Computer Journal 15(2) (1972) 156-159"
    locator: the weights (-1)^j with halved end weights for the Chebyshev extreme points
  - paper: "W. J. Taylor, Method of Lagrangian curvilinear interpolation, Journal of Research of the National Bureau of Standards 35 (1945) 151-155"
    locator: the barycentric formula for equally spaced points
---

Barycentric interpolation evaluates the polynomial $p_n$ through $(x_0, y_0), \ldots, (x_n, y_n)$ by the formula
$$p_n(t) = \frac{\displaystyle\sum_{j=0}^{n} \frac{w_j\, y_j}{t - x_j}}{\displaystyle\sum_{j=0}^{n} \frac{w_j}{t - x_j}}, \qquad w_j = \frac{1}{\prod_{k \ne j} (x_j - x_k)}.$$
It is the [Lagrange form](/lagrange-interpolation/) rewritten so that the work that does not depend on $t$ is done once. The weights cost $O(n^2)$ for general nodes and nothing for [Chebyshev points](/chebyshev-nodes/), where they have closed forms. After that, each evaluation costs $O(n)$, and adding a node costs $O(n)$. In floating point it is stable: Higham (2004) proved that its error is governed by the [Lebesgue constant](/lebesgue-constant/), which is small for good nodes. Berrut and Trefethen (2004) argued that it should be the standard way to evaluate polynomial interpolants.

## In plain words

The Lagrange formula for the curve through some points rebuilds a long product for every point at which you want the curve, so it is slow when there are many points.

The barycentric formula first computes one number per data point, its weight, which depends only on where the data points are. To find the curve's value at a new place, you then make one pass over the data points. You add up the weighted values, add up the weights alone, and divide the first sum by the second. This is fast, and the division cancels most of the rounding error. With well-chosen points the result is accurate even with thousands of data points.

## The problem

The input is a list of $n + 1$ distinct nodes $x_0, \ldots, x_n$ (in any order), values $y_0, \ldots, y_n$ and a point $t$. The output is $p_n(t)$, where $p_n$ is the unique polynomial of degree at most $n$ with $p_n(x_j) = y_j$ ([uniqueness theorem](/interpolating-polynomial-uniqueness/)). Usually many points $t$ share the same nodes.

Notation on the interpolation and approximation pages: $f$ is a function on $[a, b]$, usually $[-1, 1]$, with data $y_j = f(x_j)$; $\ell_j$ is the Lagrange basis polynomial; $\omega(x) = \prod_{j=0}^{n} (x - x_j)$ is the node polynomial; $\Lambda_n = \max_{x \in [a, b]} \sum_j |\ell_j(x)|$ is the [Lebesgue constant](/lebesgue-constant/). Costs are floating-point operations, and rounding errors are measured in the [standard model](/floating-point-model/) with unit roundoff $u$ ($u = 2^{-53}$ in double precision) and $\gamma_k = ku/(1 - ku)$.

## The algorithm

**Derivation.** Since $\ell_j(t) = \omega(t)\, w_j/(t - x_j)$, the Lagrange form becomes the *first barycentric form* (also called the modified Lagrange formula)
$$p_n(t) = \omega(t) \sum_{j=0}^{n} \frac{w_j\, y_j}{t - x_j}.$$
The data $y_j = 1$ are interpolated by the constant 1, so $1 = \omega(t) \sum_j w_j/(t - x_j)$. Dividing the first form by this identity cancels $\omega(t)$ and gives the *second barycentric form*, the formula above. Any common factor of the weights cancels too, so the $w_j$ may be rescaled freely.

```pseudo id=main
BARYCENTRIC(x, y, t)                      ▷ x[0 .. n] distinct, y[0 .. n]
L1  for j ← 0 to n do                     ▷ weights: once per set of nodes
L2      w[j] ← 1
L3      for k ← 0 to n do
L4          if k ≠ j then w[j] ← w[j] / (x[j] − x[k])
L5  num ← 0;  den ← 0                     ▷ evaluation: once per point t
L6  for j ← 0 to n do
L7      if t = x[j] then return y[j]
L8      q ← w[j] / (t − x[j])
L9      num ← num + q · y[j];  den ← den + q
L10 return num / den
```

Lines L1 to L4 compute the weights; for many points $t$ they run once and lines L5 to L10 run for each $t$. Line L7 handles a point at a node, where the formula would divide by zero; the result there is exactly $y_j$, also in floating point.

**Weights for special nodes** (Berrut and Trefethen 2004, Section 5; Trefethen, Chapter 5). After a common factor is removed:

- Chebyshev points of the second kind $x_j = \cos(j\pi/n)$: $w_j = (-1)^j \delta_j$ with $\delta_0 = \delta_n = \tfrac{1}{2}$ and $\delta_j = 1$ otherwise (Salzer 1972).
- Chebyshev points of the first kind $x_j = \cos\big((2j + 1)\pi/(2n + 2)\big)$: $w_j = (-1)^j \sin\big((2j + 1)\pi/(2n + 2)\big)$.
- Equispaced points $x_j = a + jh$: $w_j = (-1)^j \binom{n}{j}$.

**Adding a node.** To add $x_{n+1}$, divide each old $w_j$ by $x_j - x_{n+1}$ and set $w_{n+1} = 1/\prod_{j \le n} (x_{n+1} - x_j)$, in $O(n)$ operations.

## Example

Take the nodes $0, 1, 2, 4$ with the data $1, 2, 4, 16$ (the values of $2^x$), as on the [Lagrange page](/lagrange-interpolation/), and $t = 3$.

| $j$ | $x_j$ | $y_j$ | $w_j$ | $q_j = w_j/(3 - x_j)$ | $q_j y_j$ |
|---|---|---|---|---|---|
| 0 | 0 | 1 | $\frac{1}{(0-1)(0-2)(0-4)} = -\frac{1}{8}$ | $-\frac{1}{24}$ | $-\frac{1}{24}$ |
| 1 | 1 | 2 | $\frac{1}{(1-0)(1-2)(1-4)} = \frac{1}{3}$ | $\frac{1}{6}$ | $\frac{8}{24}$ |
| 2 | 2 | 4 | $\frac{1}{(2-0)(2-1)(2-4)} = -\frac{1}{4}$ | $-\frac{1}{4}$ | $-1$ |
| 3 | 4 | 16 | $\frac{1}{(4-0)(4-1)(4-2)} = \frac{1}{24}$ | $-\frac{1}{24}$ | $-\frac{16}{24}$ |

So $\mathit{num} = -33/24$ and $\mathit{den} = -4/24 = -1/6$, and line L10 returns $33/4$, the same value as the Lagrange form. The denominator is $1/\omega(3) = 1/(-6)$, as the identity $\sum_j w_j/(t - x_j) = 1/\omega(t)$ requires.

## Correctness

The weights of lines L1 to L4 are $w_j = 1/\prod_{k \ne j} (x_j - x_k)$, so $\ell_j(t) = \omega(t) w_j/(t - x_j)$ for $t$ not a node. Then $\sum_j q_j y_j = p_n(t)/\omega(t)$ and $\sum_j q_j = 1/\omega(t)$, because $\sum_j \ell_j = 1$, and the ratio is $p_n(t)$; $\omega(t) \ne 0$ off the nodes. At a node, line L7 returns $y_j = p_n(x_j)$. The [full proof](proofs/correctness.md) gives the details and the rounding error bound below.

**Rounding errors.** Assume the standard model with no underflow or overflow, weights computed by lines L1 to L4 from the stored nodes, and $(3n + 3)u < 1$. Let $S_y = \sum_j |\ell_j(t) y_j|$ and $S_1 = \sum_j |\ell_j(t)| \le \Lambda_n$ for $t \in [a, b]$, and suppose $\gamma_{3n+2} S_1 < 1$. Then the computed value $\hat p$ satisfies
$$|\hat p - p_n(t)| \le \frac{(1 + u)\,\gamma_{3n+3}\, S_y + (u + \gamma_{3n+2}\, S_1)\, |p_n(t)|}{1 - \gamma_{3n+2}\, S_1}.$$
To first order this is about $3nu\,(S_y + \Lambda_n |p_n(t)|)$. It is the same form as Higham's bound for the second barycentric form: the formula is *forward stable* whenever $\Lambda_n$ is small, which holds at Chebyshev points ($\Lambda_n \le \tfrac{2}{\pi}\log(n+1) + 1$). Higham (2004) also proved that the first form is *backward stable*: its computed value is the exact interpolant of data $y_j(1 + \delta_j)$ with $|\delta_j|$ of order $nu$, for any distinct nodes. The second form is not backward stable in general, and for nodes with a huge $\Lambda_n$, such as many equispaced points, its error can exceed that of the first form.

## Complexity

The weights take $n$ subtractions and $n$ divisions for each of the $n + 1$ nodes, that is $2n^2 + 2n$ operations. Each evaluation does, for each node, one subtraction, one division, one multiplication and two additions in lines L8 and L9, and one final division: $5(n + 1) + 1 = 5n + 6$ operations. So $m$ evaluation points cost $2n^2 + 2n + m(5n + 6)$ operations, against $m(4n^2 + 6n + 2)$ for the direct Lagrange form. For Chebyshev or equispaced points the weights cost $O(n)$, or nothing. Extra space is $\Theta(n)$ for the weights. Adding a node costs $O(n)$.

Evaluation at $m$ points can be done faster than $O(mn)$ with the fast multipole method, but for typical sizes ($n$ up to a few thousand) the direct sum is simpler and fast enough.

## Properties

- **Exact on polynomials.** If the data come from a polynomial of degree at most $n$, the formula returns its value; with `Fraction` arithmetic it is exact.
- **Scale invariant weights.** Multiplying all $w_j$ by one nonzero constant does not change the result, which allows the closed forms above and avoids overflow.
- **Exact at nodes.** At $t = x_j$ the value is $y_j$ exactly.
- **Interpolating for any weights.** For any nonzero weights, the second form still interpolates the data, because as $t \to x_j$ the $j$-th terms dominate. With weights other than the true $w_j$ it is a rational interpolant; Berrut's choice $w_j = (-1)^j$ gives a rational interpolant with no poles on the real line.
- **Order free.** The nodes need not be sorted.
- **Stable.** Forward stable when $\Lambda_n$ is small (second form) and backward stable for any nodes (first form), by Higham's analysis.

## Variants and improvements

- **First form.** $p_n(t) = \omega(t) \sum_j w_j y_j/(t - x_j)$, backward stable, at the cost of computing $\omega(t)$ in $O(n)$.
- **Chebyshev interpolation.** With the closed form weights, the second form is the evaluation step of [Chebyshev interpolation](/chebyshev-interpolation/) in systems such as Chebfun.
- **Rational barycentric interpolation.** Other weights give rational interpolants: Berrut's weights, the Floater and Hormann family for equispaced data, and the AAA algorithm, which chooses support points and weights greedily (see [rational approximation](/rational-approximation/)).
- **Trigonometric interpolation.** A barycentric formula with $\cot$ or $\csc$ kernels evaluates [trigonometric interpolants](/trigonometric-interpolation/) at equispaced points on a periodic interval.
- **Hermite data.** A barycentric form exists for [Hermite interpolation](/hermite-interpolation/), with weights for each derivative order.
- **Derivatives.** The derivative of $p_n$ at the nodes has the differentiation matrix $D_{ij} = (w_j/w_i)/(x_i - x_j)$ for $i \ne j$, with $D_{ii} = -\sum_{j \ne i} D_{ij}$; this is the basis of spectral collocation.

## When to use it

Use the second barycentric form whenever you need values of a polynomial interpolant: at many points, at high degree, or with nodes that may be extended. With Chebyshev points it is the method of choice, at $O(n)$ per point with no setup and stable for $n$ in the thousands. For monomial coefficients of $p_n$, which are rarely needed, solve a [Vandermonde system](/vandermonde-matrix/) or expand the [Newton form](/newton-interpolation/), and accept the ill-conditioning. For equispaced data of high degree no evaluation formula helps: the interpolant itself is ill conditioned, so use a lower degree, splines, or rational barycentric weights.

## Pitfalls

- **Overflow and underflow of the weights.** For $n$ in the thousands on $[-1, 1]$, the products in line L4 overflow or underflow; for Chebyshev points $|w_j|$ grows like $2^n/n$. Use the closed forms, rescale the nodes, or compute the weights with a common scale factor (or logarithms), since a common factor cancels.
- **A point at or near a node.** Line L7 catches exact equality. For $t$ extremely close to $x_j$, the term $w_j/(t - x_j)$ is huge in both sums and the ratio is still accurate: the large terms cancel in the quotient, so no special test beyond equality is needed.
- **Monomial coefficients.** Do not convert $p_n$ to $\sum c_k t^k$ and use [Horner's rule](/horner-rule/). For $f(x) = 1/(1 + 25x^2)$ at $n + 1$ Chebyshev points of the second kind, measured on a fine grid in double precision, the barycentric error is $1.2 \times 10^{-7}$ at $n = 80$ and $1.4 \times 10^{-14}$ at $n = 160$, while solving the Vandermonde system by Gaussian elimination with partial pivoting and then using Horner's rule gives $1.1 \times 10^{-3}$ and $1.4 \times 10^{-2}$; the monomial coefficients reach $10^{13}$. For $\sin(20x)$ at $n = 80$ the errors are $2.6 \times 10^{-15}$ against $8.8 \times 10^{-8}$.
- **Equispaced nodes.** The formula evaluates the equispaced interpolant accurately when $\Lambda_n$ is moderate, but the interpolant itself diverges for functions like $1/(1 + 25x^2)$ (the [Runge phenomenon](/runge-phenomenon/)), and $\Lambda_n$ grows like $2^n$, so the second form loses accuracy as well.
- **Repeated nodes.** Equal nodes make line L4 divide by zero; check that the nodes are distinct.

## Implementations

## History

W. J. Taylor gave the barycentric formula for equally spaced nodes in 1945, and the name barycentric was used by Dupuy in 1948. Salzer (1972) found the simple weights for the Chebyshev extreme points. Rutishauser (1976) and Henrici (1979) discussed the stability of the two forms, and Werner (1984) gave the $O(n)$ update of the weights. Higham (2004) proved the backward stability of the first form and the forward stability of the second form for nodes with a small Lebesgue constant. In the same year, Berrut and Trefethen's survey argued that the barycentric formula, not the Newton form, should be the standard method for polynomial interpolation. It is now the evaluation step in Chebfun.

## References
