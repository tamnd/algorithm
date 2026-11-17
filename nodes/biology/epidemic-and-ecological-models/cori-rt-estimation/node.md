---
tag: FC6CRV
kind: algorithm
slug: cori-rt-estimation
name: Cori method for time-varying reproduction number
aliases:
- EpiEstim method
- Rt estimation
area: biology/epidemic-and-ecological-models
level: advanced
summary: Estimate R_t over a sliding window with a conjugate gamma posterior from a Poisson renewal model of daily incidence.
model: real-ram
complexity:
  vars: {T: the number of days of incidence, s: the number of days in the generation interval distribution}
  time: {worst: Θ(T s), average: Θ(T s), best: Θ(T s)}
  space: {extra: Θ(T)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 2013
  people: [Anne Cori, Neil M. Ferguson, Christophe Fraser, Simon Cauchemez]
  note: Cori, Ferguson, Fraser and Cauchemez published the method with the R package EpiEstim in 2013, building on the renewal form of incidence that Fraser had used in 2007.
prereqs: [epidemic-renewal-equation, conjugate-prior, poisson-distribution]
see_also: [epidemic-renewal-equation, generation-interval, conjugate-prior, credible-interval, bayes-theorem, basic-reproduction-number, particle-filter, sequential-monte-carlo]
sources:
  - paper: "Anne Cori, Neil M. Ferguson, Christophe Fraser and Simon Cauchemez, A new framework and software to estimate time-varying reproduction numbers during epidemics, American Journal of Epidemiology 178(9), 2013"
    title: Cori et al. 2013
    locator: the Poisson renewal likelihood over a window, the gamma posterior, and the EpiEstim software
  - paper: doi:10.1371/journal.pone.0000758
    title: "Christophe Fraser, Estimating individual and household reproduction numbers in an emerging epidemic, PLoS ONE 2(8), e758, 2007"
    locator: the instantaneous reproduction number and its estimation from the renewal equation
  - url: https://rdrr.io/cran/EpiEstim/man/make_config.html
    title: EpiEstim reference manual, make_config
    locator: the window settings, with weekly sliding windows in the example, and the rule that the first entry of the serial interval distribution must be 0
  - paper: "Katelyn M. Gostic and others, Practical considerations for measuring the effective reproductive number, Rt, PLoS Computational Biology 16(12), e1008409, 2020"
    title: Gostic et al. 2020
    locator: the effects of reporting delays, of the choice of the interval distribution and of the window length on estimates of R_t
  - paper: "R. N. Thompson and others, Improved inference of time-varying reproduction numbers during infectious disease outbreaks, Epidemics 29, 2019"
    title: Thompson et al. 2019
    locator: imported cases and the uncertainty in the serial interval
---

The Cori method estimates how the reproduction number $R_t$ of an epidemic changes over time from a series of daily case counts. It assumes the [renewal equation](/epidemic-renewal-equation/): the expected number of new cases on day $t$ is $R_t$ times the total infectiousness $\Lambda_t$, the past cases weighted by the [generation interval](/generation-interval/). It takes $R_t$ as constant over a window of $\tau$ days that ends on day $t$, puts a gamma prior on it, and gets a gamma posterior in closed form, because the gamma law is the [conjugate prior](/conjugate-prior/) of the Poisson rate. Sliding the window over the series gives an estimate and a [credible interval](/credible-interval/) for every day, at a cost that is linear in the length of the series.

## In plain words

Each sick person passes the disease on to some others over the next few days. On any day, you can add up how much "infecting power" is still active from the people who fell ill before. If ten new cases appear on a day with an infecting power worth only eight cases, then each case is passing the disease on to a bit more than one other person, and the epidemic grows.

One day gives a noisy answer, so the method uses a week at a time and assumes the true value stays the same over the week. It starts from a rough guess, then updates the guess with the counts of the week. The more cases there are, the narrower the range of likely values. Then it moves the week forward by one day and does it again.

## The problem

**Input.** Daily incidence $I_1, \ldots, I_T$ (counts of new infections, or of new symptom onsets as a proxy). A generation interval distribution $w_1, \ldots, w_{s}$ with $w_u \ge 0$, $\sum_u w_u = 1$, and $w_0 = 0$. A window length $\tau \ge 1$. The shape $a > 0$ and the scale $b > 0$ of a gamma prior on $R$.

**Model.** Given the earlier counts, $I_t$ is Poisson($R_t \Lambda_t$), with $\Lambda_t = \sum_{u=1}^{s} w_u I_{t-u}$, and $R_t$ is constant over each window.

**Output.** For each window $\{t - \tau + 1, \ldots, t\}$, the posterior law of $R$: its shape $A_t$ and rate $B_t$, its mean, standard deviation and coefficient of variation, and chosen quantiles.

## The algorithm

```pseudo id=main
CORI-RT(I[1..T], w, τ, a, b)
L1  for t ← 1 to T do Λ[t] ← Σ_{u=1}^{min(t-1, s)} w[u] I[t - u]
L2  for t ← τ + 1 to T do                       ▷ window t - τ + 1 .. t, starting on day 2 or later
L3      A ← a + Σ_{u=t-τ+1}^{t} I[u]
L4      B ← 1/b + Σ_{u=t-τ+1}^{t} Λ[u]
L5      mean ← A / B, sd ← √A / B
L6      quantiles ← quantiles of Gamma(shape A, rate B)
L7      output (t, A, B, mean, sd, quantiles)
```

Lines L3 and L4 use prefix sums of $I$ and $\Lambda$, so each window costs $O(1)$ besides the quantiles. The implementation finds a quantile by bisection on the gamma distribution function, which it evaluates through the chi-squared tail: if $R$ is gamma with shape $A$ and rate $B$, then $2BR$ is chi-squared with $2A$ degrees of freedom. The prior in the example below has $a = 1$ and $b = 5$, a mean of 5 and a standard deviation of 5. That is a broad prior, and it is the value this page uses, not a property of the method.

## Example

Take $w_1 = 0.2$, $w_2 = 0.5$, $w_3 = 0.3$ and the counts

| day | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $I_t$ | 10 | 4 | 8 | 9 | 11 | 14 | 15 | 21 | 24 | 16 | 18 | 15 | 13 |
| $\Lambda_t$ | 0 | 2.0 | 5.8 | 6.6 | 7.0 | 9.1 | 11.0 | 13.3 | 15.9 | 19.8 | 21.5 | 18.8 | 16.8 |

For example, $\Lambda_5 = 0.2 \times 9 + 0.5 \times 8 + 0.3 \times 4 = 7.0$. With windows of $\tau = 4$ days and the prior $a = 1$, $b = 5$, the first window is days 2 to 5. There $A = 1 + (4 + 8 + 9 + 11) = 33$ and $B = 0.2 + (2.0 + 5.8 + 6.6 + 7.0) = 21.6$, so the posterior mean is $33 / 21.6 = 1.528$, the standard deviation is $\sqrt{33}/21.6 = 0.266$ and the 95% credible interval is $[1.052, 2.091]$. The other windows give:

| window | $A$ | $B$ | mean | 2.5% | median | 97.5% |
|---|---|---|---|---|---|---|
| 2 to 5 | 33 | 21.6 | 1.528 | 1.052 | 1.512 | 2.091 |
| 4 to 7 | 50 | 33.9 | 1.475 | 1.095 | 1.465 | 1.911 |
| 6 to 9 | 75 | 49.5 | 1.515 | 1.192 | 1.508 | 1.877 |
| 8 to 11 | 80 | 70.7 | 1.132 | 0.897 | 1.127 | 1.393 |
| 10 to 13 | 63 | 77.1 | 0.817 | 0.628 | 0.813 | 1.031 |

The estimate falls below 1 in the last window, as the counts start to decline after day 9.

**A step change.** The implementation also simulates the Poisson renewal model. With a generation interval of mean 3.99 days spread over 8 days, a seed of 20 cases a day for 5 days, $R_t = 1.8$ for 25 days and then $R_t = 0.7$, seed 20261118 and weekly windows, the estimate for the window that ends on day 30 is $1.790$ with the interval $[1.737, 1.844]$, and for the window that ends on day 55 it is $0.745$ with $[0.693, 0.799]$. The window that ends on day 35 straddles the change and gives $0.956$. So a window estimate lags a sudden change by up to $\tau$ days.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Because $w_0 = 0$, $\Lambda_u$ depends only on the counts before day $u$. So by the chain rule, the probability of the counts in the window, given the earlier counts, is the product of Poisson($R \Lambda_u$) masses. As a function of $R$, it is proportional to $R^{\sum I_u} e^{-R \sum \Lambda_u}$. Multiplying by the gamma prior density $R^{a-1} e^{-R/b}$ gives $R^{A - 1} e^{-BR}$, a gamma density with shape $A$ and rate $B$. Lines L3 and L4 compute these two numbers with prefix sums, line L5 uses the gamma mean $A/B$ and variance $A/B^2$, and line L6 inverts the gamma distribution function, which is continuous and strictly increasing, by bisection.

## Complexity

Line L1 costs $\Theta(T s)$ arithmetic operations, where $s$ is the length of the generation interval. A fast [convolution](/convolution/) would make it $O(T \log T)$, which only helps when $s$ is large. The prefix sums take $\Theta(T)$, and each window takes $O(1)$ for $A$, $B$, the mean and the standard deviation. Each quantile takes a fixed number of bisection steps for a given tolerance, each with one evaluation of the incomplete gamma function. So the total is $\Theta(T s)$ plus a cost per quantile that does not depend on $T$. The extra space is $\Theta(T)$ for $\Lambda$ and the prefix sums. When a new day of data arrives, one more $\Lambda$ value and one more window cost $O(s)$.

## Properties

- **Exact under the model.** The posterior is exact, not an approximation, for the Poisson renewal model with $R$ constant on the window. Simulation-based calibration in the tests confirms it: with $R$ drawn from the prior, the posterior distribution function at the true $R$ is uniform.
- **Scale of the counts.** If every count is multiplied by a constant reporting fraction, $\Lambda$ scales in the same way, so the posterior mean barely moves, but the interval shrinks or widens with the count.
- **Precision from the count.** The coefficient of variation of the posterior is $1/\sqrt{A}$, so it depends only on the number of cases in the window, plus $a$. About 100 cases in a window give a coefficient of variation near 0.1.
- **Uses only the past.** The estimate for day $t$ uses counts up to day $t$. It estimates the instantaneous reproduction number, not the case reproduction number, which needs future data.

## Variants and improvements

- **Uncertainty in the generation interval.** Draw many plausible interval distributions, compute the posterior for each, and pool the samples. The EpiEstim package offers this, and [Thompson et al.](#references) extended it.
- **Imported cases.** Cases infected elsewhere count in $\Lambda$, because they can infect others, but not in the window sum of $I$, because local transmission did not cause them. Counting them as local makes $R_t$ too high early in an outbreak.
- **Wallinga and Teunis.** A related method estimates the case reproduction number from the likelihood that each case infected each later one. It needs future data, so recent values are revised.
- **Smooth priors and state-space models.** In place of independent windows, let $\log R_t$ follow a random walk, and use a [particle filter](/particle-filter/) or [sequential Monte Carlo](/sequential-monte-carlo/) for the filtered law of $R_t$. This also allows observation models with reporting delays and negative binomial noise.
- **Other window rules.** Non-overlapping windows, or windows set at the times of known changes, such as the start of a lockdown.

## When to use it

Use it for quick, transparent estimates of $R_t$ from a clean daily series of infections or symptom onsets, when the generation interval is known from other studies. It has no tuning beyond the window, the prior and $w$, and it runs in a fraction of a second on a series of years. Do not use it on raw counts by report date when the delay from infection to report is long or changing; model the delay first, or use a method with an explicit observation model ([Gostic et al.](#references)).

## Pitfalls

- **Wrong interval distribution.** The estimate depends on $w$: for the same growth rate, a longer interval gives a larger $R$ (see the [generation interval](/generation-interval/)). The serial interval is often used in place of the generation interval because it is easier to observe. Its mean is about the same, but a larger spread changes $R_t$ when it is far from 1.
- **The first entry of $w$.** It must be 0. A case cannot infect on the day of its own infection, and a positive $w_0$ would put $I_t$ inside its own $\Lambda_t$. EpiEstim rejects such a distribution.
- **Reporting delays.** Counts by date of report describe infections some days earlier. An estimate from them refers to that earlier time, and it is smeared by the spread of the delay. Right truncation, the missing recent cases that are not reported yet, makes the latest estimates too low.
- **The start of an epidemic.** When $\Lambda$ is small, the prior has a large weight, and the estimate is unreliable. Check the coefficient of variation $1/\sqrt{A}$ before reading the estimate.
- **Window lag.** The estimate for the window that ends on day $t$ describes the whole window. A sudden change shows up in full only $\tau$ days later, as in the step change example.
- **Changes in testing.** If the fraction of infections that are counted changes over the window, the counts change for reasons other than transmission, and $R_t$ moves with them.

## Implementations

## History

Fraser (2007) defined the instantaneous reproduction number through the renewal equation and showed how to estimate it from incidence. Cori, Ferguson, Fraser and Cauchemez (2013) turned this into a simple Bayesian method with a gamma posterior over sliding windows, and they published it with the R package EpiEstim. The method came into wide use for real-time tracking of epidemics, and later work added the uncertainty in the serial interval, imported cases ([Thompson et al.](#references)) and studies of its biases ([Gostic et al.](#references)).

## References
