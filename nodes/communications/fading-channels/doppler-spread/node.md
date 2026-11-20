---
tag: F9D53S
kind: definition
slug: doppler-spread
name: Doppler spread
aliases:
- Doppler spectrum width
area: communications/fading-channels
level: intro
summary: "The width of the Doppler spectrum of a channel that changes in time. At speed v and carrier f_c the largest shift is f_D = v f_c/c, and Clarke's model gives an RMS width of f_D/sqrt(2)."
prereqs: [multipath-fading]
see_also: [coherence-time, clarke-model, delay-spread, wssus-channel-model, jakes-fading-simulator, inter-carrier-interference, level-crossing-rate, rician-fading-channel]
sources:
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 5.4.3 (Doppler spread and coherence time) and Section 5.7.1 (Clarke's model and its Doppler spectrum)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.2.1 (the Doppler power spectrum under uniform scattering) and Section 3.3.3 (the Doppler power spectrum and the channel coherence time)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Section 2.3 (the Doppler spread D_s and its relation to the coherence time) and Table 2.1
  - paper: doi:10.1002/j.1538-7305.1968.tb00069.x
    title: R. H. Clarke, A statistical theory of mobile-radio reception, Bell System Technical Journal 47(6), 1968
    locator: pp. 957 to 1000 (the field at a moving receiver as a sum of plane waves with Doppler shifts, and its spectrum)
  - url: https://www.etsi.org/deliver/etsi_ts/136100_136199/136104/09.11.00_60/ts_136104v091100p.pdf
    title: 3GPP TS 36.104, Base Station radio transmission and reception (E-UTRA), Release 9 (ETSI TS 136 104 V9.11.0)
    locator: Annex B.2 (multipath fading propagation conditions with maximum Doppler frequencies of 5, 70 and 300 Hz)
---

The Doppler spread of a channel measures how much a pure tone is widened in frequency when it passes through a channel that changes in time. Each path reaches a moving receiver with its own Doppler shift, so a tone comes out as a band of frequencies. The width of that band, the Doppler spread, sets how fast the channel gain changes: the [coherence time](/coherence-time/) is of the order of its inverse. The Doppler spread is the frequency-domain dual of the [delay spread](/delay-spread/), with time and frequency exchanged.

## Definition

**Doppler shift of one path.** Let a receiver move at speed $v$ and let a plane wave at carrier frequency $f_c$ arrive at angle $\theta$ to the direction of motion. The path length shrinks at the rate $v\cos\theta$, so the phase of the received wave changes by $2\pi f_c v\cos\theta / c$ radians per second, with $c$ the speed of light. The path therefore has the Doppler shift

$$\nu = f_D \cos\theta, \qquad f_D = \frac{v f_c}{c}.$$

$f_D$ is the **maximum Doppler frequency**: every shift lies in $[-f_D, f_D]$. A moving transmitter or moving scatterers add their own terms, but the bound by the sum of the speeds remains.

**Doppler power spectrum.** Let $h(t)$ be the complex gain of a flat fading channel, or of one tap of a [tapped delay line](/tapped-delay-line-channel-model/), that is wide-sense stationary with the normalized autocorrelation

$$R(\Delta t) = \frac{\mathbb{E}[h(t + \Delta t)\, h^*(t)]}{\mathbb{E}|h(t)|^2}.$$

Its Fourier transform $S(\nu) = \int R(\Delta t) e^{-j 2\pi\nu\Delta t}\, d\Delta t$ is the **Doppler power spectrum**. It is non-negative and integrates to $R(0) = 1$ by the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/). $S(\nu)$ is the power received at Doppler shift $\nu$ when a tone of unit power is sent.

**Doppler spread.** Three measures are in use, and a value must say which one it is:

1. the **maximum Doppler frequency** $f_D$;
2. the **support width**, the width of the band where $S(\nu) > 0$, which is $2f_D$ when the shifts fill $[-f_D, f_D]$; Tse and Viswanath call the largest difference of Doppler shifts the Doppler spread $D_s$, so $D_s = 2f_D$ in that case;
3. the **RMS Doppler spread**
$$\sigma_\nu = \sqrt{\int (\nu - \bar\nu)^2 S(\nu)\, d\nu}, \qquad \bar\nu = \int \nu\, S(\nu)\, d\nu.$$

The RMS form is the one that enters bounds. The dual of Fleury's bound on the [coherence bandwidth](/coherence-bandwidth/) gives $|R(\Delta t)| \ge \cos(2\pi\sigma_\nu \Delta t)$ for $2\pi\sigma_\nu\Delta t \le \pi/2$, a theorem that holds for every Doppler spectrum. The Taylor expansion $e^{j 2\pi\bar\nu\Delta t} R(\Delta t) = 1 - 2\pi^2\sigma_\nu^2\Delta t^2 + O(\Delta t^3)$ shows that $\sigma_\nu$ alone fixes how fast the correlation starts to fall.

The definition uses only second-order statistics. It needs neither CSIR nor CSIT. A model with time-correlated fading must specify $S(\nu)$; block fading and fast fading replace it by the two extremes of a constant gain and a new independent gain per symbol.

**Clarke's model (a closed form under its assumptions).** If many scattered waves of equal mean power arrive in the horizontal plane with angles uniform on $[0, 2\pi)$, the [Clarke model](/clarke-model/) gives the spectrum

$$S(\nu) = \frac{1}{\pi f_D \sqrt{1 - (\nu/f_D)^2}}, \qquad |\nu| < f_D,$$

which is the density of $f_D\cos\theta$ for uniform $\theta$. Then $\bar\nu = 0$ and $\sigma_\nu^2 = f_D^2\,\mathbb{E}[\cos^2\theta] = f_D^2/2$, so $\sigma_\nu = f_D/\sqrt2 = 0.707 f_D$. The spectrum has peaks of infinite height at $\pm f_D$, where many angles give almost the same shift.

## Examples and non-examples

**Numbers.** With $c = 299\,792\,458$ m/s:

| speed | carrier | $f_D$ | $\sigma_\nu$ (Clarke) |
|---|---|---|---|
| $3$ km/h | $2.4$ GHz | $6.67$ Hz | $4.72$ Hz |
| $50$ km/h | $1.8$ GHz | $83.4$ Hz | $59.0$ Hz |
| $30$ m/s ($108$ km/h) | $900$ MHz | $90.1$ Hz | $63.7$ Hz |
| $30$ m/s | $2$ GHz | $200.1$ Hz | $141.5$ Hz |

The Doppler spread grows with both the speed and the carrier frequency. A move from $2$ GHz to $28$ GHz at the same speed multiplies it by $14$.

**LTE test conditions.** 3GPP TS 36.104 combines its delay profiles with maximum Doppler frequencies of $5$, $70$ and $300$ Hz, as in EPA 5 Hz, EVA 70 Hz and ETU 300 Hz. With a subcarrier spacing of $15$ kHz, $300$ Hz is $2\%$ of the spacing. This normalized Doppler $f_D/\Delta f$ is the quantity that sets the [inter-carrier interference](/inter-carrier-interference/) in OFDM.

**A line-of-sight path.** In a [Rician channel](/rician-fading-channel/) with factor $K$, a fixed direct path at angle $\theta_0$ adds a spectral line of weight $K/(K+1)$ at $f_D\cos\theta_0$. The mean $\bar\nu$ moves away from $0$. The spectrum is a mixture, so $\sigma_\nu^2 = \frac{f_D^2}{K+1}\left(\frac12 + \frac{K\cos^2\theta_0}{K+1}\right)$, which tends to $0$ as $K$ grows because more of the power sits at one frequency. For small $K$ and $\theta_0 = 0$ it can first rise a little: $K = 0.5$ gives $\sigma_\nu^2 = 0.556 f_D^2$ against $0.5 f_D^2$ at $K = 0$.

**Non-example: a single path.** One path seen by a receiver at constant speed gives a single shifted tone, $S(\nu) = \delta(\nu - f_D\cos\theta)$. The Doppler spread is zero and the gain $|h(t)|$ is constant: there is a frequency offset but no fading. Fading needs several paths with different shifts.

**Non-example: oscillator offset.** A carrier frequency offset between the transmitter and receiver oscillators shifts every path by the same amount. It moves $\bar\nu$ and leaves $\sigma_\nu$ unchanged, so it does not count as Doppler spread, although a receiver must correct both.

**Non-example: a fixed terminal.** A terminal that does not move can still see a small Doppler spread from moving scatterers such as cars, people or leaves. The value $f_D = 0$ from the formula with $v = 0$ is then wrong.

## Related definitions

- [Coherence time](/coherence-time/): the time over which the gain stays correlated, of the order of $1/f_D$.
- [Clarke model](/clarke-model/): the model that gives the U-shaped Doppler spectrum and the autocorrelation $J_0(2\pi f_D\Delta t)$.
- [Delay spread](/delay-spread/): the width of the power delay profile, the dual quantity on the delay axis.
- [WSSUS channel model](/wssus-channel-model/): the frame in which each delay has its own Doppler spectrum, given by the scattering function.
- [Jakes fading simulator](/jakes-fading-simulator/): a generator of fading waveforms with a set Doppler spread.
- [Level crossing rate](/level-crossing-rate/): the rate of fades, which is proportional to $f_D$.

## References
