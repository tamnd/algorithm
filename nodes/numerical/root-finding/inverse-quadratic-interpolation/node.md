---
tag: 6ZVEEE
kind: algorithm
slug: inverse-quadratic-interpolation
name: Inverse quadratic interpolation
aliases:
- IQI
- inverse parabolic interpolation
area: numerical/root-finding
level: advanced
summary: Fit a quadratic in x as a function of y through the last three points and evaluate it at y = 0. One evaluation in each step and order 1.839 at a simple root, but no bracket.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {δ: "the tolerance on the step", K: "the cap on the number of steps"}
  time: {worst: "Θ(K)", average: "O(log log(1/δ))"}
  space: {extra: Θ(1)}
  evaluations: {worst: "K + 3", step: "1"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true}
prereqs: [secant-method, lagrange-interpolation, order-of-convergence]
see_also: [brent-method, dekker-method, chandrupatla-method, muller-method, secant-method, divided-differences, neville-algorithm, illinois-method]
sources:
  - book: isbn:9780486419985
    title: Richard P. Brent, Algorithms for Minimization without Derivatives, Prentice-Hall, 1973 (Dover reprint, 2002)
    locator: Chapter 3, The Use of Successive Interpolation for Finding Simple Zeros of a Function and its Derivatives (the order 1.839 of inverse quadratic interpolation) and Chapter 4 (its use with bisection)
  - book: "J. F. Traub, Iterative Methods for the Solution of Equations, Prentice-Hall, 1964 (reprinted by Chelsea, 1982)"
    locator: Chapter 3, difference relations for the error, and Chapter 4, interpolatory iteration functions (inverse interpolation with memory and its order)
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: the chapters on the regula falsi and on interpolation with several points (the error equation and the order of methods with memory)
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 9.3, Van Wijngaarden-Dekker-Brent Method (the inverse quadratic interpolation formula in the form that Brent's method uses)
---

Inverse quadratic interpolation (IQI) is an iteration for a root of $f$ that uses the last three points. It fits $x$ as a quadratic function of $y$ through the points $(f(x_{k-2}), x_{k-2})$, $(f(x_{k-1}), x_{k-1})$, $(f(x_k), x_k)$ and takes its value at $y = 0$ as $x_{k+1}$. Fitting $x$ in terms of $y$, not $y$ in terms of $x$ as in [Müller's method](/muller-method/), avoids the square root and the choice between two roots of a parabola. Each step costs one new evaluation, and near a simple root the order is $1.839$, the real root of $q^3 = q^2 + q + 1$. On its own it has no bracket and can fail far from the root, so [Brent's method](/brent-method/) and [Chandrupatla's method](/chandrupatla-method/) use it inside a bracket with a fallback to bisection.

## In plain words

Suppose you have tried three guesses and know the value of the function at each. Turn the picture on its side: treat the function values as the inputs and the guesses as the outputs. Draw the simplest curve, a parabola, through these three points. Now ask the parabola which guess goes with the value zero. That answer is the next guess. Drop the oldest guess and repeat. Close to a root the guesses improve very fast, and the method needs no slopes. Far from a root the parabola can send the next guess far away, so on its own it is not safe.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Given $f$ and three starting points $x_0, x_1, x_2$ near a simple root $x^*$, with distinct values $f_i = f(x_i)$, find $x^*$ to a tolerance $\delta$. The method uses only values of $f$. Since there is no bracket, the stopping test on the step is a heuristic, not a bound; see [stopping criteria](/stopping-criteria/).

## The algorithm

The [Lagrange interpolation](/lagrange-interpolation/) polynomial of $x$ in $y$ through the three points, evaluated at $y = 0$, is

$$x_3 = \frac{f_1 f_2}{(f_0 - f_1)(f_0 - f_2)} x_0 + \frac{f_0 f_2}{(f_1 - f_0)(f_1 - f_2)} x_1 + \frac{f_0 f_1}{(f_2 - f_0)(f_2 - f_1)} x_2.$$

The code uses the equal Newton form with [divided differences](/divided-differences/) of $x$ in $y$, which writes $x_3$ as $x_2$ plus a small correction:

$$x[f_2, f_1] = \frac{x_2 - x_1}{f_2 - f_1}, \qquad x[f_2, f_1, f_0] = \frac{x[f_1, f_0] - x[f_2, f_1]}{f_0 - f_2}, \qquad x_3 = x_2 - f_2\, x[f_2, f_1] + f_1 f_2\, x[f_2, f_1, f_0].$$

```pseudo id=main
IQI(f, x0, x1, x2, delta, kmax):
L1   f0 <- f(x0);  f1 <- f(x1);  f2 <- f(x2)
L2   for k = 1, 2, ..., kmax:
L3       if two of f0, f1, f2 are equal then return FAIL
L4       x3 <- x2 - f2 x[f2,f1] + f1 f2 x[f2,f1,f0]
L5       f3 <- f(x3)
L6       if f3 = 0 or |x3 - x2| <= delta then return x3
L7       (x0, f0, x1, f1, x2, f2) <- (x1, f1, x2, f2, x3, f3)
     return FAIL                                  // kmax reached
```

Line L1 evaluates $f$ at the three starting points (a starting point with $f = 0$ is returned at once). Line L3 stops when the interpolation is not defined, since two equal values of $y$ do not determine $x$ as a function of $y$. Line L4 is the step. Its first two terms are the [secant](/secant-method/) step from $x_1, x_2$, and the third term is the quadratic correction. Line L6 stops on an exact zero or on a short step. Line L7 drops the oldest point.

## Example

Take $f(x) = x^3 - x - 2$ with $x_0 = 1$, $x_1 = 1.5$, $x_2 = 2$; the root is $x^* = 1.5213797068$. The table is computed with 120 decimal digits, so the errors below $10^{-16}$ are true errors, not rounding. The ratio column is $|e_k|/(|e_{k-1}||e_{k-2}||e_{k-3}|)$, and the last column is $\log|e_k| / \log|e_{k-1}|$.

| $k$ | $x_k$ | $\lvert e_k \rvert$ | ratio | log ratio |
|---|---|---|---|---|
| 3 | 1.5272727273 | $5.893 \times 10^{-3}$ | 1.10456 | |
| 4 | 1.5213365402 | $4.317 \times 10^{-5}$ | 0.71584 | 1.958 |
| 5 | 1.5213796210 | $8.580 \times 10^{-8}$ | 0.70475 | 1.619 |
| 6 | 1.5213797068 | $2.196 \times 10^{-14}$ | 1.00614 | 1.933 |
| 7 | 1.5213797068 | $8.224 \times 10^{-26}$ | 1.01108 | 1.837 |
| 8 | 1.5213797068 | $1.567 \times 10^{-46}$ | 1.01105 | 1.826 |
| 9 | 1.5213797068 | $2.861 \times 10^{-85}$ | 1.01105 | 1.846 |

The ratio tends to the constant $C = (3f''(x^*)^2 - f'(x^*)f'''(x^*))/(6f'(x^*)^2) = 1.01105$ of the error equation below, and the log ratio swings around $1.839$. In binary64 the method stops after 5 steps, 8 evaluations in all, with $|e| < 10^{-15}$. For $\cos x - x$ from $0, 0.5, 1$ the errors are $1.09 \times 10^{-2}$, $1.11 \times 10^{-4}$, $4.62 \times 10^{-8}$, $9.21 \times 10^{-15}$.

## Correctness

At a simple root of a $C^3$ function, the error satisfies $e_{k+1} = C_k\, e_k e_{k-1} e_{k-2}$ with $C_k \to C$, by the interpolation error formula applied to the inverse function $f^{-1}$. If the starting points are close enough to $x^*$, the errors shrink at each step, and the order is the real root $q = 1.839$ of $q^3 = q^2 + q + 1$. These results are local. The loop runs at most $k_{\max}$ times, so the method always ends. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs one evaluation of $f$ (line L5) and about 10 arithmetic operations; the start costs three evaluations, and the space is $\Theta(1)$. Near a simple root the order in each evaluation is $q = 1.839$, so the efficiency index is $1.839$, higher than the [secant method](/secant-method/) ($1.618$) and [Newton's method](/newton-raphson-method/) ($\sqrt 2 = 1.414$). The number of correct digits grows by a factor of about 1.84 in each step, so reaching a tolerance $\delta$ from a good start takes $O(\log\log(1/\delta))$ steps. Using more points does not help much: inverse interpolation through all previous points has order tending to 2 (Traub 1964, Chapter 4).

## Properties

- **Derivative free.** It needs only values of $f$.
- **Not bracketing.** The new point can lie anywhere, and the method can diverge.
- **Exact on inverse quadratics.** If $f^{-1}$ is a quadratic near 0, one step gives the root exactly.
- **Local order 1.839 at a simple root.** At a root of [multiplicity](/multiplicity-of-roots/) $m > 1$, $f^{-1}$ is not smooth at 0 and the convergence is only linear.
- **Two points coincide in $y$.** The step is not defined when two values of $f$ are equal.

## Variants and improvements

- **Brent's form.** [Brent's method](/brent-method/) writes the step with ratios $s = f_2/f_0$, $t = f_1/f_0$, $r = f_2/f_1$ as $x_2 + P/Q$, and accepts it only if it lies well inside the bracket and shrinks fast enough; otherwise it bisects.
- **Chandrupatla's test.** [Chandrupatla's method](/chandrupatla-method/) accepts the IQI step only when the three points satisfy a simple condition on two ratios, which keeps the interpolant well behaved inside the bracket.
- **Secant fallback.** When two of the three values are close, falling back to the secant step through the two newest points avoids the division by a small number.
- **Direct quadratic interpolation.** [Müller's method](/muller-method/) fits $y$ as a quadratic in $x$ and solves for $x$; it has the same order 1.839 and can find complex roots from real starting points.
- **Higher degree.** Inverse cubic interpolation through four points has order 1.928; [Neville's algorithm](/neville-algorithm/) evaluates such interpolants at $y = 0$ without forming them.

## When to use it

Use it as the fast step inside a safeguarded bracketing method, as in Brent's and Chandrupatla's methods, when $f$ is smooth and costly and no derivative is available. Use it alone only when good starting points are known, for example to refine a root that a bracketing method has already isolated.

## Pitfalls

- **Equal function values (L3).** For $f(x) = x^2 - 1$ with starting points $-2$, $2$, $0.5$, the values at $-2$ and $2$ are equal, and the formula divides by zero. Line L3 must test for this, and nearly equal values give huge steps.
- **Divergence from far away (L4).** For $\arctan x$ from $2, 3, 4$ the iterates are $32$, $659.3$, $1.76 \times 10^5$, $8.96 \times 10^9$: the function is flat, the inverse quadratic is a poor model, and nothing pulls the iterates back. A bracket with a bisection fallback prevents this.
- **The step test is not an error bound (L6).** A short step $|x_3 - x_2| \le \delta$ suggests convergence only when the method converges superlinearly. Near a multiple root or during divergence the step can be short while the error is large.
- **Multiple roots.** For $(x - 1)^2(x + 2)$ from $0, 0.5, 0.8$ the errors after 6 and 12 steps are $7.6 \times 10^{-3}$ and $2.8 \times 10^{-4}$: linear convergence, no better than bisection.
- **Lagrange form with nearly equal values.** The three denominators of the Lagrange form are large and of mixed sign when the $f_i$ are close; the Newton form of L4 adds a small correction to $x_2$ and loses less to cancellation.

## Implementations

## History

Inverse interpolation is old: it is the natural way to use a table of a function to find where it takes a given value. As an iteration with memory, its order was found in the analysis of interpolatory methods by Ostrowski and by Traub (1964), whose difference equations give the order 1.839 of three-point inverse interpolation. Brent (1971, 1973) made it the main step of his zero finder, with bisection as a safeguard, and Numerical Recipes popularized that combination. Chandrupatla (1997) gave a different test for when to accept the step.

## References
