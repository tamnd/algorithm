---
tag: Y8DDW4
kind: definition
slug: level-crossing-rate
name: Level crossing rate
aliases:
- LCR
- average fade duration
area: communications/fading-channels
level: core
summary: "The mean number of times per second that a fading envelope crosses a level going down. In Clarke's model it is sqrt(2 pi) f_D rho e^(-rho^2) at level rho relative to the RMS value."
prereqs: [clarke-model]
see_also: [clarke-model, rayleigh-fading-channel, doppler-spread, coherence-time, outage-probability, gilbert-elliott-channel, interleaving, jakes-fading-simulator]
sources:
  - paper: doi:10.1002/j.1538-7305.1944.tb00874.x
    title: S. O. Rice, Mathematical analysis of random noise, Bell System Technical Journal 23(3), 1944
    locator: pp. 282 to 332 (Parts I and II, shot noise, power spectra and correlation functions)
  - paper: doi:10.1002/j.1538-7305.1945.tb00453.x
    title: S. O. Rice, Mathematical analysis of random noise (concluded), Bell System Technical Journal 24(1), 1945
    locator: pp. 46 to 156 (Part III, statistical properties of random noise, with Section 3.3 on the expected number of zeros per second)
  - book: isbn:9780780310698
    title: William C. Jakes (editor), Microwave Mobile Communications, Wiley, 1974; reissued by IEEE Press, 1994
    locator: the chapter on multipath interference (the level crossing rate and the duration of fades of the Rayleigh envelope under uniform angles of arrival)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.2.3 (level crossing rate and average fade duration, equation 3.44)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 5.7.3 (level crossing and fading statistics)
---

The level crossing rate $N_R$ of a fading channel is the mean number of times per second that the envelope $|h(t)|$ crosses a level $R$ in the downward direction. Together with the **average fade duration** $\bar t_R$, the mean time the envelope stays below $R$ after such a crossing, it describes how fades come in time: how often, and for how long. The two numbers are different quantities: $N_R$ is a rate and $\bar t_R$ is a time, and their product is the fraction of time spent below $R$. In [Clarke's model](/clarke-model/) both have closed forms that go back to Rice's analysis of random noise: $N_R = \sqrt{2\pi} f_D \rho e^{-\rho^2}$ at the level $\rho$ relative to the RMS envelope.

## Definition

**Crossings.** Let $r(t) = |h(t)|$ be the envelope of a stationary fading process with mean power $\Omega = \mathbb{E}[r^2]$, and let $R > 0$. A downward crossing of $R$ is a time $t_0$ at which $r(t_0) = R$ and $r$ goes from above $R$ to below it. The **level crossing rate** is

$$N_R = \lim_{T \to \infty} \frac{\text{number of downward crossings of } R \text{ in } [0, T]}{T},$$

which for a stationary ergodic process equals the expected number of downward crossings per second. It is usual to give the level in normalized form, $\rho = R/\sqrt\Omega$, so that $\rho = 1$ (0 dB) is the RMS value and $\rho = 0.1$ is $20$ dB below it. A stationary process crosses upward as often as downward, so $N_R$ also counts upward crossings.

**Average fade duration.** A fade below $R$ starts at a downward crossing and ends at the next upward crossing. Over a long time $T$ the envelope is below $R$ for a total of about $T \Pr[r < R]$ seconds, split into about $N_R T$ fades. So the average fade duration is

$$\bar t_R = \frac{\Pr[r < R]}{N_R}.$$

**Rice's formula (a theorem).** If $r(t)$ is differentiable and $r(t)$ and its derivative $\dot r(t)$ have a joint density $p(r, \dot r)$, then

$$N_R = \int_0^\infty \dot r\, p(R, \dot r)\, d\dot r.$$

The idea: in a short interval $dt$, a crossing upward happens when $r$ lies in $(R - \dot r\, dt, R)$ with slope $\dot r > 0$, an event of probability $\int_0^\infty p(R, \dot r)\, \dot r\, dt\, d\dot r$. Rice derived the rate of zeros of a Gaussian process this way and used the same joint statistics of a process and its derivative for the envelope (Rice 1944 and 1945).

**Rayleigh fading with a symmetric Doppler spectrum (a closed form under these assumptions).** Let $h = h_I + j h_Q$ be a circular complex Gaussian process with mean power $\Omega$ and a Doppler spectrum that is even about $0$, with RMS width $\sigma_\nu$. Then

$$N_R = 2\sqrt\pi\, \sigma_\nu\, \rho\, e^{-\rho^2}, \qquad \bar t_R = \frac{e^{\rho^2} - 1}{2\sqrt\pi\, \sigma_\nu\, \rho}.$$

*Proof.* Each of $h_I$ and $h_Q$ has variance $\Omega/2$ and autocorrelation $r_I(\tau)$. Since the spectrum is even, $h_I(t)$, $h_Q(t)$, $\dot h_I(t)$ and $\dot h_Q(t)$ are uncorrelated at the same $t$, so they are independent Gaussian variables. The derivatives have variance $b = -r_I''(0) = (2\pi)^2 \cdot \frac{\Omega}{2}\sigma_\nu^2 = 2\pi^2\sigma_\nu^2\Omega$. Write $h_I = r\cos\phi$ and $h_Q = r\sin\phi$. From $r^2 = h_I^2 + h_Q^2$, $\dot r = \dot h_I\cos\phi + \dot h_Q\sin\phi$. Given $(r, \phi)$, this is a sum of independent Gaussians with total variance $b(\cos^2\phi + \sin^2\phi) = b$. So $\dot r \sim \mathcal N(0, b)$, independent of $r$, and $p(R, \dot r) = p(R)\, \frac{1}{\sqrt{2\pi b}} e^{-\dot r^2/(2b)}$ with the Rayleigh density $p(R) = \frac{2R}{\Omega} e^{-R^2/\Omega}$. Rice's formula gives

$$N_R = p(R) \int_0^\infty \frac{\dot r}{\sqrt{2\pi b}} e^{-\dot r^2/(2b)}\, d\dot r = p(R)\sqrt{\frac{b}{2\pi}} = \frac{2\rho e^{-\rho^2}}{\sqrt\Omega} \cdot \sqrt{\pi\Omega}\,\sigma_\nu = 2\sqrt\pi\,\sigma_\nu\,\rho\, e^{-\rho^2}.$$

With $\Pr[r < R] = 1 - e^{-\rho^2}$, the formula for $\bar t_R$ follows. $\square$

**Clarke's model.** The Clarke spectrum has $\sigma_\nu = f_D/\sqrt2$, so

$$N_R = \sqrt{2\pi}\, f_D\, \rho\, e^{-\rho^2}, \qquad \bar t_R = \frac{e^{\rho^2} - 1}{\rho\, f_D \sqrt{2\pi}}.$$

These are the formulas of Jakes (1974) and of Goldsmith (Section 3.2.3), and they are closed forms under the assumptions of the model: isotropic scattering, no line of sight, a stationary process.

**Properties.** For Rayleigh fading with an even spectrum:

1. *Scaling.* $N_R$ is proportional to $\sigma_\nu$ and $\bar t_R$ to $1/\sigma_\nu$. Doubling the speed doubles the rate of fades and halves their length.
2. *Most crossings at $-3$ dB.* $\rho e^{-\rho^2}$ is largest at $\rho = 1/\sqrt2$. In Clarke's model the maximum rate is $\sqrt\pi e^{-1/2} f_D = 1.0750 f_D$.
3. *Deep fades.* For $\rho \ll 1$, $N_R \approx \sqrt{2\pi} f_D \rho$ and $\bar t_R \approx \rho/(f_D\sqrt{2\pi})$. Each $10$ dB lower level cuts the rate of fades by about $\sqrt{10} = 3.16$ and their length by the same factor, so the time spent below the level falls by $10$.
4. *Product.* $N_R\, \bar t_R = \Pr[r < R] = 1 - e^{-\rho^2}$, the [outage probability](/outage-probability/) at that level.

## Examples and non-examples

**Check values.** In Clarke's model, at the level $\rho = 1$: $N_R/f_D = \sqrt{2\pi}/e = 0.92214$ and $\bar t_R f_D = (e - 1)/\sqrt{2\pi} = 0.68550$. Their product is $1 - e^{-1} = 0.63212$. More values:

| level | $\rho$ | $N_R/f_D$ | $\bar t_R f_D$ | $\Pr[r < R]$ |
|---|---|---|---|---|
| $0$ dB | $1$ | $0.92214$ | $0.68550$ | $0.6321$ |
| $-3$ dB | $0.70711$ | $1.07505$ | $0.36600$ | $0.3935$ |
| $-10$ dB | $0.31623$ | $0.71723$ | $0.13268$ | $0.0952$ |
| $-20$ dB | $0.1$ | $0.24817$ | $0.04009$ | $0.00995$ |
| $-30$ dB | $0.03162$ | $0.07919$ | $0.01262$ | $0.00100$ |

**A car at 108 km/h.** At $v = 30$ m/s and $f_c = 900$ MHz, $f_D = 90.06$ Hz. The envelope falls below its RMS value $83.0$ times per second, for $7.61$ ms on average. It falls $10$ dB below $64.6$ times per second for $1.47$ ms, and $20$ dB below $22.4$ times per second for $0.445$ ms. At $270$ kbit/s, a $20$ dB fade spans about $120$ bits, so a code needs an [interleaver](/interleaving/) deeper than that.

**A walker.** At $3$ km/h and $2.4$ GHz, $f_D = 6.67$ Hz. Fades $10$ dB deep come $4.8$ times per second and last $19.9$ ms each. These are much longer than at vehicle speeds, which is why slow terminals suffer from long bursts of errors.

**Estimating from a sample path.** On a sampled envelope $r[k] = r(k\Delta t)$, count the $k$ with $r[k-1] \ge R > r[k]$ and divide by the length of the record; divide the time below $R$ by that count to get $\bar t_R$. The sampling interval must be well below $\bar t_R$, or short fades fall between samples.

```pseudo id=main
LCR-AFD(ρ, f_D)                       ▷ Clarke's model, ρ = R / √Ω
L1  N ← √(2π) · f_D · ρ · e^(-ρ²)
L2  P ← 1 - e^(-ρ²)                    ▷ Pr[r < R] for a Rayleigh envelope
L3  return N, P / N

COUNT-CROSSINGS(r[0..n-1], R, Δt)     ▷ estimates from a sampled envelope
L4  c ← number of k in 1..n-1 with r[k-1] ≥ R > r[k]
L5  b ← number of k in 0..n-1 with r[k] < R
L6  return c / (n Δt), (b · Δt) / c
```

The implementation follows this outline. Its tests check the table above and the proof's general formula, and they count crossings on sample paths made by summing $32$ sinusoids with random angles and phases, a method close to the [Zheng and Xiao simulator](/zheng-xiao-fading-simulator/). The counts agree with the closed forms within a stated tolerance, not exactly, because such a sum is only close to Gaussian.

**Non-example: block fading.** A block fading model holds $h$ fixed over a block and redraws it at the next one. The envelope jumps at the block edges and is not differentiable, so Rice's formula does not apply. The number of crossings per second depends on the block length, not on any Doppler spectrum.

**Non-example: the coherence time.** The [coherence time](/coherence-time/) is a lag at which the correlation of $h$ falls to a set value. It does not depend on a level. $\bar t_R$ does: in Clarke's model, fades below $-20$ dB last $0.040/f_D$, and the coherence time at correlation $0.5$ is $0.242/f_D$.

**Non-example: the rate of the power.** The power $|h|^2$ crosses $R^2$ exactly when $|h|$ crosses $R$, so it has the same crossing rate at the matching level. Quoting $N_R$ against a level in dB of power and a level in dB of amplitude gives the same table only because $20\log_{10}\rho = 10\log_{10}\rho^2$.

## Related definitions

- [Clarke model](/clarke-model/): the model behind the closed forms on this page.
- [Rayleigh fading channel](/rayleigh-fading-channel/): the first-order distribution $\Pr[r < R] = 1 - e^{-\rho^2}$.
- [Doppler spread](/doppler-spread/): $\sigma_\nu$, which sets the scale of $N_R$.
- [Outage probability](/outage-probability/): the fraction of time below a level, equal to $N_R\, \bar t_R$.
- [Gilbert-Elliott channel](/gilbert-elliott-channel/): a two-state model of good and bad periods whose transition rates can be fitted to $N_R$ and $\bar t_R$.
- [Jakes fading simulator](/jakes-fading-simulator/): a generator whose crossing rate is a common test.

## References
