---
tag: ST2SET
kind: algorithm
slug: cusum
name: CUSUM
aliases:
- Page's CUSUM
- cumulative sum control chart
area: statistics-and-inference/time-series-and-sequential-analysis
level: core
summary: Page's online detector that sums log likelihood ratios, clips the sum at zero and alarms above a threshold. Lorden proved it asymptotically optimal, Moustakides exactly optimal.
solves: [change-point-detection]
model: real-ram
complexity:
  vars: {n: "the number of observations read before the alarm or the end of the stream"}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: true, recursive: false, optimal_for_lorden_criterion: true}
history:
  year: 1954
  people: [E. S. Page]
  note: Page introduced the cumulative sum scheme for continuous inspection in Biometrika in 1954. Lorden proved its asymptotic optimality in 1971 and Moustakides its exact optimality in 1986.
prereqs: [change-point-detection, sequential-probability-ratio-test]
see_also: [bayesian-online-changepoint-detection, pelt-algorithm, binary-segmentation, exponential-moving-average, kullback-leibler-divergence, martingale, signal-detection, walds-equation]
sources:
  - paper: doi:10.1093/biomet/41.1-2.100
    title: E. S. Page, Continuous inspection schemes, Biometrika 41(1/2) (1954)
    locator: the cumulative sum scheme, its form as a sequence of sequential probability ratio tests, and its average run length
  - paper: doi:10.1214/aoms/1177693055
    title: G. Lorden, Procedures for reacting to a change in distribution, Annals of Mathematical Statistics 42(6) (1971)
    locator: the worst-case delay criterion, the asymptotic lower bound on the delay, and the asymptotic optimality of the CUSUM
  - paper: doi:10.1214/aos/1176350164
    title: George V. Moustakides, Optimal stopping times for detecting changes in distributions, Annals of Statistics 14(4) (1986)
    locator: the proof that the CUSUM minimizes Lorden's worst-case delay among all rules with the same false alarm run length
  - book: isbn:9780387961347
    title: David Siegmund, Sequential Analysis, Tests and Confidence Intervals, Springer, 1985
    locator: Chapter II (cusum tests as repeated sequential probability ratio tests) and the approximations for the average run length
  - paper: doi:10.1214/aos/1176346587
    title: Moshe Pollak, Optimal detection of a change in distribution, Annals of Statistics 13(1) (1985)
    locator: the Shiryaev-Roberts statistic and the conditional average delay criterion
  - book: isbn:9781439838204
    title: Alexander Tartakovsky, Igor Nikiforov and Michèle Basseville, Sequential Analysis, Hypothesis Testing and Changepoint Detection, CRC Press, 2014
    locator: the chapters on quickest change detection, the CUSUM and the Shiryaev-Roberts procedures
---

The CUSUM procedure watches a stream of observations for a change from a known density $f_0$ to a known density $f_1$. It adds the log [likelihood ratio](/likelihood-ratio-test/) $Z_t = \log f_1(x_t) - \log f_0(x_t)$ of each new observation to a running sum, sets the sum back to 0 whenever it goes below 0, and raises an alarm when the sum reaches a threshold $h$. The clipped sum equals the largest log likelihood ratio of "the change happened at time $k$" over all possible $k$, so the procedure is the online form of the maximum likelihood test for a change at an unknown time, and the time of the last reset estimates the change. It costs $O(1)$ time and memory per observation. Page proposed it in 1954 for quality control. Lorden (1971) proved that it is asymptotically optimal for the worst-case detection delay at a given false alarm rate, and Moustakides (1986) proved that it is exactly optimal.

## In plain words

A machine is supposed to fill bottles with one litre. Each bottle that comes out a bit light adds a little to a score; each bottle that comes out a bit heavy takes a little away. The score can never go below zero. While the machine is fine, light and heavy bottles balance, and the score keeps returning to zero. After the machine starts to underfill, the score climbs steadily. When it passes a line you chose, you stop the machine. A high line gives few false stops but a later alarm. A low line gives a quick alarm but more false stops. The last time the score was at zero is a good guess of when the problem started.

## The problem

Observations $x_1, x_2, \ldots$ arrive one at a time. Before an unknown time $\nu$ they are i.i.d. with density $f_0$; from time $\nu$ on they are i.i.d. with density $f_1$, and $\nu = \infty$ means no change. Both densities are known. Find a stopping time $T$, an alarm that may use only $x_1, \ldots, x_T$, such that the false alarm run length $E_\infty[T]$ is at least a given $\gamma$ and the detection delay after a change is small. The usual measure of delay is Lorden's worst case
$$\bar d(T) = \sup_{\nu \ge 1}\operatorname{ess\,sup} E_\nu\bigl[(T - \nu + 1)^+ \mid x_1, \ldots, x_{\nu-1}\bigr].$$
See [change-point detection](/change-point-detection/) for the other formulations.

## The algorithm

```pseudo id=main
CUSUM(z_1, z_2, ..., h)          ▷ z_t = log f_1(x_t) - log f_0(x_t), threshold h > 0
L1  S ← 0, k ← 1, t ← 0
L2  for each new z do
L3      t ← t + 1
L4      S ← S + z
L5      if S ≤ 0 then S ← 0, k ← t + 1        ▷ no evidence of a change up to now
L6      if S ≥ h then return (alarm at t, change estimate k)
L7  return no alarm
```

Line L4 adds the evidence of the new observation. Line L5 drops all evidence when the sum is not positive: a change before time $t + 1$ is then no more likely than no change at all, so the best guess of the change moves to $t + 1$. Line L6 sounds the alarm. The statistic $S_t$ after line L5 satisfies
$$S_t = \max(0, S_{t-1} + Z_t) = \max_{1 \le k \le t+1}\sum_{i=k}^{t} Z_i,$$
where the empty sum for $k = t + 1$ is 0. The sum $\sum_{i=k}^t Z_i$ is the log likelihood ratio of "the change happened at time $k$" against "no change by time $t$". So $S_t$ is the generalized likelihood ratio statistic for a change, and $k$ is a maximizer.

For a shift in a normal mean from $\mu_0$ to $\mu_1$ with variance $\sigma^2$, $Z_t = \frac{\mu_1 - \mu_0}{\sigma^2}\bigl(x_t - \frac{\mu_0 + \mu_1}{2}\bigr)$. Quality control charts often drop the factor and use the reference value $(\mu_0 + \mu_1)/2$ and a threshold on the scale of $x$.

## Example

In-control data are $N(0, 1)$ and the planned shift is to $N(1, 1)$, so $Z_t = x_t - 0.5$. With $h = 2$:

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $x_t$ | 0.3 | $-0.6$ | 0.2 | 1.4 | 0.9 | 1.6 |
| $Z_t$ | $-0.2$ | $-1.1$ | $-0.3$ | 0.9 | 0.4 | 1.1 |
| $S_t$ | 0 | 0 | 0 | 0.9 | 1.3 | 2.4 |
| $k$ | 2 | 3 | 4 | 4 | 4 | 4 |

The alarm sounds at $t = 6$, and the change is estimated to have happened at $k = 4$. Check: the sums $\sum_{i=k}^6 Z_i$ for $k = 1, \ldots, 7$ are 0.8, 1.0, 2.1, 2.4, 1.5, 1.1 and 0, and the largest is 2.4 at $k = 4$.

The threshold sets the trade-off. A Monte Carlo simulation of the average run length to a false alarm, $E_\infty[T]$, and of the average delay when the change is at the start, $E_1[T]$, gave these values:

| $h$ | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| $e^h$, a proved lower bound for $E_\infty[T]$ | 7.39 | 20.1 | 54.6 | 148.4 |
| $E_\infty[T]$, simulated | 37.3 | 121.7 | 330.0 | 913.7 |
| $E_1[T]$, simulated | 4.41 | 6.28 | 8.44 | 10.29 |
| $h / D(f_1 \,\|\, f_0) = 2h$ | 4 | 6 | 8 | 10 |

The false alarm run length grows like $e^h$, and the delay grows like $h$ divided by the [Kullback-Leibler divergence](/kullback-leibler-divergence/) $D(f_1 \,\|\, f_0) = 1/2$. So the delay grows only like the logarithm of the false alarm run length.

## Correctness

The proof is in full below. In outline:

1. **The recursion is the maximum over change times.** By induction on $t$: $\max(0, S_{t-1} + Z_t) = \max\bigl(0, \max_{k \le t}\sum_{i=k}^{t-1} Z_i + Z_t\bigr) = \max_{k \le t+1}\sum_{i=k}^t Z_i$. The variable $k$ is the largest maximizer: it moves to $t + 1$ exactly when every sum ending at $t$ is at most 0.
2. **False alarms.** Let $R_t = \sum_{k=1}^t \prod_{i=k}^t e^{Z_i}$, the Shiryaev-Roberts statistic. Under no change, $R_t - t$ is a [martingale](/martingale/), and at an alarm $R_T \ge e^{S_T} \ge e^h$. Optional stopping and Fatou's lemma give $E_\infty[T] \ge e^h$.
3. **Delay.** If the statistic starts higher, it stays higher at every later time, so the worst case in Lorden's criterion is a change that meets $S = 0$, and $\bar d(T) = E_1[T]$. Since $S_t \ge \sum_{i \le t} Z_i$, the alarm comes no later than the first time the plain sum reaches $h$, and [Wald's equation](/walds-equation/) gives $E_1[T] \le (h + E[\text{overshoot}])/D(f_1 \,\|\, f_0)$.
4. **Optimality.** Lorden (1971) proved that every rule with $E_\infty[T] \ge \gamma$ has $\bar d(T) \ge (1 + o(1))\log\gamma / D(f_1 \,\|\, f_0)$ as $\gamma \to \infty$. By facts 2 and 3, the CUSUM with $h = \log\gamma$ attains this. Moustakides (1986) proved that, with $h$ chosen so that $E_\infty[T] = \gamma$, the CUSUM minimizes $\bar d$ exactly among all rules with $E_\infty[T] \ge \gamma$. These two theorems are cited here, not proved.

## Complexity

Each observation costs one evaluation of $Z_t$, one addition and two comparisons, so $\Theta(n)$ time for $n$ observations and $\Theta(1)$ extra space. Tracking the change estimate $k$ costs nothing extra. The two-sided chart runs two CUSUMs, one for an increase and one for a decrease, and doubles the constant.

## Properties

- **Online and constant memory.** The statistic is a function of the previous statistic and the new observation only.
- **Repeated SPRT.** The CUSUM is a sequence of [SPRTs](/sequential-probability-ratio-test/) of $f_0$ against $f_1$ with lower threshold 0 and upper threshold $h$, restarted at every acceptance of $f_0$. This is Page's original description.
- **Logarithmic delay.** For a false alarm run length $\gamma$ the delay is about $\log\gamma / D(f_1 \,\|\, f_0)$, the best possible to first order.
- **Built-in change estimate.** The time of the last reset is the maximum likelihood estimate of the change time given the alarm.
- **Tuned to one alternative.** The procedure is optimal for the planned $f_1$. For a smaller shift the delay grows, and for a larger one it is not as short as a chart tuned to that shift.

## Variants and improvements

- **Two-sided CUSUM.** Run one chart for an increase and one for a decrease, and alarm when either crosses.
- **Tabular CUSUM with a reference value.** In quality control the increment is $x_t - \mu_0 - K$ with $K$ half the shift to detect, and the threshold $H$ is in units of $x$. This is the same chart with $Z_t$ scaled.
- **Unknown post-change parameter.** The generalized likelihood ratio procedure maximizes over the post-change parameter as well as over $k$. It is not recursive and costs more per step, unless the window of $k$ is limited. A mixture over the post-change parameter gives a statistic in the spirit of the [mixture SPRT](/mixture-sequential-probability-ratio-test/).
- **Shiryaev-Roberts procedure.** Replace the maximum over $k$ by the sum, $R_t = (1 + R_{t-1})e^{Z_t}$. It is optimal in a Bayesian limit and nearly optimal for Pollak's criterion (Pollak 1985).
- **Bayesian detection.** With a prior on the change time, and possibly several changes, [Bayesian online changepoint detection](/bayesian-online-changepoint-detection/) computes the posterior of the time since the last change.
- **Smoothing charts.** The EWMA chart, based on an [exponential moving average](/exponential-moving-average/), weighs recent data more. It detects small shifts about as fast but has no likelihood interpretation.
- **Offline segmentation.** When the whole series is available and there may be many changes, use [PELT](/pelt-algorithm/) or [binary segmentation](/binary-segmentation/).

## When to use it

Use the CUSUM when observations arrive online, the in-control law is known or well estimated, and there is a specific change worth detecting, such as a planned shift in the mean of a process. It is the standard tool for statistical process control of small persistent shifts, and it is used in [signal detection](/signal-detection/) and in surveillance of health outcomes. Use the Bayesian detector when there are many changes and unknown parameters, and an offline method when the whole series is available.

## Pitfalls

- **Wrong pre-change model.** The false alarm run length depends strongly on $f_0$. If the in-control variance is underestimated, false alarms come far sooner than planned.
- **Dependent data.** Autocorrelation in the in-control data makes $S_t$ drift up more often and shortens the false alarm run length. Fit a time series model and monitor its residuals instead.
- **Reading $e^h$ as the run length.** It is only a lower bound. In the example, $E_\infty[T]$ is about 5 to 6 times $e^h$. Compute the run length by simulation, by a Markov chain approximation, or from tables, and set $h$ from it.
- **Not resetting after an alarm.** After an alarm and a repair the chart should restart at 0; otherwise the old evidence triggers a second alarm at once.
- **Estimated parameters treated as known.** A chart built from a short phase I sample has a random false alarm run length, often much shorter than the nominal one.

## Implementations

## History

Page (1954) introduced the cumulative sum scheme for continuous inspection of a production process and described it as a sequence of Wald's sequential tests. Lorden (1971) defined the worst-case delay criterion, proved a lower bound for all procedures, and showed that the CUSUM attains it asymptotically as the false alarm run length grows. Moustakides (1986) proved that the CUSUM is exactly optimal for Lorden's criterion. Pollak (1985) studied the Shiryaev-Roberts procedure under a related criterion. Siegmund (1985) gives approximations for the run lengths.

## References
