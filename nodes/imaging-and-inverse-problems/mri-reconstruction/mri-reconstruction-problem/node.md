---
tag: JAYDY8
kind: problem
slug: mri-reconstruction-problem
name: MRI reconstruction
aliases:
- magnetic resonance image reconstruction
area: imaging-and-inverse-problems/mri-reconstruction
level: intro
summary: Recover the magnetization image from samples of its Fourier transform taken along k-space trajectories by one or more receive coils.
model: real-ram
prereqs: [mri-signal-equation, k-space, inverse-problem]
see_also: [sense, grappa, compressed-sensing-mri, partial-fourier-reconstruction, density-compensation, g-factor, least-squares-problem, tomographic-reconstruction-problem]
sources:
  - paper: doi:10.1002/(SICI)1522-2594(199911)42:5<952::AID-MRM16>3.0.CO;2-S
    title: Klaas P. Pruessmann, Markus Weiger, Markus B. Scheidegger and Peter Boesiger, SENSE, sensitivity encoding for fast MRI, Magnetic Resonance in Medicine 42(5), 1999, 952 to 962
    locator: the unfolding of Cartesian undersampled multi-coil data pixel group by pixel group, the noise matrix and the g-factor (general locator; equation numbers not confirmed)
  - paper: doi:10.1109/MSP.2010.936726
    title: Jeffrey A. Fessler, Model-based image reconstruction for MRI, IEEE Signal Processing Magazine 27(4), 2010, 81 to 89
    locator: the discrete system model of MRI, its noise model and the regularized least squares formulation (general locator)
  - paper: doi:10.1002/mrm.21391
    title: Michael Lustig, David Donoho and John M. Pauly, Sparse MRI, the application of compressed sensing for rapid MR imaging, Magnetic Resonance in Medicine 58(6), 2007, 1182 to 1195
    locator: undersampled k-space with a sparsity penalty and random variable density sampling (general locator)
  - paper: doi:10.1017/fms.2016.32
    title: Ben Adcock, Anders C. Hansen, Clarice Poon and Bogdan Roman, Breaking the coherence barrier, a new theory for compressed sensing, Forum of Mathematics, Sigma 5, 2017, e4
    locator: asymptotic sparsity, asymptotic incoherence and multilevel sampling for Fourier measurements and wavelets (general locator)
  - book: isbn:9780780347236
    title: Zhi-Pei Liang and Paul C. Lauterbur, Principles of Magnetic Resonance Imaging, A Signal Processing Perspective, IEEE Press, 2000
    locator: the chapters on image reconstruction and on fast and constrained reconstruction (general locator; chapter numbers not confirmed)
---

MRI reconstruction is the problem of computing an image of the transverse magnetization from the samples that the receive coils of a scanner record in [k-space](/k-space/). By the [MRI signal equation](/mri-signal-equation/), each sample is one value of the Fourier transform of the image times the sensitivity of a coil, so the problem is a linear [inverse problem](/inverse-problem/) with a Fourier forward operator and complex Gaussian noise. With a full Cartesian grid and one coil it is solved by one inverse FFT. Every faster scan drops samples, and then the answer is unique only with more knowledge: the coil sensitivities ([SENSE](/sense/), [GRAPPA](/grappa/)), a smooth image phase ([partial Fourier reconstruction](/partial-fourier-reconstruction/)) or sparsity ([compressed sensing MRI](/compressed-sensing-mri/)).

## In plain words

An MRI scanner does not take a photograph. It measures how strongly the body contains each stripe pattern of a given width and direction, one pattern at a time. A full set of patterns on a regular grid gives the picture back by one standard computation. Collecting all of them takes minutes, and patients move.

So scanners skip patterns. Then many pictures agree with the measurements, and the computer needs a reason to choose one. Several receive coils help, because each coil sees the body with its own brightness profile. A picture whose phase changes slowly helps. A picture that is simple in some description, with few large coefficients, helps too. Each family of methods uses one or more of these reasons.

## Definition

**Unknown.** An image $x \in \mathbb{C}^{n^2}$ on an $n \times n$ grid that covers the field of view $L \times L$, the transverse magnetization $m$ at the pixel centers. Some variants have a 3D volume or a time series.

**Forward model.** For $c$ receive coils with the diagonal sensitivity matrices $C_1, \ldots, C_c$, the unitary 2D DFT $F_u = n^{-1} F$ (so $F_u^H F_u = I$) and a sampling mask $M$ that keeps $m$ of the $n^2$ grid points,

$$y_j = M F_u C_j x + e_j, \quad j = 1, \ldots, c, \qquad \text{or} \qquad y = E x + e$$

with the stacked encoding matrix $E$ of size $c m \times n^2$. The k-space spacing is $\Delta k = 1/L$ and the pixel size is $L/n$. For a non-Cartesian [k-space trajectory](/k-space-trajectory/), $M F_u$ is replaced by the [nonuniform discrete Fourier transform](/nonuniform-discrete-fourier-transform/) at the sampled points $k_1, \ldots, k_m$. One uniform coil means $c = 1$ and $C_1 = I$.

**Noise.** The noise $e$ is circular complex Gaussian with mean 0: the real and imaginary parts are independent with equal variance. It is white over the samples and correlated between coils, with a $c \times c$ covariance $\Psi$, so $e \sim \mathcal{CN}(0, \Psi \otimes I_m)$. After a whitening by $\Psi^{-1/2}$ the noise is $\mathcal{CN}(0, \sigma^2 I)$, and the negative log-likelihood is $\|E x - y\|^2 / \sigma^2$ plus a constant.

**Output.** An estimate $\hat x$ of $x$, or of its magnitude $|x|$ when only that is wanted. The acceleration factor is $R = n^2 / m$, the ratio of the full number of grid samples to the number acquired.

**Well-posedness.** In the sense of Hadamard (see [well-posed problem](/well-posed-problem/)), the problem is well-posed for a full Cartesian grid. Every mask with $m < n^2$ breaks uniqueness for one coil, and with several coils uniqueness depends on the sensitivities; the Bounds section gives the exact conditions.

## Variants

- **Fully sampled Cartesian.** $M = I$ and $c = 1$: $\hat x = F_u^H y$, one inverse FFT.
- **Non-Cartesian.** Radial, spiral or [PROPELLER](/propeller-mri/) data, solved by gridding with [density compensation](/density-compensation/), by [conjugate phase reconstruction](/conjugate-phase-reconstruction/) or by iterative least squares with the [nonuniform FFT](/nonuniform-fft/).
- **Partial Fourier.** A little more than half of k-space, with the prior that $x$ is a real image times a smooth phase ([partial Fourier reconstruction](/partial-fourier-reconstruction/)).
- **Parallel imaging.** $c > 1$ with known or estimated sensitivities ([coil sensitivity map](/coil-sensitivity-map/)) and regular undersampling.
- **Compressed sensing.** Random or [variable density sampling](/variable-density-sampling/) with a sparsity penalty, posed as $\min_x \frac{1}{2}\|E x - y\|^2 + \lambda R(x)$.
- **Dynamic imaging.** A time series $x_t$ with models that couple the frames, such as the [partial separability model](/partial-separability-model/) and [low rank plus sparse](/low-rank-plus-sparse-mri/) models.
- **Model-based and quantitative.** The unknown is a parameter map such as $T_1$, $T_2$ or the field ([MR fingerprinting](/mr-fingerprinting/), [quantitative susceptibility mapping](/quantitative-susceptibility-mapping/)), and the forward model adds the [Bloch equations](/bloch-equations/) or a field model.
- **Off-resonance and motion.** The forward model includes a field map or rigid motion between parts of the scan.

## Examples

All examples use one line of $n = 8$ pixels and the unitary DFT of length 8.

**Folding.** Take $x = [1, 2, 3, 4, 5, 6, 7, 8]$, one coil, and keep only the even frequencies ($R = 2$). The zero filled image $F_u^H M F_u x$ is $[3, 4, 5, 6, 3, 4, 5, 6]$: each pixel holds $(x_j + x_{j+4})/2$, the average of two pixels half a field of view apart. The scan cannot tell $x$ from any other image with the same sums $x_j + x_{j+4}$.

**An invisible image.** The image $w_j = e^{2\pi i j/8}$ has $F_u w = [0, 2\sqrt{2}, 0, 0, 0, 0, 0, 0]$. If the mask drops frequency 1, then $x$ and $x + w$ give the same data. This is the null space of $M F_u$.

**Two coils unfold the fold.** Keep $R = 2$ and add a second coil. At the pixel pair $(j, j + 4)$ let coil 1 have the sensitivities $(1, 0.5)$ and coil 2 have $(0.5, 1)$, and let the true values be $(3, 1)$. The aliased coil images at pixel $j$ are $(1 \cdot 3 + 0.5 \cdot 1)/2 = 1.75$ and $(0.5 \cdot 3 + 1 \cdot 1)/2 = 1.25$. The system $\frac{1}{2}\begin{bmatrix} 1 & 0.5 \\ 0.5 & 1 \end{bmatrix} \begin{bmatrix} a \\ b \end{bmatrix} = \begin{bmatrix} 1.75 \\ 1.25 \end{bmatrix}$ has the unique solution $(a, b) = (3, 1)$. With white noise of equal level on both coils, the g-factor of pixel $j$ is $\sqrt{[(S^H S)^{-1}]_{11} [S^H S]_{11}} = \sqrt{(1.25/0.5625) \cdot 1.25} = 5/3$, so the SNR is $1/(\frac{5}{3}\sqrt{2}) = 0.424$ times that of the full scan.

**Non-example.** If both coils have the sensitivities $(1, 1)$ at that pair, the matrix is singular, and the second coil adds no information. Coils must differ in space to unfold.

## Known algorithms

| Method | Data and prior | What it gives |
|---|---|---|
| Inverse FFT | full Cartesian grid | exact for no noise; $O(n^2 \log n)$ |
| Gridding and adjoint [nonuniform FFT](/nonuniform-fft/) with [density compensation](/density-compensation/) | non-Cartesian | approximate inverse, one pass |
| [Conjugate phase reconstruction](/conjugate-phase-reconstruction/) | non-Cartesian with a field map | the weighted adjoint $E^H W y$; exact only in special cases |
| [Homodyne reconstruction](/homodyne-reconstruction/), [POCS partial Fourier](/pocs-partial-fourier/) | partial k-space, smooth phase | real image or phase-constrained image |
| [Root-sum-of-squares combination](/root-sum-of-squares-coil-combination/) | full data, many coils | a magnitude image without sensitivity maps |
| [SENSE](/sense/), [CG-SENSE](/cg-sense/) | undersampled, known sensitivities | weighted least squares; direct per pixel group for Cartesian data, [conjugate gradient](/conjugate-gradient-method/) otherwise |
| [GRAPPA](/grappa/), [SPIRiT](/spirit/), [ESPIRiT](/espirit/) | undersampled with a fully sampled center | missing samples or sensitivity maps from the calibration region |
| [Compressed sensing MRI](/compressed-sensing-mri/) | random or variable density sampling, sparsity | penalized least squares by [FISTA](/fista/), [ADMM](/admm/) or similar |
| [LORAKS](/loraks/), [low rank plus sparse](/low-rank-plus-sparse-mri/), [k-t BLAST](/k-t-blast/) | structured or dynamic data | low rank or prior-based completion |
| [Variational network](/variational-network-mri/) | undersampled, trained on data | an unrolled iteration with learned parts; quality is measured, not proved |
| [PROPELLER](/propeller-mri/) | rotated blades | motion estimates and a corrected image |

## Bounds

- **Counting (theorem).** Without a prior, $E$ must have full column rank, which needs $c m \ge n^2$ complex equations. For one coil this means $m = n^2$: every dropped sample adds a dimension to the null space, as in the invisible image above.
- **Cartesian SENSE (theorem).** With regular undersampling by an integer $R$ along one axis, the problem splits into independent systems $a = S z$ with $c$ equations for the $R$ pixels $z$ of one alias group. The group is determined if and only if $S$ has full column rank, which needs $R \le c$. With the noise covariance $\Psi$, the weighted least squares estimate has covariance $(S^H \Psi^{-1} S)^{-1}$, and the SNR of pixel $p$ is the SNR of the full scan divided by $g_p \sqrt{R}$ with $g_p = \sqrt{[(S^H \Psi^{-1} S)^{-1}]_{pp}\, [S^H \Psi^{-1} S]_{pp}}$ (Pruessmann and colleagues 1999). The factor $\sqrt{R}$ comes from the shorter scan and $g_p$ from the geometry; see [g-factor](/g-factor/).
- **The g-factor is at least 1 (theorem).** For a Hermitian positive definite $G$ and a unit vector $u$, the Cauchy-Schwarz inequality gives $1 = (u^H u)^2 = (u^H G^{1/2} G^{-1/2} u)^2 \le (u^H G u)(u^H G^{-1} u)$. With $G = S^H \Psi^{-1} S$ and $u = e_p$ this is $g_p^2 \ge 1$. Equality holds when the column $p$ of $\Psi^{-1/2} S$ is orthogonal to the other columns.
- **Full sampling keeps the noise (theorem).** For $M = I$ and one coil, $F_u^H e \sim \mathcal{CN}(0, \sigma^2 I)$, because $F_u$ is unitary. Since the system is square and invertible, $F_u^H y$ is the only linear unbiased estimator.
- **Sampling theory.** On a Cartesian grid, the spacing must satisfy $\Delta k \le 1/L$ for an object of size $L$, else the image folds; the extent $k_{\max}$ sets the pixel size $1/(2 k_{\max})$ ([sampling theorem](/sampling-theorem/)).
- **Compressed sensing.** Recovery guarantees by the restricted isometry property hold for random designs that are incoherent with the sparsity basis. Fourier samples and wavelets are not incoherent at coarse scales, so the theory for MRI uses asymptotic sparsity and multilevel random sampling (Adcock, Hansen, Poon and Roman 2017). These are theorems about those sampling laws; the sampling densities used on scanners are tuned heuristics.
- **Cost in the [real RAM](/real-ram/).** An inverse FFT costs $O(n^2 \log n)$. Cartesian SENSE costs $O(c R^2)$ for each of the $n^2/R$ alias groups, $O(c R n^2)$ in total. An iterative method costs $K$ times the price of one application of $E$ and one of $E^H$, that is $O(K c\, n^2 \log n)$ with FFTs, plus the cost of the penalty.

## Reductions

- **To least squares.** Under the Gaussian model, after whitening, the maximum likelihood estimate solves $\min_x \|E x - y\|^2$, a [least squares problem](/least-squares-problem/), and the MAP estimate with a prior $\propto e^{-\lambda R(x)}$ solves $\min_x \frac{1}{2}\|E x - y\|^2 + \lambda R(x)$ (with $\sigma$ absorbed into $\lambda$).
- **To an inverse FFT.** Full Cartesian data with one coil reduce to $\hat x = F_u^H y$.
- **To small dense systems.** Cartesian undersampling with coils reduces, by the folding identity of the [signal equation](/mri-signal-equation/), to $n^2/R$ systems of size $c \times R$.
- **To nonuniform Fourier inversion.** Non-Cartesian data reduce to the inversion of the nonuniform DFT; its adjoint with density weights is the gridding estimate.
- **To a real problem.** With a known phase $p$, writing $x = p \odot \rho$ with a real $\rho$ halves the number of real unknowns. This is the reduction behind partial Fourier methods.
- **From tomography.** Radial MRI and parallel beam CT meet through the [Fourier slice theorem](/fourier-slice-theorem/): each radial spoke is the 1D transform of a projection, which links this problem with the [tomographic reconstruction problem](/tomographic-reconstruction-problem/).

## Applications

- **Clinical anatomical imaging.** $T_1$, $T_2$ and proton density weighted images of every organ, mostly Cartesian with parallel imaging and partial Fourier.
- **Fast and dynamic imaging.** Cardiac cine, perfusion and contrast-enhanced angiography, where undersampling with sparsity or low rank models shortens breath holds.
- **Functional and diffusion MRI.** Echo planar data with field map correction and partial Fourier.
- **Quantitative imaging.** Parameter maps by MR fingerprinting and susceptibility maps by QSM.
- **Benchmarks for learned methods.** The fastMRI data set (Zbontar and colleagues 2018, arXiv:1811.08839) is a common test bed. Image quality numbers on it, such as [PSNR](/psnr/) and [SSIM](/structural-similarity-index/), are measurements on that data set and sampling setting, not properties of an algorithm.

## References
