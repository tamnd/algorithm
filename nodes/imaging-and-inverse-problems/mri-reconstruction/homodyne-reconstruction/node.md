---
tag: 4ZY7XX
kind: algorithm
slug: homodyne-reconstruction
name: Homodyne reconstruction
aliases:
- homodyne detection for partial Fourier
area: imaging-and-inverse-problems/mri-reconstruction
level: core
summary: "Reconstructs an MR image from partial k-space: double the unpaired high frequencies, remove a low resolution phase estimate and keep the real part. Exact for a real image with a constant phase."
solves: [partial-fourier-reconstruction]
model: real-ram
complexity:
  vars: {n: "the side of an n x n image (the number of samples along the partial axis), with n a power of two and an FFT"}
  time: {worst: O(n^2 log n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1991
  people: [Douglas C. Noll, Dwight G. Nishimura, Albert Macovski]
  note: Noll, Nishimura and Macovski named the method after homodyne detection and gave the weighting that sums to 2 across the center, with the phase taken from the symmetric low frequency band.
prereqs: [partial-fourier-reconstruction, discrete-fourier-transform]
see_also: [pocs-partial-fourier, k-space, analytic-signal, hilbert-transform, fast-fourier-transform, window-functions, phase-unwrapping, mri-signal-equation]
sources:
  - paper: doi:10.1109/42.79473
    title: Douglas C. Noll, Dwight G. Nishimura and Albert Macovski, Homodyne detection in magnetic resonance imaging, IEEE Transactions on Medical Imaging 10(2), 1991, 154 to 163
    locator: the homodyne weighting of the asymmetric data, the phase estimate from the symmetric low frequency band, and the real part after phase removal (general locator; section numbers not confirmed)
  - book: isbn:9780120928613
    title: Matt A. Bernstein, Kevin F. King and Xiaohong Joe Zhou, Handbook of MRI Pulse Sequences, Elsevier Academic Press, 2004
    locator: Section 13.4, Partial Fourier Reconstruction
  - paper: "Paul Margosian, F. Schmitt and D. E. Purdy, Faster MR imaging: imaging with half the data, Health Care Instrumentation 1, 1986, pages 195 to 197"
    locator: the earlier half Fourier method with a low resolution phase correction (general locator)
  - paper: doi:10.1148/radiology.161.2.3763926
    title: David A. Feinberg, John D. Hale, John C. Watts, Leon Kaufman and Alexander Mark, Halving MR imaging time by conjugation, demonstration at 3.5 kG, Radiology 161(2), 1986, 527 to 531
    locator: the use of conjugate symmetry to halve the number of phase encoding steps (general locator)
---

Homodyne reconstruction rebuilds an MR image from a little more than half of [k-space](/k-space/), the case of [partial Fourier reconstruction](/partial-fourier-reconstruction/). The scan acquires one side of the phase encoding axis fully and the other side only near the center. The method doubles the high frequencies that have no measured mirror partner, estimates the image phase from the small band that is measured on both sides, removes that phase, and keeps the real part. Noll, Nishimura and Macovski published it in 1991. For a real image times a constant phase factor, and with a nonnegative real part, the result is exact; this page proves it. For a smooth phase it is a good approximation, and for a phase that changes fast it fails.

## In plain words

The picture we want is made of real numbers, but the scanner adds a slowly changing tilt to each value. For a picture of real numbers, each wave in its frequency description has a mirror wave that carries the same information. So half of the frequencies would be enough, if there were no tilt.

Homodyne uses this. The scanner measures all waves on one side, and only a few on the other side near the middle. Each unpaired wave is counted twice, to stand in for its missing mirror. The few paired waves near the middle give a blurry picture, and its tilt is a good guess of the true tilt. The method turns every pixel back by that guessed tilt, and then throws away the part that is not real. What it throws away is exactly the error that the doubling made.

## The problem

The input is one line of [k-space](/k-space/) data of even length $n$ along the phase encoding axis, in DFT order with frequencies $-n/2, \ldots, n/2 - 1$, and the number $k_0$ with $0 \le k_0 < n/2 - 1$. The data are $y_f = (F_u x)(f)$ for the acquired frequencies $f \in S = \{-n/2, \ldots, k_0\}$, where $F_u$ is the unitary DFT ($F_u = n^{-1/2} F$, see [mri-signal-equation](/mri-signal-equation/)). The fraction of acquired samples is $(n/2 + k_0 + 1)/n$, for example 5/8 or 3/4. The output is a real image $\hat\rho$. The model is $x = e^{i\varphi}\rho$ with $\rho$ real and $\varphi$ smooth. For an $n_1 \times n_2$ image with partial phase encoding, an inverse DFT along the fully sampled readout axis first gives one such line per image column.

## The algorithm

$F_u^H$ is the unitary inverse DFT, computed with an FFT.

```pseudo id=main
HOMODYNE(y, n, k0)                    ▷ y known for f = -n/2 .. k0
L1  H(f) <- 0 if f > k0; 1 if |f| <= k0 or f = -n/2; 2 otherwise
L2  T(f) <- 1 - |f|/(k0 + 1) if |f| <= k0; 0 otherwise
L3  z <- F_u^H (H y)                  ▷ the weighted image
L4  l <- F_u^H (T y)                  ▷ the low resolution image
L5  for each pixel j do
L6      if l_j = 0 then rho_j <- 0
L7      else rho_j <- Re(conj(l_j) z_j / |l_j|)
L8  return rho
```

Line L1 is the homodyne filter. The two values of a pair $f, -f$ always sum to 2: the band $|f| \le k_0$ is measured on both sides and gets 1 on each side, an unpaired frequency $f < -k_0$ gets 2 and its missing partner gets 0, and the Nyquist frequency $-n/2$ is its own partner and gets 1. Line L2 is a triangular window on the symmetric band. Lines L3 and L4 read the data only where they are acquired, because $H$ and $T$ are zero elsewhere. Line L7 removes the phase of the low resolution image and keeps the real part.

A common variant replaces the step by a linear ramp on the band, $H(f) = 1 - f/(k_0+1)$ for $|f| \le k_0$. It also sums to 2 across the center and gives less ringing at the edges of the band.

## Example

Take $n = 8$, $k_0 = 1$, the real profile $\rho = [0, 0, 4, 4, 4, 0, 0, 0]$ and the constant phase $\varphi_0 = 0.5$ rad. The scan acquires $f = -4, \ldots, 1$, which is 6 of 8 samples, and misses $f = 2, 3$. Line L1 gives $H = [1, 1, 0, 0, 1, 2, 2, 1]$ in DFT order (frequencies $0, 1, 2, 3, -4, -3, -2, -1$) and line L2 gives $T = [1, \frac{1}{2}, 0, 0, 0, 0, 0, \frac{1}{2}]$. The table shows each pixel with the phase $e^{i\varphi_0}$ taken out of $z$ and $l$, rounded to 3 places.

| pixel $j$ | $\rho_j$ | zero filled $\lvert\cdot\rvert$ | $e^{-i\varphi_0} z_j$ | $e^{-i\varphi_0} l_j$ | output |
|---|---|---|---|---|---|
| 0 | 0 | 0.663 | $-1.293i$ | 0.646 | 0 |
| 1 | 0 | 0.541 | $0.414i$ | 1.500 | 0 |
| 2 | 4 | 3.870 | $4 + 0.707i$ | 2.354 | 4 |
| 3 | 4 | 3.707 | $4$ | 2.707 | 4 |
| 4 | 4 | 3.870 | $4 - 0.707i$ | 2.354 | 4 |
| 5 | 0 | 0.541 | $-0.414i$ | 1.500 | 0 |
| 6 | 0 | 0.663 | $1.293i$ | 0.646 | 0 |
| 7 | 0 | 0.707 | $0$ | 0.293 | 0 |

The zero filled image, the inverse DFT with the missing samples set to 0, is blurred and has a relative error of 0.221 against $x$. The weighted image $z$ has the exact profile in its real part and the whole error in its imaginary part. The low resolution image has the right phase at every pixel, so line L7 returns $\rho$ exactly.

## Correctness

The key fact is the sum rule $H(f) + H(-f) = 2$. Write $H = 1 + A$; then $A$ is odd. For a real profile $\rho$, the DFT $R$ is Hermitian, $R(-f) = \overline{R(f)}$, so $A R$ is anti-Hermitian and its inverse DFT is purely imaginary. Hence $z = e^{i\varphi_0}(\rho + i q)$ with $q$ real. The window $T$ is real and even, so $l = e^{i\varphi_0} r$ with $r$ real, and $r$ is $\rho$ smoothed by the Fejér kernel, which is nonnegative. Line L7 then returns $\operatorname{sign}(r_j)\rho_j$, which is $\rho_j$ when $\rho \ge 0$. The [proof](proofs/correctness.md) gives the details. This is a theorem about the model $x = e^{i\varphi_0}\rho$ with a constant $\varphi_0$; it says nothing about images whose phase varies.

## Complexity

Each line costs two inverse DFTs of length $n$ and $O(n)$ other operations: $O(n \log n)$ with an FFT when $n$ is a power of two, and $O(n^2)$ with a direct DFT. An $n \times n$ image needs one inverse DFT along the readout for each of the $n$ k-space lines and one homodyne step for each of the $n$ columns, $O(n^2 \log n)$ in total in the [real RAM](/real-ram/). The memory holds $z$ and $l$, $O(n)$ numbers per line. The method is not iterative.

## Properties

- **Exact for a constant phase.** For $x = e^{i\varphi_0}\rho$ with $\rho \ge 0$ the output is $\rho$ (theorem). With a signed real $\rho$, the output is $\rho$ multiplied by the sign of its smoothed version.
- **Approximate for a smooth phase.** On a $16 \times 16$ modified Shepp-Logan phantom with the phase $0.4 + 0.5x - 0.6y + 0.2xy$ rad on $[-1, 1]^2$ and 12 of 16 phase encoding lines, the relative error was 0.094 with the step filter and 0.085 with the ramp, against 0.333 for the zero filled magnitude (measurement with the code of this page).
- **Real output.** The method returns a real image. It discards the phase, so it does not suit phase-sensitive uses such as flow or susceptibility imaging.
- **Linear in the data for a fixed phase.** With the phase estimate fixed, lines L3 and L7 are linear in $y$.
- **One pass.** No iteration and no parameter other than $k_0$ and the shape of the filter.

## Variants and improvements

- **Ramp filter.** A linear ramp across the band in line L1 in place of the step. It keeps the sum rule and reduces the ringing that the step causes.
- **Other phase windows.** Any real, even window on the band gives a real $r$ in line L4. A nonnegative kernel, such as the triangle here, keeps the sign of $r$ right for a nonnegative image. A Hann window is another choice.
- **Iterative homodyne and POCS.** [POCS partial Fourier](/pocs-partial-fourier/) reconstruction iterates between the phase constraint and the data. It costs more and handles a varying phase better.
- **Zero filling.** The inverse DFT with the missing samples set to zero. It needs no phase model and gives a blurred image (the zero filled column of the table).
- **Earlier phase-corrected half Fourier methods.** Margosian, Schmitt and Purdy (1986) used a low resolution phase estimate before the conjugate synthesis.

## When to use it

Use homodyne reconstruction for partial Fourier magnitude images in [k-space](/k-space/) when the phase is smooth, for example in spin echo images, in echo planar images with a shortened echo time, and in fast spin echo with fewer phase encoding lines. The phase estimate is only as sharp as the band $|f| \le k_0$, so collect enough lines past the center for the phase of the object. When the phase has sharp features, or when the image phase is needed, use full sampling or a constrained method such as [POCS](/pocs-partial-fourier/). When the image is not real up to a phase, partial Fourier gives no gain.

## Pitfalls

- **Filter that does not sum to 2.** If line L1 gives the unpaired frequencies weight 1 instead of 2, the image keeps only half of their energy and is blurred. If line L1 gives the Nyquist frequency $-n/2$ weight 2, that frequency is counted twice, because it is its own mirror.
- **Window that is not even.** If line L2 uses all acquired samples, or any window that is not symmetric about 0, then $r$ is not real and the phase estimate of line L4 is wrong even for a constant phase.
- **Magnitude in place of the real part.** If line L7 takes $|z_j|$, the result is $\sqrt{\rho_j^2 + q_j^2}$, and the error $q$ stays in the image.
- **Fast phase changes.** Flow, susceptibility edges and motion change the phase faster than the band can show. The phase error then turns into signal loss and wrong signs.
- **Signed images.** For an inversion recovery image with negative real values, the output takes the sign of the smoothed image, so small negative regions next to large positive ones change sign.
- **Too narrow a band.** With a very small $k_0$, the phase estimate is poor, and the error grows.

## Implementations

## History

Feinberg and colleagues showed in 1986 that conjugate symmetry can halve the scan time. In the same year Margosian, Schmitt and Purdy described a half Fourier method that corrects the phase with a low resolution estimate. Noll, Nishimura and Macovski published the homodyne method in 1991, with a filter that sums to 2 across the center and a phase estimate from the symmetric band. The name refers to homodyne detection in radio, where a signal is demodulated with a reference of the same frequency and phase. POCS, published by Haacke, Lindskog and Lin in the same year, is its iterative relative.

## References
