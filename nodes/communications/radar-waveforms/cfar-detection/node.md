---
tag: KZD5VM
kind: problem
slug: cfar-detection
name: CFAR detection
aliases:
- constant false alarm rate detection
area: communications/radar-waveforms
level: core
summary: "Decide target or no target in each radar cell with a threshold set from the data, so that the false alarm probability stays fixed when the noise power is unknown."
model: real-ram
complexity:
  vars: {n: the number of cells along range, N: the number of reference cells}
  time: {worst: Θ(n)}
prereqs: [signal-detection, neyman-pearson-lemma]
see_also: [cell-averaging-cfar, ordered-statistic-cfar, swerling-target-models, albersheim-equation, likelihood-ratio-test, energy-detector, spectrum-sensing, range-doppler-processing]
sources:
  - paper: "H. M. Finn and R. S. Johnson, RCA Review 29(3), 1968, pp. 414 to 464"
    title: Adaptive detection mode with threshold control as a function of spatially sampled clutter-level estimates
    locator: "the whole paper (the threshold set from the mean of nearby range cells, and its loss against a fixed threshold)"
  - paper: "P. P. Gandhi and S. A. Kassam, IEEE Transactions on Aerospace and Electronic Systems 24(4), 1988, pp. 427 to 445"
    title: Analysis of CFAR processors in nonhomogeneous background
    locator: "the whole paper (CA, GO, SO and OS processors at clutter edges and with interfering targets)"
  - paper: "P. P. Gandhi and S. A. Kassam, IEEE Transactions on Information Theory 40(4), 1994, pp. 1226 to 1228"
    title: Optimality of the cell averaging CFAR detector
    locator: "the whole paper (CA-CFAR is a uniformly most powerful CFAR detector for a Swerling 1 target in exponential noise of unknown power)"
  - book: isbn:9780071444743
    title: "Mark A. Richards, Fundamentals of Radar Signal Processing, McGraw-Hill, 2005"
    locator: "Chapter 7, Constant False Alarm Rate (CFAR) Detection, Sections 7.1 to 7.3 (the effect of an unknown interference power and cell averaging) and 7.6 (order statistics)"
  - book: isbn:9780072881387
    title: "Merrill I. Skolnik, Introduction to Radar Systems, third edition, McGraw-Hill, 2001"
    locator: "Chapter 5, Detection of Signals in Noise (the threshold, false alarms and constant false alarm rate receivers)"
---

CFAR detection is the problem of deciding, for each cell of a radar's output, whether a target is present, when the power of the noise and clutter is not known and changes from place to place. A fixed threshold cannot work in that case: if the noise rises by 3 dB, a threshold set for one false alarm per second gives many per second. A CFAR detector sets the threshold of each cell from the data around it, so that the false alarm probability $P_{fa}$ stays at its design value for every noise power. The price is the CFAR loss, a small increase in the signal to noise ratio needed for the same probability of detection.

## In plain words

A radar measures the power that comes back from each range. Most cells hold only noise, and a few hold a target. You decide "target" when the power is high. "High" must be relative to the noise, and the noise level is unknown. So you look at the cells next to the one you test, estimate the noise from them, and call the cell a target when its power is some fixed multiple of that estimate. If all powers double, the decision does not change. This keeps the rate of false alarms constant. It costs a little sensitivity, because the noise estimate is itself noisy.

## Definition

The input is a sequence $x[0], \dots, x[n-1]$ of nonnegative powers, one per cell, from a square-law detector $x = |r|^2$ of complex baseband samples $r$, together with a design value $P_{fa} \in (0, 1)$. The standard model is the homogeneous one: under the hypothesis $H_0$ (no target in cell $i$), $x[i]$ is exponential with an unknown mean $\mu > 0$, the noise power. Under $H_1$, the cell also holds a target, for example a Swerling 1 target, which makes $x[i]$ exponential with mean $\mu(1 + S)$ for the signal to noise ratio $S$. The cells near cell $i$ (the reference cells) hold noise of the same mean and are independent.

The output is a decision $d_i \in \{0, 1\}$ for each cell. The requirement is the constant false alarm rate:

$$P(d_i = 1 \mid H_0, \mu) = P_{fa} \quad \text{for every } \mu > 0,$$

and, among the rules that meet it, the probability of detection $P(d_i = 1 \mid H_1)$ should be as large as possible. With a known $\mu$, the [Neyman-Pearson lemma](/neyman-pearson-lemma/) gives the fixed threshold $x[i] > \mu \ln(1/P_{fa})$. With an unknown $\mu$, that threshold cannot be computed, and a threshold of the form $x[i] > T \cdot g(\text{reference cells})$, with $g$ homogeneous of degree 1, is used instead. Such a rule does not change when all cells are multiplied by the same constant, so its false alarm probability does not depend on $\mu$.

## Variants

- **Cell averaging (CA).** $g$ is the sum of $N$ reference cells, split into a leading and a lagging half, with guard cells around the cell under test. See [cell-averaging CFAR](/cell-averaging-cfar/).
- **Greatest of (GO) and smallest of (SO).** $g$ is the larger or the smaller of the two half sums. GO controls false alarms at a clutter edge, and SO resolves two close targets.
- **Ordered statistic (OS).** $g$ is the $k$-th smallest reference value. It resists interfering targets in the window. See [ordered-statistic CFAR](/ordered-statistic-cfar/).
- **Two-dimensional CFAR.** The reference cells surround the cell under test on the output of [range-Doppler processing](/range-doppler-processing/) or an image.
- **Non-exponential clutter.** For Weibull, log-normal or K-distributed clutter, the shape of the distribution is also unknown, and a scale-invariant rule alone does not fix $P_{fa}$.
- **Several pulses.** The cells are the sums of $M$ pulses (noncoherent integration). The noise is then gamma distributed, and the threshold factor changes.

## Examples

**CA-CFAR at $N = 16$ and $P_{fa} = 10^{-6}$.** In the homogeneous model, CA-CFAR gives $P_{fa} = (1 + \tau)^{-N}$ for the factor $\tau$ on the sum. So $\tau = (10^{-6})^{-1/16} - 1 = 1.37137$, which is $\alpha = N\tau = 21.94$ times the mean of the reference cells. A known noise power would need only $\ln(10^6) = 13.82$ times the noise power. For a Swerling 1 target and $P_d = 0.9$, the fixed threshold needs $S = 21.14$ dB, and CA-CFAR needs 23.15 dB: a CFAR loss of 2.01 dB (closed form under the model, computed from $P_d = (1 + \tau/(1+S))^{-N}$).

**A small window.** Take $x = (3, 1, 2, 2, 1, 30, 9, 2, 1, 3, 2, 1, 2)$, $N = 4$ reference cells, one guard cell on each side and $P_{fa} = 10^{-2}$, so $\tau = 2.16228$. At cell 5 (the value 30), the reference cells are 2, 2, 2 and 1, the sum is 7 and the threshold is 15.14, so cell 5 is a target. At cell 6 (the value 9), the reference cells are 2, 1, 1 and 3, the threshold is again 15.14, and cell 6 is not a target. The [cell-averaging CFAR](/cell-averaging-cfar/) page gives the full trace.

**Doubling the noise.** Multiply every cell above by 2. Every sum and every threshold doubles, and the decisions are the same. This is the CFAR property in its simplest form.

## Known algorithms

- [Cell-averaging CFAR](/cell-averaging-cfar/): a running sum, $O(1)$ per cell after the first window, so $\Theta(n)$ for $n$ cells. Best in homogeneous noise.
- [Ordered-statistic CFAR](/ordered-statistic-cfar/): a selection of the $k$-th smallest value in a sliding window. $\Theta(nN)$ with a sorted list, $O(n \log N)$ with a [balanced binary search tree](/balanced-binary-search-tree/) or an [order statistic tree](/order-statistic-tree/).
- GO and SO CFAR: two running sums, $\Theta(n)$.
- In spectrum sensing, the [energy detector](/energy-detector/) with a noise estimate is the same idea in frequency.

## Bounds

- **The ideal detector.** No rule beats the Neyman-Pearson test with a known $\mu$. For a Swerling 1 target it gives $P_d = P_{fa}^{1/(1+S)}$, an upper bound for every CFAR rule.
- **CA-CFAR approaches the bound.** With $(1 + \tau)^N = 1/P_{fa}$, $\tau \to 0$ and $N\tau \to \ln(1/P_{fa})$ as $N \to \infty$, so $P_d = (1 + \tau/(1+S))^{-N} \to P_{fa}^{1/(1+S)}$. The CFAR loss falls as $N$ grows: at $P_{fa} = 10^{-6}$ the average threshold is 4.28 dB above the ideal one for $N = 8$, 0.97 dB for $N = 32$ and 0.48 dB for $N = 64$.
- **Optimality.** For a Swerling 1 target in homogeneous exponential noise of unknown power, Gandhi and Kassam (1994) proved that CA-CFAR is a uniformly most powerful CFAR detector. No other CFAR rule, OS included, has a higher $P_d$ in this model. The other rules give up some $P_d$ here in exchange for robustness outside the model.
- **Time.** Each cell must be read, so $\Omega(n)$ time is needed, and CA-CFAR meets it.

## Reductions

- **To a hypothesis test on invariants.** Divide every cell by the sum of the reference cells. The ratios do not depend on $\mu$, and a [likelihood ratio test](/likelihood-ratio-test/) on them has a constant false alarm rate. For the Swerling 1 target this test is CA-CFAR.
- **From spectrum sensing.** Deciding whether a band is occupied when the noise floor is unknown is the same problem on frequency bins in place of range cells. See [spectrum sensing](/spectrum-sensing/).

## Applications

Every search and surveillance radar uses some form of CFAR after the detector, often on the output of [range-Doppler processing](/range-doppler-processing/). Automotive radars use CA and OS CFAR on each frame. Sonar, lidar, and the detection of signals in a spectrum use the same rules. The detection probability that the [Albersheim equation](/albersheim-equation/) or the [Swerling models](/swerling-target-models/) give assumes a fixed threshold; with CFAR, add the CFAR loss.

## References
