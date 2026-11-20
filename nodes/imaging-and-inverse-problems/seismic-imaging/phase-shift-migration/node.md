---
tag: PNBG5B
kind: algorithm
slug: phase-shift-migration
name: Phase-shift migration
aliases:
- Gazdag migration
area: imaging-and-inverse-problems/seismic-imaging
level: advanced
summary: "Extrapolate the wavefield down in depth steps by a phase shift of each frequency and wavenumber, for velocity that varies only with depth."
solves: [seismic-migration]
model: real-ram
complexity:
  vars: {t: "the number of time samples", x: "the number of traces", z: "the number of depth steps"}
  time: {fft_transform: "O(t x log(t x))", depth_steps: "O(z t x)", total: "O(z t x + t x log(t x))"}
  space: {extra: "O(t x + z x)"}
properties: {deterministic: true, exact_for: "velocity v(z) in the one-way model", lateral_velocity: false, steep_dips: true, unconditionally_stable: true}
history:
  year: 1978
  people: [Jeno Gazdag]
  note: Gazdag published migration by phase shift in Geophysics in 1978, as a frequency-domain downward continuation that is exact for a velocity that changes only with depth.
prereqs: [exploding-reflector-model, seismic-migration, discrete-fourier-transform, wave-equation]
see_also: [stolt-migration, split-step-fourier-migration, finite-difference-migration, kirchhoff-migration, reverse-time-migration, fast-fourier-transform, omega-k-algorithm]
sources:
  - paper: doi:10.1190/1.1440899
    title: Jeno Gazdag, Wave equation migration with the phase-shift method, Geophysics 43(7), 1978, 1342 to 1351
    locator: the phase-shift downward continuation and the imaging at t = 0
  - paper: doi:10.1111/j.1365-2478.1976.tb00934.x
    title: D. Loewenthal, L. Lu, R. Roberson and J. Sherwood, The wave equation applied to migration, Geophysical Prospecting 24(2), 1976, 380 to 399
    locator: the exploding reflector model of zero-offset data
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001
    locator: Chapter 4 (migration), frequency-wavenumber migration
  - book: isbn:9780865423046
    title: Jon F. Claerbout, Imaging the Earth's Interior, Blackwell, 1985
    locator: the chapters on downward continuation in the frequency domain
---

Phase-shift migration images a zero-offset section in the frequency-wavenumber domain. It transforms the section in time and in space, and then it steps down in depth. At each step it multiplies every plane wave by the phase factor $e^{i k_z \Delta z}$ of the one-way wave equation, and it reads the image row as the field at time zero. In each depth layer the velocity must be the same at all $x$. Under that condition the method is exact for the one-way equation, at all dips up to 90 degrees (a theorem). It is slower than [Stolt migration](/stolt-migration/), which does the same work for one constant velocity with one change of variables. [Split-step Fourier migration](/split-step-fourier-migration/) adds a correction for lateral changes.

## In plain words

Record a line of echoes at the surface. Imagine that every reflector in the ground sent out a pulse at the same moment, and that the pulses travel up at half the true speed. Then the record is a picture of that one upward wave as it reaches the surface. If we could move the receivers down into the ground, the wave would arrive earlier at each depth. At the exact depth of a reflector, its pulse would arrive at time zero. Phase-shift migration moves the receivers down step by step. It splits the record into simple waves of one frequency and one tilt. Each simple wave moves down by one step when you turn its phase by an amount that depends on the speed of the layer. After each step, the value at time zero is the picture at that depth.

## The problem

Given a zero-offset section $d(t, x)$ (one trace per surface position, with source and receiver at the same point), sampled at $t = k\Delta t$ and $x = j\Delta x$, and the velocity $v_i$ of each depth layer $i\Delta z \le z < (i + 1)\Delta z$, find the reflectivity image $m(x, z)$. This is the [seismic migration](/seismic-migration/) problem for a velocity that changes only with depth. The model is the [exploding reflector model](/exploding-reflector-model/): the section is the upgoing field at $z = 0$ of the [wave equation](/wave-equation/) with the half velocity $v' = v/2$, and the image is the same field at $t = 0$.

## The algorithm

The time transform is $U(\omega) = \sum_t u(t) e^{-i\omega t}$, and the space transform uses $e^{-i k_x x}$. With this sign an upgoing wave reaches depth $z$ a time $z/v'$ before it reaches the surface, so one step down multiplies its transform by $e^{+i k_z \Delta z}$ with
$$k_z = \operatorname{sgn}(\omega)\sqrt{\frac{\omega^2}{v'^2} - k_x^2}.$$

```pseudo id=main
PHASE-SHIFT-MIGRATION(d, Δt, Δx, Δz, v)     ▷ d: n_t × n_x section, v[i]: velocity of layer i
L1  P ← DFT2(d)                               ▷ P[k][j] belongs to (ω_k, k_x,j)
L2  for i ← 0 to n_z - 1 do
L3      row[j] ← (1 / n_t) Σ_k P[k][j] for every j      ▷ inverse time transform at t = 0
L4      image[i] ← Re IDFT(row)
L5      v' ← v[i] / 2
L6      for every pair (k, j) do
L7          if ω_k ≠ 0 and ω_k² / v'² > k_x,j² then k_z ← sgn(ω_k) sqrt(ω_k² / v'² - k_x,j²)
L8          else P[k][j] ← 0 and go to the next pair    ▷ evanescent or zero frequency
L9          P[k][j] ← P[k][j] · exp(i k_z Δz)
L10 return image
```

Line L1 takes the 2D [discrete Fourier transform](/discrete-fourier-transform/) of the section once. The signed frequencies are $\omega_k = 2\pi k/(n_t\Delta t)$ for $2k < n_t$ and $2\pi(k - n_t)/(n_t\Delta t)$ otherwise, and $k_{x,j}$ is defined in the same way. Lines L3 and L4 form the image row of the current depth: the inverse transform in time at $t = 0$ is the plain average over the frequencies, because $e^{i\omega \cdot 0} = 1$, and then an inverse DFT in $x$ gives the row. Lines L5 to L9 move the whole field one layer down. Line L8 removes the evanescent waves, whose amplitude would grow without bound if they were continued, and the zero frequency, which carries no image. Line L9 is the phase shift of the layer. A field that is real stays real, because the factor at $(-\omega, -k_x)$ is the complex conjugate of the factor at $(\omega, k_x)$.

## Example

**A flat reflector in two layers (by hand).** Take $v = 2000$ m/s from the surface down to 100 m and $v = 3000$ m/s below, with $\Delta z = 10$ m. A section that is the same on every trace holds only the wavenumber $k_x = 0$. Then $k_z = \omega/v'$ and line L9 multiplies by $e^{i\omega\,\Delta z/v'}$: each row shifts the trace earlier by the vertical two-way time $2\Delta z/v$ of its layer. Rows 0 to 9 take $2 \cdot 10/2000 = 0.01$ s each, so row 10 is at 0.1 s. Each later row takes $2 \cdot 10/3000 = 0.00667$ s. An event at $t = 0.2$ s therefore lands at row $10 + 0.1/0.00667 = 25$, at depth 250 m. The test runs this case with a Ricker wavelet of peak value 1 at 0.2 s. The image peaks at row 25 with the value 0.9999999975 (a measurement; the small loss is the zero frequency and the band edge removed by line L8).

**A point diffractor.** A point at $x_0 = 160$ m, $z_0 = 192$ m in the constant velocity 3000 m/s gives a hyperbola $t(x) = (2/v)\sqrt{z_0^2 + (x - x_0)^2}$ in the section ($n_t = 64$, $\Delta t = 4$ ms, $n_x = 32$, $\Delta x = 10$ m). With $\Delta z = 6$ m the image collapses the hyperbola to one spot at row $192/6 = 32$, column $160/10 = 16$, and the values far from the spot are below a quarter of the peak. In 2D the migrated pulse is not symmetric, so its peak can move by a sample. In the test, the raw data peak within one sample of $(32, 16)$, and data whose traces are first filtered by $(i\omega)^{1/2}$ peak exactly at $(32, 16)$ (measurements).

## Correctness

The full proof is in proofs/correctness.md.

- **One layer (theorem).** In a layer of constant velocity, every non-evanescent plane wave satisfies $P_{zz} + k_z^2 P = 0$, and the upgoing solution is $P(z + \Delta z) = P(z)\,e^{i k_z \Delta z}$ with the sign of $k_z$ equal to the sign of $\omega$.
- **Loop invariant (theorem).** At the start of pass $i$ of line L2, $P$ is the transform of the section continued through layers $0, \ldots, i - 1$, with the evanescent parts removed. Lines L3 and L4 store the real part of that field at $t = 0$.
- **Exactness for $v(z)$ (theorem).** If the true field is a finite sum of DFT plane waves without evanescent parts, the image is exactly the field $p(0, x_j, z_i)$ of the model. For vertical waves the row $i$ is the trace at the two-way vertical time $\tau_i = \sum_{l < i} 2\Delta z/v_l$.

The exactness is a statement about the one-way model on a periodic grid. Real sections are not periodic, and the exploding reflector model ignores multiples.

## Complexity

- **Transform (real-ram).** Line L1 is one 2D DFT of an $n_t \times n_x$ array: $O(n_t n_x \log(n_t n_x))$ with an FFT and $O(n_t n_x (n_t + n_x))$ with direct sums.
- **Depth steps.** Each pass of line L2 costs $O(n_t n_x)$ for line L3, $O(n_x \log n_x)$ for line L4 and $O(n_t n_x)$ for lines L6 to L9. With $n_z$ steps the total is $O(n_z n_t n_x + n_t n_x \log(n_t n_x))$.
- **Space.** The array $P$ holds $n_t n_x$ complex numbers and the image $n_z n_x$ real numbers.

The cost does not depend on the dip of the events. In practice the frequencies outside the band of the source are skipped, which divides the work by the ratio of the Nyquist frequency to the band.

## Properties

- **All dips.** The phase shift uses the exact square root, so dips up to 90 degrees are imaged correctly (in the one-way model). The 15-degree [finite-difference migration](/finite-difference-migration/) uses an approximation of the root.
- **Unconditionally stable.** Every factor in line L9 has modulus 1 and line L8 sets the others to 0, so no step increases the energy. Any $\Delta z$ can be used; a large step only samples the image coarsely.
- **Linear in the data.** The image is a linear function of the section.
- **Periodic edges.** The DFT treats the section as periodic in $t$ and $x$, so energy that leaves one side enters at the other. Pad with zeros to avoid wrap-around.
- **No lateral velocity change.** Inside a layer the velocity must be the same at every $x$; otherwise the plane waves are not solutions.

## Variants and improvements

- **[Stolt migration](/stolt-migration/).** For one constant velocity, all depth steps can be done at once by a change of variables from $\omega$ to $k_z$, with one inverse FFT instead of $n_z$ passes.
- **Phase shift plus interpolation (PSPI).** Gazdag and Sguazzero (1984) continue the field with a few reference velocities and interpolate between the results at each $x$, which handles lateral velocity changes.
- **[Split-step Fourier migration](/split-step-fourier-migration/).** One reference velocity per layer, and a phase correction in the space domain for the local velocity.
- **Prestack depth migration.** The same phase shift, applied to sources and receivers together (the double square root equation), migrates data with offset.
- **Time migration.** With the vertical time as the depth variable, the steps follow the record time and the velocity is the rms velocity.

## When to use it

Use phase-shift migration when the velocity changes only with depth and you want an exact image at all dips. It is a reference method for testing faster or more general methods, as in the tests on this site, where Stolt, Kirchhoff, split-step and finite-difference migration are all checked against it. For one constant velocity, Stolt migration is faster. For strong lateral changes, use split-step Fourier, PSPI or [finite-difference migration](/finite-difference-migration/), and for steep dips with complex velocity use [reverse-time migration](/reverse-time-migration/).

## Pitfalls

- **The wrong sign of the phase.** With the transform $e^{-i\omega t}$, writing line L9 as $P \cdot e^{-i k_z \Delta z}$ continues the field up instead of down, and a diffractor spreads into a wider hyperbola. Use $e^{+i k_z \Delta z}$ as in line L9. Claerbout and Yilmaz use the other transform sign, so their formula has the other sign too.
- **The full velocity.** Using $v[i]$ in line L5 instead of $v[i]/2$ puts every reflector at twice its depth. Zero-offset data need the half velocity of the exploding reflector model, as in line L5.
- **Continuing evanescent waves.** If line L8 keeps the pairs with $\omega_k^2/v'^2 < k_{x,j}^2$ and uses an imaginary $k_z$ of the wrong sign, the factor grows exponentially and the image fills with noise. Set them to zero, as in line L8.
- **Imaging after the step.** Moving lines L3 and L4 after line L9 shifts every row down by one step. The image of depth $z_i$ is taken before the field is moved to $z_{i+1}$.

## Implementations

## History

Claerbout (1971) and Claerbout and Doherty (1972) introduced downward continuation of seismic data with the one-way wave equation, solved by finite differences. Loewenthal, Lu, Roberson and Sherwood (1976) described zero-offset data with the exploding reflector model and the half velocity. In 1978 Gazdag solved the same downward continuation in the frequency-wavenumber domain, where it is exact for a velocity that changes only with depth, and Stolt published the constant-velocity version in the same year. Gazdag and Sguazzero (1984) extended the method to lateral velocity changes with phase shift plus interpolation.

## References
