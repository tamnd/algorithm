---
tag: 07N33J
kind: technique
slug: single-pixel-camera
name: Single-pixel camera
aliases:
- single-pixel imaging
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: Image with one detector by measuring inner products of the scene with many random or Hadamard patterns, then reconstruct by sparse recovery.
prereqs: [compressed-sensing, walsh-hadamard-transform, basis-pursuit]
see_also: [fast-walsh-hadamard-transform, coded-aperture-imaging, candes-romberg-tao-theorem, haar-wavelet, total-variation-denoising, variable-density-sampling, mutual-coherence, image-noise]
sources:
  - paper: doi:10.1109/MSP.2007.914730
    title: Marco F. Duarte, Mark A. Davenport, Dharmpal Takhar, Jason N. Laska, Ting Sun, Kevin F. Kelly and Richard G. Baraniuk, Single-pixel imaging via compressive sampling, IEEE Signal Processing Magazine 25(2), 2008
    locator: pages 83 to 91 (the camera with a digital micromirror device and one photodiode, random binary patterns, and reconstruction by sparse recovery)
  - paper: doi:10.1038/s41566-018-0300-7
    title: Matthew P. Edgar, Graham M. Gibson and Miles J. Padgett, Principles and prospects for single-pixel imaging, Nature Photonics 13(1), 2019
    locator: pages 13 to 20 (review of pattern choices including Hadamard and Fourier patterns, differential measurement, applications at infrared and terahertz wavelengths, and time-resolved imaging)
  - paper: doi:10.1109/TIT.2005.862083
    title: Emmanuel J. Candes, Justin Romberg and Terence Tao, Robust uncertainty principles, exact signal reconstruction from highly incomplete frequency information, IEEE Transactions on Information Theory 52(2), 2006
    locator: pages 489 to 509 (recovery from a random subset of rows of an orthogonal transform, the basis of the compressive mode)
---

A single-pixel camera forms an image with one light detector. A spatial light modulator, usually a digital micromirror device (DMD), shows a sequence of patterns, and the detector records the total light of the scene seen through each pattern, which is the inner product of the scene with the pattern. With as many patterns as pixels, a Hadamard pattern set gives the image by one fast transform. With fewer patterns, the image is found by sparse recovery, as in [compressed sensing](/compressed-sensing/), which mentions this camera as an example; this page gives the measurement scheme, the noise and the pitfalls. It differs from [coded aperture imaging](/coded-aperture-imaging/), which records one shot through a fixed mask on a detector array and decodes by correlation: here there is one detector and many patterns in time.

## In plain words

Imagine you can see a picture only through a stencil, and you can only learn how much light passes in total. One stencil tells you little. But if you try many stencils, each letting through a different set of spots, you can work out the brightness of every spot, just as you can find several unknown weights from the totals of many groups. A good set of stencils makes this quick and exact. If the picture is simple, for example mostly smooth with a few edges, fewer stencils than spots are enough, and a computer finds the simplest picture that agrees with all the totals. The single detector can then be one that would be far too expensive to build as a large array.

## When it applies

- **Detector arrays are expensive or do not exist.** Short-wave infrared, mid-infrared and terahertz light, or detectors with special abilities, such as fast timing for depth, a full spectrum per measurement, or single-photon sensitivity. One good detector replaces an array.
- **The scene is static during the acquisition.** The $M$ patterns are shown one after another. The pattern rate of a DMD is in the range of thousands to tens of thousands per second, so an image of $64 \times 64$ pixels with all 4096 patterns takes from a fraction of a second to a few seconds.
- **The measurements are linear in the light.** The detector reading must be proportional to the light that reaches it, plus noise. Saturation and nonlinear gain break the model.
- **For the compressive mode: the scene is compressible.** In a [wavelet](/haar-wavelet/) basis, or with sparse gradients as measured by [total variation](/total-variation-denoising/), and the patterns are incoherent with that representation.

## The template

Let the scene be $x \in \mathbb{R}^N_{\ge 0}$, an image of $N$ pixels written as a vector, with $N$ a power of 2. Let $H$ be the $N \times N$ Sylvester Hadamard matrix, with entries $\pm1$ and $H^TH = NI$; its rows are the Walsh functions of the [Walsh-Hadamard transform](/walsh-hadamard-transform/). A DMD mirror either sends light to the detector or away from it, so a pattern has entries 0 and 1. The 0/1 version of row $h_i$ is $p_i = (h_i + \mathbf{1})/2$, so the pattern matrix is $P = (H + J)/2$ with $J$ the all-ones matrix. The first row of $H$ is all ones, so $p_1 = \mathbf{1}$ and its reading is the total light $t = \mathbf{1}^Tx$.

```pseudo id=main
SINGLE-PIXEL-IMAGE(scene x, N, M, Ψ, ε)
L1  choose a set I of M rows of H, with row 1 in I     ▷ all rows, low sequency rows, or a random set
L2  for each i in I
L3      show the pattern p_i = (h_i + 1)/2 on the DMD
L4      record y_i = ⟨p_i, x⟩ + e_i                     ▷ one detector reading
L5  t ← y_1                                              ▷ the total light
L6  for each i in I: z_i ← 2y_i - t                      ▷ the ±1 measurement ⟨h_i, x⟩ plus noise
L7  if M = N: return x̂ ← H^T z / N                      ▷ fast Walsh-Hadamard transform, O(N log N)
L8  else: return x̂ ← argmin ‖Ψ^T x‖₁ subject to ‖H_I x - z‖₂ ≤ ε   ▷ or total variation, or another sparse decoder
```

Lines L2 to L4 are the hardware. Line L6 holds because $2\langle p_i, x\rangle - \langle\mathbf{1}, x\rangle = \langle h_i + \mathbf{1}, x\rangle - \langle\mathbf{1}, x\rangle = \langle h_i, x\rangle$. Line L7 is exact without noise, because $H^TH = NI$, and the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) computes it, and the products with $H_I$ and $H_I^T$ inside the decoder of line L8, in $O(N\log N)$ operations.

**Example by hand.** Take a $2 \times 2$ image, $N = 4$, with pixels $x = (5, 1, 2, 0)$. With

$$H = \begin{pmatrix}1 & 1 & 1 & 1\\ 1 & -1 & 1 & -1\\ 1 & 1 & -1 & -1\\ 1 & -1 & -1 & 1\end{pmatrix}, \qquad P = \frac{H + J}{2} = \begin{pmatrix}1 & 1 & 1 & 1\\ 1 & 0 & 1 & 0\\ 1 & 1 & 0 & 0\\ 1 & 0 & 0 & 1\end{pmatrix},$$

the readings are $y = Px = (8, 7, 6, 5)$. The total is $t = 8$, and $z = 2y - 8 = (8, 6, 4, 2)$, which is $Hx$. Then $H^Tz = (20, 4, 8, 0)$, and dividing by $N = 4$ gives back $x = (5, 1, 2, 0)$.

**Compressive mode by hand.** Keep only rows 1, 2 and 3 of $H$, so $M = 3 < N = 4$. The columns of this $3 \times 4$ matrix are $(1, 1, 1)$, $(1, -1, 1)$, $(1, 1, -1)$ and $(1, -1, -1)$, and no two of them are parallel. So a scene with one bright pixel, $x = ce_j$, is determined: $z = c$ times column $j$, and the pattern of signs of $z$ names $j$. For example $x = 7e_3$ gives $y = (7, 7, 0)$, $t = 7$ and $z = (7, 7, -7)$, the third column times 7. But two bright pixels are not always determined: $e_1 + e_4$ and $e_2 + e_3$ both give $z = (2, 0, 0)$.

**Noise and the multiplexing advantage.** Suppose each reading has independent additive detector noise of variance $\sigma^2$, not depending on the light. Scanning one pixel at a time with $N$ readings gives each pixel with variance $\sigma^2$. With differential measurement, showing $p_i$ and its complement $\mathbf{1} - p_i$ and subtracting, $z_i = \langle h_i, x\rangle$ has noise variance $2\sigma^2$ from $2N$ readings, and $\hat x = H^Tz/N$ has noise covariance $H^T(2\sigma^2I)H/N^2 = (2\sigma^2/N)I$. Against scanning with the same $2N$ readings, variance $\sigma^2/2$, this is $N/4$ times smaller. Each pattern collects light from half of the pixels, and this is the source of the gain. When the noise is photon noise, its variance grows with the collected light, and the gain shrinks or disappears; the Hadamard optics of the 1970s studied this trade.

## Classic examples

- **The Rice single-pixel camera.** Duarte and coauthors (2008) built a camera with a DMD and one photodiode, showed random binary patterns, and reconstructed images from fewer readings than pixels by sparse recovery.
- **Computational ghost imaging.** The same measurement, a known pattern of light on the object and a detector without spatial resolution, was studied in quantum optics as ghost imaging. With a programmable modulator the second, imaging detector is not needed, and the method is a single-pixel camera with structured illumination instead of structured detection.
- **Infrared and terahertz imaging.** One cooled infrared detector, or one terahertz detector, behind a modulator replaces a focal plane array.
- **Depth and spectra.** A fast detector with photon timing gives the time of flight for each pattern, hence a depth image. A spectrometer in place of the photodiode gives a spectrum for each pattern, hence a spectral image.

## Variations

- **Pattern sets.** Full Hadamard sets with the exact inverse of line L7; random 0/1 patterns as in the Rice camera; Hadamard rows ordered by sequency (the number of sign changes), so that the first ones give a low-resolution image; Hadamard matrices with randomly permuted columns, which are more incoherent with wavelets and keep the fast transform; and sinusoidal patterns with phase shifts, which measure Fourier coefficients and are shown on a binary DMD by dithering.
- **Differential and complementary detection.** Showing each pattern and its complement removes slow drift of the light source and the background. A second detector placed in the other mirror direction records the complement at the same time, so no light is wasted.
- **Decoders.** Basis pursuit denoising with a wavelet basis, total variation minimization, greedy and thresholding methods, and learned decoders. With $M = N$ no decoder is needed beyond line L7.
- **Adaptive patterns.** Measure coarse wavelet coefficients first and refine only where they are large.

## Pitfalls

- **Hadamard and Haar are coherent.** The Walsh functions and the [Haar wavelets](/haar-wavelet/) share vectors: the constant vector is in both bases, and so is the coarsest Haar wavelet, a Walsh function with one sign change. So the [mutual coherence](/mutual-coherence/) of the two bases is the worst possible, and uniformly random rows of $H$ miss the coarse wavelet content of most images. Sample all low-sequency rows and fewer high ones, as in [variable density sampling](/variable-density-sampling/), or permute the columns at random.
- **Motion.** The $M$ readings are taken in sequence. A scene that moves during the acquisition is not described by one $x$, and the reconstruction blurs or shows artifacts.
- **Forgetting the total.** Without the total $t$ the ±1 measurements of line L6 cannot be formed from 0/1 patterns. Keep the all-ones pattern, or use differential measurements.
- **Detector noise against photon noise.** The multiplexing gain above assumes additive detector noise. With photon noise, a scene that is bright in a few pixels can be worse with Hadamard patterns than with scanning.
- **The resolution is the modulator's.** The number of pixels and the resolution are set by the modulator and the optics, not by the detector. A compressive decoder does not add detail finer than the patterns.
- **The compressive saving needs a sparse scene.** The number of readings for a decoder is of order $s\log(N/s)$ for $s$ significant coefficients, as in the [Candes-Romberg-Tao theorem](/candes-romberg-tao-theorem/) and its successors. A scene with fine texture everywhere needs nearly $N$ patterns.

## Exercises

1. Show that $P = (H + J)/2$ has entries 0 and 1 when $H$ is a Sylvester Hadamard matrix of order $N$, and that every row except the first has exactly $N/2$ ones.
2. For $N = 4$ and $x = (3, 0, 1, 4)$, compute the readings $y = Px$, form $z = 2y - y_1$, and recover $x$ by $H^Tz/4$.
3. With independent noise of variance $\sigma^2$ on each of the $N$ readings, and $z_i = 2y_i - y_1$, show that the error of $\hat x = H^Tz/N$ has variance $\sigma^2$ in the first pixel and $4\sigma^2/N$ in every other pixel. Use the fact that every column of $H$ except the first sums to 0. Compare with the differential scheme.
4. Find two different 2-sparse nonnegative scenes in $\mathbb{R}^4$ with the same readings for the first three rows of $P$, and explain why one more pattern removes the ambiguity.
5. Show that the coarsest Haar wavelet on $N = 2^k$ points, $(1, \dots, 1, -1, \dots, -1)/\sqrt N$, is a normalized row of the Sylvester Hadamard matrix. What is the scaled coherence $\sqrt N\max|\langle h_i/\sqrt N, \psi_j\rangle|$ of the two bases?

## References
