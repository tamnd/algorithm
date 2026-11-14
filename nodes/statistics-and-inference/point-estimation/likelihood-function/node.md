---
tag: T1231X
kind: definition
slug: likelihood-function
name: Likelihood function
aliases:
- likelihood
area: statistics-and-inference/point-estimation
level: intro
summary: The probability or density of the observed data, viewed as a function of the parameter with the data held fixed. Its logarithm is the log-likelihood.
prereqs: [probability-distribution, independent-random-variables, estimator]
see_also: [maximum-likelihood-estimation, score-function, sufficient-statistic, likelihood-ratio-test, fisher-information-matrix, marginal-likelihood, bayesian-inference, method-of-moments]
sources:
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 6.3.1 (the likelihood function) and Section 6.3.2 (the formal likelihood principle and Birnbaum's theorem)
  - paper: doi:10.1098/rsta.1922.0009
    title: R. A. Fisher, On the mathematical foundations of theoretical statistics, Philosophical Transactions of the Royal Society A 222, 1922
    locator: pp. 309 to 368 (the likelihood of a parameter value and its distinction from a probability)
  - paper: doi:10.1080/01621459.1962.10480660
    title: Allan Birnbaum, On the foundations of statistical inference, Journal of the American Statistical Association 57(298), 1962
    locator: pp. 269 to 306 (sufficiency and conditionality imply the likelihood principle)
  - paper: doi:10.1080/00031305.1976.10479154
    title: D. V. Lindley and L. D. Phillips, Inference for a Bernoulli process (a Bayesian view), The American Statistician 30(3), 1976
    locator: pp. 112 to 119 (9 heads and 3 tails under a binomial and a negative binomial stopping rule)
---

The likelihood function of a statistical model is the probability, or the density, of the data that were actually observed, read as a function of the parameter. The data are held fixed and the parameter varies. It measures how well each parameter value accounts for the observations, and it is the common input of [maximum likelihood estimation](/maximum-likelihood-estimation/), the [score function](/score-function/), the [likelihood ratio test](/likelihood-ratio-test/) and [Bayesian inference](/bayesian-inference/). It is not a probability distribution over the parameter.

## Definition

Let a model give the data $X$ the density or mass function $f(x; \theta)$, $\theta \in \Theta$, with respect to one fixed measure (counting measure for discrete data, Lebesgue measure for continuous data). For an observed value $x$, the likelihood function is the map

$$L(\theta; x) = f(x; \theta), \qquad \theta \in \Theta.$$

The log-likelihood is $\ell(\theta; x) = \log L(\theta; x)$, with $\ell = -\infty$ where $L = 0$.

**Independent data.** If $x = (x_1, \ldots, x_n)$ are observations of independent $X_i$ with densities $f_i(x_i; \theta)$, then

$$L(\theta; x) = \prod_{i=1}^n f_i(x_i; \theta), \qquad \ell(\theta; x) = \sum_{i=1}^n \log f_i(x_i; \theta).$$

For iid data all $f_i$ equal $f$.

**Defined up to a factor.** Two likelihood functions $L_1(\cdot; x)$ and $L_2(\cdot; y)$ on the same $\Theta$ carry the same information about $\theta$ if $L_1(\theta; x) = c\, L_2(\theta; y)$ for all $\theta$, with $c > 0$ free of $\theta$. Only ratios $L(\theta_1; x)/L(\theta_2; x)$ have meaning, which is why a change of the dominating measure, or a one-to-one change of the data such as a change of units, does not matter: both multiply $L$ by a factor free of $\theta$. Constant factors such as binomial coefficients and $(2\pi)^{-n/2}$ are often dropped.

**What it is not.** $L(\cdot; x)$ is not a density in $\theta$:

1. Its integral over $\Theta$ need not be 1, and need not be finite.
2. Under a one-to-one reparametrization $\eta = g(\theta)$, the likelihood function of $\eta$ is $L(g^{-1}(\eta); x)$, with no Jacobian factor. A density in $\theta$ would pick up $\lvert d g^{-1}/d\eta \rvert$. So the point that maximizes $L$ moves with $g$, $\hat\eta = g(\hat\theta)$, while the mode of a density does not in general.
3. A statement such as "$\theta$ is in $A$ with likelihood 0.3" has no meaning. Turning $L$ into a distribution over $\theta$ needs a prior, through [Bayes' theorem](/bayes-theorem/): the posterior is proportional to the prior times $L$.

**Relative likelihood.** When $L$ has a finite maximum $L(\hat\theta; x) > 0$, the relative likelihood $R(\theta) = L(\theta; x)/L(\hat\theta; x)$ lies in $[0, 1]$ and is free of the constant factor.

**The likelihood principle.** It states: if two experiments about the same $\theta$ give data $x$ and $y$ whose likelihood functions are proportional, then the evidence about $\theta$ from $x$ and from $y$ is the same. Birnbaum (1962) proved that it follows from two principles that most statisticians accept, the sufficiency principle and a conditionality principle (Casella and Berger, Section 6.3.2). Bayesian inference and pure likelihood methods obey it. Methods that use the sampling distribution, such as p-values and unbiasedness, depend on outcomes that were not observed and can violate it, as the second example below shows. Birnbaum's argument and its consequences are still debated; this page states the principle and does not take a side.

## Examples and non-examples

**Bernoulli data.** Five iid Bernoulli$(p)$ trials give 3 successes, in the order $(1, 0, 1, 1, 0)$. Then

$$L(p) = p^3 (1 - p)^2, \qquad \ell(p) = 3 \log p + 2 \log(1 - p), \qquad 0 \le p \le 1.$$

$\ell'(p) = 3/p - 2/(1-p) = 0$ gives the maximum at $\hat p = 3/5$, where $L = 0.6^3 \cdot 0.4^2 = 0.03456$. At $p = 1/2$, $L = 0.03125$, so $p = 0.6$ explains the data $0.03456/0.03125 = 1.10592$ times better than $p = 0.5$, which is weak evidence. If only the count 3 is recorded, $L(p) = \binom{5}{3} p^3 (1-p)^2$: a constant factor of 10, the same information.

The integral is $\int_0^1 p^3 (1-p)^2 \, dp = B(4, 3) = 3!\,2!/6! = 1/60$, not 1, which shows item 1 above. In terms of the odds $\eta = p/(1-p)$, $L = \eta^3/(1+\eta)^5$, maximized at $\eta = 1.5 = 0.6/0.4$, as item 2 says.

**Proportional likelihoods, different p-values.** Lindley and Phillips (1976) took 9 heads and 3 tails and the null value $p = 1/2$ for the head probability, against $p > 1/2$.

- If the plan was 12 tosses, the count of heads is Binomial$(12, p)$ and $L(p) = \binom{12}{9} p^9 (1-p)^3$. The one-sided p-value is $P(\text{heads} \ge 9) = (220 + 66 + 12 + 1)/4096 = 299/4096 = 0.0730$.
- If the plan was to toss until the third tail, the count of heads is negative binomial and $L(p) = \binom{11}{9} p^9 (1-p)^3$. The p-value is $P(\text{heads} \ge 9) = 67/2048 = 0.0327$.

The two likelihood functions differ by the factor $220/55 = 4$, so the likelihood principle says the evidence is the same. The p-values differ, and only the second is below 0.05, because they add up the probabilities of outcomes that did not happen, and those depend on the stopping rule.

**Normal data.** For iid $N(\mu, \sigma^2)$ data, by the second equal form on [sample variance](/sample-variance/),

$$\ell(\mu, \sigma^2) = -\frac n2 \log(2\pi\sigma^2) - \frac{\mathrm{SS} + n(\bar x - \mu)^2}{2\sigma^2}, \qquad \mathrm{SS} = \sum_i (x_i - \bar x)^2.$$

It depends on the data only through $(\bar x, \mathrm{SS})$, which is a [sufficient statistic](/sufficient-statistic/). For $x = (3, 7, 7, 9, 14)$, $\bar x = 8$ and $\mathrm{SS} = 64$, and $\ell$ is largest at $\mu = 8$, $\sigma^2 = 64/5 = 12.8$, the divisor-$n$ variance $\hat\sigma^2$.

**A discontinuous likelihood function.** For iid Uniform$(0, \theta)$ data, $f(x; \theta) = \theta^{-1}$ for $0 \le x \le \theta$, so

$$L(\theta) = \theta^{-n} \text{ for } \theta \ge \max_i x_i, \qquad L(\theta) = 0 \text{ for } \theta < \max_i x_i.$$

For the data above, $L(\theta) = \theta^{-5}$ for $\theta \ge 14$ and 0 below. It jumps at 14, is largest there, and has no zero derivative, so the score equation does not find the maximum.

**Censored data.** If a lifetime is only known to exceed $c$, its factor in $L$ is $P_\theta(X > c)$, not a density value. Factors of different kinds may be multiplied as long as each is taken with respect to its own fixed measure, since the measures do not depend on $\theta$.

**Non-example: the density at a fixed parameter.** $x \mapsto f(x; \theta_0)$ for a fixed $\theta_0$ is the model density, not the likelihood function. The two are the same formula read in two directions.

**Non-example: a product in floating point.** The product $\prod_i f(x_i; \theta)$ of 1000 density values near $10^{-3}$ is about $10^{-3000}$, far below the smallest positive double, about $4.9 \times 10^{-324}$, so it rounds to 0 for every $\theta$. Work with $\ell$, a sum of logs, and with differences of $\ell$ instead of ratios of $L$.

## Related definitions

- [Maximum likelihood estimation](/maximum-likelihood-estimation/): choose $\hat\theta$ to maximize $L(\theta; x)$; that page has its properties and failures.
- [Score function](/score-function/): the gradient of $\ell$ in $\theta$; its variance is the Fisher information, see [Fisher information matrix](/fisher-information-matrix/).
- [Sufficient statistic](/sufficient-statistic/): $T$ is sufficient exactly when $L(\theta; x)$ depends on $x$ only through $T(x)$, up to a factor free of $\theta$.
- [Likelihood ratio test](/likelihood-ratio-test/): compares the maximum of $L$ over a null set with its maximum over $\Theta$.
- [Marginal likelihood](/marginal-likelihood/): the integral of $L$ against a prior, the normalizing constant of the posterior; it is a number for each model, not a function of $\theta$.
- [Method of moments](/method-of-moments/): an estimator that does not use the likelihood function.

## References
