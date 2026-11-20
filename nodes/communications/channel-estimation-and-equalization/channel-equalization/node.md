---
tag: 1AH6PD
kind: problem
slug: channel-equalization
name: Channel equalization
aliases:
- ISI equalization
area: communications/channel-estimation-and-equalization
level: intro
summary: "Recover the symbols x from y[n] = sum of h[l] x[n-l] + w[n], a channel with intersymbol interference. The Viterbi search is optimal in O(N M^L); linear and DFE equalizers are faster but lose SNR."
prereqs: [intersymbol-interference, additive-white-gaussian-noise-channel, tapped-delay-line-channel-model]
see_also: [zero-forcing-equalizer, mmse-linear-equalizer, fractionally-spaced-equalizer, decision-feedback-equalizer, viterbi-equalizer, frequency-domain-equalization, adaptive-equalization, channel-estimation]
sources:
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Chapter 9, Section 9.4 (linear equalization) and Section 9.5 (decision-feedback equalization)"
  - book: isbn:9780792375487
    title: "John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004"
    locator: "Chapter 8 (equalization)"
  - paper: doi:10.1109/TIT.1972.1054829
    title: "G. David Forney, Maximum-likelihood sequence estimation of digital sequences in the presence of intersymbol interference, IEEE Transactions on Information Theory 18(3), 1972, pages 363 to 378"
    locator: "the whitened matched filter and the Viterbi algorithm as the maximum-likelihood sequence estimator"
  - paper: "Shahid U. H. Qureshi, Adaptive equalization, Proceedings of the IEEE 73(9), 1985, pages 1349 to 1387"
    locator: "a survey of linear, decision-feedback and adaptive equalizers"
  - paper: doi:10.1002/j.1538-7305.1965.tb01678.x
    title: "R. W. Lucky, Automatic equalization for digital communication, Bell System Technical Journal 44(4), 1965, pages 547 to 588"
    locator: "the zero-forcing equalizer and the peak distortion criterion"
---

Channel equalization is the problem of recovering transmitted symbols from a channel that smears each symbol into its neighbors. A dispersive channel, such as a telephone line, a cable or a multipath radio channel, has an impulse response longer than one symbol, so the received sample $y[n] = \sum_{l=0}^{L-1} h_l\, x[n-l] + w[n]$ mixes the current symbol with the $L - 1$ before it. This is [intersymbol interference](/intersymbol-interference/) (ISI). An equalizer is any receiver that undoes it. The optimal answer, the most likely symbol sequence, is a shortest path search over a trellis of $M^{L-1}$ states, done by the [Viterbi equalizer](/viterbi-equalizer/) in $O(N M^L)$ time for $N$ symbols from an alphabet of $M$. Cheaper answers filter the samples first and then decide one symbol at a time: the [zero-forcing](/zero-forcing-equalizer/) and [MMSE linear equalizers](/mmse-linear-equalizer/), the [fractionally spaced equalizer](/fractionally-spaced-equalizer/), and the [decision feedback equalizer](/decision-feedback-equalizer/). They cost $O(N)$ operations per symbol but lose SNR on hard channels. Most equalizers need the channel, which [channel estimation](/channel-estimation/) supplies; [blind equalization](/blind-equalization/) works without it.

## In plain words

When a symbol travels through a channel with echoes, part of it arrives late and lands on top of the next symbols. If the echoes are strong, the receiver can no longer tell the symbols apart by looking at one sample at a time. Equalization is the task of separating them again. One way is to build a filter that cancels the echoes; it is fast, but where the channel is weak it also boosts the noise. A better filter balances the echoes left over against the noise boosted. Another way is to subtract the echoes of symbols already decided. The best way checks every possible sequence of symbols against the received samples and picks the one that fits best; a clever search makes this practical when the echoes are short.

## Definition

**Input.** The channel taps $h = (h_0, \ldots, h_{L-1})$, known or estimated, the noise power $N_0$, a constellation $\mathcal{A}$ of $M$ points with energy $E_s$, and the received samples $y[0], \ldots, y[N + L - 2]$, where

$$y[n] = \sum_{l=0}^{L-1} h_l\, x[n - l] + w[n], \qquad w[n] \sim \mathcal{CN}(0, N_0) \text{ independent},$$

$x[n] \in \mathcal{A}$ for $0 \le n < N$, and $x[n] = 0$ outside this range. This is the discrete model at one sample per symbol, after a matched filter and a noise whitening filter; fractionally spaced versions take $L_s$ samples per symbol.

**Output.** Decisions $\hat x[0], \ldots, \hat x[N-1] \in \mathcal{A}$.

**Goal.** One of two criteria. The sequence criterion minimizes the probability that $\hat x \ne x$ as a whole; with equally likely sequences it is maximum likelihood, $\hat x = \arg\min_{x \in \mathcal{A}^N} \sum_n |y[n] - \sum_l h_l x[n-l]|^2$. The symbol criterion minimizes the probability that $\hat x[n] \ne x[n]$ for each $n$, which is the symbol-by-symbol MAP rule.

**Equalizer criteria.** Linear and decision feedback equalizers do not minimize either error probability directly. They use a surrogate: the peak distortion, minimized by the zero-forcing design when the eye is open, or the mean squared error $E|z[n] - x[n - \Delta]|^2$ of the filter output, minimized by the MMSE design.

## Variants

- **Known channel or adaptive.** The channel is estimated first from pilots, or the equalizer adapts its taps directly from a training sequence and then from its decisions; see [adaptive equalization](/adaptive-equalization/).
- **Blind.** No training at all, as in [blind equalization](/blind-equalization/) and the [constant modulus algorithm](/constant-modulus-algorithm/).
- **Symbol spaced or fractionally spaced.** One sample per symbol after a matched filter, or $L_s = 2$ samples per symbol, which removes the dependence on the sampling phase.
- **Time domain or frequency domain.** With a cyclic prefix or a known block structure, the equalizer works per DFT bin; see [frequency-domain equalization](/frequency-domain-equalization/) and [OFDM](/orthogonal-frequency-division-multiplexing/).
- **Hard or soft.** A turbo receiver exchanges soft information between the equalizer and the decoder; see [turbo equalization](/turbo-equalization/).
- **Channel shortening.** A filter that makes the channel short enough for a cheap Viterbi search or for the cyclic prefix; see the [channel shortening equalizer](/channel-shortening-equalizer/).

## Examples

**A mild channel, BPSK.** Let $h = (1, 0.5)$ and $x[n] = \pm 1$. Without noise, $y[n] = x[n] + 0.5\, x[n-1]$ takes the values $\pm 1.5$ and $\pm 0.5$, so the sign of $y[n]$ is still $x[n]$: the eye is open, and the smallest distance to the threshold falls from 1 to 0.5, a worst-case loss of $20 \log_{10} 2 = 6.02$ dB. A 5-tap ZF equalizer has the taps $(1, -0.5, 0.25, -0.125, 0.0625)$ and leaves the residue $0.5^5 = 0.03125$; its noise gain is 1.33, or 1.25 dB. At $N_0 = 0.1$ the 5-tap MMSE equalizer reaches the mean squared error 0.112, against 0.134 for the ZF.

**A hard channel.** The channel B of Proakis, $h = (0.407, 0.815, 0.407)$, has $\|h\|^2 = 0.9955$ and a near null, $H(e^{j\pi}) = -0.001$. At $E_s/N_0 = 20$ dB the matched filter bound is $E_s \|h\|^2 / N_0 = 19.98$ dB. The best 31-tap MMSE linear equalizer reaches an unbiased SINR of 6.60 dB, a loss of 13.4 dB, and the best 31-tap ZF equalizer has a noise gain of 2641, or 34.2 dB. A Viterbi equalizer for BPSK on this channel needs only $2^2 = 4$ states and does not invert the null. Its error events are set by the minimum distance of the noiseless outputs: the error pattern $(2, -2)$ gives $d_{\min}^2 = 4 \cdot 0.6642 = 2.657$, against $4 \|h\|^2 = 3.982$ for one isolated symbol, so the loss at high SNR is only 1.76 dB.

**Non-example: a flat channel.** If $L = 1$, then $y[n] = h_0 x[n] + w[n]$ has no ISI, and the problem is one scalar [symbol detection](/symbol-detection/) per sample, after a division by $h_0$.

## Known algorithms

- **[Viterbi equalizer](/viterbi-equalizer/).** Maximum likelihood sequence estimation: the [Viterbi algorithm](/viterbi-algorithm/) on a trellis of $M^{L-1}$ states, $O(N M^L)$ time. It is exact for the sequence criterion. See also [maximum likelihood sequence estimation](/maximum-likelihood-sequence-estimation/) and the [whitened matched filter](/whitened-matched-filter/).
- **[Zero-forcing equalizer](/zero-forcing-equalizer/).** A linear filter that inverts the channel; $O(N_f^3)$ design and $O(N_f)$ per symbol for $N_f$ taps. It enhances noise near spectral nulls.
- **[MMSE linear equalizer](/mmse-linear-equalizer/).** The linear filter with the smallest mean squared error; same costs, better at every SNR.
- **[Fractionally spaced equalizer](/fractionally-spaced-equalizer/).** The linear equalizer at $L_s = 2$ samples per symbol.
- **[Decision feedback equalizer](/decision-feedback-equalizer/).** A linear feedforward filter and a feedback filter that subtracts the ISI of past decisions; see the [MMSE-DFE canonical theorem](/mmse-dfe-canonical-theorem/).
- **[Frequency-domain equalization](/frequency-domain-equalization/).** ZF or MMSE per DFT bin, $O(\log N)$ per symbol with the FFT.
- **Adaptive versions** with the [LMS](/lms-algorithm/) and [RLS](/rls-algorithm/) algorithms, and soft equalizers such as the [soft interference cancellation equalizer](/soft-interference-cancellation-equalizer/).

## Bounds

**Matched filter bound.** No receiver does better than a receiver that sees one isolated symbol, with no ISI. Its SNR is $E_s \|h\|^2 / N_0$, and its error probability is a lower bound for every equalizer.

**Linear equalizers.** The infinite-length ZF equalizer has the output noise $N_0 \cdot \frac{1}{2\pi}\int_{-\pi}^{\pi} |H(e^{j\omega})|^{-2} d\omega$, which is infinite if $H$ has a zero on the unit circle. The infinite-length MMSE equalizer has the error $\frac{1}{2\pi}\int_{-\pi}^{\pi} E_s N_0 / (E_s |H(e^{j\omega})|^2 + N_0)\, d\omega$, which is always finite. By Jensen's inequality, both are at least the values for a flat channel of the same energy.

**Decision feedback.** The unbiased SNR of the infinite-length MMSE-DFE is given by the [MMSE-DFE canonical theorem](/mmse-dfe-canonical-theorem/) in terms of the average of $\log(1 + E_s |H(e^{j\omega})|^2/N_0)$, which links it to the capacity of the ISI channel with white inputs.

**Complexity.** The exact ML sequence search is exponential in the channel memory: $M^{L-1}$ states. For a fixed $L$, it is linear in $N$. Suboptimal search, such as reduced-state sequence estimation, cuts the states.

## Reductions

- **ISI to a vector channel.** Stacking the samples gives $y = H x + w$ with a banded Toeplitz matrix $H$, so equalization is a structured [MIMO detection](/mimo-detection/) problem, and linear equalizers are the ZF and MMSE detectors for this $H$.
- **ML sequence detection to shortest paths.** After the whitened matched filter, the ML metric is a sum of branch costs on a trellis, and the Viterbi algorithm finds the shortest path.
- **Block ISI to flat channels.** With a cyclic prefix, the DFT diagonalizes the channel, and the problem splits into $N$ scalar detection problems, one per subcarrier.
- **Equalization needs estimation.** Every non-blind equalizer reduces to [channel estimation](/channel-estimation/) followed by a detector designed for the estimate.

## Applications

Equalizers made high-speed voiceband modems possible, starting with Lucky's automatic equalizer in the 1960s. GSM receivers use a Viterbi equalizer over the training sequence in each burst. DSL, cable modems and single-carrier wireless links use DFEs and fractionally spaced linear equalizers. Magnetic recording uses [partial response signaling](/partial-response-signaling/) with a Viterbi detector. OFDM and single-carrier frequency-domain systems move the equalizer to the DFT domain.

## References
