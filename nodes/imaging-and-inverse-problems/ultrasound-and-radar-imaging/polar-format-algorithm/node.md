---
tag: 8JG48Y
kind: algorithm
slug: polar-format-algorithm
name: Polar format algorithm
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Form spotlight SAR images by placing dechirped pulses on polar lines of 2D Fourier space, interpolating to a rectangular grid and taking an FFT."
solves: [sar-image-formation]
model: real-ram
complexity:
  vars: {M: the number of pulses, N: the number of fast-time samples per pulse, K: the number of taps of the interpolator}
  time: {worst: O(M N (log(M N) + K))}
  space: {extra: O(M N), data: O(M N)}
properties: {deterministic: true, linear_in_data: true, recursive: false, exact: false}
history:
  year: 1980
  people: [Jack L. Walker]
  note: "Walker described polar format processing in 1980 for imaging rotating objects; Munson, O'Brien and Jenkins related spotlight SAR to tomography in 1983."
prereqs: [sar-image-formation, fourier-slice-theorem]
see_also: [direct-fourier-reconstruction, inverse-synthetic-aperture-radar, omega-k-algorithm, sar-backprojection, phase-gradient-autofocus, tomographic-reconstruction-problem, nonuniform-fft, sinc-interpolation]
sources:
  - paper: doi:10.1109/TAES.1980.308875
    title: "Jack L. Walker, Range-Doppler imaging of rotating objects, IEEE Transactions on Aerospace and Electronic Systems 16(1), 1980, 23 to 52"
    locator: "the polar format storage of the data and its resolution limits for a rotating object (general locator)"
  - paper: doi:10.1109/PROC.1983.12698
    title: "David C. Munson Jr., James D. O'Brien and W. Kenneth Jenkins, A tomographic formulation of spotlight-mode synthetic aperture radar, Proceedings of the IEEE 71(8), 1983, 917 to 925"
    locator: "the dechirped spotlight pulse as a slice of the 2D Fourier transform of the scene, and polar format reconstruction (general locator)"
  - book: isbn:9780792396772
    title: "Charles V. Jakowatz Jr., Daniel E. Wahl, Paul H. Eichel, Dennis C. Ghiglia and Paul A. Thompson, Spotlight-Mode Synthetic Aperture Radar: A Signal Processing Approach, Kluwer, 1996"
    locator: "the chapters A Tomographic Foundation for Spotlight-Mode SAR Imaging and Aspects of Spotlight-Mode Image Formation"
  - book: isbn:0890067287
    title: "Walter G. Carrara, Ron S. Goodman and Ronald M. Majewski, Spotlight Synthetic Aperture Radar: Signal Processing Algorithms, Artech House, 1995"
    locator: "the polar format algorithm and its limits from wavefront curvature (general locator)"
---

The polar format algorithm (PFA) forms images from spotlight [synthetic aperture radar](/synthetic-aperture-radar/) data. In spotlight mode the radar keeps one patch of ground in its beam, and each echo is dechirped against the echo of the patch center. Under the plane-wave approximation, a dechirped pulse is then a band of one radial line of the 2D Fourier transform of the scene, the line at the look angle of that pulse; this is the [Fourier slice theorem](/fourier-slice-theorem/) of tomography. All pulses together sample the transform on a polar raster, an annular sector. PFA interpolates these samples onto a rectangular grid, first along range and then along azimuth, and takes one 2D inverse FFT. It is the radar form of [direct Fourier reconstruction](/direct-fourier-reconstruction/) in computed tomography, with band-pass data on a narrow sector of angles.

## In plain words

When the radar watches one patch from slowly changing directions, each pulse, after a simple mixing step, tells you one line of the pattern of stripes that make up the picture of the patch. Each look direction gives the line at its own angle, so the data fill a fan-shaped piece of the stripe pattern. A fast inverse transform needs the pattern on a square grid, not on a fan. So you first estimate the values on the square grid from the nearby fan values, and then run the fast inverse transform. The picture of the patch appears in one step.

## The problem

The input is the dechirped data $d[m][n]$ of $M$ pulses and $N$ fast-time samples. Pulse $m$ looks at the scene center from the angle $\theta_m$, from the radar position $-R_c(\sin\theta_m, \cos\theta_m)$, and sample $n$ has the radial spatial frequency $u_n = 4\pi f_n / c$, where $f_n$ runs over the band $f_0 \pm B/2$. A point $(x, y)$ of amplitude $a$ contributes $a\, e^{-i u_n \Delta R_m}$ with $\Delta R_m = |a_m - (x, y)| - R_c$, its range relative to the center. The Fourier sign is $e^{-i 2\pi f t}$, as for the DFT; radar books often use $e^{+j\omega t}$ and so the opposite signs. Under the plane-wave approximation $\Delta R_m = x \sin\theta_m + y \cos\theta_m$, so $d[m][n] = \hat\sigma(u_n \sin\theta_m, u_n \cos\theta_m)$ with $\hat\sigma(k_x, k_y) = \sum a\, e^{-i (k_x x + k_y y)}$. The output is the complex image $\sigma$ on a pixel grid around the center.

## The algorithm

The Cartesian grid has $N$ rows $k_y$ evenly spaced from $u_{\min}$ to $u_{\max} \cos(\Delta\theta/2)$ and $M$ columns $k_x$ evenly spaced across $\pm u_{\min} \tan(\Delta\theta/2)$, the largest rectangle inside the sector of total angle $\Delta\theta$.

```pseudo id=main
PFA(d, u_n, θ_m)    ▷ d[m][n]: dechirped pulse m, sample n; returns the image
L1  for every pulse m and grid row k_y: R[m][k_y] ← d[m][·] read at u = k_y / cos θ_m     ▷ range interpolation
L2  for every grid row k_y and column k_x: G[k_y][k_x] ← R[·][k_y] read at θ = atan2(k_x, k_y)   ▷ azimuth interpolation
L3  I ← fftshift(2D IDFT of G)
L4  image[i][j] ← N M · I[i][j] · e^{i (k_{y,0} y_i + k_{x,0} x_j)}      ▷ scale and the phase of the grid origin
```

Line L1 interpolates each pulse along its radial line, so that its samples land on the rows of constant $k_y$: the point of the line at radius $u$ has $k_y = u \cos\theta_m$. After L1 the samples lie on a raster shaped like a keystone, with rows of constant $k_y$ and, in each row, points at $k_x = k_y \tan\theta_m$ that are not evenly spaced. Line L2 interpolates along each row to even $k_x$. Both steps use an 8-tap Hann-weighted [sinc interpolation](/sinc-interpolation/), which assumes the scene is small enough that its transform is smooth on the scale of the sample spacing. Line L3 is a 2D inverse FFT. Line L4 undoes the $1/(NM)$ of the inverse DFT and the phase from the grid not starting at $k = 0$, so that a point target at a pixel center gives $N M a$ at that pixel. The pixel spacing is $2\pi/(N \Delta k_y)$ in $y$ and $2\pi/(M \Delta k_x)$ in $x$.

## Example

The tests use $f_0 = 10$ GHz ($\lambda = 3$ cm), $B = 1$ GHz, $N = 32$ samples, $M = 32$ pulses over a total angle $\Delta\theta = 0.1$ rad, and $R_c = 1000$ m. The range resolution $c/(2B)$ is 0.15 m and the cross-range resolution $\lambda / (2\Delta\theta)$ is also 0.15 m. The inscribed rectangle gives pixels of 0.158 m in $x$ and 0.147 m in $y$. Three targets at pixel centers, with plane-wave data, give:

| target $(x, y)$ in m | amplitude | $\lvert$image / 1024 $-$ amplitude$\rvert$ |
|---|---|---|
| (0, 0) | 1 | 0.0063 |
| (0.631, -0.883) | 0.5 | 0.0018 |
| (-1.104, 1.178) | $0.8i$ | 0.0088 |

At these pixels the image agrees within 1% of 1024 with the brute-force polar sum $\sum_{m,n} d[m][n] e^{+i u_n (x \sin\theta_m + y \cos\theta_m)}$. Away from the targets both are below 7% of 1024; they differ there because the sum uses the whole sector and PFA the inscribed rectangle, so their side lobes differ.

With exact spherical ranges instead of plane waves, the largest pixel of a target at $(1.262, 1.178)$ m is 1.009 of 1024 at $R_c = 1000$ m, 0.990 at $R_c = 100$ m, and 0.816 at $R_c = 30$ m, while a target at $(0, 1.178)$ m keeps 1.006 at every range. At $R_c = 30$ m the brute-force sum of the same data peaks at 0.998 at a point 0.05 m in $x$ and 0.03 m in $y$ from the pixel. So at this range the loss is mostly a shift of a third of a pixel, a geometric distortion, not a blur. All values in this section are measurements on these simulations.

## Correctness

The algorithm is linear. Under the plane-wave approximation, the data are exact samples of $\hat\sigma$ on the polar raster, by the definition of $\hat\sigma$ and the [Fourier slice theorem](/fourier-slice-theorem/). If the two interpolations are exact, $G$ holds $\hat\sigma$ on the Cartesian grid, and the inverse DFT of L3 with the phase of L4 gives the scene convolved with the 2D Dirichlet kernel of the rectangle; a target at a pixel center gives exactly $N M a$ there. Without the plane-wave approximation, $\Delta R_m = x \sin\theta_m + y \cos\theta_m + (x \cos\theta_m - y \sin\theta_m)^2/(2 R_c)$ plus smaller terms, and the second term shifts and blurs targets far from the center. The proofs are in proofs/correctness.md.

## Complexity

Line L1 does $N$ interpolations of $K$ taps per pulse, $O(M N K)$. Line L2 does $M$ per row, $O(M N K)$. Line L3 is a 2D FFT, $O(M N \log(M N))$, and L4 is $O(M N)$. The total is $O(M N (\log(M N) + K))$ in the real-RAM model, with $O(M N)$ extra space for the intermediate grid.

## Properties

- Linear in the data.
- Exact under the plane-wave approximation, up to the interpolation.
- The scene size is limited: the error of the plane-wave approximation grows with the square of the distance from the center divided by $R_c$, so large scenes at short range are split into patches.
- The image is on a grid in the plane of the Fourier slices, the slant plane; a projection to the ground is a separate step.

## Variants and improvements

- **Order of interpolation.** Range first and then azimuth, as here, is the usual separable order; azimuth-first versions and the 2D [nonuniform FFT](/nonuniform-fft/) avoid separate passes.
- **Chirp-Z in azimuth.** The azimuth interpolation of L2 can be replaced by a resampling of each row with a chirp-Z transform, which avoids interpolation error along that axis.
- **Wavefront curvature correction.** A space-variant post-filter, or a subdivision of the scene into small patches each with its own center, removes most of the distortion and blur of large scenes.
- **ISAR.** The same algorithm forms images of turning targets in [inverse SAR](/inverse-synthetic-aperture-radar/), where the angle comes from the motion of the target.
- **Autofocus.** [Phase gradient autofocus](/phase-gradient-autofocus/) was developed for spotlight images formed this way.

## When to use it

Use PFA for spotlight data that are dechirped in hardware, for scenes that are small compared to the range, and when the look angle changes by a small amount. It is fast and its errors are well understood. For large scenes at short range, wide angles or curved flight paths, use [backprojection](/sar-backprojection/), which has no plane-wave approximation, or the [omega-k algorithm](/omega-k-algorithm/) for a straight track.

## Pitfalls

- **Interpolating to the wrong radius.** In L1 the range sample for row $k_y$ is at $u = k_y / \cos\theta_m$, not at $u = k_y$; the second leaves a range error that grows with $|\theta_m|$.
- **A grid outside the sector.** If the Cartesian grid extends past the polar data, L1 or L2 reads outside the samples and the image gets edge artifacts. Use the inscribed rectangle, or set the outside values to zero on purpose.
- **Forgetting the grid origin.** The grid starts at $k_y = u_{\min}$, not at 0. Without the phase of L4 the image has a phase that varies with position, which spoils interferometry and autofocus.
- **Scenes too large for the range.** The plane-wave error grows as the square of the distance from the center; check it against the depth of focus of the system before trusting the corners.
- **Sign convention.** With the data $e^{-i u \Delta R}$, the image needs the inverse DFT, which has $e^{+i}$; using the forward DFT flips the image.

## Implementations

## History

Walker (1980) described range-Doppler imaging of rotating objects and the storage of the data in polar format, which allows a resolution beyond the limit of a rectangular format. Munson, O'Brien and Jenkins (1983) showed that spotlight SAR is a tomography problem, in which each dechirped pulse is a slice of the 2D Fourier transform of the scene, and so placed PFA beside direct Fourier reconstruction. Jakowatz and colleagues (1996) and Carrara, Goodman and Majewski (1995) gave full accounts of the algorithm, its interpolations and its limits from wavefront curvature.

## References
