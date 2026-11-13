---
tag: V25SM3
kind: problem
slug: signal-detection
name: Signal detection
aliases:
- detection in noise
area: graphics-and-signals/signal-processing
level: core
summary: "Decide from noisy data whether a signal is present, trading the probability of a false alarm against the probability of detection; the likelihood ratio test is optimal."
prereqs: [additive-white-gaussian-noise-channel, bayes-theorem]
see_also: [matched-filter, roc-auc, cross-correlation, maximum-likelihood-estimation, confusion-matrix, spectral-estimation, beamforming, template-matching]
sources:
  - paper: doi:10.1098/rsta.1933.0009
    title: Jerzy Neyman and Egon S. Pearson, On the problem of the most efficient tests of statistical hypotheses, Philosophical Transactions of the Royal Society of London, Series A 231, 1933
    locator: pp. 289 to 337 (the most powerful test of a simple hypothesis against a simple alternative)
  - book: isbn:9780135041352
    title: Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume II, Detection Theory, Prentice Hall, 1998
    locator: Chapter 3, Statistical Decision Theory I (Section 3.3, the Neyman-Pearson theorem, Section 3.4, receiver operating characteristics, and Section 3.7, minimum Bayes risk detectors) and Chapter 4, Deterministic Signals (Section 4.3, matched filters)
  - paper: doi:10.1214/aoms/1177731118
    title: Abraham Wald, Sequential tests of statistical hypotheses, The Annals of Mathematical Statistics 16(2), 1945
    locator: pp. 117 to 186 (the sequential probability ratio test, its thresholds and its expected sample size)
  - paper: doi:10.1109/PROC.1967.5573
    title: Harry Urkowitz, Energy detection of unknown deterministic signals, Proceedings of the IEEE 55(4), 1967
    locator: pp. 523 to 531 (the energy detector and its chi-square performance)
---

Signal detection is the problem of deciding, from a record of noisy data, whether a signal is present (hypothesis $H_1$) or the data are noise only (hypothesis $H_0$). Every rule makes two kinds of error. A false alarm declares a signal that is not there, and a miss overlooks one that is. The probability of false alarm $P_{FA}$ and the probability of detection $P_D$ cannot both be improved by moving a threshold. The curve of the best $P_D$ against $P_{FA}$ is the receiver operating characteristic (ROC). The Neyman-Pearson lemma says that the best rule for a fixed $P_{FA}$ compares the likelihood ratio of the data with a threshold. For a known waveform in white Gaussian noise that rule is the [matched filter](/matched-filter/). Detection is the basic task of radar, sonar and digital receivers, and the same theory, under the name hypothesis testing, is a core part of statistics.

## In plain words

You listen to a noisy channel and must say "something is there" or "nothing is there". Noise alone sometimes looks like a signal, and a weak signal sometimes looks like noise, so you will sometimes be wrong. Decide first how often you can afford a false alarm. Then, for each record, compute how much more likely it is under "signal" than under "noise". Say "signal" when that ratio is high enough. No other rule catches more real signals at the same false alarm rate. A stronger signal, or more of it, makes both errors rarer.

## Definition

**Input.** A record $x = (x[0], \dots, x[N-1])$ and two models of it: the density $p_0(x)$ under $H_0$ and $p_1(x)$ under $H_1$. The standard case is $H_0: x[n] = w[n]$ and $H_1: x[n] = s[n] + w[n]$, with noise $w$ and a signal $s$ that is known, known up to some parameters, or random.

**Output.** A decision rule $\delta(x) \in \{0, 1\}$, or a randomized rule $\delta(x) \in [0, 1]$, the probability of deciding $H_1$. Its performance is

$$P_{FA} = \mathbb{E}_0[\delta(x)], \qquad P_D = \mathbb{E}_1[\delta(x)], \qquad P_M = 1 - P_D.$$

**Criteria.** *Neyman-Pearson:* maximize $P_D$ subject to $P_{FA} \le \alpha$. *Bayes:* with prior probabilities $\pi_0, \pi_1$ and costs $C_{ij}$ of deciding $i$ when $j$ is true, minimize the expected cost; with unit costs for errors, minimize the error probability $\pi_0 P_{FA} + \pi_1 P_M$. *Minimax:* minimize the largest expected cost over the priors.

The **likelihood ratio** is $\Lambda(x) = p_1(x)/p_0(x)$, and a **likelihood ratio test** decides $H_1$ when $\Lambda(x) > \eta$. The **ROC** of a family of tests is the set of points $(P_{FA}, P_D)$ they achieve.

## Variants

- **Known signal in white Gaussian noise.** The likelihood ratio reduces to the correlation $\sum_n \overline{s[n]}x[n]$, which is the [matched filter](/matched-filter/). Colored noise with covariance $C$ gives the statistic $s^H C^{-1} x$.
- **Signal with unknown parameters.** Unknown amplitude, phase, arrival time or Doppler shift. The generalized likelihood ratio test (GLRT) replaces the unknowns by their [maximum likelihood](/maximum-likelihood-estimation/) estimates; for an unknown arrival time this is the peak of the [cross-correlation](/cross-correlation/).
- **Random signal.** If $s$ is Gaussian with covariance $C_s$, the optimal statistic is the quadratic form $x^H C_s (C_s + \sigma^2 I)^{-1} x$, the estimator-correlator. If nothing is known except the band, the energy detector $\sum_n |x[n]|^2$ is used.
- **Unknown noise level.** Constant false alarm rate (CFAR) detectors estimate the noise power from nearby cells and scale the threshold, so that $P_{FA}$ stays fixed when the noise changes.
- **Sequential detection.** Samples arrive one at a time, and the rule may stop early. Wald's sequential probability ratio test (SPRT) is optimal in expected sample size.
- **Multiple hypotheses.** Deciding among $M$ signals is classification; in communication, the receiver chooses the symbol with the largest likelihood.
- **Detection with an array.** Several sensors, combined by [beamforming](/beamforming/) before the test, or tested jointly.

## Examples

The Gaussian values below were computed with the `q_function` and `q_inverse` routines on the matched filter page, which evaluate $Q(u) = \Pr(Z > u) = \tfrac12\operatorname{erfc}(u/\sqrt2)$ and invert it by bisection. The simulations used Python's `random.Random` with the seeds given.

- **The signal energy needed.** For a known signal in white Gaussian noise, $P_D = Q(Q^{-1}(P_{FA}) - \sqrt{E/\sigma^2})$. For $P_{FA} = 10^{-3}$ and $P_D = 0.9$: $Q^{-1}(10^{-3}) = 3.0902$ and $Q^{-1}(0.9) = -1.2816$, so $\sqrt{E/\sigma^2} = 4.3718$ and $E/\sigma^2 = 19.11$, which is $12.81$ dB.
- **An ROC.** For $E/\sigma^2 = 10$ (10 dB), the curve passes through these points:

| $P_{FA}$ | $10^{-1}$ | $10^{-2}$ | $10^{-3}$ | $10^{-6}$ |
|---|---|---|---|---|
| $P_D$ | $0.9700$ | $0.7984$ | $0.5287$ | $0.0558$ |

The area under it is $Q(-\sqrt{E/(2\sigma^2)}) = 0.9873$; see [ROC and AUC](/roc-auc/).
- **Bayes with equal priors.** For the same signal, the test that minimizes the error probability compares the correlation with $E/2$, and its error probability is $Q(\sqrt{E}/(2\sigma)) = 0.0569$.
- **Known against unknown shape.** A constant signal of energy $10$ spread over $N = 16$ samples, with $\sigma^2 = 1$ and $P_{FA} = 0.01$. The matched filter gives $P_D = 0.798$. The energy detector, which does not use the shape, with the exact threshold $31.9999$ of the chi-square distribution with 16 degrees of freedom, gave a measured $P_D = 0.223$ and $P_{FA} = 0.0112$ over 20000 trials each (seed 5201).
- **Sequential against fixed sample size.** Samples $x[n] \sim N(\mu, 1)$ with $\mu = \sqrt{10/16} = 0.79$ under $H_1$ and $N(0, 1)$ under $H_0$, with both error probabilities at $0.01$. A fixed-size test needs $n = (2Q^{-1}(0.01))^2/\mu^2 = 34.6$ samples. The SPRT with thresholds $\pm\ln 99$ on the log likelihood ratio, over 5000 runs per hypothesis (seed 5202), used on average $16.0$ samples under $H_0$ and $16.3$ under $H_1$, with measured $P_{FA} = 0.0064$ and $P_D = 0.9928$. Wald's approximation of the average is $14.4$.

## Known algorithms

- **[Matched filter](/matched-filter/).** Known signal in white noise: correlate and compare with $\sigma\sqrt{E}\,Q^{-1}(P_{FA})$. $\Theta(N)$ per test, $O(M \log N)$ for every shift of a record of length $M$ with the FFT.
- **Generalized matched filter.** Known signal in colored Gaussian noise: whiten and correlate, $s^H C^{-1}x$.
- **Quadrature (envelope) detector.** Known waveform with an unknown phase: compare $|\sum_n \overline{s[n]}x[n]|^2$ with $\sigma^2 E\ln(1/P_{FA})$.
- **GLRT.** Unknown parameters: maximize the likelihood ratio over them, often a bank of matched filters followed by the maximum.
- **Energy detector.** Unknown signal in a known band: compare $\sum|x[n]|^2$ with a chi-square quantile.
- **Estimator-correlator.** Gaussian random signal with a known covariance: estimate the signal by a [Wiener filter](/wiener-filter/) and correlate with the data.
- **Cell-averaging CFAR.** Threshold proportional to the mean power of the reference cells around the test cell.
- **SPRT.** Add the log likelihood ratio sample by sample and stop when it leaves the interval $(\ln\frac{\beta}{1-\alpha}, \ln\frac{1-\beta}{\alpha})$ for target error probabilities $\alpha$ and $\beta$.

## Bounds

**Neyman-Pearson lemma.** Let $\phi^*(x) = 1$ if $p_1(x) > \eta p_0(x)$, $\phi^*(x) = 0$ if $p_1(x) < \eta p_0(x)$, and $\phi^*(x) = \gamma$ on the boundary, with $\eta \ge 0$ and $\gamma \in [0, 1]$ chosen so that $\mathbb{E}_0[\phi^*] = \alpha$. Then every rule $\phi$ with $\mathbb{E}_0[\phi] \le \alpha$ has $\mathbb{E}_1[\phi] \le \mathbb{E}_1[\phi^*]$.

*Proof.* At each $x$, $(\phi^*(x) - \phi(x))(p_1(x) - \eta p_0(x)) \ge 0$. Where $p_1 > \eta p_0$, $\phi^* = 1 \ge \phi$; where $p_1 < \eta p_0$, $\phi^* = 0 \le \phi$; on the boundary the second factor is zero. Integrating over $x$,

$$\mathbb{E}_1[\phi^*] - \mathbb{E}_1[\phi] \ge \eta\,(\mathbb{E}_0[\phi^*] - \mathbb{E}_0[\phi]) \ge \eta(\alpha - \alpha) = 0.$$

The constants exist because $\Pr_0(\Lambda > \eta)$ is nonincreasing and right-continuous in $\eta$; randomization on the boundary fills a jump, and for continuous $\Lambda$ it is not needed. $\blacksquare$

So the ROC of the likelihood ratio tests lies above that of every other rule. It is concave, because randomizing between two tests reaches every point on the segment between them, and it lies above the diagonal $P_D = P_{FA}$, which a coin toss achieves.

**Bayes rule.** The expected cost of $\phi$ is a constant plus $\int \phi(x)\big(\pi_0(C_{10} - C_{00})p_0(x) - \pi_1(C_{01} - C_{11})p_1(x)\big)\,dx$. It is smallest when $\phi = 1$ exactly where the bracket is negative, that is, where $\Lambda(x) > \pi_0(C_{10} - C_{00})/(\pi_1(C_{01} - C_{11}))$. So the Bayes rule is also a likelihood ratio test, and its threshold comes from the priors and the costs, not from $\alpha$.

**Gaussian shift.** If the test statistic is $N(0, 1)$ under $H_0$ and $N(d, 1)$ under $H_1$, with deflection $d = \sqrt{E/\sigma^2}$ for the matched filter, the ROC is $P_D = Q(Q^{-1}(P_{FA}) - d)$. Every point of performance depends on the signal only through its energy.

**Error exponents.** For equal priors, the Bhattacharyya bound gives $P_e \le \tfrac12\int\sqrt{p_0p_1}$, which is $\tfrac12 e^{-E/(8\sigma^2)} = 0.143$ for $E/\sigma^2 = 10$, against the exact $0.0569$. For $N$ independent samples the best error probability decays as $e^{-NC}$, where $C$ is the Chernoff information. In the Neyman-Pearson setting with a fixed $P_{FA}$, the miss probability decays as $e^{-N D(p_0\|p_1)}$, with the Kullback-Leibler divergence (Stein's lemma).

**Sequential tests.** Among all tests with error probabilities at most $\alpha$ and $\beta$, the SPRT minimizes the expected number of samples under both hypotheses (Wald and Wolfowitz).

## Reductions

- **To hypothesis testing.** Detection is a test of two hypotheses about the distribution of the data. The statistic of an optimal test is a sufficient statistic, such as the correlation with the known signal.
- **Known signal to correlation.** For Gaussian noise, the log likelihood ratio is linear in the data, so detection reduces to one inner product, a [cross-correlation](/cross-correlation/) at one lag, and to a filter when all lags are tested.
- **Unknown arrival time to estimation.** Testing every shift and taking the maximum is the GLRT, and the position of the maximum is the maximum likelihood estimate of the delay.
- **To binary classification.** With labeled examples instead of known densities, detection becomes classification, and its errors are those of a [confusion matrix](/confusion-matrix/); the ROC and its area are used in both fields.
- **Spectral lines.** Detecting a tone of unknown frequency in white noise is a GLRT whose statistic is the largest peak of the [periodogram](/periodogram/), which connects detection to [spectral estimation](/spectral-estimation/).

## Applications

- **Radar and sonar.** Detect echoes in each range and Doppler cell, with CFAR thresholds, after pulse compression by matched filters.
- **Digital communication.** Detect the start of a frame, decide each symbol, and sense whether a radio channel is in use.
- **Gravitational wave astronomy.** Banks of matched filters search the detector data for the waveforms of merging compact binaries.
- **Medicine and biology.** Detect spikes in neural recordings, beats in the electrocardiogram and events in imaging.
- **Images.** Find a known pattern by [template matching](/template-matching/) and detect objects against clutter.
- **Fault and change detection.** Sequential tests detect a change in a process as early as possible, at a given rate of false alarms.

## References
