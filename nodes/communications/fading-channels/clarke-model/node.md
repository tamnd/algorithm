---
tag: 2J0WV7
kind: model
slug: clarke-model
name: Clarke model
aliases:
- "Clarke's model"
- Jakes Doppler spectrum
area: communications/fading-channels
level: core
summary: "A receiver moving through isotropic scattering in the plane. It gives Rayleigh fading in time with autocorrelation Omega J0(2 pi f_D tau) and a U-shaped Doppler spectrum on |f| < f_D."
prereqs: [rayleigh-fading-channel, doppler-spread]
see_also: [rayleigh-fading-channel, doppler-spread, coherence-time, level-crossing-rate, jakes-fading-simulator, zheng-xiao-fading-simulator, filtered-gaussian-fading-simulator, geometry-based-stochastic-channel-model]
sources:
  - paper: doi:10.1002/j.1538-7305.1968.tb00069.x
    title: R. H. Clarke, A statistical theory of mobile-radio reception, Bell System Technical Journal 47(6), 1968
    locator: pp. 957 to 1000 (the field at a moving receiver as a sum of plane waves from random directions, its Gaussian statistics, correlation and spectrum)
  - book: isbn:9780780310698
    title: William C. Jakes (editor), Microwave Mobile Communications, Wiley, 1974; reissued by IEEE Press, 1994
    locator: the chapter on multipath interference (the Doppler power spectrum of the field under uniform angles of arrival, its correlation functions and the level crossing rate)
  - book: isbn:9780130422323
    title: Theodore S. Rappaport, Wireless Communications, Principles and Practice, second edition, Prentice Hall, 2002
    locator: Section 5.7.1 (Clarke's model for flat fading) and Section 5.7.2 (simulation of Clarke and Gans fading models)
  - book: isbn:9780521837163
    title: Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005
    locator: Section 3.2.1 (autocorrelation, cross-correlation and power spectral density under uniform scattering)
---

Clarke's model describes the complex gain of a flat fading channel at a receiver that moves through a field of scattered waves arriving from all directions in the horizontal plane with equal probability. The gain is a circular complex Gaussian process, so its envelope is Rayleigh at every instant, and its autocorrelation is $\Omega J_0(2\pi f_D\tau)$, where $f_D = v f_c/c$ is the maximum Doppler frequency. The Fourier transform of this correlation is the U-shaped Doppler spectrum on $|f| < f_D$. Clarke (1968) gave the model; Jakes (1974) made the spectrum standard. This page is about the spectrum and the process. Programs that generate sample paths with these statistics are on separate pages: the [Jakes simulator](/jakes-fading-simulator/), the [Zheng and Xiao simulator](/zheng-xiao-fading-simulator/) and the [filtered Gaussian simulator](/filtered-gaussian-fading-simulator/).

## The machine

A receiver moves at speed $v$ in meters per second. A carrier at frequency $f_c$ in hertz, with wavelength $\lambda = c/f_c$, reaches it over $N$ paths. Path $n$ arrives in the horizontal plane at angle $\theta_n$ to the direction of motion, with amplitude $C_n$ and phase $\phi_n$. The complex baseband gain is

$$h(t) = \sum_{n=1}^{N} C_n\, e^{j(2\pi f_D \cos\theta_n\, t + \phi_n)}, \qquad f_D = \frac{v f_c}{c}.$$

The standing assumptions are:

- **Isotropic scattering.** The angles $\theta_n$ are independent and uniform on $[0, 2\pi)$.
- **Random phases.** The phases $\phi_n$ are independent, uniform on $[0, 2\pi)$, and independent of the angles.
- **Equal small powers.** No path dominates, there is no line of sight, and $\sum_n \mathbb{E}C_n^2 = \Omega$.
- **Flat fading in the plane.** All paths have nearly the same delay compared with the symbol time, all waves travel in the horizontal plane, and the antenna is omnidirectional in that plane.
- **A local area.** The receiver moves a few tens of wavelengths, so the set of scatterers, the speed and the mean power $\Omega$ stay fixed.

As $N \to \infty$, the [central limit theorem](/central-limit-theorem/) makes $h(t)$ a zero-mean circular complex Gaussian process. The model then describes **time-correlated fading**: at each time the gain is that of the [Rayleigh fading channel](/rayleigh-fading-channel/), and the gains at different times are linked by the autocorrelation below. The model is of the channel only. It says nothing about channel knowledge; pages that use it state whether the receiver has CSIR, for example from [channel estimation](/channel-estimation/), and whether there is CSIT.

## What it counts

The model predicts the second-order statistics of $h(t)$, and from them the statistics of fades in time and in space.

**Autocorrelation and spectrum.**

$$R_h(\tau) = \mathbb{E}[h(t+\tau)\, h^*(t)] = \Omega\, J_0(2\pi f_D \tau), \qquad S_h(f) = \frac{\Omega}{\pi f_D \sqrt{1 - (f/f_D)^2}} \ \text{ for } |f| < f_D,$$

and $S_h(f) = 0$ for $|f| > f_D$. Here $J_0(x) = \frac{1}{2\pi}\int_0^{2\pi} e^{j x\cos\theta}\, d\theta$ is the Bessel function of the first kind and order zero. The spectrum integrates to $\Omega$, has mean $0$ and RMS width $\sigma_\nu = f_D/\sqrt2$, and is infinite at $\pm f_D$.

**In-phase and quadrature parts.** With $h = h_I + j h_Q$, each part has autocorrelation $\frac{\Omega}{2}J_0(2\pi f_D\tau)$, and the cross-correlation $\mathbb{E}[h_I(t+\tau) h_Q(t)]$ is zero at every lag because the spectrum is even.

**Values of the correlation.** $J_0(2\pi f_D\tau)$ falls to $0.9$ at $f_D\tau = 0.1020$, to $0.5$ at $f_D\tau = 0.2421$ and to $0$ at $f_D\tau = 0.38274$, the first zero. After that it oscillates with $|J_0| \le 0.403$. These values give the [coherence time](/coherence-time/) of the model.

**Space instead of time.** In time $\tau$ the receiver moves $d = v\tau$, and $2\pi f_D \tau = 2\pi d/\lambda$. So two antennas on the receiver spaced $d$ apart, in the same field, have gains with correlation $J_0(2\pi d/\lambda)$: $0.5$ at $d = 0.242\lambda$ and $0$ at $d = 0.383\lambda$. At $d = \lambda/2$ the value is $J_0(\pi) = -0.304$. This is why antennas at a mobile placed about half a wavelength apart give useful diversity, a rule that holds only under isotropic scattering.

**Fade statistics.** The rate at which the envelope $|h|$ crosses a level $\rho\sqrt\Omega$ going down, and the mean time it stays below, are

$$N_R = \sqrt{2\pi}\, f_D\, \rho\, e^{-\rho^2}, \qquad \bar t_R = \frac{e^{\rho^2} - 1}{\rho f_D\sqrt{2\pi}},$$

with $N_R/f_D = 0.92214$ and $\bar t_R f_D = 0.68550$ at $\rho = 1$. The proof is on the [level crossing rate](/level-crossing-rate/) page.

**A worked example.** At $v = 30$ m/s and $f_c = 900$ MHz, $f_D = 90.06$ Hz and $\lambda = 0.333$ m. After $\tau = 1$ ms, $x = 2\pi f_D\tau = 0.5659$ and $J_0(x) \approx 1 - x^2/4 + x^4/64 = 0.9215$. The correlation reaches $0$ after $0.38274/f_D = 4.25$ ms, when the receiver has moved $12.8$ cm, which is $0.383\lambda$.

### Computing the correlation

The function below evaluates $R_h(\tau)$ as the mean of $\cos(x\cos\theta)$ over $N$ equally spaced angles, which is the model with $N$ paths in fixed directions. The integrand is smooth and periodic, so the midpoint rule converges faster than any power of $1/N$: its error is of the order of $|J_{2N}(x)|$, far below rounding error once $2N$ is well above $|x|$.

```pseudo id=main
CLARKE-CORRELATION(τ, f_D, Ω)             ▷ R(τ) = Ω J0(2π f_D τ)
L1  x ← 2π · f_D · τ
L2  N ← 32 + ⌈|x|⌉
L3  s ← Σ_{n=0}^{N-1} cos(x · cos(π (n + 1/2) / N))   ▷ midpoint rule on [0, π]
L4  return Ω · s / N

DOPPLER-SPECTRUM(f, f_D, Ω)               ▷ S(f), Clarke's U-shaped spectrum
L5  if |f| ≥ f_D then return 0
L6  return Ω / (π · f_D · √(1 - (f / f_D)²))
```

The cost is $O(|x| + 1)$ operations. The tests compare the result with the power series of $J_0$ and with its known zeros, check the values on this page, integrate the spectrum against the correlation, and compare a Monte Carlo average over random angles and phases with $J_0$ within a stated tolerance.

## Relation to other models

- **Rayleigh fading.** At a single time Clarke's model is the [Rayleigh fading channel](/rayleigh-fading-channel/). The model adds the time dimension that block and fast fading leave out.
- **Rician fading.** A fixed line-of-sight path at angle $\theta_0$ adds a constant times $e^{j 2\pi f_D\cos\theta_0 t}$ and gives the [Rician channel](/rician-fading-channel/) with a spectral line at $f_D\cos\theta_0$.
- **Generators.** Clarke's model is a statement about a Gaussian process, not a program. The [Jakes simulator](/jakes-fading-simulator/) sums a few sinusoids with fixed angles; Pop and Beaulieu (2001) showed that it is not wide-sense stationary. The [Zheng and Xiao simulator](/zheng-xiao-fading-simulator/) draws random angles and phases to repair this. The [filtered Gaussian simulator](/filtered-gaussian-fading-simulator/) shapes white Gaussian noise with a filter whose power response approximates $S_h$. Each matches the model only approximately; its page states the error.
- **Frequency-selective channels.** In a [tapped delay line model](/tapped-delay-line-channel-model/) each tap can be an independent Clarke process. Under the [WSSUS model](/wssus-channel-model/) this means a scattering function that is the power delay profile times the Clarke spectrum.
- **Geometric models.** A [geometry-based stochastic model](/geometry-based-stochastic-channel-model/) with scatterers on a ring around the mobile and a distant base station reduces to Clarke's model at the mobile. Seen from the base station, the same ring gives a narrow angle spread and a much slower spatial decorrelation.
- **Tracking.** The spectrum is not rational, so no finite [autoregressive model](/autoregressive-model/) has exactly the correlation $J_0$. [Kalman channel tracking](/kalman-channel-tracking/) uses an autoregressive fit, which is an approximation.

## Known results in the model

1. **The autocorrelation (a closed form under isotropic scattering).** With the phases independent and uniform, the cross terms vanish: $\mathbb{E}[e^{j(\phi_n - \phi_m)}] = 0$ for $n \ne m$. So
   $$R_h(\tau) = \sum_n \mathbb{E}C_n^2\, \mathbb{E}\big[e^{j 2\pi f_D\cos\theta\, \tau}\big] = \Omega \cdot \frac{1}{2\pi}\int_0^{2\pi} e^{j 2\pi f_D\tau\cos\theta}\, d\theta = \Omega\, J_0(2\pi f_D\tau).$$
   The result does not need $N \to \infty$: it holds for any $N$ with random angles and phases. Gaussianity is what needs a large $N$.
2. **The Doppler spectrum (a closed form under isotropic scattering).** Path $n$ contributes power $\mathbb{E}C_n^2$ at the frequency $\nu = f_D\cos\theta_n$, so $S_h/\Omega$ is the density of $f_D\cos\theta$ for uniform $\theta$. Each $\nu$ in $(-f_D, f_D)$ comes from two angles, and $|d\nu/d\theta| = f_D|\sin\theta| = f_D\sqrt{1 - (\nu/f_D)^2}$. So the density is $2 \cdot \frac{1}{2\pi} \cdot \frac{1}{f_D\sqrt{1 - (\nu/f_D)^2}}$, which is the formula above. Its variance is $f_D^2\,\mathbb{E}[\cos^2\theta] = f_D^2/2$.
3. **Independence of the gain and its derivative.** $\mathbb{E}[h'(t)\, h^*(t)] = R_h'(0) = 0$, since $J_0'(0) = 0$. With circular symmetry, $\mathbb{E}[h'(t)\, h(t)] = 0$ as well, and for jointly Gaussian variables zero correlation is independence. The derivative has power $-R_h''(0) = 2\pi^2 f_D^2\,\Omega$, from $J_0(x) = 1 - x^2/4 + O(x^4)$. These two facts give the level crossing rate.
4. **A band-limited process.** $S_h$ is zero outside $[-f_D, f_D]$, so by the [sampling theorem](/sampling-theorem/) samples at a rate above $2f_D$ determine $h(t)$. This is the basis of the pilot spacing in [pilot-symbol-assisted modulation](/pilot-symbol-assisted-modulation/).
5. **Bounds on the coherence time.** Fleury's uncertainty relation with $\sigma_\nu = f_D/\sqrt2$ gives $|J_0(2\pi f_D\tau)| \ge \cos(\sqrt2\,\pi f_D \tau)$ for $f_D\tau \le 1/(2\sqrt2)$. At the level $0.5$ the bound is $0.2357/f_D$ against the true $0.2421/f_D$; see [coherence time](/coherence-time/).

### Pitfalls

- **Model and simulator.** "Jakes model" often names the simulator and "Jakes spectrum" the spectrum. A simulation with a few fixed angles does not reproduce $J_0$ at long lags and is not stationary; quote which one is meant.
- **The peaks at $\pm f_D$.** They come from exact isotropy in a plane. Measured spectra are finite, and directional antennas or a limited angle spread change the shape of the spectrum completely.
- **Envelope correlation.** $J_0$ is the correlation of the complex gain. The correlation coefficient of the envelopes $|h|$ is close to $J_0^2$ and never negative.
- **The base station.** Isotropic scattering is a fair assumption around a mobile in a city. At an elevated base station the waves come from a narrow sector, and $J_0(2\pi d/\lambda)$ does not give the antenna correlation there.
- **The frequency in $f_D$.** $f_D$ uses the carrier frequency, not the signal bandwidth. At $28$ GHz the same speed gives fourteen times the Doppler of $2$ GHz.

## References
