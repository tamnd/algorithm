---
tag: 7K0XX7
kind: algorithm
slug: mixture-sequential-probability-ratio-test
name: Mixture sequential probability ratio test
aliases:
- mSPRT
- always valid p-value
area: statistics-and-inference/time-series-and-sequential-analysis
level: research
summary: An SPRT whose alternative is a mixture over effect sizes. Its likelihood ratio is a test martingale, so its test and its p-values stay valid at any stopping time.
model: real-ram
complexity:
  vars: {n: "the number of observations read before the test stops or the stream ends"}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, recursive: false, anytime_valid: true}
history:
  year: 1970
  people: [Herbert Robbins, Ramesh Johari, Pete Koomen, Leonid Pekelis, David Walsh]
  note: Robbins introduced the method of mixtures for boundary crossings in 1970. Johari, Koomen, Pekelis and Walsh named the mSPRT and its always valid p-values for online A/B tests in 2017.
prereqs: [sequential-probability-ratio-test, test-martingale, ville-inequality, p-value]
see_also: [confidence-sequence, group-sequential-design, bayes-factor, e-variable, z-test, multiple-comparisons-problem, cusum, alpha-spending-function]
sources:
  - paper: doi:10.1214/aoms/1177696786
    title: Herbert Robbins, Statistical methods related to the law of the iterated logarithm, Annals of Mathematical Statistics 41(5) (1970), pages 1397 to 1409
    locator: the method of mixtures, which mixes the likelihood ratio over a prior on the alternative and bounds the crossing probability of the mixture
  - paper: doi:10.1145/3097983.3097992
    title: Ramesh Johari, Pete Koomen, Leonid Pekelis and David Walsh, Peeking at A/B tests, why it matters, and what to do about it, Proceedings of KDD 2017, pages 1517 to 1525
    locator: the mSPRT with a normal mixing distribution and the always valid p-values used in an online experimentation platform
  - paper: doi:10.1287/opre.2021.2135
    title: Ramesh Johari, Pete Koomen, Leonid Pekelis and David Walsh, Always valid inference, continuous monitoring of A/B tests, Operations Research 70(3) (2022), pages 1806 to 1821
    locator: the definition of always valid p-values and confidence intervals, their construction from the mSPRT, and the choice of the mixing distribution
  - paper: doi:10.1214/23-STS894
    title: Aaditya Ramdas, Peter Grünwald, Vladimir Vovk and Glenn Shafer, Game-theoretic statistics and safe anytime-valid inference, Statistical Science 38(4) (2023), pages 576 to 601
    locator: mixture likelihood ratios as test martingales and the resulting anytime-valid p-values
---

The mixture sequential probability ratio test (mSPRT) tests a point null hypothesis $\theta = \theta_0$ against the composite alternative $\theta \ne \theta_0$ while the data arrive. Where the [SPRT](/sequential-probability-ratio-test/) needs one alternative value, the mSPRT averages the likelihood ratio over a mixing distribution of alternatives that is fixed in advance. The mixture is a [test martingale](/test-martingale/) under the null, so by [Ville's inequality](/ville-inequality/) the rule "reject when the mixture reaches $1/\alpha$" has type I error at most $\alpha$ for every way the analyst may look at the data and stop. The reciprocal of its running maximum is an always valid [p-value](/p-value/), which online experiment platforms show to users who check their results every day.

## In plain words

In an online experiment people look at the results every day and stop as soon as the effect looks significant. A normal test assumes that you look only once, at a size fixed in advance. Each extra look is a new chance for noise to look like an effect, so the false alarm rate grows well above the stated level. The mSPRT keeps a single running score that compares "there is some effect, of a size from a range fixed in advance" with "there is no effect". If there is truly no effect, the score is a fair game that cannot go below zero, so it seldom gets large. You may look after every new data point and stop when you like. The false alarm rate stays below the level you chose. The price is that a real effect needs somewhat more data to show.

## The problem

Observations $X_1, X_2, \ldots$ are i.i.d. with density $f_\theta$ from a parametric family. Test $H_0: \theta = \theta_0$ against $H_1: \theta \ne \theta_0$, with a rule that may stop at any stopping time $T$, chosen by the analyst while the data arrive, such that
$$P_{\theta_0}(\text{the test rejects at or before } T) \le \alpha \quad \text{for every stopping time } T,$$
and such that the test rejects eventually under every alternative. Also produce p-values $p_n$ with $P_{\theta_0}(p_T \le u) \le u$ for every stopping time $T$ and every $u \in [0, 1]$. These are the always valid p-values of Johari, Koomen, Pekelis and Walsh.

Given a mixing distribution $\pi$ on the parameters, the mixture likelihood ratio is
$$\Lambda_n = \int \prod_{i=1}^n \frac{f_\theta(X_i)}{f_{\theta_0}(X_i)}\,\pi(d\theta).$$
For normal data $N(\theta, \sigma^2)$ with $\sigma$ known and $\pi = N(\theta_0, \tau^2)$, with $S_n = \sum_{i \le n}(X_i - \theta_0)$, the integral has the closed form
$$\Lambda_n = \sqrt{\frac{\sigma^2}{\sigma^2 + n\tau^2}}\,\exp\left(\frac{\tau^2 S_n^2}{2\sigma^2(\sigma^2 + n\tau^2)}\right).$$

## The algorithm

```pseudo id=main
MSPRT(x_1, x_2, ..., θ_0, σ, τ, α)          ▷ σ, τ > 0 and 0 < α < 1
L1  S ← 0, n ← 0, p ← 1
L2  for each new observation x do
L3      n ← n + 1, S ← S + (x - θ_0)
L4      Λ ← sqrt(σ² / (σ² + nτ²)) · exp(τ² S² / (2σ²(σ² + nτ²)))
L5      p ← min(p, 1 / Λ)                   ▷ always valid p-value p_n
L6      if Λ ≥ 1/α then return (reject H_0, n, p)
L7  return (no rejection, n, p)
```

Line L3 keeps the centred sum, which is a sufficient statistic. Line L4 evaluates the closed-form mixture. Line L5 keeps $p_n = \min(1, 1/\max_{k \le n}\Lambda_k)$, which never increases, so a p-value once shown can only go down. Line L6 rejects at the first time the mixture reaches $1/\alpha$; this is the same event as $p_n \le \alpha$. There is no lower threshold: the test never accepts $H_0$, and if the analyst stops for another reason, line L7 reports that the test did not reject and gives the current p-value.

## Example

Let $\theta_0 = 0$, $\sigma = \tau = 1$ and $\alpha = 0.05$, so the threshold is $\Lambda \ge 20$. On the data $0.8, 1.4, -0.2, 1.1, 0.9, 1.6, 0.3, 1.2$:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $S_n$ | 0.8 | 2.2 | 2.0 | 3.1 | 4.0 | 5.6 | 5.9 | 7.1 |
| $\Lambda_n$ | 0.830 | 1.294 | 0.824 | 1.169 | 1.549 | 3.550 | 3.114 | 5.485 |
| always valid $p_n$ | 1 | 0.7731 | 0.7731 | 0.7731 | 0.6457 | 0.2817 | 0.2817 | 0.1823 |
| fixed-$n$ z-test p-value | 0.4237 | 0.1198 | 0.2482 | 0.1211 | 0.0736 | 0.0222 | 0.0257 | 0.0121 |

The mSPRT does not reject: its largest value is 5.485, far below 20. The two-sided [z-test](/z-test/) p-value $2\bar\Phi(|S_n|/\sqrt n)$ falls below 0.05 at $n = 6$, so an analyst who reruns the fixed-sample test after every observation would stop at $n = 6$ and claim an effect. That p-value is valid only if $n = 6$ was fixed in advance.

The difference matters under the null. In 2000 simulated streams of $N(0, 1)$ data with a horizon of 500 observations, the mSPRT with $\tau = 1$ rejected in 2.55% of the streams, while the z-test at level 0.05 repeated after every observation rejected at some time in 49.35% of them.

## Correctness

The proofs are in full below; this is a summary.

1. **Closed form.** With $u = \theta - \theta_0$, the product of normal likelihood ratios is $\exp(uS_n/\sigma^2 - nu^2/(2\sigma^2))$. Integrating it against the $N(0, \tau^2)$ density of $u$ is a Gaussian integral and gives the formula of line L4.
2. **Test martingale.** For each fixed $\theta$, the product $L_n(\theta) = \prod_{i \le n} f_\theta(X_i)/f_{\theta_0}(X_i)$ is a nonnegative martingale with mean 1 under $\theta_0$. By Tonelli's theorem, $E_{\theta_0}[\Lambda_n \mid \mathcal F_{n-1}] = \int E_{\theta_0}[L_n(\theta) \mid \mathcal F_{n-1}]\,\pi(d\theta) = \Lambda_{n-1}$, so $\Lambda$ is a test martingale.
3. **Level at every stopping time.** The test rejects at or before $T$ only if $\Lambda_n \ge 1/\alpha$ for some $n$. By Ville's inequality this has probability at most $\alpha$ under $\theta_0$, whatever $T$ is, including $T = \infty$.
4. **Always valid p-values.** For $u \in (0, 1]$, $\{p_T \le u\} \subseteq \{\exists n: \Lambda_n \ge 1/u\}$, which has probability at most $u$ by Ville's inequality. So $p_T$ is a valid p-value for every stopping time $T$.
5. **Power one.** If $\theta \ne \theta_0$, then $S_n/n \to \theta - \theta_0$ almost surely, the exponent in line L4 grows like $n(\theta - \theta_0)^2/(2\sigma^2)$, and the prefactor shrinks only like $n^{-1/2}$. So $\Lambda_n \to \infty$ almost surely, and the test rejects in finite time with probability 1.

## Complexity

Each observation costs one update of $S$, one exponential and one square root, so the time is $\Theta(n)$ for the $n$ observations read and the extra space is $\Theta(1)$. Under an alternative with effect $\delta = \theta - \theta_0$, setting $S_n \approx n\delta$ in line L4 shows that the test rejects at about the $n$ where
$$\frac{n\delta^2}{2\sigma^2} \approx \log\frac1\alpha + \frac12\log\frac{n\tau^2}{\sigma^2},$$
so the expected sample size grows like $2\sigma^2\log(1/\alpha)/\delta^2$ plus a term of order $\log(1/\delta)/\delta^2$. A one-sided [SPRT](/sequential-probability-ratio-test/) that knows $\delta$ needs about $2\sigma^2\log(1/\alpha)/\delta^2$; the extra logarithm is the cost of not knowing $\delta$.

## Properties

- **Anytime valid.** The type I error bound holds for continuous monitoring, for stopping when the data look good, and for never stopping.
- **One threshold.** The test never accepts $H_0$. A study that must end at a fixed horizon reports "no rejection" and the p-value at that point.
- **Monotone p-values.** $p_n$ never increases, so a result that was significant stays significant.
- **Conservative.** Ville's inequality has slack because the mixture jumps over $1/\alpha$, and because a stream that stops early has no chance to cross later. The realized level is below $\alpha$, 2.55% in the simulation above.
- **Inverts to a confidence sequence.** The set of $\theta_0$ that the mSPRT has not rejected by time $n$ is the normal mixture [confidence sequence](/confidence-sequence/).

## Variants and improvements

- **Other mixing distributions.** Any $\pi$ fixed before the data works. A normal $\pi$ gives the closed form above; a one-sided mixture on $\theta > \theta_0$ gives a one-sided test with more power on that side. The mixing scale $\tau$ chooses the effect sizes at which the test is fastest; Johari et al. (2022) discuss how to choose it from the effect sizes seen in earlier experiments.
- **Bernoulli data.** For coin flips with null $p_0$ and a $\mathrm{Beta}(a, b)$ mixture, the ratio is $B(a + h, b + k)/(B(a, b)\,p_0^h(1 - p_0)^k)$ after $h$ heads and $k$ tails. It is a [Bayes factor](/bayes-factor/) and a test martingale for the same reason.
- **Two-sample A/B tests.** With large samples, the difference of the arm means is close to normal with known variance, and the normal mSPRT is applied to it; this is the setting of Johari et al.
- **Multiple tests.** Always valid p-values can be fed into Bonferroni or Benjamini-Hochberg procedures for many metrics at once; the [multiple comparisons problem](/multiple-comparisons-problem/) remains.
- **E-processes.** For composite nulls, an infimum of test martingales over the null gives an e-process, which still gives anytime-valid tests (see [test martingale](/test-martingale/)).
- **Group sequential designs.** When the number of looks is small and fixed in advance, a [group sequential design](/group-sequential-design/) with [alpha spending](/alpha-spending-function/) gives more power than the mSPRT.

## When to use it

Use the mSPRT when analysts will look at the results continuously, the stopping rule is not fixed, and the null is a point such as "no difference between the arms". It fits online A/B tests, monitoring dashboards and adaptive data collection. When the looks are few and planned, a group sequential design has more power. When there are only two simple hypotheses, the SPRT is faster.

## Pitfalls

- **Choosing the mixture after seeing the data.** The guarantee needs $\pi$ fixed in advance. Tuning $\tau$ on the same data voids it.
- **Unknown variance.** The closed form assumes $\sigma$ known. Plugging in an estimate is an approximation that is accurate only for large $n$.
- **Dependent data.** Daily or weekly cycles in traffic break the i.i.d. assumption, and with it the martingale property.
- **Reading $p_n$ as a fixed-sample p-value.** It is larger than the fixed-sample p-value at the same $n$, as the example shows; that is the price of validity at all times.
- **Effect estimates at the stopping time.** The sample mean when the test stops is biased away from zero. Report a [confidence sequence](/confidence-sequence/) instead.

## Implementations

## History

Robbins (1970) introduced the method of mixtures: average the likelihood ratio over a distribution of alternatives and apply the maximal inequality for nonnegative martingales to bound the probability of ever crossing a boundary. He used it to build tests of power one and confidence sequences. Johari, Koomen, Pekelis and Walsh (2017, 2022) named the test the mSPRT, defined always valid p-values and confidence intervals, and deployed them in a commercial A/B testing platform. Ramdas, Grünwald, Vovk and Shafer (2023) place it within the theory of test martingales and e-values.

## References
