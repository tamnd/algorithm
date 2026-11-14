---
tag: 1PE36P
kind: algorithm
slug: abc-rejection-sampling
name: ABC rejection algorithm
aliases:
- rejection ABC
area: statistics-and-inference/bayesian-statistics
level: advanced
summary: Draw a parameter from the prior, simulate a data set, and accept the parameter when its summaries lie within epsilon of the observed ones. The accepted draws approximate the posterior.
model: real-ram
complexity:
  vars: {N: the number of accepted values, C: the cost of one simulation, A: "the acceptance probability, P(rho(S(Y), s_obs) <= eps) under the prior predictive"}
  time: {expected: Θ(N C / A)}
  space: {extra: Θ(N)}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 1997
  people: [Simon Tavaré, David J. Balding, Robert C. Griffiths, Peter Donnelly, Jonathan K. Pritchard, Mark A. Beaumont]
  note: Rubin (1984) described the procedure as a way to understand Bayes' rule. Tavaré and coauthors (1997) used it with an exact match on a discrete summary for coalescent models in population genetics. Pritchard and coauthors (1999) added the tolerance. Beaumont, Zhang and Balding (2002) named the field approximate Bayesian computation.
prereqs: [rejection-sampling, bayes-theorem, sufficient-statistic, bayesian-inference]
see_also: [approximate-bayesian-computation, abc-sequential-monte-carlo, fisher-neyman-factorization-theorem, kolmogorov-smirnov-test, posterior-predictive-distribution, importance-sampling, binomial-distribution, simulation-based-calibration]
sources:
  - paper: doi:10.1214/aos/1176346785
    title: "Donald B. Rubin, Bayesianly justifiable and relevant frequency calculations for the applied statistician, Annals of Statistics 12(4), 1984"
    locator: "pages 1151 to 1172: the description of Bayes' rule as drawing a parameter from the prior, simulating data, and keeping the parameter when the simulated data match the observed data (general locator)"
  - paper: doi:10.1093/genetics/145.2.505
    title: "Simon Tavaré, David J. Balding, Robert C. Griffiths and Peter Donnelly, Inferring coalescence times from DNA sequence data, Genetics 145(2), 1997"
    locator: "pages 505 to 518: rejection sampling of the coalescent with an exact match on the number of segregating sites (general locator)"
  - paper: doi:10.1093/oxfordjournals.molbev.a026091
    title: "Jonathan K. Pritchard, Mark T. Seielstad, Anna Perez-Lezaun and Marcus W. Feldman, Population growth of human Y chromosomes: a study of Y chromosome microsatellites, Molecular Biology and Evolution 16(12), 1999"
    locator: "pages 1791 to 1798: the rejection algorithm with summary statistics and a tolerance (general locator)"
  - paper: "Mark A. Beaumont, Wenyang Zhang and David J. Balding, Approximate Bayesian computation in population genetics, Genetics 162(4), 2002"
    title: Beaumont, Zhang and Balding 2002
    locator: "pages 2025 to 2035: the name approximate Bayesian computation, the analysis of the tolerance, and local linear regression adjustment (general locator)"
---

The ABC rejection algorithm samples from an approximate posterior when the likelihood $f(x \mid \theta)$ cannot be evaluated but data can be simulated from the model. It draws $\theta$ from the prior $\pi$, simulates a data set $Y$ at $\theta$, and keeps $\theta$ when the summaries $S(Y)$ lie within a tolerance $\varepsilon$ of the observed summaries $s_{\mathrm{obs}} = S(x)$. The kept values are an exact, independent sample from the $\varepsilon$-posterior $\pi_\varepsilon(\theta) \propto \pi(\theta)\,P_\theta(\rho(S(Y), s_{\mathrm{obs}}) \le \varepsilon)$. With discrete data, a [sufficient statistic](/sufficient-statistic/) and $\varepsilon = 0$, that is the exact posterior. It is the simplest member of [approximate Bayesian computation](/approximate-bayesian-computation/).

## In plain words

Suppose you have a machine that can produce fake data for any setting of its knobs, but no formula for how likely real data are. To learn which settings explain the real data, pick a setting at random from what you believed beforehand, run the machine, and look at the fake data. If it looks like the real data, keep the setting; if not, throw it away. Repeat many times. The settings you keep are the ones that often produce data like yours, and in the right proportions. Comparing whole data sets is too strict, so you compare a few numbers that describe them, and you allow a small gap. A smaller gap gives a better answer, but you throw away more runs.

## The problem

**Input.** A proper prior $\pi$ that can be sampled; a simulator that draws a data set $Y \sim f(\cdot \mid \theta)$ for any $\theta$; observed data $x$; a summary map $S$, a distance $\rho$ and a tolerance $\varepsilon \ge 0$; the number $N$ of values to keep.

**Output.** $N$ independent draws from $\pi_\varepsilon(\theta) \propto \pi(\theta)\, a_\varepsilon(\theta)$, where $a_\varepsilon(\theta) = P_\theta(\rho(S(Y), s_{\mathrm{obs}}) \le \varepsilon)$ is the probability that a simulation at $\theta$ is close enough.

## The algorithm

```pseudo id=main
ABC-REJECTION(π, simulator, S, s_obs, ρ, ε, N)
L1  K ← empty list
L2  while |K| < N
L3      θ ← a draw from π
L4      Y ← a data set simulated from f(· | θ)
L5      if ρ(S(Y), s_obs) ≤ ε then
L6          append θ to K
L7  return K
```

L3 and L4 draw a pair $(\theta, Y)$ from the joint law $\pi(\theta) f(y \mid \theta)$. L5 keeps the pair when the simulated summaries fall in a ball of radius $\varepsilon$ around the observed ones; this is [rejection sampling](/rejection-sampling/) from the joint law conditioned on that ball, and L6 keeps only the $\theta$ part. The algorithm never evaluates $f(x \mid \theta)$. Each pass of the loop is independent, so the passes can run in parallel, and the implementation also stops after a given number of simulations.

## Example

**Trace.** $3$ successes in $10$ Bernoulli trials, uniform prior on $p$, $S$ = the number of successes, $\rho(u, v) = |u - v|$, $\varepsilon = 0$. With `random.Random(3)`:

| proposal | $p$ (L3) | successes $S(Y)$ (L4) | kept (L5) |
|---|---|---|---|
| 1 | 0.2380 | 3 | yes |
| 2 | 0.4703 | 2 | no |
| 3 | 0.7582 | 7 | no |
| 4 | 0.8009 | 7 | no |
| 5 | 0.5072 | 2 | no |
| 6 | 0.1631 | 1 | no |
| 7 | 0.8539 | 8 | no |
| 8 | 0.0449 | 1 | no |
| 9 | 0.1974 | 2 | no |
| 10 | 0.5201 | 4 | no |
| 11 | 0.9778 | 10 | no |
| 12 | 0.4663 | 5 | no |

One proposal in $12$ is kept. The exact acceptance probability is $\int_0^1 \binom{10}{3}p^3(1-p)^7\, dp = 1/11$, and the kept values follow the exact posterior Beta(4, 8), with mean $1/3$ and variance $0.017094$.

**The effect of the tolerance.** Same model, $4000$ kept values per row, `random.Random(2025)`. The exact columns come from $\pi_\varepsilon(p) \propto \sum_{|k-3| \le \varepsilon}\binom{10}{k}p^k(1-p)^{10-k}$ in rational arithmetic.

| $\varepsilon$ | acceptance, measured | exact | mean, measured | exact | variance, measured | exact |
|---|---|---|---|---|---|---|
| 0 | 0.0903 | 0.0909 | 0.3287 | 0.3333 | 0.01632 | 0.01709 |
| 1 | 0.2766 | 0.2727 | 0.3310 | 0.3333 | 0.02158 | 0.02137 |
| 2 | 0.4583 | 0.4545 | 0.3318 | 0.3333 | 0.03048 | 0.02991 |
| 3 | 0.6425 | 0.6364 | 0.3340 | 0.3333 | 0.04188 | 0.04274 |

The window is symmetric around $3$, so the mean does not move, but the variance grows by $25$ percent at $\varepsilon = 1$ and more than doubles at $\varepsilon = 3$. A larger tolerance keeps more proposals and gives a wider answer.

**An insufficient summary.** Same data, $(0, 1, 0, 0, 1, 0, 0, 1, 0, 0)$, but $S$ = the number of successes in the first five trials only. The kept values then follow Beta(3, 4), the posterior given half of the data: measured mean $0.4285$ and variance $0.03010$, against the exact $0.4286$ and $0.03061$. The algorithm is correct for the information in $S$, not for the information in $x$.

**The curse of dimensionality.** $x_1, \ldots, x_5 \sim N(\theta, 1)$ with prior $N(0, 3^2)$; the exact posterior standard deviation is $0.4423$. With $S = \bar x$ (one number), the acceptance probability halves when $\varepsilon$ halves: $0.245$, $0.134$, $0.066$ and $0.025$ for $\varepsilon = 1, 0.5, 0.25, 0.1$, with posterior standard deviations $0.685$, $0.524$, $0.465$ and $0.445$. With $S$ = the whole data vector in $\mathbb{R}^5$ and the Euclidean distance, it is $9.0 \times 10^{-4}$ at $\varepsilon = 1$ and $3.5 \times 10^{-5}$ at $\varepsilon = 0.5$, and $2 \times 10^6$ simulations give only one kept value at $\varepsilon = 0.25$.

## Correctness

The full proof is in proofs/correctness.md. It proves:

1. **The $\varepsilon$-posterior.** The kept values are independent draws from $\pi_\varepsilon(\theta) \propto \pi(\theta)a_\varepsilon(\theta)$, and the number of simulations per kept value is geometric with mean $1/A$, where $A = \int a_\varepsilon\, d\pi$.
2. **Exactness at $\varepsilon = 0$.** For a discrete summary, $\pi_0(\theta) = \pi(\theta \mid S(x))$ and $A = m_S(s_{\mathrm{obs}})$, the marginal likelihood of the summary. If the data are discrete and $S$ is sufficient, the [Fisher-Neyman factorization theorem](/fisher-neyman-factorization-theorem/) shows $f_S(s_{\mathrm{obs}} \mid \theta) \propto f(x \mid \theta)$, so $\pi_0$ is the exact posterior. For the binomial with a uniform prior, $A = 1/(n+1)$.
3. **The limit $\varepsilon \to 0$.** For continuous summaries in $\mathbb{R}^q$ with a bounded density continuous at $s_{\mathrm{obs}}$, $\pi_\varepsilon \to \pi(\cdot \mid S(x) = s_{\mathrm{obs}})$ and $A \approx m_S(s_{\mathrm{obs}})V_q\varepsilon^q$.

The key invariant is that each pass of L3 to L5 is an independent draw of $(\theta, Y)$ from the joint law, kept when $Y$ falls in a fixed set. What is proved and what is measured: items 1 and 2 are exact, and the tests check them with exact rational probabilities over every random path of one proposal, on $500$ random discrete models. Item 3 is a limit; the size of the error at a fixed $\varepsilon > 0$ is not bounded on this page but measured in the tables. The Kolmogorov-Smirnov distance of $2000$ kept values to Beta(4, 8) is below $1.95/\sqrt{2000}$ in the test.

## Complexity

Each pass costs one prior draw and one simulation of cost $C$. The number of passes per kept value is geometric with mean $1/A$, so $N$ values cost $\Theta(NC/A)$ in expectation. $A$ is the prior predictive probability of the $\varepsilon$-ball. It falls like $\varepsilon^q$ for $q$ continuous summaries, and it is small when the prior is wide compared with the posterior; for the binomial example, $A = (2\varepsilon + 1)/11$. The kept values take $\Theta(N)$ space; nothing else is stored.

## Properties

- **Exact for $\pi_\varepsilon$.** There is no Markov chain and no weight: the kept values are independent and identically distributed.
- **Likelihood-free.** Only forward simulation is needed.
- **Embarrassingly parallel and online.** Proposals are independent and can stop at any time.
- **Two approximations.** The summary loses information unless it is sufficient, and the tolerance widens the answer.
- **Gives the evidence of the summary.** The acceptance rate estimates $A$, and $A/(V_q\varepsilon^q)$ estimates $m_S(s_{\mathrm{obs}})$, which can be used for model choice only when $S$ is sufficient for both models together.

## Variants and improvements

- **Keep the closest fraction.** Simulate a fixed number $M$ of pairs and keep the fraction with the smallest distances; $\varepsilon$ is then a quantile of the distances. This is the common form in practice.
- **Regression adjustment.** Beaumont, Zhang and Balding (2002) fit a local linear regression of $\theta$ on $S(Y)$ among the kept pairs and shift each kept value to $s_{\mathrm{obs}}$, which allows a larger $\varepsilon$ for the same accuracy.
- **Smooth kernels.** Replace the indicator in L5 by a kernel weight $K_\varepsilon(\rho)$, giving weighted draws.
- **Sequential methods.** [ABC sequential Monte Carlo](/abc-sequential-monte-carlo/) moves a population through a falling sequence of tolerances, so proposals come from near the posterior instead of the prior. ABC with a Markov chain uses the same acceptance test inside [Metropolis-Hastings](/metropolis-hastings/).
- **Scaled distances.** When summaries have different scales, divide each by a robust spread, such as the median absolute deviation over prior simulations, before L5.

## When to use it

Use ABC rejection when the likelihood is intractable but the model can be simulated fast: coalescent models in population genetics, epidemic models, and stochastic models of cells or ecosystems. It is the right first method when the prior is not much wider than the posterior and there are few summaries, because it is simple, parallel and gives independent draws. When the likelihood can be evaluated, use [Bayesian inference](/bayesian-inference/) with MCMC or [importance sampling](/importance-sampling/) instead. When the acceptance rate is tiny, use [ABC sequential Monte Carlo](/abc-sequential-monte-carlo/) or regression adjustment. Check the result with [simulation-based calibration](/simulation-based-calibration/) on simulated data sets.

## Pitfalls

- **Raw data as the summary.** Taking $S(Y) = Y$ in L5 for continuous data has acceptance probability $0$ at $\varepsilon = 0$ and tiny acceptance otherwise, as the five-dimensional row shows. Use a few informative summaries in L5, ideally sufficient or close to it.
- **Insufficient summaries.** L5 with a summary that drops information gives the posterior given $S(x)$, which can be much wider, or biased for model choice. Choose $S$ so that it captures what the parameter changes, and test the choice on simulated data with known $\theta$.
- **Unscaled distances.** With $\rho$ the Euclidean distance on summaries of very different scales, L5 effectively uses only the largest one. Scale each summary before L5.
- **An improper or very wide prior.** L3 needs a proper prior, and a wide one makes $A$ tiny. Use a proper prior that is as narrow as the knowledge allows, or a sequential method.
- **Reporting $\pi_\varepsilon$ as the posterior.** With $\varepsilon > 0$, the kept values are wider than the posterior, by $25$ percent in variance at $\varepsilon = 1$ in the table. Report $\varepsilon$, and check that the answer is stable as $\varepsilon$ falls.

## Implementations

## History

Rubin (1984) described the procedure, draw from the prior, simulate, keep the draws whose simulated data match, as a way to explain what a posterior distribution is. Tavaré, Balding, Griffiths and Donnelly (1997) used it with an exact match on the number of segregating sites to infer coalescence times from DNA data. Pritchard, Seielstad, Perez-Lezaun and Feldman (1999) used several summary statistics with a tolerance to study the growth of human populations from Y chromosome data. Beaumont, Zhang and Balding (2002) named the approach approximate Bayesian computation and introduced regression adjustment. Sequential and Markov chain versions followed, and the method spread from population genetics to ecology, epidemiology and systems biology.

## References
