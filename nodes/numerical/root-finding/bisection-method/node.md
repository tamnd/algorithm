---
tag: QXCMB9
kind: algorithm
slug: bisection-method
name: Bisection method
aliases:
- interval halving
- binary search for roots
- bisection
- Bolzano method
area: numerical/root-finding
level: intro
summary: Halve a sign-changing bracket until it is shorter than twice the tolerance. Each step costs one evaluation and halves the error bound, for every continuous function.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {w: "the width b - a of the starting bracket", δ: "the tolerance on the error of the returned point"}
  time: {worst: "Θ(log(w/δ))", best: Θ(1)}
  space: {extra: Θ(1)}
  evaluations: {worst: "⌈log2(w/(2δ))⌉ + 2"}
properties: {deterministic: true, recursive: false, bracketing: true, derivative_free: true}
prereqs: [bracketing-method, root-finding-problem, binary-search]
see_also: [regula-falsi, illinois-method, brent-method, dekker-method, chandrupatla-method, newton-bisection-hybrid, stopping-criteria, real-root-isolation]
sources:
  - book: isbn:9781305253667
    title: Richard L. Burden, J. Douglas Faires and Annette M. Burden, Numerical Analysis, tenth edition, Cengage, 2016
    locator: Section 2.1, The Bisection Method (Theorem 2.1 on the error bound)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 1, Solution of equations by iteration (the bisection method and its error bound)
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 2.5, Globally convergent methods for solving one equation in one unknown
  - paper: "K. Sikorski, Bisection is optimal, Numerische Mathematik 40, 111-117, 1982"
    locator: the minimax optimality of bisection among methods that use function values on the class of continuous functions with a sign change
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 5.1, Horner's method (the rounding error bound of a computed polynomial value)
---

The bisection method finds a root of a continuous function $f$ on a [bracket](/bracketing-method/) $[a, b]$ with $f(a) f(b) < 0$. It evaluates $f$ at the midpoint and keeps the half whose ends still have opposite signs. After $k$ steps the bracket has width $(b - a)/2^k$, so the method reaches any tolerance $\delta$ in $\lceil \log_2((b-a)/(2\delta)) \rceil$ steps, for every continuous $f$. It is slow next to the [secant method](/secant-method/) or [Newton's method](/newton-raphson-method/), but it never fails, and it is the safety net inside [Dekker's](/dekker-method/) and [Brent's](/brent-method/) methods.

## In plain words

You know that a continuous curve is below the axis at the left end of an interval and above it at the right end. So it crosses the axis somewhere in between. Look at the middle point. If the curve is below the axis there, the crossing is in the right half. If it is above, the crossing is in the left half. Keep that half and throw the other half away. Each look halves the length of the interval that must hold the crossing. After about twenty looks the interval is a million times shorter than at the start. This is the same idea as binary search in a sorted array, but on a line of real numbers.

## The problem

The input is a function $f : [a, b] \to \mathbb{R}$ that is continuous, two points $a < b$ with $f(a) f(b) < 0$, a tolerance $\delta > 0$ and a maximum number of steps $k_{\max}$. The output is a point $\hat x$ and a root $x^*$ of $f$ in $[a, b]$ with $|\hat x - x^*| \le \delta$. By the intermediate value theorem such a root exists. This is the bracketed form of the [root-finding problem](/root-finding-problem/).

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

## The algorithm

The test "same sign" compares signs. It does not form the product $f(a) f(c)$, which can underflow to zero or overflow.

```pseudo id=main
BISECT(f, a, b, δ, kmax)                  ▷ a < b, f(a) f(b) < 0, δ ≥ 0
L1  fa ← f(a), fb ← f(b)
L2  if fa = 0 then return a; if fb = 0 then return b
L3  if fa or fb is NaN, or sign(fa) = sign(fb) then error "no bracket"
L4  for k ← 1 to kmax do
L5      c ← a + (b − a)/2
L6      if c ≤ a or c ≥ b then return c           ▷ no number strictly between a and b
L7      fc ← f(c)
L8      if fc = 0 then return c; if fc is NaN then error
L9      if sign(fc) = sign(fa) then a ← c, fa ← fc
L10     else b ← c, fb ← fc
L11     if b − a ≤ 2δ then return a + (b − a)/2
L12 return a + (b − a)/2, with the flag "kmax reached"
```

Lines L1 to L3 evaluate the ends and reject an input that is not a bracket. Each pass of the loop evaluates $f$ once, at the midpoint $c$, and keeps the half $[a, c]$ or $[c, b]$ whose ends have opposite signs. Line L11 stops when the bracket is at most $2\delta$ wide: then its midpoint is within $\delta$ of each point of the bracket, and so of the root. Line L6 stops the loop in floating point when $a$ and $b$ are adjacent numbers, so a tolerance below the spacing of the numbers, or $\delta = 0$, cannot make the loop run forever. The midpoint is $a + (b - a)/2$ and not $(a + b)/2$: in floating point the second form can overflow, and for some inputs it falls outside $[a, b]$.

## Example

Take $f(x) = x^3 - x - 2$ on $[1, 2]$. Here $f(1) = -2$ and $f(2) = 4$, and the only real root is $x^* = 1.5213797068045675696\ldots$.

| k | a | b | c | f(c) | kept |
|---|---|---|---|---|---|
| 1 | 1 | 2 | 1.5 | −0.125 | [c, b] |
| 2 | 1.5 | 2 | 1.75 | 1.60938 | [a, c] |
| 3 | 1.5 | 1.75 | 1.625 | 0.666016 | [a, c] |
| 4 | 1.5 | 1.625 | 1.5625 | 0.252197 | [a, c] |
| 5 | 1.5 | 1.5625 | 1.53125 | 0.0591125 | [a, c] |
| 6 | 1.5 | 1.53125 | 1.515625 | −0.0340538 | [c, b] |
| 7 | 1.515625 | 1.53125 | 1.5234375 | 0.0122504 | [a, c] |
| 8 | 1.515625 | 1.5234375 | 1.51953125 | −0.0109712 | [c, b] |
| 9 | 1.51953125 | 1.5234375 | 1.521484375 | 0.000622176 | [a, c] |
| 10 | 1.51953125 | 1.521484375 | 1.5205078125 | −0.00517889 | [c, b] |

After 10 steps the bracket is $[1.5205078125, 1.521484375]$, of width $2^{-10}$, and it holds $x^*$. The midpoints do not get closer to $x^*$ at each step: $c_9$ is closer than $c_{10}$. Only the width of the bracket falls in a fixed way. For $\delta = 10^{-6}$ the method needs $\lceil \log_2(1/(2 \cdot 10^{-6})) \rceil = 19$ steps, so 21 evaluations in all.

## Correctness

The loop keeps this [invariant](/loop-invariant/): $a < b$, $fa = f(a)$ and $fb = f(b)$ are nonzero with opposite signs, and $b - a = (b_0 - a_0)/2^{k}$ after $k$ passes in exact arithmetic. By the intermediate value theorem, $[a, b]$ holds a root. Each pass keeps the invariant, because $f(c) \ne 0$ has the sign of $f(a)$ or of $f(b)$. The width halves in each pass, so line L11 stops after at most $\lceil \log_2((b_0 - a_0)/(2\delta)) \rceil$ passes. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The cost model is the number of evaluations of $f$, on a [real RAM](/real-ram/) for the exact analysis.

- **Evaluations.** Let $w = b_0 - a_0$. If $w > 2\delta$ and no midpoint is a root, the method makes exactly $\lceil \log_2(w/(2\delta)) \rceil$ passes, so it evaluates $f$ exactly $\lceil \log_2(w/(2\delta)) \rceil + 2$ times. A zero at an end costs 1 or 2 evaluations, and a zero at a midpoint stops the loop early.
- **Convergence.** The error bound $\beta_k = (b_0 - a_0)/2^{k+1}$ of the midpoint after $k$ passes falls by the factor $1/2$ in each step. So the bound converges linearly with rate $1/2$. The error $e_k$ itself need not fall in each step, as the example shows, so the method has no order in the sense $|e_{k+1}| \approx C |e_k|^q$; it has R-order 1.
- **Time and space.** Each pass does a fixed number of arithmetic operations besides the call of $f$. The space is $\Theta(1)$.
- **Optimality.** Sikorski (1982) proved that bisection is optimal in the worst case: among all methods that use $n$ values of $f$, adaptive or not, no method gives a smaller worst-case error over the class of continuous functions with $f(a) f(b) < 0$. Faster methods need more structure in $f$, such as smoothness near a simple root.

In the efficiency index $q^{1/w}$, bisection has $q = 1$, so the index does not compare it with other linear methods; its rate $1/2$ per evaluation does. Newton's method, with index $2^{1/2} \approx 1.414$, and the secant method, with index $1.618$, are faster, but only near a simple root.

### Floating point

Let $\hat f$ be the computed function, with $|\hat f(x) - f(x)| \le \varepsilon_f$ near the root. The method then brackets a sign change of $\hat f$, not of $f$. At a point with $|f(x)| > \varepsilon_f$ the computed sign is right, so the returned point lies within the width of the final bracket of the set $\{x : |f(x)| \le \varepsilon_f\}$. Near a simple root this set is an interval of radius about $\varepsilon_f / |f'(x^*)|$. For a polynomial evaluated by [Horner's rule](/horner-rule/), $\varepsilon_f \le \gamma_{2n} \sum_i |a_i| |x|^i$ with $\gamma_{2n} = 2nu/(1 - 2nu)$, $n$ the degree and $u$ the [unit roundoff](/machine-epsilon/) (Higham, Section 5.1). No method that uses only computed values of $f$ can do better than this limiting accuracy, so a tolerance below it only adds steps. With $\delta = 0$, line L6 stops the loop when $a$ and $b$ become adjacent numbers. In binary64 this takes at most about 2100 passes, since the width starts below $2^{1024}$ and the spacing of the numbers is at least $2^{-1074}$; for a root near 1 and a bracket of width 1 it takes 53 passes.

## Properties

- **Global.** The method converges for every continuous $f$ and every bracket. It needs no derivative and no starting point close to the root.
- **The bracket is kept.** At each step the current interval has a sign change, so the method also returns a certified enclosure $[a, b]$.
- **The work is known in advance.** The number of steps depends only on $w$ and $\delta$, not on $f$.
- **Which root.** With several roots in $[a, b]$, the method finds one of the roots where $f$ changes sign. A root of even [multiplicity](/multiplicity-of-roots/), such as the root of $(x-1)^2$, gives no sign change and cannot be bracketed.
- **Multiple roots do not slow it.** Unlike Newton's method, bisection has the same rate at a root of odd multiplicity $m \ge 3$.

## Variants and improvements

- **Bisection on the exponent.** For a bracket such as $[10^{-300}, 10^{300}]$, bisect $\log x$, or bisect the bit patterns of the floats as integers. For a bracket of positive binary64 numbers the number of steps is then at most 63, whatever the range.
- **Sign-only bisection.** The method uses only the sign of $f$. So it works when $f$ is a comparison, for example "is the computed value too large".
- **Regula falsi and Illinois.** Replace the midpoint by the root of the secant line through the ends. Plain [regula falsi](/regula-falsi/) can be slower than bisection; the [Illinois method](/illinois-method/) fixes this.
- **Hybrids.** [Dekker's method](/dekker-method/), [Brent's method](/brent-method/) and [Chandrupatla's method](/chandrupatla-method/) take a fast secant or interpolation step when it is safe, and a bisection step otherwise. They keep the bracket and converge superlinearly at a simple root. The [Newton bisection hybrid](/newton-bisection-hybrid/) does the same with Newton steps.
- **Bisection for polynomials.** With [Sturm sequences](/sturm-sequence/), bisection isolates each real root of a polynomial ([real root isolation](/real-root-isolation/)).
- **Interval bisection.** With [interval arithmetic](/interval-arithmetic/), bisection proves that a box holds no root, as in the [interval Newton method](/interval-newton-method/).

## When to use it

Use bisection when you have a bracket and need a guaranteed result with a known number of evaluations, when $f$ is only continuous, or when $f$ is noisy. Use it as the outer safeguard of a fast method. When $f$ is smooth and evaluations are expensive, use [Brent's method](/brent-method/): it needs about as many evaluations as the secant method near the root and never more than about the square of the bisection count. When $f'$ is cheap and a good starting point is known, Newton's method needs far fewer steps.

## Pitfalls

- **The product test.** The test `f(a) * f(c) > 0` in line L9 can underflow to 0 for small values or overflow to infinity. Compare signs, as line L9 does.
- **The midpoint.** `c ← (a + b)/2` in line L5 can overflow for large $a$ and $b$. Use `c ← a + (b − a)/2`.
- **A loop that never ends.** A stop test `b − a > δ` alone in line L11 loops forever when $\delta$ is smaller than the spacing of the floats near the root. Keep line L6, which stops when the midpoint is an end, and the bound $k_{\max}$ of line L4.
- **A pole is not a root.** For $f(x) = 1/(x - 1/3)$ on $[0, 1]$, the signs at the ends differ, and the method converges to the pole $1/3$. The bracket test needs continuity. Check $|f(\hat x)|$ at the end, or use a method that tracks the size of $f$.
- **A tolerance in $f$.** A stop test $|f(c)| \le \delta$ instead of line L11 does not bound the error in $x$. For the nearly flat $f(x) = (x - 1)^{5}$ the test holds at points far from the root. See [stopping criteria](/stopping-criteria/).
- **No sign change.** Line L3 must reject $f(a) f(b) > 0$. Without it, the method returns a point that is not near any root.

## Implementations

## History

Bisection is the constructive form of the intermediate value theorem, and it is the oldest of the methods on these pages. Dennis and Schnabel (Section 2.5) present it as the safe part of a globally convergent hybrid. Sikorski (1982) proved that no method based on function values has a better worst case over continuous functions.

## References
