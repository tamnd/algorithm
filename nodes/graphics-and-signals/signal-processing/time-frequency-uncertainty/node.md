---
tag: TQ9C7X
kind: theorem
slug: time-frequency-uncertainty
name: Time-frequency uncertainty principle
aliases:
- Gabor limit
- signal uncertainty principle
- Heisenberg-Gabor inequality
area: graphics-and-signals/signal-processing
level: advanced
summary: "The time spread and frequency spread of a signal satisfy sigma_t sigma_omega >= 1/2, with equality exactly for shifted, modulated Gaussians."
prereqs: [parsevals-theorem]
see_also: [window-functions, short-time-fourier-transform, time-frequency-analysis, continuous-wavelet-transform, sparse-signal-recovery, compressed-sensing, sparse-fourier-transform, sampling-theorem]
sources:
  - paper: doi:10.1049/ji-3-2.1946.0074
    title: Dennis Gabor, Theory of Communication. Part 1, The Analysis of Information, Journal of the Institution of Electrical Engineers, Part III 93(26), 1946
    locator: pp. 429 to 441 (the information diagram, the inequality between effective duration and effective bandwidth, and the Gaussian elementary signals that reach it)
  - paper: doi:10.1007/BF01397280
    title: Werner Heisenberg, Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik, Zeitschrift für Physik 43(3-4), 1927
    locator: pp. 172 to 198 (the original uncertainty relation of position and momentum)
  - paper: doi:10.1007/BF01391200
    title: Earle H. Kennard, Zur Quantenmechanik einfacher Bewegungstypen, Zeitschrift für Physik 44(4-5), 1927
    locator: pp. 326 to 352 (the first proof of the inequality for standard deviations)
  - paper: doi:10.1007/BF02649110
    title: Gerald B. Folland and Alladi Sitaram, The Uncertainty Principle, A Mathematical Survey, Journal of Fourier Analysis and Applications 3(3), 1997
    locator: pp. 207 to 238 (the Heisenberg inequality with its proof, the equality case and the extension to all square integrable functions, local and support forms, history)
  - paper: doi:10.1137/0149053
    title: David L. Donoho and Philip B. Stark, Uncertainty Principles and Signal Recovery, SIAM Journal on Applied Mathematics 49(3), 1989
    locator: pp. 906 to 931 (the discrete bound N_t N_f >= N, the picket fence as its extremal case, and recovery of signals with missing samples)
  - paper: doi:10.4310/MRL.2005.v12.n1.a11
    title: Terence Tao, An Uncertainty Principle for Cyclic Groups of Prime Order, Mathematical Research Letters 12(1), 2005
    locator: pp. 121 to 127 (the bound N_t + N_f >= N + 1 for prime N)
  - book: isbn:9780691113845
    title: Elias M. Stein and Rami Shakarchi, Fourier Analysis, An Introduction, Princeton University Press, 2003
    locator: Chapter 5, The Fourier Transform on R (the Heisenberg uncertainty principle and its proof for Schwartz functions)
  - book: isbn:9780123743701
    title: Stéphane Mallat, A Wavelet Tour of Signal Processing, The Sparse Way, third edition, Academic Press, 2009
    locator: Chapter 2, The Fourier Kingdom (the Heisenberg uncertainty theorem) and Chapter 4, Time Meets Frequency (Heisenberg boxes of windowed Fourier and wavelet atoms)
---

The time-frequency uncertainty principle says that a signal cannot be concentrated both in a short stretch of time and in a narrow band of frequencies. In its sharp form, the standard deviation $\sigma_t$ of the energy density $|x(t)|^2$ and the standard deviation $\sigma_\omega$ of the spectral density $|X(\omega)|^2$ satisfy $\sigma_t\sigma_\omega \ge 1/2$. Equality holds exactly for Gaussian pulses, possibly shifted in time and modulated in frequency. The inequality is the same mathematics as Heisenberg's relation in quantum mechanics, and it fixes the trade-off behind every window and every time-frequency picture.

## Statement

Let $x \in L^2(\mathbb{R})$ be nonzero, with Fourier transform $X(\omega) = \int_{-\infty}^{\infty} x(t)\,e^{-i\omega t}\,dt$ and energy $E = \int |x(t)|^2\,dt$. Treat $|x(t)|^2/E$ and $|X(\omega)|^2/(2\pi E)$ as probability densities; by [Parseval's theorem](/parsevals-theorem/) for the Fourier transform (Plancherel), both have total mass one. Let $t_0$, $\omega_0$ be their means and

$$\sigma_t^2 = \frac{1}{E}\int (t - t_0)^2 |x(t)|^2\,dt, \qquad \sigma_\omega^2 = \frac{1}{2\pi E}\int (\omega - \omega_0)^2 |X(\omega)|^2\,d\omega,$$

with the value $+\infty$ allowed. Then

$$\sigma_t\,\sigma_\omega \ge \frac12,$$

and equality holds if and only if

$$x(t) = C\,e^{-a(t - t_0)^2}\,e^{i\omega_0 t}$$

for some complex $C \ne 0$, real $a > 0$, real $t_0$ and real $\omega_0$. With frequency $f = \omega/(2\pi)$ in hertz the bound reads $\sigma_t\,\sigma_f \ge 1/(4\pi)$.

**Discrete form (Donoho and Stark).** For a nonzero vector $v \in \mathbb{C}^N$ with [DFT](/discrete-fourier-transform/) $V$, let $N_t$ and $N_f$ be the numbers of nonzero entries of $v$ and $V$. Then $N_t N_f \ge N$, and hence $N_t + N_f \ge 2\sqrt{N}$. When $N$ is prime the stronger bound $N_t + N_f \ge N + 1$ holds (Tao).

## In plain words

A sound that is very short, like a click, contains a wide spread of pitches. A sound with one sharp pitch, like a long pure whistle, has to last a long time. You can trade one for the other, but you cannot have both: squeezing the sound in time always spreads it out in pitch, and the other way around. The theorem puts a number on this. Multiply how spread out the sound is in time by how spread out it is in pitch, and the result can never go below a fixed floor. Exactly one family of shapes sits right on the floor: the smooth bell curve, moved to any time and any pitch. Every other shape is above it. The same rule, with physical units, is Heisenberg's uncertainty principle for a particle's position and speed.

## Proof

**Reduction.** If $\sigma_t$ or $\sigma_\omega$ is infinite there is nothing to prove, so assume both are finite. Replacing $x(t)$ by $e^{-i\omega_0 t}x(t + t_0)$ moves the time density by $-t_0$ and the spectral density by $-\omega_0$ and changes neither spread, so we may assume $t_0 = \omega_0 = 0$. We give the proof for $x$ in the Schwartz class, where every integral below converges and the boundary terms vanish. For a general $x$ with finite spreads, $tx$ and the distributional derivative $x'$ are in $L^2$, Schwartz functions are dense in the space with norm $\|x\| + \|tx\| + \|x'\|$, and both sides of each identity below are continuous in that norm; Folland and Sitaram give the details.

**Step 1, frequency spread from the derivative.** The transform of $x'$ is $i\omega X(\omega)$. By Plancherel, $\int \omega^2 |X(\omega)|^2\,d\omega = 2\pi\int |x'(t)|^2\,dt$, so

$$\sigma_\omega^2 = \frac{1}{E}\int |x'(t)|^2\,dt.$$

**Step 2, integration by parts.** Since $\frac{d}{dt}|x(t)|^2 = 2\,\mathrm{Re}\big(\overline{x(t)}\,x'(t)\big)$ and $t|x(t)|^2 \to 0$ at $\pm\infty$,

$$2\,\mathrm{Re}\int t\,\overline{x(t)}\,x'(t)\,dt = \int t\,\frac{d}{dt}|x(t)|^2\,dt = -\int |x(t)|^2\,dt = -E.$$

**Step 3, Cauchy-Schwarz.** Apply it to the functions $t\,x(t)$ and $x'(t)$:

$$\frac{E^2}{4} = \Big(\mathrm{Re}\int t\,\overline{x}\,x'\,dt\Big)^2 \le \Big|\int t\,\overline{x}\,x'\,dt\Big|^2 \le \int t^2|x|^2\,dt \int |x'|^2\,dt = E\sigma_t^2 \cdot E\sigma_\omega^2.$$

Dividing by $E^2$ gives $\sigma_t^2\sigma_\omega^2 \ge 1/4$.

**Equality.** Both inequalities in Step 3 must be equalities. Equality in Cauchy-Schwarz means $x' = c\,t\,x$ for a complex constant $c$ (the function $tx$ is not zero, since $E > 0$). Then $\int t\,\overline{x}\,x'\,dt = c\int t^2|x|^2\,dt$, and equality in the first inequality means this number is real; by Step 2 it equals $-E/2 < 0$, so $c$ is real and negative. Write $c = -2a$ with $a > 0$. The equation $x' = -2a\,t\,x$ has the solutions $x = C e^{-at^2}$ and no others. Undoing the reduction gives $C e^{-a(t - t_0)^2} e^{i\omega_0 t}$. Conversely, for $x = e^{-at^2}$, $|x|^2 = e^{-2at^2}$ has variance $1/(4a)$ and $|X|^2 = (\pi/a)e^{-\omega^2/(2a)}$ has variance $a$, so the product of the spreads is exactly $1/2$.

**Discrete form.** Let $M = \max_k |V_k|$. Each $V_k$ is a sum of $N_t$ terms of the form $v_n e^{-2\pi i nk/N}$, so by Cauchy-Schwarz over the support of $v$, $M \le \sum_n |v_n| \le \sqrt{N_t}\,\|v\|$. Parseval's identity for the DFT gives $N\|v\|^2 = \|V\|^2$, and $V$ has $N_f$ nonzero entries, each at most $M$ in size, so $\|V\|^2 \le N_f M^2$. Together, $N\|v\|^2 \le N_f M^2 \le N_f N_t \|v\|^2$, and dividing by $\|v\|^2 > 0$ gives $N_t N_f \ge N$. The sum form follows from $N_t + N_f \ge 2\sqrt{N_t N_f}$.

## Consequences

- **Windows and spectral resolution.** A window of length $T$ has a spectral main lobe of width of order $1/T$; no taper can beat this, it can only move energy between the main lobe and the side lobes. This is the forced trade-off among [window functions](/window-functions/).
- **Time-frequency analysis.** Each atom of the [short-time Fourier transform](/short-time-fourier-transform/) occupies a Heisenberg box of area at least $1/2$ in the $(t, \omega)$ plane, so no linear [time-frequency analysis](/time-frequency-analysis/) can resolve events finer than that area. The Gaussian window gives the smallest boxes, which is why the Gabor transform uses it. The [continuous wavelet transform](/continuous-wavelet-transform/) keeps the area fixed and changes the shape: short boxes at high frequency, long ones at low frequency.
- **No signal is both time limited and band limited.** A nonzero signal with a compactly supported spectrum is the restriction of an entire function and cannot vanish on an interval; this is why the [sampling theorem](/sampling-theorem/) needs infinitely many samples and why every practical band limit is approximate.
- **Recovery of sparse signals.** Donoho and Stark used $N_t N_f \ge N$ to show that a signal with few nonzero entries can be recovered uniquely from a part of its spectrum: if two signals with $N_t$ nonzero entries agree on all but $N_f$ frequencies, their difference has at most $2N_t$ nonzero entries and at most $N_f$ nonzero frequencies, so it is zero when $2N_t N_f < N$. This is an ancestor of [sparse signal recovery](/sparse-signal-recovery/) and [compressed sensing](/compressed-sensing/), and the reason a [sparse Fourier transform](/sparse-fourier-transform/) can work from few samples.
- **Quantum mechanics.** With position $t$ and momentum $p = \hbar\omega$, the same inequality is $\sigma_x\sigma_p \ge \hbar/2$, and the minimum-uncertainty states are Gaussian wave packets.

## Tightness

The bound is attained, and only by the Gaussian family. The products below are measured by composite Simpson quadrature. For the Gaussians, $\sigma_\omega$ is computed from $|X(\omega)|^2$, where $X$ is itself computed by Simpson quadrature of $x(t)e^{-i\omega t}$ on a grid of $\omega$ values, not from a formula. For the other signals, $\sigma_\omega$ comes from Step 1, $\int |x'|^2/E$, also by quadrature.

| signal | measured $\sigma_t\sigma_\omega$ | exact value |
|---|---|---|
| $e^{-at^2}$, $a = 0.25, 1, 4$ | $0.5$ to $10^{-12}$ for each $a$ | $1/2$ |
| $e^{-0.7(t - 1.5)^2}e^{3it}$ | $0.5$, means $1.5$ and $3.0$ to $10^{-12}$ | $1/2$ |
| chirp $e^{-(1 - ib)t^2}$, $b = 2$ | $1.118034$ | $\tfrac12\sqrt{1 + b^2} = 1.118034$ |
| $e^{-\lvert t\rvert}$ | $0.7071068$ | $1/\sqrt2$ |
| triangle $\max(0, 1 - \lvert t\rvert)$ | $0.5477226$ | $\sqrt{0.3}$ |
| Hermite function of order $n = 0, \ldots, 4$ | $n + 0.5$ to $10^{-9}$ | $n + \tfrac12$ |
| box of width $1$ | grows without bound | $\infty$ |

The table shows four kinds of failure of equality:

- **The chirp** is Gaussian in magnitude but has a phase that turns in time. Cauchy-Schwarz is still tight, since $x' = -2(1 - ib)\,t\,x$, but the constant is not real, so the first inequality in Step 3 is strict.
- **Sharp features** cost more. $e^{-|t|}$ has a kink and the triangle has three.
- **The box** has a jump. Its transform $2\sin(\omega/2)/\omega$ gives $\int_{-W}^{W}\omega^2|X|^2\,d\omega = 4W - 4\sin W$. Computed with the numerical $X$, this matches to within $3 \times 10^{-5}W$ for $W = 10, 40, 120$, so $\sigma_\omega = \infty$.
- **Small perturbations.** Adding $\varepsilon\,e^{-(t - 0.8)^2}$ to $e^{-t^2}$ raises the product above $1/2$ by $8.1 \times 10^{-6}$, $1.59 \times 10^{-4}$ and $1.00 \times 10^{-3}$ for $\varepsilon = 0.01$, $0.05$ and $0.2$. The growth is quadratic for small $\varepsilon$, as at a strict minimum.

Forty random sums of three complex modulated Gaussians (seeded) gave products from $0.5025$ to $4.03$, never below $1/2$.

The discrete bound is also tight. A picket fence of $N/d$ ones spaced $d$ apart has a DFT that is a picket fence of $d$ nonzero values, so $N_t N_f = N$ for every divisor $d$ of $N$. Shifting it or modulating it keeps both counts; this was checked for $N = 36$ and all nine divisors. An exhaustive check of all $3^8 - 1$ nonzero vectors with entries in $\{-1, 0, 1\}$ and $N = 8$ found the minimum of $N_t N_f$ to be exactly $8$. The analogous check for $N = 7$ confirmed $N_t + N_f \ge 8$ on all $3^7 - 1$ vectors.

## History

Heisenberg stated the uncertainty relation for position and momentum in 1927 with a heuristic argument. Kennard proved the inequality $\sigma_x\sigma_p \ge \hbar/2$ for standard deviations later the same year. Weyl's 1928 book on group theory and quantum mechanics gave the Fourier-analytic proof above and credited it to Pauli. Gabor carried the idea into communication theory in 1946. He measured a signal by an effective duration and an effective bandwidth, each $\sqrt{2\pi}$ times the standard deviations used here, so that his bound reads $\Delta t\,\Delta f \ge 1/2$. He drew the information diagram in which each elementary signal occupies a cell, and showed that Gaussian-modulated sinusoids fill the cells most economically. Those elementary signals are now called Gabor atoms, and the bound is often called the Gabor limit. Donoho and Stark's 1989 paper gave the discrete and support forms and connected them to signal recovery. Folland and Sitaram's 1997 survey collects the many variants.

## References
