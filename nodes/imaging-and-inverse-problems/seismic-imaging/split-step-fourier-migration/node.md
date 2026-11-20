---
tag: C572NA
kind: algorithm
slug: split-step-fourier-migration
name: Split-step Fourier migration
aliases:
- SSF migration
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "Extrapolate a wavefield in depth by a phase shift with a reference velocity in the wavenumber domain and a lateral velocity correction in space."
solves: [seismic-migration]
model: real-ram
complexity:
  vars: {t: "the number of time samples", x: "the number of traces", z: "the number of depth steps"}
  time: {per_step: "O(x log x)", total: "O(z t x log x + x t log t)"}
  space: {extra: "O(t x + z x)"}
properties: {deterministic: true, lateral_velocity: true, exact_for: "velocity v(z)", unconditionally_stable: true, error_grows_with: "angle and velocity contrast"}
history:
  year: 1990
  people: [Paul L. Stoffa, Jacob T. Fokkema, Rui M. de Luna Freire, William P. Kessinger]
  note: Stoffa, Fokkema, de Luna Freire and Kessinger published split-step Fourier migration in Geophysics in 1990, borrowing the split-step method of underwater acoustics and optics.
prereqs: [phase-shift-migration, fast-fourier-transform]
see_also: [phase-shift-migration, finite-difference-migration, stolt-migration, reverse-time-migration, operator-splitting, angular-spectrum-method, seismic-migration]
sources:
  - paper: doi:10.1190/1.1442850
    title: P. L. Stoffa, J. T. Fokkema, R. M. de Luna Freire and W. P. Kessinger, Split-step Fourier migration, Geophysics 55(4), 1990, 410 to 421
    locator: the split-step downward continuation with a reference slowness and a space-domain correction
  - paper: doi:10.1190/1.1440899
    title: Jeno Gazdag, Wave equation migration with the phase-shift method, Geophysics 43(7), 1978, 1342 to 1351
    locator: the phase shift that the method uses for the reference slowness
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001
    locator: Chapter 4 (migration), frequency-space and frequency-wavenumber methods for lateral velocity changes
---

Split-step Fourier migration extends [phase-shift migration](/phase-shift-migration/) to a velocity that changes along $x$. For each frequency and each depth step it does two things. First it applies the phase shift of one reference slowness $s_0$, the mean over the layer, in the wavenumber domain. Then it goes back to the space domain and multiplies every point by $e^{i\omega(s(x) - s_0)\Delta z}$, a thin-lens correction for the local slowness. When the velocity does not change along $x$ the correction is 1 and the method is exactly phase shift (a theorem). Otherwise it has a phase error that is zero for vertical waves and grows with the square of the propagation angle and with the velocity contrast (a theorem for one plane wave; how the errors add up in a general medium is a heuristic).

## In plain words

Phase-shift migration moves the recorded wave down into the ground one step at a time, but it needs the same speed everywhere across each step. Split-step Fourier migration allows the speed to change from left to right. At each step it first moves the whole wave down as if the layer had its average speed. Then it fixes each point: where the ground is slower than average, the wave should arrive later, so the method turns the phase at that point a little more, and where the ground is faster, a little less. The fix is exact for waves that go straight up and down, and it gets worse for waves that travel at a steep angle through strong speed changes. Each step costs two fast Fourier transforms.

## The problem

Given a zero-offset section $d(t, x)$ and a velocity $v(x, z)$ on the image grid (the value $v_i[j]$ for the layer $i\Delta z \le z < (i + 1)\Delta z$ at $x_j$), find the image $m(x, z)$. This is [seismic migration](/seismic-migration/) in the [exploding reflector model](/exploding-reflector-model/), so the method uses the slowness $s = 2/v$ of the half velocity.

## The algorithm

The time transform is $U(\omega) = \sum_t u(t)e^{-i\omega t}$ and the space transform uses $e^{-i k_x x}$. For a real section the negative frequencies are complex conjugates of the positive ones, so the method continues only $0 < \omega < \omega_{\text{Nyquist}}$ and takes twice the real part.

```pseudo id=main
SPLIT-STEP-FOURIER-MIGRATION(d, Δt, Δx, Δz, v)     ▷ v[i][j]: velocity of layer i at x_j
L1  P_k ← DFT in time of every trace, for every frequency index k
L2  for every frequency ω = ω_k with 0 < ω_k < the Nyquist frequency do      ▷ p ← P_k
L3      for i ← 0 to n_z - 1 do
L4          image[i] ← image[i] + (2 / n_t) Re p
L5          s[j] ← 2 / v[i][j] for every j;  s_0 ← mean of s
L6          q ← DFT(p)
L7          q[j] ← q[j] · exp(i sqrt(ω² s_0² - k_x,j²) Δz) for every j, or 0 where the root is not real
L8          p ← IDFT(q)
L9          p[j] ← p[j] · exp(i ω (s[j] - s_0) Δz) for every j
L10 return image
```

Line L1 transforms every trace in time once. For one frequency, the vector $p$ holds the field at the current depth along $x$. Line L4 adds the contribution of this frequency to the image row: the field at $t = 0$ is the sum over all frequencies divided by $n_t$, and the positive and negative frequencies together give twice the real part. Line L5 computes the slowness of the half velocity and its mean. Lines L6 to L8 are the phase shift of [phase-shift migration](/phase-shift-migration/) with the reference slowness $s_0$, applied in the wavenumber domain; the evanescent waves are removed. Line L9 is the split step: a phase correction in the space domain for the difference between the local and the reference slowness.

## Example

**One plane wave by hand.** Take $\omega = 100$ rad/s, $\Delta z = 10$ m, a reference half velocity of 1500 m/s ($s_0 = 1/1500$ s/m) and a local half velocity of 1250 m/s ($s = 1/1250$ s/m), and the wavenumber $k_x = 0.04$ rad/m, which is a wave at 30 degrees in the local medium. The exact phase over one step is $10\sqrt{0.08^2 - 0.04^2} = 0.6928$ rad. The split step gives $10\sqrt{0.06667^2 - 0.04^2} + 100 \cdot (0.0008 - 0.0006667) \cdot 10 = 0.5333 + 0.1333 = 0.6667$ rad. The error is $-0.0262$ rad per step. The leading term of the error formula below gives $10 \cdot 0.04^2/(2 \cdot 100) \cdot (1250 - 1500) = -0.020$ rad. For a vertical wave ($k_x = 0$) the error is zero.

**Tests.** For a velocity that changes only with depth (2500 m/s over 3000 m/s), the image equals the phase-shift image computed from the same positive frequencies within $10^{-9}$. For a velocity $3000 + 300\cos(2\pi j/32)$ m/s that changes along $x$ and a flat reflector at 240 m, every column of the image peaks at the right depth row (a measurement on this case).

## Correctness

The full proof is in proofs/correctness.md.

- **What the code computes (theorem).** Line L10 returns $(2/n_t)\operatorname{Re}\sum_{0 < k < n_t/2} p_k^{(i)}$, where $p_k^{(i)}$ is the trace spectrum at index $k$ after $i$ split steps. Because the step for $-\omega$ is the complex conjugate of the step for $\omega$, this is the field at $t = 0$ of the continued data without the zero and Nyquist frequencies.
- **Exact for $v(z)$ (theorem).** If the velocity does not change along $x$ in any layer, then $s = s_0$, line L9 does nothing, and the method is phase-shift migration.
- **Phase error for one plane wave (theorem).** In a layer of slowness $s$ treated with the reference $s_0$, the error of one step is $\Delta z\big(\sqrt{\omega^2 s_0^2 - k_x^2} + \omega(s - s_0) - \sqrt{\omega^2 s^2 - k_x^2}\big)$. It is zero for $k_x = 0$ or $s = s_0$, and its leading term is $\Delta z\,\frac{k_x^2}{2\omega}\big(\frac{1}{s} - \frac{1}{s_0}\big)$.
- **Stability (theorem).** Every factor has modulus at most 1, so no step increases the energy, for any $\Delta z$.

That the local plane-wave errors stay small in a smooth medium with moderate contrast is a heuristic, supported by the cosine test above.

## Complexity

- **Real-ram, with FFTs.** Line L1 costs $O(n_x n_t \log n_t)$. Each depth step for one frequency costs two FFTs of length $n_x$ and $O(n_x)$ phase factors, $O(n_x \log n_x)$. With about $n_t/2$ frequencies and $n_z$ steps the total is $O(n_z n_t n_x \log n_x)$.
- **Against phase shift.** Phase shift costs $O(n_x)$ per step and frequency once the data are in the wavenumber domain, so the split step costs a factor $\log n_x$ more for its two transforms.
- **Space.** One complex vector per frequency during its loop, and the image.

## Properties

- **Lateral velocity.** The correction uses the local slowness at every point, so the image follows lateral velocity changes, with an error that depends on the angle and the contrast.
- **Exact vertical propagation.** Waves that travel straight up are continued exactly in any $v(x, z)$.
- **Unconditionally stable.** All factors have modulus at most 1.
- **Frequencies are independent.** Each frequency is continued alone, so the loop at line L2 runs in parallel without communication.
- **Periodic in $x$.** The DFT in line L6 makes the field periodic along the line; pad with zeros or taper the edges.

## Variants and improvements

- **Several reference velocities.** Phase shift plus interpolation (Gazdag and Sguazzero 1984) runs the phase shift with a few reference velocities and interpolates at each $x$; this reduces the error for large contrasts.
- **Fourier finite difference.** Add a finite-difference correction term to the split step to reduce the angle error, in the spirit of [finite-difference migration](/finite-difference-migration/).
- **Generalized screen methods.** Higher-order terms in the expansion of the square root about the reference slowness improve wide-angle accuracy.
- **Prestack migration.** The same step continues the source and the receiver wavefields separately in shot-profile migration, followed by the [imaging condition](/imaging-condition/).
- **The [angular spectrum method](/angular-spectrum-method/).** The reference step alone is the angular spectrum propagator of optics, and the split step is the beam propagation method used for optical fibers and turbulence.

## When to use it

Use split-step Fourier migration when the velocity changes along $x$ but not too strongly, and when one-way migration is enough (no turning waves). It costs little more than phase shift and handles lateral changes that phase shift and [Stolt migration](/stolt-migration/) cannot. For strong contrasts, such as salt bodies, use several reference velocities, a Fourier finite-difference correction, or [reverse-time migration](/reverse-time-migration/).

## Pitfalls

- **A reference far from the local velocity.** Taking $s_0$ in line L5 from one corner of the layer instead of its mean makes $|s - s_0|$ large and the angle error large everywhere. Use the mean (or several references), as in line L5.
- **The correction in the wrong domain.** Applying the factor of line L9 in the wavenumber domain, before line L8, multiplies wavenumbers by a function of $x$, which has no meaning. Apply it after the inverse transform of line L8.
- **The full velocity.** Using $s = 1/v$ in line L5 doubles every depth. Zero-offset data need $s = 2/v$.
- **Dropping the factor 2.** Line L4 continues only the positive frequencies; without the factor $2/n_t$ the image has half its amplitude.

## Implementations

## History

The split-step Fourier method was used to solve parabolic wave equations in underwater acoustics and optics in the 1970s, where it propagates a field by alternating a free-space step in the wavenumber domain with a phase screen in space. Stoffa, Fokkema, de Luna Freire and Kessinger (1990) brought it to seismic migration as a cheap way to handle lateral velocity changes in phase-shift migration. Later work added finite-difference corrections and higher-order screens for wider angles.

## References
