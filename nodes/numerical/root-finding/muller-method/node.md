---
tag: 1KDQ2S
kind: algorithm
slug: muller-method
name: Muller's method
aliases:
- Müller's method
- method of parabolic interpolation for roots
area: numerical/root-finding
level: advanced
summary: Fit a parabola through the last three points and step to its root nearest the newest point. Order 1.839 with one evaluation per step; finds complex roots from real starts.
solves: [root-finding-problem, polynomial-root-finding]
model: real-ram
complexity:
  vars: {δ: the tolerance on the error, C: "|f'''(x*) / (6 f'(x*))| at a simple root"}
  time: {local: "O(log log(1/(C δ)))"}
  space: {extra: Θ(1)}
  evaluations: {per_step: "1", start: "3"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true, local: true}
history:
  year: 1956
  people: [David E. Muller]
  note: Muller published the method in 1956 for polynomial roots on early automatic computers; Traub placed it in his theory of interpolatory methods in 1964.
prereqs: [secant-method, order-of-convergence, divided-differences]
see_also: [secant-method, inverse-quadratic-interpolation, brent-method, laguerre-method, polynomial-deflation, newton-raphson-method, polynomial-root-finding, multiplicity-of-roots]
sources:
  - paper: "D. E. Muller, A method for solving algebraic equations using an automatic computer, Mathematical Tables and Other Aids to Computation 10(56) (1956) 208-215"
    locator: the parabolic interpolation step and the choice of the root of smaller modulus
  - book: "J. F. Traub, Iterative Methods for the Solution of Equations, Prentice-Hall, 1964"
    locator: Chapter 3, Interpolatory iteration functions (the error relation and the order of methods using three points)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 2.4, Muller's method
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: Chapter 3, the efficiency index
  - book: isbn:9780521880688
    title: W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 9.5, Roots of polynomials (Muller's method for complex roots)
---

Muller's method solves $f(x) = 0$ from three starting points. At each step it fits the parabola through the last three points $(x_{k-2}, f_{k-2})$, $(x_{k-1}, f_{k-1})$, $(x_k, f_k)$, takes as the next point the root of that parabola nearest to $x_k$, and drops the oldest point. It is the [secant method](/secant-method/) with a parabola in place of a line. Near a simple root it converges with order $1.839$, using one evaluation per step, and because the root of a parabola is found with a square root that may be complex, it moves from real starting points to complex roots by itself. It needs no derivatives, which made it a standard method for the complex roots of polynomials.

## In plain words

The secant method draws a straight line through the last two points on the curve and follows it to the axis. Muller's method draws the bent curve, a parabola, through the last three points, and follows it to the axis instead. A parabola hugs the curve better than a line, so the new guess is closer: about 1.84 times as many correct digits as the previous guess. A parabola can miss the axis entirely, but then its crossing points are complex numbers, and the method simply carries on with complex guesses. That is how it finds complex roots starting from ordinary numbers. Each step costs one new value of the function.

## The problem

The input is a function $f$, which must accept complex arguments if complex iterates can arise, three distinct starting points $x_0, x_1, x_2$, a tolerance with absolute part $\delta_a \ge 0$ and relative part $\delta_r \ge 0$, and a maximum number of steps $k_{\max}$. The output is a point $\hat x$ and a flag. There is no guarantee of convergence from arbitrary starts.

Notation on the root-finding pages: $x^*$ is a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error. A method has order $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, and with $w$ evaluations per step its efficiency index is $q^{1/w}$. Divided differences are $f[a, b] = (f(b) - f(a))/(b - a)$ and $f[a, b, c] = (f[b, c] - f[a, b])/(c - a)$.

## The algorithm

```pseudo id=main
MULLER(f, x0, x1, x2, δa, δr, kmax)
L1  f0, f1, f2 ← f(x0), f(x1), f(x2); if one is 0 then return that point as "root"
L2  for k ← 1 to kmax do
L3      h1 ← x1 − x0;  h2 ← x2 − x1;  if h1 = 0 or h2 = 0 or h1 + h2 = 0 then return (x2, "failure")
L4      d1 ← (f1 − f0)/h1;  d2 ← (f2 − f1)/h2;  d ← (d2 − d1)/(h1 + h2)
L5      b ← d2 + h2 · d
L6      s ← sqrt(b² − 4 f2 d)                 ▷ complex if the argument is negative or complex
L7      E ← b + s if |b + s| ≥ |b − s| else b − s
L8      if E = 0 then return (x2, "failure")
L9      h ← −2 f2 / E;  x3 ← x2 + h
L10     f3 ← f(x3); if f3 = 0 then return (x3, "root")
L11     if |h| ≤ δa + δr |x3| then return (x3, "converged")
L12     (x0, x1, x2) ← (x1, x2, x3);  (f0, f1, f2) ← (f1, f2, f3)
L13 return (x2, "kmax reached")
```

Line L4 computes the divided differences $d_1 = f[x_0, x_1]$, $d_2 = f[x_1, x_2]$ and $d = f[x_0, x_1, x_2]$. In Newton form around $x_2$ the interpolating parabola is
$$P(x) = f_2 + b(x - x_2) + d(x - x_2)^2, \qquad b = f[x_1, x_2] + (x_2 - x_1) f[x_0, x_1, x_2],$$
which is line L5. Its roots are $x_2 + h$ with $h = -2f_2/(b \pm \sqrt{b^2 - 4f_2 d})$, the form of the quadratic formula that avoids cancellation (see [quadratic formula](/quadratic-formula/)). Line L7 chooses the sign that gives the larger denominator, that is the root nearer to $x_2$. If $d = 0$ the parabola is a line and the step is the secant step $-f_2/b$. Line L8 fails when $b = 0$ and $f_2 d = 0$, so the parabola has no usable root. Line L11 is the step test; line L2 bounds the work. The implementation also returns "failure" on NaN or infinity, and keeps the iterates real while the square roots are real.

## Example

Solve $f(x) = x^3 - x - 2 = 0$ from $x_0, x_1, x_2 = 0, 1, 2$. The real root is $x^* = 1.5213797068045676$, with $f'(x^*) = 3x^{*2} - 1 = 5.94377$ and $f''' = 6$, so the predicted constant in $|e_{k+1}| \approx C|e_k e_{k-1} e_{k-2}|$ is $C = |f'''/(6f')| = 1/(3x^{*2} - 1) = 0.168243$. In 300-digit decimal arithmetic:

| $k$ | $\lvert e_k \rvert$ | $\lvert e_k \rvert / \lvert e_{k-1} e_{k-2} e_{k-3} \rvert$ |
|---|---|---|
| 0, 1, 2 | $1.521$, $0.5214$, $0.4786$ | |
| 3 | $6.395260 \cdot 10^{-2}$ | $0.168452$ |
| 4 | $2.582732 \cdot 10^{-3}$ | $0.161836$ |
| 5 | $1.323005 \cdot 10^{-5}$ | $0.167353$ |
| 6 | $3.676611 \cdot 10^{-10}$ | $0.168248$ |
| 7 | $2.113611 \cdot 10^{-18}$ | $0.168243$ |
| 8 | $1.729700 \cdot 10^{-33}$ | $0.168243$ |

The exponents of the errors, about $10$, $18$, $33$, $61$, $112$ at $k = 6$ to $10$, grow by a factor approaching $1.839$. In binary64 the program makes 5 passes and 8 evaluations of $f$ (3 to start, 1 per pass), and in the fifth pass the computed $f(x_3)$ is exactly $0$ at $x_3 = 1.5213797068045676$.

For $f(x) = x^2 + 1$ from $0, 1, 2$ the parabola is $f$ itself, $b^2 - 4f_2 d = 16 - 20 = -4$, and the first step lands exactly on $i$: 4 evaluations in all. For $x^3 + 1$ from $0, 0.5, 1$ the iterates become complex in the first step and converge to $e^{i\pi/3} = 0.5 + 0.8660254037844387i$ in 8 passes.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **Always.** The loop ends after at most $k_{\max}$ passes and $k_{\max} + 3$ evaluations. A result flagged "root" is an exact zero of the computed $f$, and one flagged "converged" passed the step test.
- **Error relation (proved).** If $f$ is analytic near the iterates and $x_3$ is the new point, then
$$f'(\xi)\,e_3 = f[x_0, x_1, x_2, x_3]\,(x_3 - x_0)(x_3 - x_1)(x_3 - x_2)$$
for a mean value $f'(\xi)$ along the segment from $x^*$ to $x_3$, in the integral sense. So once the iterates are close, $e_{k+1} \approx -\frac{f'''(x^*)}{6f'(x^*)} e_k e_{k-1} e_{k-2}$.
- **Local convergence (proved).** If $f$ is analytic in a disc around a simple root $x^*$, there is a radius $\rho > 0$ such that from any three distinct starts within $\rho$ of $x^*$ the iterates stay in the disc and converge to $x^*$, with $|e_{k+1}| \le K|e_k||e_{k-1}||e_{k-2}|$.
- **Order (proved from the relation).** If $f'''(x^*) \ne 0$, the error relation gives order $q = 1.839286755\ldots$, the real root of $q^3 = q^2 + q + 1$, by the same argument as for the secant method.
- **Global (none).** From poor starts the method can wander or converge to an unexpected root; there is no bracket.

## Complexity

The cost model is the number of evaluations of $f$.

- **Per step.** One evaluation and a complex square root. With $w = 1$ and $q = 1.839$ the efficiency index is $1.839$, above the secant method's $1.618$ and Newton's $2^{1/2} \approx 1.414$.
- **Steps to the tolerance.** In the local regime, $\log(1/|e_k|)$ grows like $1.839^k$, so $O(\log \log (1/(C\delta)))$ steps reach the tolerance $\delta$.
- **Total evaluations.** A run that ends in pass $k$ at line L10 or L11 makes $k + 3$ evaluations.
- **Space.** $\Theta(1)$.

### Floating point

The method needs only values of $f$, so its limiting accuracy is that of any method based on $f$: about $\varepsilon_f/|f'(x^*)|$ where $\varepsilon_f$ bounds the error in the computed $f$ near the root, plus $u|x^*|$. Close to the root the divided differences are formed from nearly equal values and lose accuracy, but the step $h = -2f_2/E$ is still small and correct to first order, because $f_2$ is small and $E \approx f'(x^*)$ needs only a few correct digits; this is the same self-correcting behaviour as in the secant method. Near the limiting accuracy the iterates can jitter or coincide, so the step test may not pass; then line L3 fails on equal points or line L2 ends the loop.

## Properties

- **Derivative-free and superlinear.** Order $1.839$ from values alone, with one evaluation per step.
- **Complex from real.** For real $f$ and real starts, iterates stay real only while $b^2 - 4f_2 d \ge 0$; otherwise they become complex.
- **Exact for quadratics.** If $f$ is a polynomial of degree at most 2, one step lands on a root.
- **Local.** No bracket and no global guarantee.
- **Interpolatory.** It belongs to Traub's family of methods that interpolate $f$ at the last $r$ points; with $r$ points of polynomial interpolation the order tends to $2$ as $r$ grows.

## Variants and improvements

- **Inverse quadratic interpolation.** Interpolate $x$ as a function of $y$ instead, which needs no square root and stays real ([inverse quadratic interpolation](/inverse-quadratic-interpolation/)); it is the fast step of [Brent's method](/brent-method/).
- **Bracketed Muller.** Keep a sign-change bracket and fall back to bisection, as Brent's method does with inverse interpolation, when only real roots are wanted.
- **Polynomials with deflation.** Find a root, divide it out ([polynomial deflation](/polynomial-deflation/)), restart, and polish each root on the original polynomial; this was Muller's own use.
- **Real-only version.** Replace a negative discriminant by $0$, which steps to the vertex of the parabola and keeps the iterates real.

## When to use it

Use Muller's method when derivatives are not available and complex roots are wanted, as for polynomials or for analytic functions such as characteristic determinants. For real roots with a known sign change, prefer a bracketing hybrid such as [Brent's method](/brent-method/); for polynomials with all roots wanted, prefer [Laguerre's method](/laguerre-method/) or a simultaneous method.

## Pitfalls

- **Complex arithmetic.** The function must accept complex arguments, even when started at real points.
- **Multiple roots.** At a root of multiplicity $m > 1$ the convergence is linear; the double root of $(x - 1)^2(x + 3)$ is found only to about $\sqrt u$.
- **Coinciding points.** Two equal points make the divided differences undefined; line L3 fails then, which also happens when rounding makes iterates repeat.
- **Constant or flat $f$.** If $b = 0$ and $f_2 d = 0$ there is no step; a constant $f$ fails at once.
- **Unexpected root.** The method may converge to a root other than the one near the starts, as all open methods can.

## Implementations

## History

David E. Muller published the method in 1956, for finding all roots of polynomials, real and complex, on the ILLIAC at the University of Illinois. J. F. Traub analysed it in 1964 as a member of the family of interpolatory iteration functions, together with the secant method and its higher-order generalizations.

## References
