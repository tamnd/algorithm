---
tag: N7DDFT
kind: algorithm
slug: logistic-regression
name: Logistic regression
aliases:
- logit model
- logistic regression model
- binary logistic regression
area: machine-learning/supervised-learning
level: intro
summary: Model P(y = 1 | x) as the sigmoid of a linear function and fit it by maximum likelihood with Newton's method (IRLS). The log loss is convex but has no closed form.
solves: [classification]
model: real-ram
complexity:
  vars: {n: the number of examples, d: the number of features, k: the number of Newton steps}
  time: {worst: O(k (n d^2 + d^3))}
  space: {extra: Θ(n d + d^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1958
  people: [David Cox, Joseph Berkson, John Nelder, Robert Wedderburn]
  note: Berkson named the logit in 1944. Cox (1958) gave the regression analysis of binary data, and Nelder and Wedderburn (1972) fitted it by iteratively reweighted least squares as a GLM.
prereqs: [linear-regression, maximum-likelihood-estimation, classification]
see_also: [logistic-loss, cross-entropy-loss, softmax-regression, generalized-linear-model, newton-method-for-systems, gradient-descent, linear-separability]
sources:
  - paper: doi:10.1111/j.2517-6161.1958.tb00292.x
    title: David R. Cox, The regression analysis of binary sequences, Journal of the Royal Statistical Society Series B 20(2), 215 to 242, 1958
    locator: Sections 1 to 3 (the logistic model for binary responses and its maximum likelihood fit)
  - paper: doi:10.1093/biomet/71.1.1
    title: A. Albert and J. A. Anderson, On the existence of maximum likelihood estimates in logistic regression models, Biometrika 71(1), 1 to 10, 1984
    locator: Section 3 (complete separation, quasi-complete separation and overlap, and the theorem that the estimate exists exactly under overlap)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 4.3.2 (logistic regression, the gradient and the remark on separable data) and Section 4.3.3 (iteratively reweighted least squares)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 4.4.1 (fitting logistic regression models by Newton-Raphson and IRLS) and Section 4.4.4 (L1 regularized logistic regression)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 9.2 (the backtracking line search) and Section 9.5 (Newton's method, damped and quadratic phases)
  - paper: "Daniel Soudry, Elad Hoffer, Mor Shpigel Nacson, Suriya Gunasekar and Nathan Srebro, The implicit bias of gradient descent on separable data, Journal of Machine Learning Research 19(70), 1 to 57, 2018"
    locator: Theorem 3 (on separable data the direction of gradient descent converges to the hard margin SVM direction, and the norm grows like log t)
---

Logistic regression is a linear model for [binary classification](/classification/). It models the probability of the positive class as $P(y = 1 \mid x) = \sigma(b + w^\top x)$, where $\sigma(z) = 1/(1 + e^{-z})$ is the logistic (sigmoid) function. The weights are fit by [maximum likelihood](/maximum-likelihood-estimation/), which is the same as minimizing the [logistic loss](/logistic-loss/), also called the log loss or binary [cross-entropy](/cross-entropy-loss/). The loss is convex, but its gradient equations have no closed form solution. The classical solver is Newton's method, which for this model is iteratively reweighted least squares (IRLS): each step is a weighted least squares fit. On data that a hyperplane separates, the maximum likelihood estimate does not exist: the weights grow without bound. An L2 penalty fixes this.

## In plain words

You want to predict yes or no from some input numbers, and you want a probability, not only an answer. Logistic regression first computes a weighted sum of the inputs, like linear regression. Then it squeezes that sum into a number between 0 and 1. A large positive sum gives a probability close to 1, and a large negative sum gives a probability close to 0.

To choose the weights, it makes the observed answers as likely as possible. No formula gives these weights directly. The usual method starts from zero weights and improves them in steps. Each step solves a weighted least squares problem, where the examples with uncertain predictions count most. If a straight line can split the yes and no examples perfectly, the weights keep growing at each step, and a small cost on the size of the weights is needed.

## The problem

The data are $(x_i, y_i)$, $i = 1, \dots, n$, with $x_i \in \mathbb{R}^d$ and $y_i \in \{0, 1\}$. Write $\theta = (b, w)$ and $\tilde x_i = (1, x_i)$, and let $\tilde X$ be the $n \times (d+1)$ matrix with rows $\tilde x_i^\top$. The model is $p_i = \sigma(z_i)$ with $z_i = \tilde x_i^\top\theta$, so the log-odds $\log(p_i/(1 - p_i)) = z_i$ is linear in $x_i$. The negative log-likelihood is

$$L(\theta) = -\sum_{i=1}^{n}\bigl[y_i\log p_i + (1 - y_i)\log(1 - p_i)\bigr] = \sum_{i=1}^{n}\bigl[\log(1 + e^{z_i}) - y_i z_i\bigr].$$

The fitting problem is to minimize $L(\theta) + \frac{\lambda}{2}\|w\|^2$ for some $\lambda \ge 0$, with no penalty on the bias $b$. With labels $\pm 1$, the same loss is $\sum_i \log(1 + e^{-y_i z_i})$.

**Gradient and Hessian.** Since $\sigma'(z) = \sigma(z)(1 - \sigma(z))$,

$$\nabla L = \tilde X^\top(p - y), \qquad \nabla^2 L = \tilde X^\top S\tilde X, \quad S = \operatorname{diag}\bigl(p_i(1 - p_i)\bigr).$$

**Convexity.** $S$ has positive entries, so $\nabla^2 L$ is positive semidefinite and $L$ is [convex](/convex-function/). It is strictly convex if $\tilde X$ has full column rank. The penalty adds $\lambda$ on the diagonal for the entries of $w$.

**No closed form.** At a minimum, the score equations $\tilde X^\top(y - p) = \lambda(0, w)$ hold. They are nonlinear in $\theta$ through $p_i = \sigma(\tilde x_i^\top\theta)$, and in general they have no closed form solution. The first equation (for the bias) says $\sum_i p_i = \sum_i y_i$: the fitted probabilities add up to the number of positive examples.

## The algorithm

Newton's method for the score equations solves $\nabla^2 L\,\delta = \nabla L$ and sets $\theta \leftarrow \theta - \delta$. A backtracking line search on the step makes it converge from each starting point.

```pseudo id=main
LOGISTIC-NEWTON(X, y, λ, tol)
L1  θ = (b, w) ← 0
L2  repeat
L3      p_i ← σ(x̃_iᵀ θ) for each i
L4      g ← X̃ᵀ (p − y) + λ (0, w)
L5      S ← diag(p_i (1 − p_i));  H ← X̃ᵀ S X̃ + λ diag(0, I)
L6      solve H δ = g by Cholesky
L7      t ← 1;  while J(θ − tδ) > J(θ) − t gᵀδ / 4 do t ← t / 2;   θ ← θ − tδ
L8  until t ‖δ‖ ≤ tol (1 + ‖θ‖)
L9  return θ
```

Here $J(\theta) = L(\theta) + \frac{\lambda}{2}\|w\|^2$. Line L3 must compute $\sigma$ and $\log(1 + e^z)$ without overflow: use $\sigma(z) = e^z/(1 + e^z)$ when $z < 0$, and $\log(1 + e^z) = \max(z, 0) + \log(1 + e^{-|z|})$.

**Newton is IRLS.** With $\lambda = 0$, the Newton update can be written as

$$\theta_{\text{new}} = (\tilde X^\top S\tilde X)^{-1}\tilde X^\top S\,u, \qquad u = \tilde X\theta + S^{-1}(y - p).$$

This is a [weighted least squares](/ordinary-least-squares/) fit of the working response $u$ on $\tilde X$ with weights $p_i(1 - p_i)$. The weights and the working response change at each step, so the method is called iteratively reweighted least squares. It is the same as the IRLS of [generalized linear models](/generalized-linear-model/), because the logit is the canonical link of the Bernoulli distribution.

**Gradient descent.** $\nabla^2 L \preceq \frac14\tilde X^\top\tilde X$, so the gradient is Lipschitz with constant $\frac14\|\tilde X\|_2^2$, and [gradient descent](/gradient-descent/) with step $\eta \le 4/\|\tilde X\|_2^2$ decreases $J$ at each step. Each step costs only $O(nd)$, against $O(nd^2 + d^3)$ for Newton, but it needs many more steps. For large $n$, [stochastic gradient descent](/stochastic-gradient-descent/) uses one example at a time: $\theta \leftarrow \theta - \eta(p_i - y_i)\tilde x_i$.

## Example

Fit $P(y = 1 \mid x) = \sigma(b + wx)$ to six points, two of which overlap:

| $x$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $y$ | 0 | 0 | 1 | 0 | 1 | 1 |

At $\theta = 0$, all $p_i = 1/2$, so line L4 gives $g = (\sum(1/2 - y_i), \sum x_i(1/2 - y_i)) = (0, -3.5)$, and line L5 gives $H = \frac14\begin{pmatrix} 6 & 21 \\ 21 & 91 \end{pmatrix}$. Line L6 gives $\delta = (2.8, -0.8)$, and the full step $t = 1$ passes the test of line L7.

| step | $b$ | $w$ | $L(\theta)$ |
|---|---|---|---|
| 0 | 0 | 0 | $6\log 2 = 4.15888$ |
| 1 | $-2.80000$ | $0.80000$ | 2.60645 |
| 2 | $-3.88422$ | $1.10978$ | 2.48487 |
| 3 | $-4.22144$ | $1.20612$ | 2.47802 |
| 4 | $-4.24893$ | $1.21398$ | 2.47799 |
| 5 | $-4.24910$ | $1.21403$ | 2.47799 |

The number of correct digits roughly doubles at each step from step 3 on: this is the quadratic convergence of Newton's method. The labels are symmetric about $x = 3.5$ (the label of $7 - x$ is $1$ minus the label of $x$), so the fit has $b = -3.5w$ and $P(y = 1 \mid x = 3.5) = 1/2$.

**Separable data.** Take $x = (-2, -1, 1, 2)$ with $y = (0, 0, 1, 1)$, which the point $x = 0$ separates. The bias stays at 0 by symmetry, and Newton gives

| step | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $w$ | 1.200 | 2.024 | 2.909 | 3.856 | 4.835 | 5.827 | 6.825 | 7.823 |
| $L$ | 0.7002 | 0.2829 | 0.1121 | 0.0427 | 0.0160 | 0.0059 | 0.0022 | 0.0008 |

The weight grows by about 1 at each step and the loss falls by a factor of about $e$, toward the infimum 0, which no finite $w$ reaches. With $\lambda = 0.1$, Newton stops after 7 steps at the finite minimizer $w = 2.277$, and with $\lambda = 0.01$ at $w = 3.945$.

## Correctness

Assume that $J$ has a minimizer and that $H$ is positive definite at each iterate. This holds if $\lambda > 0$ and both labels occur, or if $\lambda = 0$, $\tilde X$ has full rank and the data overlap. Then $\delta = H^{-1}g$ is a descent direction, and the line search of line L7 accepts a step of size at least some $t_{\min} > 0$. Each step lowers $J$ by at least a constant times $\|g\|^2$. So $\|g\| \to 0$, line L8 stops, and the limit solves the score equations, which for the convex $J$ means the global minimum. Near the minimum the full step is accepted, and convergence is quadratic (Boyd and Vandenberghe, Section 9.5). The proof below gives the details.

## Complexity

On a [real RAM](/real-ram/), one Newton step costs $O(nd)$ for $p$ and $g$, $O(nd^2)$ for $H$, and $O(d^3)$ for Cholesky. The line search costs $O(nd)$ for each trial. With $k$ steps the total is $O(k(nd^2 + d^3))$. Because of quadratic convergence, $k$ is usually small, 5 to 10 in practice. The extra memory is $\Theta(nd)$ for $\tilde X$ and $\Theta(d^2)$ for $H$. Gradient descent costs $O(nd)$ for each step and $O(d)$ memory beyond the data, but the number of steps grows with the condition number of the problem.

## Properties

### Existence: separation and overlap

Albert and Anderson (1984) classify the data into three cases:

- **Complete separation.** Some $\theta$ has $\tilde x_i^\top\theta > 0$ for all $y_i = 1$ and $< 0$ for all $y_i = 0$. Then $L(t\theta) = \sum_i \log(1 + e^{-t|\tilde x_i^\top\theta|}) \to 0$ as $t \to \infty$, but $L > 0$ for each finite $\theta$. So the infimum is not reached, and the maximum likelihood estimate does not exist. Every minimizing sequence has $\|\theta\| \to \infty$.
- **Quasi-complete separation.** The same with $\ge$ and $\le$, with equality for some points. The estimate does not exist either.
- **Overlap.** Neither of the above. Then the estimate exists, and it is unique when $\tilde X$ has full rank.

With an L2 penalty $\lambda > 0$ (and both labels present), $J$ is strictly convex and grows to infinity in every direction, so it has exactly one minimizer, for each data set. The weights then grow like $\log(1/\lambda)$ on separable data, as the example shows. Without a penalty, gradient descent on separable data has $\|w_t\| \to \infty$ like $\log t$, and its direction $w_t/\|w_t\|$ converges to the direction of the hard margin [support vector machine](/support-vector-machine/) (Soudry et al. 2018).

### Other properties

- **Calibration of the bias.** With an unpenalized intercept, $\sum_i p_i = \sum_i y_i$ at the optimum.
- **The decision boundary is linear.** $P(y = 1 \mid x) > 1/2$ exactly when $b + w^\top x > 0$, a hyperplane. Features such as $x^2$ give curved boundaries in the original space.
- **The coefficients are log odds ratios.** Increasing $x_j$ by 1 multiplies the odds $p/(1 - p)$ by $e^{w_j}$.
- **The Fisher information** is $\tilde X^\top S\tilde X$. Its inverse at the estimate is the usual estimate of the covariance of $\hat\theta$, which gives standard errors and Wald tests.
- **Generative link.** If the two classes are Gaussian with a shared covariance matrix, the true posterior $P(y = 1 \mid x)$ has exactly this form. Logistic regression fits it without the Gaussian assumption.

## Variants and improvements

- **[Softmax regression](/softmax-regression/).** The same model for $K > 2$ classes.
- **L1 penalty.** The [lasso](/lasso-regression/) penalty gives sparse weights. glmnet fits it by coordinate descent inside each IRLS step.
- **Quasi-Newton methods.** [L-BFGS](/limited-memory-bfgs/) is the default solver in many libraries when $d$ is large, because it never forms the $d \times d$ Hessian.
- **Stochastic methods.** SGD, SAG and SAGA for very large $n$.
- **Probit and complementary log-log.** Other links in the [GLM](/generalized-linear-model/) family with $\Phi(z)$ or $1 - \exp(-e^z)$ in place of $\sigma(z)$.
- **Firth's correction.** A penalty with the Jeffreys prior that gives a finite estimate on separable data and reduces the small-sample bias.

## When to use it

Use logistic regression for binary classification when you want calibrated probabilities, coefficients that are easy to read, and a fast, convex fit with a unique answer. It is the standard baseline for classification and the standard model for binary outcomes in statistics. Add an L2 penalty by default in machine learning, so that the fit exists on separable data. When the classes are not linearly separable in a useful way, add features, or use kernel methods, trees or neural networks.

## Pitfalls

- **Separable data with no penalty.** The weights grow without bound and the fitted probabilities become 0 and 1. Software reports a warning, very large coefficients or huge standard errors. Add a penalty, or report that the classes are separated.
- **Overflow.** $e^{z}$ overflows for $z > 709$ in double precision. Compute $\sigma$ and $\log(1 + e^z)$ in the stable forms of line L3.
- **Full Newton steps.** Without the line search of line L7, Newton can overshoot when the start is far from the optimum.
- **Reading the output as a class.** The model gives probabilities. The threshold $1/2$ is right only when the two kinds of error cost the same.
- **Penalizing the bias.** With a penalty on $b$, the fitted probabilities no longer add up to the number of positives, and the fit depends on how the classes are balanced.

## Implementations

## History

The logistic function was introduced by Verhulst in the 1830s for population growth. Berkson (1944) proposed the logit for bioassay, as an alternative to the probit. Cox (1958) developed regression for binary outcomes with the logistic model. Nelder and Wedderburn (1972) placed it in the family of generalized linear models and fitted it with iteratively reweighted least squares. Albert and Anderson (1984) gave the conditions for the estimate to exist. In machine learning it became the basic linear classifier with probabilities, and the last layer of many neural networks.

## References
