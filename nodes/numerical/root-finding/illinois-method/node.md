---
tag: C2H8P5
kind: algorithm
slug: illinois-method
name: Illinois method
aliases:
- modified regula falsi
- Illinois algorithm
area: numerical/root-finding
level: advanced
summary: Regula falsi variant that halves stagnant function values to restore superlinear speed. It keeps a bracket and has order 3^(1/3) ≈ 1.442 in each evaluation at a simple root.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {δ: "the tolerance on the width of the bracket", K: "the cap on the number of steps"}
  time: {worst: "Θ(K)", average: "O(log log(1/δ))"}
  space: {extra: Θ(1)}
  evaluations: {worst: "K + 2", step: "1"}
properties: {deterministic: true, recursive: false, bracketing: true, derivative_free: true}
prereqs: [regula-falsi, bracketing-method, secant-method]
see_also: [bisection-method, dekker-method, brent-method, ridders-method, chandrupatla-method, order-of-convergence, stopping-criteria, inverse-quadratic-interpolation]
sources:
  - paper: "M. Dowell and P. Jarratt, A modified regula falsi method for computing the root of an equation, BIT Numerical Mathematics 11, 168-174, 1971"
    locator: the Illinois modification, its error equation and the proof that its order is 3^(1/3) ≈ 1.442
  - book: isbn:9780486419985
    title: Richard P. Brent, Algorithms for Minimization without Derivatives, Prentice-Hall, 1973 (Dover reprint, 2002)
    locator: Chapter 4, An Algorithm with Guaranteed Convergence for Finding a Zero of a Function (the slow convergence of regula falsi that the modified methods repair)
  - book: "Germund Dahlquist and Åke Björck, Numerical Methods in Scientific Computing, Volume I, SIAM, 2008"
    locator: Chapter 6, Solving Scalar Nonlinear Equations, the section on the false position method and its Illinois modification
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 2.5, the bracketing hybrids and their stopping rules
---

The Illinois method finds a root of a continuous function $f$ in a bracket $[a, b]$ with $f(a)f(b) < 0$. Like [regula falsi](/regula-falsi/) it takes the zero of the line through the two end points as the next point, and it keeps the root inside the bracket. Regula falsi often keeps one end fixed for ever, which makes it converge only linearly. The Illinois method halves the function value at the end that stays, so the next line crosses zero on the far side. This simple change gives order $3^{1/3} \approx 1.442$ in each [evaluation](/order-of-convergence/) at a simple root, close to the [secant method](/secant-method/), and keeps the safety of a [bracket](/bracketing-method/).

## In plain words

You know that the answer lies between two numbers, because the function has different signs there. Draw a straight line between the two points of the graph and see where it crosses the axis. That crossing is your next guess, and it replaces the end with the same sign, so the answer stays between your two numbers. With a curved graph, one end often never moves, and the guesses creep along slowly. The fix is to pretend that the end which did not move has a value only half as large. The line then tilts, the next guess jumps past the answer, and the stuck end moves at last.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Given a continuous $f$ on $[a, b]$ with $f(a)f(b) < 0$ and a tolerance $\delta \ge 0$, find $x$ with $|x - x^*| \le \delta$ for some root $x^*$ in $[a, b]$. The method needs no derivative. Its stopping rule is the width of the bracket, which bounds the error; it is safe for every continuous $f$, while a test on $|f(x)|$ or on the step size is not (see [stopping criteria](/stopping-criteria/)).

## The algorithm

The variable $b$ always holds the newest point and $a$ the other end of the bracket, so $f(a)$ and $f(b)$ have opposite signs. The value $f_a$ is the stored value at $a$, which may have been halved.

```pseudo id=main
ILLINOIS(f, a, b, delta, kmax):              // f(a) f(b) < 0
L1   fa <- f(a);  fb <- f(b)
L2   for k = 1, 2, ..., kmax:
L3       if |b - a| <= max(delta, 4 ulp) then return b
L4       x <- b - fb (b - a)/(fb - fa)       // bisect if x is not strictly inside
L5       fx <- f(x)
L6       if fx = 0 then return x
L7       if fx and fb have opposite signs then
L8           a <- b;  fa <- fb               // the old newest point becomes the far end
L9       else  fa <- fa / 2                  // the far end stays: halve its value
L10      b <- x;  fb <- fx
     return b                                 // kmax reached: not converged
```

Line L1 evaluates $f$ at both ends (an end with $f = 0$ is returned at once). Line L3 is the stopping rule: the root lies between $a$ and $b$, so $b$ is within $|b - a|$ of it; the floor of 4 units in the last place keeps the test reachable when $\delta$ is below the spacing of floating point numbers. Line L4 is the regula falsi point of the stored values; if rounding puts it on or outside an end, the midpoint is used instead. Lines L7 and L8 are the ordinary update when the sign changes between $b$ and $x$. Line L9 is the Illinois change: when $x$ has the sign of $b$, the end $a$ stays, and its stored value is halved. Line L10 makes $x$ the newest point.

## Example

Take $f(x) = x^3 - x - 2$ on $[1, 2]$, with root $x^* = 1.5213797068$. The table gives each new point, its value, the action of lines L7 to L9, the bracket after the step, the stored $f_a$ and the error.

| $k$ | $x_k$ | $f(x_k)$ | action | bracket | stored $f_a$ | $\lvert e_k \rvert$ |
|---|---|---|---|---|---|---|
| 1 | 1.3333333333 | $-9.630 \times 10^{-1}$ | swap | [1.3333333333, 2] | 4 | $1.88 \times 10^{-1}$ |
| 2 | 1.4626865672 | $-3.333 \times 10^{-1}$ | halve | [1.4626865672, 2] | 2 | $5.87 \times 10^{-2}$ |
| 3 | 1.5394467228 | $1.089 \times 10^{-1}$ | swap | [1.4626865672, 1.5394467228] | $-0.3333$ | $1.81 \times 10^{-2}$ |
| 4 | 1.5205470884 | $-4.946 \times 10^{-3}$ | swap | [1.5205470884, 1.5394467228] | 0.1089 | $8.33 \times 10^{-4}$ |
| 5 | 1.5213682640 | $-6.801 \times 10^{-5}$ | halve | [1.5213682640, 1.5394467228] | 0.05444 | $1.14 \times 10^{-5}$ |
| 6 | 1.5213908211 | $6.606 \times 10^{-5}$ | swap | [1.5213682640, 1.5213908211] | $-6.801 \times 10^{-5}$ | $1.11 \times 10^{-5}$ |
| 7 | 1.5213797067 | $-5.805 \times 10^{-10}$ | swap | [1.5213797067, 1.5213908211] | $6.606 \times 10^{-5}$ | $9.77 \times 10^{-11}$ |
| 8 | 1.5213797068 | $-5.107 \times 10^{-15}$ | halve | [1.5213797068, 1.5213908211] | $3.303 \times 10^{-5}$ | $8.88 \times 10^{-16}$ |

Step 6 shows the effect of the halving: after step 5 the end 1.5394 would have stayed, but with its value halved the line crosses zero just past the root, at the same distance on the other side, and the bracket shrinks from $1.8 \times 10^{-2}$ to $2.3 \times 10^{-5}$. Steps 7 and 8 are then secant steps between points on both sides. With $\delta = 10^{-6}$ the method stops after 9 steps and 11 evaluations; [bisection](/bisection-method/) needs 21 evaluations. On the harder $x^{10} - 1$ on $[0, 1.3]$, where regula falsi needs 95 steps to reach a bracket of width $10^{-10}$, the Illinois method needs 15 steps and 17 evaluations.

## Correctness

The invariant at line L3 is: $a$ and $b$ are points of the original interval, $f(a)$ and $f(b)$ have opposite signs and are not zero, and the stored $f_a$ has the sign of $f(a)$. So by the intermediate value theorem a root lies between $a$ and $b$, and the return at L3 has error at most $\max(\delta, 4\,\mathrm{ulp})$. The loop runs at most $k_{\max}$ times. The proof, and the local analysis of the order, are in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs one evaluation of $f$ (line L5) and a few arithmetic operations, and the method stores $\Theta(1)$ numbers. The start costs two evaluations.

Near a simple root $x^*$ with $f''(x^*) \ne 0$, the steps settle into a cycle of three: a halving step that puts the new point on the other side of the root at about the same distance, and two secant steps between points on both sides. In logarithms, $\log|e|$ stays the same in the halving step and follows $\ell_{k+1} = \ell_k + \ell_{k-1}$ in the secant steps, so it is multiplied by 3 in each cycle: $|e_{k+3}| \approx K|e_k|^3$. The order in each evaluation is $3^{1/3} \approx 1.442$ (proved by Dowell and Jarratt, 1971; derived to first order in the proof file). In the example, $\log|e_{k+3}|/\log|e_k|$ is 3.25 from $k = 4$; for $\cos x - x$ on $[0, 1]$ the observed values are 3.56 and 3.48, and for $e^x - 2$ on $[0, 1]$ it is 3.20.

| method | evaluations in each step | order | efficiency index |
|---|---|---|---|
| [bisection](/bisection-method/) | 1 | 1 (rate 1/2) | 1 |
| regula falsi | 1 | 1 (often slow) | 1 |
| Illinois | 1 | $3^{1/3}$ in each step | 1.442 |
| [secant](/secant-method/) | 1 | 1.618 | 1.618 |
| [Newton](/newton-raphson-method/) | 2 | 2 | 1.414 |

Far from the root nothing better than termination after $k_{\max}$ steps is proved: the halving can be repeated many times on one end before it moves, as at the start of $x^{10} - 1$.

## Properties

- **Bracketing.** The root stays inside $[a, b]$ in every step, and the stop at L3 bounds the error by the width.
- **Derivative free.** It needs only values of $f$, and only their signs for the decisions.
- **Order $3^{1/3}$ at a simple root.** This is a local result for $f \in C^2$ with $f'(x^*) \ne 0$ and $f''(x^*) \ne 0$. At a root of [multiplicity](/multiplicity-of-roots/) $m > 1$ the convergence is linear.
- **One extra operation over regula falsi.** The halving is one division by 2, exact in binary floating point.

## Variants and improvements

- **Pegasus method.** Instead of halving, multiply $f_a$ by $f_b/(f_b + f_x)$. Dowell and Jarratt (1972) gave it order about 1.642 in each evaluation.
- **Anderson-Björck method.** Multiply by $1 - f_x/f_b$, or by $1/2$ if that is not positive. It is often faster still in practice.
- **Halving only after two stays.** Some versions apply the factor only when the same end has stayed twice in a row; the asymptotic cycle is the same.
- **Hybrids.** [Dekker's method](/dekker-method/) and [Brent's method](/brent-method/) use secant and [inverse quadratic interpolation](/inverse-quadratic-interpolation/) steps with bisection as a guard, and guarantee a bound on the number of evaluations. [Ridders' method](/ridders-method/) and [Chandrupatla's method](/chandrupatla-method/) are other bracketing choices.

## When to use it

Use it when a bracket is known, the function is cheap to code but has no usable derivative, and a short, robust method is wanted: a few lines more than regula falsi, with near-secant speed. When a guaranteed bound on the number of evaluations matters, use [Brent's method](/brent-method/) or plain [bisection](/bisection-method/); the Illinois method has no such bound far from the root. When $f'$ is cheap and a good start is known, [Newton's method](/newton-raphson-method/) is faster.

## Pitfalls

- **Halving the wrong value (L9).** The value to halve is $f_a$, at the end that stays. Halving $f_b$, the value at the newest point, does not tilt the line, and on $x^{10} - 1$ on $[0, 1.3]$ the bracket after 30 steps is still $[0.9966, 1.3]$, as slow as regula falsi.
- **Halving after a swap (L8).** After a swap, $f_a$ is a fresh value and must not be halved, or the line tilts the wrong way.
- **Stopping on $|f(x)|$ or on the step.** A test $|f(x_k)| \le \varepsilon$ in place of L3 says nothing about the error when $f$ is flat or steep. The bracket width is the honest test.
- **A tolerance below the spacing of floating point numbers (L3).** Without the floor of 4 ulps, with $\delta = 0$ and a bracket of two neighbor floating point numbers, line L4 can only give an end, and the loop runs to $k_{\max}$.
- **No sign change.** If $f(a)$ and $f(b)$ have the same sign, line L1 has no bracket, and the method must stop with an error rather than iterate.
- **A pole in the bracket.** For $f(x) = 1/(x - 1/3)$ on $[0, 1]$ the signs differ, but there is no root; the bracket shrinks to the pole. A check of $|f(b)|$ at the end shows it.

## Implementations

## History

The method was in use in the 1950s at the computing laboratory of the University of Illinois, which gave it its name. Dowell and Jarratt (1971) analyzed it, derived its error equation and proved the order $3^{1/3}$, and in 1972 they analyzed the Pegasus variant. Anderson and Björck (1973) gave a further variant. Brent (1973, Chapter 4) took a different path, with bisection as a guard, which led to [Brent's method](/brent-method/).

## References
