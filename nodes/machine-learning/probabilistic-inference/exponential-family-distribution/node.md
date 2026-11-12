---
tag: RGQ0M9
kind: definition
slug: exponential-family-distribution
name: Exponential family distribution
aliases:
- exponential family
area: machine-learning/probabilistic-inference
level: advanced
summary: "A family p(x | eta) = h(x) exp(eta . T(x) - A(eta)). A is convex, its gradient is E[T] and its Hessian is Cov[T]; sum T(x_i) is sufficient; members maximize entropy given E[T]."
history:
  year: 1936
  people: [Bernard O. Koopman, Edwin J. G. Pitman]
  note: In separate 1936 papers, Koopman and Pitman showed that, under regularity conditions, families with a sufficient statistic of fixed dimension are of this exponential form.
prereqs: [probability-distribution, convex-function]
see_also: [conjugate-prior, maximum-likelihood-estimation, generalized-linear-model, fisher-information-matrix, bregman-divergence, convex-conjugate, shannon-entropy, natural-gradient-descent]
sources:
  - paper: doi:10.1561/2200000001
    title: "Martin J. Wainwright and Michael I. Jordan, Graphical Models, Exponential Families, and Variational Inference, Foundations and Trends in Machine Learning 1(1-2), 2008"
    locator: Chapter 3 (exponential families, the log-partition function and its derivatives, mean parameters, conjugate duality and maximum entropy)
  - book: isbn:9780534243128
    title: "George Casella and Roger L. Berger, Statistical Inference, 2nd edition, Duxbury, 2002"
    locator: Section 3.4 (exponential families) and Section 6.2 (sufficient statistics of exponential families)
  - paper: doi:10.1090/S0002-9947-1936-1501854-3
    title: "B. O. Koopman, On Distributions Admitting a Sufficient Statistic, Transactions of the American Mathematical Society 39(3), 1936"
    locator: pp. 399-409
  - paper: doi:10.1017/S0305004100019307
    title: "E. J. G. Pitman, Sufficient Statistics and Intrinsic Accuracy, Mathematical Proceedings of the Cambridge Philosophical Society 32(4), 1936"
    locator: pp. 567-579
  - paper: doi:10.1103/PhysRev.106.620
    title: "E. T. Jaynes, Information Theory and Statistical Mechanics, Physical Review 106(4), 1957"
    locator: pp. 620-630 (maximum entropy subject to expectation constraints gives the exponential form)
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 2.4 (the exponential family, maximum likelihood and sufficient statistics, conjugate priors)
---

An exponential family is a set of probability distributions whose densities have the form $p(x \mid \eta) = h(x)\exp(\eta^\top T(x) - A(\eta))$, for a fixed base function $h$, a fixed statistic $T$, a parameter vector $\eta$, and the normalizer $A$. The Bernoulli, binomial, Poisson, Gaussian, gamma, beta, categorical and Dirichlet distributions are all of this form, and so are discrete Markov random fields such as the Ising model. The form explains several facts at once: the log-likelihood is concave in $\eta$, the derivatives of $A$ are the moments of $T$, the sum $\sum_i T(x_i)$ is a sufficient statistic of fixed size, conjugate priors exist, and each member has the largest entropy among all distributions with the same mean of $T$.

## Definition

Let $\nu$ be a measure on a space $\mathcal{X}$ (counting measure or Lebesgue measure), $h : \mathcal{X} \to [0, \infty)$ a base function, and $T : \mathcal{X} \to \mathbb{R}^d$ a statistic. Define the **log-partition function**

$$
A(\eta) = \log \int_{\mathcal{X}} h(x)\, e^{\eta^\top T(x)}\, \nu(dx)
$$

and the **natural parameter space** $\mathcal{N} = \{\eta \in \mathbb{R}^d : A(\eta) < \infty\}$. The **exponential family** with base $h$ and sufficient statistic $T$ is the set of densities

$$
p(x \mid \eta) = h(x)\exp\big(\eta^\top T(x) - A(\eta)\big), \qquad \eta \in \mathcal{N} .
$$

The family is **minimal** when the components of $T$ satisfy no affine relation $a^\top T(x) = c$ that holds $\nu$-almost everywhere with $a \ne 0$, and **regular** when $\mathcal{N}$ is open. A family written with a parameter $\theta$ and $\eta = \eta(\theta)$ is still an exponential family; $\eta$ is its natural (canonical) parameter.

**Properties.**

1. *$\mathcal{N}$ is convex and $A$ is convex on it.* For $\lambda \in (0, 1)$, Hölder's inequality with exponents $1/\lambda$ and $1/(1 - \lambda)$ gives $\int h e^{(\lambda\eta + (1-\lambda)\eta')^\top T} \le \left(\int h e^{\eta^\top T}\right)^{\lambda}\left(\int h e^{\eta'^\top T}\right)^{1-\lambda}$. Take logarithms.
2. *$\nabla A(\eta) = \mathbb{E}_\eta[T(X)]$.* In the interior of $\mathcal{N}$ the integral may be differentiated under the integral sign, so $\partial_j A = \int T_j h e^{\eta^\top T} d\nu \big/ \int h e^{\eta^\top T} d\nu = \mathbb{E}_\eta[T_j]$.
3. *$\nabla^2 A(\eta) = \operatorname{Cov}_\eta[T(X)]$.* Differentiating again, $\partial_j\partial_k A = \mathbb{E}_\eta[T_j T_k] - \mathbb{E}_\eta[T_j]\,\mathbb{E}_\eta[T_k]$. A covariance matrix is positive semidefinite, which again shows convexity. In a minimal family it is positive definite, so $A$ is strictly convex and $\eta \mapsto \mu = \nabla A(\eta)$ is one-to-one: the **mean parameters** $\mu$ describe the family as well as $\eta$ does.
4. *Sufficiency.* For i.i.d. $x_1, \ldots, x_n$, $\prod_i p(x_i \mid \eta) = \left(\prod_i h(x_i)\right)\exp\big(\eta^\top \sum_i T(x_i) - nA(\eta)\big)$, so by the factorization theorem $\sum_i T(x_i)$ is sufficient for $\eta$. Its dimension is $d$ for every $n$.
5. *Maximum likelihood matches moments.* The log-likelihood $\eta^\top \sum_i T(x_i) - nA(\eta)$ is concave, and its stationary point solves $\nabla A(\hat\eta) = \frac{1}{n}\sum_i T(x_i)$; see [maximum likelihood estimation](/maximum-likelihood-estimation/).
6. *Fisher information.* The [Fisher information matrix](/fisher-information-matrix/) in $\eta$ is $\nabla^2 A(\eta) = \operatorname{Cov}_\eta[T]$.

**Maximum entropy.** Let $\mu$ be a vector and suppose $p_\eta$ in the family has $\mathbb{E}_{p_\eta}[T] = \mu$. Measure entropy relative to $h$: $H_h(q) = -\int q \log(q/h)\, d\nu$. Then for every density $q$ with $\mathbb{E}_q[T] = \mu$,

$$
H_h(q) \le H_h(p_\eta), \quad \text{with equality only for } q = p_\eta .
$$

*Proof.* Since $\log(p_\eta/h) = \eta^\top T - A(\eta)$, we get $0 \le \mathrm{KL}(q \,\|\, p_\eta) = \int q \log(q/h) - \int q\,(\eta^\top T - A(\eta)) = -H_h(q) - \eta^\top\mu + A(\eta)$. For $q = p_\eta$ the same computation gives $H_h(p_\eta) = A(\eta) - \eta^\top\mu$. So $H_h(q) \le H_h(p_\eta)$, with equality only when the KL divergence is 0. This is Jaynes's (1957) principle: the least committal distribution that matches given expectations is an exponential family with those expectations as $T$. With $h = 1$ on a finite set, $H_h$ is the [Shannon entropy](/shannon-entropy/).

**Pitman-Koopman-Darmois theorem (statement only).** Consider a family of densities on $\mathbb{R}$ whose support does not depend on the parameter, with smoothness conditions on the densities. If for i.i.d. samples of every size $n$ there is a sufficient statistic whose dimension stays bounded as $n$ grows, then the family is an exponential family (Koopman 1936; Pitman 1936). The support condition is needed: $\mathrm{Uniform}(0, \theta)$ has the one-dimensional sufficient statistic $\max_i x_i$, but it is not an exponential family.

## Examples and non-examples

| family | $T(x)$ | $\eta$ | $A(\eta)$ | $h(x)$ |
|---|---|---|---|---|
| Bernoulli($\theta$) | $x$ | $\log\frac{\theta}{1-\theta}$ | $\log(1 + e^\eta)$ | 1 on $\{0, 1\}$ |
| Poisson($\lambda$) | $x$ | $\log\lambda$ | $e^\eta$ | $1/x!$ on $\{0, 1, \ldots\}$ |
| $\mathcal{N}(\mu, \sigma^2)$ | $(x, x^2)$ | $\left(\frac{\mu}{\sigma^2}, -\frac{1}{2\sigma^2}\right)$ | $-\frac{\eta_1^2}{4\eta_2} - \frac12\log(-2\eta_2)$ | $(2\pi)^{-1/2}$ |
| Exponential($\lambda$) | $x$ | $-\lambda$ | $-\log(-\eta)$ | 1 on $(0, \infty)$ |
| Gamma($\alpha, \beta$) | $(\log x, x)$ | $(\alpha - 1, -\beta)$ | $\log\Gamma(\eta_1 + 1) - (\eta_1 + 1)\log(-\eta_2)$ | 1 on $(0, \infty)$ |
| Categorical($\pi$) on $K$ values | one-hot $x$ | $\log \pi$ | $\log \sum_k e^{\eta_k}$ (0 at $\eta = \log\pi$) | 1 |

**Checking the derivatives.** For the Bernoulli at $\eta = \log 3$, $A'(\eta) = e^\eta/(1 + e^\eta) = 3/4 = \mathbb{E}[X]$ and $A''(\eta) = \frac34 \cdot \frac14 = 3/16 = \operatorname{Var}[X]$. For the Poisson, $A' = A'' = e^\eta = \lambda$, the mean and the variance. For $\mathcal{N}(1, 2)$, $\eta = (1/2, -1/4)$, and the gradient of $A$ is $(\mathbb{E}[X], \mathbb{E}[X^2]) = (1, 3)$. The Hessian is

$$
\operatorname{Cov}[(X, X^2)] = \begin{pmatrix} \sigma^2 & 2\mu\sigma^2 \\ 2\mu\sigma^2 & 2\sigma^4 + 4\mu^2\sigma^2 \end{pmatrix} = \begin{pmatrix} 2 & 4 \\ 4 & 16 \end{pmatrix}.
$$

The test file computes $A$, $\mathbb{E}[T]$ and $\operatorname{Cov}[T]$ from the definition, by summation or numerical integration, and compares them with finite differences of the closed-form $A$ for the Bernoulli, Poisson and Gaussian families.

**The categorical family is not minimal as written.** Since the one-hot components sum to 1, the table above is an overcomplete representation, and $\eta$ and $\eta + c\mathbf{1}$ give the same distribution. Dropping one component gives the minimal form $\eta_k = \log(\pi_k/\pi_K)$ for $k < K$ and $A(\eta) = \log(1 + \sum_{k<K} e^{\eta_k})$; the gradient of this $A$ is the softmax function.

**Maximum entropy on a finite set.** On $\{0, 1, \ldots, 5\}$ with mean $1.5$, the maximum entropy distribution is $p_k \propto r^k$ with $r \approx 0.690$, that is, $p \approx (0.348, 0.240, 0.165, 0.114, 0.079, 0.054)$. It is the member of the family with $T(x) = x$ and $\eta = \log r$. The test file checks that random perturbations that keep the sum and the mean lower the entropy.

**Graphical models.** A discrete [Markov random field](/markov-random-field/) with positive potentials is an exponential family: for the [Ising model](/ising-model/), $T(x)$ collects the $x_i$ and the products $x_i x_j$ over the edges, and $A(\eta) = \log Z(\eta)$ is the log of the partition function.

**Non-examples.**

- $\mathrm{Uniform}(0, \theta)$ and other families whose support depends on the parameter: $h(x)e^{\eta^\top T(x)}$ is positive on a set that does not depend on $\eta$.
- The Cauchy location family $p(x \mid \theta) = \frac{1}{\pi(1 + (x - \theta)^2)}$, and the Laplace location family $\frac{1}{2}e^{-|x - \theta|}$: neither log-density is of the form $\eta(\theta)^\top T(x)$ plus terms that depend on only one of $x$ and $\theta$.
- A mixture of two Gaussians with unknown means: the density is a sum of exponentials, not one exponential. A mixture of exponential family distributions is in general not one.

## Related definitions

- **Mean parameters and duality.** The convex conjugate $A^*(\mu) = \sup_\eta \{\eta^\top\mu - A(\eta)\}$ equals $-H_h(p_{\eta(\mu)})$, the negative entropy of the member with mean $\mu$; see [convex conjugate](/convex-conjugate/). The KL divergence between two members is the [Bregman divergence](/bregman-divergence/) of $A$: $\mathrm{KL}(p_{\eta} \,\|\, p_{\eta'}) = A(\eta') - A(\eta) - \nabla A(\eta)^\top(\eta' - \eta)$.
- **Curved exponential family.** The natural parameter is restricted to a curve or a lower-dimensional surface $\eta = \eta(\theta)$, as in $\mathcal{N}(\mu, \mu^2)$. Sufficiency still holds, but the likelihood need not be concave in $\theta$.
- **Conjugate prior.** The prior $\pi(\eta) \propto \exp(\eta^\top\chi - \nu A(\eta))$ is [conjugate](/conjugate-prior/): the posterior after $n$ observations has $\chi + \sum_i T(x_i)$ and $\nu + n$.
- **Generalized linear model.** A [generalized linear model](/generalized-linear-model/) sets the natural parameter of an exponential family response to a linear function of the inputs; the canonical link is $(\nabla A)^{-1}$. [Logistic regression](/logistic-regression/) is the Bernoulli case.
- **Natural gradient.** Since the Fisher metric is $\nabla^2 A$, the natural gradient with respect to $\eta$ is $(\nabla^2 A)^{-1}\nabla_\eta L = \nabla_\mu L$, the ordinary gradient with respect to the mean parameters, by the chain rule $\partial\mu/\partial\eta = \nabla^2 A$; see [natural gradient descent](/natural-gradient-descent/).

## References
