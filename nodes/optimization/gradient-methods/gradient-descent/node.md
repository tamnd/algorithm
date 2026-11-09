---
tag: WZ9ATZ
kind: algorithm
slug: gradient-descent
name: Gradient descent
aliases:
- steepest descent
- gradient method
- method of steepest descent
area: optimization/gradient-methods
level: intro
summary: Minimize a differentiable function by steps against the gradient, x_(k+1) = x_k - α ∇f(x_k). Step 1/L_f gives error L_f R^2/(2k) on convex f and a linear rate on strongly convex f.
solves: [unconstrained-smooth-minimization]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, D: "L_f R^2 (the smoothness constant times the squared distance from x_0 to x*)", ε: the target accuracy, κ: the condition number L_f/μ}
  time: {worst: O(k n)}
  space: {extra: O(n)}
  gradients: {convex: O(D/ε), strongly_convex: O(κ log(1/ε)), step: "1"}
properties: {deterministic: true, iterative: true, descent_method: true, first_order: true}
history:
  year: 1847
  people: [Augustin-Louis Cauchy, Haskell B. Curry, Boris T. Polyak]
  note: Cauchy proposed the method in 1847 to solve systems of equations. Curry studied it for nonlinear minimization in 1944.
prereqs: [gradient, smoothness, unconstrained-smooth-minimization]
see_also: [gradient-descent-convergence-theorem, linear-convergence-strongly-convex, backtracking-line-search, exact-line-search, nesterov-accelerated-gradient, stochastic-gradient-descent, projected-gradient-descent, first-order-lower-bound]
sources:
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Section 1.2.3, The gradient method (nonconvex case), and Section 2.1.5, The gradient method (convex and strongly convex cases)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.3, Gradient descent method (convergence analysis and the examples of 9.3.2)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 3, Line search methods (Section 3.3, the rate of convergence of steepest descent)
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Section 3.2, Gradient descent for smooth functions, and Section 3.4.2, Strongly convex and smooth functions
  - paper: doi:10.1090/qam/10667
    title: Haskell B. Curry, The method of steepest descent for non-linear minimization problems, Quarterly of Applied Mathematics 2(3), 1944
    locator: pages 258 to 261
  - paper: doi:10.1007/s10107-013-0653-0
    title: Yoel Drori and Marc Teboulle, Performance of first-order methods for smooth convex minimization, a novel approach, Mathematical Programming 145, 2014
    locator: the exact worst case L_f R^2/(4k + 2) of gradient descent with step 1/L_f
  - paper: doi:10.4171/dms/6/27
    title: Claude Lemaréchal, Cauchy and the gradient method, Documenta Mathematica, Extra Volume Optimization Stories, 2012
    locator: pages 251 to 254 (the 1847 note of Cauchy and its context)
  - paper: doi:10.1016/0041-5553(63)90382-3
    title: Boris T. Polyak, Gradient methods for the minimisation of functionals, USSR Computational Mathematics and Mathematical Physics 3(4), 1963
    locator: pages 864 to 878 (the linear rate under the gradient dominance condition)
---

Gradient descent minimizes a differentiable function $f : \mathbb{R}^n \to \mathbb{R}$ by repeated steps against the [gradient](/gradient/): $x_{k+1} = x_k - \alpha \nabla f(x_k)$. It solves the [unconstrained smooth minimization](/unconstrained-smooth-minimization/) problem with one gradient evaluation and $O(n)$ arithmetic per step. For a convex function with an $L_f$-Lipschitz gradient ([smoothness](/smoothness/)) and the step $\alpha = 1/L_f$, the error after $k$ steps is at most $L_f R^2 / (2k)$, where $R$ is the distance from the start to a minimizer. For a [strongly convex](/strong-convexity/) function the error falls by the factor $1 - \mu / L_f$ at each step. It is the base of almost every method for large problems, from [stochastic gradient descent](/stochastic-gradient-descent/) to [accelerated methods](/nesterov-accelerated-gradient/).

## In plain words

You stand on a hill in fog and you want to reach the lowest point. You cannot see the valley, but you can feel the slope under your feet. The slope tells you which way is uphill and how steep it is. So you take a step in the opposite direction, downhill, and you make the step longer where the hill is steeper. Then you feel the slope again and repeat.

If the steps are short enough, each step takes you lower. If they are too long, you jump over the valley and land higher on the other side, and the walk can go up without limit. On a long narrow valley the walk goes from side to side in a zigzag, and it moves slowly along the floor of the valley. The ratio of the steepest to the flattest direction decides how slow this is.

## The problem

The input is a function $f : \mathbb{R}^n \to \mathbb{R}$ that is differentiable, an oracle that returns $\nabla f(x)$ for a given $x$, a start point $x_0$, a step size $\alpha > 0$, an iteration limit $K$ and a tolerance $\varepsilon_g \ge 0$. The output is a point $x$, the last iterate.

The page uses the notation of all optimization pages: $n$ is the number of variables, $x^*$ is a minimizer and $f^* = f(x^*)$, $L_f$ is the smoothness constant ($\|\nabla f(x) - \nabla f(y)\| \le L_f \|x - y\|$), $\mu$ is the strong convexity constant, $\kappa = L_f / \mu$ is the [condition number](/condition-number-of-an-optimization-problem/), and $R = \|x_0 - x^*\|$. All norms are Euclidean. The accuracy target is $f(x_k) - f^* \le \varepsilon$ for convex $f$, and $\|\nabla f(x_k)\| \le \varepsilon$ when $f$ is not convex.

## The algorithm

```pseudo id=main
GRADIENT-DESCENT(∇f, x₀, α, K, ε_g)
L1  x ← x₀
L2  for k ← 0 to K − 1 do
L3      g ← ∇f(x)                         ▷ one call of the gradient oracle
L4      if ‖g‖ ≤ ε_g then return x        ▷ an approximate stationary point
L5      x ← x − α g
L6  return x
```

Line L3 asks the oracle for the gradient at the current point. Line L4 stops when the gradient is small, because then no direction gives a large first-order decrease. Line L5 moves against the gradient. Among all directions $d$ with $\|d\| = 1$, the directional derivative $\nabla f(x)^\top d$ is smallest for $d = -\nabla f(x) / \|\nabla f(x)\|$, by the Cauchy-Schwarz inequality, so $-g$ is the direction of steepest descent in the Euclidean norm.

The step $\alpha$ is the only parameter. The theory uses a fixed $\alpha = 1/L_f$, or $\alpha = 2/(\mu + L_f)$ when $\mu$ is also known. When $L_f$ is not known, a [backtracking line search](/backtracking-line-search/) finds an acceptable step at each iteration, and an [exact line search](/exact-line-search/) takes the best step along $-g$. The page [step size selection](/step-size-selection/) compares the rules.

## Example

Take $f(x) = \tfrac12 (x_1^2 + 10 x_2^2)$, so $\nabla f(x) = (x_1, 10 x_2)$, $x^* = (0, 0)$, $f^* = 0$, $\mu = 1$, $L_f = 10$ and $\kappa = 10$. Start at $x_0 = (10, 1)$, where $f(x_0) = 55$. Each coordinate is multiplied by $1 - \alpha \lambda$ at each step, with $\lambda = 1$ for $x_1$ and $\lambda = 10$ for $x_2$.

| $k$ | $x_k$, $\alpha = 0.1 = 1/L_f$ | $f(x_k)$ | $x_k$, $\alpha = 2/11$ | $f(x_k)$ | $x_k$, $\alpha = 0.21$ | $f(x_k)$ |
|---|---|---|---|---|---|---|
| 0 | (10, 1) | 55 | (10, 1) | 55 | (10, 1) | 55 |
| 1 | (9, 0) | 40.5 | (8.1818, −0.8182) | 36.8182 | (7.9, −1.1) | 37.2550 |
| 2 | (8.1, 0) | 32.805 | (6.6942, 0.6694) | 24.6469 | (6.2410, 1.21) | 26.7955 |
| 3 | (7.29, 0) | 26.5720 | (5.4771, −0.5477) | 16.4992 | (4.9304, −1.3310) | 21.0122 |
| 4 | (6.561, 0) | 21.5234 | (4.4813, 0.4481) | 11.0449 | (3.8950, 1.4641) | 18.3035 |
| 5 | (5.9049, 0) | 17.4339 | (3.6665, −0.3666) | 7.3937 | (3.0771, −1.6105) | 17.7029 |
| 6 | (5.3144, 0) | 14.1215 | (2.9998, 0.3000) | 4.9495 | (2.4309, 1.7716) | 18.6467 |

- With $\alpha = 1/L_f$, the steep coordinate $x_2$ is gone after one step, and $x_1$ shrinks by the factor $0.9$ per step. So $f$ shrinks by $0.81$ per step. The proved bounds are $f(x_k) \le L_f R^2 / (2k) = 505 / k$ and $f(x_k) \le 0.9^k \cdot 55$, for example $49.5$ at $k = 1$ and $29.23$ at $k = 6$. Both hold, and the second one is much closer.
- With $\alpha = 2/(\mu + L_f) = 2/11$, both coordinates shrink by the factor $9/11 = (\kappa - 1)/(\kappa + 1)$, and $x_2$ changes sign at each step. This is the zigzag. The tolerance $\|\nabla f\| \le 10^{-6}$ is met after 83 steps, against 153 steps with $\alpha = 0.1$.
- With $\alpha = 0.21 > 2/L_f$, the factor of $x_2$ is $1 - 2.1 = -1.1$, so $|x_2|$ grows by $10\%$ per step. The value $f$ falls for five steps, because $x_1$ still shrinks, and then it grows without limit.

## Correctness

Gradient descent always returns a point. What it guarantees depends on the class of $f$. Let $f$ be $L_f$-smooth and bounded below, and $0 < \alpha \le 1/L_f$.

1. **Descent.** $f(x_{k+1}) \le f(x_k) - \frac{\alpha}{2} \|\nabla f(x_k)\|^2$. So $f$ does not increase, and it falls strictly while $\nabla f(x_k) \ne 0$.
2. **Stationarity, no convexity needed.** $\min_{0 \le i < k} \|\nabla f(x_i)\|^2 \le \dfrac{2 (f(x_0) - f^*)}{\alpha k}$.
3. **Convex $f$ with a minimizer $x^*$.** $f(x_k) - f^* \le \dfrac{\|x_0 - x^*\|^2}{2 \alpha k}$, and with $\alpha = 1/L_f$ this is $\dfrac{L_f R^2}{2k}$. The distance $\|x_k - x^*\|$ does not increase.
4. **$\mu$-strongly convex $f$ and $\alpha = 1/L_f$.** $f(x_k) - f^* \le (1 - \mu/L_f)^k (f(x_0) - f^*)$ and $\|x_k - x^*\|^2 \le (1 - \mu/L_f)^k R^2$.

All four follow from the descent lemma $f(y) \le f(x) + \nabla f(x)^\top (y - x) + \frac{L_f}{2} \|y - x\|^2$ of [smoothness](/smoothness/). For claim 3, convexity gives $f(x_k) - f^* \le \nabla f(x_k)^\top (x_k - x^*)$. With the descent lemma this becomes a telescoping bound,

$$f(x_{k+1}) - f^* \le \frac{1}{2\alpha} \left( \|x_k - x^*\|^2 - \|x_{k+1} - x^*\|^2 \right).$$

Sum it over $k$ and use that $f(x_k)$ does not increase. The full proofs of the four claims are in the proof below. The theorem pages [convergence of gradient descent for smooth convex functions](/gradient-descent-convergence-theorem/) and [linear convergence under strong convexity](/linear-convergence-strongly-convex/) give the tightness examples. Under the weaker [Polyak-Lojasiewicz condition](/polyak-lojasiewicz-condition/), the rate of claim 4 for $f$ still holds without convexity.

## Complexity

**Cost of one iteration.** Line L3 is one gradient evaluation. Lines L4 and L5 take $O(n)$ arithmetic operations on the [real RAM](/real-ram/). So $k$ iterations take $k$ gradient evaluations and $O(kn)$ further operations. The extra space is $O(n)$ for $x$ and $g$.

**Number of iterations.** Set the right side of each claim to the target and solve for $k$. With $\alpha = 1/L_f$:

- Convex: $k \ge L_f R^2 / (2\varepsilon)$ steps give $f(x_k) - f^* \le \varepsilon$. This is $O(D / \varepsilon)$ with $D = L_f R^2$, a sublinear rate.
- Strongly convex: since $1 - \mu/L_f \le e^{-1/\kappa}$, $k \ge \kappa \ln\left((f(x_0) - f^*)/\varepsilon\right)$ steps suffice. This is $O(\kappa \log(1/\varepsilon))$, a linear rate.
- Nonconvex: $k \ge 2 L_f (f(x_0) - f^*) / \varepsilon^2$ steps give a point with $\|\nabla f\| \le \varepsilon$.

**These bounds are tight for gradient descent.** On the Huber function of the [convergence theorem](/gradient-descent-convergence-theorem/) page, step $1/L_f$ gives exactly $f(x_k) - f^* = L_f R^2/(4k + 2)$, which Drori and Teboulle proved is the exact worst case. On $f(x) = \frac12(\mu x_1^2 + L_f x_2^2)$, the error is $\Theta((1 - \mu/L_f)^{2k})$, so $\Theta(\kappa \log(1/\varepsilon))$ steps are needed.

**Gradient descent is not optimal.** The [first-order lower bound](/first-order-lower-bound/) is $\Omega(\sqrt{L_f R^2/\varepsilon})$ steps for convex $f$ and $\Omega(\sqrt{\kappa} \log(1/\varepsilon))$ for strongly convex $f$. [Nesterov's accelerated gradient method](/nesterov-accelerated-gradient/) reaches both, at the same cost per step.

| claim | value |
|---|---|
| time | $O(kn)$ plus $k$ gradient evaluations |
| extra space | $O(n)$ |
| gradients, convex, $\alpha = 1/L_f$ | $O(L_f R^2/\varepsilon)$ |
| gradients, strongly convex, $\alpha = 1/L_f$ | $O(\kappa \log(1/\varepsilon))$ |

## Properties

- **Descent method.** For $0 < \alpha < 2/L_f$, each step with $\nabla f(x_k) \ne 0$ lowers $f$, since the descent lemma gives $f(x_{k+1}) \le f(x_k) - \alpha (1 - L_f \alpha/2) \|\nabla f(x_k)\|^2$.
- **No memory.** The next point depends only on the current point. The momentum methods add the previous step.
- **Invariant under rotations, not under scaling.** If $f(x) = h(Qx)$ with $Q$ orthogonal, the iterates of $f$ are the rotated iterates of $h$. A change of scale of one variable changes $\kappa$ and the speed. Newton's method is invariant under all linear changes of variables.
- **Fixed points are stationary points.** $x_{k+1} = x_k$ if and only if $\nabla f(x_k) = 0$. For convex $f$ these are the minimizers. For nonconvex $f$ they can be saddle points or local minima.

## Variants and improvements

- **Line searches.** [Exact line search](/exact-line-search/) and [backtracking line search](/backtracking-line-search/) remove the need to know $L_f$. Backtracking with the Armijo constant $c = 1/2$, first step $\alpha_0$ and shrink factor $\rho$ keeps the convex rate, with $L_f$ replaced by $\max(1/\alpha_0, L_f/\rho)$.
- **Barzilai-Borwein step.** The step $\alpha_k = s^\top s / s^\top y$ with $s = x_k - x_{k-1}$ and $y = \nabla f(x_k) - \nabla f(x_{k-1})$ is often much faster in practice, but $f$ need not fall at each step.
- **[Polyak step size](/polyak-step-size/).** $\alpha_k = (f(x_k) - f^*)/\|\nabla f(x_k)\|^2$, when $f^*$ is known.
- **[Momentum](/momentum-method/) and [Nesterov acceleration](/nesterov-accelerated-gradient/).** Add a multiple of the last step. Nesterov's method improves $O(1/k)$ to $O(1/k^2)$.
- **Constraints and nonsmooth terms.** [Projected gradient descent](/projected-gradient-descent/) and the [proximal gradient method](/proximal-gradient-method/) keep the same rates for [constrained](/constrained-smooth-minimization/) and composite problems.
- **Other geometries.** [Preconditioning](/preconditioning/) uses $x_{k+1} = x_k - \alpha P^{-1} \nabla f(x_k)$. [Mirror descent](/mirror-descent/) and [natural gradient descent](/natural-gradient-descent/) change the norm. [Quasi-Newton methods](/quasi-newton-method/) learn $P$ from the gradients.
- **Noisy gradients.** [Stochastic gradient descent](/stochastic-gradient-descent/) uses an unbiased estimate of $\nabla f$, with decreasing steps.
- **One coordinate at a time.** [Coordinate descent](/coordinate-descent/).

## When to use it

Use gradient descent when $n$ is large, the gradient is cheap, and a moderate accuracy is enough, or as the inner step of a larger method. It needs only $O(n)$ memory and no linear solves. On an ill-conditioned problem it is slow: prefer [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/) or [L-BFGS](/limited-memory-bfgs/) for smooth problems of medium accuracy, and Newton's method ([Newton's method for systems](/newton-method-for-systems/) applied to $\nabla f = 0$) when $n$ is small and the Hessian is available. When $L_f$ and $\mu$ are known, the accelerated method costs the same per step and needs far fewer steps.

## Pitfalls

- **A step that is too large.** With $\alpha \ge 2/L_f$ the iteration can diverge, as the example with $\alpha = 0.21$ shows. A fixed `alpha = 1.0` that works on one problem fails after a rescale of $f$. Use $\alpha = 1/L_f$ or a line search. The test `test_worked_example` checks the growth for $\alpha = 0.21$.
- **The wrong sign.** `x = x + alpha * g` climbs the hill. Line L5 subtracts. Every test with a known minimizer catches this.
- **Stopping on a small change of $f$.** A small decrease of $f$ in one step does not mean that $x$ is near a minimizer: on a flat ill-conditioned valley $f$ changes slowly far from $x^*$. Stop on $\|\nabla f(x)\| \le \varepsilon_g$, as line L4 does, or on a known bound.
- **A stationary point is not a minimum.** For $f(x) = x_1^2 - x_2^2$ and a start with $x_2 = 0$, the iterates converge to the saddle point $0$. Convexity, or a random start, excludes this case.
- **Bad scaling.** Variables in very different units give a large $\kappa$. Rescale the variables or precondition.

## Implementations

The Python version returns the list of all iterates, so that the tests can check the bounds at each step. The tests use convex quadratics $f(x) = \frac12 (x - c)^\top A (x - c) + f^*$ with known eigenvalues, including singular ones, and check claims 1 to 4 at every iterate.

## History

Augustin-Louis Cauchy proposed the method in 1847, in a short note in the Comptes Rendus, to solve systems of equations by the minimization of a sum of squares; Lemaréchal tells the story. Haskell Curry analysed the method for nonlinear minimization in 1944. Polyak proved the linear rate under the gradient dominance condition, now called the Polyak-Lojasiewicz condition, in 1963. The non-asymptotic bounds $O(1/k)$ and $(1 - \mu/L_f)^k$ in the form of this page are in Nesterov's lectures. Drori and Teboulle found the exact worst case $L_f R^2/(4k+2)$ in 2014.

## References
