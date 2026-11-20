---
tag: KXJYFX
kind: algorithm
slug: multiscale-clean
name: Multiscale CLEAN
aliases:
- MS-CLEAN
- multi-scale CLEAN
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Extend CLEAN with components of several sizes: smooth the residual at each scale, pick the scale and pixel whose step lowers the misfit most, and update all smoothed residuals."
solves: [image-deblurring]
model: real-ram
complexity:
  vars: {n: the number of pixels, s: the number of scales, K: the number of iterations}
  time: {worst: Θ(K s n + s² n log n), average: Θ(K s n + s² n log n), best: Θ(K s n + s² n log n)}
  space: {extra: Θ(s² n)}
properties: {deterministic: true, iterative: true, linear: false, greedy: true, nonnegative: false, monotone_misfit: true}
history:
  year: 2008
  people: [Tim J. Cornwell]
  note: "Cornwell (2008) gave the multiscale form of CLEAN, with scale functions of several widths and the cross-scale beams that keep all smoothed residuals up to date."
prereqs: [hogbom-clean, dirty-image, convolution-theorem]
see_also: [cotton-schwab-clean, aperture-synthesis, maximum-entropy-method-imaging, scale-space-representation, orthogonal-matching-pursuit, coordinate-descent, discrete-wavelet-transform, w-projection]
sources:
  - paper: doi:10.1109/JSTSP.2008.2006388
    title: "T. J. Cornwell, Multiscale CLEAN deconvolution of radio synthesis images, IEEE Journal of Selected Topics in Signal Processing 2(5), 2008"
    locator: "pages 793 to 801 (the scale functions, the smoothed residuals, the cross-scale beams and the choice of scale)"
  - paper: doi:10.1051/0004-6361/201117104
    title: "U. Rau and T. J. Cornwell, A multi-scale multi-frequency deconvolution algorithm for synthesis imaging in radio interferometry, Astronomy and Astrophysics 532, A71, 2011"
    locator: "the article (multiscale components combined with a spectral model over a wide band)"
  - book: isbn:9783319444314
    title: "A. Richard Thompson, James M. Moran and George W. Swenson Jr., Interferometry and Synthesis in Radio Astronomy, third edition, Springer, 2017"
    locator: "Chapter 11, Further Imaging Techniques (CLEAN and its variants)"
---

Multiscale CLEAN fits a [dirty image](/dirty-image/) with smooth blobs of several widths in place of the single points of [Hogbom CLEAN](/hogbom-clean/). It keeps one smoothed copy of the residual for each scale, picks the scale and pixel where a step lowers the misfit to the data the most, adds a blob of that scale to the model, and subtracts the matching cross-scale beam from every smoothed residual. Extended emission, such as a nebula or a radio lobe, then needs far fewer components, and the model avoids the mottled look of point CLEAN. Like Hogbom CLEAN it works on images with a fixed dirty beam; [Cotton-Schwab CLEAN](/cotton-schwab-clean/) is the major-cycle frame around it that goes back to the visibilities.

## In plain words

Point CLEAN explains a picture with dots. That works for stars, but a smooth cloud needs hundreds of dots, and the result looks spotty. Multiscale CLEAN has a box of stamps: a dot, a small round blob and a large round blob. At each step it tries every stamp at every place, and it keeps the one that explains the most of what is left. A large cloud is then covered by a few large blobs, and the stars still get dots. To do this fast, the method keeps one blurred copy of the leftover picture for each stamp size, and it updates all of them after each step.

## The problem

The setting is that of [Hogbom CLEAN](/hogbom-clean/). The sky $x$ lives on a periodic grid of $n$ pixels. The array measures the visibilities $V = \hat x$ at the frequencies with weight $w_k > 0$, with $w_{-k} = w_k$ and $W = \sum_k w_k$. The dirty beam is $B = \frac1W \mathcal F^{-1}(n\,w)$, so $B_0 = 1$, and the dirty image is $D = B \ast x$. The misfit of a model $M$ is

$$Q(M) = \frac1W \sum_k w_k\, |V_k - \hat M_k|^2 .$$

The input also has $s$ scale functions $\phi_0, \ldots, \phi_{s-1}$. Each is real, has unit sum and is symmetric, $\phi(-q) = \phi(q)$, and $\phi_0 = \delta$ is the point. The code uses $\phi(q) \propto 1 - |q|^2/a^2$ for $|q| < a$, a truncated parabola of radius $a$ pixels. The output is a model $M = \sum_j c_j\, \phi_{s_j}(\cdot - p_j)$ and the residual $R = D - B \ast M$.

## The algorithm

Write $I_t = \phi_t \ast R$ for the residual smoothed at scale $t$, and $B_{ut} = \phi_u \ast \phi_t \ast B$ for the cross-scale beams. A blob of scale $u$ at pixel $p$ with flux $c$ changes $I_t$ by $-c\,B_{ut}(\cdot - p)$.

```pseudo id=main
MULTISCALE-CLEAN(D, B, φ_0..φ_{s-1}, g, τ, K)     ▷ φ_0 = δ
L1  I_t ← φ_t ∗ D for every scale t, M ← 0
L2  B_ut ← φ_u ∗ φ_t ∗ B for every pair of scales u, t
L3  for k ← 1 to K do
L4      (u, p) ← the scale and pixel with the largest |I_u(p)| / √B_uu(0)
L5      if |I_u(p)| ≤ τ then break
L6      c ← g I_u(p) / B_uu(0)
L7      M ← M + c φ_u(· - p)                 ▷ a blob of scale u at p
L8      I_t(q) ← I_t(q) - c B_ut(q - p) for every scale t and pixel q
L9  return M, I_0                            ▷ I_0 = R, the residual
```

Line L8 keeps every $I_t$ equal to $\phi_t \ast (D - B \ast M)$, so the smoothed residuals never need to be computed again. Line L4 is the greedy rule: a step at $(u, p)$ lowers $Q$ by $(2g - g^2)\, I_u(p)^2 / B_{uu}(0)$, and L4 picks the largest such drop. A large blob has a small $B_{uu}(0)$, because it is seen only by the short baselines, so dividing by $\sqrt{B_{uu}(0)}$ lets a large scale win on extended emission even though its smoothed peak is lower. Implementations also multiply the score by a bias factor per scale, a tuned choice that usually favors small scales; the code accepts one.

## Example

Take $n = 32$ in 1D. The sky is a Gaussian of standard deviation 2 pixels and total flux 4 centered at pixel 10, plus a point of flux 1 at pixel 24. The array measures the frequencies $0, \pm1, \pm2, \pm3, \pm5, \pm7, \pm10$. The scales have radii $0$ (the point), $3$ and $6$ pixels, with $B_{uu}(0) = 1$, $0.4549$ and $0.2487$. At the start the smoothed peaks are $2.0085$, $1.5646$ and $1.1106$, and the scores $|I_u(p)| / \sqrt{B_{uu}(0)}$ are $2.0085$, $2.3198$ and $2.2271$. So the first step takes the radius-3 blob, although the point scale has the highest peak. With $g = 0.3$ and $Q(0) = 6.3975$:

| step | scale radius | pixel | $I_u(p)$ | flux $c$ | $Q$ after |
|---|---|---|---|---|---|
| 1 | 3 | 10 | 1.5646 | 1.0318 | 3.6530 |
| 2 | 3 | 10 | 1.0952 | 0.7223 | 2.3082 |
| 3 | 6 | 10 | 0.5838 | 0.7044 | 1.6091 |
| 4 | 0 | 24 | 0.9599 | 0.2880 | 1.1391 |
| 5 | 3 | 11 | 0.5543 | 0.3656 | 0.7946 |
| 6 | 0 | 24 | 0.6435 | 0.1930 | 0.5834 |

The blobs take the extended source and the points take the point source. To bring $\max_q |R_q|$ below 1% of the peak of the dirty image, Hogbom CLEAN with the same gain needs 65 components, and its largest error against the true sky is $0.482$. Multiscale CLEAN needs 35 components (18 points, 10 blobs of radius 3 and 7 of radius 6), and its largest error is $0.146$. Both fit the data equally well; the multiscale model is closer to the sky because its components look more like the sky.

## Correctness

The proof is that of [Hogbom CLEAN](/hogbom-clean/) with a larger dictionary. For a blob $\psi = \phi_u(\cdot - p)$, expanding the square gives the exact identity

$$Q(M + c\,\psi) = Q(M) - 2c\, I_u(p) + c^2 B_{uu}(0),$$

because the inner product of $\psi$ with the residual is $(\phi_u \ast R)(p)$ when $\phi_u$ is symmetric, and $\frac1W \sum_k w_k |\hat\phi_u(k)|^2 = B_{uu}(0)$. With $c = g\, I_u(p) / B_{uu}(0)$ the drop is $(2g - g^2) I_u(p)^2 / B_{uu}(0) > 0$ for $0 < g < 2$. Because the point scale is in the dictionary, the chosen score is at least $\max_q |R_q|$ times a fixed positive constant. The drops have a finite sum, so $\max_q |R_q| \to 0$ and $Q \to 0$: the model comes to fit every measured visibility. As for Hogbom CLEAN, nothing says which of the many models that fit the data it reaches. The full proof is below.

## Complexity

Lines L1 and L2 take $\Theta(s^2 n \log n)$ time with the [FFT](/fast-fourier-transform/) and $\Theta(s^2 n)$ space for the cross beams; by symmetry $B_{ut} = B_{tu}$, so half of them suffice. Each iteration scans $s$ smoothed images and updates them, so it takes $\Theta(sn)$ time, and $K$ iterations take $\Theta(Ksn)$. The number of iterations is what matters: on extended emission, $K$ is much smaller than for Hogbom CLEAN, which pays for the factor $s$.

## Properties

- **The misfit never rises for $0 < g < 2$**, with the exact drop $(2g - g^2) I_u(p)^2 / B_{uu}(0)$.
- **Hogbom CLEAN is the case of one scale.** With only $\phi_0 = \delta$, the algorithm is line for line Hogbom CLEAN.
- **Sparse in a larger dictionary.** The model is a short list of points and blobs. On a mix of compact and smooth emission it is much shorter than a list of points.
- **Nonlinear and not unique.** The choice in line L4 depends on the data and on the set of scales.
- **Flux in large blobs depends on short baselines.** $B_{uu}(0)$ is the weighted power of $\hat\phi_u$ on the measured frequencies. If the shortest baselines are missing, a large blob is barely seen, and the step $c$ in line L6 is large and poorly constrained.

## Variants and improvements

- **Scale bias.** A factor per scale in line L4 that favors small scales. It is a tuned choice, not a derived one.
- **Other scale functions.** Gaussians, tapered parabolas or wavelet atoms (see the [discrete wavelet transform](/discrete-wavelet-transform/)). The proof needs only real, symmetric functions with $B_{uu}(0) > 0$.
- **Inside major cycles.** In practice the loop is the minor cycle of [Cotton-Schwab CLEAN](/cotton-schwab-clean/), with the model subtracted from the visibilities between cycles.
- **Multiscale multifrequency.** Rau and Cornwell (2011) let each component also have a spectrum over a wide band of frequencies.

## When to use it

Use multiscale CLEAN when the field has extended emission: nebulae, galaxies, radio lobes, the disk of a planet. For a field of compact sources, Hogbom or Clark CLEAN is cheaper and gives the same result. Pick the largest scale smaller than the largest structure the array can see, which is set by its shortest baseline.

## Pitfalls

- **Too large a scale.** A blob wider than the array can see has a small $B_{uu}(0)$, and the method puts large, poorly determined flux into it.
- **No point scale.** Without $\phi_0 = \delta$ the residual cannot reach zero at a point source, and the proof fails.
- **Scales that are not symmetric.** The identity uses $\phi(-q) = \phi(q)$; with an asymmetric function the smoothed residual is not the gradient, and the step can raise the misfit.
- **The peak in place of the score.** Choosing the scale by the largest $|I_u(p)|$ alone favors the point scale, because smoothing lowers the peak. In the example the point scale has the highest peak at the start, although a blob gives the larger drop.

## Implementations

## History

CLEAN with point components had trouble with extended sources from the start. Cornwell (2008) gave the multiscale form used in radio astronomy today: smoothed residuals at a few scales, cross-scale beams that keep them exact, and a choice of scale with a bias. Rau and Cornwell (2011) combined it with a spectral model for wide-band data.

## References
