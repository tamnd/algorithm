---
tag: WGGEP1
kind: algorithm
slug: chandrupatla-method
name: Chandrupatla's method
aliases:
- Chandrupatla's algorithm
- Chandrupatla's hybrid quadratic/bisection method
area: numerical/root-finding
level: research
summary: Bracketing method that takes an inverse quadratic interpolation step only when a two-ratio test shows the interpolant is monotone, and bisects otherwise.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {w: "the width of the starting bracket", δ: "the tolerance on the error", K: "the cap on the number of steps"}
  time: {worst: "O(min(K, w/δ))", average: "O(log log(1/δ))"}
  space: {extra: Θ(1)}
  evaluations: {worst: "min(K, ⌈2w/δ⌉) + 2", step: "1"}
properties: {deterministic: true, recursive: false, bracketing: true, derivative_free: true}
prereqs: [inverse-quadratic-interpolation, bisection-method, bracketing-method]
see_also: [brent-method, dekker-method, illinois-method, ridders-method, regula-falsi, secant-method, order-of-convergence, stopping-criteria]
sources:
  - paper: doi:10.1016/S0965-9978(96)00051-8
    title: Tirupathi R. Chandrupatla, A new hybrid quadratic/bisection algorithm for finding the zero of a nonlinear function without using derivatives, Advances in Engineering Software 28(3), 145-149, 1997
    locator: the algorithm, the two-ratio test for the quadratic step, and the comparison with Brent's method
  - book: isbn:9780486419985
    title: Richard P. Brent, Algorithms for Minimization without Derivatives, Prentice-Hall, 1973 (Dover reprint, 2002)
    locator: Chapter 3 (the order of inverse quadratic interpolation) and Chapter 4 (the zero finder that Chandrupatla compares against)
  - book: isbn:9780898713640
    title: J. E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics, 1996
    locator: Section 2.5, Methods when derivatives are unavailable
---

Chandrupatla's method finds a root of a continuous function $f$ in a bracket with a sign change. In each step it fits the inverse quadratic through the three newest points and asks a cheap question: is that interpolant monotone over the range of the three values? If yes, it takes the [inverse quadratic interpolation](/inverse-quadratic-interpolation/) point, which then lies strictly inside the bracket. If no, it [bisects](/bisection-method/). The test uses only two ratios, $\xi$ of positions and $\Phi$ of values. The method is shorter than [Brent's method](/brent-method/), converges with the order of inverse quadratic interpolation near a simple root, and in practice needs fewer evaluations than Brent on roots of high multiplicity. Its proved worst case is weaker than Brent's.

## In plain words

You hold two points where the function has opposite signs, so a root lies between them. You also remember one older point. Through these three points you can draw a smooth curve that predicts where the function crosses zero. The prediction is only trusted when the curve is well behaved, meaning it rises or falls steadily through all three points. A simple test on two ratios decides this. A trusted guess replaces one end of the interval. An untrusted guess is replaced by the middle of the interval. Either way the root stays trapped, and the interval keeps shrinking until it is as small as you asked.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Input: a continuous $f$ on the interval between $x_0$ and $x_1$ with $f(x_0) f(x_1) \le 0$, a tolerance $\delta \ge 0$ and a cap $K$ on the steps. Output: a point $x$ and a bracket $[a, b]$ that contains $x$ and a root. On convergence $|x - x^*| \le \delta + 8u|x|$ for some root $x^*$, where $u = 2^{-53}$ is the unit roundoff. This is the [bracketing](/bracketing-method/) contract: it needs no derivative and no smoothness, and it is kept even when the fast steps fail. The [stopping rule](/stopping-criteria/) is on the width of the bracket, so it cannot be fooled by a small residual.

## The algorithm

The method keeps three points. $a$ is the newest point, $b$ is the point with the opposite sign of $f$, and $c$ is the previous point, which has the sign of $f(a)$ and lies beyond $a$ as seen from $b$. The next point is $a + t(b - a)$ for a fraction $t \in (0, 1)$.

```pseudo id=main
CHANDRUPATLA(f, x0, x1, delta, K):                    // f(x0) f(x1) <= 0
L1   b <- x0;  a <- x1;  c <- a;  t <- 1/2;  return at once if f(a) or f(b) is 0
L2   for k = 1, 2, ..., K:
L3       xm <- the one of a, b with smaller |f|;  tl <- (4u|xm| + delta/2)/|b - a|;  if f(xm) = 0 or tl >= 1/2 then return xm
L4       t <- min(1 - tl, max(tl, t))                                  // keep the point off the ends
L5       x <- a + t(b - a);  fx <- f(x)
L6       if fx has the sign of fa then c <- a  else c <- b;  b <- a     // keep the sign change in [a, b]
L7       a <- x;  fa <- fx
L8       xi <- (a - b)/(c - b);  phi <- (fa - fb)/(fc - fb)
L9       if phi^2 < xi and (1 - phi)^2 < 1 - xi then t <- fa/(fb - fa) * fc/(fb - fc) + (c - a)/(b - a) * fa/(fc - fa) * fb/(fc - fb)
L10      else t <- 1/2                                                  // bisect
L11  return a                                                           // K reached, not converged
```

Line L1 makes the first step a bisection. Line L3 returns the better end once the bracket is no wider than $2(4u|x_m| + \delta/2) = \delta + 8u|x_m|$. Line L4 clamps the fraction so the new point is at least $4u|x_m| + \delta/2$ from both ends; this is what makes every step shrink the bracket by a fixed amount. Line L6 keeps a sign change between $a$ and $b$, and sends the end that leaves the bracket to $c$, so $f(c)$ always has the sign of the new $f(a)$. Line L8 computes the two ratios: $\xi$ is where $a$ sits on the segment from $b$ to $c$, and $\Phi$ is where $f(a)$ sits on the segment from $f(b)$ to $f(c)$. Line L9 is the acceptance test. When it holds, $t$ is the inverse quadratic point written as a fraction of $b - a$: it is the Lagrange form of the quadratic $x(y)$ through $(f_a, a)$, $(f_b, b)$, $(f_c, c)$ at $y = 0$, after subtracting $a$ and dividing by $b - a$.

## Example

Take $f(x) = x^3 - x - 2$ on $x_0 = 1$, $x_1 = 2$ with $\delta = 10^{-12}$. The root is $x^* = 1.5213797068045676$.

| step | rule | $t$ | $x$ | $f(x)$ | $\lvert e \rvert$ | $\xi$ | $\Phi$ | accept |
|---|---|---|---|---|---|---|---|---|
| 1 | bisect | 0.5 | 1.500000000000 | $-1.25 \times 10^{-1}$ | $2.1 \times 10^{-2}$ | 0.5000 | 0.6875 | yes |
| 2 | IQI | 0.054545 | 1.527272727273 | $3.52 \times 10^{-2}$ | $5.9 \times 10^{-3}$ | 0.0545 | 0.0388 | yes |
| 3 | IQI | 0.217660 | 1.521336540179 | $-2.57 \times 10^{-4}$ | $4.3 \times 10^{-5}$ | 0.2177 | 0.2213 | yes |
| 4 | IQI | 0.007273 | 1.521379712375 | $3.31 \times 10^{-8}$ | $5.6 \times 10^{-9}$ | 0.0073 | 0.0072 | yes |
| 5 | IQI | 0.000129 | 1.521379706805 | $-7.77 \times 10^{-15}$ | $1.3 \times 10^{-15}$ | 0.0001 | 0.0001 | yes |
| 6 | clamp | 0.000090 | 1.521379706805 | $2.97 \times 10^{-12}$ | $5.0 \times 10^{-13}$ | 0.0001 | 0.0001 | yes |

In step 1 the test reads $\Phi^2 = 0.473 < 0.5 = \xi$ and $(1 - \Phi)^2 = 0.098 < 0.5 = 1 - \xi$, so step 2 is an IQI step. The errors of steps 2 to 5 give $\log|e_{k+1}| / \log|e_k|$ of 1.96, 1.89 and 1.80, close to the IQI order 1.839. At step 6 the IQI fraction was below $t_l$, so L4 clamped it and the point landed $5 \times 10^{-13}$ on the far side of the root; the bracket then has width $5 \times 10^{-13} < \delta$ and L3 returns at the start of step 7. In total: 6 steps, 8 evaluations, final error $1.3 \times 10^{-15}$. Bisection needs 42 evaluations for the same $\delta$, Brent's method 9.

## Correctness

The invariant at line L3 is: $a$ and $b$ lie in the starting interval, and $f(a)$ and $f(b)$ are nonzero with opposite signs. So a root lies between $a$ and $b$, and a return at L3 has error at most $|b - a| \le \delta + 8u|x_m|$. The clamp of L4 puts every new point strictly inside, at distance at least $4u|x_m| + \delta/2$ from both ends, so each step cuts the width by at least $\delta/2$ and the loop ends after at most $\lceil 2w/\delta \rceil$ steps when $\delta > 0$. The test of L9 holds exactly when the inverse quadratic through the three points is strictly increasing or strictly decreasing over the whole range of values from $f(b)$ to $f(c)$; this forces the IQI point strictly between $a$ and $b$. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs one evaluation of $f$ and $O(1)$ arithmetic, plus two evaluations at the start. The proved bound is $\min(K, \lceil 2w/\delta \rceil) + 2$ evaluations, much weaker than the $O(k^2)$ of Brent's method with $k = \lceil \log_2(w/\delta) \rceil$: no rule forces a bisection after a run of small IQI steps. Near a simple root of a $C^3$ function, once the test accepts every step, the iteration is inverse quadratic interpolation and has order $q \approx 1.839$, the real root of $q^3 = q^2 + q + 1$, with efficiency index $1.839$ (one evaluation per step). That the test keeps accepting near a simple root is observed, not proved here.

Observed evaluation counts with $\delta = 10^{-12}$, against [Brent's method](/brent-method/) as implemented on that page and the 42 or so of bisection:

| function | bracket | Chandrupatla | Brent |
|---|---|---|---|
| $x^3 - x - 2$ | $[1, 2]$ | 8 | 9 |
| $\cos x - x$ | $[0, 1]$ | 8 | 8 |
| $e^x - 2$ | $[0, 1]$ | 8 | 8 |
| $x^{10} - 1$ | $[0, 1.3]$ | 11 | 10 |
| $x^9$ | $[-1, 1.1]$ | 49 | 113 |
| $(x - 1)^3$ | $[0, 3.3]$ | 44 | 108 |
| $(x - 0.3)^{19}$ | $[0, 1]$ | 42 | 117 |
| step at 0.3 | $[0, 1]$ | 42 | 42 |
| $1/(x - 1/3)$ | $[0, 1]$ | 42 | 44 |

On 600 random cubics with three simple real roots in $[-10, 10]$ and a bracket around one root, with $\delta = 10^{-10}$, the mean count was 10.5 for Chandrupatla, 12.1 for Brent and 38.3 for bisection; the largest count for Chandrupatla was 17. On multiple roots the test rejects most IQI points, so the method falls back to near-bisection speed, while Brent spends many evaluations on tiny steps first.

## Properties

- Bracketing: a sign change is kept in $[a, b]$ at every step, so the method cannot diverge.
- Derivative-free, one evaluation of $f$ per step.
- Local order about 1.839 near a simple root (observed with the test always accepting), close to bisection speed on multiple roots, where the test rejects most IQI points (observed).
- The IQI point, when accepted, is strictly inside the bracket (proved), so no separate "is it inside" test is needed.
- Deterministic and iterative, with $O(1)$ extra space.

## Variants and improvements

- Brent's method uses the same three points but accepts the interpolation step by a step-length test, and falls back to the secant step when two points coincide. It has the stronger worst-case bound.
- The [Illinois method](/illinois-method/) and [Ridders' method](/ridders-method/) are other bracketing methods with superlinear local speed.
- Alefeld, Potra and Shi's enclosing methods (TOMS 748) use cubic inverse interpolation and double-length secant steps to raise the asymptotic efficiency, with a guarantee that the bracket shrinks.
- Vectorised versions run the same test on many brackets at once, since the method has a single branch per step.

## When to use it

Use it when you have a bracket, want a short code with no derivative, and may meet multiple or nearly multiple roots, where it beats Brent in the table above. Prefer [Brent's method](/brent-method/) when you need a proved $O(k^2)$ worst case. Prefer [bisection](/bisection-method/) when the evaluation count must be predictable to the step. Prefer [Newton's method](/newton-raphson-method/) when $f'$ is cheap and a good start is known.

## Pitfalls

- L1: no sign change. The method needs $f(x_0) f(x_1) \le 0$. The implementation raises an error otherwise.
- L3 with $\delta = 0$: the stopping floor is $4u|x_m|$, which is 0 when the root is at 0. The bracket then shrinks into the subnormals, which still terminates; with $f(x) = x^3$ on $[-1, 1.1]$ it took 416 steps and stopped at $5 \times 10^{-109}$. Give a positive $\delta$ when roots near 0 are possible.
- L4: without the clamp an accepted IQI point can fall within one rounding of an end. The bracket then shrinks by almost nothing and the proved step bound is lost.
- L5 with NaN or infinite values: the sign tests of L6 are meaningless then. The implementation raises on any non-finite value.
- L8 when $f(c) = f(b)$: the ratio $\Phi$ divides by $f(c) - f(b)$. This cannot happen while the invariant holds, since $f(c)$ has the sign of $f(a)$, opposite to $f(b)$.
- L9 on a discontinuous $f$: the method still converges to a sign change, such as a jump or a pole, like any bracketing method; it does not tell you whether it found a root.

## Implementations

## History

Tirupathi R. Chandrupatla published the method in 1997 in Advances in Engineering Software as a "hybrid quadratic/bisection algorithm". His aim was a simpler alternative to Brent's 1973 procedure: he replaced Brent's step-length tests by a single condition on the two ratios $\xi$ and $\Phi$, derived from asking when the quadratic through the three points is monotone. The method later found use in vectorised scalar root finders, where its single branch per step suits array code.

## References
