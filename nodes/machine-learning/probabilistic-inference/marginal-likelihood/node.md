---
tag: 04WZ19
kind: concept
slug: marginal-likelihood
name: Marginal likelihood
aliases:
- model evidence
area: machine-learning/probabilistic-inference
level: intro
summary: "p(D | M), the probability of the data under a model with its parameters averaged over the prior. Ratios of it are Bayes factors; Laplace and BIC approximate it."
history:
  year: 1935
  people: [Harold Jeffreys, Gideon Schwarz]
  note: Jeffreys compared hypotheses by the ratio of their marginal likelihoods, now the Bayes factor. Schwarz in 1978 gave the large-sample approximation now called BIC.
prereqs: [bayesian-inference, conjugate-prior]
see_also: [maximum-likelihood-estimation, maximum-a-posteriori-estimation, evidence-lower-bound, variational-inference, importance-sampling, gaussian-process, partition-function, minimum-description-length]
sources:
  - paper: doi:10.1080/01621459.1995.10476572
    title: "Robert E. Kass and Adrian E. Raftery, Bayes Factors, Journal of the American Statistical Association 90(430), 1995"
    locator: pp. 773-795 (definition, the scale for reading Bayes factors, the Laplace and Schwarz approximations, and the history back to Jeffreys)
  - paper: doi:10.1214/aos/1176344136
    title: "Gideon Schwarz, Estimating the Dimension of a Model, Annals of Statistics 6(2), 1978"
    locator: pp. 461-464
  - paper: doi:10.1080/01621459.1986.10478240
    title: "Luke Tierney and Joseph B. Kadane, Accurate Approximations for Posterior Moments and Marginal Densities, Journal of the American Statistical Association 81(393), 1986"
    locator: pp. 82-86 (accuracy of the Laplace method)
  - book: isbn:9780521642989
    title: "David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003"
    locator: Chapter 27 (Laplace's method) and Chapter 28 (Model Comparison and Occam's Razor)
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 3.4 (Bayesian model comparison), Section 3.5 (the evidence approximation) and Section 4.4 (the Laplace approximation, with BIC in 4.4.1)
---

The marginal likelihood of a model $M$ is the probability it gives to the observed data $D$ when its parameters $\theta$ are averaged over the prior:

$$
p(D \mid M) = \int p(D \mid \theta, M)\, p(\theta \mid M)\, d\theta .
$$

It is the normalizing constant in [Bayes' theorem](/bayes-theorem/) for the posterior of $\theta$. Inside one model it is a constant and does not matter. Across models it is the score that Bayesian model comparison uses: the ratio of two marginal likelihoods is the Bayes factor. It rewards a model for fitting the data, and it penalizes a model with a broad prior, which spreads its predictions over many possible data sets. That penalty is called the Bayesian Occam effect.

## In plain words

A model with unknown settings makes many possible predictions, one for each setting. Before you see the data, the model has a spread of belief over its settings. The marginal likelihood asks what probability the model as a whole gave, in advance, to the data that you then saw. It is an average over the settings, not the score of the best setting. A very flexible model can explain almost anything, but each particular outcome then gets only a small share of its belief. A narrow model that bets on the outcome that happened gets a high score. To compare two models, divide their scores. The result tells you how much the data should shift your belief from one model to the other.

## The idea

**The normalizer.** For one model, [Bayesian inference](/bayesian-inference/) writes

$$
p(\theta \mid D) = \frac{p(D \mid \theta)\, p(\theta)}{p(D)} .
$$

The posterior needs $p(D)$ only as a constant. The value of $p(D)$ itself is the probability of the data under the model, before any fit. It is a proper distribution over data sets: summed over all possible $D$ it is 1.

**The chain rule view.** For data $x_1, \ldots, x_n$,

$$
p(D) = \prod_{i=1}^n p(x_i \mid x_1, \ldots, x_{i-1}),
$$

the product of the posterior predictive probabilities of each point given the points before it. So the evidence scores a model by how well it predicts each new point from the old ones, a form of sequential [cross-validation](/cross-validation/). The product does not depend on the order of the data when the data are exchangeable.

**Closed form for conjugate models.** When the prior is [conjugate](/conjugate-prior/), the integral is a ratio of normalizing constants. For a Bernoulli parameter with a $\mathrm{Beta}(a, b)$ prior and one ordered sequence with $s$ ones and $f$ zeros,

$$
p(D) = \int_0^1 \theta^s (1 - \theta)^f\, \frac{\theta^{a-1}(1 - \theta)^{b-1}}{B(a, b)}\, d\theta = \frac{B(a + s, b + f)}{B(a, b)} .
$$

If only the count $s$ is reported, multiply by $\binom{n}{s}$.

**Bayes factors.** For two models $M_0$ and $M_1$, Bayes' theorem in odds form gives

$$
\frac{P(M_1 \mid D)}{P(M_0 \mid D)} = \underbrace{\frac{p(D \mid M_1)}{p(D \mid M_0)}}_{\text{Bayes factor } K} \cdot \frac{P(M_1)}{P(M_0)} .
$$

Kass and Raftery give a scale for reading $K$: from 1 to 3 is barely worth a mention, from 3 to 20 is positive, from 20 to 150 is strong, and above 150 is very strong evidence for $M_1$.

**The Occam effect.** Both models must spread a total probability of 1 over all possible data sets. A model with more freedom spreads it more thinly. If the data fall where a simple model puts its mass, the simple model wins even though the complex model, at its best parameter, fits at least as well. The maximized likelihood cannot show this, because a larger model never has a lower maximum.

**The Laplace approximation.** Let $g(\theta) = \log p(D \mid \theta) + \log p(\theta)$, with maximum $\theta^*$ (the [MAP estimate](/maximum-a-posteriori-estimation/)) and $A = -\nabla^2 g(\theta^*)$. A second-order expansion of $g$ and a Gaussian integral give, for $d$ parameters,

$$
\log p(D) \approx g(\theta^*) + \frac{d}{2}\log(2\pi) - \frac{1}{2}\log \det A .
$$

Under regularity conditions, the relative error of $p(D)$ is $O(1/n)$ (Tierney and Kadane 1986).

**BIC.** For i.i.d. data, $A$ grows like $n$ times a fixed matrix, so $\log \det A = d \log n + O(1)$. Drop all terms that stay bounded and replace $\theta^*$ by the [maximum likelihood estimate](/maximum-likelihood-estimation/) $\hat\theta$:

$$
\log p(D) = \log p(D \mid \hat\theta) - \frac{d}{2}\log n + O(1).
$$

This is the Bayesian information criterion of Schwarz (1978); $-2$ times the right side is the usual BIC score. The $O(1)$ error does not vanish, so BIC is a poor estimate of the evidence itself. But the term $\frac{d}{2}\log n$ grows, so under regularity conditions BIC picks the true model among a finite list as $n \to \infty$.

**Sensitivity to the prior.** The posterior of $\theta$ forgets the prior as $n$ grows; the evidence does not. If a prior is made wider, the evidence falls roughly in proportion to its width, because the same likelihood is averaged over a larger range. With an improper prior the evidence is defined only up to an arbitrary constant, so Bayes factors need proper priors on the parameters that differ between the models.

## Examples

**Is the coin fair?** Let $M_0$ say $\theta = 1/2$ with no free parameter, and let $M_1$ put a uniform prior $\mathrm{Beta}(1, 1)$ on $\theta$. Then $p(D \mid M_0) = 2^{-10}$ for any sequence of 10 tosses, and $p(D \mid M_1) = B(s + 1, f + 1) = s!\,f!/11!$.

| ones in 10 tosses | $p(D \mid M_1)$ | $p(D \mid M_0)$ | Bayes factor $K$ |
|---|---|---|---|
| 5 | $1/2772$ | $1/1024$ | $256/693 \approx 0.37$ |
| 9 | $1/110$ | $1/1024$ | $512/55 \approx 9.3$ |
| 10 | $1/11$ | $1/1024$ | $1024/11 \approx 93$ |

With 5 ones, the data favor the fair coin by a factor of about 2.7, although the best $\theta$ under $M_1$ is also $1/2$ and fits equally well. The reason: under $M_1$ every count from 0 to 10 has prior predictive probability $1/11$, while $M_0$ puts $\binom{10}{5}/1024 \approx 0.25$ on the count 5. With 9 or 10 ones, $M_1$ wins.

**Laplace and BIC against the exact value.** Take the uniform prior and $s = 0.3n$ ones. The exact log evidence is $\log B(s + 1, n - s + 1)$. The test file compares it with the two approximations.

| $n$ | Laplace error in $\log p(D)$ | exact minus BIC |
|---|---|---|
| 10 | 0.064 | 0.075 |
| 100 | 0.0068 | 0.132 |
| 1000 | 0.00069 | 0.1379 |
| 10000 | 0.000069 | 0.1385 |

The Laplace error falls by a factor of 10 for each tenfold increase in $n$, so it is $O(1/n)$. The BIC gap tends to $\frac{1}{2}\log(2\pi \cdot 0.3 \cdot 0.7) \approx 0.1386$, the term that BIC drops.

**A Gaussian mean.** With $x_i \sim \mathcal{N}(\theta, \sigma^2)$ and $\theta \sim \mathcal{N}(\mu_0, \tau^2)$, the data vector is jointly Gaussian with mean $\mu_0 \mathbf{1}$ and covariance $\sigma^2 I + \tau^2 \mathbf{1}\mathbf{1}^\top$, and that density at $D$ is the evidence. As $\tau \to \infty$ it falls like $1/\tau$, which shows the prior sensitivity above.

## Where it is used

- **Model comparison and averaging.** Bayes factors compare models; posterior model probabilities weight the predictions of several models. [Minimum description length](/minimum-description-length/) gives a coding view of the same trade-off.
- **Hyperparameters.** Choosing prior or kernel parameters by maximizing the evidence is called type II maximum likelihood or empirical Bayes. It sets the kernel parameters of a [Gaussian process](/gaussian-process/) and the regularization strength in Bayesian linear regression.
- **Variational methods.** For any distribution $q(\theta)$, Jensen's inequality gives $\log p(D) \ge \mathbb{E}_q[\log p(D, \theta) - \log q(\theta)]$, the [evidence lower bound](/evidence-lower-bound/) that [variational inference](/variational-inference/) and the variational view of [expectation maximization](/expectation-maximization/) maximize.
- **Latent-variable models.** The likelihood of a mixture or a hidden Markov model is a marginal likelihood over the hidden variables. In an undirected model, the probability of the evidence is a ratio of two values of the [partition function](/partition-function/).
- **Monte Carlo estimates.** [Importance sampling](/importance-sampling/) estimates $p(D)$ as an average of $p(D \mid \theta)p(\theta)/q(\theta)$ over draws from $q$. Its variance is small only when $q$ is close to the posterior.

## References
