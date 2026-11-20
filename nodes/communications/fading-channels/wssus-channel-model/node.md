---
tag: 9FSEGP
kind: model
slug: wssus-channel-model
name: WSSUS channel model
aliases:
- wide-sense stationary uncorrelated scattering
area: communications/fading-channels
level: advanced
summary: "Bello's model of a randomly time-varying linear channel whose gains are wide-sense stationary in time and uncorrelated across delays, described by a scattering function S(tau, nu)."
prereqs: [tapped-delay-line-channel-model, autocorrelation, power-spectral-density]
see_also: [tapped-delay-line-channel-model, delay-spread, doppler-spread, coherence-bandwidth, coherence-time, clarke-model, two-dimensional-wiener-pilot-interpolation, orthogonal-time-frequency-space-modulation]
sources:
  - paper: doi:10.1109/TCOM.1963.1088793
    title: P. A. Bello, Characterization of randomly time-variant linear channels, IEEE Transactions on Communications Systems CS-11(4), 1963
    locator: pp. 360 to 393 (the system functions in time-frequency dual pairs, and the WSS, US, WSSUS and quasi-WSSUS channels)
  - book: isbn:9780470741863
    title: Andreas F. Molisch, Wireless Communications, second edition, Wiley, 2011
    locator: Section 6.3 (system-theoretic description of wireless channels), Section 6.4 (the WSSUS model) and Section 6.5 (condensed parameters)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.3 (wideband fading models) and Section 3.3.4 (transforms for autocorrelation and scattering functions)
  - paper: "Bernard H. Fleury, An uncertainty relation for WSS processes and its application to WSSUS systems, IEEE Transactions on Communications 44(12), 1632 to 1634, 1996"
    locator: whole paper (bounds on the coherence bandwidth and coherence time of a WSSUS channel by its RMS delay and Doppler spreads)
---

The WSSUS model describes a randomly time-varying linear channel by its second-order statistics under two assumptions: the channel is wide-sense stationary (WS) in time, and paths at different delays are uncorrelated (US). Bello introduced it in 1963, together with four system functions that describe the channel in the time, frequency, delay and Doppler domains. Under the two assumptions all second-order statistics follow from one function of delay and Doppler, the scattering function $S(\tau, \nu)$. From it come the [delay spread](/delay-spread/), the [Doppler spread](/doppler-spread/), the [coherence bandwidth](/coherence-bandwidth/) and the [coherence time](/coherence-time/). The [tapped delay line model](/tapped-delay-line-channel-model/) is the WSSUS model with a finite set of delays. The [Saleh-Valenzuela](/saleh-valenzuela-model/) and [geometry-based stochastic](/geometry-based-stochastic-channel-model/) models are ways to produce particular scattering functions, and the geometric ones are WSSUS only over a small area.

## The machine

A linear time-varying channel maps the complex baseband input $x(t)$ to

$$y(t) = \int h(t, \tau)\, x(t - \tau)\, d\tau + w(t),$$

with $w$ white circular Gaussian noise. Bello's four system functions are linked by Fourier transforms in one variable at a time. In the usual modern notation:

| function | variables | relation |
|---|---|---|
| time-variant impulse response $h(t, \tau)$ | time, delay | the kernel above |
| time-variant transfer function $H(t, f)$ | time, frequency | $\int h(t, \tau)\, e^{-j 2\pi f\tau}\, d\tau$ |
| delay-Doppler spreading function $U(\tau, \nu)$ | delay, Doppler | $\int h(t, \tau)\, e^{-j 2\pi\nu t}\, dt$ |
| Doppler-variant transfer function $B(\nu, f)$ | Doppler, frequency | $\int H(t, f)\, e^{-j 2\pi\nu t}\, dt$ |

The spreading function shows the channel as a sum of delayed and Doppler-shifted copies of the input: $y(t) = \iint U(\tau, \nu)\, x(t - \tau)\, e^{j 2\pi\nu t}\, d\tau\, d\nu + w(t)$. Bello's paper uses other symbols and names for the same objects.

The channel is random, with $\mathbb{E}\,h(t, \tau) = 0$. The standing assumptions are:

- **Wide-sense stationary in time.** $\mathbb{E}[h(t + \Delta t, \tau)\, h^*(t, \tau')]$ depends on $t$ only through $\Delta t$.
- **Uncorrelated scattering.** Gains at different delays are uncorrelated:
  $$\mathbb{E}[h(t + \Delta t, \tau)\, h^*(t, \tau')] = R(\Delta t; \tau)\, \delta(\tau - \tau').$$
- **Often, Gaussian.** With $h$ jointly circular Gaussian, the second-order statistics define the whole law, and the channel at each delay and time is Rayleigh.
- **A local area.** The assumptions hold over a region of a few tens of wavelengths and a band in which the scatterers look the same. Over larger distances the statistics change; a model that tracks this is called non-stationary.

The model is of the channel only. It can describe block, fast or time-correlated fading: the time correlation $R(\Delta t; \tau)$ is what fixes which one. Pages that use it say whether the receiver has CSIR and the transmitter CSIT.

## What it counts

All second-order statistics come from $R(\Delta t; \tau)$ or, equivalently, from

$$S(\tau, \nu) = \int R(\Delta t; \tau)\, e^{-j 2\pi\nu\Delta t}\, d\Delta t,$$

the **scattering function**: the mean power that arrives with delay $\tau$ and Doppler shift $\nu$. Its marginals and its transform give the quantities used in design:

- **Power delay profile** $P(\tau) = R(0; \tau) = \int S(\tau, \nu)\, d\nu$, with RMS width the delay spread $\sigma_\tau$.
- **Doppler power spectrum** $S_D(\nu) = \int S(\tau, \nu)\, d\tau$, with RMS width the Doppler spread $\sigma_\nu$.
- **Spaced-time spaced-frequency correlation**
  $$R_H(\Delta t, \Delta f) = \mathbb{E}[H(t + \Delta t, f + \Delta f)\, H^*(t, f)] = \iint S(\tau, \nu)\, e^{j 2\pi(\nu\Delta t - \tau\Delta f)}\, d\tau\, d\nu,$$
  which depends on neither $t$ nor $f$. Its cut at $\Delta t = 0$ gives the coherence bandwidth and its cut at $\Delta f = 0$ the coherence time.
- **Spread factor.** The product of the delay and Doppler extents, for example $2\nu_{\max}\tau_{\max}$. A channel with a spread factor much less than $1$ is called *underspread*: it changes little over its own delay spread, so pilots can track it. Mobile radio is strongly underspread. ETU with $300$ Hz gives $2 \cdot 300 \cdot 5 \cdot 10^{-6} = 0.003$.

**A hand example.** Take two equal taps at $0$ and $1$ microsecond, each with Clarke Doppler at $f_D = 100$ Hz. Then $S(\tau, \nu) = \frac12[\delta(\tau) + \delta(\tau - 1\,\mu\text{s})]\, S_{\text{Clarke}}(\nu)$ and $R_H(\Delta t, \Delta f) = J_0(2\pi f_D\Delta t) \cdot \frac12(1 + e^{-j 2\pi\Delta f \cdot 1\,\mu\text{s}})$. At $\Delta t = 1$ ms and $\Delta f = 250$ kHz, $|R_H| = J_0(0.6283) \cdot |\tfrac12(1 - j)| = 0.9037 \cdot 0.7071 = 0.639$.

## Relation to other models

- **Tapped delay line.** If $R(\Delta t; \tau) = \sum_l R_l(\Delta t)\, \delta(\tau - \tau_l)$, the channel is a [TDL](/tapped-delay-line-channel-model/) with uncorrelated taps, and $S(\tau, \nu) = \sum_l \delta(\tau - \tau_l)\, S_l(\nu)$. Conversely, a band-limited WSSUS channel sampled in delay is a TDL, though the sampled taps are correlated when paths fall between samples.
- **Flat fading.** A channel with all power at one delay is a flat fading channel; with Gaussian gains and the Clarke spectrum it is the [Clarke model](/clarke-model/).
- **Separable scattering.** Many link models take $S(\tau, \nu) = P(\tau)\, S_D(\nu)$: every delay has the same Doppler spectrum. Then $R_H(\Delta t, \Delta f) = R_T(\Delta t)\, R_F(\Delta f)$, which is the form that [two-dimensional Wiener pilot interpolation](/two-dimensional-wiener-pilot-interpolation/) uses on an OFDM grid.
- **Geometric models.** In a [geometry-based stochastic model](/geometry-based-stochastic-channel-model/) delays, angles and Doppler shifts come from the positions of scatterers. Each delay then has its own Doppler spectrum (the scattering function is not separable), and as the terminal moves over a large area the statistics change, so the model is WSSUS only locally.
- **Multicarrier.** In [OFDM](/orthogonal-frequency-division-multiplexing/) the delay spread causes frequency selectivity and the Doppler spread causes [inter-carrier interference](/inter-carrier-interference/). [OTFS](/orthogonal-time-frequency-space-modulation/) places symbols directly on the delay-Doppler grid of the spreading function.

## Known results in the model

1. **Uncorrelated scattering is stationarity in frequency (a theorem).** Write $R_H(t, \Delta t; f, f')$ for $\mathbb{E}[H(t + \Delta t, f)\, H^*(t, f')]$. Substituting the transform,
   $$R_H = \iint \mathbb{E}[h(t + \Delta t, \tau)\, h^*(t, \tau')]\, e^{-j 2\pi(f\tau - f'\tau')}\, d\tau\, d\tau' .$$
   Under US the expectation is $R(\Delta t; \tau)\delta(\tau - \tau')$, so $R_H = \int R(\Delta t; \tau)\, e^{-j 2\pi(f - f')\tau}\, d\tau$, which depends only on $f - f'$. Conversely, if $R_H$ depends only on $f - f'$, the two-dimensional transform of the delay correlation is concentrated on $\tau = \tau'$. This is Bello's time-frequency duality: WSS in time matches uncorrelated Doppler shifts, and US matches WSS in frequency.
2. **The two-dimensional transform (a closed form under WSSUS).** Inserting $R(\Delta t; \tau) = \int S(\tau, \nu)\, e^{j 2\pi\nu\Delta t}\, d\nu$ into the result of item 1 gives the formula for $R_H(\Delta t, \Delta f)$ above. With $S \ge 0$ it follows that $|R_H(\Delta t, \Delta f)| \le R_H(0, 0)$.
3. **Fleury's uncertainty relations (a theorem).** With the normalized correlations, $|R_H(0, \Delta f)| / R_H(0, 0) \ge \cos(2\pi\sigma_\tau\Delta f)$ for $2\pi\sigma_\tau\Delta f \le \pi/2$, and the same with $\sigma_\nu$ and $\Delta t$. So the coherence bandwidth at level $c$ is at least $\arccos(c)/(2\pi\sigma_\tau)$ and the coherence time at least $\arccos(c)/(2\pi\sigma_\nu)$. The proof is on the [coherence bandwidth](/coherence-bandwidth/) page.
4. **Separable channels factor (a closed form).** If $S(\tau, \nu) = P(\tau) S_D(\nu)$, the double integral splits into $\int P(\tau)\, e^{-j 2\pi\tau\Delta f}\, d\tau \cdot \int S_D(\nu)\, e^{j 2\pi\nu\Delta t}\, d\nu$, the product of the frequency and time correlations.
5. **Received power.** For a deterministic input, $\mathbb{E}|y(t) - w(t)|^2 = \int P(\tau)\, |x(t - \tau)|^2\, d\tau$, because the cross terms between delays vanish. For an input of constant power $|x|^2 = p$ the mean received power is $p \int P(\tau)\, d\tau$, whatever the shape of the profile.

### Pitfalls

- **Local, not global.** WSSUS describes a small area. Path loss, shadowing and the set of clusters change as a terminal moves, and a long simulation with one scattering function misses this.
- **Uncorrelated paths, not uncorrelated taps.** US is a statement about the continuous delay axis. Taps of a sampled channel are correlated by the receive filter.
- **Scattering function and spreading function.** $U(\tau, \nu)$ is a random function of one channel; $S(\tau, \nu)$ is its mean power density, $\mathbb{E}[U(\tau, \nu) U^*(\tau', \nu')] = S(\tau, \nu)\, \delta(\tau - \tau')\, \delta(\nu - \nu')$ under WSSUS. Mixing them up confuses one realization with the statistics.
- **Sign conventions.** Texts differ in the sign of the exponent in $H(t, f)$ and in $R_H$. The magnitudes, and every spread and coherence value, do not depend on the convention.

## References
