---
tag: BVXMK0
kind: algorithm
slug: total-variation-denoising
name: Total variation denoising
aliases:
- ROF model
- Rudin-Osher-Fatemi model
area: graphics-and-signals/image-processing
level: advanced
summary: Denoise by minimizing the convex energy 1/2 |u - f|^2 + λ TV(u), here with Chambolle's dual projection iteration and a duality gap as stop rule.
solves: [image-denoising]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, n: the number of iterations}
  time: {worst: Θ(n W H), average: Θ(n W H), best: Θ(n W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, iterative: true, convex: true, unique_minimizer: true, mean_preserving: true, edge_preserving: true}
history:
  year: 1992
  people: [Leonid I. Rudin, Stanley Osher, Emad Fatemi, Antonin Chambolle]
  note: Rudin, Osher and Fatemi proposed denoising by total variation minimization in 1992; Chambolle gave the dual projection algorithm with a convergence proof in 2004.
prereqs: [image-denoising, convex-function, strong-convexity, fenchel-duality, projected-gradient-descent]
see_also: [proximal-gradient-method, fista, proximal-operator, anisotropic-diffusion, non-local-means, bilateral-filter, richardson-lucy-deconvolution, compressed-sensing]
sources:
  - paper: doi:10.1016/0167-2789(92)90242-F
    title: Leonid I. Rudin, Stanley Osher and Emad Fatemi, Nonlinear total variation based noise removal algorithms, Physica D 60(1-4), 1992
    locator: pages 259 to 268
  - paper: doi:10.1023/B:JMIV.0000011325.36760.1e
    title: Antonin Chambolle, An algorithm for total variation minimization and applications, Journal of Mathematical Imaging and Vision 20(1-2), 2004
    locator: pages 89 to 97; Section 3, The Algorithm, Theorem 3.1 (convergence for τ ≤ 1/8) and the remark on the step 1/4 in practice
  - paper: doi:10.1109/TIP.2009.2028250
    title: Amir Beck and Marc Teboulle, Fast gradient-based algorithms for constrained total variation image denoising and deblurring problems, IEEE Transactions on Image Processing 18(11), 2009
    locator: pages 2419 to 2434 (the fast gradient projection method on the dual)
---

Total variation denoising, also called the ROF model after Rudin, Osher and Fatemi (1992), solves [image denoising](/image-denoising/) by choosing the image $u$ that minimizes

$$E(u) = \tfrac12 \lVert u - f \rVert^2 + \lambda \operatorname{TV}(u),$$

where $f$ is the noisy image, $\operatorname{TV}(u)$ is the sum over the pixels of the length of the discrete gradient, and $\lambda > 0$ sets the strength. The first term keeps $u$ close to the data. The second term penalizes oscillation, but it charges a jump only by its height times its length, not by its square, so edges survive while noise in flat regions is removed. $E$ is [strongly convex](/strong-convexity/), so the minimizer is unique and every local method that converges finds it. This page computes it with Chambolle's algorithm (2004), a [projected gradient](/projected-gradient-descent/) iteration on the dual problem that costs $\Theta(WH)$ per step for a $W \times H$ image; a duality gap gives a certificate of how close the output is. The same model is solved by the [proximal gradient method](/proximal-gradient-method/) and [FISTA](/fista/) on the dual, and by primal-dual and [augmented Lagrangian](/augmented-lagrangian-method/) methods.

## In plain words

Noise makes a picture jitter up and down from pixel to pixel. A blur removes the jitter but also softens every edge. Total variation denoising looks for a picture that stays close to the noisy one but goes up and down as little as possible in total. A sharp edge is one big step, which costs little. A thousand small random steps of noise cost a lot. So the result keeps the edges and makes the regions between them flat, like a cartoon. One number sets the balance: small keeps more detail and more noise, large gives flatter regions and also lowers the contrast of small objects. The method is a careful search that moves step by step toward the single best picture and can tell how far it still is from it.

## The problem

The input is a gray image $f$ of $W \times H$ pixels with real values. The pixel centers are at integer coordinates and one channel is used; color is handled per channel or with a vector form of TV. The values can be linear or gamma encoded; the model treats them as numbers, and the noise model is additive with no particular distribution, though the squared distance is the right choice for Gaussian noise (see [image noise](/image-noise/)).

The discrete gradient uses forward differences with a Neumann border rule: for $x < W - 1$, $(\nabla u)^1(x, y) = u(x+1, y) - u(x, y)$, and $(\nabla u)^1(W-1, y) = 0$; the second component is the same in $y$. The isotropic total variation is

$$\operatorname{TV}(u) = \sum_{x, y} \big|(\nabla u)(x, y)\big| = \sum_{x, y} \sqrt{(\nabla u)^1(x, y)^2 + (\nabla u)^2(x, y)^2}.$$

The divergence $\operatorname{div}$ is defined as minus the adjoint of $\nabla$, so that $\sum \operatorname{div}(p) \cdot u = -\sum p \cdot \nabla u$ for every field $p$ and image $u$. The output is the minimizer $u^\ast$ of $E$, or an approximation $u$ with a bound on $E(u) - E(u^\ast)$.

Rudin, Osher and Fatemi stated the model in a constrained form: minimize TV subject to a known mean and a known variance $\sigma^2$ of the noise, $\sum (u - f) = 0$ and $\sum (u - f)^2 = WH\sigma^2$. The penalized form above is its Lagrangian form; for each $\sigma$ in the useful range there is a $\lambda$ with the same solution, and the penalized form also keeps the mean (see Properties).

## The algorithm

By duality, $\lambda \operatorname{TV}(u) = \max\{\lambda \sum u \cdot \operatorname{div} p : |p(x, y)| \le 1 \text{ at each pixel}\}$, and the minimizer is $u^\ast = f - \lambda \operatorname{div} p^\ast$ where $p^\ast$ minimizes $\lVert \operatorname{div} p - f/\lambda \rVert^2$ over the fields with $|p| \le 1$. Chambolle's iteration is a semi-implicit gradient step on that dual problem:

```pseudo id=main
TV-DENOISE(f, λ, τ, n)                         ▷ λ > 0, 0 < τ ≤ 1/8
L1  p ← 0                                       ▷ two numbers per pixel
L2  repeat n times (or until the duality gap is small)
L3      v ← div p − f / λ
L4      g ← ∇v
L5      at each pixel: p ← (p + τ g) / (1 + τ |g|)
L6  return u = f − λ div p
```

Line L3 is the residual of the dual problem, and line L4 is its gradient up to a factor. Line L5 is the step, with a denominator that keeps $|p| \le 1$ at every pixel: if $|p| \le 1$ then $|p + \tau g| \le 1 + \tau|g|$. Line L6 maps the dual field back to the image.

The dual energy is $D(p) = \frac12(\lVert f \rVert^2 - \lVert f - \lambda \operatorname{div} p \rVert^2)$. For every image $v$ and every field with $|p| \le 1$, $D(p) \le E(v)$. So with $u$ from line L6, the gap $E(u) - D(p)$ is at least $E(u) - E(u^\ast)$, and because $E$ is 1-strongly convex, $\lVert u - u^\ast \rVert^2 \le 2\,(E(u) - D(p))$. The implementation checks the gap every ten steps when a tolerance is given.

## Example

Take a $4 \times 4$ image whose rows are all $(0, 0, 4, 4)$: a step of height 4 down the middle. The solution keeps each half flat. If the left half has value $\delta$ and the right half $4 - \delta$, the fidelity costs $\frac12 \cdot 16 \delta^2$ and the four rows each have one jump of height $4 - 2\delta$, so $E = 8\delta^2 + 4\lambda(4 - 2\delta)$, which is least at $\delta = \lambda/2$ while $\lambda \le 4$. So the rows of $u^\ast$ are:

| $\lambda$ | row of $u^\ast$ | $E(u^\ast)$ |
|---|---|---|
| 0.5 | $(0.25, 0.25, 3.75, 3.75)$ | 7.5 |
| 1 | $(0.5, 0.5, 3.5, 3.5)$ | 14 |
| 2 | $(1, 1, 3, 3)$ | 24 |
| 5 | $(2, 2, 2, 2)$ | 32 |

The edge stays sharp at every $\lambda$; only its height drops, by $\lambda$, which is $\lambda$ times the length of the edge (4) divided by the area of each side (8), counted from both sides. For $\lambda \ge 4$ the image becomes the constant mean 2.

The iteration for $\lambda = 1$ and $\tau = 1/8$: after step 1, line L3 is $v = (0, 0, -4, -4)$ per row, line L4 gives $g^1 = (0, -4, 0, 0)$, and line L5 gives $p^1 = (0, -1/3, 0, 0)$, so line L6 returns the row $(0, 1/3, 11/3, 4)$ with gap 11.56. After 10 steps the row is $(0.350075, 0.607364, 3.392636, 3.649925)$ with gap 1.81; after 100 steps the gap is $6.4 \cdot 10^{-6}$, and after 1000 steps it is at the level of rounding error.

For a noisy case, take a $16 \times 16$ image that is 0 on the left half and 1 on the right half, add Gaussian noise of standard deviation 0.2 from Python's `random.Random(7)`, and run 2000 steps. The mean squared error against the clean image is:

| | noisy | $\lambda = 0.05$ | 0.1 | 0.2 | 0.4 | 0.8 |
|---|---|---|---|---|---|---|
| mean squared error | 0.0409 | 0.01758 | 0.00755 | 0.00277 | 0.00310 | 0.00979 |
| TV of the output | 98.154 | 55.423 | 31.066 | 17.674 | 14.882 | 12.988 |

The clean image has TV 16. The error is least near $\lambda = 0.2$; beyond it the step loses contrast. At 2000 steps the gap is below $10^{-3}$ for $\lambda \le 0.2$ and below 0.01 for the larger values.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows:

- **Adjoint and norm.** The divergence of line L3 is minus the adjoint of the gradient, and $\lVert \operatorname{div} p \rVert^2 \le 8 \lVert p \rVert^2$.
- **Optimality.** If $p$ is a fixed point of line L5 with $|p| \le 1$, then $u = f - \lambda \operatorname{div} p$ satisfies $E(v) \ge E(u) + \frac12 \lVert v - u \rVert^2$ for every $v$, so it is the unique minimizer.
- **Weak duality.** $D(p) \le E(v)$ for every $v$ and every feasible $p$, which makes the gap a valid stopping certificate.
- **Descent and convergence.** For $\tau < 1/8$, the dual residual $\lVert \operatorname{div} p - f/\lambda \rVert^2$ decreases at every step unless $p$ is a fixed point, and the outputs converge to $u^\ast$. Chambolle's Theorem 3.1 extends this to $\tau = 1/8$.

The proof gives no rate. In practice the gap falls fast at first and then slowly.

## Complexity

- Lines L3 and L4 apply a divergence and a gradient: a constant number of operations per pixel, $\Theta(WH)$.
- Line L5 takes one square root and a division per pixel, $\Theta(WH)$.
- Line L6 and a gap check are $\Theta(WH)$.

One step costs $\Theta(WH)$ and $n$ steps $\Theta(nWH)$; the extra space is $\Theta(WH)$ for the two components of $p$ and the temporary images. The number of steps for a gap $\varepsilon$ is not bounded by the theorem. Accelerated dual methods such as the fast gradient projection of Beck and Teboulle (an application of [FISTA](/fista/)) reach a dual accuracy $\varepsilon$ in $O(1/\sqrt{\varepsilon})$ steps, each of the same cost.

## Properties

- **Unique solution.** $E$ is strongly convex, so there is exactly one minimizer, and it depends continuously on $f$: $\lVert u^\ast(f) - u^\ast(f') \rVert \le \lVert f - f' \rVert$.
- **Mean preserving.** $\sum \operatorname{div} p = 0$ for every field, so $\sum u = \sum f$ at every step of line L6.
- **Edge preserving.** A jump of height $h$ along a curve of length $\ell$ costs $\lambda h \ell$, whatever its sharpness, so the model does not prefer to smooth an edge over keeping it.
- **Contrast loss.** Flat regions move toward each other: in the Example the step shrinks by $\lambda$. In the continuous model, a disk of radius $R$ and height $c > 2\lambda/R$ on a zero background comes out as the same disk with height $c - 2\lambda/R$, so small objects lose more contrast and vanish first.
- **Staircasing.** A smooth ramp with noise turns into a staircase of flat steps, because the model favors piecewise constant images.
- **Large λ.** For $\lambda$ large enough the solution is the constant image equal to the mean of $f$.
- **Anisotropy of the grid.** The forward differences make the result depend slightly on the orientation of edges. The anisotropic form $|u_x| + |u_y|$ makes this stronger and favors edges along the axes.

## Variants and improvements

- **Anisotropic TV.** Replace $|\nabla u|$ by $|(\nabla u)^1| + |(\nabla u)^2|$. The dual constraint becomes a box, and the projection a clamp.
- **Faster dual solvers.** The [proximal gradient method](/proximal-gradient-method/) with projection onto the unit disks, and its accelerated form [FISTA](/fista/), give the fast gradient projection method of Beck and Teboulle. Chambolle reports that the step $1/4$ works in practice in place of $1/8$; the projected gradient form with step up to $1/4$ is the one covered by the standard theory.
- **Primal-dual methods.** Alternate a gradient step in $u$ and a projection in $p$; this also handles TV deblurring and inpainting, where the fidelity is $\frac12\lVert Ku - f \rVert^2$ for a linear operator $K$.
- **Split Bregman and ADMM.** Introduce $d = \nabla u$ and solve with the [augmented Lagrangian method](/augmented-lagrangian-method/) or [ADMM](/admm/); each step is a shrinkage and a linear solve.
- **Other fidelities.** The $L^1$ fidelity $\lVert u - f \rVert_1$ (TV-L1) suits salt-and-pepper noise and keeps contrast; a Poisson fidelity suits counts (compare [Richardson-Lucy](/richardson-lucy-deconvolution/)).
- **Higher order.** Total generalized variation and the infimal convolution of first and second order terms reduce staircasing.
- **Exact 1D solvers.** For a single row, the problem is solved exactly in linear time by the taut string method or by dynamic programming on the dual.

## When to use it

Use TV denoising for images that are close to piecewise constant: cartoons, scanned documents, medical images with organs of near constant intensity, depth maps, and as a regularizer inside [deblurring](/image-deblurring/), [inpainting](/image-inpainting/) and [compressed sensing](/compressed-sensing/) reconstruction. It is a good choice when a convex model with a unique answer and a certificate is wanted. Do not use it on textured natural images: it removes fine texture with the noise and gives a flat, painted look. [Non-local means](/non-local-means/) and patch or wavelet methods keep texture better, and a [bilateral filter](/bilateral-filter/) is faster when a rough result is enough.

## Pitfalls

- **Step too large.** With $\tau > 1/8$ the theorem does not apply, and with $\tau$ well above $1/4$ the iteration can oscillate. The implementation rejects $\tau > 1/8$.
- **Inconsistent gradient and divergence.** The divergence must be exactly minus the adjoint of the gradient, including the border terms; otherwise the fixed point is not the minimizer. A test of $\sum \operatorname{div}(p)\, u = -\sum p \cdot \nabla u$ on random data finds this error.
- **λ in the wrong scale.** $\lambda$ has the units of the image values. The same $\lambda$ gives very different results for values in $[0, 1]$ and in $[0, 255]$. Scale $\lambda$ with the noise level.
- **Stopping on a fixed count.** A fixed number of steps can stop far from the minimizer for a large $\lambda$; in the Example, $\lambda = 4$ is a borderline case where the iteration is slow. Stop on the duality gap.
- **Smoothing the TV.** Replacing $|\nabla u|$ by $\sqrt{|\nabla u|^2 + \epsilon^2}$ to use plain gradient descent changes the model and makes the descent step tiny for small $\epsilon$. The dual method needs no smoothing.
- **Expecting contrast to be kept.** The output always has less contrast than the input. If contrast matters, use an $L^1$ fidelity or a debiasing step on the found regions.

## Implementations

## History

Leonid Rudin, Stanley Osher and Emad Fatemi introduced total variation minimization for noise removal in 1992, in the constrained form with the noise variance as a constraint, and solved it by a time-marching gradient projection on the Euler-Lagrange equation. The model became the standard example of edge-preserving variational denoising and of nonsmooth convex optimization in imaging. Chan, Golub and Mulet and others then studied primal-dual formulations. In 2004 Antonin Chambolle gave the simple dual projection algorithm on this page with a proof of convergence for $\tau \le 1/8$. Faster first order methods followed, among them the fast gradient projection of Beck and Teboulle (2009), split Bregman (Goldstein and Osher, 2009) and the primal-dual algorithm of Chambolle and Pock (2011).

## References
