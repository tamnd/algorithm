---
tag: GD7TNS
kind: problem
slug: spectrum-sensing
name: Spectrum sensing
aliases:
- cognitive radio sensing
area: communications/link-adaptation-and-resource-allocation
level: core
summary: Decide whether a primary user occupies a band, so that a cognitive radio can use the band when it is free.
prereqs: [signal-detection, neyman-pearson-lemma]
see_also: [energy-detector, cyclostationary-feature-detection, signal-detection, neyman-pearson-lemma, likelihood-ratio-test, cfar-detection, matched-filter, power-spectral-density]
sources:
  - paper: doi:10.1109/SURV.2009.090109
    title: "Tevfik Yücek and Hüseyin Arslan, A survey of spectrum sensing algorithms for cognitive radio applications, IEEE Communications Surveys and Tutorials 11(1), 2009, pages 116 to 130"
    locator: "the hypothesis test of sensing, the comparison of energy, matched filter, cyclostationary and waveform-based detectors, cooperative sensing, and the hidden terminal problem"
  - paper: doi:10.1109/JSTSP.2007.914879
    title: "Rahul Tandra and Anant Sahai, SNR walls for signal detection, IEEE Journal of Selected Topics in Signal Processing 2(1), 2008, pages 4 to 17"
    locator: "the noise uncertainty model, the SNR wall of the radiometer, and the walls of detectors that use known features of the signal"
  - book: isbn:9780135041352
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume II: Detection Theory, Prentice Hall, 1998"
    locator: "Chapter 3 (Neyman-Pearson detection), Chapter 5 (random signals and the energy detector), Chapter 6 (composite hypothesis testing and the generalized likelihood ratio test) and Chapter 9 (unknown noise parameters)"
---

Spectrum sensing is the problem of deciding, from a short record of received samples, whether a band is in use by its licensed (primary) user, so that an unlicensed (secondary) cognitive radio may send in it only when it is free. It is a binary [hypothesis test](/signal-detection/): under $H_0$ the samples are noise, and under $H_1$ they are a primary signal, faded and often far below the noise, plus noise. A sensor is judged by its probability of detection $P_d$, which protects the primary user, and its probability of false alarm $P_{fa}$, which wastes free spectrum. When the signal is known exactly, the [Neyman-Pearson](/neyman-pearson-lemma/) best test is the [matched filter](/matched-filter/). With nothing known but the noise power, the [energy detector](/energy-detector/) is the standard choice. With known features of the modulation, [cyclostationary feature detection](/cyclostationary-feature-detection/) separates signal from noise. Sensing is hard because of three limits: very low SNR, fading that hides the primary signal from one sensor, and uncertainty in the noise power, which creates an SNR wall below which no number of samples is enough for an energy detector.

## In plain words

Some radio bands belong to a licensed user, such as a TV station, but are often idle in a given place and time. A second radio may use such a band, but only if it does not disturb the owner. So before it sends, it listens and decides: is someone using this band now, or not? It may miss a weak owner and cause harm, or it may think the band is busy when it is not and waste a chance. The owner's signal can be much weaker than the noise, and the second radio may not know the exact noise level. Listening longer helps, and several radios listening together help more, but some limits remain.

## Definition

**Model.** The sensor takes $N$ complex baseband samples

$$H_0 : y[n] = w[n], \qquad H_1 : y[n] = s[n] + w[n], \qquad n = 0, \ldots, N - 1,$$

where $w[n]$ is noise, usually $\mathcal{CN}(0, \sigma^2)$ and white, and $s[n]$ is the received primary signal, with power $P_s$ and SNR $= P_s / \sigma^2$.

**Output.** A decision $\delta(y) \in \{0, 1\}$.

**Goal.** For a target false alarm rate $\alpha$, keep $P_{fa} = \Pr[\delta = 1 \mid H_0] \le \alpha$ and make $P_d = \Pr[\delta = 1 \mid H_1]$ as large as possible, or reach a target $P_d$ with the fewest samples. In cognitive radio standards both are fixed; for example, $P_d \ge 0.9$ and $P_{fa} \le 0.1$ at a stated SNR.

**What is known.** The variants differ in what the sensor knows about $s$ and $\sigma^2$: the full waveform, a pilot or a cyclic feature, the power spectrum shape, or nothing; and the noise power exactly, within a range, or not at all.

## Variants

- **Known signal.** If $s$ is known, for example a pilot, the [likelihood ratio test](/likelihood-ratio-test/) is the matched filter, and the needed $N$ grows like $1/\mathrm{SNR}$.
- **Unknown signal, known noise power.** The energy detector compares $\sum |y[n]|^2$ with a threshold; it is the generalized likelihood ratio test for an unknown deterministic signal and the best test for a white Gaussian signal. The needed $N$ grows like $1/\mathrm{SNR}^2$.
- **Unknown noise power.** If $\sigma^2$ is known only within a factor $\rho$, tests that use only the energy have an SNR wall. Tests that estimate the noise from the data, from features the noise lacks, or from bands known to be empty avoid or move the wall.
- **Wideband sensing.** Decide for each of many subbands at once, from one wideband record; the [periodogram](/periodogram/) or a filter bank gives an energy test per subband.
- **Cooperative sensing.** Several sensors at different places combine their decisions or statistics, so that one sensor in a fade does not miss the primary user.
- **Sequential sensing.** Take samples until the evidence is strong enough, as in the [sequential probability ratio test](/sequential-probability-ratio-test/), which needs fewer samples on average.
- **Sensing and access.** A radio that senses for a time $\tau$ out of a frame $T$ trades sensing accuracy against the time left to send; the best $\tau$ maximizes the secondary throughput subject to $P_d$.

## Examples

**Samples needed.** For the energy detector with a complex Gaussian primary signal and $P_{fa} = 0.1$, $P_d = 0.9$, the normal approximation gives $N \approx \big(Q^{-1}(P_{fa}) - (1 + \mathrm{SNR})\, Q^{-1}(P_d)\big)^2 / \mathrm{SNR}^2$. This is $89$ samples at $-5$ dB, $725$ at $-10$ dB, $6{,}779$ at $-15$ dB and $66{,}354$ at $-20$ dB: about ten times more samples for each $5$ dB, and nearly $100$ times more for each $10$ dB. With the exact threshold, these numbers give $P_d = 0.904$, $0.9004$, $0.90003$ and $0.900004$.

**The SNR wall.** If the true noise power is anywhere in $[\sigma^2/\rho, \rho \sigma^2]$, the energy detector must set its threshold for the worst noise $\rho\sigma^2$, and a signal can be seen only if $P_s + \sigma^2/\rho > \rho\sigma^2$, that is, $\mathrm{SNR} > \rho - 1/\rho$. For an uncertainty of $0.1$, $0.5$, $1$ and $2$ dB, the wall is at $-13.4$, $-6.4$, $-3.3$ and $-0.2$ dB. Below the wall, no number of samples meets both targets.

**Cooperation.** Five sensors each detect with $P_d = 0.6$ at $P_{fa} = 0.02$, with independent fading. If the fusion center declares the band busy when any sensor does (the OR rule), $P_d = 1 - 0.4^5 = 0.990$ and $P_{fa} = 1 - 0.98^5 = 0.096$.

## Known algorithms

- **[Energy detector](/energy-detector/)** (radiometer). Needs only the noise power; cost $O(N)$; sensitive to noise uncertainty.
- **[Matched filter](/matched-filter/).** Correlate with a known pilot or preamble; needs the waveform and timing; best when they are known.
- **[Cyclostationary feature detection](/cyclostationary-feature-detection/).** Test for the cyclic autocorrelation at a cyclic frequency of the primary signal, such as its symbol rate or twice its carrier; noise has none, so the test works with unknown noise power, at a higher cost.
- **Eigenvalue tests.** With several antennas or oversampling, compare the largest and smallest eigenvalues of the sample covariance; the ratio does not depend on the noise power.
- **Waveform and pilot tests.** Detect a known pilot tone, preamble or synchronization pattern of the primary system.
- **Cooperative fusion.** Combine one-bit decisions by an OR, AND or $k$-out-of-$M$ rule, or combine the statistics with weights.
- **Databases.** Instead of sensing, look up a database of primary transmitters by location; regulators allowed this for TV white spaces.

## Bounds

- **Neyman-Pearson.** For simple hypotheses, the likelihood ratio test has the largest $P_d$ at each $P_{fa}$; every other detector is bounded by it.
- **Sample count.** For a known signal, the matched filter needs $N = O(1/\mathrm{SNR})$; for an unknown white signal the energy detector needs $N = O(1/\mathrm{SNR}^2)$.
- **SNR walls.** With noise power known only within a factor $\rho$, the radiometer cannot meet any targets $P_d > P_{fa}$ below $\mathrm{SNR} = \rho - 1/\rho$ (Tandra and Sahai, 2008). Detectors that use features of the signal have lower walls, set by how well the features are known and how stable the channel is.
- **Hidden terminal.** A secondary radio in a deep fade or behind a building can see no primary signal while the primary receiver nearby is disturbed. No single-sensor test fixes this; it is the reason for cooperation and databases.

## Reductions

- **To hypothesis testing.** Sensing one band is a binary test, so the theory of [signal detection](/signal-detection/) gives the best tests and their performance.
- **To CFAR detection.** When the noise power must be estimated from reference cells, the test is a [CFAR detector](/cfar-detection/) as in radar, and the noise estimate fixes the false alarm rate.
- **To spectral estimation.** Wideband sensing reduces to estimating the [power spectral density](/power-spectral-density/) and testing each subband.

## Applications

- **TV white spaces.** IEEE 802.22 regional networks and other white space devices use the idle TV channels of a place.
- **Shared bands.** Radar bands shared with commercial use, such as the US citizens broadband radio service, use sensors to protect the incumbent.
- **Listen before talk.** Wi-Fi and LTE in unlicensed bands sense the channel before each transmission, with an energy threshold.
- **Spectrum monitoring.** Regulators and operators measure occupancy and find interference with the same detectors.

## References
