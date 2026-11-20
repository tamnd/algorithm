---
tag: ARMC3S
kind: problem
slug: frequency-offset-estimation
name: Frequency offset estimation
aliases:
- carrier frequency offset estimation
- CFO estimation
area: communications/synchronization
level: core
summary: Estimate the difference between the carrier frequency of the received signal and the local oscillator from noisy samples.
prereqs: [additive-white-gaussian-noise-channel, discrete-fourier-transform, cramer-rao-bound]
see_also: [kay-frequency-estimator, rife-boorstyn-frequency-estimator, luise-reggiannini-estimator, schmidl-cox-synchronization, van-de-beek-estimator, moose-frequency-offset-estimator, carrier-recovery, modified-cramer-rao-bound]
sources:
  - book: isbn:9780306457258
    title: "Umberto Mengali and Aldo N. D'Andrea, Synchronization Techniques for Digital Receivers, Plenum Press, 1997"
    locator: "Chapter 3 (carrier frequency recovery with linear modulations: data-aided and non-data-aided, feedforward and feedback estimators)"
  - paper: doi:10.1109/TIT.1974.1055282
    title: "D. C. Rife and R. R. Boorstyn, Single-tone parameter estimation from discrete-time observations, IEEE Transactions on Information Theory 20(5), 1974, pages 591 to 598"
    locator: "the Cramer-Rao bound for the frequency of a tone, the maximum likelihood estimator and its threshold"
  - paper: doi:10.1109/TCOMM.1994.580247
    title: "A. N. D'Andrea, U. Mengali and R. Reggiannini, The modified Cramer-Rao bound and its application to synchronization problems, IEEE Transactions on Communications 42(2/3/4), 1994, pages 1391 to 1399"
    locator: "the modified Cramer-Rao bound for the carrier frequency"
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 3 (the Cramer-Rao lower bound, including the bound for the parameters of a sinusoid)"
---

Frequency offset estimation is the problem of finding how far the carrier frequency of a received signal is from the frequency of the receiver's local oscillator, from a finite block of noisy samples. With known or removed data, it is the estimation of the frequency of one complex tone in white noise. Single-carrier estimators work on the symbol samples: the [Rife and Boorstyn estimator](/rife-boorstyn-frequency-estimator/) is the maximum likelihood method, a periodogram peak with a fine search; the [Kay estimator](/kay-frequency-estimator/) averages the phase differences of consecutive samples with weights; the [Luise and Reggiannini estimator](/luise-reggiannini-estimator/) takes the angle of a sum of autocorrelations. OFDM estimators measure the phase between repeated parts of the signal, in units of the subcarrier spacing: [Schmidl-Cox synchronization](/schmidl-cox-synchronization/) uses a training symbol with two equal halves, the [Moose estimator](/moose-frequency-offset-estimator/) uses two repeated symbols, and the [van de Beek estimator](/van-de-beek-estimator/) uses the cyclic prefix with no training. They trade cost, range and the SNR at which they fail. The frequency is the first step of [carrier recovery](/carrier-recovery/), and the [modified Cramer-Rao bound](/modified-cramer-rao-bound/) is the yardstick for all of them.

## In plain words

The transmitter and the receiver each have an oscillator, and the two never run at exactly the same speed. Movement adds a Doppler shift too. So the received symbols seem to turn slowly, a little more at each step. The receiver must measure how fast they turn, so that it can turn them back. It does this from a short stretch of noisy samples, by checking how much the angle grows from one sample to a later one. A longer stretch gives a better measurement. If the turning is too fast, or the noise too strong, the measurement can be badly wrong.

## Definition

**Input.** Samples $r_k = a_k e^{j(2\pi\nu k + \theta)} + w_k$, $k = 0, \ldots, N - 1$, at one sample per symbol, where $\nu$ is the unknown frequency offset in cycles per symbol, $\theta$ is an unknown phase, $a_k$ are the symbols and $w_k \sim \mathcal{CN}(0, N_0)$ is white noise. In the data-aided case the $a_k$ are known, and $z_k = a_k^\ast r_k / |a_k|^2$ is a tone $e^{j(2\pi\nu k + \theta)}$ in noise. The signal-to-noise ratio is $\mathrm{SNR} = E|a_k|^2/N_0$.

**Output.** An estimate $\hat\nu$ of $\nu$, within a range $|\nu| < \nu_{\max}$ that the method can resolve without ambiguity.

**OFDM form.** In OFDM, the offset is written as $\varepsilon = \Delta f\, N / f_s$ in units of the subcarrier spacing, and the samples are those of the time-domain OFDM signal rather than of the symbols. An offset with a fractional part breaks the orthogonality of the subcarriers and causes [inter-carrier interference](/inter-carrier-interference/), so it must be removed before the DFT.

**Measures.** The mean square error against the bound, the range $\nu_{\max}$, the threshold SNR below which outliers start, and the cost per block.

## Variants

- **Data-aided, decision-directed or non-data-aided.** With known pilots, the data are removed exactly. For M-PSK without known data, $r_k^M$ removes the modulation and becomes a tone at $M\nu$, so the range is divided by $M$ and the noise is enhanced.
- **Feedforward or feedback.** A feedforward estimator gives one value per block, which suits bursts. A feedback frequency-locked loop drives a frequency error detector to zero, which suits continuous tracking; the Luise and Reggiannini statistic can serve as such a detector.
- **Coarse and fine.** A large offset is often split into a coarse part, from a short-lag correlation with a wide range, and a fine part, from a long-lag correlation or a long block. In OFDM, this is the split into an integer and a fractional number of subcarrier spacings.
- **Constant or varying offset.** A Doppler rate or oscillator drift makes $\nu$ change in time, and the estimator must track it.

## Examples

**The phase step (theorem).** Without noise and with $\nu = 0.1$, each product $z_{k+1} z_k^\ast = e^{j2\pi \cdot 0.1}$ has the angle $0.628$, and $0.628/(2\pi) = 0.1$. The Kay and the Rife and Boorstyn estimators return $0.1$ on this input, and so does the Luise and Reggiannini estimator for $L \le 8$, where $0.1 < 1/(L+1)$. With $\nu = 0.6$, the angle is $2\pi \cdot 0.6 - 2\pi$, and the lag-1 estimate is $-0.4$: offsets beyond the range wrap.

**The size of the bound.** With the phase unknown, the bound is $\frac{3}{2\pi^2\,\mathrm{SNR}\,N(N^2-1)}$ cycles$^2$ per symbol$^2$. For $N = 32$ and $\mathrm{SNR} = 10$ dB this is $4.64 \times 10^{-7}$, a standard deviation of $6.8 \times 10^{-4}$ cycles per symbol, or 680 Hz at a symbol rate of 1 MHz.

**Thresholds (measurements).** The pages of the three single-carrier estimators measured the mean square error over the CRB at $N = 32$, with their own seeds:

| SNR | Kay | Rife and Boorstyn | Luise and Reggiannini, $L = 16$ |
|---|---|---|---|
| $-3$ dB | not measured | $4.97$ | $1.36$ |
| 0 dB | $185$ | $1.14$ | $1.20$ |
| 5 dB | $18$ | $1.08$ | $1.12$ |
| 10 dB | $0.99$ | $1.05$ | $1.09$ |

The ML search works down to about 0 dB. The Luise and Reggiannini estimator with $L = N/2$ is close to it at low SNR, at a range of $|\nu| < 1/17$ instead of $1/2$. The Kay estimator is at the bound only from about 10 dB.

## Known algorithms

| Algorithm | Year | Data | Range | Cost | Note |
|---|---|---|---|---|---|
| [Rife and Boorstyn](/rife-boorstyn-frequency-estimator/) | 1974 | tone | $\lvert\nu\rvert < 1/2$ | $O(N\log N)$ | maximum likelihood, lowest threshold |
| [Kay](/kay-frequency-estimator/) | 1989 | tone | $\lvert\nu\rvert < 1/2$ | $O(N)$ | weighted phase differences, high threshold |
| [Luise and Reggiannini](/luise-reggiannini-estimator/) | 1995 | tone | $\lvert\nu\rvert < 1/(L+1)$ | $O(NL)$ | angle of summed autocorrelations |
| [Moose](/moose-frequency-offset-estimator/) | 1994 | OFDM, two repeated symbols | $\lvert\varepsilon\rvert < 1/2$ | $O(N\log N)$ | ML, timing known |
| [Schmidl-Cox](/schmidl-cox-synchronization/) | 1997 | OFDM, symbol with two halves | $\lvert\varepsilon\rvert < 1$, more with a second symbol | $O(N)$ per position | also gives the timing |
| [Van de Beek](/van-de-beek-estimator/) | 1997 | OFDM, cyclic prefix | $\lvert\varepsilon\rvert < 1/2$ | $O(N_{cp})$ per position | blind, also gives the timing |

Other methods fit a line to the unwrapped phase of $z_k$, apply linear prediction, or interpolate the three largest FFT values.

## Bounds

- **Cramer-Rao bound (theorem).** With known data and unknown phase, every unbiased estimator from $N$ samples has the variance at least $\frac{3}{2\pi^2\,\mathrm{SNR}\,N(N^2-1)}$ in cycles per symbol. The variance falls as $1/N^3$: the longer the block, the larger the phase that the offset builds up. Without known data, this value is the [MCRB](/modified-cramer-rao-bound/), still a valid bound but not tight at low SNR.
- **Range and accuracy (theorem for the range, rule for the trade).** An estimator from the angle of the correlation at lag $D$ cannot tell $\nu$ from $\nu + 1/D$, so its range is $|\nu| < 1/(2D)$, while its variance falls as $1/D^2$. A wider range costs accuracy, which is why coarse and fine stages are combined.
- **Threshold (rule).** All nonlinear estimators have a threshold SNR below which the error is dominated by outliers to random frequencies, and the mean square error rises far above the bound. For the ML estimator it depends on $N \cdot \mathrm{SNR}$; for the Kay estimator on the per-sample SNR.

## Reductions

- **To tone frequency estimation.** With known data, $z_k = a_k^\ast r_k/|a_k|^2$ turns the problem into the frequency of one tone, which is the classical problem of spectral estimation. The ML estimate is the peak of the [periodogram](/periodogram/).
- **From M-PSK to a tone.** Raising $r_k$ to the power $M$ removes M-PSK data and gives a tone at $M\nu$.
- **From OFDM to a phase difference.** A repeated part of the signal, $D$ samples apart, gives $r_{i+D} r_i^\ast \approx |s_i|^2 e^{j2\pi\varepsilon D/N}$, so the offset is the angle of a correlation, as in Moose, Schmidl-Cox and van de Beek.
- **To linear regression.** At high SNR, the unwrapped phase of $z_k$ is $\theta + 2\pi\nu k$ plus nearly Gaussian noise, and a least squares fit of a line estimates $\nu$; the Kay estimator is the best linear unbiased form of this idea applied to the phase differences.

## Applications

- **Burst modems.** Satellite and terrestrial burst receivers estimate the offset from a preamble before the phase.
- **OFDM systems.** Wi-Fi, LTE and DVB-T receivers estimate a coarse offset from short repeated training parts or the cyclic prefix, then a fine one from long training symbols or pilots.
- **Doppler.** Satellite and aircraft links, and radar, measure the Doppler shift of a carrier or echo.
- **Navigation.** GNSS acquisition searches over Doppler bins, then refines the frequency before the carrier loop takes over.
- **Measurement.** Instruments and power systems estimate the frequency of a sinusoid from short records.

## References
