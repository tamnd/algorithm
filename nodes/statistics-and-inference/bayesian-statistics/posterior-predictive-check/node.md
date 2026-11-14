---
tag: 2TJBEH
kind: technique
slug: posterior-predictive-check
name: Posterior predictive check
aliases:
- posterior predictive p-value
area: statistics-and-inference/bayesian-statistics
level: core
summary: Checks a Bayesian model by comparing a statistic of the data with its distribution in replicated data drawn from the posterior predictive.
history:
  year: 1984
  people: [Irwin Guttman, Donald B. Rubin, Andrew Gelman, Xiao-Li Meng, Hal Stern]
  note: Guttman (1967) proposed comparing data with their predictive distribution. Rubin (1984) defined the posterior predictive check and its p-value, and Gelman, Meng and Stern (1996) extended it to discrepancies that depend on the parameters. Meng (1994) bounded its error rate, and Robins, van der Vaart and Ventura (2000) showed that it is conservative.
prereqs: [posterior-predictive-distribution, p-value, bayesian-inference, monte-carlo-integration]
see_also: [simulation-based-calibration, chi-squared-goodness-of-fit-test, pareto-smoothed-importance-sampling-loo, widely-applicable-information-criterion, bayes-factor, hierarchical-bayesian-model, cross-validation, approximate-bayesian-computation]
sources:
  - paper: doi:10.1214/aos/1176346785
    title: "Donald B. Rubin, Bayesianly justifiable and relevant frequency calculations for the applied statistician, Annals of Statistics 12(4), 1984"
    locator: "pages 1151 to 1172: the posterior predictive distribution of a test statistic and the tail-area probability as a model check (general locator)"
  - paper: "Andrew Gelman, Xiao-Li Meng and Hal Stern, Posterior predictive assessment of model fitness via realized discrepancies, Statistica Sinica 6(4), 1996"
    title: Gelman, Meng and Stern 1996
    locator: "pages 733 to 807, with the discussion: discrepancies that depend on the parameters, their computation by simulation, and the chi-squared discrepancy (general locator)"
  - paper: doi:10.1214/aos/1176325622
    title: "Xiao-Li Meng, Posterior predictive p-values, Annals of Statistics 22(3), 1994"
    locator: "pages 1142 to 1160: the bound P(p <= alpha) <= 2 alpha under the prior predictive law, and the concentration of the p-value near 1/2 (general locator)"
  - paper: doi:10.1080/01621459.2000.10474310
    title: "James M. Robins, Aad van der Vaart and Valérie Ventura, Asymptotic distribution of p values in composite null models, Journal of the American Statistical Association 95(452), 2000"
    locator: "pages 1143 to 1156: the posterior predictive p-value is asymptotically conservative, with a law more concentrated near 1/2 than the uniform, when the mean of the statistic depends on the parameter (general locator)"
  - paper: "M. J. Bayarri and James O. Berger, P values for composite null models, Journal of the American Statistical Association 95(452), 2000"
    title: Bayarri and Berger 2000
    locator: "pages 1127 to 1142: the partial posterior predictive and conditional predictive p-values, which are closer to uniform (general locator)"
  - paper: doi:10.1111/j.2517-6161.1967.tb00676.x
    title: "Irwin Guttman, The use of the concept of a future observation in goodness-of-fit problems, Journal of the Royal Statistical Society Series B 29(1), 1967"
    locator: "pages 83 to 100 (general locator)"
---

A posterior predictive check asks whether data simulated from a fitted Bayesian model look like the observed data. Choose a test quantity $T(x, \theta)$, a statistic of the data that may also depend on the parameters. Draw $\theta$ from the posterior, draw a replicated data set $x^{\mathrm{rep}}$ of the same size from the model at $\theta$, and compare $T(x^{\mathrm{rep}}, \theta)$ with $T(x, \theta)$. Repeating this gives the [posterior predictive distribution](/posterior-predictive-distribution/) of the test quantity, and the posterior predictive p-value

$$p_B = P\big(T(x^{\mathrm{rep}}, \theta) \ge T(x, \theta) \mid x\big),$$

where the probability is over $\theta \sim \pi(\theta \mid x)$ and $x^{\mathrm{rep}} \sim f(\cdot \mid \theta)$. A value near $0$ or $1$ shows that the model cannot reproduce that feature of the data. The check uses only posterior draws and a simulator, so it applies to any model that can be fitted. Its p-value is not uniform when the model is true: it piles up near $1/2$, so it is conservative.

## In plain words

After fitting a model, use it to make fake data sets, as many as you like, each one the size of the real data. If the model describes the data well, the real data should look like one more fake data set. Pick a feature to compare, such as the largest value, the number of zeros, or how spread out the values are, and see where the real value falls among the fake ones. If it lies far out, beyond almost all fake values, the model misses that feature, and the feature tells you how to fix it. Because the fake data come from a model already fitted to the real data, they tend to resemble the real data more than they should, so the check is gentle: it rarely raises a false alarm, but it can miss real problems.

## When it applies

- **A fitted Bayesian model with posterior draws** $\theta_1, \ldots, \theta_S$, from [Markov chain Monte Carlo](/metropolis-hastings/) or any other sampler, and a way to simulate data from the model at a given $\theta$.
- **A question about fit.** The check looks for features of the data that the model does not capture, such as overdispersion, outliers, skewness, trends in residuals or dependence. It does not compare two models; for that, use [Bayes factors](/bayes-factor/) or predictive scores such as [WAIC](/widely-applicable-information-criterion/).
- **A test quantity chosen for the question.** The check has power only against misfit that changes $T$. A statistic that the model fits by construction, such as a sufficient statistic of its parameters, gives $p_B$ near $1/2$ whatever the data.

## The template

The holes are the test quantity `T` and the draws `θ_s` (the reference distribution).

```pseudo id=main
PPC(x, θ₁..θ_S, SIMULATE, T)
L1  count ← 0
L2  for s ← 1 to S                               ▷ hole: draws from the posterior
L3      x_rep ← SIMULATE(θ_s)                    ▷ same size and design as x
L4      if T(x_rep, θ_s) ≥ T(x, θ_s) then count ← count + 1   ▷ hole T
L5  return p_B ≈ count / S, and the pairs (T(x_rep, θ_s), T(x, θ_s)) for a plot
```

Common choices:

- *`T` a statistic of the data*: the maximum, the minimum, the number of zeros, the sample variance, an autocorrelation, or a quantile. Choose one the model does not fit directly.
- *`T` a discrepancy*: a function of both, such as the chi-squared discrepancy $\sum_i (x_i - \mathbb{E}[x_i \mid \theta])^2/\mathrm{Var}(x_i \mid \theta)$ of Gelman, Meng and Stern (1996). In L4 it is evaluated at the same $\theta_s$ for the real and the replicated data.
- *`θ_s` from the posterior*: the posterior predictive check. From the prior: a prior predictive check, which tests the prior as well. From the posterior without observation $i$: a cross-validated check of observation $i$.
- *Graphical*: plot the observed data among a few replicated data sets, or the observed $T$ on the histogram of replicated $T$. A plot often shows the kind of misfit better than the number $p_B$.

**Facts about $p_B$ when the model is true.** Suppose the data are drawn from the prior predictive law, that is, $\theta$ from the prior and $x$ from the model. Write $p_\theta(x) = P(T(X', \theta) \ge T(x, \theta) \mid \theta)$ for the classical p-value at a known $\theta$, so $p_B(x) = \mathbb{E}[p_\theta(x) \mid x]$.

*Mean.* $\mathbb{E}[p_B] = P(T(X', \theta) \ge T(X, \theta))$ with $X, X'$ independent given $\theta$. By symmetry this is $\frac12(1 + P(T(X', \theta) = T(X, \theta)))$, which is $\frac12$ for a continuous $T$.

*Meng's bound.* $P(p_B \le \alpha) \le 2\alpha$. *Proof.* $U = p_\theta(X)$ is a classical p-value at the true $\theta$, so $P(U \le u) \le u$ for every $u$, and its quantile function satisfies $Q_U(t) \ge t$. Let $A = \{p_B \le \alpha\}$, an event determined by $x$. Then $\mathbb{E}[U\mathbf{1}_A] = \mathbb{E}[p_B\mathbf{1}_A] \le \alpha P(A)$. Among all events of probability $P(A)$, $\mathbb{E}[U\mathbf{1}_A]$ is smallest when $A$ holds the smallest values of $U$, so $\mathbb{E}[U\mathbf{1}_A] \ge \int_0^{P(A)} Q_U(t)\, dt \ge P(A)^2/2$. Hence $P(A)^2/2 \le \alpha P(A)$, and $P(A) \le 2\alpha$. $\blacksquare$

So a check at level $\alpha$ never rejects a true model more often than $2\alpha$. In the other direction, $p_B$ is usually far more concentrated near $1/2$ than a uniform value, and a small $p_B$ is stronger evidence of misfit than the same classical p-value.

## Classic examples

**The normal mean: the pile-up near 1/2.** $x_1, \ldots, x_n \sim N(\theta, \sigma^2)$ with $\sigma$ known, prior $\theta \sim N(0, \tau^2)$, and $T = \bar x$. With $s^2 = \sigma^2/n$, the posterior is $N(m, v)$ with $v = \tau^2 s^2/(\tau^2 + s^2)$ and $m = v\bar x/s^2$, and $\bar x^{\mathrm{rep}} \mid x \sim N(m, v + s^2)$. So

$$p_B = \Phi\Big(\frac{m - \bar x}{\sqrt{v + s^2}}\Big) = \Phi(-cZ), \qquad Z = \frac{\bar x}{\sqrt{\tau^2 + s^2}}, \qquad c = \sqrt{\frac{s^2}{2\tau^2 + s^2}}.$$

When the model is true, $Z$ is standard normal, so $P(p_B \le \alpha) = \Phi(z_\alpha/c)$, with $z_\alpha = \Phi^{-1}(\alpha)$, and $\mathrm{Var}(p_B) = \arcsin\!\big(c^2/(1 + c^2)\big)/(2\pi)$. Since $c < 1$, $p_B$ is less spread than a uniform value, whose variance $1/12$ is the case $c = 1$. With $\sigma = \tau = 1$:

| $n$ | $c$ | sd of $p_B$ | $P(p_B \le 0.05)$ | $P(0.25 < p_B < 0.75)$ |
|---|---|---|---|---|
| 1 | 0.577 | 0.200 | 0.0022 | 0.757 |
| 10 | 0.218 | 0.085 | $2 \times 10^{-14}$ | above 0.999 |
| 100 | 0.071 | 0.028 | $10^{-120}$ | 1 |
| uniform | 1 | 0.289 | 0.05 | 0.5 |

With $n = 1$, $2000$ data sets from `random.Random(5)` and $S = 500$ draws each, the template gives sd $0.201$ and a share $0.752$ in $(0.25, 0.75)$. The sample mean is sufficient for $\theta$, so the posterior adapts to it and the check has almost no power for it. This is the conservative behaviour that Robins, van der Vaart and Ventura (2000) prove in general.

**An ancillary statistic gives an exact p-value.** In the same model, take $T = S^2$, the sample variance. Its law, $\frac{\sigma^2}{n-1}\chi^2_{n-1}$, does not depend on $\theta$, so the posterior predictive law of $T$ is its sampling law, $p_B$ is the classical chi-squared p-value, and $p_B$ is exactly uniform when the model is true. A test quantity whose law depends little on the parameters gives a check with nearly correct error rates.

**Overdispersed counts.** Model: $x_1, \ldots, x_{20} \sim$ Poisson($\lambda$) with $\lambda \sim$ Gamma(1, rate 0.25), so $\lambda \mid x \sim$ Gamma($1 + \sum x_i$, rate $20.25$). Test quantity: the dispersion index $T = s^2/\bar x$, near $1$ for [Poisson](/poisson-distribution/) data. With $S = 4000$:

| data | values | $T(x)$ | $p_B$ for $T = s^2/\bar x$ | $p_B$ for $T = \bar x$ | $p_B$ for $T = \max$ |
|---|---|---|---|---|---|
| A: Poisson(4) | 1, 1, 2, 3, 3, 3, 4 (ten times), 5, 5, 6, 7 | 0.54 | 0.949 | 0.493 | 0.814 |
| B: mixed Poisson, mean 4, variance 12 | 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4 (six times), 5, 5, 6, 29 | 8.45 | 0.000 | 0.495 | 0.000 |

The dispersion and the maximum both reject the Poisson model for data set B, whose value $29$ is impossible under a Poisson law with mean near $4$. The mean, a sufficient statistic, gives $p_B \approx 1/2$ for both data sets. The number of zeros, $1$ in B, gives $p_B = 0.27$ and misses the misfit too. A [hierarchical model](/hierarchical-bayesian-model/) with a gamma law for each count's rate, which gives negative binomial counts, is the usual fix. When the Poisson model is true ($400$ data sets drawn from the prior predictive), the dispersion index gives $p_B$ with sd $0.285$, close to uniform, while the mean gives sd $0.065$.

**The chi-squared discrepancy.** For a model with means $\mu_i(\theta)$ and variances $\sigma_i^2(\theta)$, the discrepancy $\sum_i (x_i - \mu_i(\theta))^2/\sigma_i^2(\theta)$ is the Bayesian form of the [chi-squared goodness-of-fit test](/chi-squared-goodness-of-fit-test/). It is evaluated at each posterior draw, for the observed and the replicated data, with no estimate plugged in and no degrees of freedom to count.

**Regression.** For a [linear regression](/linear-regression/), replicate the responses at the observed covariates and compare residual plots, or use $T$ = the correlation of the residuals with a covariate left out of the model, or the largest absolute residual.

## Variations

- **Prior predictive check.** Draw $\theta$ from the prior in L2. Its p-value is uniform under the model, but it rejects good models whose prior is vague.
- **Calibrated p-values.** Simulate many data sets from the prior predictive law, compute $p_B$ for each, and use their distribution to turn $p_B$ into a uniform p-value. This is costly, since every replicate needs a new posterior; it is the same loop as [simulation-based calibration](/simulation-based-calibration/), which checks the computation instead of the model.
- **Partial posterior predictive and conditional predictive p-values** (Bayarri and Berger 2000). Remove from the posterior the information that $T$ itself carries, so that the data are not used twice; the result is close to uniform under the model.
- **Cross-validated checks.** Compare each $x_i$ with its predictive law given the other data, for example by the probability integral transform of $x_i$, which is uniform under a good model. [Pareto smoothed importance sampling](/pareto-smoothed-importance-sampling-loo/) computes all these leave-one-out laws from one posterior sample. See also [cross-validation](/cross-validation/).
- **Hierarchical replication.** In a [hierarchical model](/hierarchical-bayesian-model/), choose which levels to replicate: new data for the same groups, or new groups as well. The choice decides which part of the model the check tests.
- **Likelihood-free models.** The template needs only a simulator, so it also checks models fitted by [approximate Bayesian computation](/approximate-bayesian-computation/).

## Pitfalls

- **Reading $p_B$ as a uniform p-value.** Under a true model, $p_B$ piles up near $1/2$; with $n = 10$ in the normal example, $P(p_B \le 0.05)$ is $2 \times 10^{-14}$, not $0.05$. A check in L4 that gives $p_B = 0.2$ is not reassuring evidence of fit, and $p_B = 0.01$ is strong evidence of misfit.
- **A test quantity the model fits by construction.** Taking `T` in L4 to be a sufficient statistic, such as the sample mean of a Poisson model, gives $p_B \approx 1/2$ for any data; in the count example it was $0.49$ for both data sets. Choose `T` to target a feature the model does not fit directly.
- **Replicating with a different design.** If L3 simulates data of another size, other covariates or another censoring pattern than the observed data, the comparison in L4 is meaningless. Replicate exactly the design of $x$.
- **Different $\theta$ for the two sides of a discrepancy.** When `T` depends on $\theta$, L4 must use the same $\theta_s$ for $T(x^{\mathrm{rep}}, \theta_s)$ and $T(x, \theta_s)$. Using a point estimate for the observed side and draws for the replicated side changes the reference law.
- **Too few draws for a small p-value.** With $S$ draws in L2, the smallest positive value is $1/S$; $p_B = 0$ in the table means fewer than $1$ in $4000$. Report it as $p_B < 1/S$, and increase $S$ if the size matters.
- **Testing many quantities without a plan.** Trying many test quantities and reporting the smallest $p_B$ finds misfit that is not there. Choose quantities that answer questions relevant to the use of the model.

## Exercises

1. In the normal mean example, derive $c = \sqrt{s^2/(2\tau^2 + s^2)}$ and $P(p_B \le \alpha) = \Phi(z_\alpha/c)$. What happens as $\tau \to 0$ and as $\tau \to \infty$?
2. Show that $\mathbb{E}[\Phi(cZ)^2] = \frac14 + \frac{1}{2\pi}\arcsin\frac{c^2}{1 + c^2}$ for standard normal $Z$, by writing $\Phi(cZ)^2$ as the probability that two independent standard normal values lie below $cZ$. Deduce the variance of $p_B$.
3. Show that if the law of $T(X)$ given $\theta$ does not depend on $\theta$, then $p_B$ equals the classical p-value, and it is uniform under the model when $T$ is continuous.
4. Prove that $\mathbb{E}[p_B] = \frac12(1 + P(T(X') = T(X)))$ under the prior predictive law. For Bernoulli data with $T$ = the number of successes and a uniform prior on the success probability, compute $\mathbb{E}[p_B]$ for $n = 1$.
5. For the Poisson-gamma model with prior Gamma($a$, rate $b$) and $T = \sum_i x_i$, show that the posterior predictive mean of $T$ is $n(a + \sum_i x_i)/(b + n)$, which tends to the observed $\sum_i x_i$ as $a, b \to 0$. Explain why this statistic cannot detect overdispersion or outliers.

## References
