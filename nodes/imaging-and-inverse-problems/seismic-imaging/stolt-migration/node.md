---
tag: HTV0W8
kind: algorithm
slug: stolt-migration
name: Stolt migration
aliases:
- f-k migration
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "Migrate zero offset data in a constant velocity medium by a 2D FFT, a change of variables from frequency to vertical wavenumber, and an inverse FFT."
solves: [seismic-migration]
model: real-ram
complexity:
  vars: {t: "the number of time samples", x: "the number of traces", z: "the number of depth samples", p: "the padding factor of the time axis"}
  time: {total: "O(p t x log(p t x) + z x log(z x))", mapping: "O(z x)"}
  space: {extra: "O(p t x + z x)"}
properties: {deterministic: true, exact_for: "constant velocity in the one-way model, up to the interpolation", lateral_velocity: false, depth_velocity: false, steep_dips: true}
history:
  year: 1978
  people: [Robert H. Stolt]
  note: Stolt published migration by Fourier transform in Geophysics in 1978, a change of variables from frequency to vertical wavenumber that images constant-velocity data with two FFTs.
prereqs: [phase-shift-migration, fast-fourier-transform]
see_also: [omega-k-algorithm, phase-shift-migration, kirchhoff-migration, split-step-fourier-migration, exploding-reflector-model, sinc-interpolation, seismic-migration]
sources:
  - paper: doi:10.1190/1.1440826
    title: R. H. Stolt, Migration by Fourier transform, Geophysics 43(1), 1978, 23 to 48
    locator: the change of variables from frequency to vertical wavenumber for constant velocity
  - paper: doi:10.1190/1.1440899
    title: Jeno Gazdag, Wave equation migration with the phase-shift method, Geophysics 43(7), 1978, 1342 to 1351
    locator: the phase-shift form of the same downward continuation
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001
    locator: Chapter 4 (migration), frequency-wavenumber migration
---

Stolt migration images a zero-offset section recorded over a medium of constant velocity. It takes the 2D FFT of the section, moves every sample of the spectrum from the frequency $\omega$ to the vertical wavenumber $k_z$ by the mapping $\omega = \operatorname{sgn}(k_z)\, v' \sqrt{k_x^2 + k_z^2}$ with a Jacobian weight, and takes the inverse FFT. The result is the same as [phase-shift migration](/phase-shift-migration/) with one constant velocity, but all depth steps are done at once. The [omega-k algorithm](/omega-k-algorithm/) of synthetic aperture radar uses the same change of variables (it is often called the Stolt mapping there). The difference is in the data: the radar algorithm first multiplies the spectrum by a reference function for the range of the scene center, and its velocity is the speed of light, while seismic data need the half velocity $v' = v/2$ of the [exploding reflector model](/exploding-reflector-model/).

## In plain words

A recorded section is a mix of simple waves, each with one frequency and one tilt. In a medium where the speed is the same everywhere, every simple wave comes from one simple pattern in the image, a set of parallel stripes at one depth spacing and one tilt. The rule that links the wave to the stripes is fixed: the frequency of the wave is the speed times the number of stripes per meter. So the image can be built by moving each part of the spectrum of the record to a new place in the spectrum of the image and weighting it. Two fast Fourier transforms and one pass of moving values do the whole job. The new places do not fall on the grid points of the old spectrum, so the method reads values between grid points by interpolation.

## The problem

Given a zero-offset section $d(t, x)$ sampled at $t = k\Delta t$, $x = j\Delta x$, and the constant velocity $v$, find the image $m(x, z)$ on a grid of $n_z$ depths with the step $\Delta z$. This is [seismic migration](/seismic-migration/) in the [exploding reflector model](/exploding-reflector-model/): the section is the upgoing field at $z = 0$ of the wave equation with the velocity $v' = v/2$, and the image is the field at $t = 0$.

## The algorithm

The phase-shift image is $m(x, z) = (2\pi)^{-2}\iint D(\omega, k_x)\, e^{i k_z z + i k_x x}\, d\omega\, dk_x$ with $k_z = \operatorname{sgn}(\omega)\sqrt{\omega^2/v'^2 - k_x^2}$. For a fixed $k_x$, change the variable from $\omega$ to $k_z$. The inverse map is $\omega(k_z, k_x) = \operatorname{sgn}(k_z)\, v'\sqrt{k_x^2 + k_z^2}$, and $d\omega = J\, dk_z$ with $J = v'|k_z|/\sqrt{k_x^2 + k_z^2}$. So the image is the inverse 2D Fourier transform of
$$M(k_z, k_x) = \frac{v'|k_z|}{\sqrt{k_x^2 + k_z^2}}\, D\big(\omega(k_z, k_x), k_x\big).$$

```pseudo id=main
STOLT-MIGRATION(d, Δt, Δx, Δz, n_z, v, p)     ▷ constant velocity v, padding factor p
L1  pad d with zeros to p · n_t time samples
L2  D ← DFT2(d)
L3  for every pair (i, j) of the n_z × n_x image spectrum do
L4      r ← sqrt(k_x,j² + k_z,i²);  ω ← sgn(k_z,i) v' r;  J ← v' |k_z,i| / r      ▷ v' = v / 2; J ← 0 if r = 0
L5      if J = 0 or ω is outside the frequency band of D then M[i][j] ← 0 and go to the next pair
L6      D_ω ← linear interpolation of D[·][j] at the frequency ω
L7      M[i][j] ← (Δt / Δz) · J · D_ω
L8  m ← IDFT2(M)
L9  return Re m
```

Line L1 pads the time axis so that the spectrum is sampled finely in $\omega$; this makes the interpolation of line L6 accurate. Line L2 is one 2D FFT. Lines L3 to L7 fill the spectrum of the image: for every image wavenumber pair $(k_{z,i}, k_{x,j})$, line L4 finds the data frequency that maps to it and the Jacobian, and line L6 reads the data spectrum there. The factor $\Delta t/\Delta z$ in line L7 converts the sums of the DFT to the integrals of the formula: the forward DFT in time is the integral divided by $\Delta t$, and the inverse DFT in depth is the inverse integral divided by $\Delta z$. Line L5 drops the point $k_z = 0$ and the frequencies at the edge of the band, where the interpolation has no neighbor. Lines L8 and L9 are one inverse 2D FFT.

## Example

**The mapping by hand.** Take $v = 2000$ m/s, so $v' = 1000$ m/s, and the image wavenumbers $k_z = 0.03$ and $k_x = 0.04$ rad/m. Then $r = 0.05$, $\omega = 1000 \cdot 0.05 = 50$ rad/s and $J = 1000 \cdot 0.03/0.05 = 600$ m/s. For $k_z = -0.03$ the frequency is $-50$ rad/s and the Jacobian is again 600. For $k_x = 0$ the mapping is $\omega = v' k_z$ and $J = v'$: a plain stretch from time to depth, $z = v' t$.

**A flat event.** With $\Delta z = v'\Delta t$ and a padded length that is a multiple of $n_z$, every frequency that line L4 asks for at $k_x = 0$ is a grid frequency, so line L6 is exact. A section that is the same on every trace then maps sample by sample to depth: in the test, every image row equals the Ricker trace at the matching time within $10^{-6}$ (the difference is the band edge removed by line L5).

**A point diffractor.** In the test case of [phase-shift migration](/phase-shift-migration/) (velocity 3000 m/s, point at $x_0 = 160$ m and $z_0 = 192$ m, $\Delta z = 6$ m), the image peaks within one sample of row 32, column 16. The relative difference to the phase-shift image depends on the padding (a measurement on this case):

| padding factor $p$ | 1 | 2 | 4 | 8 |
|---|---|---|---|---|
| relative difference to phase shift | 0.84 | 0.27 | 0.094 | 0.067 |

Without padding the interpolation error is as large as the image itself. The code uses $p = 4$.

## Correctness

The full proof is in proofs/correctness.md.

- **The change of variables (theorem).** For fixed $k_x$, the map $\omega \mapsto k_z$ is a smooth bijection from each branch $\omega > v'|k_x|$ and $\omega < -v'|k_x|$ onto $k_z > 0$ and $k_z < 0$. On both branches $d\omega/dk_z = v'|k_z|/\sqrt{k_x^2 + k_z^2} > 0$, so the integral keeps its orientation and the formula for $M$ holds.
- **The discrete scale (theorem).** For band-limited samples, the DFT sums equal the integrals times $1/(\Delta t\,\Delta x)$ and $1/(\Delta z\,\Delta x)$, which gives the factor $\Delta t/\Delta z$ of line L7.
- **What the code computes (theorem).** The output is the inverse transform of the discrete Stolt mapping with $D(\omega)$ replaced by its linear interpolant. Where the requested frequencies fall on the DFT grid, it is exact.
- **The interpolation error (heuristic, with a measurement).** Linear interpolation of the spectrum is the only approximation. Its effect is shown in the table above.

## Complexity

- **Real-ram, with FFTs.** Line L2 costs $O(p n_t n_x \log(p n_t n_x))$, lines L3 to L7 cost $O(n_z n_x)$ (one interpolation per image sample), and line L8 costs $O(n_z n_x \log(n_z n_x))$.
- **Against phase shift.** Phase shift with $n_z$ steps costs $O(n_z n_t n_x)$, so Stolt is faster by about $n_z/\log(n_t n_x)$, at the price of the interpolation error and of a single velocity.
- **Space.** The padded spectrum holds $p n_t n_x$ complex numbers.

## Properties

- **All dips.** The mapping is exact for every dip up to 90 degrees in the one-way model.
- **One velocity only.** A single constant velocity is assumed. Stolt (1978) also gave an approximate stretch of the time axis for a velocity that changes slowly with depth.
- **Periodic edges.** As with every DFT method, energy wraps around in $t$, $x$ and $z$. Pad in $x$ as well when events reach the edges.
- **Real image.** Because $J$ uses $|k_z|$, the mapped spectrum keeps the conjugate symmetry $M(-k_z, -k_x) = \overline{M(k_z, k_x)}$, and the image of real data is real.

## Variants and improvements

- **Better interpolation.** [Sinc interpolation](/sinc-interpolation/) with a short window, or a longer padding, reduces the error of line L6 at a higher cost.
- **The [omega-k algorithm](/omega-k-algorithm/).** The same mapping focuses synthetic aperture radar data after a reference function multiply.
- **Prestack Stolt migration.** A mapping in four wavenumbers images data with offset in constant velocity.
- **Stolt stretch.** A change of the time variable makes data from a velocity $v(z)$ close to constant-velocity data, with a factor that controls the error.
- **[Phase-shift migration](/phase-shift-migration/).** For a velocity $v(z)$, give up the single mapping and step down in depth.

## When to use it

Use Stolt migration for a fast first image when one velocity is a fair model, for velocity scans (migrate with many trial velocities and keep the best focus), and as a building block of the radar omega-k algorithm. Do not use it when the velocity changes strongly: the error grows with the depth and the dip. Then use [phase-shift migration](/phase-shift-migration/) for $v(z)$, or [split-step Fourier migration](/split-step-fourier-migration/) and [reverse-time migration](/reverse-time-migration/) for $v(x, z)$.

## Pitfalls

- **The Jacobian without the absolute value.** Writing $J \leftarrow v' k_z/r$ in line L4 gives a negative weight for $k_z < 0$, breaks the conjugate symmetry, and leaves a large imaginary part. Use $v'|k_z|/r$, as in line L4.
- **No padding.** Skipping line L1 makes the interpolation of line L6 coarse; in the example the error rises from 0.094 to 0.84. Pad by 4 or more, as in line L1.
- **The full velocity.** Using $v$ instead of $v' = v/2$ in line L4 doubles every depth. Zero-offset data need the half velocity.
- **The missing scale.** Leaving out $\Delta t/\Delta z$ in line L7 gives the right shape but the wrong amplitude. Keep the factor of line L7.

## Implementations

## History

Stolt (1978) derived the migration of constant-velocity data by a change of variables in the Fourier domain, and gave the stretch for depth-varying velocity in the same paper. Gazdag (1978) published the phase-shift method in the same year. The mapping became a standard tool of seismic processing for its speed. Radar engineers later took the same mapping into the omega-k (wavenumber domain) algorithm for synthetic aperture radar.

## References
