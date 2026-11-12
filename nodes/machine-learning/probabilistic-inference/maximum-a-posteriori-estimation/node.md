---
tag: WXKGVJ
kind: problem
slug: maximum-a-posteriori-estimation
name: Maximum a posteriori estimation
aliases:
- MAP estimation
- MAP estimate
- posterior mode estimate
area: machine-learning/probabilistic-inference
level: core
summary: "Pick the parameter at the mode of the posterior: maximize log-likelihood plus log prior. Gaussian priors give ridge, Laplace priors give lasso. Not invariant to reparameterization."
prereqs: [bayesian-inference, maximum-likelihood-estimation]
see_also: [ridge-regression, lasso-regression, regularization, elastic-net, weight-decay, conjugate-prior, map-inference, naive-bayes-classifier]
sources:
  - book: isbn:9780262018029
    title: "Kevin P. Murphy, Machine Learning: A Probabilistic Perspective, MIT Press, 2012"
    locator: Section 5.2.1 (MAP estimation and its drawbacks, including the dependence on the parameterization) and Section 7.5 (ridge regression as MAP estimation)
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Exercise 1.4 (the mode of a density moves under a nonlinear change of variable), Section 1.2.5 (MAP for curve fitting gives regularized least squares) and Section 3.1.4 (regularized least squares and the Laplace-type penalty)
  - paper: doi:10.1111/j.2517-6161.1996.tb02080.x
    title: "Robert Tibshirani, Regression Shrinkage and Selection via the Lasso, Journal of the Royal Statistical Society B 58(1), 1996"
    locator: pp. 267-288 (the lasso estimate as the posterior mode under independent double-exponential priors)
---

Maximum a posteriori (MAP) estimation picks the parameter value at the mode of the posterior distribution. It maximizes the log-likelihood plus the log prior, so it is maximum likelihood with a penalty. Many regularized estimators are MAP estimates: a Gaussian prior on regression weights gives [ridge regression](/ridge-regression/), and a Laplace prior gives [lasso regression](/lasso-regression/). Unlike the [maximum likelihood estimate](/maximum-likelihood-estimation/), the MAP estimate depends on how the parameter is written, because a density changes by a Jacobian factor under a change of variable.

## In plain words

Maximum likelihood picks the setting that best explains the data. MAP also takes into account how plausible each setting was before you saw the data. It picks the single most plausible setting after both are combined. A prior that prefers small values pulls the answer toward zero, which is why MAP reduces overfitting when there is little data. As the data grow, the prior matters less and MAP comes close to maximum likelihood. One warning: the "most plausible point" of a spread of belief depends on the units you use to measure it. If you describe the same unknown by its logarithm or its square, the peak can move to a different place.

## Definition

**Input.** A likelihood $p(D \mid \theta)$ and a prior density (or mass function) $p(\theta)$ on $\Theta \subseteq \mathbb{R}^d$.

**Output.** A maximizer of the posterior density

$$
\hat\theta_{\mathrm{MAP}} \in \arg\max_{\theta} p(\theta \mid D) = \arg\max_{\theta} \big[\log p(D \mid \theta) + \log p(\theta)\big].
$$

The evidence $p(D)$ does not depend on $\theta$, so it drops out. The maximizer may fail to exist (the posterior density can be unbounded) or be at the edge of $\Theta$.

**Decision view.** For a discrete $\theta$, the MAP estimate minimizes the posterior probability of error, that is, the expected 0-1 loss. For a continuous $\theta$ every point has posterior probability 0, so MAP is not the Bayes estimate for any smooth loss: the posterior mean minimizes expected squared error and the posterior median minimizes expected absolute error.

**Not invariant.** Let $\eta = g(\theta)$ with $g$ smooth and one-to-one. The posterior density of $\eta$ is

$$
p_\eta(\eta \mid D) = p_\theta(g^{-1}(\eta) \mid D)\,\left|\frac{d g^{-1}(\eta)}{d\eta}\right| .
$$

The Jacobian factor depends on $\eta$, so in general $\arg\max p_\eta \ne g(\arg\max p_\theta)$. The likelihood has no Jacobian, since it is a function of $\theta$ and not a density in $\theta$, so the MLE is invariant.

## Variants

- **Penalized likelihood.** Maximize $\ell(\theta) - \lambda R(\theta)$ for a penalty $R$. When $e^{-\lambda R}$ is integrable this is MAP with prior $p(\theta) \propto e^{-\lambda R(\theta)}$; see [regularization](/regularization/).
- **MAP in a latent-variable model.** Maximize $\log \sum_z p(D, z \mid \theta) + \log p(\theta)$. EM handles it by adding $\log p(\theta)$ to the M-step.
- **Type II MAP.** Maximize the [marginal likelihood](/marginal-likelihood/) times a prior over hyperparameters, after integrating out the parameters.
- **MAP inference in graphical models.** Find the most probable joint assignment of the hidden variables given the evidence. It is the same arg max applied to discrete hidden variables, and is treated on its own page, [MAP inference](/map-inference/).

## Examples

**Beta-Bernoulli.** With a $\mathrm{Beta}(a, b)$ prior and $s$ ones in $n$ trials, the posterior is $\mathrm{Beta}(a + s, b + n - s)$, and when both parameters exceed 1 its mode is

$$
\hat\theta_{\mathrm{MAP}} = \frac{a + s - 1}{a + b + n - 2} .
$$

With $a = b = 2$ and 6 ones in 8 trials, $\hat\theta_{\mathrm{MAP}} = 7/10$, against the MLE $3/4$. With $a = b = 1$ (a flat prior), MAP equals the MLE. As $n$ grows with $s/n$ fixed, the gap shrinks like $1/n$.

**The same posterior in the logit.** Write $\eta = \log(\theta/(1 - \theta))$. Since $d\theta/d\eta = \theta(1 - \theta)$, the $\mathrm{Beta}(8, 4)$ posterior has density in $\eta$ proportional to $\theta^8(1 - \theta)^4$ with $\theta = \sigma(\eta)$. This is maximized at $\theta = 8/12 = 2/3$. So the MAP estimate of $\eta$ is $\log 2 \approx 0.693$, which is not $\operatorname{logit}(7/10) = \log(7/3) \approx 0.847$. The same data and the same prior give two different MAP answers, $7/10$ and $2/3$, depending on the scale on which the mode is taken. The MLE is $3/4$ on both scales. The test file finds both modes by a grid search.

**Dirichlet-multinomial (add-one smoothing).** With a $\mathrm{Dirichlet}(\alpha_1, \ldots, \alpha_K)$ prior and counts $N_k$, the MAP estimate is $(N_k + \alpha_k - 1)/(N + \sum_j \alpha_j - K)$. With all $\alpha_k = 2$ this is add-one (Laplace) smoothing: the counts $(5, 2, 0)$ give $(6, 3, 1)/10$, so the unseen class does not get probability 0, as it would under the MLE. The [naive Bayes classifier](/naive-bayes-classifier/) uses this smoothing.

**Gaussian prior gives ridge regression.** Let $y = Xw + \varepsilon$ with $\varepsilon \sim \mathcal{N}(0, \sigma^2 I)$ and prior $w \sim \mathcal{N}(0, \tau^2 I)$. The negative log posterior is, up to a constant,

$$
\frac{1}{2\sigma^2}\|y - Xw\|^2 + \frac{1}{2\tau^2}\|w\|^2 ,
$$

and multiplying by $2\sigma^2$ gives the ridge objective $\|y - Xw\|^2 + \lambda\|w\|^2$ with $\lambda = \sigma^2/\tau^2$. The MAP estimate is $(X^\top X + \lambda I)^{-1}X^\top y$. A weaker prior (larger $\tau^2$) means less shrinkage. In neural networks the same penalty is called [weight decay](/weight-decay/).

**Laplace prior gives the lasso.** With independent priors $p(w_j) = \frac{1}{2b}e^{-|w_j|/b}$, the negative log posterior times $2\sigma^2$ is $\|y - Xw\|^2 + \lambda\|w\|_1$ with $\lambda = 2\sigma^2/b$. The kink of $|w_j|$ at 0 makes some MAP weights exactly 0. The test file solves it by coordinate descent with soft thresholding and checks that an irrelevant weight is set to exactly 0, while the ridge estimate on the same data leaves it nonzero. A sum of both penalties is the [elastic net](/elastic-net/).

## Known algorithms

The algorithms are those of maximum likelihood with an extra term: closed forms for conjugate models, Newton's method and gradient methods for smooth priors, and coordinate descent or proximal gradient methods for the nonsmooth $\ell_1$ penalty. A log-concave prior with a log-concave likelihood gives a concave objective with no spurious local maxima. Examples are a Gaussian or Laplace prior with logistic or Gaussian regression.

## Bounds

- **Agreement with the MLE.** If the prior density is continuous and positive at the true parameter, $\log p(\theta)$ is $O(1)$ while $\ell(\theta)$ grows like $n$. The MAP estimate and the MLE then differ by $O(1/n)$ in regular models and have the same limit distribution.
- **Shrinkage in finite samples.** For linear regression the ridge estimate is biased, but for a suitable $\lambda > 0$ its mean squared error is smaller than that of least squares; see the [bias-variance tradeoff](/bias-variance-tradeoff/).
- **A mode is not typical.** In high dimension the posterior mass can lie far from the mode. The MAP point then summarizes the posterior poorly, and it gives no measure of uncertainty. For a $\mathrm{Beta}(a, b)$ posterior with $a < 1$, the density is unbounded at 0 and no MAP estimate exists.

## Reductions

- **MLE is MAP with a flat prior.** With $p(\theta)$ constant on a bounded $\Theta$, the two coincide.
- **MAP is penalized MLE.** Every prior with a positive density gives the penalty $-\log p(\theta)$, and every penalty with $\int e^{-\lambda R} < \infty$ is a prior.
- **MAP in a changed parameterization.** Maximizing $p_\theta(\theta \mid D)\,|\det J(\theta)|^{-1}$, where $J$ is the Jacobian of $g$, gives the MAP of $\eta = g(\theta)$. So any choice of scale can be expressed as a MAP problem in $\theta$ with a modified prior.

## Applications

- Regularized regression and classification: [ridge](/ridge-regression/), [lasso](/lasso-regression/), regularized [logistic regression](/logistic-regression/).
- Smoothed count estimates in [conditional probability tables](/conditional-probability-table/) and naive Bayes.
- Training neural networks with weight decay.
- Image denoising and restoration with Markov random field priors, where the MAP image is computed by optimization.

## References
