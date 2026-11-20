---
tag: BKPK9D
kind: algorithm
slug: structured-illumination-microscopy
name: Structured illumination microscopy reconstruction
aliases:
- SIM reconstruction
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: Separate the three bands mixed by phase-shifted stripe illumination and recombine them in Fourier space. Linear SIM with the stripe frequency at the cutoff about doubles the resolution.
model: real-ram
complexity:
  vars: {D: the number of stripe directions, N: the number of pixels in a frame}
  time: {worst: Θ(D N log N), average: Θ(D N log N), best: Θ(D N log N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, iterative: false, linear: true, needs_known_pattern: true, optical_method: true}
history:
  year: 2000
  people: [Mats G. L. Gustafsson, Rainer Heintzmann, Christoph Cremer]
  note: Heintzmann and Cremer (1999) and Gustafsson (2000) lit a fluorescent sample with stripes of several phases and directions and recombined the shifted bands. Gustafsson showed a lateral resolution gain of a factor of two.
prereqs: [optical-transfer-function, abbe-diffraction-limit, discrete-fourier-transform, convolution-theorem]
see_also: [super-resolution, sofi, single-molecule-localization, wiener-filter, point-spread-function, aliasing, image-deblurring, multiframe-super-resolution]
sources:
  - paper: doi:10.1046/j.1365-2818.2000.00710.x
    title: "M. G. L. Gustafsson, Surpassing the lateral resolution limit by a factor of two using structured illumination microscopy, Journal of Microscopy 198(2), 2000, 82 to 87"
    locator: "the frequency mixing by the stripes, the separation of the bands from several phases, the shift and recombination of the bands, and the factor of two"
  - paper: doi:10.1117/12.336833
    title: "R. Heintzmann and C. Cremer, Laterally modulated excitation microscopy: improvement of resolution by using a diffraction grating, Proceedings of SPIE 3568, 1999, 185 to 196"
    locator: the excitation with a moved grating pattern and the reconstruction of the higher frequencies
  - paper: doi:10.1073/pnas.0406877102
    title: "M. G. L. Gustafsson, Nonlinear structured-illumination microscopy: wide-field fluorescence imaging with theoretically unlimited resolution, Proceedings of the National Academy of Sciences 102(37), 2005, 13081 to 13086"
    locator: "saturated excitation, the harmonics of the illumination and the larger number of bands"
---

Structured illumination microscopy (SIM) is an optical method for fluorescence microscopy that sees finer detail than the diffraction limit of the lens allows for a plain image. The microscope lights the sample with a fine pattern of stripes instead of a uniform field. The stripes multiply the sample, and this product moves fine object detail, which the lens cannot pass, to coarse moiré fringes, which it can. The reconstruction is the computation that undoes this mixing: from three images taken with three phases of the stripes it separates three copies of the object spectrum, moves each copy back to its true place in Fourier space, and combines them with a weighted (Wiener-type) filter. The result contains object frequencies up to the sum of the cutoff of the lens and the stripe frequency. With stripes at the cutoff, which is the finest pattern the same lens can make, this is about twice the widefield cutoff; this factor of two holds for linear SIM, where the emission is proportional to the light. The gain comes from the physical illumination, not from image processing; without the stripes the computation can recover nothing beyond the [Abbe limit](/abbe-diffraction-limit/).

## In plain words

A lens acts like a sieve for patterns: it passes coarse patterns and blocks fine ones. If you lay a fine striped grid over a fine pattern, you see a coarse moiré pattern, and the moiré is coarse enough to pass the sieve. SIM makes such a moiré on purpose. It lights the sample with a known striped pattern, takes a picture, moves the stripes a little, takes another, and so on. Because the stripes are known, the computer can work out which fine pattern made each moiré, and put the fine detail back where it belongs. Rotating the stripes gives fine detail in every direction.

## The problem

The sample is a fluorescent density $x$ on a periodic grid of $N = n_1 n_2$ pixels. The microscope has a known optical transfer function $H$, real and symmetric, which is $0$ above the cutoff $k_c$. For each stripe direction $d = 1, \ldots, D$ there are three frames, lit with $P_j(r) = 1 + m\cos(2\pi k_{0,d}\cdot r/n + \varphi_j)$, with a known integer stripe frequency $k_{0,d}$, a known depth $m$ and three known phases. Frame $j$ is $h \circledast (P_j x)$ plus noise. The goal is an estimate of $x$ with as many object frequencies as the data contain. By the [convolution theorem](/convolution-theorem/), the DFT of a frame is

$$\hat d_j(k) = H(k)\Bigl[X(k) + \tfrac m2 e^{i\varphi_j} X(k - k_0) + \tfrac m2 e^{-i\varphi_j} X(k + k_0)\Bigr],$$

so each frame mixes three copies of the object spectrum, two of them shifted by $\pm k_0$.

## The algorithm

Let $M$ be the $3 \times 3$ matrix with the rows $(1, \frac m2 e^{i\varphi_j}, \frac m2 e^{-i\varphi_j})$, and $w \ge 0$ the Wiener constant.

```pseudo id=main
SIM-RECONSTRUCT(frames, k0s, phases, m, H, w)
L1  num ← 0, den ← w at every frequency k
L2  for each direction d with stripe frequency k0
L3      (S0, S+, S-) ← M⁻¹ · (DFT of the three frames), at each k
L4      T+(k) ← S+(k + k0), H+(k) ← H(k + k0);  T-(k) ← S-(k - k0), H-(k) ← H(k - k0)
L5      num ← num + H·S0 + H+·T+ + H-·T-;  den ← den + H² + H+² + H-²
L6  X̂(k) ← num(k) / den(k) if den(k) > 0, else 0
L7  return the real part of the inverse DFT of X̂
```

Line L3 separates the bands $S_0 = HX$, $S_+ = H X(\cdot - k_0)$ and $S_- = HX(\cdot + k_0)$. Line L4 moves them back, so that $T_\pm(k) = H(k \pm k_0) X(k)$: each is the object seen through a shifted OTF. Line L5 is the generalized Wiener filter for several measurements of the same $X(k)$ through different transfer functions. The code uses the incoherent OTF of a circular pupil, $H(k) = \frac2\pi(\arccos\rho - \rho\sqrt{1 - \rho^2})$ with $\rho = |k|/k_c$, and periodic indices, so $k_c + |k_0|$ must stay below half the image size.

## Example

Take $32 \times 32$ pixels, the cutoff $k_c = 6$ (in DFT index units), the stripes $k_0 = (0, 5)$, $m = 1$ and the phases $0, 2\pi/3, 4\pi/3$. The OTF along the stripes is $H(0) = 1$, $H(4) = 0.2191$, $H(5) = 0.0796$ and $H(k) = 0$ for $|k| \ge 6$. The sample is the grating $x = 1 + \cos(2\pi\cdot 9c/32)$, with the frequency $9$ beyond the cutoff.

- **Widefield.** The mean of the three frames is $h \circledast x$. Since $H(9) = 0$, it is the constant $1$: the grating is invisible.
- **Raw frame.** Each frame contains a moiré fringe at the frequency $9 - 5 = 4$, inside the passband. Its DFT coefficient, divided by $N$, has the modulus $\frac m2 \cdot \frac12 \cdot H(4) = 0.0548$. Each frame also shows the stripes, at the frequency $5$, with the modulus $\frac m2 H(5) = 0.0398$.
- **Reconstruction.** Without noise and with $w = 0$, the output equals $x$ to $10^{-9}$ (a theorem, Claim 4 of the proof): the grating is fully recovered.
- **Beyond the extended support.** The grating at the frequency $12$ has $12 - 5 = 7 > 6$. No band contains it, and the output is the constant $1$.

A measurement with noise, from the test: an object with every frequency up to radius $8$, the cutoff $k_c = 5$, four stripe directions $(0,4), (4,0), (3,3), (3,-3)$, Gaussian noise with $\sigma = 0.01$ and $w = 10^{-3}$. The relative error of the SIM result is $0.069$; the Wiener deconvolution of the widefield image with the same $w$ has $0.237$. The extended support has $233$ frequencies, against $69$ for the widefield OTF.

## Correctness

The proof is in `proofs/correctness.md`. The main facts, all theorems:

1. The DFT of a frame is the sum of three bands, as in the formula of the problem.
2. The phase matrix $M$ is invertible if and only if $m \ne 0$ and the three phases are distinct modulo $2\pi$; its determinant is a [Vandermonde](/vandermonde-matrix/) determinant. For equally spaced phases its columns are orthogonal, so the noise in the side bands is $2/m$ times the noise in the center band.
3. After the shift, $T_\pm(k) = H(k \pm k_0) X(k)$.
4. Without noise the result has the DFT $\frac{\Sigma(k)}{\Sigma(k) + w}X(k)$, where $\Sigma$ is the sum of the squared OTFs of all bands; with $w = 0$ it is $x$ limited to the extended support $\{\Sigma > 0\}$.
5. For real frames the estimate is real.
6. The extended support lies inside the disk of radius $k_c + \max_d |k_{0,d}|$. If $|k_{0,d}| \le k_c$, which holds when the same lens makes the stripes, this radius is at most $2k_c$.

## Complexity

Each direction needs three 2D DFTs of $N$ pixels, $\Theta(N)$ work to separate, shift and add the bands, and one inverse DFT at the end. With power-of-two sizes and the FFT, this is $\Theta(D N \log N)$ time for $D$ directions. The extra space is $\Theta(N)$ for the bands of one direction and the two sums. The method has no iteration.

## Properties

- **Linear in the data**, for known stripe parameters. The noise in each frequency is easy to predict.
- **Optical gain.** The new frequencies come from the light pattern; the computation only undoes a known mixing.
- **Factor of two only for linear SIM.** With $|k_0| \le k_c$ the extended cutoff is at most $2k_c$. The stripes are made with the excitation light and the image is formed with the emission light, so in practice the gain is a little less than two.
- **Uneven noise.** The side bands carry $m/2$ of the signal, and the OTF is small near the edge of each band, so the high frequencies of the result are noisy. The Wiener constant $w$ trades noise against resolution.
- **Needs several frames.** Three phases for each of $D$ directions, often $D = 3$, so nine frames for a 2D image.

## Variants and improvements

- **More phases.** Use more than three phases and solve the band equations by [least squares](/least-squares-problem/).
- **Parameter estimation.** In practice $k_0$, the phases and $m$ are not known exactly. They are estimated from the data, for example from the [cross-correlation](/cross-correlation/) of the bands in their overlap.
- **Apodization.** Multiply the result by a smooth window that falls to zero at the edge of the extended support, to reduce ringing.
- **3D SIM.** Three-beam interference gives stripes that also vary along the optical axis, and the same band separation works in 3D with five bands.
- **Nonlinear (saturated) SIM.** If the emission is a nonlinear function of the light, the effective pattern has harmonics $2k_0, 3k_0, \ldots$, which bring more bands and, in principle, no fixed limit (Gustafsson 2005). Each harmonic needs more phases.

## When to use it

Use SIM for fluorescent samples when a gain of up to two in resolution is enough, when the sample must stay alive, and when a wide field must be imaged fast. It uses ordinary dyes and moderate light. For a larger gain, localization methods such as [PALM and STORM](/single-molecule-localization/) go to tens of nanometers but need many more frames and special dyes. [SOFI](/sofi/) gives a gain from the blinking of the dyes without special optics. If the sample does not fluoresce, or the stripe pattern cannot be projected, SIM does not apply.

## Pitfalls

- **Wrong pattern parameters.** A small error in $k_0$ or in a phase leaves part of one band in another, and the result shows stripes or a honeycomb pattern. Estimate the parameters from the data.
- **Equal phases.** Two equal phases make $M$ singular. The code raises an error.
- **Too small a Wiener constant.** With $w$ near $0$, frequencies where all OTFs are small get a large gain and the noise grows. Too large a $w$ smooths the result.
- **Periodic wrap.** The code works modulo the image size. If $k_c + |k_0|$ reaches half the size, the shifted bands wrap around.
- **Reading the result as more than double.** Linear SIM cannot pass frequencies beyond $k_c + |k_0|$, no matter how the reconstruction is tuned.

## Implementations

## History

Heintzmann and Cremer (1999) proposed lighting a fluorescent sample through a moved diffraction grating to improve the resolution. Gustafsson (2000) described the band separation and recombination for linear SIM and showed a lateral resolution gain of a factor of two. Gustafsson (2005) used the saturation of the dye to make harmonics of the pattern, which in principle gives no fixed limit. SIM is now a standard method for live-cell fluorescence imaging.

## References
