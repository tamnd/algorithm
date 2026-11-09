---
tag: VQR315
kind: concept
slug: polyak-step-size
name: Polyak step size
aliases:
- Polyak step
- Polyak stepsize
- Polyak's rule
area: optimization/gradient-methods
level: advanced
summary: "The step α = (f(x) - f*)/‖g‖² with g = ∇f(x) or a subgradient. With f* known, it needs no smoothness constant, never moves away from a minimizer of a convex f, and adapts to the problem."
prereqs: [gradient-descent, convex-function]
see_also: [step-size-selection, subgradient, gradient-descent, backtracking-line-search, gradient-descent-convergence-theorem, stochastic-gradient-descent]
sources:
  - paper: doi:10.1016/0041-5553(69)90061-5
    title: Boris T. Polyak, Minimization of unsmooth functionals, USSR Computational Mathematics and Mathematical Physics 9(3), 1969
    locator: pages 14 to 29 (the subgradient method with the step (f(x) - f*)/‖g‖² and its convergence)
  - book: isbn:9780911575149
    title: Boris T. Polyak, Introduction to Optimization, Optimization Software, 1987
    locator: Chapter 5, Nondifferentiable optimization (the subgradient method with a known optimal value)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 8, Primal and dual projected subgradient methods (Polyak's stepsize and its rate)
---

The Polyak step size sets the step of a gradient or subgradient method to $\alpha_k = (f(x_k) - f^*)/\|g_k\|^2$, where $g_k$ is the gradient (or a [subgradient](/subgradient/)) at $x_k$ and $f^*$ is the optimal value, which must be known. For a convex $f$ it is the step that minimizes a guaranteed bound on the next distance to a minimizer, so the distance never increases. It gives the rate $GR/\sqrt{k+1}$ on nonsmooth Lipschitz functions, $2L_f R^2/(k+1)$ on smooth functions and a linear rate on smooth strongly convex functions, all without knowing $G$, $L_f$ or $\mu$. Its weakness is the need for $f^*$, which is known in some problems (feasibility problems, interpolating models with $f^* = 0$) and must be estimated in others.

## In plain words

Picture walking downhill toward a known ground level. You know how high you are above the ground and how steep the slope under your feet is. The Polyak rule says: walk the distance that would bring you exactly to ground level if the slope stayed the same all the way down.

When you are high up, you take a long step. When you are almost at ground level, you take a short step. You do not need to know in advance how curved the landscape is. The price is that you must know the height of the ground, which is the very best value you are looking for.

## The idea

Let $f$ be convex with a minimizer $x^*$ and the optimal value $f^*$, and let $g_k \in \partial f(x_k)$, $g_k \ne 0$ (for differentiable $f$, $g_k = \nabla f(x_k)$). The method is

$$x_{k+1} = x_k - \alpha_k g_k, \qquad \alpha_k = \frac{f(x_k) - f^*}{\|g_k\|^2}.$$

The step is the root of the linear model: $f(x_k) - \alpha\|g_k\|^2 = f^*$ at $\alpha = \alpha_k$.

**Distance decrease.** For every step $\alpha$, expanding the square and the subgradient inequality $g_k^\top(x_k - x^*) \ge f(x_k) - f^*$ give

$$\|x_{k+1} - x^*\|^2 \le \|x_k - x^*\|^2 - 2\alpha(f(x_k) - f^*) + \alpha^2\|g_k\|^2.$$

The right side is a parabola in $\alpha$, minimized at $\alpha = \alpha_k$, where it is

$$\|x_{k+1} - x^*\|^2 \le \|x_k - x^*\|^2 - \frac{(f(x_k) - f^*)^2}{\|g_k\|^2}. \tag{$*$}$$

So the distance to every minimizer does not increase. The values $f(x_k)$ need not decrease.

**Nonsmooth rate.** If $\|g_k\| \le G$ for all $k$, add $(*)$ for $i = 0, \ldots, k$: $\sum_{i \le k}(f(x_i) - f^*)^2 \le G^2R^2$ with $R = \|x_0 - x^*\|$. The smallest term is at most the mean, so

$$\min_{0 \le i \le k}\left(f(x_i) - f^*\right) \le \frac{GR}{\sqrt{k+1}}.$$

This is the same bound as for the subgradient method with the constant step $R/(G\sqrt{k+1})$, which needs $G$ and $R$; the Polyak step needs neither.

**Smooth rate.** If $f$ is also $L_f$-smooth, then $\|g_k\|^2 \le 2L_f(f(x_k) - f^*)$ ([smoothness](/smoothness/)), so $\alpha_k \ge 1/(2L_f)$ and $(*)$ gives $\|x_{k+1} - x^*\|^2 \le \|x_k - x^*\|^2 - \frac{f(x_k) - f^*}{2L_f}$. Adding these for $i = 0, \ldots, k$,

$$\min_{0 \le i \le k}\left(f(x_i) - f^*\right) \le \frac{2L_f R^2}{k+1}.$$

**Strongly convex rate.** If $f$ is also $\mu$-strongly convex, then $f(x_k) - f^* \ge \frac{\mu}{2}\|x_k - x^*\|^2$, and the smooth inequality becomes

$$\|x_{k+1} - x^*\|^2 \le \left(1 - \frac{\mu}{4L_f}\right)\|x_k - x^*\|^2,$$

a linear rate with the factor $1 - 1/(4\kappa)$, where $\kappa = L_f/\mu$.

**When $f^*$ is unknown.** The method can use an estimate $\hat{f}$ in place of $f^*$. If $\hat{f} > f^*$ and $f(x_k) > \hat{f}$, the same expansion gives $\|x_{k+1} - x^*\|^2 \le \|x_k - x^*\|^2 - (f(x_k) - \hat{f})^2/\|g_k\|^2$, so either some $f(x_k) \le \hat{f}$ or $\min_{i \le k}f(x_i) - \hat{f} \le GR/\sqrt{k+1}$; if $\hat{f} < f^*$, the steps are too long and the method need not converge. Practical versions lower or raise the estimate during the run.

## Examples

- **A quadratic.** For $f(x) = \frac12(x_1^2 + 10x_2^2)$ with $f^* = 0$ and $x_0 = (10, 1)$: $f(x_0) = 55$, $\|\nabla f(x_0)\|^2 = 200$, so $\alpha_0 = 0.275$ and $x_1 = (7.25, -1.75)$ with $f(x_1) = 41.59$. The next steps are $0.1159$ and $0.4285$: the step changes with the local geometry. The method reaches $\|\nabla f\| \le 10^{-6}$ after $54$ steps, against $153$ for [gradient descent](/gradient-descent/) with step $1/L_f$ and $83$ with step $2/(\mu + L_f)$.
- **A one-dimensional quadratic.** For $f(x) = x^2$, $\alpha_k = x_k^2/(4x_k^2) = \frac14$, so $x_{k+1} = x_k/2$. The step is half of the exact minimizing step $\frac12$; the linear model predicts the drop to $f^*$ too early because $f$ is curved.
- **Nonsmooth functions.** For $f(x) = \|x\|$ with $f^* = 0$, $g = x/\|x\|$, so $\alpha = \|x\|$ and $x_1 = x - x = 0$: one step. For $f(x) = \max_i(a_i^\top x - b_i)$ with known optimal value, the method is a classical method for systems of convex inequalities.
- **Feasibility.** To find a point of $C_1 \cap \cdots \cap C_m$ for closed convex sets, minimize $f(x) = \max_i\operatorname{dist}(x, C_i)$, whose optimal value $f^* = 0$ is known when the intersection is nonempty. The Polyak step then moves to the projection on the farthest set.

## Where it is used

- Subgradient methods for nonsmooth convex problems with a known optimal value, such as feasibility problems and the method of alternating projections.
- Problems with $f^* = 0$, such as the solution of consistent systems of equations by least squares and the training of overparameterized models that fit the data exactly, where stochastic forms of the Polyak step are used with [stochastic gradient descent](/stochastic-gradient-descent/).
- As a reference rule in [step size selection](/step-size-selection/): it shows what a step size can achieve with knowledge of $f^*$ in place of knowledge of $L_f$.

## References
