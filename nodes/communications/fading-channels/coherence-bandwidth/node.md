---
tag: RBX2B1
kind: definition
slug: coherence-bandwidth
name: Coherence bandwidth
aliases:
- channel coherence bandwidth
area: communications/fading-channels
level: intro
summary: "The frequency separation over which channel gains stay correlated. A rule of thumb gives 1/(5 sigma_tau) at correlation 0.5, with sigma_tau the RMS delay spread."
prereqs: [delay-spread]
see_also: [delay-spread, coherence-time, wssus-channel-model, tapped-delay-line-channel-model, orthogonal-frequency-division-multiplexing, frequency-domain-equalization, diversity-order, two-dimensional-wiener-pilot-interpolation]
sources:
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 5.4.2 (coherence bandwidth, the rules 1/(50 sigma_tau) at correlation 0.9 and 1/(5 sigma_tau) at correlation 0.5) and Section 5.5 (flat and frequency-selective fading)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.3.2 (coherence bandwidth as the width of the spaced-frequency correlation function)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Section 2.3 (the coherence bandwidth W_c = 1/(2 T_d)) and Table 2.1
  - paper: "Bernard H. Fleury, An uncertainty relation for WSS processes and its application to WSSUS systems, IEEE Transactions on Communications 44(12), 1632 to 1634, 1996"
    locator: whole paper (the lower bound arccos(c)/(2 pi sigma_tau) on the coherence bandwidth at correlation level c)
  - url: https://www.etsi.org/deliver/etsi_ts/136100_136199/136104/09.11.00_60/ts_136104v091100p.pdf
    title: 3GPP TS 36.104, Base Station radio transmission and reception (E-UTRA), Release 9 (ETSI TS 136 104 V9.11.0)
    locator: Annex B.2 (the EPA and ETU delay profiles used in the examples)
---

The coherence bandwidth $B_c$ of a channel is the frequency separation over which the channel gains at two frequencies stay strongly correlated. Two tones closer than $B_c$ fade together; tones further apart fade almost independently. It is the frequency-domain partner of the [delay spread](/delay-spread/) $\sigma_\tau$: a theorem of Fleury gives $B_c \ge \arccos(c)/(2\pi\sigma_\tau)$ at correlation level $c$, and the rule of thumb $B_c \approx 1/(5\sigma_\tau)$ at level $0.5$ is in common use. Its time-domain counterpart is the [coherence time](/coherence-time/).

## Definition

**Frequency correlation.** Let $H(f, t)$ be the frequency response of the channel at time $t$. In the [WSSUS model](/wssus-channel-model/) with power delay profile $(\tau_l, P_l)$ and $\sum_l P_l = 1$, the correlation of the gains at two frequencies does not depend on $f$ or $t$:

$$R(\Delta f) = \frac{\mathbb{E}[H(f + \Delta f, t)\, H^*(f, t)]}{\mathbb{E}|H(f, t)|^2} = \sum_l P_l\, e^{-j 2\pi \Delta f \tau_l}.$$

The sum form holds because the taps of a [tapped delay line](/tapped-delay-line-channel-model/) are uncorrelated with $\mathbb{E}|h_l|^2 = P_l$, so all cross terms vanish. $R$ is the Fourier transform of the power delay profile, with $R(0) = 1$ and $|R(\Delta f)| \le 1$.

**Coherence bandwidth at level $c$.** For $0 < c < 1$,

$$B_c(c) = \min\{\Delta f > 0 : |R(\Delta f)| \le c\}.$$

It is the first frequency separation at which the correlation falls to $c$. Texts differ in the level: $0.9$ and $0.5$ are common. Some, such as Rappaport (Section 5.4.2), use the correlation of the envelopes $|H|$ instead of the complex gains. For Rayleigh fading the envelope correlation coefficient is close to $|R|^2$, so the two readings differ at the same $c$. A value of $B_c$ means little without its level and its reading.

The definition uses only second-order statistics. It needs neither CSIR nor CSIT, and it does not depend on whether the fading in time is block, fast or time-correlated.

**Rules of thumb.** Rappaport gives

$$B_c \approx \frac{1}{50\,\sigma_\tau} \ \text{at correlation } 0.9, \qquad B_c \approx \frac{1}{5\,\sigma_\tau} \ \text{at correlation } 0.5.$$

Both are rules, not theorems: the true $B_c$ depends on the shape of the profile and not only on $\sigma_\tau$. Tse and Viswanath define $W_c = 1/(2T_d)$ with $T_d$ the largest delay difference, as an order of magnitude only.

**Fleury's bound (a theorem).** For every power delay profile with RMS delay spread $\sigma_\tau > 0$,

$$|R(\Delta f)| \ge \cos(2\pi \sigma_\tau \Delta f) \quad \text{for } 0 \le 2\pi\sigma_\tau \Delta f \le \pi/2, \qquad \text{so} \qquad B_c(c) \ge \frac{\arccos c}{2\pi \sigma_\tau}.$$

*Proof.* Let $\bar\tau$ be the mean delay and $\theta_l = 2\pi\Delta f(\tau_l - \bar\tau)$. Then $|R| = |e^{j 2\pi\Delta f\bar\tau} R| \ge \operatorname{Re}(e^{j 2\pi\Delta f\bar\tau} R) = \sum_l P_l \cos\theta_l$, with $\sum_l P_l \theta_l = 0$ and $\sum_l P_l \theta_l^2 = s^2$, where $s = 2\pi\sigma_\tau\Delta f$. Fix $0 < s \le \pi/2$ and let $q(x) = \cos s - \frac{\sin s}{2s}(x^2 - s^2)$. The difference $\varphi(x) = \cos x - q(x)$ is even, and $\varphi'(x) = x\left(\frac{\sin s}{s} - \frac{\sin x}{x}\right)$. For $x \ge 0$: $\sin x/x$ decreases on $[0, \pi]$, and for $x > \pi$ it is below $1/\pi < 2/\pi \le \sin s/s$. So $\varphi$ decreases on $[0, s]$ and increases after $s$, and its minimum is $\varphi(s) = 0$. Hence $\cos x \ge q(x)$ for all real $x$, and
$$\sum_l P_l \cos\theta_l \ge \sum_l P_l\, q(\theta_l) = \cos s - \frac{\sin s}{2s}(s^2 - s^2) = \cos s.$$
For $|R| = c$ at $\Delta f = B_c(c)$, either $2\pi\sigma_\tau B_c \ge \pi/2 \ge \arccos c$ or $c \ge \cos(2\pi\sigma_\tau B_c)$, and both give the bound. $\square$

Two equal taps meet the bound with equality: their correlation is $|R| = |\cos(\pi\Delta f D)|$ for a spacing $D$, and $\sigma_\tau = D/2$. So the bound cannot be improved without more facts about the profile. The same proof applied to the Doppler spectrum bounds the coherence time.

**Consequences for the rules.** At $c = 0.5$ the bound is $\arccos(0.5)/(2\pi\sigma_\tau) = 1/(6\sigma_\tau)$, which is below the rule $1/(5\sigma_\tau)$. Two equal taps reach $|R| = 0.5$ at exactly $1/(6\sigma_\tau)$, so the rule $1/(5\sigma_\tau)$ can overstate $B_c(0.5)$. At $c = 0.9$ the bound is $0.0718/\sigma_\tau$ for the complex correlation and $\arccos\sqrt{0.9}/(2\pi\sigma_\tau) = 0.0512/\sigma_\tau$ when $|R|^2 = 0.9$ is used. Both exceed $1/(50\sigma_\tau) = 0.02/\sigma_\tau$, so the rule at $0.9$ always understates $B_c(0.9)$, by a factor of at least $2.5$ for the envelope reading and at least $3.6$ for the complex one.

### Pitfalls

- **Correlation can rise again.** $|R|$ need not decrease. For two equal taps $|R|$ returns to $1$ at $\Delta f = 1/D$. Use the first crossing, as in the definition.
- **Not a channel bandwidth.** $B_c$ is not the bandwidth that the channel passes. A wideband channel with a large delay spread has a small $B_c$.
- **One number per level.** A table that lists one $B_c$ without its level $c$ or without saying whether $|H|$ or $H$ is correlated cannot be compared with another table.

## Examples and non-examples

**Two equal taps.** Powers $1/2$ at $0$ and $1$ microsecond give $\sigma_\tau = 0.5$ microseconds and $|R(\Delta f)| = |\cos(\pi \Delta f \cdot 1\,\mu\text{s})|$. The correlation falls to $0.5$ at $333.3$ kHz, exactly the Fleury bound. The rule gives $1/(5\sigma_\tau) = 400$ kHz, where $|R| = 0.309$.

**Four taps.** Powers $(1/2, 1/4, 1/8, 1/8)$ at $(0, 1, 2, 4)$ microseconds have $\sigma_\tau = 1.3229$ microseconds (see [delay spread](/delay-spread/)). A direct search of $|R|$ gives

| level $c$ | exact $B_c(c)$ | Fleury bound | rule |
|---|---|---|---|
| $0.9$ | $55.6$ kHz | $54.3$ kHz | $1/(50\sigma_\tau) = 15.1$ kHz |
| $0.5$ | $285.8$ kHz | $126.0$ kHz | $1/(5\sigma_\tau) = 151.2$ kHz |

At $0.9$ the bound is almost tight; at $0.5$ the exact value is almost twice the rule.

**Exponential profile.** For $P(\tau) = e^{-\tau/\sigma_\tau}/\sigma_\tau$, $R(\Delta f) = 1/(1 + j 2\pi\sigma_\tau\Delta f)$ and $|R| = 1/\sqrt{1 + (2\pi\sigma_\tau\Delta f)^2}$. This is a closed form under the exponential assumption. It falls to $0.5$ at $\sqrt3/(2\pi\sigma_\tau) = 0.276/\sigma_\tau$ and to $0.9$ at $0.0771/\sigma_\tau$.

**LTE profiles.** For EPA ($\sigma_\tau = 43.1$ ns) the exact $B_c(0.9)$ is $1.84$ MHz and $B_c(0.5)$ is $4.60$ MHz. For ETU ($\sigma_\tau = 990.9$ ns) they are $83.7$ kHz and $942$ kHz, against the rules $20.2$ kHz and $201.8$ kHz. An LTE subcarrier spacing of $15$ kHz is well inside $B_c(0.9)$ even for ETU, so each [OFDM](/orthogonal-frequency-division-multiplexing/) subcarrier sees flat fading and a one-tap [frequency-domain equalizer](/frequency-domain-equalization/) is enough. A $20$ MHz carrier spans many coherence bandwidths, which gives frequency diversity to a coded system.

**Flat fading.** A narrowband signal of bandwidth $10$ kHz on the EPA profile sees the same gain over its whole band: $B \ll B_c$, and the channel acts as one complex gain.

**Non-example: the coherence time.** A channel can have a large $B_c$ and a short [coherence time](/coherence-time/), for example a fast car in an open area. The two describe different directions of the time-frequency plane and are set by different physics: delays for $B_c$, Doppler shifts for $T_c$.

**Non-example: one realization.** The frequency response of one draw of the channel can be nearly flat over a band much wider than $B_c$ by chance. $B_c$ is a property of the statistics, not of one draw.

## Related definitions

- [Delay spread](/delay-spread/): the width of the power delay profile, of which $R$ is the Fourier transform.
- [Coherence time](/coherence-time/): the same notion along the time axis, bounded by the Doppler spread.
- [WSSUS channel model](/wssus-channel-model/): the frame in which $R(\Delta f)$ does not depend on $f$.
- [Tapped delay line channel model](/tapped-delay-line-channel-model/): a model whose taps define $R$ by the sum above.
- [Diversity order](/diversity-order/): a band of width $W$ holds roughly $W/B_c$ independently fading pieces.
- [Two-dimensional Wiener pilot interpolation](/two-dimensional-wiener-pilot-interpolation/): pilot spacing in frequency must be well below $B_c$.

## References
