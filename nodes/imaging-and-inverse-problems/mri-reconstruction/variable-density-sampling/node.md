---
tag: G4DDC4
kind: technique
slug: variable-density-sampling
name: Variable density sampling
aliases:
- variable-density undersampling
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: Draw random k-space samples with a density that falls with distance from the center, where most of the energy of images lies.
prereqs: [k-space, compressed-sensing]
see_also: [compressed-sensing-mri, mutual-coherence, restricted-isometry-property, k-space-trajectory, density-compensation, partial-fourier-reconstruction, sampling-theorem, low-rank-plus-sparse-mri]
sources:
  - paper: doi:10.1109/LSP.2011.2163712
    title: Gilles Puy, Pierre Vandergheynst and Yves Wiaux, On variable density compressive sampling, IEEE Signal Processing Letters 18(10), 2011
    locator: pages 595 to 598 (results for bounded orthonormal systems sampled with a variable density, and a coherence-driven optimization of the density)
  - paper: doi:10.1109/TIP.2013.2288004
    title: Felix Krahmer and Rachel Ward, Stable and robust sampling strategies for compressive imaging, IEEE Transactions on Image Processing 23(2), 2014
    locator: pages 612 to 622 (local coherence, and stable recovery by l1 Haar or total variation minimization from Fourier samples drawn with an inverse square density, general locator for the theorem)
  - paper: doi:10.1017/fms.2016.32
    title: Ben Adcock, Anders C. Hansen, Clarice Poon and Bogdan Roman, Breaking the coherence barrier, a new theory for compressed sensing, Forum of Mathematics Sigma 5, 2017
    locator: article e4 (asymptotic sparsity, asymptotic incoherence and multilevel random sampling)
  - paper: doi:10.1002/mrm.21391
    title: Michael Lustig, David L. Donoho and John M. Pauly, Sparse MRI, the application of compressed sensing for rapid MR imaging, Magnetic Resonance in Medicine 58(6), 2007
    locator: pages 1182 to 1195 (variable density random undersampling and the Monte Carlo choice of a pattern with low interference)
---

Variable density sampling draws the k-space samples of an MRI scan at random, with a probability that is high near the center of k-space and falls toward the edge. It is the sampling part of [compressed sensing MRI](/compressed-sensing-mri/). Uniform random sampling, the classic design of [compressed sensing](/compressed-sensing/), fails for MRI because the low frequencies are coherent with the coarse wavelets: the [mutual coherence](/mutual-coherence/) of the Fourier and wavelet bases is the worst possible. Variable density sampling matches the density to the local coherence of each frequency. Theorems for this design exist (Krahmer and Ward 2014, Adcock et al. 2017), but the exact density used in a scanner, such as a power of the distance from the center, is a heuristic tuned by measurement.

## In plain words

In k-space, the center holds the coarse shape and the contrast of the image, and the edge holds the fine details. Most of the energy of a medical image is in the center.

If you skip samples at random with the same chance everywhere, you skip many center samples. The reconstruction then has the wrong shapes, and no sparsity model can fix that. If you take only the center, you get a blurred image, and the details are lost for good.

Variable density sampling takes the center almost completely and fewer samples farther out, picked at random. The random gaps at the edge produce a noise-like haze that a sparse reconstruction can remove. The full center gives the coarse image that the haze is measured against.

## When it applies

- **Fourier measurements of a compressible image.** The image is sparse in a wavelet basis or in its gradient, and the scanner measures Fourier samples. This is the case in MRI, and also in radio interferometry and some optical systems.
- **The sparsity varies with scale.** Coarse wavelets are not sparse: almost all of them are nonzero. Fine wavelets are sparse. Adcock, Hansen, Poon and Roman call this asymptotic sparsity. The Fourier samples at low frequency see mostly coarse wavelets, and the samples at high frequency see mostly fine ones (asymptotic incoherence).
- **The trajectory can follow a density.** Cartesian 3D scans choose points in the $(k_y, k_z)$ plane freely. 2D scans choose whole lines, so the density is along one axis. Radial and spiral trajectories are dense in the center by their geometry.
- **The reconstruction is nonlinear.** The density is designed for a sparse reconstruction. For a linear reconstruction, such as zero filling or [density compensation](/density-compensation/) of a gridded trajectory, the random gaps stay in the image as noise-like artifacts.

## The template

Let $p(k)$ be the probability of taking the k-space point $k$. A common choice keeps a small center region with $p = 1$ and uses a power law outside it:

```pseudo id=main
VARIABLE-DENSITY-MASK(grid, m, d, c, seed)
L1  for each k in the grid do
L2      if |k_1| <= c and |k_2| <= c then q(k) <- infinity        ▷ the full center
L3      else q(k) <- (1 - r(k))^d                              ▷ r = |k| / max |k|
L4  find s > 0 with sum over k of min(1, s q(k)) = m           ▷ bisection on s
L5  p(k) <- min(1, s q(k)) for every k
L6  draw M(k) = 1 with probability p(k), independently, from the seed
L7  return M
```

The expected number of samples is $m$. With $d = 0$, the samples outside the center are uniform. Larger $d$ puts more samples near the center. Other density shapes, such as $1/|k|^2$ or a Gaussian, fit lines L2 and L3.

**What the theory says.** Let $U = F \Psi^*$ be the unitary matrix that maps wavelet coefficients to Fourier samples, and let $\mu_k = \max_j |U_{kj}|$ be the local coherence of row $k$. Draw $m$ rows independently with probabilities $p_k$ and scale row $k$ by $1/\sqrt{m p_k}$. The theory of bounded orthonormal systems (theorem, constants and powers of $\log n$ left out) gives the restricted isometry property of order $s$ with high probability once $m \gtrsim K^2 s$, where $K^2 = \max_k \mu_k^2 / p_k$. Uniform sampling has $K^2 = n \max_k \mu_k^2$. The density $p_k = \mu_k^2 / \sum_j \mu_j^2$ gives the smallest value, $K^2 = \sum_k \mu_k^2$. For the 2D Fourier and Haar bases, $\mu_k^2$ falls like $1/|k|^2$, and Krahmer and Ward (2014) proved stable recovery with the inverse square density, with a number of samples that grows only with $s$ times powers of $\log n$. Puy, Vandergheynst and Wiaux (2011) chose the density by a convex minimization of the coherence bound.

**Example: local coherence.** On a $32 \times 32$ grid with the orthonormal Haar transform of 4 levels, a computation of all 1024 basis functions gives these values. The largest $\mu_k^2$ is 0.25, at $k = 0$. The sum $\sum_k \mu_k^2$ is 6.26, against $n \max_k \mu_k^2 = 256$ for uniform sampling, a factor of 41. Away from the center, $|k|^2 \mu_k^2$ stays between 0.08 and 0.5 out to $|k| = 8$, so $\mu_k^2$ falls like $1/|k|^2$ until it reaches the floor $1/256$ set by the finest Haar scale. The $5 \times 5$ center holds 28 percent of $\sum_k \mu_k^2$.

**Example: reconstruction.** Take the modified Shepp-Logan phantom on $32 \times 32$ pixels and the template above with $c = 2$ and $m = 410$ (40 percent; the draws give 386 to 422 samples). Reconstruct with 400 FISTA steps of $\frac12\|M F x - y\|^2 + \lambda \|\Psi x\|_1$, Haar $\Psi$, $\lambda = 5 \cdot 10^{-4}$, as on the [compressed sensing MRI](/compressed-sensing-mri/) page. The table gives the relative error for seeds 1, 2 and 3 (measured).

| density | zero filled | CS, seed 1 | CS, seed 2 | CS, seed 3 |
|---|---|---|---|---|
| $d = 0$ (uniform outside the center) | 0.60 to 0.62 | 0.313 | 0.390 | 0.312 |
| $d = 1$ | 0.57 | 0.263 | 0.243 | 0.251 |
| $d = 2$ | 0.55 | 0.359 | 0.268 | 0.315 |
| $d = 4$ | 0.53 to 0.54 | 0.398 | 0.406 | 0.412 |
| the $20 \times 20$ center only (400 samples) | 0.540 | 0.456 | | |

On this image, $d = 1$ is best. A steeper density spends the samples on frequencies that the center already gives, and the center alone is worst among the nonlinear results. On the image made of the 100 largest Haar coefficients of the phantom, with about 285 samples, the order changes: $d = 0$ gives errors of 0.002, $d = 1$ gives 0.014 and 0.023, and $d = 2$ gives 0.248 and 0.073 (seeds 1 and 2). That image has many fine scale coefficients and needs the high frequencies. So the best density depends on the sparsity of the image at each scale, which is what the theory of sparsity in levels describes.

## Classic examples

- **3D Cartesian imaging.** Random points in the $(k_y, k_z)$ plane with a power law or Gaussian density and a fully sampled center. This is the setting of the example above and of the angiography scans of Lustig, Donoho and Pauly (2007).
- **2D Cartesian imaging.** Random phase encoding lines with a density along $k_y$. The incoherence is only along one axis, so the gain is smaller than in 3D.
- **Radial and spiral trajectories.** Radial spokes sample the center at a density that falls like $1/|k|$, and variable density spirals change the spacing between turns. These give variable density without random draws.
- **Dynamic imaging.** A different random pattern in each frame, dense at the center in every frame, makes the artifacts incoherent in time as well. [Low rank plus sparse MRI](/low-rank-plus-sparse-mri/) uses such patterns.

## Variations

- **Multilevel sampling.** Split k-space into rings and take a set fraction of samples at random in each ring, full in the inner rings. Adcock et al. prove recovery for this design in terms of the sparsity of each wavelet level.
- **Poisson disc sampling.** Draw points with a variable density, but with a minimum distance between them, so that no two samples are too close. The gaps are more even than with independent draws, and the design is often used together with parallel imaging (a heuristic).
- **Monte Carlo design.** Draw many masks from the density, compute the interference of each (the largest side lobe of the point spread function in the wavelet domain) and keep the best. Lustig et al. used this.
- **Learned masks.** Choose the mask to reduce the error of a given reconstruction on training images. The result is a measurement for that data and that reconstruction.
- **Continuous trajectories.** Real scanners move along curves, not between free points. Later work builds curves whose time spent in each region follows the density.

## Pitfalls

- **Missing the center.** Without a fully sampled center, a random draw can skip $k = 0$. In the example with $c = 0$, seed 2 skips it for $d = 0$ and $d = 1$, and the errors are 0.700 and 0.621 instead of 0.390 and 0.243 with the center.
- **Too steep a density.** As $d$ grows, the mask turns into a low resolution scan, and the reconstruction becomes blurred. In the example, $d = 4$ is worse than uniform sampling outside the center.
- **One density for every image.** The best density depends on the image and the transform. A density tuned on brain scans need not be best for knees or angiograms.
- **Theory with large constants.** The theorems give the right scaling, not a usable number of samples for a given scan. The density in practice is chosen by measurement.
- **Noise.** Samples at high frequency carry little signal and the same noise as the center samples, so their signal-to-noise ratio is low. Undersampling the edge saves scan time without a large loss of SNR, but a sparse reconstruction at low SNR also removes fine details.
- **Hardware limits.** Gradient slew rates and echo spacing limit which patterns a scanner can acquire quickly. A pattern that is optimal on paper may cost extra time in the scan.

## Exercises

1. Show that the expected number of samples of the mask in the template is $\sum_k p(k)$, and that the bisection in line L4 finds $s$ because the sum is continuous and nondecreasing in $s$.
2. Let $U$ be unitary with local coherences $\mu_k$. Show that $\max_k \mu_k^2 / p_k$ over all probability vectors $p$ is smallest for $p_k = \mu_k^2 / \sum_j \mu_j^2$, with the value $\sum_k \mu_k^2$.
3. Show that $1 \le \sum_k \mu_k^2 \le n$ for every unitary $U$. Show that the lower value holds when all entries have modulus $n^{-1/2}$, as for the DFT against the pixel basis, and the upper value holds for the identity.
4. Compute $\mu_0^2$ for the unitary DFT on $\mathbb{C}^{n}$ and the Haar basis with the coarsest scaling function constant on blocks of length $b$. Check the value 0.25 of the example for the 2D case with $16 \times 16$ blocks on a $32 \times 32$ grid.
5. Explain why a radial trajectory with equally spaced spokes has a density that falls like $1/|k|$ in 2D.
6. In the example, $d = 2$ gives the error 0.248 for seed 1 and 0.073 for seed 2 on the sparse image. What does this say about results from one random draw?

## References
