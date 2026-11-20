---
tag: KACAK6
kind: algorithm
slug: iterative-back-projection-super-resolution
name: Iterative back-projection super-resolution
aliases:
- Irani-Peleg super-resolution
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Refine a high resolution estimate by simulating each low resolution frame and back-projecting the differences. With the mirrored PSF as kernel it is Landweber on the stacked frames."
solves: [multiframe-super-resolution]
model: real-ram
complexity:
  vars: {n: the number of high resolution pixels, m: the number of nonzero PSF entries, K: the number of frames, T: the number of iterations}
  time: {worst: Θ(T K n m), average: Θ(T K n m), best: Θ(T K n m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, iterative: true, linear: true, needs_registration: true, needs_early_stopping: true}
history:
  year: 1991
  people: [Michal Irani, Shmuel Peleg]
  note: Irani and Peleg (1991) improved image resolution by simulating the low resolution frames from an estimate and back-projecting the errors. Their 1993 paper extended the method to occlusion and transparency.
prereqs: [multiframe-super-resolution, landweber-iteration, point-spread-function]
see_also: [super-resolution, drizzle, van-cittert-deconvolution, image-registration, spectral-filter-factors, semi-convergence, richardson-lucy-deconvolution, tikhonov-regularization]
sources:
  - paper: doi:10.1016/1049-9652(91)90045-L
    title: "Michal Irani and Shmuel Peleg, Improving resolution by image registration, CVGIP: Graphical Models and Image Processing 53(3), 1991, 231 to 239"
    locator: the iterative back-projection update and the choice of the back projection kernel
  - paper: doi:10.1006/jvci.1993.1030
    title: "Michal Irani and Shmuel Peleg, Motion analysis for image enhancement: resolution, occlusion, and transparency, Journal of Visual Communication and Image Representation 4(4), 1993, 324 to 335"
    locator: "the back-projection method with motion analysis, and its convergence condition on the back projection kernel (general locator)"
  - paper: doi:10.1109/83.650118
    title: "Michael Elad and Arie Feuer, Restoration of a single superresolution image from several blurred, noisy, and undersampled measured images, IEEE Transactions on Image Processing 6(12), 1997, 1646 to 1658"
    locator: "the model with warp, blur and decimation for each frame, and the maximum likelihood, MAP and POCS solutions"
  - paper: doi:10.1109/TIP.2004.834669
    title: "Sina Farsiu, M. Dirk Robinson, Michael Elad and Peyman Milanfar, Fast and robust multiframe super resolution, IEEE Transactions on Image Processing 13(10), 2004, 1327 to 1344"
    locator: "the robust L1 data term, shift-and-add for pure translation, and the comparison with earlier methods"
---

Iterative back-projection (IBP) is the method of Irani and Peleg (1991) for [multi-frame super-resolution](/multiframe-super-resolution/). It starts from a guess of the high resolution image. It simulates each low resolution frame from the guess: shift, blur, keep every $L$-th pixel. It compares each simulated frame with the observed frame, spreads the difference back onto the high resolution grid with a back projection kernel, and adds the average of these corrections to the guess. With the mirrored PSF as the kernel, the update is $x \leftarrow x + \omega A^T(y - Ax)$ for the stacked frame operator $A$, which is the [Landweber iteration](/landweber-iteration/) with the step $\omega = \beta/K$. So all the Landweber facts apply: convergence to the minimum norm least squares solution for a small enough step, a monotone error with exact data, and [semi-convergence](/semi-convergence/) with noise. When the subpixel shifts cover every position of the high resolution grid once, the method is a deblurring filter with the factors $1 - (1 - \omega|H_q|^2)^T$, the same as in [Van Cittert deconvolution](/van-cittert-deconvolution/) in its Landweber form. The shifts must be known; in practice they come from [image registration](/image-registration/).

## In plain words

You have several small, blurred photos of the same scene. Each one is taken from a slightly different position, by a fraction of a pixel. You want one large, sharp picture. Start with any large picture, for example a plain gray one. For each small photo, ask what the camera would have recorded if the scene were your large picture: move it, blur it, and take every second or third pixel. Compare this with the real photo. Where they differ, spread the difference back over the large picture, at the right position. Average the corrections from all photos, add them, and repeat. After many rounds, your large picture explains all photos. If the photos are noisy, stop earlier, because late rounds start to copy the noise.

## The problem

The unknown is a high resolution (HR) signal or image $x$ with $n$ pixels on a periodic grid. Frame $k = 1, \ldots, K$ is

$$y_k = D\,B\,W_k\,x + e_k .$$

- $W_k$ is the motion. Here it is an integer shift on the HR grid, $(W_k x)_j = x_{(j + s_k) \bmod n}$, so a shift of one HR pixel is a shift of $1/L$ of a low resolution (LR) pixel. In 2D, $s_k$ is a pair.
- $B$ is the blur: periodic convolution with the PSF $h$, stored with its center at index $0$. Its OTF is $H_q = \sum_j h_j e^{-2\pi i jq/n}$. The PSF includes the optics and the integration over the area of the sensor pixel.
- $D$ is the decimation by the factor $L$: $(Dv)_j = v_{jL}$. A frame has $n/L$ pixels ($n/L^2$ in 2D).
- $e_k$ is noise.

Stack the frames into $y = Ax + e$ with $A = (DBW_1; \ldots; DBW_K)$. The goal is an estimate of $x$. The problem page explains when $x$ is determined by the frames.

## The algorithm

$U = D^T$ puts each LR pixel at its place on the HR grid and fills the rest with zeros. $p$ is the back projection kernel, applied by periodic convolution. The default is the mirrored PSF $p_j = h_{-j}$.

```pseudo id=main
IBP(y_1..y_K, s_1..s_K, h, p, L, beta, T, x0)   ▷ default p = mirror of h, x0 = 0
L1  x ← x0
L2  repeat T times
L3      g ← 0
L4      for k = 1 .. K
L5          r_k ← y_k - D(h * W_k x)                ▷ simulate frame k and compare
L6          g ← g + W_k^T (p * U r_k)               ▷ back-project the residual
L7      x ← x + (beta / K) · g
L8  return x
```

Line L5 is the forward model of one frame. Line L6 zero-fills the residual, convolves it with $p$ and undoes the shift. Line L7 adds the average correction with the step $\beta$. A common start is an average of the frames, interpolated to the HR grid; this changes only the start point.

## Example

Take $n = 8$, $L = 2$, the PSF $h_0 = 2/3$, $h_{\pm 1} = 1/6$, and the true signal $x^\dagger = (0, 0, 6, 0, 0, 0, 0, 0)$. Two frames have the shifts $s = 0$ and $s = 1$. The blurred signal is $(0, 1, 4, 1, 0, 0, 0, 0)$, so the frames are $y_1 = (0, 4, 0, 0)$, its even samples, and $y_2 = (1, 1, 0, 0)$, its odd samples. The shifts $0$ and $1$ cover both residues mod 2, so the frames together see every sample of the blurred signal.

The OTF is $H_q = 2/3 + (1/3)\cos(2\pi q/8)$, which is $1$, $0.9024$, $0.6667$, $0.4310$ and $1/3$ for $q = 0, \ldots, 4$. With $p$ the mirrored PSF and $\beta = 2$, the step is $\omega = 1$, and the error at frequency $q$ is multiplied by $1 - H_q^2$ in each step, at worst by $8/9$. The iterates from $x_0 = 0$:

| $T$ | $x_T$ (rounded) | $\lVert x_T - x^\dagger\rVert$ |
|---|---|---|
| 1 | $(0.1667, 1.3333, 3.0, 1.3333, 0.1667, 0, 0, 0)$ | 3.5512 |
| 2 | $(-0.1296, 1.2593, 3.8981, 1.2593, -0.1296, -0.0741, -0.0093, -0.0741)$ | 2.7630 |
| 5 | $(-0.3368, 0.7956, 4.9671, 0.7956, -0.3368, 0.0368, 0.0417, 0.0368)$ | 1.6013 |
| 10 | $(-0.2268, 0.3669, 5.5726, 0.3669, -0.2268, 0.0950, -0.0430, 0.0950)$ | 0.7580 |
| 20 | $(-0.0711, 0.0885, 5.9042, 0.0885, -0.0711, 0.0537, -0.0465, 0.0537)$ | 0.2071 |
| 50 | $(-0.0021, 0.0021, 5.9979, 0.0021, -0.0021, 0.0020, -0.0020, 0.0020)$ | 0.0059 |

The error falls in every step, and after 100 steps it is below $10^{-4}$. The first iterate is $x_1 = \omega B^T z$, where $z = (0, 1, 4, 1, 0, 0, 0, 0)$ is the interlaced data. With only the first frame ($s = 0$), the odd samples are never observed. The same iteration then converges, after 2000 steps, to $(-0.3, 1.2667, 5.3667, 1.2667, -0.3, -0.0667, 0.0333, -0.0667)$, which fits the one frame exactly but has the error $1.9494$: more iterations cannot replace a missing shift.

## Correctness

The full proof is in `proofs/correctness.md`. The main facts:

1. **Landweber form (theorem).** With $p$ the mirrored PSF, $W_k^T P U = (DBW_k)^T$, so the update is $x \leftarrow x + \omega A^T(y - Ax)$ with $\omega = \beta/K$. For $0 < \omega < 2/\lVert A\rVert^2$ and $x_0 = 0$ the iterates converge to the minimum norm least squares solution $A^{+}y$. With exact data the error never grows.
2. **Complete set of shifts (theorem).** If the shifts take each residue mod $L$ exactly once (each pair of residues in 2D), then $\sum_k W_k^T U D W_k = I$, so $A^TA = B^TB$. The iterate is then the [spectral filter](/spectral-filter-factors/) $\hat x_{T,q} = (1 - (1 - \omega|H_q|^2)^T)\,\hat z_q/H_q$ of the interlaced data $z = \sum_k W_k^T U y_k$: the Landweber factor with $\sigma = |H_q|$.
3. **The kernel condition (theorem, for a complete set of shifts).** For any kernel $p$, the error at frequency $q$ is multiplied by $1 - \omega P_q H_q$ in each step. The method converges for every $x^\dagger$ if and only if $|1 - \omega P_q H_q| < 1$ at every $q$. This is the frequency form of the condition on the back projection kernel that Irani and Peleg give. It fails for $p = \delta$ and a PSF whose OTF is negative somewhere: for the box of width 5 on 16 points, $H_4 = -1/5$ and the error grows by $1.2$ per step with $\omega = 1$.
4. **Identifiability (theorem).** If a residue mod $L$ is missing, $A$ has a null space and no method recovers $x$ from the frames alone. If every residue is present and $H_q \ne 0$ for all $q$, $A$ is injective.

## Complexity

In the real-RAM model, one iteration costs, for each frame, one shift ($\Theta(n)$), one direct periodic convolution with $m$ nonzero PSF entries ($\Theta(nm)$), the decimation, the zero fill, one convolution with $p$ (also $m$ entries for the mirrored PSF) and one shift. So one iteration costs $\Theta(Knm)$, and $T$ iterations cost $\Theta(TKnm)$. With the [FFT](/fast-fourier-transform/) each convolution costs $\Theta(n \log n)$ for $n$ a power of two. The extra space is $\Theta(n)$ for $x$ and $g$, plus one frame for the residual.

The number of iterations follows the Landweber rules. With exact data and a complete set of shifts, the error at frequency $q$ falls like $|1 - \omega|H_q|^2|^T$, so a relative error $\varepsilon$ at that frequency takes about $\log(1/\varepsilon)/(\omega|H_q|^2)$ steps for small $|H_q|$. With noise of level $\delta$, $T$ is the regularization parameter; the [discrepancy principle](/morozov-discrepancy-principle/) chooses it when $\delta$ is known.

## Properties

- Linear in the data for fixed shifts and a fixed $p$. The method has no noise model and does not keep the estimate nonnegative; the example has negative entries.
- With the mirrored PSF it is a gradient method for $\frac12\sum_k\lVert y_k - DBW_kx\rVert^2$, so each step does not increase this sum for $0 < \omega \le 2/\lVert A\rVert^2$.
- The components of $x$ in the null space of $A$ stay at their values in $x_0$. With $x_0 = 0$ they stay $0$.
- The result depends on the registration. A wrong shift puts the residual of a frame at the wrong place, and the iteration then fits an inconsistent model.

## Variants and improvements

- **Other back projection kernels.** Irani and Peleg allow a kernel $p$ different from the PSF; a sharper $p$ speeds up the high frequencies but must keep $|1 - \omega P_q H_q| < 1$. Only the mirrored PSF makes the method a gradient method for general shifts.
- **Regularized forms.** Add $-\omega\lambda\, x$ or the gradient of a smoothness term to the step. This is gradient descent on the [Tikhonov](/tikhonov-regularization/) or a total variation objective, and the iteration then needs no early stopping. Elad and Feuer (1997) put the multiframe problem in the maximum likelihood, MAP and projection onto convex sets frameworks.
- **Robust data term.** Farsiu, Robinson, Elad and Milanfar (2004) replace the squared residual by its L1 norm. For pure translation the L1 fit of the stacked frames is a pixelwise median on the HR grid (robust shift-and-add), and the L2 fit is the pixelwise mean, followed by deblurring. This makes the method robust to outliers and registration errors.
- **Faster solvers.** The same least squares problem can be solved by [CGLS](/cgls/) on the stacked operator, which needs far fewer iterations than Landweber.
- **Projection onto constraints.** Clip $x$ to $[0, x_{\max}]$ after each step, which is projected Landweber.

## When to use it

Use IBP when you have several registered frames of a static scene with subpixel shifts, a known PSF and moderate noise, and you want a simple method that is easy to check. It is a good baseline and a teaching example of the forward model $DBW_k$. For pure translations and many frames, shift-and-add followed by deblurring is cheaper and gives the same least squares answer. For astronomical data with flux to keep and bad pixels, use [drizzle](/drizzle/). For noisy data use a regularized form, and for few iterations use CGLS.

## Pitfalls

- **Missing shifts.** Frames whose shifts are equal mod $L$ add no new samples. A shift by a whole LR pixel is useless for resolution.
- **Wrong registration.** Errors of a fraction of an HR pixel blur the result, and outliers in the motion estimate create ghosts. Register on the frames with a method that reaches subpixel accuracy.
- **A kernel that breaks the condition.** With $p = \delta$ the method is the Van Cittert iteration on the HR grid and diverges where the OTF is negative, as for a box pixel integration with a large fill factor.
- **Too large a step.** $\omega$ above $2/\lVert A\rVert^2$ makes the iteration diverge. With $h \ge 0$ and $\sum h = 1$ and a complete set of shifts, $\lVert A\rVert = 1$, so any $0 < \beta/K < 2$ works.
- **Semi-convergence.** With noise, the error first falls and then rises. Without a known noise level, any stopping rule is a heuristic.
- **Boundaries.** Real frames are not periodic. The periodic model gives ringing at the border unless you pad the HR grid.

## Implementations

## History

Irani and Peleg (1991) built an HR image from several LR frames of a scene. They first registered the frames, then improved the estimate by iterative back-projection of the simulation errors. The name recalls the back projection of computed tomography. Their 1993 paper combined it with motion analysis to handle occlusion and transparency. Elad and Feuer (1997) wrote the general model with warp, blur and decimation in matrix form and solved it by maximum likelihood, MAP and projection onto convex sets, which showed that IBP is one member of a family of least squares methods. Farsiu, Robinson, Elad and Milanfar (2004) made the method robust with an L1 data term.

## References
