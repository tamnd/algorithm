---
tag: 8VVH8M
kind: algorithm
slug: secant-method
name: Secant method
aliases:
- secant iteration
- method of secants
area: numerical/root-finding
level: intro
summary: Step to the zero of the line through the last two points. Order (1 + 5^(1/2))/2 ≈ 1.618 near a simple root, with one evaluation of f per step and no derivative.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {δ: the tolerance on the error, M: "max |f''| / (2 min |f'|) near a simple root"}
  time: {local: "O(log log(1/(M δ)))"}
  space: {extra: Θ(1)}
  evaluations: {per_step: "1"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true, local: true}
prereqs: [newton-raphson-method, order-of-convergence, divided-differences]
see_also: [regula-falsi, illinois-method, muller-method, brent-method, inverse-quadratic-interpolation, steffensen-method, broyden-method, multiplicity-of-roots]
sources:
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: Chapter 3, Method of false position (regula falsi), the sections on iteration with successive adjacent points and on Horner units and the efficiency index; Chapter 12, Linear difference equations (asymptotic behaviour of the errors)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 1, Solution of equations by iteration (the secant method and its order)
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 2.6, Methods when derivatives are unavailable
  - book: isbn:9780828403122
    title: J. F. Traub, Iterative Methods for the Solution of Equations, Prentice-Hall, 1964 (reprinted by AMS Chelsea)
    locator: Chapter 6, One-point iteration functions with memory
---

The secant method solves $f(x) = 0$ by drawing the line through the last two points $(x_{k-1}, f(x_{k-1}))$ and $(x_k, f(x_k))$ and taking the zero of that line as the next point. It is [Newton's method](/newton-raphson-method/) with the derivative replaced by a difference quotient. Near a simple root of a $C^2$ function it converges with [order](/order-of-convergence/) $\varphi = (1 + \sqrt 5)/2 \approx 1.618$, and since each step needs only one new value of $f$, its efficiency index $1.618$ is higher than Newton's $2^{1/2} \approx 1.414$. Like Newton's method it is local: far from a root it can diverge.

## In plain words

Take two guesses and compute the function at both. Draw the straight line through the two points on the curve, and follow it to where it crosses the axis. That crossing is the next guess. Drop the oldest guess and repeat with the two newest ones. Near a root the curve is almost straight, so the line is a good stand-in for the curve, and the error falls fast: the number of correct digits grows by about 1.6 times in each step. Each step costs only one new function value, and the method needs no formula for the slope. The two guesses need not lie on both sides of the root, so the method can also run away from it.

## The problem

The input is a function $f$, two distinct starting points $x_0, x_1$, a tolerance (an absolute part $\delta_a \ge 0$ and a relative part $\delta_r \ge 0$, not both zero) and a maximum number of steps $k_{\max}$. The output is a point $\hat x$ and a flag. When $f \in C^2$ near a simple root $x^*$ and $x_0, x_1$ are close enough to $x^*$, the method converges to $x^*$. This is the local form of the [root-finding problem](/root-finding-problem/).

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error, and $f[a, b] = (f(b) - f(a))/(b - a)$ the first [divided difference](/divided-differences/). A method has order $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$; with $w$ evaluations per step its efficiency index is $q^{1/w}$.

## The algorithm

```pseudo id=main
SECANT(f, x0, x1, δa, δr, kmax)
L1  f0 ← f(x0); if f0 = 0 then return (x0, "root")
L2  f1 ← f(x1); if f1 = 0 then return (x1, "root")
L3  for k ← 1 to kmax do
L4      if f1 = f0 or f0, f1 not finite then return (x1, "failure")
L5      s ← −f1 · (x1 − x0) / (f1 − f0)
L6      x2 ← x1 + s
L7      if x2 is not finite then return (x1, "failure")
L8      if |s| ≤ δa + δr · |x2| then return (x2, "converged")
L9      f2 ← f(x2); if f2 = 0 then return (x2, "root")
L10     x0, f0 ← x1, f1; x1, f1 ← x2, f2
L11 return (x1, "kmax reached")
```

Lines L1 and L2 evaluate the two starting points. Line L5 computes the step to the zero of the line through $(x_0, f_0)$ and $(x_1, f_1)$; it is the Newton step $-f_1 / f[x_0, x_1]$ with the divided difference in place of $f'(x_1)$. The form $x_1 + s$ adds a small correction to the newest point, which loses less to rounding than the symmetric form $(x_0 f_1 - x_1 f_0)/(f_1 - f_0)$. Line L4 stops when the line is horizontal ($f_1 = f_0$), when the step is undefined. Line L8 is the relative step test of the [stopping criteria](/stopping-criteria/); it returns $x_2$ without evaluating $f$ there. Line L10 drops the oldest point.

## Example

Solve $\cos x - x = 0$ from $x_0 = 0$, $x_1 = 1$ in binary64, with $\delta_a = 0$ and $\delta_r = 2^{-51}$. The root is $x^* = 0.73908513321516064165\ldots$.

| $k$ | $x_k$ | $f(x_k)$ | step to $x_k$ | $\lvert e_k \rvert$ | $q_k$ |
|---|---|---|---|---|---|
| 0 | 0.0 | $1.000000$ | | $7.391 \cdot 10^{-1}$ | |
| 1 | 1.0 | $-4.596977 \cdot 10^{-1}$ | | $2.609 \cdot 10^{-1}$ | |
| 2 | 0.6850733573260451 | $8.929928 \cdot 10^{-2}$ | $-3.149266 \cdot 10^{-1}$ | $5.401 \cdot 10^{-2}$ | |
| 3 | 0.736298997613654 | $4.660039 \cdot 10^{-3}$ | $5.122564 \cdot 10^{-2}$ | $2.786 \cdot 10^{-3}$ | 1.882 |
| 4 | 0.7391193619116293 | $-5.728599 \cdot 10^{-5}$ | $2.820364 \cdot 10^{-3}$ | $3.423 \cdot 10^{-5}$ | 1.484 |
| 5 | 0.7390851121274639 | $3.529262 \cdot 10^{-8}$ | $-3.424978 \cdot 10^{-5}$ | $2.109 \cdot 10^{-8}$ | 1.680 |
| 6 | 0.7390851332150012 | $2.667866 \cdot 10^{-13}$ | $2.108754 \cdot 10^{-8}$ | $1.594 \cdot 10^{-13}$ | 1.595 |
| 7 | 0.7390851332151607 | $0$ | $1.594077 \cdot 10^{-13}$ | $3.1 \cdot 10^{-17}$ | |

The observed order $q_k = \log(|e_k|/|e_{k-1}|) / \log(|e_{k-1}|/|e_{k-2}|)$ oscillates around $1.618$. The ratios $|e_{k+1}| / (|e_k| |e_{k-1}|)$ are $0.198, 0.227, 0.221, 0.2208$; they tend to $|f''(x^*)/(2 f'(x^*))| = 0.22081$, as the error identity below says. At $x_7$ the computed $f$ is exactly $0$, so line L9 returns after 8 evaluations of $f$. Newton's method on the same problem needed 5 evaluations of $f$ and 4 of $f'$.

## Correctness

All claims are proved in [the correctness proof](proofs/correctness.md).

- **Always.** The loop ends after at most $k_{\max}$ passes, a result with the flag "root" is an exact zero, and a result with the flag "converged" passed the step test.
- **The error identity.** If $f \in C^2$ on an interval that holds $x_{k-1}$, $x_k$ and $x^*$, and $f[x_{k-1}, x_k] \ne 0$, then
$$e_{k+1} = \frac{f[x_{k-1}, x_k, x^*]}{f[x_{k-1}, x_k]}\, e_k\, e_{k-1} = \frac{f''(\xi_k)}{2 f'(\eta_k)}\, e_k\, e_{k-1}$$
for some $\xi_k, \eta_k$ in that interval.
- **Local convergence (proved).** Let $f \in C^2$ on $I = [x^* - r, x^* + r]$, $f' \ne 0$ on $I$, $M = \max_I |f''| / (2 \min_I |f'|)$, and $x_0, x_1 \in I$ with $M |e_0| \le 1/2$ and $M |e_1| \le 1/2$. Then in exact arithmetic $|e_{k+1}| \le M |e_k| |e_{k-1}| \le \tfrac12 |e_k|$, and $x_k \to x^*$.
- **Order $\varphi$ (proved).** If moreover $f''(x^*) \ne 0$ and no $e_k$ is zero, then $|e_{k+1}| / |e_k|^{\varphi} \to C^{1/\varphi}$ with $C = |f''(x^*)/(2 f'(x^*))|$ and $\varphi = (1 + \sqrt 5)/2$, the positive root of $q^2 = q + 1$.

## Complexity

The cost model is the number of evaluations of $f$.

- **Per step.** One new evaluation, plus two to start. So a run that stops at line L8 in pass $k$ costs $k + 1$ evaluations, and one that stops at line L9 in pass $k$ costs $k + 2$.
- **Efficiency.** Order $\varphi$ with $w = 1$ gives the index $\varphi \approx 1.618$. Two secant steps cost as much as one Newton step when $f'$ costs as much as $f$, and they multiply the number of correct digits by $\varphi^2 \approx 2.618 > 2$.
- **Steps to the tolerance.** With $d_k = -\log_2(M |e_k|)$, the bound $|e_{k+1}| \le M |e_k| |e_{k-1}|$ gives $d_{k+1} \ge d_k + d_{k-1}$, a Fibonacci recurrence. From $d_0, d_1 \ge 1$, $d_k \ge F_{k+1} \approx \varphi^{k+1}/\sqrt 5$, so $|e_k| \le \delta$ after $O(\log \log (1/(M \delta)))$ steps.
- **Space.** $\Theta(1)$: two points and two values.

### Floating point

Near the root, $f_1$ and $f_0$ are small and close, and $f_1 - f_0$ has a large relative error. This error goes into the slope, not into the residual $f_1$, so it slows the convergence but does not change the limiting accuracy, which is about $\varepsilon_f / |f'(x^*)|$ as for Newton's method. When both values are at rounding level, $f_1 = f_0$ can occur with $x_1 \ne x_0$, and line L4 then stops; the current $x_1$ is already at the limiting accuracy. Without line L4 the method divides by zero.

## Properties

- **Local.** No bracket is kept; the iterates can leave the region of convergence.
- **Derivative free.** Only values of $f$ are used.
- **With memory.** The step uses two old points. In Traub's terms it is a one-point method with memory. A one-point method without memory that uses only the value of $f$ has order at most 1; reusing the old point lifts the order to $1.618$ (Traub, Chapters 5 and 6).
- **Multiple roots.** At a double root the method is linear with rate $(\sqrt 5 - 1)/2 \approx 0.618$ ([multiplicity of roots](/multiplicity-of-roots/)).
- **Symmetric in the two points.** The secant line does not depend on the order of the two points, but the update of line L5 does in rounding.

## Variants and improvements

- **Keep a bracket.** [Regula falsi](/regula-falsi/) keeps the two points on opposite sides of the root; it is safe but linear. The [Illinois method](/illinois-method/) repairs the slow side.
- **Hybrids.** [Dekker's method](/dekker-method/) and [Brent's method](/brent-method/) take secant steps inside a bracket and bisect when the step is poor.
- **Higher-order interpolation.** [Muller's method](/muller-method/) fits a parabola through three points (order $1.839$, complex roots); [inverse quadratic interpolation](/inverse-quadratic-interpolation/) fits $x$ as a quadratic in $f$.
- **Systems.** [Broyden's method](/broyden-method/) generalizes the secant condition to a Jacobian approximation in $\mathbb{R}^n$.
- **Finite-difference Newton.** Using $(f(x_k + h) - f(x_k))/h$ with a separate $h$ costs two evaluations per step; with $h$ of order $|e_k|$ it keeps order 2, with a fixed $h$ it is linear.

## When to use it

Use the secant method when $f$ is smooth, no derivative is available or it is expensive, and two good starting points are known. Per evaluation it is faster than Newton's method. When a bracket is known and a guarantee is needed, use [Brent's method](/brent-method/), which runs secant and inverse quadratic steps inside the bracket. When the root may be multiple, or $f$ is noisy, prefer [bisection](/bisection-method/).

## Pitfalls

- **Equal values.** If $f(x_0) = f(x_1)$, line L5 divides by zero. Line L4 must test $f_1 = f_0$; a test of $x_1 = x_0$ alone does not catch it. For $f(x) = x^2 - 1$ and the start $x_0 = -0.5$, $x_1 = 0.5$, the secant line is horizontal.
- **The symmetric form.** Writing line L6 as $x_2 \leftarrow (x_0 f_1 - x_1 f_0)/(f_1 - f_0)$ loses accuracy when the iterates are close, by cancellation of two large products. Use $x_1 + s$.
- **No bracket.** For $f(x) = \arctan x$ with $x_0 = 2$, $x_1 = 3$, the iterates are $-5.80$, $-1.15$, $6.15$, $1.61$, $-10.04$, and after 16 steps they reach about $3 \cdot 10^{22}$, where the two values of $\arctan$ are equal and line L4 stops with a failure. Only a bracket or a check that $|f|$ falls prevents this.
- **Testing $|f|$ only.** A residual test in line L8 instead of the step test does not bound the error for a flat $f$ ([stopping criteria](/stopping-criteria/)).
- **An extra evaluation.** Evaluating $f(x_2)$ before the step test of line L8 costs one evaluation that the result does not need.

## Implementations

## History

The rule of false position, which uses the same line through two points, is ancient. The secant method in the modern sense, which always keeps the two newest points, was analysed by Ostrowski, who gave its order $(1 + \sqrt 5)/2$ through linear difference equations and introduced the efficiency index to compare it with Newton's method (Ostrowski, Chapters 3 and 12). Traub (1964) placed it among the one-point methods with memory.

## References
