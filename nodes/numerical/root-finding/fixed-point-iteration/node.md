---
tag: KFHFSG
kind: algorithm
slug: fixed-point-iteration
name: Fixed-point iteration
aliases:
- functional iteration
- Picard iteration
- simple iteration
- successive substitution
area: numerical/root-finding
level: intro
summary: Repeat x ← g(x). If g is a contraction near the fixed point, the error shrinks by about |g'(x*)| at each step; the method of order q has g' to g^(q-1) zero at x*.
solves: [root-finding-problem]
model: real-ram
complexity:
  vars: {L: "a Lipschitz constant of g with L < 1", r: "the starting error |x0 - x*|", δ: "the tolerance"}
  time: {worst: "O(log(r/((1 - L)δ)) / log(1/L))"}
  space: {extra: Θ(1)}
  evaluations: {worst: "O(log(r/((1 - L)δ)) / log(1/L))"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true}
prereqs: [root-finding-problem, order-of-convergence]
see_also: [banach-fixed-point-theorem, newton-raphson-method, steffensen-method, aitken-delta-squared, halley-method, householder-methods, stopping-criteria, quadratic-convergence]
sources:
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 1, Solution of equations by iteration (simple iteration, the contraction mapping theorem on an interval, the rate of convergence)
  - book: isbn:9781305253667
    title: Richard L. Burden, J. Douglas Faires and Annette M. Burden, Numerical Analysis, tenth edition, Cengage, 2016
    locator: Section 2.2, Fixed-Point Iteration (Theorem 2.3 and the Fixed-Point Theorem 2.4) and Section 2.4, Error Analysis for Iterative Methods
  - book: "J. F. Traub, Iterative Methods for the Solution of Equations, Prentice-Hall, 1964"
    locator: Chapter 1 and Chapter 2 (one-point iteration functions, the order of an iteration function and its relation to the derivatives at the fixed point)
  - book: "A. M. Ostrowski, Solution of Equations and Systems of Equations, second edition, Academic Press, 1966"
    locator: the chapters on iteration and the convergence of x ← g(x) at a point of attraction
  - book: isbn:9780898713527
    title: C. T. Kelley, Iterative Methods for Linear and Nonlinear Equations, SIAM Frontiers in Applied Mathematics 16, 1995
    locator: Chapter 4, Local convergence and fixed point iteration
---

Fixed-point iteration solves $x = g(x)$ by the rule $x_{k+1} = g(x_k)$. A root of $f$ is a fixed point of $g(x) = x - \lambda f(x)$ for each $\lambda \ne 0$, and of many other rewrites, so the method is the common frame of the methods for the [root-finding problem](/root-finding-problem/). When $g$ is a contraction with constant $L < 1$ on an interval that it maps into itself, the [Banach fixed-point theorem](/banach-fixed-point-theorem/) gives convergence from every start in the interval, with the error at most $L^k$ times the first error. Near a fixed point the rate is $|g'(x^*)|$, and [Newton's method](/newton-raphson-method/) is the fixed-point iteration whose $g'$ is zero at the root, which makes it [quadratic](/quadratic-convergence/).

## In plain words

Some equations can be written as "the unknown equals a formula of the unknown". Then you can guess a value, put it in the formula, and use the result as the next guess. If the formula pulls guesses together, so that two guesses get closer after you apply it, the guesses settle down to the one value that the formula does not change. That value solves the equation. A calculator shows this: start with any number, and press the cosine key again and again, in radians. The display settles at 0.739085, the number whose cosine is itself. Not every rewrite works. If the formula pushes guesses apart, the guesses run away, even when you start close to the answer.

## The problem

The input is a function $g : I \to \mathbb{R}$ on an interval $I$, a start $x_0 \in I$, a tolerance $\delta > 0$, a maximum number of steps $k_{\max}$, and, when it is known, a Lipschitz constant $L < 1$ of $g$. The output is a point $\hat x$ with $|\hat x - x^*| \le \delta$ for a fixed point $x^* = g(x^*)$. To solve $f(x) = 0$, choose $g$ with the same fixed points as the roots of $f$, for example $g(x) = x - \lambda f(x)$.

Notation on the root-finding pages: $x_k$ are the iterates and $e_k = x_k - x^*$ the error. The method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C|e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f$ and its first $m - 1$ derivatives vanish there and $f^{(m)}$ does not. The cost is the number of evaluations of $g$; a method of order $q$ with $w$ evaluations in each step has efficiency index $q^{1/w}$.

## The algorithm

```pseudo id=main
FIXED-POINT(g, x0, δ, kmax, L)          ▷ L < 1 a Lipschitz constant of g, or unknown
L1  τ ← δ (1 − L)/L if L is known, else τ ← δ
L2  x ← x0
L3  for k ← 1 to kmax do
L4      y ← g(x)
L5      if y is NaN or infinite then error "the iteration diverged"
L6      if |y − x| ≤ τ then return y
L7      x ← y
L8  return x, with the flag "kmax reached"
```

Line L4 is the whole method. Line L6 stops when two iterates are close. With a known contraction constant $L$, the a posteriori bound $|x_{k+1} - x^*| \le \frac{L}{1 - L}|x_{k+1} - x_k|$ turns the test into a guarantee, which is why line L1 scales the tolerance. Without $L$ the test $|y - x| \le \delta$ is a heuristic: for $L$ close to 1 the error can be much larger than the step. Line L5 catches a run to infinity, and the bound $k_{\max}$ of line L3 ends a slow or cycling run.

## Example

Take $g(x) = \cos x$ and $x_0 = 1$. The cosine maps $[0, 1]$ into $[\cos 1, 1] \subset [0, 1]$, and $|g'(x)| = |\sin x| \le \sin 1 = 0.8415$ there, so $g$ is a contraction on $[0, 1]$. The fixed point is $x^* = 0.73908513321516064\ldots$, the Dottie number, and $g'(x^*) = -\sin x^* = -0.67361$.

| k | $x_k$ | $e_k$ | $e_k / e_{k-1}$ |
|---|---|---|---|
| 0 | 1.000000000000 | 2.609e−01 | |
| 1 | 0.540302305868 | −1.988e−01 | −0.7619 |
| 2 | 0.857553215846 | 1.185e−01 | −0.5960 |
| 3 | 0.654289790498 | −8.480e−02 | −0.7158 |
| 4 | 0.793480358743 | 5.440e−02 | −0.6415 |
| 5 | 0.701368773623 | −3.772e−02 | −0.6934 |
| 6 | 0.763959682901 | 2.487e−02 | −0.6595 |
| 8 | 0.750417761764 | 1.133e−02 | −0.6673 |
| 10 | 0.744237354901 | 5.152e−03 | −0.6708 |
| 12 | 0.741425086610 | 2.340e−03 | −0.6723 |

The ratio $e_k/e_{k-1}$ tends to $g'(x^*) = -0.67361$. The sign alternates because $g' < 0$, so the iterates lie on both sides of $x^*$. The method needs 55 steps to reach $|e_k| \le 10^{-10}$.

The rewrite matters. The root $x^* = 1.52137970680457$ of $f(x) = x^3 - x - 2$ is a fixed point of $g_1(x) = (x + 2)^{1/3}$ and of $g_2(x) = x^3 - 2$. Here $g_1'(x^*) = 0.14401$, and from $x_0 = 1$ the errors are $-5.214 \times 10^{-1}$, $-7.913 \times 10^{-2}$, $-1.148 \times 10^{-2}$, $-1.655 \times 10^{-3}$, falling by about $0.144$ per step. But $g_2'(x^*) = 6.9438$, and from $x_0 = 1.6$ the iterates are $2.096$, $7.208$, $372.5$, $5.17 \times 10^{7}$: they run away.

## Correctness

The main results are proved in [the correctness proof](proofs/correctness.md).

- **Global (proved).** If $g$ maps a closed interval $I$ into itself and $|g(x) - g(y)| \le L|x - y|$ on $I$ with $L < 1$, then $g$ has exactly one fixed point $x^*$ in $I$, the iterates converge to it from each $x_0 \in I$, and $|e_k| \le L^k |e_0|$ and $|x_k - x^*| \le \frac{L}{1-L}|x_k - x_{k-1}|$. This is the one-dimensional case of the [Banach fixed-point theorem](/banach-fixed-point-theorem/).
- **Local (proved).** If $g$ is $C^1$ near a fixed point $x^*$ and $|g'(x^*)| < 1$, there is $\rho > 0$ such that the iterates converge to $x^*$ from each $x_0$ with $|x_0 - x^*| \le \rho$, and $e_{k+1}/e_k \to g'(x^*)$.
- **Order $q$ (proved, local).** If $g$ is $C^q$ near $x^*$ with $q \ge 2$, $g'(x^*) = \cdots = g^{(q-1)}(x^*) = 0$ and $g^{(q)}(x^*) \ne 0$, then convergence is local of order exactly $q$ with $e_{k+1}/e_k^q \to g^{(q)}(x^*)/q!$.
- **Repulsion (proved).** If $|g'(x^*)| > 1$ and $g$ is $C^1$, no sequence of iterates converges to $x^*$ unless it lands on $x^*$ exactly.

## Complexity

The cost model is the number of evaluations of $g$, one per step, on a [real RAM](/real-ram/).

- **Steps.** Under the global hypothesis, $|e_k| \le L^k r$ with $r = |e_0|$, so $\lceil \log(r/\delta)/\log(1/L) \rceil$ steps make $|e_k| \le \delta$. The stop test of line L6 with the scaled tolerance $\tau = \delta(1-L)/L$ sees this a little later: it holds once $L^{k-1}|x_1 - x_0| \le \tau$, and $|x_1 - x_0| \le (1 + L) r$. So the method stops after $O(\log(r/((1-L)\delta))/\log(1/L))$ evaluations, one per step, with the exact bound in the proof.
- **Rate.** For linear convergence the number of correct digits grows by $\log_{10}(1/|g'(x^*)|)$ per step: about 0.17 for the cosine, 0.84 for $g_1$ above. For $|g'(x^*)|$ close to 1 the method is very slow.
- **Efficiency.** A method of order $q$ that uses one evaluation of $g$ has efficiency index $q$. But $g$ often costs several evaluations of $f$ and its derivatives: the Newton map uses $f$ and $f'$, so its index is $2^{1/2}$.
- **Space.** $\Theta(1)$.

### Floating point

Let the computed map be $\hat g(x) = g(x) + \eta$ with $|\eta| \le \varepsilon_g$. Under the global hypothesis, $|e_{k+1}| \le L|e_k| + \varepsilon_g$, so after enough steps $|e_k| \le \varepsilon_g/(1 - L)$ plus a term that falls like $L^k$. This is the limiting accuracy, and it is worse when $L$ is close to 1. In the root-finding form $g(x) = x - \lambda f(x)$, the error of $\lambda \hat f$ near a simple root gives $\varepsilon_g \approx |\lambda| \varepsilon_f$, and the best possible $\lambda = 1/f'(x^*)$ gives the usual limit $\varepsilon_f/|f'(x^*)|$. A tolerance below the limiting accuracy can make the test of line L6 fail forever, as the iterates move about in that small region, so the bound $k_{\max}$ is required.

## Properties

- **Local in general.** Outside the global hypothesis, the iterates can diverge, cycle (for example between two points) or behave chaotically, as for the logistic map $g(x) = 4x(1 - x)$.
- **One-sided or alternating.** If $0 < g'(x^*) < 1$, the iterates approach from one side; if $-1 < g'(x^*) < 0$, they alternate around $x^*$, as in the example.
- **Multiple roots.** For a root of multiplicity $m \ge 2$, the Newton map has $g'(x^*) = 1 - 1/m$, so Newton's method becomes a linear fixed-point iteration with rate $1 - 1/m$.
- **Self-correcting.** An error in one step is damped by later steps, as the floating-point bound shows.

## Variants and improvements

- **Relaxation.** Iterate $g_\lambda(x) = x - \lambda f(x)$ and choose $\lambda \approx 1/f'(x^*)$, which makes $g_\lambda'(x^*) \approx 0$. With $\lambda = 1/f'(x_k)$ at each step, this is [Newton's method](/newton-raphson-method/).
- **Aitken and Steffensen.** [Aitken's $\Delta^2$ process](/aitken-delta-squared/) extrapolates three iterates of a linear iteration. [Steffensen's method](/steffensen-method/) restarts the iteration from the extrapolated value, which gives order 2 with two evaluations of $g$ per step and no derivative.
- **Higher order.** [Halley's method](/halley-method/) and the [Householder methods](/householder-methods/) are fixed-point iterations of order 3 and more.
- **Systems.** In $\mathbb{R}^n$ the same rule converges when $g$ is a contraction in some norm; the local rate is the [spectral radius](/spectral-radius/) of the Jacobian at $x^*$. The [Jacobi](/jacobi-method/) and [Gauss-Seidel](/gauss-seidel-method/) methods for linear systems are fixed-point iterations.

## When to use it

Use the plain iteration when the problem already has the form $x = g(x)$ with a strong contraction, as in many equilibrium and self-consistency problems, or when $g$ is cheap and $|g'(x^*)|$ is small. Use it to analyse other methods: each one-point method is a fixed-point iteration, and its order comes from the derivatives of $g$ at $x^*$. For a root of a smooth $f$ with a cheap derivative, Newton's method is faster. When a bracket is known, [bisection](/bisection-method/) or [Brent's method](/brent-method/) gives a guarantee that the plain iteration does not.

## Pitfalls

- **A rewrite that repels.** $x = x^3 - 2$ has the same root as $x^3 - x - 2 = 0$, but $|g'(x^*)| = 6.94 > 1$, and the iterates run away. Check $|g'| < 1$ near the root before you use line L4 with a given $g$.
- **The step is not the error.** The test $|y - x| \le \delta$ in line L6 does not give $|y - x^*| \le \delta$ when $L > 1/2$. For $L = 0.99$ the error can be 99 times the step. Use $\tau = \delta(1 - L)/L$ when $L$ is known, as line L1 does.
- **A tolerance below the noise.** With $\delta$ below $\varepsilon_g/(1 - L)$, the test of line L6 may never hold. Keep the bound $k_{\max}$ of line L3.
- **A map that leaves the interval.** The global result needs $g(I) \subseteq I$. A map such as $g(x) = \sqrt{x - 3}$ can leave its domain, and then $g$ returns NaN; line L5 catches it.
- **Overflow.** A divergent run can overflow to infinity in a few steps, as $g_2$ above does; then $|y - x|$ is NaN and the test of line L6 is false for every step. Line L5 must come before line L6.

## Implementations

## History

The rule $x \leftarrow g(x)$ is as old as the methods that it describes, such as Newton's method. The contraction form of the convergence proof is due to Banach (1922) for general complete metric spaces. Ostrowski and Traub (1964) built the theory of the order of one-point iteration functions from the derivatives of $g$ at the fixed point (Traub, Chapters 1 and 2).

## References
