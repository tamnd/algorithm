---
tag: 98XJ80
kind: definition
slug: missing-data-mechanism
name: Missing-data mechanism
aliases:
- MCAR
- MAR
- MNAR
- missing at random
- missing completely at random
area: statistics-and-inference/point-estimation
level: core
summary: 'The law of which values are missing given the data: missing completely at random, missing at random, or missing not at random. It decides which analyses of incomplete data stay valid.'
prereqs: [likelihood-function]
see_also: [multiple-imputation, multiple-imputation-by-chained-equations, expectation-maximization, inverse-probability-weighting, ignorability, maximum-likelihood-estimation, estimator-bias]
sources:
  - paper: doi:10.1093/biomet/63.3.581
    title: Donald B. Rubin, Inference and missing data, Biometrika 63(3), 1976
    locator: pages 581 to 592 (missing at random, observed at random, distinct parameters, and when the missingness process can be ignored)
  - book: isbn:9780470526798
    title: Roderick J. A. Little and Donald B. Rubin, Statistical Analysis with Missing Data, third edition, Wiley, 2019
    locator: Chapter 1 (missingness patterns and mechanisms), Chapter 6 (likelihood-based inference and ignorability) and Chapter 15 (missing not at random models)
  - paper: doi:10.1214/13-STS415
    title: Shaun Seaman, John Galati, Dan Jackson and John Carlin, What is meant by "missing at random"?, Statistical Science 28(2), 2013
    locator: pages 257 to 268 (realized and everywhere versions of missing at random and missing completely at random)
---

A missing-data mechanism is the probability law of which values in a data set are missing, given the values themselves. Rubin (1976) put it at the centre of the analysis of incomplete data. The three classes, missing completely at random, missing at random and missing not at random, say how much the pattern of missing values depends on the data. The class decides whether a complete-case analysis is unbiased, whether a [likelihood](/likelihood-function/) analysis of the observed data can ignore the mechanism, and whether [multiple imputation](/multiple-imputation/) is valid without a model for the missingness.

## Definition

Let $Y = (Y_{ij})$ be the complete data, an $n \times p$ array that we would see if nothing were missing. Let $R = (R_{ij})$ be the response indicator: $R_{ij} = 1$ if $Y_{ij}$ is observed and $R_{ij} = 0$ if it is missing. For each $R$, split $Y = (Y_{\mathrm{obs}}, Y_{\mathrm{mis}})$ into the observed and the missing entries. The complete data have a model $f(Y \mid \theta)$.

**Mechanism.** The missing-data mechanism is the conditional law $f(R \mid Y, \phi)$ of the response indicator given the complete data, with a parameter $\phi$.

**Missing completely at random (MCAR).** The mechanism does not depend on the data:

$$f(R \mid Y, \phi) = f(R \mid \phi) \quad \text{for all } Y.$$

Rubin (1976) defined missing at random and "observed at random"; the name missing completely at random for the two together came later and is the one used by Little and Rubin.

**Missing at random (MAR).** The mechanism depends on the data only through the observed values:

$$f(R \mid Y_{\mathrm{obs}}, Y_{\mathrm{mis}}, \phi) = f(R \mid Y_{\mathrm{obs}}, \phi) \quad \text{for all } Y_{\mathrm{mis}}.$$

**Missing not at random (MNAR).** The mechanism is not missing at random: for some observed pattern, the probability of that pattern depends on the values that are missing.

**Distinct parameters.** The parameters $\theta$ and $\phi$ are distinct if their joint parameter space is a product $\Omega_\theta \times \Omega_\phi$; for Bayesian inference, if in addition their prior distributions are independent.

**Ignorable mechanism.** The mechanism is ignorable for likelihood inference about $\theta$ if the data are missing at random and $\theta$ and $\phi$ are distinct.

**Realized and everywhere versions.** The conditions above can be read for the one realized pair $(Y_{\mathrm{obs}}, R)$ that was actually seen, or for every possible pair. Seaman et al. (2013) call these realized and everywhere missing at random. The realized version is enough for direct-likelihood and Bayesian inference; repeated-sampling statements, such as the frequentist distribution of an estimator, need the everywhere version.

### Properties

**Ignorability for likelihood.** If the data are missing at random and $\theta$, $\phi$ are distinct, then the likelihood of $\theta$ based on $(Y_{\mathrm{obs}}, R)$ is proportional to the likelihood based on $Y_{\mathrm{obs}}$ alone.

*Proof.* The joint density of what is observed is

$$f(Y_{\mathrm{obs}}, R \mid \theta, \phi) = \int f(Y_{\mathrm{obs}}, Y_{\mathrm{mis}} \mid \theta)\,f(R \mid Y_{\mathrm{obs}}, Y_{\mathrm{mis}}, \phi)\,dY_{\mathrm{mis}}.$$

Under missing at random the second factor does not depend on $Y_{\mathrm{mis}}$, so it comes out of the integral:

$$f(Y_{\mathrm{obs}}, R \mid \theta, \phi) = f(R \mid Y_{\mathrm{obs}}, \phi)\cdot f(Y_{\mathrm{obs}} \mid \theta).$$

As a function of $(\theta, \phi)$ on the product space $\Omega_\theta \times \Omega_\phi$, this factors into a function of $\phi$ times a function of $\theta$. So the maximizer in $\theta$, and every likelihood ratio in $\theta$, are the same as for $f(Y_{\mathrm{obs}} \mid \theta)$. $\square$

This is why the [EM algorithm](/expectation-maximization/) and direct maximum likelihood on the observed data, and the imputation step of multiple imputation, need no model for $R$ under missing at random.

**Complete-case analysis.** Under missing completely at random, the complete cases are a random subsample of the full sample, so any estimator that is unbiased for complete data is unbiased on the complete cases; only precision is lost. Under missing at random this is false in general (see the example below). Under missing not at random, neither complete-case analysis nor an ignorable likelihood analysis is consistent in general.

**What the data can tell.** Missing completely at random has testable consequences: the observed values of one variable must have the same distribution in every response pattern. Missing at random against missing not at random cannot be tested from $(Y_{\mathrm{obs}}, R)$ alone: for every model that is missing not at random there is one that is missing at random with the same law of the observed data. The choice rests on knowledge of how the data were collected, and analyses under missing not at random are done as sensitivity analyses (Little and Rubin, Chapter 15).

## Examples and non-examples

**Missing completely at random.** A lab drops each blood sample with probability 0.1, independently of everything. The mean of the measured values is unbiased for the population mean.

**Missing at random, with a biased complete-case mean.** Let $X \sim N(0, 1)$ always be observed, and $Y = X + \varepsilon$ with $\varepsilon \sim N(0, 1)$ independent of $X$. The value $Y$ is observed with probability 1 when $X \le 0$ and with probability 0.2 when $X > 0$. The response depends only on the observed $X$, so the data are missing at random. The true mean is $\mathrm E Y = 0$. The mean over complete cases tends to

$$\mathrm E[Y \mid R = 1] = \frac{\mathrm E[X;\ X \le 0] + 0.2\,\mathrm E[X;\ X > 0]}{0.5 + 0.2 \cdot 0.5} = \frac{-0.8\,\varphi(0)}{0.6} = -0.53192,$$

where $\varphi(0) = 1/\sqrt{2\pi}$ and $\mathrm E[X; A]$ means $\mathrm E[X\,\mathbf 1_A]$. The complete-case mean is biased by more than half a standard deviation. The least-squares regression of $Y$ on $X$ over complete cases is still unbiased here, because selection depends only on the regressor. An analysis that uses $X$, such as likelihood, regression imputation or multiple imputation, removes the bias.

**Missing not at random.** People with high incomes are less likely to report their income. The probability that $Y_{ij}$ is missing depends on $Y_{ij}$ itself, even after conditioning on everything observed. An observed-data likelihood that ignores $R$ underestimates the mean income, and no analysis of the observed data alone can detect this.

**Censoring.** A survival time that is right-censored at a known value $c$ is missing not at random in this framework, because it is missing exactly when it exceeds $c$. It is handled by a likelihood that uses the event $\{Y > c\}$, not by ignoring it.

**Dropout in a longitudinal study.** If a patient leaves the study because the last observed measurement was poor, the dropout is missing at random. If the patient leaves because of a poor value at the next, unrecorded visit, it is missing not at random.

**Non-example: missing by design.** In a planned design where a random half of the subjects are not asked a question, the values are missing completely at random by construction; this is a planned mechanism, not a model assumption.

**Non-example: "missing at random" in the everyday sense.** A pattern that looks haphazard is not the same as missing completely at random. The definition concerns the conditional law of $R$ given $Y$, which cannot be seen by looking at the pattern of missing cells.

## Related definitions

- [Multiple imputation](/multiple-imputation/) and [multiple imputation by chained equations](/multiple-imputation-by-chained-equations/): valid under missing at random with a good imputation model.
- [Expectation-maximization](/expectation-maximization/): maximizes the observed-data likelihood, which is the right likelihood under ignorability.
- [Inverse probability weighting](/inverse-probability-weighting/): weights complete cases by the inverse of a response probability modelled under missing at random.
- [Ignorability](/ignorability/): the corresponding assumption in causal inference, where the unobserved potential outcome is the missing value.
- [Estimator bias](/estimator-bias/): the bias of complete-case analysis is a bias in this sense.

## References
