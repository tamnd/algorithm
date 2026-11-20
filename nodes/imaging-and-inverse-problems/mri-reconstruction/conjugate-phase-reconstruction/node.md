---
tag: ES8X47
kind: algorithm
slug: conjugate-phase-reconstruction
name: Conjugate phase reconstruction
aliases:
- off-resonance correction by conjugate phase
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: "Reconstructs each pixel by weighting every k-space sample with its density weight and the conjugate of its predicted phase, field map term included: the adjoint of the signal model."
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {m: the number of k-space samples, N: the number of pixels}
  time: {worst: O(m N)}
  space: {extra: O(1)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1988
  people: [Akira Maeda, Koichi Sano, Tetsuo Yokoyama]
  note: Maeda, Sano and Yokoyama reconstructed data from time-varying gradients by weighted correlation with the expected signal of each pixel. Noll, Meyer, Pauly, Nishimura and Macovski added the off-resonance phase of a field map in 1991.
prereqs: [mri-signal-equation, density-compensation]
see_also: [nonuniform-fft, cg-sense, conjugate-gradient-method, least-squares-problem, k-space-trajectory, back-projection-operator, forward-operator, phase-unwrapping]
sources:
  - paper: doi:10.1109/42.3926
    title: Akira Maeda, Koichi Sano and Tetsuo Yokoyama, Reconstruction by weighted correlation for MRI with time-varying gradients, IEEE Transactions on Medical Imaging 7(1), 1988, 26 to 31
    locator: the reconstruction of each pixel by correlation of the data with its expected signal (general locator)
  - paper: doi:10.1109/42.108599
    title: Douglas C. Noll, Craig H. Meyer, John M. Pauly, Dwight G. Nishimura and Albert Macovski, A homogeneity correction method for magnetic resonance imaging with time-varying gradients, IEEE Transactions on Medical Imaging 10(4), 1991, 629 to 637
    locator: the conjugate phase correction of off-resonance with a field map for time-varying gradients (general locator)
  - paper: doi:10.1109/TMI.2002.808360
    title: Bradley P. Sutton, Douglas C. Noll and Jeffrey A. Fessler, Fast, iterative image reconstruction for MRI in the presence of field inhomogeneities, IEEE Transactions on Medical Imaging 22(2), 2003, 178 to 188
    locator: the least squares alternative with a field map and its fast approximation (general locator)
  - paper: doi:10.1109/MSP.2010.936726
    title: Jeffrey A. Fessler, Model-based image reconstruction for MRI, IEEE Signal Processing Magazine 27(4), 2010, 81 to 89
    locator: the system model of MRI and model-based reconstruction (general locator)
---

Conjugate phase reconstruction makes an MR image from samples anywhere in [k-space](/k-space/), and it can correct the blur and shift that an uneven magnetic field causes. For each pixel it multiplies every sample by its density weight and by the conjugate of the phase that the [signal equation](/mri-signal-equation/) predicts for that pixel at that sample, and adds the products. With a field map, the predicted phase includes the extra precession $\omega(r)\, t$ of the pixel at the time of the sample. In matrix form the result is $A^H W s$, the adjoint of the signal model applied to the weighted data. Maeda, Sano and Yokoyama described the weighted correlation in 1988, and Noll and colleagues added the field map in 1991. The method is exact on a full Cartesian grid with a constant field; this page proves it. For a field that varies it is an approximation, and a least squares solution of the full model, as in [CG-SENSE](/cg-sense/), gives the exact answer for data without noise when the model matrix has full column rank.

## In plain words

Each measurement of the scanner mixes the signal of every pixel. Each pixel enters the mix with a known turn, which depends on where the pixel is and, if the magnet is not perfectly even, on how fast that pixel spins. To get back one pixel, the method turns every measurement back by the turn that this pixel would have given it, and adds them up. The signal of that pixel then adds up in step, while the signals of the other pixels point in many directions and mostly cancel.

Measurements that sit close together in the frequency plane get less weight, so that crowded places do not count too much.

## The problem

The input is a set of $m$ samples $s_j$ at k-space positions $k_j$ (cycles per unit length) and times $t_j$ after excitation, the density weights $w_j$ (for example from [density compensation](/density-compensation/)), the pixel positions $r_i$, and a field map $\omega_i$ in rad/s at each pixel. The signal model for one coil, without relaxation during the readout, is

$$s_j = \sum_i x_i\, e^{-i \omega_i t_j}\, e^{-2\pi i\, k_j \cdot r_i}, \qquad s = A x,$$

the discrete [signal equation](/mri-signal-equation/) with an off-resonance term. The sign is that of the forward DFT. The output is an image $\hat x$ that approximates $x$.

## The algorithm

```pseudo id=main
CONJUGATE-PHASE(s, k, t, w, r, omega)
L1  for each pixel i do
L2      acc <- 0
L3      for each sample j do
L4          acc <- acc + w_j s_j exp(+i 2 pi k_j . r_i) exp(+i omega_i t_j)
L5      xhat_i <- acc
L6  return xhat
```

Line L4 removes, for pixel $i$, the phase of both encodings: the spatial phase $2\pi k_j \cdot r_i$ and the off-resonance phase $\omega_i t_j$. With $\omega = 0$ the method is the adjoint nonuniform DFT with density weights, which gridding approximates. The double loop is the direct method; gridding with a [nonuniform FFT](/nonuniform-fft/) and a split of the field into a few frequency bins or time segments makes it fast.

## Example

Take a $16 \times 16$ image that is 1 inside the disk $|r| < 0.84 \cdot 8$ pixels and 0 outside. The field is a Gaussian bump with a peak of 40 Hz at the pixel $(2.67, -2)$ and a width of 4 pixels. The scan is a full Cartesian grid read in echo planar order, line by line with alternating direction, with an echo spacing of 0.5 ms and a dwell time of 4 microseconds. The last sample comes 7.56 ms after the first, so the largest off-resonance phase is 1.89 rad. The weights are $w_j = 1/256$. The relative errors were as follows (measurement with the code of this page).

| reconstruction | complex error | magnitude error |
|---|---|---|
| without the field map ($\omega = 0$ in line L4) | 0.54 | 0.0645 |
| conjugate phase with the field map | 0.0373 | 0.0345 |

The uncorrected image has the wrong phase in the region of the bump and is shifted along the phase encoding axis, where the time between samples is long. The conjugate phase image is close to the true disk. The rest of the error comes from the change of the field across the point spread function.

## Correctness

Line L4 adds $\overline{A_{ji}}\, w_j s_j$, so the output is $\hat x = A^H W s$, and with data $s = A x$ the output is $P x$ with $P = A^H W A$. The [proof](proofs/correctness.md) shows:

- The method is exact for every image if and only if $P = I$.
- On a full Cartesian $n \times n$ grid with $w_j = 1/n^2$ and no field, $P = I$: the method is the inverse DFT.
- A constant field cancels in $P$, so the method is exact for a constant field with any sample times.
- The field enters $P$ only through the differences $\omega_i - \omega_{i'}$.

The key invariant is that the output equals $P x$, the true image seen through the point spread function. For a field that varies, $P$ is not the identity. The quality then depends on how much the field changes across the width of the point spread function; this is a heuristic, and the example gives a measurement.

## Complexity

The direct method computes $m$ complex exponentials per pixel, $O(m N)$ operations for $N$ pixels in the [real RAM](/real-ram/), and needs $O(1)$ memory beyond the input and the output. For $N = n^2$ pixels and $m = n^2$ samples this is $O(n^4)$. Gridding with a nonuniform FFT costs $O(m + N \log N)$ without a field. With the field split into $L$ frequency bins or time segments, the cost is $O(L (m + N \log N))$, and the error depends on $L$.

## Properties

- **Linear.** The output is linear in the data.
- **Adjoint of the model.** $\hat x = A^H W s$ (theorem). With $W = I$ it is the adjoint used inside iterative solvers.
- **Exact cases.** Full Cartesian sampling with $w = 1/n^2$ and a constant field (theorem).
- **Approximate for a varying field.** On the example the complex error fell from 0.54 to 0.037 (measurement). The error grows with the field gradient and the readout time.
- **No iteration.** One pass, with no parameter other than the weights and the field map.

## Variants and improvements

- **Without a field map.** With $\omega = 0$ it is the weighted adjoint nonuniform DFT, the basis of gridding for radial and spiral data.
- **Fast approximations.** The phase $e^{i \omega_i t_j}$ is approximated by a sum of a few terms that separate in $i$ and $j$, by time segmentation or by frequency segmentation. Each term needs one gridding step.
- **Least squares.** Solve $\min_x \|A x - s\|^2$, often with a penalty, by the [conjugate gradient method](/conjugate-gradient-method/). Sutton, Noll and Fessler (2003) used a time segmented model with the nonuniform FFT. This removes the approximation of $P \approx I$ at the cost of several applications of $A$ and $A^H$.
- **Field map estimation.** The map $\omega$ comes from the phase difference of two images at different echo times, divided by the echo time difference, often after [phase unwrapping](/phase-unwrapping/).

## When to use it

Use conjugate phase reconstruction for spiral and echo planar images with a known field map when a fast, non-iterative correction is enough, and as the first step or the adjoint inside iterative methods. When the field changes fast, for example near air-tissue boundaries, or when the error must be small, use least squares with the full model. The field map must be accurate; an error of $\delta\omega$ leaves a phase error of $\delta\omega\, t_j$.

## Pitfalls

- **Wrong sign of the phase.** If line L4 uses $e^{-i \omega_i t_j}$, the correction doubles the off-resonance phase instead of removing it. The same holds for the spatial term, where a sign flip mirrors the image. Scanners and books use both sign conventions.
- **Times from the wrong origin.** The times $t_j$ in line L4 must be measured from the same origin as in the field map, usually the echo time or the start of the readout. A shift adds a constant phase per pixel.
- **No density weights.** If line L4 uses $w_j = 1$ for a radial or spiral trajectory, the center of k-space counts too much and the image is blurred.
- **Large field gradients.** Where the field changes fast, the point spread function is not narrow, and the method leaves blur and signal loss.
- **Cost of the direct sum.** The double loop of lines L1 and L3 is $O(m N)$; for a $256 \times 256$ image with as many samples it needs about $4 \times 10^9$ exponentials.

## Implementations

## History

Maeda, Sano and Yokoyama (1988) reconstructed MR data from time-varying gradients by correlating the data with the expected signal of each pixel. Noll, Meyer, Pauly, Nishimura and Macovski (1991) used the field map in the same correlation to correct off-resonance for spiral and other time-varying gradients. Sutton, Noll and Fessler (2003) replaced the correction by an iterative least squares solution with a fast approximation of the model. Fessler (2010) reviews model-based reconstruction for MRI, which uses the same system matrix.

## References
