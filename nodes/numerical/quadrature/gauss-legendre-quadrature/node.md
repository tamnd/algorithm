---
tag: ACS9SM
kind: algorithm
slug: gauss-legendre-quadrature
name: Gauss-Legendre quadrature
aliases:
- Gauss-Legendre rule
- Gauss-Legendre formula
- Legendre-Gauss quadrature
area: numerical/quadrature
level: advanced
summary: The n-point Gaussian rule on [-1,1] with w = 1, whose nodes are the roots of the Legendre polynomial. It is exact to degree 2n-1 and converges geometrically for analytic f.
solves: [numerical-integration, gauss-nodes-and-weights]
model: floating-point-model
complexity:
  vars: {n: "the number of nodes", m: "the number of panels"}
  time: {worst: "O(n^2)"}
  space: {extra: Θ(n)}
  evaluations: {worst: "n m"}
properties: {deterministic: true, degree_of_precision: "2n-1", positive_weights: true, nested: false, open: true}
history:
  year: 1814
  people: [Carl Friedrich Gauss, Carl Gustav Jacob Jacobi]
  note: Gauss derived the rules in 1814 and computed them up to seven nodes. Jacobi showed in 1826 that the nodes are the zeros of the Legendre polynomial.
prereqs: [gaussian-quadrature, legendre-polynomials]
see_also: [gauss-quadrature-theorem, golub-welsch-algorithm, gauss-nodes-and-weights, gauss-kronrod-quadrature, gauss-lobatto-quadrature, clenshaw-curtis-quadrature, newton-raphson-method, composite-quadrature]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 2, the section on integration rules of Gauss type (Section 2.7), Gauss-Legendre rules and their error
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 19, Clenshaw-Curtis and Gauss quadrature (the Bernstein ellipse bound and the comparison with Clenshaw-Curtis)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Chapter 5, Section 5.3, Gaussian numerical integration (the Gauss-Legendre error formula)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 10, Numerical integration II (Gauss quadrature on [-1, 1])
  - book: isbn:9780198506720
    title: Walter Gautschi, Orthogonal Polynomials, Computation and Approximation, Oxford University Press, 2004
    locator: Chapter 1, Section 1.4 (Gauss-type quadrature rules)
  - paper: "Nicholas Hale and Alex Townsend, Fast and accurate computation of Gauss-Legendre and Gauss-Jacobi quadrature nodes and weights, SIAM Journal on Scientific Computing 35(2) (2013) A652-A674"
    locator: Newton iteration with asymptotic initial guesses and O(n) total cost
  - paper: "Carl Friedrich Gauss, Methodus nova integralium valores per approximationem inveniendi, Commentationes Societatis Regiae Scientiarum Gottingensis Recentiores 3 (1814)"
    locator: the original derivation and tables
  - paper: "Lloyd N. Trefethen, Is Gauss quadrature better than Clenshaw-Curtis?, SIAM Review 50(1) (2008) 67-87"
    locator: the comparison of the two rules in practice
---

Gauss-Legendre quadrature approximates $\int_{-1}^1 f(x)\,dx$ by $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$ with the $n$ nodes at the zeros of the [Legendre polynomial](/legendre-polynomials/) $P_n$ and the weights $w_i = 2/((1 - x_i^2)P_n'(x_i)^2)$. It is the case $w = 1$ of [Gaussian quadrature](/gaussian-quadrature/), so it is exact for all polynomials of degree at most $2n - 1$. For $f$ analytic in a Bernstein ellipse $E_\rho$ the error is $O(\rho^{-2n})$, and for $f \in C^{2n}$ it is $c_n f^{(2n)}(\xi)$ with an explicit constant. This page computes the rule by [Newton's method](/newton-raphson-method/) on $P_n$ with safe brackets, in $O(n^2)$ operations, and applies it on any interval $[a, b]$.

## In plain words

To find the area under a curve on an interval, Gauss-Legendre quadrature looks at the curve at a few carefully chosen points, multiplies each height by a weight, and adds. The points are not equally spaced: they crowd toward the ends of the interval, and they are the roots of a classical polynomial named after Legendre. With $n$ points the answer is exact for every polynomial up to degree $2n - 1$. For smooth functions the error shrinks very fast as $n$ grows, often reaching machine precision with 10 to 30 points. For functions with kinks or singularities it still works, but much more slowly.

## The problem

**Notation.** As on all quadrature pages: $I(f) = \int_a^b f(x)\,dx$ (here $w = 1$); $Q_n(f) = \sum_{i=1}^n w_i f(x_i)$, where $n$ counts nodes; $E_n(f) = I(f) - Q_n(f)$; $d$ is the [degree of precision](/degree-of-precision/). For composite rules, $h = (b - a)/m$ is the width of each of $m$ panels.

Given $n \ge 1$, compute the nodes and weights of the $n$-point rule on $[-1, 1]$. Given also $f$ and a finite interval $[a, b]$, return

$$Q_n(f; a, b) = \frac{b - a}{2} \sum_{i=1}^n w_i\, f\Bigl(\frac{a + b}{2} + \frac{b - a}{2} x_i\Bigr),$$

which is the rule mapped by the affine change of variables. The map keeps the degree of precision. It also covers $b < a$ (the factor $(b - a)/2$ is negative) and gives $0$ for $a = b$.

## The algorithm

Write the nodes in decreasing order as $x = \cos\theta_i$. By Bruns' inequality, $\theta_i \in \bigl((i - \frac12)\pi/(n + \frac12),\ i\pi/(n + \frac12)\bigr)$, so each node has a bracket that contains no other node. Newton's method starts at the middle of the bracket, $\cos((i - \frac14)\pi/(n + \frac12))$, and $P_n$, $P_{n-1}$ come from Bonnet's recurrence $(k + 1)P_{k+1} = (2k + 1)xP_k - kP_{k-1}$.

```pseudo id=main
GAUSS-LEGENDRE(n)                               ▷ n ≥ 1
L1  for i ← 1 to ⌊n/2⌋ do                       ▷ positive nodes, largest first
L2      [lo, hi] ← [cos(iπ/(n+½)), cos((i−½)π/(n+½))]; x ← cos((i−¼)π/(n+½))
L3      repeat
L4          compute P_n(x) and P_(n−1)(x) by Bonnet's recurrence
L5          P' ← n(x P_n(x) − P_(n−1)(x)) / (x^2 − 1)
L6          shrink [lo, hi] to the half that keeps the sign change; δ ← P_n(x)/P'
L7          if |δ| ≤ 2u|x| then x ← x − δ and leave the loop; else x ← x − δ if inside (lo, hi), else (lo + hi)/2
L8      w ← 2 / ((1 − x^2) P'^2)
L9      store (x, w) and its mirror (−x, w)
L10 if n is odd then store the node 0 with weight 2/P_n'(0)^2
L11 return the nodes in increasing order and their weights
```

Line L5 uses the identity $(x^2 - 1)P_n' = n(xP_n - P_{n-1})$, so one pass of the recurrence gives both $P_n$ and $P_n'$. Line L6 keeps a bracket, so a bad Newton step falls back to bisection (line L7) and the iteration cannot jump to a neighbouring zero. Line L7 stops when the Newton correction is below the rounding level of $x$. The final weight is computed at the converged node (line L8). Symmetry halves the work (line L9), and for odd $n$ the middle node is exactly $0$ (line L10). The implementation recomputes $P_n$ and $P_n'$ once at the final $x$ before line L8.

## Example

Take $n = 5$. For $i = 1$ the bracket is $[0.84125, 0.95949]$ and Newton starts at $0.90963$:

| step | $x$ | $P_5(x)$ | $P_5'(x)$ | correction $\delta$ |
|---|---|---|---|---|
| 0 | $0.9096319953545184$ | $2.41 \times 10^{-2}$ | $7.112693$ | $3.39 \times 10^{-3}$ |
| 1 | $0.9062388229618967$ | $4.05 \times 10^{-4}$ | $6.874440$ | $5.90 \times 10^{-5}$ |
| 2 | $0.9061798635561052$ | $1.21 \times 10^{-7}$ | $6.870335$ | $1.76 \times 10^{-8}$ |
| 3 | $0.9061798459386655$ | $1.04 \times 10^{-14}$ | $6.870333$ | $1.51 \times 10^{-15}$ |
| 4 | $0.906179845938664$ | $-1.8 \times 10^{-16}$ | $6.870333$ | $-2.6 \times 10^{-17}$ |

The correction falls quadratically, and at step 4 it is below $2u|x|$, so the loop stops. The second node, from the bracket $[0.41542, 0.65486]$, converges to $0.5384693101056831$ in four steps as well. The rule is

| $x_i$ | $\pm 0.9061798459386640$ | $\pm 0.5384693101056831$ | $0$ |
|---|---|---|---|
| $w_i$ | $0.2369268850561891$ | $0.4786286704993664$ | $0.5688888888888889 = \tfrac{128}{225}$ |

Applied on $[0, 1]$ to $e^x$, it gives $1.7182818284583912$, an error of $6.54 \times 10^{-13}$ with 5 evaluations. The error formula below predicts $E_5 = \frac{(5!)^4}{11\,((10)!)^3} e^{\xi}$ with $\xi \in [0, 1]$, between $3.94 \times 10^{-13}$ and $1.07 \times 10^{-12}$; the value at $\xi = \frac12$ is $6.50 \times 10^{-13}$.

## Correctness

Bonnet's recurrence defines $P_n$, and the derivative identity follows from orthogonality: $(x^2 - 1)P_n' - nxP_n$ has degree at most $n - 1$, is orthogonal to all polynomials of degree $n - 2$, and equals $-n$ at $x = 1$. The weight formula follows by applying the rule exactly to $P_{n-1}(x)P_n(x)/(x - x_i)$, of degree $2n - 2$, which gives $w_i = 2/(nP_{n-1}(x_i)P_n'(x_i))$, and then using the derivative identity at the zero. The Bruns brackets are disjoint and each holds one sign change of $P_n$, so the safeguarded iteration converges to the right zero. The full proof is in [the correctness proof](proofs/correctness.md).

**Error formula (proved).** For $f \in C^{2n}[a, b]$ there is $\xi \in [a, b]$ with

$$E_n(f) = \frac{(b - a)^{2n+1}(n!)^4}{(2n + 1)\,((2n)!)^3}\, f^{(2n)}(\xi).$$

This is part 6 of the [Gauss quadrature theorem](/gauss-quadrature-theorem/) with $\int_{-1}^1 \tilde P_n^2 = \frac{2^{2n+1}(n!)^4}{(2n+1)((2n)!)^2}$ for the monic $\tilde P_n$, scaled to $[a, b]$. For $n = 1$ it is the midpoint error $\frac{(b-a)^3}{24}f''(\xi)$, and for $n = 2$ it is $\frac{(b-a)^5}{4320}f^{(4)}(\xi)$.

**Analytic $f$ (proved).** If $f$ is analytic in the open Bernstein ellipse $E_\rho$ for $[-1, 1]$, $\rho > 1$, with $|f| \le M$ there, and $n \ge 2$, then $|E_n(f)| \le \frac{64}{15}\,\frac{M\rho^{2-2n}}{\rho^2 - 1}$. The proof is on the theorem page.

## Complexity

The cost model counts evaluations of $f$, and separately the operations that build the rule.

- **Evaluations.** $n$ per rule, and $nm$ for the composite rule on $m$ panels.
- **Building the rule.** Each Newton step costs $O(n)$ for the recurrence. In the implementation the average number of recurrence passes per positive node is 6.0, 5.1 and 4.9 for $n = 10, 100, 1000$ (including the bracket test and the final weight). So the cost is $O(n^2)$ operations; $n = 1000$ took 0.47 seconds in pure Python. Evaluating $P_n$ by asymptotic expansions instead of the recurrence makes it $O(n)$ in all (Hale and Townsend 2013).
- **Space.** $\Theta(n)$ for the nodes and weights.
- **Rate.** For analytic $f$, the number of nodes for a tolerance $\tau$ is about $\log(1/\tau)/(2\log\rho)$. For $f$ with a singularity on $[a, b]$ the error is algebraic in $n$, and a [composite](/composite-quadrature/) or [adaptive](/adaptive-quadrature/) scheme is needed.

## Properties

- **Degree $2n - 1$, positive weights.** The weights add up to $2$, so $\sum_i |w_i| = 2$ for every $n$: the rule converges for every continuous $f$ and amplifies no rounding errors in the values $f(x_i)$.
- **Open rule.** No node is at $\pm 1$; the distance from the largest node to $1$ is about $2.9/n^2$. So an integrable endpoint singularity is never evaluated.
- **Nodes cluster at the ends** with the density $\frac{n}{\pi\sqrt{1 - x^2}}$, like [Chebyshev points](/chebyshev-nodes/).
- **Not nested.** The 5-point and 10-point rules share no nodes. For error estimation, pair the rule with its [Kronrod extension](/gauss-kronrod-quadrature/).
- **Accuracy of the computed rule.** Against the Golub-Welsch code, the nodes agreed to within $1.7 \times 10^{-15}$ and the weights to a relative $8.7 \times 10^{-12}$ for $n = 500$; the weights sum to $2$ within $10^{-15}$.

## Variants and improvements

- **Composite Gauss-Legendre.** Apply the $n$-point rule on each of $m$ panels of width $h$; for $f \in C^{2n}$ the error is $\frac{(b-a)h^{2n}(n!)^4}{(2n+1)((2n)!)^3}f^{(2n)}(\xi)$. With $n = 3$ the measured rate for $e^x$ is $h^6$, and for $\sqrt{x}$ it drops to $h^{3/2}$ because of the left panel.
- **Gauss-Kronrod.** The $(2n+1)$-point Kronrod extension reuses the $n$ Gauss values and gives an error estimate; G7-K15 is the standard panel rule of QUADPACK.
- **Gauss-Radau and Gauss-Lobatto.** Include one or both endpoints, with degree $2n - 2$ or $2n - 3$; used in spectral element methods and in implicit Runge-Kutta methods.
- **Golub-Welsch.** The eigenvalue method gives the same rule with $O(n^2)$ work for any weight.
- **Fast methods.** Glaser, Liu and Rokhlin (2007) integrate an ODE for the zeros, Hale and Townsend (2013) use Newton with asymptotic expansions of $P_n$, and Bogaert (2014) gives explicit asymptotic formulas with $O(1)$ cost per node, so rules with millions of nodes take well under a second in compiled code.
- **Gauss-Jacobi.** Put a known endpoint singularity $(1 - x)^\alpha(1 + x)^\beta$ into the weight; see [Gauss-Jacobi quadrature](/gauss-jacobi-quadrature/).

## When to use it

Use Gauss-Legendre for a smooth integrand on a finite interval when $n$ can be chosen in advance, when evaluations are expensive, or as the panel rule inside composite and adaptive schemes. It is the default rule in finite element codes (tensor products on squares and cubes). For a nested family, use [Clenshaw-Curtis](/clenshaw-curtis-quadrature/), which is about as accurate for most functions and computable by FFT. For singular, kinked or strongly oscillatory integrands, use adaptive, transformed or [oscillatory](/oscillatory-integration/) methods.

## Pitfalls

- **Expecting a fast rate for nonsmooth $f$.** Measured errors at $n = 4, 8, \ldots, 64$ fall like $n^{-3}$ for $\sqrt{x}$, $n^{-2}$ for $\log x$, and $n^{-1}$ for $x^{-1/2}$ on $[0, 1]$. The rule gives a finite number for $x^{-1/2}$, which can hide the singularity.
- **Kinks and jumps inside the interval.** For $|x - 0.3|$ the errors at $n = 10, 40, 160$ are $6.8 \times 10^{-3}$, $4.3 \times 10^{-4}$ and $3.7 \times 10^{-5}$, slow and not monotone. Split the interval at the kink.
- **Oscillation.** For $\cos 30x$ on $[-1, 1]$ the 10-point rule has error above $10^{-2}$, and convergence starts only once $n$ exceeds about $30$; Gauss needs about $\pi$ nodes per wavelength.
- **Starting Newton from equispaced or Chebyshev guesses without a bracket.** The iteration can converge to a neighbouring zero, so two nodes come out equal and one is missing. The bracket of line L2 prevents this.
- **Cancellation in $1 - x^2$.** For nodes near $\pm 1$, compute $(1 - x)(1 + x)$, as the implementation does, not $1 - x \cdot x$.
- **Copying tabulated values.** A typo or a truncated digit in a hand-copied table breaks the degree of precision silently; computing the rule is cheap, and checking $Q_n(x^k)$ for $k \le 2n - 1$ catches such errors.
- **Long intervals or large values.** The rounding error of $Q_n$ is about $u\sum_i |w_i f(x_i)| \cdot (b - a)/2$; an absolute tolerance below that cannot be reached.

## Implementations

## History

Gauss presented the method in 1814 in "Methodus nova integralium valores per approximationem inveniendi", derived through continued fractions and the hypergeometric series, and he computed the nodes and weights for up to seven points. Jacobi (1826) gave the proof by orthogonality and identified the nodes as the zeros of the Legendre polynomial. Christoffel (1858) generalized the construction to other weights. Tables of Gauss-Legendre rules were a staple of numerical handbooks until the 1960s, when Golub and Welsch (1969) and Newton codes made the computation routine. Since 2007, fast methods have made rules with millions of nodes practical.

## References
