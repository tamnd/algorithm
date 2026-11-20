---
tag: 6HDCHG
kind: definition
slug: total-generalized-variation
name: Total generalized variation
aliases:
- TGV
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: A regularizer that balances first and higher order derivatives through an auxiliary field, which keeps edges like total variation without its staircasing.
prereqs: [total-variation-denoising, variational-regularization, convex-conjugate]
see_also: [chambolle-pock-algorithm, analysis-and-synthesis-sparsity, image-denoising, sobolev-space, finite-difference-method, proximal-operator]
sources:
  - paper: doi:10.1137/090769521
    title: Kristian Bredies, Karl Kunisch and Thomas Pock, Total generalized variation, SIAM Journal on Imaging Sciences 3(3), 2010
    locator: pages 492 to 526 (the definition of TGV of order k, its kernel and convexity, the second order case and its discrete denoising model)
  - paper: doi:10.1007/s002110050258
    title: Antonin Chambolle and Pierre-Louis Lions, Image recovery via total variation minimization and related problems, Numerische Mathematik 76(2), 1997
    locator: pages 167 to 188 (the infimal convolution of first and second order total variation)
  - paper: doi:10.1002/mrm.22595
    title: Florian Knoll, Kristian Bredies, Thomas Pock and Rudolf Stollberger, Second order total generalized variation (TGV) for MRI, Magnetic Resonance in Medicine 65(2), 2011
    locator: pages 480 to 491 (TGV of order 2 as the regularizer for undersampled MRI)
  - paper: doi:10.1017/S096249291600009X
    title: Antonin Chambolle and Thomas Pock, An introduction to continuous optimization for imaging, Acta Numerica 25, 2016
    locator: pages 161 to 319 (the discrete TGV model and its primal-dual solution)
---

Total generalized variation (TGV) is a convex regularizer of Bredies, Kunisch and Pock (2010) that measures an image by its first derivative minus an auxiliary vector field and by the symmetrized derivative of that field. Of second order it is $\mathrm{TGV}^2_\alpha(u) = \min_w \alpha_1\|\nabla u - w\|_1 + \alpha_0\|\mathcal{E}w\|_1$. It is 0 on affine images, so smooth ramps cost little and do not turn into steps, while a jump still costs $\alpha_1$ times its height as in [total variation](/total-variation-denoising/).

## Definition

Let $\Omega \subset \mathbb{R}^d$ be a bounded domain, $u \in L^1(\Omega)$, $k \ge 1$ and weights $\alpha = (\alpha_0, \dots, \alpha_{k-1})$ with all $\alpha_l > 0$. Let $\mathrm{Sym}^k(\mathbb{R}^d)$ be the space of symmetric tensors of order $k$. The **total generalized variation of order $k$** is

$$\mathrm{TGV}^k_\alpha(u) = \sup\Big\{\int_\Omega u\,\operatorname{div}^k v\,dx \;:\; v \in C_c^k(\Omega, \mathrm{Sym}^k(\mathbb{R}^d)),\ \|\operatorname{div}^l v\|_\infty \le \alpha_l \text{ for } l = 0, \dots, k - 1\Big\}.$$

For $k = 1$ this is $\alpha_0\,\mathrm{TV}(u)$. For $k = 2$ the test fields $v$ are symmetric matrix fields with $\|v\|_\infty \le \alpha_0$ and $\|\operatorname{div} v\|_\infty \le \alpha_1$, and the supremum is equal to the **minimum form**

$$\mathrm{TGV}^2_\alpha(u) = \min_{w} \ \alpha_1\|Du - w\|_{\mathcal{M}} + \alpha_0\|\mathcal{E}w\|_{\mathcal{M}},$$

where $w$ is a vector field of bounded deformation, $\mathcal{E}w = \tfrac12(\nabla w + \nabla w^\top)$ is its symmetrized derivative, and $\|\cdot\|_{\mathcal{M}}$ is the total variation norm of a measure.

**Discrete form.** For an image $u \in \mathbb{R}^{n_1 \times n_2}$, let $\nabla u$ be the field of forward differences, one vector of $\mathbb{R}^2$ per pixel. For a field $w$ of the same shape, let $\mathcal{E}w$ have, per pixel, the symmetric matrix

$$\begin{pmatrix} \partial_1 w_1 & \tfrac12(\partial_2 w_1 + \partial_1 w_2) \\ \tfrac12(\partial_2 w_1 + \partial_1 w_2) & \partial_2 w_2 \end{pmatrix}$$

with finite differences $\partial_i$. Then

$$\mathrm{TGV}^2_\alpha(u) = \min_{w} \ \alpha_1\sum_{\text{pixels}}|(\nabla u - w)_{ij}| + \alpha_0\sum_{\text{pixels}}|(\mathcal{E}w)_{ij}|_F,$$

with the Euclidean length of a vector and the Frobenius norm $|M|_F = \sqrt{m_{11}^2 + 2m_{12}^2 + m_{22}^2}$ of a symmetric matrix. Both terms are isotropic in each pixel. The minimum over $w$ is part of the reconstruction problem, so a TGV model has the unknowns $(u, w)$ and is solved by a primal-dual method such as the [Chambolle-Pock algorithm](/chambolle-pock-algorithm/).

**Basic properties** (Bredies, Kunisch and Pock 2010). $\mathrm{TGV}^k_\alpha$ is a supremum of linear functionals, so it is convex and lower semicontinuous on $L^1(\Omega)$. It is a seminorm, and it is invariant under rotations and translations of the domain. Its kernel is the set of polynomials of degree less than $k$: $\mathrm{TGV}^2_\alpha(u) = 0$ exactly when $u$ is affine.

**Two bounds.** Taking $w = 0$ gives $\mathrm{TGV}^2_\alpha(u) \le \alpha_1\mathrm{TV}(u)$. For the infimal convolution $\mathrm{ICTV}(u) = \min_{u_1 + u_2 = u}\alpha_1\mathrm{TV}(u_1) + \alpha_0\mathrm{TV}(\nabla u_2)$ of Chambolle and Lions (1997), taking $w = \nabla u_2$ gives $\mathrm{TGV}^2_\alpha(u) \le \mathrm{ICTV}(u)$.

## Examples and non-examples

The examples are in one dimension with the discrete form $\min_w \alpha_1\sum_i|(Du)_i - w_i| + \alpha_0\sum_i|w_{i+1} - w_i|$, the forward difference $D$ and $\alpha_1 = 1$. In one dimension this is an $\ell_1$ problem whose minimum is reached with every $w_i$ equal to one of the values $(Du)_j$, so a check of finitely many $w$ gives the value.

| signal $u$ | $Du$ | TV | $\mathrm{TGV}^2_\alpha(u)$ | the best $w$ |
|---|---|---|---|---|
| ramp $(0, 1, 2, 3)$ | $(1, 1, 1)$ | 3 | 0 | $w = Du$ |
| step $(0, 0, 1, 1)$ | $(0, 1, 0)$ | 1 | $\min(\alpha_1, 2\alpha_0)$ | $w = 0$ if $2\alpha_0 \ge \alpha_1$ |
| kink $(0, 1, 2, 2, 2)$ | $(1, 1, 0, 0)$ | 2 | $\min(\alpha_0, 2\alpha_1)$ | $w = Du$ if $\alpha_0 \le 2\alpha_1$ |

- **Ramp.** An affine signal has a constant slope, $w$ follows it at no cost, and TGV is 0. Total variation charges the full rise 3. This is why a TGV denoiser keeps a noisy ramp a ramp, while a total variation denoiser makes it a staircase.
- **Step.** When $2\alpha_0 \ge \alpha_1$, TGV charges a jump $\alpha_1$ times its height, the same as $\alpha_1\mathrm{TV}$. With a smaller $\alpha_0$ the field $w$ can follow the one sample jump as a spike, which is a grid effect. In the continuous setting a jump of height $h$ costs exactly $\alpha_1 h$ for every $\alpha_0$: $Du$ has the point mass $h\delta$, and a field $w$ of bounded deformation has no point mass to cancel it.
- **Kink.** At a change of slope by 1, TGV charges $\alpha_0$ times the change of slope, not the rise. Total variation charges the rise 2. In the continuous setting, with $w$ equal to the slope of each piece, a piecewise affine signal costs at most $\alpha_0$ times the sum of its slope changes plus $\alpha_1$ times the sum of its jumps.
- **Non-example: the sum of two orders.** $\alpha_1\mathrm{TV}(u) + \alpha_0\mathrm{TV}(\nabla u)$ is not TGV. It does not vanish on affine images (the first term does not) and it is infinite at a jump (the second derivative of a step is not a measure). TGV is a minimum over the split $w$, not a sum.
- **Non-example: ICTV.** The infimal convolution splits $u$ itself into a first order and a second order part. It is an upper bound for TGV, and it can be strictly larger, as $w$ in TGV need not be the gradient of a function.
- **Non-example: second order only.** $\mathrm{TV}(\nabla u)$ alone also vanishes on affine images, but it does not allow jumps, so a model with it blurs edges.

## Related definitions

- **Total variation.** $\mathrm{TGV}^1_\alpha = \alpha_0\,\mathrm{TV}$. The [ROF model](/total-variation-denoising/) is the first order case, and [Chambolle's projection algorithm](/chambolle-projection-algorithm/) solves it.
- **Infimal convolution of TV and TV2.** The earlier model of Chambolle and Lions (1997) and an upper bound for TGV of order 2.
- **Higher orders.** $\mathrm{TGV}^k_\alpha$ for $k \ge 3$ is 0 on polynomials of degree less than $k$ and has a minimum form with $k - 1$ auxiliary tensor fields. Order 2 is the most used in imaging.
- **Analysis regularizers.** TGV is an [analysis](/analysis-and-synthesis-sparsity/) type regularizer: it applies $\ell_1$ type norms to operators of $(u, w)$, not to the coefficients of a dictionary.
- **TGV in MRI.** Knoll et al. (2011) use $\mathrm{TGV}^2$ with an undersampled Fourier operator in [variational regularization](/variational-regularization/). The ratio $\alpha_0/\alpha_1$ sets the scale below which a slope change is treated as a jump; its value is chosen for the data.

## References
