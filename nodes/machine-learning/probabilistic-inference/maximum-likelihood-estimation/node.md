---
tag: 8RHNEA
kind: problem
slug: maximum-likelihood-estimation
name: Maximum likelihood estimation
aliases:
- MLE
- maximum likelihood estimator
area: machine-learning/probabilistic-inference
level: core
summary: "Pick the parameter that gives the observed data the highest probability. Invariant, consistent and efficient in regular models; fails in Neyman-Scott and mixtures."
history:
  year: 1922
  people: [Ronald A. Fisher]
  note: Fisher used the method in 1912 and named it, with the likelihood, consistency and efficiency, in his 1922 paper on the foundations of statistics.
prereqs: [probability-distribution, independent-random-variables]
see_also: [fisher-information-matrix, maximum-a-posteriori-estimation, expectation-maximization, exponential-family-distribution, logistic-regression, ordinary-least-squares, gaussian-mixture-model, newton-raphson-method]
sources:
  - paper: doi:10.1098/rsta.1922.0009
    title: "R. A. Fisher, On the Mathematical Foundations of Theoretical Statistics, Philosophical Transactions of the Royal Society A 222, 1922"
    locator: pp. 309-368
  - paper: doi:10.2307/1914288
    title: "J. Neyman and Elizabeth L. Scott, Consistent Estimates Based on Partially Consistent Observations, Econometrica 16(1), 1948"
    locator: pp. 1-32 (the inconsistent variance estimate with many nuisance means)
  - book: isbn:9780534243128
    title: "George Casella and Roger L. Berger, Statistical Inference, 2nd edition, Duxbury, 2002"
    locator: Section 7.2.2 (maximum likelihood estimators, Theorem 7.2.10 on invariance), Section 7.3.2 (the Cramér-Rao inequality) and Section 10.1 (consistency and asymptotic efficiency of MLEs)
  - book: isbn:9780521784504
    title: "A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998"
    locator: Chapter 5 (M- and Z-estimators, consistency and asymptotic normality of the MLE)
---

Maximum likelihood estimation picks, from a family of probability models $\{p(\cdot \mid \theta) : \theta \in \Theta\}$, the parameter under which the observed data are most probable. It is the default way to fit a statistical model. In regular models it is consistent, asymptotically normal, and asymptotically efficient: no unbiased estimator has a smaller variance in the limit. It can also fail. With many nuisance parameters it can be inconsistent, and for mixtures of Gaussians the likelihood has no maximum.

## In plain words

You have data and a model with some unknown settings. For each setting, the model says how likely the data you saw would be. Maximum likelihood picks the setting that makes your data most likely. For coin tosses, this is the fraction of heads. For a bell curve, it is the sample average and the average squared distance from it. If you report the answer in other units, for example as a square or a logarithm, you get the same choice in the new units. With a lot of data from a well-behaved model, the answer gets close to the truth and is about as precise as any method can be. It can mislead when the number of unknowns grows with the data.

## Definition

**Input.** A parametric family of densities or mass functions $p(x \mid \theta)$, $\theta \in \Theta \subseteq \mathbb{R}^d$, and data $x_1, \ldots, x_n$ that are i.i.d. given $\theta$.

**Output.** A maximizer

$$
\hat\theta \in \arg\max_{\theta \in \Theta} L(\theta), \qquad L(\theta) = \prod_{i=1}^n p(x_i \mid \theta),
$$

or, equivalently, of the log-likelihood $\ell(\theta) = \sum_i \log p(x_i \mid \theta)$. A maximizer need not exist or be unique. When $\ell$ is differentiable and $\hat\theta$ is interior, it solves the likelihood equation $\nabla \ell(\theta) = 0$; the gradient $\nabla \ell$ is the score.

**Invariance.** If $\tau = g(\theta)$ for any function $g$, define the induced likelihood $L^*(\tau) = \sup\{L(\theta) : g(\theta) = \tau\}$. Then $g(\hat\theta)$ maximizes $L^*$ (Casella and Berger, Theorem 7.2.10). *Proof.* For every $\tau$, $L^*(\tau) \le \sup_\theta L(\theta) = L(\hat\theta) \le L^*(g(\hat\theta))$, where the last step holds because $\hat\theta$ is one of the $\theta$ with $g(\theta) = g(\hat\theta)$. So the MLE of $\theta^2$ is $\hat\theta^2$ and the MLE of $\log \theta$ is $\log \hat\theta$. This property does not hold for the [MAP estimate](/maximum-a-posteriori-estimation/).

**Exponential families.** If $p(x \mid \eta) = h(x)\exp(\eta^\top T(x) - A(\eta))$, then $\ell(\eta) = n(\eta^\top \bar T - A(\eta)) + \text{const}$ with $\bar T = \frac{1}{n}\sum_i T(x_i)$. Since $A$ is convex and $\nabla A(\eta) = \mathbb{E}_\eta[T]$, the likelihood equation is

$$
\mathbb{E}_{\hat\eta}[T(X)] = \bar T :
$$

the MLE matches the expected sufficient statistics to their sample averages. The log-likelihood is concave, so a stationary point is a global maximum. It exists only when $\bar T$ lies in the interior of the set of possible means. See [exponential family distribution](/exponential-family-distribution/).

## Variants

- **Conditional maximum likelihood.** Maximize $\prod_i p(y_i \mid x_i, \theta)$ for a model of outputs given inputs, as in [logistic regression](/logistic-regression/) and [generalized linear models](/generalized-linear-model/).
- **Penalized likelihood.** Maximize $\ell(\theta) - \lambda R(\theta)$. When $R$ is a negative log prior this is [MAP estimation](/maximum-a-posteriori-estimation/); a squared norm gives [ridge regression](/ridge-regression/).
- **Incomplete data.** With hidden variables $z$, maximize the marginal $\sum_z p(x, z \mid \theta)$. [Expectation maximization](/expectation-maximization/) does this by a sequence of complete-data fits.
- **Profile and restricted likelihood.** Maximize over nuisance parameters first, or use a likelihood that does not depend on them. Restricted (residual) likelihood removes the bias of the Neyman-Scott example below.
- **Constrained MLE.** Maximize over a subset of $\Theta$, for example monotone or nonnegative parameters, or the parameters allowed by a graph in a [graphical model](/graphical-model/).

## Examples

**Bernoulli.** With $s$ ones in $n$ trials, $\ell(\theta) = s\log\theta + (n - s)\log(1 - \theta)$ and $\hat\theta = s/n$. For 6 ones in 8 trials, $\hat\theta = 3/4$. By invariance the MLE of the log odds is $\log 3$, which is also the root of the moment equation $\sigma(\eta) = 3/4$ in the natural parameter.

**Gaussian.** For $\mathcal{N}(\mu, \sigma^2)$, $\hat\mu = \bar x$ and $\hat\sigma^2 = \frac{1}{n}\sum_i (x_i - \bar x)^2$. For the data $1, 2, 6$: $\hat\mu = 3$ and $\hat\sigma^2 = 14/3$. Since $\mathbb{E}[\hat\sigma^2] = \frac{n-1}{n}\sigma^2$, the MLE of the variance is biased, but the bias vanishes as $n \to \infty$.

**Uniform.** For $\mathrm{Uniform}(0, \theta)$, $L(\theta) = \theta^{-n}$ when $\theta \ge \max_i x_i$ and 0 otherwise, so $\hat\theta = \max_i x_i$. The maximum is at a boundary of the region where $L > 0$, not at a zero of the score.

**Neyman-Scott.** Let $x_{ij} \sim \mathcal{N}(\mu_i, \sigma^2)$ for strata $i = 1, \ldots, k$ and $j = 1, \ldots, m$, with a separate mean per stratum. The MLE is $\hat\mu_i = \bar x_i$ and

$$
\hat\sigma^2 = \frac{1}{km}\sum_{i,j}(x_{ij} - \bar x_i)^2, \qquad \mathbb{E}[\hat\sigma^2] = \frac{m-1}{m}\sigma^2 .
$$

The expectation holds because each stratum contributes $\mathbb{E}\sum_j (x_{ij} - \bar x_i)^2 = (m - 1)\sigma^2$. If $m$ stays fixed and $k \to \infty$, $\hat\sigma^2 \to \frac{m-1}{m}\sigma^2$: with pairs ($m = 2$) it converges to $\sigma^2/2$. More data never fixes it, because each new stratum brings a new parameter. The test file checks the expectation exactly, by enumerating a three-point noise with variance $1/2$, and the limit $\sigma^2/2$ by simulation.

**Unbounded mixture likelihood.** For a mixture $\frac12\mathcal{N}(\mu_1, \sigma_1^2) + \frac12\mathcal{N}(\mu_2, \sigma_2^2)$, set $\mu_1 = x_1$ and let $\sigma_1 \to 0$. The first component's density at $x_1$ grows like $1/\sigma_1$, while the second component keeps every other point's density bounded away from 0. So $L \to \infty$ and there is no MLE. Fitting a [Gaussian mixture model](/gaussian-mixture-model/) therefore looks for a good local maximum, or bounds the variances from below.

## Known algorithms

- **Closed form.** Counts, sample means and sample covariances for the Bernoulli, multinomial, Poisson and Gaussian families, and the counts $N(x, u)/N(u)$ for each [conditional probability table](/conditional-probability-table/) of a Bayesian network.
- **Newton and Fisher scoring.** Iterate $\theta \leftarrow \theta + J(\theta)^{-1}\nabla\ell(\theta)$ with $J$ the observed or the expected information. For GLMs this is iteratively reweighted least squares. See the [Newton-Raphson method](/newton-raphson-method/).
- **Gradient methods.** Stochastic [gradient descent](/gradient-descent/) on $-\ell$ for large models such as neural networks. [Natural gradient descent](/natural-gradient-descent/) preconditions by the Fisher information.
- **EM** for models with hidden variables. Each step does not lower the likelihood, but it can stop at a local maximum.

For exponential families the problem is concave and these methods find the global optimum. For mixtures and other latent-variable models the log-likelihood is not concave and has many local maxima.

## Bounds

**Fisher information and Cramér-Rao.** For one observation, $I(\theta) = \mathbb{E}_\theta[(\partial_\theta \log p(X \mid \theta))^2] = -\mathbb{E}_\theta[\partial_\theta^2 \log p(X \mid \theta)]$ under regularity conditions. Any unbiased estimator $T$ from $n$ i.i.d. observations has

$$
\operatorname{Var}_\theta(T) \ge \frac{1}{n I(\theta)}
$$

(Casella and Berger, Section 7.3.2; the multivariate form uses the [Fisher information matrix](/fisher-information-matrix/)). For the Bernoulli, $I(\theta) = 1/(\theta(1 - \theta))$ and $\operatorname{Var}(s/n) = \theta(1 - \theta)/n$, so the MLE attains the bound exactly.

**Consistency.** If the model is identifiable, $\Theta$ is compact or $\ell$ is concave, and suitable continuity and integrability conditions hold, then $\hat\theta_n \to \theta_0$ in probability (van der Vaart, Chapter 5). The proof uses the [law of large numbers](/law-of-large-numbers/) on $\frac{1}{n}\ell$ and the fact that $\mathbb{E}_{\theta_0}\log p(X \mid \theta)$ is maximized at $\theta_0$, by [Jensen's inequality](/jensens-inequality/).

**Asymptotic normality and efficiency.** Under further smoothness, with $\theta_0$ interior and a support that does not depend on $\theta$,

$$
\sqrt{n}\,(\hat\theta_n - \theta_0) \xrightarrow{d} \mathcal{N}\!\left(0, I(\theta_0)^{-1}\right),
$$

so the MLE reaches the Cramér-Rao bound in the limit. The proof expands the score around $\theta_0$ and uses the [central limit theorem](/central-limit-theorem/) on $\nabla\ell(\theta_0)$.

**Where the bounds fail.** The uniform family breaks the support condition; there $\hat\theta$ converges at rate $1/n$, not $1/\sqrt{n}$. Neyman-Scott breaks the fixed dimension: the number of parameters grows with $n$. Mixtures break identifiability and boundedness.

## Reductions

- **To KL minimization.** Maximizing $\frac{1}{n}\ell(\theta)$ is the same as minimizing the cross-entropy between the empirical distribution $\hat p$ and $p(\cdot \mid \theta)$, or $\mathrm{KL}(\hat p \,\|\, p_\theta)$, since the entropy of $\hat p$ does not depend on $\theta$.
- **Least squares.** With $y_i = f(x_i; \theta) + \varepsilon_i$ and $\varepsilon_i \sim \mathcal{N}(0, \sigma^2)$, the MLE of $\theta$ minimizes the sum of squared residuals; for a linear $f$ it is [ordinary least squares](/ordinary-least-squares/).
- **MAP with a flat prior.** With a constant prior on a bounded $\Theta$, the MAP estimate equals the MLE.

## Applications

- Fitting [logistic regression](/logistic-regression/), [generalized linear models](/generalized-linear-model/) and the [naive Bayes classifier](/naive-bayes-classifier/).
- Learning the tables of a [Bayesian network](/bayesian-network/) from complete data, and the parameters of hidden Markov models and Gaussian mixtures by EM.
- Training most neural networks: minimizing the cross-entropy loss is maximizing a conditional likelihood.
- Model scores such as BIC start from the maximized likelihood; see [marginal likelihood](/marginal-likelihood/).

## References
