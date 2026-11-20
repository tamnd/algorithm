---
tag: Z633YX
kind: definition
slug: peak-to-average-power-ratio
name: Peak-to-average power ratio
aliases:
- PAPR
- crest factor
area: communications/ofdm-and-multicarrier
level: core
summary: "The peak power of a signal block divided by its mean power. OFDM symbols have a high PAPR, so the power amplifier must back off. Measure it with 4 times oversampling."
prereqs: [orthogonal-frequency-division-multiplexing, central-limit-theorem]
see_also: [iterative-clipping-and-filtering, selected-mapping, partial-transmit-sequence, tone-reservation, active-constellation-extension, sc-fdma, multicarrier-modulation, zadoff-chu-sequence]
sources:
  - paper: doi:10.1109/MWC.2005.1421929
    title: "Seung Hee Han and Jae Hong Lee, An overview of peak-to-average power ratio reduction techniques for multicarrier transmission, IEEE Wireless Communications 12(2), 2005, pages 56 to 65"
    locator: "the definition of the PAPR of a multicarrier block, its CCDF under the independence approximation, the oversampled measurement and the overview of reduction methods"
  - paper: "Hideki Ochiai and Hideki Imai, On the distribution of the peak-to-average power ratio in OFDM signals, IEEE Transactions on Communications 49(2), 2001, pages 282 to 289"
    locator: "the distribution of the PAPR of the continuous-time OFDM signal, where the independent-sample rule does not hold"
  - paper: "Gerhard Wunder, Robert F. H. Fischer, Holger Boche, Simon Litsyn and Jong-Seon No, The PAPR problem in OFDM transmission: new directions for a long-lasting problem, IEEE Signal Processing Magazine 30(6), 2013, pages 130 to 144"
    locator: "the PAPR and the related metrics, and the limits of what reduction can achieve"
  - book: isbn:9780792379881
    title: "Jose Tellado, Multicarrier Modulation with Low PAR: Applications to DSL and Wireless, Kluwer Academic Publishers, 2000"
    locator: "chapter Peak to Average Ratio (the definition, the distribution of the peak and the effect of oversampling)"
---

The peak-to-average power ratio (PAPR) of a block of complex baseband samples $x[n]$ is the largest instantaneous power $|x[n]|^2$ in the block divided by the mean power $E|x[n]|^2$. An [OFDM](/orthogonal-frequency-division-multiplexing/) symbol is a sum of $N$ subcarriers with independent data, so a few samples can be much larger than the rest, and its PAPR can approach $N$. A power amplifier is linear only up to a saturation level, so the transmitter must set the mean power well below that level, the backoff, and this costs power efficiency. This page defines the measure and its distribution. The methods that lower it have their own pages: [clipping and filtering](/iterative-clipping-and-filtering/), [selected mapping](/selected-mapping/), [partial transmit sequences](/partial-transmit-sequence/), [tone reservation](/tone-reservation/) and [active constellation extension](/active-constellation-extension/), and the waveform [SC-FDMA](/sc-fdma/), which avoids most of the problem. The page uses the unitary DFT pair of the OFDM page, $x = F^H X$ with $F[k, n] = e^{-j 2\pi k n / N} / \sqrt N$, $j$ is the imaginary unit, and the constellations are normalized to $E_s = E|X[k]|^2 = 1$.

## Definition

**PAPR of a block.** For the samples $x[0], \ldots, x[M-1]$ of one block,

$$\mathrm{PAPR} = \frac{\max_{0 \le n < M} |x[n]|^2}{E\,|x[n]|^2}, \qquad \mathrm{PAPR}_{\mathrm{dB}} = 10 \log_{10} \mathrm{PAPR}.$$

The PAPR is a random variable: it changes from one OFDM symbol to the next. Many authors put the time average $\frac{1}{M}\sum_n |x[n]|^2$ of the block in the denominator instead of the ensemble mean. For constant-modulus symbols such as QPSK the two are equal, because by [Parseval's theorem](/parsevals-theorem/) the block energy is $\sum_k |X[k]|^2 = N$ for every block. For 16-QAM they differ a little from block to block.

**Crest factor.** The crest factor is the peak amplitude divided by the RMS amplitude, $\mathrm{CF} = \sqrt{\mathrm{PAPR}}$. In decibels the two numbers are the same, since $20 \log_{10} \mathrm{CF} = 10 \log_{10} \mathrm{PAPR}$.

**Continuous time and oversampling.** The amplifier sees the analog signal $x(t)$, and its peaks can fall between the samples $x[n] = x(nT/N)$. The PAPR of $x(t)$ over the symbol is at least the PAPR of the $N$ samples. To measure it, oversample by a factor $L$: put $(L - 1)N$ zeros in the middle of $X$, between $X[N/2 - 1]$ and $X[N/2]$, so that the indices $k \ge N/2$ stay the negative frequencies, and take an inverse DFT of size $LN$. The standard choice is $L = 4$. With the scale $\sqrt L$, the oversampled block $x_L$ satisfies two facts that follow from the definition of the DFT:

1. $x_L[L n] = x[n]$ for $n = 0, \ldots, N - 1$, so the oversampled block contains the Nyquist-rate samples, and its PAPR is never smaller.
2. $\frac{1}{LN} \sum_m |x_L[m]|^2 = \frac{1}{N} \sum_k |X[k]|^2$, so the mean power does not change.

```pseudo id=main
PAPR(X[0..N-1], L)                              ▷ N and L are powers of two; L = 4 is the usual choice
L1  Z ← (X[0], .., X[N/2-1], 0, .., 0, X[N/2], .., X[N-1])    ▷ (L-1)N zeros in the middle, length LN
L2  x ← √L · F_LNᴴ Z                            ▷ unitary inverse FFT of size LN, scaled by √L
L3  P ← max_m |x[m]|²
L4  return P / E|x[m]|²                         ▷ the time average of |x[m]|² for constant-modulus X
```

The cost is one inverse [FFT](/fast-fourier-transform/) of size $LN$, $O(LN \log(LN))$ operations per symbol in the real-RAM model.

**The upper bound $N$.** With the time-average denominator, $\mathrm{PAPR} \le N$ for every block and every $L$, and also for the continuous signal. Each sample is $x(t) = \frac{1}{\sqrt N} \sum_k X[k] e^{j 2\pi f_k t}$, so by the Cauchy-Schwarz inequality $|x(t)|^2 \le \frac{1}{N} \big(\sum_k |X[k]|\big)^2 \le \sum_k |X[k]|^2$, and the mean power is $\frac{1}{N} \sum_k |X[k]|^2$. Equality needs all $|X[k]|$ equal and all subcarriers in phase at one instant, for example $X[k] = 1$ for all $k$.

**The distribution and the rule.** The CCDF $\Pr(\mathrm{PAPR} > \gamma)$ describes a waveform better than one number. If the $N$ samples are independent and each is $\mathcal{CN}(0, 1)$, then $|x[n]|^2$ is exponential with mean 1, $\Pr(|x[n]|^2 \le \gamma) = 1 - e^{-\gamma}$, and

$$\Pr(\mathrm{PAPR} > \gamma) = 1 - (1 - e^{-\gamma})^N.$$

This is exact in one case: if the $X[k]$ are i.i.d. $\mathcal{CN}(0, 1)$ and the denominator is the ensemble mean, then $x = F^H X$ is again i.i.d. $\mathcal{CN}(0, 1)$, because $F^H$ is unitary. For QPSK or QAM data it is a rule, not a theorem. The [central limit theorem](/central-limit-theorem/) makes each sample close to Gaussian for large $N$, but the rule assumes independent samples and ignores oversampling, and the oversampled samples are strongly correlated. At $N = 64$ and $\gamma = 10$ dB the rule gives $1 - (1 - e^{-10})^{64} = 2.90 \cdot 10^{-3}$. Ochiai and Imai (2001) give a better approximation for the continuous-time signal.

**Baseband and passband.** The definition above uses the complex envelope. Some texts call it the peak-to-mean envelope power ratio (PMEPR). The real passband signal $s(t) = \mathrm{Re}\{x(t) \sqrt 2\, e^{j 2\pi f_c t}\}$ has mean power $E|x|^2$ and, for a carrier frequency much larger than the bandwidth, peaks close to $2 \max |x(t)|^2$, so its PAPR is about 3.01 dB higher. The factor $\sqrt 2$ does not change this ratio; without it, both the peak and the mean are halved. Always say which one a number refers to.

## Examples and non-examples

**Four subcarriers, a hidden peak.** Take $N = 4$ and the BPSK block $X = (1, 1, 1, -1)$. The Nyquist-rate samples are

$$x[n] = \tfrac{1}{2} \textstyle\sum_k X[k] e^{j 2\pi k n / 4} = (1,\ j,\ 1,\ -j),$$

all of magnitude 1, so the PAPR of the 4 samples is 1, that is 0 dB. With $L = 4$ the PAPR is 2.32 dB, and with $L = 64$ it is 2.48 dB, close to the continuous-time value. The samples at the Nyquist rate miss the peak completely.

**All subcarriers in phase.** $X[k] = 1$ for all $k$ gives $x[0] = \sqrt N$ and $x[n] = 0$ for $n = 1, \ldots, N - 1$ at the Nyquist rate. The PAPR is $N$, the upper bound: 6.02 dB for $N = 4$ and 18.06 dB for $N = 64$. A block of training symbols with this pattern would drive the amplifier hard, which is one reason why preambles use sequences with a flat envelope, such as [Zadoff-Chu sequences](/zadoff-chu-sequence/).

**64 subcarriers with QPSK.** A simulation of 4000 random QPSK symbols with $N = 64$ (Python `random.Random(1)`) gives the CCDF below. The rule fits the Nyquist-rate samples well. The 4 times oversampled signal exceeds each level about twice as often as the rule says, which is the error from ignoring the peaks between samples.

| $\gamma$ | 6 dB | 7 dB | 8 dB | 9 dB | 10 dB |
|---|---|---|---|---|---|
| rule $1 - (1 - e^{-\gamma})^{64}$ | 0.701 | 0.348 | 0.110 | 0.0225 | 0.0029 |
| simulation, $L = 1$ | 0.755 | 0.355 | 0.103 | 0.0188 | 0.0025 |
| simulation, $L = 4$ | 0.954 | 0.636 | 0.236 | 0.0488 | 0.0070 |

In the same run the mean PAPR is 6.83 dB at $L = 1$ and 7.48 dB at $L = 4$, and the PAPR exceeded by 1 percent of the symbols is 9.30 dB and 9.85 dB. So, to clip at most 1 percent of the symbols, the mean power must be about 9.9 dB below the saturation power of the amplifier. In a second run of 300 symbols, the PAPR at $L = 16$ was on average 0.07 dB above the value at $L = 4$ (at most 0.34 dB), while the value at $L = 4$ was on average 0.71 dB above the value at $L = 1$ (at most 3.29 dB). So $L = 4$ captures most of the peak, and $L = 1$ does not.

**A single carrier.** The symbol-spaced samples of single-carrier QPSK all have power 1, so their PAPR is 0 dB. For 16-QAM the largest point $(3 + 3j)/\sqrt{10}$ has power $18/10$, so the PAPR is $10 \log_{10} 1.8 = 2.55$ dB. These are values at the symbol instants. The filtered waveform after [pulse shaping](/pulse-shaping/) has peaks between the symbols, and its PAPR depends on the roll-off. Still, it is far below the PAPR of OFDM, which is the reason for [SC-FDMA](/sc-fdma/) in the LTE uplink.

**Non-example: the mean over many symbols.** The ratio of the largest peak in a long transmission to the mean power is not the PAPR of an OFDM symbol. It grows with the length of the record, because a longer record contains rarer peaks. Report the CCDF per symbol, or a quantile of it.

**Non-example: a pure tone.** A single subcarrier, $x[n] = e^{j 2\pi k n / N}$, has a constant envelope and a PAPR of 0 dB in baseband. Its real passband signal is a sinusoid with a PAPR of 2, 3.01 dB. Both numbers are correct; they measure different signals.

## Related definitions

- [Orthogonal frequency-division multiplexing](/orthogonal-frequency-division-multiplexing/) and [multicarrier modulation](/multicarrier-modulation/): the waveforms whose sums of subcarriers cause the high PAPR.
- [Iterative clipping and filtering](/iterative-clipping-and-filtering/) and [active constellation extension](/active-constellation-extension/): methods that change the signal and add distortion, or move outer constellation points, to cut the peaks.
- [Selected mapping](/selected-mapping/) and [partial transmit sequences](/partial-transmit-sequence/): methods that pick, among several equivalent versions of the symbol, the one with the lowest PAPR, and send side information.
- [Tone reservation](/tone-reservation/): a method that spends a few subcarriers on a peak-cancelling signal.
- [SC-FDMA](/sc-fdma/): DFT-spread OFDM, whose samples are a filtered single-carrier signal with a much lower PAPR.
- [Central limit theorem](/central-limit-theorem/): the reason the OFDM samples are close to complex Gaussian, and the envelope close to the Rayleigh distribution of the [Rayleigh fading channel](/rayleigh-fading-channel/).

## References
