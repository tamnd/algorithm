---
tag: ZFVWK9
kind: algorithm
slug: kirchhoff-migration
name: Kirchhoff migration
aliases:
- diffraction summation migration
area: imaging-and-inverse-problems/seismic-imaging
level: core
summary: "Image each subsurface point by a weighted sum of the data along the diffraction traveltime curve of that point."
solves: [seismic-migration]
model: real-ram
complexity:
  vars: {t: "the number of time samples", x: "the number of traces (and of image columns)", z: "the number of image depths", a: "the number of traces in the aperture"}
  time: {filter: "O(x t log t)", sum: "O(z x a)", total: "O(x t log t + z x a)"}
  space: {extra: "O(x t + z x)"}
properties: {deterministic: true, linear_in_data: true, high_frequency_approximation: true, irregular_geometry: true, target_oriented: true}
history:
  year: 1978
  people: [William A. Schneider]
  note: Schneider derived integral (Kirchhoff) migration from the wave equation in 1978, with the obliquity and spreading weights and the half-derivative filter; Bleistein (1987) gave the weights that make it an asymptotic inverse.
prereqs: [exploding-reflector-model, seismic-migration]
see_also: [phase-shift-migration, stolt-migration, reverse-time-migration, least-squares-migration, imaging-condition, eikonal-equation, delay-and-sum-beamforming, sar-backprojection]
sources:
  - paper: doi:10.1190/1.1440828
    title: William A. Schneider, Integral formulation for migration in two and three dimensions, Geophysics 43(1), 1978, 49 to 76
    locator: the Kirchhoff integral for migration with its weights and filter
  - paper: doi:10.1190/1.1442363
    title: Norman Bleistein, On the imaging of reflectors in the earth, Geophysics 52(7), 1987, 931 to 942
    locator: the asymptotic inversion weights for true-amplitude Kirchhoff migration
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001
    locator: Chapter 4 (migration), Kirchhoff migration and its 2D and 3D filters
---

Kirchhoff migration builds the image one point at a time. For each image point it sums the data along the diffraction curve of that point, the curve of times at which a small scatterer at the point would appear in the record. Each sample in the sum gets an obliquity and spreading weight, and the traces are first filtered by a half derivative. In constant velocity the zero-offset curve is $t = (2/v)\sqrt{z^2 + (x - x_r)^2}$. The method is a high-frequency (ray) approximation of the exact downward continuation of [phase-shift migration](/phase-shift-migration/), and it is the adjoint of a ray-based modeling operator, not its inverse (theorems). Because it needs only traveltimes and weights, it works for any acquisition geometry and for any velocity for which the traveltimes can be computed, for example with the [eikonal equation](/eikonal-equation/).

## In plain words

A small scatterer in the ground sends an echo to every receiver, and the echo arrives later at receivers that are farther away. On the record the echo draws a curve shaped like an upside-down bowl. To test whether a point in the ground scatters, compute its bowl, go along that bowl on the record, and add up the values. If a scatterer is really there, the values line up and the sum is large. If not, positive and negative values cancel. Do this for every point and you get a picture. Two small corrections make the strengths right: echoes that arrive at a steep angle or from far away get less weight, and each trace gets a fixed filter that sharpens it before the sums.

## The problem

Given a zero-offset section $d(t, x_r)$ on traces $x_r = r\Delta x$ with the time step $\Delta t$, and a constant velocity $v$, compute the image $m(x, z)$ at $x = j\Delta x$, $z = i\Delta z$. This is [seismic migration](/seismic-migration/) in the [exploding reflector model](/exploding-reflector-model/), where waves travel up with $v' = v/2$, so the traveltime from the image point to the trace is $\rho/v'$ with $\rho = \sqrt{z^2 + (x - x_r)^2}$.

## The algorithm

The 2D zero-offset formula (Schneider 1978; Yilmaz 2001, Chapter 4) is
$$m(x, z) = \Delta x \sum_r \frac{\cos\theta}{\sqrt{2\pi v'\rho}}\; h_r\Big(\frac{\rho}{v'}\Big), \qquad \cos\theta = \frac{z}{\rho},$$
where $h_r$ is trace $r$ filtered by the half derivative with the symbol $(-i\omega)^{1/2}$ in the sign convention $U(\omega) = \int u(t) e^{-i\omega t}\,dt$. Texts that use the opposite sign write the same filter as $(i\omega)^{1/2}$.

```pseudo id=main
KIRCHHOFF-MIGRATION(d, Δt, Δx, Δz, n_z, v)     ▷ constant velocity v, v' = v / 2
L1  h_r ← trace r filtered by (-iω)^(1/2), for every trace r
L2  for every image point (i, j) with i ≥ 1 do      ▷ z = iΔz, x = jΔx
L3      s ← 0
L4      for every trace r do      ▷ x_r = rΔx
L5          ρ ← sqrt(z² + (x - x_r)²);  w ← (z / ρ) / sqrt(2π v' ρ)
L6          s ← s + w · h_r(ρ / v')      ▷ linear interpolation in time, 0 outside the record
L7      image[i][j] ← Δx · s
L8  return image
```

Line L1 applies the half-derivative filter to every trace with one FFT and one inverse FFT per trace. Lines L2 to L7 are the diffraction sum. Line L5 computes the distance to the trace, the obliquity factor $\cos\theta = z/\rho$ and the 2D spreading factor $1/\sqrt{\rho}$. Line L6 reads the filtered trace at the diffraction time $\rho/v' = 2\rho/v$; the time almost never falls on a sample, so the code interpolates linearly. Row 0 ($z = 0$) is left at zero, because the weight needs $z > 0$. The sum over $r$ can be limited to an aperture of $a$ traces around $x$, which saves time and removes noise from far traces.

## Example

**One weight by hand.** For $v = 2000$ m/s ($v' = 1000$ m/s), the image point $(x, z) = (0, 300)$ m and the trace at $x_r = 400$ m, $\rho = 500$ m. The diffraction time is $500/1000 = 0.5$ s, and the weight is $(300/500)/\sqrt{2\pi \cdot 1000 \cdot 500} = 0.6/1772.45 = 3.385 \times 10^{-4}$.

**A point diffractor.** The test uses the case of [phase-shift migration](/phase-shift-migration/): $v = 3000$ m/s, a point at $x_0 = 160$ m, $z_0 = 192$ m, 32 traces at 10 m, 64 samples at 4 ms, and $\Delta z = 6$ m. The image peaks within one sample of row 32 and column 16. On rows 4 to 47 its relative difference to the phase-shift image is about 0.09 (a measurement); the difference comes from the high-frequency approximation, the finite line of traces and the linear interpolation in time.

## Correctness

The full proof is in proofs/correctness.md.

- **What the code computes (theorem).** For $i \ge 1$, line L8 returns exactly the weighted sum of the formula, with $h_r$ read by linear interpolation.
- **The kernel (theorem).** For one frequency, the downward continuation of phase shift, written as an integral over the traces, has the kernel $G = \frac{ik}{2}\frac{z}{\rho}H_1^{(1)}(k\rho)$ with $k = \omega/v'$. This follows from the plane-wave (Weyl) form of the 2D Green's function.
- **High-frequency limit (theorem).** As $k\rho \to \infty$, $G = \frac{z/\rho}{\sqrt{2\pi v'\rho}}(-i\omega)^{1/2}e^{i\omega\rho/v'}(1 + O(1/(k\rho)))$. Integrated over $\omega$, this gives the formula. So the Kirchhoff sum equals the exact one-way image up to a relative error that goes to zero with the frequency times the distance.
- **Adjoint pair (theorem).** The diffraction sum of lines L2 to L8 and the modeling routine that spreads each image value along its curve are exact transposes. The test checks $\langle S d, m\rangle = \langle d, S^* m\rangle$ to $10^{-12}$.

The replacement of the integral over traces by a sum and of $h_r(t)$ by an interpolant are discretizations without an error bound here (heuristic steps).

## Complexity

- **Real-ram.** Line L1 costs $O(n_t \log n_t)$ per trace with an FFT, $O(n_x n_t \log n_t)$ in total. The sum costs $O(1)$ per image point and trace: $O(n_z n_x a)$ with an aperture of $a$ traces, or $O(n_z n_x^2)$ with the whole line.
- **3D.** For a 3D image of $N$ points and $T$ traces, the cost is $O(N T)$, which is why production codes limit the aperture and compute the traveltimes on a coarse grid.
- **Space.** The filtered traces and the image, $O(n_x n_t + n_z n_x)$.

## Properties

- **Any geometry.** The sum needs only the traveltime and the weight from each image point to each trace. Irregular, sparse or 3D acquisition is no harder than a regular line.
- **Target oriented.** Any subset of image points can be computed alone, for example one region of interest.
- **Linear in the data.** The image is a linear function of the section, and the method is the adjoint of the matching modeling operator.
- **High-frequency approximation.** Amplitudes are right only when the wavelength is small compared with the distance and with the scale of velocity changes. Caustics and multiple arrivals break the single-traveltime form.
- **Aliasing.** When the diffraction curve is steep and the traces are far apart, the sum picks up aliased energy; anti-alias filters that depend on the local slope are a common addition.

## Variants and improvements

- **Variable velocity.** Replace $\rho/v'$ by the traveltime from a ray tracer or an [eikonal equation](/eikonal-equation/) solver such as the [fast marching method](/fast-marching-method/), and the weights by the ray amplitudes.
- **Prestack Kirchhoff migration.** For data with offset, the time is the sum of the source-to-point and point-to-receiver traveltimes, and the sum runs over all source and receiver pairs.
- **True-amplitude migration.** Bleistein (1987) gave weights that make the sum an asymptotic inverse of the Born modeling, so the image amplitude is the reflection coefficient.
- **[Least-squares migration](/least-squares-migration/).** Use the sum as the adjoint in a conjugate gradient loop to correct amplitudes and the effect of the finite line.
- **Beam migration.** Sum along local plane-wave beams instead of single curves, which handles multiple arrivals.

## When to use it

Use Kirchhoff migration when the geometry is irregular, when only part of the image is needed, or when a fast image with ray traveltimes is enough, as in velocity analysis by migration. It is the standard prestack depth migration in many workflows. Prefer wave-equation methods ([phase-shift](/phase-shift-migration/), [split-step Fourier](/split-step-fourier-migration/) or [reverse-time migration](/reverse-time-migration/)) under complex velocity, such as below salt, where the ray approximation fails. The same idea, with other weights, is [delay-and-sum beamforming](/delay-and-sum-beamforming/) in ultrasound and [backprojection](/sar-backprojection/) in radar.

## Pitfalls

- **No half-derivative filter.** Leaving out line L1 gives an image whose wavelet is too smooth and shifted in phase by 45 degrees. Filter every trace first, as in line L1.
- **The wrong filter sign.** With the transform $e^{-i\omega t}$, the filter is $(-i\omega)^{1/2}$. Using $(i\omega)^{1/2}$ in line L1 turns the phase the wrong way. Check the sign with a point diffractor.
- **The two-way time.** Reading the trace at $\rho/v$ in line L6 puts every point at twice its depth. Zero-offset data need $\rho/v' = 2\rho/v$, as in line L6.
- **Nearest sample.** Rounding $\rho/v'$ to the nearest sample in line L6 adds a time error of up to half a sample, which is noise at high frequencies. Interpolate, as in line L6.

## Implementations

## History

Diffraction stacking began as a graphical method before computers: interpreters summed the data along hyperbolas drawn on the record. Schneider (1978) derived the sum from the Kirchhoff integral of the wave equation, with the obliquity and spreading weights and the half-derivative filter in 2D and the derivative in 3D. Bleistein (1987) and his coworkers derived weights that make the sum an asymptotic inverse of the Born modeling operator, which gave true-amplitude migration. Kirchhoff prestack depth migration then became a standard imaging tool of the industry.

## References
