---
tag: 5HMWEW
kind: technique
slug: approximate-bayesian-computation
name: Approximate Bayesian computation
aliases:
- likelihood-free inference
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: 'Bayesian inference without a likelihood: simulate data from parameters drawn from the prior and keep those whose summary statistics are close to the observed ones.'
history:
  year: 2002
  people: [Donald B. Rubin, Simon Tavaré, Jonathan K. Pritchard, Mark A. Beaumont, David J. Balding]
  note: Rubin (1984) described the idea as a thought experiment. Tavaré and coauthors (1997) and Pritchard and coauthors (1999) used it for population genetics, and Beaumont, Zhang and Balding (2002) named it and added regression adjustment. Markov chain and sequential versions followed in 2003 and 2007 to 2009.
prereqs: [bayesian-inference, rejection-sampling, sufficient-statistic, bayes-theorem]
see_also: [abc-rejection-sampling, abc-sequential-monte-carlo, bayes-factor, simulation-based-calibration, metropolis-hastings, linear-regression, posterior-predictive-check, sequential-monte-carlo]
sources:
  - paper: doi:10.1214/aos/1176346785
    title: "Donald B. Rubin, Bayesianly justifiable and relevant frequency calculations for the applied statistician, Annals of Statistics 12(4), 1984"
    locator: "pages 1151 to 1172: drawing from the prior, simulating, and keeping matches as a description of Bayes' rule (general locator)"
  - paper: "Mark A. Beaumont, Wenyang Zhang and David J. Balding, Approximate Bayesian computation in population genetics, Genetics 162(4), 2002"
    title: Beaumont, Zhang and Balding 2002
    locator: "pages 2025 to 2035: the name, the tolerance, and local linear regression adjustment with Epanechnikov weights (general locator)"
  - paper: doi:10.1073/pnas.1102900108
    title: "Christian P. Robert, Jean-Marie Cornuet, Jean-Michel Marin and Natesh S. Pillai, Lack of confidence in approximate Bayesian computation model choice, Proceedings of the National Academy of Sciences 108(37), 2011"
    locator: "pages 15112 to 15117: summaries sufficient within each model need not be sufficient for model choice; the Poisson against geometric example (general locator)"
  - paper: "Jean-Michel Marin, Natesh S. Pillai, Christian P. Robert and Judith Rousseau, Relevant statistics for Bayesian model choice, Journal of the Royal Statistical Society Series B 76(5), 2014"
    title: Marin, Pillai, Robert and Rousseau 2014
    locator: "pages 833 to 859: conditions on the summaries under which ABC model choice is consistent (general locator)"
  - paper: doi:10.1093/genetics/145.2.505
    title: "Simon Tavaré, David J. Balding, Robert C. Griffiths and Peter Donnelly, Inferring coalescence times from DNA sequence data, Genetics 145(2), 1997"
    locator: "pages 505 to 518 (general locator)"
---

Approximate Bayesian computation (ABC) is a family of methods for [Bayesian inference](/bayesian-inference/) when the likelihood $f(x \mid \theta)$ cannot be computed but data can be simulated from the model. It replaces the condition "the simulated data equal the observed data" by "the summaries of the simulated data are within $\varepsilon$ of the observed summaries". Every ABC method targets the $\varepsilon$-posterior

$$\pi_\varepsilon(\theta) \propto \pi(\theta)\, P_\theta\big(\rho(S(Y), S(x)) \le \varepsilon\big),$$

where $S$ is a summary map and $\rho$ a distance. Two approximations separate $\pi_\varepsilon$ from the true posterior: the summaries, which lose information unless they are [sufficient](/sufficient-statistic/), and the tolerance $\varepsilon$. The methods differ in how they sample $\pi_\varepsilon$ (rejection, Markov chains, sequential Monte Carlo) and in how they correct for $\varepsilon$ afterwards.

## In plain words

Some models are easy to run forward but hard to write down as a formula. A model of how genes spread through a population, or how a disease spreads through a city, can produce fake data for any setting, but no one can compute how likely the real data are. ABC learns the settings anyway. Pick a setting from what you believed beforehand, run the model, and compare a few key numbers of the fake data with those of the real data. Keep the setting when they are close. The kept settings form an approximate answer. The answer depends on which numbers you compare and on how close counts as close. Choosing those two things well is most of the work.

## When it applies

- **The model can be simulated, but the likelihood cannot be evaluated.** Typical cases are coalescent models in population genetics, stochastic epidemic and ecological models, and agent-based models. If the likelihood can be evaluated, even slowly, likelihood-based methods are more accurate.
- **A proper prior that can be sampled.** All ABC samplers start from prior draws.
- **A small set of informative summaries.** The cost grows like $\varepsilon^{-q}$ for $q$ summaries, so $q$ must be small; and the answer is only as good as the information in $S$.
- **Simulations are affordable.** Even good ABC samplers need thousands to millions of simulations.

## The template

The holes are the summaries `S`, the distance `ρ`, the tolerance `ε`, the sampler `SAMPLER` and the correction `ADJUST`.

```pseudo id=main
ABC(x, π, SIMULATE, S, ρ, ε, SAMPLER, ADJUST)
L1  s_obs ← S(x)                                     ▷ hole S: the summaries
L2  accept(θ, Y) ← [ρ(S(Y), s_obs) ≤ ε]               ▷ holes ρ and ε
L3  (θᵢ, sᵢ), i = 1..N ← SAMPLER(π, SIMULATE, accept) ▷ rejection, MCMC or SMC
L4  θᵢ ← ADJUST(θᵢ, sᵢ, s_obs)                        ▷ e.g. regression; the identity if none
L5  return θ₁..θ_N                                    ▷ they target π_ε, or an adjusted version
```

Common choices:

- *`SAMPLER` = rejection*: draw $\theta$ from the prior and keep it when it passes L2; the [ABC rejection algorithm](/abc-rejection-sampling/) proves that the kept values are exact draws from $\pi_\varepsilon$.
- *`SAMPLER` = Markov chain*: a [Metropolis-Hastings](/metropolis-hastings/) chain on $\theta$ whose proposal is accepted only if a fresh simulation passes L2 and the usual prior and proposal ratio test passes. It leaves $\pi_\varepsilon$ invariant.
- *`SAMPLER` = sequential Monte Carlo*: [ABC-SMC](/abc-sequential-monte-carlo/) moves a weighted population through falling tolerances.
- *`ε` as a quantile*: simulate a fixed number of pairs and keep the closest fraction, for example $1$ percent.
- *`ρ` scaled*: divide each summary by its spread across prior simulations before taking the Euclidean distance.

**Why the template targets $\pi_\varepsilon$.** The pair $(\theta, Y)$ drawn from $\pi(\theta)f(y \mid \theta)$ and kept when $Y$ lies in the set $\{\rho(S(Y), s_{\mathrm{obs}}) \le \varepsilon\}$ has $\theta$-marginal $\pi(\theta)P_\theta(\rho \le \varepsilon)$, up to a constant. With $\varepsilon = 0$, discrete data and a sufficient $S$, this is the exact posterior, by the [Fisher-Neyman factorization theorem](/fisher-neyman-factorization-theorem/). Both proofs are on the [ABC rejection](/abc-rejection-sampling/) page.

**Regression adjustment (Beaumont, Zhang and Balding 2002).** Among the kept pairs, fit $\theta_i \approx \alpha + \beta(s_i - s_{\mathrm{obs}})$ by weighted [linear regression](/linear-regression/), with Epanechnikov weights $1 - (\rho_i/\varepsilon)^2$, and replace $\theta_i$ by $\theta_i - \hat\beta(s_i - s_{\mathrm{obs}})$.

*Why it works.* Suppose that, under the joint law of $(\theta, S(Y))$, $\theta = \alpha + \beta(S - s_{\mathrm{obs}}) + e$ with $e$ independent of $S$. Then $\theta \mid S = s_{\mathrm{obs}}$ has the law of $\alpha + e$, and every adjusted value $\theta_i - \beta(s_i - s_{\mathrm{obs}}) = \alpha + e_i$ has that law, whatever $s_i$ is. So the tolerance no longer widens the answer. $\blacksquare$ When the relation is not linear or the spread of $e$ depends on $S$, the adjustment is only approximately right, which is why it is applied locally, within a moderate $\varepsilon$.

## Classic examples

**Binomial data with rejection.** For $3$ successes in $10$ trials, a uniform prior and $S$ = the number of successes, [ABC rejection](/abc-rejection-sampling/) with $\varepsilon = 0$ keeps one proposal in $11$ and gives the exact posterior Beta(4, 8). With $\varepsilon = 1$ the variance of the kept values grows from $0.0171$ to $0.0214$. That page has the full tables.

**Sequential ABC on the same model.** With $6$ successes in $20$ trials, [ABC-SMC](/abc-sequential-monte-carlo/) with tolerances $(6, 3, 1, 0)$ and $500$ particles reaches Beta(7, 15) with $9238$ simulations, against about $10500$ for rejection. With $30$ successes in $100$ trials the saving is a factor of two.

**Population genetics.** Tavaré, Balding, Griffiths and Donnelly (1997) inferred the age of the most recent common ancestor of a sample of DNA sequences under the coalescent by keeping the simulated genealogies whose number of segregating sites matched the data. The summary is discrete, so the match was exact. Pritchard and coauthors (1999) used several summaries of Y chromosome data with a tolerance.

**Regression adjustment for a normal mean.** $x_1, \ldots, x_5 \sim N(\theta, 1)$ with prior $\theta \sim N(0, 3^2)$ and $S = \bar x$; the exact posterior has mean $0.6476$ and standard deviation $0.4423$. With $20000$ simulations from `random.Random(30)`:

| $\varepsilon$ | kept | plain mean | plain sd | adjusted mean | adjusted sd |
|---|---|---|---|---|---|
| 0.1 | 501 | 0.6643 | 0.4691 | 0.6574 | 0.4687 |
| 0.5 | 2545 | 0.6256 | 0.5333 | 0.6449 | 0.4508 |
| 1.0 | 5033 | 0.6084 | 0.7190 | 0.6436 | 0.4494 |
| 2.0 | 9626 | 0.5402 | 1.1763 | 0.6468 | 0.4472 |

Without adjustment, the standard deviation grows with $\varepsilon$; with it, $\varepsilon = 2$ keeps half of all simulations and is still within $1.1$ percent of the exact value. Here the relation of $\theta$ to $\bar x$ is exactly linear with normal noise, the case in which the adjustment is exact.

**Model choice needs more than sufficiency within each model.** Robert, Cornuet, Marin and Pillai (2011) give this example. Model P: $x_1, \ldots, x_n$ are Poisson($\lambda$) with $\lambda \sim$ Exp(1). Model G: they are geometric, $P(x \mid p) = p(1-p)^x$, with $p \sim$ Uniform(0, 1). The sum $S = \sum_i x_i$ is sufficient within each model. The exact evidences are

$$m_P(x) = \frac{S!}{(n+1)^{S+1}\prod_i x_i!}, \qquad m_G(x) = \frac{n!\, S!}{(n+S+1)!}.$$

Within model $k$, the law of $x$ given $S = s$ does not depend on the parameter: it is multinomial, $h_P(x) = s!/(n^s\prod_i x_i!)$, under P, and uniform over the $\binom{n+s-1}{s}$ compositions, $h_G(x) = 1/\binom{n+s-1}{s}$, under G. So $m_k(x) = m_k^S(s)\, h_k(x)$, and the Bayes factors satisfy

$$B_{PG}(x) = B_{PG}^S(s)\cdot\frac{h_P(x)}{h_G(x)}.$$

ABC with $S$ and $\varepsilon = 0$ estimates $B^S$, not $B$. For $n = 3$ and $S = 3$, $B^S = 189/128 = 1.477$ for every data set, while $x = (0, 0, 3)$ has $B = 35/64 = 0.547$ and $x = (1, 1, 1)$ has $B = 105/32 = 3.281$; the factors $h_P/h_G$ are $10/27$ and $20/9$. With equal prior model probabilities and $200000$ simulations per run from one `random.Random(4)` stream, ABC with $S$ gives $P(\text{P} \mid x) \approx 0.597$ for $(0, 0, 3)$ and $0.598$ for $(1, 1, 1)$ (exact for $S$: $0.596$). ABC on the sorted data, which are sufficient for both the parameter and the model index, gives $0.348$ for $(0, 0, 3)$ (exact: $0.354$) and $0.771$ for $(1, 1, 1)$ (exact: $0.766$). The [Bayes factor](/bayes-factor/) from an insufficient summary can point to the wrong model.

## Variations

- **Choice of summaries.** Semi-automatic ABC fits a regression of $\theta$ on many candidate statistics from pilot simulations and uses the fitted values as $S$; other methods select summaries by information criteria or learn them with neural networks.
- **Kernel ABC.** Replace the indicator of L2 by a smooth kernel weight $K_\varepsilon(\rho)$, giving weighted samples.
- **Non-linear adjustment.** Replace the linear regression of L4 by a heteroscedastic non-linear regression, such as a neural network.
- **Synthetic likelihood.** Assume that $S(Y)$ is normal given $\theta$, estimate its mean and covariance from simulations at each $\theta$, and use the normal density as an approximate likelihood inside MCMC.
- **Neural posterior estimation.** Train a conditional density estimator on simulated pairs $(\theta, Y)$ to approximate $p(\theta \mid y)$ directly; this is the modern form of likelihood-free inference, and it is checked with [simulation-based calibration](/simulation-based-calibration/).
- **Model checking.** The same simulations give a [posterior predictive check](/posterior-predictive-check/) of the summaries, which shows whether the model can reproduce the data at all.

## Pitfalls

- **Treating $\pi_\varepsilon$ as the posterior.** L2 with $\varepsilon > 0$ widens the answer: in the table, the standard deviation is $1.18$ instead of $0.44$ at $\varepsilon = 2$. Report $\varepsilon$, check stability as it falls, or adjust in L4.
- **Insufficient summaries in model choice.** Using L1 with summaries sufficient within each model gives the Bayes factor of the summaries, which in the example is $1.48$ where the truth is $0.55$. Use summaries whose means differ between the models (Marin, Pillai, Robert and Rousseau 2014), or avoid ABC model choice.
- **Too many summaries.** L2 with $q$ summaries keeps a fraction of order $\varepsilon^q$; with the whole data vector of five normal values, $2 \times 10^6$ simulations kept a single value at $\varepsilon = 0.25$. Reduce the summaries to a few informative ones, one per parameter if possible.
- **Unscaled distance.** In L2, a summary measured in thousands drowns a summary measured in fractions. Scale each summary first.
- **Extrapolating the adjustment.** L4 with a global linear fit over a huge tolerance relies on linearity far from $s_{\mathrm{obs}}$. Keep the Epanechnikov weights and a moderate $\varepsilon$, and compare the adjusted answer for two tolerances.
- **No check of calibration.** ABC answers can be overconfident without any warning. Run the whole pipeline on simulated data sets with known parameters and test the coverage, as in [simulation-based calibration](/simulation-based-calibration/).

## Exercises

1. Show that for $n$ Bernoulli trials with a uniform prior and $S$ = the number of successes, ABC rejection with $\varepsilon = 0$ keeps a proposal with probability $1/(n+1)$, whatever the observed count is. What is the probability for the window $|S(Y) - s| \le k$ when it stays inside $\{0, \ldots, n\}$?
2. Let $x_1, \ldots, x_n \sim N(\theta, \sigma^2)$ with $\sigma$ known, a flat prior on $\theta$, $S = \bar x$ and $\rho(u, v) = |u - v|$. Show that $\pi_\varepsilon$ is the law of $\bar x + Z + U$ with $Z \sim N(0, \sigma^2/n)$ and $U \sim$ Uniform$(-\varepsilon, \varepsilon)$ independent, so its variance is $\sigma^2/n + \varepsilon^2/3$.
3. In the Poisson against geometric example, derive $m_P(x)$, $m_G(x)$ and the factors $h_P$ and $h_G$. Find a data set with $n = 3$ and $S = 3$ for which the true Bayes factor is largest.
4. Show that for independent and identically distributed data, the sorted data set is sufficient for the model index of any two models, so ABC with $\varepsilon = 0$ on sorted discrete data gives the true posterior model probabilities.
5. Show that the ABC Metropolis-Hastings chain, which accepts a move $\theta \to \theta'$ only if a fresh simulation at $\theta'$ passes L2 and a uniform draw is below $\pi(\theta')q(\theta \mid \theta')/(\pi(\theta)q(\theta' \mid \theta))$, satisfies detailed balance with respect to the joint law $\pi_\varepsilon(\theta, y) \propto \pi(\theta)f(y \mid \theta)\mathbf{1}\{\rho(S(y), s_{\mathrm{obs}}) \le \varepsilon\}$.

## References
