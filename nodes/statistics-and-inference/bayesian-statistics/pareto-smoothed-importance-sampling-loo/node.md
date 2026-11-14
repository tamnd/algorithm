---
tag: NR2Y7A
kind: algorithm
slug: pareto-smoothed-importance-sampling-loo
name: Pareto smoothed importance sampling leave-one-out cross-validation
aliases:
- PSIS-LOO
- PSIS leave-one-out
area: statistics-and-inference/bayesian-statistics
level: research
summary: Estimates leave-one-out predictive accuracy from one set of posterior draws, by importance weights whose tail is smoothed with a fitted generalized Pareto law.
model: real-ram
complexity:
  vars: {n: the number of observations, S: the number of posterior draws}
  time: {worst: Θ(n S log S), best: Θ(n S log S)}
  space: {extra: Θ(n + S)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Aki Vehtari, Andrew Gelman, Jonah Gabry, Daniel Simpson, Yuling Yao]
  note: Gelfand, Dey and Chang (1992) estimated leave-one-out predictive densities by importance sampling from the full posterior. Vehtari, Gelman and Gabry (2015 preprint, 2017 journal) stabilized the weights with a fitted Pareto tail and used the fitted shape as a diagnostic.
prereqs: [importance-sampling, cross-validation, posterior-predictive-distribution, bayesian-inference]
see_also: [widely-applicable-information-criterion, akaike-information-criterion, bayesian-information-criterion, effective-sample-size, hamiltonian-monte-carlo, marginal-likelihood, bayes-factor, posterior-predictive-check]
sources:
  - paper: "Aki Vehtari, Daniel Simpson, Andrew Gelman, Yuling Yao and Jonah Gabry, Pareto smoothed importance sampling, Journal of Machine Learning Research 25(72), 2024 (arXiv:1507.02646)"
    title: Vehtari, Simpson, Gelman, Yao and Gabry 2024
    locator: "Section 2.1 and Algorithm 1 (tail length M = floor(min(0.2 S, 3 sqrt(S))), the threshold, the quantiles at (z - 1/2)/M and the cap at the largest raw ratio); Section 3 (k-hat as a diagnostic, Eq. 13 for the threshold min(1 - 1/log10 S, 0.7)); Appendix G (shrinkage of k-hat toward 0.5); Appendix H (MCMC draws)"
  - paper: doi:10.1007/s11222-016-9696-4
    title: "Aki Vehtari, Andrew Gelman and Jonah Gabry, Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC, Statistics and Computing 27(5), 2017"
    locator: pages 1413 to 1432 (PSIS-LOO, its standard error, p_loo, and the comparison with WAIC; general locator)
  - paper: doi:10.1198/tech.2009.08017
    title: "Jin Zhang and Michael A. Stephens, A new and efficient estimation method for the generalized Pareto distribution, Technometrics 51(3), 2009"
    locator: pages 316 to 325 (the profile likelihood in theta = -k/sigma, the grid of theta values and the weighted estimate; general locator)
  - paper: "Alan E. Gelfand, Dipak K. Dey and Hong Chang, Model determination using predictive distributions with implementation via sampling-based methods, Bayesian Statistics 4, Oxford University Press, 1992"
    title: Gelfand, Dey and Chang 1992
    locator: the estimate of the leave-one-out predictive density by importance sampling from the full posterior (general locator)
  - paper: "Ilenia Epifani, Steven N. MacEachern and Mario Peruggia, Case-deletion importance sampling estimators: central limit theorems and related results, Electronic Journal of Statistics 2, 2008"
    title: Epifani, MacEachern and Peruggia 2008
    locator: conditions under which the raw case-deletion importance weights have finite variance (general locator)
  - book: isbn:9781439840955
    title: "Andrew Gelman, John B. Carlin, Hal S. Stern, David B. Dunson, Aki Vehtari and Donald B. Rubin, Bayesian Data Analysis, 3rd edition, CRC Press, 2013"
    locator: Chapter 7, Sections 7.1 and 7.2 (log predictive density, leave-one-out cross-validation and WAIC)
---

PSIS-LOO estimates how well a Bayesian model predicts each data point when that point is left out, without refitting the model $n$ times. It reuses one set of draws from the full posterior $p(\theta \mid y)$ and gives each draw the importance ratio $1/p(y_i \mid \theta)$. Raw ratios can have a very heavy tail, so the method replaces the largest ones by quantiles of a fitted generalized Pareto law, and the fitted shape $\hat k$ tells the user when the estimate cannot be trusted. The cost is one sort per observation, $\Theta(n S \log S)$ for $n$ observations and $S$ draws.

## In plain words

To check a model honestly, you want to predict each data point from a model fitted without it. Refitting for every point is slow. A shortcut is to reweight the draws you already have: draws that explain the left-out point badly get more weight, because the model without that point would favour them. A few draws can get huge weights, and then the answer is noisy. PSIS keeps the small weights as they are and replaces the largest ones by smooth values from a fitted tail curve. The steepness of that curve is a warning light: if it is too heavy, the shortcut is not reliable for that point, and you should refit or use a better model.

## The problem

**Input.** A model with likelihood $p(y \mid \theta) = \prod_{i=1}^n p(y_i \mid \theta)$, so the observations are conditionally independent given $\theta$. Draws $\theta^1, \ldots, \theta^S$ from the posterior $p(\theta \mid y)$, for example from [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/). The matrix $\ell_{is} = \log p(y_i \mid \theta^s)$.

**Output.** An estimate of the expected log pointwise predictive density for new data,

$$\mathrm{elpd}_{\mathrm{loo}} = \sum_{i=1}^n \log p(y_i \mid y_{-i}), \qquad p(y_i \mid y_{-i}) = \int p(y_i \mid \theta)\, p(\theta \mid y_{-i})\, d\theta,$$

where $y_{-i}$ is the data without point $i$. Also its standard error, the effective number of parameters $p_{\mathrm{loo}}$, the shapes $\hat k_1, \ldots, \hat k_n$, and the list of points whose $\hat k_i$ is too large.

**The identity behind it.** If $p(y_i \mid \theta) > 0$ on the support of the posterior, then

$$p(y_i \mid y_{-i}) = \frac{1}{\mathbb{E}\big[\, 1/p(y_i \mid \theta) \mid y \,\big]},$$

so leave-one-out needs only expectations under the full posterior. With the ratios $r_{is} = 1/p(y_i \mid \theta^s)$ this is [importance sampling](/importance-sampling/) with the full posterior as the proposal and $p(\theta \mid y_{-i})$ as the target. The proof is in Correctness.

## The algorithm

The outer routine runs once per observation. GPD-FIT is the shape and scale estimate of Zhang and Stephens (2009), with the shrinkage of Vehtari et al. (2024, Appendix G).

```pseudo id=main
PSIS-LOO(ℓ)                                 ▷ ℓ[i][s] = log p(yᵢ | θˢ), n rows, S draws from p(θ | y)
L1  M ← ⌊min(0.2 S, 3 √S)⌋                  ▷ tail length
L2  for i ← 1 to n do
L3      ρₛ ← -ℓ[i][s] - maxₜ(-ℓ[i][t])  for every s       ▷ log ratios, the largest is 0
L4      sort the draws by ρ; u ← exp(ρ at rank S - M)      ▷ the threshold
L5      (k̂ᵢ, σ̂) ← GPD-FIT(exp(ρ) - u over the M largest draws)
L6      for z ← 1 to M do  the z-th of the M largest draws gets weight min(u + F⁻¹((z - 1/2)/M; k̂ᵢ, σ̂), 1)
L7      the other S - M draws keep the weight exp(ρₛ); call all weights w̃ₛ
L8      eᵢ ← log Σₛ w̃ₛ exp(ℓ[i][s]) - log Σₛ w̃ₛ
L9  flagged ← { i : k̂ᵢ > min(1 - 1/log₁₀ S, 0.7) }
L10 elpd ← Σᵢ eᵢ
L11 se ← √(n · sample variance of e₁, ..., eₙ)
L12 return elpd, se, p_loo = Σᵢ log((1/S) Σₛ exp(ℓ[i][s])) - elpd, (k̂ᵢ), flagged

GPD-FIT(x₁, ..., x_M)                       ▷ exceedances x ≥ 0, sorted, x_M > 0
L13 m ← 30 + ⌊√M⌋
L14 θⱼ ← 1/x_M + (1 - √(m/(j - 1/2)))/(3 x*)  for j = 1, ..., m     ▷ x* is the first quartile
L15 Lⱼ ← M (log(-θⱼ/κ(θⱼ)) - κ(θⱼ) - 1)  with κ(θ) = (1/M) Σ log(1 - θ xₜ)
L16 πⱼ ← exp(Lⱼ) / Σₗ exp(Lₗ)
L17 θ̂ ← Σⱼ πⱼ θⱼ;  k̂ ← κ(θ̂);  σ̂ ← -k̂/θ̂
L18 k̂ ← (M k̂ + 10 · 0.5)/(M + 10);  return (k̂, σ̂)
```

$F^{-1}(p; k, \sigma) = \sigma\big((1 - p)^{-k} - 1\big)/k$ is the quantile function of the generalized Pareto law with location $0$, shape $k$ and scale $\sigma$, and $-\sigma \log(1 - p)$ when $k = 0$. Line L3 shifts the log ratios so that the largest raw ratio is $1$; this changes no estimate, because L8 is a ratio. Line L6 replaces the $M$ largest ratios by the expected order statistics of the fitted tail, in the same order, and caps them at the largest raw ratio. Line L8 is self-normalized importance sampling. Line L15 is the profile log-likelihood of the generalized Pareto law in $\theta = -k/\sigma$; L16 and L17 average it over a grid, which is more stable than its maximum. Line L18 pulls $\hat k$ toward $0.5$ with the weight of 10 observations, which helps when $M$ is small. Sums of exponentials use the log-sum-exp trick: subtract the largest term before exponentiating, and add it back after the logarithm.

If $M < 5$ or all exceedances are $0$, the implementation skips the smoothing and reports $\hat k_i = \infty$, as the reference implementations do.

## Example

**Five points.** The model is $y_i \sim N(\theta, 1)$ with prior $\theta \sim N(0, 100)$, and the data are $y = (0.5, 1, 2, 2.5, 4)$. The posterior is $N(1.996, 0.1996)$. Leave-one-out has a closed form here: $p(y_i \mid y_{-i})$ is the normal density at $y_i$ with the mean and variance of the posterior from the other four points, plus $1$ for the noise. We take $S = 4000$ draws with `random.Random(1)`, so L1 gives $M = \lfloor \min(800, 189.7) \rfloor = 189$.

Trace for the last point, $y_5 = 4$:

1. L3 and L4: the threshold is $u = 0.1324$ times the largest ratio.
2. L5: GPD-FIT on the $189$ exceedances gives $\hat k_5 = 0.421$ and $\hat\sigma = 0.0723$.
3. L6: the three largest ratios were $0.926$, $0.985$ and $1$; after smoothing all three are at the cap $1$. Kong's [effective sample size](/effective-sample-size/) of the weights goes from $1127$ to $1148$.
4. L8: $e_5 = -3.5044$. Raw importance sampling gives $-3.5076$, and the exact value is $-3.5390$.

| $i$ | $y_i$ | $\hat k_i$ | PSIS $e_i$ | exact $\log p(y_i \mid y_{-i})$ |
|---|---|---|---|---|
| 1 | 0.5 | 0.352 | $-2.4210$ | $-2.4283$ |
| 2 | 1.0 | 0.292 | $-1.6476$ | $-1.6500$ |
| 3 | 2.0 | 0.165 | $-1.0279$ | $-1.0303$ |
| 4 | 2.5 | 0.235 | $-1.1831$ | $-1.1889$ |
| 5 | 4.0 | 0.421 | $-3.5044$ | $-3.5390$ |
| sum | | | $-9.784$ | $-9.8365$ |

L12 gives $p_{\mathrm{loo}} = 1.607$. No point is flagged. All five errors have the same sign, because they use the same draws. [WAIC](/widely-applicable-information-criterion/) from the same draws gives $\mathrm{elpd}_{\mathrm{waic}} = -9.746$.

**One outlier.** Take 19 points from `random.Random(7)` (standard normal, rounded to 2 decimals) and add a last point $y_{20}$. The draws use `random.Random(11)`, $S = 4000$.

| $y_{20}$ | $\hat k_{20}$ | flagged | PSIS $e_{20}$ | exact $e_{20}$ | PSIS elpd | exact elpd |
|---|---|---|---|---|---|---|
| a 20th normal point | 0.077 | none | | | $-26.649$ | $-26.640$ |
| 4 | 0.394 | none | | | $-35.048$ | $-35.037$ |
| 6 | 0.564 | none | | | $-45.276$ | $-45.264$ |
| 9 | 0.827 | point 20 | $-40.367$ | $-40.398$ | $-68.104$ | $-68.105$ |
| 15 | 1.358 | point 20 | $-109.110$ | $-109.448$ | $-140.493$ | $-140.785$ |

At $y_{20} = 15$ the error is $0.34$ nats, and raw importance sampling ($-109.117$) is no better. Exact refitting is the fix. In this model the true tail of the ratios is light: $r \propto \exp((y_i - \theta)^2/2)$ with $\theta \sim N(m, v)$ has finite moments of every order below $1/v \approx 20$. The large $\hat k$ is a finite-sample effect: in the range of ratios that 4000 draws can reach, the tail behaves like a Pareto tail with shape near $0.8$ or $1.4$. This is what the diagnostic is meant to report.

## Correctness

Four facts, proved in proofs/correctness.md:

1. **The identity.** $p(y_i \mid y_{-i}) = 1/\mathbb{E}[1/p(y_i \mid \theta) \mid y]$ when the observations are conditionally independent given $\theta$ and $p(y_i \mid \theta) > 0$ on the support of the posterior. In particular $\mathbb{E}[1/p(y_i \mid \theta) \mid y]$ is always finite, so raw importance sampling is consistent by the [law of large numbers](/law-of-large-numbers/) for independent draws (or the ergodic theorem for a Markov chain). The variance of the raw ratios can still be infinite.
2. **The code is Algorithm 1.** Lines L1 to L12 compute the tail length, threshold, quantiles and cap of Algorithm 1 of Vehtari et al. (2024).
3. **Smoothing keeps the order and the cap.** Only the $M$ largest ratios change; they stay in the same order, at least $u$ and at most the largest raw ratio.
4. **L15 is the profile likelihood.** For a fixed $\theta = -k/\sigma$ the generalized Pareto log-likelihood is maximized at $k = \kappa(\theta)$, and its value there is $L(\theta)$ of line L15.

What is proved: the four facts above, and the tests check them on exact cases. What is only cited: that the smoothed estimate has finite variance and is consistent as $S$ grows, and that it is reliable when $\hat k < \min(1 - 1/\log_{10} S, 0.7)$ (Vehtari et al. 2024, Section 3). These come from the theory of the generalized Pareto tail and from experiments. On this page they are only measured, in the tables above.

## Complexity

For each of the $n$ rows: L3 is $\Theta(S)$, the sort in L4 is $\Theta(S \log S)$, GPD-FIT costs $\Theta(M (30 + \sqrt M)) = O(S)$ because $M \le 3\sqrt S$, and L6 to L8 are $\Theta(S)$. The total is $\Theta(n S \log S)$ in the best and the worst case. A selection of the $M$ largest ratios instead of a full sort lowers this to $\Theta(n S)$ expected time. Extra space is $\Theta(S)$ for one row of weights plus $\Theta(n)$ for the outputs. The input matrix itself has $nS$ entries, and computing it costs $nS$ likelihood evaluations, which usually dominates. Exact leave-one-out would cost $n$ extra posterior fits.

## Properties

- **Deterministic given the draws.** All randomness is in the posterior draws.
- **Not exact.** It is a Monte Carlo estimate of $\mathrm{elpd}_{\mathrm{loo}}$. Each $e_i$ is biased upward for finite $S$, because $\log$ is concave ([Jensen's inequality](/jensens-inequality/)); the bias falls like $1/S$ when the ratios have finite variance.
- **Pointwise.** It needs a likelihood that factorizes over the units that you want to leave out. For time series or spatial data, leaving out one point is often the wrong question.
- **Diagnostic included.** $\hat k_i$ is computed for every point at no extra cost. A large $\hat k_i$ marks a point that is very influential for the posterior, often an outlier or a sign of a misspecified model.
- **Same target as WAIC.** Both estimate $\mathrm{elpd}$ for new data from the same process. They agree to first order in regular models (Watanabe 2010), but PSIS-LOO has a diagnostic and is more robust when the posterior is far from normal (Vehtari, Gelman and Gabry 2017).
- **Not the marginal likelihood.** PSIS-LOO measures prediction of each point from the others. The [marginal likelihood](/marginal-likelihood/) and the [Bayes factor](/bayes-factor/) measure prediction of all data from the prior. The two can rank models differently.

## Variants and improvements

- **MCMC draws.** With correlated draws, Appendix H of Vehtari et al. (2024) uses $3\sqrt{S/R_{\mathrm{eff}}}$ in the tail length, where $R_{\mathrm{eff}}$ is the relative effective sample size of the ratios.
- **Rounding.** The paper takes the floor in L1. The reference implementations take the ceiling. The difference is one draw in the tail.
- **Moment matching.** For flagged points, transform the existing draws so that their moments match the leave-one-out posterior, then recompute the weights (Paananen and coauthors, 2021).
- **Exact refits for flagged points.** Refit the model without each flagged point and use the exact value for those points only. This is cheap when few points are flagged.
- **K-fold.** If many points are flagged, use [K-fold cross-validation](/cross-validation/) with refits.
- **Truncated importance sampling.** Ionides (2008) truncates the ratios at $\sqrt S$ times their mean. It also bounds the variance, but has more bias than PSIS when the tail is light.
- **PSIS outside LOO.** The same smoothing stabilizes importance sampling in general, and $\hat k$ checks variational approximations (Yao and coauthors, 2018).

## When to use it

Use it to compare Bayesian models by their predictive accuracy when you already have posterior draws and a pointwise log-likelihood. Report $\mathrm{elpd}_{\mathrm{loo}}$ with its standard error, and for a comparison of two models use the standard error of the pointwise differences, not the difference of the two standard errors. Check $\hat k$ for every point. Prefer it to [WAIC](/widely-applicable-information-criterion/), which has no diagnostic. Do not use it to test a hypothesis; for that question, see the [Bayes factor](/bayes-factor/) page, which has a different target.

## Pitfalls

- **Ignoring $\hat k$.** A large $\hat k$ means that the estimate for that point can be far off, as in the outlier table. Raw importance sampling does not fix it.
- **Thinning and too few draws.** With small $S$ the tail has few draws, the threshold falls (it is $0.5$ at $S = 100$), and the estimate is noisy.
- **The wrong unit.** Hierarchical models with one observation per group can have large $\hat k$ for most points, because removing one point changes its group parameter a lot. Leave out whole groups, or integrate the group parameter out.
- **Dependent data.** Leave-one-out for a time series uses the future to predict the past. Use leave-future-out or block designs.
- **Overflow.** Use logarithms. Ratios like $\exp(100)$ are common.
- **Small differences.** A difference of $\mathrm{elpd}$ smaller than a few standard errors of the difference does not show that one model is better.

## Implementations

## History

Geisser and Eddy (1979) and Gelfand, Dey and Chang (1992) introduced predictive model checks from leave-one-out densities, and Gelfand and coauthors estimated them by importance sampling from the full posterior, which gives the harmonic mean formula of the identity. Epifani, MacEachern and Peruggia (2008) showed when the raw case-deletion weights have finite variance. Ionides (2008) proposed truncated importance sampling. Vehtari and Gelman posted Pareto smoothed importance sampling in 2015, Vehtari, Gelman and Gabry (2017) applied it to leave-one-out cross-validation and compared it with WAIC, and the full treatment with the threshold $\min(1 - 1/\log_{10} S, 0.7)$ appeared in the Journal of Machine Learning Research in 2024. The R package loo and the Python package ArviZ implement it.

## References
