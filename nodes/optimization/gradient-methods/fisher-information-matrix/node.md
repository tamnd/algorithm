---
tag: WXMZKF
kind: definition
slug: fisher-information-matrix
name: Fisher information matrix
aliases:
- Fisher information
- expected information matrix
- Fisher metric
area: optimization/gradient-methods
level: advanced
summary: Expected outer product of the score function, defining the local geometry of a statistical model.
prereqs: [expected-value, maximum-likelihood-estimation, gradient]
see_also: [natural-gradient-descent, kronecker-factored-approximate-curvature, natural-policy-gradient, exponential-family-distribution, bregman-divergence, positive-definite-matrix, logistic-regression, variance]
sources:
  - paper: doi:10.1017/S0305004100009580
    title: R. A. Fisher, Theory of statistical estimation, Mathematical Proceedings of the Cambridge Philosophical Society 22(5), 1925
    locator: pages 700 to 725, the amount of information in a sample and the efficiency of estimates
  - book: isbn:9780387985022
    title: E. L. Lehmann and George Casella, Theory of Point Estimation, second edition, Springer, 1998
    locator: Chapter 2, the information inequality, the regularity conditions, and the information matrix of a multiparameter family
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 11.10, Fisher information and the Cramér-Rao inequality
  - paper: doi:10.1162/089976698300017746
    title: Shun-ichi Amari, Natural gradient works efficiently in learning, Neural Computation 10(2), 1998
    locator: pages 251 to 276, the Fisher information as the Riemannian metric of a statistical model
  - paper: "C. Radhakrishna Rao, Information and the accuracy attainable in the estimation of statistical parameters, Bulletin of the Calcutta Mathematical Society 37, 1945, pages 81 to 91"
    locator: the variance bound through the information, and the Fisher information as a metric
  - url: https://arxiv.org/abs/1905.12558
    title: Frederik Kunstner, Lukas Balles and Philipp Hennig, Limitations of the empirical Fisher approximation for natural gradient descent, NeurIPS 2019
    locator: Section 3, the difference between the Fisher and the empirical Fisher
---

The Fisher information matrix of a parametric family of distributions $p(y;\theta)$ is the covariance of the score, the [gradient](/gradient/) of $\log p(y;\theta)$ with respect to $\theta$. It measures how much one observation tells about $\theta$: large information means that a small change of $\theta$ changes the distribution a lot. Under regularity conditions it equals the expected negative Hessian of the log-likelihood, it is the Hessian of the Kullback-Leibler divergence at $\theta$, and its inverse bounds the variance of unbiased estimators. Fisher (1925) defined it, and [natural gradient descent](/natural-gradient-descent/) uses it as a metric.

## Definition

Let $\{p(\cdot;\theta) : \theta \in \Theta\}$ be a family of densities (or probability mass functions) on a space $\mathcal{Y}$, with $\Theta \subseteq \mathbb{R}^d$ open. Assume that $\log p(y;\theta)$ is differentiable in $\theta$ for each $y$. The **score** is $s(\theta; y) = \nabla_\theta\log p(y;\theta)$, and the **Fisher information matrix** is the $d \times d$ matrix

$$I(\theta) = \mathbb{E}_{y \sim p(\cdot;\theta)}\big[s(\theta; y)\,s(\theta; y)^\top\big], \qquad I(\theta)_{jk} = \mathbb{E}_\theta\Big[\frac{\partial\log p(y;\theta)}{\partial\theta_j}\,\frac{\partial\log p(y;\theta)}{\partial\theta_k}\Big].$$

The expectation is under the model at the same $\theta$, not under the data. For a conditional model $p(y \mid x;\theta)$ with inputs $x$ drawn from a distribution $q$, the Fisher information is $\mathbb{E}_{x \sim q}\mathbb{E}_{y \sim p(\cdot \mid x;\theta)}[ss^\top]$.

The results below need **regularity**: the support $\{y : p(y;\theta) > 0\}$ does not depend on $\theta$, and the integral $\int p(y;\theta)\,dy$ can be differentiated under the integral sign (once for the first result, twice for the second).

### Basic properties

**The score has mean zero.** $\mathbb{E}_\theta[s(\theta; y)] = \int\nabla_\theta p(y;\theta)\,dy = \nabla_\theta\int p(y;\theta)\,dy = \nabla_\theta 1 = 0$, where the first step uses $p\,\nabla\log p = \nabla p$. So $I(\theta)$ is the covariance matrix of the score.

**Information identity.** If $\log p$ is twice differentiable,

$$I(\theta) = -\mathbb{E}_\theta\big[\nabla_\theta^2\log p(y;\theta)\big].$$

Differentiate $\nabla\log p = \nabla p/p$ once more: $\nabla^2\log p = \nabla^2p/p - (\nabla p)(\nabla p)^\top/p^2 = \nabla^2p/p - ss^\top$. Take the expectation; $\mathbb{E}_\theta[\nabla^2p/p] = \int\nabla^2p\,dy = \nabla^2\int p\,dy = 0$.

**Positive semidefinite.** $v^\top I(\theta)v = \mathbb{E}_\theta[\langle v, s\rangle^2] \ge 0$. It is [positive definite](/positive-definite-matrix/) exactly when no nonzero combination $\langle v, s(\theta; y)\rangle$ is zero for almost every $y$, that is, when the parameters are locally identifiable to first order.

**Additive over independent samples.** For $N$ independent observations from $p(\cdot;\theta)$, the log-likelihood is a sum, the scores are independent with mean zero, and the information is $NI(\theta)$.

**Change of parameters.** If $\theta = g(\xi)$ with $g$ differentiable and Jacobian $J = \partial\theta/\partial\xi$, the chain rule gives $s_\xi = J^\top s_\theta$, so

$$I_\xi(\xi) = J^\top I_\theta(g(\xi))\,J.$$

This is how a metric tensor changes under a change of coordinates.

**Hessian of the KL divergence.** Under regularity with three derivatives, $\operatorname{KL}(p_\theta\,\Vert\,p_{\theta + \delta}) = \frac{1}{2}\delta^\top I(\theta)\delta + o(\lVert\delta\rVert^2)$. The value at $\delta = 0$ is $0$, the gradient in $\delta$ at $0$ is $-\mathbb{E}_\theta[s] = 0$, and the Hessian is $-\mathbb{E}_\theta[\nabla^2\log p] = I(\theta)$.

**Exponential families.** For an [exponential family](/exponential-family-distribution/) $p(y;\eta) = h(y)\exp(\langle\eta, T(y)\rangle - A(\eta))$ in the natural parameter $\eta$, the score is $T(y) - \nabla A(\eta)$, so $I(\eta) = \operatorname{Cov}_\eta(T) = \nabla^2A(\eta)$. It does not depend on $y$, and the Hessian of the negative log-likelihood equals $I(\eta)$ for every sample.

**Cramér-Rao bound.** For one parameter and an unbiased estimator $\hat\theta(y)$ of $\theta$ with finite [variance](/variance/), $\operatorname{Var}_\theta(\hat\theta) \ge 1/I(\theta)$. Differentiate $\mathbb{E}_\theta\hat\theta = \theta$ under the integral: $\mathbb{E}_\theta[\hat\theta\,s] = 1$. Since $\mathbb{E}_\theta s = 0$, this is $\operatorname{Cov}(\hat\theta, s) = 1$, and the Cauchy-Schwarz inequality gives $1 \le \operatorname{Var}(\hat\theta)\,I(\theta)$. In $d$ dimensions, $\operatorname{Cov}(\hat\theta) \succeq I(\theta)^{-1}$ when $I(\theta)$ is invertible.

## Examples and non-examples

**Bernoulli.** $p(y;q) = q^y(1 - q)^{1-y}$ for $y \in \{0, 1\}$. The score is $y/q - (1 - y)/(1 - q)$, and $I(q) = q\cdot\frac{1}{q^2} + (1 - q)\cdot\frac{1}{(1 - q)^2} = \frac{1}{q(1 - q)}$. At $q = 0.5$, $I = 4$; at $q = 0.9$, $I \approx 11.1$. In the natural parameter $\eta = \log(q/(1 - q))$, $dq/d\eta = q(1 - q)$, and the change of parameters gives $I(\eta) = q(1 - q)$, which is $A''(\eta)$ for $A(\eta) = \log(1 + e^\eta)$. This is the weight in each step of iteratively reweighted least squares for [logistic regression](/logistic-regression/).

**Gaussian.** For $N(m, \sigma^2)$ in the parameters $(m, \sigma)$, the score is $\big((y - m)/\sigma^2,\ -1/\sigma + (y - m)^2/\sigma^3\big)$, and

$$I(m, \sigma) = \begin{pmatrix} 1/\sigma^2 & 0 \\ 0 & 2/\sigma^2\end{pmatrix}.$$

The off-diagonal entry is $\mathbb{E}[(y - m)^3]/\sigma^5 - \mathbb{E}[y - m]/\sigma^3 = 0$. In the parameter $\sigma^2$ instead of $\sigma$, the second entry becomes $1/(2\sigma^4)$, by the change of parameters with $d\sigma/d\sigma^2 = 1/(2\sigma)$.

**Poisson.** For the Poisson distribution with mean $\lambda$, the score is $y/\lambda - 1$ and $I(\lambda) = \operatorname{Var}(y)/\lambda^2 = 1/\lambda$. The sample mean of $N$ observations has variance $\lambda/N$, so it attains the Cramér-Rao bound.

**Linear regression with Gaussian noise.** For $y = x^\top\theta + e$ with $e \sim N(0, \sigma^2)$ and inputs $x \sim q$, the Fisher information is $\mathbb{E}_q[xx^\top]/\sigma^2$, which does not depend on $\theta$.

**Non-example: a support that moves.** For the uniform distribution on $[0, \theta]$, $\log p(y;\theta) = -\log\theta$ on the support, so the score is $-1/\theta$ for every $y$. Its mean is $-1/\theta \ne 0$, because the support depends on $\theta$ and the derivative cannot pass under the integral. The information identity fails: $\mathbb{E}[s^2] = 1/\theta^2$, while $-\mathbb{E}[\partial^2\log p] = -1/\theta^2$. The Cramér-Rao bound fails as well: the estimator $\frac{N+1}{N}\max_iy_i$ is unbiased with variance $\theta^2/(N(N + 2))$, of order $1/N^2$.

**Non-example: the empirical Fisher.** The matrix $\frac{1}{N}\sum_i\nabla\log p(y_i \mid x_i;\theta)\nabla\log p(y_i \mid x_i;\theta)^\top$, with the observed labels $y_i$ in place of samples from the model, is not the Fisher information. It agrees with it only when the model fits the data, and preconditioning by it can give very different steps (Kunstner, Balles and Hennig 2019).

## Related definitions

- **Observed information.** $-\nabla^2\log p(y;\theta)$ at the data, without the expectation. At the maximum likelihood estimate it is a common estimate of $NI(\theta)$.
- **Fisher-Rao metric.** The Riemannian metric $\langle u, v\rangle_\theta = u^\top I(\theta)v$ on the parameter space. Rao (1945) proposed it, and the change of parameters rule above shows that it does not depend on the coordinates. Natural gradient descent is gradient descent in this metric (Amari 1998).
- **Generalized Gauss-Newton matrix.** For a model whose output is the natural parameter of an exponential family, the Fisher information equals the generalized Gauss-Newton matrix $\mathbb{E}[J^\top\nabla^2A\,J]$. [K-FAC](/kronecker-factored-approximate-curvature/) approximates it by Kronecker products for neural networks.
- **Bregman divergence.** In an exponential family, the KL divergence is the [Bregman divergence](/bregman-divergence/) of $A$ with the arguments swapped, and $\nabla^2A = I$. The quadratic expansion of the KL divergence above is then the second-order Taylor expansion of $D_A$.

## References
