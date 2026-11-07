---
tag: GD9DJV
kind: algorithm
slug: dekker-method
name: Dekker's method
aliases:
- Dekker's root-finding method
- Dekker's algorithm
area: numerical/root-finding
level: advanced
summary: Hybrid of bisection and secant; the ancestor of Brent's method. It keeps a bracket, takes secant steps when they fall between the best point and the midpoint, and bisects otherwise.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {w: "the width b - a of the starting bracket", δ: "the tolerance on the error"}
  time: {worst: "O(w/δ)", average: "O(log log(1/δ))"}
  space: {extra: Θ(1)}
  evaluations: {worst: "⌈2w/δ⌉ + 2", step: "1"}
properties: {deterministic: true, recursive: false, bracketing: true, derivative_free: true}
prereqs: [secant-method, bisection-method, bracketing-method]
see_also: [brent-method, illinois-method, inverse-quadratic-interpolation, chandrupatla-method, regula-falsi, ridders-method, order-of-convergence, stopping-criteria]
sources:
  - paper: "T. J. Dekker, Finding a zero by means of successive linear interpolation, in B. Dejon and P. Henrici (eds.), Constructive Aspects of the Fundamental Theorem of Algebra, Wiley-Interscience, London, 1969"
    locator: the algorithm that combines linear interpolation with bisection inside a bracket, with the minimum step size
  - book: isbn:9780486419985
    title: Richard P. Brent, Algorithms for Minimization without Derivatives, Prentice-Hall, 1973 (Dover reprint, 2002)
    locator: Chapter 4, An Algorithm with Guaranteed Convergence for Finding a Zero of a Function (Dekker's algorithm, its slow cases and the bound of the modified algorithm)
  - paper: doi:10.1093/comjnl/14.4.422
    title: Richard P. Brent, An algorithm with guaranteed convergence for finding a zero of a function, The Computer Journal 14(4), 422-425, 1971
    locator: the description of Dekker's algorithm and the example where it needs far more evaluations than bisection
  - paper: "J. C. P. Bus and T. J. Dekker, Two efficient algorithms with guaranteed convergence for finding a zero of a function, ACM Transactions on Mathematical Software 1(4), 330-345, 1975"
    locator: the later algorithms of Dekker's school with a bound on the number of evaluations
---

Dekker's method finds a root of a continuous function $f$ in a bracket $[a, b]$ with $f(a)f(b) < 0$. It keeps the best point $b$, with $|f(b)| \le |f(a)|$, and the contrapoint $a$, with a root between them. In each step it takes the [secant](/secant-method/) point through $b$ and the previous best point if that point lies between $b$ and the midpoint of the bracket, and the midpoint ([bisection](/bisection-method/)) otherwise. Near a simple root it is as fast as the secant method, with order 1.618, and it can never leave the bracket. Its weak point is that it can creep: in bad cases it takes steps of the minimum size, and the number of evaluations grows like $w/\delta$ instead of $\log(w/\delta)$. [Brent's method](/brent-method/) adds a test that repairs this.

## In plain words

You know that the answer lies between two numbers. Keep the one where the function is closer to zero as your best guess. From the best guess and the guess before it, draw a straight line and see where it crosses zero. If that crossing lies between your best guess and the middle of the interval, use it. If not, use the middle. Then keep the interval that still holds the answer. When the line works well, this is very fast. When the line gives only tiny steps, it can be much slower than always taking the middle.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Given a continuous $f$ on $[a, b]$ with $f(a)f(b) < 0$ and a tolerance $\delta \ge 0$, find $x$ with $|x - x^*| \le \delta + 8u|x|$ for a root $x^*$ in $[a, b]$, where $u = 2^{-53}$ is the unit roundoff of binary64. The term $8u|x|$ makes the test reachable for every $\delta$, including $\delta = 0$ (see [stopping criteria](/stopping-criteria/)).

## The algorithm

The variables are the best point $b$, the contrapoint $a$ and the previous best point $p$. The step size floor is $t = 4u|b| + \delta/2$.

```pseudo id=main
DEKKER(f, a, b, delta, kmax):                // f(a) f(b) < 0
L1   fa <- f(a);  fb <- f(b);  p <- a;  fp <- fa
L2   for k = 1, 2, ..., kmax:
L3       if |fa| < |fb| then p <- b;  swap (a, fa) and (b, fb)
L4       m <- (a + b)/2;  t <- 4u|b| + delta/2;  if |m - b| <= t then return b
L5       if fb != fp then s <- b - fb (b - p)/(fb - fp) else s <- m
L6       if s is not strictly between b and m then s <- m
L7       if |s - b| < t then s <- b + t sign(m - b)
L8       p <- b;  fp <- fb;  b <- s;  fb <- f(s)      // return b if fb = 0
L9       if fa and fb have the same sign then a <- p;  fa <- fp
     return b                                        // kmax reached: not converged
```

Line L1 evaluates the ends (an end with $f = 0$ is returned). Line L3 makes $b$ the point with the smaller $|f|$; after a swap the previous point is the old $b$, so the next secant step is a [regula falsi](/regula-falsi/) step through the two ends. Line L4 stops when the bracket has width at most $2t$. Line L5 is the secant step through $b$ and $p$, and line L6 rejects it when it does not fall between $b$ and the midpoint. Line L7 enforces a minimum step of size $t$ toward the midpoint, so that each step makes progress. Line L8 evaluates $f$ at the new point, and line L9 keeps the contrapoint on the other side of the root: if $f(b)$ now has the sign of $f(a)$, the old best point becomes the contrapoint.

## Example

Take $f(x) = x^3 - x - 2$ on $[1, 2]$ with $\delta = 10^{-12}$; the root is $x^* = 1.5213797068$. Line L3 swaps first, so $b = 2$ and the first step is regula falsi.

| $k$ | step | $x_k$ | $\lvert e_k \rvert$ | $\log\lvert e_k\rvert / \log\lvert e_{k-1}\rvert$ |
|---|---|---|---|---|
| 1 | secant | 1.333333333333 | $1.88 \times 10^{-1}$ | |
| 2 | secant | 1.642857142857 | $1.21 \times 10^{-1}$ | |
| 3 | secant | 1.503250975293 | $1.81 \times 10^{-2}$ | |
| 4 | secant | 1.519780718147 | $1.60 \times 10^{-3}$ | 1.605 |
| 5 | secant | 1.521402209247 | $2.25 \times 10^{-5}$ | 1.659 |
| 6 | secant | 1.521379679151 | $2.77 \times 10^{-8}$ | 1.627 |
| 7 | secant | 1.521379706804 | $4.78 \times 10^{-13}$ | 1.632 |
| 8 | minimum step | 1.521379706805 | $2.29 \times 10^{-14}$ | |

The log ratios are close to the secant order $1.618$. Step 8 is a minimum step of size $t$ past the last point; it lands on the other side of the root, the bracket shrinks to width $5 \times 10^{-13}$, and line L4 stops. In all, 8 steps and 10 evaluations; [bisection](/bisection-method/) needs 42. On $\cos x - x$ on $[0, 1]$ and $e^x - 2$ on $[0, 1]$ Dekker's method needs 8 and 9 evaluations, and on $x^{10} - 1$ on $[0, 1.3]$ it needs 10, with two bisection steps.

## Correctness

The invariant at line L4 is: $f(a)$ and $f(b)$ are nonzero with opposite signs, $|f(b)| \le |f(a)|$, and $a, b$ lie in the starting interval. So a root lies strictly between $a$ and $b$, and the return at L4 has error less than $|a - b| \le 2t = \delta + 8u|b|$. Each step either halves the width or cuts it by at least $t \ge \delta/2$, which proves termination within $\lceil 2w/\delta \rceil$ steps for $\delta > 0$. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs one evaluation of $f$ and a few operations; the start costs two, and the space is $\Theta(1)$.

- **Worst case.** At most $\lceil 2w/\delta \rceil$ steps for $\delta > 0$ (proved). This bound is linear in $w/\delta$, not logarithmic, and it is nearly reached: on $f(x) = x^9$ on $[-1, 1.1]$ with $\delta = 10^{-12}$, the method takes 319 steps, 306 of them secant steps that creep toward the root of multiplicity 9; bisection needs about 42. On $(x - 0.3)^{19}$ on $[0, 1]$ it takes 702 steps.
- **Near a simple root.** Once $b$ and $p$ are close to a simple root of a $C^2$ function, the secant point lies between $b$ and the midpoint, the steps are secant steps, and the order is $1.618$ with one evaluation in each step, so the efficiency index is $1.618$. This is local; it is observed in the example.
- **Multiple roots.** At a root of multiplicity $m > 1$, secant steps converge linearly, and the method can be slower than bisection, as in the cases above.

## Properties

- **Bracketing.** A root stays between $a$ and $b$ at every step, for every continuous $f$.
- **Derivative free.** Only values of $f$, and their signs, are used.
- **No logarithmic bound.** The guaranteed bound is $O(w/\delta)$ steps. Bisection has $\lceil \log_2(w/\delta) \rceil$.
- **Superlinear near a simple root.** It inherits the order 1.618 of the secant method.

## Variants and improvements

- **[Brent's method](/brent-method/).** Brent (1971, 1973) adds [inverse quadratic interpolation](/inverse-quadratic-interpolation/) and, more important, a test that forces a bisection when the interpolation steps do not shrink the bracket fast enough. That gives a bound of about $(\log_2(w/\delta))^2$ evaluations.
- **Bus and Dekker (1975).** Two algorithms of the same kind, with a bound on the number of evaluations that is a small multiple of the bisection count $\log_2(w/\delta)$.
- **Illinois-type ends.** The [Illinois method](/illinois-method/) keeps a bracket by changing the stored values instead of testing the step.
- **[Chandrupatla's method](/chandrupatla-method/).** It uses inverse quadratic interpolation under a simpler acceptance test.

## When to use it

Dekker's method is mainly of historical and teaching interest: it shows the idea of a safeguarded secant step in a few lines. In practice use [Brent's method](/brent-method/), which is as fast on smooth functions and has a much better worst case, or [bisection](/bisection-method/) when a fixed, small worst case matters more than speed.

## Pitfalls

- **Creeping steps (L7).** When the secant steps are accepted but short, the method takes many steps of size about $t$. The test of L6 checks only that the step stays inside, not that the bracket shrinks fast. The $x^9$ example takes 319 steps. Brent's extra test is the fix.
- **No minimum step (L7).** Without L7, a step can be so short that the bracket does not shrink at all in floating point, and the method can loop until $k_{\max}$.
- **No swap (L3).** Without L3, the best point can be the one with the larger $|f|$, the secant step starts from the worse point, and the stopping test of L4 returns the worse end.
- **A tolerance without the relative term (L4).** With $t = \delta/2$ and $\delta = 0$, the test $|m - b| \le t$ is never true once $a$ and $b$ are neighbor floating point numbers, and the loop runs to $k_{\max}$.
- **A pole in the bracket.** For $1/(x - 1/3)$ on $[0, 1]$ the signs differ but there is no root; the method returns a point next to the pole. Check $|f(b)|$ at the end.

## Implementations

## History

The method comes from the Mathematical Centre in Amsterdam, where van Wijngaarden, Zonneveld and Dijkstra worked on such combinations in the 1960s. Dekker published it in 1969 as a combination of linear interpolation and bisection with a minimum step. Brent (1971) noticed that it can need far more evaluations than bisection and added inverse quadratic interpolation and a test on the progress, giving the method now called Brent's method. Bus and Dekker (1975) gave two more algorithms with better bounds.

## References
