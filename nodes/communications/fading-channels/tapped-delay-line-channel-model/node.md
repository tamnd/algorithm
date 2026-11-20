---
tag: CCPRAH
kind: model
slug: tapped-delay-line-channel-model
name: Tapped delay line channel model
aliases:
- TDL channel model
area: communications/fading-channels
level: core
summary: "The channel as an FIR filter with time-varying taps: y(t) = sum_l h_l(t) x(t - tau_l) + w(t), with uncorrelated fading taps whose mean powers form the power delay profile."
prereqs: [multipath-fading, rayleigh-fading-channel, fir-filter]
see_also: [wssus-channel-model, delay-spread, coherence-bandwidth, clarke-model, saleh-valenzuela-model, geometry-based-stochastic-channel-model, orthogonal-frequency-division-multiplexing, rake-receiver]
sources:
  - book: isbn:9780470741863
    title: Andreas F. Molisch, Wireless Communications, second edition, Wiley, 2011
    locator: Section 7.3 (wideband models), Section 7.3.1 (tapped delay line models) and Section 7.3.2 (models for the power delay profile)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Chapter 2 (the discrete-time baseband model, in which the sample-spaced taps are sinc-weighted sums of the path gains)
  - url: https://www.etsi.org/deliver/etsi_ts/136100_136199/136104/09.11.00_60/ts_136104v091100p.pdf
    title: 3GPP TS 36.104, Base Station radio transmission and reception (E-UTRA), Release 9 (ETSI TS 136 104 V9.11.0)
    locator: Annex B.2 (multipath fading propagation conditions, the EPA, EVA and ETU tapped delay line profiles and their maximum Doppler frequencies)
  - url: https://www.etsi.org/deliver/etsi_tr/138900_138999/138901/18.00.00_60/tr_138901v180000p.pdf
    title: 3GPP TR 38.901 V18.0.0 (Release 18), Study on channel model for frequencies from 0.5 to 100 GHz
    locator: Clause 7.7.2 (the TDL-A to TDL-E models with normalized delays) and Clause 7.7.3 (scaling of the delays to a wanted delay spread)
---

The tapped delay line (TDL) model writes a frequency-selective fading channel as a finite impulse response filter whose tap gains are random processes in time. Each tap stands for a group of paths at one delay; its mean power is one entry of the power delay profile, and its gain fades as in a flat fading channel. It is the working model of link-level simulation and of the standard test profiles of 3GPP. The [WSSUS model](/wssus-channel-model/) is the statistical frame that the TDL fills with a finite set of delays; the [Saleh-Valenzuela model](/saleh-valenzuela-model/) and the [geometry-based stochastic model](/geometry-based-stochastic-channel-model/) are ways to choose the delays and powers from measurements or from geometry.

## The machine

The input is a complex baseband signal $x(t)$ and the output is

$$y(t) = \sum_{l=0}^{L-1} h_l(t)\, x(t - \tau_l) + w(t), \qquad h(t, \tau) = \sum_{l=0}^{L-1} h_l(t)\, \delta(\tau - \tau_l),$$

with $w(t)$ white circular Gaussian noise of spectral density $N_0$. The parameters are:

- the number of taps $L$ and the delays $0 = \tau_0 < \tau_1 < \cdots < \tau_{L-1}$ in seconds;
- the mean tap powers $P_l = \mathbb{E}|h_l(t)|^2$, normalized so that $\sum_l P_l = 1$; path loss and shadowing scale all of them together;
- the law of each tap process $h_l(t)$.

The standing assumptions are:

- **Rayleigh or Rician taps.** Each $h_l(t)$ is a zero-mean circular complex Gaussian process, so $|h_l|$ is Rayleigh. Some profiles give the first tap a fixed line-of-sight part, which makes it Rician.
- **Uncorrelated scattering.** Different taps are independent. Combined with stationarity in time this is the WSSUS assumption.
- **Time behavior.** The taps are constant over a block and independent between blocks (block fading), redrawn every symbol (fast fading), or time-correlated with a Doppler spectrum, most often the [Clarke spectrum](/clarke-model/) with maximum Doppler $f_D$.
- **Channel knowledge.** The model is of the channel only. A receiver with CSIR knows the $h_l(t)$, for example from [channel estimation](/channel-estimation/); there is no CSIT unless the page that uses the model says so.

With symbols of energy $E_s$ the mean SNR is $\bar\gamma = E_s/N_0 \cdot \sum_l P_l = E_s/N_0$.

**Sampled form.** A receiver that samples at rate $W = 1/T_s$ with an ideal band-limited front end sees the discrete-time [FIR filter](/fir-filter/)

$$y[n] = \sum_k g_k[n]\, x[n - k] + w[n], \qquad g_k[n] = \sum_l h_l(nT_s)\, \operatorname{sinc}(k - \tau_l W),$$

a time-varying [discrete convolution](/discrete-convolution/). A path whose delay is not a multiple of $T_s$ leaks into several sample-spaced taps by [sinc interpolation](/sinc-interpolation/). The standard profiles give $\tau_l$ and $P_l$; the sampled taps $g_k$ follow from them.

## What it counts

**The frequency response.** At time $t$,

$$H(f, t) = \sum_l h_l(t)\, e^{-j 2\pi f \tau_l}.$$

At each frequency $H(f, t)$ is a sum of independent circular Gaussians with total variance $\sum_l P_l = 1$, so every frequency, and every [OFDM](/orthogonal-frequency-division-multiplexing/) subcarrier, sees Rayleigh fading with the same mean power.

**Correlation across frequency.** Because the taps are uncorrelated,

$$\mathbb{E}[H(f + \Delta f, t)\, H^*(f, t)] = \sum_l P_l\, e^{-j 2\pi \Delta f \tau_l},$$

the Fourier transform of the power delay profile. Its width is the [coherence bandwidth](/coherence-bandwidth/), and the RMS width of the profile is the [delay spread](/delay-spread/) $\sigma_\tau$. The time correlation of each tap is set by its Doppler spectrum: $\mathbb{E}[h_l(t + \Delta t) h_l^*(t)] = P_l J_0(2\pi f_D\Delta t)$ for Clarke taps.

**Intersymbol interference and OFDM.** A single-carrier link at symbol period $T$ sees each symbol smeared over about $\tau_{L-1}/T$ later symbols, the [intersymbol interference](/intersymbol-interference/) that an equalizer must undo. An OFDM link with a [cyclic prefix](/cyclic-prefix/) longer than $\tau_{L-1}$ and a channel constant over one symbol turns the filter into $Y[k] = H[k] X[k] + W[k]$ with $H[k] = H(k\Delta f_{sc})$, one complex gain per subcarrier.

**Diversity.** If the receiver resolves the $L$ taps, a [rake receiver](/rake-receiver/) or an ideal equalizer can combine their independent fades.

### A two-tap example

Take $L = 2$ with $P_0 = P_1 = 1/2$ at $\tau_0 = 0$ and $\tau_1 = T_s$, and block fading. Then $H(f) = h_0 + h_1 e^{-j 2\pi f T_s}$ and the frequency correlation is $\frac12 + \frac12 e^{-j 2\pi\Delta f T_s}$. At $\Delta f = 1/(2T_s)$ the correlation is $\frac12 - \frac12 = 0$: the gains $H(0) = h_0 + h_1$ and $H(1/(2T_s)) = h_0 - h_1$ are independent, although they come from the same two taps. With $\sigma_\tau = T_s/2$, the rule $B_c \approx 1/(5\sigma_\tau)$ gives $0.4/T_s$, while the true correlation falls to $0.5$ at $1/(3T_s)$.

## Relation to other models

- **Flat fading.** With $L = 1$ the model is the [Rayleigh fading channel](/rayleigh-fading-channel/) (or the [Rician](/rician-fading-channel/) one if the tap has a fixed part).
- **WSSUS.** A TDL with independent taps that are each stationary in time is a WSSUS channel with a discrete delay axis. Its scattering function is $S(\tau, \nu) = \sum_l P_l\, \delta(\tau - \tau_l)\, S_l(\nu)$, where $S_l$ is the Doppler spectrum of tap $l$, normalized to integrate to $1$. The [WSSUS model](/wssus-channel-model/) covers continuous delay profiles and general scattering functions.
- **Standard profiles.** 3GPP TS 36.104, Annex B.2, defines EPA, EVA and ETU with 7, 9 and 9 taps, RMS delay spreads of 43, 357 and 991 ns and maximum Doppler frequencies of 5, 70 or 300 Hz. 3GPP TR 38.901, Clause 7.7.2, defines TDL-A to TDL-E with delays normalized to a delay spread of 1. Clause 7.7.3 scales them by $\tau_{\text{scaled}} = \tau_{\text{model}} \cdot \text{DS}_{\text{desired}}$, with example spreads from 10 to 1000 ns; TDL-D and TDL-E have a Rician first tap. These profiles are measurements condensed into fits, not results of a theory.
- **Clustered and geometric models.** The [Saleh-Valenzuela model](/saleh-valenzuela-model/) gives a random clustered delay profile; sampling it gives a TDL with random delays. A [geometry-based stochastic model](/geometry-based-stochastic-channel-model/) or a clustered delay line adds angles of departure and arrival to each path, which matter for several antennas; for one antenna at each end the angles fold into the tap gains and the result is a TDL.
- **Sequences of states.** The [Gilbert-Elliott channel](/gilbert-elliott-channel/) models the effect of fading on bits; the TDL models the waveform.

## Known results in the model

1. **Rayleigh at every frequency (a theorem under the Gaussian assumption).** $H(f, t)$ is a linear combination of independent circular Gaussians, hence circular Gaussian with variance $\sum_l P_l |e^{-j 2\pi f\tau_l}|^2 = \sum_l P_l = 1$. So the frequency response has a Rayleigh envelope at each frequency, whatever the profile.
2. **The frequency correlation (a closed form under uncorrelated scattering).** All cross terms $\mathbb{E}[h_l h_m^*]$ with $l \ne m$ vanish, which gives the formula above. Fleury's bound then holds: $|R(\Delta f)| \ge \cos(2\pi\sigma_\tau\Delta f)$ for $2\pi\sigma_\tau\Delta f \le \pi/2$, with equality for the two-tap example; see [coherence bandwidth](/coherence-bandwidth/).
3. **Energy of the sampled taps (a theorem).** For band-limited sinc pulses, $\sum_k \operatorname{sinc}(k - a)\operatorname{sinc}(k - b) = \operatorname{sinc}(a - b)$ for all real $a$ and $b$. Hence $\sum_k |g_k|^2 = \sum_{l, m} h_l h_m^* \operatorname{sinc}((\tau_l - \tau_m)W)$, and taking the mean with independent taps gives $\mathbb{E}\sum_k |g_k|^2 = \sum_l P_l$. The sampled taps keep the mean energy, but they are correlated with one another when the paths fall between samples.
4. **Diversity order $L$ (a theorem under resolvable paths and the matched filter bound).** For one isolated symbol and perfect CSIR, the combined SNR is $\frac{E_s}{N_0}\sum_l |h_l|^2$. With $L$ independent Rayleigh taps of equal power $1/L$, BPSK has the error probability of $L$-branch [maximal ratio combining](/maximal-ratio-combining/) at mean branch SNR $\bar\gamma/L$, which falls as $\bar\gamma^{-L}$: the [diversity order](/diversity-order/) is $L$. In the two-tap example at $\bar\gamma = 10$ dB this bound is $5.53 \cdot 10^{-3}$, against $0.0233$ for a single Rayleigh tap. The bound ignores the intersymbol interference between symbols, so a real receiver on a stream of symbols does no better than it.
5. **Scaling (an identity).** Multiplying every delay by $a$ multiplies $\sigma_\tau$ by $a$ and replaces $R(\Delta f)$ by $R(a\Delta f)$. This is why TR 38.901 can publish one normalized table per profile.

### Pitfalls

- **Linear powers.** The profiles list powers in dB. Convert to linear values and normalize before use; for EPA the linear powers sum to $3.11$, not $1$.
- **Rounding delays to the sample grid.** Moving each tap to the nearest sample changes the frequency correlation. At a $30.72$ MHz sample rate ($T_s = 32.6$ ns), the EPA taps at 30, 70, 90 and 110 ns fall on non-integer sample positions; rounding them is a further approximation, not part of the standard.
- **Correlated sampled taps.** Even with independent path taps, the sample-spaced taps $g_k$ are correlated. A simulator that draws the $g_k$ as independent Rayleigh gains with the same powers simulates a different channel.
- **Independent Doppler per tap.** Each tap needs its own fading process. Running copies of one generator with the same seed makes all taps fade together and removes the frequency selectivity.
- **Measurements, not laws.** The 3GPP profiles summarize measurement campaigns and are meant for comparing systems. A real site can have a different delay spread and shape.

## References
