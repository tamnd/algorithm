---
tag: 2GQVTS
kind: algorithm
slug: regula-falsi
name: Regula falsi
aliases:
- false position method
- method of false position
- rule of false position
area: numerical/root-finding
level: intro
summary: Bracketing method that cuts the bracket at the zero of the chord through its ends. It always keeps a root but is only linear, often with one end stuck.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {δ: the tolerance on the error, C: the linear rate in (0 1)}
  time: {one_end_fixed: "O(log(1/δ)/log(1/C))"}
  space: {extra: Θ(1)}
  evaluations: {per_step: "1"}
properties: {deterministic: true, recursive: false, bracketing: true, derivative_free: true, local: false}
prereqs: [bisection-method, secant-method, bracketing-method]
see_also: [illinois-method, bisection-method, secant-method, brent-method, dekker-method, ridders-method, chandrupatla-method, stopping-criteria]
sources:
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: Chapter 3, Method of false position (regula falsi)
  - book: isbn:9780898716443
    title: Germund Dahlquist and Åke Björck, Numerical Methods in Scientific Computing, Volume I, SIAM, 2008
    locator: Chapter 6, Solving scalar nonlinear equations, the section on the method of false position and its modifications
  - book: isbn:9780521880688
    title: W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 9.2, Secant method, false position method, and Ridders' method
  - paper: "M. Dowell and P. Jarratt, A modified regula falsi method for computing the root of an equation, BIT 11 (1971) 168-174"
    locator: the Illinois modification and its order
---

Regula falsi solves $f(x) = 0$ on a bracket $[a, b]$ with $f(a) f(b) < 0$. Like [bisection](/bisection-method/) it cuts the bracket at an inner point $c$ and keeps the half where the sign changes, so a root is never lost. Unlike bisection it does not take the midpoint: $c$ is the zero of the chord through $(a, f(a))$ and $(b, f(b))$, as in the [secant method](/secant-method/). For a continuous $f$ the method always converges to a root in exact arithmetic. Near a simple root where $f''$ has a fixed sign, though, one end of the bracket never moves, and the convergence is only linear.

## In plain words

You know that the curve is below the axis at one end of an interval and above it at the other, so it crosses somewhere in between. Draw the straight line between the two end points of the curve and see where the line crosses the axis. Compute the function there. If it is negative, that point becomes the new left end; if positive, the new right end. The crossing is always kept inside. When the curve is bent the same way across the interval, the same end gets replaced every time and the other end stays put, so the steps shrink by a fixed factor rather than faster and faster. Sometimes that is quicker than halving, and sometimes much slower.

## The problem

The input is a function $f$, real valued on $[a, b]$ with $a < b$, a tolerance $\delta \ge 0$ and a maximum number of steps $k_{\max}$. When $f(a)$ and $f(b)$ are finite and of opposite signs, the output is a point $\hat x$ and a flag, together with a bracket $[a_k, b_k] \subseteq [a, b]$ that still has a sign change. This is the bracketed form of the [root-finding problem](/root-finding-problem/).

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error, and $f[a, b] = (f(b) - f(a))/(b - a)$ the first [divided difference](/divided-differences/). A bracket is an interval $[a, b]$ with $f(a) f(b) < 0$. A method has order $q$ and rate $C$ when $|e_{k+1}| \approx C |e_k|^q$; with $w$ evaluations per step its efficiency index is $q^{1/w}$.

## The algorithm

```pseudo id=main
REGULA-FALSI(f, a, b, δ, kmax)
L1  fa ← f(a); fb ← f(b)
L2  if fa = 0 then return (a, "root"); if fb = 0 then return (b, "root")
L3  if fa or fb is not finite, or fa and fb have the same sign, then return (a, "no bracket")
L4  cprev ← none
L5  for k ← 1 to kmax do
L6      c ← b − fb · (b − a) / (fb − fa); if not a < c < b then c ← a + (b − a)/2
L7      fc ← f(c); if fc = 0 then return (c, "root"); if fc is not finite then return (c, "failure")
L8      if fc has the sign of fa then a, fa ← c, fc else b, fb ← c, fc
L9      if b − a ≤ 2δ then return (a + (b − a)/2, "bracket")
L10     if cprev ≠ none and |c − cprev| ≤ δ then return (c, "converged")
L11     cprev ← c
L12 return (c, "kmax reached")
```

Line L3 checks the bracket; NaN fails the test because a comparison with NaN is false. Line L6 computes the zero of the chord. Since $f(a)$ and $f(b)$ have opposite signs, $f(b) - f(a) \ne 0$ and the exact point lies strictly inside $(a, b)$; the guard on the same line only matters in rounding, when the computed $c$ can land on an end. Line L8 keeps the half with the sign change. Line L9 is a certified test: the root lies in $[a, b]$, so the midpoint is within $\delta$ of it. Line L10 is a step test on successive cut points; it is the usual test in practice but is not certified, because one end may be fixed while the other creeps (see the pitfalls). With $\delta = 0$, line L10 still ends the loop once the cut point repeats, which happens when the bracket has shrunk to adjacent floating-point numbers.

## Example

Solve $x^3 - x - 2 = 0$ on $[1, 2]$ in binary64, with $\delta = 10^{-12}$. Here $f(1) = -2$ and $f(2) = 4$, and the root is $x^* = 1.52137970680456756960\ldots$ Since $f'' = 6x > 0$, the chord lies above the graph, every $f(c)$ is negative, and the right end $b = 2$ never moves.

| $k$ | $c_k$ | $\lvert c_k - x^* \rvert$ | ratio |
|---|---|---|---|
| 1 | 1.3333333333333335 | $1.880 \cdot 10^{-1}$ | |
| 2 | 1.462686567164179 | $5.869 \cdot 10^{-2}$ | 0.312 |
| 3 | 1.5040190039499488 | $1.736 \cdot 10^{-2}$ | 0.296 |
| 4 | 1.516330564760263 | $5.049 \cdot 10^{-3}$ | 0.291 |
| 5 | 1.519918550023356 | $1.461 \cdot 10^{-3}$ | 0.289 |
| 6 | 1.5209574813719304 | $4.222 \cdot 10^{-4}$ | 0.2892 |
| 10 | 1.5213767690871818 | $2.938 \cdot 10^{-6}$ | 0.2888 |
| 15 | 1.521379700903058 | $5.902 \cdot 10^{-9}$ | 0.2888 |

The ratio of successive errors tends to $C = 1 - f'(x^*)(b - x^*)/f(b) = 0.28880$, as the rate formula below predicts. Line L10 stops at $k = 23$ with $c_{23} = 1.521379706804282$, error $2.86 \cdot 10^{-13}$, after 25 evaluations of $f$. Bisection needs 39 halvings for a bracket of width $2 \cdot 10^{-12}$, and the [secant method](/secant-method/) from the same two points 10 evaluations, without keeping a bracket. With $\delta = 0$ the loop ends at $k = 30$, where the computed $f(c)$ is exactly $0$.

## Correctness

All claims are proved in [the correctness proof](proofs/correctness.md).

- **Always.** The loop ends after at most $k_{\max}$ passes and $k_{\max} + 2$ evaluations, and when line L3 passes, every bracket $[a, b]$ that the method holds has $f(a)$, $f(b)$ of opposite signs. This holds in floating point too, for the computed values of $f$.
- **Convergence (proved, exact arithmetic).** Let $f$ be continuous on $[a_0, b_0]$ with $f(a_0) f(b_0) < 0$, and let the method run with $\delta = 0$ and $k_{\max} = \infty$. Then $a_k$ increases to a limit $\alpha$, $b_k$ decreases to a limit $\beta$, every end that moves infinitely often tends to a root, and every limit point of the cut points $c_k$ is a root of $f$ in $[a_0, b_0]$. The bracket width need not tend to $0$.
- **One end fixed (proved).** If $f \in C^2$ with $f'' > 0$ on $[a_0, b_0]$ and $f(a_0) < 0 < f(b_0)$, then $f(c_k) < 0$ for every $k$, so $b_k = b_0$ for all $k$ and $a_k = c_k$ increases to the unique root $x^*$. The other sign cases follow by symmetry.
- **Linear rate (proved).** In the setting of the previous item, with $b = b_0$ fixed and no $e_k$ zero,
$$\frac{e_{k+1}}{e_k} \to C = 1 - \frac{f'(x^*)\,(b - x^*)}{f(b)}, \qquad 0 < C < 1.$$
The identity behind it is the secant error identity with the fixed end in place of the older point: $e_{k+1} = e_k\,(b - x^*)\, f[x_k, b, x^*] / f[x_k, b]$.

## Complexity

The cost model is the number of evaluations of $f$.

- **Per step.** One evaluation, plus two at the start. A run that stops in pass $k$ costs $k + 2$ evaluations.
- **Steps to the tolerance.** When one end is fixed the error falls like $C^k$, so about $\log(1/\delta)/\log(1/C)$ steps are needed. The order is $1$ and the efficiency index is $1$. The rate $C$ can be close to $1$ when $f$ is strongly curved over the bracket, and then the method is far slower than bisection, which has rate $1/2$ on the bracket width.
- **No bound in terms of the bracket.** Unlike bisection there is no bound on the number of steps in terms of $(b - a)/\delta$ alone, since the width need not tend to $0$.
- **Space.** $\Theta(1)$.

### Floating point

The guard in line L6 keeps $c$ in $[a, b]$ even when rounding pushes the computed chord zero onto an end. The sign test of line L8 uses the computed $f(c)$. Near the root, where $|f(c)|$ is at the level of its rounding error $\varepsilon_f$, the computed sign can be wrong, so the final bracket is a bracket of the computed function: it holds a true root only up to about $\varepsilon_f / |f'(x^*)|$, the limiting accuracy. For a simple root and an $f$ evaluated with relative error near the unit roundoff $u$, this is about $u |x^*|$ times the [condition number](/root-conditioning/) of the root. Tolerances below this level make line L9 unreachable; line L10 or $k_{\max}$ then ends the loop.

## Properties

- **Bracketing.** The sign change is kept by construction, and a root is never lost.
- **Derivative free.** Only values of $f$ are used.
- **Linear.** Near a simple root with $f''(x^*) \ne 0$ the end on the convex side gets stuck, and the method reduces to the secant method with a fixed old point, which is linear (Ostrowski, Chapter 3).
- **Not symmetric in the roles of the ends.** Which end stays depends on the sign of $f''$, not on the start.
- **Exact on lines.** If $f$ is affine, the first cut point is the root.

## Variants and improvements

- **Illinois method.** When the same end is kept twice, halve its stored function value. This makes the chord steeper, moves the stuck end, and gives order $3^{1/3} \approx 1.442$ per evaluation ([Illinois method](/illinois-method/); Dowell and Jarratt, 1971).
- **Pegasus and Anderson-Björck.** Scale the stored value of the kept end by a factor computed from the last function values instead of $1/2$. Both have a higher order than the Illinois method (Dahlquist and Björck, Chapter 6; Anderson and Björck, 1973).
- **Ridders' method.** Use one extra evaluation at the midpoint and an exponential factor to straighten $f$ before taking the chord ([Ridders' method](/ridders-method/)).
- **Hybrids.** [Dekker's method](/dekker-method/), [Brent's method](/brent-method/) and [Chandrupatla's method](/chandrupatla-method/) take interpolation steps inside the bracket and fall back to bisection, which bounds the number of steps.

## When to use it

Regula falsi is a teaching method and the base of its modified forms. It is safe and simple, and it does well on functions that are nearly linear over the bracket. For production use, the Illinois method costs the same per step and avoids the stuck end, and Brent's method adds a guaranteed bound on the number of steps.

## Pitfalls

- **The stuck end.** For $f(x) = x^{10} - 1$ on $[0, 1.3]$ with $\delta = 10^{-10}$, the right end stays at $1.3$, the rate is close to $1$ at first, and line L10 stops only after 91 passes and 93 evaluations. Bisection reaches a bracket of width $2 \cdot 10^{-10}$ in 33 halvings.
- **The step test is not certified.** In the same run the returned point $0.999999999715045$ has error $2.85 \cdot 10^{-10}$, larger than $\delta$, because the creeping end moves less than the error. Line L9 certifies the error; line L10 does not. With a known rate $C$, the error is about $C/(1 - C)$ times the last step.
- **Width is not error.** The bracket width $b - a$ can stay near $b_0 - x^*$ forever, so a test on $b - a$ alone may never succeed; line L10 or $k_{\max}$ must stop the loop.
- **No sign change.** At an even multiplicity root, such as $(x - 1)^2$, the sign does not change and line L3 rejects the interval; at a pole, such as $1/(x - 0.3)$ on $[0, 1]$, the sign also changes and the bracket closes in on the pole (in binary64 a cut point lands exactly on $0.3$ and the evaluation divides by zero). Check $|f(\hat x)|$ at the end.
- **The product test.** Testing $f(a) f(c) < 0$ can underflow to $0$ or overflow; compare signs instead, as line L8 does.

## Implementations

## History

The rule of false position is one of the oldest methods of algebra. Solving a linear problem from two trial values appears in the Chinese Nine Chapters on the Mathematical Art as the rule of excess and deficiency, and medieval Arabic and European texts, among them Fibonacci's Liber Abaci (1202), teach it as the rule of double false position. Applied to a nonlinear $f$ and repeated, it becomes the iteration on this page. Ostrowski analysed its convergence and the stuck end (Ostrowski, Chapter 3). Dowell and Jarratt (1971) studied the Illinois modification, and Anderson and Björck (1973) gave a further one.

## References
