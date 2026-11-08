---
tag: XXZ87A
kind: algorithm
slug: shooting-method
name: Shooting method
aliases:
- single shooting
- multiple shooting
- simple shooting
area: numerical/differential-equations
level: core
summary: "Turn a two-point boundary value problem into root finding on the unknown initial values: integrate an initial value problem, compare with the far boundary condition, and correct by Newton's method."
solves: [bvp-boundary-value-problem]
model: real-ram
complexity:
  vars: {n: "the number of RK4 steps per solve", I: "the number of Newton iterations", K: "the number of segments, 1 for single shooting", C: "the cost of one evaluation of g, g_y and g_p (each is evaluated 4 n I times)"}
  time: {worst: "Θ(I (n C + K^3))"}
  space: {extra: "Θ(K^2)"}
  evaluations: {worst: "4 n I"}
properties: {deterministic: true, implicit: false, one_step: true, order: "that of the inner integrator, 4 with RK4", a_stable: false, symplectic: false}
history:
  year: 1962
  people: [D. D. Morrison, J. D. Riley, J. F. Zancanaro, Herbert B. Keller, Roland Bulirsch]
  note: The idea of aiming an initial value problem at a far target is old. Morrison, Riley and Zancanaro (1962) described multiple shooting, Keller (1968) gave the convergence theory for shooting, and Bulirsch and Stoer made multiple shooting a standard tool in the 1970s.
prereqs: [bvp-boundary-value-problem, newton-raphson-method, runge-kutta-methods]
see_also: [finite-difference-method, collocation-method, secant-method, sturm-liouville-problem, gronwall-inequality, condition-number]
sources:
  - book: isbn:9780387954523
    title: Josef Stoer and Roland Bulirsch, Introduction to Numerical Analysis, third edition, Springer, 2002
    locator: Section 7.3 (boundary value problems; simple shooting, its stability problems, and the multiple shooting method)
  - book: isbn:9780898713541
    title: Uri M. Ascher, Robert M. M. Mattheij and Robert D. Russell, Numerical Solution of Boundary Value Problems for Ordinary Differential Equations, SIAM, 1995
    locator: Chapter 4 (initial value methods, simple shooting, its conditioning, multiple shooting)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 7 (shooting and multiple shooting)
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.3 (convergence of one-step methods, used for the inner integrator)
  - paper: "D. D. Morrison, J. D. Riley and J. F. Zancanaro, Multiple shooting method for two-point boundary value problems, Communications of the ACM 5 (1962) 613-614"
    locator: the multiple shooting idea
---

The shooting method solves a two-point [boundary value problem](/bvp-boundary-value-problem/) such as $y'' = g(x, y, y')$, $y(a) = \alpha$, $y(b) = \beta$, by guessing the missing initial slope $s = y'(a)$, integrating the [initial value problem](/ode-initial-value-problem/) from $a$ to $b$, and adjusting $s$ until the computed $y(b)$ hits $\beta$. The adjustment is root finding on the scalar function $\Phi(s) = y(b; s) - \beta$, usually by the [Newton-Raphson method](/newton-raphson-method/). It reuses any good ODE integrator and inherits its order, but it fails when small changes of $s$ are amplified strongly across $[a, b]$. Multiple shooting splits the interval to fix that.

## In plain words

Think of a cannon that must hit a target at a known distance. You do not know the right angle, so you fire, see where the ball lands, and correct the angle. If the ball fell short, you aim higher; if it flew too far, you aim lower. After a few shots, you hit the target.

The shooting method does the same with an equation. One end of the curve is fixed, and so is the height at the other end, but the starting slope is unknown. Guess a slope, follow the equation across, and see how far you miss. Then use the rate at which the miss changes with the slope to make a better guess. When the equation magnifies tiny changes a lot, one long shot is hopeless, so you shoot over short pieces and make the pieces join up.

## The problem

Given $g : [a, b] \times \mathbb{R}^2 \to \mathbb{R}$ with partial derivatives $g_y$ and $g_p$ (where $p = y'$), boundary values $\alpha$ and $\beta$ and a start slope $s_0$, find $y$ with $y'' = g(x, y, y')$, $y(a) = \alpha$, $y(b) = \beta$. We write the second-order equation as the first-order system $u' = F(x, u)$ with $u = (y, y') \in \mathbb{R}^2$, so the page notation $y' = f(t, y)$ applies with $t = x$, $f = F$ and $d = 2$. A boundary value problem may have no solution, one, or several (the Bratu example below has two), so the method finds the solution whose slope is near $s_0$. The cost is the number of evaluations of $g$, $g_y$ and $g_p$, which is $4n$ of each per Newton iteration when the integrator is RK4 with $n$ steps.

## The algorithm

Let $w = \partial y / \partial s$. Differentiating the equation in $s$ gives the variational equation $w'' = g_y w + g_p w'$, $w(a) = 0$, $w'(a) = 1$, and $\Phi'(s) = w(b)$. Single shooting integrates $y$ and $w$ together:

```pseudo id=main
SHOOT(g, g_y, g_p, a, b, α, β, s0, n)
L1  s ← s0
L2  for k ← 1 to max_iter do
L3      (y_b, w_b) ← RK4 with n steps on (y, y', w, w') from (α, s, 0, 1), x from a to b
L4      r ← y_b − β;  if |r| ≤ tol·max(1, |β|) then return s
L5      s ← s − r / w_b                       ▷ Newton step; error if w_b = 0
L6      if |r / w_b| ≤ tol·(1 + |s|) then return s
L7  report failure
```

Line L3 is one initial value solve of a system of dimension 4. Line L4 measures the miss at the far end, and line L5 is the Newton correction. Line L6 stops when the correction is negligible, which matters when rounding keeps $|r|$ above the tolerance (see Pitfalls). Without $g_y$ and $g_p$, the [secant method](/secant-method/) replaces the derivative by a difference quotient of two misses, at one initial value solve of dimension 2 per iteration.

*Multiple shooting.* Split $[a, b]$ at $a = x_0 < x_1 < \cdots < x_K = b$. The unknowns are the slope $p_0$ at $a$ and the pairs $(y_k, p_k)$ at the inner nodes, $2K - 1$ numbers. Integrate from each node to the next and require that the end values match the next node's values, and that the last one hits $\beta$. This is a nonlinear system of $2K - 1$ equations, solved by Newton's method with the segment Jacobians from the variational equation. Its matrix is block bidiagonal.

## Example

Take $y'' = 2y^3$ on $[0, 1]$ with $y(0) = 1$, $y(1) = 1/2$. The exact solution is $y = 1/(1 + x)$, with slope $s^* = y'(0) = -1$. Newton from $s_0 = 0$ with RK4 and $n = 50$ steps gives:

| $k$ | $s_k$ | $\lvert r_k \rvert$ |
|---|---|---|
| 0 | 0 | 2.718 |
| 1 | -0.527384759259 | 8.948e-1 |
| 2 | -0.906372612535 | 1.500e-1 |
| 3 | -0.996882629641 | 4.837e-3 |
| 4 | -0.999996751768 | 5.080e-6 |
| 5 | -1.000000028871 | 5.602e-12 |

The number of correct digits roughly doubles per step, the mark of quadratic convergence. The final slope differs from $-1$ by about $2.9 \times 10^{-8}$. This is not rounding: it is the error of the discrete shooting function, which has its root at $s_h \ne s^*$. Its size against $n$ (observed):

| $n$ | 5 | 10 | 20 | 40 |
|---|---|---|---|---|
| $\lvert s_h + 1 \rvert$ | 3.023e-4 | 1.863e-5 | 1.144e-6 | 7.068e-8 |

Each halving of $h$ divides the error by about 16, so the observed order is 4, the order of RK4, as the theorem below predicts.

*Two solutions.* The Bratu problem $y'' = -e^y$, $y(0) = y(1) = 0$ has the solutions $y = -2 \ln\big(\cosh((x - \frac12)\theta/2) / \cosh(\theta/4)\big)$, where $\theta = \sqrt{2}\cosh(\theta/4)$, which has the two roots $\theta \approx 1.5171646$ and $\theta \approx 10.9387$. The initial slopes are $y'(0) = \theta\tanh(\theta/4)$, about $0.5493527$ and $10.8469$. Newton from $s_0 = 0$ or $s_0 = 5$ finds the small solution and from $s_0 = 10$ the large one. The start value selects the solution.

## Correctness

Line L3 integrates the variational equation with the same RK4 steps as the solution, and the result is exactly the derivative of the discrete shooting function $\Phi_h$, so line L5 is a true Newton step for $\Phi_h$ (Lemma 1 in the proof). Newton's method converges quadratically from close enough starting slopes to a root with $\Phi_h' \ne 0$.

**Theorem (proved).** Let $g \in C^4$ with $F$ Lipschitz in $u$ with constant $L$, and let $s^*$ be a simple root of the exact shooting function, $\Phi(s^*) = 0 \ne \Phi'(s^*)$. Then for $h$ small enough, $\Phi_h$ has a root $s_h$ near $s^*$, every such root satisfies $|s_h - s^*| \le C h^4 / m$ with $m$ a lower bound of $|\Phi'|$ near $s^*$, and the computed profile has max-norm error $O(h^4)$ on the grid, with constant $C + e^{L(b - a)} C/m$.

The proof uses the intermediate value theorem for the existence of $s_h$ and the [Gronwall inequality](/gronwall-inequality/) for the profile. It is in the proof file. The bound is for exact arithmetic; the factor $e^{L(b - a)}$ is what goes wrong in floating point.

## Complexity

Each Newton iteration is one RK4 solve of the system of dimension 4: $n$ steps, $4n$ evaluations each of $g$, $g_y$ and $g_p$, and $\Theta(n)$ further work. With $I$ iterations the total is $\Theta(I n C)$ and the extra space is $\Theta(1)$ (or $\Theta(d^2)$ for a system of dimension $d$ with $d/2$ unknown initial values, plus a $d/2 \times d/2$ linear solve per iteration). Near a simple root $I$ grows like $\log \log (1/\text{tol})$. Multiple shooting with $K$ segments of $n/K$ steps does the same integration work per iteration, plus a linear solve of size $2K - 1$. The dense elimination of the implementation takes $\Theta(K^3)$; a solver for the block bidiagonal structure takes $\Theta(K)$.

## Properties

- **Order.** The order of the inner integrator, here 4.
- **Deterministic.** Yes. Different start slopes can give different solutions.
- **Local convergence.** Quadratic for Newton, superlinear of order $(1 + \sqrt5)/2$ for the secant variant, both only from a good start.
- **Linear problems.** If $g$ is affine in $(y, y')$, then $\Phi_h$ is affine and one Newton step from any $s_0$ is exact up to rounding.
- **Conditioning.** A change $\delta$ in $s$ moves $y(b)$ by about $\Phi'(s)\delta$. For $y'' = \lambda^2 y$ on $[0, 1]$ this factor is $\sinh(\lambda)/\lambda$, so rounding in $s$ is amplified by $e^\lambda$.

## Variants and improvements

- **Secant shooting.** No derivatives of $g$; one solve of dimension 2 per iteration and order $(1 + \sqrt5)/2$.
- **Bisection shooting.** When two slopes with misses of opposite signs are known, [bisection](/bisection-method/) on $s$ is slow but safe.
- **Multiple shooting.** $K$ segments cut the amplification from $e^{\lambda(b - a)}$ to $e^{\lambda(b - a)/K}$ per segment (Stoer and Bulirsch, Section 7.3).
- **Systems and general boundary conditions.** For $u' = F(x, u)$ in $\mathbb{R}^d$ with conditions $B(u(a), u(b)) = 0$, the unknown is the whole start vector and the Jacobian is $d \times d$, from the fundamental matrix of the variational system.
- **Eigenvalue problems.** For [Sturm-Liouville problems](/sturm-liouville-problem/) one shoots on the eigenvalue instead of the slope.
- **Parameter continuation.** Solve a sequence of nearby problems and use each solution as the start of the next, to reach problems where a cold start fails.

## When to use it

Use single shooting for nonlinear boundary value problems on modest intervals where the solution modes neither grow nor decay fast, and when a good adaptive IVP solver is already at hand: it is short, uses little memory and keeps the accuracy of the integrator. Use multiple shooting when growth across the interval is large or when the initial value problem blows up for poor slopes. For stiff or strongly unstable problems, global methods such as [finite differences](/finite-difference-method/) or [collocation](/collocation-method/) are usually more robust (Ascher, Mattheij and Russell, Chapter 4).

## Pitfalls

- **Exponential amplification.** On $y'' = \lambda^2 y$, $y(0) = 1$, $y(1) = e^{-\lambda}$, with exact solution $e^{-\lambda x}$, RK4 with $n = 400$ gives these max-norm profile errors (observed): single shooting $1.22 \times 10^{-9}$ for $\lambda = 10$, $2.00 \times 10^{-8}$ for $\lambda = 20$, $7.09 \times 10^{-4}$ for $\lambda = 30$ and $10.2$ for $\lambda = 40$, where the computed $y(1)$ is $-10.23$ instead of $4 \times 10^{-18}$. The slope is right to about 16 digits, but $e^{40} \varepsilon$ is not small. Multiple shooting with $K = 10$ gives errors $1.2 \times 10^{-9}$, $1.5 \times 10^{-8}$, $4.2 \times 10^{-8}$ and $6.6 \times 10^{-8}$, each in one Newton iteration.
- **Residual tests that never pass.** With amplification $A$ the computed miss has noise about $A\varepsilon$, so a test $|r| \le 10^{-12}$ alone may loop forever. Line L6 also stops on a small Newton step.
- **Blow-up.** For a bad slope the initial value problem may blow up before $x = b$ (for $y'' = 2y^3$ with a positive slope, $y$ reaches infinity in finite $x$), giving overflow instead of a miss.
- **Critical points.** If $\Phi_h'(s) = 0$, the Newton step is undefined. For $y'' = -\pi^2 y$, $y(0) = 0$, $y(1) = 1$, every slope gives $y(1) \approx 0$, and indeed the problem has no solution.
- **Several solutions.** The start slope decides which solution is found; report it with the answer.

## Implementations

## History

Aiming an initial value problem at a far target is an old idea, named after gunnery. Morrison, Riley and Zancanaro (1962) proposed multiple shooting for two-point problems. Keller (1968) gave a convergence theory of shooting with the book Numerical Methods for Two-Point Boundary-Value Problems. Bulirsch, Stoer and their students developed multiple shooting into a robust method in the 1970s, as described in Stoer and Bulirsch (Section 7.3).

## References
