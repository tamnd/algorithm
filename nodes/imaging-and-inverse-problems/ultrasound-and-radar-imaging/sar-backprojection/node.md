---
tag: KA63T0
kind: algorithm
slug: sar-backprojection
name: Time-domain backprojection for SAR
aliases:
- global backprojection SAR
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: core
summary: "Form a SAR image by summing at each pixel the range compressed echoes at the round trip delay of that pixel, for any flight path."
solves: [sar-image-formation]
model: real-ram
complexity:
  vars: {P: the number of pulses, n: the number of pixels along one side of the image, N: the number of samples per pulse, F: the upsampling factor}
  time: {worst: O(P (n^2 + F N log(F N)))}
  space: {extra: O(n^2 + F N), data: O(P N)}
properties: {deterministic: true, linear_in_data: true, recursive: false, exact: false}
history:
  year: 1992
  people: [Mita D. Desai, W. Kenneth Jenkins]
  note: "Desai and Jenkins formed spotlight SAR images by convolution backprojection in 1992, carrying the backprojection of computed tomography to radar; the same sum along the true range of each pixel serves any flight path."
prereqs: [sar-image-formation, back-projection-operator]
see_also: [fast-factorized-backprojection, saft, total-focusing-method, polar-format-algorithm, omega-k-algorithm, kirchhoff-migration, delay-and-sum-beamforming, phase-gradient-autofocus]
sources:
  - paper: doi:10.1109/83.199920
    title: "Mita D. Desai and W. Kenneth Jenkins, Convolution backprojection image reconstruction for spotlight mode synthetic aperture radar, IEEE Transactions on Image Processing 1(4), 1992, 505 to 517"
    locator: "the backprojection sum over the pulses with 1D interpolation along each filtered pulse, and its O(N^3) cost (general locator)"
  - paper: doi:10.1109/TAES.2003.1238734
    title: "Lars M. H. Ulander, Hans Hellsten and Gunnar Stenstrom, Synthetic-aperture radar processing using fast factorized back-projection, IEEE Transactions on Aerospace and Electronic Systems 39(3), 2003, 760 to 776"
    locator: "the global (direct) backprojection that the fast algorithm approximates, for a general flight path (general locator)"
  - book: isbn:0471297062
    title: "Mehrdad Soumekh, Synthetic Aperture Radar Signal Processing with MATLAB Algorithms, Wiley, 1999"
    locator: "the time-domain reconstruction methods (general locator)"
---

Time-domain backprojection forms a [synthetic aperture radar](/synthetic-aperture-radar/) image directly from the definition of focusing. For every pixel and every pulse, it computes the range from the antenna at that pulse to the pixel, reads the range compressed echo at the matching round trip delay, removes the carrier phase of that range, and adds the result to the pixel. The echoes of a target at the pixel then add in phase, and the echoes of other targets do not. Nothing in the method assumes a straight flight path, a constant speed or a flat Earth, only that the antenna positions are known. It is the radar form of the [back-projection operator](/back-projection-operator/) of tomography, applied along range spheres instead of straight lines, and it is the same sum as [SAFT](/saft/) in ultrasound. Its cost of one operation per pixel and pulse is its weak point; [fast factorized backprojection](/fast-factorized-backprojection/) reduces it.

## In plain words

Each echo tells you how strongly something reflected at each distance from the antenna, but not in which direction. For one point of the picture, you know how far it was from the antenna at each pulse. Look up each echo at that distance, turn each value so that a real reflector at the point would give the same phase every time, and add them all. A real reflector at the point gives a large total. Anything else gives values that point in different directions and mostly cancel. Do this for every point of the picture.

## The problem

The input is $P$ range compressed pulses $d_p[j]$, $j = 0, \ldots, N - 1$, sampled at the two-way delays $t_0 + j/f_s$, the antenna positions $a_p$ at the pulses, the carrier frequency $f_0$ and a list of pixels $q$ on the ground. A point target of amplitude $\alpha$ at $q_0$ gives $d_p(t) = \alpha\, g(t - 2R_p(q_0)/c)\, e^{-i 4\pi f_0 R_p(q_0)/c}$, where $R_p(q) = |a_p - q|$ and $g$ is the compressed pulse, here $\operatorname{sinc}(B t)$ for a bandwidth $B$. The Fourier sign is $e^{-i 2\pi f t}$, as for the DFT; radar books often use $e^{+j\omega t}$ and so the opposite signs. The output is the complex image
$$I(q) = \sum_{p} d_p\big(2R_p(q)/c\big)\, e^{+i 4\pi f_0 R_p(q)/c},$$
the [matched filter](/matched-filter/) for a target at $q$ when the pulse $g$ has already been compressed.

## The algorithm

```pseudo id=main
BACKPROJECT(d, a, pixels, f_0, f_s, t_0, F)    ▷ d[p][j]: range compressed pulses; I starts at 0
L1  for every pulse p: e ← UPSAMPLE(d[p], F)                ▷ zero padding of the DFT; spacing Δr = c / (2 F f_s)
L2      for every pixel q: R ← |a_p - q|
L3          u ← (R - c t_0 / 2) / Δr                        ▷ fractional sample index of R
L4          v ← (1 - w) e[⌊u⌋] + w e[⌊u⌋ + 1] with w = u - ⌊u⌋     ▷ skip q if u is outside e
L5          I[q] ← I[q] + v · e^{+i 4π f_0 R / c}
L6  return I
```

The pseudocode works pulse by pulse, so only one upsampled pulse is in memory at a time. Line L1 interpolates the pulse by the factor $F$ with zero padding of its DFT, which is exact for a periodic band-limited signal. This lets L4 use cheap linear interpolation on the fine grid with a small error. L2 computes the true range, with the antenna height if there is one. L3 turns the range into a sample index of the fine grid. L5 removes the carrier phase $e^{-i 4\pi f_0 R/c}$ of a target at the pixel; its sign is the opposite of the sign of the echo phase. Line L6 returns the image.

## Example

The tests use $f_0 = 300$ MHz ($\lambda = 1$ m), $B = 100$ MHz, $f_s = 120$ MHz, $N = 64$ samples starting at the range 370 m, and $P = 64$ pulses from a straight path at 1.25 m spacing, an aperture of $L = 80$ m. Targets of amplitude 1 at $(0, 400)$ m and 0.5 at $(5, 410)$ m are imaged on a grid of 0.625 m pixels with $F = 8$.

- The largest pixel is at $(0, 400)$ with the value 63.78, against the ideal $P = 64$; the phase is near 0.
- The image is within 1% of 64 of the brute-force sum that reads each pulse with exact sinc interpolation over all its samples.
- Along the track through the target, the first null is at 2.5 m, the value $\lambda R/(2L) = 1 \cdot 400 / 160$ m, and the value there is below 3% of the peak.
- With a curved and noisy flight path, of up to 2.5 m sideways and 0.3 m in height, the image with the true positions gives both targets within 3% of 64 at their pixels. The image of the same data with the positions of the straight path stays below $0.3 \cdot 64$ everywhere on the grid.

All values are measurements on these simulations.

## Correctness

The sum is linear in the data. For one target and exact interpolation, the term of pulse $p$ at the pixel $q$ is $\alpha\, g(\Delta_p)\, e^{i 2\pi f_0 \Delta_p}$ with $\Delta_p = 2(R_p(q) - R_p(q_0))/c$. At $q = q_0$ every $\Delta_p$ is 0, so the pixel gets $P \alpha\, g(0)$. Elsewhere the triangle inequality gives a value of at most this size, with equality only where every range is the same as at $q_0$; for a straight track and pixels on one side of it, two pulses at different places along the track already fix the point. The proofs are in proofs/correctness.md.

## Complexity

Line L1 costs $O(F N \log(F N))$ per pulse with an FFT. Lines L2 to L5 cost $O(1)$ per pixel and pulse, so an $n \times n$ image costs $O(P n^2)$. The total is $O(P (n^2 + F N \log(F N)))$ in the real-RAM model, with $O(n^2)$ space for the image and $O(F N)$ for one upsampled pulse. For $P \approx n$, the usual case, the cost is $O(n^3)$, against $O(n^2 \log n)$ for the frequency-domain algorithms.

## Properties

- Linear in the data.
- Works for any known flight path, with no approximation of the range.
- Exact up to the interpolation of L4 and the stop-and-go approximation.
- Each pixel and each pulse can be processed independently, so the method is easy to run in parallel, and pulses can be added as they arrive.
- The image can be formed on any surface, for example a digital elevation model.

## Variants and improvements

- **Fast factorized backprojection.** [FFBP](/fast-factorized-backprojection/) forms images of short subapertures on coarse polar grids and merges them, for $O(n^2 \log n)$.
- **Convolution backprojection.** For spotlight data that are dechirped, each pulse is a slice of the 2D Fourier transform of the scene, and backprojection after a ramp filter is the [filtered back-projection](/filtered-back-projection/) of tomography (Desai and Jenkins, 1992).
- **Interpolation.** Nearest neighbor on a highly upsampled pulse, linear interpolation as here, or a short sinc kernel without upsampling trade memory against accuracy.
- **Weights.** A window over the pulses lowers the azimuth side lobes, and weights for the antenna pattern and the range loss can be included in the sum.

## When to use it

Use backprojection when the flight path is not straight, when the aperture is wide or the range short, as in airborne systems at low frequency or in ground-based radar, or when the image must be formed on a given surface. It is also the reference to test faster algorithms against. When the path is straight and the scene is large, the [omega-k algorithm](/omega-k-algorithm/) or the [range-Doppler algorithm](/range-doppler-algorithm/) is much faster.

## Pitfalls

- **The sign of the phase correction.** The echo has $e^{-i 4\pi f_0 R/c}$, so the correction is $e^{+i 4\pi f_0 R/c}$. With the opposite sign the terms do not add in phase and the target does not focus.
- **Too coarse an interpolation.** Linear interpolation of the pulse at its own sample rate leaves an amplitude and phase error that varies with the pixel. Upsample first, or use a better kernel.
- **Wrong positions.** The method needs the antenna positions to a small part of the wavelength. A path error of a few wavelengths defocuses the image, as the test with the wrong path shows; the cure is better navigation data or [autofocus](/phase-gradient-autofocus/).
- **Delay reference.** The delay of a sample must be counted from the same instant as the range, including the start time $t_0$ of the record and any fixed delays of the system.
- **Pixel spacing.** The pixels must be smaller than the resolution, about $c/(2B)$ in range and $\lambda R/(2L)$ in azimuth, or targets between pixels lose much of their peak value.

## Implementations

## History

Backprojection comes from computed tomography. Munson, O'Brien and Jenkins (1983) showed that spotlight SAR is a tomography problem, and Desai and Jenkins (1992) formed spotlight SAR images by convolution backprojection with 1D interpolation along each filtered pulse, at the cost $O(N^3)$. Because the time-domain sum uses the true range, it was then used for airborne systems with wide apertures and curved paths, and Ulander, Hellsten and Stenstrom (2003) gave a fast factorized version that makes it practical for large images.

## References
