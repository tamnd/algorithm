---
tag: WV8WGC
kind: algorithm
slug: newton-raphson-method
name: Newton-Raphson method
aliases:
- Newton's method
- Newton iteration for roots
- method of tangents
area: numerical/root-finding
level: intro
summary: Replace f by its tangent line at the current point and step to the zero of the tangent, x - f(x)/f'(x). Quadratic convergence near a simple root, no guarantee far from it.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {δ: the tolerance on the error, M: "max |f''| / (2 min |f'|) near a simple root, with M |e_0| ≤ 1/2"}
  time: {local: "O(log log(1/(M δ)))"}
  space: {extra: Θ(1)}
  evaluations: {per_step: "2"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: false, local: true}
history:
  year: 1690
  people: [Isaac Newton, Joseph Raphson, Thomas Simpson]
  note: Newton used the idea on polynomials around 1669; Raphson published an iterative form in 1690; Simpson gave the general form with derivatives in 1740.
prereqs: [root-finding-problem, quadratic-convergence, order-of-convergence]
see_also: [secant-method, newton-bisection-hybrid, newton-method-for-systems, newton-square-root, multiplicity-of-roots, halley-method, newton-fractal, kantorovich-theorem]
sources:
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Section 2.2, Newton's method for solving one equation in one unknown; Section 2.4, Convergence of Newton's method
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 1, Solution of equations by iteration (Newton's method)
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: Chapter 6, Newton-Raphson method; Chapter 7, Fundamental existence theorems for Newton-Raphson iteration
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 25, Nonlinear systems and Newton's method (limiting accuracy with errors in f and f')
  - paper: doi:10.1137/1037125
    title: Tjalling J. Ypma, Historical development of the Newton-Raphson method, SIAM Review 37(4), 531-551, 1995
    locator: the work of Newton, Raphson and Simpson
---

The Newton-Raphson method solves $f(x) = 0$ by replacing $f$ at the current point $x_k$ with its tangent line and taking the zero of that line as the next point, $x_{k+1} = x_k - f(x_k)/f'(x_k)$. Near a simple root of a function with a continuous second derivative it converges with [order 2](/quadratic-convergence/): the number of correct digits about doubles in each step. Far from a root it can diverge or cycle, and at a [multiple root](/multiplicity-of-roots/) it is only linear. It is the base of most fast methods for the [root-finding problem](/root-finding-problem/), for [systems](/newton-method-for-systems/), and for square roots and division in hardware.

## In plain words

Draw the curve of the function and pick a guess on the horizontal axis. Go up to the curve, and draw the straight line that touches the curve there. Follow that line down to where it crosses the axis. That crossing is the new guess. Near a crossing of the curve, a curve looks almost like a straight line, so the new guess is much closer: the error of the new guess is about the square of the old error. If the old guess had three correct digits, the new one has about six. Far from a crossing, the touching line can point anywhere, and the guesses can run away. Each step needs the value of the function and the value of its slope.

## The problem

The input is a function $f$ and its derivative $f'$, both given as procedures, a starting point $x_0$, a tolerance (an absolute part $\delta_a \ge 0$ and a relative part $\delta_r \ge 0$, not both zero) and a maximum number of steps $k_{\max}$. The output is a point $\hat x$ and a flag that says whether the stopping test passed. When $f \in C^2$ near a simple root $x^*$ and $x_0$ is close enough to $x^*$, the method converges to $x^*$; otherwise there is no guarantee. This is the local form of the [root-finding problem](/root-finding-problem/).

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error, $s_k = x_{k+1} - x_k$ the step. A method has order $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$. The cost is the number of evaluations of $f$ and $f'$; a method of order $q$ with $w$ evaluations per step has efficiency index $q^{1/w}$.

## The algorithm

```pseudo id=main
NEWTON(f, f', x0, δa, δr, kmax)
L1  x ← x0
L2  for k ← 1 to kmax do
L3      fx ← f(x)
L4      if fx = 0 then return (x, "root")
L5      d ← f'(x)
L6      if d = 0 or fx or d is not finite then return (x, "failure")
L7      s ← −fx / d
L8      xnew ← x + s
L9      if xnew is not finite then return (x, "failure")
L10     if |s| ≤ δa + δr · |xnew| then return (xnew, "converged")
L11     x ← xnew
L12 return (x, "kmax reached")
```

Each pass evaluates $f$ and $f'$ at $x$ (lines L3 and L5) and moves to the zero of the tangent line $t(y) = f(x) + f'(x)(y - x)$, which is $x - f(x)/f'(x)$ (lines L7 and L8). Line L4 returns at once when $x$ is an exact root. Line L6 stops when the tangent is horizontal, so that it has no zero, or when a value is NaN or infinite. Line L10 is the relative step test of the [stopping criteria](/stopping-criteria/) page: for a superlinear method the step $|s|$ is a good estimate of the error of $x$, and $x_{\text{new}}$ is much better. Line L2 bounds the work, so the loop always ends, also in floating point, where the iterates can cycle between two adjacent numbers.

## Example

Solve $\cos x - x = 0$ from $x_0 = 1$, with $f'(x) = -\sin x - 1$, in binary64, with $\delta_a = 0$ and $\delta_r = 4u = 2^{-51}$. The root is $x^* = 0.73908513321516064165\ldots$, and $f'(x^*) = -1.673612$.

| $k$ | $x_k$ | $f(x_k)$ | $f'(x_k)$ | $s_k$ | $\lvert e_k \rvert$ |
|---|---|---|---|---|---|
| 0 | 1.0 | $-4.596977 \cdot 10^{-1}$ | $-1.841471$ | $-2.496361 \cdot 10^{-1}$ | $2.609 \cdot 10^{-1}$ |
| 1 | 0.7503638678402439 | $-1.892307 \cdot 10^{-2}$ | $-1.681905$ | $-1.125098 \cdot 10^{-2}$ | $1.128 \cdot 10^{-2}$ |
| 2 | 0.7391128909113617 | $-4.645590 \cdot 10^{-5}$ | $-1.673633$ | $-2.775753 \cdot 10^{-5}$ | $2.776 \cdot 10^{-5}$ |
| 3 | 0.739085133385284 | $-2.847206 \cdot 10^{-10}$ | $-1.673612$ | $-1.701234 \cdot 10^{-10}$ | $1.701 \cdot 10^{-10}$ |
| 4 | 0.7390851332151607 | $0$ | | | $3.1 \cdot 10^{-17}$ |

The ratios $|e_{k+1}|/|e_k|^2$ are $0.166$, $0.218$ and $0.2208$, and they tend to $C = |f''(x^*)/(2 f'(x^*))| = \cos x^* / (2(1 + \sin x^*)) = 0.22081$. The step is close to $-e_k$ from step 1 on. At $x_4$ the computed $f$ is exactly $0$, so line L4 returns in the fifth pass, after 5 evaluations of $f$ and 4 of $f'$. The returned value is the binary64 number nearest to $x^*$.

## Correctness

Newton's method has no global guarantee, so the claims are of three kinds, all proved in [the correctness proof](proofs/correctness.md).

- **Always.** The loop ends after at most $k_{\max}$ passes; a result with the flag "root" is an exact zero of $f$; a result with the flag "converged" satisfies the step test.
- **Local (proved).** Let $f \in C^2$ on $I = [x^* - r, x^* + r]$, $f(x^*) = 0$, $f' \ne 0$ on $I$, and $M = \max_I |f''| / (2 \min_I |f'|)$. If $x_0 \in I$ and $M |e_0| \le 1/2$, then in exact arithmetic $|e_{k+1}| \le M |e_k|^2 \le |e_k|/2$, the iterates converge to $x^*$ quadratically, and when line L10 stops after the step $s_k$, the returned point satisfies $|x_{k+1} - x^*| \le 4 M s_k^2$. The key identity is $e_{k+1} = \frac{f''(\xi_k)}{2 f'(x_k)} e_k^2$, from Taylor's theorem.
- **Monotone (proved).** If $f \in C^2$, $f' > 0$ and $f'' \ge 0$ on $[x^*, \infty)$, and $x_0 > x^*$, then $x_1 \ge x_2 \ge \cdots \ge x^*$ and $x_k \to x^*$, whatever the size of $e_0$. The same holds for the other three sign patterns, by symmetry. This covers $x^2 - a$ for square roots (Fourier's condition, Ostrowski, Chapter 9).

## Complexity

The cost model is the number of evaluations of $f$ and $f'$, on a [real RAM](/real-ram/) for the exact analysis.

- **Per step.** Each pass makes one evaluation of $f$ and one of $f'$, so $w = 2$, and the efficiency index is $2^{1/2} \approx 1.414$. The [secant method](/secant-method/), with $w = 1$ and order $1.618$, has the larger index $1.618$, so it is faster per evaluation when $f'$ costs as much as $f$.
- **Steps to the tolerance.** Under the local hypotheses with $M |e_0| \le 1/2$, $M |e_k| \le (M |e_0|)^{2^k} \le 2^{-2^k}$. So $|e_k| \le \delta$ once $2^k \ge \log_2(1/(M\delta))$, that is after $k = \lceil \log_2 \log_2 (1/(M\delta)) \rceil$ steps. For binary64 accuracy from two correct bits this is about 6 steps.
- **Total evaluations.** A run that stops at line L10 in pass $k$ makes exactly $k$ evaluations of $f$ and $k$ of $f'$. A run that stops at line L4 in pass $k$ makes $k$ of $f$ and $k - 1$ of $f'$.
- **Space.** $\Theta(1)$ besides $f$ and $f'$.

### Floating point

Let the computed $f$ have error at most $\varepsilon_f$ near $x^*$, and the computed $f'$ a relative error $\eta < 1/2$. Then the computed step is the exact step for a nearby function, and the iterates reach an error of about
$$|e| \lesssim \frac{\varepsilon_f}{|f'(x^*)|} + u |x^*|,$$
the limiting accuracy (Higham, Chapter 25). An error in $f'$ only slows the convergence: with a fixed relative error $\eta$ the order drops to 1 with rate about $\eta$, but the limiting accuracy is unchanged. So $f'$ can be computed to low precision, while $f$ must be accurate. Near a multiple root of order $m$, the limit is about $(m!\, \varepsilon_f/|f^{(m)}(x^*)|)^{1/m}$.

## Properties

- **Local.** Quadratic convergence holds only near a simple root. The region of convergence can be small and has a fractal boundary for complex $f$ ([Newton fractal](/newton-fractal/)).
- **Affine invariant.** Replacing $f$ by $c f$ with $c \ne 0$ does not change the iterates. A change of the variable $x = \alpha y + \beta$ changes them in the same way.
- **Self-correcting.** An error in one step is corrected by the later steps, as long as the iterate stays in the region of convergence.
- **Works in $\mathbb{C}$.** The same formula with complex arithmetic finds complex roots, for example $\pm i$ for $x^2 + 1$ from a non-real start.
- **No bracket.** The iterates need not stay on one side of the root, and the method does not certify the error by itself.

## Variants and improvements

- **Newton with a bracket.** Keep a sign-change bracket and fall back to bisection when the Newton point leaves it: the [Newton bisection hybrid](/newton-bisection-hybrid/).
- **Damped Newton.** Take $x_{k+1} = x_k + \lambda_k s_k$ with $\lambda_k \in (0, 1]$ chosen so that $|f|$ decreases. This is the start of the globally convergent methods for systems.
- **Multiple roots.** Use $x_{k+1} = x_k - m f(x_k)/f'(x_k)$ for a known multiplicity $m$, or Newton's method on $f/f'$.
- **Without a derivative.** The [secant method](/secant-method/) replaces $f'(x_k)$ by a difference quotient; [Steffensen's method](/steffensen-method/) keeps order 2 with $f(x + f(x))$.
- **Higher order.** [Halley's method](/halley-method/) and [Householder's methods](/householder-methods/) use $f''$ and more for order 3 and higher.
- **Systems.** [Newton's method for systems](/newton-method-for-systems/) solves $J(x_k) s_k = -F(x_k)$ in each step. The [Kantorovich theorem](/kantorovich-theorem/) gives conditions at $x_0$ alone that prove convergence.
- **Algebra.** [Newton iteration](/newton-iteration/) for power series and $p$-adic numbers doubles the precision in each step, as here.
- **Special cases.** [Newton square root](/newton-square-root/), [integer Newton roots](/newton-integer-root/) and [Newton-Raphson division](/newton-raphson-division/).

## When to use it

Use Newton's method when $f'$ is available and cheap, a good starting point is known (from a model, a previous solve, or a few bisection steps), and the root is simple. Then it is hard to beat: from three correct digits, three or four steps give full binary64 accuracy. When $f'$ costs as much as $f$, the secant method is faster per evaluation. When no good start is known, use a bracketing method such as [Brent's method](/brent-method/), or the Newton bisection hybrid. For polynomials with many roots, use a method that finds all roots together ([polynomial root finding](/polynomial-root-finding/)).

## Pitfalls

- **A zero derivative.** For $f(x) = x^2 - 1$ and $x_0 = 0$, $f'(x_0) = 0$ and line L7 would divide by zero. Line L6 must test $d = 0$ and stop with a failure.
- **A cycle.** For $f(x) = x^3 - 2x + 2$ and $x_0 = 0$, the iterates are $0, 1, 0, 1, \ldots$ forever. Only the bound $k_{\max}$ of line L2 ends the loop; a version with `while true` in place of line L2 never stops.
- **Divergence.** For $f(x) = \arctan x$ and $x_0 = 1.5$, the iterates are $-1.694$, $2.321$, $-5.114$, $32.30$, $-1575$, growing without bound. Line L9 catches an overflow; a check that $|f|$ falls is the better fix.
- **An equality test.** For $x^2 - 2$ from $x_0 = 1$ in binary64 the iterates end in the cycle $1.414213562373095$, $1.4142135623730951$. A test $x_{\text{new}} = x$ in line L10 never passes. Use the relative step test with $\delta_r$ a small multiple of $u$.
- **A multiple root.** At a double root the method is linear with rate $1/2$, so it needs about 50 steps for binary64 accuracy instead of 6, and the step test of line L10 is then a weaker error estimate.
- **An inaccurate $f$.** Asking for a tolerance below the limiting accuracy $\varepsilon_f / |f'(x^*)|$ makes the loop run to $k_{\max}$. Choose $\delta_a$ and $\delta_r$ above it.

## Implementations

## History

Newton described the method around 1669, in *De analysi*, for the cubic $x^3 - 2x - 5 = 0$; he worked with a sequence of polynomials, not with derivatives. Raphson published in 1690 a simpler form that computes each new approximation from the original equation. Simpson gave in 1740 the general form with fluxions, for equations that are not polynomials, and applied it to systems of two equations. Ypma (1995) traces this history. Fourier studied the sign conditions under which the iterates approach the root from one side (Ostrowski, Chapter 9).

## References
