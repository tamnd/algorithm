---
tag: 5AJF7V
kind: technique
slug: aperture-synthesis
name: Aperture synthesis
aliases:
- synthesis imaging
- radio interferometric imaging
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: core
summary: "Sample the Fourier transform of the sky with pairs of antennas, using the earth rotation to fill the uv plane, and invert the samples to an image."
history:
  year: 1960
  people: [Martin Ryle, Antony Hewish]
  note: "Ryle and Hewish (1960) described how a few small antennas, moved or carried by the rotation of the earth, can measure what one very large telescope would measure."
prereqs: [van-cittert-zernike-theorem, discrete-fourier-transform]
see_also: [dirty-image, hogbom-clean, w-projection, nonuniform-fft, synthetic-aperture-radar, beamforming, speckle-masking, sampling-theorem]
sources:
  - paper: doi:10.1093/mnras/120.3.220
    title: "M. Ryle and A. Hewish, The synthesis of large radio telescopes, Monthly Notices of the Royal Astronomical Society 120(3), 1960"
    locator: "the article from page 220 (the synthesis of a large aperture from pairs of small antennas and the use of the rotation of the earth)"
  - book: isbn:9783319444314
    title: "A. Richard Thompson, James M. Moran and George W. Swenson Jr., Interferometry and Synthesis in Radio Astronomy, third edition, Springer, 2017"
    locator: "Chapter 2, pp. 59 to 88 (the theory of interferometry and synthesis imaging); Chapter 4, pp. 109 to 151 (the coordinates of the baselines and their tracks in the uv plane); Chapter 1, pp. 1 to 58 (the history of radio interferometry)"
  - paper: doi:10.1051/0004-6361/201117104
    title: "U. Rau and T. J. Cornwell, A multi-scale multi-frequency deconvolution algorithm for synthesis imaging in radio interferometry, Astronomy and Astrophysics 532, 2011"
    locator: "article A71 (imaging with many frequency channels at once, with a spectral model of the sky)"
---

Aperture synthesis makes an image of the sky from the signals of an array of separate antennas. Each pair of antennas measures one sample of the Fourier transform of the sky, by the [Van Cittert-Zernike theorem](/van-cittert-zernike-theorem/), and the rotation of the earth moves each sample along a track, so that a few antennas fill much of the Fourier plane in a few hours. This page is the whole technique, from the antennas to the image; the [dirty image](/dirty-image/) is its first product, and [Hogbom CLEAN](/hogbom-clean/), its relatives and [w-projection](/w-projection/) are the steps that turn incomplete samples into a good image.

## In plain words

One radio dish sees only coarse detail, because its resolution depends on its size, and a dish many kilometres wide cannot be built. But two small dishes far apart, with their signals combined, see the same fine detail as a giant dish of that width, in one direction. Each pair of dishes gives one piece of the picture, a stripe pattern of a given width and angle. As the earth turns, every pair sees the sky from a slowly changing angle and gives many more pieces. After some hours, the pieces from all pairs cover much of what a giant dish would have seen. A computer then puts the pieces together into a picture. The picture still has gaps, because the pieces never cover everything, and a second step cleans away the patterns that the gaps make.

## When it applies

**Notation.** The array has $A$ antennas at known positions, and observes at wavelength $\lambda$. Lengths are in wavelengths. A baseline is the vector $b = (u, v, w)$ between two antennas, with $w$ toward the phase center of the field. The sky brightness is $I(l, m)$, in direction cosines from the phase center, and $I' = I / \sqrt{1 - l^2 - m^2}$.

The technique applies when the [Van Cittert-Zernike theorem](/van-cittert-zernike-theorem/) applies: the source is far, its parts radiate independently, and the band is cut into channels narrow enough. Then the correlated signal of a pair is the visibility

$$V(u, v, w) = \iint I'(l, m)\, e^{-2\pi i (u l + v m + w (\sqrt{1 - l^2 - m^2} - 1))}\, dl\, dm,$$

which for a small field, or with $w$ handled separately, is the 2D Fourier transform $\widehat{I'}(u, v)$. The basic facts are these.

- **Pairs.** $A$ antennas give $A(A - 1)/2$ baselines at each moment. Each baseline gives two samples, at $(u, v)$ and at $(-u, -v)$, because $V(-b) = \overline{V(b)}$ for a real sky. An array of 27 antennas has 351 baselines.
- **Earth rotation.** The baselines are fixed on the ground and turn with the earth, so seen from the source they change with the hour angle $H$. For an east-west baseline of length $D$ and a source at declination $\delta$, $u = D \cos H$ and $v = D \sin\delta \sin H$, so the track is an ellipse with semi-axes $D$ and $D \sin\delta$. A source on the celestial equator ($\delta = 0$) gives a line, and an east-west array then has no resolution in $v$.
- **Resolution.** The longest baseline $D_{\max}$ sets the finest detail, about $1/D_{\max}$ radians. The shortest baseline $D_{\min}$ sets the largest structure that the array sees, about $1/D_{\min}$; smoother emission is lost.
- **Field of view.** Each antenna of diameter $d$ sees only a field of about $1/d$ radians, its primary beam. Larger fields need several pointings.
- **What it is not.** The samples do not cover the whole Fourier plane, so the inverse Fourier transform of the samples is not the sky. It is the sky convolved with the [dirty beam](/dirty-image/), and deconvolution must fill the gaps with prior knowledge.

## The template

```pseudo id=main
APERTURE-SYNTHESIS(antennas, phase center, hour angles, channels)
L1  track the phase center with every antenna                 ▷ hole: the array layout
L2  for each time t and each channel do
L3      for each pair (j, k) of antennas do
L4          remove the geometric delay toward the phase center
L5          V_jk(t) ← average of E_j(t) · conj(E_k(t))         ▷ the correlator
L6          (u, v, w)_jk(t) ← (r_j - r_k) seen from the source, in wavelengths
L7  calibrate the gain of each antenna with known sources     ▷ hole: calibration, self-calibration
L8  choose a weight for each sample                           ▷ hole: natural, uniform or robust weighting
L9  form the dirty image and the dirty beam                   ▷ hole: gridding and FFT, w-projection
L10 deconvolve and restore                                    ▷ hole: Hogbom, Cotton-Schwab or multiscale CLEAN, maximum entropy
L11 return the image
```

Lines L2 to L6 are the measurement. Line L6 uses the rotation of the earth: with the baseline $(L_x, L_y, L_z)$ in an equatorial frame, $u$, $v$ and $w$ are fixed functions of the hour angle and the declination, given in Thompson, Moran and Swenson, chapter 4. Lines L7 to L10 are computation, and each has many choices. Line L9 gives the [dirty image](/dirty-image/). Line L10 is where [Hogbom CLEAN](/hogbom-clean/), [Cotton-Schwab CLEAN](/cotton-schwab-clean/), [multiscale CLEAN](/multiscale-clean/) or the [maximum entropy method](/maximum-entropy-method-imaging/) comes in. For wide fields, [w-projection](/w-projection/) replaces the plain Fourier transform in L9 and in the major cycles of L10.

## Classic examples

**Three antennas on an east-west line.** Put antennas at 0, 100 and 300 wavelengths on an east-west line, so the baselines are 100, 200 and 300, with no baseline twice. Observe a source at declination 30 degrees, once each hour from $H = -6$ h to $H = 6$ h. Each baseline traces half an ellipse with semi-axes $D$ and $D/2$, and the samples at $-b$ give the other half.

| hour angle | baseline 100 | baseline 300 | baseline 200 |
|---|---|---|---|
| $-6$ h | $(0, -50)$ | $(0, -150)$ | $(0, -100)$ |
| $-3$ h | $(70.7, -35.4)$ | $(212.1, -106.1)$ | $(141.4, -70.7)$ |
| 0 h | $(100, 0)$ | $(300, 0)$ | $(200, 0)$ |
| 3 h | $(70.7, 35.4)$ | $(212.1, 106.1)$ | $(141.4, 70.7)$ |
| 6 h | $(0, 50)$ | $(0, 150)$ | $(0, 100)$ |

The 13 times give 78 samples with their conjugates. A single snapshot at $H = 0$ has samples only on the $u$ axis, at $u = \pm 100, \pm 200, \pm 300$. Its dirty beam, $\frac13 (\cos 2\pi 100 l + \cos 2\pi 200 l + \cos 2\pi 300 l)$ along $l$, is 1 again at $l = 0.01$, because all baselines are multiples of 100, and it is 1 at every $m$, because nothing is measured in $v$. With the full track, the dirty beam falls to half at $l = 0.00124$ and at $m = 0.00225$, so the beam is longer in $m$ by a factor close to $1/\sin\delta = 2$. The repeat at $l = 0.01$ falls to 0.238, but the gaps between the hourly samples leave sidelobes up to 0.535 within $|l|, |m| \le 0.06$. The [dirty image](/dirty-image/) page uses this beam.

**The synthesis of large telescopes.** Ryle and Hewish (1960) described how a few antennas, together with the rotation of the earth, measure the Fourier plane of a much larger telescope over a period of hours. This is the scheme of the classic east-west arrays.

**Very long baseline interferometry.** Antennas on different continents record their signals with their own clocks, and a correlator combines the recordings later. The baselines are thousands of kilometres, so the resolution is very fine, but the phase of each antenna is poorly known. Products of visibilities around triangles of antennas, whose phases cancel the antenna errors, help here; [speckle masking](/speckle-masking/) uses the same cancellation in optics.

**Optical and infrared interferometry.** The same technique works at short wavelengths with telescopes linked by optical paths. The atmosphere changes the phase of each telescope in milliseconds, so these arrays rely on the modulus of the visibility and on closure phases.

## Variations

- **Multi-frequency synthesis.** The baseline in wavelengths changes with the frequency, so each channel samples other points of the Fourier plane. Using all channels fills the plane further, but the sky changes with the frequency, which needs a spectral model (Rau and Cornwell, 2011).
- **Mosaicking.** Several pointings, each with its own primary beam, cover a field larger than one primary beam, and the imaging combines them.
- **Self-calibration.** The gains of the antennas are solved together with the image: image, predict the visibilities, fit the gains, and repeat. This works because there are more baselines than antennas.
- **Snapshot imaging.** Short observations give sparse coverage but a nearly flat array of baselines, which keeps the w term small (see [w-projection](/w-projection/)).
- **Synthetic aperture radar.** [SAR](/synthetic-aperture-radar/) also builds a large aperture, but from one moving antenna with an active pulse. Its geometry and processing are different.

## Pitfalls

- **Redundant or regular baselines.** Baselines on a regular grid repeat the same samples and make grating lobes in the dirty beam, like the repeat at $l = 0.01$ in the example. A good layout spreads the baselines.
- **Missing short spacings.** No pair of antennas measures near $b = 0$, so the total flux and smooth emission are lost, and the image has a negative bowl around extended sources. Add single-dish data if large scales matter.
- **A source near the equator with an east-west array.** The tracks degenerate to lines, and the image has no resolution in one direction.
- **Wide band without channels.** Averaging over a wide band smears sources far from the phase center in the radial direction. Keep the channels narrow, or image them with a spectral model.
- **Ignoring the w term.** For wide fields and long baselines that are not in one plane, the plain 2D transform distorts sources far from the center (see [w-projection](/w-projection/)).
- **Uncalibrated gains.** Errors of the antenna gains act like a changing sky. CLEAN cannot remove them, and they show as stripes and rings.

## Exercises

1. Show that for an east-west baseline of length $D$, the track satisfies $u^2 + (v / \sin\delta)^2 = D^2$. What does it become for $\delta = 90$ degrees and for $\delta = 0$?
2. An array has antennas at 0, 1, 4 and 6 units on a line. List the baselines and show that each length from 1 to 6 appears once. Why does this help?
3. Compute the snapshot dirty beam of the example at $l = 0.005$ and explain why it is $-1/3$.
4. With 27 antennas, 10 channels and one sample every 10 seconds for 8 hours, how many visibilities does the correlator give, with and without the conjugate samples?
5. A source of total flux 1 is a smooth disk of radius 0.01 radian. Which baselines see it, and what does an array whose shortest baseline is 500 wavelengths measure?

## References
