---
tag: ZF9XZ7
kind: algorithm
slug: steffensen-method
name: Steffensen's method
aliases:
- Steffensen iteration
- Aitken-Steffensen method
area: numerical/root-finding
level: advanced
summary: "A derivative-free method of order 2: a secant step whose increment is f(x) itself, x - f(x)^2 / (f(x + f(x)) - f(x)). For fixed points it is Aitken's extrapolation applied at every step."
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {δ: the tolerance on the error, C: "|f''(x*) (1 + f'(x*)) / (2 f'(x*))| at a simple root"}
  time: {local: "O(log log(1/(C δ)))"}
  space: {extra: Θ(1)}
  evaluations: {per_step: "2"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true, local: true}
history:
  year: 1933
  people: [Johan Frederik Steffensen, Alexander Aitken]
  note: Aitken gave the delta-squared extrapolation in 1926; Steffensen used it in 1933 to turn a linearly convergent fixed-point iteration into a quadratically convergent one.
prereqs: [newton-raphson-method, secant-method, fixed-point-iteration, aitken-delta-squared]
see_also: [aitken-delta-squared, fixed-point-iteration, secant-method, newton-raphson-method, muller-method, banach-fixed-point-theorem, order-of-convergence, multiplicity-of-roots]
sources:
  - paper: "J. F. Steffensen, Remarks on iteration, Skandinavisk Aktuarietidskrift 16 (1933) 64-72"
    locator: the iteration and its quadratic convergence
  - paper: doi:10.1017/S0370164600022070
    title: "A. C. Aitken, On Bernoulli's numerical solution of algebraic equations, Proceedings of the Royal Society of Edinburgh 46 (1926) 289-305"
    locator: the delta-squared process for accelerating linear convergence
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 2.6, Aitken extrapolation for linearly convergent sequences (with the Steffensen form)
  - paper: doi:10.1145/321850.321860
    title: "H. T. Kung and J. F. Traub, Optimal order of one-point and multipoint iteration, Journal of the ACM 21(4) (1974) 643-651"
    locator: Steffensen's method as the optimal two-evaluation method and the conjecture on optimal order
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: Chapter 3, the efficiency index
---

Steffensen's method solves $f(x) = 0$ by the step
$$x_{k+1} = x_k - \frac{f(x_k)^2}{f(x_k + f(x_k)) - f(x_k)}.$$
It is a [secant](/secant-method/) step through $x_k$ and $x_k + f(x_k)$: the increment of the difference quotient is the value $f(x_k)$ itself, which goes to zero as fast as the error, so the quotient approximates $f'(x_k)$ as well as Newton's method needs. The method converges with order 2 near a simple root, like [Newton's method](/newton-raphson-method/), with two evaluations of $f$ per step and no derivative. For a fixed-point problem $x = g(x)$ it is [Aitken's delta-squared process](/aitken-delta-squared/) applied after every two steps of [fixed-point iteration](/fixed-point-iteration/), which turns linear convergence into quadratic convergence.

## In plain words

Newton's method needs the slope of the function. Steffensen's method estimates the slope from two values: the value at the current guess, and the value a little to the side. The clever part is how far to the side: exactly as far as the current function value. Far from the root that is a big step and the slope estimate is rough; near the root the function value is tiny, so the second point is very close and the estimate is almost exact. The result behaves like Newton's method, doubling the correct digits in each step near the root, using two function values per step and no derivative.

## The problem

The input is a function $f$ given as a procedure, a start $x_0$, a tolerance with an absolute part $\delta_a \ge 0$ and a relative part $\delta_r \ge 0$, and a maximum number of steps $k_{\max}$. The output is a point $\hat x$ and a flag. Convergence is guaranteed only near a simple root of a function with a continuous second derivative.

Notation on the root-finding pages: $x^*$ is a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error, $s_k = x_{k+1} - x_k$ the step. A method has order $q$ and rate constant $C$ when $|e_{k+1}| \approx C|e_k|^q$. The cost is the number of evaluations of $f$; with $w$ evaluations per step the efficiency index is $q^{1/w}$. Divided differences are $f[a, b] = (f(b) - f(a))/(b - a)$ and $f[a, b, c] = (f[b, c] - f[a, b])/(c - a)$.

## The algorithm

```pseudo id=main
STEFFENSEN(f, x0, δa, δr, kmax)
L1  x ← x0
L2  for k ← 1 to kmax do
L3      fx ← f(x); if fx = 0 then return (x, "root")
L4      if fx is not finite then return (x, "failure")
L5      y ← x + fx; if y = x then return (x, "residual"); fy ← f(y)
L6      d ← (fy − fx) / (y − x); if d = 0 or fy is not finite then return (x, "failure")
L7      s ← −fx / d
L8      xnew ← x + s
L9      if xnew is not finite then return (x, "failure")
L10     if |s| ≤ δa + δr · |xnew| then return (xnew, "converged")
L11     x ← xnew
L12 return (x, "kmax reached")
```

Line L5 places the second point at distance $f(x)$ from $x$. In floating point it divides by the computed increment $y - x$ rather than by $f(x)$, so the slope is the exact difference quotient of the two points actually used. If $|f(x)|$ is below half a unit in the last place of $x$, then $y = x$ and no slope can be formed; the program returns with the flag "residual", which says that $|f(x)| \le u|x|$, not that $x$ is close to a root. Line L6 forms the slope $d = f[x, y]$, and lines L7 and L8 take the secant step. Line L10 is the step test of the [stopping criteria](/stopping-criteria/) page, and line L2 bounds the work.

**The fixed-point form.** For $x = g(x)$, apply the method to $f(x) = g(x) - x$. With $y = g(x)$ and $z = g(y)$, the point $x + f(x)$ is $y$ and $f(y) = z - y$, and the step becomes
$$x_{k+1} = x_k - \frac{(y - x_k)^2}{z - 2y + x_k},$$
which is Aitken's extrapolation of the three iterates $x_k, y, z$ of the fixed-point iteration. The implementation provides both forms.

## Example

Solve $\cos x - x = 0$ from $x_0 = 1$ in binary64, with $\delta_a = 0$ and $\delta_r = 2^{-50}$. The root is $x^* = 0.73908513321516064\ldots$, with $f'(x^*) = -1.673612$ and $f''(x^*) = -\cos x^* = -0.739085$.

| $k$ | $x_k$ | $f(x_k)$ | $\lvert e_k \rvert$ (exact arithmetic) |
|---|---|---|---|
| 0 | 1.0 | $-4.596977 \cdot 10^{-1}$ | $2.6091 \cdot 10^{-1}$ |
| 1 | 0.728010361467617 | $1.848939 \cdot 10^{-2}$ | $1.1075 \cdot 10^{-2}$ |
| 2 | 0.7390669669086738 | $3.040323 \cdot 10^{-5}$ | $1.8166 \cdot 10^{-5}$ |
| 3 | 0.7390851331660756 | $8.214929 \cdot 10^{-11}$ | $4.9085 \cdot 10^{-11}$ |
| 4 | 0.7390851332151607 | $0$ | $3.5836 \cdot 10^{-22}$ |

In 300-digit arithmetic the ratios $|e_{k+1}|/|e_k|^2$ are $0.1627$, $0.1481$, $0.14874$, $0.148737$ and tend to
$$C = \left|\frac{f''(x^*)(1 + f'(x^*))}{2f'(x^*)}\right| = \frac{0.739085 \cdot 0.673612}{2 \cdot 1.673612} = 0.148737,$$
the constant of the Correctness section. In binary64 the computed $f(x_4)$ is exactly $0$, so the program returns in pass 5 after 9 evaluations: two in each of passes 1 to 4 and one in pass 5. Newton's method from the same start needs 5 values of $f$ and 4 of $f'$. The fixed-point form with $g = \cos$ reaches the same point, within one unit in the last place.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **Always.** The loop ends after at most $k_{\max}$ passes and $2k_{\max}$ evaluations. A result flagged "root" is an exact zero of the computed $f$, one flagged "converged" passed the step test, and one flagged "residual" has $|f(\hat x)| \le u|\hat x|$.
- **Error identity (proved).** With $y_k = x_k + f(x_k)$,
$$e_{k+1} = \frac{f[x^*, x_k, y_k]}{f[x_k, y_k]}\, e_k\,(e_k + f(x_k)).$$
- **Local quadratic convergence (proved).** Let $f \in C^2$ near a simple root $x^*$, and on $I = [x^* - r, x^* + r]$ let $L = \max_I |f'|$, $\mu = \min_I |f'| > 0$ and $M = \max_I |f''|$. If $(1 + L)|e_0| \le r$ and $\frac{M(1 + L)}{2\mu}|e_0| \le \frac12$, the iterates stay in $I$ and $|e_{k+1}| \le \frac{M(1 + L)}{2\mu}|e_k|^2 \le \frac12|e_k|$. Asymptotically $e_{k+1} \approx \frac{f''(x^*)(1 + f'(x^*))}{2f'(x^*)}e_k^2$, so the method is of order 3 when $f'(x^*) = -1$.
- **Fixed points (proved).** If $g \in C^2$ near a fixed point $x^*$ with $g'(x^*) \ne 1$, the fixed-point form converges quadratically from close starts, even when $|g'(x^*)| > 1$ and the plain iteration $x \leftarrow g(x)$ diverges. This is the root form applied to $g(x) - x$, whose derivative $g'(x^*) - 1$ is nonzero.
- **Global (none).** From poor starts the increment $f(x)$ can be large and the slope estimate useless.

## Complexity

The cost model is the number of evaluations of $f$.

- **Per step.** Two evaluations, so with $q = 2$ and $w = 2$ the efficiency index is $2^{1/2} \approx 1.414$, the same as Newton's method when $f'$ costs as much as $f$, and below the secant method's $1.618$. Kung and Traub (1974) showed that order 2 is the best possible for methods of this kind with two evaluations, and conjectured that $2^{w-1}$ is the best order for $w$ evaluations without memory.
- **Steps to the tolerance.** In the local regime, $\lceil \log_2 \log_2 (1/(K\delta)) \rceil$ steps with $K = M(1 + L)/(2\mu)$.
- **Total evaluations.** A run that ends by the step test in pass $k$ makes $2k$ evaluations; one that ends at line L3 or L5 in pass $k$ makes $2k - 1$.
- **Space.** $\Theta(1)$.

### Floating point

Near the root, $f(x)$ is small, and the two values $f(x)$ and $f(x + f(x))$ differ by about $f'(x)f(x)$. The error $\varepsilon_f$ in each computed value then gives a relative error of about $\varepsilon_f/|f'(x)f(x)|$ in the slope. That error does not spoil the step while $|f(x)| \gg \varepsilon_f$, because the step is $f(x)/d$ and only needs a few correct digits of $d$; it stops the convergence near the limiting accuracy $\varepsilon_f/|f'(x^*)| + u|x^*|$ of every method that uses values of $f$. Once $|f(x)| < u|x|/2$ the second point coincides with $x$, and line L5 stops; in a well-scaled problem with $|f'(x^*)|$ near 1 that is the limiting accuracy, but in a badly scaled one it can happen far from the root. The step test may never pass on rounding noise, so line L2 is needed.

## Properties

- **Derivative-free, order 2.** No derivative and quadratic local convergence.
- **Not scale invariant.** Replacing $f$ by $cf$ changes the increment $f(x)$ and so changes the iterates. Newton's and the secant method are scale invariant; Steffensen's is not, and it works best when $|f'| \approx 1$ near the root.
- **No memory.** Each step uses only the current point, unlike the secant method, which reuses the previous value.
- **Exact for linear functions.** If $f$ is linear, the first step lands on the root.
- **Accelerates fixed-point iterations.** The fixed-point form converges even for repelling fixed points.

## Variants and improvements

- **Scaled increment.** Use $y = x + \gamma f(x)$ with a constant $\gamma$ chosen to make $\gamma f'$ of order 1, which restores robustness for badly scaled $f$; with $\gamma \approx -1/f'(x^*)$ the order rises to 3.
- **Secant method.** Reuse the previous point instead of a new one: one evaluation per step, order $1.618$, efficiency $1.618$.
- **Higher-order Steffensen-type methods.** Multipoint methods with $w$ evaluations and order $2^{w-1}$, optimal in the sense of Kung and Traub, built from divided differences without derivatives.
- **Systems.** Replace the derivative by a matrix of divided differences with increments $F_i(x)$, giving a quadratically convergent derivative-free method for systems.

## When to use it

Use Steffensen's method when derivatives are not available, a good start is known and $f$ is well scaled, or in its fixed-point form to accelerate a slowly convergent fixed-point iteration. Otherwise the [secant method](/secant-method/) is usually more efficient per evaluation, and a bracketing method is safer.

## Pitfalls

- **Poor scaling.** For $f(x) = 2^{-60}(x - 1)$ from $0.5$, the increment $f(x)$ is below half an ulp of $x$, and the program stops at once with the flag "residual", far from the root.
- **Large values far from the root.** For $e^x - 1$ from $3$, the increment is $f(3) = 19$ and $f(22) \approx 3.6 \cdot 10^9$, so the slope is huge and the steps are tiny; after 100 passes the iterate is still $2.99999$ (observed).
- **Divergence.** For $\arctan x$ from $2$ the iterates run off to infinity and the program fails after 6 passes.
- **Multiple roots.** Convergence becomes linear; for $(x - 1)^2$ from $3$ the program stops by the residual test after 31 passes with error $1.0 \cdot 10^{-8}$.
- **Flat pieces.** If $f(x + f(x)) = f(x)$, the slope is zero and line L6 fails.

## Implementations

## History

Alexander Aitken introduced the delta-squared process in 1926, in a paper on Bernoulli's method for polynomial roots. Johan Frederik Steffensen, a Danish actuary and numerical analyst, used it in 1933 inside the iteration, so that each step extrapolates from two fresh fixed-point steps; the root form follows by applying it to $g(x) = x + f(x)$. Kung and Traub placed it in 1974 as the first member of a family of optimal derivative-free multipoint methods.

## References
