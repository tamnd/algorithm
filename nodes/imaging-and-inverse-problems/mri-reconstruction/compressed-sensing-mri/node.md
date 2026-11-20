---
tag: 09KKZ1
kind: technique
slug: compressed-sensing-mri
name: Compressed sensing MRI
aliases:
- sparse MRI
- CS-MRI
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: Undersample k-space at random and reconstruct by minimizing a sparsity penalty, such as wavelet L1 and total variation, subject to data consistency.
prereqs: [compressed-sensing, mri-reconstruction-problem, proximal-operator]
see_also: [variable-density-sampling, low-rank-plus-sparse-mri, loraks, sense, total-variation-denoising, iterative-shrinkage-thresholding, discrete-wavelet-transform, variational-network-mri]
sources:
  - paper: doi:10.1002/mrm.21391
    title: Michael Lustig, David L. Donoho and John M. Pauly, Sparse MRI, the application of compressed sensing for rapid MR imaging, Magnetic Resonance in Medicine 58(6), 2007
    locator: pages 1182 to 1195 (the l1 wavelet and total variation objective under a data constraint, incoherent random undersampling with a variable density, and the reconstruction by nonlinear conjugate gradients)
  - paper: doi:10.1109/TIT.2005.862083
    title: Emmanuel J. Candès, Justin Romberg and Terence Tao, Robust uncertainty principles, exact signal reconstruction from highly incomplete frequency information, IEEE Transactions on Information Theory 52(2), 2006
    locator: pages 489 to 509 (exact recovery from random Fourier samples by l1 or total variation minimization, with the Shepp-Logan phantom as the example)
  - paper: doi:10.1017/fms.2016.32
    title: Ben Adcock, Anders C. Hansen, Clarice Poon and Bogdan Roman, Breaking the coherence barrier, a new theory for compressed sensing, Forum of Mathematics Sigma 5, 2017
    locator: article e4 (sparsity in levels, local coherence in levels and multilevel random sampling, the theory for Fourier sampling with wavelets)
  - paper: doi:10.1137/080716542
    title: Amir Beck and Marc Teboulle, A fast iterative shrinkage-thresholding algorithm for linear inverse problems, SIAM Journal on Imaging Sciences 2(1), 2009
    locator: pages 183 to 202 (FISTA and its O(1/k^2) rate in the objective)
---

Compressed sensing MRI (CS-MRI) applies [compressed sensing](/compressed-sensing/) to the MRI scanner. The scanner measures samples of the Fourier transform of the image, one at a time, so the scan time grows with the number of samples. CS-MRI skips a random subset of these samples and reconstructs the image by [sparse signal recovery](/sparse-signal-recovery/): it looks for the image that fits the measured samples and has the smallest $\ell_1$ norm in a wavelet basis, often with a [total variation](/total-variation-denoising/) term. The general theory of compressed sensing asks for a measurement matrix with the [restricted isometry property](/restricted-isometry-property/), and then [basis pursuit](/basis-pursuit/) recovers every sparse signal. MRI does not meet this condition: the measurements must be rows of the Fourier matrix, and the low frequencies are coherent with the coarse wavelets. So CS-MRI samples the center of k-space densely ([variable density sampling](/variable-density-sampling/)), and its guarantees come from a theory of sparsity in levels. Lustig, Donoho and Pauly (2007) introduced the method.

## In plain words

An MRI scanner measures an image one frequency at a time. Measuring all frequencies takes long, and the patient must lie still.

Most medical images can be described by a small number of wavelet patterns. So most of the measured data are redundant. CS-MRI measures only some frequencies, picked at random, with more of them near the center, where most of the energy is.

If you set the missing frequencies to zero, the image gets a noise-like haze, because the samples were random. The haze is spread over many wavelet patterns, while the true image uses few. A computer then searches for the image that agrees with the measured frequencies and uses the fewest wavelet patterns. This removes the haze and keeps the image.

## When it applies

- **The image is compressible in a known transform.** There is an orthonormal wavelet basis $\Psi$, or a finite difference operator, in which the image has few large coefficients. Anatomical images, angiograms and dynamic series (in a temporal transform) have this property. Images that are mostly texture or noise do not.
- **The scanner can sample k-space at chosen points.** On a Cartesian grid, the readout direction is always fully sampled. So random undersampling applies to the phase encoding directions: random lines in 2D imaging, or random points in the $(k_y, k_z)$ plane in 3D imaging. Non-Cartesian trajectories, such as radial and spiral ones, give a similar effect.
- **The undersampling artifacts are incoherent.** The zero filled image $F^* M y$ is the true image plus an interference term. With random sampling, this term looks like noise in the transform domain, and a sparse estimate can remove it. With regular sampling, it is a set of shifted copies of the image, which are as sparse as the image itself and cannot be removed.
- **The scan time is the limit.** The gain is a shorter scan, or a higher resolution in the same time. The reconstruction runs afterwards on a computer and is iterative.
- **The noise is moderate.** Undersampling does not raise the signal-to-noise ratio. At low SNR, the sparse estimate removes small details together with the noise.

## The template

Let $x \in \mathbb{C}^n$ be the image, $F$ the unitary 2D DFT, $M$ a 0/1 mask with $m$ ones and $y = M F x + e$ the data. Lustig, Donoho and Pauly solve

$$\min_x \|\Psi x\|_1 + \alpha \operatorname{TV}(x) \quad \text{subject to} \quad \|M F x - y\|_2 \le \varepsilon.$$

In practice, one solves the penalized form $\min_x \frac12 \|M F x - y\|_2^2 + \lambda \|\Psi x\|_1$ (with a TV term if wanted). The weights $\alpha$ and $\lambda$ are design choices. With an orthonormal $\Psi$ and no TV term, [FISTA](/fista/) solves it with closed form steps:

```pseudo id=main
CS-MRI(x, Psi, density, lambda, K)
L1  draw the mask M at random with the given density   ▷ dense near k = 0
L2  y <- M F x + e                                     ▷ the scan: only m of n samples
L3  u <- F* M y;  z <- u;  t <- 1                       ▷ the zero filled image
L4  for k = 1 to K do
L5      v <- z - F* M (M F z - y)                       ▷ gradient step with step 1
L6      u_new <- Psi* soft(Psi v, lambda)              ▷ proximal step of lambda ||Psi x||_1
L7      t_new <- (1 + sqrt(1 + 4 t^2)) / 2
L8      z <- u_new + ((t - 1) / t_new) (u_new - u);  u <- u_new;  t <- t_new
L9  return u
```

Lines L1 and L2 are the acquisition, and lines L3 to L9 are the reconstruction. The step size 1 in line L5 is valid because $\|M F\| \le 1$, so the gradient of the data term is 1-Lipschitz. Line L6 is the [proximal operator](/proximal-operator/) of $\lambda \|\Psi x\|_1$ for an orthonormal $\Psi$: $\operatorname{soft}(c, \lambda) = c \max(0, 1 - \lambda / |c|)$ for each complex coefficient. Without lines L7 and L8, this is ISTA, the [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/) method. FISTA reaches an objective within $O(1/k^2)$ of the minimum after $k$ steps (Beck and Teboulle 2009, a theorem). Each step costs two FFTs and two wavelet transforms, so $O(n \log n)$ for an image of $n$ pixels.

**Why the center must be sampled.** Let $\Psi$ be the orthonormal Haar basis. Its coarsest function is the constant vector $n^{-1/2} \mathbf{1}$, which is also the DFT row at $k = 0$. So the coherence $\sqrt n \max |\langle f_k, \psi_j \rangle|$ is $\sqrt n$, the worst possible value. So the theorems for uniformly random rows, whose sample count grows with the square of the coherence, give no useful bound here. This says nothing against the method itself, only against that theory. The low frequencies carry the coarse wavelets, which are not sparse, and the high frequencies carry the fine wavelets, which are sparse. Adcock, Hansen, Poon and Roman (2017) proved recovery guarantees for this structure: sparsity in levels, with sampling that is full or dense in the low frequency levels and sparse in the high ones.

**Example.** Take the modified Shepp-Logan phantom on $32 \times 32$ pixels, the orthonormal Haar transform with 4 levels, and random masks in the 2D k-space plane. Each mask keeps the $5 \times 5$ lowest frequencies and draws the other points with probability proportional to $(1 - r)^d$, where $r$ is the distance from $k = 0$ divided by its largest value. The scale is set so that the expected number of samples is fixed. The values below are relative errors, measured with a short script.

- **An exactly sparse image.** Keep the 100 largest Haar coefficients of the phantom, so the image is 100-sparse. Measure about 285 samples (28 percent), with $d = 0$ (uniform outside the center). The zero filled image has the error 0.647. After 600 FISTA steps with $\lambda = 2 \cdot 10^{-4}$, the error is 0.0018: the image is recovered up to the small bias of $\lambda$. With $d = 1$ the error is 0.014. The $16 \times 16$ lowest frequencies (256 samples) give 0.618 with the same solver, because they hold no information on the fine wavelets.
- **The phantom itself.** It has 317 nonzero Haar coefficients and is only compressible. With about 395 samples (39 percent), $d = 1$, $\lambda = 5 \cdot 10^{-4}$ and 400 steps, the error is 0.263 against 0.571 for zero filling, for three seeds 0.24 to 0.26. The $20 \times 20$ lowest frequencies give 0.456, and uniform sampling outside the center gives 0.31 to 0.39.

So the gain over zero filling is large for a sparse image and moderate for a compressible one, and the best density depends on the image. The [variable density sampling](/variable-density-sampling/) page has the full table.

## Classic examples

- **Brain imaging with fast spin echo.** Lustig, Donoho and Pauly undersampled 2D multislice brain scans with random phase encoding lines, more of them near the center, and reconstructed with wavelets and TV.
- **3D contrast enhanced angiography.** Angiograms are sparse in the image domain itself, because only the vessels are bright. Random points in the $(k_y, k_z)$ plane give strong acceleration. This was the second main example of the 2007 paper.
- **Dynamic imaging.** A cardiac cine or perfusion series is sparse in a temporal Fourier transform. Sampling patterns that change from frame to frame make the artifacts incoherent in time. [Low rank plus sparse MRI](/low-rank-plus-sparse-mri/) adds a low rank part to this model.
- **Combination with parallel imaging.** With coil maps, the operator $M F$ becomes the [SENSE](/sense/) operator $(M F c_j)_j$. The same template applies, and the coil maps and the sparsity both help to remove the undersampling artifacts.

## Variations

- **The sparsity term.** Wavelets, TV, [total generalized variation](/total-generalized-variation/), learned dictionaries ([k-SVD](/k-svd/)) and low rank models of local patches or of k-space neighborhoods ([LORAKS](/loraks/)) all fit the same template.
- **The solver.** Lustig et al. used nonlinear conjugate gradients on a smoothed penalized form. ISTA, FISTA, [ADMM](/admm/) and the split Bregman method are now common, because their steps are exact for the $\ell_1$ term. Greedy methods such as [CoSaMP](/cosamp/) and [iterative hard thresholding](/iterative-hard-thresholding/) also fit.
- **Constrained or penalized.** The constrained form uses the noise level $\varepsilon$ directly. The penalized form needs a choice of $\lambda$, for example by the [discrepancy principle](/morozov-discrepancy-principle/).
- **Learned reconstructions.** The [variational network](/variational-network-mri/) and other unrolled networks replace the hand-made sparsity term by a learned one, with a fixed number of steps.

## Pitfalls

- **Regular undersampling.** Skipping every second line gives aliasing copies of the image, not incoherent noise, and CS cannot remove them. Use random sampling, or combine regular sampling with coil maps.
- **Missing the k-space center.** A random draw that skips $k = 0$ loses the mean of the image, which no sparse model can recover. Always sample a small center region fully.
- **Too strong a penalty.** A large $\lambda$ removes small structures and low contrast details, and TV makes smooth regions look like flat patches. Check the residual $\|M F u - y\|$ against the noise level.
- **Phase.** MRI images are complex, and their phase is not sparse. Use complex soft thresholding on the magnitude, or a model that handles the phase, such as LORAKS.
- **Errors and metrics.** A low mean squared error does not mean that all small lesions are kept. The quality of a CS reconstruction for a clinical task is a measurement.
- **Not converged.** Stopping FISTA early leaves part of the artifacts. The objective, not the image error, is what FISTA is proved to reduce.

## Exercises

1. Let $\Psi$ be unitary. Show that the proximal operator of $\lambda \|\Psi x\|_1$ is $v \mapsto \Psi^* \operatorname{soft}(\Psi v, \lambda)$.
2. Show that $\|M F\| \le 1$ for a unitary $F$ and a 0/1 mask $M$, and that the gradient of $\frac12 \|M F x - y\|^2$ is 1-Lipschitz.
3. Show that the zero filled image $F^* M y$ is the solution of $M F x = y$ with the least $\ell_2$ norm.
4. Show that the coherence of the unitary DFT and the orthonormal Haar basis of $\mathbb{C}^n$ is $\sqrt n$. Which pairs of vectors reach it?
5. Let $M$ keep every second column of k-space. Show that $F^* M F x = \frac12 (x + x')$, where $x'$ is $x$ moved by half the field of view. Why can a sparse penalty not separate $x$ from $x'$?
6. In the example, the low resolution mask has 256 samples and gives a CS error of 0.618 on the 100-sparse image. Explain why a sparse penalty cannot fill in high frequencies that are not measured at all.

## References
