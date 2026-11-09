---
tag: 4RG0K9
kind: problem
slug: finite-sum-minimization
name: Finite-sum minimization
aliases:
- empirical risk minimization with a finite dataset
- finite-sum optimization
- incremental optimization
area: optimization/gradient-methods
level: advanced
summary: Minimize an average of n smooth functions, the structure of most training objectives.
prereqs: [gradient, smoothness, strong-convexity]
see_also: [stochastic-optimization, empirical-risk-minimization, stochastic-gradient-descent, svrg, saga, composite-minimization, logistic-regression, ridge-regression]
sources:
  - paper: doi:10.1007/s10107-016-1030-6
    title: Mark Schmidt, Nicolas Le Roux and Francis Bach, Minimizing finite sums with the stochastic average gradient, Mathematical Programming 162, 2017
    locator: pages 83 to 112, the SAG method and the first linear rate with a cost per step independent of n
  - paper: "Rie Johnson and Tong Zhang, Accelerating stochastic gradient descent using predictive variance reduction, Advances in Neural Information Processing Systems 26, 2013"
    locator: Theorem 1, the linear rate of SVRG with O((n + κ) log(1/ε)) component gradients
  - url: https://arxiv.org/abs/1407.0202
    title: Aaron Defazio, Francis Bach and Simon Lacoste-Julien, SAGA, A fast incremental gradient method with support for non-strongly convex composite objectives, NeurIPS 2014
    locator: Theorem 1, the linear rate of SAGA for strongly convex composite finite sums
  - paper: "Shai Shalev-Shwartz and Tong Zhang, Stochastic dual coordinate ascent methods for regularized loss minimization, Journal of Machine Learning Research 14, 2013, pages 567 to 599"
    locator: Section 2, the dual problem and the linear rate of SDCA for smooth losses
  - url: https://arxiv.org/abs/1603.05953
    title: Zeyuan Allen-Zhu, Katyusha, The first direct acceleration of stochastic gradient methods, Journal of Machine Learning Research 18(221), 2018
    locator: Theorem 2.1, the O((n + √(nκ)) log(1/ε)) rate for strongly convex finite sums
  - url: https://arxiv.org/abs/1605.08003
    title: Blake Woodworth and Nathan Srebro, Tight complexity bounds for optimizing composite objectives, NeurIPS 2016
    locator: Section 3, the lower bound Ω(n + √(nκ) log(1/ε)) for randomized algorithms with component gradient and prox oracles
  - paper: doi:10.1007/s10107-017-1173-0
    title: Guanghui Lan and Yi Zhou, An optimal randomized incremental gradient method, Mathematical Programming 171, 2018
    locator: Section 3, the lower bound of order (n + √(nκ)) log(1/ε) for randomized incremental gradient methods and a method that attains it
  - url: https://arxiv.org/abs/1807.01695
    title: Cong Fang, Chris Junchi Li, Zhouchen Lin and Tong Zhang, SPIDER, Near-optimal non-convex optimization via stochastic path integrated differential estimator, NeurIPS 2018
    locator: Theorems 1 and 3, the O(n + √n ε^-2) upper bound and the matching lower bound for smooth nonconvex finite sums
  - paper: doi:10.1109/JPROC.2020.3028013
    title: Robert M. Gower, Mark Schmidt, Francis Bach and Peter Richtárik, Variance-reduced methods for machine learning, Proceedings of the IEEE 108(11), 2020
    locator: pages 1968 to 1983, a survey of SAG, SAGA, SVRG and their rates
---

Finite-sum minimization is the problem of minimizing an average $F(x) = \frac{1}{n}\sum_{i=1}^n f_i(x)$ of $n$ [smooth](/smoothness/) functions, where one evaluation of a single $\nabla f_i$ is the unit of cost. It is the form of every training objective in [empirical risk minimization](/empirical-risk-minimization/), with one term per data point. Because a random $\nabla f_i$ is an unbiased estimate of $\nabla F$, the problem is a special case of [stochastic optimization](/stochastic-optimization/), but the finite structure allows variance-reduced methods such as [SVRG](/svrg/) and [SAGA](/saga/) that converge linearly at a cost per step independent of $n$. For a $\mu$-[strongly convex](/strong-convexity/) $F$ with condition number $\kappa$, the best possible cost is of order $(n + \sqrt{n\kappa})\log(1/\varepsilon)$ component gradients.

## In plain words

The function to minimize is an average of many small pieces, often one piece per data point. Computing the exact slope of the average means visiting every piece, which is slow when there are millions of them.

A cheaper step uses the slope of one random piece. That slope is right on average but noisy. The noise does not fade even at the best point, because single pieces still disagree there. Methods for this problem keep a memory of old slopes and use it to cancel the noise, so they get the accuracy of exact steps at almost the cost of cheap ones.

## Definition

Notation: $n$ is the number of components, $d$ the number of variables, $\varepsilon$ the target accuracy and $\kappa = L/\mu$.

**Input.** Functions $f_1, \dots, f_n : \mathbb{R}^d \to \mathbb{R}$, each convex with an $L$-Lipschitz gradient, such that $F = \frac{1}{n}\sum_if_i$ is $\mu$-strongly convex. In the composite form there is also a convex, possibly nonsmooth term $\psi$ with a cheap [proximal operator](/proximal-operator/), and the objective is $F + \psi$. Access is through an **incremental first-order oracle**: on a query $(i, x)$ it returns $f_i(x)$ and $\nabla f_i(x)$, at unit cost.

**Output.** A point $\hat{x}$, possibly random, with $\mathbb{E}[F(\hat{x})] - F^* \le \varepsilon$ (or $\mathbb{E}\lVert\hat{x} - x^*\rVert^2 \le \varepsilon$).

The **cost** is the number of oracle calls. A full gradient $\nabla F(x)$ costs $n$ calls; a random component gradient costs one.

The difference from general stochastic optimization is the noise at the solution. With $i$ uniform, $\nabla f_i(x^*)$ has mean $\nabla F(x^*) = 0$ and variance $\sigma_*^2 = \frac{1}{n}\sum_i\lVert\nabla f_i(x^*)\rVert^2$, which is usually positive. Plain [SGD](/stochastic-gradient-descent/) therefore needs diminishing steps and converges sublinearly. A variance-reduced estimator $g$ has $\mathbb{E}g = \nabla F(x)$ and a variance that goes to $0$ as $x$ and the stored points approach $x^*$.

## Variants

- **Composite.** Add a nonsmooth term $\psi$, such as the $\ell_1$ norm in the [lasso](/lasso-regression/), and use proximal steps ([composite minimization](/composite-minimization/)).
- **Convex but not strongly convex.** The target is $F(\hat{x}) - F^* \le \varepsilon$ with rates in $1/\varepsilon$ instead of $\log(1/\varepsilon)$.
- **Nonconvex.** Each $f_i$ is $L$-smooth, $F$ is bounded below, and the target is $\mathbb{E}\lVert\nabla F(\hat{x})\rVert \le \varepsilon$.
- **Different smoothness constants.** Component $i$ has its own $L_i$; sampling $i$ with probability proportional to $L_i$ replaces $\max_iL_i$ by the mean of the $L_i$ in the rates.
- **Linear models.** $f_i(x) = \phi_i(\langle a_i, x\rangle) + \frac{\lambda}{2}\lVert x\rVert^2$. Each gradient is a scalar multiple of $a_i$ plus $\lambda x$, which allows storage of one scalar per component and dual methods.
- **Distributed and federated.** The components are split across machines, and communication rounds are counted as well as oracle calls.

## Examples

**A one-dimensional example with noise at the solution.** Let $f_i(x) = \frac{1}{2}(x - b_i)^2$ with $b = (0, 1, 5)$. Then $F(x) = \frac{1}{2}(x - 2)^2 + \frac{7}{3}$, so $x^* = 2$, $L = \mu = 1$ and $F^* = 7/3$. The component gradients at $x^*$ are $-2$, $-1$ and $3$: their mean is $0$, but $\sigma_*^2 = (4 + 1 + 9)/3 = 14/3$. SGD with a constant step $\eta$ started at $x^*$ moves away from it. SAGA started anywhere converges to $x^*$, because its table of stored gradients cancels the disagreement.

**Ridge regression.** $f_i(x) = \frac{1}{2}(\langle a_i, x\rangle - b_i)^2 + \frac{\lambda}{2}\lVert x\rVert^2$, with $L = \max_i\lVert a_i\rVert^2 + \lambda$ and $\mu \ge \lambda$ ([ridge regression](/ridge-regression/)).

**Regularized logistic regression.** $f_i(x) = \log(1 + e^{-b_i\langle a_i, x\rangle}) + \frac{\lambda}{2}\lVert x\rVert^2$ with labels $b_i \in \{-1, 1\}$, so $L \le \frac{1}{4}\max_i\lVert a_i\rVert^2 + \lambda$ and $\mu \ge \lambda$ ([logistic regression](/logistic-regression/)).

**Costs in numbers.** For $n = 10^6$ components and $\kappa = 10^3$, the factor in front of $\log(1/\varepsilon)$ is $n\kappa = 10^9$ for gradient descent, $n\sqrt{\kappa} \approx 3.2 \cdot 10^7$ for accelerated gradient descent, $n + \kappa \approx 10^6$ for SVRG and SAGA, and $n + \sqrt{n\kappa} \approx 1.03 \cdot 10^6$ for the optimal methods. When $\kappa \le n$, variance reduction costs a constant number of passes per digit of accuracy.

## Known algorithms

Costs are in component gradient calls, for $L$-smooth convex $f_i$ and a $\mu$-strongly convex $F$, up to constant factors.

| method | cost to accuracy $\varepsilon$ | memory |
|---|---|---|
| [gradient descent](/gradient-descent/) | $n\kappa\log(1/\varepsilon)$ | $O(d)$ |
| [Nesterov's accelerated gradient](/nesterov-accelerated-gradient/) | $n\sqrt{\kappa}\log(1/\varepsilon)$ | $O(d)$ |
| [SGD](/stochastic-gradient-descent/), steps of order $1/(\mu k)$ | $\sigma_*^2/(\mu^2\varepsilon) + \kappa\log(1/\varepsilon)$, for $\mathbb{E}\lVert x - x^*\rVert^2 \le \varepsilon$ | $O(d)$ |
| SAG (Schmidt, Le Roux and Bach 2017) | $(n + \kappa)\log(1/\varepsilon)$ | $O(nd)$, or $O(n)$ for linear models |
| [SAGA](/saga/) | $(n + \kappa)\log(1/\varepsilon)$ | $O(nd)$, or $O(n)$ for linear models |
| [SVRG](/svrg/) | $(n + \kappa)\log(1/\varepsilon)$ | $O(d)$ |
| SDCA (Shalev-Shwartz and Zhang 2013) | $(n + \kappa)\log(1/\varepsilon)$, linear models | $O(n + d)$ |
| Katyusha (Allen-Zhu 2018) | $(n + \sqrt{n\kappa})\log(1/\varepsilon)$ | $O(d)$ |

For smooth nonconvex finite sums, SPIDER and related methods find $\mathbb{E}\lVert\nabla F\rVert \le \varepsilon$ with $O(n + \sqrt{n}\,\varepsilon^{-2})$ calls, against $O(n\varepsilon^{-2})$ for gradient descent (Fang, Li, Lin and Zhang 2018).

## Bounds

- **Strongly convex, lower bound.** Any randomized method that uses component gradients (and component proximal steps) needs $\Omega(n + \sqrt{n\kappa}\log(1/\varepsilon))$ calls in the worst case (Woodworth and Srebro 2016; Lan and Zhou 2018 for incremental gradient methods). Katyusha and the method of Lan and Zhou attain this up to the placement of the logarithm, so the problem is solved in the oracle model.
- **Against full gradients.** Since $n + \sqrt{n\kappa} \le 2n\sqrt{\kappa}$ when $\kappa \ge 1$, the optimal finite-sum cost is never worse than accelerated gradient descent by more than a factor of 2, and the ratio $n\sqrt{\kappa}/(n + \sqrt{n\kappa})$ is at least $\frac{1}{2}\min(\sqrt{\kappa}, \sqrt{n})$.
- **Nonconvex.** For $n \le O(\varepsilon^{-4})$, $\Theta(\sqrt{n}\,\varepsilon^{-2})$ calls are necessary and sufficient for averaged smooth components (Fang et al. 2018).
- **Against the stochastic problem.** If only the sample average matters, the statistical error of order $1/n$ makes accuracy far beyond that level of little use, so training rarely runs a variance-reduced method to machine precision.

## Reductions

- **From stochastic optimization.** Sample average approximation replaces $\mathbb{E}f(x, \xi)$ by $\frac{1}{n}\sum_if(x, \xi_i)$, which is a finite sum.
- **To stochastic optimization.** Pick $i$ uniformly; then $\nabla f_i(x)$ is an unbiased oracle for $\nabla F(x)$, and every stochastic method applies.
- **To a dual problem.** For linear models with a strongly convex regularizer, the Fenchel dual is a separable problem with one variable per component, solved by randomized [coordinate descent](/coordinate-descent/) (SDCA). This uses the [convex conjugate](/convex-conjugate/) of each loss.
- **Strongly convex from convex.** Adding $\frac{\varepsilon}{2R^2}\lVert x\rVert^2$ turns a convex finite sum into a strongly convex one with $\kappa = LR^2/\varepsilon$, so the strongly convex methods solve the convex case at the price of this $\kappa$.

## Applications

- Training linear and generalized linear models: least squares, ridge, lasso, logistic regression and [support vector machines](/svm-training/).
- Training neural networks, where the finite sum is the training loss and $n$ is the size of the data set.
- Matrix factorization and recommender systems, with one term per observed entry.
- Maximum likelihood with independent data, where the log-likelihood is a sum over observations ([maximum likelihood estimation](/maximum-likelihood-estimation/)).

## References
