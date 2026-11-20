---
tag: 8R216E
kind: concept
slug: multipath-fading
name: Multipath fading
aliases:
- small-scale fading
area: communications/fading-channels
level: intro
summary: "The fast change of a received signal as copies that arrive over different paths add with changing phases: deep fades occur about every half wavelength of movement."
prereqs: [free-space-path-loss]
see_also: [rayleigh-fading-channel, rician-fading-channel, nakagami-m-fading-channel, delay-spread, doppler-spread, coherence-time, coherence-bandwidth, maximal-ratio-combining]
sources:
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Section 2.3 (time and frequency coherence) and Section 2.4.2 (Rayleigh and Rician fading)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 5.1 (small-scale multipath propagation and the Doppler shift), Section 5.5 (types of small-scale fading) and Section 5.6 (Rayleigh and Ricean distributions)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.2.2 (envelope and power distributions) and Section 3.3 (wideband fading models)
  - paper: doi:10.1002/j.1538-7305.1968.tb00069.x
    title: R. H. Clarke, A statistical theory of mobile-radio reception, Bell System Technical Journal 47(6), 1968
    locator: pp. 957 to 1000 (many scattered waves from all directions around a moving receiver give a Gaussian field and a Rayleigh envelope)
---

Multipath fading is the fast change of the received signal that occurs when copies of the transmitted wave arrive over several paths and add with different phases. A movement of half a wavelength, 17 cm at 900 MHz, can change a sum of strong copies into a deep fade. It acts on a much smaller scale than [path loss](/log-distance-path-loss-model/) and [shadowing](/log-normal-shadowing/), and it is the reason that wireless links need diversity, coding over time or frequency, and fade margins.

## In plain words

A radio wave reflects from buildings, the ground and cars, so the receiver gets several copies of it. Each copy travels a different distance and arrives with its own delay and phase. When the copies are in step they add and the signal is strong; when they are out of step they cancel and the signal almost disappears. A small movement of the receiver, or of anything near it, changes the lengths of the paths and so the phases. The result is a signal that rises and falls many times per second while a car drives. If the delays are short compared with one symbol, the whole band fades together. If they are long, some frequencies fade while others do not, and the copies of one symbol overlap the next symbols.

## The idea

**The sum of the paths.** Path $i$ has an amplitude $a_i$ and a delay $\tau_i(t)$. For a transmitted baseband signal $x(t)$ at the carrier $f_c$, the received baseband signal is

$$y(t) = \sum_i a_i\, e^{-j 2 \pi f_c \tau_i(t)}\, x(t - \tau_i(t)) + w(t).$$

A change of $\lambda$ in the length of one path, which is a change of $1/f_c$ in its delay, turns its phase by a full $2 \pi$. At 900 MHz $\lambda = 0.333$ m, so the phases, and with them the sum, change over a few centimeters.

**Flat fading.** If all the delays are close, so that the [delay spread](/delay-spread/) is much smaller than the symbol time, then $x(t - \tau_i) \approx x(t - \tau)$ for every path. One complex gain multiplies the signal:

$$y = h x + w, \qquad h = \sum_i a_i e^{-j 2 \pi f_c \tau_i}, \qquad w \sim \mathcal{CN}(0, N_0).$$

This is the flat fading channel. Its statistics depend on the paths:

- many paths of similar strength and no dominant one: by the [central limit theorem](/central-limit-theorem/), $h$ is close to $\mathcal{CN}(0, \Omega)$, the [Rayleigh fading channel](/rayleigh-fading-channel/);
- one strong line-of-sight path plus scattered paths: the [Rician fading channel](/rician-fading-channel/);
- a fit with one more shape parameter: the [Nakagami-m fading channel](/nakagami-m-fading-channel/).

The instantaneous SNR is $\gamma = |h|^2 E_s / N_0$, and its mean is $\bar\gamma = \Omega E_s / N_0$.

**Frequency-selective fading.** If the delay spread is comparable with the symbol time, the channel is a filter with several taps, and its gain changes across the band. The width over which the gain stays nearly constant is the [coherence bandwidth](/coherence-bandwidth/), about the inverse of the delay spread. The [tapped delay line model](/tapped-delay-line-channel-model/) describes this case.

**Time variation.** A receiver moving at speed $v$ sees a path from direction $\theta$ shifted in frequency by $(v / \lambda) \cos\theta$. The largest shift is the Doppler frequency $f_D = v / \lambda$, and the spread of the shifts is the [Doppler spread](/doppler-spread/). The gain stays nearly constant over the [coherence time](/coherence-time/), about the inverse of the Doppler spread. Clarke 1968 derived the statistics for waves from all directions around a moving receiver; see the [Clarke model](/clarke-model/).

**How the time variation is modeled.** Three cases are common. In *block fading*, $h$ is constant over a block of symbols and independent from block to block. In *fast fading*, $h$ is independent from symbol to symbol, which models a channel after ideal [interleaving](/interleaving/). In *time-correlated fading*, $h$ follows a process with a given autocorrelation, for example the [Jakes simulator](/jakes-fading-simulator/). The receiver may know $h$ (CSIR, from [channel estimation](/channel-estimation/)), and the transmitter may know it too (CSIT, through feedback).

## Examples

**Two paths.** Let $h = 1 + a e^{j \phi}$ with $0 < a < 1$. As $\phi$ turns, $|h|$ moves between $1 - a$ and $1 + a$. The ratio of the strongest to the weakest power is $20 \log_{10}((1 + a)/(1 - a))$ dB: 25.58 dB for $a = 0.9$ and 9.54 dB for $a = 0.5$. Two paths of nearly equal strength give the deepest fades.

**Two paths in frequency.** If the second path arrives $\Delta\tau$ later, its phase is $2 \pi f \Delta\tau$ at the frequency $f$, so the nulls of $|h(f)|$ repeat every $1/\Delta\tau$ Hz. With $\Delta\tau = 1$ microsecond, there is a null every 1 MHz. A 200 kHz channel fades almost flat, and a 20 MHz channel sees about 20 nulls.

**Speed.** At 30 m/s (108 km/h), $f_D$ is 90.06 Hz at 900 MHz and 200.14 Hz at 2 GHz. The number of fades per second is of the order of $f_D$; the [level crossing rate](/level-crossing-rate/) gives the exact count for each depth.

**Depth of fades in Rayleigh fading.** With $\mathbb{E}|h|^2 = 1$, $\Pr[|h|^2 < x] = 1 - e^{-x}$. The power is more than 10 dB below its mean with probability 0.0952, and more than 20 dB below with probability 0.00995. A deep fade of 20 dB occurs about 1 percent of the time.

**Effect on the error rate.** For BPSK with coherent detection at $\bar\gamma = 10$ dB, the [AWGN channel](/additive-white-gaussian-noise-channel/) gives a [bit error rate](/bit-error-rate/) of $3.87 \cdot 10^{-6}$ and the Rayleigh channel gives $0.0233$. To reach $10^{-5}$, the Rayleigh channel needs a mean SNR of 43.98 dB. The errors come from the fades, not from the average noise.

## Where it is used

- **Link budgets.** A fade margin on top of the path loss and the shadowing margin covers the deep fades that the system must tolerate.
- **Diversity.** Independent copies of the signal rarely fade together. [Maximal ratio combining](/maximal-ratio-combining/), [selection combining](/selection-combining/), the [Alamouti code](/alamouti-code/) and coding with [interleaving](/interleaving/) all use this, and the [diversity order](/diversity-order/) measures the gain.
- **Multicarrier systems.** [OFDM](/orthogonal-frequency-division-multiplexing/) splits a frequency-selective channel into many narrow subcarriers, and each one sees flat fading.
- **Spread spectrum.** A [rake receiver](/rake-receiver/) resolves the paths of a wideband signal and combines them, so the multipath becomes a source of diversity.
- **MIMO.** Rich scattering makes the gains between antennas nearly independent, which [spatial multiplexing](/spatial-multiplexing/) needs.
- **Rate and scheduling.** [Adaptive modulation](/adaptive-modulation/) and [multiuser diversity](/multiuser-diversity/) send more data when the channel is strong.
- **Capacity.** The [ergodic capacity](/ergodic-capacity/) averages over the fades, and the [outage probability](/outage-probability/) measures how often a fixed rate fails.

## References
