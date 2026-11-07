---
tag: AGQH37
kind: algorithm
slug: ridders-method
name: Ridders' method
aliases:
- Ridders' exponential method
- Ridders' algorithm
area: numerical/root-finding
level: advanced
summary: "A bracketing method: evaluate the midpoint, remove an exponential factor so that the three values lie on a line, and take the false-position point. Keeps the bracket and at least halves it per pass."
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {L: "b - a, the width of the initial bracket", δ: the tolerance on the bracket half-width}
  time: {worst: "O(log(L/δ))"}
  space: {extra: Θ(1)}
  evaluations: {per_step: "2", worst: "2 + 2 log_2(L/(2δ))"}
properties: {deterministic: true, recursive: false, bracketing: true, derivative_free: true, local: false}
history:
  year: 1979
  people: [C. J. F. Ridders]
  note: Ridders published the method in 1979 in a short note in the IEEE Transactions on Circuits and Systems; Numerical Recipes made it widely known.
prereqs: [bisection-method, regula-falsi, bracketing-method]
see_also: [bisection-method, regula-falsi, brent-method, chandrupatla-method, secant-method, inverse-quadratic-interpolation, stopping-criteria, order-of-convergence]
sources:
  - paper: doi:10.1109/TCS.1979.1084580
    title: "C. J. F. Ridders, A new algorithm for computing a single root of a real continuous function, IEEE Transactions on Circuits and Systems 26(11) (1979) 979-980"
    locator: the exponential factor, the update formula and the claimed quadratic convergence
  - book: isbn:9780521880688
    title: W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 9.2, Secant method, false position method, and Ridders' method (zriddr and its convergence remarks)
  - book: "R. P. Brent, Algorithms for Minimization without Derivatives, Prentice-Hall, 1973 (reprinted by Dover, 2002)"
    locator: Chapter 4, An algorithm with guaranteed convergence for finding a zero of a function (the standard for bracketing hybrids)
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: Chapter 3, the efficiency index
---

Ridders' method finds a root of a continuous function $f$ in a bracket $[a, b]$ with $f(a)f(b) < 0$. In each pass it evaluates $f$ at the midpoint $m$, multiplies $f$ by an exponential $e^{Q(x - a)}$ chosen so that the three values at $a$, $m$ and $b$ lie on a straight line, and takes the point where the [false position](/regula-falsi/) line through $(a, \cdot)$ and $(m, \cdot)$ crosses zero. The result has the closed form
$$x = m + (m - a)\,\operatorname{sign}(f(a) - f(b))\,\frac{f(m)}{\sqrt{f(m)^2 - f(a)f(b)}},$$
which always lies in the half of the bracket that contains the sign change. The bracket is then shrunk to a sign change among $a$, $m$, $x$, $b$. So the bracket is kept and at least halves in every pass, as in [bisection](/bisection-method/), at two evaluations per pass. Near a root it is usually much faster: when both ends of the bracket converge the error is squared in each pass, but sometimes one end stays behind and only the Ridders point converges quickly.

## In plain words

Start with two points where the function has opposite signs, so a root lies between them. Look at the middle too. A straight line through the end values would guess the root well only if the curve were straight, so Ridders first bends the curve with an exponential factor until the three values at the left end, the middle and the right end lie on one line. For the bent curve the line is a good guess, and the bending does not move the root, because multiplying by a positive factor never changes where a function is zero. The guess always lands in the half where the root is. Then keep the smallest piece that still has a sign change, and repeat.

## The problem

The input is a continuous real function $f$ on $[a, b]$, with $f(a)f(b) < 0$, a tolerance $\delta \ge 0$ and a maximum number of passes $k_{\max}$. The output is a point $\hat x$, a final bracket $[a, b]$ with a sign change (or an exact zero), and a flag. When the flag is "bracket", the true root in the final bracket is within $\delta$ of $\hat x$; that is certified, in floating point too, as long as the computed signs of $f$ are right.

Notation on the root-finding pages: $x^*$ is a root, $e_k = x_k - x^*$ the error of the $k$-th Ridders point, $[a, b]$ a bracket with $f(a)f(b) < 0$. A method has order $q$ and rate constant $C$ when $|e_{k+1}| \approx C|e_k|^q$; the cost is the number of evaluations of $f$, and with $w$ evaluations per step the efficiency index is $q^{1/w}$.

## The algorithm

```pseudo id=main
RIDDERS(f, a, b, δ, kmax)
L1  fa ← f(a); fb ← f(b); if fa = 0 return a; if fb = 0 return b; if fa, fb have the same sign return "no sign change"
L2  for k ← 1 to kmax do
L3      m ← a + (b − a)/2; if m is not strictly between a and b then return (m, "bracket"); fm ← f(m); if fm = 0 return (m, "root")
L4      s ← sqrt(fm² − fa·fb)                         ▷ computed as t·sqrt((fm/t)² − (fa/t)(fb/t)), t = max(|fa|, |fb|, |fm|)
L5      x ← m + (m − a) · sign(fa − fb) · fm / s;  clamp x to [a, b]
L6      fx ← f(x); if fx = 0 return (x, "root")
L7      if sign(fm) ≠ sign(fx) then [a, b] ← [min(m, x), max(m, x)]
        else if sign(fa) ≠ sign(fx) then b ← x
        else a ← x
L8      if b − a ≤ 2δ then return ((a + b)/2, "bracket")
L9      if k > 1 and |x − xprev| ≤ δ then return (x, "converged")
L10     xprev ← x
L11 return ((a + b)/2, "kmax reached")
```

Line L1 checks the bracket. Line L3 evaluates the midpoint, and stops when the bracket is two adjacent floating point numbers. Lines L4 and L5 compute the Ridders point. Because $f(a)f(b) < 0$, the square root is at least $|f(m)|$, so $|x - m| \le m - a$ and $x$ lies in $[a, b]$; the clamp only guards against rounding. The scaling in line L4 avoids overflow and underflow when the values are huge or tiny. Line L7 keeps a sign change: either between $m$ and $x$, or between $x$ and the end with the other sign. Line L8 is the certified bracket test, and line L9 the step test of Numerical Recipes, which stops when two successive Ridders points agree even though one end of the bracket may still be far away; its result is not certified by the bracket, but it is still inside the final bracket. The implementation also returns "failure" on NaN or infinity.

**Where the formula comes from.** Let $h = m - a$ and look for $Q$ such that $g(x) = f(x)e^{Q(x - a)}$ takes values $f(a)$, $f(m)w$, $f(b)w^2$ on a line, where $w = e^{Qh} > 0$. That means $f(a) + f(b)w^2 = 2f(m)w$, a quadratic in $w$ whose two roots have product $f(a)/f(b) < 0$, so exactly one is positive. False position on $g$ between $a$ and $m$, or equivalently between $m$ and $b$, then gives the closed form above. Since $e^{Q(x - a)} > 0$, $g$ and $f$ have the same zeros. If $f(x) = e^{\lambda x}(\alpha x + \beta)$, then $g$ is exactly linear and $x$ is exactly the root.

## Example

Solve $x^3 - x - 2 = 0$ on $[1, 2]$, root $x^* = 1.5213797068045676$, in binary64 with $\delta = 0$. Here $f(1) = -2$, $f(2) = 4$, $m = 1.5$ and $f(m) = -0.125$, so $s = \sqrt{0.015625 + 8} = 2.8311$ and $x_1 = 1.5 + 0.5 \cdot 0.125/2.8311 = 1.5220755392844174$.

| pass | Ridders point $x_k$ | $\lvert e_k \rvert$ | bracket width after the pass |
|---|---|---|---|
| 1 | 1.5220755392844174 | $6.96 \cdot 10^{-4}$ | $2.21 \cdot 10^{-2}$ |
| 2 | 1.5213797263830957 | $1.96 \cdot 10^{-8}$ | $1.03 \cdot 10^{-2}$ |
| 3 | 1.5213797068047001 | $1.33 \cdot 10^{-13}$ | $5.17 \cdot 10^{-3}$ |
| 4 | 1.5213797068045676 | $0$ | |

In pass 4 the computed $f(x_4)$ is exactly $0$, after 10 evaluations (2 for the ends and 2 per pass). The bracket only halves in each pass: the left end is always the previous midpoint, below the root, and the right end is always the Ridders point, just above it. In 200-digit arithmetic the same happens for many more passes: the width halves, the error ratio $|e_{k+1}|/|e_k|$ falls by a factor of about 4 per pass ($2.8 \cdot 10^{-5}$, $6.8 \cdot 10^{-6}$, $1.7 \cdot 10^{-6}$, ...), which is superlinear convergence but of order 1. The same one-sided pattern appears for $\cos x - x$ on $[0, 1]$, where the program stops by the step test after 6 passes and 14 evaluations with $\hat x = 0.7390851332151608$, one unit in the last place from the root, while the bracket is still $7.3 \cdot 10^{-3}$ wide. For $x e^x - 1$ on $[0, 1]$ both ends converge, and the errors in 400-digit arithmetic, $3.3 \cdot 10^{-14}$, $5.7 \cdot 10^{-27}$, $1.4 \cdot 10^{-55}$, $1.0 \cdot 10^{-109}$, are squared in each pass (all observed).

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md).

- **Bracket kept (proved).** After every pass, $f(a)f(b) < 0$ or an exact zero has been returned, and the new bracket lies inside the half of the old bracket that contains the sign change, so its width is at most half the old one.
- **Termination and certificate (proved).** The loop ends after at most $k_{\max}$ passes. With $\delta > 0$ it ends by line L8 after at most $\lceil \log_2((b - a)/(2\delta)) \rceil$ passes, and then a root of $f$ lies within $\delta$ of the returned point. In floating point with $\delta = 0$, line L3 ends the loop once the bracket consists of two adjacent numbers.
- **Global convergence (proved).** For continuous $f$, the brackets shrink to a point, which is a root.
- **Exactness (proved).** If $f(x) = e^{\lambda x}(\alpha x + \beta)$ with $\alpha \ne 0$, the first Ridders point is the root.
- **Speed near a root (observed).** Ridders (1979) claims quadratic convergence per pass, that is order $\sqrt 2$ per evaluation. The runs above show this when both ends converge, and only superlinear convergence of order 1 of the Ridders points, with the bracket halving, when one end stays behind. No proof of a rate is given here.

## Complexity

The cost model is the number of evaluations of $f$.

- **Per pass.** Two evaluations, at $m$ and at $x$, and one square root.
- **Worst case.** At most $2 + 2\lceil \log_2((b - a)/(2\delta)) \rceil$ evaluations to the tolerance $\delta$: twice the bound of bisection, because the bracket is only guaranteed to halve per pass.
- **Typical case.** For smooth $f$ with a simple root, a handful of passes reach full binary64 accuracy, as in the examples. If the quadratic rate per pass holds, the efficiency index is $2^{1/2} \approx 1.414$, below the [secant method](/secant-method/)'s $1.618$ and about that of Newton's method.
- **Space.** $\Theta(1)$.

### Floating point

The bracket test needs only the signs of the computed $f$, so as long as those signs are right, the root in the returned bracket is certified. Near a root the computed signs are noise below the level $\varepsilon_f$ of the error in $f$, so the true accuracy is limited to about $\varepsilon_f/|f'(x^*)|$ (the limiting accuracy of every method based on values of $f$). The scaling in line L4 keeps $s$ finite and nonzero whenever $f(a)$, $f(b)$, $f(m)$ are finite and $f(a)f(b) < 0$, even when their product would overflow or underflow. With $\delta = 0$ the loop ends when the bracket cannot be split, after at most a few thousand passes in binary64, and $k_{\max}$ bounds it in any case.

## Properties

- **Bracketing and derivative-free.** Uses only values of $f$ and keeps a sign change.
- **Never worse than twice bisection.** The bracket at least halves in each pass of two evaluations.
- **Exact for an exponential times a line.** The exponential factor makes such functions linear.
- **Invariant under scaling of $f$.** Replacing $f$ by $cf$ with $c \ne 0$ does not change the iterates.
- **No interpolation history.** Each pass uses only the current bracket and midpoint, so it is simpler than [Brent's method](/brent-method/).

## Variants and improvements

- **Brent's method and Chandrupatla's method.** Hybrids of bisection with inverse quadratic interpolation that guarantee convergence and have a proved superlinear rate in the generic case; usually preferred ([Brent's method](/brent-method/), [Chandrupatla's method](/chandrupatla-method/)).
- **Illinois and Pegasus modifications of false position.** Other ways to stop one end from sticking, by scaling the stored function value.
- **Step test.** The stop of line L9 is the one used in Numerical Recipes; without it, one-sided cases waste passes halving a bracket around an already accurate point.

## When to use it

Use Ridders' method when a sign change is known and a short, robust, derivative-free method is wanted, as an alternative to Brent's method. If a proved rate matters, or evaluations are expensive, prefer Brent's or Chandrupatla's method.

## Pitfalls

- **No sign change.** Like every bracketing method it needs $f(a)f(b) < 0$; for $x^2 + 1$ on $[-1, 1]$ it stops at once.
- **Bracket test only.** With the step test removed, the one-sided cases run until the bracket is small, which for $\cos x - x$ costs many passes after the answer is already exact.
- **Multiple roots.** At a root of odd multiplicity the method is no faster than bisection per pass; for $(x - 1)^3$ on $[0, 3]$ with $\delta = 10^{-12}$ it takes 34 passes and 70 evaluations (observed). At even multiplicity there is no sign change.
- **Discontinuities and poles.** A sign change at a pole is found like a root; check $|f|$ at the result.
- **Overflow in $f(m)^2 - f(a)f(b)$.** Computing it directly overflows for values near $10^{154}$; scale as in line L4.

## Implementations

## History

C. J. F. Ridders published the method in 1979 in a one-and-a-half-page note in the IEEE Transactions on Circuits and Systems, as a simple alternative to the method of Dekker and Brent, with a claim of quadratic convergence. It became widely known through Numerical Recipes, which presents it as a robust competitor of Brent's method.

## References
