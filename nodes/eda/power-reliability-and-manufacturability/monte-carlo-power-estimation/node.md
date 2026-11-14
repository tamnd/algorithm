---
tag: QFM309
kind: algorithm
slug: monte-carlo-power-estimation
name: Monte Carlo power estimation
aliases:
- Burch-Najm-Yang-Trick estimation
- statistical power estimation
area: eda/power-reliability-and-manufacturability
level: core
summary: Simulates random input samples until a confidence interval on the mean power is tight enough, a stopping rule by Burch, Najm, Yang and Trick.
model: word-ram
complexity:
  vars: {N: the number of samples drawn, T: the number of clock cycles per sample, G: the number of gates, P: the number of gate input pins, n: the number of primary inputs}
  time: {worst: "O(N T (G + P))"}
  space: {extra: "O(G + n)"}
properties: {deterministic: false, exact: false, recursive: false, online: true}
history:
  year: 1992
  people: [Richard Burch, Farid N. Najm, Ping Yang, Timothy N. Trick]
  note: Burch, Najm, Yang and Trick proposed to simulate a circuit with random inputs in independent samples and to stop when a normal-theory confidence interval for the mean power is narrow relative to the mean, first as McPOWER at ICCAD 1992 and then in IEEE Transactions on VLSI Systems in 1993.
prereqs: [central-limit-theorem, confidence-interval, switching-activity]
see_also: [sample-size-determination, welford-algorithm, t-confidence-interval, monte-carlo-integration, transition-density, bdd-switching-activity-estimation, event-driven-logic-simulation, confidence-sequence]
sources:
  - paper: doi:10.1109/92.219908
    title: Richard Burch, Farid N. Najm, Ping Yang and Timothy N. Trick, A Monte Carlo approach for power estimation, IEEE Transactions on VLSI Systems 1(1), 63 to 71, March 1993
    locator: the sampling of the power over random input periods, the normality argument, and the stopping criterion with a minimum number of samples (the exact form of the criterion was not checked against the paper)
  - paper: "Richard Burch, Farid N. Najm, Ping Yang and Timothy N. Trick, McPOWER: a Monte Carlo approach to power estimation, IEEE/ACM International Conference on Computer-Aided Design, 90 to 97, November 1992"
    title: Richard Burch, Farid N. Najm, Ping Yang and Timothy N. Trick, McPOWER, a Monte Carlo approach to power estimation, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design, 90 to 97, November 1992
    locator: the first presentation of the method
  - paper: doi:10.1109/92.335013
    title: Farid N. Najm, A survey of power estimation techniques in VLSI circuits, IEEE Transactions on VLSI Systems 2(4), 446 to 455, December 1994
    locator: the section on statistical techniques
  - paper: "Y. S. Chow and Herbert Robbins, On the asymptotic theory of fixed-width sequential confidence intervals for the mean, Annals of Mathematical Statistics 36(2), 457 to 462, 1965"
    title: Y. S. Chow and Herbert Robbins, On the asymptotic theory of fixed-width sequential confidence intervals for the mean, Annals of Mathematical Statistics 36(2), 457 to 462, 1965
    locator: the asymptotic coverage of a confidence interval whose sample size is chosen by a stopping rule on the sample variance
---

Monte Carlo power estimation finds the average power of a circuit by simulation with random inputs, and decides by itself when to stop. Each sample is the power of the circuit over a short period of simulated clock cycles with random input vectors, and the samples are independent. By the [central limit theorem](/central-limit-theorem/), the mean of $N$ samples is close to normal for large $N$, so after each sample the method computes a [confidence interval](/confidence-interval/) for the mean power. It stops when the half width of the interval is below a fraction $\varepsilon$ of the sample mean, after a minimum number of samples. Burch, Najm, Yang and Trick (1992, 1993) proposed this method. It works with any simulator and any delay model, it handles reconvergent fanout, correlation and glitches as well as the simulator does, and the number of samples depends on the spread of the power, not on the size of the circuit. The result is a statistical statement: with probability about $1 - \alpha$ the true mean is within the interval.

## In plain words

To learn the average power of a chip, run it on random inputs for a short time, measure the power, and do this again and again. Each run gives a number, and the average of the numbers approaches the true average.

The question is when to stop. After each run, look at how much the numbers differ from each other. From that spread and the number of runs, statistics tells how far the current average can be from the true one, with a chosen confidence such as 95 percent.

Stop when that distance is small compared with the average itself, for example under 5 percent. Circuits whose power varies little stop after a few dozen runs.

## The problem

The input is a circuit with a simulator, a random model of its inputs, a period of $T$ clock cycles, a relative error $\varepsilon \in (0, 1)$ and a confidence level $1 - \alpha$. A *sample* is the power over one period: the simulator starts from a random state of the inputs, applies $T$ random input vectors, adds $\frac{1}{2} C_y V_{DD}^2$ for every transition of every node $y$ with load $C_y$, and divides by the period. The samples $E_1, E_2, \ldots$ are independent and have the same law, with an unknown mean $\mu > 0$, the average power, and a finite variance $\sigma^2$. The output is an estimate $\eta$ of $\mu$ with a half width $h$ such that $h < \varepsilon \eta$ and the interval $[\eta - h, \eta + h]$ contains $\mu$ with probability about $1 - \alpha$.

## The algorithm

```pseudo id=main
MONTE-CARLO-POWER(sample, ε, α, N_min, N_max)
L1  z ← the 1 − α/2 quantile of the standard normal law
L2  N ← 0; mean ← 0; M2 ← 0; h ← ∞
L3  repeat
L4      E ← sample()  ▷ simulate one period of T cycles with random inputs
L5      N ← N + 1; δ ← E − mean; mean ← mean + δ / N; M2 ← M2 + δ · (E − mean)
L6      if N ≥ 2 then s ← sqrt(M2 / (N − 1)); h ← z · s / sqrt(N)
L7  until N ≥ N_max or (N ≥ N_min and h < ε · mean)
L8  return mean, h, N
```

Line L5 is [Welford's update](/welford-algorithm/), which keeps the mean and the sum of squared deviations in one pass without loss of precision. Line L7 is the stopping rule. $N_{\min}$, often 30, keeps the rule from stopping on a few samples that happen to agree, and $N_{\max}$ stops the loop when the mean is 0 or the samples vary too much.

## Example

Take a two-bit ripple-carry adder built from two full adders (10 gates: per bit two XOR, two AND and one OR), with unit load on each gate output, $V_{DD} = 1$, and energies in units of $C V_{DD}^2$ per cycle. Each of the five inputs is a two-state Markov chain from cycle to cycle with its own switching probabilities. Enumerating all $4^5$ pairs of consecutive vectors in exact arithmetic gives the true mean: $233/120 \approx 1.942$ per cycle with zero delay, and $5519/2160 \approx 2.555$ per cycle with unit transport delay, where the extra 24 percent is glitches.

One run with $T = 4$, $\varepsilon = 0.1$ and $\alpha = 0.05$ ($z = 1.96$):

| delay model | samples $N$ | estimate $\eta$ | half width $h$ | $h / \eta$ | true mean | covered |
|---|---|---|---|---|---|---|
| zero | 33 | 1.955 | 0.190 | 0.097 | 1.942 | yes |
| transport | 64 | 2.314 | 0.231 | 0.100 | 2.555 | no |

The second run misses: its interval ends at 2.545. A 95 percent interval misses about one run in 20, and this is one of them. Over 300 runs with different seeds and zero delay, the interval contained the true mean in 94.7 percent of the runs, with 30 to 63 samples per run; over 150 runs with transport delay, in 96.0 percent, with 30 to 77 samples. With $T = 1$, single-cycle samples, the runs needed about 149 samples and the coverage fell to 92.0 percent, because one-cycle energies take few values and are far from normal. These are measured frequencies, not proved values.

## Correctness

Three facts hold, with the details in the [full proof](proofs/correctness.md).

**When the interval covers, the relative error is bounded.** At the stop, $h < \varepsilon \eta$. If also $|\eta - \mu| \le h$, then $|\eta - \mu| < \varepsilon \eta$, and since then $\eta < \mu / (1 - \varepsilon)$, the error relative to the true mean is below $\varepsilon / (1 - \varepsilon)$. For $\varepsilon = 0.05$ this is 5.3 percent.

**For a fixed number of samples, the interval has the stated confidence.** If $N$ is fixed and the samples are normal, $(\eta - \mu) / (s / \sqrt{N})$ has the Student $t$ law with $N - 1$ degrees of freedom, so the interval with the $t$ quantile in place of $z$ has coverage exactly $1 - \alpha$; with $z$ the coverage is slightly lower, about 94 percent in place of 95 at $N = 30$ for $\alpha = 0.05$. If the samples are not normal but have finite variance, the coverage tends to $1 - \alpha$ as $N$ grows, by the central limit theorem and the convergence of $s$ to $\sigma$.

**With the stopping rule, the confidence is only asymptotic.** Here $N$ depends on the data, and the coverage is not exactly $1 - \alpha$ even for normal samples. Chow and Robbins (1965) proved that for the analogous rule with a fixed width the coverage tends to $1 - \alpha$ as the width tends to 0; the relative rule behaves the same way when $\mu > 0$. This is cited, not proved here. In practice the coverage is measured, as in the example.

## Complexity

Each sample simulates $T$ cycles, and one zero-delay simulation of a cycle costs $O(G + P)$, so the run costs $O(N T (G + P))$ time and $O(G + n)$ space beyond the circuit. With an event-driven simulator the cost per cycle is proportional to the number of events, which is smaller when activity is low. The number of samples is set by the stopping rule: the rule stops near

$$ N \;\approx\; \left(\frac{z\, \sigma}{\varepsilon\, \mu}\right)^2, $$

the usual [sample size](/sample-size-determination/) for a relative error. It grows as $1 / \varepsilon^2$ and with the square of the coefficient of variation $\sigma / \mu$ of the samples, and it does not depend on the number of gates. Longer periods $T$ lower $\sigma / \mu$ and so lower $N$, at a higher cost per sample.

## Properties

- **Unbiased samples, approximate stop.** Each $E_k$ has mean $\mu$ exactly when the inputs start from their stationary law; the estimate at the stop has a small bias because the stop depends on the data.
- **Any delay model.** The method uses the simulator as a black box. Glitches, real gate delays, and correlated or sequential inputs are handled as well as the simulator handles them.
- **Online.** Samples can be added one at a time, and the run can be paused and resumed, since Welford's update keeps all the state in three numbers.
- **Parallel.** Samples are independent, so they can be run on many machines and the means and variances merged.
- **Statistical guarantee only.** No finite run proves a bound. A miss happens with probability about $\alpha$, and with heavy-tailed or very skewed samples more often.

## Variants and improvements

- **Student $t$ quantile.** Use the $t$ quantile with $N - 1$ degrees of freedom in place of $z$ at line L6, as in a [t confidence interval](/t-confidence-interval/). For $N \ge 30$ the two differ by a few percent.
- **Absolute error for small values.** For the activity of single nodes, a node that rarely switches would need a huge $N$ for a relative error. Najm and his students certified such nodes with an absolute error bound instead, and used the relative rule only above a threshold.
- **Nonparametric stopping.** Methods based on order statistics drop the normal assumption on the samples.
- **Variance reduction.** [Stratified sampling](/stratified-sampling/) of input patterns and [importance sampling](/importance-sampling/) lower $\sigma$ and so $N$.
- **Anytime-valid intervals.** A [confidence sequence](/confidence-sequence/) holds at every $N$ at once, so it allows any stopping rule with an exact guarantee, at the cost of a wider interval.
- **Exact methods.** For small circuits, [BDD-based switching activity estimation](/bdd-switching-activity-estimation/) gives the exact mean under its delay model, and [transition density](/transition-density/) gives a fast approximation without simulation.

## When to use it

Use it for the average power of a large gate-level or transistor-level circuit when the input statistics are known and a stated accuracy is needed, especially when glitches, real delays or correlations make probabilistic methods unreliable. It is the reference method against which faster estimators are checked. Do not use it for the peak power or the worst case: it estimates a mean, and rare high-power vectors barely affect the mean.

## Pitfalls

- **Non-stationary start.** If each sample starts from a fixed state, for example all zeros, the first cycles have a different law and the mean is biased. Start from the stationary law, or discard a warm-up period.
- **Dependent samples.** Consecutive periods of one long simulation are correlated. The interval then is too narrow. Use independent restarts, or batch means with batches long enough.
- **Too short periods.** Samples of one or two cycles take few values and are skewed, so the normal interval covers less than its nominal level, as the example shows.
- **Mean near zero.** The relative rule never stops when $\mu$ is 0 or tiny. Use $N_{\max}$, or an absolute error.
- **Stopping too early.** With $N_{\min}$ too small, a few samples that happen to agree give a small $s$ and an early stop.
- **The input model is part of the answer.** The interval is about the mean under the chosen random inputs. If real workloads differ, the estimate is precise and wrong.

## Implementations

## History

Burch, Najm, Yang and Trick presented McPOWER at ICCAD in 1992 and published the method in the first issue of IEEE Transactions on VLSI Systems in 1993. They argued that the power over a period with random inputs is close to normal, and applied a stopping rule from the normal interval with a minimum number of samples, so that the simulation length follows from the requested accuracy and not from a guess. Najm's 1994 survey set the statistical approach next to the probabilistic ones, and later work extended it to the activity of each node, to sequential circuits and to nonparametric stopping rules. The statistical background, sequential intervals whose sample size depends on the data, goes back to Chow and Robbins (1965).

## References
