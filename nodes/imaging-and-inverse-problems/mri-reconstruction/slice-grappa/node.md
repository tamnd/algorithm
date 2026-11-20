---
tag: 863VBG
kind: algorithm
slug: slice-grappa
name: Slice-GRAPPA
aliases:
- simultaneous multi-slice GRAPPA
area: imaging-and-inverse-problems/mri-reconstruction
level: research
summary: "Separates slices that were excited at the same time: one GRAPPA-type kernel per slice maps the collapsed k-space of all coils to the k-space of that slice, fitted on single-slice calibration data."
solves: [mri-reconstruction-problem]
model: real-ram
complexity:
  vars: {n: "the side of the n x n k-space", c: "the number of coils", S: "the number of slices", a: "the number of calibration rows", q: "the number of kernel positions per coil"}
  time: {worst: "O(S (a n c^2 q^2 + c^3 q^3 + c^2 q n^2))"}
  space: {extra: "O(c^2 q^2 + a n c q + S c n^2)"}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2012
  people: [Kawin Setsompop, Borjan A. Gagoski, Jonathan R. Polimeni, Thomas Witzel, Van J. Wedeen, Lawrence L. Wald]
  note: Setsompop and colleagues introduced blipped CAIPI for echo planar imaging and the slice-GRAPPA kernel that separates the collapsed slices.
prereqs: [grappa]
see_also: [sense, g-factor, spirit, coil-sensitivity-map, aliasing, k-space, root-sum-of-squares-coil-combination, espirit]
sources:
  - paper: doi:10.1002/mrm.23097
    title: Kawin Setsompop, Borjan A. Gagoski, Jonathan R. Polimeni, Thomas Witzel, Van J. Wedeen and Lawrence L. Wald, Blipped-controlled aliasing in parallel imaging for simultaneous multislice echo planar imaging with reduced g-factor penalty, Magnetic Resonance in Medicine 67(5), 2012, 1210 to 1224
    locator: the blipped CAIPI shift and the slice-GRAPPA kernel fitted on single-slice calibration data (general locator; section numbers not confirmed)
  - paper: doi:10.1002/1522-2586(200102)13:2<313::AID-JMRI1045>3.0.CO;2-W
    title: David J. Larkman, Joseph V. Hajnal, Amy H. Herlihy, Glyn A. Coutts, Ian R. Young and Gosta Ehnholm, Use of multicoil arrays for separation of signal from multiple slices simultaneously excited, Journal of Magnetic Resonance Imaging 13(2), 2001, 313 to 317
    locator: the separation of simultaneously excited slices with coil sensitivities (general locator)
  - paper: doi:10.1002/mrm.20401
    title: Felix A. Breuer, Martin Blaimer, Robin M. Heidemann, Matthias F. Mueller, Mark A. Griswold and Peter M. Jakob, Controlled aliasing in parallel imaging results in higher acceleration (CAIPIRINHA) for multi-slice imaging, Magnetic Resonance in Medicine 53(3), 2005, 684 to 691
    locator: the shift of the slices against each other by phase cycling of the excitation (general locator)
  - paper: doi:10.1002/mrm.24898
    title: Stephen F. Cauley, Jonathan R. Polimeni, Himanshu Bhat, Lawrence L. Wald and Kawin Setsompop, Interslice leakage artifact reduction technique for simultaneous multislice acquisitions, Magnetic Resonance in Medicine 72(1), 2014, 93 to 102
    locator: the leakage between slices in slice-GRAPPA and the split slice-GRAPPA fit that reduces it (general locator)
---

Slice-GRAPPA reconstructs simultaneous multi-slice (SMS) MR data. The scan excites $S$ slices at once, so each coil records the sum of their k-spaces, the collapsed k-space. For each slice, a small kernel maps a patch of the collapsed k-space of all coils to the k-space sample of every coil of that slice. The kernel is fitted by [least squares](/least-squares-problem/) on single-slice calibration data, summed into a synthetic collapsed k-space. With blipped CAIPI, each slice is shifted by a fraction of the field of view, so the slices overlap less in the coil images and the separation is better conditioned. Setsompop and colleagues published the method in 2012. It extends [GRAPPA](/grappa/) from skipped lines to stacked slices.

## In plain words

Several slices are imaged at once, and each coil hears all of them added together. Each coil sits closer to some slices and farther from others, so it hears them with different loudness, in a way that changes smoothly over the image. Slice-GRAPPA learns, from separate short scans of each slice, a recipe that pulls one slice out of the mix. Shifting one slice by half the picture before mixing helps, because then two places with different coil loudness overlap instead of two places with almost the same loudness.

## The problem

The input is the collapsed k-space $y_b = \sum_z \tilde x_{z,b}$ of each coil $b$ on an $n \times n$ grid, the shifts $\Delta_z$ in rows, and calibration k-space of each slice alone on a block of $a$ center rows. $\tilde x_{z,b}$ is the k-space of coil $b$ of slice $z$ after the CAIPI shift, that is, with row $\kappa_1$ multiplied by $e^{-2\pi i \kappa_1 \Delta_z/n}$. The output is $x_{z,b}$ for every slice and coil. The kernel size $k_r \times k_c$, the calibration size and the regularization are choices.

## The algorithm

```pseudo id=main
SLICE-GRAPPA(y, calib, Delta, kernel shape)
L1  y_cal <- sum over z of the shifted calibration k-space of slice z   ▷ synthetic collapsed data
L2  for each slice z do
L3      collect patches u(kappa) of y_cal for kappa in the calibration rows,
            with the targets (shifted calibration of slice z at kappa) for every coil
L4      W_z <- least squares solution of U W = Y (small Tikhonov term)
L5      for each kappa do
L6          u <- patch of y around kappa (all coils, k_r x k_c)
L7          x~_{z,a}(kappa) <- sum_s u_s W_z[s][a] for every coil a
L8      x_{z,a} <- remove the shift Delta_z from x~_{z,a}
L9  return x
```

Line L1 builds collapsed calibration data with the same shifts as the scan, so the kernel learns to undo exactly that mixing. Lines L3 and L4 are the fit of GRAPPA, with all collapsed neighbors as sources and one slice as target. Line L7 is a convolution of the collapsed k-space with the kernel. Line L8 multiplies row $\kappa_1$ by $e^{2\pi i \kappa_1 \Delta_z/n}$. The code handles SMS without in-plane undersampling; with in-plane acceleration, a GRAPPA step fills the missing lines after the separation.

## Example

Two slices, a $32 \times 32$ modified Shepp-Logan phantom in slice 0 and a disk of radius 0.7 with a darker inner disk in slice 1, four coils, no noise. The band maps have only the image frequencies 0 and 1 on each axis; the ring maps are smooth Gaussian profiles, with the ring turned by 20 degrees in slice 0 and by 65 degrees in slice 1. The table gives the relative k-space error of each slice after separation, with a $3 \times 3$ kernel and the regularization $10^{-8}$ times the mean diagonal (measurement with the code of this page).

| maps | CAIPI shift | calibration rows | error slice 0 | error slice 1 |
|---|---|---|---|---|
| band | 0 | 16 | $4.9 \times 10^{-5}$ | $2.1 \times 10^{-5}$ |
| band | $n/2$ | 16 | $1.5 \times 10^{-5}$ | $6.8 \times 10^{-6}$ |
| ring | 0 | 12 | 0.094 | 0.045 |
| ring | 0 | 16 | 0.087 | 0.042 |
| ring | $n/2$ | 12 | 0.051 | 0.025 |
| ring | $n/2$ | 16 | 0.047 | 0.023 |
| ring | $n/2$ | 24 | 0.046 | 0.022 |

For the band maps the separation is exact up to the regularization, as the theorem says. For the ring maps the half field of view shift halves the error, and more calibration rows help little.

## Correctness

The CAIPI shift of an image by a whole number of rows keeps the coil maps band-limited with the same support, only with new phases. So, as for [GRAPPA](/grappa/), every collapsed source and every target is a linear function of the object samples of all slices in a small window. If the target of one slice lies in the span of the collapsed sources, and the calibration data contain enough independent patterns, every exact solution of the fit gives the exact slice at every k-space position. The [proof](proofs/correctness.md) gives the details. This is a theorem about maps with a finite k-space support and integer shifts. For real coils the leakage between slices is a measurement.

## Complexity

In the [real RAM](/real-ram/), with $q = k_r k_c$ and $m = c q$ sources: line L1 costs $O(S c n^2)$. For each slice, the fit of lines L3 and L4 costs $O(a n m^2)$ to form the normal equations and $O(m^3)$ to solve them, and lines L5 to L7 cost $O(c m n^2)$. The total is $O(S(a n c^2 q^2 + c^3 q^3 + c^2 q n^2))$. Image domain application of the kernel with FFTs reduces the last term to $O(c^2 n^2 + c n^2 \log n)$ per slice. The memory holds the normal equations, the calibration patches and the output, $O(c^2 q^2 + a n c q + S c n^2)$.

## Properties

- **Exact for band-limited maps.** Under the span and calibration assumptions, the output is the k-space of each slice (theorem).
- **CAIPI lowers the noise and the leakage.** Shifting the slices against each other makes the coil profiles of overlapping pixels more different. For the ring maps of the example, the shift by $n/2$ halved the error (measurement). Setsompop et al. (2012) report lower g-factors with blipped CAIPI on in vivo data (measurement).
- **No SNR loss from fewer samples.** SMS does not skip k-space samples, so there is no $\sqrt{R}$ loss; the cost is the [g-factor](/g-factor/) of the separation.
- **Slice leakage.** The fit minimizes the error of the target slice on the calibration data. It does not force the contribution of the other slices to zero, so signal from one slice can leak into another (Cauley et al. 2014).
- **Linear.** For a fixed kernel, the output is linear in the data.

## Variants and improvements

- **Split slice-GRAPPA.** Cauley et al. (2014) fit the kernel so that it also cancels the other slices on their own calibration data, which reduces the leakage at a small cost in noise.
- **SENSE for SMS.** With coil maps of each slice, the separation is a [SENSE](/sense/) problem with the slices as the folded pixels (Larkman et al. 2001).
- **CAIPIRINHA.** Breuer et al. (2005) shifted the slices by alternating the phase of the excitation from line to line; blipped CAIPI does the same in echo planar imaging with gradient blips.
- **In-plane acceleration.** SMS is often combined with in-plane undersampling; the slices are separated first, then [GRAPPA](/grappa/) fills the missing lines.
- **Iterative methods.** [SPIRiT](/spirit/) and other consistency methods can include the slice dimension.

## When to use it

Use slice-GRAPPA for simultaneous multi-slice echo planar imaging, as in functional MRI and diffusion MRI, where many slices must be acquired in a short time and the k-space of each slice is already sampled as fast as the hardware allows. Use a CAIPI shift whenever the sequence allows it. Collect a single-slice calibration scan with the same contrast and geometry. For quantitative studies of activation in neighboring slices, check the leakage, or use split slice-GRAPPA.

## Pitfalls

- **Calibration without the shift.** If line L1 sums the calibration slices without the CAIPI shifts of the scan, the kernel learns a different mixing and fails.
- **Forgetting to undo the shift.** Without line L8, each slice is shifted by $\Delta_z$ rows.
- **Slices with the same coil profiles.** If the slices are close together along the coil axis, the coils hear them alike, and the separation is ill-conditioned even with CAIPI.
- **Calibration from a different scan.** Motion or different contrast between the calibration scan and the SMS scan makes the kernel wrong.
- **Leakage taken for activation.** In fMRI, a signal from one slice that leaks into another can look like activation there.
- **Non-integer shifts.** A shift that is not a whole number of rows on the grid does not move the image periodically, and the model of the proof fails.

## Implementations

## History

Larkman and colleagues showed in 2001 that coil arrays can separate slices excited at the same time. Breuer and colleagues proposed CAIPIRINHA in 2005: shift the slices against each other to make the aliasing easier to undo. Setsompop, Gagoski, Polimeni, Witzel, Wedeen and Wald published blipped CAIPI and slice-GRAPPA in 2012, which made SMS echo planar imaging practical for diffusion imaging and fMRI. Cauley and colleagues reduced the leakage between slices with split slice-GRAPPA in 2014.

## References
