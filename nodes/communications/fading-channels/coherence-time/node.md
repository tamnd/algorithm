---
tag: VTX2J3
kind: definition
slug: coherence-time
name: Coherence time
aliases:
- channel coherence time
area: communications/fading-channels
level: intro
summary: "The time over which the channel gain stays correlated. For maximum Doppler f_D the rules of thumb 9/(16 pi f_D) and 0.423/f_D are in use; they differ by a factor of 2.4."
prereqs: [doppler-spread]
see_also: [doppler-spread, coherence-bandwidth, clarke-model, pilot-symbol-assisted-modulation, interleaving, kalman-channel-tracking, level-crossing-rate, sampling-theorem]
sources:
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 5.4.3 (Doppler spread and coherence time, the rules 9/(16 pi f_m) and 0.423/f_m) and Section 5.5 (fast and slow fading)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.2.1 (the autocorrelation J_0(2 pi f_D tau) under uniform scattering) and Section 3.3.3 (the channel coherence time)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Section 2.3 (the coherence time T_c = 1/(4 D_s)) and Table 2.1
  - paper: "Bernard H. Fleury, An uncertainty relation for WSS processes and its application to WSSUS systems, IEEE Transactions on Communications 44(12), 1632 to 1634, 1996"
    locator: whole paper (the uncertainty relation between the width of a WSS correlation function and the RMS width of its spectrum)
  - paper: doi:10.1002/j.1538-7305.1968.tb00069.x
    title: R. H. Clarke, A statistical theory of mobile-radio reception, Bell System Technical Journal 47(6), 1968
    locator: pp. 957 to 1000 (the correlation of the field at a moving receiver)
---

The coherence time $T_c$ of a channel is the time over which its complex gain stays strongly correlated with its present value. Over a span much shorter than $T_c$ the channel is nearly constant; samples further apart fade almost independently. It is the time-domain partner of the [Doppler spread](/doppler-spread/): it scales as $1/f_D$, where $f_D$ is the maximum Doppler frequency. Two rules of thumb, $9/(16\pi f_D)$ and $0.423/f_D$, are both in common use and differ by a factor of $2.4$. Its frequency-domain counterpart is the [coherence bandwidth](/coherence-bandwidth/).

## Definition

**Time correlation.** Let $h(t)$ be the complex gain of a flat fading channel, or of one tap of a [tapped delay line](/tapped-delay-line-channel-model/), that is wide-sense stationary. Its normalized autocorrelation is

$$R(\Delta t) = \frac{\mathbb{E}[h(t + \Delta t)\, h^*(t)]}{\mathbb{E}|h(t)|^2},$$

the inverse Fourier transform of the Doppler power spectrum $S(\nu)$.

**Coherence time at level $c$.** For $0 < c < 1$,

$$T_c(c) = \min\{\Delta t > 0 : |R(\Delta t)| \le c\}.$$

As for the coherence bandwidth, a value must state the level $c$ and whether it uses the correlation of $h$ or of the envelope $|h|$.

**Clarke's model.** Under isotropic scattering the [Clarke model](/clarke-model/) gives $R(\Delta t) = J_0(2\pi f_D\Delta t)$, with $J_0$ the Bessel function of the first kind and order zero. This is a closed form under the model's assumptions. Its values give:

| level | $T_c$ in Clarke's model | Fleury bound $\arccos(c)/(2\pi\sigma_\nu)$ |
|---|---|---|
| $\lvert R\rvert = 0.9$ | $0.1020/f_D$ | $0.1015/f_D$ |
| $\lvert R\rvert = 0.5$ | $0.2421/f_D$ | $0.2357/f_D$ |
| $\lvert R\rvert^2 = 0.5$ | $0.1793/f_D$ | |
| first zero of $J_0$ | $0.3827/f_D$ | |

**Fleury's bound (a theorem).** For every Doppler spectrum with RMS width $\sigma_\nu$, $|R(\Delta t)| \ge \cos(2\pi\sigma_\nu\Delta t)$ for $2\pi\sigma_\nu\Delta t \le \pi/2$, so $T_c(c) \ge \arccos(c)/(2\pi\sigma_\nu)$. The proof is the one on the [coherence bandwidth](/coherence-bandwidth/) page with delays replaced by Doppler shifts. For Clarke's spectrum $\sigma_\nu = f_D/\sqrt2$, and the bound is within $3\%$ of the true value at both levels in the table.

**The rules of thumb.** Rappaport (Section 5.4.3) gives two rules:

$$T_c \approx \frac{9}{16\pi f_D} = \frac{0.179}{f_D} \qquad \text{and} \qquad T_c \approx \frac{0.423}{f_D}.$$

The first is close to the lag at which $|J_0|^2 = 0.5$, that is, an envelope correlation of about $0.5$. The second is the geometric mean of $1/f_D$ and $9/(16\pi f_D)$: $\sqrt{9/(16\pi)} = 0.4231$. Both are rules, not theorems, and they differ by a factor of $0.423 \cdot 16\pi/9 = 2.36$. Tse and Viswanath use $T_c = 1/(4D_s)$ with $D_s = 2f_D$, that is $1/(8f_D) = 0.125/f_D$, as an order of magnitude.

The definition uses only second-order statistics and needs neither CSIR nor CSIT. It is what decides which of the time models applies. If a block of data is much shorter than $T_c$, block fading is a fair model. If a symbol is longer than $T_c$, the fading is fast. Between the two, the fading is time-correlated with the correlation $R(\Delta t)$.

**Sampling the channel.** Clarke's spectrum is zero outside $[-f_D, f_D]$, so by the [sampling theorem](/sampling-theorem/) pilots spaced at most $1/(2f_D)$ apart determine $h(t)$ in the limit of no noise. This is a theorem for any spectrum limited to $f_D$, and it sets the pilot spacing in [pilot-symbol-assisted modulation](/pilot-symbol-assisted-modulation/). In practice the spacing is chosen a few times smaller to leave room for noise and estimation error.

### Pitfalls

- **The rule $0.423/f_D$ lies past the first zero.** In Clarke's model $J_0(2\pi \cdot 0.423) = -0.124$. At that lag the gains are already uncorrelated and slightly anti-correlated, so the name "coherence time" fits the rule poorly if strong correlation is meant.
- **Correlation comes back.** $J_0$ oscillates. After its first zero, $|J_0|$ never exceeds $0.403$ again, so for $c > 0.403$ the first crossing is also the last. For smaller $c$ the first crossing is the only sensible choice.
- **Mixing rules.** The three rules give $1.79$, $4.23$ and $1.25$ ms at $f_D = 100$ Hz. A design that takes $T_c$ from one text and a target from another can be wrong by a factor of $3$.

## Examples and non-examples

**Speeds and carriers.** With $f_D = v f_c / c$ and $c = 299\,792\,458$ m/s, the three rules give, in milliseconds:

| speed | carrier | $f_D$ | $9/(16\pi f_D)$ | $0.423/f_D$ | $1/(8f_D)$ |
|---|---|---|---|---|---|
| $3$ km/h | $2$ GHz | $5.56$ Hz | $32.2$ | $76.1$ | $22.5$ |
| $60$ km/h | $2$ GHz | $111.2$ Hz | $1.61$ | $3.80$ | $1.12$ |
| $120$ km/h | $2$ GHz | $222.4$ Hz | $0.805$ | $1.90$ | $0.562$ |
| $120$ km/h | $3.5$ GHz | $389.2$ Hz | $0.460$ | $1.09$ | $0.321$ |
| $300$ km/h | $2$ GHz | $555.9$ Hz | $0.322$ | $0.761$ | $0.225$ |
| $60$ km/h | $28$ GHz | $1556.6$ Hz | $0.115$ | $0.272$ | $0.080$ |

An LTE subframe lasts $1$ ms. At $3$ km/h the channel is nearly constant over many subframes; at $300$ km/h it changes within one subframe, and pilots must be dense in time.

**Slow fading.** A $1$ Msymbol/s link at $60$ km/h and $2$ GHz has $T_s = 1$ microsecond, more than a thousand times shorter than $T_c$. Over a packet of $1000$ symbols the gain hardly changes, and a block fading model fits.

**Interleaving.** To make a code see independent fades, an [interleaver](/interleaving/) must spread neighbouring coded bits further apart than $T_c$. At $3$ km/h that is tens of milliseconds, which may exceed the delay a voice link can accept; the code then sees long bursts.

**Non-example: average fade duration.** The mean time the envelope stays below a level, given by the [level crossing rate](/level-crossing-rate/) analysis, also scales as $1/f_D$ but depends on the level. It is the length of a fade, not the length of the correlation.

**Non-example: a constant gain with a frequency offset.** A single path with a constant Doppler shift gives $h(t) = e^{j 2\pi\nu t}$ and $|R(\Delta t)| = 1$ for all lags. The coherence time is infinite: the phase turns, but a receiver that tracks the offset sees no fading.

## Related definitions

- [Doppler spread](/doppler-spread/): the width of the Doppler spectrum, which bounds $T_c$ from below through $\sigma_\nu$.
- [Coherence bandwidth](/coherence-bandwidth/): the same notion along the frequency axis.
- [Clarke model](/clarke-model/): the model behind the $J_0$ correlation used in the table.
- [Pilot-symbol-assisted modulation](/pilot-symbol-assisted-modulation/) and [Kalman channel tracking](/kalman-channel-tracking/): methods that follow $h(t)$ within its coherence time.
- [Level crossing rate](/level-crossing-rate/): the rate and length of fades, also on the time scale $1/f_D$.

## References
