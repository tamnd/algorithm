---
tag: SW8RBX
kind: problem
slug: sparse-view-ct-reconstruction
name: Sparse-view CT reconstruction
aliases:
- few-view tomography
- sparse-view CT
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: "Reconstruct a CT image from far fewer projection angles than the sampling condition asks, which needs a prior such as small total variation."
model: real-ram
prereqs: [tomographic-reconstruction-problem, radon-transform, compressed-sensing]
see_also: [asd-pocs, filtered-back-projection, sart, chambolle-pock-algorithm, limited-angle-tomography, aliasing, learned-primal-dual, total-variation-denoising]
sources:
  - paper: doi:10.1090/S0002-9904-1977-14406-6
    title: K. T. Smith, D. C. Solmon and S. L. Wagner, Practical and mathematical aspects of the problem of reconstructing objects from radiographs, Bulletin of the American Mathematical Society 83(6), 1977
    locator: pp. 1227 to 1270 (finitely many projections do not determine an object)
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Chapter III (sampling conditions for the parallel scanning geometry and resolution)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 5 (aliasing artifacts in CT images, including too few views) and Chapter 7 (algebraic reconstruction)
  - paper: doi:10.1109/TIT.2005.862083
    title: Emmanuel J. Candes, Justin Romberg and Terence Tao, Robust uncertainty principles, exact signal reconstruction from highly incomplete frequency information, IEEE Transactions on Information Theory 52(2), 2006
    locator: exact recovery of a piecewise constant image from incomplete Fourier samples by TV minimization (general locator)
  - paper: doi:10.1088/0031-9155/53/17/021
    title: Emil Y. Sidky and Xiaochuan Pan, Image reconstruction in circular cone-beam computed tomography by constrained, total-variation minimization, Physics in Medicine and Biology 53(17), 2008
    locator: the constrained TV problem for few-view CT and the ASD-POCS algorithm (general locator)
  - paper: doi:10.1088/0031-9155/57/10/3065
    title: Emil Y. Sidky, Jakob H. Jorgensen and Xiaochuan Pan, Convex optimization problem prototyping for image reconstruction in computed tomography with the Chambolle-Pock algorithm, Physics in Medicine and Biology 57(10), 2012
    locator: convergent primal-dual solvers for the constrained and penalized TV problems of CT (general locator)
---

Sparse-view CT reconstruction asks for a CT image from projections at only a few angles, far fewer than the sampling condition of [filtered back-projection](/filtered-back-projection/) needs. The motive is a lower X-ray dose or a faster scan. With few angles, the linear system $A x = y$ has fewer equations than unknowns, so many images fit the data exactly, and the angular gaps alias into streaks in the FBP image. No method can recover a general image from the data alone. Every method adds a prior: nonnegativity, a small total variation, a sparse representation, or a model learned from training images. The best-known approach, minimizing total variation under a data constraint, comes from [compressed sensing](/compressed-sensing/).

## In plain words

A CT scanner sends X-rays through the body from many angles and records how much each ray is weakened. From these records, a computer builds a cross-section image. The usual method needs many angles, about one and a half times the number of detector cells across the body. Each angle costs radiation.

With only a few angles, the records do not pin down the image. Many different images give exactly the same records, and the usual method fills the gaps with straight streaks. To choose one image, the computer must use knowledge about what real images look like. Real cross-sections are made of a few organs or materials, each with a nearly constant value, so a good choice is the image with the fewest and smallest jumps in value that still matches the records.

## Definition

Let $f$ be the unknown attenuation on the unit disk, and $\mathcal{R}f(\theta, s)$ its [Radon transform](/radon-transform/). The data are noisy samples
$$y_{k,j} = \mathcal{R}f(\theta_k, s_j) + e_{k,j}, \qquad k = 0, \dots, a - 1,\quad j = 0, \dots, d - 1,$$
at $a$ angles $\theta_k = k\pi/a$ and $d$ detector bins, with the noise norm $\|e\| \le \delta$. Discretized on an $n \times n$ grid, the model is $y = A x + e$ with a nonnegative system matrix $A$ of size $ad \times n^2$ (from [Siddon's algorithm](/siddon-algorithm/), [Joseph's projector](/joseph-projector/) or the [distance-driven projector](/distance-driven-projector/)). The problem is sparse-view when the number of angles $a$ is far below the sampling condition $a \approx \pi d/2$ of the parallel geometry (Natterer, Chapter III). In practice this means tens of angles instead of hundreds or a thousand.

The output is an image $x$ that fits the data and is close to the true image. The standard formulation with a total variation prior is the convex problem
$$\min_x \operatorname{TV}(x) \quad\text{subject to}\quad \|A x - y\| \le \varepsilon,\quad x \ge 0,$$
with $\varepsilon \approx \delta$, or its penalized form $\min_x \frac{1}{2}\|A x - y\|^2 + \mu \operatorname{TV}(x)$ over $x \ge 0$.

**What the data do not fix.** If $a d < n^2$, the null space of $A$ has dimension at least $n^2 - a d$, and adding any null space vector to a solution gives another solution. This is a statement about the discrete model. In the continuous model it is stronger: Smith, Solmon and Wagner (1977) showed that for any finite set of directions there are nonzero smooth functions with compact support whose projections in all these directions vanish. So finitely many projections never determine a general object.

## Variants

- **Fan-beam and cone-beam geometry.** The same problem with divergent rays. Sidky and Pan studied the circular cone-beam case.
- **Limited angle.** The few angles are not spread over $[0, \pi)$ but bunched in a smaller range. This is a different and harder problem with a missing wedge in Fourier space; see [limited-angle tomography](/limited-angle-tomography/).
- **Interior and truncated data.** Few views combined with a detector that does not cover the object; see [interior tomography](/interior-tomography/).
- **Low dose.** Many angles with high noise per ray instead of few angles. The trade between the number of views and the dose per view is a design question.
- **Discrete objects.** If the object takes only a few known values, the problem becomes [discrete tomography](/discrete-tomography/), which needs even fewer views.

## Examples

**A null space in a 2 by 2 image.** Take the image $x = (x_0, x_1; x_2, x_3)$ and two views, the row sums and the column sums. The matrix has 4 rows and rank 3, and its null space is spanned by the checkerboard $c = (1, -1; -1, 1)$, because each row and each column of $c$ sums to 0. For the true image $x = (2, 0; 0, 0)$, the data are the row sums $(2, 0)$ and the column sums $(2, 0)$, and every image $x + t c = (2 + t, -t; -t, t)$ fits them exactly.

- The minimum-norm solution, which [SIRT](/sirt/) or [ART](/kaczmarz-method/) give from $x_0 = 0$, removes the part of $x$ along $c$: $\langle x, c\rangle / \|c\|^2 = 2/4 = 1/2$, so it is $(3/2, 1/2; 1/2, -1/2)$. It has a negative value, which is impossible for an attenuation.
- Nonnegativity alone fixes the answer here: $2 + t \ge 0$, $-t \ge 0$ and $t \ge 0$ force $t = 0$.
- The anisotropic total variation, the sum of the absolute differences of the four neighbor pairs, is $2|2 + 2t| + 2|2t| = 4(|1 + t| + |t|)$. It is smallest, with the value 4, for all $t \in [-1, 0]$, so TV alone does not decide, but TV together with nonnegativity gives $t = 0$.

**A measured case.** A $16 \times 16$ phantom of three ellipses (values 0 to 1.5), 6 angles with 23 bins each, 138 equations for 256 unknowns, and exact data. ART with positivity reaches the relative error 0.068 after 200 sweeps and stays near 0.067. [ASD-POCS](/asd-pocs/), which adds TV steps, reaches 0.050 after 200 iterations and 0.037 after 400 with one parameter set ($g = 10$, $\alpha = 0.05$). These are measurements of this setup, made with the code of the ASD-POCS page.

## Known algorithms

| Method | Prior | What it gives |
|---|---|---|
| [Filtered back-projection](/filtered-back-projection/) | none | fast and linear; with few views, streaks from angular aliasing (Kak and Slaney, Chapter 5) |
| [ART](/kaczmarz-method/), [SART](/sart/), [SIRT](/sirt/) | the start point, early stopping | a solution near the start in a weighted norm; fewer streaks than FBP, but the null space error stays |
| [ASD-POCS](/asd-pocs/) (Sidky and Pan 2008) | TV and nonnegativity | alternating data and TV steps with adaptive lengths; a heuristic without a convergence proof |
| [Chambolle-Pock algorithm](/chambolle-pock-algorithm/) (Sidky, Jorgensen and Pan 2012) | TV, constrained or penalized | a primal-dual method that converges to a solution of the convex problem |
| [ADMM](/admm/), [split Bregman](/split-bregman-method/) | TV or other sparsity priors | splitting methods for the penalized problem, with convergence proofs |
| [Total generalized variation](/total-generalized-variation/) | piecewise smooth images | less staircasing than TV, at a higher cost |
| [Learned primal-dual](/learned-primal-dual/), [algorithm unrolling](/algorithm-unrolling/) | learned from training data | trained iterations that use the projector and its adjoint; no guarantee outside the training distribution |
| [Plug-and-play priors](/plug-and-play-priors/), [deep image prior](/deep-image-prior/) | a denoiser or a network structure | a prior given by a denoiser or by the bias of a network; convergence only under conditions on the denoiser |

## Bounds

- **Counting (theorem).** With $a d < n^2$ equations, the discrete null space has dimension at least $n^2 - a d$, so no method that uses only the data can recover every image.
- **Finite data in the continuum (theorem).** No finite set of projections determines a general compactly supported function (Smith, Solmon and Wagner 1977). Every positive result needs a restricted class of images.
- **Sampling (theorem with assumptions).** For an image of bandwidth $b$ on the unit disk, the parallel geometry resolves it with about $a \approx \pi d/2$ angles and a detector spacing of about $1/(2b)$ (Natterer, Chapter III). Sparse-view CT lives far below this count.
- **Sparse gradients (theorem for random Fourier samples).** Candes, Romberg and Tao proved ([their theorem](/candes-romberg-tao-theorem/)) that a signal whose gradient has $s$ nonzero entries is recovered exactly by TV minimization from a number of randomly chosen Fourier samples of order $s \log N$, with high probability. CT data on a few angles give Fourier samples on a few radial lines (the [Fourier slice theorem](/fourier-slice-theorem/)), which are not random, so the theorem does not cover CT. Their exact recovery of a phantom from radial lines was a numerical experiment, not a theorem.
- **Heuristic rules.** How many views TV reconstruction needs for a given class of images is known from experiments and from studies of phase transitions, not from a theorem for CT geometry.

## Reductions

- **To a convex program.** The TV problem with $\|A x - y\| \le \varepsilon$ and $x \ge 0$ is a second-order cone program, so interior-point methods solve it for small images, and first-order methods such as Chambolle-Pock for large ones.
- **To compressed sensing.** By the Fourier slice theorem, each view gives the 2D Fourier transform of the image on one line through the origin. With a gridding step, sparse-view CT becomes recovery of an image with a sparse gradient from Fourier samples on radial lines.
- **To sinogram inpainting.** Treat the missing angles as missing rows of the sinogram, fill them by [inpainting](/image-inpainting/) or interpolation, and then run FBP. This uses the structure of sinograms rather than of images.
- **To discrete tomography.** If the image takes only the values 0 and 1, sparse-view CT is [discrete tomography](/discrete-tomography/), where two directions can already be enough in special cases, and three directions make the decision problem NP-complete.

## Applications

- **Low-dose medical CT.** Fewer views lower the dose for screening and for children, at the price of a prior.
- **Fast and gated scans.** In cardiac CT and in perfusion studies, only the views taken during a short time window are usable.
- **Industrial and security CT.** Inspection of parts made of a few materials, where TV and discrete priors fit well and scan time is limited.
- **Electron and X-ray microscopy.** Tilt series with few projections because the sample is damaged by the beam; usually combined with a limited angle range.
- **Tomosynthesis.** Breast and chest tomosynthesis take few views over a limited range, so they combine the sparse-view and limited-angle problems.

## References
