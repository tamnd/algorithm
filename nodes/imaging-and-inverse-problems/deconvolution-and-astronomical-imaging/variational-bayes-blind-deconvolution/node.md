---
tag: JZ0W9B
kind: algorithm
slug: variational-bayes-blind-deconvolution
name: Variational Bayes blind deconvolution
aliases:
- Fergus blind deblurring
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: research
summary: "Estimate a blur kernel by variational Bayes with a sparse gradient prior on the image, averaging over the image instead of taking a joint MAP estimate of image and kernel."
solves: [image-deblurring]
model: real-ram
complexity:
  vars: {n: the number of pixels, m: the number of kernel entries, K: the number of passes}
  time: {worst: Θ(K (n³ + 2^m m³)), average: Θ(K (n³ + 2^m m³)), best: Θ(K (n³ + 2^m m³))}
  space: {extra: Θ(n²)}
properties: {deterministic: true, iterative: true, linear: false, nonnegative: true, monotone_free_energy: true, needs_good_start: true}
history:
  year: 2000
  people: [James Miskin, David J. C. MacKay, Rob Fergus, Barun Singh, Aaron Hertzmann, Sam T. Roweis, William T. Freeman, Anat Levin, Yair Weiss, Frédo Durand]
  note: Miskin and MacKay (2000) applied ensemble learning to blind source separation and deconvolution. Fergus and coworkers (2006) made it work on photos by using a prior on image gradients. Levin and coworkers (2009, 2011) explained why averaging over the image avoids the no-blur answer of joint MAP.
prereqs: [image-deblurring, point-spread-function, variational-inference, gaussian-mixture-model]
see_also: [ayers-dainty-blind-deconvolution, expectation-maximization, evidence-lower-bound, maximum-a-posteriori-estimation, marginal-likelihood, total-variation-denoising, richardson-lucy-deconvolution, quadratic-programming]
sources:
  - paper: "James Miskin and David J. C. MacKay, Ensemble learning for blind image separation and deconvolution, in Advances in Independent Component Analysis, Springer, 2000"
    title: Miskin and MacKay 2000
    locator: the chapter (the variational free energy for an unknown image and an unknown kernel)
  - paper: "Rob Fergus, Barun Singh, Aaron Hertzmann, Sam T. Roweis and William T. Freeman, Removing camera shake from a single photograph, ACM Transactions on Graphics 25(3), 2006"
    title: Fergus et al. 2006
    locator: pages 787 to 794 (the mixture prior on gradients, the variational kernel estimate and the coarse to fine scheme)
  - paper: "Anat Levin, Yair Weiss, Frédo Durand and William T. Freeman, Understanding and evaluating blind deconvolution algorithms, IEEE Conference on Computer Vision and Pattern Recognition, 2009"
    title: Levin et al. 2009
    locator: pages 1964 to 1971 (why joint MAP of image and kernel prefers no blur, and why the marginal estimate of the kernel does not)
  - paper: "Anat Levin, Yair Weiss, Frédo Durand and William T. Freeman, Efficient marginal likelihood optimization in blind deconvolution, IEEE Conference on Computer Vision and Pattern Recognition, 2011"
    title: Levin et al. 2011
    locator: the article (the EM form with a Gaussian q for the image and a point estimate of the kernel)
  - paper: "S. Derin Babacan, Rafael Molina and Aggelos K. Katsaggelos, Variational Bayesian blind deconvolution using a total variation prior, IEEE Transactions on Image Processing 18(1), 2009"
    title: Babacan et al. 2009
    locator: the article (a total variation prior in the same variational frame)
---

Variational Bayes blind deconvolution estimates an unknown blur kernel $k$ from one blurred image $y = k \ast x + e$ by averaging over the unknown sharp image $x$ instead of estimating it jointly with $k$. The image gets a sparse prior: most of its gradients are near zero and a few are large. The exact average over the image is not tractable, so the method fits an approximate posterior $q$ for the image by [variational inference](/variational-inference/), and alternates between three steps: update $q$ for the image gradients, update $q$ for the hidden labels of the prior mixture, and set the kernel to the value that fits the data best on average under $q$. Each step increases a lower bound on the log [evidence](/marginal-likelihood/) of the kernel, the [ELBO](/evidence-lower-bound/), so the bound never falls. The point of the averaging is to avoid a failure of the joint [MAP](/maximum-a-posteriori-estimation/) estimate: with a sparse prior, the pair "sharp image equal to the data, no blur" often scores better than the true pair. Miskin and MacKay proposed the variational approach in 2000, and Fergus and coworkers made it work on real photos with camera shake in 2006. After the kernel is found, a non-blind method, such as [Richardson-Lucy](/richardson-lucy-deconvolution/), recovers the image.

## In plain words

A blurred photo can be explained in many ways: a sharp scene behind a wide blur, or a soft scene behind no blur at all. If you ask "which single scene and single blur are most likely together", the soft scene with no blur often wins, because blurring makes an image look smoother, and a prior that likes smooth images is happy with that. The variational method asks a different question: "which blur makes this photo most likely, when we average over all scenes that could be behind it". A blur that is too small needs scenes that are already soft, and few such scenes are typical, so the average penalizes it. The method keeps a cloud of plausible scenes and uses its spread when it picks the blur. Without the spread it is a joint fit again, and it can fall back to "no blur".

## The problem

The grid is periodic with $n$ pixels and the method works on the gradient of the data. If $y = k \ast x + e$, then $d = \nabla y = k \ast g + \nabla e$ with $g = \nabla x$, because a convolution commutes with a difference. In the code $\nabla$ is the forward difference on one dimension; on an image the same steps run on the two gradient images. The model is

- $d = Kg + \varepsilon$, with $K$ the circulant matrix of $k$ and $\varepsilon \sim N(0, \sigma^2 I)$;
- each $g_i$ has a hidden label $z_i$ with $P(z_i = j) = \pi_j$, and $g_i \mid z_i = j \sim N(0, v_j)$: a [Gaussian mixture](/gaussian-mixture-model/) with zero means, one narrow component for the flat regions and one wide component for the edges;
- the kernel lies in $\mathcal K$: $k \ge 0$, $k = 0$ outside a known support $T$ of $m$ entries, and $\sum k = 1$.

The goal is the kernel with the largest evidence $p(d \mid k) = \int p(d \mid g, k)\, p(g)\, dg$. This is the marginal estimate. The joint MAP estimate instead minimizes $D(Kg, d) + \lambda R(g)$ over $g$ and $k$ together, with a data term $D$ and a sparse penalty $R$.

## The algorithm

The approximate posterior is $q(g)\,q(z)$, and the free energy is $\mathcal F(q, k) = \mathbb E_q[\log p(d, g, z \mid k)] + H[q] = \log p(d \mid k) - \mathrm{KL}(q \,\Vert\, p(g, z \mid d, k))$. The method maximizes $\mathcal F$ by coordinate ascent over $q(g)$, $q(z)$ and $k$.

```pseudo id=main
VB-BLIND(d, k0, T, π, v, σ², K)
L1  k ← k0, zero outside T
L2  w_i ← Σ_j π_j / v_j for every pixel i            ▷ prior precision of g_i
L3  repeat K times
L4      S ← (KᵀK/σ² + diag(w))⁻¹; μ ← S Kᵀ d / σ²     ▷ q(g) = N(μ, S)
L5      r_ij ∝ π_j v_j^(-1/2) exp(-(μ_i² + S_ii)/(2 v_j)); w_i ← Σ_j r_ij / v_j   ▷ q(z)
L6      A, b ← the expected misfit E_q ||d - K g||² as k_Tᵀ A k_T - 2 bᵀ k_T + const
L7      k ← argmin of k_Tᵀ A k_T - 2 bᵀ k_T over k_T ≥ 0, Σ k_T = 1
L8  return k, μ, S
```

In line L6, $A_{st} = \sum_r (\mu_{r-s}\mu_{r-t} + S_{r-s,\,r-t})$ and $b_s = \sum_r d_r \mu_{r-s}$ for $s, t \in T$. The term with $S$ comes from the spread of $q(g)$. Line L7 is a convex [quadratic program](/quadratic-programming/) on the simplex. The code solves it exactly by trying each face of the simplex: on each set of positive entries it solves the KKT system with the sum constraint, keeps the solutions that are feasible, and returns the best one. This costs $2^m$ small solves and is only for small kernels. The "naive" option of the code drops $S$ in lines L5 and L6, which turns the method into an alternating joint fit of $g$ and $k$ with a reweighted quadratic penalty, in the style of [iteratively reweighted least squares](/iteratively-reweighted-least-squares/).

This is the form of Levin and coworkers (2011): a Gaussian $q$ for the image, the labels as in [expectation maximization](/expectation-maximization/), and a point estimate of the kernel. Fergus and coworkers (2006), following Miskin and MacKay, put a prior on the kernel as well and used a fully factorized $q$, with a diagonal covariance, for both. The code keeps the full covariance $S$, which is exact for the step of line L4 but costs $\Theta(n^3)$.

## Example

**Joint MAP prefers no blur, exactly.** Take the bar $x = (0, 0, 1, 0, 0)$ on a periodic grid of 5 pixels. Its forward difference is $(0, 1, -1, 0, 0)$, with $\ell_1$ norm $2$. Blur it with $k_0 = k_1 = 0.5$: $k \ast x = (0, 0, 0.5, 0.5, 0)$, whose difference is $(0, 0.5, 0, -0.5, 0)$, with $\ell_1$ norm $1$. With the Laplace prior $R(g) = \lVert g\rVert_1$ and no noise, the true pair costs $\lambda \cdot 2$ and the pair "the gradient is the data, the kernel is $\delta$" costs $\lambda \cdot 1$. So joint MAP picks no blur, by a factor of 2. This is a special case of $\lVert k \ast g\rVert_1 \le \lVert g\rVert_1$ for every kernel in $\mathcal K$ (a theorem, Claim 7 of the proof).

**A measured run.** On a periodic signal of $n = 24$ samples with 4 random steps of random heights in $[0, 2)$, blurred by the kernel $(0.1, 0.3, 0.35, 0.15, 0.1)$ on the offsets $-2$ to $2$, plus Gaussian noise of standard deviation $0.01$, both versions run 50 passes from the flat kernel $0.2$, with $\pi = (0.9, 0.1)$, $v = (10^{-3}, 1)$ and $\sigma^2 = 2 \cdot 10^{-4}$. The table gives the relative error $\lVert \hat k - k\rVert/\lVert k\rVert$. These are measurements, with the generator of the tests.

| seed | variational (with $S$) | naive (without $S$) |
|---|---|---|
| 1 | 0.062 | 0.714 |
| 2 | 0.536 | 0.58 |
| 3 | 0.287 | 0.307 |
| 4 | 0.571 | 0.698 |
| 5 | 0.098 | 1.475 |
| 6 | 0.424 | 0.536 |

The delta kernel has the error 1.475, so on seed 5 the naive estimate ends exactly at "no blur". On seed 1 the variational kernel is $(0.095, 0.278, 0.372, 0.149, 0.106)$. The variational estimate is better on all six seeds, but on seeds 2, 4 and 6 it is still far from the truth: 24 samples with 4 edges hold little information about a kernel of 5 entries. On signals of 36 samples with 5 steps and 30 passes it was better on 5 of 6 seeds. The free energy did not decrease in any run, as the theory says.

## Correctness

The full proof is in the proofs file. Lines L4 and L5 are the exact maximizers of $\mathcal F$ over $q(g)$ and $q(z)$ (Claims 1 and 2). The expected misfit in line L6 is a convex quadratic in the kernel (Claim 3), and the face enumeration of line L7 finds its exact minimizer on the simplex (Claim 4). So each line is an exact coordinate ascent step, $\mathcal F$ never decreases, and it is bounded above by the largest log evidence, so the values converge (Claim 5). With one mixture component the bound is tight, $\mathcal F = \log p(d \mid k)$ (Claim 6). Joint MAP with a Laplace prior prefers $(d, \delta)$ to the true pair on noise-free data (Claim 7). When $S = cI$ the covariance term is $c\,n\lVert k\rVert^2$, which is largest at the delta kernels (Claim 8). The proof does not show that the kernel converges, or that it converges to the kernel of largest evidence: $\mathcal F$ is not concave in $(q, k)$ jointly, and the bound is not tight for a mixture prior. That the covariance term keeps the estimate away from $\delta$ in general is a heuristic, supported by the measurements above.

## Complexity

Line L4 factors a dense $n \times n$ matrix, $\Theta(n^3)$. Lines L5 and L6 cost $\Theta(n)$ and $\Theta(n m^2)$ with the covariance entries that line L6 needs. Line L7 tries $2^m - 1$ faces with a solve of size up to $m + 1$, $\Theta(2^m m^3)$. So $K$ passes cost $\Theta(K(n^3 + 2^m m^3))$, and the dense covariance needs $\Theta(n^2)$ space. This is for small tests only. Practical codes keep only the diagonal of $S$, compute $\mu$ by conjugate gradients with FFT products in $\Theta(n \log n)$ per product, solve the kernel step with a projected or active set QP solver in time polynomial in $m$, and work from coarse to fine scales of the image.

## Properties

- The free energy never decreases along the steps (theorem). The kernel sequence has no proved limit.
- The kernel is nonnegative, zero outside its support and of sum 1 after every pass.
- The estimate depends on the start kernel, on the prior $(\pi, v)$, on $\sigma^2$ and on the support.
- Without the covariance term the method is a joint fit, and it can end at the delta kernel (measured on seed 5).
- It estimates only the kernel. The image comes from a separate non-blind step.

## Variants and improvements

- **Fully factorized ensemble learning.** Miskin and MacKay (2000) and Fergus and coworkers (2006) use a $q$ that factors over all pixels and kernel entries, with priors on both, and a coarse to fine scheme over image scales.
- **EM with a point kernel.** Levin and coworkers (2011) keep $q(g)$ Gaussian and estimate $k$ as a point, as here, and approximate $S$ by its diagonal. They report that this is simpler than the fully factorized method and gives results of similar quality.
- **Other sparse priors.** A [total variation](/total-variation-denoising/) prior in a variational frame (Babacan and coworkers, 2009), Student t priors, and priors learned from natural images.
- **Joint MAP with tricks.** Methods that alternate sharp image and kernel estimates can still work if they add edge prediction, shock filters or a careful schedule of the weight $\lambda$. Levin and coworkers (2009) discuss why these tricks are needed.
- **Laplace and other approximations.** The [Laplace approximation](/laplace-approximation/) and [empirical Bayes](/empirical-bayes/) give other ways to approximate the evidence of the kernel.

## When to use it

Use it to estimate a camera shake or defocus kernel from one photo when no calibration is available and the scene has some strong edges. Estimate the kernel on a region with edges, then deblur the full image with a non-blind method. Do not use it when the kernel varies across the image, when the image has few edges, or when the noise is strong; and do not use the dense form of this page on images of more than a few hundred pixels. When a star or a calibration target is in the field, measure the PSF there instead.

## Pitfalls

- Dropping the covariance term, even by accident through a diagonal approximation that is too crude, can send the estimate to the delta kernel.
- The support $T$ must contain the true kernel. A support that is too large makes the problem worse posed, so practical codes start small at a coarse scale and grow it.
- The gradient of white noise is not white; the model treats it as white. This is a modelling simplification, and $\sigma^2$ is a tuning value rather than a known noise level.
- The kernel is found only up to a shift, together with an opposite shift of the image; compare kernels after centering them.
- The free energy rises, but a rising bound does not mean a better kernel. The measured runs on seeds 2, 4 and 6 end far from the truth with a monotone bound.
- The face enumeration of the code grows as $2^m$; use a real QP solver for larger kernels.

## Implementations

## History

Blind deconvolution by alternating fits of image and kernel goes back to the 1980s, with methods such as [Ayers-Dainty](/ayers-dainty-blind-deconvolution/), which have no noise model and no prior. In 2000 Miskin and MacKay applied ensemble learning, a form of variational Bayes, to blind separation and deconvolution of images. In 2006 Fergus, Singh, Hertzmann, Roweis and Freeman used it with a mixture prior on image gradients and a coarse to fine scheme, and removed camera shake from real photos; this made the approach widely known. Levin, Weiss, Durand and Freeman (2009) analysed why the joint MAP estimate with a sparse prior prefers no blur, while the marginal estimate of the kernel does not, and in 2011 they gave a simpler EM form. Babacan, Molina and Katsaggelos (2009) and others extended the variational frame to other priors.

## References
