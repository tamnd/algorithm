---
tag: 9JY1HF
kind: algorithm
slug: sequential-probability-ratio-test
name: Sequential probability ratio test
aliases:
- SPRT
- Wald's sequential test
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: Wald's test that reads one observation at a time and stops when the likelihood ratio leaves an interval (B, A). No test with its error rates has a smaller expected sample size.
model: real-ram
complexity:
  vars: {n: "the number of observations read before the test stops, a random stopping time"}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, recursive: false, exact_error_bounds: true}
history:
  year: 1945
  people: [Abraham Wald]
  note: Wald developed the test in 1943 in the Statistical Research Group at Columbia University and published it in the Annals of Mathematical Statistics in 1945. Wald and Wolfowitz proved its optimality in 1948.
prereqs: [likelihood-ratio-test, type-i-and-type-ii-errors, walds-equation]
see_also: [mixture-sequential-probability-ratio-test, cusum, test-martingale, ville-inequality, neyman-pearson-lemma, group-sequential-design, signal-detection, statistical-model-checking]
sources:
  - paper: doi:10.1214/aoms/1177731118
    title: Abraham Wald, Sequential tests of statistical hypotheses, Annals of Mathematical Statistics 16(2) (1945), pages 117 to 186
    locator: the definition of the test, the inequalities for the thresholds A and B, and the approximation of the expected sample size
  - book: isbn:9780486439129
    title: Abraham Wald, Sequential Analysis, Wiley, 1947, reprinted by Dover, 2004
    locator: Chapter 3 (the sequential probability ratio test) and the appendix (the fundamental identity)
  - paper: doi:10.1214/aoms/1177730197
    title: A. Wald and J. Wolfowitz, Optimum character of the sequential probability ratio test, Annals of Mathematical Statistics 19(3) (1948), pages 326 to 339
    locator: the theorem that the SPRT minimizes the expected sample size under both hypotheses among tests with no larger error probabilities
  - book: isbn:9780387961347
    title: David Siegmund, Sequential Analysis, Tests and Confidence Intervals, Springer, 1985
    locator: Chapter II (the sequential probability ratio test, the approximations for the error probabilities and the expected sample size, and its optimality)
  - book: isbn:9781439838204
    title: Alexander Tartakovsky, Igor Nikiforov and Michèle Basseville, Sequential Analysis, Hypothesis Testing and Changepoint Detection, CRC Press, 2014
    locator: Chapter 3 (sequential hypothesis testing, two simple hypotheses)
---

The sequential probability ratio test (SPRT) decides between two simple hypotheses, $H_0$: the observations have density $f_0$, and $H_1$: they have density $f_1$, by reading one observation at a time. After each one it updates the log [likelihood ratio](/likelihood-ratio-test/) and stops as soon as it leaves an interval $(a, b)$ set by the target [error rates](/type-i-and-type-ii-errors/) $\alpha$ and $\beta$. Wald's thresholds guarantee error rates at most $\alpha/(1 - \beta)$ and $\beta/(1 - \alpha)$ with no approximation, and the expected number of observations is often half of what a fixed-sample test of the same strength needs. Wald and Wolfowitz proved that no sequential test with the same error probabilities has a smaller expected sample size under either hypothesis.

## In plain words

You want to know whether a coin is fair or biased toward heads, and each flip costs money. Keep a score. A head is more likely under the biased coin, so it adds to the score; a tail subtracts. The amounts come from how much more likely each outcome is under one answer than under the other. Before you start, set an upper line and a lower line from how often you accept being wrong each way. Flip until the score crosses a line. Cross the upper line and you declare the coin biased; cross the lower line and you declare it fair. When the evidence is clear you stop early. When it is mixed you keep going. On average you need far fewer flips than a plan that fixes the number in advance.

## The problem

Observations $X_1, X_2, \ldots$ are i.i.d. with density $f$ with respect to a measure $\nu$, and $f \in \{f_0, f_1\}$. The densities $f_0$ and $f_1$ are positive on the same set, and they differ on a set of positive $\nu$-measure. Given $\alpha, \beta > 0$ with $\alpha + \beta < 1$, find a stopping rule $N$, which may depend only on the observations seen so far, and a decision at time $N$ such that the realized error rates
$$\alpha' = P_0(\text{reject } H_0), \qquad \beta' = P_1(\text{accept } H_0)$$
are about $\alpha$ and $\beta$, and the average sample numbers $E_0[N]$ and $E_1[N]$ are small. Write $Z_i = \log f_1(X_i) - \log f_0(X_i)$ and $\Lambda_n = Z_1 + \cdots + Z_n$.

## The algorithm

```pseudo id=main
SPRT(x_1, x_2, ..., f_0, f_1, α, β)        ▷ α, β > 0 and α + β < 1
L1  a ← log(β / (1 - α)),  b ← log((1 - β) / α)
L2  Λ ← 0, n ← 0
L3  for each new observation x do
L4      n ← n + 1
L5      Λ ← Λ + log f_1(x) - log f_0(x)    ▷ Λ is now Λ_n
L6      if Λ ≥ b then return (reject H_0, n)
L7      if Λ ≤ a then return (accept H_0, n)
```

Line L1 sets Wald's thresholds. In the ratio scale they are $A = e^b = (1 - \beta)/\alpha$ and $B = e^a = \beta/(1 - \alpha)$, and $B < 1 < A$ because $\alpha + \beta < 1$. Lines L4 and L5 add one log likelihood ratio per observation, so $\Lambda$ is a random walk with negative drift $-D(f_0 \,\|\, f_1)$ under $H_0$ and positive drift $D(f_1 \,\|\, f_0)$ under $H_1$, where $D$ is the [Kullback-Leibler divergence](/kullback-leibler-divergence/). Lines L6 and L7 stop at the first exit from $(a, b)$; the walk usually jumps past the threshold, and this overshoot makes the true error rates smaller than the nominal ones.

## Example

Test a fair coin, $f_0$: heads with probability $0.5$, against $f_1$: heads with probability $0.8$, with $\alpha = \beta = 0.1$. Then $b = \log 9 \approx 2.197$ and $a = -2.197$. A head adds $\log(0.8/0.5) = \log 1.6 \approx 0.470$ and a tail adds $\log(0.2/0.5) = \log 0.4 \approx -0.916$. On the flips HHTHHHHH:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| flip | H | H | T | H | H | H | H | H |
| $\Lambda_n$ | 0.470 | 0.940 | 0.024 | 0.494 | 0.964 | 1.434 | 1.904 | 2.374 |

At $n = 8$, $\Lambda_8 = 7\log 1.6 + \log 0.4 \approx 2.374 \ge 2.197$, so the test rejects $H_0$.

The state of this test after $n$ flips is the number of heads, so a dynamic program over (flips, heads) gives its exact operating characteristics:

| quantity | exact | Wald's value |
|---|---|---|
| type I error $\alpha'$ | 0.08443 | bound $\alpha/(1 - \beta) = 0.1111$ |
| type II error $\beta'$ | 0.07738 | bound $\beta/(1 - \alpha) = 0.1111$ |
| $E_0[N]$ | 9.365 | approximation 7.877 |
| $E_1[N]$ | 10.474 | approximation 9.120 |

The fixed-sample binomial test with $\alpha \le 0.1$ and $\beta \le 0.1$ needs 19 flips (reject when there are at least 13 heads; its errors are 0.0835 and 0.0676). The SPRT uses about half as many on average.

For normal data, $H_0$: $N(0, 1)$ against $H_1$: $N(0.5, 1)$ with $\alpha = \beta = 0.05$, 20 000 simulated runs under each hypothesis gave $\alpha' \approx 0.040$, $\beta' \approx 0.039$ and an average sample number of about 24.1 under both, against Wald's approximation 21.2. The one-sided fixed-sample [z-test](/z-test/) needs $n = (2 \times 1.645 / 0.5)^2 \approx 43.3$, so 44 observations.

## Correctness

Four facts, proved in full below.

1. **Termination.** Under any i.i.d. law for which $Z_1$ is not almost surely 0, in particular under $H_0$ and $H_1$, there are $m \ge 1$ and $\delta > 0$ with $P(N > km) \le (1 - \delta)^k$. Any block of $m$ consecutive increments that are all larger than $c$, with $mc > b - a$, forces an exit. So $N < \infty$ almost surely and $E[N] < \infty$.
2. **Wald's error bounds.** On $\{N = n\}$, the measures $P_1$ and $P_0$ differ by the factor $e^{\Lambda_n}$. On rejection $e^{\Lambda_N} \ge A$ and on acceptance $e^{\Lambda_N} \le B$, so $1 - \beta' \ge A\alpha'$ and $\beta' \le B(1 - \alpha')$. These give
$$\alpha' \le \frac{\alpha}{1 - \beta}, \qquad \beta' \le \frac{\beta}{1 - \alpha}, \qquad \alpha' + \beta' \le \alpha + \beta.$$
The bound on $\alpha'$ also follows from [Ville's inequality](/ville-inequality/), because $e^{\Lambda_n}$ is a [test martingale](/test-martingale/) under $H_0$.
3. **The average sample number.** If $E_j|Z_1| < \infty$, [Wald's equation](/walds-equation/) gives $E_j[\Lambda_N] = E_j[Z_1]\,E_j[N]$ exactly. Replacing $\Lambda_N$ by $b$ on rejection and $a$ on acceptance, that is, ignoring the overshoot, gives Wald's approximations
$$E_0[N] \approx \frac{\alpha b + (1 - \alpha) a}{-D(f_0 \,\|\, f_1)}, \qquad E_1[N] \approx \frac{(1 - \beta) b + \beta a}{D(f_1 \,\|\, f_0)}.$$
These are approximations, not bounds. In the coin example they are below the exact values by 1.5 and 1.4 observations.
4. **Optimality.** Wald and Wolfowitz (1948) proved that among all tests, sequential or not, with $P_0(\text{reject}) \le \alpha'$ and $P_1(\text{accept}) \le \beta'$, where $\alpha'$ and $\beta'$ are the error rates of the SPRT itself, none has a smaller $E_0[N]$ or a smaller $E_1[N]$. This page cites that theorem and does not prove it.

## Complexity

Each observation costs one evaluation of $\log f_1 - \log f_0$, one addition and two comparisons, so the time is $\Theta(n)$ for the $n$ observations read, and the extra space is $\Theta(1)$. The number read is the random stopping time $N$: it has an exponential tail by fact 1, and its mean is given by fact 3. For the exact operating characteristics of a discrete model, the dynamic program of the example costs $O(n_{\max}^2)$ for a horizon $n_{\max}$, since after $n$ flips only the number of heads matters.

## Properties

- **Exact one-sided guarantees.** The bounds of fact 2 hold for every pair $f_0, f_1$ and need no approximation. The nominal $\alpha$ and $\beta$ themselves are not guaranteed: in the worst case $\alpha'$ can reach $\alpha/(1 - \beta)$.
- **Conservative in practice.** The overshoot makes $\alpha'$ and $\beta'$ smaller than $\alpha$ and $\beta$ for most models, as in both examples.
- **Valid under optional stopping for $H_0$.** Since $e^{\Lambda_n}$ is a test martingale under $H_0$, stopping the test early, or ignoring the lower threshold, keeps the type I error at most $1/A$.
- **Unbounded sample size.** $N$ has no deterministic upper bound, although $P(N > n)$ decays exponentially.
- **Sensitive to the alternative.** If the truth is neither $f_0$ nor $f_1$, the walk may have drift near 0, and $E[N]$ is then largest.

## Variants and improvements

- **Composite hypotheses with an indifference zone.** For a one-parameter family with monotone likelihood ratio, the SPRT of $\theta_0$ against $\theta_1 > \theta_0$ is used to test $\theta \le \theta_0$ against $\theta \ge \theta_1$. Its rejection probability, the operating characteristic, is monotone in $\theta$, so the error bounds at $\theta_0$ and $\theta_1$ hold over each side.
- **Truncated SPRT.** Stop at a maximum $n_{\max}$ and decide by the sign of $\Lambda$ there. The error rates change slightly; the dynamic program of the example computes them exactly for discrete data.
- **Mixture SPRT.** Replace $f_1$ by a mixture over a range of alternatives, and drop the lower threshold. The result is the [mixture SPRT](/mixture-sequential-probability-ratio-test/), which tests a point null against a composite alternative and gives always valid p-values.
- **CUSUM.** Running an SPRT with lower threshold 0 and restarting it each time it accepts gives Page's [CUSUM](/cusum/) procedure for detecting a change from $f_0$ to $f_1$.
- **Grouped data.** When observations arrive in batches and can be analysed only a few times, a [group sequential design](/group-sequential-design/) replaces the continuous boundary.
- **Applications.** [Statistical model checking](/statistical-model-checking/) runs an SPRT on simulation outcomes, and radar and communication receivers use it for [signal detection](/signal-detection/).

## When to use it

Use the SPRT when observations arrive one at a time, each one has a cost, and the question is a choice between two well-defined hypotheses, or two points that bound an indifference zone: acceptance sampling, model checking by simulation, and quick screening decisions. Use a fixed-sample test when the data come in one batch or when an unbiased estimate of the effect size matters more than the number of observations. Use the mixture SPRT or a [confidence sequence](/confidence-sequence/) when the alternative is not a single point.

## Pitfalls

- **Wrong alternative.** The thresholds give guarantees only at $f_0$ and $f_1$. If the true effect is half of the planned one, the expected sample size can exceed the fixed-sample size of the planned test.
- **Reading the approximations as bounds.** Wald's average sample numbers ignore the overshoot and are too small, as the example shows. Compute the exact values by dynamic programming or simulation when they matter.
- **Densities that are not mutually absolutely continuous.** If $f_0(x) = 0 < f_1(x)$, then $\log f_0(x) = -\infty$ and the test must stop at once with rejection. Code that computes the log ratio in floating point must handle this case.
- **Estimation after stopping.** The sample mean at the stopping time is biased, because the test stops when the data look extreme. Do not report it as if $n$ had been fixed.
- **Changing the plan midway.** Changing $f_1$, $\alpha$ or $\beta$ after seeing the data voids the bounds, except for the option to stop early under $H_0$ noted above.

## Implementations

## History

Wald developed the test in 1943, in the Statistical Research Group at Columbia University, for wartime acceptance sampling, and published it in the Annals of Mathematical Statistics in 1945 with the inequalities for $A$ and $B$ and the approximations for the average sample number; his 1947 book Sequential Analysis gives the full theory. Wald and Wolfowitz (1948) proved that the SPRT minimizes the expected sample size under both hypotheses. Siegmund (1985) gives a modern treatment with corrected approximations for the overshoot.

## References
