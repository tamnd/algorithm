---
tag: NP62PK
kind: problem
slug: unconstrained-smooth-minimization
name: Unconstrained smooth minimization
aliases:
- smooth unconstrained optimization
- unconstrained minimization
area: optimization/gradient-methods
level: intro
summary: Minimize a differentiable function over all of R^n, given an oracle for its value and gradient. The model problem of gradient methods, with matching bounds on gradient calls.
prereqs: [gradient, smoothness]
see_also: [gradient-descent, nesterov-accelerated-gradient, first-order-lower-bound, constrained-smooth-minimization, convex-optimization-problem, limited-memory-bfgs, strong-convexity, finite-sum-minimization]
sources:
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Chapter 1, Nonlinear optimization (Section 1.1.3 for the complexity of global optimization, Section 1.2 for local methods), and Chapter 2, Smooth convex optimization (Sections 2.1 and 2.2 for the lower and upper bounds)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 2, Fundamentals of unconstrained optimization (Section 2.1, the optimality conditions, Theorems 2.2 to 2.5)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Chapter 9, Unconstrained minimization (Section 9.1, the problem and its assumptions)
  - paper: doi:10.1007/s10107-019-01406-y
    title: Yair Carmon, John C. Duchi, Oliver Hinder and Aaron Sidford, Lower bounds for finding stationary points I, Mathematical Programming 184, 2020
    locator: pages 71 to 120 (the lower bound of order ε^(-2) for first-order methods on smooth nonconvex functions)
  - paper: doi:10.1007/BF02592948
    title: Katta G. Murty and Santosh N. Kabadi, Some NP-complete problems in quadratic and nonlinear programming, Mathematical Programming 39(2), 1987
    locator: pages 117 to 129 (copositivity and the hardness of global and local minimization)
---

Unconstrained smooth minimization asks for a point that minimizes a differentiable function $f : \mathbb{R}^n \to \mathbb{R}$ over all of $\mathbb{R}^n$, when the algorithm can only ask an oracle for $f(x)$ and the [gradient](/gradient/) $\nabla f(x)$ at points of its choice. For convex $f$ with an $L_f$-Lipschitz gradient, the number of oracle calls needed for accuracy $\varepsilon$ is $\Theta(\sqrt{L_f R^2 / \varepsilon})$ in high dimension: [Nesterov's accelerated method](/nesterov-accelerated-gradient/) reaches it and the [first-order lower bound](/first-order-lower-bound/) shows that no method does better. It is the model problem of all gradient methods, and the inner problem of many constrained methods.

## In plain words

You have a formula or a program that gives a number for each setting of some dials, and you want the setting with the smallest number. There are no rules on the dials: each one can take any real value. You can ask, for any setting, for the number and for the slope in each dial direction. You cannot see the whole landscape at once.

The question is how few questions you need to get close to the best value. The answer depends on how curved the landscape can be, on how far the start is from the best setting, and on whether the landscape is a single bowl. For a bowl, good methods exist and their cost is known exactly. For a landscape with many valleys, finding the deepest one is hard in general, and methods aim only for a flat spot.

## Definition

**Input.** A function $f : \mathbb{R}^n \to \mathbb{R}$ that is differentiable, given by a *first-order oracle* that returns $(f(x), \nabla f(x))$ for each query point $x$; a start point $x_0$; and an accuracy $\varepsilon > 0$.

**Output.** For a function that has a minimizer, a point $x$ with $f(x) - f^* \le \varepsilon$, where $f^* = \min_x f(x)$. For a nonconvex function, the usual goal is weaker: a point $x$ with $\|\nabla f(x)\| \le \varepsilon$ (an $\varepsilon$-stationary point).

**The classes of functions.** The bounds are stated for classes, with the notation of all optimization pages:

- $\mathcal{F}_{L_f}$: convex and $L_f$-[smooth](/smoothness/) functions with a minimizer $x^*$. The size of an instance is $R = \|x_0 - x^*\|$ (for the minimizer nearest to $x_0$).
- $\mathcal{S}_{\mu, L_f}$: functions in $\mathcal{F}_{L_f}$ that are also $\mu$-[strongly convex](/strong-convexity/), with $\kappa = L_f / \mu$.
- $L_f$-smooth functions that are bounded below, with no convexity. The size is $f(x_0) - \inf f$.

**Optimality conditions.** Let $f$ be differentiable.

1. If $x^*$ is a local minimizer, then $\nabla f(x^*) = 0$ (proved on the [gradient](/gradient/) page). If $f$ is twice continuously differentiable, also $\nabla^2 f(x^*) \succeq 0$.
2. If $f$ is twice continuously differentiable, $\nabla f(x^*) = 0$ and $\nabla^2 f(x^*) \succ 0$, then $x^*$ is a strict local minimizer.
3. If $f$ is [convex](/convex-function/), then $\nabla f(x^*) = 0$ if and only if $x^*$ is a global minimizer.

**Existence.** A minimizer need not exist ($f(x) = e^x$). It exists when $f$ is continuous and *coercive*, that is, $f(x) \to \infty$ as $\|x\| \to \infty$. *Proof.* The level set $\{x : f(x) \le f(x_0)\}$ is closed because $f$ is continuous, and bounded because $f$ is coercive. A continuous function attains its minimum on a nonempty compact set, and a minimizer on the level set is a global minimizer. $\square$ A strongly convex function is coercive, so it has a minimizer, and the minimizer is unique.

## Variants

- **Exact or approximate.** The exact minimizer is rarely computable in finite time; iterative methods reach $f(x) - f^* \le \varepsilon$, $\|x - x^*\| \le \varepsilon$ or $\|\nabla f(x)\| \le \varepsilon$. For convex $L_f$-smooth $f$, $\|\nabla f(x)\|^2 \le 2 L_f (f(x) - f^*)$, so a value bound gives a gradient bound.
- **Global or local.** For nonconvex $f$, the global problem is hard (see the bounds), and practical methods find stationary points or local minimizers.
- **Quadratic.** $f(x) = \frac12 x^\top A x - b^\top x$ with $A$ symmetric [positive definite](/positive-definite-matrix/) is the same problem as the linear system $Ax = b$. The [conjugate gradient method](/conjugate-gradient-method/) solves it in at most $n$ steps in exact arithmetic.
- **Finite sums.** $f = \frac{1}{m}\sum_{i=1}^m f_i$ with a cheap oracle for each $f_i$ is the [finite-sum minimization](/finite-sum-minimization/) problem of machine learning, where [stochastic gradient descent](/stochastic-gradient-descent/) and its variance-reduced forms apply.
- **Composite.** $f = g + h$ with smooth $g$ and a simple nonsmooth $h$ is [composite minimization](/composite-minimization/), solved by the [proximal gradient method](/proximal-gradient-method/).
- **With constraints.** Minimization over a convex set is [constrained smooth minimization](/constrained-smooth-minimization/).
- **Other oracles.** A zeroth-order oracle gives only $f(x)$ ([derivative-free optimization](/derivative-free-optimization/)). A second-order oracle also gives $\nabla^2 f(x)$, as in Newton's method.

## Examples

- **Least squares.** $f(x) = \frac12 \|Ax - b\|^2$ is convex and $L_f$-smooth with $L_f = \lambda_{\max}(A^\top A)$. The minimizers solve the [normal equations](/normal-equations/) $A^\top A x = A^\top b$. It is strongly convex exactly when $A$ has full column rank.
- **Logistic regression.** $f(w) = \frac{1}{m}\sum_i \log(1 + e^{-y_i a_i^\top w})$ is convex and smooth but has no closed-form minimizer, and if the data are linearly separable it has no minimizer at all: $f$ tends to $0$ along a separating direction. Adding $\frac{\lambda}{2}\|w\|^2$ makes it $\lambda$-strongly convex.
- **The Rosenbrock function.** $f(x_1, x_2) = (1 - x_1)^2 + 100 (x_2 - x_1^2)^2$ is nonconvex, with the unique minimizer $(1, 1)$ and $f^* = 0$, at the end of a curved narrow valley. The standard start is $(-1.2, 1)$, where $f = 24.2$ and $\nabla f = (-215.6, -88)$. Gradient methods move slowly along the valley; quasi-Newton methods such as [BFGS](/bfgs/) solve it in a few dozen steps.
- **A nonconvex function with a simple landscape.** $f(x) = x^2 + 3\sin^2 x$ has $f^* = 0$ at $x^* = 0$ and is not convex, but it satisfies the [Polyak-Lojasiewicz condition](/polyak-lojasiewicz-condition/), so gradient descent still converges at a linear rate.
- **No solution.** $f(x) = \log(1 + e^{x})$ is convex and $\frac14$-smooth with $\inf f = 0$, but no point attains it. $f(x) = x_1^2 - x_2^2$ is unbounded below.

## Known algorithms

| algorithm | class | gradient calls for accuracy $\varepsilon$ |
|---|---|---|
| [gradient descent](/gradient-descent/), step $1/L_f$ | $\mathcal{F}_{L_f}$ | $L_f R^2 / (2\varepsilon)$ |
| [gradient descent](/gradient-descent/), step $1/L_f$ | $\mathcal{S}_{\mu, L_f}$ | $\kappa \ln((f(x_0) - f^*)/\varepsilon)$ |
| [gradient descent](/gradient-descent/), step $1/L_f$ | smooth, bounded below, $\|\nabla f\| \le \varepsilon$ | $2 L_f (f(x_0) - f^*)/\varepsilon^2$ |
| [Nesterov's accelerated gradient](/nesterov-accelerated-gradient/) | $\mathcal{F}_{L_f}$ | $\sqrt{2 L_f R^2 / \varepsilon}$ |
| [Nesterov's accelerated gradient](/nesterov-accelerated-gradient/), constant momentum | $\mathcal{S}_{\mu, L_f}$ | $O(\sqrt{\kappa} \log(1/\varepsilon))$ |
| [heavy ball momentum](/momentum-method/) | strongly convex quadratics | $O(\sqrt{\kappa} \log(1/\varepsilon))$ |
| [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/) | smooth | convergence of $\liminf \|\nabla f(x_k)\|$ to $0$ under line search conditions |
| [BFGS](/bfgs/), [L-BFGS](/limited-memory-bfgs/) | smooth, strongly convex near $x^*$ | superlinear (BFGS) or linear (L-BFGS) local rate |
| Newton's method ([for systems](/newton-method-for-systems/), on $\nabla f = 0$) | twice differentiable, $\nabla^2 f(x^*) \succ 0$ | quadratic local rate, one Hessian solve per step |

The step size rules ([exact line search](/exact-line-search/), [backtracking line search](/backtracking-line-search/), the [Wolfe conditions](/wolfe-conditions/), the [Polyak step size](/polyak-step-size/)) make these methods work without the knowledge of $L_f$. [Coordinate descent](/coordinate-descent/) uses one partial derivative per step.

## Bounds

All bounds count oracle calls of a deterministic first-order method, in the worst case over the class.

- **Convex and smooth.** Upper bound $O(\sqrt{L_f R^2/\varepsilon})$ by Nesterov's method. Lower bound $\Omega(\sqrt{L_f R^2/\varepsilon})$: for each $k \le (n - 1)/2$ there is a convex quadratic in $\mathcal{F}_{L_f}$ on which every method whose iterates lie in the span of the past gradients has $f(x_k) - f^* \ge 3 L_f R^2 / (32 (k+1)^2)$ ([first-order lower bound](/first-order-lower-bound/)). So the complexity is $\Theta(\sqrt{L_f R^2/\varepsilon})$ when $n$ is large enough.
- **Strongly convex and smooth.** $\Theta(\sqrt{\kappa}\log(1/\varepsilon))$ calls, with the upper bound by Nesterov's method and the lower bound by Nesterov's worst-case quadratic in infinite dimension.
- **Smooth, nonconvex, $\varepsilon$-stationary point.** Gradient descent needs $O(L_f (f(x_0) - f^*)/\varepsilon^2)$ calls. Carmon, Duchi, Hinder and Sidford proved a lower bound of the same order $\varepsilon^{-2}$ for every first-order method, when the dimension may grow with $1/\varepsilon$. So gradient descent is optimal for this goal, up to a constant factor.
- **Global minimization of nonconvex functions.** For Lipschitz functions on a box, every method needs a number of calls exponential in $n$ to reach accuracy $\varepsilon$ (Nesterov, Section 1.1.3). In the Turing model, global minimization of a polynomial of degree 4 is NP-hard: Murty and Kabadi showed that testing the copositivity of a matrix $Q$, which is the nonnegativity of $\sum_{i,j} Q_{ij} x_i^2 x_j^2$, is co-NP-complete.
- **Small dimension.** When $n$ is small compared to the number of steps, cutting-plane methods such as the [ellipsoid method](/ellipsoid-method/) need $O(n^2 \log(1/\varepsilon))$ oracle calls on convex problems, so the lower bound above needs $n \ge 2k + 1$.

## Reductions

- **Linear systems.** Solving $Ax = b$ with $A$ symmetric positive definite is minimizing $\frac12 x^\top A x - b^\top x$, since the gradient is $Ax - b$. Each first-order method is a linear system solver, and the [conjugate gradient method](/conjugate-gradient-method/) is the optimal one on this class.
- **Nonlinear equations.** A root of $F : \mathbb{R}^n \to \mathbb{R}^n$ is a global minimizer of $\frac12 \|F(x)\|^2$ with value $0$. The converse direction can fail: a local minimizer with a positive value is not a root.
- **Constrained problems.** Penalty, [barrier](/barrier-method/) and [augmented Lagrangian](/augmented-lagrangian-method/) methods replace a constrained problem by a sequence of unconstrained smooth problems.
- **Maximization.** Maximizing $f$ is minimizing $-f$.

## Applications

- Training of models in machine learning: [linear regression](/linear-regression/), [logistic regression](/logistic-regression/), [ridge regression](/ridge-regression/) and neural networks trained by [backpropagation](/backpropagation/).
- Maximum likelihood estimation in statistics, where $f$ is the negative log-likelihood.
- Inverse problems such as image reconstruction, as least squares with a smooth regularizer.
- The inner solves of [interior-point methods](/interior-point-method/) and [augmented Lagrangian methods](/augmented-lagrangian-method/).

## References
