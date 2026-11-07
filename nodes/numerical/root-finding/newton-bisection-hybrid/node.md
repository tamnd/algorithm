---
tag: STTPS1
kind: algorithm
slug: newton-bisection-hybrid
name: Safeguarded Newton method
aliases:
- rtsafe
- Newton with bisection fallback
- Newton-bisection hybrid
area: numerical/root-finding
level: core
summary: Newton steps kept inside a bracket, with a bisection whenever a step leaves the bracket or fails to halve the previous one. Always converges; fast near a simple root.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {N: "ceil(log2((b - a)/δ))", δ: the tolerance}
  time: {worst: "O(N^2)", local: "O(log log(1/δ))"}
  space: {extra: Θ(1)}
  evaluations: {per_step: "2"}
properties: {deterministic: true, recursive: false, bracketing: true, derivative_free: false, local: false}
prereqs: [newton-raphson-method, bisection-method, bracketing-method]
see_also: [newton-raphson-method, bisection-method, brent-method, dekker-method, regula-falsi, interval-newton-method, stopping-criteria, multiplicity-of-roots]
sources:
  - book: isbn:9780521880688
    title: W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 9.4, Newton-Raphson method using derivative (the routine rtsafe)
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 2.5, Methods for solving a nonlinear equation globally (the hybrid of Newton and bisection)
  - book: isbn:9780486419985
    title: Richard P. Brent, Algorithms for Minimization without Derivatives, Prentice-Hall, 1973 (reprinted by Dover, 2002)
    locator: Chapter 4, An algorithm with guaranteed convergence for finding a zero of a function
---

The safeguarded Newton method finds a root of $f$ in a bracket $[a, b]$ with $f(a) f(b) < 0$. In each step it proposes the [Newton](/newton-raphson-method/) point from the newest iterate. It accepts the point when it lies strictly inside the current bracket and the step is at most half the previous one; otherwise it takes the midpoint, as in [bisection](/bisection-method/). Each new point shrinks the bracket. So the method never loses the root, converges for every continuous $f$ with a bracket, and near a simple root it takes only Newton steps and converges quadratically. This is the scheme of the routine rtsafe in Numerical Recipes.

## In plain words

Newton's method is fast when it works and can fly off when it does not. Bisection is slow but cannot fail once the function changes sign over an interval. Run both together. Keep an interval where the sign changes. At each step, try the Newton step. If it lands outside the interval, or if it is not at least twice as short as the step before, the Newton step is not making good progress, so cut the interval in half instead. Every new point is used to shrink the interval. Near the root the Newton steps pass both tests, and the method is as fast as Newton's.

## The problem

The input is a function $f$ and its derivative $f'$, a bracket $[a, b]$ with $a < b$, a tolerance $\delta \ge 0$ and a maximum number of steps $k_{\max}$. The output is a point $\hat x$, a flag, and the final bracket. This is the bracketed form of the [root-finding problem](/root-finding-problem/), with derivatives available.

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A bracket is an interval $[a, b]$ with $f(a) f(b) < 0$. A method has order $q$ and rate $C$ when $|e_{k+1}| \approx C |e_k|^q$; with $w$ evaluations per step its efficiency index is $q^{1/w}$. Here $s_k = x_{k+1} - x_k$ is the step of pass $k$.

## The algorithm

```pseudo id=main
SAFE-NEWTON(f, f', a, b, δ, kmax)
L1  fa ← f(a); fb ← f(b); if fa = 0 then return (a, "root"); if fb = 0 then return (b, "root")
L2  if fa or fb is not finite, or fa and fb have the same sign, then return (a, "no bracket")
L3  x ← a + (b − a)/2; sprev ← b − a
L4  for k ← 1 to kmax do
L5      fx ← f(x); if fx = 0 then return (x, "root"); if fx is not finite then return (x, "failure")
L6      if fx has the sign of fa then a, fa ← x, fx else b, fb ← x, fx
L7      if b − a ≤ 2δ then return (a + (b − a)/2, "bracket")
L8      d ← f'(x); if d is finite and nonzero then xn ← x − fx/d else xn ← none
L9      if xn is none, or not a < xn < b, or |xn − x| > |sprev|/2 then xn ← a + (b − a)/2
L10     if |xn − x| ≤ δ then return (xn, "converged")
L11     sprev ← xn − x; x ← xn
L12 return (x, "kmax reached")
```

Line L6 makes the new point an end of the bracket, so $x$ is always an end when line L8 runs. Line L9 is the safeguard: it rejects a Newton point that is undefined, outside the open bracket, or not at least a halving of the previous step. The midpoint is then at distance $(b - a)/2$ from $x$. Line L7 is a certified test: the root lies in $[a, b]$. Line L10 ends on a small step. After a Newton step it is not certified, but near a simple root the error after a step of size $\tau$ is at most $4 M \tau^2$, where $M = \max|f''|/(2\min|f'|)$ (see the Newton page). After a bisection the step is half the width, so line L7 has already caught that case.

## Example

Solve $f(x) = x^3 - 2x + 2 = 0$ on $[-3, 2]$ in binary64 with $\delta = 10^{-12}$; $f(-3) = -19$, $f(2) = 6$, and the only real root is $x^* = -1.76929235423863141524\ldots$ Plain Newton from $0$ cycles forever: $0 \to 1 \to 0$.

| pass | $x$ | $f(x)$ | bracket after line L6 | proposal | taken |
|---|---|---|---|---|---|
| 1 | $-0.5$ | $2.875$ | $[-3, -0.5]$ | Newton $1.8$, outside | midpoint $-1.75$ |
| 2 | $-1.75$ | $1.406 \cdot 10^{-1}$ | $[-3, -1.75]$ | $-1.7695652173913043$ | Newton |
| 3 | $-1.7695652173913043$ | $-2.017 \cdot 10^{-3}$ | $[-1.76957, -1.75]$ | $-1.7692924076914929$ | Newton |
| 4 | $-1.7692924076914929$ | $-3.951 \cdot 10^{-7}$ | $[-1.7692924, -1.75]$ | $-1.7692923542386334$ | Newton |
| 5 | $-1.7692923542386334$ | $-1.465 \cdot 10^{-14}$ | $[-1.76929235, -1.75]$ | $-1.7692923542386314$ | Newton, step $2 \cdot 10^{-15} \le \delta$ |

The errors of the points evaluated in passes 2 to 5 are $1.93 \cdot 10^{-2}$, $2.73 \cdot 10^{-4}$, $5.35 \cdot 10^{-8}$ and $1.99 \cdot 10^{-15}$, a quadratic sequence. Line L10 returns $-1.7692923542386314$, the binary64 number nearest to $x^*$, after 7 evaluations of $f$ and 5 of $f'$. The right end stays at $-1.75$: the Newton iterates approach the root from the left, which is normal and is why the method stops on the step, not on the width. Bisection alone needs 42 halvings for the same tolerance.

## Correctness

All claims are proved in [the correctness proof](proofs/correctness.md).

- **Always.** The loop ends after at most $k_{\max}$ passes. When line L2 passes, every bracket the method holds has end values of opposite signs, and every point evaluated lies in the bracket. This holds in floating point for the computed values.
- **Bounded number of passes (proved, exact arithmetic).** If $\delta > 0$ and $N = \lceil \log_2((b - a)/\delta) \rceil$, the method returns after at most $(N + 1)^2$ passes, whatever $f$ and $f'$ are.
- **Global convergence (proved, exact arithmetic).** If $f \in C^1$ on $[a, b]$, $\delta = 0$ and $k_{\max} = \infty$, then the iterates converge to a root of $f$ in $[a, b]$, or the method returns an exact root.
- **Local quadratic convergence (proved, with a hypothesis).** Let $f \in C^2$ with $f' > 0$ and $f'' > 0$ on the bracket (the other sign cases are symmetric). If a Newton step is accepted from a point $x_k > x^*$ with $M (x_k - x^*) \le 1/6$, then every later pass takes the Newton step, and the convergence is quadratic. That the method reaches such a point quickly is what happens in practice (as in the example), but the rule does not guarantee it.

## Complexity

The cost model is the number of evaluations of $f$ and $f'$.

- **Per pass.** One evaluation of $f$ and one of $f'$, plus two of $f$ at the start.
- **Worst case.** At most $(N + 1)^2$ passes by the bound above: at most $N$ bisections, and between two bisections at most $N$ Newton steps, since each halves the step. This is weaker than the $N$ steps of bisection; Brent's method has a bound of the same kind.
- **Near a simple root.** Quadratic: $O(\log \log (1/\delta))$ passes, with efficiency index $2^{1/2}$ when $f'$ costs as much as $f$.
- **Space.** $\Theta(1)$.

### Floating point

The bracket test of line L7 cannot go below the spacing of the floating-point numbers near the root. With $\delta = 0$ the loop still ends: when $a$ and $b$ are adjacent numbers, any Newton point fails the strict test $a < x_n < b$, the computed midpoint equals an end, which is $x$ itself, and line L10 sees a zero step. Near the root the computed sign of $f$ can be wrong once $|f(x)|$ is at the level of its rounding error $\varepsilon_f$, so the bracket is a bracket of the computed function, accurate to about $\varepsilon_f/|f'(x^*)|$ ([stopping criteria](/stopping-criteria/)).

## Properties

- **Bracketing and global.** The root is never lost, and no starting guess is needed beyond the bracket.
- **Needs the derivative.** Each pass evaluates $f'$; where $f'$ is unavailable, use [Brent's method](/brent-method/).
- **Not every point is an improvement in $|f|$.** A bisection point can have a larger $|f|$ than the previous point.
- **Asymmetric bracket shrinking.** Near a root with $f'' \ne 0$ the Newton iterates stay on one side, and the far end of the bracket stops moving.

## Variants and improvements

- **The rtsafe rule.** Numerical Recipes tests whether the Newton point lies in the bracket by the sign of $((x - b) f' - f)((x - a) f' - f)$, which avoids the division, and compares $|2 f|$ with $|s_{\text{prev}} f'|$ for the halving test.
- **Newton from the best end.** Starting each Newton step from the end with the smaller $|f|$ keeps quadratic progress after a forced bisection.
- **Derivative free.** [Dekker's method](/dekker-method/) and [Brent's method](/brent-method/) use secant and inverse quadratic steps with a similar safeguard, and Brent's rule also bounds the number of evaluations by about $N^2$.
- **Interval arithmetic.** The [interval Newton method](/interval-newton-method/) contracts a bracket using an enclosure of $f'$, and can prove that the root is unique.
- **Multiple roots.** With the multiplicity $m$ known, the step $-m f/f'$ restores quadratic convergence ([multiplicity of roots](/multiplicity-of-roots/)).

## When to use it

Use the safeguarded Newton method when a bracket is known, the derivative is cheap, and a guarantee is wanted. Examples are inverting a monotone function such as a cumulative distribution function, and computing implied parameters in financial models. When the derivative is expensive or unavailable, Brent's method is the standard choice.

## Pitfalls

- **Multiple roots.** At a root of multiplicity $m$ Newton is linear with rate $1 - 1/m$. For $m = 3$ the rate $2/3$ fails the halving test every second pass: for $(x - 1)^3$ on $[0, 3]$ with $\delta = 10^{-12}$ the passes alternate between Newton and bisection, 63 passes and 65 evaluations of $f$, more than the 41 of plain bisection.
- **Width as the only stopping test.** In the example the bracket width stays near $0.02$; a test on the width alone would bisect for many more passes.
- **Discontinuities.** At a pole the sign changes; the method closes in on the pole. Check $|f(\hat x)|$.
- **A wrong derivative.** An error in $f'$ does not break the guarantee (the safeguard catches bad steps), but it destroys the quadratic convergence silently. Test $f'$ against a finite difference.

## Implementations

## History

Safeguarding a fast local method with bisection is the idea of Dekker (1969) and Brent (1973) for derivative-free methods. The Newton form with a halving test appears as the routine rtsafe in Numerical Recipes (first edition, 1986), and Dennis and Schnabel (1983) describe the hybrid of Newton's method and bisection as the model of a globally convergent method in one variable.

## References
