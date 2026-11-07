---
tag: K3E565
kind: concept
slug: stopping-criteria
name: Stopping criteria
aliases:
- termination criteria
- convergence tests
- stopping rules
area: numerical/root-finding
level: intro
summary: Tests on the step, the residual, the bracket width and the iteration count that decide when a root-finding iteration ends, and what each test proves about the error.
prereqs: [root-finding-problem, order-of-convergence, machine-epsilon]
see_also: [bisection-method, newton-raphson-method, brent-method, root-conditioning, quadratic-convergence, fixed-point-iteration, newton-method-for-systems, floating-point-arithmetic]
sources:
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 7.2, Stopping criteria
  - book: isbn:9780898713527
    title: C. T. Kelley, Iterative Methods for Linear and Nonlinear Equations, SIAM Frontiers in Applied Mathematics 16, 1995
    locator: Chapter 5, Newton's method (the termination of the iteration, by the relative and absolute residual test)
  - book: isbn:9780486419985
    title: Richard P. Brent, Algorithms for Minimization without Derivatives, Prentice-Hall, 1973 (reprinted by Dover, 2002)
    locator: Chapter 4, An algorithm with guaranteed convergence for finding a zero of a function (the tolerance 2 eps |b| + t)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 25, Nonlinear systems and Newton's method (the limiting accuracy and residual of Newton's method)
---

A stopping criterion is the test that ends an iterative method for the [root-finding problem](/root-finding-problem/). It decides whether the current point is close enough to a root, whether the method has stopped making progress, or whether it has run out of its budget of steps. A good rule is cheap, says something true about the error $|x_k - x^*|$, and always ends the loop, also in floating point, where the error cannot fall below a limiting accuracy.

## In plain words

An iterative method makes a sequence of guesses that should come closer to the root. The program must decide when to stop. It can stop when two guesses in a row are very close, when the function value at the guess is very small, or when an interval that is known to hold the root is short enough. Each test can be wrong: the guesses can creep forward slowly while still far from the root, and a function can be tiny at a point far from its root when the curve is flat. On a computer the guesses cannot get closer than the spacing of the numbers, so a test that asks for more never passes. So each loop also needs a limit on the number of steps.

## The idea

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error, $s_k = x_{k+1} - x_k$ the step, $[a, b]$ a bracket with $f(a) f(b) < 0$, $\delta$ the tolerance and $u$ the [unit roundoff](/machine-epsilon/) ($u = 2^{-53}$ in binary64).

### The tests

1. **Bracket width.** Stop when $b - a \le 2\delta$ and return the midpoint. If $f$ is continuous, the midpoint is within $\delta$ of a root. This is the only test of this list that proves an error bound with no further knowledge of $f$. [Bisection](/bisection-method/) and [Brent's method](/brent-method/) use it.
2. **Step.** Stop when $|s_k| \le \delta_a + \delta_r |x_{k+1}|$, with an absolute part $\delta_a$ and a relative part $\delta_r$. The relative part makes the test independent of the scale of $x$; the absolute part handles a root at or near $0$.
3. **Residual.** Stop when $|f(x_k)| \le \varepsilon$. For systems, Kelley (Chapter 5) uses $\|F(x_k)\| \le \tau_r \|F(x_0)\| + \tau_a$.
4. **Budget.** Stop with a failure flag after $k_{\max}$ steps or evaluations.
5. **Stagnation and failure.** Stop when $|s_{k+1}| \ge |s_k|$ after the steps have become small, when $x_{k+1} = x_k$, when a derivative is $0$, or when a value is NaN or infinite.

### What each test proves

- **Step test, superlinear method.** If $x_k \to x^*$ superlinearly, then $|s_k| / |e_k| \to 1$, because $s_k = e_{k+1} - e_k$ and $|e_{k+1}|/|e_k| \to 0$. So near the root the step is a good estimate of the error of $x_k$, and $x_{k+1}$ is far better. This is only asymptotic: it says nothing in the early steps.
- **Step test, linear method.** Let $x_{k+1} = g(x_k)$ with $|g(x) - g(y)| \le C |x - y|$, $C < 1$, on an interval that holds the iterates and $x^*$. Then $|e_{k+1}| = |g(x_k) - g(x^*)| \le C |e_k| \le C (|s_k| + |e_{k+1}|)$, so
$$|e_{k+1}| \le \frac{C}{1 - C}\, |s_k|.$$
When $C$ is close to 1 the error is much larger than the step. For Newton's method at a double root $C = 1/2$, and the bound is $|e_{k+1}| \le |s_k|$.
- **Residual test.** By the mean value theorem, $f(x_k) = f(x_k) - f(x^*) = f'(\xi)\, e_k$ for some $\xi$ between $x_k$ and $x^*$. So $|e_k| \le |f(x_k)| / \min |f'|$ over that interval. Without a lower bound on $|f'|$, a small residual proves nothing about the error, and with a large $|f'|$ the residual test is too strict. The residual test does say that $x_k$ is an exact root of the nearby function $f - f(x_k)$, a backward error statement ([root conditioning](/root-conditioning/)).

### Floating point

- **Limiting accuracy.** The iterates are floating-point numbers, so $|e_k|$ cannot fall below about $u |x^*|$. If the computed $f$ has error at most $\varepsilon_f$ near a simple root, then its sign is reliable only outside an interval of radius about $\varepsilon_f / |f'(x^*)|$, and no method that uses computed values can do better. A tolerance $\delta$ below these limits never passes, so the loop runs to $k_{\max}$.
- **Pick $\delta$ with a relative floor.** Brent's zero finder (Brent, Chapter 4) uses the tolerance $2u|b| + t$, where $b$ is the current best point and $t > 0$ is the user's absolute tolerance. The first term keeps the test attainable for large roots, the second for a root at $0$.
- **Do not test for equality.** Near the end, a method can cycle between two adjacent numbers, so $x_{k+1} = x_k$ never holds (see Examples).
- **Test NaN.** A comparison with NaN is false, so a loop `while abs(s) > tol` ends at once when $s$ is NaN, as if it had converged. Check for NaN explicitly, or write the test so that NaN leads to the failure exit.

### A rule that always ends

A robust loop combines the tests: stop with success when the bracket test or the step test (with a relative floor) passes and the residual is not large; stop with failure when $k_{\max}$ is reached, a value is NaN or infinite, or a derivative is zero. Report which test ended the loop. Dennis and Schnabel (Section 7.2) give scaled forms of the step and residual tests for systems, with a failure exit for too many steps and for a step that stays at its maximum length.

## Examples

**A cycle that defeats an equality test.** Newton's method for $x^2 - 2$ from $x_0 = 1$ in binary64 reaches $x_5 = 1.4142135623730951$, the rounded $\sqrt 2$, and then alternates between $1.414213562373095$ and $1.4142135623730951$ forever, with residuals $\mp 4.44 \cdot 10^{-16}$. The test $x_{k+1} = x_k$ never passes, and nor does an absolute step test with $\delta_a = 10^{-17}$. The relative test $|s_k| \le 4u |x_{k+1}|$ stops after 6 steps.

**A small step far from the root.** The linear iteration $x_{k+1} = 1 + 0.999 (x_k - 1)$ from $x_0 = 2$ converges to $1$ with rate $C = 0.999$. The step test $|s_k| \le 10^{-9}$ first passes at step 13810, where the step is $9.996 \cdot 10^{-10}$ but the error is $9.986 \cdot 10^{-7}$, close to the bound $C/(1 - C) \cdot |s_k| = 999 |s_k|$.

**A small residual far from the root.** For the nearly flat $f(x) = (x - 1)^5$, the point $x = 1.01$ has residual $f(1.01) = 1.0 \cdot 10^{-10}$, so a residual test with $\varepsilon = 10^{-8}$ accepts it, but its error is $10^{-2}$.

**A large residual at the root.** For $f(x) = 10^{10}(x - 1)$, the floating-point neighbour $1 + 2.2 \cdot 10^{-16}$ of the root has residual about $2.2 \cdot 10^{-6}$. A residual test with $\varepsilon = 10^{-8}$ rejects every floating-point number except $1$ itself, which works here only because the root is exactly representable.

**A certified stop.** Bisection on $x^3 - x - 2$ over $[1, 2]$ with $\delta = 10^{-6}$ stops after 19 halvings with a bracket of width $2^{-19} < 2 \cdot 10^{-6}$; its midpoint is within $10^{-6}$ of the root $1.5213797068\ldots$ whatever the shape of $f$.

## Where it is used

- [Bisection method](/bisection-method/): the bracket test, with a stop when the midpoint equals an end.
- [Brent's method](/brent-method/): the bracket test with the tolerance $2u|b| + t$. [Dekker's method](/dekker-method/) and [Ridders' method](/ridders-method/) also stop on the bracket width.
- [Newton's method](/newton-raphson-method/), the [secant method](/secant-method/) and [Steffensen's method](/steffensen-method/): the relative step test with a budget, and a check for a zero derivative or difference.
- [Fixed-point iteration](/fixed-point-iteration/): the step test with the factor $C/(1 - C)$ when $C$ is known.
- [Newton's method for systems](/newton-method-for-systems/): scaled step and residual tests in norms.
- [Polynomial root finding](/polynomial-root-finding/): a residual test against the rounding error bound of [Horner's rule](/horner-rule/), which stops when the value is at the level of its own error.

## References
