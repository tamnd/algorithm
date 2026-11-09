---
tag: 7HXACE
kind: concept
slug: condition-number-of-an-optimization-problem
name: Condition number of an optimization problem
aliases:
- condition number L/mu
- ratio of smoothness to strong convexity
- kappa
area: optimization/gradient-methods
level: intro
summary: The ratio κ = L_f/μ of the smoothness and strong convexity constants. Gradient descent needs about κ log(1/ε) steps and accelerated methods about √κ log(1/ε), so large κ means a slow problem.
prereqs: [smoothness, strong-convexity]
see_also: [condition-number, preconditioning, linear-convergence-strongly-convex, momentum-method, nesterov-accelerated-gradient, conjugate-gradient-method, first-order-lower-bound, ridge-regression]
sources:
  - book: isbn:9783319915777
    title: Yurii Nesterov, Lectures on Convex Optimization, second edition, Springer, 2018
    locator: Section 2.1, Minimization of smooth functions (the class of smooth strongly convex functions, its condition number, and the lower and upper bounds in terms of it)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.1.2, Strong convexity and implications (the condition number of sublevel sets), and Section 9.3, Gradient descent method (the effect of the condition number and of a change of coordinates)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Section 3.3, Rate of convergence (steepest descent on a quadratic, with the factor in terms of the extreme eigenvalues)
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Section 3.4, Strong convexity, and Section 3.5, Lower bounds
---

The condition number of a smooth strongly convex minimization problem is $\kappa = L_f/\mu$, the ratio of the [smoothness](/smoothness/) constant $L_f$ to the [strong convexity](/strong-convexity/) constant $\mu$. It is at least $1$, and it measures how stretched the level sets of $f$ are. The number of steps of first-order methods grows with $\kappa$: [gradient descent](/gradient-descent/) needs about $\kappa \ln(1/\varepsilon)$ steps, and the best first-order methods need about $\sqrt{\kappa}\ln(1/\varepsilon)$, which is also a lower bound. For a quadratic $\frac12 x^\top A x - b^\top x$ it is the [condition number](/condition-number/) $\lambda_{\max}(A)/\lambda_{\min}(A)$ of the matrix $A$.

## In plain words

Think of a bowl. If it is round, the steepest way down at each point goes straight to the bottom, and a ball rolls there fast. If it is a long narrow valley, the steepest way down points mostly across the valley, not along it, so a walker who follows the slope crosses from side to side and makes slow progress toward the bottom.

The condition number tells how long and narrow the valley is: the ratio of the strongest curve to the weakest curve. A value near one means a round bowl and an easy problem. A large value means a narrow valley, many small steps, and a problem that is also sensitive to small changes in the data. Changing the units of the variables changes this number, which is why rescaling the data can make a slow problem fast.

## The idea

Let $f$ be $L_f$-smooth and $\mu$-strongly convex with $\mu > 0$. Then for all $x, y$

$$\frac{\mu}{2}\|y - x\|^2 \le f(y) - f(x) - \nabla f(x)^\top (y - x) \le \frac{L_f}{2}\|y - x\|^2,$$

so $\mu \le L_f$ and $\kappa = L_f/\mu \ge 1$. If $f$ is twice differentiable, this is $\mu I \preceq \nabla^2 f(x) \preceq L_f I$ for all $x$, and the best constants give $\kappa = \sup_x \lambda_{\max}(\nabla^2 f(x)) / \inf_x \lambda_{\min}(\nabla^2 f(x))$.

**Quadratics.** For $f(x) = \frac12 x^\top A x - b^\top x$ with $A$ symmetric [positive definite](/positive-definite-matrix/), the constants are the extreme [eigenvalues](/eigenvalue/), $L_f = \lambda_{\max}(A)$ and $\mu = \lambda_{\min}(A)$. So $\kappa = \operatorname{cond}_2(A)$, the same number that bounds the relative change of the solution $x^* = A^{-1} b$ under a relative change of $b$. The level sets $\{f \le c\}$ are ellipsoids whose longest and shortest axes have the ratio $\sqrt{\kappa}$.

**The cost of first-order methods in terms of $\kappa$.**

| method | factor per step | steps for accuracy $\varepsilon$ |
|---|---|---|
| gradient descent, step $1/L_f$ | $1 - 1/\kappa$ | $\kappa \ln(1/\varepsilon)$ |
| gradient descent, step $2/(\mu + L_f)$ | $(\kappa - 1)/(\kappa + 1)$ on distances | $\frac{\kappa + 1}{2}\ln(1/\varepsilon)$ |
| [exact line search](/exact-line-search/) on a quadratic | $\left((\kappa - 1)/(\kappa + 1)\right)^2$ on $f - f^*$ | $\frac{\kappa + 1}{4}\ln(1/\varepsilon)$ |
| [heavy ball momentum](/momentum-method/), quadratics | $(\sqrt{\kappa} - 1)/(\sqrt{\kappa} + 1)$, asymptotically | $\frac{\sqrt{\kappa}}{2}\ln(1/\varepsilon)$ |
| [Nesterov's accelerated gradient](/nesterov-accelerated-gradient/) | $1 - 1/\sqrt{\kappa}$ | $\sqrt{\kappa}\ln(1/\varepsilon)$ |
| [conjugate gradient](/conjugate-gradient-method/), quadratics | $(\sqrt{\kappa} - 1)/(\sqrt{\kappa} + 1)$ in the $A$-norm | $\frac{\sqrt{\kappa}}{2}\ln(2/\varepsilon)$ |
| any first-order method, worst case ([lower bound](/first-order-lower-bound/)) | at best $\left((\sqrt{\kappa} - 1)/(\sqrt{\kappa} + 1)\right)^2$ | $\Omega(\sqrt{\kappa}\ln(1/\varepsilon))$ |

The step counts are estimates for large $\kappa$: a factor $q$ near $1$ needs about $\ln(1/\varepsilon)/(1 - q)$ steps, since $\ln(1/q) \approx 1 - q$. The rates for gradient descent are proved on the page of the [linear convergence theorem](/linear-convergence-strongly-convex/).

**Not invariant under a change of variables.** If $x = M y$ with $M$ invertible, then $g(y) = f(My)$ has Hessian $M^\top \nabla^2 f(My) M$, and its condition number can be much larger or much smaller than that of $f$. Gradient descent depends on this choice; Newton's method does not, because its steps transform with $M$. [Preconditioning](/preconditioning/) picks $M$ to make $\kappa$ small: with $M = A^{-1/2}$ the quadratic becomes $\frac12\|y\|^2 - (A^{-1/2} b)^\top y$ with $\kappa = 1$, and one gradient step with step $1$ solves it. Quasi-Newton methods such as [BFGS](/bfgs/) build such a scaling from gradient differences.

**Local condition number.** For a twice differentiable $f$ that is not strongly convex everywhere, the condition number $\operatorname{cond}_2(\nabla^2 f(x^*))$ at the minimizer sets the local linear rate of gradient methods near $x^*$. If $\mu = 0$, as for convex functions that are not strongly convex, $\kappa = \infty$ and only the sublinear rates hold.

## Examples

- **A diagonal quadratic.** $f(x) = \frac12 (x_1^2 + 10 x_2^2)$ has $\mu = 1$, $L_f = 10$, $\kappa = 10$. Gradient descent with step $1/L_f = 0.1$ multiplies $x_1$ by $0.9$ at each step and sets $x_2$ to $0$ after one step. With $\varepsilon = 10^{-6}$, $\kappa \ln(1/\varepsilon) \approx 138$ steps, against $\sqrt{\kappa}\ln(1/\varepsilon) \approx 44$ for an accelerated method. For $\kappa = 1000$ the counts are about $13{,}816$ and $437$.
- **Units of the data.** Rescale the first variable of $\frac12(x_1^2 + x_2^2)$, which has $\kappa = 1$, by $x_1 = 100 y_1$. Then $g(y) = \frac12(10^4 y_1^2 + y_2^2)$ has $\kappa = 10^4$. Features measured in very different units have the same effect on least squares, which is why data are often standardized before training.
- **Least squares and ridge regression.** For the line fit with rows $(1, 0), (1, 1), (1, 2)$, the matrix $A^\top A = \begin{pmatrix} 3 & 3 \\ 3 & 5 \end{pmatrix}$ has eigenvalues $4 \pm \sqrt{10}$, that is $7.162$ and $0.838$, so $\kappa = 8.55$. [Ridge regression](/ridge-regression/) adds $\frac{\lambda}{2}\|x\|^2$, which adds $\lambda$ to each eigenvalue: with $\lambda = 1$, $\kappa = 8.162/1.838 = 4.44$. In general ridge regularization gives $\kappa = (\sigma_{\max}^2 + \lambda)/(\sigma_{\min}^2 + \lambda)$.
- **Regularized logistic regression.** The average logistic loss is $\|A\|_2^2/(4m)$-smooth and is not strongly convex in general. With the term $\frac{\lambda}{2}\|w\|^2$, $\kappa \le 1 + \|A\|_2^2/(4 m \lambda)$, so a small $\lambda$ means a large condition number.

## Where it is used

- Choice of method: for small $\kappa$ plain gradient descent is enough; for large $\kappa$ accelerated methods, [nonlinear conjugate gradient](/nonlinear-conjugate-gradient/) or quasi-Newton methods pay off.
- Choice of parameters: the step $2/(\mu + L_f)$ of gradient descent and the parameters of heavy ball and Nesterov's method are functions of $\mu$ and $L_f$.
- Data preparation in machine learning: feature scaling, whitening and batch normalization aim to reduce the condition number.
- Complexity statements: the bounds $\Theta(\sqrt{\kappa}\log(1/\varepsilon))$ of strongly convex optimization and the analysis of [preconditioning](/preconditioning/) for linear systems.

## References
