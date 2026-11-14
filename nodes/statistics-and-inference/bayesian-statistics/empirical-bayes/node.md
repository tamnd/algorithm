---
tag: NGX20X
kind: technique
slug: empirical-bayes
name: Empirical Bayes
aliases:
- empirical Bayes method
- type II maximum likelihood
area: statistics-and-inference/bayesian-statistics
level: core
summary: Estimates the prior from many parallel cases, often by maximizing the marginal likelihood, and then applies the Bayes rule with that prior. The James-Stein estimator is one case.
prereqs: [bayes-estimator, bayes-theorem, marginal-likelihood, maximum-likelihood-estimation, poisson-distribution]
see_also: [james-stein-estimator, hierarchical-bayesian-model, local-false-discovery-rate, linear-mixed-model, expectation-maximization, spike-and-slab-prior, horseshoe-prior, credible-interval]
sources:
  - paper: "Herbert Robbins, An empirical Bayes approach to statistics, Proceedings of the Third Berkeley Symposium on Mathematical Statistics and Probability, volume 1, University of California Press, 1956"
    title: Robbins 1956
    locator: the Poisson case and the estimate (x + 1) f(x + 1)/f(x) of the Bayes rule (general locator)
  - book: isbn:9781107149892
    title: "Bradley Efron and Trevor Hastie, Computer Age Statistical Inference, Cambridge University Press, 2016"
    locator: Chapter 6, Section 6.1 (Robbins's formula and Table 6.1, the automobile insurance claims, with the gamma maximum likelihood column)
  - paper: doi:10.1080/01621459.1973.10481350
    title: "Bradley Efron and Carl Morris, Stein's estimation rule and its competitors, an empirical Bayes approach, Journal of the American Statistical Association 68(341), 1973"
    locator: pages 117 to 130 (the normal-normal model, the marginal estimate of the shrinkage factor and the James-Stein rule as empirical Bayes)
  - paper: doi:10.1198/jasa.2011.tm11181
    title: "Bradley Efron, Tweedie's formula and selection bias, Journal of the American Statistical Association 106(496), 2011"
    locator: pages 1602 to 1614 (Tweedie's formula E[mu | z] = z + sigma^2 d/dz log f(z), and its use against selection bias; general locator)
  - paper: doi:10.1080/01621459.1983.10477920
    title: "Carl N. Morris, Parametric empirical Bayes inference: theory and applications, Journal of the American Statistical Association 78(381), 1983"
    locator: pages 47 to 55 (the sections on error estimates and empirical Bayes confidence intervals; general locator)
  - book: isbn:9780521192491
    title: "Bradley Efron, Large-Scale Inference: Empirical Bayes Methods for Estimation, Testing, and Prediction, Cambridge University Press, 2010"
    locator: Chapter 1 (empirical Bayes and the James-Stein estimator) and Chapters 5 and 6 (local false discovery rates)
---

Empirical Bayes is a way to use Bayes's rule when you have many similar cases but no trusted prior. It estimates the prior, or the marginal law of the data that the prior induces, from all the cases together, and then applies the [Bayes estimator](/bayes-estimator/) to each case as if the estimated prior were known. Robbins (1956) introduced it with a formula that needs no model for the prior at all. Efron and Morris (1973) showed that the [James-Stein estimator](/james-stein-estimator/) is the empirical Bayes rule of the normal model, and the same idea is behind [local false discovery rates](/local-false-discovery-rate/) and the shrinkage estimates of mixed models.

## In plain words

Suppose you must estimate the accident rate of each of nine thousand drivers from one year of claims. One driver's record says little. But the whole group tells you how rates are spread among drivers, and that spread is the prior. With it, you can say how much of a good or bad year is luck. A driver with no claims is probably not perfect, and a driver with seven claims is probably not as bad as seven. Empirical Bayes learns the spread from the group and then applies the ordinary Bayes answer to each driver. The price is that the spread is itself estimated, and simple versions forget this uncertainty.

## When it applies

- **Many parallel cases with the same structure.** Observations $x_1, \ldots, x_N$ with $x_i \mid \theta_i \sim f(x \mid \theta_i)$, the $\theta_i$ drawn independently from an unknown prior $g$. The cases share $g$ but not $\theta_i$.
- **The marginal law identifies what you need.** Each $x_i$ has the marginal law $m_g(x) = \int f(x \mid \theta)\, g(\theta)\, d\theta$, and $m_g$ can be estimated from the $x_i$. Either $g$ itself is identified from $m_g$, or, as in Robbins's and Tweedie's formulas, the Bayes rule is a function of $m_g$ alone.
- **$N$ is large enough.** The estimate of $g$ has error of order $1/\sqrt N$ in parametric models and slower in nonparametric ones. With few cases, such as the eight schools below, a full [hierarchical model](/hierarchical-bayesian-model/) that puts a prior on the parameters of $g$ is safer.
- **Not for one case.** With $N = 1$ there is nothing to borrow.

## The template

The holes are the sampling model `f`, the class `G` of priors, the fitting method `FIT` and the decision `RULE`.

```pseudo id=main
EMPIRICAL-BAYES(x₁, ..., x_N, f, G, FIT, RULE)
L1  m_g(x) ← ∫ f(x | θ) g(θ) dθ  for g ∈ G          ▷ the marginal law of one observation
L2  ĝ ← FIT(x₁, ..., x_N; m)                        ▷ type II ML: ĝ = argmax over G of Σᵢ log m_g(xᵢ)
L3  for i ← 1 to N do
L4      δᵢ ← RULE(posterior p(θ | xᵢ) under ĝ)       ▷ posterior mean, interval, or P(null | xᵢ)
L5  return δ₁, ..., δ_N
```

Common choices:

- *`FIT` by type II maximum likelihood* (g-modeling): maximize the [marginal likelihood](/marginal-likelihood/) $\prod_i m_g(x_i)$ over a parametric family, or over all priors (the nonparametric maximum likelihood estimate of Kiefer and Wolfowitz, computed by [EM](/expectation-maximization/) or convex optimization).
- *`FIT` by moments*: match the mean and the variance of $m_g$ to those of the data.
- *f-modeling*: skip $g$ and estimate $m_g$ directly, then plug it into a formula for the Bayes rule in terms of $m_g$.

**Robbins's formula.** Let $x \mid \theta \sim$ Poisson$(\theta)$ and $\theta \sim g$, any prior on $(0, \infty)$. Then

$$\mathbb{E}[\theta \mid x] = (x + 1)\, \frac{m(x + 1)}{m(x)}, \qquad m(x) = \int e^{-\theta} \frac{\theta^x}{x!}\, g(d\theta).$$

*Proof.* By [Bayes's theorem](/bayes-theorem/) the posterior is $g(d\theta \mid x) = e^{-\theta}\theta^x g(d\theta)/(x!\, m(x))$. So

$$\mathbb{E}[\theta \mid x] = \frac{1}{x!\, m(x)} \int \theta\, e^{-\theta}\theta^x\, g(d\theta) = \frac{(x + 1)!\, m(x + 1)}{x!\, m(x)} = (x + 1)\frac{m(x + 1)}{m(x)}. \qquad \blacksquare$$

Robbins's estimate replaces $m(x)$ by the observed frequency of the value $x$: $\hat{\mathbb{E}}[\theta \mid x] = (x + 1) N_{x+1}/N_x$, where $N_x$ is the number of cases with value $x$.

**Tweedie's formula.** Let $z \mid \mu \sim N(\mu, \sigma^2)$ with $\sigma^2$ known, and $\mu \sim g$, any prior. Let $f(z) = \int \varphi_\sigma(z - \mu)\, g(d\mu)$ be the marginal density, with $\varphi_\sigma$ the $N(0, \sigma^2)$ density. Then

$$\mathbb{E}[\mu \mid z] = z + \sigma^2 \frac{d}{dz} \log f(z).$$

*Proof.* Since $\varphi_\sigma'(u) = -(u/\sigma^2)\varphi_\sigma(u)$, the integrand of $f$ has $z$-derivative $\frac{\mu - z}{\sigma^2}\varphi_\sigma(z - \mu)$. Its absolute value is at most $\sup_u \lvert u \rvert \varphi_\sigma(u)/\sigma^2 = 1/(\sigma^2\sqrt{2\pi e})$, a constant, which is integrable against the probability measure $g$. So dominated convergence lets us differentiate under the integral:

$$f'(z) = \frac{1}{\sigma^2}\int (\mu - z)\, \varphi_\sigma(z - \mu)\, g(d\mu) = \frac{f(z)}{\sigma^2}\big(\mathbb{E}[\mu \mid z] - z\big),$$

because $\varphi_\sigma(z - \mu)\, g(d\mu)/f(z)$ is the posterior. Divide by $f(z)/\sigma^2$. $\blacksquare$

Both formulas give the Bayes rule from the marginal density alone, so a good estimate of $m$ or $f$ from many cases gives a good estimate of the rule. Efron (2011) uses Tweedie's formula to correct the selection bias of the largest $z$-values.

## Classic examples

**Insurance claims (Robbins).** Efron and Hastie (2016, Table 6.1) give the number of claims of $9461$ policy holders in one year: $7840, 1317, 239, 42, 14, 4, 4, 1$ holders had $0, 1, \ldots, 7$ claims. Robbins's formula and a gamma prior fitted by maximum marginal likelihood (the marginal is negative binomial; the fit is shape $\hat\nu = 0.7015$ and scale $0.3056$, so the prior mean equals the sample mean $0.2144$) give these estimates of next year's rate:

| claims $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Robbins $(x+1)N_{x+1}/N_x$ | 0.168 | 0.363 | 0.527 | 1.333 | 1.429 | 6.000 | 1.750 |
| gamma prior, $(x + \hat\nu)\hat\sigma/(1 + \hat\sigma)$ | 0.164 | 0.398 | 0.632 | 0.866 | 1.100 | 1.334 | 1.568 |

The two rules agree where the counts are large. For $x \ge 3$ Robbins's estimate rests on a handful of holders and jumps around, and it is not even monotone; the gamma prior gives a smooth line. Table 6.1 of the book prints $1.25$ for Robbins at $x = 6$; the formula gives $7 \cdot 1/4 = 1.75$.

**Normal means and James-Stein.** Let $x_i \sim N(\theta_i, \sigma^2)$ and $\theta_i \sim N(\mu, \tau^2)$. The marginal law is $x_i \sim N(\mu, \sigma^2 + \tau^2)$, so type II maximum likelihood gives $\hat\mu = \bar x$ and $\hat\tau^2 = \max\big(0, \frac1N\sum_i (x_i - \bar x)^2 - \sigma^2\big)$. The rule is $\hat\theta_i = \hat\mu + (1 - \hat B)(x_i - \hat\mu)$ with the shrinkage factor $\hat B = \sigma^2/(\sigma^2 + \hat\tau^2)$. With $\mu = 0$ fixed, replacing the maximum likelihood estimate of $1/(\sigma^2 + \tau^2)$ by the unbiased one gives the [James-Stein estimator](/james-stein-estimator/), and with $\mu$ estimated by $\bar x$ it gives Lindley's variant toward the mean; their risks are on that page. With ten means drawn by `random.Random(2)` ($\theta_i \sim N(0, 1)$, $\sigma = 1$), $x = (1.83, -0.95, -0.51, 0.57, 0.29, -4.6, 0.78, -1.14, -1.82, -0.58)$ gives $\hat\mu = -0.613$, $\hat\tau^2 = 1.788$ and $\hat B = 0.359$. The total squared error falls from $14.07$ for $x$ to $7.40$ for the empirical Bayes rule.

**Large-scale testing.** In the two-groups model each $z$-value is null with prior probability $\pi_0$, and the marginal density is $f = \pi_0 f_0 + (1 - \pi_0) f_1$. The posterior probability of the null is the [local false discovery rate](/local-false-discovery-rate/) $\pi_0 f_0(z)/f(z)$. Efron estimates $f$ from all the $z$-values, which is f-modeling again.

**Mixed models.** In a [linear mixed model](/linear-mixed-model/) the random effects are the $\theta_i$, the variance components are the parameters of $g$, and REML or maximum likelihood fits them from the marginal law. The predicted random effects (BLUPs) are the posterior means under the fitted $g$: empirical Bayes under another name.

## Variations

- **Parametric and nonparametric $g$.** Parametric families (normal, gamma, beta) give stable fits and smooth rules. The nonparametric maximum likelihood estimate of $g$ is discrete and adapts to any shape, at a slower rate.
- **Hierarchical Bayes.** Put a prior on the parameters of $g$ and integrate them out, as on the [hierarchical model](/hierarchical-bayesian-model/) page. The answers agree with empirical Bayes when $N$ is large, and the hierarchical version is better calibrated when $N$ is small.
- **Empirical Bayes intervals.** Morris (1983) widens the plug-in posterior variance to account for the error in $\hat\mu$ and $\hat\tau^2$. Robust versions keep their coverage over a whole class of priors.
- **Empirical Bayes priors in variable selection.** The prior inclusion probability of a [spike-and-slab prior](/spike-and-slab-prior/) or the global scale of a [horseshoe prior](/horseshoe-prior/) can be set by maximizing the marginal likelihood. The estimate of the global scale can collapse to $0$, so a full prior is usually preferred.
- **Type II maximum likelihood in machine learning.** The hyperparameters of a [Gaussian process](/gaussian-process/) are usually fitted by maximizing the marginal likelihood. This is the same template with one case.

## Pitfalls

- **Plug-in intervals are too short.** They treat $\hat g$ as known. The table at the end of this section shows how much coverage they lose.
- **$\hat\tau^2 = 0$ is common.** For the eight schools of Rubin (1981), $y = (28, 8, -3, 7, -1, 1, 18, 12)$ with standard errors $(15, 10, 16, 11, 9, 11, 10, 18)$, the marginal log-likelihood with $\mu$ profiled out is $-29.674, -29.687, -29.725, -29.994, -30.892, -33.318$ at $\tau = 0, 1, 2, 5, 10, 20$. The maximum is at $\tau = 0$, so empirical Bayes pools all eight schools to $7.69$ and claims there is no variation at all. The likelihood is almost flat up to $\tau = 5$, which the plug-in answer hides.
- **Using the data twice.** The prior is fitted to the same data that it is then applied to. This is fine for the averaged risk across cases, which is the point of the method, but statements about one case must account for it.
- **Few or unlike cases.** Borrowing strength across cases that do not share a prior pulls each case toward the wrong center. Group the cases first.
- **Robbins's formula with sparse counts.** The ratio $N_{x+1}/N_x$ is noisy where $N_x$ is small, and the estimate need not be monotone in $x$. Smooth the counts or fit a parametric $g$.
- **Selection.** Reporting only the largest raw estimates overstates them. The empirical Bayes estimates correct this, as Tweedie's formula shows, but only if the rule is applied to all cases, not to the selected ones after a separate fit.

**Coverage of plug-in intervals.** The simulation draws $\theta_i \sim N(0, \tau^2)$ and $x_i \sim N(\theta_i, 1)$, fits $\hat\mu$ and $\hat\tau^2$ by type II maximum likelihood, and forms the 95% plug-in intervals $\hat\theta_i \pm 1.96\sqrt{(1 - \hat B)\sigma^2}$. It uses `random.Random(100 + N)`, with 4000 runs for $N \le 20$ and 1000 runs for $N = 50$. When $\hat\tau^2 = 0$, every interval has length $0$.

| cases $N$ | $\tau^2$ | coverage | share of runs with $\hat\tau^2 = 0$ |
|---|---|---|---|
| 8 | 0.5 | 53.4% | 36.8% |
| 20 | 0.5 | 70.9% | 17.8% |
| 50 | 0.5 | 85.3% | 4.1% |
| 8 | 2 | 80.4% | 7.6% |
| 8 | 10 | 92.9% | 0.3% |

## Exercises

1. Prove Robbins's formula for the geometric model $P(x \mid \theta) = (1 - \theta)\theta^x$, $x = 0, 1, \ldots$: show $\mathbb{E}[\theta \mid x] = m(x + 1)/m(x)$.
2. In the normal-normal model with known $\sigma^2$ and $\mu = 0$, show that $\lVert x \rVert^2/(\sigma^2 + \tau^2) \sim \chi^2_N$ and that $(N - 2)\sigma^2/\lVert x \rVert^2$ is unbiased for $B = \sigma^2/(\sigma^2 + \tau^2)$. Which estimator of $B$ does type II maximum likelihood give?
3. Apply Tweedie's formula to the prior $\mu \sim N(0, A)$ and check that it gives the posterior mean $\frac{A}{A + \sigma^2} z$.
4. Show that for the gamma prior with shape $\nu$ and scale $s$, the marginal of a Poisson count is negative binomial, and that the maximum likelihood estimate of its mean is the sample mean for any fixed $\nu$.
5. Explain why the plug-in posterior variance $(1 - \hat B)\sigma^2$ is $0$ when $\hat\tau^2 = 0$, and propose a correction that adds a term for the uncertainty in $\hat B$.

## References
