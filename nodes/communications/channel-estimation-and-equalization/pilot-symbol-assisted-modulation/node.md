---
tag: EFR7K7
kind: technique
slug: pilot-symbol-assisted-modulation
name: Pilot symbol assisted modulation
aliases:
- PSAM
- pilot-aided transmission
area: communications/channel-estimation-and-equalization
level: core
summary: "Put one known symbol in every P symbols so the receiver can sample a fading channel and interpolate it. P must be below 1/(2 f_D T), the Nyquist limit of the fading."
prereqs: [rayleigh-fading-channel, clarke-model, sampling-theorem, lmmse-channel-estimation]
see_also: [channel-estimation, doppler-spread, coherence-time, two-dimensional-wiener-pilot-interpolation, comb-pilot-channel-estimation, kalman-channel-tracking, differential-phase-shift-keying, sinc-interpolation]
sources:
  - paper: doi:10.1109/25.108378
    title: "James K. Cavers, An analysis of pilot symbol assisted modulation for Rayleigh fading channels, IEEE Transactions on Vehicular Technology 40(4), 1991, pages 686 to 693"
    locator: "the frame with one pilot symbol, the Wiener interpolator over nearby pilots, the condition on the pilot spacing and the error rate analysis in Rayleigh fading"
  - book: isbn:9780133457117
    title: "Steven M. Kay, Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory, Prentice Hall, 1993"
    locator: "Chapter 12 (linear Bayesian estimators), for the Wiener interpolator"
---

Pilot symbol assisted modulation (PSAM) is a way to get a channel estimate for coherent detection on a fading channel. The transmitter divides the symbol stream into frames of $P$ symbols and makes the first symbol of each frame a pilot, a symbol the receiver knows. On a flat fading channel the received symbol is $y[n] = c[n]\, x[n] + w[n]$, so each pilot gives one noisy sample $c[aP] + w[aP]/b$ of the channel gain $c$. The receiver interpolates these samples to the data positions between them, usually with a [Wiener](/lmmse-channel-estimation/) filter over the $K$ nearest pilots, and then detects each data symbol with the estimate. The fading process has a spectrum limited to the Doppler frequency $f_D$, so by the [sampling theorem](/sampling-theorem/) the pilots must come at least $2 f_D$ times per second: $P < 1/(2 f_D T)$ for the symbol period $T$. Cavers (1991) gave the analysis of this scheme. The cost is a rate loss of $1/P$ and the energy spent on pilots. The gain is that the receiver can use any constellation, such as 16-QAM, with coherent detection, which differential detection cannot do well.

## In plain words

On a moving radio link, the channel changes its strength and phase all the time. To decide what was sent, the receiver must know the channel at each moment. So the sender puts a known symbol in the stream at regular gaps. At each known symbol, the receiver sees what the channel did. Between them, it guesses the channel by joining the known points smoothly, as you would draw a curve through points. If the known symbols come often enough compared with how fast the channel changes, this guess is good. If they come too rarely, the curve can miss the changes between them, and no amount of signal power fixes that.

## When it applies

- The channel is flat over the signal band, or flat on each subcarrier, and changes in time because of motion. Its time correlation is set by the Doppler spread, as in the [Clarke model](/clarke-model/), where $E[c[n+k]\, \overline{c[n]}] = J_0(2\pi f_D T k)$.
- The receiver wants coherent detection of a constellation with several amplitude levels, such as QAM, where the phase and the amplitude of the channel must both be known.
- The fading is slow compared with the symbol rate, $f_D T \ll 1$, so that a pilot every $P$ symbols, with $P$ well above 1, is enough. If $f_D T$ is close to $1/2$, nearly every symbol would have to be a pilot.
- The receiver can wait for the pilots after the data it detects; the interpolator looks ahead by about $K/2$ frames.

## The template

**Frame.** Symbol $aP$ is the pilot $b$, with $|b|^2 = E_p$, and the symbols $aP + 1, \ldots, aP + P - 1$ carry data with energy $E_s$. The data rate is a fraction $(P - 1)/P$ of the symbol rate.

**Pilot samples.** At each pilot, $z_a = y[aP] / b = c[aP] + v_a$, where $v_a$ has the variance $N_0 / E_p$.

**Interpolation.** For the data symbol at $n = aP + i$, $0 < i < P$, take the $K$ pilots nearest to it, with indices $a_1, \ldots, a_K$. With the fading correlation $R_c(k) = E[c[n+k]\, \overline{c[n]}]$ and a mean power of 1, let

$$A_{uv} = R_c\big((a_u - a_v) P\big) + \frac{N_0}{E_p}\, [u = v], \qquad r_u = R_c(a_u P - n), \qquad A w = r.$$

The estimate is $\hat c[n] = \sum_u \overline{w_u}\, z_{a_u}$, and its mean squared error is $\sigma_e^2(i) = 1 - r^H w$. This is the LMMSE estimate of $c[n]$ from the pilot samples. If $c$ is Gaussian, it is also the conditional mean. The weights depend only on the offset $i$, so there are $P - 1$ weight vectors, computed once.

**Detection.** Detect $x[n]$ from $y[n]$ with $\hat c[n]$ in place of $c[n]$, for example as the point $x$ that minimizes $|y[n] - \hat c[n]\, x|^2$.

**The spacing rule.** The samples $c[aP]$ are samples of a process whose spectrum lies in $|f| \le f_D$ at the rate $1/(PT)$. They determine the process without aliasing only if $1/(PT) > 2 f_D$, that is $P < 1/(2 f_D T)$. Below this limit, the interpolation error tends to zero as the pilot SNR and $K$ grow. Above it, the error has a floor that more power does not remove.

**Cost.** The interpolation is $K$ multiplications per data symbol. The overhead is one symbol in $P$ and the pilot energy, a fraction $E_p / (E_p + (P - 1) E_s)$ of the transmitted energy.

## Classic examples

**The spacing at highway speed.** At the carrier frequency $f_c = 2$ GHz and the speed $v = 30$ m/s, the Doppler frequency is $f_D = v f_c / c = 30 \cdot 2 \cdot 10^9 / (2.998 \cdot 10^8) = 200.1$ Hz. With $T = 10\ \mu$s, the limit is $1/(2 \cdot 200.1 \cdot 10^{-5}) = 249.8$, so a pilot every 249 symbols is the most that sampling allows. A practical design keeps a margin of 2 or more, for example $P = 100$, which still gives 99 percent of the symbols to data.

**The error below and above the limit.** Take $f_D T = 0.01$, so the limit is $P < 50$, the Clarke correlation $R_c(k) = J_0(2\pi \cdot 0.01\, k)$, and $K = 11$ pilots centered on the frame. The mean error over the positions in a frame is:

| $P$ | 10 | 25 | 40 | 60 | 80 |
|---|---|---|---|---|---|
| $E_p/N_0 = 20$ dB | 0.0032 | 0.0062 | 0.0092 | 0.268 | 0.389 |
| $E_p/N_0 = 60$ dB | 0.0000 | 0.0000 | 0.0001 | 0.259 | 0.382 |

Below the limit, the error is under the pilot noise level $N_0/E_p = 0.01$, because the filter averages several pilots, and it goes to zero with more power. At $P = 60$ and $P = 80$ the pilots alias the fading, and the error stays near 0.26 and 0.38 at any SNR. The error at the pilot positions is small even there; the large errors are in the middle of the frames.

**Nearest pilot only.** With $K = 1$ and no noise, $\hat c[n] = R_c(i)\, c[aP]$ for the pilot at distance $i$, and $\sigma_e^2 = 1 - J_0(2\pi f_D T i)^2$. For $f_D T = 0.01$ and $i = 5$ this is $1 - J_0(0.314)^2 = 0.048$. So even in the best case, holding the last pilot is much worse than interpolation over several pilots.

## Variations

- **Two dimensions.** OFDM places pilots on a grid in time and frequency and interpolates in both; see [comb pilot channel estimation](/comb-pilot-channel-estimation/) and [two-dimensional Wiener pilot interpolation](/two-dimensional-wiener-pilot-interpolation/). The same sampling rule holds in frequency, with the delay spread in place of the Doppler spread.
- **Simple interpolators.** Linear interpolation, a low-order polynomial, or [sinc interpolation](/sinc-interpolation/) with a window, instead of the Wiener filter. They need no knowledge of $R_c$ or $N_0$ but do not filter the noise as well.
- **Tracking.** A state model of the fading, such as an autoregressive model, and [Kalman channel tracking](/kalman-channel-tracking/) give causal estimates with no look-ahead.
- **Decision-directed refinement.** After a first pass, detected data symbols are used as extra pilots to improve the estimate.
- **Pilot blocks for dispersive channels.** On a channel with ISI, a block of pilots replaces the single symbol, and each block gives a [least squares](/least-squares-channel-estimation/) estimate of all taps.
- **No pilots.** [Differential PSK](/differential-phase-shift-keying/) detects the phase change between symbols and needs no estimate. For binary signals in slow Rayleigh fading, its error rate $1/(2(1 + \bar\gamma))$ is about twice the coherent value $1/(4\bar\gamma)$ at high SNR, a loss of 3 dB, and it does not handle multilevel amplitudes.

## Pitfalls

- **Spacing at the limit.** $P$ just below $1/(2 f_D T)$ satisfies the rule, but with finite $K$ and noise the error is already large. Keep a margin, and design for the highest speed the system must support.
- **Wrong Doppler in the filter.** The Wiener weights depend on $f_D$. A filter designed for a smaller Doppler than the real one cuts off part of the fading spectrum. A common choice is to design for the largest expected $f_D$.
- **Frequency offset.** A carrier frequency offset $\Delta f$ rotates $c[n]$ and shifts its spectrum, so the pilots must sample $f_D + |\Delta f|$, not $f_D$.
- **Edges and delay.** Near the start and the end of a burst there are pilots on one side only, and the error is larger. The look-ahead of $K/2$ frames adds delay.
- **Energy split.** Pilot energy improves the estimate but takes energy from the data. Neither extreme is good: with weak pilots the estimate is poor, and with strong pilots the data SNR falls.

## Exercises

1. At $f_c = 900$ MHz, $v = 25$ m/s and $T = 40\ \mu$s, find $f_D$ and the largest pilot spacing that the sampling rule allows.
2. Show that with $K = 1$, no noise and the nearest pilot at distance $i$, the best gain is $R_c(i)$ and the error is $1 - |R_c(i)|^2$.
3. Show that if $R_c(k) = 1$ for all $k$, a constant channel, the Wiener weights for $K$ pilots are equal and the error is $(N_0/E_p) / (K + N_0/E_p)$.
4. For a fixed total energy per frame, write the effective SNR of a data symbol as a function of the pilot energy fraction, using the model $y = \hat c\, x + (c - \hat c)\, x + w$, and find the best fraction when $K = 1$ and $c$ is constant.
5. With $f_D T = 0.01$ and $P = 60$, explain with the spectrum of the pilot samples why the error stays near 0.26 when the SNR grows.

## References
