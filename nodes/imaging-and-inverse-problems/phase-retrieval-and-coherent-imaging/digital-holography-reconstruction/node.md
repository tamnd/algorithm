---
tag: JPPVSQ
kind: algorithm
slug: digital-holography-reconstruction
name: Digital holography reconstruction
aliases:
- numerical hologram reconstruction
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: Recover the complex object wave from a recorded hologram by filtering one sideband in Fourier space and numerically propagating it to focus.
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {n: "the side of an n x n hologram, a power of two, with an FFT"}
  time: {worst: O(n^2 log n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, online: false, in_place: false, exact: true}
history:
  year: 1994
  people: [Ulf Schnars, Werner Juptner]
  note: Schnars and Juptner recorded a hologram directly on a CCD and reconstructed the object wave numerically. The off-axis geometry goes back to Leith and Upatnieks (1962), and the spatial filtering of one sideband to Takeda, Ina and Kobayashi (1982) and Cuche, Marquet and Depeursinge (2000).
prereqs: [angular-spectrum-method, discrete-fourier-transform, convolution-theorem]
see_also: [twin-image-problem, phase-retrieval, transport-of-intensity-equation, phase-unwrapping, analytic-signal, fast-fourier-transform, aliasing, coherent-diffraction-imaging]
sources:
  - paper: doi:10.1364/AO.33.000179
    title: Ulf Schnars and Werner Juptner, Direct recording of holograms by a CCD target and numerical reconstruction, Applied Optics 33(2), 1994, 179 to 181
    locator: the recording on a CCD and the numerical reconstruction of the object wave (general locator)
  - paper: doi:10.1364/AO.39.004070
    title: Etienne Cuche, Pierre Marquet and Christian Depeursinge, Spatial filtering for zero-order and twin-image elimination in digital off-axis holography, Applied Optics 39(23), 2000, 4070
    locator: the Fourier filtering of one sideband of an off-axis hologram (general locator)
  - paper: doi:10.1364/JOSA.72.000156
    title: Mitsuo Takeda, Hideki Ina and Seiji Kobayashi, Fourier-transform method of fringe-pattern analysis for computer-based topography and interferometry, Journal of the Optical Society of America 72(1), 1982, 156
    locator: the selection of one spectral sideband of a carrier fringe pattern and its shift to the origin (general locator)
  - paper: doi:10.1364/JOSA.52.001123
    title: Emmett N. Leith and Juris Upatnieks, Reconstructed wavefronts and communication theory, Journal of the Optical Society of America 52(10), 1962, 1123 to 1130
    locator: the off-axis reference that separates the twin images (general locator)
  - paper: doi:10.1038/161777a0
    title: D. Gabor, A new microscopic principle, Nature 161(4098), 1948, 777 to 778
    locator: in-line holography and the twin image (general locator)
  - paper: doi:10.1364/OL.22.001268
    title: Ichirou Yamaguchi and Tong Zhang, Phase-shifting digital holography, Optics Letters 22(16), 1997, 1268
    locator: the recovery of the complex wave from several holograms with shifted reference phase (general locator)
  - paper: doi:10.1103/PhysRevLett.98.233901
    title: Tatiana Latychevskaia and Hans-Werner Fink, Solution to the twin image problem in holography, Physical Review Letters 98(23), 2007, 233901
    locator: iterative reconstruction of in-line holograms that removes the twin image (general locator)
  - book: isbn:9780974707723
    title: Joseph W. Goodman, Introduction to Fourier Optics, third edition, Roberts and Company, 2005
    locator: the chapter on holography (general locator)
---

Digital holography reconstruction computes the complex wave of an object, both its amplitude and its phase, from one intensity image, the hologram, recorded on a camera. The hologram is the interference of the object wave with a known reference wave. In the off-axis geometry the reference arrives at an angle, so the term that carries the object wave sits at its own place in the Fourier transform of the hologram. The algorithm cuts out that term, moves it to the center, and refocuses it with the [angular spectrum method](/angular-spectrum-method/). It solves the [phase retrieval](/phase-retrieval/) problem by experiment design: the reference makes the phase visible in the intensity.

## In plain words

A camera records only brightness. To see the phase of a light wave, the setup adds a second, clean wave that comes in at a small angle. Where the two waves add up the camera sees bright lines, and where they cancel it sees dark lines. The exact position of the lines shifts with the phase of the object wave, so the phase is now written in the brightness.

The computer takes the frequency picture of the recorded image. Because of the angle, the useful part sits away from the center, apart from two unwanted parts. The method cuts the useful part out, moves it back to the center, and transforms it back. The result is the wave at the camera. A second step moves the wave back to the object plane to bring it into focus, as a lens would.

## The problem

The object wave on the sensor is a complex field $O$ on an $n_1 \times n_2$ grid with spacing $d$. The reference is the tilted plane wave $R = r\, e^{2\pi i (c_1 i/n_1 + c_2 j/n_2)}$ with a known amplitude $r > 0$ and an integer carrier $c$, in DFT index units. The camera records the hologram

$$h = |R + O|^2 = r^2 + |O|^2 + \overline{R}\, O + R\, \overline{O}.$$

The task is to find $O$, and then the wave $O_0$ in the object plane at distance $z$ before the sensor, with $O = P_z O_0$ for the propagation $P_z$ of the angular spectrum method. Only the third term carries $O$ linearly. The fourth carries $\overline{O}$, which gives the [twin image](/twin-image-problem/). The [DFT](/discrete-fourier-transform/) is unnormalized, and a DFT index $k$ stands for its signed value $\bar k$, in $[-n/2, n/2)$.

## The algorithm

$B$ is the half-width of the square passband in DFT index units, and $H_{-z}$ is the transfer function of free space for the distance $-z$, zero for evanescent waves.

```pseudo id=main
DH-RECONSTRUCT(h, c, B, r, d, λ, z)
L1  Ĥ <- DFT2(h)
L2  for each index k = (k1, k2), with S[k] <- 0 at the start do
L3      if |k̄1| <= B and |k̄2| <= B then
L4          S[k] <- Ĥ[k - c] / r          ▷ cut the sideband at -c and move it to 0
L5          S[k] <- S[k] · H_-z(k)        ▷ back-propagate to the object plane
L6  return IDFT2(S)
```

Line L4 does the demodulation and the filtering in one step: the window around $-c$ is read and written to the window around $0$. Dividing by $r$ removes the reference amplitude. With $z = 0$ the output is the wave on the sensor. Lines L2 to L5 cost $O(n^2)$, so the algorithm needs only one forward and one inverse FFT.

**The carrier.** If the tilt of the reference is not known, take the peak of $|\hat h|$ outside a small central square: for an object with a strong unscattered wave, the sidebands peak at $\pm c$. The hologram is real, so $|\hat h(k)| = |\hat h(-k)|$, and the sign of $c$ cannot be found from the data. The wrong sign reconstructs the twin wave, which focuses at $-z$ instead of $z$.

## Example

Take $n_1 = 8$ rows and $n_2 = 32$ columns, $d = 1\ \mu$m and $\lambda = 0.5\ \mu$m, so every grid frequency propagates. The object wave on the sensor is a random field whose DFT is nonzero only for $|\bar k_1|, |\bar k_2| \le B = 2$. The reference has $r = 1$ and the carrier $c = (0, c_2)$, so along the columns the four terms of the hologram spectrum sit at:

- $r^2$: index $0$;
- $|O|^2$: $|\bar k_2| \le 2B = 4$;
- the sideband $\overline{R} O$: $-c_2 - 2 \le \bar k_2 \le -c_2 + 2$;
- the twin term $R\overline{O}$: $c_2 - 2 \le \bar k_2 \le c_2 + 2$.

The table gives the relative error $\|O_{\text{rec}} - O\| / \|O\|$ of the wave reconstructed on the sensor ($z = 0$), as measured by the test file.

| carrier $c_2$ | condition | relative error |
|---|---|---|
| 5 | $c_2 < 3B$: the sideband overlaps the autocorrelation term | $1.9 \times 10^{-1}$ |
| 6 | $c_2 = 3B$: they share one column | $5.6 \times 10^{-2}$ |
| 7 | separated | $1.2 \times 10^{-15}$ |
| 9 | separated | $1.3 \times 10^{-15}$ |
| 13 | separated, $c_2 + B = 15 < 16$ | $2.1 \times 10^{-15}$ |
| 14 | $c_2 + B = 16 = n_2/2$: sideband meets the twin | $4.7 \times 10^{-1}$ |

Inside the window $7 \le c_2 \le 13$ the result is exact to rounding, as the theorem says. One step outside it on either side, the error is large.

## Correctness

The [proof](proofs/correctness.md) works on the periodic grid, with the object wave band-limited to the square $|\bar k_1|, |\bar k_2| \le B$. It shows three things.

- **Where the four terms sit (theorem).** The DFT of $r^2$ is at $0$, that of $|O|^2$ in the square of half-width $2B$, that of $\overline{R}O$ in the square of half-width $B$ around $-c$, and that of $R\overline{O}$ around $+c$. The second statement holds because the DFT of a product is a convolution of the DFTs.
- **Exact recovery (theorem).** If for one axis $a$ the carrier satisfies $3B < |c_a|$ and $|c_a| + B < n_a/2$, the window around $-c$ meets no other term. Then lines L1 to L4 give the DFT of $O$ exactly, and the output is $P_{-z} O$, which is $O_0$ when the band of $O_0$ propagates.
- **Noise (theorem).** Every step is linear and the filter discards everything outside the window, so additive noise $e$ in the hologram changes the output by at most $\|e\|/r$.

The proof also gives the in-line case: with $c = 0$, back propagation returns $O_0$ plus the twin, the conjugate wave focused at $-z$, plus the $|O|^2$ term. That is the [twin image problem](/twin-image-problem/), and the off-axis carrier is one way to solve it.

## Complexity

In the [real RAM](/real-ram/) model with the [fast Fourier transform](/fast-fourier-transform/), lines L1 and L6 cost $O(n^2 \log n)$ for an $n \times n$ hologram with $n$ a power of two. Lines L2 to L5 cost $O(n^2)$, with one complex exponential per entry for the transfer function, which can be stored for repeated use. The method keeps two arrays of $n^2$ complex numbers. A refocusing series at many distances costs one FFT for the hologram and then $O(n^2 \log n)$ per distance.

## Properties

- **One shot.** One hologram gives the complex wave. This allows the imaging of moving or changing objects at the frame rate of the camera.
- **Linear in the hologram.** The output is a linear map of $h$, and noise passes with a gain of at most $1/r$.
- **Resolution versus carrier.** The passband must fit between the central terms and the Nyquist limit. Along the carrier axis, $3B < |c_a|$ and $|c_a| + B < n_a/2$ give $B < n_a/8$. So off-axis holography uses at most about a quarter of the frequency range of the camera along that axis for the object.
- **Numerical refocus.** The distance $z$ is a parameter of the computation, so one recording can be focused at any depth afterward.
- **Quantitative phase.** The output phase is the optical path difference modulo $2\pi$. Large phase ranges need [phase unwrapping](/phase-unwrapping/).

## Variants and improvements

- **Phase-shifting holography (Yamaguchi and Zhang 1997).** Record several in-line holograms with the reference phase shifted by known steps, and solve for the complex wave pixel by pixel. It uses the full band of the camera, at the cost of several exposures of a static object.
- **Fresnel transform reconstruction.** Propagate with a single-FFT Fresnel transform instead of the angular spectrum method. The output pixel size is then $\lambda z/(n d)$, which suits long distances.
- **Removal of the zero order.** Subtract the mean of the hologram, or record the reference and object intensities separately and subtract them, which removes $r^2$ and $|O|^2$. Then only the twin must be separated, and the condition on the carrier becomes $B < |c_a|$.
- **Phase compensation.** A non-integer carrier, a spherical reference or the optics of a microscope add a phase to the result. Methods fit and remove it, for example by a reference hologram with no object, or by fitting a polynomial to an empty region.
- **In-line reconstruction with phase retrieval.** For in-line holograms, iterative [phase retrieval](/phase-retrieval/) with a support or a positivity constraint can remove the twin, as in the work of Latychevskaia and Fink.

## When to use it

Use off-axis reconstruction for quantitative phase imaging of living cells, for metrology of surfaces and for the measurement of deformation, when one exposure must give the full wave. Use phase-shifting when the object is static and the full resolution of the camera is needed. For a coherent source with no stable reference, use the [transport of intensity equation](/transport-of-intensity-equation/) or iterative phase retrieval instead.

## Pitfalls

- **The carrier is too small or too large.** The sideband then overlaps the $|O|^2$ term or the twin, as in the example. Plan the tilt of the reference so that the sideband sits between them. A real optical carrier is $\sin\theta/\lambda$ for the tilt $\theta$; on the camera it must stay below $1/(2d)$ minus the object band.
- **A non-integer carrier.** If the tilt does not match a grid frequency, the moved spectrum is off by a fraction of a pixel, and the result carries a residual linear phase. Fit and remove it.
- **A too wide window.** A larger window passes more resolution but also more of the other terms and more noise. A smooth window, for example a raised cosine edge, reduces ringing at the cost of a little resolution.
- **Wrap-around in refocusing.** Long refocusing distances spread the light beyond the window of the camera. Pad before the propagation, as in the angular spectrum method.
- **The sign of the carrier.** The data cannot tell $c$ from $-c$. If the focus is found at the wrong side of the sensor, the twin was selected.
- **Saturation and nonlinearity of the camera.** The analysis assumes a linear camera. Clipped fringes add harmonics of the carrier, at $\pm 2c$ and higher, which can fall into the window.

## Implementations

## History

Gabor (1948) invented holography in the in-line form, where the twin image lies on top of the reconstruction. Leith and Upatnieks (1962) added the tilted reference, which separates the terms in angle. Takeda, Ina and Kobayashi (1982) gave the Fourier transform method for carrier fringe patterns, which isolates one sideband numerically. Schnars and Juptner (1994) recorded holograms on a CCD and reconstructed them by computer. Yamaguchi and Zhang (1997) introduced phase-shifting digital holography, and Cuche, Marquet and Depeursinge (2000) described the spatial filtering of the sideband for digital off-axis holography.

## References
