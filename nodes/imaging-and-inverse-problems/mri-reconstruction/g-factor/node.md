---
tag: 1N3E4K
kind: definition
slug: g-factor
name: Geometry factor
aliases:
- g-factor
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: "The noise amplification of a parallel imaging method at each pixel, beyond the sqrt(R) loss from fewer samples. For SENSE it is sqrt([M^-1]_pp [M]_pp) with M = E^H Psi^-1 E, and it is at least 1."
prereqs: [sense, positive-definite-matrix]
see_also: [coil-sensitivity-map, cg-sense, grappa, slice-grappa, image-noise, generalized-least-squares, root-sum-of-squares-coil-combination, matrix-norms]
sources:
  - paper: doi:10.1002/(SICI)1522-2594(199911)42:5<952::AID-MRM16>3.0.CO;2-S
    title: Klaas P. Pruessmann, Markus Weiger, Markus B. Scheidegger and Peter Boesiger, SENSE, sensitivity encoding for fast MRI, Magnetic Resonance in Medicine 42(5), 1999, 952 to 962
    locator: the definition of the geometry factor and the relation SNR_red = SNR_full / (g sqrt(R)) (general locator; equation numbers not confirmed)
  - paper: doi:10.1002/mrm.21728
    title: Philip M. Robson, Aaron K. Grant, Ananth J. Madhuranthakam, Riccardo Lattanzi, Daniel K. Sodickson and Charles A. McKenzie, Comprehensive quantification of signal-to-noise ratio and g-factor for image-based and k-space-based parallel imaging reconstructions, Magnetic Resonance in Medicine 60(4), 2008, 895 to 907
    locator: the pseudo multiple replica method for g-factor maps of any linear reconstruction (general locator)
  - paper: doi:10.1002/mrm.22066
    title: Felix A. Breuer, Stephan A. R. Kannengiesser, Martin Blaimer, Nicole Seiberlich, Peter M. Jakob and Mark A. Griswold, General formulation for quantitative g-factor calculation in GRAPPA reconstructions, Magnetic Resonance in Medicine 62(3), 2009, 739 to 746
    locator: the analytic g-factor of GRAPPA from the image domain form of the kernel (general locator)
  - paper: doi:10.1002/mrm.20713
    title: Peter Kellman and Elliot R. McVeigh, Image reconstruction in SNR units, a general method for SNR measurement, Magnetic Resonance in Medicine 54(6), 2005, 1439 to 1447
    locator: SNR maps in units of the noise standard deviation, with the noise covariance and the g-factor (general locator)
---

The g-factor, or geometry factor, measures how much a parallel imaging reconstruction amplifies the noise at each pixel. Skipping samples costs a factor $\sqrt{R}$ in signal to noise ratio, because the scan collects $R$ times fewer samples. The coil geometry adds a second loss, the g-factor, because the unfolding of [SENSE](/sense/) and the k-space fit of [GRAPPA](/grappa/) mix the noise of the coils. Pruessmann, Weiger, Scheidegger and Boesiger defined it for SENSE in 1999. It depends on the [coil sensitivity maps](/coil-sensitivity-map/), the noise covariance and the sampling pattern, not on the object.

## Definition

Take the Cartesian SENSE model of an $n \times n$ image with $c$ coils, reduction factor $R$, $m = n/R$, and the $c \times c$ Hermitian positive definite noise covariance $\Psi$ between the coils. For the folded pixel $(i, j)$ let $E$ be the $c \times R$ matrix with $E[k][p] = s_k(i + pm, j)$, and let

$$M = E^H \Psi^{-1} E.$$

If $M$ is invertible, the **g-factor** of the image pixel $(i + pm, j)$ is

$$g_p = \sqrt{[M^{-1}]_{pp}\, [M]_{pp}}.$$

With independent k-space noise of covariance $\Psi$ between the coils at each sample, the SENSE output at that pixel has the variance $R\,[M^{-1}]_{pp}$, while the optimal combination of fully sampled data has the variance $1/[M]_{pp}$. So

$$\mathrm{SNR}_{\text{red}} = \frac{\mathrm{SNR}_{\text{full}}}{g_p \sqrt{R}}.$$

The [proof on the SENSE page](/sense/) derives both variances and shows $g_p \ge 1$ (a theorem, by the Cauchy-Schwarz inequality), with equality if and only if column $p$ of $E$ is orthogonal to the other columns in the inner product $u^H \Psi^{-1} w$.

For any linear reconstruction $\hat x = H y$, the same ratio defines the g-factor in general: $g$ at a pixel is the standard deviation of $\hat x$ there, divided by $\sqrt{R}$ times the standard deviation of the optimal fully sampled reconstruction. It can be computed from $H$ (for GRAPPA, Breuer et al. 2009) or estimated by reconstructing many noise samples, the pseudo multiple replica method (Robson et al. 2008). A Monte Carlo estimate is a measurement with a sampling error.

## Examples and non-examples

- **No acceleration.** For $R = 1$, $M$ is a $1 \times 1$ matrix and $g = 1$ at every pixel.
- **Orthogonal coils.** If the coils of a pixel group are disjoint, for example coil 1 sees only the top half and coil 2 only the bottom half, the columns of $E$ are orthogonal and $g = 1$. Then parallel imaging loses only $\sqrt{R}$.
- **Two coils, $R = 2$.** With the column profiles $s_1 = (1, 0.9, 0.5, 0.3)$ and $s_2 = (0.5, 0.6, 1, 0.9)$, $n = 4$ and $\Psi = I$, the pixel group $\{0, 2\}$ has $M = \begin{pmatrix} 1.25 & 1 \\ 1 & 1.25 \end{pmatrix}$, $[M^{-1}]_{00} = 2.2222$ and $g = 1.6667$; the group $\{1, 3\}$ has $g = 1.6288$ (the example of [SENSE](/sense/)).
- **R close to the number of coils.** For four Gaussian ring coils on a $32 \times 32$ grid (the maps of the [coil sensitivity map](/coil-sensitivity-map/) page), the g-factor had the mean 1.342 and the maximum 2.918 at $R = 2$, and the mean 67.3 and the maximum 393 at $R = 4$ (measurement with the SENSE code). With four coils, only about two of them differ along the phase encoding axis at each pixel group, so $R = 4$ is nearly singular.
- **Non-example: the $\sqrt{R}$ loss.** The factor $\sqrt{R}$ comes from the shorter scan and is outside the g-factor. A scan with $g = 1$ still loses $\sqrt{R}$.
- **Non-example: nonlinear methods.** For [compressed sensing MRI](/compressed-sensing-mri/) and other nonlinear reconstructions, the noise in the output depends on the object and on the noise level, so a g-factor map is defined only for a given object and a given noise level, and it is a measurement.

## Related definitions

- [SENSE](/sense/) is the reconstruction for which the closed form holds; [CG-SENSE](/cg-sense/) has the same noise at convergence for the same sampling.
- [GRAPPA](/grappa/) and [slice-GRAPPA](/slice-grappa/) have their own g-factors, from the image domain form of their kernels. In simultaneous multi-slice imaging, the CAIPI shift lowers the g-factor by moving the aliased copies apart.
- The [root-sum-of-squares](/root-sum-of-squares-coil-combination/) and the optimal coil combinations of fully sampled data give the reference noise level $1/[M]_{pp}$.
- Noise models for MR images and the conversion to SNR units: [image noise](/image-noise/); Kellman and McVeigh (2005).

## References
