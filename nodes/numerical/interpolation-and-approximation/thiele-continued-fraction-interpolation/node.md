---
tag: D0H64Z
kind: algorithm
slug: thiele-continued-fraction-interpolation
name: Thiele continued-fraction interpolation
aliases:
- Thiele interpolation
- Thiele's interpolation formula
- Interpolation by inverse differences
area: numerical/interpolation-and-approximation
level: research
summary: Builds the rational interpolant through n points as a continued fraction whose coefficients are inverse differences. O(n^2) to build, O(n) to evaluate; it can detect unattainable points.
solves: [rational-approximation]
model: real-ram
complexity:
  vars: {n: the number of nodes}
  time: {fit: Θ(n^2), evaluate: Θ(n)}
  space: {extra: Θ(n)}
  flops: {fit: "1.5 n^2", evaluate: "7 n"}
properties: {deterministic: true, recursive: false, interpolates: true, linear_in_data: false, exact_on_rational_functions: true, can_fail_on_unattainable_points: true}
history:
  year: 1909
  people: [Thorvald N. Thiele]
  note: Thiele's Interpolationsrechnung (1909) introduced the continued fraction with reciprocal and inverse differences; Bulirsch and Stoer (1964) made rational interpolation a standard tool for extrapolation.
prereqs: [rational-approximation, continued-fraction, newton-interpolation]
see_also: [pade-approximation, neville-algorithm, bulirsch-stoer-method, sequence-extrapolation, polynomial-interpolation, runge-phenomenon, barycentric-interpolation, minimax-approximation]
sources:
  - paper: "Thorvald N. Thiele, Interpolationsrechnung, B. G. Teubner, Leipzig, 1909"
    locator: the interpolating continued fraction and reciprocal differences
  - book: isbn:9780387954523
    title: Josef Stoer and Roland Bulirsch, Introduction to Numerical Analysis, third edition, Springer, 2002
    locator: Section 2.2, Interpolation by rational functions (unattainable points, inverse and reciprocal differences, Thiele's continued fraction, Neville-type algorithms)
  - book: isbn:9780521450072
    title: George A. Baker Jr. and Peter Graves-Morris, Padé Approximants, second edition, Cambridge University Press, 1996
    locator: the chapter on multipoint Padé approximants (Thiele's continued fraction and reciprocal differences)
  - paper: "Roland Bulirsch and Josef Stoer, Fehlerabschätzungen und Extrapolation mit rationalen Funktionen bei Verfahren vom Richardson-Typus, Numerische Mathematik 6 (1964) 413-427"
    locator: rational extrapolation to the limit by a Neville-type recurrence
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 26, Rational interpolation and linearized least-squares (nonexistence, unattainable points and spurious poles)
---

Thiele's continued-fraction interpolation finds a rational function, a quotient of two polynomials, that takes prescribed values at $n$ points. It writes the answer as a continued fraction
$$R(t) = b_0 + \cfrac{t - x_0}{b_1 + \cfrac{t - x_1}{b_2 + \cdots + \cfrac{t - x_{n-2}}{b_{n-1}}}}$$
whose coefficients $b_k$ are **inverse differences**, computed by a triangular table much like Newton's divided differences. Rational interpolants can follow poles and steep behaviour that defeat polynomials, but they may not exist: some data sets have **unattainable points**, and the algorithm must notice them.

## In plain words

Polynomials are poor at imitating functions that blow up, level off, or turn sharply, and passing a polynomial through many equally spaced points can make it swing wildly. A ratio of two polynomials handles such shapes much better.

Thiele's method builds such a ratio through given points one point at a time, as a nested fraction: a number plus a fraction whose denominator is a number plus another fraction, and so on. Each new level is chosen so that the next point is matched without disturbing the earlier ones.

The catch is that a ratio of polynomials of the allowed size does not always exist for the given values. The method then hits a zero divided by zero, and a careful implementation reports it instead of returning a wrong value.

## The problem

Notation on the interpolation pages: distinct nodes $x_0, \ldots, x_{n-1}$ with values $y_i = f(x_i)$; a rational function has **type** $(\mu, \nu)$ when it can be written $p/q$ with $\deg p \le \mu$, $\deg q \le \nu$, $q \not\equiv 0$; $\infty$ is the point at infinity, with $c/0 = \infty$ for $c \ne 0$ and $c/\infty = 0$.

**Rational interpolation.** Given the data and $\mu + \nu = n - 1$, find $R = p/q$ of type $(\mu, \nu)$ with $R(x_i) = y_i$. The **linearized** problem asks only $p(x_i) = y_i\, q(x_i)$; it always has a nonzero solution (a homogeneous linear system with $n + 1$ unknowns and $n$ equations), and all its solutions define the same rational function $p/q$. The original problem is solvable exactly when this reduced $p/q$ takes the value $y_i$ at every node. A node where the reduced $p/q$ does not take the value $y_i$ is **unattainable**; there every linearized solution has $p(x_i) = q(x_i) = 0$.

Thiele's fraction with $n$ coefficients has type $(\lceil (n-1)/2 \rceil, \lfloor (n-1)/2 \rfloor)$, the diagonal or one-above-diagonal entry, which is the usual choice.

**Inverse differences.** With $\varphi_0(x_i) = y_i$ and, for $k \ge 1$ and $i \ge k$,
$$\varphi_k(x_i) = \frac{x_i - x_{k-1}}{\varphi_{k-1}(x_i) - \varphi_{k-1}(x_{k-1})},$$
the coefficients are $b_k = \varphi_k(x_k)$. Unlike divided differences, inverse differences depend on the order of the nodes and may be $\infty$.

## The algorithm

```pseudo id=main
THIELE(x_0..x_(n-1), y_0..y_(n-1), t)
L1  φ_i ← y_i for i = 0..n−1
L2  for k = 1..n−1: for i = k..n−1: φ_i ← (x_i − x_(k−1)) / (φ_i − φ_(k−1)), with ∞ ↦ 0 and c/0 ↦ ∞; then move a finite φ_i to position k, or stop if all are ∞
L3  b_k ← φ_k for the m coefficients kept
L4  for k = 1..m−1: (A_k, B_k) ← b_k (A_(k−1), B_(k−1)) + (t − x_(k−1)) (A_(k−2), B_(k−2)), from (A_(−1), B_(−1)) = (1, 0), (A_0, B_0) = (b_0, 1)
L5  return A_(m−1) / B_(m−1), or ∞ if only B vanishes, or report 0/0
```

Line L2 overwrites one array in place, as in the divided difference table, so the fit uses $\Theta(n)$ memory. If $\varphi_{k-1}(x_i)$ equals the pivot, the current partial fraction already matches $x_i$ and $\varphi_k(x_i) = \infty$; such nodes are moved behind a node with finite $\varphi_k$, and if every remaining node has $\varphi_k = \infty$ the fraction stops early with $m = k$ coefficients, which happens when the data come from a rational function of lower type.

Lines L4 and L5 evaluate the fraction through the three-term recurrence for its numerator and denominator (the fundamental recurrence of [continued fractions](/continued-fraction/)), so that a node $t = x_k$ needs no special case and a $0/0$ is detected. The backward evaluation $r \leftarrow b_k + (t - x_k)/r$ is cheaper, three flops per level, but must special-case $r = 0$ and cannot tell a pole from an unattainable point.

## Example

**By hand.** Take $f(t) = 1/(1 + t)$ at $x = 0, 1, 2$, so $y = 1, \tfrac12, \tfrac13$.

| $i$ | $x_i$ | $\varphi_0$ | $\varphi_1$ | $\varphi_2$ |
|---|---|---|---|---|
| 0 | 0 | $1$ | | |
| 1 | 1 | $\tfrac12$ | $\dfrac{1 - 0}{\tfrac12 - 1} = -2$ | |
| 2 | 2 | $\tfrac13$ | $\dfrac{2 - 0}{\tfrac13 - 1} = -3$ | $\dfrac{2 - 1}{-3 - (-2)} = -1$ |

So $b = (1, -2, -1)$ and
$$R(t) = 1 + \cfrac{t}{-2 + \cfrac{t - 1}{-1}} = 1 + \frac{t}{-1 - t} = \frac{1}{1 + t},$$
the function itself: Thiele interpolation reproduces rational functions of the fraction's type exactly. Through four points of $t^2$ at $0, 1, 2, 3$ it gives $b = (0, 1, -2, -1)$ and reproduces $t^2$, a polynomial of degree 2 inside type $(2, 1)$.

**An unattainable point.** For $x = 0, 1, 2$ and $y = 1, 2, 2$ the inverse differences give $b = (1, 1, 1)$, $A_2 = 2t$, $B_2 = t$. As a rational function $R = 2$, which misses $y_0 = 1$; at $t = 0$ the evaluation meets $0/0$. Solving the linearized system directly confirms it: $p = 2t$, $q = t$ (up to a factor) is the only solution, so no rational function of type $(1, 1)$ takes these values.

**Rational against polynomial.** Equally spaced nodes, maximum error at 400 points in double precision:

| function and interval | $n$ | Thiele | polynomial |
|---|---|---|---|
| $\tan t$ on $[-1.5, 1.5]$ | 9 | $3.4 \times 10^{-4}$ | $2.6$ |
| | 17 | $2.0 \times 10^{-11}$ | $0.77$ |
| | 33 | $9.2 \times 10^{-13}$ | $8.6 \times 10^{-2}$ |
| $e^t$ on $[-1, 1]$ | 9 | $1.9 \times 10^{-9}$ | $5.8 \times 10^{-8}$ |
| | 17 | $3.8 \times 10^{-14}$ | $1.3 \times 10^{-13}$ |
| | 33 | $5.7 \times 10^{-12}$ | $4.4 \times 10^{-9}$ |
| $\lvert t \rvert$ on $[-1, 1]$ | 9 | $3.3 \times 10^{-2}$ | $0.32$ |
| | 33 | $5.1 \times 10^{-3}$ | $1.0 \times 10^{5}$ |

The poles of $\tan$ at $\pm\pi/2$ lie just outside the interval and ruin the polynomial, while the rational interpolant places poles near them. For [Runge's function](/runge-phenomenon/) $1/(1 + 25t^2)$, which is rational of type $(0, 2)$, the algorithm in exact arithmetic stops after 5 coefficients for 5, 9 or 17 nodes and reproduces it exactly. The $e^t$ rows also show rounding: with 33 nodes the rational error grows from $10^{-14}$ to $10^{-12}$ (observed, not a bound).

## Correctness

Write $P_k(t; w)$ for the numerator and denominator pair of the fraction $b_0, \ldots, b_{k-1}$ with last partial denominator $w$ in place of $b_k$: $P_k(t; w) = w\,(A_{k-1}, B_{k-1}) + (t - x_{k-1})(A_{k-2}, B_{k-2})$, with $P_k(t; \infty) = (A_{k-1}, B_{k-1})$. The recurrence gives the tail identity $P_k(t; w) = w\, P_{k-1}\big(t; b_{k-1} + (t - x_{k-1})/w\big)$, and the definition of inverse differences says exactly that $\varphi_{k-1}(x_i) = b_{k-1} + (x_i - x_{k-1})/\varphi_k(x_i)$. By induction on $k$, $P_k(x_i; \varphi_k(x_i))$ is a multiple of $(y_i, 1)$ for every remaining node; for $x_k$ this is $A_k(x_k) = y_k B_k(x_k)$, and the recurrence preserves the relation at earlier nodes because the factor $t - x_{k-1}$ vanishes at $x_{k-1}$. So the output solves the linearized problem at all nodes, and $B \not\equiv 0$ by the determinant formula $A_k B_{k-1} - A_{k-1} B_k = \pm \prod_{j<k} (t - x_j)$. Hence $R(x_i) = y_i$ wherever $B(x_i) \ne 0$, and a $0/0$ at a node is reported. The full proof, with the $\infty$ cases and the early stop, is in the proof file.

## Complexity

- **Fit:** $n(n-1)/2$ inverse differences, each with two subtractions and a division, so about $1.5\, n^2$ flops and $\Theta(n)$ memory when the table is overwritten in place.
- **Evaluation:** $\Theta(n)$ per point: seven flops per level with the three-term recurrence, three with backward evaluation.
- **Adding a node** costs $\Theta(n)$ more inverse differences, as with Newton's form; the fraction is extended, not rebuilt.

## Properties

- **Exact on rational functions:** if $f$ is rational of the fraction's type and has no pole at the nodes, the interpolant is $f$ (exact arithmetic).
- **Uniqueness:** when the rational interpolation problem is solvable, its solution is unique as a rational function, so in exact arithmetic the result does not depend on the order of the nodes, although the $b_k$ do.
- **Not linear in the data**, unlike polynomial interpolation; scaling $y$ is fine, adding two data sets is not.
- **Convergence is not guaranteed.** Rational interpolants of analytic functions can have spurious poles, pole-zero pairs (Froissart doublets) that appear inside the interval and move with the data; there is no general convergence theorem for equally spaced nodes comparable to the polynomial theory. Good behaviour, as in the table, is observed rather than proved.
- **Order dependence in floating point:** different node orders give different rounding errors and different near-singular inverse differences.

## Variants and improvements

- **Reciprocal differences.** Thiele's symmetric differences $\rho_k$ do not depend on the order of the nodes; the coefficients are $b_k = \rho_k - \rho_{k-2}$. They allow a table built in the usual sliding order.
- **Neville-type rational recurrence (Bulirsch and Stoer 1964).** Evaluates the diagonal rational interpolant at one point without forming coefficients, the [Neville algorithm](/neville-algorithm/) of rational interpolation; used for rational extrapolation to $h = 0$ in the [Bulirsch-Stoer method](/bulirsch-stoer-method/) and Romberg-type schemes.
- **Pivoting for reliability.** Reordering nodes when an inverse difference is infinite or nearly so, as done here, is the idea behind the reliable algorithms of Werner and of Graves-Morris; they also certify unattainable points.
- **Barycentric rational interpolation.** Floater-Hormann interpolants have no real poles by construction, at the price of lower order; AAA (Nakatsukasa, Sète and Trefethen 2018) chooses support points greedily and is the modern default for rational approximation from samples.
- **Multipoint Padé approximation.** With repeated nodes, Thiele interpolation becomes Hermite rational interpolation; with all nodes at one point it gives the [Padé approximant](/pade-approximation/), and the fraction becomes the corresponding continued fraction.

## When to use it

Use Thiele interpolation for smooth data from functions with poles or steep fronts near the interval, for extrapolating a sequence of computed values to a limit, and for building a compact rational model of a tabulated function, with exact or high-precision arithmetic when possible. For general approximation from many samples prefer barycentric forms (AAA, Floater-Hormann), which are better conditioned; for polynomial-friendly functions use [Chebyshev interpolation](/chebyshev-interpolation/).

## Pitfalls

- **Unattainable points and nonexistence.** Some data have no interpolant of the chosen type; an implementation that returns $y_i$ at the nodes by fiat hides this. Check for $0/0$.
- **Exact equality tests in floating point.** The rule $\varphi_{k-1}(x_i) = \varphi_{k-1}(x_{k-1}) \Rightarrow \infty$ rarely fires with rounded data; nearly equal values give huge inverse differences and a near-pole in the interpolant. Pivot on the largest denominator, not on the first nonzero one.
- **Spurious poles between nodes.** Always check the interpolant on a fine grid, or compute the zeros of $B$; a small error at the nodes says nothing about the interior.
- **Ordering.** Inverse differences of the same data in different orders can differ by many orders of magnitude; a Leja-like order, or ordering by distance from the evaluation point for extrapolation, is usually more stable.
- **Overflow.** The three-term recurrence values grow like products of $t - x_j$; rescale $A$ and $B$ together, as the implementation does for floats.

## Implementations

## History

Thorvald Nicolai Thiele, the Danish astronomer and actuary, presented interpolation by continued fractions with reciprocal differences in his Interpolationsrechnung (1909), as the rational analogue of Newton's divided difference formula. Milne-Thomson's Calculus of Finite Differences (1933) made reciprocal and inverse differences standard textbook material. Bulirsch and Stoer (1964) used rational interpolation for extrapolation in Richardson-type methods, the basis of the Bulirsch-Stoer integrator. The difficulties of nonexistence and unattainable points were analysed by Werner and by Graves-Morris around 1980, and rational interpolation was revived in the 2010s by barycentric methods such as AAA.

## References
