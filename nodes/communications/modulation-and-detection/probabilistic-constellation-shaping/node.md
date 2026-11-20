---
tag: S1G9VP
kind: technique
slug: probabilistic-constellation-shaping
name: Probabilistic constellation shaping
aliases:
- probabilistic amplitude shaping
- PAS
area: communications/modulation-and-detection
level: research
summary: Sends inner constellation points more often than outer ones, close to a Gaussian input, to close the shaping gap to capacity.
prereqs: [pulse-amplitude-modulation, channel-capacity, shannon-entropy, bit-interleaved-coded-modulation]
see_also: [constant-composition-distribution-matching, bit-interleaved-coded-modulation, soft-demapping, ldpc-code, multilevel-coding, arithmetic-coding, shannon-hartley-theorem, link-adaptation]
sources:
  - paper: doi:10.1109/18.256499
    title: Frank R. Kschischang and Subbarayan Pasupathy, Optimal nonuniform signaling for Gaussian channels, IEEE Transactions on Information Theory 39(3), 913-929, 1993
    locator: the Maxwell-Boltzmann distributions on a constellation and their shaping gain
  - paper: doi:10.1109/TCOMM.2015.2494016
    title: Georg Böcherer, Fabian Steiner and Patrick Schulte, Bandwidth efficient and rate-matched low-density parity-check coded modulation, IEEE Transactions on Communications 63(12), 4651-4665, 2015
    locator: probabilistic amplitude shaping with a distribution matcher and a systematic binary LDPC code, and rate matching by changing the distribution
  - paper: doi:10.1109/TIT.2015.2499181
    title: Patrick Schulte and Georg Böcherer, Constant composition distribution matching, IEEE Transactions on Information Theory 62(1), 430-434, 2016
    locator: the distribution matcher used to produce the shaped amplitudes
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 12 (maximum entropy distributions)
---

Probabilistic constellation shaping sends the points of a fixed constellation with unequal probabilities: points of low energy often, points of high energy rarely. On the AWGN channel the best input is Gaussian, and a uniform choice of points on a square grid wastes up to $\pi e/6$, that is $1.53$ dB, of power at high SNR. Shaping the probabilities to a sampled Gaussian, the Maxwell-Boltzmann distribution, recovers most of this gap with the same constellation and the same receiver structure. The practical form is probabilistic amplitude shaping (PAS), due to Böcherer, Steiner and Schulte in 2015: a distribution matcher such as [CCDM](/constant-composition-distribution-matching/) produces the amplitudes with the wanted distribution, and a systematic binary code adds the signs from its parity bits. Changing the distribution also changes the rate in fine steps with one code, which gives rate adaptation for free.

## In plain words

Points near the center of a constellation cost little energy; points at the edge cost a lot. If all points are used equally often, the average energy is high for the number of bits sent. Shaping uses the cheap points more often and the expensive ones less often. Each symbol then carries a little less information, but the energy drops by more, so at the same energy a stronger code can be used. A special encoder turns the incoming bits into a stream of amplitudes with the right frequencies, and the error-correcting code adds the signs. The receiver decodes as usual and then turns the amplitudes back into bits.

## When it applies

- The channel is close to AWGN, or the receiver has good channel state, so the Gaussian input is the target. On the optical fiber channel the same idea applies with some care for nonlinear effects.
- The constellation is large enough for shaping to matter: 8-ASK, 64-QAM and more. For QPSK all points have the same energy and there is nothing to shape.
- The binary code is systematic, so that its information bits can be the amplitude labels and its parity bits the signs, as in PAS with [LDPC codes](/ldpc-code/).
- The block is long enough that the rate loss of the distribution matcher is small, hundreds of symbols or more for CCDM.

## The template

1. **Choose the distribution.** For an ASK constellation $\mathcal{X} = \{\pm 1, \pm 3, \ldots, \pm(2^m - 1)\}$ (in raw units), use the Maxwell-Boltzmann distribution
$$P_\nu(x) = \frac{e^{-\nu x^2}}{\sum_{x' \in \mathcal{X}} e^{-\nu x'^2}}, \qquad \nu \ge 0.$$
Among all distributions on $\mathcal{X}$ with a given average energy, it has the largest entropy. For QAM, use it on each axis.
2. **Pick $\nu$ for the target.** For a given SNR, choose $\nu$ (and the scale of the constellation, so that the average energy meets the power constraint) to maximize $I(X; Y)$, or to reach a target rate at the lowest SNR.
3. **Split amplitude and sign.** $P_\nu$ is symmetric, so $X = S \cdot A$ with a uniform sign $S$ independent of the amplitude $A \in \{1, 3, \ldots, 2^m - 1\}$, and $H(X) = H(A) + 1$.
4. **Match the amplitudes.** A distribution matcher maps $k$ uniform bits to $n$ amplitudes with frequencies close to $P_A$.
5. **Encode.** A systematic binary code of rate $c$ takes the $(m - 1)$ label bits of each amplitude, plus $\gamma$ extra uniform bits per symbol, as information bits, and its parity bits become the remaining signs. The parity fits into the signs when $(1 - c)m \le 1$. The transmission rate is
$$R = H(A) + \gamma = H(A) + 1 - (1 - c)m$$
bits per real dimension, with $\gamma = 1 - (1 - c)m$, ignoring the rate loss of the matcher.
6. **Decode.** Demap with the nonuniform priors $P_A$ in the [soft demapper](/soft-demapping/), decode the binary code, and invert the matcher on the decoded amplitudes.

The upper limit of the gain comes from a high-SNR comparison: a uniform distribution on an interval needs $\pi e/6 = 1.4233$ times, or $1.53$ dB, more power than a Gaussian with the same differential entropy.

## Classic examples

**8-ASK at 2 bits per dimension.** Uniform 8-ASK reaches $I(X; Y) = 2$ bits at an SNR of $12.62$ dB; the Shannon limit $\frac12\log_2(1 + \mathrm{SNR}) = 2$ needs $11.76$ dB. With the Maxwell-Boltzmann distribution and $\nu = 0.0505$, 8-ASK reaches $2$ bits at $11.84$ dB, a gain of $0.78$ dB, only $0.08$ dB from the limit. The probabilities are

| amplitude | 1 | 3 | 5 | 7 |
|---|---|---|---|---|
| probability of $+a$ (and of $-a$) | 0.2434 | 0.1625 | 0.0725 | 0.0216 |

The entropy is $H(X) = 2.632$ bits, and the average energy is $9.15$ in raw units, against $21$ for uniform 8-ASK. In PAS with $H(A) = 1.632$, the rate $R = 2$ needs a code of rate $c$ with $1.632 + 1 - 3(1 - c) = 2$, so $c = 0.79$.

**Probabilistically shaped 64-QAM.** Shaping each axis of 64-QAM in the same way gives the same gain per dimension for twice the rate. Coherent optical transceivers use shaped QAM to tune the rate to the length of the link with one code and one constellation.

**Rate adaptation.** With a fixed code rate $c$ and constellation, the rate $R = H(A) + 1 - (1 - c)m$ moves with $H(A)$, which the matcher sets by the choice of $\nu$. A fine grid of rates follows from one code.

## Variations

- **Distribution matchers.** [CCDM](/constant-composition-distribution-matching/) uses one composition. Matchers that allow several compositions, or all sequences below an energy bound (sphere shaping), lose less rate at short block lengths.
- **Shell mapping and trellis shaping.** Older methods that pick sequences of low energy directly. The V.34 modem used shell mapping.
- **Geometric shaping.** Move the points instead of changing their probabilities, for example with nonuniform spacing. It can be combined with probabilistic shaping.
- **Shaping with multilevel coding.** Shape the levels of a [multilevel code](/multilevel-coding/) and decode in stages.
- **Other channels.** On the optical fiber channel, the energy distribution also changes the nonlinear interference, and the best distribution is not exactly Maxwell-Boltzmann.

## Pitfalls

- **The rate loss of the matcher.** A short block wastes rate: CCDM with $n = 10$ loses $0.55$ bits per symbol for a 4-amplitude target, which is more than the gain. Use long blocks or a better matcher.
- **The demapper must use the priors.** The LLRs need $P_A$ in the metric; a demapper that assumes uniform points gives biased LLRs and loses part of the gain.
- **$\nu$ depends on the SNR.** A distribution tuned for one SNR is not the best at another; the gain falls and can turn into a loss at low SNR with a high $\nu$.
- **The code rate constraint.** In basic PAS, all parity bits must fit in the signs: $c \ge (m - 1)/m$. Lower rates need a different construction.
- **Peak power.** Shaping lowers the average energy but not the peak, so the peak-to-average power ratio rises. This matters for amplifiers with a peak limit; see [peak-to-average power ratio](/peak-to-average-power-ratio/).
- **Error propagation in the dematcher.** A wrong amplitude after decoding can corrupt many output bits of the matcher. Keep the matcher blocks short enough, or protect the decoder output well.

## Exercises

1. Show with a Lagrange multiplier that $P_\nu$ maximizes $H(X)$ on $\mathcal{X}$ under the constraint $E[X^2] = E$.
2. Show that a uniform distribution on $[-a, a]$ and a Gaussian with the same differential entropy have the power ratio $\pi e/6$.
3. Compute the average energy and the entropy of the 8-ASK distribution in the table, and check the values $9.15$ and $2.632$.
4. In PAS with 16-ASK ($m = 4$), find the smallest code rate that keeps all parity bits in the signs, and the rate $R$ with $H(A) = 2.5$ bits and $c = 5/6$.
5. Explain why a symmetric distribution makes the sign bits uniform and independent of the amplitudes, and why PAS needs this.

## References
