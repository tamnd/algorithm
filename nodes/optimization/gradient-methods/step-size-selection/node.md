---
tag: QEFMQS
kind: problem
slug: step-size-selection
name: Step size selection
aliases:
- line search problem
- choosing the learning rate
- step length selection
area: optimization/gradient-methods
level: core
summary: Given a point and a descent direction, choose how far to move. Too long a step can diverge and too short a step wastes work; line search conditions make the choice safe without knowing L_f.
prereqs: [gradient-descent]
see_also: [backtracking-line-search, exact-line-search, armijo-condition, wolfe-conditions, polyak-step-size, learning-rate-schedule, golden-section-search, adam]
sources:
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 3, Line search methods (Section 3.1, Step length; Section 3.2, Convergence of line search methods, with Zoutendijk's theorem; Section 3.5, Step-length selection algorithms)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.2, Descent methods (exact line search and backtracking line search)
  - book: isbn:9781886529052
    title: Dimitri P. Bertsekas, Nonlinear Programming, third edition, Athena Scientific, 2016
    locator: Chapter 1, Unconstrained optimization (the stepsize rules of gradient methods, namely minimization, limited minimization, Armijo, constant and diminishing stepsizes)
  - paper: doi:10.1093/imanum/8.1.141
    title: Jonathan Barzilai and Jonathan M. Borwein, Two-point step size gradient methods, IMA Journal of Numerical Analysis 8(1), 1988
    locator: pages 141 to 148 (the two-point step size)
---

Step size selection is the subproblem that every line search method solves at each iteration: given the current point $x$ and a descent direction $d$, with $\nabla f(x)^\top d < 0$, choose $\alpha > 0$ and move to $x + \alpha d$. A step that is too long can increase $f$ and make the method diverge; a step that is too short makes almost no progress. A constant step $1/L_f$ works when the [smoothness](/smoothness/) constant $L_f$ is known. Otherwise a line search picks $\alpha$ from values of $\varphi(\alpha) = f(x + \alpha d)$ and its derivative, and the [Armijo](/armijo-condition/) and [Wolfe conditions](/wolfe-conditions/) are enough to give global convergence.

## In plain words

A downhill method knows which way to go. It still has to decide how far to walk before it looks at the slope again. If it walks too far, it can pass the bottom of the valley and end up higher than before. If it walks only a tiny distance each time, it needs a very large number of steps.

There are a few common ways to decide. Use a fixed distance that is known to be safe. Look along the chosen line for the lowest point. Try a long distance and cut it in half until the result is good enough. Or use a rule computed from the last few steps. A good rule gives a clear decrease at each step without much extra work.

## Definition

**Input.** A differentiable $f : \mathbb{R}^n \to \mathbb{R}$, a point $x$, and a direction $d$ with $\nabla f(x)^\top d < 0$. Write $\varphi(\alpha) = f(x + \alpha d)$ for $\alpha \ge 0$, so $\varphi'(0) = \nabla f(x)^\top d < 0$.

**Output.** A step $\alpha > 0$ that meets the conditions required by the outer method. The common requirements are:

- *Exact minimization:* $\alpha \in \arg\min_{\alpha \ge 0}\varphi(\alpha)$ ([exact line search](/exact-line-search/)).
- *Sufficient decrease* ([Armijo condition](/armijo-condition/)): $\varphi(\alpha) \le \varphi(0) + c_1\alpha\varphi'(0)$ for a constant $c_1 \in (0, 1)$.
- *Sufficient decrease and curvature* ([Wolfe conditions](/wolfe-conditions/)): the Armijo condition and $\varphi'(\alpha) \ge c_2\varphi'(0)$ with $0 < c_1 < c_2 < 1$; the strong form asks $|\varphi'(\alpha)| \le c_2|\varphi'(0)|$.
- *Goldstein conditions:* $\varphi(0) + (1 - c)\alpha\varphi'(0) \le \varphi(\alpha) \le \varphi(0) + c\alpha\varphi'(0)$ with $c \in (0, \frac12)$.

**Why a condition is needed.** A decrease $f(x_{k+1}) < f(x_k)$ at each step is not enough for convergence. With $f(x) = x^2$, $x_0 = 2$ and the steps $x_{k+1} = x_k - \alpha_k f'(x_k)$ with $\alpha_k = 2^{-(k+3)}$, each step decreases $f$, but $x_k$ stays above $2\prod_{k \ge 0}(1 - 2^{-(k+2)}) > 1$, so it never reaches the minimizer $0$. The steps are too short. Steps that are too long relative to the decrease cause the opposite failure. The Wolfe conditions exclude both.

## Variants

- **Constant step.** $\alpha_k = \alpha$ for all $k$. For an $L_f$-smooth $f$, the step $\alpha \le 1/L_f$ gives the bounds of the [convergence theorem](/gradient-descent-convergence-theorem/), and every $\alpha \in (0, 2/L_f)$ decreases $f$ at each gradient step, since $f(x - \alpha g) \le f(x) - \alpha(1 - L_f\alpha/2)\|g\|^2$.
- **Steps from the problem constants.** $2/(\mu + L_f)$ for strongly convex $f$ ([linear convergence](/linear-convergence-strongly-convex/)), and the parameters of [momentum](/momentum-method/) and [Nesterov's method](/nesterov-accelerated-gradient/).
- **Exact line search.** Minimize $\varphi$; closed form for quadratics, otherwise approximate by bracketing and [golden-section search](/golden-section-search/).
- **Inexact line search.** [Backtracking line search](/backtracking-line-search/) for the Armijo condition; bracketing and zoom for the Wolfe conditions, as in the method of Moré and Thuente.
- **Polyak step.** $\alpha = (f(x) - f^*)/\|\nabla f(x)\|^2$ when $f^*$ is known ([Polyak step size](/polyak-step-size/)).
- **Barzilai-Borwein steps.** With $s = x_k - x_{k-1}$ and $y = \nabla f(x_k) - \nabla f(x_{k-1})$, $\alpha_k = s^\top s / s^\top y$ or $s^\top y / y^\top y$. The values of $f$ need not decrease at each step.
- **Diminishing steps.** $\alpha_k \to 0$ with $\sum_k\alpha_k = \infty$, often with $\sum_k\alpha_k^2 < \infty$, for subgradient methods and for [stochastic gradient descent](/stochastic-gradient-descent/), in the tradition of the [Robbins-Monro algorithm](/robbins-monro-algorithm/). A [learning rate schedule](/learning-rate-schedule/) sets such a sequence in practice.
- **Adaptive per-coordinate steps.** [AdaGrad](/adagrad/), [RMSProp](/rmsprop/) and [Adam](/adam/) scale each coordinate by a running estimate of past gradients.

## Examples

Gradient descent on $f(x) = \frac12(x_1^2 + 10x_2^2)$, with $L_f = 10$, $\mu = 1$ and $x_0 = (10, 1)$:

| step $\alpha$ | factor on $x_1$ | factor on $x_2$ | result |
|---|---|---|---|
| $0.1 = 1/L_f$ | $0.9$ | $0$ | converges, $153$ steps to $\|\nabla f\| \le 10^{-6}$ |
| $2/11 = 2/(\mu + L_f)$ | $9/11$ | $-9/11$ | converges, $83$ steps to $\|\nabla f\| \le 10^{-6}$ |
| $0.21 > 2/L_f$ | $0.79$ | $-1.1$ | diverges, $|x_2|$ grows by $1.1$ per step |

[Exact line search](/exact-line-search/) from the same start picks $\alpha = 2/11$ at every step on this function, and $f$ falls by the factor $(9/11)^2$ per step. [Backtracking](/backtracking-line-search/) with $\alpha_0 = 1$ and $\rho = \frac12$ needs no knowledge of $L_f$ and accepts a step of at least $\min(\alpha_0, \rho(1 - c_1)\cdot 2/L_f)$.

## Known algorithms

- [Backtracking line search](/backtracking-line-search/): shrink a trial step by a factor $\rho$ until the [Armijo condition](/armijo-condition/) holds.
- [Exact line search](/exact-line-search/): closed form on quadratics, or bracketing followed by [golden-section search](/golden-section-search/) or a safeguarded interpolation.
- Strong Wolfe line search by bracketing and zoom (Nocedal and Wright, Algorithms 3.5 and 3.6), used by [BFGS](/bfgs/), [L-BFGS](/limited-memory-bfgs/) and [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/).
- The Moré-Thuente line search, with guaranteed termination at a point that meets the strong Wolfe conditions.
- The [Polyak step size](/polyak-step-size/), and the Barzilai-Borwein step with a nonmonotone safeguard.

## Bounds

- **Zoutendijk's theorem.** If $f$ is bounded below and $L_f$-smooth, each $d_k$ is a descent direction, and each $\alpha_k$ meets the Wolfe conditions, then $\sum_k\cos^2\theta_k\|\nabla f(x_k)\|^2 < \infty$, where $\theta_k$ is the angle between $d_k$ and $-\nabla f(x_k)$. So $\nabla f(x_k) \to 0$ whenever the angles stay away from $90$ degrees. The proof is on the page of the [Wolfe conditions](/wolfe-conditions/).
- **Cost of backtracking.** With an $L_f$-smooth $f$, the Armijo condition along $d = -\nabla f(x)$ holds for every $\alpha \le 2(1 - c_1)/L_f$, so backtracking from $\alpha_0$ needs at most $\max(0, \lceil\log_{1/\rho}(\alpha_0 L_f/(2(1 - c_1)))\rceil)$ reductions per iteration.
- **Wolfe steps exist.** For a smooth $\varphi$ that is bounded below, an interval of steps meets the strong Wolfe conditions, and bracketing finds one in finitely many evaluations.
- **Exact line search does not fix conditioning.** On a quadratic with condition number $\kappa$, steepest descent with exact line search still has the worst-case factor $\left(\frac{\kappa - 1}{\kappa + 1}\right)^2$ per step on $f - f^*$.

## Reductions

- **To one-dimensional minimization.** Exact line search is the minimization of $\varphi$ on $[0, \infty)$. If $\varphi$ is [unimodal](/unimodal-function/) on a bracket, [golden-section search](/golden-section-search/) or [ternary search](/ternary-search/) solves it to any accuracy.
- **Quadratics.** For $f(x) = \frac12x^\top Ax - b^\top x$, $\varphi$ is a parabola, and the exact step is $\alpha = -\nabla f(x)^\top d / (d^\top Ad)$, as in the [conjugate gradient method](/conjugate-gradient-method/).
- **To a root of $\varphi'$.** For convex $\varphi$, exact line search is solving $\varphi'(\alpha) = 0$, for example by the [secant method](/secant-method/).

## Applications

- Every line search method: [gradient descent](/gradient-descent/), [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/), [quasi-Newton methods](/quasi-newton-method/), and damped Newton methods.
- The learning rate of [stochastic gradient descent](/stochastic-gradient-descent/) and its variants in machine learning, where the step is a tuned parameter or a schedule.
- Projected and proximal methods, where backtracking on the smoothness constant replaces the unknown $L_f$.

## References
