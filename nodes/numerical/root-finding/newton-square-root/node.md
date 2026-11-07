---
tag: MBGG7T
kind: algorithm
slug: newton-square-root
name: Newton's method for square root
aliases:
- Heron's method
- Babylonian method
area: numerical/root-finding
level: core
summary: Approximates the square root of a by repeatedly averaging a guess x with a/x. Converges from every positive start, quadratically, with an exact error formula.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {p: the working precision in digits}
  time: {passes: "O(log p)"}
  space: {extra: Θ(1)}
  evaluations: {divisions_per_pass: "1"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: false, local: false}
prereqs: [newton-raphson-method, quadratic-convergence]
see_also: [integer-square-root, newton-integer-root, newton-raphson-division, fast-inverse-square-root, digit-by-digit-square-root, newton-iteration, stopping-criteria, order-of-convergence]
sources:
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 3.5, Square root
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 1, Solution of equations by iteration (Newton's method)
  - paper: "D. Fowler and E. Robson, Square root approximations in Old Babylonian mathematics: YBC 7289 in context, Historia Mathematica 25 (1998) 366-378"
    locator: the Babylonian approximation of the square root of 2
---

Newton's method for the square root computes $\sqrt a$, $a > 0$, by the iteration
$$x_{k+1} = \frac12\Big(x_k + \frac{a}{x_k}\Big),$$
the average of a guess and $a$ divided by the guess. It is [Newton's method](/newton-raphson-method/) applied to $f(x) = x^2 - a$, and it is older than Newton by about two thousand years. Unlike Newton's method in general it converges from every positive start, every iterate after the first is an upper bound, and its error obeys an exact formula: the quantity $(x_k - \sqrt a)/(x_k + \sqrt a)$ is squared in each step. With an exact range reduction and a fixed start, binary64 needs at most a handful of steps.

## In plain words

If a guess $x$ is too big, then $a/x$ is too small, and the other way round, because their product is exactly $a$. The true root lies between them, so their average is a better guess. Repeat. Each step roughly doubles the number of correct digits. To start well for any size of $a$, first pull out a power of four, which changes the root by a power of two and is exact in binary, so that the rest lies between one half and two. Then start from a fixed guess and stop when the guesses stop going down.

## The problem

The input is a floating-point number $a$. The output is a floating-point approximation of $\sqrt a$ when $a \ge 0$, and a flag "invalid" for negative numbers and NaN. In exact arithmetic it is the [root-finding problem](/root-finding-problem/) for $f(x) = x^2 - a$ with the root $x^* = \sqrt a$.

Notation on the root-finding pages: $f$ is the function, $x^*$ the root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has order $q$ and rate $C$ when $|e_{k+1}| \approx C |e_k|^q$. Here we also use $t_k = (x_k - \sqrt a)/(x_k + \sqrt a)$, and $u = 2^{-53}$ is the unit roundoff of binary64.

## The algorithm

```pseudo id=main
NEWTON-SQRT(a, kmax)
L1  if a < 0 or a is NaN then return "invalid"; if a = 0 or a = +∞ then return a
L2  write a = m · 4^e with 1/2 ≤ m < 2 and e an integer (exact)
L3  x ← (1 + m)/2
L4  for k ← 1 to kmax do
L5      y ← (x + m/x)/2
L6      if y ≥ x then return x · 2^e
L7      x ← y
L8  return x · 2^e with the flag "kmax reached"
```

Line L2 splits off an even power of two, so $\sqrt a = \sqrt m \cdot 2^e$ exactly, and the iteration works on $m$ only. Line L3 is the first Newton step from $x_0 = 1$, so $x \ge \sqrt m$ from the start. Line L5 is the Newton step for $x^2 - m$: $x - (x^2 - m)/(2x) = (x + m/x)/2$. Line L6 uses that the exact iterates decrease strictly after the first step: the first computed iterate that fails to decrease shows that rounding has taken over, and the previous one is returned. The computed iterates are strictly decreasing floating-point numbers while the loop runs, so the loop ends even with $k_{\max} = \infty$. Line L8 is reached only when $k_{\max}$ is too small.

## Example

$a = 2$ in binary64. Line L2 gives $m = 1/2$ and $e = 1$, and since multiplying by a power of two is exact, the iterates on $m$ are those for $a = 2$ divided by $2$. The table shows them for $a = 2$, from $x_0 = 1$.

| $k$ | $x_k$ | relative error | $t_k$ |
|---|---|---|---|
| 0 | 1.0 | $2.929 \cdot 10^{-1}$ | $1.716 \cdot 10^{-1}$ |
| 1 | 1.5 | $6.066 \cdot 10^{-2}$ | $2.944 \cdot 10^{-2}$ |
| 2 | 1.4166666666666665 | $1.735 \cdot 10^{-3}$ | $8.666 \cdot 10^{-4}$ |
| 3 | 1.4142156862745097 | $1.502 \cdot 10^{-6}$ | $7.509 \cdot 10^{-7}$ |
| 4 | 1.4142135623746899 | $1.128 \cdot 10^{-12}$ | $5.639 \cdot 10^{-13}$ |
| 5 | 1.414213562373095 | $8.865 \cdot 10^{-17}$ | $4.433 \cdot 10^{-17}$ |

Each $t_k$ is the square of the previous one, $t_0 = (1 - \sqrt2)/(1 + \sqrt2) = -(3 - 2\sqrt2)$ and $t_k = (3 - 2\sqrt 2)^{2^k}$ for $k \ge 1$, until rounding. In pass 5 the computed $y$ equals $x_5$, line L6 returns $1.414213562373095$, and the run used 5 divisions. The correctly rounded value is $1.4142135623730951$, one unit in the last place higher. In exact rational arithmetic the iterates are $3/2, 17/12, 577/408, 665857/470832$; the value $577/408$ already has an error of $2.1 \cdot 10^{-6}$.

## Correctness

All claims are proved in [the correctness proof](proofs/correctness.md), except those marked observed.

- **The exact error formula (proved).** For every $x_k > 0$,
$$x_{k+1} - \sqrt a = \frac{(x_k - \sqrt a)^2}{2 x_k}, \qquad \frac{x_{k+1} - \sqrt a}{x_{k+1} + \sqrt a} = \Big(\frac{x_k - \sqrt a}{x_k + \sqrt a}\Big)^2 .$$
So $t_k = t_0^{2^k}$, with $|t_0| < 1$ for every $x_0 > 0$.
- **Global convergence (proved).** For every $x_0 > 0$, in exact arithmetic: $x_k \ge \sqrt a$ for $k \ge 1$, $(x_k)_{k \ge 1}$ is non-increasing, and $x_k \to \sqrt a$ quadratically, with $e_{k+1}/e_k^2 \to 1/(2\sqrt a)$.
- **Steps from the reduced start (proved).** With $1/2 \le m < 2$ and $x_0 = 1$, $|t_0| \le 3 - 2\sqrt 2 < 0.1716$, so after $k$ steps the relative error is at most $2 \cdot 0.1716^{2^k}/(1 - 0.1716^{2^k})$, which is below $u$ for $k \ge 5$.
- **Termination in floating point (proved).** The loop of lines L4 to L7 ends for every input: while it runs, the computed iterates strictly decrease, and they are positive floating-point numbers.
- **Accuracy in binary64 (observed).** On 200000 random inputs over the whole exponent range the result was within one unit in the last place of $\sqrt a$, correctly rounded for about $75$ percent of them, exact on all of 20000 perfect squares $k^2$ with $k \le 2^{26}$, and the loop used at most 5 passes.

## Complexity

The cost model is the number of divisions.

- **Per pass.** One division, one addition and one halving.
- **Passes.** From the reduced start the error after $k$ steps is about $0.1716^{2^k}$, so $p$ decimal digits need about $\log_2(p / 0.77)$ steps from $x_0 = 1$. In binary64 that is 5 steps: line L3 and 4 passes, plus the pass that detects the stop. The run for $a = 2$ above used 5 passes.
- **Space.** $\Theta(1)$.
- **In high precision.** With multiple-precision numbers it is cheaper to compute $1/\sqrt a$ by the division-free Newton iteration $y \leftarrow y (3 - a y^2)/2$ and to double the working precision in each step; then the whole computation costs a constant times one multiplication at full precision (Brent and Zimmermann, Section 3.5).

### Floating point

Each pass adds a rounding error of a few $u$ relative, and the true root is a fixed point of the exact map but not of the computed one. Near $\sqrt m$ the computed iterates can stall one unit above the root or step one unit below it; once they stop decreasing, line L6 stops. The returned value is then the last decreasing iterate, which is not always the correctly rounded root, as $a = 2$ shows. Hardware square root and `math.sqrt` are correctly rounded by the IEEE 754 standard; a Newton-based implementation needs a final correction step to reach that, for example by checking the sign of $x^2 - a$ with a fused multiply-add and adjusting by one unit.

## Properties

- **Global.** Converges for every positive start, unlike Newton's method for a general $f$.
- **One-sided after one step.** $x_k \ge \sqrt a$ for $k \ge 1$ by the inequality of arithmetic and geometric means, and $a / x_k \le \sqrt a$, so $[a / x_k, x_k]$ is a bracket of shrinking width.
- **Scale invariant.** Replacing $a$ by $4a$ and $x_0$ by $2x_0$ doubles every iterate, which makes the range reduction of line L2 exact.
- **Exact in rational arithmetic.** With rational $a$ and $x_0$ all iterates are rational, and the exact formula gives their errors.

## Variants and improvements

- **Inverse square root.** The iteration $y \leftarrow y(3 - a y^2)/2$ for $1/\sqrt a$ needs no division; $\sqrt a = a \cdot (1/\sqrt a)$. With a bit-level start it is the [fast inverse square root](/fast-inverse-square-root/).
- **Integers.** For integers the iteration with floor division, started above the root, gives $\lfloor \sqrt n \rfloor$ exactly ([integer square root](/integer-square-root/)); for $k$-th roots see [Newton's integer root](/newton-integer-root/).
- **Better starting values.** A linear or table-driven approximation of $\sqrt m$ on $[1/2, 2)$ cuts the number of steps; with a start accurate to 8 digits one step gives 16.
- **Higher order.** Halley's method for $x^2 - a$ gives $x(x^2 + 3a)/(3x^2 + a)$, of order 3, at the cost of more operations per step.
- **Digit by digit.** The [digit-by-digit method](/digit-by-digit-square-root/) produces one correct digit per step, exactly.

## When to use it

Use it to compute square roots in software arithmetic: multiple precision, rational or interval arithmetic, fixed point, or on hardware without a square root instruction. In binary64 on ordinary hardware, use the built-in square root, which is correctly rounded and faster.

## Pitfalls

- **Stopping on $|x_{k+1} - x_k| \le \tau$ with a small $\tau$.** The computed iterates can stall one unit apart, and a tolerance below the unit roundoff never succeeds; the monotone test of line L6 always ends ([stopping criteria](/stopping-criteria/)).
- **No range reduction.** From $x_0 = 1$, $a = 10^{300}$ needs about 500 steps, since while $x_k \gg \sqrt a$ each step only halves $x_k$.
- **Negative input.** For $a < 0$ the real iteration never converges; with $x_0$ real it wanders chaotically. Check the sign first.
- **Starting at $0$.** $a/x_0$ divides by zero.
- **Assuming correct rounding.** The result can be one unit off.

## Implementations

## History

A clay tablet from the Old Babylonian period, YBC 7289, gives $\sqrt 2 \approx 1;24,51,10$ in base 60, that is $1.41421296\ldots$, correct to about six decimal places; it is consistent with the averaging rule, although the method used is not recorded (Fowler and Robson, 1998). Heron of Alexandria describes the averaging rule explicitly in his Metrica (first century AD), which is why it is also called Heron's method. As a special case of Newton's method it was later recognized to converge quadratically.

## References
