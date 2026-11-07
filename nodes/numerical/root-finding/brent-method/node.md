---
tag: E222GS
kind: algorithm
slug: brent-method
name: Brent's method
aliases:
- Brent-Dekker method
- zeroin
- van Wijngaarden-Dekker-Brent method
area: numerical/root-finding
level: advanced
summary: Robust bracketing method mixing inverse quadratic interpolation, secant, and bisection. Superlinear near a simple root, never more than a fixed multiple of k^2 evaluations, with k the bisection count.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {w: "the width b - a of the starting bracket", δ: "the tolerance on the error", k: "the bisection count ⌈log2(w/δ)⌉"}
  time: {worst: "O(k^2)", average: "O(log log(1/δ))"}
  space: {extra: Θ(1)}
  evaluations: {worst: "2(k + 2)^2 + 2", step: "1"}
properties: {deterministic: true, recursive: false, bracketing: true, derivative_free: true}
prereqs: [dekker-method, inverse-quadratic-interpolation, bisection-method]
see_also: [secant-method, illinois-method, chandrupatla-method, ridders-method, regula-falsi, stopping-criteria, order-of-convergence, bracketing-method]
sources:
  - paper: doi:10.1093/comjnl/14.4.422
    title: Richard P. Brent, An algorithm with guaranteed convergence for finding a zero of a function, The Computer Journal 14(4), 422-425, 1971
    locator: the algorithm, the test that forces bisection, and the comparison with Dekker's algorithm
  - book: isbn:9780486419985
    title: Richard P. Brent, Algorithms for Minimization without Derivatives, Prentice-Hall, 1973 (Dover reprint, 2002)
    locator: Chapter 4, An Algorithm with Guaranteed Convergence for Finding a Zero of a Function (the procedure zero, its bound on the number of evaluations and the numerical tests) and Chapter 3 (the order of the interpolation steps)
  - book: "George E. Forsythe, Michael A. Malcolm and Cleve B. Moler, Computer Methods for Mathematical Computations, Prentice-Hall, 1977"
    locator: Chapter 7, Solution of Nonlinear Equations (the Fortran function ZEROIN, a translation of Brent's procedure)
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 9.3, Van Wijngaarden-Dekker-Brent Method
  - paper: doi:10.1145/210089.210111
    title: G. E. Alefeld, F. A. Potra and Yixun Shi, Algorithm 748, Enclosing zeros of continuous functions, ACM Transactions on Mathematical Software 21(3), 327-344, 1995
    locator: the comparison with Brent's method and the enclosing methods with a better asymptotic efficiency
---

Brent's method finds a root of a continuous function $f$ in a bracket $[a, b]$ with $f(a)f(b) < 0$. In each step it tries a fast interpolation step, [inverse quadratic interpolation](/inverse-quadratic-interpolation/) through three points or the [secant](/secant-method/) step through two, and it accepts that step only if it lands well inside the bracket and is less than half the step before the last one. Otherwise it [bisects](/bisection-method/). The root never leaves the bracket. Near a simple root the method converges superlinearly, and on any continuous function it needs at most a fixed multiple of $k^2$ evaluations, where $k = \lceil \log_2(w/\delta) \rceil$ is the number that bisection needs. It is the standard zero finder of numerical libraries, often under the name zeroin, and it repairs the slow cases of [Dekker's method](/dekker-method/).

## In plain words

You know that the answer lies between two numbers, because the function changes sign there. Each round, make a smart guess from the last few values: a straight line or a sideways parabola through them, crossing zero. Check the guess. It must fall well inside the interval, and the step to it must be clearly shorter than the step two rounds ago. If both checks pass, take it; if not, cut the interval in half. Keep the half that still holds the answer. On smooth functions the smart guesses win and the answer comes very fast. On nasty functions the halving keeps the work bounded.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Given a continuous $f$ on $[a, b]$ with $f(a)f(b) < 0$ and a tolerance $\delta \ge 0$, find $x$ with $|x - x^*| \le \delta + 8u|x|$ for a root $x^*$ in $[a, b]$, where $u = 2^{-53}$ is the unit roundoff. Here $w = b - a$ and the step $d$ is distinct from the error $e_k$; in the code the variable $e$ holds the step before the last.

## The algorithm

The variables are the best point $b$ (with $|f(b)| \le |f(c)|$), the contrapoint $c$ (so a root lies between $b$ and $c$), the previous best point $a$, the last step $d$ and the step before it, $e$.

```pseudo id=main
BRENT(f, a, b, delta, kmax):                         // f(a) f(b) < 0
L1   fa <- f(a);  fb <- f(b);  c <- a;  fc <- fa;  d <- e <- b - a
L2   for k = 1, 2, ..., kmax:
L3       if fb and fc have the same sign then c <- a;  fc <- fa;  d <- e <- b - a
L4       if |fc| < |fb| then a <- b;  b <- c;  c <- a;  fa <- fb;  fb <- fc;  fc <- fa
L5       t <- 4u|b| + delta/2;  m <- (c - b)/2;  if |m| <= t or fb = 0 then return b
L6       if |e| >= t and |fa| > |fb| then
L7           s <- fb/fa;  if a = c then p <- 2ms;  q <- 1 - s                       // secant
             else q <- fa/fc;  r <- fb/fc;  p <- s(2mq(q - r) - (b - a)(r - 1));  q <- (q - 1)(r - 1)(s - 1)   // IQI
L8           if p > 0 then q <- -q;   p <- |p|
L9           if 2p < min(3mq - |tq|, |eq|) then e <- d;  d <- p/q  else d <- m;  e <- m
L10      else d <- m;  e <- m                                                     // bisect
L11      a <- b;  fa <- fb;  if |d| > t then b <- b + d else b <- b + t sign(m);  fb <- f(b)
     return b                                                                      // kmax reached
```

Line L1 sets up the bracket $[b, c]$ and sets both step sizes to the full width. Line L3 restores the bracket after a step: if the new $b$ has the sign of $c$, the previous point $a$ becomes the contrapoint. Line L4 makes $b$ the point with the smaller $|f|$; after it, $a$ is the previous best point. Line L5 stops when the bracket has width at most $2t$ or $f(b) = 0$. Lines L6 to L8 compute an interpolation step $d = p/q$ toward $c$: the secant step when only two distinct points are known ($a = c$), and inverse quadratic interpolation through $a$, $b$, $c$ otherwise, written with ratios of function values. Line L9 accepts the step only if the new point lies within three quarters of the way from $b$ to $c$, and $|d|$ is less than half of $e$, the step before the last. Lines L9 and L10 fall back to the midpoint. Line L11 moves $b$, by at least $t$.

## Example

Take $f(x) = x^3 - x - 2$ on $[1, 2]$ with $\delta = 10^{-12}$; the root is $x^* = 1.5213797068$.

| $k$ | step | $x_k$ | $\lvert e_k \rvert$ | $\log\lvert e_k\rvert / \log\lvert e_{k-1}\rvert$ |
|---|---|---|---|---|
| 1 | secant | 1.333333333333 | $1.88 \times 10^{-1}$ | |
| 2 | IQI | 1.582800284293 | $6.14 \times 10^{-2}$ | |
| 3 | secant | 1.511876874025 | $9.50 \times 10^{-3}$ | |
| 4 | secant | 1.520944027716 | $4.36 \times 10^{-4}$ | 1.662 |
| 5 | IQI | 1.521379953272 | $2.46 \times 10^{-7}$ | 1.967 |
| 6 | secant | 1.521379706722 | $8.25 \times 10^{-11}$ | 1.526 |
| 7 | secant | 1.521379706805 | $< 10^{-16}$ | |

The method stops after 7 steps and 9 evaluations. The secant steps appear when the newest point and the contrapoint are the only two distinct points (after line L3 resets $c$). The table compares the number of evaluations with $\delta = 10^{-12}$:

| function, bracket | bisection | Dekker | Brent |
|---|---|---|---|
| $x^3 - x - 2$, $[1, 2]$ | 42 | 10 | 9 |
| $\cos x - x$, $[0, 1]$ | 42 | 8 | 8 |
| $e^x - 2$, $[0, 1]$ | 42 | 9 | 8 |
| $x^{10} - 1$, $[0, 1.3]$ | 43 | 10 | 10 |
| $x^9$, $[-1, 1.1]$ | 43 | 321 | 113 |
| $(x - 0.3)^{19}$, $[0, 1]$ | 42 | 704 | 117 |
| $(x - 1)^3$, $[0, 3.3]$ | 44 | 102 | 108 |

On smooth functions with simple roots Brent's method is 4 to 5 times cheaper than bisection. At roots of high multiplicity it is worse than bisection, but far better than Dekker's method, and always within its bound.

## Correctness

The invariant at line L5 is: $f(b)$ and $f(c)$ are nonzero with opposite signs, $|f(b)| \le |f(c)|$, and $b, c$ lie in the starting interval. So a root lies between $b$ and $c$, and the return at L5 has error less than $|c - b| \le 2t = \delta + 8u|b|$. Each step moves $b$ strictly toward $c$ by at least $t$, so the width falls by at least $t$; the halving test of L9 forces a bisection after at most $2k + 4$ interpolation steps in a row, which gives the bound of $2(k + 2)^2$ steps. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs one evaluation of $f$ and a few arithmetic operations; the start costs two, and the space is $\Theta(1)$.

- **Worst case (proved).** For $\delta > 0$ at most $2(k + 2)^2$ steps, with $k = \lceil \log_2(w/\delta) \rceil$. Brent (1973, Chapter 4) gives a sharper count of the same order $k^2$. Compare $k$ for bisection and $O(w/\delta)$ for Dekker's method.
- **Near a simple root (local).** For $f \in C^3$ with $f'(x^*) \ne 0$, the interpolation steps are eventually accepted, and the convergence is superlinear, with order between that of the secant step, $1.618$, and that of inverse quadratic interpolation, $1.839$, one evaluation in each step. The observed log ratios in the example are 1.53 to 1.97.
- **Multiple roots.** Interpolation converges linearly at a multiple root, and the bisection test takes over; the method then costs a few times the bisection count, as in the table.

## Properties

- **Bracketing.** A root stays between $b$ and $c$ for every continuous $f$.
- **Derivative free.** It uses only values of $f$.
- **Guaranteed bound.** $O(k^2)$ evaluations in the worst case, against $O(w/\delta)$ for Dekker's method.
- **Superlinear near a simple root.** Usually 4 to 10 evaluations for full binary64 accuracy on smooth functions with a reasonable bracket.
- **Ratios, not differences.** The interpolation step is computed from the ratios $s = f(b)/f(a)$, $r = f(b)/f(c)$, $q = f(a)/f(c)$, so the step is formed as a small correction $p/q$ to $b$.

## Variants and improvements

- **Algorithm 748 (Alefeld, Potra and Shi, 1995).** Enclosing methods that use cubic inverse interpolation and a double-length secant step, with a proved asymptotic efficiency index of about 1.65 for the bracket width, which Brent's method does not have.
- **[Chandrupatla's method](/chandrupatla-method/).** A simpler test to accept inverse quadratic interpolation, with similar results.
- **Brent's minimizer.** The same safeguard idea, with parabolic interpolation and the [golden section search](/golden-section-search/), gives Brent's method for one-dimensional minimization (Brent 1973, Chapter 5).
- **[Illinois](/illinois-method/) and [Ridders](/ridders-method/) methods.** Simpler bracketing methods without a $k^2$ bound but with good average speed.

## When to use it

Use it as the default for a root of a function of one real variable when a bracket is known and no derivative is used: it is robust on any continuous function and fast on smooth ones. If a derivative is cheap and the start is good, [Newton's method](/newton-raphson-method/), possibly safeguarded by the bracket, needs fewer evaluations. If the worst case must be exactly $\lceil\log_2(w/\delta)\rceil$, use [bisection](/bisection-method/). If no bracket is known, find one first; see [bracketing methods](/bracketing-method/).

## Pitfalls

- **Dropping the halving test (L9).** Without the condition $2p < |eq|$, the method becomes Dekker's method with IQI and can creep: on $x^9$ on $[-1, 1.1]$ Dekker's version needs 321 evaluations against 113.
- **Not resetting the steps (L3).** When the contrapoint changes, $d$ and $e$ must be reset to the width, or the halving test compares against a stale step.
- **A tolerance without the relative term (L5).** With $t = \delta/2$ and $\delta = 0$, the test never succeeds once $b$ and $c$ are neighbor floating point numbers, and the method runs to $k_{\max}$. The term $4u|b|$ fixes this away from 0.
- **No sign change (L1).** With $f(a)f(b) > 0$ there is no bracket and the method must stop with an error; Brent's procedure assumes the sign change and does not check it.
- **A pole in the bracket.** For $1/(x - 1/3)$ on $[0, 1]$ the method returns a point next to the pole after 44 evaluations. A check of $|f(b)|$ at the end shows it.
- **Tolerance near zero (L5).** For a root at $x^* = 0$ and $\delta = 0$, $t = 4u|b|$ shrinks with $b$. For $x^3$ on $[-1, 1.1]$ the method then takes 930 evaluations and stops only when $f(b)$ underflows to 0 at $b \approx -9.7 \times 10^{-109}$. Use $\delta > 0$.

## Implementations

## History

Brent built the method in 1971 on the algorithm of Dekker (1969), which goes back to work by van Wijngaarden, Zonneveld and Dijkstra at the Mathematical Centre in Amsterdam. He added inverse quadratic interpolation and the test that forces bisection, proved the bound of order $k^2$, and published the ALGOL 60 procedure zero in his 1973 book. Forsythe, Malcolm and Moler (1977) translated it to the Fortran function ZEROIN, which spread to many libraries; Numerical Recipes calls it the van Wijngaarden-Dekker-Brent method. Alefeld, Potra and Shi (1995) gave enclosing methods with a better proved asymptotic efficiency.

## References
