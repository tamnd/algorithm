---
tag: 4V4H83
kind: algorithm
slug: halley-method
name: Halley's method
aliases:
- Halley's irrational formula
- Halley's rational method
- Halley iteration
area: numerical/root-finding
level: advanced
summary: Iteration x <- x - 2 f f'/(2 f'^2 - f f'') using f, f' and f''. Order 3 at a simple root, linear with rate (m-1)/(m+1) at a root of multiplicity m.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {δ: "the tolerance on the step", K: "the cap on the number of steps", e0: "the starting error"}
  time: {worst: "Θ(K)", average: "O(log log(1/δ))"}
  space: {extra: Θ(1)}
  evaluations: {worst: "3K", step: "3"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: false, efficiency_index: "3^(1/3)"}
prereqs: [newton-raphson-method, order-of-convergence]
see_also: [householder-methods, laguerre-method, quadratic-convergence, multiplicity-of-roots, steffensen-method, stopping-criteria, newton-fractal, secant-method]
sources:
  - paper: "Edmond Halley, Methodus nova accurata & facilis inveniendi radices aequationum quarumcumque generaliter, sine praevia reductione, Philosophical Transactions of the Royal Society of London 18, 136-148, 1694"
    locator: the rational and irrational formulas for correcting an approximate root of a polynomial equation
  - book: "J. F. Traub, Iterative Methods for the Solution of Equations, Prentice-Hall, 1964 (Chelsea reprint, 1982)"
    locator: the chapter on one-point iteration functions (the Halley iteration function, its order 3 and its error constant)
  - paper: "T. R. Scavo and J. B. Thoo, On the geometry of Halley's method, The American Mathematical Monthly 102(5), 417-426, 1995"
    locator: Halley's method as Newton's method on f divided by the square root of f', and its tangent hyperbola interpretation
  - paper: "Walter Gander, On Halley's iteration method, The American Mathematical Monthly 92(2), 131-134, 1985"
    locator: the family of third order methods containing Halley's, Chebyshev's and the super-Halley method
  - book: isbn:9780898713640
    title: J. E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics, 1996
    locator: Chapter 2, Nonlinear Problems in One Variable (Newton's method, its local convergence and stopping tests)
---

Halley's method solves $f(x) = 0$ with the step
$$x_{k+1} = x_k - \frac{2f(x_k)f'(x_k)}{2f'(x_k)^2 - f(x_k)f''(x_k)} .$$
It uses the first and second derivatives, and near a simple root it has order 3: the number of correct digits roughly triples each step. It is [Newton's method](/newton-raphson-method/) applied to $f/\sqrt{|f'|}$, and the case $d = 2$ of [Householder's methods](/householder-methods/). Each step costs three evaluations ($f$, $f'$, $f''$), so its efficiency index $3^{1/3} \approx 1.442$ is only a little above Newton's $2^{1/2} \approx 1.414$; it pays off when $f''$ is cheap given $f$ and $f'$, as for polynomials and many special functions. Like Newton it is local: far from a root, or at a root of multiplicity $m$, it can wander or slow to a linear rate $(m - 1)/(m + 1)$.

## In plain words

Newton's method replaces the curve by its tangent line and jumps to where the line crosses zero. Halley's method replaces the curve by a curve that also matches its bending, and jumps to where that curve crosses zero. Matching one more property of the curve buys one more order: near the root each step roughly triples the number of correct digits, where Newton doubles them. The price is that you must also compute the second derivative. Started far from a root, it has no guarantee, just like Newton.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Input: $f$, $f'$, $f''$ as functions, a start $x_0$, a tolerance $\delta$ and a cap $K$ on the steps. Output: a point and a status. Here an evaluation means one value of each of $f$, $f'$, $f''$ at the same point, so $w = 3$ when each counts as one. The [stopping rule](/stopping-criteria/) is on the step: stop when $|x_{k+1} - x_k| \le \delta(1 + |x_{k+1}|)$, or when $f(x_k) = 0$ exactly, or after $K$ steps. Near a simple root the step is an excellent error estimate, since $e_k = (x_k - x_{k+1}) + e_{k+1}$ and $e_{k+1} = O(e_k^3)$; far from a root a small step proves nothing, and the status says only which test fired.

## The algorithm

```pseudo id=main
HALLEY(f, f', f'', x0, delta, K):
L1   for k = 1, 2, ..., K:
L2       evaluate f(x), f'(x), f''(x);  fail if any is not finite
L3       if f(x) = 0 then return x, "exact"
L4       D <- 2 f'(x)^2 - f(x) f''(x);  if D = 0 then return x, "zero-denominator"
L5       s <- 2 f(x) f'(x) / D;  if s = 0 then return x, "stalled"
L6       x <- x - s
L7       if |s| <= delta (1 + |x|) then return x, "converged"
L8   return x, "max-iter"
```

Line L4 forms the denominator. It vanishes only when $2f'^2 = ff''$, which near a simple root cannot happen because $f'(x^*) \ne 0$ and $f(x^*) = 0$. Line L5 computes the step in the rational form $2ff'/(2f'^2 - ff'')$; dividing by $f'$ is avoided, so the step is defined when $f'(x) = 0$, but it is then $0$, and the method cannot move. The status "stalled" reports this instead of claiming convergence. An equivalent form is $s = N/(1 - \tfrac12 N f''/f')$ with the Newton step $N = f/f'$: Halley's step is Newton's step corrected by the curvature.

## Example

Take $f(x) = x^3 - x - 2$, $x_0 = 1$, $\delta = 10^{-14}$. At $x_0$: $f = -2$, $f' = 2$, $f'' = 6$, so $D = 2 \cdot 4 + 12 = 20$ and $s = -8/20 = -0.4$, giving $x_1 = 1.4$. The root is $x^* = 1.52137970680456757$. Exact rational arithmetic gives the errors and ratios:

| $k$ | $x_k$ | $e_k$ | $e_k / e_{k-1}^3$ |
|---|---|---|---|
| 0 | 1 | $-5.21 \times 10^{-1}$ | |
| 1 | 1.4 | $-1.21 \times 10^{-1}$ | 0.856 |
| 2 | 1.52048657111887 | $-8.93 \times 10^{-4}$ | 0.499 |
| 3 | 1.52137970650397 | $-3.01 \times 10^{-10}$ | 0.4219 |
| 4 | 1.52137970680456757 | $-1.15 \times 10^{-29}$ | 0.42140 |

The ratio tends to $c_2^2 - c_3 = 0.421403$, where $c_j = f^{(j)}(x^*)/(j!\,f'(x^*))$, as the theory below predicts. In floating point $x_4$ rounds to a number at which $f$ evaluates to exactly 0, so the implementation stops at L3 with status "exact" after 4 steps and 5 evaluations of the triple. Newton's method from the same start needs 7 steps, 14 evaluations of $f$ and $f'$.

Other runs with $\delta = 10^{-14}$, final error 0 in each: $\cos x - x$ from 1 in 3 steps (Newton 5), $e^x - 2$ from 0 in 3 steps (Newton 7), $x^{10} - 1$ from 1.5 in 5 steps. For $\arctan x$, where Newton diverges from $|x_0| > 1.39$, Halley converged from every start tried, up to $x_0 = 100$, in 4 or 5 steps; this is observed, not a theorem.

## Correctness

If $f \in C^3$ near a simple root $x^*$, there is $\rho > 0$ such that from every $x_0$ with $|e_0| \le \rho$ the iterates stay within $\rho$, converge to $x^*$, and satisfy $e_{k+1} = (c_2^2 - c_3)e_k^3 + o(e_k^3)$. So the order is at least 3, and exactly 3 when $c_2^2 \ne c_3$. If $f(x) = (x - x^*)^m h(x)$ with $m \ge 2$ and $h(x^*) \ne 0$, $h \in C^2$, the error satisfies $e_{k+1} = \frac{m - 1}{m + 1}e_k + O(e_k^2)$, so convergence is linear. The loop always stops, after at most $K$ steps. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs one evaluation of each of $f$, $f'$, $f''$ and $O(1)$ arithmetic, so a run costs at most $3K$ evaluations. From a start in the cubic region, reaching error $\delta$ takes about $\log_3(\log(1/\delta)/\log(1/|e_0|))$ steps, that is $O(\log\log(1/\delta))$. With order $q = 3$ and $w = 3$ the efficiency index is $3^{1/3} \approx 1.442$, against $2^{1/2} \approx 1.414$ for Newton and $1.618$ for the [secant method](/secant-method/). If $f''$ costs much less than $f$, as for a polynomial evaluated together with its derivatives by Horner's rule, the effective $w$ is close to 1 and the gain over Newton is real.

## Properties

- Order 3 at simple roots (local, proved), with error constant $c_2^2 - c_3$.
- Linear at multiple roots with rate $(m - 1)/(m + 1)$, better than Newton's $(m - 1)/m$; for $f = x^3$ the iterates halve exactly.
- Not bracketing and not globally convergent. It inherits Newton's chaotic behaviour on some functions; on $x^2 + 1$, which has no real root, it wanders until $K$.
- Uses no division by $f'$ in the rational form, so a zero of $f'$ stalls it rather than causing an overflow.

## Variants and improvements

- Halley's irrational formula $x - 2f/(f' + \sqrt{f'^2 - 2ff''})$ (with the sign that makes the denominator large) jumps to a root of the osculating parabola. It also has order 3, and can produce complex values where the rational form stays real.
- Chebyshev's method $x - N(1 + \tfrac12 N f''/f')$ and the super-Halley method form, with Halley's, Gander's family of third order methods.
- [Householder's methods](/householder-methods/) of order $d + 1$ use $f, \dots, f^{(d)}$; Halley's is $d = 2$, Newton's $d = 1$.
- [Laguerre's method](/laguerre-method/) for polynomials also uses $p$, $p'$, $p''$, has order 3 at simple roots, and for a polynomial whose roots are all real it converges from every real start.
- At a root of known multiplicity $m$, the step $f/\bigl(\tfrac{m+1}{2m}f' - \tfrac{ff''}{2f'}\bigr)$, which is Halley's method applied to $f^{1/m}$, restores order 3.

## When to use it

Use Halley's method when $f''$ is cheap once $f$ and $f'$ are known, as for polynomials, for $x^n - a$ (where it gives cubically convergent iterations for $n$-th roots), and for special functions defined by differential equations, where $f''$ follows from $f$ and $f'$. Prefer [Newton's method](/newton-raphson-method/) when $f''$ is expensive. Prefer a bracketing method such as [Brent's](/brent-method/) when no good start is known.

## Pitfalls

- L2: an expensive or inaccurate $f''$ wipes out the gain. A finite difference for $f''$ costs evaluations and accuracy, and the order drops.
- L3: a residual of exactly 0 can happen in floating point before the step test fires, as in the example; report it as a root, not as a failure.
- L5: at a zero of $f'$ the step is exactly 0. With $f = x^2 - 2$ and $x_0 = 0$ the method cannot move, and the status is "stalled", not "converged". Newton would divide by zero at the same point.
- L6 at a multiple root: convergence is linear, so $K$ must allow for it. For $(x - 1)^2(x + 2)$ from 2 the error falls by $1/3$ per step and needed 30 steps, and the attainable error is about $u^{1/m}$ in general.
- L7: a small step far from any root, near a local extremum of $f$, may stop the method at a point that is not a root. Check $|f(x)|$ against the expected accuracy afterwards.

## Implementations

## History

Edmond Halley published both his rational and irrational formulas in 1694 in the Philosophical Transactions, as a way to solve polynomial equations without first reducing them; the rational one is the method above. Schröder (1870) and later Householder placed it in families of higher order methods. Traub's 1964 book gave its order and error constant in the modern form, and Scavo and Thoo (1995) surveyed its geometry and its many rediscoveries, including the view as Newton's method on $f/\sqrt{f'}$.

## References
