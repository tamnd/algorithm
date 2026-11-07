---
tag: XBBB8M
kind: technique
slug: bracketing-method
name: Bracketing
aliases:
- bracketing interval
- sign-change bracket
- bracketing methods
- enclosing methods
area: numerical/root-finding
level: intro
summary: Keep an interval [a, b] with f(a) f(b) < 0, so that a root of the continuous function f stays enclosed while the interval shrinks.
prereqs: [root-finding-problem, loop-invariant]
see_also: [bisection-method, regula-falsi, illinois-method, brent-method, chandrupatla-method, real-root-isolation, interval-newton-method, stopping-criteria]
sources:
  - book: isbn:9780486419985
    title: Richard P. Brent, Algorithms for Minimization without Derivatives, Prentice-Hall, 1973 (Dover reprint, 2002)
    locator: Chapter 4, An algorithm with guaranteed convergence for finding a zero of a function (the bracket invariant and the tolerance 2u|b| + t)
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 2.5, Globally convergent methods for solving one equation in one unknown
  - book: isbn:9781305253667
    title: Richard L. Burden, J. Douglas Faires and Annette M. Burden, Numerical Analysis, tenth edition, Cengage, 2016
    locator: Section 2.1 (bisection) and Section 2.3 (the method of false position)
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 9.1, Bracketing and Bisection (bracket expansion and the search for a sign change)
  - paper: doi:10.1145/210089.210111
    title: G. E. Alefeld, F. A. Potra and Yixun Shi, Algorithm 748, enclosing zeros of continuous functions, ACM Transactions on Mathematical Software 21(3), 327-344, 1995
    locator: enclosing methods whose bracket width, not only the iterate, converges with order greater than 1
---

Bracketing is the technique of keeping an interval $[a, b]$ with $f(a) f(b) < 0$ around a root of a continuous function $f$, and shrinking it step by step. The intermediate value theorem guarantees a root in each such interval, so a bracketing method never loses the root, whatever the next trial point is. The [bisection method](/bisection-method/), [regula falsi](/regula-falsi/), the [Illinois method](/illinois-method/), [Brent's method](/brent-method/) and [Chandrupatla's method](/chandrupatla-method/) are all instances; they differ only in how they choose the next point inside the bracket. The technique is the base of the safe solvers of the [root-finding problem](/root-finding-problem/) in one variable.

## In plain words

A continuous curve that is below the axis at one point and above it at another must cross the axis between them. So a pair of points with values of opposite signs traps a crossing. A bracketing method keeps such a pair. At each step it picks a new point between the two, looks at the sign of the curve there, and replaces the end that has the same sign. The pair always traps a crossing, and the gap between the two points gets smaller. A method can pick the new point in the middle, which is slow and safe, or by a clever guess, which is fast when the guess is good. A careful method uses the guess and falls back to the middle when the guess does not shrink the gap enough.

## When it applies

- $f$ is a continuous real function of one real variable, and you can find two points where its values have opposite signs.
- You need a guarantee: the method must not diverge, must not jump to another root far away, and must stop.
- The root has odd [multiplicity](/multiplicity-of-roots/), so $f$ changes sign there. A root of even multiplicity, such as the root of $(x - 1)^2$, cannot be bracketed by sign.
- $f$ has no usable derivative, or is noisy, or is given only as a program.
- The problem has a sign test but no value, for example "is the computed load too large". Bisection needs only the sign.

Signals in a problem statement: "find the value where the quantity changes from too small to too large", "solve for the parameter that makes the error zero, which lies between these two limits", an inverse of a monotone function, a quantile of a distribution, or the crossing of two curves.

## The template

The holes are CHOOSE, STOP and BEST. The notation is that of the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error; a method has order $q$ and rate $C$ when $|e_{k+1}| \approx C|e_k|^q$; the cost is the number of evaluations of $f$; $\delta$ is the tolerance.

```pseudo id=main
BRACKET-SOLVE(f, a, b, δ, kmax)          ▷ a < b, f continuous on [a, b]
L1  fa ← f(a), fb ← f(b)
L2  if fa = 0 then return a; if fb = 0 then return b
L3  if sign(fa) = sign(fb) or a value is NaN then error "no bracket"
L4  for k ← 1 to kmax do
L5      c ← CHOOSE(a, b, fa, fb, memory)     ▷ hole: a point with a < c < b
L6      fc ← f(c); if fc = 0 then return c
L7      if sign(fc) = sign(fa) then a ← c, fa ← fc
L8      else b ← c, fb ← fc
L9      if STOP(a, b, fa, fb, δ) then return BEST(a, b, fa, fb)   ▷ holes
L10 return BEST(a, b, fa, fb), with the flag "kmax reached"
```

The invariant of the loop is: $a < b$, $fa = f(a)$ and $fb = f(b)$ are nonzero, and their signs differ. Lines L1 to L3 make it true. In lines L6 to L8, the new value $f(c)$ is nonzero, so it has the sign of $fa$ or the sign of $fb$; the end with the same sign moves to $c$, and the signs at the two ends still differ. This holds for every choice of $c$ in $(a, b)$, which is why CHOOSE is free. By the intermediate value theorem, $[a, b]$ holds a root after each step.

The invariant does not by itself make the width $b - a$ go to zero. That needs a property of CHOOSE: the width must fall by at least a fixed factor $\rho < 1$ at least once in every fixed number $s$ of steps. Then after $k$ steps the width is at most $\rho^{\lfloor k/s \rfloor}(b_0 - a_0)$, and the method stops after $O(s \log((b_0 - a_0)/\delta))$ steps.

- **CHOOSE.** The midpoint gives bisection, with $\rho = 1/2$ and $s = 1$. The root of the line through $(a, fa)$ and $(b, fb)$ gives regula falsi, which has no such $\rho$. Safeguarded interpolation gives Dekker, Brent and Chandrupatla.
- **STOP.** The usual test is $b - a \le 2\delta$, or, in floating point, $b - a \le 2(\delta + 2u|c|)$ with $u$ the [unit roundoff](/machine-epsilon/). Brent's method uses a test of this form, $2u|b| + t$, so that a tolerance below the spacing of the numbers cannot make the loop run forever (Brent, Chapter 4).
- **BEST.** Return the midpoint, which is within $(b - a)/2$ of a root, or the end with the smaller $|f|$, which is the usual choice of interpolation methods.

## Classic examples

1. **[Bisection](/bisection-method/).** CHOOSE is the midpoint. The width halves at each step, so the cost is $\lceil \log_2((b-a)/(2\delta)) \rceil + 2$ evaluations for every continuous $f$.
2. **[Regula falsi](/regula-falsi/).** CHOOSE is the secant point $c = b - fb (b - a)/(fb - fa)$. It keeps the bracket, but for a convex or concave $f$ one end never moves. For $f(x) = x^{10} - 1$ on $[0, 1.3]$, the right end stays at $1.3$: after 10 steps the bracket is $[0.68694, 1.3]$, of width $0.61306$, while bisection has width $0.00127$. Regula falsi needs 95 steps to get within $10^{-10}$ of the root $1$.
3. **[Illinois method](/illinois-method/).** CHOOSE is the secant point, but the value at an end that stays twice in a row is halved. The fixed end then moves, and the order becomes $3^{1/3} \approx 1.442$ per evaluation.
4. **[Ridders' method](/ridders-method/).** CHOOSE uses the midpoint and an exponential factor. The order is $\sqrt 2$ per evaluation, and the bracket is kept.
5. **[Dekker's method](/dekker-method/) and [Brent's method](/brent-method/).** CHOOSE is a secant or [inverse quadratic interpolation](/inverse-quadratic-interpolation/) step, accepted only when it lies in the bracket and shrinks it enough, else a bisection step. Brent's version bounds the cost by about the square of the bisection count.
6. **[Chandrupatla's method](/chandrupatla-method/).** CHOOSE is inverse quadratic interpolation when a simple test on the last three points says that it is safe, else bisection.
7. **[Real root isolation](/real-root-isolation/) and [Sturm sequences](/sturm-sequence/).** The bracket is certified by a count of sign changes in a sequence of polynomials instead of by the sign of $f$, so roots of even multiplicity are found too. The [bisection eigenvalue algorithm](/bisection-eigenvalue-algorithm/) uses the same idea with a [Sturm count](/sturm-sequence-eigenvalue-count/) for a symmetric tridiagonal matrix.

## Variations

- **Finding a bracket.** Start with a guess $[a, b]$. While $f(a)$ and $f(b)$ have the same sign, move the end with the smaller $|f|$ away from the other end by a factor, for example $a \leftarrow a + 1.6(a - b)$ (Press et al., Section 9.1). For $f(x) = e^x - 100$ from $[0, 1]$, two expansions give $[0, 6.76]$ with $f(0) < 0 < f(6.76)$. The search can fail: $x^2 + 1$ has no real root, and $(x - 1)^2 - 10^{-12}$ has two roots so close together that a coarse grid sees no sign change.
- **Brackets by counts.** For a real polynomial, the number of sign changes in a Sturm sequence gives the number of roots in an interval, so an interval with count 1 is a certified bracket even for a root that a sign test misses.
- **Enclosures with fast order.** Plain hybrids converge fast in the iterate, but the bracket width can stay large. Alefeld, Potra and Shi (1995) give enclosing methods whose width itself converges with order above 1.
- **Interval arithmetic.** With [interval arithmetic](/interval-arithmetic/), an interval $X$ with $0 \notin f(X)$ is proved to hold no root, and the [interval Newton method](/interval-newton-method/) proves that a box holds exactly one root. This extends bracketing to systems.
- **Brackets for a minimum.** For a minimum of a unimodal function, the bracket is a triple $a < b < c$ with $f(b) < f(a)$ and $f(b) < f(c)$. [Golden section search](/golden-section-search/) shrinks it.

## Pitfalls

- **A pole looks like a root.** $f(x) = 1/(x - 1/3)$ has $f(0) < 0 < f(1)$ but no root in $[0, 1]$. The bracket guarantee needs continuity on all of $[a, b]$. Check $|f|$ at the result.
- **The product test.** Writing `fa * fc > 0` instead of comparing signs underflows to 0 when both values are tiny, for example $10^{-200}$, and then the wrong end moves. Compare the signs.
- **A width that does not shrink.** A CHOOSE without a guarantee, as in plain regula falsi, can leave one end fixed. Then the width stays large, and a stop test on the width never holds.
- **A tolerance below rounding.** A stop test $b - a \le 2\delta$ with $\delta$ below the spacing of the numbers near the root never holds. Add the relative term $4u|c|$, stop when the midpoint equals an end, and bound the steps by $k_{\max}$.
- **Rounding of the sign.** Near the root the computed sign of $f$ is noise. With $|\hat f - f| \le \varepsilon_f$, the method only brackets a sign change of the computed $\hat f$, which is within about $\varepsilon_f / |f'(x^*)|$ of a root at a simple root. A smaller tolerance buys nothing.
- **Several roots.** A bracket with three roots inside gives one of them, and which one depends on CHOOSE. If you need all roots, isolate them first.

## Exercises

1. Show that the template stops after at most $s\lceil \log_{1/\rho}((b_0 - a_0)/(2\delta)) \rceil$ steps when CHOOSE shrinks the width by the factor $\rho$ at least once in every $s$ steps and never makes it grow.
2. For $f(x) = x^2 - 2$ on $[1, 2]$, show that regula falsi keeps the end $b = 2$ for every step, and that its error falls by a factor of about $|1 - f'(x^*)(b - x^*)/f(b)|$ per step. Compute this factor. (It is $3 - 2\sqrt 2 \approx 0.1716$.)
3. Let $f(x) = \min(0, x - 1/3) + \max(0, x - 2/3)$ on $[0, 1]$. Show that $f$ is continuous with $f(0) < 0 < f(1)$ and has infinitely many roots, and find the point that bisection returns. (It returns $1/2$ after one step, since $f(1/2) = 0$.)

## References
